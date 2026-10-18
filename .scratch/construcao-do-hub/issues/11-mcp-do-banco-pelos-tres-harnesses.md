# 11: MCP do banco pelos três harnesses

Type: task
Status: resolved
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
- 2026-10-17 14:58 (Cinzel): rodada 2, só o Codex (0.162.1, gpt-6-luna pela regra nova), 14:47 a 14:54 com a trava: PASSA (log `../etapas/logs/11-harness-3.log`, evidência e96cd70). Cita A, B e C. Captura: as instruções do MCP não vão ao primeiro pedido; chegam só na saída da ferramenta com que o modelo lista as ferramentas, à frente da descrição de cada uma. integracao d298826 juntada (e63d951), 4/4 + 1 pulado. Rodada 2 pedida ao Fiel.
- 2026-10-17 15:10 (Cinzel): r2 do Fiel VOLTOU por conserto mecânico (modelo à mão; detector do 43). Conserto 28782df: o aceite usa MODELO_CODEX; harness-real + 11: 12 passam, 1 pulado. A junção anterior (e63d951) era da integracao 98a7ced, não d298826. Rodada curta pedida.
- 2026-10-17 16h16 (integrador, Rebite): juntado em `integracao`, commit 51fa382 (merge `--no-ff` de `ticket-11` 28782df, o HEAD da rodada 3 "passa" em acordo do Fiel; árvore juntada igual à do ramo; o fork não muda: `ticket-11` do fork = 34c3e50 = `integracao` do fork). Testes: suíte `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis, com a trava, em a7d1517 (11 e docs): 294, 282 verdes, 12 pulados, 0 falhas, `git status` limpo (log `etapas/logs/juncao-11-docs-suite.log`). Harness real não repetido: arquivos idênticos aos revisados; o Codex de verdade passou com o Cinzel (`etapas/logs/11-harness-3.log`). Ressalvas do parecer: (1) o Copilot sem a opção não põe as instruções do servidor no prompt: a cabeça só chega se o kit (23) ligar `--allow-all-mcp-server-instructions` ou listar o `hub-banco` (requisito do kit); (2) o Claude Code adia as ferramentas MCP, e a regra curta do `write_note` só chega quando o modelo procura a ferramenta; (3) para o 25: regra seguida, banco recriado no meio da sessão, banco cifrado pelos harnesses; (4) a evidência do Copilot traz a lista de skills de `%USERPROFILE%\.agents\skills` da máquina (não é segredo, mas é ambiente pessoal no repositório); a captura mostra as instruções só em volta da `delete_note`. **Resolvido.**
