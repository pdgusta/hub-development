# 06: Gerador de exclusões

Type: task
Status: ready-for-agent
Etapa: 1 (esqueleto)
Blocked by: 04, 02

**What to build:** O script que gera, a partir dos marcadores (`local: true` e tudo que tem ponto), a lista do que não replica nem entra na busca, na forma que o sincronizador e a busca leem.

**Fonte:** Ticket 12 ("Pasta não replicada"); faixa 1; resultado da prova 02. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 04 (Esqueleto do hub e hub de ensaio), 02 (Prova: pastas com ponto aninhadas fora do LiveSync)

- [ ] uma pasta com `index.md` `local: true` e qualquer caminho com ponto saem na lista gerada
- [ ] a lista funciona no sincronizador na forma provada pelo ticket 02 e na exclusão da busca

## Comments
