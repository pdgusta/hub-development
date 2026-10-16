# Relatório da etapa zero, banco: prova 1 (ticket 01)

Brasa, 2026-10-16. Ramo `ticket-01` (worktree `C:\context-hub-wt\ticket-01`, a partir de `integracao` e com ela juntada
em 3857c98). A prova 2 (pastas com ponto, ticket 02) passou para a Vela, no ramo dela.

- 2026-10-16: Brasa parou a pedido; até aqui só li as regras e o brief e listei o material (nenhum código, worktree ou contêiner).

## Prova 1: dois CouchDB replicando com o LiveSync. **Passou.**

### O que foi montado (forma do kit, não arranjo de teste)

Tudo em `agents/code/test/provas/01-banco/`:

- `compose.yml`: **um** CouchDB 3.5.2 por par; o mesmo arquivo serve aos dois, e o par muda só pelo `.env`
  (`docker compose -p <contêiner> --env-file <par>.env`). Porta só em `127.0.0.1`.
- `couchdb.ini`: o `couchdb-init.ini` do es617 (o do spike), sem `[admins]` nem `uuid` fixos.
- `04.env.modelo`: os nomes das variáveis (`HUB_BANCO_CONTEINER`, `HUB_BANCO_PORTA`, `HUB_BANCO_INI`, `COUCHDB_USER`,
  `COUCHDB_PASSWORD`, `COUCHDB_DATABASE`, `COUCHDB_PASSPHRASE`, `HUB_BANCO_SAL`, `HUB_OUTRO_PAR_URL`/`_USER`/`_PASSWORD`,
  `HUB_ROOT`, `HUB_LIVESYNC_DB`, `HUB_LIVESYNC_CLI`). Os `COUCHDB_*` são os do compose do es617, que o MCP do banco usa.
- `banco.psm1`: as funções do kit (subir o par, gravar o sal, ligar a replicação de envio, configurar o dispositivo,
  subir o sincronizador, derrubar). O ticket 07 leva isto para `kit/par/04-banco.ps1`.
- `prova.ps1`: o teste de ponta a ponta. Costura: as duas pastas no disco e os documentos crus dos dois CouchDB.

Sequência de um par, como a prova faz: o CouchDB sobe → bancos `_users`, `_replicator` e `hub` → o kit grava o **mesmo**
sal da E2EE em `_local/obsidian_livesync_sync_parameters` dos dois bancos → uma replicação de envio no `_replicator` de
cada par (`hub-envio-para-b` no A, `hub-envio-para-a` no B; S3) → o CLI se configura pelo caminho dos testes oficiais
(`init-settings --force`, `remote-add hub sls+http://…?db=hub`, depois os campos `liveSync`, `encrypt`, `passphrase`,
`usePathObfuscation`, `E2EEAlgorithm v2`, `syncMaxSizeInMB 200`, `isConfigured`) → `mark-resolved` → `daemon --vault`.
A pasta A nasce com o hub de ensaio do `montar.mjs` da ponta de `integracao`; a B nasce vazia.

Material: CouchDB `couchdb:3.5.2`; CLI do LiveSync do spike, commit `1414144` (o `14141446` do ticket 48), sem
recompilar (`C:\Projetos\spike-livesync\livesync-src\src\apps\cli\dist\index.cjs`); Node 24.19; Docker 29.8.

### Evidência

Comando: `pwsh -NoProfile -File agents/code/test/provas/01-banco/prova.ps1` (sai 0 quando tudo passa). Commits
43a4ea9, 246393b e 0c8c639 (montar.mjs em `agents/code/test`, depois do ticket 05).

Depois de juntar `integracao` em 0d04985 (tickets 02 e 05), rodada de novo do HEAD 0c8c639: **tudo passou**; o hub de
ensaio, agora com 90 arquivos, chegou ao B em 16,3 s, e as travessias levaram de 0,5 a 2,1 s. A rodada abaixo é a de
antes do merge.
Rodada final, com E2EE e caminho ofuscado (a escolha aceita):

```
[PASSA] replicação de envio do par A em running (running)
[PASSA] replicação de envio do par B em running (running)
[PASSA] hub de ensaio A->B (44 arquivos) em 3,9 s
[PASSA] nota criada A->B em 2,1 s
[PASSA] nota editada volta B->A em 1,6 s
[PASSA] nota apagada A->B em 1,0 s
[PASSA] nota criada B->A em 1,6 s
[PASSA] nota editada volta A->B em 1,0 s
[PASSA] nota apagada B->A em 0,5 s
[PASSA] base da colisão chegou ao B
[PASSA] cada par gravou a sua versão no próprio banco com a replicação pausada
[PASSA] conflito no banco do par A (1 documento com _conflicts)
[PASSA] as duas versões guardadas no banco do par A (2 folhas)
[PASSA] conflito no banco do par B (1 documento com _conflicts)
[PASSA] as duas versões guardadas no banco do par B (2 folhas)
[VÊ] disco do par A com o conflito aberto: # Colisão  Linha mudada no A marca-b49ea93d.
[VÊ] disco do par B com o conflito aberto: # Colisão  Linha mudada no B marca-b49ea93d.
[PASSA] nada em claro no banco do par A
[PASSA] nada em claro no banco do par B
prova 1: tudo passou
```

Os critérios do ticket:

| Critério | Resultado |
|---|---|
| Criada, editada e apagada no A chega ao B, e vice-versa | Passou, de 0,5 a 2,1 s (limite do teste: 30 s) |
| Mesma linha nos dois pares com a replicação pausada vira conflito nos dois bancos, sem versão perdida | Passou: `_conflicts` no documento da nota nos dois CouchDB, e as duas folhas lidas com o texto de cada par |
| Com E2EE e caminho ofuscado, o mesmo vale e nada em claro nos documentos crus | Passou: nos `_all_docs` crus dos dois bancos, nada da marca da rodada, de trechos do texto nem dos nomes (`nota-de-a`, `nota-de-b`, `colisao`, `teste/`) |
| Contêineres apagados ao fim | Sim: a prova derruba os dois (`down -v`) e apaga a pasta do ensaio no `finally` |

Também rodados:

- **Sem cifra** (`-SemCifra`): tudo passou (sem o caso "nada em claro"); travessias de 0,5 a 2,1 s, hub de ensaio em
  3,2 s.
- **Contraprova sem o sal comum** (`-SemSalComum`): **falha, como esperado**. O B lê o próprio sal (`GET
  …/_local/obsidian_livesync_sync_parameters -> 200`) e não decifra o que veio do A: `{"status":"failed","error":
  {"message":"The operation failed for an operation-specific reason","name":"OperationError"}}` (WebCrypto), e o `daemon`
  sai com `[Daemon] Initial replication failed, cannot continue`. Isso prova que o passo do kit que grava o sal é
  necessário.
- **`couchdb.ini` em CRLF** (como o `core.autocrlf=true` desta máquina deixa num checkout novo): tudo passou.

Como o conflito é lido com a cifra ligada: o caminho no CouchDB é cifrado (`f:c4aae2…`), então a prova acha o
documento em conflito pelo `_conflicts` cru e lê as folhas por um **dispositivo leitor** (um CLI com banco local
próprio: `sync`, `info <caminho>`, `cat-rev <caminho> <rev>`), que dá o caminho em claro. É o caminho que o spec
descreve para a vigia (faixa 7).

### Achados no caminho (cada um quebrou a prova uma vez)

1. **O sal da E2EE não replica.** O sal mora em `_local/obsidian_livesync_sync_parameters`, e documento `_local` não
   viaja na replicação do CouchDB. Sem o mesmo sal nos dois bancos, o B não decifra nada (contraprova acima). O kit grava
   o mesmo sal (32 bytes, base64; `HUB_BANCO_SAL`) nos dois bancos **antes** do primeiro dispositivo. O milestone
   (`_local/obsydian_livesync_milestone`: aceite dos dispositivos e trava) também é `_local`: cada banco tem o seu, e cada
   dispositivo é aceito no banco do próprio par.
2. **Cofre sob pasta com ponto não sincroniza nada.** O observador do CLI ignora `/(^|[/\\])\./` aplicado ao caminho
   **absoluto** (`src/apps/cli/managers/CLIStorageEventManagerAdapter.ts`, `baseIgnored`). Com o ensaio em
   `<worktree>\.local\`, nenhuma mudança chegou ao banco, sem erro nenhum. A raiz do ensaio passou para
   `%TEMP%\hub-ensaio-<nome>`. Avisei a Vela (ticket 02).
3. **O CouchDB regrava o `.ini` montado.** Ele escreve `[admins]` (com o hash), `uuid` e `secret` de volta no último
   arquivo de `local.d`, que era o nosso `couchdb.ini`. Com os dois pares montando o mesmo arquivo, os admins se
   misturaram e o login falhou. O kit copia um `.ini` por par (`HUB_BANCO_INI`), e o compose monta a cópia.
4. **O CouchDB 3.5 trava o usuário depois de logins falhos** ("Authentication rejected for locked-out user"). O kit
   espera o `_up` **sem** credencial e só depois autentica.
5. **O node cai ao sair no Windows** (`Assertion failed: !(handle->flags & UV_HANDLE_CLOSING), file src\win\async.c, line
   94`) depois de o comando terminar (`[Verification] … ACCEPTED`, `[Done] Command 'mark-resolved' completed`). O código
   de saída fica diferente de 0 com o comando feito. O kit confere a linha `[Done]` (e o `ACCEPTED` no `mark-resolved`),
   não só o código.
6. Sem `--verbose`, o `daemon` não escreve "NOW TRACKING"; o sinal de pronto é `[Daemon] LiveSync active` (stderr).

### O que vai doer ao ligar

- **O sal no par novo.** O par 2 (notebook) precisa receber o sal junto com a frase-senha, ou o kit copia o documento
  `_local/obsidian_livesync_sync_parameters` do par 1 para o banco do par 2 antes de o CLI do par 2 rodar. Se o CLI ou o
  plugin do par 2 tocar o banco vazio antes, ele gera um sal próprio e o par fica mudo, com `OperationError` só no log.
  A vigia (faixa 7) deveria conferir que os dois bancos têm o mesmo sal. Se o banco for recriado (assistente do plugin,
  "rebuild"), o sal muda e precisa ser regravado no outro par.
- **O plugin no Obsidian não foi exercido.** O plugin entra pelo Setup URI; com E2EE, o URI carrega a frase-senha, mas o
  sal vem do banco. Falta ver que o plugin aponta para o CouchDB local e usa o sal já gravado, sem recriar o banco (ticket
  30: o assistente destrói e recria). Com o plugin aberto, o modal de conflito deveria abrir nos dois cofres; só o CLI foi
  visto aqui.
- **Conflito aberto deixa os discos diferentes.** Com o plugin fechado, o disco do A ficou com a versão do A e o do B
  com a do B, sem marca nenhuma na nota. Nada se perde (as duas folhas estão nos dois bancos), mas um agente que lê o
  disco do B vê só a versão do B. A vigia e o `read_note` com aviso de conflito (faixas 5 e 7) é que mostram.
- **Endereço do outro par.** No ensaio, a replicação sai do contêiner para `host.docker.internal:<porta>`. Na tailnet, o
  `HUB_OUTRO_PAR_URL` vira o endereço Tailscale do outro par, e o CouchDB precisa escutar nessa interface, não só em
  `127.0.0.1` (não decidido, ponto aberto do 34). A replicação leva o usuário e a senha do outro par no `_replicator`:
  cada par guarda a credencial do outro.
- **Replicação parada em silêncio.** Na prova, pausar = apagar o documento do `_replicator`; ao recriar, ela retoma. Com o
  outro par desligado, o estado da tarefa no `_scheduler/docs` é o que a vigia lê (não testado aqui).
- **Pastas com ponto.** O hub de ensaio tem `.git` e `.gitignore` na raiz; ficaram fora (primeiro nível). As aninhadas e
  o `.livesync/ignore` são a prova 2 (Vela). O achado 2 vale também para o hub de verdade: `C:\context-hub` não pode
  morar sob pasta com ponto.
- **O CLI do spike.** É o build com uma linha de log a mais (`[teste48] …`, ticket 48) e mora fora do hub. O kit precisa
  de um lugar fixo para o build e de um jeito de refazê-lo no notebook (o 48 diz como: `npm install` e `npm run build -w
  self-hosted-livesync-cli`, sem compilador).
- **Tarefa agendada.** Na prova, o `daemon` roda como processo em segundo plano. O laço de minuto do Agendador (48) e o
  sinal de pronto (`LiveSync active`) ficam para o ticket 07.
- **Segunda máquina.** Tudo aqui é nesta máquina, com dois CouchDB em portas diferentes. A latência da tailnet, o par
  desligado por dias e a volta dele não foram vistos.

### O que muda no spec

Nada falhou. Acréscimos para o bloco do Worker 4 e o ticket 07:

- o kit grava o mesmo sal da E2EE nos dois bancos (`HUB_BANCO_SAL`) antes do primeiro dispositivo;
- um `couchdb.ini` por par (`HUB_BANCO_INI`), porque o CouchDB grava admin, `uuid` e `secret` nele;
- esperar o CouchDB sem credencial (trava de usuário);
- conferir a linha `[Done]` do CLI, não só o código de saída;
- o hub e os cofres de ensaio fora de qualquer pasta com ponto.

### Limpeza

Os contêineres `hub-ensaio-00-a` e `hub-ensaio-00-b`, os volumes e as redes foram apagados a cada rodada
(`docker ps -a --filter name=hub-ensaio-00` e `docker volume ls --filter name=hub-ensaio-00` vazios). A pasta
`%TEMP%\hub-ensaio-00` foi apagada. Os processos do CLI foram parados só pelo PID que a prova abriu. A imagem
`couchdb:3.5.2` fica no Docker (baixada para a prova). Os logs das rodadas estão em `C:\context-hub-wt\ticket-01\.local\`
(fora do git).
