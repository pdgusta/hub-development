// node extra-v3.mjs <edge> <perfil> <html> <saida-dir>
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
const [edge, perfil, arq, saida] = process.argv.slice(2);
const porta = 9300 + Math.floor(Math.random() * 500);
const proc = spawn(edge, ['--headless=new', '--disable-gpu', '--no-first-run', `--user-data-dir=${perfil}`, `--remote-debugging-port=${porta}`, 'about:blank'], { stdio: 'ignore' });
const espera = ms => new Promise(r => setTimeout(r, ms));
async function alvo() { for (let i = 0; i < 50; i++) { try { const l = await (await fetch(`http://127.0.0.1:${porta}/json`)).json(); const p = l.find(x => x.type === 'page'); if (p) return p.webSocketDebuggerUrl } catch { } await espera(200) } throw new Error('sem CDP') }
const out = {};
try {
  const ws = new WebSocket(await alvo()); await new Promise(r => ws.addEventListener('open', r, { once: true }));
  let id = 0; const pend = new Map();
  ws.addEventListener('message', ev => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id) } });
  const cdp = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })) });
  const ev = async e => { const r = await cdp('Runtime.evaluate', { expression: e, returnByValue: true }); return r.result.exceptionDetails ? 'ERRO ' + JSON.stringify(r.result.exceptionDetails).slice(0, 200) : r.result.result.value };
  const abrir = async (w, h, toque) => { await cdp('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: false }); await cdp('Emulation.setTouchEmulationEnabled', { enabled: !!toque, maxTouchPoints: toque ? 5 : 0 }); await cdp('Page.navigate', { url: pathToFileURL(arq).href }); await espera(1500) };
  const shot = async nome => { const s = await cdp('Page.captureScreenshot', { format: 'png' }); writeFileSync(`${saida}/${nome}.png`, Buffer.from(s.result.data, 'base64')) };
  const banco = async () => JSON.parse(await ev('(function(){var b=document.querySelector("[data-item=\\"Banco local\\"]").getBoundingClientRect();return JSON.stringify([Math.round(b.left+b.width/2),Math.round(b.top+b.height/2)])})()'));
  const tq = (type, pts) => cdp('Input.dispatchTouchEvent', { type, touchPoints: pts.map(p => ({ x: p[0], y: p[1], id: p[2] })) });
  await cdp('Page.enable');
  // A. arrasto de um dedo longo (30 passos) em cima do Banco local; termina num bairro; depois toque simples abre a ficha
  await abrir(1280, 1000, true);
  { const p = await banco(), a = p.slice(); await tq('touchStart', [[p[0], p[1], 0]]); for (let i = 1; i <= 30; i++) { await tq('touchMove', [[p[0] - i * 5, p[1] - i * 3, 0]]); await espera(10) } await tq('touchEnd', []); await espera(300);
    const b = await banco(); out.A_arrasto_longo = `pedido -150,-90 obtido ${b[0] - a[0]},${b[1] - a[1]} ficha=${await ev('document.getElementById("ficha").classList.contains("aberta")')}`;
    await tq('touchStart', [[b[0], b[1], 0]]); await espera(40); await tq('touchEnd', []); await espera(300);
    out.A_toque_depois = await ev('document.getElementById("ficha").classList.contains("aberta")+" "+((document.querySelector("#ficha li.alvo b")||{}).textContent||"-")'); await ev('document.getElementById("fechar").click()') }
  // B. pinça -> um dedo -> o dedo que ficou arrasta 20 passos
  await abrir(1280, 1000, true);
  await ev(`window.__ev=[];['pointerdown','pointerup','pointercancel','lostpointercapture','gotpointercapture'].forEach(function(n){document.addEventListener(n,function(e){__ev.push(n+':'+e.pointerId+':'+(e.target.id||e.target.tagName))},true)});var __n=0;document.addEventListener('pointermove',function(e){__n++;if(__n%5==0)__ev.push('move:'+e.pointerId)},true)`);
  { await tq('touchStart', [[400, 600, 0]]); await tq('touchStart', [[400, 600, 0], [800, 600, 1]]); for (let i = 1; i <= 5; i++) await tq('touchMove', [[400 - i * 6, 600, 0], [800 + i * 6, 600, 1]]);
    await tq('touchEnd', [[830, 600, 1]]); await espera(50); const a = await banco();
    for (let i = 1; i <= 20; i++) { await tq('touchMove', [[370 + i * 4, 600 + i * 2, 0]]); await espera(10) } await tq('touchEnd', []); await espera(200);
    const b = await banco(); out.B_pinca_um_dedo = `pedido 80,40 obtido ${b[0] - a[0]},${b[1] - a[1]}`; out.B_ev = await ev('__ev.join(" ")') }
  // C. cancelamento: touchCancel no meio do arrasto encerra; o toque seguinte abre ficha
  await abrir(1280, 1000, true);
  { const p = await banco(); await tq('touchStart', [[p[0], p[1], 0]]); for (let i = 1; i <= 5; i++) await tq('touchMove', [[p[0] + i * 8, p[1], 0]]);
    await cdp('Input.dispatchTouchEvent', { type: 'touchCancel', touchPoints: [] }); await espera(200);
    out.C_cancel = await ev('JSON.stringify({arrastando:document.getElementById("tela").classList.contains("arrastando"),ficha:document.getElementById("ficha").classList.contains("aberta")})');
    const b = await banco(); await tq('touchStart', [[b[0], b[1], 0]]); await espera(40); await tq('touchEnd', []); await espera(300);
    out.C_toque_depois = await ev('document.getElementById("ficha").classList.contains("aberta")') }
  // D. cabeçalhos
  for (const [w, h] of [[1280, 720], [1280, 1000], [960, 800], [1100, 700], [320, 640]]) { await abrir(w, h, false);
    out[`D_topo_${w}x${h}`] = await ev('Math.round(document.querySelector(".topo").getBoundingClientRect().height)+"px zoom "+document.getElementById("z-nivel").textContent+" classes="+document.querySelector(".cen-botoes").className');
    await shot(`v3-${w}x${h}`) }
  // E. fileira a 960: rola até o fim e o esmaecido troca de lado
  await abrir(960, 800, false);
  out.E_fim = await ev('(function(){var r=document.querySelector(".cen-botoes");r.scrollLeft=1e5;r.dispatchEvent(new Event("scroll"));return r.className})()');
  // F. ficha aberta a 1280 e a janela vai a 320: vira modal, foco dentro; volta a 1280: deixa de ser modal
  await abrir(1280, 1000, false);
  await ev('document.querySelector("[data-abre=nucleo]").focus();document.querySelector("[data-abre=nucleo]").dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}))');
  const fic = () => ev('JSON.stringify({modal:document.getElementById("ficha").getAttribute("aria-modal"),inert:document.getElementById("tela").hasAttribute("inert"),foco:document.activeElement.id||document.activeElement.tagName})');
  out.F_1280 = await fic();
  await cdp('Emulation.setDeviceMetricsOverride', { width: 320, height: 640, deviceScaleFactor: 1, mobile: false }); await espera(400); out.F_320 = await fic();
  await cdp('Emulation.setDeviceMetricsOverride', { width: 1280, height: 1000, deviceScaleFactor: 1, mobile: false }); await espera(400); out.F_volta_1280 = await fic();
  await ev('document.getElementById("fechar").click()'); out.F_fechou = await ev('document.activeElement.getAttribute("data-abre")');
  ws.close();
} finally { proc.kill() }
console.log(JSON.stringify(out, null, 1));
