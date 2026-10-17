# 43: Os testes do Codex usam o gpt-6-luna por padrão

Type: task
Status: ready-for-agent
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
