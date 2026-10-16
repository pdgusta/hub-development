# Consertos da amostra, volta 2

Porta da amostra, volta 1 (`portas/amostra-1/`). A volta 1 está guardada em `amostra-v1.html`. Gerador novo:
`fontes/build_amostra2.py` (cópia de `build_amostra.py` com `fontes/patch_v2.py` aplicado; a navegação em `fontes/nav_v2.js`).

## Prumo (código)

| # | Conserto | Situação |
|---|---|---|
| 1 | Toque simples ativa fichas e botões | **feito.** O toque não é capturado no aperto; só vira captura depois de 6 px de movimento. Os botões de zoom ficam fora do gesto. O clique que nasce de um arrasto é barrado por uma marca do próprio gesto, que o próximo aperto apaga (sem `setTimeout`). Conferido com toque emulado do Edge: tocar no `+` aproxima; tocar no Banco local abre a ficha nele; arrastar com um dedo anda e não abre ficha. **Corrigido na volta 3:** o arrasto de um dedo andava só os primeiros 12 px e parava (QA da volta 2); o meu teste deu 8 x 5 px para um pedido de 64 x 40 e eu li como certo. |
| 2 | Pinça para um dedo sem salto; mesma limpeza no cancelamento e na perda de captura | **feito.** Ao mudar o número de dedos, a referência do gesto vem do dedo que ficou. `pointerup`, `pointercancel` e `lostpointercapture` passam pela mesma função. Conferido: depois da pinça, tirar um dedo e mover 2 px desloca 2 px. **Corrigido na volta 3:** ligar `lostpointercapture` à mesma limpeza encerrava o gesto de um dedo; e o meu teste de "tirar um dedo" não soltava o dedo (ver volta 3). |
| 3 | "Ver tudo" e `0` enquadram a cidade inteira também em 320 | **feito.** "Ver tudo" e `0` chamam um enquadramento só deles; a abertura é outra função. O zoom mínimo passa a ser 35% ou o enquadramento inteiro, o que for menor (a 320 x 640: 25%). |
| 4 | Semântica do SVG e ficha que cobre a tela | **feito.** O SVG virou `role="group"` com nome (tem controles dentro). Quando a ficha ocupa a largura toda, ela vira diálogo modal (`role="dialog"`, `aria-modal`) e o topo e o desenho ficam `inert`; ao fechar, volta tudo e o foco volta ao bairro. Mais estreita que a tela, segue painel não modal. Leitor de tela: não verificado. |
| 5 | Acusar nomes descartados pelo empacotamento | **feito.** Nome sem lugar vai ao console (`console.warn` com o bairro e os nomes) e ao atributo `data-sobra-nomes` do bairro. Hoje: nenhum. |
| 6 | Dados e SVG legíveis; roteiro de atualização | **feito.** `G` e `C` em várias linhas; o SVG quebra linha por bairro, item e ligação; um comentário no topo do HTML diz o que mudar junto quando um ticket muda o desenho. |
| — | Roda com `deltaMode=2` (menor) | **feito.** Página vira a altura da área. |

## UX revisor

| # | Conserto | Situação |
|---|---|---|
| 1 | Salto a partir do segundo arrasto com o botão direito | **feito.** Causa: o aperto levava o foco ao bairro, e a vista ia até ele. Agora o aperto do botão direito e do meio não leva foco (`mousedown` e `pointerdown` cancelados); a vista só vai até o bairro focado quando o foco vem do Tab; a área do desenho nunca rola (`scroll` volta a 0). Conferido com entrada real do Edge (protocolo de depuração): três arrastos seguidos, o banco anda exatamente 100 x 60 px em cada um e não mexe no aperto; botão do meio igual. |
| 2 | `+` e `−` em volta do centro | **feito.** Conferido: o centro da vista fica no mesmo ponto do desenho depois de três `+` e três `−` (1280 x 1000: [600, 450] antes e depois). |
| 3 | Arrasto esquerdo seleciona texto | **feito** (só a parte pedida): `user-select: none` no desenho. Seleção depois do arrasto: 0 caracteres. O arrasto esquerdo que anda ficou **fora**, como o brief manda. |
| 4 | Cabeçalho a 960 px | **feito.** Abaixo de 1100 px a legenda recolhe no botão "Legenda" e os cenários ficam numa fileira que rola para os lados. A 960 x 800: 106 px (era 290). |
| 5 | Vista inicial fora do canto dos botões; 75% se o menor nome ficar abaixo de 13 px | **feito.** Ver decisões 13 e 14. A 960 x 800 abre inteira a 72%; a 1280 x 720 abre a 75% no Banco local; a 1280 x 1000 segue em 93%; a 1920 x 1080 em 104%. Gustavo fora dos botões em todas. |
| 6 | "Um agente novo", passo 6: dois roxos colados | **feito de outro jeito** (a segunda saída do parecer): a linha do Checkpoint junta-se ao traço do Contrato e os dois descem num traço só até os agentes. Decisão 15. |
| 7 | "Um maestro novo": a linha corta o nome da Biblioteca | **feito.** A linha entra no caderno pela direita, longe do nome. |
| 8 | Etiquetas coladas embaixo de um nome | **feito.** Pelo menos 10 unidades (meia altura de um nome) entre a etiqueta e o nome de cima; 6 dos outros lados. As 40 cabem. Decisão 16. |

## Tech lead

| # | Conserto | Situação |
|---|---|---|
| 1 | Claude Desktop e Cliente na camada de detalhe (opcional) | **feito.** Duas etiquetas ao aproximar: "Claude Desktop" embaixo do Gustavo e "Cliente" embaixo dos Agentes; abrem a ficha "Quem chega ao hub" já no item. Não somam rótulo à vista inicial. |

## Conferência desta volta

- Medidas a 320, 960 e 1280: 27 rótulos, 20 ligações visíveis, 0 cruzamentos, folga mínima 22,3 px a 1280 (rótulo 19),
  razão entre grupos 1,53 (igual à volta 1: a planta não mudou), contraste 58 de 58, sem rolagem.
- Tab real: 23 paradas, todas com foco visível.
- Cenários: 39 passos, todos com número, distância máxima 16; Esc devolve `aria-pressed="false"`; altura 1000.
- Navegação com entrada real a 320, 960, 1280 x 720, 1280 x 1000 e 1920 x 1080 (`fontes/teste-v2.mjs`).
- Não testado: aparelho de toque de verdade (só toque emulado do Edge), leitor de tela.

## Volta 3 (porta amostra-2)

Volta 2 guardada em `amostra-v2.html`. Gerador: `fontes/build_amostra3.py` = `build_amostra2.py` + `fontes/patch_v3.py`.

**Correção do que a volta 2 afirmou.** A tabela acima dizia que o arrasto com um dedo andava. Não andava: parava depois
de 12 px, em qualquer alvo, a 1280 e a 320 (QA, `qa/amostra-2/navegacao/toque-alvos.json`). Dois erros meus: o meu teste
pedia 64 x 40 px, recebia 8 x 5 e eu li como certo; e, no teste da pinça, o protocolo não soltava o dedo (`touchMove`
com menos dedos não solta nenhum), então "tirar um dedo e mover 2 px" media outra coisa. As linhas da volta 2 ficam
como estavam, com a nota de correção.

| # | Conserto | Situação |
|---|---|---|
| Prumo 1 (bloqueio) | Arrasto de um dedo segue por todo o percurso | **feito.** `lostpointercapture` só encerra o gesto quando quem perde a captura é a própria tela. A perda no elemento tocado, quando a tela toma a captura aos 6 px, é transferência e passa direto. `pointerup` e `pointercancel` seguem com a limpeza de antes. **Reproduzi antes** com o roteiro do QA (`toque-alvos.mjs`, mesmos três alvos, 8 passos de 12 x 6 px, a 1280 x 1000 e 320 x 640): 12 x 6 nos seis casos. **Depois:** 96 x 48 nos seis, sem ficha aberta. |
| — | O que precisava continuar | **conferido com toque emulado do Edge:** arrasto longo (30 passos) em cima do Banco local anda -150 x -90 como pedido e não abre ficha; o toque seguinte abre a ficha no Banco local; toque no `+` aproxima (93 para 117%); pinça, soltar um dedo (`touchEnd` só com ele) e arrastar o outro 20 passos: 80 x 40 como pedido; `touchCancel` no meio do arrasto encerra (sem "arrastando") e o toque seguinte abre ficha. Mouse sem mudança: três arrastos com o botão direito sem salto, botão do meio, `+` no centro, `0`. |
| Prumo 3 | Documentação | **feito.** Nota de correção nas linhas da volta 2 (acima) e em `amostra.md`; esta seção traz a evidência nova. |
| Prumo (ressalva) | Modalidade da ficha acompanha a largura | **feito.** Com a ficha aberta, ao redimensionar, ela vira modal (fundo inerte) se passa a cobrir a tela e deixa de ser se não cobre. Ao virar modal com o foco fora dela, o foco vai para "Fechar". Conferido: aberta a 1280 (não modal) → 320 (modal, foco em "Fechar") → 1280 (não modal); fechar devolve o foco ao bairro. |
| UX 2 | Cabeçalho a 1280 x 720 | **feito.** A legenda recolhe no botão "Legenda" também com a janela abaixo de 800 px de altura. 1280 x 720: 139 px (era 185). 1280 x 1000 sem mudança (185). |
| UX 3 | Fileira de cenários cortada sem aviso | **feito.** Quando a fileira rola, a borda do lado em que há mais botões esmaece (direita no começo, esquerda no fim, as duas no meio). O botão que recebe foco pelo Tab rola para a vista. |

Conferência: medidas a 320, 960 e 1280 iguais (27 rótulos, 20 ligações, 0 cruzamentos, folga 22,3 px, razão 1,53,
contraste 58/58, sem rolagem); Tab real 23 paradas com foco visível; cenários 39 passos, distância máxima 16, Esc
devolve `aria-pressed="false"`. Scripts: `fontes/toque-alvos-ui.mjs` (o do QA com perfil próprio), `fontes/extra-v3.mjs`,
`fontes/teste-v2.mjs` (pinça corrigida). Não testado: aparelho de toque de verdade, leitor de tela.
