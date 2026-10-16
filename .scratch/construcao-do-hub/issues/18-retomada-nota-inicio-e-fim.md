# 18: Retomada: nota de sete campos, início e fim

Type: task
Status: ready-for-agent
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
