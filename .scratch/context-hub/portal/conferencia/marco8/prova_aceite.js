// Marco 8: provas no navegador dos itens da §8 que os testes Python não cobrem.
// uso: node prova_aceite.js <pasta da cópia da fixture (contém horta/)> <url da cópia> <url do real>
// Só escreve na CÓPIA da fixture; no portal real só lê (GET).
const puppeteer = require('puppeteer-core');
const fs = require('fs'); const path = require('path');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const [copia, BASE, REAL] = process.argv.slice(2);
const horta = path.join(copia, 'horta');
const espera = ms => new Promise(r => setTimeout(r, ms));

// troca de rota só no hash não dispara 'load': passa por about:blank antes
async function ir(p, url, quando = 'networkidle0') { await p.goto('about:blank'); await p.goto(url, { waitUntil: quando, timeout: 60000 }); }

async function cronometrar(p, mudar, condicao, limite = 8000) {
  const t0 = Date.now(); mudar();
  while (Date.now() - t0 < limite) { if (await p.evaluate(condicao)) return Date.now() - t0; await espera(100); }
  return null;
}

(async () => {
  const r = {};
  const b = await puppeteer.launch({ executablePath: EDGE, headless: 'new', args: ['--disable-gpu'] });
  const p = await b.newPage(); await p.setViewport({ width: 1600, height: 900 });
  const erros = []; p.on('pageerror', e => erros.push(String(e)));

  // 1a. mudança no mapa chega à tela (Decisões, Diário de bordo) em até 3 s
  await ir(p, BASE + '#/rumo', 'networkidle0'); await espera(1500);
  const mapa = path.join(horta, 'mapa.md');
  r.mapa_ms = await cronometrar(p, () => {
    const s = fs.readFileSync(mapa, 'utf8');
    fs.writeFileSync(mapa, s.replace('## Decisions so far\n', '## Decisions so far\n\n- [Estufa](issues/08-estufa.md): DECISAO-SONDA-MAPA\n'));
  }, () => document.body.innerText.includes('DECISAO-SONDA-MAPA'));

  // 1b. mudança numa rodada chega à tela (Responder) em até 3 s
  await ir(p, BASE + '#/autorizacoes', 'networkidle0'); await espera(1500);
  const rodada = path.join(horta, 'portal', 'rodadas', '2026-10-02-composteira-r1.md');
  r.rodada_ms = await cronometrar(p, () => {
    const s = fs.readFileSync(rodada, 'utf8');
    fs.writeFileSync(rodada, s.replace('titulo: Onde fica a composteira', 'titulo: RODADA-SONDA composteira'));
  }, () => document.body.innerText.includes('RODADA-SONDA'));

  // 2. Markdown do ticket passa pelo DOMPurify; link externo com noopener noreferrer
  const ticket = path.join(horta, 'issues', '04-composteira.md');
  fs.appendFileSync(ticket, '\n\nSONDA-XSS <script>window.__xss = "script"</script> <img src="x" onerror="window.__xss = \'onerror\'"> [link externo](https://example.com/)\n');
  await espera(3500);
  await ir(p, BASE + '#/partidas?ticket=04', 'load'); await espera(4000);
  r.markdown = await p.evaluate(() => {
    const corpo = [...document.querySelectorAll('aside, [role="dialog"], .gaveta')].find(e => e.innerText.includes('SONDA-XSS'));
    if (!corpo) return { achou: false };
    const a = [...corpo.querySelectorAll('a')].find(x => x.href.startsWith('https://example.com'));
    return { achou: true, xss: window.__xss || null, scripts: corpo.querySelectorAll('script').length,
      onerror: [...corpo.querySelectorAll('img')].filter(i => i.hasAttribute('onerror')).length,
      link: a ? { target: a.target, rel: a.rel } : null };
  });

  // 3. iframe da carta: sandbox só allow-scripts; a carta não lê a API nem o portal
  fs.writeFileSync(path.join(horta, 'cartas', 'regas-do-poco.html'), `<!doctype html><meta charset="utf-8"><p>sonda</p><script>
    let pai = 'leu'; try { void parent.document.body.innerHTML; } catch (e) { pai = 'bloqueado: ' + e.name; }
    fetch('/api/estado').then(r => r.text()).then(t => parent.postMessage({ sonda: 1, api: 'leu ' + t.length + ' bytes', pai }, '*'))
      .catch(e => parent.postMessage({ sonda: 1, api: 'bloqueado: ' + e.name, pai }, '*'));
  </script>`);
  await ir(p, BASE + '#/cartas', 'networkidle0'); await espera(500);
  await p.evaluate(() => { window.__sondas = []; addEventListener('message', ev => ev.data && ev.data.sonda && window.__sondas.push(ev.data)); });
  await p.evaluate(() => { location.hash = '#/cartas/regas-do-poco'; }); await espera(3500);
  r.carta = await p.evaluate(() => ({
    sandbox: [...document.querySelectorAll('iframe')].map(f => f.getAttribute('sandbox')),
    sondas: window.__sondas }));

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
  r.erros_js = erros;
  console.log(JSON.stringify(r, null, 1));
  await b.close();
})();
