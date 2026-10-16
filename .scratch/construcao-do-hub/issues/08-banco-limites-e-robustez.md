# 08: Banco: limites e robustez

Type: task
Status: ready-for-agent
Etapa: 2 (banco)
Blocked by: 07, 06

**What to build:** O banco aguenta o uso real: exclusões pela lista do gerador, limite de 200 MiB, colisão de binário recuperável, kit idempotente, laço que religa o sincronizador, e um retrato do banco (conflito aberto, binário com ramo apagado, replicação parada) para as etapas seguintes.

**Fonte:** Bloco do Worker 4 (os itens que eram "se sobrar" voltam a ser entrega cheia); tickets 33, 47, 48. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 07 (Banco do par: dois CouchDB, LiveSync e vista `.md`), 06 (Gerador de exclusões)

- [ ] nada com ponto nem `local: true` chega ao banco, com o CLI rodando e na partida
- [ ] arquivo de 60 MiB viaja e o de 201 MiB não
- [ ] colisão de binário deixa a versão perdida num ramo recuperável
- [ ] o kit roda de novo sem mudar nada; com o CLI morto ou o banco fora na partida, o laço religa
- [ ] o retrato do banco está gravado para as etapas 3 e 6

## Comments
