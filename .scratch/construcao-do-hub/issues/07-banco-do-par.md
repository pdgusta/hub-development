# 07: Banco do par: dois CouchDB, LiveSync e vista `.md`

Type: task
Status: claimed
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
- 2026-10-16 20:30 (maestro): receita da etapa 2 decidida (rodada `2026-10-16-etapa-2-receita`, A): Brasa faz o 07 e depois o 08.
- 2026-10-16 20:50, Brasa: peguei (Status claimed). Worktree `C:\context-hub-wt\ticket-07`, ramo `ticket-07`, de `integracao` 8b9beef (com o 06). Plano: passo do kit `agents/code/kit/par/04-banco.ps1 -EnvFile <par.env> [-WhatIf] [-Descer]` sobre o módulo `agents/code/kit/par/banco/` (compose, ini, módulo) e `agents/code/kit/par/env/04.env.modelo`; o passo roda o gerador de exclusões (06) antes da primeira partida do CLI. Teste de ponta a ponta `agents/code/test/07-banco.test.ps1` (Docker, fora do `node --test`), com contêineres `hub-ensaio-07-a/b` em 5994/5995. Ressalvas: (1) "nada em claro" também com nomes e trechos do hub de ensaio; (2) nome do contêiner vem do `.env` (ensaio `hub-ensaio-07-*`); (3) as provas 01 e 02 e o teste do 06 passam a importar o módulo do kit, sem cópia. Falta: tudo.
- 2026-10-16 21:20, Brasa: commit 4967c69 com o passo do kit (`agents/code/kit/par/04-banco.ps1`, módulo em `kit/par/banco/`, modelo em `kit/par/env/04.env.modelo`) e o teste `agents/code/test/07-banco.test.ps1`: verde, 21 PASSA (os três critérios, o -WhatIf, nada em claro com 76 nomes e trechos do hub, -Descer). Achado: o daemon herdava os handles de quem chamava o kit e travava o chamador; agora sobe sem herdar. Falta: juntar as cópias das provas 01/02 e do teste do 06 no módulo (ressalva 3), relatório, revisão.
- 2026-10-16 ~21h05, Brasa: ressalva 3 feita (commit 810bbde): provas 01 e 02 e o teste do 06 importam `agents/code/test/banco/ensaio.psm1`, sobre o módulo do kit; cópias apagadas; as três verdes. Achado e conserto (7fa0e56): o passo não religava o CLI quando o gerador mudava a lista com o daemon rodando; caso novo no teste. `integracao` 8d1d785 juntada (3babfb2). Teste do 07: 24 PASSA. Relatório `etapas/relatorio-07-banco-do-par.md`. Falta: rodada final das três depois da junção, revisão.
- 2026-10-16 ~21h20, Brasa: rodada final verde depois da junção (07: 24 PASSA; prova 01: 17; prova 02: 12; teste do 06: 14). Pedi revisão ao Fiel. Achado fora do ticket: a suíte `node --test` chama os harnesses de verdade (teste do 14 e prova 03), com cópia de login; registrado no relatório.
- 2026-10-16 ~23h10, Brasa: rodada 1 voltou (três consertos no `banco.psm1`). Feitos em 6911857, com teste sem Docker (`agents/code/test/banco/kit-sem-docker.ps1`, CLI falso, chamado pelo `07-kit-sem-docker.test.mjs`): verde. Achado no caminho: o CLI cifra o remoto depois do aceite, e com o daemon rodando nenhum comando abre o banco local; a conferência do remoto usa a marca do aceite. A fila Docker foi morta pelo sistema por falta de memória; espero aval para religar.
