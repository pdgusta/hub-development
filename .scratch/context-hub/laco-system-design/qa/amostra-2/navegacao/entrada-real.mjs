// Navegação do canvas com entrada real do navegador (protocolo de depuração do Edge): mouse, roda, teclado e toque.
// Uso: node entrada-real.mjs <raiz-do-laco> <saida.json>
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const RAIZ = process.argv[2], SAIDA = process.argv[3];
const EDGE = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe' : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png' };
const srv = http.createServer((q, r) => {
  const p = path.join(RAIZ, decodeURIComponent(q.url.split('?')[0]));
  if (!p.startsWith(RAIZ) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); r.end(); return; }
  r.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r);
});
await new Promise(ok => srv.listen(0, '127.0.0.1', ok));
const PORTA = srv.address().port, URL = `http://127.0.0.1:${PORTA}/amostra/amostra.html`;
const DBG = 9300 + Math.floor(Math.random() * 500);
const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'qa-real-'));
const edge = spawn(EDGE, ['--headless=new', '--disable-gpu', '--no-first-run', `--user-data-dir=${perfil}`, `--remote-debugging-port=${DBG}`, 'about:blank'], { stdio: 'ignore' });
const esp = ms => new Promise(r => setTimeout(r, ms));
async function json(u) { for (let i = 0; i < 60; i++) { try { return await (await fetch(u)).json(); } catch { await esp(250); } } throw new Error('sem Edge'); }
const alvos = await json(`http://127.0.0.1:${DBG}/json`);
const pag = alvos.find(a => a.type === 'page');
const ws = new WebSocket(pag.webSocketDebuggerUrl);
await new Promise(ok => ws.addEventListener('open', ok));
let id = 0; const pend = new Map();
ws.addEventListener('message', m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } });
const cmd = (method, params = {}) => new Promise(ok => { const i = ++id; pend.set(i, ok); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => { const r = await cmd('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }); if (r.result.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails).slice(0, 300)); return r.result.result.value; };
await cmd('Page.enable'); await cmd('Runtime.enable');

const ESTADO = `(function(){var t=document.getElementById('tela'),s=document.querySelector('svg.cidade');var a=s.getAttribute('viewBox').split(' ').map(Number);
 var bl=document.querySelector('[data-item="Banco local"]').getBoundingClientRect();var tr=t.getBoundingClientRect();
 var ae=document.activeElement;
 return {vb:{x:a[0],y:a[1],w:a[2],h:a[3]},nivel:document.getElementById('z-nivel').textContent,banco:{x:bl.left+bl.width/2,y:bl.top+bl.height/2},
  tela:{l:tr.left,t:tr.top,w:tr.width,h:tr.height},scrollY:window.scrollY,scrollX:window.scrollX,docH:document.documentElement.scrollHeight,innerH:innerHeight,innerW:innerWidth,
  sel:String(getSelection()),ficha:document.getElementById('ficha').classList.contains('aberta'),ativo:ae?(ae.id||ae.getAttribute('data-abre')||ae.className&&ae.className.baseVal||ae.tagName):null,
  centro:{x:a[0]+a[2]/2,y:a[1]+a[3]/2},perto:s.classList.contains('perto'),telaScroll:[t.scrollTop,t.scrollLeft]}})()`;
const estado = () => ev(ESTADO);
async function abrir(w, h, toque = false) {
  await cmd('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: false });
  await cmd('Emulation.setTouchEmulationEnabled', { enabled: toque, maxTouchPoints: toque ? 5 : 0 });
  await cmd('Page.navigate', { url: URL });
  for (let i = 0; i < 60; i++) { await esp(250); try { if (await ev(`document.readyState==='complete'&&!!document.getElementById('z-nivel')&&document.getElementById('z-nivel').textContent!==''`)) break; } catch { } }
  await esp(500);
}
const mouse = (type, x, y, o = {}) => cmd('Input.dispatchMouseEvent', Object.assign({ type, x, y, button: 'none', buttons: 0, clickCount: 0, modifiers: 0 }, o));
async function arrasto(botao, x0, y0, dx, dy, passos = 8) {
  const b = botao === 'right' ? 2 : botao === 'middle' ? 4 : 1;
  await mouse('mouseMoved', x0, y0);
  await mouse('mousePressed', x0, y0, { button: botao, buttons: b, clickCount: 1 });
  for (let i = 1; i <= passos; i++) await mouse('mouseMoved', x0 + dx * i / passos, y0 + dy * i / passos, { button: botao, buttons: b });
  await mouse('mouseReleased', x0 + dx, y0 + dy, { button: botao, buttons: 0, clickCount: 1 });
  await esp(60);
}
async function roda(x, y, dx, dy, modifiers = 0) { await mouse('mouseWheel', x, y, { deltaX: dx, deltaY: dy, modifiers }); await esp(60); }
async function tecla(key, extra = {}) {
  const t = key.length === 1 ? key : undefined;
  const cod = { ArrowLeft: 37, ArrowRight: 39, ArrowUp: 38, ArrowDown: 40, '0': 48, '+': 187, '-': 189, Tab: 9, Escape: 27, Enter: 13 }[key];
  await cmd('Input.dispatchKeyEvent', Object.assign({ type: 'keyDown', key, text: t, windowsVirtualKeyCode: cod }, extra));
  await cmd('Input.dispatchKeyEvent', Object.assign({ type: 'keyUp', key, windowsVirtualKeyCode: cod }, extra));
  await esp(40);
}
const toqueEv = (type, pts) => cmd('Input.dispatchTouchEvent', { type, touchPoints: pts.map((p, i) => ({ x: p.x, y: p.y, id: p.id ?? i })) });
const R = { URL: URL.replace(/:\d+/, ':<porta>'), data: new Date().toISOString(), tamanhos: {} };
const rd = n => +n.toFixed(1);

const TAMANHOS = [[1280, 1000], [960, 800], [1280, 720], [1920, 1080], [320, 640]];
for (const [W, H] of TAMANHOS) {
  const T = {}; R.tamanhos[`${W}x${H}`] = T;
  try {
    // ---- vista inicial
    await abrir(W, H);
    let s = await estado();
    T.inicial = { nivel: s.nivel, vb: s.vb, tela: s.tela, docH: s.docH, innerH: s.innerH, scrollY: s.scrollY };
    T.inicial.cabecalho_px = await ev(`(function(){var t=document.getElementById('tela').getBoundingClientRect();return Math.round(t.top)})()`);
    T.inicial.gustavo_sob_botoes = await ev(`(function(){var z=document.querySelector('.zoom').getBoundingClientRect();var g=[].slice.call(document.querySelectorAll('[data-item="Gustavo"],.pessoa'));
      return g.some(function(e){var r=e.getBoundingClientRect();return r.width&&r.left<z.right&&r.right>z.left&&r.top<z.bottom&&r.bottom>z.top})})()`);
    T.inicial.cidade_inteira_na_tela = await ev(`(function(){var m=document.querySelector('.muralha').getBoundingClientRect(),t=document.getElementById('tela').getBoundingClientRect();return m.left>=t.left-1&&m.right<=t.right+1&&m.top>=t.top-1&&m.bottom<=t.bottom+1})()`);
    T.inicial.menor_texto_px = await ev(`(function(){var h=1e9;document.querySelectorAll('svg.cidade text').forEach(function(t){if(t.closest('.detalhe'))return;var r=t.getBoundingClientRect();if(r.height>0&&r.height<h)h=r.height});return Math.round(h*10)/10})()`);

    // ---- arrastos seguidos com o botão direito, apertando em cima do bairro / do nome / do vazio
    const pontos = await ev(`(function(){var tr=document.getElementById('tela').getBoundingClientRect();function c(sel){var e=document.querySelector(sel);if(!e)return null;var r=e.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}}
      return {banco:c('[data-item="Banco local"]'),vazio:{x:tr.left+tr.width*.5,y:tr.top+tr.height*.5},tela:{l:tr.left,t:tr.top,w:tr.width,h:tr.height}}})()`);
    let p = pontos.banco; const dentro = q => q && q.x > pontos.tela.l + 30 && q.x < pontos.tela.l + pontos.tela.w - 30 && q.y > pontos.tela.t + 30 && q.y < pontos.tela.t + pontos.tela.h - 90;
    if (!dentro(p)) p = pontos.vazio;
    for (const botao of ['right', 'middle']) {
      await abrir(W, H); const arr = [];
      for (let i = 0; i < 4; i++) {
        const a = await ev(`(function(){var r=document.querySelector('[data-item="Banco local"]').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`);
        const antes = await estado();
        const x0 = dentro(a) ? a.x : p.x, y0 = dentro(a) ? a.y : p.y;
        await mouse('mouseMoved', x0, y0); const cx = Math.sign(i % 2 ? -1 : 1) * 100; // alterna o sentido
        await mouse('mousePressed', x0, y0, { button: botao, buttons: botao === 'right' ? 2 : 4, clickCount: 1 });
        const noAperto = await estado();
        for (let k = 1; k <= 8; k++) await mouse('mouseMoved', x0 + cx * k / 8, y0 + 60 * k / 8, { button: botao, buttons: botao === 'right' ? 2 : 4 });
        await mouse('mouseReleased', x0 + cx, y0 + 60, { button: botao, buttons: 0, clickCount: 1 });
        await esp(80);
        const depois = await estado();
        arr.push({ n: i + 1, pedido: [cx, 60], banco_antes: [rd(antes.banco.x), rd(antes.banco.y)],
          salto_no_aperto_px: rd(Math.hypot(noAperto.banco.x - antes.banco.x, noAperto.banco.y - antes.banco.y)),
          moveu_px: [rd(depois.banco.x - antes.banco.x), rd(depois.banco.y - antes.banco.y)],
          erro_px: rd(Math.hypot(depois.banco.x - antes.banco.x - cx, depois.banco.y - antes.banco.y - 60)),
          ficha_aberta: depois.ficha, scrollY: depois.scrollY, tela_scroll: depois.telaScroll, ativo: depois.ativo, selecao: depois.sel.length });
      }
      T[`arrasto_${botao}`] = arr;
    }

    // ---- arrasto esquerdo: não anda e não seleciona texto
    await abrir(W, H);
    s = await estado(); const e0 = s.vb;
    const tx = await ev(`(function(){var e=document.querySelector('svg.cidade text');var r=e.getBoundingClientRect();return {x:r.left+2,y:r.top+r.height/2}})()`);
    await arrasto('left', Math.max(5, tx.x), Math.max(70, tx.y), 200, 40);
    s = await estado(); T.arrasto_esquerdo = { vb_mudou: JSON.stringify(s.vb) !== JSON.stringify(e0), selecao_chars: s.sel.length, ficha_aberta: s.ficha };

    // ---- roda
    await abrir(W, H); s = await estado();
    const cxm = s.tela.l + s.tela.w * .35, cym = s.tela.t + s.tela.h * .4;
    const ponto = async () => ev(`(function(){var s=document.querySelector('svg.cidade'),p=s.createSVGPoint();p.x=${cxm};p.y=${cym};var m=s.getScreenCTM().inverse();var q=p.matrixTransform(m);return {x:q.x,y:q.y}})()`);
    const q0 = await ponto(); await roda(cxm, cym, 0, -200, 2); const sz = await estado(); const q1 = await ponto();
    T.ctrl_roda = { nivel_antes: s.nivel, nivel_depois: sz.nivel, ponto_sob_o_mouse_moveu_unid: rd(Math.hypot(q1.x - q0.x, q1.y - q0.y)), scrollY: sz.scrollY, pagina_zoom_do_navegador: await ev('visualViewport.scale') };
    const v1 = (await estado()).vb; await roda(cxm, cym, 0, 120, 8); const v2 = (await estado()).vb;
    T.shift_roda = { dx_unid: rd(v2.x - v1.x), dy_unid: rd(v2.y - v1.y) };
    const v3 = (await estado()).vb; await roda(cxm, cym, 0, 120, 0); const v4 = (await estado()).vb;
    T.roda_simples = { dx_unid: rd(v4.x - v3.x), dy_unid: rd(v4.y - v3.y), scrollY: (await estado()).scrollY };

    // ---- + e - em volta do centro (teclas reais, foco no desenho)
    await abrir(W, H);
    await ev(`document.getElementById('tela').focus()`);
    const c0 = (await estado()).centro;
    for (let i = 0; i < 3; i++) await tecla('+');
    const cm = await estado();
    for (let i = 0; i < 3; i++) await tecla('-');
    const c1 = await estado();
    T.mais_menos = { centro_antes: [rd(c0.x), rd(c0.y)], centro_apos_mais3: [rd(cm.centro.x), rd(cm.centro.y)], centro_apos_menos3: [rd(c1.centro.x), rd(c1.centro.y)], nivel_apos_mais3: cm.nivel, nivel_final: c1.nivel };
    // setas e 0
    const a0 = (await estado()).vb; await tecla('ArrowRight'); const a1 = (await estado()).vb; await tecla('ArrowDown'); const a2 = (await estado()).vb;
    T.setas = { dx_unid: rd(a1.x - a0.x), dy_unid: rd(a2.y - a1.y) };
    for (let i = 0; i < 2; i++) await tecla('+');
    await tecla('0'); const z0 = await estado();
    T.tecla_zero = { nivel: z0.nivel, vb: z0.vb };
    T.tecla_zero.cidade_inteira = await ev(`(function(){var m=document.querySelector('.muralha').getBoundingClientRect(),t=document.getElementById('tela').getBoundingClientRect(),z=document.querySelector('.zoom').getBoundingClientRect();
      return {dentro:m.left>=t.left-1&&m.right<=t.right+1&&m.top>=t.top-1&&m.bottom<=t.bottom+1,sob_botoes:(function(){var g=document.querySelectorAll('.item,.bairro>.zona');var n=0;g.forEach(function(e){var r=e.getBoundingClientRect();if(r.width&&r.left<z.right&&r.right>z.left&&r.top<z.bottom&&r.bottom>z.top)n++});return n})()}})()`);
    // zoom mínimo e máximo
    for (let i = 0; i < 45; i++) await tecla('+'); const zmax = (await estado()).nivel;
    for (let i = 0; i < 70; i++) await tecla('-'); const zmin = (await estado()).nivel;
    T.limites = { max: zmax, min: zmin };

    // ---- "Ver tudo" com clique real do mouse
    await abrir(W, H);
    for (let i = 0; i < 3; i++) await tecla('+');
    const bt = await ev(`(function(){var r=document.getElementById('z-tudo').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`);
    const antesV = await estado();
    await mouse('mouseMoved', bt.x, bt.y); await mouse('mousePressed', bt.x, bt.y, { button: 'left', buttons: 1, clickCount: 1 }); await mouse('mouseReleased', bt.x, bt.y, { button: 'left', clickCount: 1 }); await esp(120);
    const tudo = await estado();
    T.ver_tudo = { nivel_antes: antesV.nivel, nivel_depois: tudo.nivel, vb_igual_ao_zero: null };
    T.ver_tudo.cidade_inteira = await ev(`(function(){var m=document.querySelector('.muralha').getBoundingClientRect(),t=document.getElementById('tela').getBoundingClientRect(),z=document.querySelector('.zoom').getBoundingClientRect();
      var n=0;document.querySelectorAll('.item,.bairro>.zona,.pessoa').forEach(function(e){var r=e.getBoundingClientRect();if(r.width&&r.left<z.right&&r.right>z.left&&r.top<z.bottom&&r.bottom>z.top)n++});
      return {dentro:m.left>=t.left-1&&m.right<=t.right+1&&m.top>=t.top-1&&m.bottom<=t.bottom+1,sob_botoes:n,menor_texto_px:(function(){var h=1e9;document.querySelectorAll('svg.cidade text').forEach(function(t){if(t.closest('.detalhe'))return;var r=t.getBoundingClientRect();if(r.height>0&&r.height<h)h=r.height});return Math.round(h*10)/10})()}})()`);
    await ev(`document.getElementById('tela').focus()`); for (let i = 0; i < 3; i++) await tecla('+'); await tecla('0'); const zz = await estado();
    T.ver_tudo.vb_igual_ao_zero = JSON.stringify(zz.vb) === JSON.stringify(tudo.vb);

    // ---- toque (se o navegador emula)
    await abrir(W, H, true);
    const tq = {}; R.tamanhos[`${W}x${H}`].toque = tq;
    const bm = await ev(`(function(){var r=document.getElementById('z-mais').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`);
    const n0 = (await estado()).nivel;
    await toqueEv('touchStart', [{ x: bm.x, y: bm.y }]); await toqueEv('touchEnd', []); await esp(150);
    tq.toque_no_mais = { nivel_antes: n0, nivel_depois: (await estado()).nivel };
    await abrir(W, H, true);
    const bb = await ev(`(function(){var r=document.querySelector('[data-item="Banco local"]').getBoundingClientRect();var t=document.getElementById('tela').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2,ok:r.left>t.left&&r.right<t.right&&r.top>t.top&&r.bottom<t.bottom}})()`);
    await toqueEv('touchStart', [{ x: bb.x, y: bb.y }]); await toqueEv('touchEnd', []); await esp(200);
    const fi = await estado(); tq.toque_no_banco = { visivel: bb.ok, ficha_aberta: fi.ficha };
    // arrasto de um dedo
    await abrir(W, H, true); const t0 = await estado();
    const px0 = t0.tela.l + t0.tela.w * .5, py0 = t0.tela.t + t0.tela.h * .5;
    await toqueEv('touchStart', [{ x: px0, y: py0 }]);
    for (let i = 1; i <= 8; i++) { await toqueEv('touchMove', [{ x: px0 - 12 * i, y: py0 - 6 * i }]); await esp(15); }
    await toqueEv('touchEnd', []); await esp(150); const t1 = await estado();
    tq.um_dedo = { moveu_banco_px: [rd(t1.banco.x - t0.banco.x), rd(t1.banco.y - t0.banco.y)], pedido: [-96, -48], ficha_aberta: t1.ficha };
    // pinça: dois dedos se afastam, depois tira um dedo e move o outro 2 px
    await abrir(W, H, true); const p0 = await estado();
    const mx = p0.tela.l + p0.tela.w * .5, my = p0.tela.t + p0.tela.h * .5;
    await toqueEv('touchStart', [{ x: mx - 40, y: my, id: 1 }, { x: mx + 40, y: my, id: 2 }]);
    for (let i = 1; i <= 8; i++) { await toqueEv('touchMove', [{ x: mx - 40 - 10 * i, y: my, id: 1 }, { x: mx + 40 + 10 * i, y: my, id: 2 }]); await esp(15); }
    const pz = await estado();
    tq.pinca = { nivel_antes: p0.nivel, nivel_depois: pz.nivel };
    // tirar um dedo (o 1) e mover o 2 em 2 px
    await toqueEv('touchEnd', [{ x: mx + 120, y: my, id: 2 }]); await esp(60);
    const r0 = await estado();
    await toqueEv('touchMove', [{ x: mx + 122, y: my, id: 2 }]); await esp(60);
    const r1 = await estado();
    tq.tirar_um_dedo = { banco_deslocou_px: [rd(r1.banco.x - r0.banco.x), rd(r1.banco.y - r0.banco.y)], pedido_px: [2, 0], nivel_estavel: r0.nivel === r1.nivel };
    await toqueEv('touchEnd', []); await esp(100);
    const rf = await estado(); tq.apos_soltar_tudo = { ficha_aberta: rf.ficha };
    // tela cheia: ficha cobre a tela? (320) papel modal
    await abrir(W, H, true);
    const f2 = await ev(`(function(){var b=document.querySelector('.bairro');b.dispatchEvent(new MouseEvent('click',{bubbles:true}));var f=document.getElementById('ficha');var r=f.getBoundingClientRect();return {aberta:f.classList.contains('aberta'),larg:r.width,tela:innerWidth,role:f.getAttribute('role'),modal:f.getAttribute('aria-modal'),topo_inert:[].slice.call(document.querySelectorAll('header,main,.tela')).some(function(e){return e.inert})}})()`);
    tq.ficha = f2;
    await cmd('Emulation.setTouchEmulationEnabled', { enabled: false });
  } catch (e) { T.erro = String(e).slice(0, 400); }
}

// ---- Tab real: foco visível em cada parada (1280 x 1000)
try {
  await abrir(1280, 1000);
  await ev(`document.activeElement&&document.activeElement.blur&&document.activeElement.blur();document.body.focus()`);
  const paradas = [];
  const LER = `(function(){var e=document.activeElement;if(!e||e===document.body)return null;var cs=getComputedStyle(e);var z=e.querySelector&&e.querySelector(':scope>.zona,:scope .anel');var zc=z?getComputedStyle(z):null;
   var r=e.getBoundingClientRect();
   return {nome:(e.getAttribute('aria-label')||e.textContent||'').trim().slice(0,40),tag:e.tagName.toLowerCase(),focus_visible:e.matches(':focus-visible'),outline:cs.outlineStyle+' '+cs.outlineWidth,
    filho:zc?{stroke:zc.stroke,strokeWidth:zc.strokeWidth,fill:zc.fill}:null,
    na_tela:r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight}})()`;
  // linha de base do filho .zona sem foco
  const base = await ev(`(function(){var z=document.querySelector('.bairro>.zona'),c=getComputedStyle(z);return {stroke:c.stroke,strokeWidth:c.strokeWidth}})()`);
  for (let i = 0; i < 34; i++) { await tecla('Tab'); const a = await ev(LER); if (!a) break; paradas.push(a); if (a.nome === '' && paradas.length > 30) break; }
  R.tab_real = { base_zona: base, total: paradas.length, paradas: paradas.map((p, i) => Object.assign({ n: i + 1 }, p, { muda: p.filho ? (p.filho.strokeWidth !== base.strokeWidth || p.filho.stroke !== base.stroke) : null })) };
} catch (e) { R.tab_real = { erro: String(e).slice(0, 300) }; }

fs.writeFileSync(SAIDA, JSON.stringify(R, null, 1));
try { ws.close(); } catch { }
edge.kill(); srv.close();
setTimeout(() => process.exit(0), 500);
