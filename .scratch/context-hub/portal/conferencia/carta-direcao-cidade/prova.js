// Portal REAL (porta 8770), só leitura: a carta da direção visual da cidade no leitor e sozinha, em 1280 e 320.
// Bloqueia qualquer POST (nada é gravado na caixa real). Uso: node prova.js <pasta com puppeteer-core>
const puppeteer = require(require('path').join(process.argv[2], 'puppeteer-core'));
const fs = require('fs'); const path = require('path');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const PERFIL = path.join(process.env.TEMP || 'C:/Temp', 'carta-cidade-edge-perfil');
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
    // sozinha, página inteira, nos dois tamanhos e nas três escolhas
    for (const w of [1280, 320]) {
      await p.setViewport({ width: w, height: 900 });
      await p.goto(BASE + 'carta/direcao-visual-cidade/', { waitUntil: 'networkidle0' }); await espera(1500);
      for (const c of ['a', 'b', 'c']) {
        await p.click(`[data-c="${c}"]`); await espera(1800);
        const m = await p.evaluate(() => ({
          rolagemHorizontal: document.documentElement.scrollWidth > document.documentElement.clientWidth,
          altura: document.documentElement.scrollHeight,
          palco: document.getElementById('palco').getBoundingClientRect().height,
          ideia: document.getElementById('f-ideia').textContent,
          selecionada: document.querySelector('[aria-selected="true"]').dataset.c,
          menorFonte: Math.min(...[...document.querySelectorAll('body *')].filter(el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && el.getBoundingClientRect().width).map(el => parseFloat(getComputedStyle(el).fontSize)))
        }));
        res.medidas[`sozinha-${w}-${c}`] = m;
        await p.setViewport({ width: w, height: m.altura }); await espera(800);
        await foto(`sozinha-${w}-${c}-inteira.png`);
        await p.setViewport({ width: w, height: 900 }); await espera(300);
      }
    }
    // no leitor do portal e na grade de Designs
    for (const [w, h] of [[1280, 800], [320, 800]]) {
      await p.setViewport({ width: w, height: h });
      await p.goto(BASE + '#/cartas/direcao-visual-cidade', { waitUntil: 'networkidle0' }); await espera(3000);
      await foto(`leitor-${w}x${h}.png`);
      res.medidas[`leitor-${w}`] = await p.evaluate(() => ({ rolagemHorizontal: document.documentElement.scrollWidth > document.documentElement.clientWidth, topo: (document.querySelector('.contador') || {}).innerText || null }));
      if (w === 320) { // comparação: outra carta no mesmo leitor
        await p.goto(BASE + '#/cartas/mapeamento', { waitUntil: 'networkidle0' }); await espera(2500);
        res.medidas['leitor-320-outra-carta'] = await p.evaluate(() => ({ rolagemHorizontal: document.documentElement.scrollWidth > document.documentElement.clientWidth }));
      }
      await p.goto(BASE + '#/cartas', { waitUntil: 'networkidle0' }); await espera(2500);
      await foto(`grade-${w}x${h}.png`);
    }
  } finally { await b.close(); }
  fs.writeFileSync(path.join(__dirname, 'prova.json'), JSON.stringify(res, null, 1));
  console.log(JSON.stringify(res, null, 1));
})();
