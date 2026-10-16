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
const SHOT = process.argv[4] || '.';
const R = { URL: URL.replace(/:\d+/, ':<porta>'), data: new Date().toISOString(), tamanhos: {} };
const rd = n => +n.toFixed(1);



const EXPR_BANCO = `(function(){var r=document.querySelector('[data-item="Banco local"]').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`;
const FICHA = `document.getElementById('ficha').classList.contains('aberta')`;
for (const [W,H] of [[1920,1080],[320,640],[1280,1000]]) {
  const T = {}; R.tamanhos[`${W}x${H}`] = T; T.rodadas = [];
  for (const modo of ['como_antes','arrasto_curto_longe_do_bairro','dois_toques_seguidos_sem_arrasto']) {
    await abrir(W,H,true);
    await ev(`(function(){window.__ev=[];['pointerdown','pointerup','pointercancel','click','lostpointercapture'].forEach(function(n){document.addEventListener(n,function(e){var t=e.target;window.__ev.push(n+':'+(t.tagName||'')+(t.getAttribute&&t.getAttribute('class')?'.'+t.getAttribute('class'):''))},true)})})()`);
    const b = await ev(EXPR_BANCO); const r = {modo};
    if (modo==='como_antes') {
      await toqueEv('touchStart',[{x:b.x-40,y:b.y-20,id:0}]); for(let i=1;i<=6;i++){ await toqueEv('touchMove',[{x:b.x-40+i*40/3,y:b.y-20+i*20/3,id:0}]); await esp(10);}
      await toqueEv('touchEnd',[{x:b.x+40,y:b.y+20,id:0}]); await esp(150);
    } else if (modo==='arrasto_curto_longe_do_bairro') {
      const st = await estado(); const x=st.tela.l+20,y=st.tela.t+st.tela.h*.5;
      await toqueEv('touchStart',[{x,y,id:0}]); for(let i=1;i<=6;i++){ await toqueEv('touchMove',[{x:x+10*i,y,id:0}]); await esp(10);}
      await toqueEv('touchEnd',[{x:x+60,y,id:0}]); await esp(150);
    }
    r.ficha_apos_arrasto = await ev(FICHA);
    const b2 = await ev(EXPR_BANCO);
    r.banco_antes=b; r.banco_depois=b2;
    r.elemento_no_ponto = await ev(`(function(){var e=document.elementFromPoint(${b2.x},${b2.y});return e?(e.tagName+'.'+(e.getAttribute('class')||'')):null})()`);
    r.dentro_da_tela = await ev(`(function(){var t=document.getElementById('tela').getBoundingClientRect();return ${b2.x}>t.left&&${b2.x}<t.right&&${b2.y}>t.top&&${b2.y}<t.bottom})()`);
    await ev(`window.__ev=[]`);
    await toqueEv('touchStart',[{x:b2.x,y:b2.y,id:0}]); await toqueEv('touchEnd',[{x:b2.x,y:b2.y,id:0}]); await esp(200);
    r.ficha_apos_toque_seguinte = await ev(FICHA);
    r.eventos_do_toque = await ev(`window.__ev.join(' ')`);
    T.rodadas.push(r);
  }
  await cmd('Emulation.setTouchEmulationEnabled',{enabled:false});
}
fs.writeFileSync(SAIDA, JSON.stringify(R,null,1));
try{ws.close()}catch{}
edge.kill(); srv.close(); setTimeout(()=>process.exit(0),500);

