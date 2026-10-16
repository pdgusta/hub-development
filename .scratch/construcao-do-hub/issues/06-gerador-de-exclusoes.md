# 06: Gerador de exclusões

Type: task
Status: claimed
Etapa: 1 (esqueleto)
Blocked by: 04, 02

**What to build:** O script que gera, a partir dos marcadores (`local: true` e tudo que tem ponto), a lista do que não replica nem entra na busca, na forma que o sincronizador e a busca leem.

**Fonte:** Ticket 12 ("Pasta não replicada"); faixa 1; resultado da prova 02. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 04 (Esqueleto do hub e hub de ensaio), 02 (Prova: pastas com ponto aninhadas fora do LiveSync)

- [ ] uma pasta com `index.md` `local: true` e qualquer caminho com ponto saem na lista gerada
- [ ] a lista funciona no sincronizador na forma provada pelo ticket 02 e na exclusão da busca

## Comments
- 2026-10-16 20h00 (integrador, Rebite): lição do ticket 02 (relatório `etapas/00-provas/relatorio-pastas-com-ponto.md` e parecer do Fiel): a forma provada é `.livesync/ignore` com `.*` e `.*/`, escrito em cada máquina antes da partida do CLI, sem negação (o CLI lança erro com `!`; `import: .gitignore` traz as negações), e mudança exige reinício. O próprio `.livesync/ignore` não viaja pela replicação.
- 2026-10-16 ~23h20 (Vela): pego (`claimed`). Worktree `C:\context-hub-wt\ticket-06`, ramo `ticket-06`, de `integracao` c8d2267. Falta: ler 12/faixa 1/busca, teste, gerador, relatório, revisão.
- 2026-10-16 ~23h50 (Vela): gerador em `agents/code/bin/gerar-exclusoes.mjs` (escreve `.livesync/ignore` e `.local/exclusoes/busca.env`); testes em `agents/code/test/gerar-exclusoes/` (5/5 do gerador e da política da busca; 14/14 do sincronizador de ponta a ponta, `hub-ensaio-06-a/b` em 5998/5999). `integracao` 0d04985 juntada; ramo até d45be5d. Relatório: `etapas/relatorio-06-gerador-de-exclusoes.md` (ponto principal: pasta local nova criada com o CLI rodando vaza; precisa parar, gerar e religar). Falta: revisão do Fiel e do Fielzinho.
