// Prova da regra "carta substituída" numa CÓPIA da fixture (%TEMP%\cs-horta, porta 8774), onde
// "regas-com-cisterna" grava "substitui": "regas-por-gotejamento". Uso:
//   NODE_PATH=<node_modules com puppeteer-core> node prova.js [url-base] [prefixo-das-capturas]   (só lê: não grava nada no portal)
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const BASE = process.argv[2] || 'http://127.0.0.1:8774';
const PREFIXO = process.argv[3] || 'copia';
const AQUI = __dirname;
const espera = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const perfil = fs.mkdtempSync(path.join(require('os').tmpdir(), 'cs-edge-'));
  const b = await puppeteer.launch({ executablePath: EDGE, headless: 'new', args: ['--disable-gpu'], userDataDir: perfil });
  const erros = []; const resultado = { base: BASE };
  for (const [w, hgt] of [[1600, 900], [1280, 800]]) {
    const p = await b.newPage(); p.on('pageerror', e => erros.push(String(e)));
    await p.setViewport({ width: w, height: hgt });
    await p.goto('about:blank'); await p.goto(BASE + '/#/cartas', { waitUntil: 'networkidle0' }); await espera(1500);
    const leitura = await p.evaluate(() => {
      const nomes = sel => [...document.querySelectorAll(sel)].map(e => e.querySelector('h3')?.textContent.trim());
      const arq = [...document.querySelectorAll('.arquivo-cartas .cartao-carta')].map(e => ({
        titulo: e.querySelector('h3')?.textContent.trim(),
        selo: e.querySelector('.quadro-link .selo-historica')?.textContent.trim(),
        ligacao: e.querySelector('.ligacao-subst.por')?.textContent.trim() || null }));
      const subst = [...document.querySelectorAll('.grade-cartas .ligacao-subst.substitui')].map(e => e.textContent.trim());
      const minFonte = Math.min(...[...document.querySelectorAll('.ligacao-subst, .selo-historica')].map(e => parseFloat(getComputedStyle(e).fontSize)));
      return { vigentes: nomes('.grade-cartas .cartao-carta'), arquivo: arq, nova_mostra: subst, menor_fonte_px: minFonte };
    });
    resultado[`tela_${w}`] = leitura;
    {
      const alvo = await p.$('.arquivo-cartas .ligacao-subst.por a');
      if (alvo) await alvo.evaluate(e => e.scrollIntoView({ block: 'center' }));
      await espera(600);
      await p.screenshot({ path: path.join(AQUI, `${PREFIXO}-designs-${w}.png`) });
      await p.screenshot({ path: path.join(AQUI, `${PREFIXO}-designs-${w}-inteira.png`), fullPage: true });
    }
    if (w === 1600) {
      const alvo = await p.$('.arquivo-cartas .ligacao-subst.por a');
      if (alvo) {
        await alvo.click(); await espera(1500);
        resultado.clique = await p.evaluate(() => ({ hash: location.hash, leitor_aberto: !document.getElementById('leitor').hidden,
          titulo_no_leitor: document.querySelector('#leitor .tira strong')?.textContent,
          iframe: document.querySelector('#leitor iframe')?.getAttribute('src') }));
        await p.screenshot({ path: path.join(AQUI, `${PREFIXO}-leitor-da-nova-1600.png`) });
        // o leitor da antiga mostra o selo "substituída" e a ligação para a nova
        await p.goto('about:blank'); await p.goto(BASE + '/#/cartas/regas-por-gotejamento', { waitUntil: 'networkidle0' }); await espera(1500);
        resultado.leitor_da_antiga = await p.evaluate(() => ({ selo: document.querySelector('#leitor .tira .selo-historica')?.textContent,
          ligacao: document.querySelector('#leitor .tira a.ligacao-subst')?.textContent }));
        if (resultado.leitor_da_antiga.selo) await p.screenshot({ path: path.join(AQUI, `${PREFIXO}-leitor-da-antiga-1600.png`) });
      }
    }
    await p.close();
  }
  resultado.erros = erros;
  fs.writeFileSync(path.join(AQUI, `${PREFIXO}-resultado.json`), JSON.stringify(resultado, null, 2));
  console.log(JSON.stringify(resultado, null, 1));
  await b.close();
  fs.rmSync(perfil, { recursive: true, force: true });
})();
