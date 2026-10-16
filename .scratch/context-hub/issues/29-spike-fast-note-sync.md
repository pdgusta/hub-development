# Spike: Fast Note Sync

Type: task
Status: resolved

## Question

Caminho O3-C ("Montar: banco central com plugin do Obsidian").

Spike no Windows desta máquina, sobre conteúdo de teste (sem dado de cliente), medindo:
1. a instalação do servidor;
2. a vista `.md` de mão dupla com uma edição do Gustavo no Obsidian voltando ao banco;
3. uma colisão provocada entre duas pastas que fazem o papel das duas máquinas, e como ela aparece;
4. a gravação do agente pelo MCP, inclusive uma escrita com base desatualizada.
Resultado: um relatório curto com o que funcionou, o que falhou e o esforço real do que falta montar.
Aprovado pelo Gustavo em 2026-10-04 (R8: "sim para os 2 spikes"); roda quando ele mandar.
Insumo de "Como a verdade viaja entre as máquinas".

## Comments

- 2026-10-04: pelo "Debate sobre o Dolt", este é o primeiro spike. Montagem a testar: C1 (a gravação do agente leva a base), C2 (Manual Merge nas duas máquinas) e X1 da pesquisa 28.
- 2026-10-06: spike iniciado (Gustavo: "pode iniciar o spike"). Montagem fora do repo, em
  `C:\Projetos\spike-fns\` (servidor em `server\`, credenciais e tokens em arquivos locais, cliente MCP
  de teste em `mcp.py`).
  - **Item 1, instalação:** release 3.6.1 (`windows-amd64`, 47 MB compactado, binário de 109 MB).
    Extrair e rodar `fast-note-sync-service.exe run -c config/config.yaml`: sobe em cerca de 1 s com
    SQLite, sem instalador e sem dependência. Mudanças no config: `http-port: 127.0.0.1:9000`,
    `auth-token-key` própria, log `info`. Registro e criação de token só aceitam o cliente `webgui`
    (código 314 sem o header `X-Client: webgui`, `internal/middleware/webgui_auth.go`). Tokens por
    cliente com escopo e cofre (`POST /api/token`). O servidor consulta versão/atualização por conta
    própria (tarefas `check_version` e `update_support` no log).
  - **Achado de armazenamento:** o SQLite guarda metadados; o texto de cada nota fica em arquivo
    (`storage/vault/u_1/note/n_N/content.txt` e `snapshot.txt`; histórico em `history/h_N/diff.patch`).
  - **Item 4, gravação do agente pelo MCP:** MCP StreamableHTTP em `/api/mcp` funcionou de primeira
    (26 ferramentas; `note_create_or_update` só recebe `vault`, `path`, `content`). Teste: o agente
    grava v1 → a "máquina B" grava v2 pelo REST → o agente grava v3 a partir da v1. **Resultado: v3
    aceita sem erro e v2 perdida em silêncio.** A v2 não ficou nem no histórico (o histórico vai de v1
    direto para v3; o snapshot tem atraso de `history-save-delay: 10s` e só guarda o estado vigente);
    busca de texto em todo `storage\` não acha a v2. O REST também ignora `baseHash` (base falsa
    `999999` aceita). No código 3.6.1, `baseHash` só é conferido no caminho WebSocket
    (`internal/routers/websocket_router/ws_note.go` 140–164, só com `manualMerge`); MCP
    (`internal/routers/mcp_router/note_tools.go` 141–150) e REST não leem o campo. Logo o C1 da
    pesquisa 28 é obrigatório, e precisa cobrir também o REST.
  - **Item 2, vista `.md` de mão dupla:** o Gustavo abriu `cofre-a` no Obsidian (plugin 2.4.0 posto à
    mão em `.obsidian/plugins`, com `data.json` pré-configurado: URL, token em texto puro, cofre e
    `offlineSyncStrategy: manualMerge`). As notas do servidor desceram para o disco. A edição dele
    ("hello world") chegou ao banco em segundos (versão 3, cliente `ObsidianPlugin`, WebSocket
    `NoteModify`). No sentido inverso, um `note_append` do agente pelo MCP apareceu no `.md` do
    `cofre-a` em menos de 3 s. **Funcionou nos dois sentidos, sem configuração extra.**
  - **Item 3, colisão:** com os dois cofres sincronizados, o `cofre-b` foi fechado ("máquina
    desligada"). O Gustavo trocou `hello world` por `hello da máquina A` no `cofre-a`, e eu editei a
    mesma linha no disco do `cofre-b` fechado (`hello da máquina B (editado offline)`). Ao reabrir o B,
    o servidor recusou a subida (log: *"manual merge conflict intercepted on direct NoteModify, blocked
    and sent 530"*), e o plugin abriu sozinho o modal "Note Conflicts" com `teste/agente.md`, um
    contador vermelho "1" na barra de status e um botão em chinês sem tradução ("去解决冲突", "ir
    resolver o conflito"; o contador também está em chinês). Nada foi sobrescrito: servidor e A ficaram
    com "máquina A", e o B manteve a versão offline no disco. Edição offline feita **no disco com o
    Obsidian fechado** também foi detectada (o plugin compara com o `fileHashMap.json` ao abrir).
  - **Tela de resolução** (botão do modal): "Resolve Note Conflicts" em inglês, com três colunas:
    Local e Remote (só leitura, cada uma com o diff contra a base, como `hello world` riscado e a
    linha nova em verde, e os botões "Copy" e "Use Local ->"/"Use Remote ->") e "Resolved Conflict
    Content" (editável, começa com a versão local), mais os botões "Resolve Conflict" e "Cancel". A
    base reconstruída do histórico está certa (`hello world`).
  - **Resolução:** o Gustavo juntou as duas linhas na coluna da direita e clicou em "Resolve
    Conflict". O servidor gravou (*"conflict resolved manually by client, writing directly"*), e a
    junção chegou ao `cofre-a` e ao `cofre-b` (arquivos idênticos ao servidor, byte a byte). **Mas 50 ms
    depois o B mandou outra `NoteModify`, que levou um novo 530**, e o modal voltou a listar
    `teste/agente.md` com o contador "1". O plugin guarda o conflito em
    `.obsidian/plugins/fast-note-sync/conflict-notes/` (`*.base.md` e `*.remote.md`), e os dois já
    contêm a versão juntada; o disco do B também. É um conflito fantasma depois da resolução (em
    investigação).
  - **Conflito fantasma:** ao reabrir, as três colunas (Local, Remote e resultado) são idênticas à
    versão juntada. O conteúdo está certo e nada se perdeu; é um alarme falso que exige um clique a
    mais. A causa no plugin não foi investigada.
  - **Fim:** um segundo "Resolve Conflict" (com as três colunas iguais) limpou o contador, e o modal
    mostra "当前无发生冲突的笔记" ("nenhuma nota em conflito").

## Answer

Spike de 2026-10-06, FNS 3.6.1 (servidor) + plugin 2.4.0, SQLite, em `C:\Projetos\spike-fns\`;
detalhes e evidências nos comentários acima.

**Funcionou**
1. **Instalação:** binário Windows, sem instalador, sobe em cerca de 1 s. Conta e tokens só pelo
   cliente `webgui`; token por cliente, restrito ao cofre.
2. **Vista `.md` de mão dupla:** a edição no Obsidian chega ao banco em segundos, e a gravação do
   agente pelo MCP aparece no `.md` em menos de 3 s.
3. **Colisão entre "máquinas":** com Manual Merge, o servidor recusa (530) e nada é sobrescrito. O
   plugin avisa sozinho (modal e contador) e abre a tela de três vias (local, remoto e resultado
   editável, com a base certa); a junção chega às duas pastas. Pegou até edição feita no disco com o
   Obsidian fechado.

**Falhou**
4. **Gravação do agente com base desatualizada:** aceita, e **a versão do outro some sem deixar
   rastro, nem no histórico**. Na 3.6.1, a base só é conferida no caminho WebSocket do plugin; o MCP
   `note_create_or_update` e o REST `POST /api/note` gravam às cegas. Viola o critério 4 enquanto o
   C1 não existir.
5. **Conflito fantasma:** depois de resolver, o plugin reenviou a nota e reabriu um conflito com as
   três versões iguais. Some com um segundo clique; é ruído, não perda. Causa não investigada.
6. **Acabamento:** parte da interface de conflitos está em chinês sem tradução.

**Achado para "Como a verdade viaja entre as máquinas":** no FNS, o SQLite guarda os metadados e o
texto de cada nota fica em arquivo no servidor (`storage/vault/u_N/note/n_N/content.txt`).

**Esforço real do que falta (Trilha C)**
- **C1, base na gravação do agente:** obrigatório. Patch no servidor para `note_create_or_update`
  **e** `POST /api/note` aceitarem um hash esperado e recusarem se a base mudou. `note_append`,
  `note_prepend` e `note_replace` agem sobre o conteúdo atual do servidor e não precisam disso. Cerca
  de 1 dia (antes, de 0,5 a 1). A alternativa de um MCP fino na frente tem janela de corrida contra o
  plugin.
- **C2, configuração:** confirmado em menos de 1 h (Manual Merge e token via `data.json`). Falta
  desligar o registro (`user.register-is-enable: false`) e ligar o MCP nos três harnesses.
- **X1, checagem de início de sessão:** inalterado, cerca de 1 dia. Não testado.
- **Conflito fantasma e tradução:** aceitar, ou abrir issue/PR upstream; de 0 a 0,5 dia.
- **Total:** de 2 a 2,5 dias, em linha com a pesquisa 28.

**Não testado:** Postgres, duas máquinas reais (rede e Tailscale), o cliente headless (X2), escala,
a busca do `note_list`, o MCP no Codex e no Copilot, e o atraso do histórico (`history-save-delay`)
como mitigação parcial.

- 2026-10-06: servidor do spike desligado a pedido do Gustavo. Pasta `C:\Projetos\spike-fns\` mantida
  (cofres de teste, dados do servidor e scripts).
