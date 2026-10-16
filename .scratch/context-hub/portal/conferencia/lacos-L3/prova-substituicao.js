// Prova da recuperação da substituição (revisão do Prumo, 2026-10-15), numa CÓPIA da fixture na porta 8775.
// uso: node prova-substituicao.js <pasta da cópia>   (junta o resultado em prova.json, chave "substituicao")
// Caso do Prumo: Juntador 120→200, depois 120→250 (substitui o primeiro); começa 300; o maestro RECUSA o de 250 antes
// do envio. A tela não pode ficar presa à referência recusada: diz em palavras o que houve e oferece "Enviar como pedido
// novo" (UUID novo, sem referência), preservando valor e texto, também depois de recarregar. Também o 400 real
// `substitui-invalido` (a tela forçada a ver o laço antigo), parada, e pausa/retomada (capacidade posta só na cópia).
const puppeteer = require('puppeteer-core');
const fs = require('fs'); const path = require('path');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const COPIA = process.argv[2];
const BASE = 'http://127.0.0.1:8775/';
const PERFIL = path.join(process.env.TEMP || 'C:/Temp', 'l3-edge-perfil-subst');
const CAIXA = path.join(COPIA, 'portal', 'caixa');
const REGAS = path.join(COPIA, 'lacos', 'regas');
const espera = ms => new Promise(r => setTimeout(r, ms));
const res = { quando: new Date().toISOString(), passos: {}, erros_js: [], capturas: [] };
const ok = (nome, cond, extra) => { res.passos[nome] = { ok: !!cond, ...(extra || {}) }; console.log(`${cond ? 'OK ' : 'FALHOU'} ${nome}${extra ? ' ' + JSON.stringify(extra).slice(0, 400) : ''}`); };
const jsons = () => fs.readdirSync(CAIXA).filter(f => f.endsWith('.json') && f.includes('alteracao-laco')).map(f => ({ f: f.replace(/\.json$/, ''), d: JSON.parse(fs.readFileSync(path.join(CAIXA, f), 'utf8')) }));
const nomes = () => new Set(jsons().map(x => x.f));
const novos = (antes, filtro) => jsons().filter(x => !antes.has(x.f) && filtro(x.d));
// a máquina pode estar carregada: espera a condição (até 12 s) em vez de um tempo fixo
const aguardar = async (fn, ms = 12000) => { const fim = Date.now() + ms; let v; while (!(v = await fn()) && Date.now() < fim) await espera(300); return v; };
const novoArquivo = (antes, filtro) => aguardar(() => novos(antes, filtro)[0]);
const avivar = () => { const t = Date.now() / 1000; for (const n of ['manha.jsonl', 'tarde.jsonl']) fs.utimesSync(path.join(REGAS, 'livros', n), t, t); };
// o maestro dá o desfecho no .md (como faria): estado recusado, com motivo
const recusar = (nome, motivo) => { const p = path.join(CAIXA, `${nome}.md`); let s = fs.readFileSync(p, 'utf8'); s = s.replace(/^estado:.*$/m, 'estado: recusado').replace(/^motivo:.*$/m, `motivo: ${motivo}`); fs.writeFileSync(p, s, 'utf8'); };

(async () => {
  fs.rmSync(PERFIL, { recursive: true, force: true });
  avivar();
  const b = await puppeteer.launch({ executablePath: EDGE, headless: 'new', userDataDir: PERFIL, args: ['--disable-gpu', '--hide-scrollbars'] });
  try {
    const p = await b.newPage();
    p.on('pageerror', e => res.erros_js.push(String(e)));
    p.on('console', m => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) res.erros_js.push('console: ' + m.text()); });
    const posts = [];
    p.on('response', async r => { if (r.url().endsWith('/api/caixa') && r.request().method() === 'POST') { let c = null; try { c = await r.json(); } catch {} posts.push({ status: r.status(), corpo: c, pedido: JSON.parse(r.request().postData() || '{}') }); } });
    await p.setViewport({ width: 1600, height: 900 });
    const clicar = async sel => { for (let i = 0; ; i++) { try { await p.waitForSelector(sel, { visible: true, timeout: 8000 }); await p.waitForFunction(() => !document.querySelector('#brisa .sopro'), { timeout: 8000 }); await p.click(sel); return; } catch (e) { if (i >= 2 || !/detached|not clickable/i.test(String(e))) throw e; await espera(400); } } };
    const digitar = async (sel, texto, limpar = true) => { await p.waitForSelector(sel, { visible: true, timeout: 8000 }); if (limpar) await p.$eval(sel, el => { el.focus(); el.select && el.select(); }); else await p.focus(sel); await p.keyboard.type(texto); };
    const capturar = async (nome, sel) => { if (sel) await p.$eval(sel, el => el.scrollIntoView({ block: 'center' })).catch(() => {}); await espera(300); await p.screenshot({ path: path.join(__dirname, `${nome}.png`) }); res.capturas.push(`${nome}.png`); };
    const NUM = '[data-foco="num-max_celulas_novas_por_onda"]', PEDIR = '[data-foco="pedir-max_celulas_novas_por_onda"]', TXT = '[data-foco="por-que-max_celulas_novas_por_onda"]';
    const REC = '[data-foco^="rec-max_celulas_novas_por_onda-"]';
    const bloco = () => p.evaluate(() => document.querySelector('.recuperar-subst')?.innerText || null);
    const rascunho = () => p.evaluate(() => { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k.includes(':laco:pesquisa-de-regas:')) return JSON.parse(localStorage.getItem(k)); } return null; });

    // ---- A. o caso do Prumo, detectado antes de enviar (o maestro recusa enquanto o Gustavo escreve)
    await p.goto(BASE + '#/lacos/pesquisa-de-regas?no=juntador', { waitUntil: 'networkidle0' }); await espera(3000);
    let antes = nomes();
    await digitar(NUM, '200'); await clicar(PEDIR); await espera(1800);
    const p1 = await novoArquivo(antes, d => d.corpo.controle === 'max_celulas_novas_por_onda');
    antes = nomes();
    await digitar(NUM, '250'); await espera(300);
    const nota = await p.evaluate(() => document.querySelector('#gaveta-no .nota-substitui')?.innerText || null);
    await clicar(PEDIR); await espera(1800);
    const p2 = await novoArquivo(antes, d => d.corpo.controle === 'max_celulas_novas_por_onda');
    ok('A1: 120→200 e 120→250; o segundo substitui o primeiro, dito em palavras', p1 && p2 && p2.d.corpo.substitui === p1.f && !p1.d.corpo.substitui && /substitui o seu pedido anterior/.test(nota || ''), { p1: p1?.f, p2: p2?.f, substitui: p2?.d.corpo.substitui, nota });
    await digitar(NUM, '300'); await espera(600); res.rascunho_apos_300 = (await rascunho())?.controles?.max_celulas_novas_por_onda; await digitar(TXT, 'terceira tentativa', false); await espera(600); res.rascunho_apos_texto = (await rascunho())?.controles?.max_celulas_novas_por_onda;
    const envioDoRascunho = (await rascunho())?.controles?.max_celulas_novas_por_onda?.envio;
    const postsAntes = posts.length;
    recusar(p2.f, 'fora da janela de teste');
    await aguardar(bloco, 15000); // a casca vê o .md mudado e a tela relê o laço
    const blocoA = await bloco();
    ok('A2: recusa antes do envio → a tela diz em palavras e oferece "Enviar como pedido novo", sem enviar nada', /já teve desfecho: recusado/.test(blocoA || '') && /fora da janela de teste/.test(blocoA || '') && /Enviar como pedido novo/.test(blocoA || '') && posts.length === postsAntes, { blocoA, posts: posts.length - postsAntes });
    await capturar('subst-A-recusado-antes-de-enviar-1600x900', '.recuperar-subst');
    // clicar "Pedir ao maestro" direto também não envia com a referência velha
    await clicar(PEDIR); await espera(1200);
    ok('A3: "Pedir ao maestro" com o alvo vencido não envia (mostra a escolha)', posts.length === postsAntes && !!(await bloco()), { posts: posts.length - postsAntes });
    // recarga: o rascunho guardado não ressuscita a referência; valor e texto preservados
    await p.reload({ waitUntil: 'networkidle0' }); await espera(3500);
    const recarga = await p.evaluate((NUM, TXT) => ({ valor: document.querySelector(NUM)?.value, texto: document.querySelector(TXT)?.value, bloco: document.querySelector('.recuperar-subst')?.innerText || null }), NUM, TXT);
    const rasc = (await rascunho())?.controles?.max_celulas_novas_por_onda;
    ok('A4: depois de recarregar, a escolha continua, valor 300 e texto preservados, sem referência guardada', recarga.valor === '300' && recarga.texto === 'terceira tentativa' && /Enviar como pedido novo/.test(recarga.bloco || '') && rasc && !('substitui' in rasc && rasc.substitui), { recarga, rascunho: rasc });
    await capturar('subst-A-depois-da-recarga-1600x900', '.recuperar-subst');
    antes = nomes();
    await clicar('[data-foco="rec-max_celulas_novas_por_onda-novo"]');
    await espera(2000);
    const p3 = await novoArquivo(antes, d => d.corpo.controle === 'max_celulas_novas_por_onda');
    const ultimoA = posts[posts.length - 1];
    ok('A5: "Enviar como pedido novo" → 200 com UUID novo, sem substituir o recusado, valor e texto preservados', p3 && ultimoA.status === 200 && !p3.d.corpo.substitui && p3.d.corpo.depois.valor === 300 && p3.d.corpo.texto === 'terceira tentativa' && p3.d.envio !== envioDoRascunho && await aguardar(async () => !(await bloco())), { p3: p3?.f, envio_novo: p3?.d.envio, envio_do_rascunho: envioDoRascunho, corpo: p3?.d.corpo });

    // ---- B. o 400 real `substitui-invalido`: a tela é forçada a ver o laço antigo (pedido ainda aberto) até o POST
    await digitar(NUM, '350'); await espera(400); // alvo visto: o pedido de 300, aberto
    const velho = await p.evaluate(async () => (await fetch('/api/laco/pesquisa-de-regas', { headers: { 'X-Torre': '1' } })).text());
    await p.setRequestInterception(true);
    let antigo = true;
    const intercepta = req => {
      if (req.method() === 'POST' && req.url().endsWith('/api/caixa')) { antigo = false; return req.continue(); }
      if (antigo && req.method() === 'GET' && /\/api\/laco\/pesquisa-de-regas$/.test(req.url())) return req.respond({ status: 200, contentType: 'application/json', body: velho });
      req.continue();
    };
    p.on('request', intercepta);
    recusar(p3.f, 'já basta uma onda');
    await espera(4000);
    const n400 = posts.length;
    await clicar(PEDIR); await espera(2500);
    const r400 = posts[n400];
    const blocoB = await bloco();
    p.off('request', intercepta); await p.setRequestInterception(false);
    ok('B1: 400 `substitui-invalido` vira explicação em palavras e a escolha (relidos os pedidos)', r400 && r400.status === 400 && r400.corpo?.erro === 'substitui-invalido' && r400.pedido.substitui === p3.f && /já teve desfecho: recusado/.test(blocoB || '') && /já basta uma onda/.test(blocoB || ''), { http: r400?.status, erro: r400?.corpo?.erro, blocoB });
    await capturar('subst-B-400-recuperacao-1600x900', '.recuperar-subst');
    antes = nomes();
    await clicar('[data-foco="rec-max_celulas_novas_por_onda-novo"]'); await espera(2000);
    const p4 = await novoArquivo(antes, d => d.corpo.controle === 'max_celulas_novas_por_onda');
    ok('B2: o reenvio sai com UUID novo, sem referência, valor 350', p4 && !p4.d.corpo.substitui && p4.d.corpo.depois.valor === 350 && p4.d.envio !== r400.pedido.envio, { p4: p4?.f, envio_400: r400?.pedido.envio, envio_novo: p4?.d.envio });
    await p.keyboard.press('Escape'); await espera(600);

    // ---- C. parada: o segundo pedido de parada substitui o primeiro; o maestro recusa o primeiro antes do envio
    await p.goto(BASE + '#/lacos/pesquisa-de-regas', { waitUntil: 'networkidle0' }); await espera(3000);
    await clicar('[data-foco="pedir-parada"]'); await espera(600);
    await clicar('[data-foco="cap-parar-de-despachar"]');
    antes = nomes();
    await clicar('[data-foco="parada-enviar"]'); await espera(1800);
    const q1 = await novoArquivo(antes, d => d.corpo.operacao === 'pedir-parada');
    await clicar('[data-foco="pedir-parada"]'); await espera(800);
    const notaParada = await p.evaluate(() => document.querySelector('.nota-substitui')?.innerText || null);
    await p.$eval('[data-foco="onda-alvo"]', el => { el.value = ''; }); await digitar('[data-foco="onda-alvo"]', '4');
    const nC = posts.length;
    recusar(q1.f, 'a onda 2 ainda não fechou');
    await aguardar(bloco, 15000);
    const blocoC = await bloco();
    ok('C1: parada — recusa do pedido anterior antes do envio vira escolha em palavras', q1 && /substitui o seu pedido anterior/.test(notaParada || '') && /já teve desfecho: recusado/.test(blocoC || '') && posts.length === nC, { notaParada, blocoC });
    await capturar('subst-C-parada-1600x900', '.recuperar-subst');
    antes = nomes();
    await clicar('[data-foco="rec-parada-novo"]'); await espera(2000);
    const q2 = await novoArquivo(antes, d => d.corpo.operacao === 'pedir-parada');
    ok('C2: parada sai como pedido novo, sem referência, depois da onda 4', q2 && !q2.d.corpo.substitui && q2.d.corpo.onda === 4 && q2.d.envio !== q1.d.envio, { q2: q2?.d.corpo });

    // ---- D. pausa e retomada (capacidade posta só na cópia): retomada substituiria a pausa recusada
    const lacoJson = path.join(REGAS, 'laco.json'); const L = JSON.parse(fs.readFileSync(lacoJson, 'utf8'));
    L.capacidades.push({ id: 'pausar-retomar' }); fs.writeFileSync(lacoJson, JSON.stringify(L, null, 2), 'utf8');
    await p.goto(BASE + '#/lacos/pesquisa-de-regas', { waitUntil: 'networkidle0' }); await espera(4000);
    // a parada aberta (q2) é substituída pela pausa, dito em palavras
    await clicar('[data-foco="pedir-pausa"]'); await espera(800);
    const notaPausa = await p.evaluate(() => document.querySelector('.nota-substitui')?.innerText || null);
    antes = nomes();
    await clicar('[data-foco="parada-enviar"]'); await espera(1800);
    const r1 = await novoArquivo(antes, d => d.corpo.operacao === 'pedir-pausa');
    await clicar('[data-foco="pedir-retomada"]'); await espera(800);
    await digitar('[data-foco="parada-texto"]', 'retomar só depois do almoço', false);
    const nD = posts.length;
    recusar(r1.f, 'o laço não estava pausável agora');
    await aguardar(bloco, 15000);
    const blocoD = await bloco();
    ok('D1: pausa substitui a parada (dito); retomada com a pausa recusada vira escolha em palavras', r1 && r1.d.corpo.substitui === q2.f && /substitui o seu pedido anterior/.test(notaPausa || '') && /já teve desfecho: recusado/.test(blocoD || '') && posts.length === nD, { notaPausa, blocoD });
    await capturar('subst-D-retomada-1600x900', '.recuperar-subst');
    antes = nomes();
    await clicar('[data-foco="rec-parada-novo"]'); await espera(2000);
    const r2 = await novoArquivo(antes, d => d.corpo.operacao === 'pedir-retomada');
    ok('D2: retomada sai como pedido novo, sem referência, texto preservado', r2 && !r2.d.corpo.substitui && r2.d.corpo.texto === 'retomar só depois do almoço', { r2: r2?.d.corpo });

    ok('zero erros de JS', res.erros_js.length === 0, { erros: res.erros_js });
  } catch (e) {
    res.excecao = String(e && e.stack || e); console.log('EXCEÇÃO', e);
  } finally {
    res.tudo_ok = !res.excecao && Object.values(res.passos).every(x => x.ok);
    const pj = path.join(__dirname, 'prova.json');
    const prova = fs.existsSync(pj) ? JSON.parse(fs.readFileSync(pj, 'utf8')) : {};
    prova.substituicao = res;
    fs.writeFileSync(pj, JSON.stringify(prova, null, 2), 'utf8');
    await b.close();
  }
})();
