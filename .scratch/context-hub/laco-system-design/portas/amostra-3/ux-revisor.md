# Parecer do UX revisor, porta da amostra, volta 3 (a última)

2026-10-15. Peça: `amostra/amostra.html` (volta 3). Pelo brief, só os dois menores do meu parecer da volta 2
(`portas/amostra-2/ux-revisor.md`) e problema novo. Conferi também, com entrada real, o conserto que eu tinha
recomendado (o arrasto com um dedo) e que o mouse não regrediu. Relatório do QA: `qa/amostra-3/relatorio.md`.

## Arquivos ao lado deste parecer

`ux-captura-1280x1000.png`, `ux-captura-1280x720.png`, `ux-captura-960x800.png`, `ux-captura-320x640.png`,
`ux-1280x720-cenario.png`, `ux-1280x720-legenda.png`, `ux-960-fileira-meio.png`, `ux-960-fileira-fim.png`,
`ux-960-tab-ultimo-cenario.png`.

## Conferência

| Conserto | Situação | Como conferi | Aceito? |
|---|---|---|---|
| Volta 2, 1: arrasto com um dedo (recomendado) | feito | toque pelo protocolo do Edge, 12 passos, pedido de -96 x -48 px: o Banco local andou -96 x -48, sem ficha aberta (era 8 x 4) | sim |
| Volta 2, 2: cabeçalho a 1280 x 720 | feito: a legenda recolhe também abaixo de 800 px de altura | o desenho começa a 139 px do topo (era 185); a ajuda do mouse segue visível; o nome "Gustavo" fica livre dos botões de zoom (`ux-captura-1280x720.png`). Com "Legenda" aberta, o topo volta a 185 px, o que é o esperado | sim |
| Volta 2, 3: fileira de cenários a 960 cortada sem aviso | feito: a borda esmaece do lado em que há mais botões | no começo, a direita esmaece; rolada até o meio, as duas bordas; no fim, a esquerda (`ux-960-fileira-meio.png`, `ux-960-fileira-fim.png`). O botão focado pelo Tab rola para a vista | sim |

Regressão, de passagem: três arrastos seguidos com o botão direito a 1280 x 1000 andam exatamente o pedido, sem salto no
aperto (0 px). O QA cobriu o resto (zoom, roda, `+` e `−`, Tab 23 de 23, sete cenários, medidas iguais).

## Problemas novos

Nenhum. A observação do QA sobre o toque logo depois de um arrasto (às vezes o emulador não gera o clique com menos de
200 ms) aparece também na volta 2 e não muda a peça. Fica para conferir num aparelho de verdade.

## Regras e notas

R1, R2, R3 e R6 seguem em "passa"; a planta não mudou (QA: 0 cruzamentos, folga mínima de 22,3 px, razão de 1,53).
R4 e R5 não são do meu papel.

| # | Dimensão | Nota | Volta 2 | Por quê |
|---|---|---|---|---|
| 1 | Linhas (R1) | 5 | 5 | |
| 2 | Vista de cima (R2) | 5 | 5 | |
| 3 | Respiro (R3) | 4 | 4 | razão de 1,53, perto do limiar |
| 6 | Forma nova (R6) | 5 | 5 | |
| 7 | Hierarquia visual | 5 | 5 | |
| 8 | Composição | 5 | 4 | a 1280 x 720 o cabeçalho deixou de comer um quarto da altura |
| 9 | Densidade | 3 | 3 | a 1280 x 1000 o cabeçalho segue com a legenda inteira à vista; é o desenho aprovado |
| 10 | Affordance (conforto do canvas) | 4 | 3 | mouse, teclado e toque fazem o que prometem; a fileira avisa que rola |
| 11 | Cor | 4 | 4 | |
| 12 | Tipografia | 4 | 4 | |

## Veredito: **passa** (na minha parte)

Sem consertos pendentes da minha parte.

## Não verificado

- Aparelho de toque de verdade, mouse e roda físicos, leitor de tela.
- O conteúdo (é do Tech lead) e o código (é do Prumo).
