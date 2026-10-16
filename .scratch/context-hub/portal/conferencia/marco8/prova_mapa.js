// Marco 8: mudança no mapa chega à tela Decisões em até 3 s (o resumo fica recolhido: conta pelo textContent).
// uso: node prova_mapa.js <mapa.md da CÓPIA da fixture> <url da cópia>
const puppeteer = require('puppeteer-core'); const fs = require('fs');
const [mapa, BASE] = process.argv.slice(2);
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: 'new', args: ['--disable-gpu'] });
  const p = await b.newPage(); await p.setViewport({ width: 1600, height: 900 });
  await p.goto(BASE + '#/rumo', { waitUntil: 'networkidle0' }); await new Promise(r => setTimeout(r, 1500));
  const marca = 'SONDA-MAPA-' + Date.now();
  const t0 = Date.now();
  fs.writeFileSync(mapa, fs.readFileSync(mapa, 'utf8').replace('## Decisions so far\n', `## Decisions so far\n\n- [Estufa](issues/08-estufa.md): ${marca}\n`));
  let ms = null;
  while (Date.now() - t0 < 8000) { if (await p.evaluate(m => document.body.textContent.includes(m), marca)) { ms = Date.now() - t0; break; } await new Promise(r => setTimeout(r, 100)); }
  console.log(JSON.stringify({ mapa_ms: ms }));
  await b.close();
})();
