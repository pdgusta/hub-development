---
title: Pesquisa 19, zvec-grep na camada de busca do hub
data: 2026-10-02
origem: subagente de pesquisa (Claude Code), ticket 19 "zvec-grep na camada de busca"
aviso: saída de modelo. Fontes primárias: README, docs/ e código-fonte do zvec-ai/zvec-grep no commit `30c3160` (02/10/2026), lidos em raw.githubusercontent.com; API do GitHub (metadados, releases, issues, PRs); registro npm de `@zvec/zvec-grep`; README do alibaba/zvec; clone local do FreeLLMAPI (commit `ac6d29d`, 16/09/2026), só para a questão do nome do modelo. Nada foi clonado, instalado ou executado. O que não foi conferido na fonte está marcado como **não verificado**.
---

# zvec-grep na camada de busca do hub: levantamento de 02/10/2026

Abreviações: `R` = https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723 (todas as
citações de arquivo do zvec-grep são relativas a esse commit); `I#n` = https://github.com/zvec-ai/zvec-grep/issues/n.

## Resumo (uma tela)

1. **Objetivo, nas palavras do autor:** ser *"the local-first search layer for humans and agents"*, que
   *"unifies ripgrep, BM25, and vector search behind one local-first interface"*, para usar *"directly from the
   terminal, or let your agent use it for you"*. Isso vale para código e também para documentação e notas.
2. **Relação com a camada de busca do hub:** **existe, mas só na metade de leitura**. O zvec-grep entrega ao
   agente o trecho certo de uma pasta sem que ele leia tudo, e quebra o Markdown por seção de título. **Não grava
   nada**: o conjunto padrão de ferramentas MCP *"intentionally exposes only search"*.
3. **O que se encaixa:** Windows nativo (CI unitário em `windows-latest`), daemon com MCP que o próprio
   instalador registra no Claude Code, no Codex, no Copilot CLI e no VS Code, modelos locais multilíngues, BM25 +
   vetor + RRF, reindexação incremental por tamanho/mtime e SHA-256, watcher recursivo e reconciliação a cada hora.
4. **O que falta ou atrapalha:**
   - sem **filtro por frontmatter**: o frontmatter nem é reconhecido hoje (a PR #79, que trata disso, segue aberta);
   - sem leitura por seção como ferramenta: devolve `arquivo:linhas` e a prévia;
   - o BM25 usa o tokenizador `jieba` + `lowercase`, **sem stemming e sem remoção de acentos** (ruim para pt-BR no lado lexical);
   - **FreeLLMAPI só por contorno**: o remoto aceita qualquer endpoint compatível com OpenAI, mas o nome do modelo
     é fixo (`text-embedding-v4` ou `qwen3.7-text-embedding`), com 1.024 dimensões. O suporte genérico (#120) está aberto;
   - o índice fica em `<pasta>/.zvec-grep/`, **dentro do hub**, e precisa de `.gitignore`;
   - é pré-1.0 (v0.2.2), com bugs abertos que destroem o índice (#140, #158) e um laço de re-embedding no Windows
     depois de uma rajada de mudanças (#137).
5. **Conclusão:** **serve como parte**, a lente de busca, e não como camada inteira. **Recomendo que entre no spike
   como uma das duas candidatas, ao lado do markdown-vault-mcp**, porque é a mais madura e a única com instalador
   para os três agentes do hub. O spike deve medir: a qualidade em pt-BR com modelo local multilíngue, o BM25 com
   acentos e o comportamento depois de um `git pull` com muitos arquivos.

## 1. O objetivo do zvec-grep (com as palavras do autor)

**O que é e para quem.**
- Lema do README: *"Know the words—or don't. Just zg."* e *"The local-first search layer for humans and agents."*
  ([R/README.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/README.md)).
- Descrição do repositório (API do GitHub): *"Local-first search across your workspace, built for humans and AI agents."*
- README: *"**zg** (**z**vec-**g**rep), powered by zvec, unifies ripgrep, BM25, and vector search behind one
  local-first interface. Use it directly from the terminal, or let your agent use it for you."*

**Que problema resolve.** O argumento do README é que o agente gasta menos para achar o trecho certo:
- *"Less searching, less context — ranked, source-linked results surface the right evidence with fewer tool calls,
  fewer tokens, and less noise."*
- *"Search beyond keywords — discover by meaning, rank by relevance, then verify with exact text or regex when needed."*

**Não é só para código.**
- [R/docs/03-mcp.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/docs/03-mcp.md):
  *"The same rules apply to source code and non-code material such as documentation, books, research material,
  meeting notes, knowledge-base exports, manuals, configuration, and data."*
- README, sobre os benchmarks: *"code is indexed with symbols, signatures, and breadcrumbs, while prose is retrieved
  as focused sections and chunks"*. Um dos dois benchmarks (BrowseComp-Plus) é de texto geral. O caso de uso mais
  medido, porém, é código: *"zg works best when evidence spans files or modules and the target location is unknown,
  especially for call-chain, data-flow, and architectural questions."*

**Para onde vai.** O roadmap
([R/docs/08-roadmap.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/docs/08-roadmap.md))
diz que o destino é *"one dependable, local-first search layer that people and agents can use without choosing among
separate retrieval tools"*. A fase atual é *"make the public preview dependable"*. Os próximos passos são PDF/PPT/OCR,
grafo de conhecimento, reranking, GUI e celular. Escrever ou editar arquivos não aparece no roadmap.

**Estado declarado:** *"zvec-grep is a work in progress. Commands and configuration may change before the first
stable release."* ([R/docs/README.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/docs/README.md)).

**A base, zvec** ([alibaba/zvec](https://github.com/alibaba/zvec)): *"an open-source, in-process vector database —
lightweight, lightning-fast, and designed to embed directly into applications. Battle-tested within Alibaba Group"*.
Ela oferece FTS e busca híbrida nativas (*"Fuse vector similarity, full-text search, and structured filters in a single
query"*), WAL e *"Multiple processes can read the same collection simultaneously; writes are single-process exclusive."*
Plataformas: *"Windows (x86_64)"* entre elas. Apache-2.0, 16 mil estrelas, criada em 12/2025, v0.7.0 em 24/08/2026. O
zvec-grep é o produto de busca em pasta da própria equipe do zvec. O README do zvec o anuncia na v0.7.0: *"Searching
code or documents? Try zvec-grep"*.

**Duas implementações.** O README e a doc descrevem a versão TypeScript/Node.js. Há uma reescrita em Rust em `rust/`:
*"The Rust implementation is developed separately"* (README). O instalador npm atual é o Node (`npm install -g
@zvec/zvec-grep`, *"Requires Node.js 22 or newer"*).

## 2. Relação com a camada de busca do hub

A camada de busca, pelo `GLOSSARY.md`, é *"o que entrega ao agente o trecho certo do context hub sem que ele leia
tudo. Pode também gravar, mas toda gravação termina como arquivo no disco."*

- **Leitura: o objetivo coincide.** Busca local, numa pasta, para agentes, por significado e por termo, com
  resultado compacto por trecho. O Markdown é quebrado por título, como pede a camada.
- **Gravação: fora do objetivo.** *"The default `agent` toolset intentionally exposes only search"*. Mesmo o conjunto
  `full` só acrescenta `rg`, index, drop e status
  ([R/docs/03-mcp.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/docs/03-mcp.md)).
  O pedido "um MCP que busca e grava" fica pela metade. No hub, a gravação pode continuar sendo a escrita direta dos
  agentes no disco, ou vir de outra peça.

Como a relação existe, aplico abaixo os critérios que fazem sentido para uma ferramenta de busca.

## 3. Critérios aplicados

### 3.1 Arquitetura de busca (vetorial, lexical, híbrida)

- [R/docs/05-architecture.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/docs/05-architecture.md):
  dois caminhos. *"Indexed search<br/>BM25 + vector + RRF"* e *"Managed ripgrep<br/>exact text + regex"*. E também:
  *"Indexed search can combine lexical and vector candidates and fuse their ranks with reciprocal rank fusion (RRF)."*
- Rotas de consulta: posicional/`--hybrid`, `--fts`, `--vector` e `--rg`
  ([R/docs/04-pipeline.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/docs/04-pipeline.md)).
- **Lexical em pt-BR.** O campo de texto é indexado com `tokenizerName: "jieba"` e `filters: ["lowercase"]`
  ([R/src/engine/storage/zvec.ts](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/src/engine/storage/zvec.ts),
  em torno da linha 933). Não há stemming nem remoção de acentos. Portanto "decisão" × "decisões" × "decisao" não
  devem casar no BM25. Isso é inferência pela leitura; o comportamento do jieba com texto latino acentuado é **não
  verificado**. O lado vetorial compensa em parte.

### 3.2 Markdown: corte por título e frontmatter

- **Corte por título: sim.** *"Markdown | `.md`, `.mdx` | `MarkdownExtractor` | Heading sections and breadcrumbs"*
  ([R/docs/04-pipeline.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/docs/04-pipeline.md)).
  No código, cada seção guarda `heading`, `level` e `scope` (a trilha de títulos unida por `::`)
  ([R/src/engine/extraction/markdown/extractor.ts](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/src/engine/extraction/markdown/extractor.ts)).
  Não existe ferramenta `read(path, section)`. A busca devolve `arquivo:linhas`, e com `preview: "full"` devolve
  *"all available source lines ... of each retrieved item"* (docs/03-mcp.md).
- **Frontmatter: não.** O extrator não reconhece frontmatter: `scanHeadings` só trata cercas de código, títulos ATX e
  Setext. A PR aberta [#79](https://github.com/zvec-ai/zvec-grep/pull/79) ("feat(markdown): add CommonMark-aware
  extraction") confirma o problema: *"A YAML sequence item immediately before a closing front matter delimiter can
  resemble a Markdown Setext heading"*. Ela propõe *"Treat leading YAML front matter as a document envelope"* e
  *"Normalize ... front matter fields into generic `frontMatter` metadata"*. Mesmo a PR não promete filtro de busca por
  campo.
- **Filtros que existem:** `globs`, `fileTypes`, `symbolTypes`, `modifiedAfter` e `modifiedBefore` (docs/03-mcp.md). No
  hub, dá para filtrar por pasta e por data, não por `tipo:` ou `status:`.

### 3.3 Windows nativo

- README: *"use the same workspace from the CLI or your agent on macOS, Linux, and Windows"*. Há exemplo em
  PowerShell (`$env:ZVEC_GREP_INDEX_EMBEDDING_CONCURRENCY = "1"`).
- CI: a matriz `unit` do Node inclui `os: windows-latest`, com Node 24
  ([R/.github/workflows/ci.yml](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/.github/workflows/ci.yml)).
  O CI do Rust usa `os: [ubuntu-latest, macos-latest, windows-latest]`
  ([R/.github/workflows/rust-ci.yml](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/.github/workflows/rust-ci.yml)).
  Só os testes unitários do Node rodam no Windows; se há teste de integração no Windows, é **não verificado**.
- Há uso real em Windows nas issues: [#137](https://github.com/zvec-ai/zvec-grep/issues/137) (*"zg 0.2.2 / Windows 11 /
  Node 24"*) e o PR fechado #84, *"fix(windows): preserve managed rg path separators"*.
- O watcher usa `fs.watch(root, { recursive: true })` em toda plataforma que não seja Linux
  ([R/src/daemon/watch-manager.ts](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/src/daemon/watch-manager.ts):
  `requiresDirectoryWatchers(platform) { return platform === "linux"; }`). No Windows, é o watcher recursivo nativo.

### 3.4 Modelos de embedding (locais, por API, compatível com OpenAI, pt-BR)

Fonte: [R/docs/07-embedding.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/docs/07-embedding.md).

- **Locais multilíngues no catálogo:**
  - `local/potion-multilingual-128m`: *"Static model trained for 101 languages"*;
  - `local/multilingual-e5-small`: o mesmo modelo do obsidian-hybrid-search;
  - `local/embeddinggemma-300m`: *"General multilingual code and documents"*;
  - `local/qwen3-embedding-0.6b`: GGUF, 8.192 tokens.
  Os modelos são baixados do Hugging Face, com espelho no ModelScope, para `~/.zvec-grep/models`. A qualidade em
  pt-BR é **não verificada** (não há benchmark em pt-BR no repositório).
- **Remoto:** o catálogo é fechado e só tem Qwen: `qwen/text-embedding-v4`, `qwen/qwen3.7-text-embedding` e
  `qwen/qwen3-vl-embedding`.
  - O pedido de texto **tem formato OpenAI**: `POST` com `Authorization: Bearer`, corpo `{ model, input, dimensions,
    encoding_format: "float" }` e leitura de `data[]`
    ([R/src/engine/models/backends/qwen.ts](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/src/engine/models/backends/qwen.ts),
    comentário *"Text embedding models (OpenAI-compatible API)"*).
  - O endpoint pode ser trocado (`--endpoint` ou `ZVEC_GREP_ENDPOINT`).
  - **O campo `model` é fixo** no nome do catálogo (`model: this.entry.model`), e `dimensions` vai sempre como 1.024.
- **FreeLLMAPI:** a issue aberta [#120](https://github.com/zvec-ai/zvec-grep/issues/120) descreve exatamente esse
  limite: *"that transport is coupled to the Qwen provider and a closed model catalog. A self-hosted OpenAI-compatible
  embeddings service ... cannot be represented accurately unless it impersonates a Qwen model, emits a hard-coded vector
  dimension, accepts Qwen-specific optional request fields, and tolerates a dummy Bearer token."* A sub-issue #122
  (backend genérico) foi fechada dois minutos depois de aberta. O `main` não tem nenhum arquivo `openai*` em
  `src/engine/models/backends/`, então o backend genérico **não está no main**. A PR #132 ("self-hosted DGX endpoints")
  está aberta.
  - Com isso, usar o FreeLLMAPI exigiria que ele atendesse `model: "text-embedding-v4"` com `dimensions: 1024`. No clone
    local (`server/src/services/embeddings.ts`, `resolveFamily`), o FreeLLMAPI resolve `model` pelo nome da família ou
    pelo id de modelo do provedor (*"a family name → itself; a provider-specific model id → its family"*). Se dá para
    registrar um modelo personalizado com esse id e esse tamanho de vetor é **não verificado**.
  - Fora isso, o remoto exige autorização explícita por comando ou por pasta (`zg --auth grant --scope workspace`), e o
    MCP pede consentimento por elicitation.

### 3.5 Como o índice acompanha mudanças (watcher, `git pull`, edição externa)

- **Watcher no daemon:** *"Watcher-reported path updates skip workspace-wide status scans. Because file-system watchers
  can silently miss events, the Server schedules an hourly full reconciliation probe"* e *"Large bursts of exact watcher
  events are compacted into directory-scoped updates"*
  ([R/docs/06-server.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/docs/06-server.md)).
  O watcher é liberado *"after four hours without a client request or a relevant file-system change"*; com
  `ZVEC_GREP_WATCHER_IDLE_TIMEOUT_SECONDS=0`, fica ligado sempre.
- **Na busca:** cada resultado traz `freshness: fresh | possibly_stale`. O MCP aceita `freshness: wait_for_fresh` e
  `autoUpdate`. No modo Server, a atualização padrão é `background`.
- **`git pull` e edição externa (Obsidian, agentes):** para o zvec-grep, são só mudanças de arquivo; nada é específico
  do git. O diff incremental pula o arquivo quando tamanho e mtime batem. Se não batem, calcula SHA-256 e só reindexa
  quando o conteúdo mudou
  ([R/src/engine/pipeline/indexing/index.ts](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/src/engine/pipeline/indexing/index.ts),
  em torno da linha 688). Assim, um checkout que só toca o mtime não gera novos embeddings. `.git` e `.zvec-grep` ficam
  sempre fora.
- **Riscos abertos:**
  - [#137](https://github.com/zvec-ai/zvec-grep/issues/137), no Windows 11: depois que um cliente de sync mudou cerca
    de 80 arquivos em 2 minutos, um job do watcher entrou em laço de re-embedding remoto por mais de 33 minutos. É o
    padrão de um `git pull` grande no hub;
  - [#158](https://github.com/zvec-ai/zvec-grep/issues/158): numa pasta com cerca de 20 mil arquivos Markdown/texto, o
    incremental falhou e deixou o índice impossível de abrir;
  - [#140](https://github.com/zvec-ai/zvec-grep/issues/140): `--rebuild` na 0.2.2 apagou o índice sem reconstruir;
  - [#108](https://github.com/zvec-ai/zvec-grep/issues/108): cerca de 15 MiB gravados para uma edição de 24 bytes;
  - [#213](https://github.com/zvec-ai/zvec-grep/issues/213): a atualização automática segura a trava e faz leituras
    concorrentes falharem.

  Todos afetam só o índice, que pode ser reconstruído, e não os arquivos do hub: o zvec-grep não grava neles.

### 3.6 Onde o índice fica (importa para o sync git)

- *"The index is stored in `.zvec-grep/` under the indexed project root."* (README). Os arquivos são `manifest.json`,
  `files.zvec` e `index.zvec`. **O manifest pode guardar a chave de API:** *"including an API key when one was explicitly
  persisted for that workspace"* (docs/04-pipeline.md).
- O estado global e o daemon ficam em `~/.zvec-grep/` (*"Use `ZVEC_GREP_HOME` to relocate Server state"*). **Não achei
  opção documentada para tirar o índice de dentro da pasta**; a busca nos docs e no código não encontrou nenhuma
  (**não verificado** de forma exaustiva).
- Para o hub, `C:\context-hub\.zvec-grep\` entra no `.gitignore` do hub. O repositório do próprio zvec-grep faz isso
  (`.zvec-grep/` no seu `.gitignore`), mas o zg não cria esse arquivo sozinho (**não verificado**), e a PR aberta
  [#109](https://github.com/zvec-ai/zvec-grep/pull/109) só propõe documentar a recomendação. A PR também explica por
  que o índice não viaja entre máquinas: *"zvec-grep stores host-specific absolute paths and tracks filesystem mtime
  (which Git checkout resets), sharing prebuilt index binaries across machines ... is not supported"*. Cada máquina
  mantém o seu índice, o que combina com o hub.

### 3.7 MCP e CLI para Claude Code, Codex e Copilot

- **Transporte:** o daemon expõe *"Streamable HTTP MCP"* em `http://127.0.0.1:7999/mcp`, só em loopback, com Bearer
  opcional (docs/03-mcp.md e docs/06-server.md). Há também a ponte stdio `zg --server --stdio` (docs/01-agents.md).
- **Instalador por agente**
  ([R/docs/01-agents.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/docs/01-agents.md)):

  | Agente | Arquivos que o instalador mexe |
  |---|---|
  | Codex | `~/.codex/config.toml` e `~/.codex/AGENTS.md` |
  | Claude Code | `~/.claude.json`, `~/.claude/settings.json` e `~/.claude/CLAUDE.md` |
  | GitHub Copilot | `~/.copilot/mcp-config.json` e `~/.copilot/copilot-instructions.md` |
  | VS Code | `mcp.json` de cada perfil e `~/.copilot/instructions/zvec-grep.instructions.md` |

  O instalador **escreve um bloco de orientação nos arquivos globais de instrução**, entre marcadores
  `ZVEC_GREP_START`/`ZVEC_GREP_END`, preservando o resto. Isso cruza com o contrato do hub nesses mesmos arquivos
  (pesquisas 13 e 18). Bug aberto: [#223](https://github.com/zvec-ai/zvec-grep/issues/223), *"Claude Code truncates the
  MCP instructions at 2048 characters, and the CLAUDE.md block repeats the part that survives"*.
- **Ferramentas:** `zvec_grep_search` (padrão). No conjunto `full`: `zvec_grep_rg`, `zvec_grep_index`,
  `zvec_grep_index_drop`, `zvec_grep_index_status` e `zvec_grep_server_status`. Toda chamada exige `root` absoluto.
- **CLI:** `zg "consulta"`, `zg --fts`, `zg --vector`, `zg --rg`, `zg --index` e `zg --status`
  ([R/docs/02-cli.md](https://github.com/zvec-ai/zvec-grep/blob/30c316052f4298ff6fac1e71f45ea40606e24723/docs/02-cli.md)).

### 3.8 Licença e maturidade (API do GitHub e npm, 02/10/2026)

- **Licença:** Apache-2.0.
- **Repositório:** criado em 10/07/2026 (menos de 3 meses), 3.869 estrelas, 225 forks, 65 issues/PRs abertas, cerca
  de 288 commits no `main`, último push em 02/10/2026. Os quatro maiores contribuidores somam cerca de 280 commits.
- **Releases no GitHub:** v0.1.5 (16/07) e v0.2.0 (27/08).
- **npm:** `@zvec/zvec-grep` 0.2.2 (07/09/2026), `engines: node >=22`. O ritmo é rápido, e uma reescrita em Rust está
  em paridade (`rust/RUST_MAIN_PARITY.md`).
- **Leitura:** é o projeto mais popular entre as candidatas, mas é pré-1.0, com mudanças de CLI anunciadas e bugs de
  integridade do índice abertos. É preciso fixar a versão.

## 4. Comparação com as candidatas da §10.4.1

A comparação é justa só na **parte de busca**: as quatro indexam uma pasta de Markdown para agentes. As três da §10.4.1
foram feitas para vaults de notas; o zvec-grep, para pastas em geral, com o código como caso principal. Os dados das
três vêm da §10.4.1 e da §10.2 da exploração e não foram pesquisados de novo.

| Ponto | zvec-grep | grooveseek | markdown-vault-mcp | obsidian-hybrid-search |
|---|---|---|---|---|
| Busca | BM25 (jieba, sem stemming) + vetor + RRF, mais ripgrep | vetorial (`bge-m3`); lexical não consta na §10.4.1 | FTS5 BM25 (porter) + vetor, RRF | híbrida pelo nome; a §10.4.1 não detalha |
| Grava arquivos | **não** | não consta na §10.4.1 | **sim**, com etag e `READ_ONLY` | não consta na §10.4.1 |
| Windows nativo | sim, CI unitário no Windows | binário `windows-msvc`, tempos medidos no Windows | README não menciona, CI só Ubuntu | não consta na §10.4.1 |
| Embeddings locais pt-BR | potion-multilingual, multilingual-e5-small, embeddinggemma, qwen3-0.6b | `bge-m3` | FastEmbed/Ollama | `multilingual-e5-small` |
| Endpoint OpenAI (FreeLLMAPI) | só se passando por Qwen (#120 aberta) | não consta na §10.4.1 | sim, "endpoint compatível" | não consta na §10.4.1 |
| Acompanha mudanças | watcher recursivo, reconciliação por hora, SHA-256 | watcher cobre `git pull` | hash + reconciliação no arranque; watcher ou pull loop do git | não consta na §10.4.1 |
| Índice | dentro da pasta (`.zvec-grep/`) | não consta na §10.4.1 | não consta na §10.2 | dentro do vault por padrão |
| Frontmatter | não reconhece (PR #79 aberta) | filtros de frontmatter | filtros de frontmatter | filtro na CLI |
| Corte por título | seções com trilha de títulos; sem `read(section)` | sim | sim, com `read(path, section)` | não consta na §10.4.1 |
| MCP / CLI | MCP HTTP + stdio, instalador para Claude Code, Codex, Copilot e VS Code; CLI | CLI + daemon (MCP não consta na §10.4.1) | MCP stdio/HTTP | CLI (MCP não consta na §10.4.1) |
| Licença | Apache-2.0 | MIT/Apache-2.0 | MIT | não consta na §10.4.1 |
| Maturidade | 3,9 mil estrelas, 3 meses, v0.2.2 | 8 estrelas | 34 estrelas, v5.0.0, criado em 03/2026 | 107 estrelas |

## 5. Conclusão

- **Inteiro: não serve.** A camada pedida busca **e grava** por MCP, e gravar está fora do objetivo do zvec-grep e do
  roadmap dele. Também não filtra por frontmatter.
- **Como parte: serve, como lente de busca.** É a parte de leitura da camada: achar a seção certa do Markdown sem ler
  tudo, para os três agentes do hub, no Windows nativo. A gravação continuaria sendo feita pelos agentes direto no
  disco ou por outra peça (por exemplo, as ferramentas de escrita do markdown-vault-mcp).
- **Spike: recomendo que entre como uma das duas candidatas, no lugar do grooveseek ou do obsidian-hybrid-search,
  contra o markdown-vault-mcp.** Motivos:
  1. é, de longe, a candidata mais madura em uso e equipe;
  2. tem Windows no CI e relatos reais no Windows;
  3. traz MCP e instalador para Claude Code, Codex e Copilot;
  4. tem modelos locais multilíngues;
  5. o incremental por hash evita re-embedding em checkout.

  O par ficaria "só busca, mais robusta" contra "busca + escrita, menor".
- **O spike deve medir, nesta ordem:**
  1. a qualidade em pt-BR com `local/potion-multilingual-128m` e com `local/embeddinggemma-300m`, incluindo consultas
     com e sem acento (o BM25 não normaliza);
  2. o comportamento depois de um `git pull` que muda dezenas de arquivos (o risco da #137);
  3. o efeito do frontmatter cru nos trechos (Setext falso, #79);
  4. a convivência do bloco que o instalador escreve no `CLAUDE.md`, no `AGENTS.md` e no `copilot-instructions.md` com o
     contrato do hub (#223).

  Use modelo local. O FreeLLMAPI só entra se o spike provar que ele atende `model: "text-embedding-v4"` com 1.024
  dimensões, ou quando a #120 for resolvida.
