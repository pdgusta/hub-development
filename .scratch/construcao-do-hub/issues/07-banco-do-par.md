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
- 2026-10-16 20h28 (integrador, Rebite): lições do ticket 01 (parecer do Fiel, `etapas/00-provas/parecer-Brasa.md`): (1) o caso "nada em claro" da prova 01 só procura nomes e textos que ela mesma cria; incluir nomes e trechos do hub de ensaio, como a sonda do Fiel (`_all_docs?include_docs=true` crus dos dois bancos); (2) os contêineres da prova se chamam `hub-ensaio-00-*`, o spec do Worker 4 diz `hub-ensaio-04-*`: o kit decide; (3) `banco.psm1` está duplicado entre as provas 01 e 02 (e o 06 importa o da 02): juntar aqui.
