# Brief da amostra (fase 4)

Do maestro ao UI engineer, 2026-10-15. Fase 4 do `orquestracao.md`, etapa 11.

## O que o Gustavo decidiu

A carta da mistura foi **aprovada sem alteração** (envio `8c6e7d3e…`, 17:17): "absolutamente perfeito", "você encontrou a
forma perfeita de mostrar cada cenário". E uma regra muda: **o teto de 25 rótulos sai.** Podem existir mais rótulos,
desde que a peça siga sem poluição, com a folga e o espaço devidos a cada rótulo. As demais regras da régua continuam
(0 cruzamentos fora de encontro, folga mínima, razão entre grupos e dentro de grupo, contraste, foco).

## O pedido

Construir a mistura aprovada como **amostra da peça final**, numa página à parte: `laco-system-design/amostra/` (crie),
sem tocar o `system-design.html` nem `conceitos/mistura/`. A amostra é o que, com o aval do Gustavo, vai substituir o
`system-design.html`, aberto no portal "System design" do Maestri ao lado do terminal.

O Gustavo pediu para essa página, em 2026-10-14 (nota no `map.md`), uma forma de **canvas de tela inteira, sem rolagem**:
- arrastar com o botão direito do mouse;
- Ctrl + roda para zoom;
- Shift + roda para andar na horizontal;
- quase tudo estático; os cards (as fichas) clicáveis.

Junte isso à mistura sem perder o que foi aprovado (a planta das duas cidades, a cor de quem aciona, as fichas com dono
e quem lê, os sete cenários acesos passo a passo). Com o teto de rótulos solto, você pode trazer da ficha para o desenho o
que ajudar a ler sem abrir (por exemplo, os nomes de componentes que hoje só aparecem na ficha), desde que a folga e a
separação passem. Mantenha a marcação `data-item`, `data-grupo`, `data-ligacao`, `data-encontro`, `data-cenario`, que o
QA mede.

Fonte do conteúdo: a descrição do hub (`descricao/descricao-do-hub.md`, v3.2). HTML único, CSS e SVG embutidos, sem CDN
nem rede. Teclado: Tab e foco visível; zoom e deslocamento também pelo teclado (setas e +/−). Em 320 px: utilizável.

## Entrega, em `amostra/`

- `amostra.html`; `amostra.md` (o que mudou em relação à mistura e por quê; como navegar); `decisoes.md`.
- Depois: o QA testa, o UX revisor e o Tech lead revisam e um revisor de código revisa, até 3 voltas; então o Gustavo vê a
  amostra pronta.

Ao terminar: `maestri ask "Claude Code" "pronto: <caminho>"`.
