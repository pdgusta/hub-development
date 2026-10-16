// Portal REAL (porta 8770), só leitura: a carta do esboço da árvore (ticket 12) no leitor e sozinha, em 1280 e 320,
// abrindo notas de exemplo. Bloqueia qualquer POST (nada é gravado na caixa real). Uso: node prova.js <pasta com puppeteer-core>
const puppeteer = require(require('path').join(process.argv[2], 'puppeteer-core'));
const fs = require('fs'); const path = require('path');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const PERFIL = path.join(process.env.TEMP || 'C:/Temp', 'carta-12-arvore-edge-perfil');
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
    const medir = () => p.evaluate(() => ({
      rolagemHorizontal: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      altura: document.documentElement.scrollHeight,
      fonte: getComputedStyle(document.querySelector('h1')).fontFamily,
      menorFonte: Math.min(...[...document.querySelectorAll('body *')].filter(el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && el.getBoundingClientRect().width).map(el => parseFloat(getComputedStyle(el).fontSize))),
      aberta: document.getElementById('l-caminho').textContent
    }));
    for (const w of [1280, 320]) {
      for (const nota of ['initiative', 'pdfmd', 'index-brutos', 'work']) {
        await p.setViewport({ width: w, height: 900 });
        await p.goto(BASE + 'carta/prototipo-12-arvore/', { waitUntil: 'networkidle0' }); await espera(800);
        await p.evaluate(n => document.querySelector(`[data-nota="${n}"]`).click(), nota); await espera(500);
        const m = await medir(); res.medidas[`sozinha-${w}-${nota}`] = m;
        if (nota === 'initiative' || w === 1280) {
          await p.setViewport({ width: w, height: m.altura }); await espera(600);
          await foto(`sozinha-${w}-${nota}-inteira.png`);
        }
      }
    }
    for (const [w, h] of [[1280, 800], [320, 800]]) {
      await p.setViewport({ width: w, height: h });
      await p.goto(BASE + '#/cartas/prototipo-12-arvore', { waitUntil: 'networkidle0' }); await espera(3000);
      await foto(`leitor-${w}x${h}.png`);
      const carta = p.frames().find(f => /\/carta\/prototipo-12-arvore\/$/.test(f.url()));
      res.medidas[`leitor-${w}`] = carta ? await carta.evaluate(() => ({ rolagemHorizontal: document.documentElement.scrollWidth > document.documentElement.clientWidth, fonte: getComputedStyle(document.querySelector('h1')).fontFamily })) : 'sem quadro';
      if (carta) { await carta.evaluate(() => document.querySelector('[data-nota="retomada"]').click()); await espera(800); await foto(`leitor-${w}x${h}-retomada.png`); }
    }
  } finally { await b.close(); }
  fs.writeFileSync(path.join(__dirname, 'prova.json'), JSON.stringify(res, null, 1));
  console.log(JSON.stringify(res, null, 1));
})();
