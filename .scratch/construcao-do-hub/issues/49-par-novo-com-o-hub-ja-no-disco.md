# 49: Par novo com o hub já no disco

Type: task
Status: ready-for-agent
Etapa: preparo do 26 (par B)
Blocked by: 46

**What to build:** No 26, o par B vai ter o hub **clonado em `C:\context-hub`** antes de o banco dele receber a
replicação do par A. Nenhum teste provou o que o CLI do LiveSync faz quando o disco do par novo já tem os mesmos
arquivos que chegam do banco (`agents/code/docs/instalacao.md` §2, "não verificado"). Pode virar conflito em massa
(duas versões de cada nota), ou duplicar, ou ser inócuo. Provar no ensaio, com a trava e Docker:
1. par A de pé com o hub de ensaio; par B com uma cópia **idêntica** do hub no disco (como um clone), banco vazio;
   subir o B pelo kit e esperar a convergência (passo `espera` do 46);
2. contar conflitos no banco (`_conflicts`), arquivos duplicados ou renomeados no disco do B, e o que a vigia diz;
3. repetir com uma diferença pequena entre os discos (um arquivo a mais no B, um alterado), para saber o que ganha.
Se der conflito ou perda, propor o caminho seguro para o 26 (ex.: B sobe com o disco vazio e o código do kit fora do
hub, ou o clone só depois da convergência) e escrever no relatório.

**Fonte:** decisão do Gustavo (2026-10-18 ~12h45: "concordo" com o teste curto enquanto o par A é instalado).

**Blocked by:** 46 (resolvido)

- [ ] ensaio com o disco do B igual ao do A: conflitos, duplicados e vigia contados
- [ ] ensaio com uma diferença pequena: o que ganha
- [ ] recomendação para o par B do 26 no relatório

## Comments

- 2026-10-18 ~12h45 (maestro): publicado. Dona: a Brasa (banco do par, 07/08/45). Prioridade: antes do par B.
