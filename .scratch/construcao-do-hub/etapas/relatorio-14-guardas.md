# Relatório do ticket 14: guardas de regravação e ficha (Trilho)

## Estado
- 2026-10-17: ticket pego (worktree `C:\context-hub-wt\ticket-14`, ramo `ticket-14`, de `integracao` 0d04985).
- Primeiro commit do ramo (3055de9), separado: **sai o `README.md` da raiz**. Decisão do ticket 12: a raiz tem só o
  `AGENTS.md` e as seis raízes; o README era o marcador do "Início do hub". O `verificar-hub` passa sem ele (só o aviso
  de `agents/blocks.md`, caminho sem tipo).

## Uso do login no ensaio (aval do Gustavo, rodada 2026-10-16-login-dos-harnesses-no-ensaio)
- 2026-10-16 23:28 (UTC): **rodada sem querer do Claude.** Para conferir a sintaxe do teste de ponta a ponta usei um
  `import()` do arquivo, e ele executou os testes. A rodada do Claude foi inteira, já com o aval: copiou
  `%USERPROFILE%\.claude\.credentials.json` para o `CLAUDE_CONFIG_DIR` de ensaio em `%TEMP%\hub-ensaio-14-*`, rodou
  uma sessão `claude -p` com haiku e apagou a pasta no `finally`. O processo acabou antes da rodada do Codex e antes do
  `after`, e por isso os hashes não foram gravados. Conferido depois: nenhuma cópia de login sobrou em
  `%TEMP%\hub-ensaio-14-*`. Resultado no registro da guarda: regravação de `context.md` recusada, troca de trecho
  passou, nota sem `status` recusada, nota certa passou.
