// Correção de 2026-10-14 (relato do Gustavo na resposta 65ca59e5): prova no navegador dos dois defeitos.
//  1. rodada reescrita depois da resposta volta a esperar (contador, lista, formulário novo, resposta anterior como
//     histórico) e a resposta nova sai com base = sha256 novo e substitui = a anterior; rodada absorvida não volta;
//  2. a atualização ao vivo (arquivo mudando enquanto ele escreve) não mexe no formulário em edição: foco, cursor,
//     seleção, rolagem, texto, <details> aberto e rascunho ficam (Responder, emenda, comentário na gaveta); mudança
//     na própria rodada vira o aviso "a rodada mudou" em vez de trocar o formulário.
// uso: node prova_correcao.js <pasta horta/ de uma CÓPIA NOVA da fixture> <url do servidor da cópia>
// Só escreve na cópia. Grava prova_correcao.json e as capturas nesta pasta.
const puppeteer = require('puppeteer-core');
const fs = require('fs'); const path = require('path');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const [horta, BASE] = process.argv.slice(2);
const AQUI = __dirname;
const R = '2026-10-01-canteiros-e-caminhos-r2';
const ARQ_RODADA = path.join(horta, 'portal', 'rodadas', R + '.md');
const espera = ms => new Promise(r => setTimeout(r, ms));
async function ir(p, url) { await p.goto('about:blank'); await p.goto(url, { waitUntil: 'networkidle0', timeout: 60000 }); await espera(800); }
async function ate(p, fn, arg, limite = 9000) { const t0 = Date.now(); while (Date.now() - t0 < limite) { if (await p.evaluate(fn, arg)) return Date.now() - t0; await espera(100); } return null; }
const marcarTela = p => p.evaluate(() => { const n = document.querySelector('#tela > *'); n.__velha = 1; const l = document.querySelector('.lista-rodadas, .gaveta-cabeca'); if (l) l.__velha = 1; });
// a tela foi redesenhada: o cabeçalho/lista (não preservados) são nós novos
const redesenhou = () => { const l = document.querySelector('.lista-rodadas'); return !!l && !l.__velha; };
function mudarTicket(n, sonda) { const f = fs.readdirSync(path.join(horta, 'issues')).find(x => x.startsWith(n + '-')); fs.appendFileSync(path.join(horta, 'issues', f), `\n${sonda}\n`); }
const contador = p => p.evaluate(() => document.querySelector('#contador .palhetas')?.textContent || '');
// rola só a área da tela (#tela), nunca o documento, até o seletor ficar no topo
const rolarAte = (p, sel) => p.evaluate(sel => { const m = document.getElementById('tela'); const el = document.querySelector(sel); if (el) m.scrollTop += el.getBoundingClientRect().top - m.getBoundingClientRect().top - 12; window.scrollTo(0, 0); }, sel);
const foto = (p, nome) => p.screenshot({ path: path.join(AQUI, nome) });

(async () => {
  const r = { quando: new Date().toISOString() };
  const b = await puppeteer.launch({ executablePath: EDGE, headless: 'new', args: ['--disable-gpu'] });
  const p = await b.newPage(); await p.setViewport({ width: 1600, height: 900 });
  const erros = []; p.on('pageerror', e => erros.push(String(e)));
  const posts = []; p.on('request', q => { if (q.method() === 'POST' && q.url().endsWith('/api/caixa')) posts.push(JSON.parse(q.postData())); });

  // ---------------------------------------------------------------- 2a. Responder: comentário em edição + ticket muda
  await ir(p, BASE + '#/autorizacoes/' + R);
  r.contador_inicial = await contador(p);
  await p.evaluate(() => { document.querySelector('[data-foco="q-largura-outra"]').closest('details').open = true; document.querySelector('[data-foco="q-largura-comentario"]').closest('details').open = true; });
  await p.focus('[data-foco="q-largura-comentario"]');
  await p.keyboard.type('primeira linha do comentario');
  const antesA = await p.evaluate(() => { const t = document.activeElement; t.__marca = 1; t.setSelectionRange(8, 13, 'forward'); const m = document.getElementById('tela'); m.scrollTop = 420; return { chave: t.dataset.foco, selecao: [t.selectionStart, t.selectionEnd], rolagem: m.scrollTop, texto: t.value }; });
  await marcarTela(p);
  mudarTicket('05', 'SONDA-TICKET-05');
  const msA = await ate(p, redesenhou);
  const depoisA = await p.evaluate(() => { const t = document.activeElement; const m = document.getElementById('tela'); const k = Object.keys(localStorage).find(x => x.includes('canteiros-e-caminhos-r2')); return {
    mesmo_elemento: t.__marca === 1, chave: t.dataset?.foco, selecao: [t.selectionStart, t.selectionEnd], rolagem: m.scrollTop, texto: t.value,
    outra_aberto: document.querySelector('[data-foco="q-largura-outra"]').closest('details').open,
    rascunho: JSON.parse(localStorage.getItem(k)).respostas.largura.comentario }; });
  await foto(p, 'formulario-depois-de-mudanca-externa-1600.png');
  await p.setViewport({ width: 1280, height: 800 }); await espera(300);
  await foto(p, 'formulario-depois-de-mudanca-externa-1280.png');
  await p.setViewport({ width: 1600, height: 900 }); await espera(300);
  await p.keyboard.type('LINHA');   // substitui a seleção, como ele faria
  const continuaA = await p.evaluate(() => document.activeElement.value);
  r.responder_comentario = { antes: antesA, redesenho_ms: msA, depois: depoisA, digitou_depois: continuaA,
    ok: msA !== null && depoisA.mesmo_elemento && depoisA.selecao.join() === '8,13' && depoisA.rolagem === antesA.rolagem && depoisA.texto === antesA.texto && depoisA.outra_aberto && depoisA.rascunho === antesA.texto && continuaA === 'primeiraLINHAa do comentario' };

  // ---------------------------------------------------------------- 2b. emenda: célula em edição + ticket muda
  await p.focus('[data-foco="q-mutirao-montar-tempo"]');
  await p.keyboard.press('End'); await p.keyboard.type(' e meia');
  const antesB = await p.evaluate(() => { const t = document.activeElement; t.__marca = 2; t.setSelectionRange(2, 2); return { texto: t.value, selecao: [t.selectionStart, t.selectionEnd] }; });
  await marcarTela(p); mudarTicket('06', 'SONDA-TICKET-06');
  const msB = await ate(p, redesenhou);
  const depoisB = await p.evaluate(() => { const t = document.activeElement; return { mesmo_elemento: t.__marca === 2, texto: t.value, selecao: [t.selectionStart, t.selectionEnd], mudancas: document.querySelector('.emenda .mudancas')?.innerText }; });
  r.emenda = { antes: antesB, redesenho_ms: msB, depois: depoisB, ok: msB !== null && depoisB.mesmo_elemento && depoisB.texto === '3 h e meia' && depoisB.selecao.join() === '2,2' };

  // ---------------------------------------------------------------- 2c. gaveta: comentário em edição + o próprio ticket muda
  fs.appendFileSync(path.join(horta, 'issues', '04-composteira.md'), '\n' + Array.from({ length: 60 }, (_, i) => `Linha de enchimento ${i + 1} para a gaveta ter rolagem.\n`).join('\n'));
  await espera(3500);
  await ir(p, BASE + '#/partidas?ticket=04');
  await p.click('#gaveta [data-foco="acao-comentario"]'); await espera(200);
  await p.focus('#gaveta [data-foco="acao-texto"]');
  await p.keyboard.type('comentario longo que o Gustavo esta escrevendo');
  const antesC = await p.evaluate(() => { const t = document.activeElement; t.__marca = 3; t.setSelectionRange(11, 16); const c = document.querySelector('#gaveta .gaveta-corpo'); c.scrollTop = 120; return { texto: t.value, selecao: [t.selectionStart, t.selectionEnd], rolagem_corpo: c.scrollTop }; });
  mudarTicket('04', 'SONDA-GAVETA-04');
  const msC = await ate(p, () => (document.querySelector('#gaveta .gaveta-corpo')?.innerText || '').includes('SONDA-GAVETA-04'));
  await espera(300);
  const depoisC = await p.evaluate(() => { const t = document.activeElement; const c = document.querySelector('#gaveta .gaveta-corpo'); return { mesmo_elemento: t.__marca === 3, texto: t.value, selecao: [t.selectionStart, t.selectionEnd], rolagem_corpo: c.scrollTop }; });
  await foto(p, 'gaveta-depois-de-mudanca-externa-1600.png');
  r.gaveta = { antes: antesC, atualizou_ms: msC, depois: depoisC, ok: msC !== null && depoisC.mesmo_elemento && depoisC.texto === antesC.texto && depoisC.selecao.join() === '11,16' && depoisC.rolagem_corpo === antesC.rolagem_corpo && antesC.rolagem_corpo > 0 };

  // ---------------------------------------------------------------- 2c'. leitor de carta: comentário da carta em edição + ticket muda
  await ir(p, BASE + '#/cartas/regas-do-poco');
  await p.click('#leitor [data-foco="acao-comentario"]'); await espera(200);
  await p.focus('#leitor [data-foco="acao-texto"]'); await p.keyboard.type('nota sobre a carta');
  await p.evaluate(() => { const t = document.activeElement; t.__marca = 5; t.setSelectionRange(2, 4); });
  mudarTicket('10', 'SONDA-TICKET-10'); await espera(4500);
  const depoisCarta = await p.evaluate(() => { const t = document.activeElement; return { mesmo_elemento: t.__marca === 5, texto: t.value, selecao: [t.selectionStart, t.selectionEnd] }; });
  r.carta_comentario = { depois: depoisCarta, ok: depoisCarta.mesmo_elemento && depoisCarta.texto === 'nota sobre a carta' && depoisCarta.selecao.join() === '2,4' };

  // ---------------------------------------------------------------- 2d. a própria rodada muda enquanto ele escreve
  await ir(p, BASE + '#/autorizacoes/' + R);
  await p.focus('[data-foco="q-algo-mais-texto"]');
  await p.keyboard.type('texto que nao pode sumir');
  const antesD = await p.evaluate(() => { const t = document.activeElement; t.__marca = 4; t.setSelectionRange(6, 9); return { texto: t.value }; });
  const baseVelha = await p.evaluate(async rid => (await (await fetch('/api/estado')).json()).rodadas.find(x => x.id === rid).base, R);
  fs.appendFileSync(ARQ_RODADA, '\nO maestro acrescentou esta linha enquanto o Gustavo escrevia.\n');
  const msD = await ate(p, () => !!document.querySelector('[data-foco="ver-versao-nova"]'));
  const depoisD = await p.evaluate(base => { const t = document.activeElement; const k = Object.keys(localStorage).find(x => x.endsWith(':' + base)); return { mesmo_elemento: t.__marca === 4, texto: t.value, selecao: [t.selectionStart, t.selectionEnd], rascunho_versao_velha: k ? JSON.parse(localStorage.getItem(k)).respostas['algo-mais'].texto : null, aviso: !!document.querySelector('.aviso-rodada.rodada-mudou') }; }, baseVelha);
  await espera(3500); // mais um ciclo de 3 s: o formulário continua o mesmo
  const aindaD = await p.evaluate(() => ({ mesmo_elemento: document.activeElement.__marca === 4, texto: document.activeElement.value }));
  await rolarAte(p, '.aviso-rodada.rodada-mudou'); await espera(200);
  await foto(p, 'rodada-mudou-durante-edicao-1600.png');
  await p.focus('[data-foco="q-algo-mais-texto"]');
  await p.click('[data-foco="ver-versao-nova"]'); await espera(500);
  const painel = await p.evaluate(() => (document.querySelector('.formulario-rodada .aviso-rodada.ambar')?.innerText || '').slice(0, 80));
  await p.click('[data-foco="copiar-rascunho"]'); await espera(300);
  const copiado = await p.evaluate(() => document.querySelector('[data-foco="q-algo-mais-texto"]').value);
  r.rodada_mudou_em_edicao = { aviso_ms: msD, depois: depoisD, um_ciclo_depois: aindaD, painel_da_versao_nova: painel, copiado_para_a_nova: copiado,
    ok: msD !== null && depoisD.mesmo_elemento && depoisD.texto === antesD.texto && depoisD.selecao.join() === '6,9' && depoisD.rascunho_versao_velha === antesD.texto && depoisD.aviso && aindaD.mesmo_elemento && copiado === antesD.texto };

  // ---------------------------------------------------------------- 1. responder, o maestro reescreve, a rodada volta a esperar
  await ir(p, BASE + '#/autorizacoes/' + R);
  await p.click('[data-foco="enviar-torre"]');
  await ate(p, () => !!document.querySelector('[data-foco="confirmacao"]'));
  const r1 = posts[posts.length - 1];
  await ate(p, () => document.querySelector('#contador .palhetas')?.textContent === '0');
  const respondida = { contador: await contador(p), situacao: await p.evaluate(() => document.querySelector('.rodada-cabeca .carimbo')?.textContent) };
  const estado1 = await p.evaluate(async rid => (await (await fetch('/api/estado')).json()).rodadas.find(x => x.id === rid), R);
  fs.appendFileSync(ARQ_RODADA, '\nE o maestro reescreveu a rodada depois da resposta.\n');
  const msE = await ate(p, () => !!document.querySelector('[data-foco="aviso-reaberta"]'));
  await ate(p, () => !!document.querySelector('[data-foco="copiar-anterior"]'));
  const reaberta = await p.evaluate(rid => ({
    contador: document.querySelector('#contador .palhetas')?.textContent,
    grupo: [...document.querySelectorAll('.grupo-rodadas')].find(g => g.querySelector(`a[href$="${rid}"]`))?.querySelector('h2')?.firstChild?.textContent,
    carimbo_lista: document.querySelector(`a[href$="${rid}"] .carimbo`)?.textContent,
    situacao: document.querySelector('.rodada-cabeca .carimbo')?.textContent,
    tem_formulario: !!document.querySelector('.formulario-rodada'),
    historico: (document.querySelector('[data-foco="resposta-anterior"]')?.innerText || '').slice(0, 120) }), R);
  await rolarAte(p, '.rodada-cabeca'); await espera(200);
  await foto(p, 'rodada-reaberta-1600.png');
  await rolarAte(p, '[data-foco="resposta-anterior"]');
  await foto(p, 'rodada-reaberta-historico-1600.png');
  await p.setViewport({ width: 1280, height: 800 }); await p.evaluate(() => { document.getElementById('tela').scrollTop = 0; }); await espera(300);
  await foto(p, 'rodada-reaberta-1280.png');
  await p.setViewport({ width: 1600, height: 900 }); await espera(300);
  await p.click('[data-foco="copiar-anterior"]'); await espera(400);
  const nPosts = posts.length;
  await p.click('[data-foco="enviar-torre"]');
  await ate(p, () => !!document.querySelector('[data-foco="confirmacao"]'));
  const r2 = posts[nPosts];
  const estado2 = await p.evaluate(async rid => { const e = await (await fetch('/api/estado')).json(); return { rodada: e.rodadas.find(x => x.id === rid), caixa: e.caixa.filter(c => c.alvo.id === rid) }; }, R);
  const arq1 = estado2.caixa.find(c => c.envio === r1.envio)?.arquivo;
  await ate(p, () => document.querySelector('#contador .palhetas')?.textContent === '0');
  r.rodada_reescrita = { primeira_resposta_base: r1.base, base_na_primeira: estado1.base, respondida_antes: respondida, reaberta_ms: msE, reaberta,
    segunda_resposta: { base: r2 && r2.base, substitui: r2 && r2.substitui, respostas: r2 && Object.keys(r2.respostas) },
    base_atual: estado2.rodada.base, respondida_depois: estado2.rodada.respondida, ultima_resposta: estado2.rodada.ultima_resposta, contador_depois: await contador(p),
    ok: msE !== null && reaberta.contador === '1' && reaberta.grupo === 'Aguardando você' && reaberta.tem_formulario && reaberta.historico.includes('Sua resposta à versão anterior')
      && r2 && r2.base === estado2.rodada.base && r2.base !== r1.base && r2.substitui === arq1 && estado2.rodada.respondida && (await contador(p)) === '0' };

  // ---------------------------------------------------------------- 1b. rodada absorvida reescrita não volta a esperar
  fs.writeFileSync(ARQ_RODADA, fs.readFileSync(ARQ_RODADA, 'utf8').replace('estado: aberta', 'estado: absorvida') + '\nlinha depois de absorvida\n');
  await ate(p, rid => document.querySelector(`a[href$="${rid}"] .carimbo`)?.textContent === 'ABSORVIDA', R);
  r.absorvida = { contador: await contador(p), carimbo: await p.evaluate(rid => document.querySelector(`a[href$="${rid}"] .carimbo`)?.textContent, R) };
  r.absorvida.ok = r.absorvida.contador === '0' && r.absorvida.carimbo === 'ABSORVIDA';

  r.erros_js = erros;
  r.tudo_ok = ['responder_comentario', 'emenda', 'gaveta', 'carta_comentario', 'rodada_mudou_em_edicao', 'rodada_reescrita', 'absorvida'].every(k => r[k].ok) && !erros.length;
  fs.writeFileSync(path.join(AQUI, 'prova_correcao.json'), JSON.stringify(r, null, 1));
  console.log(JSON.stringify(r, null, 1));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
