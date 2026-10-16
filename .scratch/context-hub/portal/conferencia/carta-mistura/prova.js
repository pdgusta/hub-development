// Portal REAL (porta 8770), só leitura: a carta da mistura no leitor e sozinha, em 1280 e 320, com um cenário
// acionado dentro dela. Bloqueia qualquer POST (nada é gravado na caixa real). Uso: node prova.js <pasta com puppeteer-core>
const puppeteer = require(require('path').join(process.argv[2], 'puppeteer-core'));
const fs = require('fs'); const path = require('path');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const PERFIL = path.join(process.env.TEMP || 'C:/Temp', 'carta-mistura-edge-perfil');
const BASE = 'http://127.0.0.1:8770/';
const espera = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  fs.rmSync(PERFIL, { recursive: true, force: true });
  const b = await puppeteer.launch({ executablePath: EDGE, headless: 'new', userDataDir: PERFIL, args: ['--disable-gpu', '--hide-scrollbars'] });
  const res = { quando: new Date().toISOString(), capturas: [], medidas: {}, erros_js: [], posts_bloqueados: 0 };
  try {
    const p = await b.newPage();
    await p.setRequestInterception(true);
    p.on('request', r => { if (r.method() !== 'GET') { res.posts_bloqueados++; return r.abort(); } r.continue(); });
    p.on('response', r => { if (r.status() >= 400 && !/favicon/.test(r.url())) res.erros_js.push(r.status() + ' ' + r.url()); });
    p.on('pageerror', e => res.erros_js.push(String(e)));
    p.on('console', m => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) res.erros_js.push('console: ' + m.text()); });
    const foto = async (arq) => { await p.screenshot({ path: path.join(__dirname, arq) }); res.capturas.push(arq); };
    const peca = () => p.frames().find(f => /\/mistura\.html$/.test(f.url()));
    const cenario = async (nome) => {
      const f = peca(); if (!f) return 'sem quadro da mistura';
      await f.evaluate(n => document.querySelector(`[data-cen="${n}"]`).scrollIntoView({ block: 'center' }), nome); await espera(300);
      // clique pelo DOM: o quadro está reduzido por transform, e o clique por coordenada do puppeteer não o alcança
      await f.evaluate(n => document.querySelector(`[data-cen="${n}"]`).click(), nome); await espera(400);
      await f.evaluate(() => document.getElementById('cen-prox').scrollIntoView({ block: 'center' })); await espera(200);
      for (let i = 0; i < 2; i++) { await f.evaluate(() => document.getElementById('cen-prox').click()); await espera(300); }
      await f.evaluate(() => window.scrollTo(0, 0)); await espera(400);
      return f.evaluate(() => (document.querySelector('.cen-passo') || {}).innerText || '');
    };
    // sozinha, página inteira
    for (const w of [1280, 320]) {
      await p.setViewport({ width: w, height: 900 });
      await p.goto(BASE + 'carta/mistura-da-cidade/', { waitUntil: 'networkidle0' }); await espera(1500);
      const m = await p.evaluate(() => ({
        rolagemHorizontal: document.documentElement.scrollWidth > document.documentElement.clientWidth,
        altura: document.documentElement.scrollHeight,
        palco: document.getElementById('palco').getBoundingClientRect().height,
        menorFonte: Math.min(...[...document.querySelectorAll('body *')].filter(el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && el.getBoundingClientRect().width).map(el => parseFloat(getComputedStyle(el).fontSize)))
      }));
      res.medidas[`sozinha-${w}`] = m;
      await p.setViewport({ width: w, height: m.altura }); await espera(800);
      await foto(`sozinha-${w}-inteira.png`);
    }
    // no leitor do portal, normal e com um cenário no passo 3
    for (const [w, h] of [[1280, 800], [320, 800]]) {
      await p.setViewport({ width: w, height: h });
      await p.goto(BASE + '#/cartas/mistura-da-cidade', { waitUntil: 'networkidle0' }); await espera(3000);
      await foto(`leitor-${w}x${h}.png`);
      res.medidas[`leitor-${w}`] = { topo: await p.evaluate(() => (document.querySelector('.contador') || {}).innerText || null) };
      const carta = p.frames().find(f => /\/carta\/mistura-da-cidade\/$/.test(f.url()));
      if (carta) await carta.evaluate(() => document.getElementById('palco').scrollIntoView({ block: 'start' }));
      await espera(800);
      res.medidas[`leitor-${w}`].cenario = await cenario('gustavo-edita');
      await espera(400);
      await foto(`leitor-${w}x${h}-cenario.png`);
    }
  } finally { await b.close(); }
  fs.writeFileSync(path.join(__dirname, 'prova.json'), JSON.stringify(res, null, 1));
  console.log(JSON.stringify(res, null, 1));
})();
