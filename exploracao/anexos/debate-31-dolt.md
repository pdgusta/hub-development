---
title: Debate sobre o Dolt (transcrição integral)
data: 2026-10-04
origem: nota "Debate Dolt" do canvas do Maestri; Basalto (Claude Code, defensor) e Cardo (Claude Code, crítico), conversando entre si
aviso: saída de modelo; o veredito está no ticket 31
---

# Debate sobre o Dolt

Transcrição dos turnos (Basalto defende, Cardo contraria). Cada um acrescenta o próprio turno ao fim.

## Turno 1, Basalto (defensor): a tese

O critério que decide é "nada diverge em silêncio, com proteção contra edição concorrente" (critérios 4 e 5, ticket 27). Nele, o Dolt é o único dos três que cumpre por padrão; O1 e O3-C só cumprem depois de mexer na escrita do agente.

1. A garantia mora no motor, não num plugin. Colisão por célula vira linha em dolt_conflicts_<t> (base, ours, theirs); em autocommit o merge com conflito "will be automatically rolled back"; dolt_allow_commit_conflicts=0 recusa o commit (docs.dolthub.com: git/conflicts.md, merges.md, dolt-sysvars.md; pesquisa 27, P9). Nos rivais, a escrita do agente hoje sobrescreve: o es617 declara "No conflict resolution... last write wins" (README; pesquisa 26); o note_create_or_update do FNS grava sem BaseHash (note_tools.go 140-150; pesquisa 28), e o padrão do plugin FNS é "No Merge, Keep Latest", que descarta a edição local (en.ts 84-89).
2. Não depende do Obsidian aberto. No O3, "os plugins só rodam com o Obsidian aberto" (pesquisa 28, resumo item 3). No Dolt, o agente grava no sql-server local e o sync é dolt_pull/dolt_push, sem Obsidian; "Offline First" é caso de uso oficial (use-cases/offline-first.md; pesquisa 27, seção 5).
3. A verdade num banco de fato. Histórico, diff e branch por linha via SQL (dolt_diff_<t>, DOLT_BRANCH_STATUS, DOLT_PREVIEW_MERGE_CONFLICTS_SUMMARY): a checagem de início de sessão sai quase pronta (pesquisa 27, P10). O beads (27,6 mil estrelas) já usa o Dolt como verdade (README do beads).
4. Agentes e ponto de encontro prontos. Bloco mcp_server no config.yaml e "claude mcp add -t http dolt-mcp http://localhost:7007/mcp" (server/configuration.md); dolt-mcp com build Windows (README). Encontro no GitHub privado (refs/dolt/data) ou no próprio servidor pela tailnet (remotesapi).

Concedo:
- A vista .md de mão dupla não existe: é a maior peça, 3 a 6 dias (V1); total de 9 a 20 dias, contra peças de 0,5 a 3 dias no O3-C e "P" no O1.
- Merge por célula: nota inteira em TEXT colide com edições em parágrafos diferentes (inferência, pesquisa 24). Mitigação: corpo em JSON por seção ou uma linha por bloco.
- O remote git é de 2026 e ainda recebe correções sérias (#11741, #11949).
- Não verificado: Dolt como serviço Windows e a versão em que entrou o MCP embutido.

Por que caminho, e não reserva: o custo extra do Dolt é construção previsível numa ponte, fora do núcleo. O custo dos rivais está na própria garantia central, que hoje falha por padrão. Melhor construir a vista sobre um motor que já para e avisa.

## Turno 2, Cardo (crítico)

Tese: o critério é a verdade num banco, com o .md editável no Obsidian e volta ao banco sem divergir em silêncio (ticket 27). No Dolt, justamente a parte que toca o Gustavo ainda não existe. O O3-C (FNS) e o O1 já a entregam.

Réplica:

1. O "cumpre por padrão" vale só para o merge entre máquinas. A edição do Gustavo entra pela ponte .md, e "Não existe ponte pronta Dolt ↔ vault" (pesquisa 27, P12). A guarda dessa ponte é código novo, de 3 a 6 dias. Na escrita do agente, o dolt-mcp expõe `exec` cru, e o "ler, pensar, gravar" pede coluna de versão mais UPDATE condicional, marcado como "construir" (pesquisa 27, P5). É o mesmo remendo que você cobra dos rivais, só que maior. Nos rivais:
   - no FNS, basta repassar `expected_hash` como `BaseHash`, porque o servidor já recusa com 530 (ws_note.go 132–163; pesquisa 28, C1, de 0,5 a 1 dia);
   - no O1, o `conflictBaseRev` já existe em `putDBEntry` (EntryManagerImpls.ts 207–221; pesquisa 26, §3, de 1 a 2 dias).
2. O "descarta por padrão" do FNS se resolve com configuração: Manual Merge nas duas máquinas, de 2 a 4 horas (pesquisa 28, C2).
3. Obsidian aberto: concedo o limite do plugin. Mas, se o Gustavo está editando, o Obsidian está aberto; o resíduo é a fila pendente, e a checagem de sessão avisa. O agente grava pelo MCP do servidor, sem depender do Obsidian. O O1 tem ainda o `daemon` do CLI oficial do LiveSync (src/apps/cli/README.md; no Windows, não verificado). O Dolt também exige um processo vivo, o daemon da ponte.
4. O beads não é precedente para a vista: o `.jsonl` dele é "an export … not the source of truth" (README do beads). Não há .md editável voltando ao banco.
5. "Construção fora do núcleo" inverte o risco. A ponte é onde a garantia se cumpre para o Gustavo, e uma ponte nova e sem teste pode recriar a sobrescrita silenciosa (a "falha da volta sem conferência" do sqlite-memory, pesquisa 27, §6.2). No O1, essa garantia já mora na árvore de revisões do LiveSync: "Postponement therefore does not make the conflict invisible" (specs_conflict_resolution.md).

Concedo:
- o motor para e avisa;
- o histórico e o diff por SQL são superiores;
- o MCP embutido é real (configuration.md).

Mantenho: são de 9 a 20 dias contra cerca de 2. Além disso, o merge por célula colide por nota inteira e exige redesenhar o schema. Por isso o Dolt é reserva, não caminho.

## Turno 3, Basalto (defensor)

Concedo: o beads não é precedente para a vista .md; o padrão do FNS se resolve com Manual Merge (pesquisa 28, C2); e o mínimo do Dolt fica em uns 9 dias (pesquisa 27, seção 9), contra 2 a 3 no O3-C (C1 + C2 + X1, pesquisa 28, seção 8).

Rebato:

1. Escrita do agente: empate, não "o mesmo remendo, maior". A guarda é SQL que o dolt-mcp já executa (UPDATE ... WHERE versao = ?), sem patch em código de terceiros: "0,5 dia só com skills" (pesquisa 27, C5). Um usuário SQL só com procedure fecha o atalho (inferência; access-management.md, não verificado). O C1 do FNS é um patch em Go num fork, de 0,5 a 1 dia.

2. A ponte pode delegar a guarda ao motor, em vez de inventá-la. Ela grava a edição do Obsidian numa branch e chama DOLT_MERGE. Se colidir, "you must resolve them using the dolt_conflicts system tables before the transaction can be committed" (dolt-sql-procedures.md). Uma só regra cobre as três entradas: o sync, o agente e o Gustavo. O sqlite-memory falhou porque não conferia nada; aqui, quem confere é o merge de três vias. Não verificado: criar a branch a partir do commit-base gravado no frontmatter, porque a doc de DOLT_BRANCH só mostra uma branch como ponto de partida. Reserva: o UPDATE condicional que devolve 0 linhas gera a nota de colisão (pesquisa 27, seção 6.2).

3. Nos rivais, a garantia também mora fora do núcleo. O Manual Merge do FNS é do plugin, que só roda com o Obsidian aberto (pesquisa 28, resumo item 3). Concedo que o O1 é o rival forte: o LiveSync junta trechos que não se sobrepõem, e o Dolt, por célula, não junta.

4. "Redesenhar o schema" exagera. O C1 custa de 0,5 a 1 dia, e a primeira opção é aceitar a colisão por nota inteira (pesquisa 27, seção 6.3). O FNS também decide por nota: o modal mostra base, servidor e local da nota (pesquisa 28, seção 5).

5. O que a semana a mais compra:
- histórico, diff e branch por SQL (você concedeu);
- um único motor que para e avisa nas três entradas;
- nenhum projeto pequeno de terceiros no caminho crítico, porque o dolt-mcp é da DoltHub (README).
A ponte se paga uma vez; a garantia em plugin alheio se paga a cada atualização dele.

Proposta: o Dolt é o caminho, condicionado a um spike da ponte V1 com teste de colisão nas três entradas. Se o spike falhar, o O1 assume.

## Turno 4, Cardo (crítico)

Concedo:
- a ponte com branch e DOLT_MERGE é elegante;
- o FNS também decide por nota.

Rebato:

1. A guarda "só com skills" é voluntária. Nada impede o agente de usar `exec` cru. A pesquisa 27 lista isso como risco, e a mitigação (um usuário só com procedure) está marcada "não verificado" (§9). No FNS, a recusa é do servidor: com `serverHash != baseHash`, ele "block[s] the override… return[s] 530" (ws_note.go 132–163). E há o C1(b): um MCP fino na frente, com "zero código no servidor" (pesquisa 28, §8). A guarda imposta existe pronta no FNS; no Dolt, não.
2. A ponte com DOLT_MERGE apoia-se num ponto não verificado central. Conferi a doc: DOLT_BRANCH só mostra "start point of tip of feature1 branch". Partir de um commit não aparece (dolt-sql-procedures.md). E a ponte continua inteira por construir: o parse do frontmatter, o watcher, o debounce e a nota de colisão, de 1 a 2 dias, que no FNS e no LiveSync já vêm prontos (pesquisa 27, §8; pesquisa 28, §7).
3. No FNS, a garantia mora no servidor, não no plugin. Quem confere o `baseHash` e devolve base, servidor e local é o ws_note.go.
4. Você aceita a colisão por nota inteira e ainda paga para construir o aviso dela. Com a mesma granularidade, o FNS entrega o modal pronto. E o O1 faz melhor que os dois: junta trechos que não se sobrepõem.
5. O argumento do "projeto pequeno de terceiros" vira contra o Dolt.
   - O dolt-mcp tem 19★ e está na v0.3.8 (pesquisa 27, P3).
   - O FNS tem 2.395★ no servidor e 3.047★ no plugin (pesquisa 28, §3.3); o LiveSync, 12.648★ (pesquisa 26, P2).
   - A ponte do Dolt seria o menor projeto de todos: código nosso, com zero usuários e manutenção perpétua nossa. "Plugin alheio a cada atualização" troca-se por "ponte própria a cada bug".
6. O histórico também existe nos rivais. O FNS tem histórico por nota, lixeira e espelho Git (README). O LiveSync tem `cat-rev` e `pull-rev` (pesquisa 26, F8). O diff por SQL é superior, mas não está nos critérios do Gustavo (ticket 27).

Contraproposta sobre o spike: a ordem decide. Primeiro o FNS, com C1, C2 e X1, cerca de 2 dias, porque é o teste mais barato do critério inteiro. O O1 vem como segundo. O spike da ponte Dolt, de 9 dias para cima, só entra se os dois falharem. Isso é reserva, não caminho.

## Turno 5, Basalto (defensor, fechamento)

Concedo:
- Guarda imposta: hoje só o FNS a tem pronta (ws_note.go 132–163). A minha saída do "usuário só com procedure" enfraquece. A doc do Dolt diz que o GRANT "Only handles static privileges down to the table level" (supported-statements.md). Há um caminho no motor: um trigger que recusa o UPDATE quando NEW.versao ≠ OLD.versao + 1. A doc marca CREATE TRIGGER como suportado, mas BEFORE UPDATE com SIGNAL ficou não verificado. Ainda é promessa.
- A ponte por branch depende de um ponto não verificado: criar a branch a partir de um commit. O parse, o watcher e a nota de colisão estão por construir.
- Maturidade: o dolt-mcp tem 19★ e está na v0.3.8 (pesquisa 27, P3). A ponte seria código nosso, sem usuários. Meu argumento de "projeto pequeno de terceiros" se volta contra mim nesse ponto.
- O diff por SQL não está nos critérios do ticket 27. O histórico existe nos três.
- A ordem do spike: o FNS testa o critério inteiro em cerca de 2 dias (pesquisa 28, seção 8). É o teste mais barato e deve vir primeiro.

Mantenho:
1. Entre as máquinas, só o Dolt para e avisa por padrão do motor: colisão por célula, merge desfeito em autocommit e commit recusado (git/conflicts.md, merges.md, dolt-sysvars.md). No FNS e no O1, isso depende de configuração ou de um fork (Manual Merge, C1, conflictBaseRev).
2. O motor do Dolt é maduro: 24,6 mil★, Apache-2.0, release v2.4.1 de 2026-10-02 com instalador Windows (pesquisa 24, tabela). O que é imaturo é a periferia (dolt-mcp, remote git), não o motor.
3. "Reserva" não pode ser "último da fila": isso esconde a opção. Peço uma sonda de meio dia, em paralelo ao spike do FNS, só para os dois pontos não verificados que decidem o desenho:
   - (a) um trigger BEFORE UPDATE com SIGNAL recusando versão velha;
   - (b) criar uma branch a partir de um commit e rodar DOLT_MERGE com colisão.
   Se os dois passarem, a guarda imposta e a ponte delegada ao motor ficam provadas a custo baixo. Se falharem, eu mesmo aceito o Dolt como reserva.

Fechamento: pelos critérios do ticket 27 e pelo custo, o FNS merece o primeiro spike, e o Cardo ganhou esse ponto. O Dolt continua sendo a única opção em que a regra de "nada diverge em silêncio" é do motor, e não de quem o configura. Ele não deve ficar no fim da fila sem que a sonda de meio dia seja feita.

## Turno 6, Cardo (crítico, fechamento)

Concedo:
- O motor do Dolt é maduro (24,6 mil★, Apache-2.0, v2.4.1 com .msi; pesquisa 24). A imaturidade está na periferia: o dolt-mcp, o remote git e a ponte, que ainda não existe.
- Só o Dolt recusa o commit com colisão por regra do motor (merges.md, dolt-sysvars.md).
- A sonda de meio dia é justa e barata. Ela testa exatamente os dois pontos que deixei como não verificados: o trigger com SIGNAL e a branch criada a partir de um commit. Quem decide se ela entra é o Gustavo.

Mantenho:
1. "Para e avisa entre máquinas" não é exclusivo do Dolt. No O1, o CouchDB não descarta o perdedor: escolhe um vencedor determinístico e guarda os outros em `_conflicts` (conflicts.rst). O LiveSync só junta quando é seguro; fora disso, "Ask the user". O "Always overwrite with a newer file" vem como "Testing only" (specs_conflict_resolution.md, settings.md; pesquisa 26, §6). A diferença real é outra: no Dolt a recusa é do motor, e no O1 é da árvore de revisões somada ao plugin. As duas cumprem os critérios 4 e 5 sem configuração especial. A exceção são os binários no LiveSync, e o hub grava só `.md`.
2. Mesmo que a sonda passe, o custo continua: a ponte, a nota de colisão e o sincronizador. Com a sonda, a garantia passa de promessa a prova, mas o total segue em 9 dias ou mais (pesquisa 27, §9). O FNS testa o critério inteiro em cerca de 2 dias (pesquisa 28, §8).
3. A granularidade favorece o O1. O merge por célula colide por nota inteira, enquanto o LiveSync junta trechos que não se sobrepõem (pesquisa 26, P2).

Fechamento: pelos critérios do ticket 27, o caminho é o O3-C (FNS com C1, C2 e X1) e, em segundo, o O1. O Dolt fica como reserva nomeada, não esquecida. Se o Gustavo quiser, a sonda de meio dia do Basalto corre em paralelo e decide se a reserva sobe. O argumento mais forte do Dolt, a regra no motor, é real. Mas ele protege a parte do critério que os rivais já cobrem, e deixa por construir a parte que o Gustavo vê, a vista `.md` de mão dupla.
