# Ticket 16: costuras propostas (Trilho, 2026-10-17 ~04h50)

Ramo `ticket-16`, worktree `C:/context-hub-wt/ticket-16`, de `integracao` 33b817a. Fora daqui: telas, hooks de início,
`notify`, mod e `statusLine` (ticket 17); tarefa agendada e laço do kit (23, 24).

## Onde mora
`agents/skills/vigia/` (o agente chama o `recuperar`; o spec diz "skill com scripts, como a nova iniciativa"):
`vigia.mjs` (comandos `passada` e `recuperar`) e `SKILL.md`. O estado continua por `agents/code/bin/lib/vigia.mjs`
(o 27 e o 31 já gravam itens por ele); a passada regrava o arquivo inteiro e guarda os itens dos outros
(`fim-da-resposta`, `acervo-peca-sumida`, `copia-diaria`).

## Costuras (o teste só olha o lado de fora)
1. **`vigia passada --env <par>.env`** → `<hub>/.local/vigia/estado.json` e a notificação.
   - Sem Docker, na suíte comum: CouchDB dublê (servidor HTTP local com respostas gravadas de `_scheduler/docs` e do
     outro par) e leitor dublê (CLI falso, no molde do `cli-falso.cjs` do 07: `sync`, `ls`, `info`, `pull-rev`).
     Notificador dublê por variável (`HUB_VIGIA_NOTIFICAR`, o comando recebe o texto; o teste lê o registro).
   - Cenários agora: tudo em ordem; conflito de texto citado pelo caminho decifrado; replicação parada há mais de
     15 min com o outro par ligado (`divergencia`); outro par sem resposta (`informa`, com o motivo, sem suprimir a
     replicação parada); item `copia-diaria` de exemplo (`informa`, com notificação); itens de outros preservados.
   - Notificação: mesma passada duas vezes, uma só; piora na terceira, nova.
2. **`vigia recuperar <caminho> --env <par>.env`** → arquivo ao lado do original com os bytes da versão perdida;
   nada apagado. Mesmo leitor dublê.
3. **Ponta a ponta com Docker** (pela fila): dois pares do `ensaio.psm1` do 07 com E2EE, portas próprias
   (5996/5997). Conflito de texto forjado e binário com ramo apagado: o estado cita os dois pelo caminho em claro; o
   `recuperar` devolve os bytes. Teste em PowerShell, como o `07-banco.test.ps1`.

## Escolhas técnicas (decido se ninguém objetar)
- O caminho em claro vem de um **dispositivo leitor** da vigia (banco local próprio do CLI, como o `Get-Leitor` do
  ensaio do 07): `sync`, `ls` (o `*` marca conflito), `info`, `pull-rev`. O daemon trava o banco local dele, por isso o
  leitor é outro. Sem decifrar no Node.
- Outro par: `HUB_OUTRO_PAR_URL` respondeu = ligado; sem resposta = `informa` "outro par sem resposta; não sei se está
  desligado"; nunca `ok`.

## Perguntas
1. **"Piora"** (ponto aberto do spec): proponho "um item passa a ter nível acima do que tinha na passada anterior
   (item que não existia conta como `ok`)". Item novo de `informa` notifica (o spec pede notificação no
   `copia-diaria`). Ficar igual ou melhorar não notifica.
2. **Ramo apagado** (para o `recuperar`): forjo com o `resolve <path> <rev>` do CLI? É o que a resolução por `mtime`
   do 08 faz? Pergunto à Brasa. O leitor só recebe as folhas no `sync`, então o corpo da versão apagada pode não estar
   nele: o desenho do `recuperar` depende disso, e vou provar no Docker antes de escrever.
3. Lugar `agents/skills/vigia/`: confirma? O spec diz "a confirmar pelo Prumo".

## Respostas (2026-10-17 ~05h00)
- Maestro: costuras aceitas; piora = item sobe de nível em relação à passada anterior; item novo conta como `ok` antes;
  item que desce e volta a subir notifica de novo. Lugar `agents/skills/vigia/`.
- Brasa (pelo fonte do CLI 14141446, sem Docker ainda): o **daemon** apaga o ramo perdedor do binário
  (`conflictResolution/operations.ts` → `deleteRevisionFromDB` → `deleteDBEntryByPath(path, {rev})`): `get` da rev
  perdedora, `_deleted = true` no documento inteiro (children, path, mtime, size ficam) e `put`. A folha apagada
  replica; os pedaços `h:` ficam. Forjar fiel: `GET <db>/<id>?rev=<perdedora>` e `PUT` do mesmo corpo com
  `_rev=<perdedora>` e `_deleted:true`. O `pull-rev` recusa revisão apagada. Receita de recuperar
  (`Restore-RamoApagado`, `agents/code/test/banco/ensaio.psm1` no ramo ticket-08): `_replicate` para `<db>-recupera`,
  `PUT` do corpo sem `_deleted` na cópia, sal no `_local` da cópia, leitor apontado para a cópia faz `sync` +
  `pull-rev` da rev nova. Detalhes em `etapas/relatorio-08-banco-limites.md`, "Achados".
- Plano da leitura: `_changes?style=all_docs` acha documentos com mais de uma folha; `GET <id>?open_revs=all` dá as
  folhas (viva em conflito = conflito; apagada com `children` = binário descartado). O caminho em claro vem do `ls` do
  leitor: a rev vencedora do documento cru é a rev que o `ls` mostra para o caminho.

## Combinado com o Cinzel (ticket 10, 2026-10-17 ~05h)
- O `estado_do_hub` devolve o `estado.json` como está, sem o campo `vistos`; sem arquivo ou ilegível, "estado indisponível".
- Passada com mais de 15 min: devolve o JSON e o aviso "a vigia não roda desde <hora>" (sugestão minha, aceita pelo maestro). Sem `passada`, sem aviso.

## Feito até 60756e6
- `agents/skills/vigia/{vigia.mjs,notificar.ps1,recuperar.ps1,SKILL.md}`; `gravarPassada` em `agents/code/bin/lib/vigia.mjs`; leitor da vigia no passo do banco do kit (`HUB_VIGIA_LEITOR_DB`).
- Testes: `agents/code/test/16-vigia.test.mjs` 8/8 (sem Docker); `agents/code/test/16-vigia.test.ps1` (Docker, pela fila) a rodar.
- Achado para o maestro: `agents/skills/busca/SKILL.md` ainda cita a ferramenta `read` do hub-busca, que o 12 r3 tirou dos harnesses.
- Conserto do 12 (pedido do maestro), commit separado b4e7272: agents/skills/busca/SKILL.md não cita mais a read do hub-busca. Vai para o relatório do 16.

## Cenários do 08 na passada (2026-10-17 ~08h45; proposta ao maestro)
A passada chama o kit do 08 por um pwsh só (`Read-EnvPar` do .env do par): `Get-AcimaDoLimite`, `Get-PidSincronizador`,
`Update-Exclusoes` (o gerador), `Stop-`/`Start-Sincronizador`. Costura do teste: a mesma `vigia passada --env`.
1. **Binário descartado**: `_changes?style=all_docs` → documentos com mais de uma folha → `open_revs=all`; folha apagada
   com `path` ao lado da viva = descartado. Caminho em claro: a rev viva casada com a rev do `ls` do leitor.
   `divergencia`. "Até o Gustavo olhar" (aberto no spec): proposta, sai com `vigia recuperar` dele ou `vigia olhei
   <caminho>`; guardado por rev em `.local/vigia/olhados.json`. Dublê: o retrato `binario-ramo-apagado.json`.
2. **Acima de 200 MiB**: `Get-AcimaDoLimite`; um item `divergencia` por arquivo, com o caminho.
3. **Sincronizador parado**: `Get-PidSincronizador` vazio → `informa` (não é uma das três divergências; o laço religa
   em até 1 min). Dublê: o CLI falso ganha `daemon`.
4. **Laço**: o que o laço fez desde a passada anterior (`laco.log`) → `informa` "o laço religou ... às HH:MM".
5. **Gerador a cada passada** (decisão 2026-10-16 20:38): `mudou` → para e religa o sincronizador, item `informa`;
   código 2 → item `informa` com o caminho do `index.md` ilegível, sem religar.
6. **Config Doctor** (sem detector no spec): no fonte do plugin 1.0.35, o Doctor abre na partida quando
   `checkUnsuitableValues(settings).version != settings.doctorProcessedVersion`. Detector: `doctorProcessedVersion` do
   `<hub>/.obsidian/plugins/obsidian-livesync/data.json` diferente da versão da `DoctorRegulation` no `main.js`
   instalado → `informa` "Config Doctor pendente: o sync do Obsidian para até você responder". Plugin ausente: sem item.
   Não verificado com o Obsidian aberto.
