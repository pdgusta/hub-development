# 06: Gerador de exclusões

Type: task
Status: resolved
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
- 2026-10-17 (Vela): Fiel = **passa** na rodada 2 (parecer em `etapas/01-esqueleto/parecer-Vela.md`). Ramo em 76d82b2 com integracao 45ec3b0; 7/7 e 14/14. Encaminhado ao Rebite.
- 2026-10-16 20h32 (integrador, Rebite): juntado em `integracao`, commit 8b9beef (merge `--no-ff` de `ticket-06` 76d82b2; o parecer "passa" da rodada 2 do Fiel é do b7cd714, e depois dele só entrou a junção de `integracao` 45ec3b0, que muda só `agents/code/test/provas/01-banco/`). Testes: `node --test` de `agents/code/test/*.test.mjs`, `gerar-exclusoes/*.test.mjs` e `instalar.test.mjs` do 03 = 44/44 verdes (o gerador com o obsidian-hybrid-search local). O `sincronizador.ps1` (Docker) não foi repetido: os arquivos dele e o que ele usa (gerador, `banco.psm1` da prova 02, montador) são idênticos aos do b7cd714 testado pelo Fiel (14/14; `-SoPonto` com 6 FALHA esperadas). As provas 01, 02 e 03 também não, árvores idênticas às revisadas. Ressalvas (decisões do Gustavo): pasta local nova criada com o CLI rodando vaza (parar, gerar, religar); quem roda o gerador depois da instalação; exclusão do git; limpeza ao pôr `local: true` numa pasta que já replicou; `index.md` ilegível trava a lista inteira e quem chama tem de mostrar o erro. A leitura do Fielzinho ficou pendente (limite de uso). **Resolvido.**
