# Amostra: a cidade e quem a aciona, em tela inteira

A mistura aprovada pelo Gustavo, como página final: a mesma planta, as mesmas linhas, as mesmas fichas e os mesmos sete
cenários, agora num canvas de tela inteira, sem rolagem, que se arrasta e aproxima. Fonte do conteúdo:
`descricao/descricao-do-hub.md`, v3.2. A mistura em `conceitos/mistura/` não foi tocada; o `system-design.html` também
não.

## Como navegar

| Para | Mouse | Teclado | Toque |
|---|---|---|---|
| andar pelo desenho | arrastar com o botão direito (ou o do meio); roda: para cima e para baixo; **Shift + roda**: para os lados | foco no desenho (Tab até ele), **setas** | arrastar com um dedo |
| aproximar e afastar | **Ctrl + roda** (o ponto sob o mouse fica parado) | **+** e **−** | pinça com dois dedos |
| ver tudo de novo | botão "Ver tudo" (mostra também o nível de zoom): a cidade inteira, em qualquer largura | **0** | botão "Ver tudo" |
| abrir uma ficha | clique num bairro, num componente, numa etiqueta ou numa pessoa | Tab até o bairro ou a pessoa, Enter; Esc fecha | toque (arrastar não abre) |
| seguir um cenário | botão do cenário; Anterior e Próximo | as setas avançam e voltam o passo quando o foco não está no desenho; Esc sai | toque |

O clique esquerdo fica para as fichas e não seleciona texto, como o Gustavo pediu ("quase tudo estático; os cards clicáveis"). Quando o
foco do Tab cai num bairro fora da vista, a vista vai até ele (o foco que vem do mouse não mexe na vista). No cenário, a vista vai até o número do passo se ele
estiver fora da tela.

## O que mudou em relação à mistura, e por quê

1. **Canvas de tela inteira.** A página ocupa a janela e não rola; o desenho fica numa área que se arrasta e aproxima
   (o zoom muda o recorte do desenho, não o tamanho da página). O topo tem o título, a legenda e os cenários; com um
   cenário ligado, a faixa do passo toma o lugar da legenda e dos botões, como na mistura.
2. **Visão inicial = a planta aprovada.** Abre enquadrada (93% a 1280 x 1000). Em telas estreitas, em que caber tudo
   deixaria o texto pequeno demais, abre a 75% centrada no Banco local; "Ver tudo" mostra a cidade inteira.
3. **Mais nomes no desenho (o teto de 25 saiu).** Dois componentes que eram ícones sem nome ganharam rótulo: o
   **Agendador do Windows** (o relógio) e a **Biblioteca do Maestri** (o caderno). São 27 rótulos na visão inicial.
4. **Camada de detalhe ao aproximar.** A partir de 140% de zoom, cada bairro mostra, em etiquetas pequenas, os
   componentes que antes só estavam na ficha (40 etiquetas: Checagem de sessão, Guarda do acervo, Porta de leitura,
   Índice da busca, Avisos, Raiz, inbox/, Cópia no GitHub, Kit de par e os outros). Cada etiqueta abre a ficha nela. É a
   camada "aproximar" que a régua já prevê para o detalhe; a visão inicial não fica mais carregada. As etiquetas acham
   lugar sozinhas, longe dos nomes e das linhas.
5. **A fileira de cima e a de baixo ficaram 45 e 70 unidades mais altas**, para caberem as etiquetas da Disciplina, do
   Conteúdo, da Periferia e das Ferramentas. Nada mudou de lugar na ordem: os bairros, as linhas e os pontos de encontro
   são os mesmos; a miniatura do outro par acompanha a planta nova.
6. **Detalhes de posição:** o nome da Periferia do par subiu e a linha do Agendador até a vigia passou pela direita do
   bairro, para o relógio ter nome; o caderno da Biblioteca ficou no meio do bairro, com o nome embaixo; os botões de
   zoom ficam no canto de baixo à esquerda, que é vazio em todos os cenários (no canto direito passa a linha do maestro
   à biblioteca).

## Conferência própria

- `medidas-da-peca` a 320 e a 1280 px: 27 rótulos na visão inicial, 20 ligações visíveis, 0 cruzamentos, folga mínima
  22,3 px (rótulo de 19 px), razão entre grupos 1,53 (limite 1,5), contraste 58 de 58 textos, sem rolagem.
- Tab real: 23 de 23 paradas com foco visível (7 cenários, o desenho, 9 bairros, 3 pessoas, 3 botões de zoom).
- Os sete cenários, todos os 39 passos: cada passo desenha o seu número, a no máximo 16 unidades do que acende; depois
  de Esc, os botões voltam a `aria-pressed="false"`; a página tem a altura da janela.
- Ficha: o clique no nome "Sincronizador" abre a ficha do Núcleo já nele.
- 320 x 640: sem rolagem da página; a vista abre no Banco local; no cenário, vai até o passo.
- Mouse de verdade (eventos do Edge pelo protocolo de depuração): arrastar com o botão direito anda; Ctrl + roda
  aproxima até 160% e liga a camada de detalhe; Shift + roda anda para os lados; depois disso, o clique esquerdo no
  Banco local abre a ficha nele.
- Não testado: o toque (arrastar com um dedo, pinça) num aparelho de verdade.

## Volta 2 (porta amostra-1)

Consertos linha a linha em `consertos.md`; escolhas em `decisoes.md` (13 a 19). Em resumo:
- **Arrasto sem salto**: o aperto do botão direito ou do meio não leva o foco; a vista só segue o foco do Tab.
- **Toque**: tocar abre ficha e aperta botão; da pinça para um dedo, sem salto. (Dizia também "arrastar com um dedo
  anda": errado nesta volta, parava em 12 px; corrigido na volta 3.)
- **`+` e `−`** aproximam em volta do centro. **"Ver tudo" e `0`** mostram a cidade inteira, até a 320 px (25%).
- **Abertura**: inteira se o menor nome ficar com 13 px ou mais, fora do canto dos botões; se não, 75% no Banco local.
- **Cabeçalho** compacto abaixo de 1100 px (legenda no botão, cenários numa fileira): 106 px a 960.
- **Cenários**: Checkpoint → Agentes desce num traço só com o Contrato; a linha da Biblioteca entra pela direita.
- **Camada de detalhe**: 10 unidades entre etiqueta e o nome de cima; Claude Desktop e Cliente junto das pessoas
  (42 etiquetas); nome sem lugar é acusado no console e em `data-sobra-nomes`.
- **Código**: SVG como grupo com nome; ficha modal quando cobre a tela; dados e SVG em várias linhas, com um roteiro de
  atualização no topo do HTML.

## Volta 3 (porta amostra-2)

Consertos e evidência em `consertos.md`, seção "Volta 3"; decisões 20 e 21 em `decisoes.md`.
- **Arrasto com um dedo anda por todo o percurso** (antes parava em 12 px): a perda de captura do elemento tocado,
  quando o desenho toma a captura, não encerra mais o gesto. Conferido com o roteiro do QA: 96 x 48 px de 96 x 48.
- **Ficha**: vira modal ou deixa de ser conforme a largura, também com ela aberta.
- **Cabeçalho**: a legenda recolhe também em janela baixa (menos de 800 px): 139 px a 1280 x 720.
- **Cenários numa fileira**: a borda esmaece do lado em que há mais botões.
