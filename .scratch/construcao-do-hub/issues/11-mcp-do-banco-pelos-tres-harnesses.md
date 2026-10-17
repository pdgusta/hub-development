# 11: MCP do banco pelos três harnesses

Type: task
Status: claimed
Etapa: 3 (MCP do banco)
Blocked by: 10, 03

**What to build:** Claude Code, Codex e Copilot CLI, em modo não interativo e com a pasta de configuração de ensaio, usam o MCP do banco de verdade. Pergunta ao Gustavo na hora: login dos três harnesses na pasta de ensaio.

**Fonte:** Bloco do Worker 5, teste (9); tickets 36 e 41. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 10 (MCP do banco: três instâncias, cabeça, regra curta e estado), 03 (Prova: hooks do Codex em acesso total)

- [ ] os três harnesses citam o que receberam do servidor
- [ ] a requisição do Codex é capturada para ver onde o `instructions` chega
- [ ] no Copilot CLI, com e sem a opção que libera as instruções do MCP

## Comments
- 2026-10-16 20:24 (maestro): aval do Gustavo para copiar o login dos três harnesses em pasta de ensaio (rodada `2026-10-16-login-dos-harnesses-no-ensaio`, A, vale para a construção inteira); condições em `../etapas/regras-da-construcao.md`.

- 06:38 (maestro): passado ao Cinzel (o 10 foi juntado: hub 9cc878b, fork 34c3e50). A pergunta do login já está respondida: aval do Gustavo para a construção inteira (rodada `2026-10-16-login-dos-harnesses-no-ensaio`, nas regras). Harness real pela fila; Codex com cota desde 06:58.

- 2026-10-17 ~06h45 (Cinzel): peguei o 11 (`claimed`). Worktree `C:/context-hub-wt/ticket-11` de `integracao` 9cc878b. Costuras propostas ao maestro: `etapas/costuras-11-Cinzel.md`.

- 06:41 (maestro, mandato): costuras do Cinzel aceitas (`../etapas/costuras-11-Cinzel.md`). (1) fork em modo local (pasta), sem Docker: os critérios medem o que o servidor entrega ao harness, não o CouchDB; o caminho inteiro com banco cifrado fica para o 25. (2) aval para duas sessões do Copilot (com e sem `--allow-all-mcp-server-instructions`), modelo barato, nas condições do aval de login. (3) "regra seguida" e banco recriado ficam fora (não estão nos critérios); registrar no relatório como ressalva para o 25.

- 07:32 (maestro): lição do 15 (Trilho): no Codex, `mcp__hub-banco__...` chega ao hook como `mcp__hub_banco__...` (hífen vira sublinhado); confira nos matchers e no que o harness cita.
- 2026-10-17 07:45 (Cinzel): rodada 1 com harness real: Claude Code e Copilot (sem e com a opção) PASSA; o Codex falhou por erro do teste (conserto bfd1af3); rodada só do Codex na fila. Hub `ticket-11` bfd1af3.
- 2026-10-17 ~07h55 (Cinzel): Codex sem cota até 12h15 (maestro): fecho o que dá com Claude e Copilot. Hub `ticket-11` ab374b4 (com `integracao` e2b7607). Revisão pedida ao Fiel da parte fechada; o Codex roda depois de 12h15 (fila, item 4) e entra como rodada 2.
- 2026-10-17 07:55 (Cinzel): parecer da rodada 1 do Fiel: sem conserto (`../etapas/parecer-11-Cinzel.md`). Falta só a rodada 2, com o Codex, depois de 12h15. Ressalvas levadas ao maestro: Copilot sem a opção (requisito do kit 23); Claude adia as ferramentas MCP; lista de skills da máquina na evidência do Copilot.
