# Volta 3 da amostra: build_amostra3.py = build_amostra2.py + estes consertos (porta amostra-2).
# Uso, na pasta amostra/: python -I fontes/patch_v3.py && python -I fontes/build_amostra3.py .
import os
AQUI = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(AQUI, 'build_amostra2.py'), encoding='utf-8').read()

def troca(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)

# 1. perda de captura: só encerra o gesto quando quem perde é a própria tela. A perda no elemento tocado, quando a
#    tela toma a captura (transferência, aos 6 px), borbulha até aqui e não pode apagar o dedo que segue arrastando.
troca("['pointerup','pointercancel','lostpointercapture'].forEach(function(n){tela.addEventListener(n,solta)});",
      "['pointerup','pointercancel'].forEach(function(n){tela.addEventListener(n,solta)});\n"
      "tela.addEventListener('lostpointercapture',function(ev){if(ev.target===tela)solta(ev)});")

# 2. a modalidade da ficha acompanha a largura enquanto ela está aberta; ao virar modal, o foco vai para dentro dela
troca("document.getElementById('fechar').addEventListener('click',fechar);",
      "document.getElementById('fechar').addEventListener('click',fechar);\n"
      "window.addEventListener('resize',function(){if(!f.classList.contains('aberta'))return;var m=f.offsetWidth>=window.innerWidth-1;\n"
      " if(m===(f.getAttribute('aria-modal')==='true'))return;fundo(m);if(m&&!f.contains(document.activeElement))document.getElementById('fechar').focus({preventScroll:true})});")

# 3. a legenda recolhe também em janela baixa (menos de 800 px de altura)
troca("@media (max-width:1100px){",
      "@media (max-height:800px){\n .legendas{display:none}.legendas.aberta{display:block}.dobra{display:inline-block}\n}\n@media (max-width:1100px){")

# 4. fileira de cenários que rola: as bordas esmaecem do lado em que há mais botões
troca(".cen-passo{margin-top:2px}",
      ".cen-passo{margin-top:2px}\n"
      ".cen-botoes.mais-dir{-webkit-mask-image:linear-gradient(90deg,#000 calc(100% - 64px),transparent);mask-image:linear-gradient(90deg,#000 calc(100% - 64px),transparent)}\n"
      ".cen-botoes.mais-esq{-webkit-mask-image:linear-gradient(90deg,transparent,#000 48px);mask-image:linear-gradient(90deg,transparent,#000 48px)}\n"
      ".cen-botoes.mais-esq.mais-dir{-webkit-mask-image:linear-gradient(90deg,transparent,#000 48px,#000 calc(100% - 64px),transparent);mask-image:linear-gradient(90deg,transparent,#000 48px,#000 calc(100% - 64px),transparent)}")
troca("var dobra=document.getElementById('dobra-leg');",
      "(function(){var r=document.querySelector('.cen-botoes');function marca(){var x=r.scrollLeft,fim=r.scrollWidth-r.clientWidth;r.classList.toggle('mais-esq',x>2);r.classList.toggle('mais-dir',x<fim-2)}\n"
      " r.addEventListener('scroll',marca);window.addEventListener('resize',marca);marca();\n"
      " r.addEventListener('focusin',function(ev){if(ev.target.scrollIntoView)ev.target.scrollIntoView({block:'nearest',inline:'nearest'})})})();\n"
      "var dobra=document.getElementById('dobra-leg');")

open(os.path.join(AQUI, 'build_amostra3.py'), 'w', encoding='utf-8', newline='\n').write(s)
print('patch v3 ok')
