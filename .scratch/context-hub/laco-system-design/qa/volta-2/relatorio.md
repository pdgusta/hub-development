# Relatório do QA, volta 2 (fase 3, porta)

Medido em 2026-10-15 com `medidas-da-peca` corrigida (a cópia da suite e a minha são idênticas), larguras 320, 768,
1280 e 1920. Só medi e relato; não editei nada. Saída em `conceito-a\`, `conceito-b\`, `conceito-c\`.

**Modo:** marcado nos três (15 itens, 8 grupos, 1 ponto de encontro; 11 ligações em A e C, 10 em B). Nada adivinhado.

## Resumo (1280 px, visão geral) e comparação com a volta 1

| Medida (limiar) | A volta 2 (volta 1) | B volta 2 (volta 1) | C volta 2 (volta 1) |
|---|---|---|---|
| R1 cruzamentos (0) | 0 passa (0) | 0 passa (0) | 0 passa (0) |
| R2 rótulos no desenho (máx. 25) | **25** passa, no limite (23) | **25** passa, no limite (23) | **25** passa, no limite (23) |
| R3 folga mínima (>= 21 px) | 29,5 px passa (23,5) | 29,1 px passa (29,1) | 28,9 px passa (34,1) |
| R3 pares abaixo de 1 rótulo | 0 passa (0) | 0 passa (0) | 0 passa (0) |
| R3 razão entre grupos / dentro (>= 1,5) | 2,05 passa (1,81) | 2,03 passa (1,80) | 1,76 passa (1,85) |
| Contraste | 36 de 36 passa (34 de 34) | 36 de 36 passa (34 de 34) | 36 de 36 passa (34 de 34) |
| Item focável sem nome | 0 passa (0) | 0 passa (0) | 0 passa (0) |
| tabindex positivo | 0 passa (0) | 0 passa (0) | 0 passa (0) |
| Foco muda ao focar (script) | 0 de 10, **não verificado** (0 de 10, falha) | idem | idem |
| Links quebrados | 0, sem links no HTML (0) | 0 (0) | 0 (0) |
| Rolagem horizontal 320 a 1920 | não passa (não) | não passa (não) | não passa (não) |
| Texto visível na 1ª tela (desenho + HTML) | 36 (34) | 36 (34) | 36 (34) |
| Documento | 30,2 KB (24,4) | 32,0 KB (25,9) | 30,3 KB (25,1) |
| Carga, tempo virtual | 65 ms (73) | 66 ms (62) | 109 ms (36) |
| Códigos internos soltos | 0 (0) | 0 (0) | 0 (0) |

## Por largura (folga mínima px / razão entre grupos)

| Largura | A | B | C |
|---|---|---|---|
| 320 | 21,8 / 2,09 | 21,0 / 2,03 | 21,0 / 1,78 |
| 768 | 17,6 / 2,11 | 17,6 / 2,05 | 17,2 / 1,80 |
| 1280 | 29,5 / 2,05 | 29,1 / 2,03 | 28,9 / 1,76 |
| 1920 | 29,5 / 2,05 | 29,1 / 2,03 | 28,9 / 1,76 |

Altura do rótulo: 15 px em 320, 12 px em 768, 21 px de 1280 em diante. Folga acima da altura em todas as larguras
(320: 21,0 a 21,8 contra 15; 768: 17,2 a 17,6 contra 12). 0 cruzamentos, 0 pares abaixo do limiar, 0 falhas de
contraste em todas.

## O que mudou da volta 1

- **R2 subiu de 23 para 25 rótulos** nos três: é exatamente o limite. Passa, mas sem folga; qualquer rótulo a mais
  falha. Os rótulos novos são os das legendas das linhas dentro do desenho (buscar, gravar etc.) e a legenda curta
  "cada bairro abre uma ficha".
- **R3 razão entre grupos** subiu em A (1,81 para 2,05) e B (1,80 para 2,03); **caiu em C** (1,85 para 1,76), ainda
  acima de 1,5.
- **R3 folga mínima** subiu em A (+6 px), igual em B, caiu em C (34,1 para 28,9). Todas acima de 21 px. A mais
  apertada: Camada de busca e Porta do banco em C, 28,9 px.
- **Peso** subiu uns 5 a 7 KB por conceito (o sinal de abrir ficha). Nada externo.
- **Carga** de C foi de 36 para 109 ms em tempo virtual; serve só para comparar, ainda é pequeno.

## Foco (a pendência da volta 1)

A medição por script não viu mudança em 0 dos 10 itens focáveis nos três. Pela regra desta volta isso deveria
sair "não verificado", não "falha", se há regra de foco no CSS. O CSS tem: `.bairro:focus-visible .zona` (contorno
do bairro escurece, traço 3,5) e `.pessoa:focus-visible .corpo`, nos três arquivos. Mas a medição marcou
`regra_de_foco_no_css: false` e `nao_verificado_focus_visible: 0`: ela só procura regra no próprio elemento
focável, não nas partes dentro dele. Resultado:

- **Falha: não afirmo.** A regra existe e muda o desenho de dentro do item.
- **Passa: também não afirmo.** O foco por script não aciona `:focus-visible`; ninguém apertou Tab de verdade.
- Situação: **não verificado**; precisa de Tab real na captura (UX revisor). Aviso ao maestro: a `medidas-da-peca`
  corrigida ainda não reconhece regra de foco que atua em elemento filho; vale ajustar para a volta seguinte.

## Não verificado

- Foco visível ao Tab real (acima); olho apertado de R2; abrir e fechar a ficha e Esc; passar o mouse.
- Links: não há `<a>` no HTML; links montados por JavaScript não entram em `links.json`.
- break-ui (dados extremos): não pedido nesta etapa.
- Os consertos da volta 1 (`consertos.md`) não foram conferidos por mim: isso é dos juízes; só medi os números.

## Arquivos

`conceito-a\`, `conceito-b\`, `conceito-c\`: `medidas-320|768|1280|1920.json`, `captura-<largura>.png`,
`links.json`, `resumo.txt`.
