# 27: O verificador cuida das pastas: `index.md`, links `par://`, `other/` e o fim da resposta

Type: task
Status: resolved
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
- 2026-10-16 ~20h55 (maestro): perguntas da Vela no 27: aceitos como técnicos (1) `HUB_PAR_ID` por variável do kit, (2) três parecidas em `other/` pelo `why_other`, (3) lista do `index.md` entre `<!-- lista:inicio -->`/`<!-- lista:fim -->`, (4) contagem de 10 entradas diretas sem ponto; (5) proteção contra laço no fim da resposta foi para a rodada `2026-10-16-laco-no-fim-da-resposta` (vale também para o 18).
- 2026-10-16 20:39 (maestro): proteção contra laço no fim da resposta decidida pelo Gustavo (rodada `2026-10-16-laco-no-fim-da-resposta`, B): devolve até três vezes seguidas; na quarta parada ainda com falta, solta e registra a falta no `estado.json` da vigia (início da próxima sessão e tela de estado).
- 2026-10-16 ~21h05 (maestro): pergunta da Vela: `agents/frontmatter/**` vira tipo null no `paths.yml` (oficina, como `agents/code/`), para não pedir `index.md` com 30 descrições dos esquemas; decisão técnica do maestro.
- 2026-10-17 (Vela): links par:// e cartão da pasta feitos (286236e, 8/8). Falta: aviso de other/, fim da resposta nos três harnesses. Retomada em `etapas/retomada-Vela.md`.
- 2026-10-17 (Vela): aviso de other/ feito (efcd0a5; 27: 11/11). integracao 8d1d785 juntada (a5fef35). Falta: fim da resposta nos três harnesses.
- 2026-10-17 ~00h25 UTC (Vela): fim da resposta nos três harnesses feito (cdcb683, 8d8f1b9); prova real verde nos três; 97/97 sem harness. Pedida a revisão ao Fiel. Relatório: etapas/relatorio-27-verificador-pastas.md.
- 2026-10-17 ~00h45 UTC (Vela): rodada 2 com os cinco consertos do Fiel (d87e556, evidência 5df8972); 106/106 sem harness; ponta a ponta dos três verde, hashes iguais. Pedida a rodada 2 ao Fiel.
- 2026-10-17 (Vela): rodada 2 PASSA (Fiel e Fielzinho). Avisado o Rebite.
- 2026-10-16 21h51 (integrador, Rebite): juntado em `integracao`, commit 0a8e17f (merge `--no-ff` de `ticket-27` 5df8972, o HEAD da rodada 2 "passa" de Fiel e Fielzinho; árvore juntada idêntica à do ramo). Testes sem harness (regra provisória do maestro, até o 29): `node --test "agents/code/test/*.test.mjs" "agents/code/test/gerar-exclusoes/*.test.mjs"` = 106/106 verdes. A ponta a ponta dos três (`ponta-a-ponta/27-fim-da-resposta.test.mjs`) não foi rodada: harness real, fora pela regra provisória, e árvore idêntica à revisada. Ressalvas do parecer: link para fora do hub no `par://` é ponto aberto ao maestro (o caminho é "a partir da raiz do hub"); vigia × item `fim-da-resposta` (comentado no 16); na quarta parada (solta para a vigia) os avisos novos daquela parada não são entregues nem marcados como avisados; o `.codex/config.toml` real mudou durante a rodada dos três na rodada 1 (causa provável: sessões reais do Codex; a repetição saiu com hashes iguais). **Resolvido.**
