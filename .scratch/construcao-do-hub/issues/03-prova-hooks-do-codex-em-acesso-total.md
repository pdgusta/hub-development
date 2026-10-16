# 03: Prova: hooks do Codex em acesso total

Type: task
Status: resolved
Etapa: 0 (provas de risco)
Blocked by: None (can start immediately)

**What to build:** Os hooks do Codex no modo de acesso total decidido em "Acesso dos agentes", com a pasta de configuração de ensaio. Aval do Gustavo (rodada `2026-10-16-etapa-0-receita`): copiar só o arquivo de login do Codex para a pasta de ensaio durante a prova e apagá-lo ao fim.

**Fonte:** Tickets 14 e 44; bancada de acesso do Codex; blocos dos Workers 2, 6 e 8. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** None (can start immediately)

- [ ] em `codex exec` com acesso total e a pasta de configuração de ensaio, o hook de início injeta texto
- [ ] o hook antes da ferramenta recusa um `apply_patch` que regrava arquivo existente
- [ ] o hook de fim devolve ao agente e depois solta
- [ ] o `notify` dispara
- [ ] o login copiado foi apagado, com a confirmação no relatório

## Comments
- 2026-10-16 (Vela): ticket pego (`claimed`). Worktree `C:\context-hub-wt\ticket-03`, ramo `ticket-03`, da ponta de `integracao` (69cb383). Lidos: regras, brief, tickets 14 e 44, bancada do Codex, Workers 2, 6, 7 e 8. Costura: `codex exec` real (0.162.1) com `CODEX_HOME` de ensaio e hub de ensaio, por `node --test`. Falta: teste, scripts em `provas/03-codex-hooks/`, rodar, relatório, revisão do Fiel.
- 2026-10-16 ~22h10 (Vela): os quatro critérios passaram em `codex exec` 0.162.1 com `danger-full-access` e `CODEX_HOME` de ensaio; login copiado apagado a cada rodada (5/5 verdes, ramo `ticket-03` até a14d996). Relatório: `etapas/00-provas/relatorio-codex.md` (inclui "O que vai doer ao ligar": `notify` único substitui o do Computer Use; Codex regrava o `config.toml`; hash aprova o comando, não o script). Falta: revisão do Fiel.
- 2026-10-16 ~22h20 (Vela): rodada 1 do Fiel = volta (o instalador aprovava hooks alheios). Consertado com teste de composição; prova movida para `agents/code/test/provas/03-codex-hooks/`; `integracao` (b68f540) juntada; 8/8 verdes, ramo até f4bb98b. Falta: rodada 2 do Fiel.
- 2026-10-16 ~22h30 (Vela): rodada 2 do Fiel = **passa** (parecer em `etapas/00-provas/parecer-Vela.md`). Evidência da execução do revisor gravada no ramo. Maestro avisado; falta juntar em `integracao` e resolver o ticket (maestro).
- 2026-10-16 ~21h20 (maestro): **resolvido.** Parecer do Fiel `etapas/00-provas/parecer-Vela.md` (rodada 2: passa). Juntado em `integracao` (3857c98); a árvore juntada é idêntica à de `ticket-03` (7532cc9), onde o Fiel rodou os 8 testes da prova; na junção rodaram os 11 do esqueleto (verdes). A prova não foi repetida para não chamar o Codex de novo com o login copiado. Lições para o kit anotadas no ticket 23.
