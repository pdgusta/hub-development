// uso: node mede.js <pasta-saida> [sufixo]
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const URL = 'http://127.0.0.1:8765/amostra-inicio.html';
const out = process.argv[2]; const suf = process.argv[3] || '';
fs.mkdirSync(out, { recursive: true });
(async () => {
  const b = await puppeteer.launch({ executablePath: fs.existsSync(EDGE) ? EDGE : 'C:/Program Files/Microsoft/Edge/Application/msedge.exe', headless: 'new', args: ['--disable-gpu', '--hide-scrollbars'] });
  const erros = [];
  for (const [w, h] of [[1600, 900], [1280, 800]]) {
    const p = await b.newPage(); p.on('pageerror', e => erros.push(String(e))); p.on('console', m => m.type() === 'error' && erros.push(m.text()));
    await p.setViewport({ width: w, height: h });
    await p.goto(URL + '?v=' + Date.now(), { waitUntil: 'networkidle0' });
    await new Promise(r => setTimeout(r, 2600));
    await p.screenshot({ path: path.join(out, `amostra-v3-${w}x${h}${suf}.png`) });
    await p.screenshot({ path: path.join(out, `amostra-v3-${w}-inteira${suf}.png`), fullPage: true });
    const m = await p.evaluate(() => {
      const r = {}; const doc = document.documentElement;
      r.rolagemHorizontal = doc.scrollWidth > doc.clientWidth;
      // menor fonte visível
      let menor = 99, onde = '';
      document.querySelectorAll('body *').forEach(el => { if (!el.childNodes.length) return; const temTexto = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()); if (!temTexto) return; const cs = getComputedStyle(el); if (cs.display === 'none' || el.closest('[hidden]')) return; const f = parseFloat(cs.fontSize); if (f < menor) { menor = f; onde = el.className + ':' + el.textContent.trim().slice(0, 30); } });
      r.menorFonte = menor + ' ' + onde;
      // marcos: sobreposição e transbordo
      const caixas = [...document.querySelectorAll('.marco, .cartucho, .indice')].map(e => ({ t: e.dataset.t || e.className, r: e.getBoundingClientRect() }));
      const sob = [];
      for (let i = 0; i < caixas.length; i++) for (let j = i + 1; j < caixas.length; j++) { const a = caixas[i].r, c = caixas[j].r; if (a.left < c.right && c.left < a.right && a.top < c.bottom && c.top < a.bottom) sob.push(caixas[i].t + ' x ' + caixas[j].t); }
      r.sobreposicoes = sob;
      const cam = document.getElementById('caminho').getBoundingClientRect();
      r.caminho = [Math.round(cam.width), Math.round(cam.height)];
      r.marcos = [...document.querySelectorAll('.marco')].map(e => { const b = e.getBoundingClientRect(); return `${e.dataset.t}:${Math.round(b.width)}x${Math.round(b.height)}`; }).join(' ');
      r.fios = document.querySelectorAll('#fios path.fio').length;
      // fios que cruzam marcos que não são as pontas
      const fios = [...document.querySelectorAll('#fios path.fio')];
      const cruz = [];
      const svg = document.getElementById('fios'); const base = svg.getBoundingClientRect();
      fios.forEach((f, k) => { const L = f.getTotalLength(); for (let s = 6; s < L - 6; s += 4) { const pt = f.getPointAtLength(s); const x = pt.x + base.left, y = pt.y + base.top; document.querySelectorAll('.marco, .cartucho, .indice').forEach(e => { const b = e.getBoundingClientRect(); if (x > b.left + 2 && x < b.right - 2 && y > b.top + 2 && y < b.bottom - 2) cruz.push(k + '>' + (e.dataset.t || e.className)); }); } });
      r.fiosCruzando = [...new Set(cruz)];
      return r;
    });
    console.log(w, JSON.stringify(m, null, 1));
    // estado com um ponto escolhido (16) e dica de um quadrado
    await p.click('.marco[data-t="09"]');
    await new Promise(r => setTimeout(r, 400));
    await p.screenshot({ path: path.join(out, `amostra-v3-${w}x${h}-escolhido09${suf}.png`) });
    await p.hover('.folha[data-t="25"]'); await new Promise(r => setTimeout(r, 300));
    await p.screenshot({ path: path.join(out, `amostra-v3-${w}x${h}-dica${suf}.png`) });
    await p.close();
  }
  console.log('erros', erros);
  await b.close();
})();
