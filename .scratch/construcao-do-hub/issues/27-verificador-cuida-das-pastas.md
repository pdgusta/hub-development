# 27: O verificador cuida das pastas: `index.md`, links `par://`, `other/` e o fim da resposta

Type: task
Status: claimed
Etapa: 1 (esqueleto)
Blocked by: 05, 06

**What to build:** As quatro tarefas do verificador sem IA que ficaram fora do ticket 05: criar o `index.md` de uma pasta quando ela chega a 10 arquivos ou guarda arquivo que a busca não lê, e manter a lista dos que têm `summary: auto`, preservando o texto livre do topo (o anexo com texto irmão dispensa linha); conferir os links pelo cartão das pastas e corrigir nos dois sentidos (link para o que não replica vira `par://<par_id>/<caminho>`, e o contrário), avisando o agente; avisar quando três notas parecidas em `other/` pedem bloco novo; e o fragmento de fim de resposta de cada harness (mod do Claude Code, hook `Stop` do Codex, hook `agentStop` do Copilot) que roda o verificador e devolve ao agente a lista do que falta. Os fragmentos ficam em `agents/code/hooks/` e `agents/code/mods/`; o kit de par (ticket 23) os junta.

**Fonte:** Faixa 1 em `spec-partes/faixas-01-02.md` ("Verificador sem IA", tarefas (e) a (h); "`index.md`, cartão da pasta"; user stories 20, 35 a 43); ticket 12; prova 03 (`etapas/00-provas/relatorio-codex.md`) para o hook `Stop` do Codex. Decisão do Gustavo na rodada `2026-10-16-ticket-05-perguntas-do-trilho` (pergunta 1, A). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 05 (Frontmatter imposto), 06 (Gerador de exclusões: o que não replica decide os links `par://` e o `local: true` do `index.md`)

- [ ] uma pasta do hub de ensaio que chega a 10 arquivos, ou que guarda um PNG, ganha `index.md` válido; rodar de novo atualiza a lista e preserva o texto livre do topo
- [ ] um link comum para uma pasta `local: true` vira `par://`, e um `par://` para o que replica vira link comum, com aviso ao agente
- [ ] três notas parecidas em `other/` geram o aviso de bloco novo
- [ ] nos três harnesses, com HOME de ensaio, o fim da resposta roda o verificador e devolve a falta ao agente; sem falta, solta

## Comments

- 2026-10-16 ~21h30 (maestro): publicado pela decisão do Gustavo (rodada `2026-10-16-ticket-05-perguntas-do-trilho`, pergunta 1, A). As quatro tarefas estavam no spec e ficaram fora dos 26 tickets no fatiamento do `/to-tickets`.
- 2026-10-17 (Vela): pego (`claimed`). Worktree `C:\context-hub-wt\ticket-27`, ramo `ticket-27`, de `integracao` 8b9beef. Falta: tudo (4 tarefas).
