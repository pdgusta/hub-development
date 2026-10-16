// Portal REAL (porta 8770), só leitura: a carta da amostra no leitor e sozinha, em 1280 e 320, com mouse de verdade
// (eventos do navegador pelo protocolo de depuração) dentro do canvas: arrastar com o botão direito, Ctrl + roda,
// Shift + roda e clique numa ficha. Bloqueia qualquer POST. Uso: node prova.js <pasta com puppeteer-core>
const puppeteer = require(require('path').join(process.argv[2], 'puppeteer-core'));
const fs = require('fs'); const path = require('path');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const PERFIL = path.join(process.env.TEMP || 'C:/Temp', 'carta-amostra-edge-perfil');
const BASE = 'http://127.0.0.1:8770/';
const espera = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  fs.rmSync(PERFIL, { recursive: true, force: true });
  const b = await puppeteer.launch({ executablePath: EDGE, headless: 'new', userDataDir: PERFIL, args: ['--disable-gpu', '--hide-scrollbars'] });
  const res = { quando: new Date().toISOString(), capturas: [], medidas: {}, erros_js: [], posts_bloqueados: 0 };
  try {
    const p = await b.newPage();
    await p.setRequestInterception(true);
    p.on('request', r => { if (r.method() !== 'GET') { res.posts_bloqueados++; return r.abort(); } r.continue(); });
    p.on('response', r => { if (r.status() >= 400 && !/favicon/.test(r.url())) res.erros_js.push(r.status() + ' ' + r.url()); });
    p.on('pageerror', e => res.erros_js.push(String(e)));
    p.on('console', m => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) res.erros_js.push('console: ' + m.text()); });
    const foto = async (arq) => { await p.screenshot({ path: path.join(__dirname, arq) }); res.capturas.push(arq); };
    const estado = async (f) => f.evaluate(() => {
      const svgs = [...document.querySelectorAll('svg[viewBox]')].sort((a, b) => b.getBoundingClientRect().width * b.getBoundingClientRect().height - a.getBoundingClientRect().width * a.getBoundingClientRect().height);
      const f = document.getElementById('ficha');
      const ficha = f && getComputedStyle(f).display !== 'none' && !f.hidden && f.getBoundingClientRect().width > 50 ? f : null;
      return { viewBox: svgs[0] && svgs[0].getAttribute('viewBox'), zoom: (document.getElementById('z-tudo') || {}).innerText, ficha: ficha ? ficha.innerText.slice(0, 60).replace(/\s+/g, ' ') : null };
    });
    for (const [w, h, rota, nome] of [[1280, 800, '#/cartas/amostra-da-cidade', 'leitor'], [320, 800, '#/cartas/amostra-da-cidade', 'leitor'], [1280, 800, 'carta/amostra-da-cidade/', 'sozinha'], [320, 700, 'carta/amostra-da-cidade/', 'sozinha']]) {
      await p.goto('about:blank'); // página nova a cada tamanho: nada do teste anterior (ficha aberta, zoom) passa adiante
      await p.setViewport({ width: w, height: h });
      await p.goto(BASE + rota, { waitUntil: 'networkidle0' }); await espera(3000);
      const chave = `${nome}-${w}x${h}`;
      await foto(`${chave}.png`);
      const carta = nome === 'leitor' ? p.frames().find(f => /\/carta\/amostra-da-cidade\/$/.test(f.url())) : p.mainFrame();
      const peca = p.frames().find(f => /\/amostra\.html$/.test(f.url()));
      if (!carta || !peca) { res.medidas[chave] = 'sem quadro'; continue; }
      // rola a carta até o quadro ocupar a tela (em telas estreitas a faixa sai de vista)
      await carta.evaluate(() => document.querySelector('.moldura').scrollIntoView({ block: 'start' })); await espera(500);
      const caixaCarta = nome === 'leitor' ? await p.evaluate(() => { const r = document.querySelector('iframe.carta-cheia').getBoundingClientRect(); return { x: r.x, y: r.y }; }) : { x: 0, y: 0 };
      const caixaQuadro = await carta.evaluate(() => { const r = document.getElementById('quadro').getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; });
      const cx = caixaCarta.x + caixaQuadro.x + caixaQuadro.w / 2, cy = caixaCarta.y + caixaQuadro.y + Math.min(caixaQuadro.h * 0.6, (h - caixaCarta.y - caixaQuadro.y) * 0.6);
      const m = { quadro: caixaQuadro, inicio: await estado(peca) };
      const rolagemAntes = await carta.evaluate(() => window.scrollY);
      // arrastar com o botão direito
      await p.mouse.move(cx, cy); await p.mouse.down({ button: 'right' });
      for (let i = 1; i <= 8; i++) { await p.mouse.move(cx - i * 15, cy - i * 8); await espera(20); }
      await p.mouse.up({ button: 'right' }); await espera(300);
      m.depoisDoArrasto = await estado(peca);
      // Ctrl + roda: aproximar
      await p.mouse.move(cx, cy);
      await p.keyboard.down('Control'); for (let i = 0; i < 4; i++) { await p.mouse.wheel({ deltaY: -120 }); await espera(80); } await p.keyboard.up('Control'); await espera(400);
      m.depoisDoZoom = await estado(peca);
      // Shift + roda: para os lados
      await p.keyboard.down('Shift'); await p.mouse.wheel({ deltaY: 200 }); await p.keyboard.up('Shift'); await espera(300);
      m.depoisDoShift = await estado(peca);
      m.cartaRolouSozinha = (await carta.evaluate(() => window.scrollY)) !== rolagemAntes;
      m.paginaComZoom = await p.evaluate(() => window.visualViewport ? window.visualViewport.scale : 1);
      await foto(`${chave}-zoom.png`);
      // clique esquerdo abre ficha
      await p.mouse.click(cx, cy); await espera(500);
      m.depoisDoClique = await estado(peca);
      await foto(`${chave}-clique.png`);
      res.medidas[chave] = m;
    }
  } finally { await b.close(); }
  fs.writeFileSync(path.join(__dirname, 'prova.json'), JSON.stringify(res, null, 1));
  console.log(JSON.stringify(res, null, 1));
})();
