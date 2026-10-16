// node shot.mjs <edge> <perfil> <arquivo.html> <saida.png> <larg> <alt> [js]
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
const [edge, perfil, arq, saida, larg, alt, js] = process.argv.slice(2);
const porta = 9300 + Math.floor(Math.random() * 500);
const proc = spawn(edge, ['--headless=new','--disable-gpu','--no-first-run',`--user-data-dir=${perfil}`,`--remote-debugging-port=${porta}`,'about:blank'], { stdio: 'ignore' });
const espera = ms => new Promise(r => setTimeout(r, ms));
async function alvo(){for(let i=0;i<50;i++){try{const l=await (await fetch(`http://127.0.0.1:${porta}/json`)).json();const p=l.find(x=>x.type==='page');if(p)return p.webSocketDebuggerUrl}catch{}await espera(200)}throw new Error('sem CDP')}
try{
 const ws=new WebSocket(await alvo());await new Promise(r=>ws.addEventListener('open',r,{once:true}));
 let id=0;const pend=new Map();ws.addEventListener('message',ev=>{const m=JSON.parse(ev.data);if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id)}});
 const cdp=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}))});
 await cdp('Page.enable');await cdp('Emulation.setDeviceMetricsOverride',{width:+larg,height:+alt,deviceScaleFactor:1,mobile:+larg<700});
 await cdp('Page.navigate',{url:pathToFileURL(arq).href});await espera(1500);
 if(js){const r=await cdp('Runtime.evaluate',{expression:js,returnByValue:true});if(r.result.exceptionDetails)console.log(JSON.stringify(r.result.exceptionDetails).slice(0,300));else if(r.result.result.value!==undefined)console.log(r.result.result.value)}
 await espera(500);
 const shot=await cdp('Page.captureScreenshot',{format:'png'});writeFileSync(saida,Buffer.from(shot.result.data,'base64'));ws.close();
}finally{proc.kill()}
