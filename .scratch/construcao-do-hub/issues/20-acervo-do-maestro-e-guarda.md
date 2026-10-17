# 20: Acervo do maestro e a guarda dele

Type: task
Status: claimed
Etapa: 8 (skills e acervo)
Blocked by: 19, 03

**What to build:** A família `maestro-*` com o primeiro lote, o lembrete de início que só age dentro do Maestri e a guarda do acervo, que decide pelo arquivo de destino, inclusive pelo atalho e fora do hub. As propostas do Codex e do Copilot e o registro de uso ficam fora da guarda.

**Fonte:** Bloco do Worker 9; tickets 40, 43, 44; escolha aceita 17. Perguntas ao Gustavo na hora: as três lacunas de dono (onde fica o registro do aval de mudança no contrato, quem escolhe o modelo do verificador da guarda, como chega a ele o erro de peça que sumiu). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 19 (Roteamento de skills), 03 (Prova: hooks do Codex em acesso total)

- [ ] sem o Maestri, o hook de início não faz nada; com ele, injeta o lembrete
- [ ] gravar numa peça protegida pede aval no Claude Code e é recusado no Codex e no Copilot, pelo caminho real, pelo atalho e numa sessão fora do hub
- [ ] gravar nas propostas passa; o maestro grava a tabela de roteamento
- [ ] cada peça da família tem nome e descrição válidos

## Comments
- 2026-10-16 ~22h35 (maestro): próximo da Vela depois do 19 (juntado dc56d47); primeiro commit do ramo conserta as duas ressalvas do 19 (import do registro fora do try no fim-da-resposta; `dentroDoHub` sem resolver junction).
- 2026-10-17 (Vela): pegou o 20. Status claimed; ramo ticket-20, worktree C:/context-hub-wt/ticket-20, de integracao dc56d47. Primeiro: commit separado com os dois consertos do 19 (teste antes).
- 2026-10-17 (Vela): commit 8acd1ce, os dois consertos do 19 (import dinâmico do registro dentro do try; bin/lib/caminhos.mjs resolve junction no fim e na entrada). Suíte 131 verdes, 5 pulados. Falta: o 20 em si (família maestro-*, lembrete de início, guarda do acervo).
- 2026-10-16 ~22h50 (maestro): perguntas da Vela: (4) identidade do maestro por `HUB_PAPEL=maestro`, posta pela receita de setup (confia no ambiente, não é autenticação); (5) guarda no Claude Code por hook de settings `PreToolUse` com `ask`, desde que cumpra o verificador em outro modelo. As três lacunas de dono foram para a rodada `2026-10-16-acervo-do-maestro-tres-lacunas`.
- 2026-10-17 (Vela): 2cc4eea, família maestro-* com o primeiro lote e verificador do acervo (cada peça com nome e descrição válidos). Falta: hook de início, guarda, registro de uso.
- 2026-10-17 (Vela): 8301996 lembrete de início; 86a24d9 guarda do acervo (Codex e Copilot recusam com o caminho de propostas; Claude pede parecer do verificador em outro modelo e depois aval; HUB_PAPEL=maestro grava a tabela). 20-acervo 11/11. Falta: prova real nos três harnesses, relatório, revisão.
- 2026-10-17 (Vela): e5d24a7, prova real verde no Claude Code e no Copilot; Codex sem cota até 01:34. Relatório etapas/relatorio-20-acervo-do-maestro.md.
- 2026-10-16 ~23h35 (maestro): pontos da Vela: linha acrescentada no catálogo sem aval foi para a rodada `2026-10-16-catalogo-do-acervo-linha-nova`; partitura guardada sem o texto de cliente das notas (acervo genérico), decisão do maestro; verificador provisório em Sonnet até a rodada das três lacunas. Revisão pedida já; prova do Codex depois de 01:34.
- 2026-10-17 (Vela): rodada 2 do Fiel PASSA em 5811579; levado ao Rebite. Pendente: prova real do Codex depois de 01:34 (commit só de evidência, rodada curta do Fiel).
