const puppeteer = require('puppeteer-core');
const fs = require('fs');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const URL = 'http://127.0.0.1:8765/amostra-inicio.html';
const espera = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: fs.existsSync(EDGE) ? EDGE : 'C:/Program Files/Microsoft/Edge/Application/msedge.exe', headless: 'new', args: ['--disable-gpu'] });
  const erros = [];
  for (const reduz of [false, true]) {
    const p = await b.newPage(); p.on('pageerror', e => erros.push(String(e)));
    await p.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: reduz ? 'reduce' : 'no-preference' }]);
    await p.setViewport({ width: 1600, height: 900 });
    await p.goto(URL + '?v=' + Date.now(), { waitUntil: 'networkidle0' }); await espera(2500);
    const estado = () => p.evaluate(() => {
      const d = document.getElementById('dica');
      const op = sel => [...document.querySelectorAll(sel)].map(e => +getComputedStyle(e).opacity);
      const f01 = document.querySelector('.folha[data-t="01"]'); const cs = getComputedStyle(f01);
      return { dica: !d.hidden, foco: document.activeElement.dataset.t || document.activeElement.className, placa: !document.getElementById('placa').hidden,
        marcosOpMin: Math.min(...op('.marco')), folhasOpMin: Math.min(...op('.folha')), f01: cs.backgroundColor + ' / ' + cs.color };
    });
    const r = {};
    await p.click('.marco[data-t="32"]'); await espera(300); r.escolhido32 = await estado();
    await p.keyboard.press('Escape'); await espera(300); r.esc32 = await estado();
    await p.focus('.selo'); await espera(100); r.focoAcha = await estado();
    await p.keyboard.press('Escape'); await espera(100); r.escAcha = await estado();
    await p.focus('.marco[data-t="16"]'); await p.keyboard.press('Enter'); await espera(200); r.enter16 = await estado();
    await p.keyboard.press('Escape'); await espera(400); r.esc16 = await estado();
    // ponteiro: do marco para dentro da dica
    await p.mouse.move(5, 5); await p.focus('.barra a'); await espera(100);
    await p.hover('.marco[data-t="11"]'); await espera(150);
    const box = await p.evaluate(() => { const r = document.getElementById('dica').getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; });
    await p.mouse.move(box.x, box.y, { steps: 8 }); await espera(500); r.dentroDaDica = await estado();
    await p.mouse.move(5, 5); await espera(500); r.foraDaDica = await estado();
    await p.hover('.conquistas button'); await espera(200); r.conquista = await estado();
    console.log(reduz ? 'REDUZIDO' : 'NORMAL', JSON.stringify(r, null, 1));
    await p.close();
  }
  console.log('erros', erros); await b.close();
})();
