// Portal REAL (porta 8770), só leitura: capturas da tela Laços com os dois laços reais, nos dois tamanhos. Bloqueia
// qualquer POST por garantia (nada é gravado na caixa real). Junta o resultado ao prova.json da pasta.
const puppeteer = require('puppeteer-core');
const fs = require('fs'); const path = require('path');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const PERFIL = path.join(process.env.TEMP || 'C:/Temp', 'l3-edge-perfil-real');
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
    p.on('pageerror', e => res.erros_js.push(String(e)));
    p.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.text())) res.erros_js.push('console: ' + m.text()); });
    for (const [w, h] of [[1600, 900], [1280, 800]]) {
      for (const [nome, rota] of [['real-embeddings', '#/lacos/modelos-de-embeddings'], ['real-ampla', '#/lacos/pesquisa-ampla'], ['real-ampla-gaveta-juntador', '#/lacos/pesquisa-ampla?no=juntador']]) {
        await p.setViewport({ width: w, height: h });
        await p.goto(BASE + rota, { waitUntil: 'networkidle0' }); await p.reload({ waitUntil: 'networkidle0' }); await espera(3000);
        const arq = `${nome}-${w}x${h}.png`; await p.screenshot({ path: path.join(__dirname, arq) }); res.capturas.push(arq);
        if (!nome.includes('gaveta')) res.medidas[`${nome}-${w}-limpeza`] = await p.evaluate(require('./limpeza.js'));
        res.medidas[`${nome}-${w}`] = await p.evaluate(() => {
          let menor = 99;
          document.querySelectorAll('body *').forEach(el => {
            if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
            const cs = getComputedStyle(el); if (cs.display === 'none' || el.closest('[hidden]') || el.closest('iframe')) return;
            if (!el.getBoundingClientRect().width) return;
            menor = Math.min(menor, parseFloat(cs.fontSize));
          });
          const t = document.getElementById('tela');
          return { menorFonte: menor, rolagemHorizontal: t.scrollWidth > t.clientWidth + 1 || document.documentElement.scrollWidth > document.documentElement.clientWidth, lista: [...document.querySelectorAll('.item-laco .titulo')].map(x => x.innerText), botoesDePedido: document.querySelectorAll('.laco-acoes button, .proposta-no').length };
        });
        if (!nome.includes('gaveta')) {
          const alt = await p.evaluate(() => document.getElementById('tela').scrollHeight + 160);
          await p.setViewport({ width: w, height: Math.max(h, alt) }); await espera(700);
          const arq2 = `${nome}-${w}-inteira.png`; await p.screenshot({ path: path.join(__dirname, arq2) }); res.capturas.push(arq2);
        }
      }
    }
  } finally {
    await b.close();
    const pj = path.join(__dirname, 'prova.json');
    const prova = fs.existsSync(pj) ? JSON.parse(fs.readFileSync(pj, 'utf8')) : {};
    prova.portal_real = res;
    fs.writeFileSync(pj, JSON.stringify(prova, null, 2), 'utf8');
    console.log(JSON.stringify(res, null, 1));
  }
})();
