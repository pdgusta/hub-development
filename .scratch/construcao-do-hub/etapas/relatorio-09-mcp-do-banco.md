# Relatório do ticket 09: MCP do banco, gravar com versão e conflito à vista (Cinzel)

Dois ramos `ticket-09`:
- **Fork** em `C:\Projetos\hub-mcp-banco`, repositório próprio (decisão A do Gustavo). Parte de v0.10.0 (1a4d53f).
  Commits 289ec4c (o código), dd9ddb5 (consertos do teste) e 61a6e70 (as folhas são lidas antes de limpar o sal da
  E2EE; só o 404 conta como nota nova).
- **Hub**: worktree `C:\context-hub-wt\ticket-09`, da ponta de `integracao` 763813a.
  - Commits ce9790b (o passo do kit e os testes) e 619655f (o passo remonta um build velho; o teste B ganha o conflito
    na mesma linha e a fusão do LiveSync).
  - Depois, `integracao` 33b817a (os tickets 33 e 35) foi juntada em 3d9d0bb. Ela não toca no banco nem no kit dele,
    só no registro da busca e no verificador. O teste sem Docker segue verde depois da junção; o Docker rodou em
    619655f.

## O que foi construído

### No fork: a gravação com versão

O que um agente vê pelas ferramentas:

| Ferramenta | Antes (upstream) | Agora |
|---|---|---|
| `read_note` | só o texto | o texto mais a linha `base_rev: <versão>`. Nota em conflito: `CONFLITO`, com uma linha `- versão <rev>` para cada versão guardada. O parâmetro `rev` opcional lê uma versão dada |
| `write_note` | grava por cima da versão que vence | grava como filha da `base_rev`. Base velha: "conflito: releia e refaça", e as duas versões ficam no banco. Sem `base_rev` numa nota que existe, ou com uma base que a nota nunca teve: `Recusado:`. Nota nova sem base: nasce como raiz própria |
| `edit_note` | troca, anexa ou antepõe sobre a versão que vence | a troca de trecho exige `base_rev` e age sobre o texto dessa versão. Anexar e antepor sem base agem sobre a versão lida na mesma chamada e gravam como filha dela |
| `delete_note` | apaga a versão que vence | exige `base_rev`. Base velha: conflito, e a versão do outro escritor continua legível |
| `move_note` | grava no destino e apaga a origem, às cegas | exige a `base_rev` da origem; recusa destino que já existe |
| `get_conflicts` | não existia | lista as notas em conflito, com as versões de cada uma |

**De onde vem a guarda: a biblioteca do LiveSync já tem o gancho.** É o ponto aberto da faixa 5 ("gancho de revisão
de base, não conferido no código").
- `putDBEntry(nota, false, base)`, no modo `force-base` (`lib/livesync-commonlib/src/managers/EntryManager/EntryManagerImpls.ts`),
  grava o documento de metadados com `_rev = base` e `put(..., {force: true})`.
- No PouchDB, esse `put` vira `_bulk_docs` com `new_edits=false` e `_revisions [nova, base]`: o mesmo caminho do
  `r1.py` do spike.
- Os pedaços do texto passam pela própria biblioteca (`createChunks`). Por isso saem cifrados quando a E2EE está ligada.
- Para apagar, a biblioteca tem `storeDeletionAtRevision(caminho, base)`, que grava a deleção (`deleted: true`) como
  filha da base, também com `force`. A guarda do `delete_note` pedida pelo maestro saiu barata, sem ticket seguinte.
- Para criar, `putDBEntryAsIndependentRoot` grava uma raiz nova. Duas criações ao mesmo tempo viram duas raízes, ou
  seja, um conflito, sem que nenhuma suma.

**Quando é conflito (mudança de desenho, que precisa de olho na revisão):** a resposta só é "conflito: releia e
refaça" quando a base já não era uma versão viva antes da gravação, isto é, quando a gravação abriu um ramo novo.
- Gravar com a versão viva de uma nota que já tinha conflito aberto grava, e a resposta avisa que o conflito segue
  aberto e que a resolução é no Obsidian, pelo aviso do LiveSync.
- O motivo: com a regra "há mais de uma versão, então é conflito", o "reler e regravar com a versão nova: grava" do
  aceite (faixa 5) responderia conflito para sempre, e o agente ficaria em laço.

**Modo local do upstream** (`VAULT_PATH`, decisão d): a versão é um hash do texto (`h-<16 hex>`). Base velha é
recusada com "conflito: releia e refaça; nada foi gravado", porque uma pasta não guarda duas versões.

**Não está no 09** (é do ticket 10): a regra curta nas descrições, a cabeça do `AGENTS.md` no `instructions`, as
três instâncias, `estado_do_hub` e o validador de frontmatter. As descrições ganharam só o necessário para o uso:
`base_rev` e `rev` explicados, em inglês como as do upstream. As respostas novas são em pt-BR.

### No hub: o passo 05 do kit

`agents/code/kit/par/05-mcp-banco.ps1` (módulo `mcp-banco/mcp-banco.psm1`), no contrato do kit:

| Uso | O que faz |
|---|---|
| `pwsh 05-mcp-banco.ps1 -EnvFile <par>.env` | confere o fork (`npm ci --ignore-scripts` se faltar `node_modules`; build se faltar `dist\main.js` ou se ele for mais velho que algum fonte de `src\` ou `lib\`) e sobe o MCP de escrita; idempotente (de pé, não religa) |
| `... -WhatIf` | só lista o que faria |
| `... -Descer` | para o MCP |

- Lê o mesmo `.env` do par do passo 04 (CouchDB, frase-senha, pasta de estado), mais três linhas do modelo
  `env/05.env.modelo`: `HUB_MCP_BANCO_DIR`, `HUB_MCP_BANCO_URL` e `HUB_MCP_BANCO_TOKEN`.
- A URL tem de ser `http://127.0.0.1:<porta>/mcp`; qualquer outra é recusada.
- Os segredos vão só no ambiente do processo, nunca na linha de comando.
- `DATA_DIR` fica em `<estado do par>\mcp-banco-<porta>`: sem isso, o upstream grava em `~\.obsidian-mcp`.
- O PID salvo só vale se o processo for `node` com o `dist\main.js` do fork e a marca `--hub-mcp-banco=<porta>`.
  Parar nunca mata processo alheio.
- Com a cifra ligada, liga `COUCHDB_OBFUSCATE_PROPERTIES` (o par do 07 ofusca os caminhos).

## Critérios do ticket

| Critério | Costura A (fork, CouchDB sem cifra) | Costura B (hub, par do 07 com cifra) |
|---|---|---|
| ler e gravar com a versão lida grava, e a leitura seguinte traz a versão nova | PASSA | PASSA; a gravação chega ao `.md` em 0,5 s |
| gravar com versão velha deixa as duas versões no banco e a resposta diz "conflito: releia e refaça" | PASSA | PASSA; 2 folhas pelo dispositivo leitor, e a versão do outro escritor fica intacta no `.md` |
| regravar nota existente sem a versão é recusado | PASSA | PASSA; o `.md` não muda |
| a leitura de nota em conflito avisa e lista as versões; a ferramenta de conflitos lista os abertos | PASSA | PASSA; cada versão listada se lê pelo `rev` |

### Costura A: e2e do fork

`npm run test:e2e:banco` (`scripts/e2e-banco.mjs` e `test/versao.e2e.test.ts`).
- Sobe o CouchDB 3.5.2 em `hub-ensaio-09-f`, só em 127.0.0.1:5996, com senha aleatória. Cria um banco novo por rodada
  e apaga o contêiner no fim, também quando falha.
- O MCP roda em 127.0.0.1:8796, com token.
- Olha de fora: as respostas das ferramentas e, direto no CouchDB, as folhas (`open_revs=all`) e o texto de cada uma,
  montado dos pedaços.
- 12 casos: os 4 critérios e mais base inventada, regravar sobre a versão relida com conflito aberto, os dois casos
  do `edit_note`, os dois do `delete_note`, o `move_note` e nota sem conflito sem aviso.

| Rodada | Resultado | Log (no fork, `.local/`) |
|---|---|---|
| vermelho: `src` de v0.10.0 com os testes novos | 11 falham, 1 passa (nota sem conflito lê sem aviso, o que o upstream já faz); a primeira falha é "read_note gave no base_rev" | `costuraA-vermelho.log` |
| verde, primeira volta | 11 de 12; a falha era do teste: o `open_revs=all` responde em multipart sem `Accept: application/json` | (sobrescrito) |
| verde, segunda volta | 11 de 12; a falha era do teste: duas leituras ao mesmo tempo, na mesma sessão e com o mesmo `id` JSON-RPC, e uma resposta se perdia (o servidor respondeu às duas em 12 ms, visto com `HUB_TESTE_LOGS=1`) | `costuraA-verde2.log` |
| verde | **12 de 12, saída 0** | `costuraA-verde.log` |

### Costura B: ponta a ponta no hub

`pwsh -NoProfile -File agents/code/test/09-mcp-banco.test.ps1`.
- O par do 07 de verdade, pelo `ensaio.psm1`: `hub-ensaio-09-a/b` nas portas 5996/5997, cifra e caminho ofuscado
  ligados, o hub de ensaio na pasta A.
- O passo chamado como o kit chama.
- O outro escritor é a vista `.md`: uma edição no disco que o sincronizador leva ao banco.
- As versões guardadas são lidas pelo dispositivo leitor do CLI (`Get-VersoesDaNota`).

| Rodada | Resultado | Log (`etapas/logs/`) |
|---|---|---|
| 1 | 14 PASSA, 5 FALHA: o agente e o outro escritor acrescentavam linhas diferentes no fim. A resposta foi "conflito", mas o sincronizador do LiveSync no par **fundiu as duas versões sozinho**, e ficou uma folha. É a fusão automática de mudanças que não se sobrepõem; no 07, o conflito ficou porque os dois mudaram a mesma linha. O teste mudou: conflito de verdade na mesma linha (o caso do aceite), e a fusão virou o caso 4b | `09-docker-1.log` |
| 2 | 19 PASSA, 1 FALHA: "reler e regravar" respondeu conflito | `09-docker-2.log` |
| 3 | o mesmo, agora com registro: a base era versão viva nas duas leituras. A causa: o passo só montava o fork quando faltava `dist\main.js`, e o `dist` era de antes da regra "só é conflito se a base não é viva". Conserto: o passo remonta quando um fonte é mais novo que o build (caso novo no teste sem Docker) | `09-docker-3.log` |
| 4 | **21 PASSA, saída 0**; nenhum contêiner nem pasta `hub-ensaio-09-*` sobrou | `09-docker-4.log` |

O que a rodada 4 conferiu, além dos critérios:
- o `-WhatIf` não sobe o MCP nem grava arquivo;
- o passo de novo não religa (mesmo PID);
- reler e regravar com a versão nova numa nota com conflito aberto grava, chega ao `.md` em 0,5 s, e a resposta avisa
  que o conflito segue aberto;
- linhas diferentes com a versão velha (4b): a resposta é "conflito", e depois o sincronizador fundiu as duas
  mudanças numa versão, sem perder nenhuma;
- o `-Descer` para o MCP.

### Sem Docker, na suíte comum

`agents/code/test/09-mcp-banco-sem-docker.test.mjs`, que chama `banco/mcp-banco-sem-docker.ps1`: 12 PASSA (1 teste do
`node --test`, verde antes e depois da junção).
- Confere: o `-WhatIf` só lista e não grava; `0.0.0.0`, `localhost` e falta de token são recusados; o PID de um node
  alheio, ou de outra porta, não vale.
- O build conta como velho sem `dist\main.js`, ou quando um fonte é mais novo que ele; não conta quando é mais novo
  que os fontes.
- Esse teste passou de primeira, sem fase vermelha: o passo foi escrito antes dele. O teste de ponta a ponta (B) foi
  escrito antes de qualquer rodada do passo.

### Testes do upstream

Medidos antes da mudança, em v0.10.0, nesta máquina:
- Unitários (`node --import tsx --test "src/**/*.test.ts"`, com `TEMP` em caminho longo): 271 passam e 1 falha
  (`listNotes` "lists all .md files recursively": separador `\` do Windows).
- Com o `TEMP` curto (`GUSTAV~1.DEL`), 20 falham: o `realpath` devolve o caminho longo e a guarda de caminho do modo
  local recusa.
- No Windows, `npm test` acha 0 testes: as aspas simples do glob no `package.json` não são tiradas.
- e2e local (`test/e2e.test.ts`): 34 passam e 7 falham na base, as mesmas do separador `\`.

Depois da mudança:
- Unitários: 272 e 1, com o caso novo do `readOnlyVault` (as gravações com versão também recusadas na instância de
  leitura).
- e2e local: 36 e 7, as mesmas 7 da base. Três testes do upstream mudaram para a regra nova: a troca de trecho, mover
  e apagar agora passam a `base_rev`. Ganharam dois casos: recusa sem base, e base velha no modo local.
- O servidor do e2e local às vezes não sobe nos 10 s do teste com a máquina carregada. Aconteceu duas vezes; rodado
  de novo, passou.

## O que vai doer ao ligar

- **A resposta "conflito" pode não durar.** Com o sincronizador do LiveSync rodando no par, um conflito de mudanças
  em linhas diferentes é fundido sozinho logo depois (caso 4b). O agente recebe "conflito: releia e refaça", e a
  releitura já mostra a versão fundida, sem aviso. Nada se perde, e reler e refazer continua o caminho certo. Mas a
  fusão é do LiveSync, não do agente, e ninguém a revisa. Só a colisão na mesma linha fica como conflito para a pessoa.

- **Conflito que só cresce.** Ninguém pelo MCP fecha um conflito: a resolução é a pessoa, no Obsidian, e a tela de
  colisão é ticket seguinte. Cada gravação atrasada abre mais um ramo. O `get_conflicts` mostra quantos há.
- **Compactação do CouchDB.** A compactação apaga o corpo das revisões antigas. Depois dela, uma `base_rev` velha
  (não folha) some, e a gravação é recusada como "base que a nota nunca teve", em vez de virar conflito. É seguro (nada
  grava às cegas), mas a mensagem engana. Política de compactação: ponto aberto da faixa 5.
- **Leitura enquanto o outro par replica.** O MCP lê e grava direto no CouchDB do par. A versão do outro par só existe
  aqui depois da replicação. Uma gravação feita nesse intervalo vira conflito quando a replicação chega, que é o
  caminho certo, mas o agente não recebe a resposta "conflito" na hora: só a próxima leitura avisa.
- **`package-lock.json` do fork:** o `npm install` tirou o `jose` 5.10.0 (opcional, peer). A mudança ficou fora dos
  commits; o passo 05 usa `npm ci`.
- **MCP depois de o banco ser recriado:** não testado aqui (ponto aberto da faixa 5).

## Rodada 2 (consertos do parecer da rodada 1)

Parecer: `etapas/parecer-09-Cinzel.md` (VOLTA, 3 consertos). Levados ao `ticket-09` por fast-forward, árvore igual à
testada pelo Fiel no Docker:

- Fork `ticket-09` em d2a5a40: duas gravações ao mesmo tempo da mesma base. Também é conflito quando aparece uma folha
  que não estava antes da gravação e não é a dela: quem chega depois ouve "conflito: releia e refaça" (antes, as duas
  ouviam "saved"). Quem chega primeiro pode ainda ouvir "saved"; a leitura seguinte mostra o CONFLITO. `move_note` com
  conflito ou recusa na origem diz que o destino já foi gravado. Dois casos novos no `test/versao.e2e.test.ts`.
- Hub `ticket-09` em ca17738: o passo 05 religa o MCP quando o `dist` é mais novo que o processo; caso novo no
  `09-mcp-banco.test.ps1`.
- Testes (Fiel, com a trava, 05h02–05h05): fork 16/16 (com a sonda dele); hub 21 PASSA. Hub sem Docker 1/1.

## Uso de harness e login

Nenhum. O 09 não chama Claude Code, Codex nem Copilot, e não copiou login. Nada foi gravado em `~`.
