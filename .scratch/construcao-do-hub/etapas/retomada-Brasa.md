# Retomada da Brasa

Atualizada em 2026-10-17 ~04h. Regras novas: um subagente por vez (tarefa leve) e até três Haiku esforço médio (só simples ou QA; conferir o que trazem). Papel: construtora. Regras em `etapas/regras-da-construcao.md`: leia inteiras, em
especial "Um trabalho pesado por vez" (a trava `etapas/trava-pesada.md`) e "Testes com harness de verdade".
- Revisores: Fiel e Fielzinho, em dupla (o Fiel fecha).
- Integrador: Rebite (`maestri ask "Rebite" ...`, depois do "passa").
- Maestro: `maestri ask "Claude Code" ...`.
- Fila: o ticket 07 agora, depois o 08 (receita da etapa 2, opção A).

## Ticket 22 (proxy e kit de cliente): construindo

- Ramo `ticket-22`, worktree `C:/context-hub-wt/ticket-22`, de `integracao` 9cc878b. Costuras aceitas pelo maestro (comentário no ticket 22); (4) sim: uma sessão de cada harness como cliente depois do Docker verde, modelos baratos, trava e aval de login.
- Feito (sem Docker verde): `agents/code/kit/cliente/ligar-cliente.ps1` (três harnesses, Bearer de variável `HUB_PROXY_TOKEN_*`, -Escrita, contrato em bloco marcado em CLAUDE.md/AGENTS.md/copilot-instructions.md, lançador `copilot-hub.cmd` em -Saida; sem -Contrato lê `AGENTS.md` por read_note na rota de leitura); `agents/code/kit/par/10-proxy.ps1` + `proxy/proxy.psm1` (TBXark/mcp-proxy 1.1.0, SHA-256 do pacote e do exe fixos, config com `${VAR}`, autoReconnect, pronto = `/_readyz` 200 e cada rota 401 sem token; ponte Desktop `mcp-remote@0.14.3` com `--header-file` e pasta conectada em `<estado>/desktop/`); `env/10.env.modelo` (HUB_PROXY_ADDR=127.0.0.1:8790). Testes: `node --test agents/code/test/22-kit-cliente.test.mjs agents/code/test/22-proxy-sem-docker.test.mjs` (MCP falso `test/proxy/mcp-falso.mjs`).
- Achados: a flag `--allow-all-mcp-server-instructions` do Copilot não tem chave de config (lançador); o `tar` no PATH do Git Bash é o do MSYS (usar System32	ar.exe); o `after` do ajudante da pasta roda antes do meu: descer processos no `finally` do teste.
- Fork: worktree minha `C:/Projetos/hub-mcp-banco-wt/brasa-22` (destacada em integracao 34c3e50; a `integracao` do fork é do Rebite, não montar lá). Rodar o Docker com `$env:HUB_MCP_BANCO_DIR='C:/Projetos/hub-mcp-banco-wt/brasa-22'` (o passo 05 faz npm ci e build: pesado, com a trava). Fila: item 5.
- Falta: teste Docker `agents/code/test/22-proxy.test.ps1` (escrito, 69fbf09) (par do 07 com 5996/5997? conferir portas livres; fork `C:/Projetos/hub-mcp-banco-wt/integracao`; busca real com `iniciar.ps1`; cliente HTTP pelo proxy; Host; instructions medido; ponte do Desktop rodada uma vez com npm cache no ensaio); depois os harnesses reais; relatório `etapas/relatorio-22-proxy-e-kit-de-cliente.md`; revisão.

## Ticket 08 (banco: limites e robustez): em revisão com o Fiel; a fatia 2 pendente

- ~08h20: r2 PASSA de código (Fiel e Fielzinho); NÃO levar ao Rebite ainda. Na hora quieta (maestro avisa; fila), rodar as fatias 1 e 2 NUMA SUBIDA: `Start-Process pwsh -WindowStyle Hidden -ArgumentList '-NoProfile','-File','C:/context-hub-wt/ticket-08/.local/fatias.ps1','-Fatias','1+2'` (log `etapas/logs/08-fatias-1-2.log`; o corredor chama o teste por -Command, porque por -File `-Fatias 1,2` vira 12). Depois avisar o Fiel, que fecha o passa.
- ~08h: r1 VOLTA por 1 conserto (`Get-AcimaDoLimite`), feito em 514db7a; r2 pedida ao Fiel. O Fiel roda as fatias 1 e 2 no Docker (a 2 na hora quieta).

- ~07h: revisão pedida ao Fiel (decisão do maestro) com a fatia 2 pendente no relatório. Ponta 124f43d (integracao 9cc878b juntada; sem Docker verde). A fatia 2 roda quando o maestro disser que a máquina está quieta; o Fiel fecha a rodada com ela. Passos 1 e 3 abaixo: o 3 já foi.

- Ramo `ticket-08`, worktree `C:/context-hub-wt/ticket-08`, ponta b02fa4f (com `integracao` 9453e3e juntada em 68fc451).
- Costuras confirmadas pelo maestro ~03h15 (comentário no ticket 08). Retrato em `agents/code/test/banco/retrato/`.
- Docker verde: fatias 1 (03h37), 3 a 7 (06h20 a 06h39) e o teste do 07 (06h39, 24 PASSA). Logs em
  `etapas/logs/08-fatia-N.log`; estado do corredor em `etapas/logs/08-fatias.status`.
- Relatório `etapas/relatorio-08-banco-limites.md` com a tabela preenchida, menos a fatia 2.

### Feito

- 5110f3f: `Write-TarefaSincronizador` (XML em `<estado>/tarefa-sincronizador.xml`, nunca registrado; o teste o valida
  pelo COM `Schedule.Service` com `NewTask(0).XmlText`, sem registrar), `Invoke-VoltaLaco` e `kit/par/banco/laco.ps1`,
  passo novo no `Install-ParBanco`.
- 08ce7c7: `Get-AcimaDoLimite` (`$script:LimiteMiB`); em `test/banco/ensaio.psm1`: `Get-InfoNoBanco`, `Get-FolhasCruas`,
  `Get-RamosApagados`, `Restore-RamoApagado`; teste `agents/code/test/08-banco-limites.test.ps1` com 8 fatias
  (exclusões; 60/201 MiB; colisão de binário e recuperação antes e depois da compactação; conflito de texto aberto;
  retrato em dia; kit de novo; laço; retrato parado). Retrato vai para `agents/code/test/banco/retrato/`.
- Sem Docker: `pwsh -NoProfile -File agents/code/test/banco/kit-sem-docker.ps1` tudo passou.

### Armadilhas

- Arquivo grande gravado direto no hub derruba o observador do CLI (EBUSY) e o CLI sai ("Exiting for systemd restart"):
  o laço é o supervisor. No teste, `New-Aleatorio` escreve fora do hub e move (só a fatia 2 usa `-Direto`, de
  propósito), e as esperas de binário usam `Espera-ComLaco`.
- Com o caminho ofuscado, a folha apagada se reconhece pelo `path` (o `children` em claro vem vazio); `open_revs` só em
  JSON com `Accept: application/json`, e o array vem como um item só (achados do Trilho, ticket 16).
- `@($null).Count` é 1: conferir `$null -ne` antes de contar.
- O Docker roda no WSL (`vmmemWSL`), que cresce com a carga; 60 MiB nos dois bancos derrubou a memória livre para 513 MB.
- Python em heredoc com caminho do Windows estraga `\t` e `\0`: usar o Edit ou `chr(92)`; conferir caracteres de
  controle com `grep -a -P '[\x00-\x08]'`.
- Nunca deixar o corredor esperar a trava sozinho: ele passava à frente da fila (05h47). Agora sai se ocupada.

- O CLI resolve colisão de binário sozinho pelo `mtime` (`conflictResolution/operations.ts`, isBinary) e apaga a
  perdida com `_deleted` sobre o corpo inteiro (`EntryManagerImpls.js`). O `pull-rev` recusa revisão apagada: a
  recuperação copia o banco (`_replicate`), reabre a folha com PUT do mesmo corpo sem `_deleted`, grava o sal na cópia
  e tira o arquivo por um leitor apontado para a cópia.
- Docker só pelo corredor `.local/pesado.ps1 <teste> <rótulo>`: espera a trava, cria sem sobrescrever (CreateNew),
  piso de 2 GB livres, apaga a trava no fim. Registro em `.local/pesado.log`.

### Próximo passo exato

1. A fatia 2 (51 e 201 MiB; a03b3ac) numa hora de máquina quieta que o maestro combina (fila, último item). Lançar
   destacado: `Start-Process pwsh -WindowStyle Hidden -ArgumentList '-NoProfile','-File','C:/context-hub-wt/ticket-08/.local/fatias.ps1','-Fatias','2'`
   e vigiar `etapas/logs/08-fatias.status` (Monitor com tail -F).
   - O corredor (cópia em `etapas/logs/08-corredor-fatias.ps1`): sai se a trava estiver ocupada na partida; piso de
     2 GB antes de cada fatia (20 min: SEM-MEMORIA, avisar o maestro); corte abaixo de 700 MB, com limpeza; cede entre
     fatias com `.local/ceder` (nome de quem) ou o Codex do 15 depois das 06:58, e aí PARA e anota o que falta.
   - Ao pegar a trava: tirar o meu nome da fila. Ao soltar: avisar o primeiro da fila.
2. Preencher a linha da fatia 2 no relatório; `git merge integracao` se andou; teste sem Docker
   (`pwsh -NoProfile -File agents/code/test/banco/kit-sem-docker.ps1`). Sem a suíte inteira (só o Rebite, na junção).
3. Pedir a revisão ao Fiel: ramo `ticket-08`, relatório `etapas/relatorio-08-banco-limites.md`.

## Ticket 07 (fechado: juntado e resolvido, integracao 763813a)

- Ramo `ticket-07`, worktree `C:/context-hub-wt/ticket-07`. Ponta `6b1d7e8` (consertos da r2) sobre 99ea624 (`integracao` 57e85cf juntada).
- Rodada 2 voltou (parecer `etapas/02-banco/parecer-Brasa.md`, seção "Rodada 2"); consertos feitos, relatório seção "Rodada 3".
- Suíte comum em 99ea624, com a trava e `--test-concurrency=1`: 179 PASSA, 8 pulados, 0 falhas (`.local/suite-r2d.log`).
- A rodada 3 é a última: passa, com ressalvas escritas. O Fiel roda o Docker nela.

### Próximo passo exato

1. Ticket 07 juntado e resolvido pelo Rebite (integracao 763813a, 186 verdes, 8 pulados). Lição das esperas fixas comentada no 08. Espero o maestro passar o 08.
2. Depois do passa: avisar o Rebite (ramo, testes, relatório, parecer).

### Os testes com Docker da rodada 2 (todos verdes, um de cada vez)

| Teste | Resultado | Log |
|---|---|---|
| `07-banco.test.ps1` (em 6911857) | 24 PASSA | `.local/07-r2e.log` |
| prova 01 (em 87ce68b) | 17 PASSA; hub A→B de 260 arquivos em 70 s | `.local/prova01-r2g.log` |
| prova 02 | 12 PASSA | `.local/prova02-r2f.log` |
| teste do 06 | 14 PASSA | `.local/06-r2f.log` |

- A fila tem conferência de memória: `.local/fila-docker.ps1`, registro em `.local/fila-docker.log`. Antes de cada
  prova, abaixo de 2 GB livres, espera 3 min. O Docker roda no WSL (vmmemWSL, cresce com a carga; ~2,2 GB em 05h12).
- A fila não cria nem apaga a trava sozinha: criar antes e apagar depois, à mão.
- O sistema parou a fila duas vezes por falta de memória (~23h05 e ~23h40). Limpei o que sobrou e registrei no
  relatório.

### O que a rodada 2 mudou no kit (`agents/code/kit/par/banco/banco.psm1`)

- `Get-PidSincronizador`: o PID só vale se o processo for `node.exe`, com o `CliDb` do par e `daemon` na linha de
  comando.
- `Initialize-Dispositivo`:
  - O dispositivo aceito tem a marca `<cli-db>\.livesync\hub-aceito`, com db, porta, usuário e hora, sem senha. A marca
    só é gravada depois do `ACCEPTED`. Se o `mark-resolved` falha, `isConfigured` volta a `false`.
  - Na volta cedo, o kit confere `encrypt`, `passphrase` e `usePathObfuscation` do `settings.json`, e db, porta e
    usuário da marca, contra o `.env`. Se algo diverge, recusa e diz o campo.
- Espera do `LiveSync active`: 180 s.

### Decisões e armadilhas

- **O remoto no CLI de verdade.** Depois do aceite, o CLI guarda o remoto cifrado em
  `remoteConfigurations[...].uri` (`isEncrypted: true`); os `couchDB_*` ficam vazios.
  - Com o daemon rodando, nenhum outro comando do CLI abre o banco local. O `remote-export` falhava assim, e por isso
    a conferência usa a marca.
- **O daemon não herda handles.** Ele sobe por `cmd /c ... > log 2> err`, sem `-Redirect*`. O PID gravado é o do
  `node` filho do `cmd`.
- **O passo e o gerador.** O passo roda o gerador de exclusões antes da partida. Se a lista mudou com o daemon
  rodando, o passo religa o CLI.
- **Lições da etapa 0, já no módulo:**
  - o mesmo sal nos dois bancos (o kit recusa outro sal);
  - um `couchdb.ini` por par;
  - esperar o `_up` sem credencial;
  - vale a linha `[Done]`;
  - `HUB_ROOT` sob pasta com ponto é recusado.
- **Achar daemon órfão:** o script `.local/orfaos.ps1` filtra a linha de comando por `hub-ensaio-00`. No Git Bash, a
  consulta Win32 com aspas quebra: use um script `.ps1`. Nunca matar por nome.
- **Escape no Python dentro de heredoc:** `\t` e `\b` em caminho viram caractere de controle. Para editar caminho com
  barra invertida, use o Edit ou `chr(92)`.

### Comandos de teste

- Sem Docker (entram na suíte):
  - `node --test agents/code/test/07-kit-sem-docker.test.mjs`
  - ou direto: `pwsh -NoProfile -File agents/code/test/banco/kit-sem-docker.ps1` (11 PASSA).
- Com Docker, com a trava e um de cada vez:
  - `pwsh -NoProfile -File agents/code/test/07-banco.test.ps1`
  - `agents/code/test/provas/01-banco/prova.ps1`
  - `agents/code/test/provas/02-pastas-com-ponto/prova.ps1`
  - `agents/code/test/gerar-exclusoes/sincronizador.ps1`
- Suíte comum, com a trava: `node --test "agents/code/test/**/*.test.mjs"`. Os testes de harness ficam pulados sem
  `HUB_HARNESS_REAL=1`.

## Feito antes (fechado)

- **Ticket 01** (prova dos dois CouchDB): juntado pelo Rebite em 45ec3b0.
- **Ticket 29** (harness só sob pedido): juntado e resolvido pelo Rebite (`integracao` d5e4e16).
  - Parecer: `etapas/parecer-29-Brasa.md`. Relatório: `etapas/relatorio-29-harness-sob-pedido.md`.
  - Fica comigo só o que o Fielzinho achar depois, como ressalva.
