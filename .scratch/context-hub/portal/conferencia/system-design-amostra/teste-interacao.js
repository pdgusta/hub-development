// Prova de interação da amostra "planta técnica" do System design.
// Uso: node teste-interacao.js <url-file> <url-pagina-iframe> <pasta-saida>
// Requer puppeteer-core (NODE_PATH) e o Edge instalado.
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const [,, URL_FILE, URL_IFRAME, OUT] = process.argv;
const ATUAL = 'C:/Projetos/context-hub/.scratch/context-hub/system-design.html';

function textosDoAtual() {
  const html = fs.readFileSync(ATUAL, 'utf8');
  const dec = s => s.replace(/<[^>]+>/g, '').replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
  const out = [];
  for (const m of html.matchAll(/<text\b[^>]*>([\s\S]*?)<\/text>/g)) out.push(dec(m[1]));
  out.push(dec(html.match(/<h1>([\s\S]*?)<\/h1>/)[1]));
  out.push(dec(html.match(/<p class="sub">([\s\S]*?)<\/p>/)[1]));
  out.push(dec(html.match(/<span class="tag">([\s\S]*?)<\/span>/)[1]));
  const leg = html.match(/<div class="legend">([\s\S]*?)<\/div>/)[1];
  out.push(dec(leg.match(/<b>([\s\S]*?)<\/b>/)[1]));
  for (const m of leg.matchAll(/<span class="lg">([\s\S]*?)<\/span>/g)) out.push(dec(m[1]));
  return out.filter(Boolean);
}

async function provar(page, ctx, nome, W, H) {
  const r = { contexto: nome, janela: `${W}x${H}`, checagens: {} };
  const ok = (k, v, extra) => { r.checagens[k] = Object.assign({ ok: !!v }, extra || {}); };
  const view = () => ctx.evaluate(() => window.__planta.view());
  const toScreen = (v, wx, wy) => [v.tx + wx * v.s, v.ty + wy * v.s];

  await ctx.evaluate(() => window.__planta.fit());
  const fitV = await view();

  // 1. sem rolagem
  const sc = await ctx.evaluate(() => ({
    sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
    sh: document.documentElement.scrollHeight, ch: document.documentElement.clientHeight,
    bsw: document.body.scrollWidth, bsh: document.body.scrollHeight,
    ov: getComputedStyle(document.documentElement).overflow + '/' + getComputedStyle(document.body).overflow
  }));
  ok('sem_rolagem', sc.sw <= sc.cw && sc.sh <= sc.ch && sc.bsw <= sc.cw && sc.bsh <= sc.ch, sc);

  // 2. menor fonte no enquadramento
  const fonte = await ctx.evaluate(() => {
    const v = window.__planta.view(); let min = 1e9, qual = '';
    document.querySelectorAll('#world text').forEach(t => {
      if (!t.textContent.trim()) return;
      let fs = parseFloat(getComputedStyle(t).fontSize) * v.s;
      if (t.hasAttribute('textLength')) { // texto comprimido: altura igual, largura menor
        const real = t.getAttribute('textLength'); fs = fs; t.dataset.sq = real;
      }
      if (fs < min) { min = fs; qual = t.textContent; }
    });
    const comprimidos = [...document.querySelectorAll('#world text[textLength]')].map(t => t.textContent);
    return { escala: v.s, menor_px: +min.toFixed(2), texto: qual, comprimidos };
  });
  ok('fonte_minima_14px', fonte.menor_px >= 14, fonte);

  // 3. arrastar com o botão direito anda
  let v0 = await view();
  await page.mouse.move(700, 400);
  await page.mouse.down({ button: 'right' });
  await page.mouse.move(760, 440, { steps: 6 });
  await page.mouse.move(800, 470, { steps: 6 });
  await page.mouse.up({ button: 'right' });
  let v1 = await view();
  ok('direito_anda', Math.abs(v1.tx - v0.tx - 100) < 2 && Math.abs(v1.ty - v0.ty - 70) < 2, { antes: v0, depois: v1 });

  // 4. arrastar com o esquerdo (em área vazia) não anda
  await ctx.evaluate(() => window.__planta.fit());
  v0 = await view();
  const [ex, ey] = toScreen(v0, 150, 860); // sala QUEM USA, parte vazia
  await page.mouse.move(ex, ey);
  await page.mouse.down({ button: 'left' });
  await page.mouse.move(ex + 120, ey - 60, { steps: 8 });
  await page.mouse.up({ button: 'left' });
  v1 = await view();
  ok('esquerdo_nao_anda', v1.tx === v0.tx && v1.ty === v0.ty && v1.s === v0.s, { antes: v0, depois: v1 });

  // 5. menu de contexto bloqueado no canvas
  const cm = await ctx.evaluate(() => {
    const ev = new MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: 300, clientY: 300, button: 2 });
    const alvo = document.elementFromPoint(300, 300) || document.getElementById('stage');
    alvo.dispatchEvent(ev); return { bloqueado: ev.defaultPrevented, alvo: alvo.tagName };
  });
  ok('menu_contexto_bloqueado', cm.bloqueado, cm);

  // 6. Ctrl+roda dá zoom centrado no ponteiro
  v0 = await view();
  const px = 640, py = 380;
  const w0 = [(px - v0.tx) / v0.s, (py - v0.ty) / v0.s];
  await page.mouse.move(px, py);
  await page.keyboard.down('Control');
  await page.mouse.wheel({ deltaY: -300 });
  await page.keyboard.up('Control');
  await new Promise(r => setTimeout(r, 150));
  v1 = await view();
  const w1 = [(px - v1.tx) / v1.s, (py - v1.ty) / v1.s];
  ok('ctrl_roda_zoom', v1.s > v0.s * 1.3 && Math.abs(w1[0] - w0[0]) < 0.5 && Math.abs(w1[1] - w0[1]) < 0.5,
     { escala_antes: v0.s, escala_depois: v1.s, ponto_mundo_antes: w0, ponto_mundo_depois: w1 });
  await page.screenshot({ path: path.join(OUT, `${nome}-${W}x${H}-zoom.png`) });

  // 7. Shift+roda anda na horizontal
  v0 = await view();
  await page.keyboard.down('Shift');
  await page.mouse.wheel({ deltaY: 200 });
  await page.keyboard.up('Shift');
  await new Promise(r => setTimeout(r, 150));
  v1 = await view();
  ok('shift_roda_horizontal', v1.tx !== v0.tx && v1.ty === v0.ty && v1.s === v0.s, { antes: v0, depois: v1 });

  // 8. roda sozinha anda na vertical
  v0 = await view();
  await page.mouse.wheel({ deltaY: 200 });
  await new Promise(r => setTimeout(r, 150));
  v1 = await view();
  ok('roda_vertical', v1.ty !== v0.ty && v1.s === v0.s, { antes: v0, depois: v1 });

  // 9. tecla 0 e botão enquadrar voltam ao enquadramento
  await page.keyboard.press('0');
  v1 = await view();
  const k0 = Math.abs(v1.s - fitV.s) < 1e-6 && Math.abs(v1.tx - fitV.tx) < .5;
  await page.mouse.move(700, 400); await page.mouse.down({ button: 'right' }); await page.mouse.move(500, 300, { steps: 4 }); await page.mouse.up({ button: 'right' });
  await ctx.click('#fit');
  v1 = await view();
  ok('enquadrar_tecla0_e_botao', k0 && Math.abs(v1.s - fitV.s) < 1e-6 && Math.abs(v1.tx - fitV.tx) < .5, { fit: fitV, depois: v1 });

  // 10. clique num card abre a ficha; Esc fecha
  v0 = await view();
  const [cx, cy] = toScreen(v0, 350 + 112, 556 + 38); // Sessão
  await page.mouse.click(cx, cy);
  const f1 = await ctx.evaluate(() => { const f = document.getElementById('ficha'); return { aberta: !f.hidden, titulo: (f.querySelector('h2') || {}).textContent, texto: f.innerText }; });
  await page.screenshot({ path: path.join(OUT, `${nome}-${W}x${H}-ficha.png`) });
  await page.keyboard.press('Escape');
  const f2 = await ctx.evaluate(() => !document.getElementById('ficha').hidden);
  ok('clique_abre_ficha_esc_fecha', f1.aberta && f1.titulo === 'Sessão' && !f2, { ficha: f1, aberta_depois_esc: f2 });

  // 11. Tab + Enter abre (teclado)
  // clique esquerdo no papel vazio (antes das placas na ordem do documento) define o ponto de partida do Tab
  { const vv = await view(); const [qx, qy] = toScreen(vv, 150, 860); await page.mouse.click(qx, qy); }
  await page.keyboard.press('Tab');
  const foco = await ctx.evaluate(() => document.activeElement && document.activeElement.getAttribute('data-id'));
  await page.keyboard.press('Tab');
  const foco2 = await ctx.evaluate(() => document.activeElement && document.activeElement.getAttribute('data-id'));
  await page.keyboard.press('Enter');
  const f3 = await ctx.evaluate(() => { const f = document.getElementById('ficha'); return { aberta: !f.hidden, titulo: (f.querySelector('h2') || {}).textContent }; });
  await page.keyboard.press('Escape');
  const f4 = await ctx.evaluate(() => ({ aberta: !document.getElementById('ficha').hidden, foco: document.activeElement && document.activeElement.getAttribute('data-id') }));
  ok('tab_enter_abre', foco === 'maestri' && f3.aberta && f3.titulo === 'Peças' && !f4.aberta, { primeiro_tab: foco, segundo_tab: foco2, ficha: f3, depois_esc: f4 });

  // 12. clique esquerdo arrastando sobre card abre ficha mas não anda
  await ctx.evaluate(() => window.__planta.fit());
  const sc2 = await ctx.evaluate(() => ({ x: window.scrollX, y: window.scrollY }));
  ok('documento_nao_rolou', sc2.x === 0 && sc2.y === 0, sc2);

  await ctx.evaluate(() => window.__planta.fit());
  return r;
}

(async () => {
  const resultado = { gerado: new Date().toISOString(), rodadas: [], erros_js: [] };
  const browser = await puppeteer.launch({ executablePath: EDGE, headless: 'new', args: ['--disable-gpu', '--allow-file-access-from-files'] });
  try {
    for (const [W, H] of [[1600, 900], [1280, 800]]) {
      // (a) arquivo direto
      let page = await browser.newPage();
      page.on('pageerror', e => resultado.erros_js.push(`file ${W}: ${e.message}`));
      page.on('console', m => { if (m.type() === 'error') resultado.erros_js.push(`file ${W} console: ${m.text()}`); });
      await page.setViewport({ width: W, height: H });
      await page.goto(URL_FILE, { waitUntil: 'networkidle0' });
      await page.evaluate(() => document.fonts.ready);
      await new Promise(r => setTimeout(r, 1800));
      resultado.rodadas.push(await provar(page, page.mainFrame(), 'file', W, H));
      if (W === 1600) {
        // paridade de conteúdo
        const amostra = await page.evaluate(() => [...document.querySelectorAll('#world text')].map(t => t.textContent.replace(/\s+/g, ' ').trim()).filter(Boolean));
        const atual = textosDoAtual();
        const cont = a => a.reduce((m, s) => (m[s] = (m[s] || 0) + 1, m), {});
        const ca = cont(atual), cb = cont(amostra);
        const faltando = [], novo = [];
        for (const k in ca) if ((cb[k] || 0) < ca[k]) faltando.push({ texto: k, no_atual: ca[k], na_amostra: cb[k] || 0 });
        for (const k in cb) if ((ca[k] || 0) < cb[k]) novo.push({ texto: k, no_atual: ca[k] || 0, na_amostra: cb[k] });
        const ui = await page.evaluate(() => ({ botao: document.getElementById('fit').textContent.trim(), rotulos_ficha: ['chega de', 'vai para', '×'] }));
        fs.writeFileSync(path.join(OUT, 'paridade.json'), JSON.stringify({
          regra: 'Todos os <text> do SVG atual + título, subtítulo, data e legenda HTML do atual, contra todos os <text> do desenho da amostra (com contagem). Texto de interface fora do desenho listado à parte.',
          total_atual: atual.length, total_amostra: amostra.length,
          faltando_na_amostra: faltando, novo_na_amostra: novo,
          interface_fora_do_desenho: ui,
          textos_atual: atual, textos_amostra: amostra
        }, null, 2));
      }
      await page.close();

      // (b) dentro de iframe sandbox allow-scripts, servido por http
      page = await browser.newPage();
      page.on('pageerror', e => resultado.erros_js.push(`iframe ${W}: ${e.message}`));
      page.on('console', m => { if (m.type() === 'error') resultado.erros_js.push(`iframe ${W} console: ${m.text()}`); });
      await page.setViewport({ width: W, height: H });
      await page.goto(URL_IFRAME, { waitUntil: 'networkidle0' });
      await new Promise(r => setTimeout(r, 2000));
      const frame = page.frames().find(f => f.url().includes('system-design-planta'));
      const sandbox = await page.evaluate(() => document.querySelector('iframe').getAttribute('sandbox'));
      const origem = await frame.evaluate(() => { try { return String(window.origin); } catch (e) { return 'erro'; } });
      const r = await provar(page, frame, 'iframe', W, H);
      r.sandbox = sandbox; r.origem_no_iframe = origem;
      resultado.rodadas.push(r);
      await page.close();
    }
  } finally { await browser.close(); }
  resultado.tudo_ok = resultado.rodadas.every(r => Object.values(r.checagens).every(c => c.ok)) && resultado.erros_js.length === 0;
  fs.writeFileSync(path.join(OUT, 'resultado-interacao.json'), JSON.stringify(resultado, null, 2));
  const resumo = resultado.rodadas.map(r => `${r.contexto} ${r.janela}: ` + Object.entries(r.checagens).map(([k, c]) => `${k}=${c.ok ? 'ok' : 'FALHA'}`).join(' ')).join('\n');
  console.log(resumo + '\nerros_js: ' + resultado.erros_js.length + '\ntudo_ok: ' + resultado.tudo_ok);
})();
