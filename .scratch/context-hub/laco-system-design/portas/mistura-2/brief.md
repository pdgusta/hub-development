# Brief da porta da mistura, volta 2

Do maestro, 2026-10-15. Peça: `conceitos/mistura/mistura.html` (volta 2), com `consertos.md` (uma linha por conserto
pedido na volta 1), `decisoes.md` (14 a 21 são desta volta) e a volta 1 guardada em `mistura-v1.html`. Contexto, ordem e
critério: os mesmos de `portas/mistura-1/brief.md` (leia se chegar sem memória). Resultado da volta 1:
`portas/mistura-1/resultado.md`.

## Ordem

1. **QA tester** mede de novo (larguras 320, 768, 1280, 1920 e os sete cenários), saída em `qa/mistura-2/`, relatório
   em `qa/mistura-2/relatorio.md`.
2. **UX revisor** e **Tech lead** julgam em paralelo, com o relatório do QA:
   - primeiro, cada um confere os consertos que pediu na volta 1 (`portas/mistura-1/<seu parecer>.md`) contra
     `conceitos/mistura/consertos.md` e a peça: feito, feito de outro jeito (aceita ou não) ou faltando;
   - depois, só problema novo que um conserto criou. Não reabra o que já passou.
   - UX revisor: foco com Tab real em todas as paradas e os sete cenários sem texto. Parecer em
     `portas/mistura-2/ux-revisor.md`.
   - Tech lead: R4, R5 e R6 contra a descrição v3.2. Parecer em `portas/mistura-2/tech-lead.md`.

Passa com R1 a R6 em "passa" e nenhuma dimensão abaixo de 3. Cada parecer termina com **passa** ou **volta** e os
consertos numerados. Esta é a volta 2 de 3.

Ao terminar, cada um avisa: `maestri ask "Claude Code" "pronto: <caminho>"`.
