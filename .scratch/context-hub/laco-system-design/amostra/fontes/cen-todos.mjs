import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
const [edge, perfil, saida, arq, larg, alt] = process.argv.slice(2);
mkdirSync(saida, { recursive: true });
const porta = 9300 + Math.floor(Math.random() * 500);
const proc = spawn(edge, ['--headless=new','--disable-gpu','--no-first-run',`--user-data-dir=${perfil}`,`--remote-debugging-port=${porta}`,'about:blank'], { stdio: 'ignore' });
const espera = ms => new Promise(r => setTimeout(r, ms));
async function alvo(){for(let i=0;i<50;i++){try{const l=await (await fetch(`http://127.0.0.1:${porta}/json`)).json();const p=l.find(x=>x.type==='page');if(p)return p.webSocketDebuggerUrl}catch{}await espera(200)}throw new Error('sem CDP')}
try{
 const ws=new WebSocket(await alvo());await new Promise(r=>ws.addEventListener('open',r,{once:true}));
 let id=0;const pend=new Map();ws.addEventListener('message',ev=>{const m=JSON.parse(ev.data);if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id)}});
 const cdp=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}))});
 const ev=async e=>(await cdp('Runtime.evaluate',{expression:e,returnByValue:true})).result.result.value;
 await cdp('Page.enable');await cdp('Emulation.setDeviceMetricsOverride',{width:+larg,height:+alt,deviceScaleFactor:1,mobile:false});
 await cdp('Page.navigate',{url:pathToFileURL(arq).href});await espera(1500);
 const cens=await ev(`Array.from(document.querySelectorAll('[data-cen]')).map(b=>b.getAttribute('data-cen'))`);
 const out=[];
 for(const c of cens){
  await ev(`document.querySelector('[data-cen="${c}"]').click()`);
  const N=await ev(`parseInt(document.getElementById('cen-num').textContent.split(' de ')[1])`);
  for(let n=1;n<=N;n++){
   if(n>1)await ev(`document.getElementById('cen-prox').click()`);await espera(120);
   const r=await ev(`(()=>{const ms=[...document.querySelectorAll('.marca-passo')];const ag=document.querySelector('.marca-passo.agora');
     const svg=document.querySelector('svg.cidade');let dist=null;
     if(ag){const c=ag.firstChild;const x=+(c.getAttribute('cx')||c.getAttribute('points').split(/[ ,]/)[0]),y=+(c.getAttribute('cy')||+c.getAttribute('points').split(/[ ,]/)[1]+15);
       const acc=[...document.querySelectorAll('.agora[data-chave]')].filter(e=>!e.classList.contains('lig-fundo'));
       dist=Math.min(...acc.map(e=>{if(e.tagName==='path'){const L=e.getTotalLength();let m=1e9;for(let i=0;i<=40;i++){const p=e.getPointAtLength(L*i/40);m=Math.min(m,Math.hypot(p.x-x,p.y-y))}return m}
         const b=e.getBBox();const dx=Math.max(b.x-x,0,x-b.x-b.width),dy=Math.max(b.y-y,0,y-b.y-b.height);return Math.hypot(dx,dy)}))}
     return {marcas:ms.length,dist:dist&&Math.round(dist)}})()`);
   out.push(`${c} ${n}/${N}: marcas=${r.marcas} distancia_ao_aceso=${r.dist}`);
   if(n===N){const shot=await cdp('Page.captureScreenshot',{format:'png'});writeFileSync(`${saida}/${c}-${n}.png`,Buffer.from(shot.result.data,'base64'))}
  }
  await ev(`document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}))`);
  const ap=await ev(`document.querySelector('[data-cen="${c}"]').getAttribute('aria-pressed')+' '+getComputedStyle(document.querySelector('[data-cen="${c}"]')).backgroundColor`);
  out.push(`${c} depois de Esc: aria-pressed=${ap}`);
 }
 const h=await ev('document.documentElement.scrollHeight');out.push('altura da pagina: '+h);
 writeFileSync(`${saida}/cenarios.txt`,out.join('\n'));console.log(out.join('\n'));ws.close();
}finally{proc.kill()}
