var tela=document.getElementById('tela'),svgC=document.querySelector('svg.cidade'),CONT={x:0,y:24,w:1200,h:852},vb=null,MAX=5;
// modo: 'abertura' ou 'tudo' enquanto ninguém mexeu (o redimensionamento refaz o mesmo enquadramento); null depois
var modo='abertura';
function px(){return tela.clientWidth/vb.w}
function aplicar(){svgC.setAttribute('viewBox',vb.x.toFixed(2)+' '+vb.y.toFixed(2)+' '+vb.w.toFixed(2)+' '+vb.h.toFixed(2));
 svgC.classList.toggle('perto',px()>=1.4);var z=document.getElementById('z-nivel');if(z)z.textContent=Math.round(px()*100)+'%'}
// canto dos botões de zoom: o enquadramento desconta a faixa de baixo ou a coluna da esquerda (fica a que dá mais zoom)
function cantoZoom(){var z=document.querySelector('.zoom');if(!z)return {w:0,h:0};return {w:z.offsetLeft+z.offsetWidth+8,h:tela.clientHeight-z.offsetTop+8}}
// caixas do que se vê na planta (itens, bairros, muralha, pessoas): o canto do zoom só conta se cobrir alguma
var CAIXAS=[];svgC.querySelectorAll('.item,.bairro>.zona,.muralha').forEach(function(e){var b=e.getBBox();if(b.width||b.height)CAIXAS.push(b)});
function cobre(r,c){var W=tela.clientWidth,H=tela.clientHeight,e=r.e,x0=CONT.x+CONT.w/2-(r.l+r.w/2)/e,y0=CONT.y+CONT.h/2-(r.t+r.h/2)/e;
 var zx2=x0+c.w/e,zy1=y0+(H-c.h)/e;return CAIXAS.some(function(b){return b.x<zx2&&b.y+b.height>zy1})}
function enquadrar(){var W=tela.clientWidth,H=tela.clientHeight,m=10,c=cantoZoom();
 var t={e:Math.min((W-2*m)/CONT.w,(H-2*m)/CONT.h),l:0,t:0,w:W,h:H};if(!cobre(t,c))return t;
 var a={e:Math.min((W-2*m)/CONT.w,(H-c.h-2*m)/CONT.h),l:0,t:0,w:W,h:H-c.h},b={e:Math.min((W-c.w-2*m)/CONT.w,(H-2*m)/CONT.h),l:c.w,t:0,w:W-c.w,h:H};
 return a.e>=b.e?a:b}
// o menor zoom manual: 35%, ou menos se a cidade inteira só cabe abaixo disso (tela estreita)
function minimo(){return Math.min(.35,enquadrar().e)}
// "Ver tudo" e a tecla 0: a cidade inteira, fora do canto dos botões, em qualquer largura
function tudo(){var W=tela.clientWidth,H=tela.clientHeight,r=enquadrar(),e=r.e;
 vb={w:W/e,h:H/e};vb.x=CONT.x+CONT.w/2-(r.l+r.w/2)/e;vb.y=CONT.y+CONT.h/2-(r.t+r.h/2)/e;aplicar()}
// abertura: tudo à vista só se o menor nome ficar com 13 px ou mais; se não, 75% centrado no Banco local
var ROT=0;svgC.querySelectorAll('text').forEach(function(t){var h=t.getBBox().height;if(h&&(!ROT||h<ROT))ROT=h});
function abertura(){var r=enquadrar();if(r.e*ROT>=13){tudo();return}
 var W=tela.clientWidth,H=tela.clientHeight,e=.75,bl=document.querySelector('[data-item="Banco local"]').getBBox();
 vb={w:W/e,h:H/e};vb.x=bl.x+bl.width/2-vb.w/2;vb.y=bl.y+bl.height/2-vb.h/2;aplicar()}
function ajustarTela(){if(!vb)return;var cx=vb.x+vb.w/2,cy=vb.y+vb.h/2,e=px();var W=tela.clientWidth,H=tela.clientHeight;if(!W||!H)return;vb.w=W/e;vb.h=H/e;vb.x=cx-vb.w/2;vb.y=cy-vb.h/2;aplicar()}
function prender(){var lim=Math.min(vb.w,vb.h)*.5;
 vb.x=Math.min(Math.max(vb.x,CONT.x-vb.w+lim),CONT.x+CONT.w-lim);vb.y=Math.min(Math.max(vb.y,CONT.y-vb.h+lim),CONT.y+CONT.h-lim)}
// zoom em volta de um ponto da tela (sx, sy); sem ponto, em volta do centro da área do desenho
function zoom(f,sx,sy){modo=null;var e=px(),n=Math.min(MAX,Math.max(minimo(),e*f));f=n/e;if(Math.abs(f-1)<1e-4)return;
 if(sx==null){sx=tela.clientWidth/2;sy=tela.clientHeight/2}
 var ux=vb.x+sx/e,uy=vb.y+sy/e;vb.w/=f;vb.h/=f;vb.x=ux-sx/n;vb.y=uy-sy/n;prender();aplicar()}
function andar(dx,dy){modo=null;var e=px();vb.x+=dx/e;vb.y+=dy/e;prender();aplicar()}
function mostrar(x,y){var mx=vb.w*.08,my=vb.h*.08;if(x<vb.x+mx||x>vb.x+vb.w-mx||y<vb.y+my||y>vb.y+vb.h-my){vb.x=x-vb.w/2;vb.y=y-vb.h/2;prender();aplicar()}}
tela.addEventListener('wheel',function(ev){ev.preventDefault();var r=tela.getBoundingClientRect(),k=ev.deltaMode===1?16:ev.deltaMode===2?tela.clientHeight:1,d=ev.deltaY*k,dx=ev.deltaX*k;
 if(ev.ctrlKey||ev.metaKey){zoom(Math.exp(-d*.0018),ev.clientX-r.left,ev.clientY-r.top)}
 else if(ev.shiftKey){andar(dx||d,0)}else{andar(dx,d)}},{passive:false});
tela.addEventListener('contextmenu',function(ev){ev.preventDefault()});
// a área nunca rola: o foco num bairro não pode deslocar o desenho por baixo da vista
tela.addEventListener('scroll',function(){if(tela.scrollTop||tela.scrollLeft){tela.scrollTop=0;tela.scrollLeft=0}});
// arrasto: botão direito ou do meio (captura já no aperto); toque: um dedo anda, dois aproximam.
// O toque só é capturado depois de virar arrasto (6 px): o toque simples chega à ficha ou ao botão.
var toques={},arr=null,suprimir=false;
function ref(id){var t=toques[id];return {x:t.x,y:t.y,mov:true,id:+id}}
tela.addEventListener('mousedown',function(ev){if(ev.button===1||ev.button===2)ev.preventDefault()});
tela.addEventListener('pointerdown',function(ev){suprimir=false;
 if(ev.target.closest&&ev.target.closest('.zoom'))return;
 if(ev.pointerType==='touch'){toques[ev.pointerId]={x:ev.clientX,y:ev.clientY};var ids=Object.keys(toques);
  if(ids.length===1)arr={x:ev.clientX,y:ev.clientY,mov:false,id:ev.pointerId};
  else{arr=ref(ids[0]);try{tela.setPointerCapture(ev.pointerId)}catch(e){}}
  return}
 if(ev.button!==2&&ev.button!==1)return;
 ev.preventDefault();arr={x:ev.clientX,y:ev.clientY,mov:false,id:ev.pointerId};tela.setPointerCapture(ev.pointerId)});
tela.addEventListener('pointermove',function(ev){if(!arr)return;
 if(ev.pointerType==='touch'){if(!toques[ev.pointerId])return;var ids=Object.keys(toques);
  if(ids.length>=2){var a=toques[ids[0]],b=toques[ids[1]],d0=Math.hypot(a.x-b.x,a.y-b.y);toques[ev.pointerId]={x:ev.clientX,y:ev.clientY};
   a=toques[ids[0]];b=toques[ids[1]];var d1=Math.hypot(a.x-b.x,a.y-b.y),r=tela.getBoundingClientRect();
   if(d0>0)zoom(d1/d0,(a.x+b.x)/2-r.left,(a.y+b.y)/2-r.top);return}
  toques[ev.pointerId]={x:ev.clientX,y:ev.clientY}}
 if(ev.pointerId!==arr.id)return;
 var dx=ev.clientX-arr.x,dy=ev.clientY-arr.y;
 if(!arr.mov){if(Math.hypot(dx,dy)<6)return;arr.mov=true;tela.classList.add('arrastando');
  if(ev.pointerType==='touch'){try{tela.setPointerCapture(ev.pointerId)}catch(e){}}}
 andar(-dx,-dy);arr.x=ev.clientX;arr.y=ev.clientY});
// fim do gesto (soltar, cancelar ou perder a captura): a mesma limpeza; de dois dedos para um, a referência vem do dedo que ficou
function solta(ev){
 if(ev.pointerType==='touch'){if(!toques[ev.pointerId])return;delete toques[ev.pointerId];var ids=Object.keys(toques);
  if(ids.length){arr=ref(ids[0]);return}}
 else if(!arr||ev.pointerId!==arr.id)return;
 if(arr&&arr.mov)suprimir=true;arr=null;tela.classList.remove('arrastando')}
['pointerup','pointercancel','lostpointercapture'].forEach(function(n){tela.addEventListener(n,solta)});
// o clique que nasce de um arrasto não abre ficha (vale até o próximo aperto)
tela.addEventListener('click',function(ev){if(suprimir){suprimir=false;ev.stopPropagation();ev.preventDefault()}},true);
tela.addEventListener('keydown',function(ev){if(ev.target!==tela)return;var k=ev.key,p=60;
 if(k==='ArrowLeft')andar(-p,0);else if(k==='ArrowRight')andar(p,0);else if(k==='ArrowUp')andar(0,-p);else if(k==='ArrowDown')andar(0,p);
 else if(k==='+'||k==='=')zoom(1.25);else if(k==='-'||k==='_')zoom(1/1.25);else if(k==='0'){modo='tudo';tudo()}else return;ev.preventDefault()});
document.getElementById('z-mais').addEventListener('click',function(){zoom(1.25)});
document.getElementById('z-menos').addEventListener('click',function(){zoom(1/1.25)});
document.getElementById('z-tudo').addEventListener('click',function(){modo='tudo';tudo()});
// o foco que vem do teclado (Tab) num bairro ou pessoa fora da vista leva a vista até ele; o do mouse, não
var porTeclado=false;
document.addEventListener('keydown',function(ev){if(ev.key==='Tab')porTeclado=true},true);
document.addEventListener('pointerdown',function(){porTeclado=false},true);
svgC.addEventListener('focusin',function(ev){if(!porTeclado)return;var b=ev.target.getBBox&&ev.target.getBBox();if(b)mostrar(b.x+b.width/2,b.y+Math.min(b.height/2,40))});
function reajustar(){if(!tela.clientWidth||!tela.clientHeight)return;if(document.body.classList.contains('cen')||!modo)ajustarTela();else if(modo==='tudo')tudo();else abertura()}
if(window.ResizeObserver)new ResizeObserver(reajustar).observe(tela);else window.addEventListener('resize',reajustar);
abertura();window.addEventListener('load',reajustar);
