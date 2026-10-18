---
name: rodada-explicacao-acima-das-perguntas
description: "No .md da rodada, a explicação vai no contexto acima do primeiro ##; texto entre o cabeçalho da pergunta e as opções quebra o leitor do portal"
metadata:
  type: feedback
---
O leitor do portal (`portal/nucleo/leitores.py`, `_parse_perguntas`) espera as opções `- A: ...` logo depois de
`id:`/`tipo:`/`recomendada:`. Em 2026-10-16 a rodada `ticket-05-perguntas-do-trilho` levou parágrafos, lista e tabela
entre o cabeçalho e as opções, e o portal mostrou "rodada malformada: pergunta ... do tipo escolha sem opções".

**Why:** o Gustavo viu o erro no portal e teve de avisar; a rodada ficou inutilizável até o conserto.

**How to apply:** pôr toda explicação (numerada por pergunta, se preciso) no contexto acima da primeira `##`; dentro de
cada pergunta, só os campos e as opções. Antes de avisar "pergunta nova no portal", validar com
`python -I -c` chamando `leitores._parse_perguntas` sobre o corpo. Ver [[rodada-no-portal-o-essencial-na-opcao]], [[portal-do-projeto]].
