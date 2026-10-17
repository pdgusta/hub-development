# 30: O montador do hub de ensaio mostra a falha do git

Type: task
Status: claimed
Etapa: infraestrutura de teste (fora da sequência)
Blocked by: None (can start immediately)

**What to build:** Quando um comando git do `agents/code/test/hub-de-ensaio/montar.mjs` falha (ou o processo nem abre), o montador diz qual comando falhou e mostra o stdout, o stderr e o erro do processo; hoje ele só imprime o stderr e sai 1 calado. Os testes que chamam o montador (o do 27 primeiro) mostram o stdout dele quando ele falha. Objetivo: explicar o vermelho intermitente que o Rebite viu na junção do 20 (27-pastas, "o montador saiu 1 sem stderr").

**Fonte:** Proposta da Vela (retomada `../etapas/retomada-Vela.md`); log da junção do 20 em `../etapas/juncao-*-suite-falha-*.log`. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** None (can start immediately)

- [ ] com um git que falha (por exemplo, um diretório que não é repositório ou um comando inválido forçado no teste), o montador sai diferente de 0 e a saída nomeia o comando e traz stdout, stderr e erro
- [ ] o teste do 27 mostra a saída inteira do montador quando ele falha
- [ ] a suíte segue verde

## Comments

- 2026-10-17 ~00h05 (maestro): publicado pela proposta da Vela, que o faz.
- 2026-10-17 ~00h15 (maestro): a Vela achou datas fixas (`updated: 2026-10-16`) em dois testes do 05 que viraram vermelhos à meia-noite; conserto no 30, commit separado, só no teste, com aval do maestro; Trilho avisado.
- 2026-10-17 ~00h40 (Vela): claimed; worktree C:/context-hub-wt/ticket-30 de integracao f83c8f5. c52ccc1 montador nomeia o comando e mostra stdout/stderr/erro (2 testes no 04-esqueleto); 03cbbb6 as 17 asserções do montador mostram stdout+stderr; ca5b389 bomba de data no 05-frontmatter (aval do maestro). Relatório etapas/relatorio-30-montador-mostra-falha.md. Falta: suíte, revisão do Fiel, Rebite.
