const puppeteer = require('puppeteer-core'); const path = require('path');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: 'new', args: ['--disable-gpu', '--hide-scrollbars'] });
  for (const [rota, sel, nome] of [['cartas', '.cartao-texto .decisao button', 'designs-decisao-contrato'], ['rumo', '.coluna-fora button.codigo', 'decisoes-codigo-fora'], ['rumo', '.eco', 'decisoes-eco']]) {
    const p = await b.newPage(); await p.setViewport({ width: 1280, height: 800 });
    await p.goto('http://127.0.0.1:8770/#/' + rota, { waitUntil: 'networkidle0' }); await new Promise(x => setTimeout(x, 2000));
    const r = await p.evaluate(sel => { const a = document.querySelector(sel); a.focus(); return { dica: !document.getElementById('dica').hidden, faixa: document.getElementById('leitura').classList.contains('lendo') }; }, sel);
    await new Promise(x => setTimeout(x, 300));
    await p.screenshot({ path: path.join(process.argv[2], `v2-dica-${nome}-1280.png`) });
    console.log(nome, JSON.stringify(r)); await p.close();
  }
  await b.close();
})();
