# Registro de junções em `integracao`

- 2026-10-16 ~20h55, ticket 04, b68f540, 11 testes do esqueleto verdes (maestro).
- 2026-10-16 ~21h20, ticket 03, 3857c98, 11 do esqueleto verdes; prova do Codex não repetida, árvore idêntica à revisada (maestro).
- 2026-10-16 20h00, ticket 02, c8d2267, 14 verdes (11 do esqueleto + 3 do instalador do 03); provas 02 (Docker) e 03 (codex) não repetidas, árvores idênticas às revisadas (Rebite).
- 2026-10-16 20h11, ticket 05, 0d04985, 37 verdes (34 do agents/code/test + 3 do instalador do 03); prova 02 e prova 03 não repetidas, árvores idênticas às revisadas (Rebite).
- 2026-10-16 20h28, ticket 01, 45ec3b0, 37 verdes (34 do agents/code/test + 3 do instalador do 03); provas 01, 02 e 03 não repetidas, árvores idênticas às revisadas (Rebite).
- 2026-10-16 20h32, ticket 06, 8b9beef, 44 verdes (agents/code/test, gerar-exclusoes, instalador do 03); sincronizador.ps1 e provas 01/02/03 não repetidos, árvores idênticas às revisadas (Rebite).
- 2026-10-16 21h03, ticket 14, 8d1d785, 81 verdes (agents/code/test, gerar-exclusoes, instalador do 03); ponta a ponta dos três harnesses e provas não repetidas, árvores idênticas às revisadas (Rebite).
- 2026-10-16 21h51, ticket 27, 0a8e17f, 106 verdes sem harness (agents/code/test/*.test.mjs e gerar-exclusoes); ponta a ponta dos três fora (regra provisória até o 29) e árvore idêntica à revisada (Rebite).
- 2026-10-16 22h02, ticket 29, d5e4e16, suíte inteira sem HUB_HARNESS_REAL: 116, 112 verdes, 4 pulados (harness real), git limpo; harness real não repetido, árvore idêntica à revisada (Rebite).
- 2026-10-16 22h28, ticket 19, dc56d47, suíte sem variável: 133, 128 verdes, 5 pulados (2ª rodada; a 1ª teve 1 falha intermitente no 05-frontmatter, que passou sozinho e na repetição); harness real não repetido, árvore idêntica à revisada (Rebite).
- 2026-10-16 23h10, ticket 12, c5b946a, suíte sem variável: 147, 141 verdes, 6 pulados, git limpo; harness real não repetido, árvore idêntica à revisada; aceite real do Codex pendente (Rebite).
- 2026-10-16 23h47, ticket 15, ac1cd2c, suíte sem variável: 157, 150 verdes, 7 pulados (2ª rodada; a 1ª teve 1 falha de tempo no 12-busca, log etapas/juncao-15-suite-falha-12.log); harness real não repetido, árvore idêntica à revisada; aceite real do Codex pendente (Rebite).
- 2026-10-17 00h01, ticket 20, f83c8f5, suíte sem variável: 174, 166 verdes, 8 pulados (2ª rodada; a 1ª teve 1 falha intermitente no 27-pastas, montador saiu 1 sem stderr, log etapas/juncao-20-suite-falha-27.log); harness real não repetido; prova real do Codex pendente (Rebite).
- 2026-10-17 00h35, conferência do 15 e do 20 pela regra nova (sobre f83c8f5): 12-busca sozinho 3 verdes; suíte com --test-concurrency=1 interrompida por memória crítica (99 verdes, 3 vermelhos: 2 do 05 pela bomba de data, consertada no 30, e 1 do 12 por lentidão); junções mantidas por ordem do maestro; repetir depois do 30, com a trava. Log etapas/juncao-15-20-suite-c1.log (Rebite).
- 2026-10-17 00h53, ticket 30, 5d84d76, suíte com --test-concurrency=1 e trava: 176, 168 verdes, 8 pulados, 0 falhas, git limpo; fecha a conferência do 15 e do 20 (Rebite).
