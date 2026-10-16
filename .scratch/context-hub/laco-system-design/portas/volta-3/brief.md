# Brief da porta, volta 3

Do maestro, 2026-10-15. Fase 3 do `orquestracao.md`, etapa 9. Peças: `conceitos/volta-3/` (`conceito-a.html`,
`conceito-b.html`, `conceito-c.html`, cada um com seu `.md` e a tabela de R5; `index.html` é só o seletor).

## Ordem

1. **QA tester** mede primeiro: `medidas-da-peca` em cada conceito (larguras 320, 768, 1280 e 1920), saída em
   `qa/volta-3/<conceito>/`, relatório em `qa/volta-3/relatorio.md`. Só mede e relata.
2. **UX revisor** e **Tech lead** julgam em paralelo, com o relatório do QA na mão, pelo roteiro de
   `regua-da-cidade/como-julgar.md`:
   - UX revisor: R1, R2, R3 e R6 sobre capturas próprias (1280 e 320) e as seis dimensões das críticas. Parecer em
     `portas/volta-3/ux-revisor.md`.
   - Tech lead: R4, R5 e R6 contra o `texto-do-hub.md` (rótulos, tabela de R5, agrupamentos, a busca como porta do
     conteúdo, itens "a decidir"). Parecer em `portas/volta-3/tech-lead.md`.

## Critério (decidido em `como-julgar.md`)

Um conceito passa com R1 a R6 em "passa" e nenhuma dimensão abaixo de 3. Cada parecer termina com, por conceito:
**passa** ou **volta**, e a lista de consertos numerada (o que, onde, por quê). Não escolha favorito: a escolha é do
Gustavo, na carta. Se um conceito for melhor numa dimensão, diga qual e por quê, sem ranking geral.

## O que muda nesta volta

- Cada juiz confere, primeiro, os consertos que pediu na volta 2 (`portas/volta-2/<seu parecer>.md`) contra
  `conceitos/volta-3/consertos.md` e a peça: feito, feito de outro jeito (aceita ou não) ou faltando.
- O QA usa a `medidas-da-peca` corrigida: foco de item com regra `:focus-visible` que não muda por script sai como "não
  verificado", não "falha".
- Problema novo que o conserto criou também entra.

## Volta 3, a penúltima

- Confira só os consertos que você pediu na volta 2 (`portas/volta-2/<seu parecer>.md`) contra
  `conceitos/volta-3/consertos.md` e a peça, e qualquer problema novo que eles criaram. Não reabra o que já passou.
- UX revisor: foco com Tab real nas 10 paradas de cada conceito, pessoas incluídas.
- Rótulos seguem no limite de 25.
