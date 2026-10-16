# Resultado da porta, volta 1

Maestro, 2026-10-15 ~12h20. Critério (`regua-da-cidade/como-julgar.md`): passa com R1 a R6 em "passa" e nenhuma
dimensão abaixo de 3, nos dois pareceres.

| Conceito | QA (medidas) | UX revisor | Tech lead | Resultado |
|---|---|---|---|---|
| A, Linhas do hub | tudo passa; folga 23,5 px, a mais justa | passa | volta: Nomes (R4) em falha | **volta** |
| B, Duas cidades e a estrada | tudo passa | passa | volta: Nomes (R4) em falha | **volta** |
| C, A cidade em corte | tudo passa | passa | volta: Nomes (R4) e Papel na cidade (R5) em falha | **volta** |

- O foco que o QA viu falhar por script aparece com Tab real nos três (contorno de 3,5 px, `:focus-visible`):
  não é falha. Lição para `medidas-da-peca`: o foco por `el.focus()` não aciona `:focus-visible`; o relatório deve
  dizer "não verificado", não "falha".
- Os três seguem para a volta 2 com os consertos dos dois pareceres. Nenhum é descartado: os de Nomes são só nos
  dados das fichas, e o de C tem conserto proposto pelo Tech lead (trocar a chave da altura ou descer o Conteúdo).
