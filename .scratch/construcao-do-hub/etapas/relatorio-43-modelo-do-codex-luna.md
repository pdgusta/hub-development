# Relatório do ticket 43: os testes do Codex usam o gpt-6-luna por padrão

Brasa, 2026-10-17. Ramo `ticket-43`, worktree `C:/context-hub-wt/ticket-43`, de `integracao` d298826. Ponta 32e8217.

## O que mudou

- `agents/code/test/harness-real.mjs`: `MODELO_CODEX = process.env.HUB_MODELO_CODEX || 'gpt-6-luna'`. Uso `||` e não
  `??`: uma variável vazia também cai no Luna.
- `ponta-a-ponta/17-vigia-tela.test.mjs` e `ponta-a-ponta/22-cliente.test.mjs` passam a usar a constante. O 22-cliente
  ganha também `model_reasoning_effort="low"`, como os outros.
- `22-kit-cliente.test.mjs`: o `model = "gpt-6-luna"` do `config.toml` de ensaio (só um dado do usuário, nada roda)
  vira `model = "o-do-usuario"`, para o grep ficar limpo.
- Para o Sol num teste difícil: `HUB_MODELO_CODEX=gpt-6.1-sol` no ambiente do `node --test`.

## Testes (no `harness-real.test.mjs`, o detector do 29)

- `o modelo do Codex nos testes é o gpt-6-luna, salvo HUB_MODELO_CODEX`: importa o módulo num processo sem a
  variável (Luna) e com ela (Sol). Vermelho antes (dava o Sol).
- `nenhum teste escreve o modelo do Codex à mão`: varre os `.mjs` de `agents/code/test` (fora as evidências e o
  próprio `harness-real.mjs`) atrás de `gpt-<dígito>`. Vermelho antes (17-vigia-tela, 22-cliente, 22-kit-cliente).
- `node --test harness-real.test.mjs 22-kit-cliente.test.mjs ponta-a-ponta/17-vigia-tela.test.mjs
  ponta-a-ponta/22-cliente.test.mjs`: 12 passam, 2 pulados (os ponta a ponta, sem `HUB_HARNESS_REAL`). O Codex de
  verdade não rodou: a prova real vem nas rodadas de cada ticket.
