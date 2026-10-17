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
