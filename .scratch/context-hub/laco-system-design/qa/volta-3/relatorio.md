# Relatório do QA, volta 3 (fase 3, porta)

Medido em 2026-10-15 com `medidas-da-peca`, larguras 320, 768, 1280 e 1920. Só medi e relato; não editei nada.
Saída em `conceito-a\`, `conceito-b\`, `conceito-c\`.

**Modo:** marcado nos três (15 itens, 8 grupos, 1 ponto de encontro; 11 ligações em A e C, 10 em B). Nada adivinhado.

## Resumo (1280 px, visão geral) e comparação com a volta 2

| Medida (limiar) | A volta 3 (volta 2) | B volta 3 (volta 2) | C volta 3 (volta 2) |
|---|---|---|---|
| R1 cruzamentos (0) | 0 passa (0) | 0 passa (0) | 0 passa (0) |
| R2 rótulos no desenho (máx. 25) | 25 passa, no limite (25) | 25 passa, no limite (25) | 25 passa, no limite (25) |
| R3 folga mínima (>= 21 px) | 29,5 px passa (29,5) | 29,1 px passa (29,1) | 28,9 px passa (28,9) |
| R3 pares abaixo de 1 rótulo | 0 passa (0) | 0 passa (0) | 0 passa (0) |
| R3 razão entre grupos / dentro (>= 1,5) | 1,96 passa (2,05) | 2,23 passa (2,03) | **1,69** passa (1,76) |
| Contraste | 36 de 36 passa (36) | 36 de 36 passa (36) | 36 de 36 passa (36) |
| Item focável sem nome | 0 passa (0) | 0 passa (0) | 0 passa (0) |
| tabindex positivo | 0 passa (0) | 0 passa (0) | 0 passa (0) |
| Foco muda ao focar (script) | 0 de 10, **não verificado** (idem) | idem | idem |
| Links quebrados | 0, sem links no HTML (0) | 0 (0) | 0 (0) |
| Rolagem horizontal 320 a 1920 | não passa (não) | não passa (não) | não passa (não) |
| Documento | 30,5 KB (30,2) | 33,7 KB (32,0) | 30,6 KB (30,3) |
| Carga, tempo virtual | 116 ms (65) | 158 ms (66) | 96 ms (109) |
| Códigos internos soltos | 0 (0) | 0 (0) | 0 (0) |

## Por largura (folga mínima px / razão entre grupos / rótulos)

| Largura | A | B | C |
|---|---|---|---|
| 320 | 21,8 / 2,00 / 25 | 21,0 / 2,25 / 25 | 21,0 / 1,67 / 25 |
| 768 | 17,6 / 2,02 / 25 | 17,6 / 2,24 / 25 | 17,2 / 1,69 / 25 |
| 1280 | 29,5 / 1,96 / 25 | 29,1 / 2,23 / 25 | 28,9 / 1,69 / 25 |
| 1920 | 29,5 / 1,96 / 25 | 29,1 / 2,23 / 25 | 28,9 / 1,69 / 25 |

Altura do rótulo: 15 px em 320, 12 px em 768, 21 px de 1280 em diante; a folga fica acima dela em todas as
larguras. 0 cruzamentos, 0 pares abaixo do limiar e 0 falhas de contraste em todas.

## O que mudou da volta 2

- Folga mínima e rótulos: iguais nos três (25 continua no limite exato; um rótulo a mais falha).
- **Razão entre grupos:** A caiu de 2,05 para 1,96; B subiu de 2,03 para 2,23; **C caiu de 1,76 para 1,69**. C é
  o que tem menos margem sobre 1,5 (queda em duas voltas seguidas: 1,85, 1,76, 1,69).
- Peso: +0,2 a +1,6 KB. Nada externo.
- Carga virtual: subiu em A (65 para 116 ms) e B (66 para 158 ms), caiu em C (109 para 96). Só serve para comparar;
  B é o mais lento, ainda sem relevância.

## Foco

- Pelo script: 0 de 10 itens mudam ao focar nos três; a ordem do Tab tem as mesmas 10 paradas (7 bairros e 3
  pessoas), todas com nome ("Abrir a ficha: …"), nenhum tabindex positivo.
- O CSS dos três tem `.bairro:focus-visible .zona` e `.pessoa:focus-visible .anel` (regra posta no filho).
- **Aviso ao maestro:** o código do `medir.js` já tem a correção do filho (suite e cópia minha, 12:20), mas rodando
  hoje o resultado saiu `regra_de_foco_no_css: false` e `nao_verificado_focus_visible: 0` nos 10 itens, e os 10 caíram
  em `sem_mudanca_ao_focar`. Ou seja, **o campo do JSON ainda diz "sem mudança" mesmo com a regra existir**. Não
  consegui explicar o porquê sem mexer na skill, e não mexo.
- **Minha leitura:** "não verificado", não "falha". A regra existe e o foco por script não aciona `:focus-visible`.
  Quem decide é o Tab real do UX revisor. Quem só olhar o campo `sem_mudanca_ao_focar` vai ler 10 falhas por engano.

## Não verificado

- Foco visível ao Tab real; olho apertado de R2; abrir e fechar a ficha e Esc; passar o mouse.
- Links: não há `<a>` no HTML; links montados por JavaScript não entram em `links.json`.
- break-ui (dados extremos): não pedido nesta etapa.
- Conferir os consertos da volta 2 é dos juízes; só medi números.

## Arquivos

`conceito-a\`, `conceito-b\`, `conceito-c\`: `medidas-320|768|1280|1920.json`, `captura-<largura>.png`,
`links.json`, `resumo.txt`.
