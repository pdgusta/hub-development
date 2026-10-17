# 17: Vigia nas telas dos harnesses

Type: task
Status: claimed
Etapa: 6 (vigia)
Blocked by: 16, 03

**What to build:** O estado da vigia chega aos harnesses: hook de início com o resumo nos três, o `notify` do Codex, a barra de estado do Copilot e o mod do Claude Code. Os avisos do Codex não se repetem enquanto o estado não muda.

**Fonte:** Bloco do Worker 7, item (d); ticket 14 ("Checagem de início", "Estado da vigia na tela"); escolha aceita 22. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 16 (Vigia: passada, estado e notificação), 03 (Prova: hooks do Codex em acesso total)

- [ ] o hook de início, com a entrada de cada harness, devolve o resumo; sem a vigia e sem o MCP, diz "estado indisponível"
- [ ] o `notify` do Codex não repete o aviso enquanto o estado não muda
- [ ] o mod e a barra do Copilot mostram o estado de um arquivo de exemplo

## Comments
- 2026-10-16 20:24 (maestro): aval do Gustavo para copiar o login dos três harnesses em pasta de ensaio (rodada `2026-10-16-login-dos-harnesses-no-ensaio`, A, vale para a construção inteira); condições em `../etapas/regras-da-construcao.md`.

- 05:09 (maestro, mandato): começa antes do 16 ser resolvido, com a Vela, sobre a ponta de `integracao`, contra o `estado.json` combinado entre o Trilho (16) e o Cinzel (10) em `../etapas/costuras-16-Trilho.md` (exemplo fixo nos testes). Quando o 16 for juntado, `git merge integracao` e trocar o exemplo pelo real. Junção só com o 16 resolvido.
- 2026-10-17 05h11 (Vela): claimed; costuras propostas em ../etapas/costuras-17-Vela.md, esperando o maestro antes de codar.

- 05:12 (maestro, mandato): costuras da Vela aceitas (`../etapas/costuras-17-Vela.md`). 1) variáveis e formato do `estado_do_hub` confirmados com o Cinzel; 2) mod pela linha de status (`$.ui.status`); a faixa acima do prompt fica para o Gustavo, se quiser; 3) `barra-copilot.cmd` se o `statusLine` não aceitar argumentos; 4) com `ok`, a linha curta é injetada e o agente não fala dela (resposta calada, como o spec pede).
- 2026-10-17 ~06h00 (Vela): feitos 2947951..96bddcb (início nos três, reserva pelo MCP, notify, barra, fragmentos, mod); 17-vigia-tela 15/15, mod 2/2. Falta: ponta a ponta real (Codex depois das 06h58), relatório, merge do 16 quando entrar, Fiel, Rebite. Retomada gravada antes do /clear.
- 2026-10-17 07:28 (Vela): ponta a ponta real verde nos três (Claude e Copilot 4/4 às 06:22, Codex 2/2 às 07:26, notify uma vez); integracao 9cc878b juntada; HEAD 86c5a88. Relatório ../etapas/relatorio-17-vigia-nas-telas.md. Revisão pedida ao Fiel. Falta: merge do 16 quando entrar (teste sobre o estado.json real), Rebite (junção só com o 16 resolvido).
- 2026-10-17 07:49 (Vela): rodada 2 do Fiel PASSA em 3e8bbc8 (rodada 1 voltou: estado sem passada). Rebite avisado; junção só depois do 16.
