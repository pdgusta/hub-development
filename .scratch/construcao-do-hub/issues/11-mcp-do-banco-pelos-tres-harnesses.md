# 11: MCP do banco pelos três harnesses

Type: task
Status: ready-for-agent
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
