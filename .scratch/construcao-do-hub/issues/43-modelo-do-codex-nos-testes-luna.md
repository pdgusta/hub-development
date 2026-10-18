# 43: Os testes do Codex usam o gpt-6-luna por padrão

Type: task
Status: resolved
Etapa: infraestrutura de teste (fora da sequência)
Blocked by: 38

**What to build:** Regra nova do Gustavo (2026-10-17 ~14h35, `etapas/regras-da-construcao.md`): o Codex fica só para os
testes, com `gpt-6-luna` por padrão e `gpt-6.1-sol` só quando o teste é difícil para o Luna. Hoje
`agents/code/test/harness-real.mjs` fixa `MODELO_CODEX = 'gpt-6.1-sol'` (ticket 38) e o
`ponta-a-ponta/22-cliente.test.mjs` traz `'gpt-6.1-sol'` escrito à mão. Trocar a constante por
`process.env.HUB_MODELO_CODEX ?? 'gpt-6-luna'` e fazer todo teste que chama o Codex usar a constante (22-cliente
incluído; o 17-vigia-tela já usa luna à mão: passar à constante).

**Fonte:** pedido do Gustavo (chat do maestro, 2026-10-17 ~14h35).

**Blocked by:** 38 (resolvido)

- [ ] `MODELO_CODEX` vem de `HUB_MODELO_CODEX`, senão `gpt-6-luna`
- [ ] nenhum teste traz o nome do modelo do Codex escrito à mão (grep)
- [ ] testes leves verdes (sem rodar o Codex de verdade; a prova real vem nas rodadas de cada ticket)

## Comments

- 2026-10-17 ~14h40 (maestro, pedido do Gustavo): publicado. Dona: a Brasa (livre até a vez do Codex do 22). Pequeno; revisão curta do Fiel.
- 2026-10-17 ~14h55, Brasa: feito no ramo `ticket-43` (worktree `C:/context-hub-wt/ticket-43`). Constante por `HUB_MODELO_CODEX || 'gpt-6-luna'`; 17-vigia-tela e 22-cliente pela constante; grep limpo. Dois testes novos no detector do 29 (vermelho→verde); 12 passam, 2 pulados. Relatório `etapas/relatorio-43-modelo-do-codex-luna.md`. Fiel PASSA (parecer `etapas/parecer-43-Brasa.md`); levado ao Rebite ~15h05.
- 2026-10-17 15h22 (integrador, Rebite): juntado em `integracao`, commit 45e34c7 (merge `--no-ff` de `ticket-43` 32e8217, o HEAD do "passa" do Fiel). Testes: suíte `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis (e sem `HUB_MODELO_CODEX`), com a trava, em 98a7ced (41, 40, 43 e três junções dos docs do Lume): 289, 278 verdes, 10 pulados, 1 falha, `git status` limpo (log `etapas/juncao-docs-suite-falha-27.log`). A falha é do `27-pastas.test.mjs:247` pelo conteúdo de uma página dos docs (`agents/code/docs/componentes/mcp-do-banco.md:105`, o exemplo `[Open in Obsidian](...)` lido como link); não toca este ticket. Decisão do maestro (15h20): resolver; a docs fica pendente; a causa no verificador vira o ticket 44 (Brasa). Ressalvas do parecer: o detector olha só `.mjs` com `gpt-<dígito>` (não pega `.ps1`/`.json` nem nome montado; hoje nada disso existe); o `22-cliente` ganhou `model_reasoning_effort="low"`, e a prova real dele com o Luna vem na rodada do Codex do 22. **Resolvido.**
