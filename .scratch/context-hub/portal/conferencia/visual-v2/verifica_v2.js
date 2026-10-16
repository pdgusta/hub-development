// roteiro de interação da v2 no portal real (8770): realce, nota de leitura, Esc, placa, gaveta, redesenho, dica flutuante
const puppeteer = require('puppeteer-core');
const espera = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: 'new', args: ['--disable-gpu'] });
  const erros = [];
  for (const reduz of [false, true]) {
    const p = await b.newPage(); p.on('pageerror', e => erros.push(String(e)));
    await p.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: reduz ? 'reduce' : 'no-preference' }]);
    await p.setViewport({ width: 1600, height: 900 });
    await p.goto('http://127.0.0.1:8770/#/torre', { waitUntil: 'networkidle0' }); await espera(2500);
    const est = () => p.evaluate(() => {
      const op = sel => Math.min(...[...document.querySelectorAll(sel)].map(e => +getComputedStyle(e).opacity));
      const nota = document.getElementById('leitura'); const a = document.activeElement;
      const f = document.querySelector('.folha'); const cs = getComputedStyle(f);
      return { foco: a.dataset.foco || a.tagName, nota: nota.classList.contains('lendo') ? nota.querySelector('.dica-titulo')?.textContent : '(repouso)',
        placa: !document.querySelector('.placa').hidden, flutuante: !document.getElementById('dica').hidden,
        opMarcos: op('.marco'), opFolhas: op('.folha'), folha01: `${cs.backgroundColor} / ${cs.color}`,
        acesas: document.querySelectorAll('.folha.acesa').length, corrente: document.querySelectorAll('.marco.na-corrente').length };
    });
    const r = {};
    await p.click('.marco[data-t="32"]'); await espera(250); r.escolhe32 = await est();
    await p.keyboard.press('Escape'); await espera(300); r.esc32 = await est();
    await p.mouse.move(2, 2);
    await p.focus('.cartucho .selo'); await espera(150); r.focoCriterio = await est();
    await p.keyboard.press('Escape'); await espera(150); r.escCriterio = await est();
    await p.focus('.marco[data-t="16"]'); await p.keyboard.press('Enter'); await espera(250); r.enter16 = await est();
    await p.evaluate(() => document.dispatchEvent(new CustomEvent('torre:redesenhar'))); await espera(400); r.redesenho = await est();
    await p.keyboard.press('Escape'); await espera(300); r.esc16 = await est();
    await p.focus('.folha'); await p.keyboard.press('End'); r.end = await est(); await p.keyboard.press('Home'); r.home = await est();
    await p.keyboard.press('ArrowDown'); r.baixo = await est();
    await p.click('.marco[data-t="09"]'); await espera(200); await p.click('.placa .botao.primario'); await espera(700);
    r.gaveta = await p.evaluate(() => ({ aberta: !document.getElementById('gaveta').hidden, hash: location.hash }));
    await p.keyboard.press('Escape'); await espera(300);
    // dica flutuante nas outras telas: eco do horizonte, Esc dispensa
    await p.goto('http://127.0.0.1:8770/#/rumo', { waitUntil: 'networkidle0' }); await espera(1500);
    await p.evaluate(() => document.querySelector('.eco').focus()); await espera(150); const d1 = await p.evaluate(() => !document.getElementById('dica').hidden);
    await p.keyboard.press('Escape'); await espera(150); const d2 = await p.evaluate(() => !document.getElementById('dica').hidden);
    r.rumo = { dicaComFoco: d1, depoisDoEsc: d2, foco: await p.evaluate(() => document.activeElement.dataset.foco) };
    console.log(reduz ? 'REDUZIDO' : 'NORMAL'); for (const [k, v] of Object.entries(r)) console.log(' ', k, JSON.stringify(v));
    await p.close();
  }
  console.log('erros', erros); await b.close();
})();
