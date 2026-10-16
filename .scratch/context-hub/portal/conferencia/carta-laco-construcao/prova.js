// Portal REAL (porta 8770), só leitura: a carta do laço da construção no leitor e sozinha, em 1280 e 320.
// Mede rolagem lateral, fontes carregadas e erros; bloqueia qualquer POST. Uso: node prova.js <pasta com puppeteer-core>
const puppeteer = require(require('path').join(process.argv[2], 'puppeteer-core'));
const fs = require('fs'); const path = require('path');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const PERFIL = path.join(process.env.TEMP || 'C:/Temp', 'carta-laco-edge-perfil');
const BASE = 'http://127.0.0.1:8770/';
const espera = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  fs.rmSync(PERFIL, { recursive: true, force: true });
  const b = await puppeteer.launch({ executablePath: EDGE, headless: 'new', userDataDir: PERFIL, args: ['--disable-gpu', '--hide-scrollbars'] });
  const res = { quando: new Date().toISOString(), capturas: [], medidas: {}, erros: [], posts_bloqueados: 0 };
  try {
    const p = await b.newPage();
    await p.setRequestInterception(true);
    p.on('request', r => { if (r.method() !== 'GET') { res.posts_bloqueados++; return r.abort(); } r.continue(); });
    p.on('response', r => { if (r.status() >= 400 && !/favicon/.test(r.url())) res.erros.push(r.status() + ' ' + r.url()); });
    p.on('pageerror', e => res.erros.push(String(e)));
    for (const [w, h, rota, nome, inteira] of [[1280, 800, '#/cartas/laco-construcao', 'leitor', false], [320, 800, '#/cartas/laco-construcao', 'leitor', false], [1280, 800, 'carta/laco-construcao/', 'sozinha', true], [320, 800, 'carta/laco-construcao/', 'sozinha', true]]) {
      await p.goto('about:blank');
      await p.setViewport({ width: w, height: h });
      await p.goto(BASE + rota, { waitUntil: 'networkidle0' }); await espera(2500);
      const chave = `${nome}-${w}x${h}`;
      const carta = nome === 'leitor' ? p.frames().find(f => /\/carta\/laco-construcao\/$/.test(f.url())) : p.mainFrame();
      res.medidas[chave] = carta ? await carta.evaluate(() => ({
        largura: innerWidth, rolagemLateral: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        altura: document.documentElement.scrollHeight,
        barlow: document.fonts.check('800 20px "Barlow Condensed"') && document.fonts.check('500 16px Barlow'),
        malha: document.querySelectorAll('#malha line').length,
        mapaRola: (q => q.scrollWidth > q.clientWidth)(document.querySelector('.quadro')),
      })) : 'sem quadro da carta';
      await p.screenshot({ path: path.join(__dirname, `${chave}.png`), fullPage: inteira });
      res.capturas.push(`${chave}.png`);
    }
  } catch (e) { res.erros.push('prova: ' + e); }
  finally { await b.close(); fs.writeFileSync(path.join(__dirname, 'prova.json'), JSON.stringify(res, null, 2)); console.log(JSON.stringify(res, null, 1)); }
})();
