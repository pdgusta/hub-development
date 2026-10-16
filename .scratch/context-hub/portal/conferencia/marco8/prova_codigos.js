// Marco 8: varredura de códigos internos no portal REAL (só leitura). uso: node prova_codigos.js <url do real>
const puppeteer = require('puppeteer-core');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const REAL = process.argv[2]; const espera = ms => new Promise(r => setTimeout(r, ms));
async function ir(p, url, quando) { await p.goto('about:blank'); await p.goto(url, { waitUntil: quando, timeout: 60000 }); }
(async () => {
  const r = {}; const b = await puppeteer.launch({ executablePath: EDGE, headless: 'new', args: ['--disable-gpu'] });
  const p = await b.newPage(); await p.setViewport({ width: 1600, height: 900 });
  // 4. códigos internos: no portal REAL (só leitura), texto visível com cara de código (Q7, R88, T1...)
  r.codigos = {};
  for (const rota of ['torre', 'partidas', 'partidas/rotas', 'autorizacoes', 'cartas', 'rumo']) {
    await ir(p, REAL + '#/' + rota, 'networkidle0'); await espera(2000);
    r.codigos[rota] = await p.evaluate(() => {
      const achados = []; const re = /\b[A-Z]{1,2}\d{1,3}\b/g;
      const w = document.createTreeWalker(document.getElementById('tela') || document.body, NodeFilter.SHOW_TEXT);
      while (w.nextNode()) {
        const n = w.currentNode; const el = n.parentElement; if (!el || el.closest('[hidden], script, style, iframe')) continue;
        const m = n.textContent.match(re); if (!m) continue;
        const dono = el.closest('[aria-label], [title]');
        achados.push({ codigo: m.join(','), texto: el.textContent.trim().slice(0, 60), rotulo: dono ? (dono.getAttribute('aria-label') || dono.getAttribute('title')).slice(0, 80) : null, contexto: (el.parentElement?.textContent || '').trim().slice(0, 90) });
      }
      return achados;
    });
  }
  console.log(JSON.stringify(r.codigos, null, 1)); await b.close();
})();
