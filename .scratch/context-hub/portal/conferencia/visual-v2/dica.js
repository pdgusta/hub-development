const puppeteer = require('puppeteer-core'); const fs = require('fs'); const path = require('path');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: 'new', args: ['--disable-gpu', '--hide-scrollbars'] });
  for (const [w, h] of [[1600, 900], [1280, 800]]) {
    const p = await b.newPage(); await p.setViewport({ width: w, height: h });
    await p.goto('http://127.0.0.1:8770/#/torre', { waitUntil: 'networkidle0' }); await new Promise(x => setTimeout(x, 2500));
    const res = [];
    for (const sel of ['.marco[data-t="09"]', '.marco[data-t="12"]', '.marco[data-t="14"]', '.marco[data-t="11"]', '.marco[data-t="15"]', '.marco[data-t="16"]', '.marco[data-t="17"]', '.folha[data-t="25"]', '.selo']) {
      await p.hover(sel); await new Promise(x => setTimeout(x, 350));
      if (sel.includes('"09"')) await p.screenshot({ path: path.join(process.argv[2], `v2-torre-${w}x${h}-dica09.png`) });
      if (sel.includes('"16"')) await p.screenshot({ path: path.join(process.argv[2], `v2-torre-${w}x${h}-dica16.png`) });
      res.push(await p.evaluate(s => {
        const d = document.getElementById('dica'); if (d.hidden) return s + ': sem dica';
        const r = d.getBoundingClientRect(); const alvo = document.querySelector(s);
        const cobre = [...document.querySelectorAll('.marco, .cartucho')].filter(m => m !== alvo && !m.contains(alvo)).filter(m => { const q = m.getBoundingClientRect(); return q.left < r.right && r.left < q.right && q.top < r.bottom && r.top < q.bottom; }).map(m => m.dataset.t || m.className);
        return `${s}: cobre [${cobre}]`;
      }, sel));
      await p.mouse.move(2, 2); await new Promise(x => setTimeout(x, 400));
    }
    console.log(w, res.join(' | '));
    await p.close();
  }
  await b.close();
})();
