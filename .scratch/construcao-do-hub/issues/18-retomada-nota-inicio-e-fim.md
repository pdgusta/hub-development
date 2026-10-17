# 18: Retomada: nota de sete campos, início e fim

Type: task
Status: claimed
Etapa: 7 (retomada)
Blocked by: 04, 17, 03

**What to build:** A nota de retomada de sete campos por trabalho; no fim da resposta, o mod do Claude Code, o hook de fim do Codex e o do Copilot perguntam "a nota mudou?" e devolvem ao agente se não mudou; no início da sessão, a checagem abre a nota junto com o estado da vigia.

**Fonte:** Bloco do Worker 2; faixa 2 em `spec-partes/faixas-01-02.md`; tickets 10 e 14; escolha aceita 16 (regra fixa, sem IA). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 04 (Esqueleto do hub e hub de ensaio), 17 (Vigia nas telas dos harnesses), 03 (Prova: hooks do Codex em acesso total)

- [ ] numa sessão com a pasta de ensaio, o fim da resposta deixa a nota com os sete campos
- [ ] resposta que não mudou a nota é devolvida; a que mudou, solta
- [ ] a sessão seguinte começa com a nota no contexto, nos três harnesses

## Comments
- 2026-10-16 ~19h55 (maestro): **pergunta em aberto antes deste ticket.** O Gustavo levantou que vários agentes trabalham
  no mesmo trabalho (maestro, sessão sozinha, recrutas) e que nem uma nota para todos nem uma por agente fica bom.
  Proposta do maestro em `../rascunhos/retomada-com-varias-sessoes.md` (nota do trabalho só de quem conduz, mais uma
  passagem por sessão que não conduz). Decidir numa rodada antes de pegar este ticket.
- 2026-10-16 20:24 (maestro): aval do Gustavo para copiar o login dos três harnesses em pasta de ensaio (rodada `2026-10-16-login-dos-harnesses-no-ensaio`, A, vale para a construção inteira); condições em `../etapas/regras-da-construcao.md`.
- 2026-10-16 20:39 (maestro): proteção contra laço no fim da resposta decidida pelo Gustavo (rodada `2026-10-16-laco-no-fim-da-resposta`, B): devolve até três vezes seguidas; na quarta parada ainda com falta, solta e registra a falta no `estado.json` da vigia (início da próxima sessão e tela de estado).

- 07:28 (maestro, mandato): começa já com a Vela, num ramo ticket-18 da ponta de `integracao` com o `ticket-17` juntado por merge (o 17 está na revisão; o 18 usa o hook de início e o fim da resposta dela). Junção só depois do 17 (e do 16) resolvidos.
- 2026-10-17 07:30 (Vela): claimed; ramo ticket-18 (integracao 9cc878b + ticket-17 86c5a88). Costuras em ../etapas/costuras-18-Vela.md, com a pergunta das várias sessões (A recomendada: passagem do recruta em work/); esperando o maestro antes de codar.

- 07:31 (maestro, mandato; **muda o spec, para rever com o Gustavo**): várias sessões no mesmo trabalho: **A**. Quem conduz (sem `MAESTRI_TERMINAL_ID`, ou com `HUB_PAPEL=maestro`) mantém a `retomada.md` da iniciativa; cada recruta mantém a sua passagem em `<iniciativa>/work/passagem-<terminal>.md`; o início abre as duas. O spec dizia nota única; a mudança evita que sessões paralelas briguem pela mesma nota (é como esta construção já trabalha). Costuras aceitas (`../etapas/costuras-18-Vela.md`).
- 2026-10-17 07:49 (Vela): feitos ca2bb45..b291ca2 (fim devolve sem a nota; passagem do recruta em work/; sete campos; last_agent; aviso da memória do Claude); 18-retomada 8/8. Falta: início com a nota, AGENTS.md, ponta a ponta real, relatório, Fiel, Rebite. Retomada gravada antes do /clear.
- 2026-10-17 08:15 (Vela): feitos 8950ed7 (início com a nota), e4e3708 (AGENTS.md), 68bf70b (ponta a ponta real escrita); 18 + 17: 31/31. Relatório ../etapas/relatorio-18-retomada.md. Falta: real Claude e Copilot (fila, depois da Brasa), Codex depois das 12h15, Fiel, Rebite (junção depois do 17 e do 16).
- 2026-10-17 09:30 (Vela): rodada 1 do Fiel voltou (o fim cobrava a nota de quem não gravou); conserto e1c5eac, 69/69. Rodada 2 pedida; real de novo pela fila.

- 09:06 (maestro, mandato): ressalva 1 da rodada 2 (gravação pelo shell fora da lista do fim) aceita; a rede (mtime só no cwd, com aviso) vira o ticket 37.
