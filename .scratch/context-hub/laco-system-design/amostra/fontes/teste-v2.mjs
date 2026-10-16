// node teste-v2.mjs <edge> <perfil> <html> <larg> <alt> <saida-dir>
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
const [edge, perfil, arq, larg, alt, saida] = process.argv.slice(2);
const W = +larg, H = +alt;
const porta = 9300 + Math.floor(Math.random() * 500);
const proc = spawn(edge, ['--headless=new', '--disable-gpu', '--no-first-run', `--user-data-dir=${perfil}`, `--remote-debugging-port=${porta}`, 'about:blank'], { stdio: 'ignore' });
const espera = ms => new Promise(r => setTimeout(r, ms));
async function alvo() { for (let i = 0; i < 50; i++) { try { const l = await (await fetch(`http://127.0.0.1:${porta}/json`)).json(); const p = l.find(x => x.type === 'page'); if (p) return p.webSocketDebuggerUrl } catch { } await espera(200) } throw new Error('sem CDP') }
const out = {};
try {
  const ws = new WebSocket(await alvo()); await new Promise(r => ws.addEventListener('open', r, { once: true }));
  let id = 0; const pend = new Map(); const logs = [];
  ws.addEventListener('message', ev => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id) } else if (m.method === 'Runtime.consoleAPICalled') logs.push(m.params.type + ': ' + m.params.args.map(a => a.value).join(' ')); else if (m.method === 'Runtime.exceptionThrown') logs.push('EXC ' + JSON.stringify(m.params.exceptionDetails).slice(0, 300)) });
  const cdp = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })) });
  const ev = async e => { const r = await cdp('Runtime.evaluate', { expression: e, returnByValue: true }); return r.result.exceptionDetails ? 'ERRO ' + JSON.stringify(r.result.exceptionDetails).slice(0, 200) : r.result.result.value };
  const shot = async nome => { const s = await cdp('Page.captureScreenshot', { format: 'png' }); writeFileSync(`${saida}/${nome}-${W}x${H}.png`, Buffer.from(s.result.data, 'base64')) };
  await cdp('Page.enable'); await cdp('Runtime.enable');
  await cdp('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: W < 700 });
  await cdp('Page.navigate', { url: pathToFileURL(arq).href }); await espera(1500);
  const vb = () => ev('document.querySelector("svg.cidade").getAttribute("viewBox")+" | "+document.getElementById("z-nivel").textContent');
  const banco = () => ev('(function(){var b=document.querySelector("[data-item=\\"Banco local\\"]").getBoundingClientRect();return Math.round(b.left)+","+Math.round(b.top)})()');
  const estado = () => ev('JSON.stringify({vb:document.querySelector("svg.cidade").getAttribute("viewBox"),z:document.getElementById("z-nivel").textContent,scroll:document.getElementById("tela").scrollTop,foco:(document.activeElement.getAttribute("aria-label")||document.activeElement.tagName).slice(0,30),ficha:document.getElementById("ficha").classList.contains("aberta"),sel:String(getSelection()).length})');
  out.inicio = await estado();
  out.topo = await ev('Math.round(document.querySelector(".topo").getBoundingClientRect().height)');
  out.rot = await ev('(function(){var m=1e9;document.querySelectorAll("svg.cidade text").forEach(function(t){var r=t.getBoundingClientRect();if(r.height&&r.height<m)m=r.height});return Math.round(m*10)/10})()');
  // a cidade inteira cabe e fica fora do canto do zoom?
  const caixas = 'JSON.stringify((function(){var t=document.getElementById("tela").getBoundingClientRect(),z=document.querySelector(".zoom").getBoundingClientRect(),g=document.querySelector("[data-item=Gustavo]").getBoundingClientRect(),m=document.querySelector("[data-item=Maestro]").getBoundingClientRect(),mu=document.querySelector(".muralha").getBoundingClientRect(),o=document.querySelector("[data-item=\\"Outro par\\"]").getBoundingClientRect();function sob(a,b){return !(a.right<b.left||a.left>b.right||a.bottom<b.top||a.top>b.bottom)}return {gustavoSobZoom:sob(g,z),muralhaSobZoom:sob(mu,z),dentro:[Math.round(m.left-t.left),Math.round(mu.top-t.top),Math.round(t.right-o.right),Math.round(t.bottom-mu.bottom)]}})())';
  out.caixas_inicio = await ev(caixas);
  out.sobra = await ev('Array.prototype.map.call(document.querySelectorAll("[data-sobra]"),function(e){return e.getAttribute("data-sobra-nomes")}).join(";")||"nenhuma"');
  out.etiquetas = await ev('document.querySelectorAll(".etq").length');
  await shot('inicio');
  const m = (type, x, y, o = {}) => cdp('Input.dispatchMouseEvent', { type, x, y, ...o });
  const cx = Math.round(W * .55), cy = Math.round(H * .6);
  // três arrastos seguidos com o botão direito; antes de cada aperto, onde está o banco; depois do aperto parado, de novo
  out.arrastos = [];
  for (let k = 0; k < 3; k++) {
    const antes = await banco();
    await m('mousePressed', cx, cy, { button: 'right', buttons: 2, clickCount: 1 }); await espera(150);
    const apertado = await banco();
    for (let i = 1; i <= 10; i++) await m('mouseMoved', cx - i * 10, cy - i * 6, { button: 'right', buttons: 2 });
    await m('mouseReleased', cx - 100, cy - 60, { button: 'right', buttons: 0, clickCount: 1 }); await espera(150);
    out.arrastos.push(`antes ${antes} | apertado ${apertado} | depois ${await banco()}`);
  }
  // botão do meio
  { const antes = await banco(); await m('mousePressed', cx, cy, { button: 'middle', buttons: 4, clickCount: 1 }); await espera(150); const ap = await banco();
    for (let i = 1; i <= 5; i++) await m('mouseMoved', cx + i * 10, cy, { button: 'middle', buttons: 4 }); await m('mouseReleased', cx + 50, cy, { button: 'middle', buttons: 0, clickCount: 1 }); await espera(100);
    out.meio = `antes ${antes} | apertado ${ap} | depois ${await banco()}`; out.meio_estado = await estado() }
  // arrasto esquerdo não seleciona texto
  await m('mousePressed', cx - 200, cy - 200, { button: 'left', buttons: 1, clickCount: 1 });
  for (let i = 1; i <= 10; i++) await m('mouseMoved', cx - 200 + i * 30, cy - 200 + i * 20, { button: 'left', buttons: 1 });
  await m('mouseReleased', cx + 100, cy, { button: 'left', buttons: 0, clickCount: 1 }); await espera(100);
  out.esquerdo = await estado();
  await ev('document.getElementById("fechar").click()');
  // + três vezes com o foco no desenho: o centro da tela fica no mesmo ponto do desenho
  await ev('document.getElementById("z-tudo").click()'); await ev('document.getElementById("tela").focus()');
  const centro = 'JSON.stringify((function(){var v=document.querySelector("svg.cidade").getAttribute("viewBox").split(" ").map(Number);return [Math.round(v[0]+v[2]/2),Math.round(v[1]+v[3]/2)]})())';
  out.centro_antes = await ev(centro);
  for (let i = 0; i < 3; i++) { await cdp('Input.dispatchKeyEvent', { type: 'keyDown', key: '+', code: 'Equal', text: '+', modifiers: 8 }); await cdp('Input.dispatchKeyEvent', { type: 'keyUp', key: '+', code: 'Equal', modifiers: 8 }) }
  await espera(100); out.centro_mais3 = await ev(centro) + ' ' + await vb(); await shot('mais3');
  for (let i = 0; i < 3; i++) await ev('document.getElementById("z-menos").click()');
  out.centro_menos3 = await ev(centro);
  // tecla 0: cidade inteira
  await cdp('Input.dispatchKeyEvent', { type: 'keyDown', key: '0', code: 'Digit0', text: '0' }); await cdp('Input.dispatchKeyEvent', { type: 'keyUp', key: '0', code: 'Digit0' }); await espera(100);
  out.tecla0 = await vb(); out.caixas_tecla0 = await ev(caixas); await shot('tecla0');
  // toque: um toque no + aproxima; um toque num bairro abre a ficha
  await cdp('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  const tq = async (type, pts) => cdp('Input.dispatchTouchEvent', { type, touchPoints: pts.map((p, i) => ({ x: p[0], y: p[1], id: p[2] ?? i })) });
  const centroDe = async sel => JSON.parse(await ev(`(function(){var b=document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect();return JSON.stringify([Math.round(b.left+b.width/2),Math.round(b.top+b.height/2)])})()`));
  { const z0 = await vb(); const p = await centroDe('#z-mais'); await tq('touchStart', [p]); await espera(50); await tq('touchEnd', []); await espera(300); out.toque_mais = `${z0} -> ${await vb()}` }
  await ev('document.getElementById("z-tudo").click()'); await espera(100);
  { const p = await centroDe('[data-item="Banco local"]'); await tq('touchStart', [p]); await espera(50); await tq('touchEnd', []); await espera(400);
    out.toque_ficha = await ev('document.getElementById("ficha").classList.contains("aberta")+" "+((document.querySelector("#ficha li.alvo b")||{}).textContent||"-")');
    await ev('document.getElementById("fechar").click()') }
  // arrasto com um dedo não abre ficha
  { const p = await centroDe('[data-item="Banco local"]'); const a = await banco(); await tq('touchStart', [p]); for (let i = 1; i <= 8; i++) await tq('touchMove', [[p[0] + i * 8, p[1] + i * 5]]); await tq('touchEnd', []); await espera(400);
    out.toque_arrasto = `banco ${a} -> ${await banco()} ficha ${await ev('document.getElementById("ficha").classList.contains("aberta")')}` }
  // pinça e depois um dedo: sem salto
  { const a = [Math.round(W * .3), Math.round(H * .6), 0], b = [Math.round(W * .7), Math.round(H * .6), 1];
    await tq('touchStart', [a]); await tq('touchStart', [a, b]);
    for (let i = 1; i <= 5; i++) await tq('touchMove', [[a[0] - i * 6, a[1], 0], [b[0] + i * 6, b[1], 1]]);
    const pin = await vb(); const bp = await banco();
    await tq('touchEnd', [[b[0] + 30, b[1], 1]]); await espera(50);  // tira o dedo 1, fica o 0 (no protocolo, touchEnd lista o dedo que sai)
    await tq('touchMove', [[a[0] - 28, a[1] + 2, 0]]); await espera(50);
    out.pinca = `depois da pinça ${pin} banco ${bp} | um dedo andou 2px: banco ${await banco()}`;
    await tq('touchEnd', []) }
  out.logs = logs;
  ws.close();
} finally { proc.kill() }
console.log(JSON.stringify(out, null, 1));
