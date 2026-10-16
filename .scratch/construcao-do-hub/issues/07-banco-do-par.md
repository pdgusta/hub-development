# 07: Banco do par: dois CouchDB, LiveSync e vista `.md`

Type: task
Status: ready-for-agent
Etapa: 2 (banco)
Blocked by: 01, 04

**What to build:** Par A e par B de ensaio nesta máquina, cada um com o seu CouchDB e uma replicação de envio, o CLI do LiveSync como sincronizador com a cifra de ponta a ponta e o caminho ofuscado, e a vista `.md` de mão dupla sobre o hub de ensaio. Sobe pelo passo do kit de par desta etapa.

**Fonte:** Bloco do Worker 4; faixa 4 em `spec-partes/faixas-03-04.md`; tickets 25, 33, 34, 47, 48. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 01 (Prova: dois CouchDB replicando com o LiveSync), 04 (Esqueleto do hub e hub de ensaio)

- [ ] o kit sobe os dois bancos e as duas replicações em andamento
- [ ] nota criada na pasta A aparece na B, e a editada na B volta à A, sem texto claro no banco
- [ ] a mesma linha editada nos dois pares vira conflito nos dois bancos, sem versão perdida

## Comments
