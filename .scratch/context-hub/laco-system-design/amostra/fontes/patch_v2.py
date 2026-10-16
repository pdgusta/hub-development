# Volta 2 da amostra: aplica os consertos da porta amostra-1 sobre build_amostra2.py (cópia de build_amostra.py).
import os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(AQUI, 'build_amostra2.py')
s = open(P, encoding='utf-8').read()

def troca(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

# 1. navegação nova (toque, pinça, Ver tudo, foco, rolagem, zoom no centro, canto dos botões)
i = s.index("var tela=document.getElementById('tela')")
j = s.index("var dobra=document.getElementById('dobra-leg');")
nav = open(os.path.join(AQUI, 'nav_v2.js'), encoding='utf-8').read()
s = s[:i] + nav + s[j:]

# 2. camada de detalhe: meia altura de nome entre etiqueta e nome; nomes sem lugar acusados; Desktop e Cliente junto das pessoas
troca("svgC.querySelectorAll('text').forEach(function(t){var b=t.getBBox();obst.push([b.x-8,b.y-6,b.x+b.width+8,b.y+b.height+6])});",
      "svgC.querySelectorAll('text').forEach(function(t){var b=t.getBBox();obst.push([b.x-8,b.y-6,b.x+b.width+8,b.y+b.height+10])});")
a = s.index(" document.querySelectorAll('.bairro').forEach(function(z){var gid=z.getAttribute('data-abre')")
b = s.index("  if(sobra){z.setAttribute('data-sobra',sobra)}})})();")
b2 = b + len("  if(sobra){z.setAttribute('data-sobra',sobra)}})})();")
novo = r'''
 // põe uma etiqueta dentro do retângulo zr, no primeiro lugar livre (de cima para baixo, da esquerda para a direita)
 function colocar(lay,nome,papel,zr,cor,abre){var t=document.createElementNS(NS,'text');t.textContent=nome;var e=document.createElementNS(NS,'g');e.setAttribute('class','etq');e.setAttribute('data-item',nome);
  if(abre)e.setAttribute('data-abre',abre);e.appendChild(t);lay.appendChild(e);var tb=t.getBBox(),w=tb.width+8,h=13,pos=null;
  for(var y=zr.y+8;y+h<=zr.y+zr.height-6&&!pos;y+=1){for(var x=zr.x+8;x+w<=zr.x+zr.width-8;x+=3){var a=[x,y,x+w,y+h];if(livreR(a)){pos=a;break}}}
  if(!pos){lay.removeChild(e);return false}obst.push([pos[0]-3,pos[1]-3,pos[2]+3,pos[3]+3]);
  var r=document.createElementNS(NS,'rect');r.setAttribute('x',pos[0]);r.setAttribute('y',pos[1]);r.setAttribute('width',w);r.setAttribute('height',h);r.setAttribute('rx',6.5);r.setAttribute('stroke',cor);
  e.insertBefore(r,t);t.setAttribute('x',pos[0]+4);t.setAttribute('y',pos[1]+9.5);
  var ti=document.createElementNS(NS,'title');ti.textContent=nome+': '+papel;e.appendChild(ti);return true}
 // nome sem lugar não some calado: fica no console e em data-sobra-nomes do bairro (a ficha continua com ele)
 function acusar(z,onde,nomes){if(!nomes.length)return;z.setAttribute('data-sobra',nomes.length);z.setAttribute('data-sobra-nomes',nomes.join(' | '));
  if(window.console)console.warn('Camada de detalhe: sem lugar em "'+onde+'" para: '+nomes.join(', ')+'. A ficha ainda mostra; abra espaço no bairro.')}
 document.querySelectorAll('.bairro').forEach(function(z){var gid=z.getAttribute('data-abre'),g=G[gid];if(!g)return;var zr=z.querySelector('.zona').getBBox(),s=COR2[gid];
  var lay=document.createElementNS(NS,'g');lay.setAttribute('class','detalhe');z.appendChild(lay);var sobra=[];
  g.itens.filter(function(i){return !DES[i[0]]}).forEach(function(i){if(!colocar(lay,i[0],i[1],zr,s))sobra.push(i[0])});
  acusar(z,g.nome,sobra)});
 // quem chega sem estar desenhado: o Claude Desktop junto do Gustavo (é ele pelo app) e o cliente junto dos agentes; abrem a ficha "Quem chega"
 (function(){var gente=G.gente;if(!gente)return;var lay=document.createElementNS(NS,'g');lay.setAttribute('class','detalhe');svgC.appendChild(lay);var sobra=[];
  [['Claude Desktop','Gustavo'],['Cliente','Agentes']].forEach(function(p){if(DES[p[0]])return;var it=gente.itens.filter(function(i){return i[0]===p[0]})[0],pe=document.querySelector('.pessoa[data-item="'+p[1]+'"]');if(!it||!pe)return;
   var b=pe.getBBox(),zr={x:4,y:b.y+b.height-4,width:182,height:64};if(!colocar(lay,it[0],it[1],zr,'#4a433c','gente'))sobra.push(it[0])});
  acusar(lay,gente.nome,sobra)})()})();'''
s = s[:a] + novo.lstrip('\n') + s[b2:]

# 3. o foco devolvido pela ficha não rola nada; ficha de largura inteira deixa o fundo inerte
troca("function fechar(){f.classList.remove('aberta');if(volta)volta.focus()}",
      "function fundo(v){['.topo','#tela'].forEach(function(q){var e=document.querySelector(q);if(v)e.setAttribute('inert','');else e.removeAttribute('inert')})}\n"
      "function fechar(){f.classList.remove('aberta');fundo(false);if(volta)volta.focus({preventScroll:true})}")
troca(" f.classList.add('aberta');document.getElementById('fechar').focus({preventScroll:true});f.scrollTop=0;",
      " f.classList.add('aberta');fundo(f.offsetWidth>=window.innerWidth-1);document.getElementById('fechar').focus({preventScroll:true});f.scrollTop=0;")

# 4. linhas só do cenário: Checkpoint → Agentes junta-se ao traço do Contrato (um traço só até os agentes);
#    Maestro → Biblioteca entra no caderno pela direita, longe do nome (coordenadas finais, fora do remapeamento)
troca("lig('Checkpoint → Agentes', 'M340,185 H312 V238 H107 V355', 'disc so-cen')",
      "lig('Checkpoint → Agentes', 'M340,185 H312 V238 H95 V355', 'disc so-cen')")
troca("lig('Maestro → Biblioteca do Maestri', 'M108,85 V16 H1197 V766 H565 V688', 'maestro so-cen')",
      "lig('Maestro → Biblioteca do Maestri', 'M108,85 V16 H1197 V881 H655 V714 H582', 'maestro so-cen', fixo=True)")

# 5. CSS: sem seleção de texto no desenho; cabeçalho compacto abaixo de 1100 px
troca(".tela{flex:1 1 auto;position:relative;overflow:hidden;outline:none;touch-action:none;cursor:default;background:var(--papel)}",
      ".tela{flex:1 1 auto;position:relative;overflow:hidden;outline:none;touch-action:none;cursor:default;background:var(--papel);-webkit-user-select:none;user-select:none}")
troca("@media (max-width:760px){",
      "@media (max-width:1100px){\n"
      " .legendas{display:none}.legendas.aberta{display:block}.dobra{display:inline-block}\n"
      " .cen-botoes{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px;scrollbar-width:thin}.cen-botoes button{white-space:nowrap}\n"
      " .ajuda{display:none}header{flex-wrap:nowrap;align-items:center}h1{white-space:nowrap}.ideia{font-size:14px;flex:1 1 280px}.dobra{flex:0 0 auto}\n"
      "}\n@media (max-width:760px){")

# 6. semântica: o desenho tem controles dentro, então é um grupo com nome, não uma imagem
troca('tabindex="-1" focusable="false" role="img" aria-label="Planta da cidade do par',
      'tabindex="-1" focusable="false" role="group" aria-label="Planta da cidade do par')

# 7. legível para editar: dados em várias linhas, SVG quebrado por elemento, roteiro de atualização no topo
troca('JS.replace("__DADOS__", json.dumps(dados, ensure_ascii=False)).replace("__CEN__", json.dumps(cen_js, ensure_ascii=False))',
      'JS.replace("__DADOS__", json.dumps(dados, ensure_ascii=False, indent=1)).replace("__CEN__", json.dumps(cen_js, ensure_ascii=False, indent=1))')
troca("    svg = mapear(cidade())\n",
      "    svg = mapear(cidade())\n"
      "    for tag in ('<g class=\"bairro', '<g class=\"item', '<path data-ligacao', '<path class=\"lig-fundo', '<rect data-fixo'):\n"
      "        svg = svg.replace(tag, '\\n' + tag)\n")
troca('<html lang="pt-BR"><head><meta charset="utf-8">',
      '<html lang="pt-BR"><head><meta charset="utf-8">\n' + '''<!--
Como atualizar quando um ticket muda o desenho. A fonte é amostra/fontes/build_amostra2.py: prefira mudar lá e regerar
(python -I build_amostra2.py <pasta da amostra>). À mão, mude junto, no mesmo nome exato:
 1. Ficha: no script, o objeto G (bairro -> itens [nome, papel, {{dono, aciona, le, ...}}, selos] e lig [De -> Para, frase, selos]).
 2. Componente desenhado: o <g class="item" data-item="Nome"> no SVG, com data-cenario="cenario:passo" e data-chave.
 3. Ligação: <path data-ligacao="De -> Para"> (e o lig-fundo, se a decidir), com data-cenario e data-chave.
 4. Cenários: o objeto C; cada passo lista as chaves (nomes de itens e ligações) que acende.
 5. Camada de detalhe: nasce de G sozinha (componentes da ficha sem desenho). Nome sem lugar no bairro aparece no console
    e no atributo data-sobra-nomes do bairro: abra espaço ou mude o bairro de tamanho.
-->''')

open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('patch ok')

# 8. a 760 px ou menos o cabeçalho volta a quebrar linha (o botão Legenda não pode sair da tela)
s = open(P, encoding='utf-8').read()
a = " header{display:flex;padding:8px 12px 2px;gap:4px 10px}h1{font-size:19px}"
assert s.count(a) == 1
s = s.replace(a, " header{display:flex;flex-wrap:wrap;padding:8px 12px 2px;gap:4px 10px}h1{font-size:19px;white-space:normal}")
open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('patch 8 ok')

# 9. ficha de largura inteira: vira diálogo modal (fundo inerte); estreita ao lado do desenho, segue painel complementar
s = open(P, encoding='utf-8').read()
a = "function fundo(v){['.topo','#tela'].forEach(function(q){var e=document.querySelector(q);if(v)e.setAttribute('inert','');else e.removeAttribute('inert')})}"
assert s.count(a) == 1
s = s.replace(a, a[:-1] + ";if(v){f.setAttribute('role','dialog');f.setAttribute('aria-modal','true')}else{f.removeAttribute('role');f.removeAttribute('aria-modal')}}")
open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('patch 9 ok')
