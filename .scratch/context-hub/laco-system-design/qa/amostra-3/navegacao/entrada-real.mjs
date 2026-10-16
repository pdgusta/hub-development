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
async function shot(nome){ const r = await cmd('Page.captureScreenshot',{format:'png'}); fs.writeFileSync(path.join(SHOT,nome), Buffer.from(r.result.data,'base64')); }
const FICHA = `document.getElementById('ficha').classList.contains('aberta')`;
const TAMANHOS = [[1280,1000],[960,800],[1280,720],[1920,1080],[320,640]];
for (const [W,H] of TAMANHOS) {
  const T = {}; R.tamanhos[`${W}x${H}`] = T;
  try {
    await abrir(W,H);
    let s = await estado();
    T.inicial = { nivel:s.nivel, tela:s.tela, docH:s.docH, innerH:s.innerH, scrollY:s.scrollY };
    T.inicial.gustavo_sob_botoes = await ev(`(function(){var z=document.querySelector('.zoom').getBoundingClientRect();return [].slice.call(document.querySelectorAll('.pessoa')).some(function(e){var r=e.getBoundingClientRect();return r.width&&r.left<z.right&&r.right>z.left&&r.top<z.bottom&&r.bottom>z.top})})()`);
    T.inicial.cidade_inteira = await ev(`(function(){var m=document.querySelector('.muralha').getBoundingClientRect(),t=document.getElementById('tela').getBoundingClientRect();return m.left>=t.left-1&&m.right<=t.right+1&&m.top>=t.top-1&&m.bottom<=t.bottom+1})()`);
    T.inicial.menor_texto_px = await ev(`(function(){var h=1e9;document.querySelectorAll('svg.cidade text').forEach(function(t){if(t.closest('.detalhe'))return;var r=t.getBoundingClientRect();if(r.height>0&&r.height<h)h=r.height});return Math.round(h*10)/10})()`);
    T.cabecalho = await ev(`(function(){function r(e){if(!e)return null;var b=e.getBoundingClientRect();return {t:Math.round(b.top),b:Math.round(b.bottom),h:Math.round(b.height),w:Math.round(b.width)}}
      var cb=document.querySelector('.cen-botoes');var bs=[].slice.call(cb.querySelectorAll('button'));
      var vis=bs.filter(function(b){var q=b.getBoundingClientRect(),c=cb.getBoundingClientRect();return q.left>=c.left-1&&q.right<=c.right+1}).length;
      var cs=getComputedStyle(cb);var lg=document.querySelector('.legendas');
      return {topo:r(document.querySelector('.topo')),header:r(document.querySelector('header')),legendas:r(lg),legendas_visivel:getComputedStyle(lg).display!=='none'&&lg.getBoundingClientRect().height>0,cenarios:r(document.querySelector('.cenarios')),fileira:r(cb),
       botoes:bs.length,botoes_inteiros_visiveis:vis,scrollW:cb.scrollWidth,clientW:cb.clientWidth,rola_p_lado:cb.scrollWidth>cb.clientWidth+1,overflowX:cs.overflowX,wrap:cs.flexWrap,
       tela_top:Math.round(document.getElementById('tela').getBoundingClientRect().top),tela_h:Math.round(document.getElementById('tela').getBoundingClientRect().height),
       dobra_visivel:document.getElementById('dobra-leg').getBoundingClientRect().width>0}})()`);
    if ((W===1280&&H===720)||(W===960&&H===800)||(W===1280&&H===1000)) await shot(`cabecalho-${W}x${H}.png`);
    if (W===960) {
      T.fileira_960 = await ev(`(function(){var cb=document.querySelector('.cen-botoes');cb.scrollLeft=cb.scrollWidth;var u=[].slice.call(cb.querySelectorAll('button')).pop().getBoundingClientRect(),c=cb.getBoundingClientRect();return {ultimo_alcancavel:u.right<=c.right+1,scrollLeft:Math.round(cb.scrollLeft)}})()`);
      await shot('fileira-960x800-rolada.png');
      await ev(`document.querySelector('.cen-botoes').scrollLeft=0`);
      const rf = await ev(`(function(){var r=document.querySelector('.cen-botoes').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`);
      const sl0 = await ev(`document.querySelector('.cen-botoes').scrollLeft`);
      await roda(rf.x, rf.y, 0, 150, 8); const sl1 = await ev(`document.querySelector('.cen-botoes').scrollLeft`);
      T.fileira_960.shift_roda_na_fileira = [sl0, sl1];
      await ev(`document.querySelector('.cen-botoes').scrollLeft=0`);
    }
    if ((W===1280&&H===720) || W===960) {
      const lb = await ev(`(function(){var r=document.getElementById('dobra-leg').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2,w:r.width}})()`);
      if (lb.w>0) { await mouse('mouseMoved',lb.x,lb.y); await mouse('mousePressed',lb.x,lb.y,{button:'left',buttons:1,clickCount:1}); await mouse('mouseReleased',lb.x,lb.y,{button:'left',clickCount:1}); await esp(150);
        T.legenda_aberta = await ev(`(function(){var l=document.querySelector('.legendas');return {expanded:document.getElementById('dobra-leg').getAttribute('aria-expanded'),h:Math.round(l.getBoundingClientRect().height),tela_top:Math.round(document.getElementById('tela').getBoundingClientRect().top),tela_h:Math.round(document.getElementById('tela').getBoundingClientRect().height)}})()`);
        await shot(`legenda-aberta-${W}x${H}.png`);
        await mouse('mouseMoved',lb.x,lb.y); await mouse('mousePressed',lb.x,lb.y,{button:'left',buttons:1,clickCount:1}); await mouse('mouseReleased',lb.x,lb.y,{button:'left',clickCount:1}); await esp(100); }
    }
    for (const botao of ['right','middle']) {
      await abrir(W,H); const arr=[]; const b=botao==='right'?2:4;
      for (let i=0;i<4;i++) {
        const a = await ev(EXPR_BANCO); const antes = await estado();
        const tr = antes.tela; const ok = a.x>tr.l+30&&a.x<tr.l+tr.w-30&&a.y>tr.t+30&&a.y<tr.t+tr.h-90;
        const x0 = ok?a.x:tr.l+tr.w/2, y0 = ok?a.y:tr.t+tr.h/2, cx = (i%2?-100:100);
        await mouse('mouseMoved',x0,y0); await mouse('mousePressed',x0,y0,{button:botao,buttons:b,clickCount:1});
        const noAperto = await estado();
        for (let k=1;k<=8;k++) await mouse('mouseMoved',x0+cx*k/8,y0+60*k/8,{button:botao,buttons:b});
        await mouse('mouseReleased',x0+cx,y0+60,{button:botao,buttons:0,clickCount:1}); await esp(80);
        const d = await estado();
        arr.push({n:i+1,salto_no_aperto_px:rd(Math.hypot(noAperto.banco.x-antes.banco.x,noAperto.banco.y-antes.banco.y)),moveu_px:[rd(d.banco.x-antes.banco.x),rd(d.banco.y-antes.banco.y)],pedido:[cx,60],
          erro_px:rd(Math.hypot(d.banco.x-antes.banco.x-cx,d.banco.y-antes.banco.y-60)),ficha_aberta:d.ficha,scrollY:d.scrollY,selecao:d.sel.length});
      }
      T[`arrasto_${botao}`] = arr;
    }
    await abrir(W,H);
    let a = await ev(EXPR_BANCO); { const st=await estado(); if(!(a.x>st.tela.l+30&&a.y>st.tela.t+30&&a.x<st.tela.l+st.tela.w-30&&a.y<st.tela.t+st.tela.h-90)) a={x:st.tela.l+st.tela.w/2,y:st.tela.t+st.tela.h/2}; }
    await arrasto('right',a.x,a.y,40,30);
    a = await ev(EXPR_BANCO);
    await mouse('mouseMoved',a.x,a.y); await mouse('mousePressed',a.x,a.y,{button:'left',buttons:1,clickCount:1}); await mouse('mouseReleased',a.x,a.y,{button:'left',buttons:0,clickCount:1}); await esp(150);
    T.clique_apos_arrasto = await ev(`({ficha:${FICHA},alvo:(function(){var l=document.querySelector('#ficha li.alvo');return l?l.firstChild.textContent:null})(),role:document.getElementById('ficha').getAttribute('role')})`);
    await tecla('Escape'); await esp(100);
    T.clique_apos_arrasto.esc_fecha = await ev(`!${FICHA}`);
    await abrir(W,H); const e0 = (await estado()).vb;
    const tx = await ev(`(function(){var tr=document.getElementById('tela').getBoundingClientRect();var e=[].slice.call(document.querySelectorAll('svg.cidade text')).filter(function(t){var r=t.getBoundingClientRect();return r.top>tr.top+10&&r.left>5})[0];var r=e.getBoundingClientRect();return {x:r.left+2,y:r.top+r.height/2}})()`);
    await arrasto('left',tx.x,tx.y,200,40); s = await estado();
    T.arrasto_esquerdo = {vb_mudou:JSON.stringify(s.vb)!==JSON.stringify(e0),selecao_chars:s.sel.length,ficha_aberta:s.ficha};
    await abrir(W,H); s = await estado();
    const cxm = s.tela.l+s.tela.w*.35, cym = s.tela.t+s.tela.h*.4;
    const ponto = async()=>ev(`(function(){var s=document.querySelector('svg.cidade'),p=s.createSVGPoint();p.x=${cxm};p.y=${cym};var q=p.matrixTransform(s.getScreenCTM().inverse());return {x:q.x,y:q.y}})()`);
    const q0 = await ponto(); await roda(cxm,cym,0,-200,2); const sz = await estado(); const q1 = await ponto();
    T.ctrl_roda = {nivel_antes:s.nivel,nivel_depois:sz.nivel,ponto_moveu_unid:rd(Math.hypot(q1.x-q0.x,q1.y-q0.y)),scrollY:sz.scrollY};
    const v1=(await estado()).vb; await roda(cxm,cym,0,120,8); const v2=(await estado()).vb; T.shift_roda={dx:rd(v2.x-v1.x),dy:rd(v2.y-v1.y)};
    const v3=(await estado()).vb; await roda(cxm,cym,0,120,0); const v4=(await estado()).vb; T.roda_simples={dx:rd(v4.x-v3.x),dy:rd(v4.y-v3.y)};
    await abrir(W,H); await ev(`document.getElementById('tela').focus()`);
    const c0=(await estado()).centro; for(let i=0;i<3;i++) await tecla('+'); const cm=await estado(); for(let i=0;i<3;i++) await tecla('-'); const c1=await estado();
    T.mais_menos={centro_antes:[rd(c0.x),rd(c0.y)],apos_mais3:[rd(cm.centro.x),rd(cm.centro.y)],apos_menos3:[rd(c1.centro.x),rd(c1.centro.y)],nivel_mais3:cm.nivel,nivel_final:c1.nivel};
    await tecla('0'); const z0=await estado();
    T.tecla_zero={nivel:z0.nivel};
    T.tecla_zero.cidade=await ev(`(function(){var m=document.querySelector('.muralha').getBoundingClientRect(),t=document.getElementById('tela').getBoundingClientRect(),z=document.querySelector('.zoom').getBoundingClientRect();var n=0;document.querySelectorAll('.item,.bairro>.zona,.pessoa').forEach(function(e){var r=e.getBoundingClientRect();if(r.width&&r.left<z.right&&r.right>z.left&&r.top<z.bottom&&r.bottom>z.top)n++});
      var h=1e9;document.querySelectorAll('svg.cidade text').forEach(function(t){if(t.closest('.detalhe'))return;var r=t.getBoundingClientRect();if(r.height>0&&r.height<h)h=r.height});
      return {dentro:m.left>=t.left-1&&m.right<=t.right+1&&m.top>=t.top-1&&m.bottom<=t.bottom+1,sob_botoes:n,menor_texto_px:Math.round(h*10)/10}})()`);
    for(let i=0;i<45;i++) await tecla('+'); const zmax=(await estado()).nivel; for(let i=0;i<70;i++) await tecla('-'); T.limites={max:zmax,min:(await estado()).nivel};
    await abrir(W,H); for(let i=0;i<3;i++) await tecla('+');
    const bt = await ev(`(function(){var r=document.getElementById('z-tudo').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`);
    await mouse('mouseMoved',bt.x,bt.y); await mouse('mousePressed',bt.x,bt.y,{button:'left',buttons:1,clickCount:1}); await mouse('mouseReleased',bt.x,bt.y,{button:'left',clickCount:1}); await esp(120);
    const tv = await estado();
    T.ver_tudo={nivel:tv.nivel,vb_igual_ao_zero:JSON.stringify(tv.vb)===JSON.stringify(z0.vb)};
    T.ver_tudo.cidade=await ev(`(function(){var m=document.querySelector('.muralha').getBoundingClientRect(),t=document.getElementById('tela').getBoundingClientRect();return m.left>=t.left-1&&m.right<=t.right+1&&m.top>=t.top-1&&m.bottom<=t.bottom+1})()`);
    if (W===320) await shot('ver-tudo-320x640.png');

    const tq = {}; T.toque = tq;
    await abrir(W,H,true);
    const bm = await ev(`(function(){var r=document.getElementById('z-mais').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`);
    const n0=(await estado()).nivel; await toqueEv('touchStart',[{x:bm.x,y:bm.y,id:0}]); await toqueEv('touchEnd',[{x:bm.x,y:bm.y,id:0}]); await esp(150);
    tq.toque_no_mais={antes:n0,depois:(await estado()).nivel};
    await abrir(W,H,true); let bb = await ev(EXPR_BANCO);
    await toqueEv('touchStart',[{x:bb.x,y:bb.y,id:0}]); await toqueEv('touchEnd',[{x:bb.x,y:bb.y,id:0}]); await esp(200);
    tq.toque_no_banco={ficha:await ev(FICHA),alvo:await ev(`(function(){var l=document.querySelector('#ficha li.alvo');return l?l.firstChild.textContent:null})()`)};
    const ALVOS = {
      fundo_do_desenho:`(function(){var t=document.getElementById('tela').getBoundingClientRect();return {x:t.left+8,y:t.top+t.height*.5}})()`,
      em_cima_do_Banco_local:EXPR_BANCO,
      em_cima_de_um_nome:`(function(){var tr=document.getElementById('tela').getBoundingClientRect();var t=[].slice.call(document.querySelectorAll('svg.cidade text')).filter(function(e){var r=e.getBoundingClientRect();return !e.closest('.detalhe')&&r.width>0&&r.left>tr.left+10&&r.right<tr.right-10&&r.top>tr.top+10&&r.bottom<tr.bottom-70})[0];var r=t.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`
    };
    tq.arrasto_um_dedo = {};
    for (const [nome,expr] of Object.entries(ALVOS)) for (const passos of [8,30]) {
      await abrir(W,H,true); const t0=await estado(); const p=await ev(expr);
      const dx = passos===8?12:-5, dy = passos===8?6:-3;
      await toqueEv('touchStart',[{x:p.x,y:p.y,id:0}]);
      for (let i=1;i<=passos;i++){ await toqueEv('touchMove',[{x:p.x+dx*i,y:p.y+dy*i,id:0}]); await esp(10); }
      const fim = {x:p.x+dx*passos,y:p.y+dy*passos};
      const durante = await ev(`document.getElementById('tela').classList.contains('arrastando')`);
      await toqueEv('touchEnd',[{x:fim.x,y:fim.y,id:0}]); await esp(150);
      const t1=await estado();
      const apos = await ev(`document.getElementById('tela').classList.contains('arrastando')`);
      tq.arrasto_um_dedo[`${nome}_${passos}passos`]={pedido:[dx*passos,dy*passos],moveu_px:[rd(t1.banco.x-t0.banco.x),rd(t1.banco.y-t0.banco.y)],erro_px:rd(Math.hypot(t1.banco.x-t0.banco.x-dx*passos,t1.banco.y-t0.banco.y-dy*passos)),ficha_aberta:t1.ficha,arrastando_durante:durante,arrastando_depois:apos};
    }
    await abrir(W,H,true); { const b=await ev(EXPR_BANCO);
      await toqueEv('touchStart',[{x:b.x-40,y:b.y-20,id:0}]); for(let i=1;i<=6;i++){ await toqueEv('touchMove',[{x:b.x-40+i*40/3,y:b.y-20+i*20/3,id:0}]); await esp(10);}
      await toqueEv('touchEnd',[{x:b.x+40,y:b.y+20,id:0}]); await esp(150);
      const f1=await ev(FICHA); const b2=await ev(EXPR_BANCO);
      await toqueEv('touchStart',[{x:b2.x,y:b2.y,id:0}]); await toqueEv('touchEnd',[{x:b2.x,y:b2.y,id:0}]); await esp(200);
      tq.clique_apos_arrasto={ficha_apos_arrasto:f1,ficha_apos_toque_seguinte:await ev(FICHA)}; }
    await abrir(W,H,true); { const st=await estado(); const x=st.tela.l+st.tela.w*.5,y=st.tela.t+st.tela.h*.5;
      await toqueEv('touchStart',[{x,y,id:0}]); for(let i=1;i<=4;i++){ await toqueEv('touchMove',[{x:x+10*i,y,id:0}]); await esp(10);}
      const antes=await estado();
      await cmd('Input.dispatchTouchEvent',{type:'touchCancel',touchPoints:[]}); await esp(120);
      const dep=await estado(); const arr=await ev(`document.getElementById('tela').classList.contains('arrastando')`);
      const b=await ev(EXPR_BANCO); await toqueEv('touchStart',[{x:b.x,y:b.y,id:0}]); await toqueEv('touchEnd',[{x:b.x,y:b.y,id:0}]); await esp(200);
      tq.cancelamento={moveu_antes_px:[rd(antes.banco.x-st.banco.x),rd(antes.banco.y-st.banco.y)],arrastando_apos_cancelar:arr,vb_mudou_apos_cancelar:JSON.stringify(dep.vb)!==JSON.stringify(antes.vb),ficha_no_toque_seguinte:await ev(FICHA)}; }
    await abrir(W,H,true); { const p0=await estado(); const mx=p0.tela.l+p0.tela.w*.5,my=p0.tela.t+p0.tela.h*.5;
      await toqueEv('touchStart',[{x:mx-40,y:my,id:1},{x:mx+40,y:my,id:2}]);
      for(let i=1;i<=8;i++){ await toqueEv('touchMove',[{x:mx-40-10*i,y:my,id:1},{x:mx+40+10*i,y:my,id:2}]); await esp(15); }
      const pz=await estado();
      await toqueEv('touchEnd',[{x:mx-120,y:my,id:1}]); await esp(80);
      const r0=await estado();
      await toqueEv('touchMove',[{x:mx+122,y:my,id:2}]); await esp(60); const r1=await estado();
      for(let i=1;i<=20;i++){ await toqueEv('touchMove',[{x:mx+122+4*i,y:my+2*i,id:2}]); await esp(10); }
      const r2=await estado();
      await toqueEv('touchEnd',[{x:mx+202,y:my+40,id:2}]); await esp(150); const rf=await estado();
      tq.pinca={nivel_antes:p0.nivel,nivel_apos:pz.nivel,salto_ao_soltar_um_dedo_px:[rd(r0.banco.x-pz.banco.x),rd(r0.banco.y-pz.banco.y)],
        mover_2px:[rd(r1.banco.x-r0.banco.x),rd(r1.banco.y-r0.banco.y)],depois_20_passos:[rd(r2.banco.x-r1.banco.x),rd(r2.banco.y-r1.banco.y)],pedido_20_passos:[80,40],
        ficha_ao_soltar:rf.ficha,nivel_final:rf.nivel}; }
    await cmd('Emulation.setTouchEmulationEnabled',{enabled:false});
  } catch (e) { T.erro = String(e).slice(0,400); }
}
for (const [W,H] of [[1280,1000],[320,640]]) {
  try {
    await abrir(W,H);
    await ev(`document.activeElement&&document.activeElement.blur&&document.activeElement.blur();document.body.focus()`);
    const base = await ev(`(function(){var z=document.querySelector('.bairro>.zona'),c=getComputedStyle(z);return {stroke:c.stroke,strokeWidth:c.strokeWidth}})()`);
    const LER = `(function(){var e=document.activeElement;if(!e||e===document.body)return null;var cs=getComputedStyle(e);var z=e.querySelector&&e.querySelector(':scope>.zona,:scope .anel');var zc=z?getComputedStyle(z):null;
      return {nome:(e.getAttribute('aria-label')||e.textContent||'').trim().slice(0,40),tag:e.tagName.toLowerCase(),fv:e.matches(':focus-visible'),outline:cs.outlineStyle+' '+cs.outlineWidth,sombra:cs.boxShadow==='none'?null:'sim',filho:zc?{sw:zc.strokeWidth,s:zc.stroke,f:zc.fill}:null}})()`;
    const paradas=[];
    for (let i=0;i<34;i++){ await tecla('Tab'); const a=await ev(LER); if(!a) break; paradas.push(a); }
    R[`tab_${W}x${H}`]={base,total:paradas.length,
      paradas:paradas.map((p,i)=>Object.assign({n:i+1},p,{muda:p.filho?(p.filho.sw!==base.strokeWidth||p.filho.s!==base.stroke):null}))};
  } catch (e) { R[`tab_${W}x${H}`]={erro:String(e).slice(0,300)}; }
}
fs.writeFileSync(SAIDA, JSON.stringify(R,null,1));
try{ws.close()}catch{}
edge.kill(); srv.close(); setTimeout(()=>process.exit(0),500);

