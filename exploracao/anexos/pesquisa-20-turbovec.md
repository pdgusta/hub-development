---
title: Pesquisa 20, turbovec na camada de busca do hub
data: 2026-10-03
origem: subagente de pesquisa (Claude Code), ticket 20 "turbovec na camada de busca"
aviso: saída de modelo. Fontes primárias: README, docs/ e arquivos de build/CI do RyanCodrai/turbovec no commit `c6cf0ba` (02/10/2026), lidos em raw.githubusercontent.com; API do GitHub (metadados, releases, issues); API JSON do PyPI para `turbovec`. Nada foi clonado, instalado ou executado. O que não foi conferido na fonte está marcado como **não verificado**.
---

# turbovec na camada de busca do hub: levantamento de 03/10/2026

Abreviação: `R` = https://github.com/RyanCodrai/turbovec/blob/c6cf0baba11ddc0b0ec7f95d4024d816df3bd8ec (todas as
citações de arquivo do turbovec são relativas a esse commit).

## Resumo (uma tela)

1. **Objetivo, nas palavras do autor:** *"A vector index built on TurboQuant, written in Rust with Python bindings"*.
   É uma **biblioteca de índice vetorial** (concorrente do FAISS), que comprime vetores de embedding em 2 a 4 bits e
   busca neles rápido. O público declarado é quem monta RAG grande: *"A 10 million document corpus takes 31 GB of RAM
   as float32. turbovec fits it in 4 GB - and searches it faster than FAISS."*
2. **Relação com a camada de busca do hub:** **só indireta, como peça interna**. O turbovec recebe vetores prontos e
   devolve ids. Não lê arquivos, não quebra Markdown, não gera embeddings, não tem busca por palavra, não tem CLI nem
   MCP. Ele seria, no máximo, o "armazém de vetores" **dentro** de uma ferramenta de busca que alguém construísse.
3. **O problema que ele resolve não existe no hub.** O ganho é memória e velocidade com milhões de vetores. Um hub
   pessoal de Markdown tem ordem de grandeza de milhares a dezenas de milhares de trechos (estimativa, **não medida**:
   o tamanho do hub não consta da exploração). Nessa escala, um índice float32 comum cabe em dezenas de MB.
4. **Comparação com as candidatas da §10.4.1 e com o zvec-grep: não é justa.** Elas são ferramentas de busca prontas;
   o turbovec é um componente de uma delas, no nível do FAISS ou do próprio motor zvec. A tabela da seção 4 só mostra
   o que faltaria construir em volta dele.
5. **Conclusão:** **não serve como camada de busca, nem inteira nem como parte pronta.** Recomendo não incluí-lo no
   spike. Só voltaria à mesa se o hub decidisse construir a própria camada de busca e o índice vetorial virasse
   gargalo, o que não é o caso.

## 1. O objetivo do turbovec (com as palavras do autor)

**O que é.**
- Descrição do repositório (API do GitHub): *"A vector index built on TurboQuant, written in Rust with Python
  bindings"*. Tópicos: `ann`, `faiss`, `nearest-neighbor`, `quantization`, `rag`, `vector-search`, entre outros.
- README ([R/README.md](https://github.com/RyanCodrai/turbovec/blob/c6cf0baba11ddc0b0ec7f95d4024d816df3bd8ec/README.md)):
  *"turbovec is a Rust vector index with Python bindings, built on Google Research's **TurboQuant** algorithm — a
  data-oblivious quantizer with near-optimal distortion and no separate training phase."*
- Descrição do crate em `turbovec/Cargo.toml` e no PyPI: *"Fast vector quantization with 2-4 bit compression and SIMD
  search"*.

**Que problema resolve.** Caber muitos vetores na memória e buscar neles mais rápido que o FAISS:
- *"A 10 million document corpus takes 31 GB of RAM as float32. turbovec fits it in 4 GB - and searches it faster than
  FAISS."* (README, primeira frase).
- Pontos do README: *"Online ingest. Add vectors, they're indexed — no train step, no parameter tuning, no rebuilds as
  the corpus grows"*; *"Incremental saves. `sync(path)` persists just what changed since the last sync"*; *"Filter at
  search time. Pass an id allowlist (or a slot bitmask) to `search()`"*; *"Pure local. No managed service, no data
  leaving your machine or VPC. Pair with any open-source embedding model for a fully air-gapped RAG stack."*
- Para quem: *"Building RAG where privacy, memory, or latency matters? **You're in the right place.**"*

**O que entra e o que sai.** Entra matriz `float32` de vetores; sai `(scores, indices)`:
- *"`vectors` and `query` are 2-D `float32` arrays of shape `(n, dim)` — other dtypes are rejected rather than silently
  converted"* (README).
- A referência da API
  ([R/docs/api.md](https://github.com/RyanCodrai/turbovec/blob/c6cf0baba11ddc0b0ec7f95d4024d816df3bd8ec/docs/api.md))
  abre com *"turbovec exposes two index types and one serialization format per type"*: `TurboQuantIndex` (posicional)
  e `IdMapIndex` (*"stable external `u64` ids"*). Os métodos são `add`, `search`, `remove`/`swap_remove`, `calibrate`,
  `write`/`load`, `sync`. Não há nada de texto.

**Busca híbrida é responsabilidade de outro sistema.** O README chama de *"Hybrid retrieval (filtered search)"* o
seguinte: *"Restrict results to a candidate set produced by another system (SQL, BM25, ACL, time window, …)"*. Ou seja,
o BM25 vem de fora, e o turbovec só faz o *"dense rerank within the candidate set"*.

**Integrações.** Substitutos diretos dos armazéns em memória de LangChain, LlamaIndex, Haystack e Agno: *"Drop-in
replacements for the in-tree reference vector / document stores in each framework"* (README). No exemplo do LangChain
([R/docs/integrations/langchain.md](https://github.com/RyanCodrai/turbovec/blob/c6cf0baba11ddc0b0ec7f95d4024d816df3bd8ec/docs/integrations/langchain.md)),
o modelo de embedding é do usuário (`HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")`). A issue aberta
[#427](https://github.com/RyanCodrai/turbovec/issues/427) reforça o escopo: *"turbovec should own indexing and search;
the frameworks should own documents."*

**Base acadêmica.** Implementa o artigo *"TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate"*
(ICLR 2026, arXiv 2504.19874), com uma correção de comprimento adaptada do RaBitQ e o layout do FAISS FastScan no x86
(README, "References").

## 2. Relação com a camada de busca do hub

A camada de busca, pelo `GLOSSARY.md`, é *"o que entrega ao agente o trecho certo do context hub sem que ele leia
tudo. Pode também gravar, mas toda gravação termina como arquivo no disco."*

- **Não é uma camada de busca.** Para entregar "o trecho certo" a um agente, faltam no turbovec: ler a pasta, quebrar
  o Markdown, gerar embeddings, busca lexical, acompanhar mudanças nos arquivos e uma interface para o agente (CLI ou
  MCP). Nenhum desses itens está no README, na `docs/api.md` ou no roadmap implícito das issues abertas (a mais
  próxima de "superfície de serviço" é [#182](https://github.com/RyanCodrai/turbovec/issues/182), *"gRPC server surface
  for turbovec"*, aberta e sem MCP).
- **Pode ser peça interna de uma camada.** O que ele faz (guardar vetores, achar os vizinhos mais próximos, filtrar por
  lista de ids, salvar incremental) é o que as candidatas já fazem por dentro: o zvec-grep usa o motor zvec; o
  markdown-vault-mcp e o obsidian-hybrid-search usam bancos próprios (detalhes na §10.2 e §10.4.1 da exploração, não
  pesquisados de novo aqui). Nenhuma delas permite trocar o motor vetorial pelo turbovec (**não verificado** em cada
  uma; não há menção nas fontes já lidas).
- **A vantagem dele não pesa no hub.** O ganho declarado é de escala (10 milhões de documentos, 31 GB → 4 GB). Conta
  rápida: 20 mil trechos × 1.024 dimensões × 4 bytes ≈ 80 MB em float32, que qualquer índice comum guarda sem esforço.
  O tamanho real do hub é **não medido**.

Como a relação é só indireta, aplico abaixo apenas os critérios que dizem algo sobre o turbovec como peça, para
registro. Os critérios de ferramenta (pt-BR, frontmatter, MCP, `git pull`) não se aplicam a ele.

## 3. Critérios que fazem sentido para uma peça

### 3.1 Windows nativo

- **Sim.** O CI roda Rust e Python em `os: [ubuntu-latest, macos-14, windows-latest]`
  ([R/.github/workflows/ci.yml](https://github.com/RyanCodrai/turbovec/blob/c6cf0baba11ddc0b0ec7f95d4024d816df3bd8ec/.github/workflows/ci.yml),
  linhas 24, 285, 361 e 452). Há também um teste de impressão digital da codificação nos três sistemas: *"CI runs it on
  every OS in the matrix and fails if they disagree"* (README).
- O PyPI publica a roda `turbovec-1.0.0-cp39-abi3-win_amd64.whl` (API JSON do PyPI), gerada pelo job *"Windows x64"*
  ([R/.github/workflows/release-pypi.yml](https://github.com/RyanCodrai/turbovec/blob/c6cf0baba11ddc0b0ec7f95d4024d816df3bd8ec/.github/workflows/release-pypi.yml)).
  O `pyproject.toml` declara *"Operating System :: Microsoft :: Windows"*.

### 3.2 Embeddings (locais, por API, FreeLLMAPI)

- **Fora do escopo.** O turbovec não gera embeddings; recebe vetores `float32` de qualquer origem. Logo, aceitaria
  vetores do FreeLLMAPI ou de um modelo local, mas quem chama o modelo é o código em volta.
- Restrição: *"`dim` must be a positive multiple of 8 and `≤ 16384`"* (docs/api.md). As dimensões comuns (384, 768,
  1.024, 1.536) cumprem isso.
- Os números de recall publicados são com embeddings OpenAI (d=1536, d=3072) e GloVe (d=200). Não há medição com
  modelo multilíngue nem com texto em pt-BR. A issue aberta [#370](https://github.com/RyanCodrai/turbovec/issues/370)
  diz que a vantagem de recall *"holds for real embeddings but loses to FAISS on isotropic Gaussian and weak-block
  sparse"*, e a [#332](https://github.com/RyanCodrai/turbovec/issues/332) registra uma perda de 1,5 a 3,5 pontos de
  recall@10 pela tabela de consulta de 7 bits. Como é compressão com perda, a busca é aproximada mesmo num índice
  pequeno.

### 3.3 Acompanhar mudanças (`git pull`, edição externa)

- **Só a parte do índice.** `IdMapIndex.remove(id)` é O(1) e `sync(path)` grava só o que mudou: *"An append writes the
  new 32-row blocks plus a commit header. A removal writes no block at all"*, e *"Every sync is durable when it
  returns"* (docs/api.md, "Incremental saves").
- Descobrir **quais** arquivos mudaram, recortar de novo e regerar os embeddings fica com o código em volta. Não há
  watcher.
- Limites declarados: *"Two processes syncing one path concurrently is not supported"*, e a carga não confere a
  integridade do conteúdo: *"Damage arriving from outside the writer ... loads clean and changes search results
  silently"* (docs/api.md, "Versioning and limits"). Num hub, o índice seria reconstruível, então isso pesa pouco.

### 3.4 Licença e maturidade (API do GitHub e PyPI, 03/10/2026)

- **Licença:** MIT.
- **Repositório:** criado em 26/03/2026, 17.276 estrelas, 1.479 forks, 20 issues/PRs abertas, último push em
  03/10/2026. Linguagens: Rust e Python.
- **Versões:** `turbovec` 1.0.0 no PyPI (18/08/2026) e no crates.io (`turbovec/Cargo.toml`), 19 versões no PyPI desde
  maio. Python `>=3.9`, única dependência `numpy>=1.20`.
- **Leitura:** projeto maduro e bem testado para o que se propõe (CI em três sistemas, testes de durabilidade
  adversariais, gate de mutantes). A maturidade não muda a conclusão, porque o que ele se propõe não é a camada de busca.

## 4. Comparação com as candidatas da §10.4.1 e com o zvec-grep

**A comparação não é justa**: as outras quatro são ferramentas que indexam uma pasta de Markdown e respondem a um
agente; o turbovec é uma biblioteca que um desenvolvedor usaria para construir uma delas. A tabela abaixo serve só
para mostrar o que faltaria construir. Os dados das outras colunas vêm da pesquisa 19
([pesquisa-19-zvec-grep.md](pesquisa-19-zvec-grep.md), seção 4) e não foram pesquisados de novo.

| Ponto | turbovec | zvec-grep | markdown-vault-mcp | grooveseek / obsidian-hybrid-search |
|---|---|---|---|---|
| O que é | biblioteca de índice vetorial (Rust + Python) | ferramenta de busca local para agentes | servidor MCP sobre vault | ferramentas de busca sobre vault |
| Lê a pasta e quebra Markdown | **não** | sim, por título | sim, por título | sim (grooveseek por título) |
| Gera embeddings | **não** (recebe vetores) | sim, modelos locais ou Qwen remoto | sim, FastEmbed/Ollama/endpoint compatível | sim (`bge-m3` / `multilingual-e5-small`) |
| Busca lexical (BM25) | **não**, só filtro por lista de ids vinda de fora | sim | sim | não consta na §10.4.1 |
| Acompanha mudanças nos arquivos | **não**; só remoção O(1) e `sync` incremental do índice | watcher + reconciliação | hash + reconciliação, pull loop do git | grooveseek: watcher cobre `git pull` |
| Interface para agente | **nenhuma** (API Python/Rust) | MCP + CLI | MCP | CLI (+ daemon no grooveseek) |
| Windows nativo | sim, CI e roda `win_amd64` | sim, CI unitário | README não menciona | grooveseek sim |
| Licença / maturidade | MIT, 17,3 mil estrelas, v1.0.0 | Apache-2.0, 3,9 mil estrelas, v0.2.2 | MIT, 34 estrelas, v5.0.0 | 8 / 107 estrelas |

## 5. Conclusão

- **Inteiro: não serve.** O turbovec não é uma camada de busca; é um índice vetorial para quem constrói uma.
- **Como parte: só se o hub construísse a própria camada.** Mesmo então, a vantagem dele (memória e velocidade em
  milhões de vetores) não aparece na escala de um hub pessoal, e a busca dele é aproximada por construção. Um índice
  float32 simples, ou o que a ferramenta escolhida já traz, resolve.
- **Recomendação:** **não incluir no spike** do ticket "Camada de busca" e não substituir nenhuma candidata. Ele não
  compete com o zvec-grep nem com o markdown-vault-mcp; está uma camada abaixo deles. Quem decide é o Gustavo, no
  ticket "Camada de busca".
