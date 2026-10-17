# Ticket 15 — Trilho — parecer independente do Fielzinho

2026-10-17. Rodada pedida sobre 3d34bd1 (ponta conferida), com foco na seção Rodada de 2026-10-17. Worktree limpa. Li código/adaptadores, fragmento Codex, testes local e real, relatório, ticket, spec Worker 6 e decisão 11 (rodadas 3/4). Não li parecer do Fiel desta rodada.

## Veredito

**PASSA esta rodada.** Sem consertos novos bloqueantes. Matcher e adaptador do Codex concordam em mcp__hub_busca__search; o teste reproduz esse nome. A sandbox foi ajustada apenas no HOME de ensaio. O teste Claude junta o deny da read do MCP com o hook de leitura.

## Evidência

- Execução própria: `node --test agents/code/test/15-leitura.test.mjs`: 9/9, saída 0. Avisos sem recusa, uma vez por arquivo/sessão, trecho apontado calado e registro por leitura.
- `git diff --check 9cc878b..HEAD`: saída 0.
- Li os registros reais versionados dos três em evidencia-15: A sem busca recebe busque antes; B apontado/trecho fica calado; C apontado/inteiro recebe leia o trecho; repetição de A fica calada. No Codex são quatro leituras na mesma sessão. Log etapas/logs/trilho-15-codex.log termina 1 teste aprovado, nenhuma falha.
- hashes-codex.json registra apagado=true e configurações comparadas iguais; .claude.json diverge e está explicitamente fora da asserção. São evidências do construtor; não rodei harness real nem copiei login.

## Ressalvas preservadas

A leitura por shell é reconhecimento parcial, conforme contrato: comando composto com filtro pode classificar outra leitura inteira como trecho. O estado por sessão não tem limpeza automática. O aviso ainda alcança caminhos que a busca não indexa, e HUB_LEITURA_GRANDE inválido pode calá-lo. Esses limites já constam do relatório/ticket resolvido; não são regressões desta rodada. O teste real checa a entrega do aviso ao modelo explicitamente só no Claude; nos demais, a evidência central é o registro do hook. A leitura foi aceita e não houve recusa nos casos demonstrados.

Fiel fecha a rodada. Nenhuma alteração em código/spec/ticket; sem subagentes.
