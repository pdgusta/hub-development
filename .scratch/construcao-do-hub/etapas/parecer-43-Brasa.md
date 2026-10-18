# Parecer do ticket 43 (Brasa): os testes do Codex usam o gpt-6-luna por padrão

## Rodada 1 (curta) — 2026-10-17 ~15h10 (Fiel + 2ª leitura por subagente Sonnet 5.5, regra nova)

Ramo `ticket-43`, 32e8217 (de `integracao` d298826). **Veredito: PASSA**, sem conserto.

- Critério 1: `harness-real.mjs:9`, `HUB_MODELO_CODEX || 'gpt-6-luna'`; teste novo cobre sem e com a variável.
  `gpt-6-luna` existe no `models_cache.json` do Codex.
- Critério 2: todo `codex exec` de `agents/code/test` passa `-m MODELO_CODEX` (ponta a ponta 12, 14, 15, 17, 19, 20,
  22, 27 e prova 03); nenhum `.ps1` chama o Codex. Grep sem nome à mão.
- Critério 3: Fiel 12 passam, 2 pulados (harness-real, 22-kit-cliente, ponta a ponta 17 e 22); `git status` limpo.
- 2ª leitura (`parecer-43-Brasa-segunda-leitura.md`): PASSA; `merge-tree` com a integracao limpo.

Ressalvas (em acordo, não pedem conserto):
1. O detector olha só `.mjs` com `gpt-<dígito>`: não pega `.ps1`/`.json` nem nome montado. Hoje nada disso existe.
2. O 22-cliente ganhou `model_reasoning_effort="low"` (o relatório já diz); a prova real dele com o Luna vem na rodada
   do Codex do 22.
