// uso: node telas.js <pasta> [rotas separadas por vírgula] [larguras]
const puppeteer = require('puppeteer-core');
const path = require('path'); const fs = require('fs');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const BASE = process.env.BASE || 'http://127.0.0.1:8770/';
const out = process.argv[2]; fs.mkdirSync(out, { recursive: true });
const rotas = (process.argv[3] || 'torre,partidas,autorizacoes,cartas,rumo').split(',');
const tamanhos = (process.argv[4] || '1600x900,1280x800').split(',').map(t => t.split('x').map(Number));
(async () => {
  const b = await puppeteer.launch({ executablePath: fs.existsSync(EDGE) ? EDGE : 'C:/Program Files/Microsoft/Edge/Application/msedge.exe', headless: 'new', args: ['--disable-gpu', '--hide-scrollbars'] });
  for (const [w, h] of tamanhos) for (const r of rotas) {
    const p = await b.newPage(); const erros = [];
    p.on('pageerror', e => erros.push(String(e))); p.on('console', m => m.type() === 'error' && erros.push(m.text()));
    await p.setViewport({ width: w, height: h });
    await p.goto(BASE + '#/' + r, { waitUntil: 'networkidle0' }); await new Promise(x => setTimeout(x, 2500));
    const nome = r.replace(/[\/?=&]/g, '_');
    await p.screenshot({ path: path.join(out, `v2-${nome}-${w}x${h}.png`) });
    // página inteira: a tela rola dentro de <main>; abre a altura para capturar tudo
    const alt = await p.evaluate(() => { const m = document.getElementById('tela'); return m.scrollHeight + 90; });
    await p.setViewport({ width: w, height: Math.max(h, alt) }); await new Promise(x => setTimeout(x, 600));
    await p.screenshot({ path: path.join(out, `v2-${nome}-${w}-inteira.png`) });
    await p.setViewport({ width: w, height: h }); await new Promise(x => setTimeout(x, 300));
    const m = await p.evaluate(() => {
      let menor = 99, onde = '';
      document.querySelectorAll('body *').forEach(el => {
        if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
        const cs = getComputedStyle(el); if (cs.display === 'none' || el.closest('[hidden]') || el.closest('iframe')) return;
        const r = el.getBoundingClientRect(); if (!r.width) return;
        const f = parseFloat(cs.fontSize); if (f < menor) { menor = f; onde = (el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className) + ':' + el.textContent.trim().slice(0, 25); }
      });
      const t = document.getElementById('tela');
      return { menorFonte: `${menor} ${onde}`, rolagemH: t.scrollWidth > t.clientWidth + 1 || document.documentElement.scrollWidth > document.documentElement.clientWidth };
    });
    console.log(`${r} ${w}: ${JSON.stringify(m)} erros=${JSON.stringify(erros.filter(e => !/favicon/.test(e)))}`);
    await p.close();
  }
  await b.close();
})();
