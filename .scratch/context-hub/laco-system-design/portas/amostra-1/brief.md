# Brief da porta da amostra, volta 1 (fase 4, etapa 12)

Do maestro, 2026-10-15. Peça: `amostra/amostra.html`, com `amostra.md` (o que mudou em relação à mistura e como navegar)
e `decisoes.md`. Brief do UI engineer: `amostra/brief.md`.

## Contexto (para quem chega sem memória)

O Gustavo aprovou sem alteração a mistura (`conceitos/mistura/mistura.html`; portas em `portas/mistura-1` e
`portas/mistura-2`) e tirou o teto de 25 rótulos: pode haver mais, desde que a folga e a separação sigam sem poluição. A
amostra é a mistura como peça final, que com o aval dele substituirá o `system-design.html` (aberto num portal do
Maestri ao lado do terminal). Ele pediu para essa página um canvas de tela inteira sem rolagem: arrastar com o botão
direito, Ctrl + roda para zoom, Shift + roda para andar na horizontal, quase tudo estático e as fichas clicáveis.
Fonte do conteúdo: `descricao/descricao-do-hub.md` (v3.2).

## Ordem

1. **QA tester** testa primeiro, em `qa/amostra-1/`, relatório em `qa/amostra-1/relatorio.md`: `medidas-da-peca` nas
   larguras 320, 768, 1280 e 1920 (na vista inicial e num nível de zoom aproximado); os sete cenários; e a navegação do
   canvas (arrastar com o botão direito, Ctrl + roda, Shift + roda, o mesmo pelo teclado, nada de rolagem da página).
2. Em paralelo, com o relatório do QA:
   - **UX revisor:** R1, R2 (sem teto fixo: o critério agora é não poluir), R3 e R6, as seis dimensões, Tab real, os
     cenários sem texto e o conforto da navegação no canvas. Parecer em `portas/amostra-1/ux-revisor.md`.
   - **Tech lead:** R4, R5 e R6 contra a descrição v3.2; o que a mistura aprovada tinha e a amostra precisa manter.
     Parecer em `portas/amostra-1/tech-lead.md`.
   - **Prumo** (revisor de código): o `amostra.html` como código: estrutura, acessibilidade no código (papéis ARIA,
     teclado), eventos do canvas (roda, botão direito, toque), desempenho, nada externo (sem CDN nem rede), manutenção
     (dá para atualizar a peça quando um ticket for resolvido?). Parecer em `portas/amostra-1/prumo.md`.

Passa com os três aprovando (R1 a R6 em "passa", nenhuma dimensão abaixo de 3, e o Prumo sem bloqueio). Cada parecer
termina com **passa** ou **volta** e os consertos numerados. Até 3 voltas; ao bater o teto, o laço para e espera o
Gustavo.

Ao terminar, cada um avisa: `maestri ask "Claude Code" "pronto: <caminho>"`.
