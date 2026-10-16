// Teste ao vivo: a fixture acrescenta eventos (10x) e o painel, aberto, tem de acompanhar.
// Confere: pico de 10 subagentes, sem sinal que aparece sozinho, gaveta e foco que sobrevivem, DOM que não é refeito,
// estado final igual ao que um leitor independente tira dos arquivos. Uso: node vivo.mjs [velocidade]
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { QA, PAINEL, servidor, pronto, navegador, LER_TELA, esp } from './comum.mjs';

const VEL = process.argv[2] || '10';
const pasta = path.join(QA, 'exec-vivo');
const ger = spawn('node', [path.join(PAINEL, 'fixture', 'gerar.mjs'), '--saida', pasta, '--velocidade', VEL], { stdio: ['ignore', 'pipe', 'pipe'] });
let gerLog = ''; ger.stdout.on('data', d => gerLog += d); ger.stderr.on('data', d => gerLog += d);
for (let i = 0; i < 100 && !gerLog.includes('ao vivo'); i++) await esp(100);
const T0 = Date.now();

// ---- leitor independente (não usa leitor.js): tira dos arquivos o que o painel deveria mostrar ----
function oraculo(agoraMs) {
  const dir = path.join(pasta, 'eventos'); const ag = {};
  for (const f of fs.readdirSync(dir)) {
    const id = f.replace('.jsonl', ''); const txt = fs.readFileSync(path.join(dir, f), 'utf8');
    const completas = txt.slice(0, txt.lastIndexOf('\n') + 1).split('\n').filter(Boolean).map(l => { try { return JSON.parse(l) } catch { return null } }).filter(Boolean);
    const subs = new Set(); let atual = null, ultimo = 0, fim = false;
    for (const e of completas) {
      ultimo = Math.max(ultimo, Date.parse(e.t));
      if (e.tipo === 'abriu_subagente') subs.add(e.sub); else if (e.tipo === 'fechou_subagente') subs.delete(e.sub);
      else if (e.tipo === 'pegou_ticket') atual = e.ticket;
      else if (['passou_ticket', 'resolveu_ticket', 'devolveu', 'esperando_gustavo'].includes(e.tipo)) atual = null;
      else if (e.tipo === 'fim') { fim = true; subs.clear(); atual = null }
    }
    ag[id] = { subs: subs.size, atual, ultimo, fim, semSinal: !fim && agoraMs - ultimo > 300000 };
  }
  const tk = {};
  for (const f of fs.readdirSync(path.join(pasta, 'tickets'))) {
    const t = fs.readFileSync(path.join(pasta, 'tickets', f), 'utf8'); const n = f.split('-')[0];
    tk[n] = { status: /Status:\s*(\S+)/.exec(t)[1], com: (/Com:\s*(.*)/.exec(t) || [])[1]?.trim() || '', dep: (/Blocked by:\s*(.*)/.exec(t)[1].match(/\d+/g) || []).map(x => x.padStart(2, '0')) };
  }
  return { ag, tk };
}
function colunas(o) {
  const c = {};
  for (const [n, t] of Object.entries(o.tk)) {
    let col;
    const aberto = t.dep.some(d => !o.tk[d] || o.tk[d].status !== 'resolved');
    if (['ready-for-human', 'needs-info'].includes(t.status)) col = 'esperando';
    else if (t.status === 'resolved') col = 'feito';
    else if (t.status === 'wontfix') col = 'descartado';
    else if (t.status === 'testing' || (t.status === 'claimed' && /^testador/.test(t.com))) col = 'teste';
    else if (t.status === 'review' || (t.status === 'claimed' && /^(revisor|prumo)/.test(t.com))) col = 'revisao';
    else if (t.status === 'claimed') col = 'em_curso';
    else if (['open', 'ready-for-agent', 'needs-triage'].includes(t.status)) col = aberto ? 'bloqueado' : 'a_fazer';
    else col = 'desconhecido';
    c[col] = (c[col] || 0) + 1;
  }
  return c;
}
const idDe = (titulo) => titulo.startsWith('Fable') ? 'fable-1' : titulo.toLowerCase().replace(/ · conduz/, '').replace(/ (\d)/, '-$1');

const s = servidor(pasta, 8772); await pronto('http://127.0.0.1:8772/api/execucao');
const n = await navegador();
const R = { velocidade: VEL, amostras: [], eventos: [] };
try {
  await n.abrir('http://127.0.0.1:8772/', 1280, 800);
  await n.ev(`document.querySelectorAll('.agente').forEach(function(e){e.__qa=1}); document.querySelectorAll('.estacao').forEach(function(e){e.__qa=1}); 1`);
  const historico = []; let pico = 0, picoQuando = null, semSinalVisto = null, gavetaAberta = false, fotoPico = false, focoOk = [];
  const FIM = 340000;
  while (Date.now() - T0 < FIM) {
    const dt = (Date.now() - T0) / 1000;
    const tela = await n.ev(LER_TELA), orac = oraculo(Date.now());
    historico.push({ t: Date.now(), orac }); while (historico.length > 4) historico.shift();
    // subagentes: o painel tem de bater com o oráculo de agora ou com o de até ~8 s atrás (o painel lê a cada 3 s)
    let dif = [];
    for (const c of tela.cartoes) {
      const id = idDe(c.nome), o = orac.ag[id]; if (!o) continue;
      const aceitos = historico.map(h => h.orac.ag[id]?.subs);
      if (!aceitos.includes(c.abertos)) dif.push(`${id}: tela ${c.abertos}, arquivos ${aceitos.join('/')}`);
    }
    const c2 = tela.cartoes.find(c => c.nome === 'Construtor 2');
    if (c2 && c2.abertos > pico) { pico = c2.abertos; picoQuando = dt }
    const ts1 = tela.cartoes.find(c => c.nome === 'Testador 1');
    if (ts1 && ts1.sit === 'sem_sinal' && semSinalVisto == null) semSinalVisto = { dt, texto: ts1.sinal, alerta: tela.alertas.map(a => a.txt).filter(t => /Testador 1/.test(t)) };
    R.amostras.push({ dt: +dt.toFixed(1), leitura: tela.leitura, trab: tela.trab, feitos: tela.feitos, c2: c2 && c2.abertos, ts1: ts1 && ts1.sit, dif, gaveta: tela.gaveta.aberta ? tela.gaveta.titulo : null, ativo: tela.ativo, alertas: tela.alertas.length, w: tela.largura.scrollW });
    // gesto 1: ~20 s, abre a gaveta do Construtor 2 com clique de verdade
    if (!gavetaAberta && dt > 20) {
      const r = await n.ev(`(function(){var c=[].filter.call(document.querySelectorAll('.agente'),function(e){return e.querySelector('.nome>span').textContent==='Construtor 2'})[0].getBoundingClientRect();return {x:c.left+c.width/2,y:c.top+c.height/2}})()`);
      await n.clicar(r.x, r.y); gavetaAberta = true;
      R.gavetaAbriu = (await n.ev(LER_TELA)).gaveta;
    }
    if (!fotoPico && c2 && c2.abertos >= 9) { await n.foto('vivo-pico-1280x800.png'); fotoPico = true; R.fotoPicoEm = dt }
    await esp(2000);
  }
  R.final = await n.ev(LER_TELA);
  R.corpoGaveta = await n.ev(`document.getElementById('g-corpo').innerText.slice(0,400)`);
  R.domPreservado = await n.ev(`({agentes:document.querySelectorAll('.agente').length, comMarca:[].filter.call(document.querySelectorAll('.agente'),function(e){return e.__qa}).length, estacoes:[].filter.call(document.querySelectorAll('.estacao'),function(e){return e.__qa}).length, nos:document.getElementsByTagName('*').length})`);
  await n.foto('vivo-final-1280x800.png');
  R.orFinal = oraculo(Date.now()); R.colunasOraculo = colunas(R.orFinal);
  R.pico = { subagentes: pico, em: picoQuando }; R.semSinalVisto = semSinalVisto;
  R.erros = n.erros; R.geradorLog = gerLog;
} finally { n.fechar(); s.kill(); ger.kill(); }
fs.writeFileSync(path.join(QA, 'vivo.json'), JSON.stringify(R, null, 1));
const difs = R.amostras.filter(a => a.dif.length);
console.log('amostras', R.amostras.length, 'com divergência', difs.length, difs.slice(0, 5).map(a => a.dt + ' ' + a.dif.join('; ')));
console.log('pico c2', R.pico, 'sem sinal t1', JSON.stringify(R.semSinalVisto));
console.log('final feitos', R.final.feitos, R.final.total, 'colunas tela', R.final.estacoes.map(e => e.col + ':' + e.n).join(' '), '| oraculo', JSON.stringify(R.colunasOraculo));
console.log('dom', JSON.stringify(R.domPreservado), 'gaveta', R.gavetaAbriu && R.gavetaAbriu.titulo, '->', R.final.gaveta.titulo, 'erros', R.erros.length);
process.exit(0);
