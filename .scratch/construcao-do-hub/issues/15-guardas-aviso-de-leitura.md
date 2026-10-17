# 15: Guardas: aviso de leitura fora da busca

Type: task
Status: claimed
Etapa: 5 (guardas no disco)
Blocked by: 14, 12

**What to build:** O aviso, sem recusa, quando o agente lê um arquivo grande sem ter buscado antes: guarda por sessão o que a busca devolveu e o que foi aberto.

**Fonte:** Bloco do Worker 6, item (c); ticket 11, rodadas 3 e 4. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 14 (Guardas: regravação inteira e ficha fora do esquema), 12 (Busca local com aceite)

- [ ] ler arquivo grande sem busca antes dá um aviso, uma vez por arquivo por sessão
- [ ] ler o trecho que a busca apontou não avisa

## Comments
- 2026-10-16 ~23h15 (maestro): passado ao Trilho depois do 12 (juntado c5b946a); bloqueios 14 e 12 resolvidos. Às 01:40 ele pausa para o aceite do Codex do 12.
- 2026-10-16 ~23h25 (Trilho): pego (`claimed`). Worktree `C:/context-hub-wt/ticket-15`, ramo `ticket-15`, de `integracao` c5b946a. Às 01:40 pausa para o Codex do 12.
- 2026-10-16 ~23h25 (maestro): costuras do Trilho aceitas; 'grande' medido no vault antigo (só tamanhos, números agregados no relatório, sem caminho nem nome), como pede a user story 29 da faixa 6.
- 2026-10-16 ~23h40 (Trilho): costuras aceitas pelo maestro. Medida de 'grande' (vault antigo, só tamanhos, só agregados; .md fora de pastas com ponto): 737 notas; bytes p50 6278, p75 14625, p90 40097, p95 84456, p99 185935, maior 347820; linhas p50 74, p75 167, p90 359, p95 654, p99 1245, maior 3016. Acima de 8 KB: 41% das notas, 89% dos bytes; 16 KB: 23%/77%; 20 KB: 19%/72%; 32 KB: 12%/63%; 40 KB: 10%/58%. Proposta: 20 000 bytes (HUB_LEITURA_GRANDE).
- 2026-10-16 ~23h55 (Trilho): desenho: hook DEPOIS da ferramenta nos três (o preToolUse do Copilot não injeta contexto e recusa se o hook falhar; o PostToolUse dos três aceita additionalContext; doc em etapas/doc-15/). Peça agents/code/hooks/leitura/ (depois-da-ferramenta.mjs + leitura.mjs), estado por sessão em .local/leitura/. Claude: 5 testes verdes em agents/code/test/15-leitura.test.mjs (commit 1ffde0a). Falta: fora do hub, Copilot (view, hub-busca-search), Codex (MCP e leitura por Bash), fragmentos, ponta a ponta real, relatório.
