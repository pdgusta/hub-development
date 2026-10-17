# Parecer do ticket 24 (Cinzel): kit de par ao vivo nos três harnesses

## Rodada 1 — 2026-10-17 ~11h (ramo ticket-24, 7d3753b, do ticket-23 f304e6c)

Veredito: **sem conserto próprio; aceite final pendente** do Codex (rodada 2, depois das 12h15) e do conserto 2 do
23 (o 24 herda o vermelho do detector do 29: `harness-real.test.mjs` 4/6 neste ramo). Fiel sozinho.

- Teste ponta a ponta lido: palavra sorteada só no `AGENTS.md` do hub de ensaio; harness aberto num repositório fora
  do hub, sem pasta-mãe com contrato; ferramentas negadas; casa como `USERPROFILE`/`HOME`; login copiado e apagado.
- Evidência: Claude e Copilot respondem `jacaranda-9889c5` sem ferramenta; no Claude, os servidores do hub vêm do
  `.claude.json` da casa e a skill de marca aparece no `init`. `apagado: true`, `pasta_apagada: true`. Sem segredo (o
  único casamento é o nome do arquivo `.copilot/hooks/gsd-session.json` nos hashes).
- Sem harness, o 24 aparece pulado.
