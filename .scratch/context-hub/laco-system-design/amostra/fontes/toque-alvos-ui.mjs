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
const perfil = process.argv[4];
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



const GRAVA = `(function(){window.__ev=[];['pointerdown','pointermove','pointerup','pointercancel','lostpointercapture','gotpointercapture','click'].forEach(function(n){document.addEventListener(n,function(e){window.__ev.push(n+':'+e.target.tagName+(e.target.getAttribute&&e.target.getAttribute('class')?'.'+e.target.getAttribute('class'):''))},true)});return 1})()`;
for (const [W,H] of [[1280,1000],[320,640]]) {
  const T = {}; R.tamanhos[`${W}x${H}`] = T;
  const alvos = {
    fundo_do_svg: `(function(){var t=document.getElementById('tela').getBoundingClientRect();return {x:t.left+8,y:t.top+t.height*.5}})()`,
    em_cima_do_Banco_local: `(function(){var r=document.querySelector('[data-item="Banco local"]').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`,
    em_cima_de_um_nome: `(function(){var t=[].slice.call(document.querySelectorAll('svg.cidade text')).filter(function(e){var r=e.getBoundingClientRect(),tr=document.getElementById('tela').getBoundingClientRect();return !e.closest('.detalhe')&&r.width>0&&r.left>tr.left+10&&r.right<tr.right-10&&r.top>tr.top+10&&r.bottom<tr.bottom-70})[0];var r=t.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`
  };
  for (const [nome, expr] of Object.entries(alvos)) {
    await abrir(W,H,true); await ev(GRAVA); const t0 = await estado(); const p = await ev(expr);
    await toqueEv('touchStart',[{x:p.x,y:p.y,id:0}]);
    for (let i=1;i<=8;i++){ await toqueEv('touchMove',[{x:p.x+12*i,y:p.y+6*i,id:0}]); await esp(20); }
    await toqueEv('touchEnd',[{x:p.x+96,y:p.y+48,id:0}]); await esp(150);
    const t1 = await estado();
    T[nome] = { moveu_banco_px:[rd(t1.banco.x-t0.banco.x),rd(t1.banco.y-t0.banco.y)], pedido:[96,48], ficha_aberta:t1.ficha, eventos:(await ev('window.__ev.slice(0,8).join(" ")')) };
  }
  await cmd('Emulation.setTouchEmulationEnabled',{enabled:false});
}
fs.writeFileSync(SAIDA, JSON.stringify(R,null,1));
try{ws.close()}catch{}
edge.kill();srv.close();setTimeout(()=>process.exit(0),500);
