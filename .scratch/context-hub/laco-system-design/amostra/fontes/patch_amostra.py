import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:100], s.count(a))
    s = s.replace(a, b)

rep('# Mistura, volta 2: planta da B com as linhas de quem aciona (da A) e cenários acesos. Conteúdo só de descricao-do-hub.md (v3.2).',
    '# Amostra (fase 4): a mistura aprovada num canvas de tela inteira (arrastar, zoom, roda). Conteúdo só de descricao-do-hub.md (v3.2).')

# ---------------- desenho: nomes que estavam só na ficha
# Ferramentas: o caderno da biblioteca com nome; a configuração vira etiqueta da camada de detalhe
rep("inner=caixa_ferramentas(490, 660, 'ferramentas')))",
    "inner=item('Biblioteca do Maestri', caderno(478, 656, 'ferramentas') + t(524, 682, 'Biblioteca do Maestri'))))")
rep("def caixa_ferramentas(x, y, gid):", """def caderno(x, y, gid):  # caderno de papéis da biblioteca do Maestri
    s = COR[gid][1]
    return (f'<rect x="{x}" y="{y}" width="34" height="38" rx="4" fill="#fffdf8" stroke="{s}" stroke-width="2.2"/>'
            + ''.join(f'<line x1="{x+6}" y1="{y+10+i*8}" x2="{x+(28 if i < 3 else 22)}" y2="{y+10+i*8}" stroke="{s}" stroke-width="1.6"/>' for i in range(4)))

def caixa_ferramentas(x, y, gid):""")
# Periferia: relógio com nome; o nome do bairro sobe; a linha até a vigia sobe pela direita
rep("zona('periferia', '<rect x=\"700\" y=\"604\" width=\"185\" height=\"131\" rx=\"16\"/>', (712, 722),\n        inner=item('Agendador do Windows', relogio(800, 655, 'periferia'))))",
    "zona('periferia', '<rect x=\"700\" y=\"604\" width=\"185\" height=\"131\" rx=\"16\"/>', (712, 632),\n        inner=item('Agendador do Windows', relogio(800, 672, 'periferia') + t(792, 716, 'Agendador do Windows', anchor='middle'))))")
rep("lig('Agendador do Windows → Sincronizador', 'M783,655 H705 V486 H640', 'agendador'),",
    "lig('Agendador do Windows → Sincronizador', 'M783,672 H705 V486 H640', 'agendador'),")
rep("lig('Agendador do Windows → Vigia do sync', 'M800,638 V472', 'agendador'),",
    "lig('Agendador do Windows → Vigia do sync', 'M817,672 H868 V470 H816', 'agendador'),")
rep("lig('Maestro → Biblioteca do Maestri', 'M108,85 V16 H1197 V766 H607 V706', 'maestro so-cen'),",
    "lig('Maestro → Biblioteca do Maestri', 'M108,85 V16 H1197 V766 H495 V694', 'maestro so-cen'),")

# ---------------- página: canvas de tela inteira
ini = s.index("CSS = r'''"); fim = s.index("JS = r'''")
css = s[ini:fim]
css = css.replace("html,body{margin:0;background:var(--papel);color:var(--tinta);font-family:\"Segoe UI\",system-ui,-apple-system,Roboto,sans-serif}",
 """html,body{margin:0;height:100%;overflow:hidden;background:var(--papel);color:var(--tinta);font-family:"Segoe UI",system-ui,-apple-system,Roboto,sans-serif}
body{display:flex;flex-direction:column;height:100vh;height:100dvh}
.topo{flex:0 0 auto;border-bottom:1px solid var(--linha);background:var(--papel);position:relative;z-index:2}
.tela{flex:1 1 auto;position:relative;overflow:hidden;outline:none;touch-action:none;cursor:default;background:var(--papel)}
.tela.arrastando{cursor:grabbing}
.tela:focus-visible{box-shadow:inset 0 0 0 3px var(--tinta)}
svg.cidade{display:block;width:100%;height:100%}
.zoom{position:absolute;right:14px;bottom:14px;display:flex;gap:6px;z-index:2}
.zoom button{font:inherit;font-size:18px;font-weight:700;min-width:40px;height:40px;border:1px solid var(--linha);background:var(--cartao);color:var(--tinta);border-radius:10px;cursor:pointer;box-shadow:0 2px 6px rgba(60,40,20,.12)}
.zoom button.txt{font-size:14px;font-weight:600;padding:0 12px}
.zoom button:focus-visible,.topo button:focus-visible{outline:3px solid var(--tinta);outline-offset:2px}
.ajuda{position:absolute;left:14px;bottom:14px;z-index:2;font-size:13px;color:var(--suave);background:rgba(255,252,246,.92);border:1px solid var(--linha);border-radius:10px;padding:6px 10px;max-width:calc(100% - 230px)}
.ajuda kbd{font:inherit;font-weight:700;color:var(--tinta)}
.detalhe{display:none}
.perto .detalhe{display:inline}
.etq rect{fill:#fffdf8;stroke-width:1.2}
.etq text{font-size:8.5px;font-weight:600;fill:var(--tinta)}
.etq{cursor:pointer}
.etq:hover rect{stroke:var(--tinta);stroke-width:2}
.dobra{display:none;font:inherit;font-size:13px;border:1px solid var(--linha);background:var(--cartao);border-radius:999px;padding:5px 12px;color:var(--tinta);cursor:pointer}""")
css = css.replace("header{padding:14px 24px 4px;display:flex;flex-wrap:wrap;gap:6px 22px;align-items:baseline}",
                  "header{padding:10px 24px 2px;display:flex;flex-wrap:wrap;gap:4px 22px;align-items:baseline}")
css = css.replace("h1{font-family:Georgia,\"Times New Roman\",serif;font-size:26px;margin:0;font-weight:700}",
                  "h1{font-family:Georgia,\"Times New Roman\",serif;font-size:24px;margin:0;font-weight:700}")
css = css.replace("svg.cidade{display:block;width:100%;max-width:1240px;height:auto;margin:0 auto}\n", "")
css = css.replace("@media (min-width:761px){body.cen svg.cidade{max-height:calc(100vh - 150px)}}", "")
css = css.replace(".cen-passo{position:sticky;top:0;z-index:3;display:flex;", ".cen-passo{display:flex;")
css = css.replace(".cen-botoes{display:flex;flex-wrap:wrap;gap:6px;align-items:center}", ".cen-botoes{display:flex;flex-wrap:wrap;gap:6px;align-items:center}\n.cen-passo{margin-top:2px}")
i = css.index("@media (max-width:760px){")
css = css[:i] + """@media (max-width:760px){
 header{display:flex;padding:8px 12px 2px;gap:4px 10px}h1{font-size:19px}.ideia{display:none}
 .legendas{padding:0 12px 4px}.legendas{display:none}.legendas.aberta{display:block}
 .dobra{display:inline-block}
 .cenarios{padding:2px 12px 6px}
 .cen-botoes{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px}
 .cen-botoes button{white-space:nowrap}
 .cen-passo{gap:6px 8px;padding:6px 8px}.cen-txt{font-size:15px;flex-basis:100%}
 .cen-passo button{padding:5px 10px;font-size:13px}
 .ajuda{display:none}
 .zoom{right:10px;bottom:10px}
}
'''

"""
s = s[:ini] + css + s[fim:]

# ---------------- JS: canvas (viewBox), detalhe ao aproximar, cenário que leva a vista ao passo
rep("""// a faixa do desenho e a página seguem o passo atual (tela estreita ou baixa)
 if(ultima){var pal=document.querySelector('.palco'),rb=ultima.getBoundingClientRect(),rp=pal.getBoundingClientRect();
  if(rb.left<rp.left+20||rb.right>rp.right-20)pal.scrollLeft+=rb.left-rp.left-rp.width/2;
  var topo=painel.getBoundingClientRect().bottom;if(rb.top<topo+10||rb.bottom>window.innerHeight-10)window.scrollBy(0,rb.top-(topo+window.innerHeight)/2)}}""",
""" // a vista vai até o número do passo atual se ele estiver fora da tela
 if(ultima){var b=ultima.getBBox();mostrar(b.x+b.width/2,b.y+b.height/2)}}""")
rep(""" if(!atual){document.body.classList.remove('cen');painel.hidden=true;botoes.forEach(function(b){b.setAttribute('aria-pressed','false')});return}""",
""" if(!atual){document.body.classList.remove('cen');painel.hidden=true;botoes.forEach(function(b){b.setAttribute('aria-pressed','false')});ajustarTela();return}""")
rep(""" var cen=C[atual],N=cen.passos.length;document.body.classList.add('cen');painel.hidden=false;""",
""" var cen=C[atual],N=cen.passos.length,antes=document.body.classList.contains('cen');document.body.classList.add('cen');painel.hidden=false;if(!antes)ajustarTela();""")
rep(""" if(atual&&!f.classList.contains('aberta')){
  if(ev.key==='ArrowRight'""", """ if(atual&&!f.classList.contains('aberta')&&document.activeElement!==tela){
  if(ev.key==='ArrowRight'""")
rep("""// tela estreita: a faixa abre já centrada no Banco local
function centrar(){var p=document.querySelector('.palco'),b=document.querySelector('[data-item="Banco local"]');
 if(!p||!b||p.scrollWidth<=p.clientWidth+1)return;var rp=p.getBoundingClientRect(),rb=b.getBoundingClientRect();
 p.scrollLeft=Math.max(0,p.scrollLeft+rb.left-rp.left-(rp.width-rb.width)/2)}
if(document.readyState==='complete')centrar();else window.addEventListener('load',centrar);""", r"""""")
rep("""var NS='http://www.w3.org/2000/svg';""", r"""var NS='http://www.w3.org/2000/svg';
// ---- canvas: a vista é o viewBox do desenho
var tela=document.getElementById('tela'),svgC=document.querySelector('svg.cidade'),CONT={x:0,y:0,w:1200,h:780},vb=null,MIN=.35,MAX=5;
function px(){return tela.clientWidth/vb.w}
function aplicar(){svgC.setAttribute('viewBox',vb.x.toFixed(2)+' '+vb.y.toFixed(2)+' '+vb.w.toFixed(2)+' '+vb.h.toFixed(2));
 svgC.classList.toggle('perto',px()>=1.7);var z=document.getElementById('z-nivel');if(z)z.textContent=Math.round(px()*100)+'%'}
function caber(){var W=tela.clientWidth,H=tela.clientHeight,m=10,e=Math.min((W-2*m)/CONT.w,(H-2*m)/CONT.h);return e}
function ajustar(){var W=tela.clientWidth,H=tela.clientHeight,e=caber();
 if(e<.6){e=.75;var bl=document.querySelector('[data-item="Banco local"]').getBBox();var cx=bl.x+bl.width/2,cy=bl.y+bl.height/2;vb={w:W/e,h:H/e};vb.x=cx-vb.w/2;vb.y=cy-vb.h/2}
 else{vb={w:W/e,h:H/e};vb.x=CONT.x-(vb.w-CONT.w)/2;vb.y=CONT.y-(vb.h-CONT.h)/2}aplicar()}
function ajustarTela(){if(!vb)return;var cx=vb.x+vb.w/2,cy=vb.y+vb.h/2,e=px();var W=tela.clientWidth,H=tela.clientHeight;if(!W||!H)return;vb.w=W/e;vb.h=H/e;vb.x=cx-vb.w/2;vb.y=cy-vb.h/2;aplicar()}
function prender(){var e=px(),lim=Math.min(vb.w,vb.h)*.5;
 vb.x=Math.min(Math.max(vb.x,CONT.x-vb.w+lim),CONT.x+CONT.w-lim);vb.y=Math.min(Math.max(vb.y,CONT.y-vb.h+lim),CONT.y+CONT.h-lim)}
function zoom(f,sx,sy){var e=px(),n=Math.min(MAX,Math.max(MIN,e*f));f=n/e;if(f===1)return;
 var r=tela.getBoundingClientRect();if(sx==null){sx=r.width/2;sy=r.height/2}
 var ux=vb.x+sx/e,uy=vb.y+sy/e;vb.w/=f;vb.h/=f;vb.x=ux-sx/n;vb.y=uy-sy/n;prender();aplicar()}
function andar(dx,dy){var e=px();vb.x+=dx/e;vb.y+=dy/e;prender();aplicar()}
function mostrar(x,y){var mx=vb.w*.08,my=vb.h*.08;if(x<vb.x+mx||x>vb.x+vb.w-mx||y<vb.y+my||y>vb.y+vb.h-my){vb.x=x-vb.w/2;vb.y=y-vb.h/2;prender();aplicar()}}
tela.addEventListener('wheel',function(ev){ev.preventDefault();var r=tela.getBoundingClientRect(),d=ev.deltaMode===1?ev.deltaY*16:ev.deltaY;
 if(ev.ctrlKey||ev.metaKey){zoom(Math.exp(-d*.0018),ev.clientX-r.left,ev.clientY-r.top)}
 else if(ev.shiftKey){andar(ev.deltaX||d,0)}else{andar(ev.deltaX,d)}},{passive:false});
tela.addEventListener('contextmenu',function(ev){ev.preventDefault()});
var toques={},arr=null;
tela.addEventListener('pointerdown',function(ev){
 if(ev.pointerType==='touch'){toques[ev.pointerId]={x:ev.clientX,y:ev.clientY}}
 else if(ev.button!==2&&ev.button!==1)return;
 arr={x:ev.clientX,y:ev.clientY,mov:false};tela.setPointerCapture(ev.pointerId)});
tela.addEventListener('pointermove',function(ev){if(!arr)return;
 var ids=Object.keys(toques);
 if(ev.pointerType==='touch'&&ids.length===2&&toques[ev.pointerId]){var o=ids.map(function(i){return toques[i]}),d0=Math.hypot(o[0].x-o[1].x,o[0].y-o[1].y);
  toques[ev.pointerId]={x:ev.clientX,y:ev.clientY};var n=ids.map(function(i){return toques[i]}),d1=Math.hypot(n[0].x-n[1].x,n[0].y-n[1].y),r=tela.getBoundingClientRect();
  if(d0>0)zoom(d1/d0,(n[0].x+n[1].x)/2-r.left,(n[0].y+n[1].y)/2-r.top);arr.mov=true;return}
 if(ev.pointerType==='touch')toques[ev.pointerId]={x:ev.clientX,y:ev.clientY};
 var dx=ev.clientX-arr.x,dy=ev.clientY-arr.y;if(!arr.mov&&Math.hypot(dx,dy)<6)return;
 arr.mov=true;tela.classList.add('arrastando');andar(-dx,-dy);arr.x=ev.clientX;arr.y=ev.clientY});
function solta(ev){delete toques[ev.pointerId];if(arr&&arr.mov){tela.dataset.arrastou='1';setTimeout(function(){delete tela.dataset.arrastou},0)}
 if(!Object.keys(toques).length){arr=null;tela.classList.remove('arrastando')}}
tela.addEventListener('pointerup',solta);tela.addEventListener('pointercancel',solta);
tela.addEventListener('click',function(ev){if(tela.dataset.arrastou){ev.stopPropagation();ev.preventDefault()}},true);
tela.addEventListener('keydown',function(ev){if(ev.target!==tela)return;var k=ev.key,p=60;
 if(k==='ArrowLeft')andar(-p,0);else if(k==='ArrowRight')andar(p,0);else if(k==='ArrowUp')andar(0,-p);else if(k==='ArrowDown')andar(0,p);
 else if(k==='+'||k==='=')zoom(1.25);else if(k==='-'||k==='_')zoom(1/1.25);else if(k==='0')ajustar();else return;ev.preventDefault()});
document.getElementById('z-mais').addEventListener('click',function(){zoom(1.25)});
document.getElementById('z-menos').addEventListener('click',function(){zoom(1/1.25)});
document.getElementById('z-tudo').addEventListener('click',ajustar);
// o foco (Tab) num bairro ou pessoa fora da vista leva a vista até ele
svgC.addEventListener('focusin',function(ev){var b=ev.target.getBBox&&ev.target.getBBox();if(b)mostrar(b.x+b.width/2,b.y+Math.min(b.height/2,40))});
window.addEventListener('resize',ajustarTela);
ajustar();
var dobra=document.getElementById('dobra-leg');dobra.addEventListener('click',function(){var l=document.querySelector('.legendas'),a=l.classList.toggle('aberta');dobra.setAttribute('aria-expanded',a);ajustarTela()});
// ---- camada de detalhe: ao aproximar, cada bairro mostra, em etiquetas pequenas, os componentes que só estavam na ficha
(function(){var DES={};document.querySelectorAll('[data-item]').forEach(function(e){DES[e.getAttribute('data-item')]=1});
 var obst=[];svgC.querySelectorAll('text').forEach(function(t){var b=t.getBBox();obst.push([b.x-3,b.y-3,b.x+b.width+3,b.y+b.height+3])});
 svgC.querySelectorAll('.item').forEach(function(g){var b=g.getBBox();obst.push([b.x-3,b.y-3,b.x+b.width+3,b.y+b.height+3])});
 svgC.querySelectorAll('.lig:not(.so-cen),.lig-fundo').forEach(function(p){var L=p.getTotalLength(),w=parseFloat(getComputedStyle(p).strokeWidth)/2+4;for(var d=0;d<=L;d+=5){var q=p.getPointAtLength(d);obst.push([q.x-w,q.y-w,q.x+w,q.y+w])}});
 svgC.querySelectorAll('.mini,.via,.encontro').forEach(function(r){var b=r.getBBox();obst.push([b.x-2,b.y-2,b.x+b.width+2,b.y+b.height+2])});
 function livreR(a){return a[0]>=0&&obst.every(function(b){return a[2]<b[0]||a[0]>b[2]||a[3]<b[1]||a[1]>b[3]})}
 document.querySelectorAll('.bairro').forEach(function(z){var gid=z.getAttribute('data-abre'),g=G[gid];if(!g)return;var zr=z.querySelector('.zona').getBBox(),s=COR2[gid];
  var falta=g.itens.filter(function(i){return !DES[i[0]]}),lay=document.createElementNS(NS,'g');lay.setAttribute('class','detalhe');z.appendChild(lay);var sobra=0;
  falta.forEach(function(i){var t=document.createElementNS(NS,'text');t.textContent=i[0];var e=document.createElementNS(NS,'g');e.setAttribute('class','etq');e.setAttribute('data-item',i[0]);
   e.appendChild(t);lay.appendChild(e);var tb=t.getBBox(),w=tb.width+8,h=13,pos=null;
   for(var y=zr.y+8;y+h<=zr.y+zr.height-6&&!pos;y+=3){for(var x=zr.x+8;x+w<=zr.x+zr.width-8;x+=3){var a=[x,y,x+w,y+h];if(livreR(a)){pos=a;break}}}
   if(!pos){lay.removeChild(e);sobra++;return}obst.push([pos[0]-3,pos[1]-3,pos[2]+3,pos[3]+3]);
   var r=document.createElementNS(NS,'rect');r.setAttribute('x',pos[0]);r.setAttribute('y',pos[1]);r.setAttribute('width',w);r.setAttribute('height',h);r.setAttribute('rx',6.5);r.setAttribute('stroke',s);
   e.insertBefore(r,t);t.setAttribute('x',pos[0]+4);t.setAttribute('y',pos[1]+9.5);
   var ti=document.createElementNS(NS,'title');ti.textContent=i[0]+': '+i[1];e.appendChild(ti)});
  if(sobra){z.setAttribute('data-sobra',sobra)}})})();""")
rep("""var G=__DADOS__,C=__CEN__;""", """var G=__DADOS__,C=__CEN__,COR2=__COR__;""")

# ---------------- página
ini = s.index("def pagina():")
fim = s.index("with open(os.path.join(OUT, 'mistura.html')")
s = s[:ini] + r'''def pagina():
    dados = {k: dict(nome=v['nome'], frase=v['frase'],
                     itens=[[a, b, q, [list(s_) for s_ in ss]] for a, b, q, ss in v['itens']],
                     lig=[[a, b, [list(s_) for s_ in ss]] for a, b, ss in v['lig']]) for k, v in G.items()}
    cen_js = {cid: dict(nome=nome, passos=[[txt, ch, fl] for txt, ch, fl in passos]) for cid, nome, passos in CENARIOS}
    bcen = ''.join(f'<button type="button" data-cen="{cid}" aria-pressed="false">{esc(nome)}</button>' for cid, nome, _ in CENARIOS)
    svg = cidade()
    faltam = set(CEN) - USADAS
    assert not faltam, faltam
    titulo_p = 'A cidade e quem a aciona'
    ideia = 'Cada linha sai de quem aciona e tem a cor dele. Escolha um cenário para ver o caminho aceso, passo a passo.'
    cor2 = {k: v[1] for k, v in COR.items()}
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo_p}</title><style>{CSS}</style></head>
<body>
<div class="topo">
<header><h1>{titulo_p}</h1><p class="ideia">{esc(ideia)}</p><button type="button" class="dobra" id="dobra-leg" aria-expanded="false">Legenda</button></header>
{LEGENDA}
<section class="cenarios" aria-label="Cenários">
<div class="cen-botoes"><span class="rot-cen">Cenários</span>{bcen}</div>
<div class="cen-passo" id="cen-passo" hidden aria-live="polite"><span class="cen-n"><span class="nome" id="cen-nome"></span><span id="cen-num"></span></span><span class="cen-txt" id="cen-txt"></span>
<button type="button" id="cen-ant">← Anterior</button><button type="button" id="cen-prox">Próximo →</button><button type="button" id="cen-sair">Sair do cenário</button></div>
</section>
</div>
<main class="tela" id="tela" tabindex="0" aria-label="Planta do hub. Setas andam, + e − aproximam e afastam, 0 mostra tudo.">
<svg class="cidade" viewBox="0 0 1200 780" role="img" aria-label="Planta da cidade do par: muralha com nove bairros, as pessoas à esquerda com as linhas do que cada uma aciona, a estrada da rede privada e o outro par em miniatura.">{DEFS}{svg}</svg>
<p class="ajuda">Arraste com o botão direito · <kbd>Ctrl</kbd> + roda: zoom · <kbd>Shift</kbd> + roda: para os lados · aproxime para ver mais nomes</p>
<div class="zoom" role="group" aria-label="Zoom"><button type="button" id="z-menos" aria-label="Afastar">−</button><button type="button" id="z-mais" aria-label="Aproximar">+</button><button type="button" class="txt" id="z-tudo">Ver tudo <span id="z-nivel" aria-hidden="true"></span></button></div>
</main>
<aside id="ficha" aria-live="polite" aria-label="Ficha do bairro"><button id="fechar" type="button">Fechar</button><div id="ficha-corpo"></div></aside>
<script>{JS.replace("__DADOS__", json.dumps(dados, ensure_ascii=False)).replace("__CEN__", json.dumps(cen_js, ensure_ascii=False)).replace("__COR__", json.dumps(cor2))}</script>
</body></html>"""

''' + s[fim:]
rep("with open(os.path.join(OUT, 'mistura.html'), 'w', encoding='utf-8', newline='\\n') as fh:",
    "with open(os.path.join(OUT, 'amostra.html'), 'w', encoding='utf-8', newline='\\n') as fh:")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
