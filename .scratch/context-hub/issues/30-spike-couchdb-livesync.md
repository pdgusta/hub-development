# Spike: CouchDB e LiveSync

Type: task
Status: resolved

## Question

Caminho O1 ("Montar: CouchDB, LiveSync e MCP").

Spike no Windows desta máquina, sobre conteúdo de teste (sem dado de cliente), medindo:
1. a instalação do servidor;
2. a vista `.md` de mão dupla com uma edição do Gustavo no Obsidian voltando ao banco;
3. uma colisão provocada entre duas pastas que fazem o papel das duas máquinas, e como ela aparece;
4. a gravação do agente pelo MCP, inclusive uma escrita com base desatualizada.
Resultado: um relatório curto com o que funcionou, o que falhou e o esforço real do que falta montar.
Aprovado pelo Gustavo em 2026-10-04 (R8: "sim para os 2 spikes"); roda quando ele mandar.
Insumo de "Como a verdade viaja entre as máquinas".

## Comments

- 2026-10-06: ticket reservado pelo /wayfinder (primeiro da fronteira; o outro aberto e sem bloqueio é
  a "Sonda do Dolt", que é opcional). Aguardando o "pode iniciar" do Gustavo, porque o spike instala
  software nesta máquina. Repete os quatro itens do "Spike: Fast Note Sync", com o mesmo conteúdo de
  teste, para comparar lado a lado. Montagem fora do repo, em `C:\Projetos\spike-livesync\`.
- 2026-10-06: spike iniciado (Gustavo, no Maestri: "pode iniciar o spike"). Sem admin nesta máquina,
  então o MSI do CouchDB fica fora; o Docker Desktop (instalado, estava desligado) foi ligado para o
  caminho S1 da pesquisa 26: o compose do es617 (imagens `couchdb:3` e
  `ghcr.io/es617/obsidian-sync-mcp:latest`), com as portas só em 127.0.0.1, sem E2EE, conteúdo de
  teste. O `docker compose up` foi **bloqueado pelo classificador de permissões do Claude Code**
  (execução de imagem de terceiro). Aguardando o Gustavo liberar ou escolher outro caminho.
- 2026-10-06: o Gustavo tem admin (o meu teste olhou só o shell, que não roda elevado; correção). Ele
  roda o `docker compose up` e libera a regra para `docker compose`. Compose e `.env` gravados em
  `C:\Projetos\spike-livesync\`.
  - **Item 1, instalação:** o Gustavo rodou o `docker compose up -d` (com a regra liberada). Download
    das imagens `couchdb:3` (464 MB) e `ghcr.io/es617/obsidian-sync-mcp` 0.7.3 (421 MB); os três
    contêineres subiram em cerca de 25 s depois do download (o `db-init` criou o banco `obsidian` e
    saiu). MCP em `http://127.0.0.1:8787/mcp`, com OAuth por senha (`MCP_AUTH_TOKEN`), também aceita
    `Bearer`. Sem E2EE, para o spike. Tropeço: o `!` do Claude Code roda no Bash, então caminho com
    barra invertida quebra.
  - Plugin LiveSync 1.0.35 (release de 2026-10-05) posto à mão em `cofre-a` e `cofre-b`; o `cofre-a`
    leva a nota de teste `teste/agente.md` ("hello world"). A configuração segue o caminho oficial
    "Configure CouchDB manually on the first device" (`docs/quick_setup.md`) no A, e o B entra por um
    Setup URI gerado pelo A.
  - Configuração do cofre A (Gustavo, com prints no Maestri): "Check server requirements" todo verde
    (CouchDB 3.5.2, o `couchdb-init.ini` do es617 basta); "Overwrite Server" destrói e recria o banco
    (3 documentos depois: a nota, um chunk e a versão). Tropeços: o MCP perdeu o feed quando o banco
    foi recriado (`ChangeManager Error watching changes`; resolvido com restart do contêiner); o
    "Config Doctor" do plugin reclamou do tamanho de chunk logo depois do assistente (respondido "No");
    **o assistente termina com todos os modos de sync desligados** (`liveSync`, `syncOnSave`,
    `periodicReplication` = false no `data.json`), então a gravação do agente pelo MCP chegou ao banco
    mas não desceu ao disco. Falta escolher Sync Mode = LiveSync (Sync Settings).
  - MCP: `tools/list` com 9 ferramentas (`read_note`, `write_note`, `edit_note`, `list_notes`,
    `list_folders`, `list_tags`, `delete_note`, `move_note`, `get_note_metadata`); `read_note` não
    devolve revisão, só o texto e o link. Cliente de teste em `C:\Projetos\spike-livesync\mcp.py`.
  - **Item 2, sentido agente → disco:** com Sync Mode = LiveSync, a linha gravada antes desceu, e um
    novo `edit_note` (append) pelo MCP chegou ao `.md` do `cofre-a` em cerca de 0,2 s.
  - **Item 2, sentido Gustavo → banco:** a troca de `hello world` por `hello do Gustavo` no Obsidian
    chegou ao CouchDB (revisão 5) e o `read_note` do MCP já a devolve. Uma terceira gravação do agente,
    feita com o Gustavo no Maestri, também chegou em cerca de 0,2 s. Avisos extras do plugin depois da
    configuração: "Remote storage size notifications are not configured" (diálogo de limite do banco;
    "Ask me later"). **Vista `.md` de mão dupla: funcionou nos dois sentidos.**
  - **Item 4, gravação do agente com base desatualizada** (nota `teste/colisao-agente.md`): o agente
    grava v1 pelo `write_note` (rev 1) e lê; a "máquina A" grava v2 no disco do `cofre-a`, e o plugin
    sobe (rev 2; o `read_note` já devolve v2); o agente grava v3 pelo `write_note` a partir da v1.
    **Resultado: v3 aceita sem erro, sem conflito (`_conflicts` vazio), e a v2 sumiu do disco e da
    folha atual.** Diferença para o FNS: a v2 continua no banco como revisão antiga (rev 2
    `available`, com o chunk `h:19mgdc710sj1i` íntegro), recuperável à mão por `?rev=`, **até a
    compactação**: pela doc do CouchDB (`maintenance/compaction.rst`), a compactação troca revisões
    antigas por "tombstones", e a compactação automática ("smoosh") vem ligada desde a 2.1.1. Ou seja,
    o rastro existe mas é temporário e invisível para o Gustavo.
  - `edit_note` com `replace` é uma guarda natural: com `old_text` velho ("hello world"), devolve
    "old_text not found in note." e não grava. `append`/`prepend` agem sobre o conteúdo atual. O buraco
    é só o `write_note` (substitui tudo), como diz o README do es617 ("last write wins").
  - **Emulação da guarda R1** (a correção recomendada pela pesquisa 26, sem mexer no es617):
    `C:\Projetos\spike-livesync\r1.py` grava direto no CouchDB como o fork faria, com a escrita do
    agente como filha da revisão que ele leu (`_bulk_docs` com `new_edits: false`). Teste: o agente lê
    rev 3; a "máquina A" grava v4 no disco (rev `4-bfb9…`); o agente grava a partir da rev 3. **O
    CouchDB guardou as duas**: vencedora `4-bfb9…` (máquina A) e `_conflicts: ["4-7596…"]` (agente).
    O disco do A não mudou. Falta ver se o plugin mostra esse conflito ao Gustavo.
  - **O plugin mostrou o conflito da R1 sozinho:** no cofre A abriu o modal "Conflicting changes" com
    `teste/colisao-agente.md`, um diff por trecho entre as duas versões (navegação "Prev/Next", 1/3),
    as datas ("Base" = versão vencedora da máquina A, 18:26:13; "Conflicted" = a do agente, 18:26:21)
    e os botões "Use Base", "Use Conflicted", "Concat both" e "Not now"; a barra de status ganhou um
    contador de conflito ("1"). O diff é por caractere, o que deixa a leitura confusa em linhas parecidas.
  - **"Concat both" juntou por trecho, não por versão:** o resultado (nos dois cofres, rev 5, sem
    conflito) é `v4 da máquina A (depois da leitura do agente)` + `o agente (base = rev que ele leu)`.
    O começo comum "v4 d" ficou só uma vez, então a linha do agente perdeu "v4 d" e ficou truncada.
    Nada da máquina A se perdeu, mas a versão do agente saiu mutilada. (O `\n` literal no fim é
    artefato do meu `r1.py`, não do plugin.)
  - Cofre B montado pelo Setup URI do A ("Time-bound", vale até 2026-10-07 21h; "Overwrite all with
    remote files"): as duas notas desceram idênticas. **O B também terminou com o sync desligado**
    (`liveSync: false`), como o A.
  - **Item 3, colisão:** B com LiveSync ligado e fechado ("máquina desligada"). O Gustavo trocou a
    1ª linha de `teste/agente.md` para `hello da máquina A` no A (subiu ao banco); eu troquei a mesma
    linha no disco do B fechado para `hello da máquina B (editado offline)`. O A não mudou (o B estava
    mesmo fora). Próximo: reabrir o B.
  - **Reabrir o B:** os dois cofres abriram sozinhos o modal "Conflicting changes" para
    `teste/agente.md` (diff "hello da máquina A" × "B (editado offline)", 1/2); o A também mostra a
    faixa "This file has unresolved conflicts" e "[conflict] Manual merge required!" no topo da nota,
    e o contador de conflitos na barra de status. **Nada foi sobrescrito:** o disco do A ficou com a
    versão A, o do B com a versão B, e o banco guardou as duas folhas (vencedora `7-10a3…` = A;
    `_conflicts: ["6-4828…"]` = B, ramo a partir da rev 5). Script `revs.py` lista as folhas.
  - **O MCP não enxerga o conflito:** `read_note` devolve só a vencedora (A), sem aviso. Um
    `edit_note` (append) do agente durante o conflito gravou sobre a vencedora (rev 8) e **manteve** o
    conflito (a folha B continua); o plugin não desceu essa linha ao disco de nenhum dos cofres
    enquanto o conflito está aberto.
  - O modal não tem coluna editável: as saídas são "Use Base", "Use Conflicted", "Concat both" e "Not
    now" (no FNS havia o resultado editável de três vias).
  - **Resolução:** o Gustavo clicou "Concat both" só no A. De novo a junção foi por caractere: a linha
    virou `hello da máquina AB (editado offline)`, uma mistura que não é nenhuma das duas. A linha que
    o agente gravou durante o conflito ficou. O modal do B **sumiu sozinho** quando a resolução chegou;
    os dois discos ficaram idênticos (rev 9; a folha B virou `deleted`); **sem conflito fantasma**.

## Answer

Spike de 2026-10-06: CouchDB 3.5.2 + es617/obsidian-sync-mcp 0.7.3 em Docker Desktop (compose do
es617, portas em 127.0.0.1, sem E2EE), plugin Self-hosted LiveSync 1.0.35, em
`C:\Projetos\spike-livesync\`. Detalhes e evidências nos comentários acima.

**Funcionou**
1. **Instalação:** dois contêineres (imagens de 464 MB e 421 MB), de pé em cerca de 25 s depois do
   download; o `couchdb-init.ini` do es617 passa em todo o "Check server requirements". O assistente do
   plugin tem cerca de 10 telas e destrói e recria o banco; o segundo cofre entra por Setup URI.
2. **Vista `.md` de mão dupla:** a edição no Obsidian chega ao banco, e a gravação do agente pelo MCP
   chega ao `.md` em cerca de 0,2 s, também com o Obsidian em segundo plano.
3. **Colisão entre "máquinas":** os dois cofres avisaram sozinhos (modal, faixa na nota e contador),
   nada foi sobrescrito, o banco guardou as duas folhas, e a resolução feita num cofre limpou o aviso no
   outro, sem conflito fantasma. Pegou edição feita no disco com o Obsidian fechado.
4. **A correção R1 da pesquisa 26 funciona com o plugin:** emulada direto no CouchDB (`r1.py`), a
   gravação atrasada do agente virou um conflito, e o plugin abriu o modal ao Gustavo sem tocar na
   versão da máquina A.

**Falhou**
5. **Gravação do agente com base desatualizada:** o `write_note` aceita, sem conflito, e a versão do
   outro some do disco. Ao contrário do FNS, ela continua no banco como revisão antiga, recuperável à mão
   **até a compactação automática** do CouchDB, mas invisível para o Gustavo. Viola o critério 4
   enquanto a R1 não existir. (`edit_note` com `replace` já recusa texto velho; `append` e `prepend`
   agem sobre o atual.)
6. **O MCP não vê conflito:** o `read_note` devolve só a vencedora, sem aviso, e grava sobre ela (o
   conflito continua aberto, e o plugin segura a descida ao disco).
7. **"Concat both" junta por caractere:** nas duas vezes produziu texto mutilado (`hello da máquina AB
   (editado offline)`); não há campo editável no modal. Para não errar, o Gustavo precisa escolher uma
   versão e reeditar à mão.
8. **Acabamento da configuração:** o assistente termina com o sync desligado nos dois cofres (é
   preciso escolher Sync Mode = LiveSync à mão), o "Config Doctor" reclama da configuração recém-criada,
   e o MCP perde o feed quando o banco é recriado (restart).

**Achado para "Como a verdade viaja entre as máquinas":** no CouchDB a nota é um documento de
metadados (`children`) mais chunks `h:…` com o texto; o histórico de revisões e as folhas em conflito
moram no banco e replicam com ele. A busca do agente pode ler o `.md` em disco (pesquisa 26, B1).

**Esforço real do que falta (caminho O1)**
- **R1 no fork do es617:** `read_note` devolve a revisão, `write_note`/`edit_note` aceitam `base_rev` e
  gravam como filha dela (o gancho `conflictBaseRev` da commonlib vem da pesquisa 26, não conferido por
  mim no código). Lado CouchDB e plugin já provado pela emulação. Cerca de 1 dia.
- **Conflito visível ao agente:** aviso no `read_note` ou ferramenta `get_conflicts`. Cerca de 0,5 dia.
- **Configuração:** Sync Mode, limite de tamanho e E2EE (com a passphrase também no MCP). Menos de 1 h,
  num roteiro.
- **Servidor para as duas máquinas:** contêiner numa delas mais Tailscale, ou outra opção da pesquisa 26.
  Não testado; cerca de meio dia.
- **X1, checagem de início de sessão:** cerca de 1 dia, como no FNS.
- **"Concat both" por caractere:** aceitar (escolher uma versão e reeditar) ou abrir issue upstream; de
  0 a 0,5 dia.
- **Total:** de 3 a 3,5 dias.

**Comparação com o "Spike: Fast Note Sync"**

| | FNS 3.6.1 | CouchDB + LiveSync 1.0.35 |
|---|---|---|
| Instalação | binário Windows, 1 s | Docker, 2 imagens (~885 MB), assistente longo |
| Vista de mão dupla | ok (< 3 s) | ok (~0,2 s), mas o sync começa desligado |
| Colisão para o Gustavo | tela de três vias **editável** | escolher um lado ou "Concat both" (mutila) |
| Depois de resolver | conflito fantasma, interface em chinês | limpo nos dois cofres |
| Agente com base velha | perde sem rastro | perde, com rastro até a compactação |
| Correção | C1 no servidor Go (MCP e REST), ~1 dia | R1 no MCP TypeScript, ~1 dia, já provada |
| Agente vê conflito | não testado | não |
| Total que falta | 2 a 2,5 dias | 3 a 3,5 dias |

**Não testado:** duas máquinas reais (rede e Tailscale), E2EE, o CLI do LiveSync, o MCP no Codex e no
Copilot, escala, compactação real do histórico.
