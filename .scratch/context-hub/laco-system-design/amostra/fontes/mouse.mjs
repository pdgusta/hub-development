import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';
const [edge, perfil, arq] = process.argv.slice(2);
const porta = 9300 + Math.floor(Math.random() * 500);
const proc = spawn(edge, ['--headless=new','--disable-gpu','--no-first-run',`--user-data-dir=${perfil}`,`--remote-debugging-port=${porta}`,'about:blank'], { stdio: 'ignore' });
const espera = ms => new Promise(r => setTimeout(r, ms));
async function alvo(){for(let i=0;i<50;i++){try{const l=await (await fetch(`http://127.0.0.1:${porta}/json`)).json();const p=l.find(x=>x.type==='page');if(p)return p.webSocketDebuggerUrl}catch{}await espera(200)}throw new Error('sem CDP')}
try{
 const ws=new WebSocket(await alvo());await new Promise(r=>ws.addEventListener('open',r,{once:true}));
 let id=0;const pend=new Map();ws.addEventListener('message',ev=>{const m=JSON.parse(ev.data);if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id)}});
 const cdp=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}))});
 const ev=async e=>(await cdp('Runtime.evaluate',{expression:e,returnByValue:true})).result.result.value;
 await cdp('Page.enable');await cdp('Emulation.setDeviceMetricsOverride',{width:1280,height:1000,deviceScaleFactor:1,mobile:false});
 await cdp('Page.navigate',{url:pathToFileURL(arq).href});await espera(1500);
 const vb=()=>ev('document.querySelector("svg.cidade").getAttribute("viewBox")+" | "+document.getElementById("z-nivel").textContent');
 console.log('inicio      ', await vb());
 const m=(type,x,y,o={})=>cdp('Input.dispatchMouseEvent',{type,x,y,...o});
 await m('mousePressed',600,500,{button:'right',buttons:2,clickCount:1});
 for(let i=1;i<=10;i++)await m('mouseMoved',600-i*20,500-i*10,{button:'right',buttons:2});
 await m('mouseReleased',400,400,{button:'right',buttons:0,clickCount:1});await espera(100);
 console.log('arrasto dir.', await vb());
 await m('mouseWheel',600,500,{deltaX:0,deltaY:-300,modifiers:2});await espera(100);
 console.log('ctrl+roda   ', await vb(), await ev('document.querySelector("svg.cidade").classList.contains("perto")'));
 await m('mouseWheel',600,500,{deltaX:0,deltaY:200,modifiers:8});await espera(100);
 console.log('shift+roda  ', await vb());
 // clique esquerdo num bairro ainda abre a ficha depois disso
 await cdp('Runtime.evaluate',{expression:'document.getElementById("z-tudo").click()'});await espera(100);
 const r=await ev('(function(){var b=document.querySelector("[data-item=\\"Banco local\\"]").getBoundingClientRect();return [b.left+b.width/2,b.top+b.height/2]})()');
 await m('mousePressed',r[0],r[1],{button:'left',buttons:1,clickCount:1});await m('mouseReleased',r[0],r[1],{button:'left',buttons:0,clickCount:1});await espera(200);
 console.log('clique      ', await ev('document.getElementById("ficha").classList.contains("aberta")+" "+(document.querySelector("#ficha li.alvo b")||{}).textContent'));
 ws.close();
}finally{proc.kill()}
