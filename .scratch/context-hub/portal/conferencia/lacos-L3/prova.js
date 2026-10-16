// Prova da tela Laços (marco L3) sobre uma CÓPIA da fixture horta, servida na porta 8775 (nunca o portal real).
// uso: node prova.js <pasta da cópia> [saída]   (NODE_PATH apontando para o puppeteer-core)
// Prova: lista, fluxo, gaveta; mudar-controle, pedir-parada, comentário de nó e de laço gravando na caixa da cópia;
// 400 e 409 em palavras (409 com definicao_mudou null e true); erro de rede reenvia o mesmo envio; recarga preserva o
// que se digita; laço terminado só leitura; conflito do maestro põe o laço em "espera você"; recibo inválido em tijolo;
// zero erros de JS, fonte mínima 14 px, sem rolagem horizontal da página; capturas em 1600×900 e 1280×800.
const puppeteer = require('puppeteer-core');
const fs = require('fs'); const path = require('path');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const COPIA = process.argv[2];
const SAIDA = process.argv[3] || __dirname;
const BASE = 'http://127.0.0.1:8775/';
const PERFIL = path.join(process.env.TEMP || 'C:/Temp', 'l3-edge-perfil-prova');
const CAIXA = path.join(COPIA, 'portal', 'caixa');
const REGAS = path.join(COPIA, 'lacos', 'regas');
const espera = ms => new Promise(r => setTimeout(r, ms));
const LIMPEZA = require('./limpeza.js');
const limpo = l => l && !l.cortados.length && !l.pilulaEmLinha.length && !l.pilulaEmPilula.length && !l.linhaEmTexto.length && l.folgaEnvelopes.every(f => f >= 6);
const prova = { quando: new Date().toISOString(), copia: COPIA, passos: {}, erros_js: [], capturas: [] };
const ok = (nome, cond, extra) => { prova.passos[nome] = { ok: !!cond, ...(extra || {}) }; console.log(`${cond ? 'OK ' : 'FALHOU'} ${nome}${extra ? ' ' + JSON.stringify(extra).slice(0, 300) : ''}`); };
const jsonsDaCaixa = () => fs.readdirSync(CAIXA).filter(f => f.endsWith('.json') && f.includes('alteracao-laco')).map(f => ({ f, d: JSON.parse(fs.readFileSync(path.join(CAIXA, f), 'utf8')) }));
const novoNaCaixa = (antes, filtro) => jsonsDaCaixa().filter(x => !antes.has(x.f) && filtro(x.d));
const nomes = () => new Set(jsonsDaCaixa().map(x => x.f));
const avivar = () => { const t = Date.now() / 1000; for (const n of ['manha.jsonl', 'tarde.jsonl']) fs.utimesSync(path.join(REGAS, 'livros', n), t, t); };
const lerJson = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const gravarJson = (p, d) => fs.writeFileSync(p, JSON.stringify(d, null, 2), 'utf8');

async function medir(p) {
  return p.evaluate(() => {
    let menor = 99, onde = '';
    document.querySelectorAll('body *').forEach(el => {
      if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
      const cs = getComputedStyle(el); if (cs.display === 'none' || el.closest('[hidden]') || el.closest('iframe') || el.closest('.visualmente-oculto')) return;
      const r = el.getBoundingClientRect(); if (!r.width) return;
      const f = parseFloat(cs.fontSize); if (f < menor) { menor = f; onde = `${el.tagName}.${(el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className)}: ${el.textContent.trim().slice(0, 30)}`; }
    });
    const t = document.getElementById('tela');
    return { menorFonte: menor, onde, rolagemHorizontal: t.scrollWidth > t.clientWidth + 1 || document.documentElement.scrollWidth > document.documentElement.clientWidth };
  });
}
async function capturar(p, nome, inteira = false) {
  const vp = p.viewport();
  if (inteira) {
    const alt = await p.evaluate(() => document.getElementById('tela').scrollHeight + 160);
    await p.setViewport({ width: vp.width, height: Math.max(vp.height, alt) }); await espera(700);
  }
  const arq = path.join(SAIDA, `${nome}.png`);
  await p.screenshot({ path: arq });
  prova.capturas.push(path.basename(arq));
  if (inteira) { await p.setViewport(vp); await espera(400); }
}
async function ir(p, rota, ms = 2500) { await p.goto(BASE + rota, { waitUntil: 'networkidle0' }); await espera(ms); }
// o aviso passageiro (brisa, 5 s, canto de baixo à direita) pode cobrir um botão da gaveta: espera ele sumir
// e o redesenho ao vivo pode trocar o nó entre achá-lo e clicá-lo: tenta de novo (até 3 vezes)
const clicar = async (p, sel) => {
  for (let i = 0; ; i++) {
    try { await p.waitForSelector(sel, { visible: true, timeout: 8000 }); await p.waitForFunction(() => !document.querySelector('#brisa .sopro'), { timeout: 8000 }); await p.click(sel); return; }
    catch (e) { if (i >= 2 || !/detached|not clickable/i.test(String(e))) throw e; await espera(400); }
  }
};
async function digitar(p, sel, texto, limpar = true) {
  await p.waitForSelector(sel, { visible: true, timeout: 8000 });
  if (limpar) await p.$eval(sel, el => { el.focus(); el.select && el.select(); });
  else await p.focus(sel);
  await p.keyboard.type(texto);
}
const texto = (p, sel) => p.$eval(sel, el => el.innerText).catch(() => null);

(async () => {
  fs.mkdirSync(SAIDA, { recursive: true });
  fs.rmSync(PERFIL, { recursive: true, force: true }); // perfil limpo: nenhum rascunho de uma rodada anterior no localStorage
  avivar();
  const b = await puppeteer.launch({ executablePath: EDGE, headless: 'new', userDataDir: PERFIL, args: ['--disable-gpu', '--hide-scrollbars'] });
  try {
    const p = await b.newPage();
    p.on('pageerror', e => prova.erros_js.push(String(e)));
    p.on('console', m => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) prova.erros_js.push('console: ' + m.text()); });
    const respostas = [];
    p.on('response', async r => { if (r.url().endsWith('/api/caixa') && r.request().method() === 'POST') { let c = null; try { c = await r.json(); } catch {} respostas.push({ status: r.status(), corpo: c, envio: JSON.parse(r.request().postData() || '{}').envio }); } });
    await p.setViewport({ width: 1600, height: 900 });

    // 1. lista e fluxo
    await ir(p, '#/lacos', 3000);
    const lista = await p.evaluate(() => [...document.querySelectorAll('.grupo-lacos')].map(g => ({ grupo: g.querySelector('.grupo-lacos-titulo').innerText.trim(), lacos: [...g.querySelectorAll('.item-laco .titulo')].map(t => t.innerText) })));
    ok('lista por grupo', lista.length === 3 && lista[1].lacos.length === 1 && lista[2].lacos.length === 1, { lista });
    const fluxo = await p.evaluate(() => ({ nos: [...document.querySelectorAll('svg.fluxo .no')].map(n => n.getAttribute('data-foco')), rotulos: [...document.querySelectorAll('svg.fluxo .rotulo-lig text')].map(t => t.textContent), situacao: document.querySelector('.laco-cabeca .selo-laco')?.innerText }));
    ok('fluxo com os 8 nós e uma palavra por seta', fluxo.nos.length === 8 && fluxo.rotulos.length === 9 && fluxo.rotulos.every(r => r.split(' ').length <= 2), fluxo);
    ok('situação rodando', /rodando/.test(fluxo.situacao || ''), { situacao: fluxo.situacao });
    const m1 = await medir(p);
    ok('fonte mínima 14 px e sem rolagem horizontal (1600)', m1.menorFonte >= 14 && !m1.rolagemHorizontal, m1);
    await capturar(p, 'lacos-1600x900'); await capturar(p, 'lacos-1600-inteira', true);
    const lz1 = await p.evaluate(LIMPEZA);
    ok('fluxo limpo: nada cortado, pílula sem linha alheia, linha sem texto, envelope afastado', limpo(lz1), lz1);

    // 2. gaveta do nó (geradores): configurado × em uso × proposta; mudar-controle grava na caixa
    await clicar(p, '[data-foco="no-geradores"]'); await espera(900);
    const gav = await p.evaluate(() => { const g = document.getElementById('gaveta-no'); return { aberta: !g.hidden, titulo: g.querySelector('h2')?.innerText, foco: g.contains(document.activeElement), blocos: [...g.querySelectorAll('.bloco-titulo')].map(x => x.innerText.split('\n')[0]), cfg: g.querySelector('.linha-cfg')?.innerText, uso: g.querySelector('.linha-uso')?.innerText }; });
    ok('gaveta abre, prende o foco e mostra configurado × em uso', gav.aberta && gav.titulo === 'Geradores' && gav.foco && /configurado/.test(gav.cfg) && /não confirmado/.test(gav.uso), gav);
    await capturar(p, 'gaveta-geradores-1600x900');
    let antes = nomes();
    await digitar(p, '[data-foco="num-trabalhadores_por_gerador"]', '24');
    await digitar(p, '[data-foco="por-que-trabalhadores_por_gerador"]', 'mais vazão na tarde', false);
    await capturar(p, 'gaveta-proposta-1600x900');
    await clicar(p, '[data-foco="pedir-trabalhadores_por_gerador"]'); await espera(1800);
    let novos = novoNaCaixa(antes, d => d.corpo.operacao === 'mudar-controle');
    ok('mudar-controle gravado (20 → 24, revisão vista, só ids e valores)', novos.length === 1 && novos[0].d.corpo.antes.valor === 20 && novos[0].d.corpo.depois.valor === 24 && /^[0-9a-f]{64}$/.test(novos[0].d.corpo.revisao) && novos[0].d.corpo.controle === 'trabalhadores_por_gerador', novos[0] && { arquivo: novos[0].f, corpo: novos[0].d.corpo });
    const arqMudar = novos[0] && novos[0].f.replace(/\.json$/, '');

    // 3. comentário de nó
    antes = nomes();
    await digitar(p, `[data-foco="com-no:pesquisa-de-regas:regas-2026-10-14:geradores-texto"]`, 'trocar o harness do recruta da tarde?', false);
    await clicar(p, '[data-foco="com-no:pesquisa-de-regas:regas-2026-10-14:geradores-enviar"]'); await espera(1600);
    novos = novoNaCaixa(antes, d => d.corpo.operacao === 'comentario-no');
    ok('comentario-no gravado', novos.length === 1 && novos[0].d.corpo.no === 'geradores' && novos[0].d.corpo.texto.startsWith('trocar'), novos[0] && novos[0].d.corpo);
    const pedidosNo = await p.$$eval('#gaveta-no .bloco-pedidos .cartao-pedido', els => els.map(e => e.querySelector('.estado-pedido')?.innerText));
    ok('pedidos do nó com estado em palavras', pedidosNo.length >= 2 && pedidosNo.includes('enviado'), { pedidosNo });
    await capturar(p, 'gaveta-pedidos-1600x900');
    await p.keyboard.press('Escape'); await espera(900);
    const fechou = await p.evaluate(() => ({ escondida: document.getElementById('gaveta-no').hidden, foco: document.activeElement?.getAttribute('data-foco'), rota: location.hash }));
    ok('Esc fecha a gaveta e devolve o foco ao nó', fechou.escondida && fechou.foco === 'no-geradores' && !/no=/.test(fechou.rota), fechou);

    // 4. comentário do laço + recarga preservando o que se digita (ao vivo: a cada 10 s e quando um arquivo muda)
    const selCom = '[data-foco="com-laco:pesquisa-de-regas:regas-2026-10-14-texto"]';
    await digitar(p, selCom, 'escrevendo devagar', false);
    await p.$eval(selCom, el => { el.__marca = 'mesmo-no'; el.setSelectionRange(4, 4); });
    avivar(); fs.utimesSync(path.join(REGAS, 'laco.json'), new Date(), new Date()); // muda a versão: a casca redesenha
    await espera(12500); // e o relógio de 10 s da tela também
    const pres = await p.$eval(selCom, el => ({ marca: el.__marca, valor: el.value, foco: document.activeElement === el, cursor: el.selectionStart }));
    ok('redesenho preserva texto, foco e cursor', pres.marca === 'mesmo-no' && pres.valor === 'escrevendo devagar' && pres.foco && pres.cursor === 4, pres);
    await p.keyboard.type(' (ainda)');
    antes = nomes();
    await clicar(p, '[data-foco="com-laco:pesquisa-de-regas:regas-2026-10-14-enviar"]'); await espera(1600);
    novos = novoNaCaixa(antes, d => d.corpo.operacao === 'comentario-laco');
    ok('comentario-laco gravado', novos.length === 1 && novos[0].d.corpo.texto === 'escr (ainda)evendo devagar', novos[0] && novos[0].d.corpo);

    // 5. pedir parada depois da onda 3 (onda em curso 2), com o aviso de cota
    await clicar(p, '[data-foco="pedir-parada"]'); await espera(700);
    const aviso = await texto(p, '.painel-parada .nota-cota');
    await p.$eval('[data-foco="onda-alvo"]', el => { el.value = ''; });
    await digitar(p, '[data-foco="onda-alvo"]', '3');
    await capturar(p, 'pedir-parada-1600x900');
    antes = nomes();
    await clicar(p, '[data-foco="parada-enviar"]'); await espera(1600);
    novos = novoNaCaixa(antes, d => d.corpo.operacao === 'pedir-parada');
    ok('pedir-parada gravado (depois da onda 3)', novos.length === 1 && novos[0].d.corpo.capacidade === 'parar-apos-onda' && novos[0].d.corpo.onda === 3 && /gastam cota/.test(aviso || ''), novos[0] && { corpo: novos[0].d.corpo, aviso });
    const arqParada = novos[0] && novos[0].f.replace(/\.json$/, '');

    // 6. 400 em palavras: a capacidade some do laço depois que a página a leu
    const lacoJson = path.join(REGAS, 'laco.json'); const lacoOriginal = fs.readFileSync(lacoJson, 'utf8');
    await clicar(p, '[data-foco="pedir-parada"]'); await espera(600);
    await clicar(p, '[data-foco="cap-parar-de-despachar"]');
    const semCap = lerJson(lacoJson); semCap.capacidades = semCap.capacidades.filter(c => c.id !== 'parar-de-despachar'); gravarJson(lacoJson, semCap);
    antes = nomes();
    await clicar(p, '[data-foco="parada-enviar"]'); await espera(1400);
    const e400 = await texto(p, '.painel-parada .erro-acao');
    ok('400 em palavras, nada gravado', /recusou/.test(e400 || '') && /não declara/.test(e400 || '') && !/parar-de-despachar/.test(e400 || '') && novoNaCaixa(antes, () => true).length === 0, { mensagem: e400, http: respostas[respostas.length - 1]?.status });
    await capturar(p, 'recusa-400-1600x900');
    fs.writeFileSync(lacoJson, lacoOriginal, 'utf8');
    await clicar(p, '.painel-parada .fechar'); await espera(500);

    // 7. 409 de revisão com definicao_mudou null: o configurado muda enquanto a proposta está aberta
    await ir(p, '#/lacos/pesquisa-de-regas?no=juntador', 3000);
    await digitar(p, '[data-foco="num-max_celulas_novas_por_onda"]', '200');
    const cfgJson = path.join(REGAS, 'config.json'); const cfg = lerJson(cfgJson); cfg.max_celulas_novas_por_onda = 150; gravarJson(cfgJson, cfg);
    antes = nomes();
    await clicar(p, '[data-foco="pedir-max_celulas_novas_por_onda"]'); await espera(1500);
    const c409 = await p.evaluate(() => { const g = document.getElementById('gaveta-no'); const e = g.querySelector('.erro-acao'); return { texto: e && e.innerText, tri: e && [...e.querySelectorAll('.conflito-tri b')].map(b => b.innerText) }; });
    const r409 = respostas[respostas.length - 1];
    ok('409 null: "você viu / agora está / você pediu" + a regra ou a configuração mudou', r409 && r409.status === 409 && r409.corpo?.conflito?.definicao_mudou === null && c409.tri.join('|') === '120 células|150 células|200 células' && /o portal não sabe qual/.test(c409.texto) && novoNaCaixa(antes, () => true).length === 0, { http: r409 && r409.status, definicao_mudou: r409?.corpo?.conflito?.definicao_mudou, tri: c409.tri });
    await p.$eval('#gaveta-no .erro-acao', el => el.scrollIntoView({ block: 'center' })); await espera(300);
    await capturar(p, 'conflito-409-null-1600x900');
    await clicar(p, '[data-foco="adotar-max_celulas_novas_por_onda"]'); await espera(1500);
    const ainda = await p.$eval('[data-foco="num-max_celulas_novas_por_onda"]', el => el.value);
    await clicar(p, '[data-foco="pedir-max_celulas_novas_por_onda"]'); await espera(1600);
    novos = novoNaCaixa(antes, d => d.corpo.operacao === 'mudar-controle' && d.corpo.controle === 'max_celulas_novas_por_onda');
    ok('"Propor sobre o valor atual" grava 150 → 200', ainda === '200' && novos.length === 1 && novos[0].d.corpo.antes.valor === 150 && novos[0].d.corpo.depois.valor === 200, novos[0] && novos[0].d.corpo);

    // 8. 409 com definicao_mudou true: a faixa do botão encolhe e o pedido não cabe mais nela
    await ir(p, '#/lacos/pesquisa-de-regas?no=parada', 3000);
    await digitar(p, '[data-foco="num-gate_novos"]', '40');
    const faixa = lerJson(lacoJson); faixa.controles.find(c => c.id === 'gate_novos').faixa = [0.01, 0.3]; gravarJson(lacoJson, faixa);
    antes = nomes();
    await clicar(p, '[data-foco="pedir-gate_novos"]'); await espera(1500);
    const t409 = await p.evaluate(() => document.querySelector('#gaveta-no .erro-acao')?.innerText);
    const r409b = respostas[respostas.length - 1];
    ok('409 true: "a regra deste botão mudou"', r409b && r409b.status === 409 && r409b.corpo?.conflito?.definicao_mudou === true && /regra deste botão mudou/.test(t409 || '') && novoNaCaixa(antes, () => true).length === 0, { http: r409b && r409b.status, corpo: r409b && r409b.corpo, texto: t409 });
    await p.$eval('#gaveta-no .erro-acao', el => el.scrollIntoView({ block: 'center' })); await espera(300);
    await capturar(p, 'conflito-409-true-1600x900');
    fs.writeFileSync(lacoJson, lacoOriginal, 'utf8');

    // 9. erro ambíguo (rede): "tentar de novo" reenvia o MESMO envio, e a caixa guarda um arquivo só
    await ir(p, '#/lacos/pesquisa-de-regas?no=despachante', 3000);
    await p.setRequestInterception(true);
    let derrubar = true; const enviosVistos = [];
    const intercepta = req => { if (req.url().endsWith('/api/caixa') && req.method() === 'POST') { enviosVistos.push(JSON.parse(req.postData()).envio); if (derrubar) { derrubar = false; return req.abort('failed'); } } req.continue(); };
    p.on('request', intercepta);
    await digitar(p, '[data-foco="com-no:pesquisa-de-regas:regas-2026-10-14:despachante-texto"]', 'a rede caiu aqui', false);
    antes = nomes();
    await clicar(p, '[data-foco="com-no:pesquisa-de-regas:regas-2026-10-14:despachante-enviar"]'); await espera(1200);
    const rotulo = await texto(p, '[data-foco="com-no:pesquisa-de-regas:regas-2026-10-14:despachante-enviar"]');
    await capturar(p, 'rede-caiu-1600x900');
    await clicar(p, '[data-foco="com-no:pesquisa-de-regas:regas-2026-10-14:despachante-enviar"]'); await espera(1600);
    novos = novoNaCaixa(antes, d => d.corpo.operacao === 'comentario-no' && d.corpo.no === 'despachante');
    ok('rede caiu → "Tentar de novo" com o mesmo envio; um arquivo só', /Tentar de novo/.test(rotulo || '') && enviosVistos.length === 2 && enviosVistos[0] === enviosVistos[1] && novos.length === 1 && novos[0].d.envio === enviosVistos[0], { rotulo, enviosVistos, arquivos: novos.map(x => x.f) });
    p.off('request', intercepta); await p.setRequestInterception(false);

    // 10. o maestro marca um pedido em conflito e grava um recibo inválido noutro (só na cópia): espera você, envelope
    // cheio no nó, "Propor de novo"; recibo inválido em tijolo, nunca "aplicado"
    const md = n => path.join(CAIXA, `${n}.md`);
    const trocarFrente = (n, campos) => { let s = fs.readFileSync(md(n), 'utf8'); for (const [k, v] of Object.entries(campos)) s = s.replace(new RegExp(`^${k}:.*$`, 'm'), `${k}: ${v}`); fs.writeFileSync(md(n), s, 'utf8'); };
    trocarFrente(arqMudar, { estado: 'conflito', agora_esta: '{"tipo": "inteiro", "valor": 22}' });
    trocarFrente(arqParada, { estado: 'aplicado', aplicado_em: '2026-10-14T20:00:00-03:00' });
    avivar();
    await ir(p, '#/lacos', 6000); // a casca vê o .md mudado em até 3 s e a tela relê o laço na hora
    const esp = await p.evaluate(() => ({ grupo: [...document.querySelectorAll('.grupo-lacos')][0].innerText, faixa: document.querySelector('.espera-voce')?.innerText, envelope: !!document.querySelector('[data-foco="no-geradores"] .envelope-no.conflito'), contador: document.getElementById('contador').innerText.replace(/\s+/g, ' ') }));
    const cartoes = await p.$$eval('.pedidos-laco .cartao-pedido', els => els.map(e => ({ o: e.querySelector('.pedido-o-que').innerText, estado: e.querySelector('.estado-pedido').innerText, tri: [...e.querySelectorAll('.conflito-tri b')].map(b => b.innerText), propor: !!e.querySelector('[data-foco^="propor-"]'), erros: [...e.querySelectorAll('.erros-recibo li')].map(li => li.innerText) })));
    const cf = cartoes.find(c => c.estado === 'conflito'); const inv = cartoes.find(c => /recibo inválido/.test(c.estado));
    ok('conflito atual: grupo "espera você", envelope cheio, "você viu 20 · agora está 22 · você pediu 24", Propor de novo', /Pesquisa de horários/.test(esp.grupo) && /em conflito/.test(esp.faixa || '') && esp.envelope && cf && cf.tri.join('|') === '20 trabalhadores|22 trabalhadores|24 trabalhadores' && cf.propor, { esp, cf });
    ok('recibo inválido em tijolo, nunca "aplicado"', inv && inv.erros.length > 0, inv);
    ok('contador do topo segue o contrato (rodadas + cartas)', /^1 ?aguardando você/.test(esp.contador), { contador: esp.contador });
    await capturar(p, 'espera-voce-1600x900'); await capturar(p, 'espera-voce-1600-inteira', true);
    const lz2 = await p.evaluate(LIMPEZA);
    ok('fluxo limpo também com envelopes e conflito', limpo(lz2) && lz2.folgaEnvelopes.length >= 2, lz2);
    await clicar(p, `.pedidos-laco [data-foco^="propor-"]`); await espera(1800);
    const propor = await p.evaluate(() => ({ rota: location.hash, valor: document.querySelector('[data-foco="num-trabalhadores_por_gerador"]')?.value, substitui: document.querySelector('#gaveta-no .nota-substitui')?.innerText }));
    ok('Propor de novo abre o nó com o valor pedido e liga ao pedido em conflito', /no=geradores/.test(propor.rota) && propor.valor === '24' && /substitui/.test(propor.substitui || ''), propor);
    antes = nomes();
    await clicar(p, '[data-foco="pedir-trabalhadores_por_gerador"]'); await espera(1600);
    novos = novoNaCaixa(antes, d => d.corpo.operacao === 'mudar-controle');
    ok('o envio novo substitui o pedido em conflito', novos.length === 1 && novos[0].d.corpo.substitui === arqMudar && novos[0].d.corpo.antes.valor === 20, novos[0] && novos[0].d.corpo);
    await p.keyboard.press('Escape'); await espera(600);

    // 11. laço terminado: só leitura (sem botões de pedido nem proposta), comentário continua
    await ir(p, '#/lacos/censo-de-sementes', 3000);
    const term = await p.evaluate(() => ({ botoes: [...document.querySelectorAll('.laco-acoes button')].map(b => b.innerText), soLeitura: document.querySelector('.so-leitura')?.innerText, comentario: !!document.querySelector('.comentario-laco textarea') }));
    await clicar(p, '[data-foco="no-parada"]'); await espera(900);
    const termGav = await p.evaluate(() => ({ propostas: document.querySelectorAll('#gaveta-no .proposta-no').length, cfg: document.querySelector('#gaveta-no .linha-cfg')?.innerText, comentario: !!document.querySelector('#gaveta-no .comentario-form textarea') }));
    ok('terminado: sem botões de pedido nem proposta; comentário continua', term.botoes.length === 0 && /só leitura/.test(term.soLeitura || '') && term.comentario && termGav.propostas === 0 && /configurado/.test(termGav.cfg || '') && termGav.comentario, { term, termGav });
    await capturar(p, 'terminado-gaveta-1600x900');
    await p.keyboard.press('Escape'); await espera(500);
    await capturar(p, 'terminado-1600x900');
    const lz3 = await p.evaluate(LIMPEZA);
    ok('fluxo limpo no laço terminado', limpo(lz3), lz3);

    // 11b. laço malformado (só na cópia): a linha fica na lista com o selo e o erro; o detalhe diz em palavras, sem botões
    const semJson = path.join(COPIA, 'lacos', 'sementes', 'laco.json'); const semOriginal = fs.readFileSync(semJson, 'utf8');
    const quebrado = JSON.parse(semOriginal); quebrado.ligacoes[0].de = []; gravarJson(semJson, quebrado);
    await ir(p, '#/lacos/censo-de-sementes', 6000);
    const mal = await p.evaluate(() => ({ selo: document.querySelector('.item-laco.malformado .selo-laco')?.innerText, aviso: document.querySelector('.laco-aberto .aviso-rodada')?.innerText, botoes: document.querySelectorAll('.laco-aberto button, .laco-aberto textarea').length, outro: !!document.querySelector('.item-laco.g-em-voo') }));
    ok('malformado: selo na lista, erro em palavras, sem botões nem comentário; o outro laço intacto', /malformado/.test(mal.selo || '') && /fora do contrato/.test(mal.aviso || '') && mal.botoes === 0 && mal.outro, mal);
    await capturar(p, 'malformado-1600x900');
    fs.writeFileSync(semJson, semOriginal, 'utf8');

    // 12. 1280×800
    await p.setViewport({ width: 1280, height: 800 });
    avivar();
    await ir(p, '#/lacos/pesquisa-de-regas', 3000);
    const m2 = await medir(p);
    ok('fonte mínima 14 px e sem rolagem horizontal da página (1280)', m2.menorFonte >= 14 && !m2.rolagemHorizontal, m2);
    await capturar(p, 'lacos-1280x800'); await capturar(p, 'lacos-1280-inteira', true);
    const aviso1280 = await p.evaluate(() => { const m = document.querySelector('.fluxo-moldura'); return { transborda: m.classList.contains('transborda'), selo: getComputedStyle(m.querySelector('.rola-aviso')).display }; });
    ok('1280: o fluxo que não cabe mostra que continua (borda esmaecida + "rola →")', !aviso1280.transborda || aviso1280.selo !== 'none', aviso1280);
    await clicar(p, '[data-foco="no-teto"]'); await espera(900);
    await capturar(p, 'gaveta-teto-1280x800');
    const m3 = await medir(p);
    ok('gaveta em 1280: fonte mínima 14 px', m3.menorFonte >= 14, m3);
    await p.keyboard.press('Escape'); await espera(500);

    ok('zero erros de JS', prova.erros_js.length === 0, { erros: prova.erros_js });
  } catch (e) {
    prova.excecao = String(e && e.stack || e); console.log('EXCEÇÃO', e);
  } finally {
    prova.tudo_ok = !prova.excecao && Object.values(prova.passos).every(x => x.ok);
    fs.writeFileSync(path.join(SAIDA, 'prova.json'), JSON.stringify(prova, null, 2), 'utf8');
    await b.close();
  }
})();
