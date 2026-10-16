// Fixture ao vivo da execução do hub, no formato de painel/contrato.md (formato 1).
// Elenco: 10 agentes (5 construtores, 2 revisores, 2 testadores, 1 integrador) + 2 Prumos + maestro
// + 1 Fable (agente próprio, entra no minuto -30). 25 tickets com bloqueios.
//
//   node gerar.mjs                       passado na hora, resto ao vivo (10x: 6 s reais por minuto)
//   node gerar.mjs --velocidade 1        ao vivo em tempo real
//   node gerar.mjs --so-historia         grava até o minuto 0 e sai (captura e teste)
//   node gerar.mjs --so-historia --ate -40   grava só até o minuto -40 (começo)
//   node gerar.mjs --so-historia --ate 30    grava tudo até +30 (fim; carimbos no futuro)
//   node gerar.mjs --excesso             11o subagente do construtor-2 (borda do limite 10)
//   node gerar.mjs --defeitos            linha ruim, tipo novo, agente fora da lista, ticket estranho, ciclo
//   node gerar.mjs --saida <pasta>       padrão: ./execucao-fake (ao lado do script)
//
// Grava só em --saida (apaga e recria). Nunca aponte para a pasta real da execução.
// Momentos: minuto 0 = agora. Passado leva carimbos de agora-75 min até agora; o ao vivo leva o
// carimbo do instante em que sai. Com --ate > 0 os carimbos ficam no futuro (só para captura).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const opt = (n, d) => { const i = process.argv.indexOf('--' + n); if (i < 0) return d; const v = process.argv[i + 1]; return (v === undefined || v.startsWith('--')) ? true : v; };
const SAIDA = path.resolve(opt('saida', path.join(AQUI, 'execucao-fake')));
const VEL = parseFloat(opt('velocidade', '10'));
const SO_HIST = process.argv.includes('--so-historia');
const ATE = parseFloat(opt('ate', '0'));
const EXCESSO = process.argv.includes('--excesso');
const DEFEITOS = process.argv.includes('--defeitos');

const OPUS = 'claude-opus-5-5', FABLE = 'claude-fable-5-1';
const AGENTES = {};
const ag = (id, papel, titulo, modelo = OPUS, esforco = 'alto', x = {}) => { AGENTES[id] = { id, papel, titulo, modelo, esforco, terminal: titulo, ...x }; };
ag('maestro', 'maestro', 'Maestro');
for (let n = 1; n <= 5; n++) ag(`construtor-${n}`, 'construtor', `Construtor ${n}`);
for (let n = 1; n <= 2; n++) ag(`revisor-${n}`, 'revisor', `Revisor ${n}`);
for (let n = 1; n <= 2; n++) ag(`testador-${n}`, 'testador', `Testador ${n}`);
ag('integrador-1', 'integrador', 'Integrador 1');
for (let n = 1; n <= 2; n++) ag(`prumo-${n}`, 'prumo', `Prumo ${n}`);
ag('fable-1', 'construtor', 'Fable do ticket 14', FABLE, 'medio', { temporario: true, ticket: '14' });

// ---- tickets ----
const T = {};
const tk = (n, titulo, dep = []) => { const k = String(n).padStart(2, '0'); T[k] = { n: k, titulo, dep: dep.map(d => String(d).padStart(2, '0')), status: 'open', dono: 'construtor', com: '' }; };
tk(1, 'Esqueleto do portal e rotas'); tk(2, 'Leitor de arquivos do hub'); tk(3, 'Modelo de dados dos laços');
tk(4, 'Indexador de notas'); tk(5, 'Página de laços, lista', [1]); tk(6, 'Cache do leitor', [2]);
tk(7, 'Esquema de tickets', [3]); tk(8, 'Validador de tickets', [3]); tk(9, 'Detalhe do laço', [5, 6]);
tk(10, 'Importador de tickets', [7]); tk(11, 'Fila de revisão', [7]); tk(12, 'Busca por tema', [9]);
tk(13, 'Exportador de relatório', [10]); tk(14, 'Motor de ligações entre notas', [9, 11]);
tk(15, 'Filtros da busca', [12]); tk(16, 'Histórico de versões', [13]); tk(17, 'Mapa das ligações', [14]);
tk(18, 'Painel de pendências', [15, 16]); tk(19, 'Atalhos de teclado', [17]);
tk(20, 'Segundo par de olhos: aval do Gustavo', [5]); tk(21, 'Notebook de exemplo', [20]);
tk(22, 'Página de saúde do hub', [18, 19, 4]); tk(23, 'Documentação de uso', [22]);
tk(24, 'Pacote de entrega', [21, 23]); tk(25, 'Passagem final', [24]);
tk(26, 'Formato do relatório: falta resposta de quem pediu'); tk(27, 'Ideia solta de integração, sem triagem'); tk(28, 'Revisão rápida do guia de uso');
T['26'].dono = 'integrador'; T['26'].status = 'needs-info';
T['27'].status = 'needs-triage';
T['28'].dono = 'revisor'; T['28'].status = 'claimed'; T['28'].com = 'revisor-1'; // em revisão pela regra do papel, sem Status: review
// Status do arquivo (seção 4). "a fazer" e "bloqueado" saem de open + Blocked by, calculados pelo painel.
const S = { curso: 'claimed', rev: 'review', teste: 'testing', feito: 'resolved', gustavo: 'ready-for-human', aberto: 'open' };

const EV = []; // {m, a, tipo, p, st, parcial}
const ev = (m, a, tipo, p = {}, st = null) => EV.push({ m, a, tipo, p, st });
const SUBS = ['ler arquivo', 'rodar linter', 'escrever teste', 'checar contrato', 'gerar docs', 'comparar versões',
  'procurar uso', 'montar exemplo', 'checar acessibilidade', 'resumir diff'];
const setk = (k, status, com = '') => ({ k, status: S[status], com });

function ciclo(c, k, m0, dur, subs = 3, rev = 'revisor-1', teste = null, devolve = false) {
  ev(m0, c, 'pegou_ticket', { ticket: k }, setk(k, 'curso', c));
  for (let i = 0; i < subs; i++) {
    const s = `${c}-${k}-s${i + 1}`, a = m0 + 0.5 + i * dur * 0.15;
    ev(a, c, 'abriu_subagente', { ticket: k, sub: s, assunto: SUBS[(i + Number(k)) % SUBS.length], modelo: OPUS });
    ev(Math.min(a + dur * 0.25, m0 + dur * 0.8), c, 'fechou_subagente', { ticket: k, sub: s, ok: true });
  }
  ev(m0 + dur * 0.7, c, 'rodou_teste', { ticket: k, ok: true, assunto: `pytest tests/ticket_${k}`, detalhe: '12 passaram' });
  ev(m0 + dur * 0.85, c, 'commit', { ticket: k, ok: true, assunto: `ticket ${k}: ${T[k].titulo.toLowerCase()}` });
  ev(m0 + dur, c, 'passou_ticket', { ticket: k, para: rev }, setk(k, 'rev', rev));
  const r = m0 + dur + 3;
  ev(m0 + dur + 1, rev, 'pegou_ticket', { ticket: k });
  if (devolve) { ev(r, rev, 'devolveu', { ticket: k, detalhe: 'contrato do leitor não cobre arquivo vazio' }, setk(k, 'aberto', '')); return; }
  if (teste) {
    ev(r, rev, 'passou_ticket', { ticket: k, para: teste }, setk(k, 'teste', teste));
    ev(r + 1, teste, 'pegou_ticket', { ticket: k });
    ev(r + 4, teste, 'rodou_teste', { ticket: k, ok: true, assunto: `pytest tests/aceite_${k}`, detalhe: 'aceite passou' });
    ev(r + 4.2, teste, 'resolveu_ticket', { ticket: k }, setk(k, 'feito', ''));
  } else ev(r, rev, 'resolveu_ticket', { ticket: k }, setk(k, 'feito', ''));
}
const msg = (m, de, para, assunto, recebe = false) => {
  ev(m, de, 'mandou_mensagem', { para, assunto });
  if (recebe) ev(m + 0.1, para, 'recebeu_mensagem', { de, assunto });
};

for (const a of Object.keys(AGENTES)) if (a !== 'fable-1') ev(-75, a, 'inicio', { modelo: AGENTES[a].modelo });
// construtor-1
ciclo('construtor-1', '01', -74, 8, 2);
ciclo('construtor-1', '05', -62, 9, 3, 'revisor-2');
ciclo('construtor-1', '09', -50, 12, 4, 'revisor-1', 'testador-1');
ciclo('construtor-1', '12', -34, 14, 4, 'revisor-1', 'testador-2');
// construtor-2
ciclo('construtor-2', '02', -74, 7, 2);
ciclo('construtor-2', '06', -63, 9, 3, 'revisor-2');
ciclo('construtor-2', '10', -50, 11, 3);
ciclo('construtor-2', '13', -36, 10, 3, 'revisor-1', 'testador-1');
ciclo('construtor-2', '16', -22, 10, 5);
// construtor-3 e o Fable
ciclo('construtor-3', '03', -74, 6, 2);
ciclo('construtor-3', '07', -64, 10, 3);
ciclo('construtor-3', '11', -52, 13, 4, 'revisor-2');
ev(-38, 'construtor-3', 'pegou_ticket', { ticket: '14' }, setk('14', 'curso', 'construtor-3'));
ev(-37, 'construtor-3', 'abriu_subagente', { ticket: '14', sub: 'construtor-3-14-s1', assunto: 'mapear ligações', modelo: OPUS });
ev(-33, 'construtor-3', 'fechou_subagente', { ticket: '14', sub: 'construtor-3-14-s1', ok: true });
msg(-31, 'construtor-3', 'maestro', 'ticket 14 é complexo demais; peço um especialista');
ev(-30, 'construtor-3', 'chamou_fable', { ticket: '14', para: 'fable-1', modelo: FABLE });
ev(-30, 'fable-1', 'inicio', { modelo: FABLE });
ev(-29.5, 'fable-1', 'pegou_ticket', { ticket: '14' }, setk('14', 'curso', 'fable-1'));
for (let i = 0; i < 6; i++) {
  const s = `fable-1-14-s${i + 1}`;
  ev(-28 + i * 2, 'fable-1', 'abriu_subagente', { ticket: '14', sub: s, assunto: SUBS[i], modelo: i === 0 ? FABLE : OPUS });
  ev(-24 + i * 2.2, 'fable-1', 'fechou_subagente', { ticket: '14', sub: s, ok: true });
}
ev(4, 'fable-1', 'rodou_teste', { ticket: '14', ok: true, assunto: 'pytest tests/ligacoes', detalhe: '31 passaram' });
ev(6, 'fable-1', 'commit', { ticket: '14', ok: true, assunto: 'ticket 14: motor de ligações' });
ev(8, 'fable-1', 'passou_ticket', { ticket: '14', para: 'revisor-1' }, setk('14', 'rev', 'revisor-1'));
ev(9, 'fable-1', 'fim');
ev(9.5, 'revisor-1', 'pegou_ticket', { ticket: '14' });
ev(13, 'revisor-1', 'resolveu_ticket', { ticket: '14' }, setk('14', 'feito', ''));
msg(11, 'revisor-1', 'maestro', 'ticket 14 aprovado; o Fable já encerrou');
// construtor-4: estoura a hora no ticket 04
ev(-74, 'construtor-4', 'pegou_ticket', { ticket: '04' }, setk('04', 'curso', 'construtor-4'));
for (let i = 0; i < 4; i++) {
  const s = `construtor-4-04-s${i + 1}`;
  ev(-70 + i * 12, 'construtor-4', 'abriu_subagente', { ticket: '04', sub: s, assunto: `reindexar lote ${i + 1}`, modelo: OPUS });
  ev(-60 + i * 12, 'construtor-4', 'fechou_subagente', { ticket: '04', sub: s, ok: i !== 2 });
}
ev(-14, 'construtor-4', 'passou_1h', { ticket: '04' });
msg(-13, 'construtor-4', 'maestro', 'ticket 04 passou de 1 hora; indexador ainda lento');
ev(3, 'construtor-4', 'abriu_subagente', { ticket: '04', sub: 'construtor-4-04-s5', assunto: 'reindexar lote 5', modelo: OPUS });
// construtor-5
ciclo('construtor-5', '08', -63, 10, 3);
ciclo('construtor-5', '15', -16, 10, 3);
ciclo('construtor-5', '17', 14, 10, 4, 'revisor-2');
ev(33, 'construtor-5', 'fim');
// construtor-2: pico de 10 subagentes no ticket 18
ev(3, 'construtor-2', 'pegou_ticket', { ticket: '18' }, setk('18', 'curso', 'construtor-2'));
for (let i = 0; i < (EXCESSO ? 11 : 10); i++) {
  const s = `construtor-2-18-s${i + 1}`;
  ev(3.2 + i * 0.1, 'construtor-2', 'abriu_subagente', { ticket: '18', sub: s, assunto: SUBS[i % SUBS.length], modelo: OPUS });
  ev(9 + i * 0.6, 'construtor-2', 'fechou_subagente', { ticket: '18', sub: s, ok: i !== 7 });
}
EV.push({ m: 16, a: 'construtor-2', tipo: 'commit', p: { ticket: '18', ok: true, assunto: 'ticket 18: painel de pendências' }, st: null, parcial: true });
ev(17, 'construtor-2', 'passou_ticket', { ticket: '18', para: 'revisor-1' }, setk('18', 'rev', 'revisor-1'));
ev(18, 'revisor-1', 'pegou_ticket', { ticket: '18' });
ev(22, 'revisor-1', 'resolveu_ticket', { ticket: '18' }, setk('18', 'feito', ''));
// falha: testador-2 reprova o 12, volta ao construtor-1
ev(-12, 'testador-2', 'rodou_teste', { ticket: '12', ok: false, assunto: 'pytest tests/aceite_12', detalhe: 'busca por tema retorna vazio com acento' });
ev(-7, 'testador-2', 'falhou', { ticket: '12', detalhe: 'busca por tema retorna vazio com acento; teste de aceite quebrou' });
ev(-6.9, 'testador-2', 'devolveu', { ticket: '12', detalhe: 'volta ao construtor-1 para ajustar o acento' }, setk('12', 'aberto', ''));
msg(-6.5, 'testador-2', 'construtor-1', 'ticket 12 falhou: acento na busca');
ev(2, 'construtor-1', 'pegou_ticket', { ticket: '12' }, setk('12', 'curso', 'construtor-1'));
ev(8, 'construtor-1', 'commit', { ticket: '12', ok: true, assunto: 'ticket 12: corrige acento na busca' });
ev(9, 'construtor-1', 'passou_ticket', { ticket: '12', para: 'testador-2' }, setk('12', 'teste', 'testador-2'));
ev(10, 'testador-2', 'pegou_ticket', { ticket: '12' });
ev(13, 'testador-2', 'rodou_teste', { ticket: '12', ok: true, assunto: 'pytest tests/aceite_12', detalhe: 'aceite passou' });
ev(13.2, 'testador-2', 'resolveu_ticket', { ticket: '12' }, setk('12', 'feito', ''));
// espera o Gustavo
ev(-45, 'integrador-1', 'pegou_ticket', { ticket: '20' }, setk('20', 'curso', 'integrador-1'));
ev(-43, 'integrador-1', 'esperando_gustavo', { ticket: '20', detalhe: 'aval do segundo par de olhos' }, setk('20', 'gustavo', 'integrador-1'));
msg(-42, 'integrador-1', 'maestro', 'ticket 20 espera o aval do Gustavo');
ev(-30, 'integrador-1', 'commit', { ok: true, assunto: 'integra tickets 01 a 07' });
ev(-9, 'integrador-1', 'commit', { ok: true, assunto: 'integra tickets 09 a 13' });
ev(15, 'integrador-1', 'commit', { ok: true, assunto: 'integra tickets 14 a 16' });
// conversas
msg(-58, 'construtor-1', 'construtor-2', 'qual formato o leitor devolve?', true);
msg(-57, 'construtor-2', 'construtor-1', 'lista de objetos com caminho e data');
msg(-46, 'revisor-2', 'construtor-3', 'esquema de tickets sem campo de dono');
msg(-27, 'construtor-5', 'construtor-3', 'o validador espera o campo Blocked by');
msg(-20, 'construtor-2', 'integrador-1', 'ticket 13 pronto para integrar');
msg(-3, 'revisor-1', 'construtor-5', 'ticket 15: filtros sem teste de borda');
msg(5, 'construtor-5', 'revisor-1', 'cobri a borda; pode olhar de novo');
msg(18, 'testador-1', 'construtor-2', 'ticket 18: botão de pendências sem foco');
msg(-40, 'prumo-1', 'maestro', 'marco 1 do laço confere com a spec');
msg(10, 'prumo-2', 'maestro', 'fatias verticais; nenhum ticket só de camada');
msg(-35, 'maestro', 'construtor-3', 'autorizado chamar o Fable no ticket 14');
msg(20, 'maestro', 'integrador-1', 'o Gustavo ainda não deu o aval do ticket 20');
ev(-6, 'testador-2', 'pegou_ticket', { ticket: '12' });
ev(-2, 'revisor-1', 'pegou_ticket', { ticket: '28' });
// testador-1: último sinal em +1; revisor-2: último sinal em -46
ev(-5, 'testador-1', 'rodou_teste', { ticket: '16', ok: true, assunto: 'pytest tests/aceite_16', detalhe: 'aceite passou' });
ev(1, 'testador-1', 'rodou_teste', { ticket: '16', ok: true, assunto: 'pytest tests/regressao', detalhe: 'ok' });

// ---- batimentos (sinal): 1/min enquanto vive, menos os que "caem"; com o freio de 30 s ----
const VIVE = Object.fromEntries(Object.keys(AGENTES).map(a => [a, [-75, 999]]));
VIVE['fable-1'] = [-30, 9]; VIVE['revisor-2'] = [-75, -46]; VIVE['testador-1'] = [-75, 1]; VIVE['construtor-5'] = [-75, 33];
const base = [...EV].sort((a, b) => a.m - b.m);
for (const [a, [i, f]] of Object.entries(VIVE)) {
  for (let m = i + 1; m <= Math.min(f, 40); m++) {
    const ultimo = Math.max(...base.filter(e => e.a === a && e.m <= m).map(e => e.m), -Infinity);
    if (m - ultimo >= 0.5) EV.push({ m, a, tipo: 'sinal', p: {}, st: null });
  }
}
EV.sort((x, y) => x.m - y.m);

// ---- gravação ----
const iso = (ts) => { const d = new Date(ts), p = (n, l = 2) => String(n).padStart(l, '0'), o = -d.getTimezoneOffset(), s = o >= 0 ? '+' : '-';
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}${s}${p(Math.floor(Math.abs(o) / 60))}:${p(Math.abs(o) % 60)}`; };
const slug = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const arqTicket = (k) => path.join(SAIDA, 'tickets', `${k}-${slug(T[k].titulo)}.md`);
function escreveTicket(k) {
  const t = T[k];
  fs.writeFileSync(arqTicket(k), `# ${t.titulo}\n\nType: task\nStatus: ${t.status}\nDono: ${t.dono}\nCom: ${t.com}\nBlocked by: ${t.dep.join(', ')}\n\n## Pronto quando\nO painel mostra este ticket sem erro.\n\n## Comments\n`);
}
function escreveExecucao(t0) {
  fs.writeFileSync(path.join(SAIDA, 'execucao.json'), JSON.stringify({
    formato: 1, id: 'fixture-construcao', titulo: 'Construção do context hub (fixture)', inicio: iso(t0), terminou_em: null,
    limites: { tentativa_min: 60, subagentes_por_agente: 10, sem_sinal_apos_s: 300 },
    fases: [{ id: 'spec', titulo: 'Spec', estado: 'feita' }, { id: 'tickets', titulo: 'Tickets de construção', estado: 'feita' }, { id: 'execucao', titulo: 'Execução', estado: 'em-curso' }],
    papeis: ['construtor', 'revisor', 'testador', 'integrador', 'prumo', 'maestro'].map(id => ({ id, titulo: id[0].toUpperCase() + id.slice(1) })),
    agentes: Object.values(AGENTES),
    padroes: { teste: ['^pytest\\b', '^python -m pytest\\b', '^npm (run )?test\\b'], commit: ['^git commit\\b'] },
  }, null, 1));
}
const arqEv = (a) => path.join(SAIDA, 'eventos', a + '.jsonl');
function aplica(e, ts) {
  const linha = JSON.stringify({ t: iso(ts), agente: e.a, tipo: e.tipo, ...e.p });
  if (e.parcial && ts - AGORA > 1000) { // ao vivo: metade da linha, o resto 1,5 s depois
    const meio = Math.floor(linha.length / 2);
    fs.appendFileSync(arqEv(e.a), linha.slice(0, meio));
    setTimeout(() => fs.appendFileSync(arqEv(e.a), linha.slice(meio) + '\n'), 1500);
  } else fs.appendFileSync(arqEv(e.a), linha + '\n');
  if (e.st) { const t = T[e.st.k]; t.status = e.st.status; t.com = e.st.com; escreveTicket(e.st.k); }
}

fs.rmSync(SAIDA, { recursive: true, force: true });
fs.mkdirSync(path.join(SAIDA, 'eventos'), { recursive: true });
fs.mkdirSync(path.join(SAIDA, 'tickets'), { recursive: true });
const AGORA = Date.now();
escreveExecucao(AGORA - 75 * 60000);
for (const k of Object.keys(T)) escreveTicket(k);

const corte = SO_HIST ? ATE : 0;
const passado = EV.filter(e => e.m <= corte), futuro = EV.filter(e => e.m > corte);
for (const e of passado) { const ee = SO_HIST ? { ...e, parcial: false } : e; aplica(ee, AGORA + e.m * 60000); }

if (DEFEITOS) {
  const w = (f, s) => fs.appendFileSync(f, s);
  w(arqEv('construtor-1'), 'isto não é json\n');
  w(arqEv('construtor-1'), JSON.stringify({ t: iso(AGORA - 60000), agente: 'construtor-1', tipo: 'tipo_novo_do_hook', extra: 1 }) + '\n');
  w(arqEv('construtor-1'), `{"t":"${iso(AGORA)}","agente":"construtor-1","tipo":"sinal"`); // sem fechar e sem \n
  fs.writeFileSync(arqEv('agente-nao-listado'), JSON.stringify({ t: iso(AGORA - 30000), agente: 'agente-nao-listado', tipo: 'inicio', modelo: OPUS }) + '\n');
  fs.writeFileSync(path.join(SAIDA, 'tickets', '29-ticket-com-status-estranho.md'), '# Ticket com status estranho\n\nType: task\nStatus: em-andamento\nDono: construtor\nCom:\nBlocked by: 99\n');
  fs.writeFileSync(path.join(SAIDA, 'tickets', '30-ciclo-a.md'), '# Ciclo A\n\nType: task\nStatus: open\nDono: construtor\nCom:\nBlocked by: 31\n');
  fs.writeFileSync(path.join(SAIDA, 'tickets', '31-ciclo-b.md'), '# Ciclo B\n\nType: task\nStatus: open\nDono: construtor\nCom:\nBlocked by: 30\n');
}

console.log(`passado: ${passado.length} eventos em ${SAIDA}`);
if (SO_HIST || !futuro.length) process.exit(0);
console.log(`ao vivo: ${futuro.length} eventos, ~${Math.round(futuro.at(-1).m * 60 / VEL)} s reais (velocidade ${VEL}). Ctrl+C para parar.`);
const t0 = Date.now(); let i = 0;
const timer = setInterval(() => {
  const dt = (Date.now() - t0) / 1000 * VEL / 60;
  while (i < futuro.length && futuro[i].m <= dt) { aplica(futuro[i], Date.now()); i++; }
  if (i >= futuro.length) { clearInterval(timer); console.log('fim do roteiro'); setTimeout(() => process.exit(0), 2000); }
}, 200);
