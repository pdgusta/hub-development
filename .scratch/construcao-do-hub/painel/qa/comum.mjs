// Utilidades do QA do painel: sobe servidor.py numa porta própria, abre o Edge sem cabeça com perfil próprio
// e fala com ele pelo protocolo de depuração. Nada de mouse nem teclado da tela do Gustavo.
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

export const QA = path.dirname(fileURLToPath(import.meta.url));
export const PAINEL = path.resolve(QA, '..');
export const esp = (ms) => new Promise(r => setTimeout(r, ms));
const EDGE = ['C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe'].find(p => fs.existsSync(p));

export function gerar(pasta, args = []) {
  const r = spawnSync('node', [path.join(PAINEL, 'fixture', 'gerar.mjs'), '--saida', pasta, ...args], { encoding: 'utf8' });
  if (r.status !== 0) throw new Error('gerar falhou: ' + r.stderr);
  return r.stdout;
}
export function servidor(pasta, porta, extra = []) {
  const p = spawn('python', ['-I', path.join(PAINEL, 'servidor.py'), '--pasta', pasta, '--porta', String(porta), ...extra], { stdio: ['ignore', 'pipe', 'pipe'] });
  p.log = ''; p.stdout.on('data', d => p.log += d); p.stderr.on('data', d => p.log += d);
  return p;
}
export async function pronto(url, n = 40) { for (let i = 0; i < n; i++) { try { const r = await fetch(url); return r.status } catch { await esp(250) } } throw new Error('servidor não subiu: ' + url) }

export async function navegador() {
  const DBG = 9600 + Math.floor(Math.random() * 300);
  const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'qa-painel-'));
  const edge = spawn(EDGE, ['--headless=new', '--disable-gpu', '--no-first-run', `--user-data-dir=${perfil}`, `--remote-debugging-port=${DBG}`, 'about:blank'], { stdio: 'ignore' });
  let alvos;
  for (let i = 0; i < 60; i++) { try { alvos = await (await fetch(`http://127.0.0.1:${DBG}/json`)).json(); break } catch { await esp(250) } }
  const pag = alvos.find(a => a.type === 'page');
  const ws = new WebSocket(pag.webSocketDebuggerUrl);
  await new Promise(ok => ws.addEventListener('open', ok));
  let id = 0; const pend = new Map(); const erros = [];
  ws.addEventListener('message', m => {
    const d = JSON.parse(m.data);
    if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id) }
    else if (d.method === 'Runtime.exceptionThrown') erros.push(d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text);
    else if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') erros.push('console.error: ' + d.params.args.map(a => a.value ?? a.description).join(' '));
  });
  const cmd = (method, params = {}) => new Promise(ok => { const i = ++id; pend.set(i, ok); ws.send(JSON.stringify({ id: i, method, params })) });
  const ev = async (expr) => { const r = await cmd('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }); if (r.result.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails).slice(0, 300)); return r.result.result.value };
  await cmd('Page.enable'); await cmd('Runtime.enable');
  const nav = {
    cmd, ev, erros, perfil,
    async abrir(url, w, h) {
      await cmd('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: false });
      await cmd('Page.navigate', { url });
      for (let i = 0; i < 60; i++) { await esp(250); try { if (await ev(`document.readyState==='complete'&&document.querySelectorAll('.agente').length>0`)) break } catch { } }
      await esp(600);
    },
    async foto(arq) { const r = await cmd('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(QA, 'capturas', arq), Buffer.from(r.result.data, 'base64')) },
    async tecla(key, extra = {}) {
      const cod = { Tab: 9, Escape: 27, Enter: 13, ' ': 32 }[key];
      await cmd('Input.dispatchKeyEvent', { type: 'keyDown', key, windowsVirtualKeyCode: cod, text: key.length === 1 ? key : undefined, ...extra });
      await cmd('Input.dispatchKeyEvent', { type: 'keyUp', key, windowsVirtualKeyCode: cod, ...extra }); await esp(80);
    },
    async clicar(x, y) {
      await cmd('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await cmd('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', buttons: 1, clickCount: 1 });
      await cmd('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', buttons: 0, clickCount: 1 }); await esp(120);
    },
    fechar() {
      try { ws.close() } catch { }
      // mata só o msedge deste perfil (por linha de comando), nunca por nome
      spawnSync('powershell', ['-NoProfile', '-Command', `Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*${path.basename(perfil)}*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }`]);
    },
  };
  return nav;
}

// leitura do estado da tela (cartões, placar, alertas, estações)
export const LER_TELA = `(function(){
  var $=function(i){return document.getElementById(i)};
  var cart=[].map.call(document.querySelectorAll('.agente'),function(c){
    var r=c.getBoundingClientRect(),cls=c.className.split(/\\s+/);
    var sit=['trabalhando','ocioso','falhou','sem_sinal','encerrado','nao_comecou'].filter(function(s){return cls.indexOf(s)>=0})[0]||null;
    var pips=c.querySelectorAll('.subs i');
    return {nome:c.querySelector('.nome>span').textContent,sit:sit,estourou:cls.indexOf('estourou')>=0,fable:cls.indexOf('com-fable')>=0,
      abertos:[].filter.call(pips,function(p){return p.className}).length,pips:pips.length,
      oque:c.querySelector('.oque').textContent,sinal:c.querySelector('.sinal').textContent,
      x:r.left,y:r.top,w:r.width,h:r.height,corta:[c.scrollWidth>c.clientWidth+1,c.scrollHeight>c.clientHeight+1],selo:!!c.querySelector('.selo')};
  });
  var est=[].map.call(document.querySelectorAll('.estacao'),function(e){return {col:e.getAttribute('data-col'),n:+e.querySelector('.est-cab .n').textContent,marcas:[].map.call(e.querySelectorAll('.tk'),function(t){return {n:t.querySelector('.n').textContent,cls:t.className}})}});
  var al=[].map.call(document.querySelectorAll('#alertas-lista li'),function(l){return {cls:l.firstChild.className,txt:l.textContent.trim()}});
  return {trab:$('p-trab-n').textContent,trabDe:$('p-trab-de').textContent,nota:$('p-trab-nota').textContent,feitos:$('p-feitos-n').textContent,total:$('p-feitos-de').textContent,
    desde:$('p-desde-h').textContent,desdeHa:$('p-desde-ha').textContent,leitura:$('leitura-txt').textContent,leituraCls:$('leitura').className,
    problemas:$('b-problemas').hidden?null:$('b-problemas').textContent,ilegivel:$('ilegivel').hidden?null:$('ilegivel').textContent,
    cartoes:cart,estacoes:est,alertas:al,
    largura:{scrollW:document.documentElement.scrollWidth,innerW:innerWidth,scrollH:document.documentElement.scrollHeight,innerH:innerHeight},
    gaveta:{aberta:!$('gaveta').hidden,titulo:$('g-titulo').textContent},faixa:$('faixa-txt').textContent,
    ativo:document.activeElement?(document.activeElement.id||document.activeElement.className||document.activeElement.tagName):null};
})()`;
