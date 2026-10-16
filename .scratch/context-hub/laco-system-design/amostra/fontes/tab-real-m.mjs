// Tab real (Input.dispatchKeyEvent pelo CDP) num Edge sem cabeça com perfil próprio.
// Uso: node tab-real.mjs <edge.exe> <perfil> <saida> <arquivo.html>...
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const [edge, perfil, saida, ...pecas] = process.argv.slice(2);
const porta = 9300 + Math.floor(Math.random() * 500);
const proc = spawn(edge, ['--headless=new', '--disable-gpu', '--no-first-run', `--user-data-dir=${perfil}`,
  `--remote-debugging-port=${porta}`, '--remote-debugging-address=127.0.0.1', '--window-size=1280,1000', 'about:blank'], { stdio: 'ignore' });
const espera = ms => new Promise(r => setTimeout(r, ms));

async function alvo() {
  for (let i = 0; i < 50; i++) {
    try { const l = await (await fetch(`http://127.0.0.1:${porta}/json`)).json(); const p = l.find(x => x.type === 'page'); if (p) return p.webSocketDebuggerUrl; } catch {}
    await espera(200);
  }
  throw new Error('sem CDP');
}

try {
  const ws = new WebSocket(await alvo());
  await new Promise(r => ws.addEventListener('open', r, { once: true }));
  let id = 0; const pend = new Map();
  ws.addEventListener('message', ev => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } });
  const cdp = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  await cdp('Page.enable');
  await cdp('Emulation.setDeviceMetricsOverride', { width: 1280, height: 1000, deviceScaleFactor: 1, mobile: false });
  const relato = [];
  for (const arq of pecas) {
    await cdp('Page.navigate', { url: pathToFileURL(arq).href });
    await espera(1500);
    const nome = arq.split(/[\\/]/).pop();
    for (let n = 1; n <= 20; n++) {
      for (const type of ['keyDown', 'keyUp']) await cdp('Input.dispatchKeyEvent', { type, key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9, nativeVirtualKeyCode: 9 });
      await espera(150);
      const r = await cdp('Runtime.evaluate', { returnByValue: true, expression: `(() => { const e = document.activeElement; if (!e) return null;
        const b = e.getBoundingClientRect(); const anel = e.querySelector('.anel'); const zona = e.querySelector('.zona');
        const cs = x => x ? getComputedStyle(x) : null;
        return { abre: e.getAttribute('data-abre'), item: e.getAttribute('data-item'), grupo: e.getAttribute('data-grupo'),
          fv: e.matches(':focus-visible'), anel: anel ? cs(anel).stroke + ' / ' + cs(anel).fill : null,
          zona: zona ? cs(zona).stroke + ' ' + cs(zona).strokeWidth : null, x: b.x, y: b.y, w: b.width, h: b.height }; })()` });
      const v = r.result.result.value;
      relato.push({ peca: nome, parada: n, ...v });
      if (v && v.item && false) {
        const pad = 30;
        const shot = await cdp('Page.captureScreenshot', { format: 'png', clip: { x: Math.max(0, v.x - pad), y: Math.max(0, v.y - pad), width: v.w + 2 * pad, height: v.h + 2 * pad, scale: 2 } });
        writeFileSync(`${saida}/foco-${nome.replace('.html', '')}-${n}-${v.item}.png`, Buffer.from(shot.result.data, 'base64'));
      }
    }
  }
  writeFileSync(`${saida}/tab-real.json`, JSON.stringify(relato, null, 1));
  for (const r of relato) console.log(r.peca, r.parada, r.item || r.grupo || r.abre, 'focus-visible=' + r.fv, r.anel ? 'anel=' + r.anel : 'zona=' + r.zona);
  ws.close();
} finally {
  proc.kill();
}
