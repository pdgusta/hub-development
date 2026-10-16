# Pesquisa ampla: lugares e mecanismos de busca — síntese

Ticket "Pesquisa ampla: lugares e mecanismos de busca" (`.scratch/context-hub/issues/50-...`). Escrita pelo maestro
(Claude Opus 5.5) em 2026-10-13, a partir de:
- o laço (5 ondas, 5526 itens);
- as cinco etapas (limpeza, triagem, conferência, auditoria e síntese);
- a varredura de atualidade (S2) e a régua dos finalistas (S3);
- a rodada de cobertura de 2026-10-14 (S6): junção das entidades, stack classificada por área e uma segunda régua
  com 55 itens do catálogo (27 de busca e 28 de stack).

**Tudo o que a pesquisa achou** está no anexo [`pesquisa-50-inventario.md`](pesquisa-50-inventario.md), gerado por
script. Ali estão as 169 entidades de busca, as 184 de stack (por área), os 292 conceitos, as 92 fichas de régua e o que
ficou de fora, com a regra de cada exclusão. Esta síntese discute o que importa para as decisões.

**Onde estão os dados (todos em `.scratch/context-hub/laco/`):**
- catálogo consolidado: `sintese/catalogo-final.json`, e depois da junção, `sintese/catalogo-entidades.json`;
- áreas da stack: `sintese/stack-areas.json`;
- conceitos: `sintese/conceitos-final.json`;
- achados da S2 com citação: `sintese/s2/*.json`;
- régua com citação: `sintese/s3/*.json` (finalistas, tabela em `sintese/regua.md`) e `sintese/s6/*.json` (segunda
  lista, com a regra em `sintese/s6-lista.json`).

**Como ler as afirmações:** cada fato vem de um desses arquivos, e eles guardam a URL e a citação literal. O que diz
"não verificado" (NV) não tem fonte primária. As estimativas de dias são minhas e não foram medidas.

## 0. Resumo de uma tela

- **A busca nativa do CouchDB não serve ao hub.** O LiveSync grava as notas em pedaços e com E2EE, então o Nouveau,
  o Clouseau e o Mango indexam documentos que não contêm o texto. "Dentro do MCP do banco" passa a significar outra
  coisa: o próprio MCP mantém um índice do texto já decifrado, alimentado pelo feed de mudanças do CouchDB.
- **Nenhuma ferramenta pronta cumpre a régua inteira.** A régua é:
  - Windows nativo;
  - MCP;
  - português na parte léxica;
  - endpoint OpenAI-compatível para embeddings;
  - acompanhar o disco sozinha;
  - filtrar por frontmatter.

  As duas que mais se aproximam são **obsidian-hybrid-search** (beta, CI em 3 sistemas, filtro por frontmatter,
  watcher e `OPENAI_BASE_URL`) e **memtomem** (alpha, CI no Windows, watcher e `BASE_URL`). As duas falham no mesmo
  ponto: o BM25 é do SQLite FTS5, **sem stemmer de português**.
- **Português na parte léxica existe nos motores, não nas ferramentas.** Tantivy, Lucene/OpenSearch, Bleve,
  Xapian, Orama e Pagefind têm stemmer de português com fonte. As ferramentas prontas para agentes usam FTS5 com
  `unicode61` ou `porter`; o `porter` é stemmer de inglês.
- **Embeddings resolvem a metade semântica.** O multilingual-e5-small é o padrão de várias ferramentas. No MTEB-BR,
  o EmbeddingGemma-300m é o melhor modelo aberto pequeno (0,649, 13º de 93). O bge-m3 é a opção de qualidade.
- **O repasse de MCP está pronto e é leve.** O TBXark/mcp-proxy (binário Go para Windows) e o 1MCP (CI no Windows)
  juntam o MCP do banco e um MCP de busca num endpoint só, que pode ser exposto na tailnet.
- **A cópia leve para sandbox sem tailnet é viável.** O Pagefind (binário Windows, stemmer de português) gera um
  pacote estático. Um arquivo SQLite com FTS5 é a outra via.
- **Recomendação** (a decisão é do Gustavo, em "Camada de busca"):
  1. spike de bancada **obsidian-hybrid-search contra memtomem**, sobre uma cópia de conteúdo real em pt e en;
  2. o resultado decide entre ficar com a ferramenta pronta no disco mais o repasse (C2) ou montar o índice dentro
     do MCP do banco (C3);
  3. a cópia leve (C4) entra depois, só para sandbox.
- **A segunda régua não muda a recomendação; ela a reforça e dá peças à C3.** Ela cobriu os motores mais citados do
  catálogo:
  - **Weaviate e Milvus** (servidor) só rodam com WSL ou Docker;
  - **Elasticsearch e Solr** têm português e MCP, mas são JVM pesada, e o MCP do Solr pede Docker;
  - **Chroma** não tem português léxico;
  - **Whoosh e lunr.js** estão parados (2016 e 2020).

  Para montar um índice próprio, há bibliotecas com analisador de português e Windows confirmado: **Bleve** (Go, CI no
  Windows), **Xapian** (C++, GPL), **Lucene.NET** (.NET, beta) e **Snowball** com **stopwords-pt** como peças soltas.
  Para o grep no disco, o **ripgrep** é a escolha, e o The Silver Searcher e o The Platinum Searcher estão parados.
- **Na stack, as peças da construção estão confirmadas para Windows nativo:**
  - o SDK Python do MCP (v2, CI no Windows);
  - python-frontmatter e PyYAML;
  - Watchman (binário Windows) ou watchdog;
  - lingua-py, para detectar pt ou en por nota;
  - Docling e pandoc, para importar anexos;
  - ONNX Runtime e Ollama, como reserva local do FreeLLMAPI.

  Ficam de fora:
  - LocalAI, que só roda com Docker ou WSL;
  - n8n: o início rápido usa Docker, o Windows nativo ficou NV, e a licença é restritiva;
  - SurrealDB, que trocaria o CouchDB e tem licença BSL;
  - Dataview e Templater, que exigem o Obsidian aberto (detalhes na §4).

## 1. Como se chegou aqui

| Etapa | O que entrou → o que saiu | Quem | Custo medido |
|---|---|---|---|
| Laço (5 ondas) | 98 células → 5526 itens; curva de novos 100%, 76%, 37%, 27%, 22% | FreeLLMAPI (267 modelos) | 7388 tentativas, gratuitas |
| Limpar | 298 ambíguos decididos; 5433 itens, 193 em quarentena; 606 READMEs de 1439 repositórios (620 inventados); 767 sites com texto; 874 cartões de conceito | Tear (Sonnet), scripts | conversa do Tear, não medida |
| Triagem | 1363 repositórios e sites, metade para cada lado; 874 conceitos | FreeLLMAPI (2 modelos por item) e Haiku 5.5 | FreeLLMAPI 4,70 milhões de tokens gratuitos; Haiku 12,0 milhões |
| Conferência | 1063 itens úteis, com dúvida ou com divergência | Sonnet 5.5 (Salina, Tear e Osmose) | 14,2 milhões de tokens Sonnet |
| Auditoria | 195 itens (10% da conferência e 10% dos conceitos) | Opus 5.5 | 2,56 milhões de tokens Opus |
| S1 Consolidar | 475 entidades úteis (240 de busca, 235 de stack); 292 conceitos | script e 1 juiz Sonnet | 0,05 milhão Sonnet |
| S2 Atualidade | 10 temas, 80 achados com citação | Sonnet com web | 0,73 milhão Sonnet |
| S3 Régua | 36 finalistas (só 12 deles estavam no catálogo; 24 vieram da S2 e das pesquisas antigas; depois da junção, o Tantivy também casou com o catálogo: 13 e 23) | Sonnet com web | 0,90 milhão Sonnet |
| S6 Junção | 475 → 353 entidades (169 de busca, 184 de stack); ex.: Elasticsearch juntou 25 variações | script e 1 juiz Sonnet (a 1ª rodada foi descartada) | 0,14 milhão Sonnet |
| S6 Stack por área | 184 entidades em 12 áreas; 178 em acordo, 6 divergentes | FreeLLMAPI (2 modelos, 3º desempata) | ~600 tentativas, gratuitas |
| S6 Régua | 55 itens do catálogo, por regra: 27 de busca e 28 de stack | Sonnet com web | 1,04 milhão Sonnet (piloto incluído) |

**Qualidade da cadeia** (auditoria do Opus):
- **Projetos:** o veredito do Sonnet errou o essencial em 3 de 107 itens (2,8%).
- **Conceitos sem fonte:** 11 erros graves em 88 (12,5%).
- **Triagem contra o veredito final** (só nos itens conferidos):

  | Quem triou | Acertos |
  |---|---|
  | Dois modelos gratuitos que concordam | 83% |
  | Haiku | 75% |
  | Um modelo gratuito sozinho | 70% |

## 2. O que mudou o desenho

### 2.1 O CouchDB não enxerga o texto das notas

O ticket listava como lugares possíveis "dentro do MCP do banco" e "o MCP do banco repassando à busca do disco".
A pesquisa mostrou que a busca do próprio banco está fechada, por dois motivos:
- **O CouchDB tem busca, mas só léxica:**
  - o Nouveau (Lucene 10, servidor JVM separado, experimental) tem analisador `portuguese` (`s2/t01`,
    `s3/couchdb-nouveau.json`);
  - o Clouseau tem o PortugueseAnalyzer;
  - o Mango tem índice `$text`;
  - nenhum tem busca vetorial, e o Windows nativo ficou NV nos dois servidores.
- **Ele indexaria o que está no banco, e o hub guarda ali pedaços cifrados.** A E2EE do LiveSync está decidida
  ("Onde o servidor mora"), e o LiveSync divide as notas em pedaços (spike "CouchDB e LiveSync"). O texto só existe
  decifrado no disco de cada par e no MCP, que tem a frase-senha.

Consequência: um índice "dentro do MCP do banco" é um índice **do MCP**. Ele é alimentado pelo `_changes` do CouchDB
e pelo texto que o MCP já decifra para ler e gravar. Esse desenho tem duas vantagens que nenhuma ferramenta de disco
tem: não depende do watcher do disco e serve os clientes pela tailnet sem cópia.

### 2.2 As ferramentas de disco convivem com o LiveSync pelas pastas com ponto

O sincronizador decidido não leva ao banco pastas com ponto em qualquer nível ("Revisão do sync"). Por isso, onde
cada ferramenta guarda o índice decide se ela convive bem com o LiveSync:

| Ferramenta | Onde guarda o índice | Convivência |
|---|---|---|
| ck | `.ck/` | segura, por herança da regra |
| zvec-grep | `.zvec-grep/` | segura, por herança da regra |
| obsidian-hybrid-search | **arquivo** `.obsidian-hybrid-search.db` na raiz do cofre | a regra fala de pastas; se cobre arquivo com ponto é NV, e precisa de exclusão explícita no CLI e no plugin |
| memtomem | fora da pasta (SQLite próprio) | segura |
| markdown-vault-mcp | fora da pasta | segura |
| obsidian-brain | sem informação do local do índice | **grava notas** na pasta, o que o põe no caminho da edição concorrente |
| markdown-vault-mcp | — | **grava notas** na pasta, o que o põe no caminho da edição concorrente |

As duas que gravam notas só podem entrar com a escrita desligada, porque a escrita do hub é do MCP do banco, com
`base_rev`.

### 2.3 A régua separa "pronto" de "encaixa"

A régua cheia (Windows, MCP, português, endpoint OpenAI, watcher e frontmatter) deixou os finalistas em quatro
grupos (tabela completa em `sintese/regua.md`):

- **Encaixam com ressalvas:**
  - obsidian-hybrid-search: beta, CI em 3 sistemas operacionais, filtro por frontmatter, watcher chokidar,
    `OPENAI_BASE_URL`, e5 multilíngue e reranker multilíngue opcional;
  - memtomem: alpha, CI no Windows, watcher, `BASE_URL` e chunking por título; o filtro por campo arbitrário do
    frontmatter é NV;
  - LocalVectorSearchMcp: .NET 10, 0.1.x, CI no Windows, watcher opcional e endpoint OpenAI; não filtra por campo do
    frontmatter;
  - markdown-vault-mcp: v5, estável, filtro por frontmatter e endpoint OpenAI; **Windows NV** (CI só Ubuntu) e grava
    na pasta.
- **Prontas, mas com um impedimento claro:**
  - qmd: Windows NV e só modelos GGUF locais, sem endpoint;
  - ck: sem endpoint, otimizado para código e sem busca semântica no binário Windows;
  - grepai: feito para código e sem commit desde 10/09;
  - vexor: sem watcher, sem filtro por frontmatter confirmado;
  - devrag: só reindexa na partida e só vetor;
  - zvec-grep: o endpoint remoto só aceita o provedor Qwen, e o filtro por frontmatter é NV;
  - obsidian-semantic-mcp: só Ollama, Node 24;
  - obsidian-brain: sem endpoint OpenAI e grava na pasta;
  - kb-index: indexação agendada, sem watcher;
  - local-notes-search-mcp: indexação manual, só vetor;
  - vault-cortex: Docker, modelos só em inglês.
- **Fora pela premissa** (Windows nativo, sem Docker, Obsidian que pode ficar fechado):
  - Typesense: só WSL ou Docker;
  - vault-cortex: Docker;
  - Omnisearch, Local REST API e o Smart Connections: exigem o Obsidian aberto, que pode ficar fechado ("Revisão do
    sync", R75). Servem de conveniência na máquina, não de camada de busca.
- **Motores e serviços:**
  - Meilisearch: binário Windows, MCP embutido experimental e embedder REST configurável; o stemmer de português
    não foi documentado;
  - Qdrant: binário Windows e MCP oficial, mas só com FastEmbed;
  - OpenSearch: zip com JDK, analisador `portuguese`/`brazilian` e MCP oficial; pesado (JVM, cluster);
  - Manticore: licença GPLv3 e Docker para o Buddy.

  Todos exigem um alimentador próprio, porque nenhum lê a pasta.

**Os mais citados do catálogo (segunda régua, `s6/`).** Eles se dividem em quatro grupos:

- **Fora pela premissa:**
  - Weaviate e o servidor do Milvus: só com WSL ou Docker. O Milvus Lite, embutido em Python, roda no Windows;
  - pgvector e pg_bigm: exigiriam um PostgreSQL ao lado do CouchDB;
  - Pyserini: Windows NV, Java 21 e PyTorch. Serve de bancada, não de busca do hub.
- **Serviços pesados, com português e MCP:**
  - Elasticsearch: zip Windows com JDK, analisador `portuguese` e MCP oficial; licença AGPL, SSPL ou ELv2;
  - Solr: testado no Windows, quatro stemmers de português e MCP da Apache em incubação, mas o MCP pede Docker.

  Os dois são exagero para duas máquinas.
- **Parados ou sem português:**
  - Whoosh: último release em 2016, sem stemmer de português;
  - lunr.js: parado desde 2020;
  - elasticlunr.js: procura mantenedor;
  - Chroma: busca léxica só por substring ou regex;
  - Haystack e LlamaIndex: frameworks grandes, que serviriam só de cola.
- **Peças para montar** (detalhes na C3):
  - léxico com português: Bleve, Xapian, Lucene e Lucene.NET, Snowball e stopwords-pt;
  - vetor: FAISS (wheels Windows), hnswlib e Annoy (CI no Windows), todos só vetor;
  - grep: ripgrep (binário Windows, ativo); ripgrep-all para PDF e DOCX (AGPL);
  - Zoekt: Windows NV e foco em repositórios.

### 2.4 Português: onde ele existe

Português na busca tem duas metades: a léxica (stemmer, stopwords, acentos) e a semântica (o modelo de embeddings).

**Parte léxica com fonte** (`s2/t05`, S3 e S6):

| Peça | O que tem |
|---|---|
| Tantivy | `Language::Portuguese` |
| Lucene / OpenSearch / Nouveau | PortugueseAnalyzer (stemmer RSLP, Light e Minimal) |
| Lucene.NET | PortugueseAnalyzer, com stopwords e Snowball (beta) |
| Elasticsearch | analisador `portuguese`, com stopwords e stemmer light |
| Solr | quatro stemmers de português |
| Bleve | analisador `pt` pronto (minúsculas, stopwords e stemmer light), CI no Windows |
| Xapian | stemmer Snowball de português, stopwords |
| Snowball | o algoritmo de português (europeu e brasileiro), como peça para um analisador próprio |
| stopwords-pt | lista de stopwords (de 2016, sem stemmer) |
| Whoosh, Chroma, Milvus | **sem** português léxico |
| Orama | `@orama/stemmers` |
| Pagefind | stemming `pt` |
| Qdrant | índice de texto do payload com Snowball por idioma |
| SQLite FTS5 | **não tem stemmer de português**; o `unicode61 remove_diacritics=2` resolve os acentos; o `fts5-snowball` daria o stemmer, mas é extensão a compilar, com Windows NV |

**Parte semântica:**
- EmbeddingGemma-300m: 0,649 no MTEB-BR, 13º de 93 (`s2/t06`, arXiv 2607.04581). A licença Gemma exige aceite.
- multilingual-e5-small: MIT, 384 dimensões, prefixos `query:`/`passage:`, limite de 512 tokens.
- bge-m3: MIT, 8K de contexto, ~1,2 GB no Ollama.
- granite-embedding-107m-multilingual e Qwen3-Embedding-0.6B: ambos Apache-2.0.
- Jina v3: CC-BY-NC, **evitar**.

**Rerank:** bge-reranker-v2-m3, com versão ONNX.

**Idioma por nota:** o lingua-py detecta pt e en offline, com wheels Windows, e serve para escolher o analisador por
nota. A precisão cai em textos curtos e em notas que misturam os dois idiomas.

**Lacuna:** não há benchmark em notas Markdown que misturam pt e en. O spike tem de medir isso.

### 2.5 Os lugares próprios do hub, agora preenchidos

| Lugar | Mecanismo léxico com português | Vetorial / híbrido | Pronto hoje |
|---|---|---|---|
| Disco de cada máquina | ferramentas: FTS5 sem stemmer de português; motores: Tantivy, Bleve, Xapian; grep: ripgrep | obsidian-hybrid-search, memtomem, LocalVectorSearchMcp, markdown-vault-mcp, zvec-grep | sim, com as ressalvas de 2.3 |
| Dentro do MCP do banco (índice do MCP, alimentado por `_changes`) | conforme a linguagem do MCP: Tantivy (Rust/Python), Bleve (Go), Lucene.NET (.NET), Xapian (C++, GPL) ou FTS5 com `fts5-snowball` | sqlite-vec, LanceDB, FAISS ou hnswlib, com embeddings pelo FreeLLMAPI ou ONNX local | **não: é montagem** |
| MCP do banco repassando à busca do disco | o da ferramenta de disco | o da ferramenta de disco | sim: TBXark/mcp-proxy, 1MCP ou FastMCP `mount` (se o MCP for Python) |
| Serviço na rede | OpenSearch (`portuguese`), Meilisearch (Charabia, sem stemmer documentado), Manticore | Meilisearch híbrido, Qdrant, OpenSearch k-NN | sim, mas pesado e sem leitura da pasta |
| Cópia leve no cliente ou sandbox | Pagefind (stemmer `pt`), Orama (stemmer `pt`), SQLite FTS5 exportado; lunr.js e elasticlunr.js estão parados | Orama com vetores pré-calculados | sim, para leitura; sem MCP (a montar: um MCP mínimo sobre o pacote) |
| Lado do Obsidian | Omnisearch (BM25), a busca do Obsidian (Local REST API, CLI) | Smart Connections e Copilot com Miyo | só com o Obsidian aberto |

### 2.6 Quem fica atendido em cada situação

| Situação → | Agente na máquina | Cliente pela tailnet | Sandbox sem tailnet | Tailnet fora do ar | Obsidian fechado |
|---|---|---|---|---|---|
| Disco (ferramenta pronta) | sim | não (só com repasse) | não | sim, local | sim |
| Disco + repasse (proxy na tailnet) | sim | sim (MCP agregado do par) | não | sim, local | sim |
| Índice no MCP do banco | sim | sim (o mesmo MCP de leitura) | não | sim, no par local | sim |
| Serviço na rede | sim | sim | não | só no par que hospeda | sim |
| Cópia leve | sim (redundante) | sim | **sim** (pacote levado junto) | sim | sim |
| Lado do Obsidian | só com o Obsidian aberto | não | não | sim, local | **não** |

## 3. Combinações

### C1. Leve: uma ferramenta pronta no disco de cada par

- **Peças:**
  - obsidian-hybrid-search **ou** memtomem em cada máquina, sobre a pasta do hub, como MCP stdio do agente local;
  - embeddings pelo FreeLLMAPI (`OPENAI_BASE_URL`), com o e5-small local de reserva;
  - a escrita continua no MCP do banco.
- **Pronto:**
  - a busca híbrida;
  - o watcher;
  - o MCP;
  - os filtros por frontmatter (no obsidian-hybrid-search).
- **Falta montar** (~1 dia, estimativa):
  - instalação e configuração nos dois pares;
  - exclusão explícita do `.obsidian-hybrid-search.db`;
  - checar se o FreeLLMAPI serve o modelo de embeddings escolhido (NV);
  - a entrada no contrato e nas portas de entrada (contrato global, skill e MCP de cada harness).
- **Convivência:**
  - só leitura;
  - o watcher pega o que o CLI do LiveSync grava;
  - o índice fica local e não viaja, então cada par reindexa.
- **Riscos:**
  - alpha/beta;
  - BM25 sem stemmer de português;
  - clientes sem busca.
- **O spike precisa provar:**
  - qualidade em português (léxica e semântica);
  - tempo de reindexação depois de uma rajada do LiveSync;
  - consumo de memória;
  - a instalação no Windows sem WSL.

### C2. Leve com alcance: C1 + repasse na tailnet

- **Peças:**
  - C1 em cada par;
  - o TBXark/mcp-proxy ou o 1MCP em cada par, juntando o MCP do banco (só leitura, para clientes) e o MCP de busca
    num endpoint HTTP com token, exposto só na tailnet, como o MCP de leitura já decidido.
- **Pronto:** o proxy (binário Windows).
- **Falta montar** (~0,5 a 1 dia a mais):
  - a configuração do proxy;
  - o token;
  - o grant da tag dos clientes;
  - o teste em cada harness.
- **Ganho:** os clientes ganham busca sem cópia.
- **Riscos:**
  - mais um processo por par;
  - dois MCPs com nomes de ferramentas que precisam ser coerentes.
- **O spike precisa provar:**
  - latência pela tailnet;
  - que o proxy repassa ferramentas stdio no Windows.

### C3. Robusta: índice dentro do MCP do banco

- **Peças:**
  - o fork do MCP do es617 (já decidido, com `base_rev`) ganha um índice próprio por par;
  - parte léxica: Tantivy (stemmer de português) ou SQLite FTS5 + `fts5-snowball`; conforme a linguagem do MCP,
    também Bleve (Go), Lucene.NET (.NET) ou Xapian (C++, GPL), todos com analisador de português (S6);
  - parte vetorial: sqlite-vec ou LanceDB; FAISS ou hnswlib se o índice vetorial ficar à parte;
  - detecção do idioma por nota com o lingua-py, se o analisador mudar por idioma;
  - fusão RRF;
  - rerank bge-reranker-v2-m3 opcional;
  - embeddings pelo FreeLLMAPI, com reserva local em ONNX (FastEmbed ou e5-small);
  - o índice é alimentado pelo `_changes` do CouchDB local, com o texto já decifrado pelo MCP;
  - chunking por título e frontmatter como filtro;
  - as ferramentas `search` e `get` ao lado das de gravação (a interface que a "Camada de busca" pede: buscar, gravar
    e estado do sync).
- **Pronto:** as peças (bibliotecas estáveis).
- **Falta montar** (~5 a 8 dias, estimativa NV):
  - o consumidor do `_changes`;
  - a montagem do texto a partir dos pedaços (o MCP já faz isso para ler);
  - o esquema do índice;
  - a reindexação total;
  - as ferramentas MCP;
  - os testes;
  - a linguagem do MCP do es617, que define a biblioteca: Python (tantivy-py, sqlite-vec, LanceDB, SDK do MCP v2 com
    CI no Windows), Node (Orama, sqlite-vec, SDK TypeScript do MCP sem CI no Windows comprovado), Go (Bleve) ou .NET
    (Lucene.NET).
- **Ganhos:**
  - um índice só para agentes locais e clientes;
  - não depende do watcher do disco nem do Obsidian;
  - português léxico de verdade;
  - a escrita e a busca no mesmo processo, então a busca vê a gravação na hora.
- **Riscos:**
  - construção própria (manutenção);
  - cada par reconstrói o próprio índice (o índice não replica);
  - o custo dos embeddings na carga inicial (cota do FreeLLMAPI).
- **O spike precisa provar:**
  - o tempo de reindexação total do conteúdo real;
  - a qualidade contra C1;
  - a estabilidade do consumidor do `_changes` com a E2EE.

### C4. Para sandbox: cópia leve exportada

- **Peças:**
  - uma tarefa agendada em cada par gera um pacote Pagefind (stemmer `pt`) ou um SQLite FTS5 só de leitura, a
    partir da pasta (só o que o contrato permitir sair);
  - o sandbox leva o pacote junto;
  - um MCP mínimo de leitura sobre o pacote, ou a ferramenta da própria sandbox.
- **Falta montar** (~1 a 2 dias):
  - o gerador;
  - o filtro do que sai;
  - o MCP mínimo.
- **Riscos:**
  - fica velho até a próxima exportação;
  - dado de cliente sai da máquina, então segue a regra de dados de cliente.
- **O spike precisa provar:** só o tamanho e o tempo de geração; a qualidade é a do Pagefind.

### C5. Reserva: duas vias juntas

- **Peças:** C3 como principal e C1 como reserva no par. Se o MCP do banco cair, o agente local ainda busca no disco.
  A C4 cobre a sandbox.
- **Custo:** C3 + C1 + C4. Só se justifica se a busca virar caminho crítico do contrato (o checkpoint e a nota de
  retomada já dependem do disco, não da busca).

**Leve contra robusta, em uma linha:**
- **C1 e C2** compram tempo com software de terceiros em alpha/beta, sem português léxico.
- **C3** compra controle e português com 1 a 2 semanas de construção.
- **C4** é complemento, não alternativa.

## 4. A stack além da busca

Depois da junção, o catálogo tem **184 entidades de stack**. O FreeLLMAPI as classificou em 12 áreas (2 modelos; um 3º
desempata), e a lista completa, área por área, está no inventário (§2). A régua com fonte (`s6/`) cobriu as 3 mais
citadas de cada área com encaixe "central" unânime. Ficaram fora da régua o que já está decidido (o CouchDB, a
especificação do MCP e o registro de plugins do Obsidian), o Node.js, o DistilBERT e o fastText.

O encaixe dado pelos modelos gratuitos é generoso: 94 das 184 saíram como "central". Por isso, abaixo vale o que a
régua confirmou; o resto é "só README".

| Área (entidades) | Confirmado com fonte (`s6/`) | Também no catálogo (só README) |
|---|---|---|
| MCP (10) | **SDK Python v2.3** (CI no Windows; a v2 mudou a API e pede Python 3.11+); **servidores de referência** (CI no Windows; modelos, não produção); SDK TypeScript v2.3 (**Windows NV**: CI só Ubuntu) | FastMCP (S3: 4.1, `mount`), mcp-go, rmcp (Rust), proxies da S3 |
| Sync e CouchDB (18) | **PouchDB** 9.0.0 (2024; sem CI no Windows; cliente JS que replica, útil a um MCP em Node ou à cópia leve, mas não substitui o LiveSync) | couchdb-python, couchdb-nano, `_changes`, Mango, views, Yjs (CRDT) |
| Markdown e frontmatter (32) | **python-frontmatter** 1.3.0 (2026) e **PyYAML** 6.0.3 (wheels Windows; usar `safe_load`); gray-matter (Node, último release em 2019, NV em idiomas) | remark e remark-frontmatter, unified, markdown-it(-py), mistune, Goldmark, js-yaml |
| Texto em português (21) | **lingua-py** (detecta pt e en, wheels Windows); **spaCy** 3.8 (modelos `pt_core_news`, opcional); **stopwords-pt** (lista de 2016) | NLTK, Stanza, Unidecode, UDPipe, OpenNLP |
| Embeddings e rerank (18) | **ONNX Runtime** 1.31 (wheels Windows; plano B ao FreeLLMAPI); Transformers 5.19 (pesado, PyTorch); ort (Rust, RC, Windows NV) | FastEmbed (S3), sentence-transformers (S6, busca), XLM-RoBERTa, Transformers.js |
| Modelos locais e gateways (8) | **Ollama** 0.40 (app nativa no Windows, base_url OpenAI; duplica o FreeLLMAPI); LocalAI (**só Docker ou WSL**); GPT4All (parado, sem endpoint de embeddings) | LiteLLM, llamafile, llama-cpp-python |
| Extração de texto (12) | **Docling** 2.138 (Windows, PDF/DOCX/PPTX/HTML → Markdown, tem MCP; idiomas do OCR NV); **pandoc** 3.12 (binário Windows; GPL, usar como processo); Apache Tika 4.1 (Java 17) | Unstructured, MarkItDown/PyMuPDF, Marker, Trafilatura |
| Bancos e armazenamento (23) | **SQLite** 3.54 (DLL nativa; índice derivado, não replica); rusqlite (Rust); SurrealDB (troca o CouchDB, BSL: **não**) | DuckDB, RocksDB, diskcache, LevelDB |
| Eventos, filas e vigias (14) | **Watchman** (binário Windows, ativo); **watchdog** 6.0 (ReadDirectoryChangesW; sem release desde 2024-11; não filtra os eventos duplicados do LiveSync) | NATS, nng, Celery, Chokidar (o watcher do obsidian-hybrid-search) |
| Frameworks de agente e RAG (9) | n8n (início rápido com Docker, Windows NV, licença Sustainable Use: **não**) | LangChain, Mem0, Pydantic AI, Langfuse |
| Obsidian (6) | obsidian-api (só tipos, para um plugin próprio); Dataview 0.5.70 (sem release desde 2025-04); Templater (AGPL, executa JS e comandos). **Os três exigem o Obsidian aberto** | Advanced URI |
| Serviço e API (1) e outros (6) | — | FastAPI; Git, Docker Desktop, fzf |

**O que isso muda na construção:**
- se o MCP do banco ficar em **Python**, todas as peças têm Windows confirmado: o SDK do MCP v2,
  python-frontmatter/PyYAML, lingua-py, ONNX Runtime e a parte léxica (tantivy-py) da C3. Em Node, o SDK do MCP
  e o PouchDB não têm CI no Windows;
- o **watcher** de uma ferramenta de disco (C1/C2) tem de aguentar as rajadas do LiveSync: o watchdog não filtra
  eventos duplicados, e o Watchman é um serviço a mais;
- os **anexos** (até 200 MiB) entram na busca só por extração: o Docling é o mais completo; o pandoc e o Tika
  servem a casos menores;
- não há candidato que substitua o CouchDB/LiveSync com vantagem (SurrealDB: BSL e outra replicação).

**Ficou de fora com motivo:**
- LangChain e LlamaIndex: frameworks pesados para um índice pequeno;
- DistilBERT, GloVe e fastText: não são busca de trechos;
- NATS, nng e Redis Streams: mensageria que o hub não usa;
- Elasticsearch e Logstash: escala de cluster.

**Conceitos** (292 depois do filtro): os mais citados confirmam o que a busca do hub precisa ter:
- busca híbrida (67 cartões);
- BM25 (25);
- filtro por frontmatter (15) e por metadados (13);
- stemming (14) e stemming em português (9);
- remoção de acentos;
- RRF.

Nenhum conceito trouxe peça que não esteja acima.

## 5. Recomendação para "Camada de busca" (a decisão é do Gustavo)

1. **Spike de bancada: obsidian-hybrid-search contra memtomem**, nos dois casos no disco, sobre uma cópia de conteúdo
   real do hub em pt e en.
   - **Corpus de teste:** 30 a 40 perguntas com resposta conhecida.
   - **Métricas:**
     - acerto nos 5 primeiros e MRR;
     - BM25 sozinho contra híbrido;
     - e5-small local contra o embedding do FreeLLMAPI;
     - reindexação depois de uma rajada do CLI do LiveSync;
     - memória;
     - instalação no Windows sem WSL.
   - Isso troca a recomendação antiga (zvec-grep contra memtomem): o zvec-grep fica atrás na régua (endpoint só
     Qwen, frontmatter NV).
2. **O resultado decide o caminho:**
   - se a ferramenta pronta acertar bem em português, **C2** (C1 + repasse na tailnet);
   - se o português léxico pesar, ou se os clientes precisarem de busca igual à local, **C3**, com um protótipo de
     1 dia antes (Tantivy + sqlite-vec alimentados pelo `_changes`) para medir a reindexação total.
3. **C4** quando surgir a primeira sandbox de verdade.
4. **Fatos a confirmar antes:**
   - se o FreeLLMAPI serve um modelo de embeddings multilíngue (e qual);
   - a linguagem do MCP do es617;
   - se a exclusão de pastas com ponto do LiveSync cobre arquivos com ponto.

## 6. Aprendizados para o template "suite de busca" do acervo do maestro

- **Geradores sem busca na web inventam e envelhecem.** Nenhum modelo do FreeLLMAPI buscou, mesmo quando o pedido
  mandava. De 52% a 76% das URLs eram reais, e nenhuma das candidatas atuais apareceu. Daí:
  - a amplitude vem dos modelos gratuitos;
  - a atualidade vem de subagentes com WebSearch em temas estreitos (a S2 custou 0,73 milhão e achou o que o laço
    não achou);
  - a régua vem de subagentes com web na lista curta (a S3).
- **Dois modelos gratuitos que concordam valem mais que um Haiku** (83% contra 75%). A divergência entre eles é o
  melhor filtro para mandar à conferência.
- **A cadeia triagem → Sonnet → Opus é confiável para projetos com fonte** (2,8% de erro grave na auditoria). Para
  conceitos sem fonte, não é (12,5%). Conceitos pedem outra régua.
- **A junção por chave não junta entidades.** Medido na S6: das 475 entidades, sobraram 353. O Elasticsearch
  juntou 25 variações, entre clientes, plugins e páginas. O passo certo tem três partes:
  - candidatos por script (repositório comum e nome contido);
  - um juiz que vê **todos** os membros do grupo. Na 1ª rodada, o mais citado não estava na lista, e o juiz o deixou
    de fora em 19 grupos;
  - ajustes do maestro gravados em arquivo.
- **Os nomes vêm da memória dos modelos; a URL manda.** "Local Search Engine" era o Bleve, "PageAssist" o GPT4All,
  "pt" o The Platinum Searcher e "Portuguese Stemming" o stopwords-pt. Por isso, a régua confere a identidade pela
  URL antes de tudo.
- **A lista curta precisa de regra gravada.** Montada à mão, a lista da S3 tinha só 12 itens do catálogo, e a pesquisa
  pareceu ter "36 finalistas" quando o catálogo tinha 475 entidades úteis. A S6 escolheu por regra, gravada em
  `s6-lista.json`, e o inventário completo vai em anexo, gerado por script.
- **Custos medidos por item:**

  | Etapa | Tokens por item |
  |---|---|
  | Triagem Haiku com README | 14 mil |
  | Conceito | 3,3 mil |
  | Conferência Sonnet | 13,4 mil |
  | Auditoria Opus | 13 a 15 mil |
  | Régua com web (S3) | ~26 mil |
  | Régua com web (S6, com identidade pela URL) | ~19 mil |
  | Juiz de junção (46 grupos) | ~74 mil por rodada |
  | Classificação da stack no FreeLLMAPI | ~3,3 tentativas por item, gratuitas |
  | Tema da S2 | ~73 mil |

  O piloto sempre veio antes da leva.
- **Operação:**
  - despachantes finos, com teto de 40% de contexto e `/clear` entre frentes;
  - mensagem para recruta ocupado fica sem Enter, então conferir com `check`;
  - `/clear` pela CLI no Git Bash pede `MSYS_NO_PATHCONV=1`;
  - processos longos fora do Claude Code (`Start-Process`);
  - índice 0-based dito por extenso no prompt (um lote foi repetido por engano);
  - a API do GitHub limita os subagentes com web; usar feeds atom e `raw.githubusercontent`.
- **Os painéis do Designer** (maré, depois dessalinização) leem um `.js` regravado por script a cada 60 s, sem
  chamar modelo. O serviço do painel precisa sobreviver a arquivo ruim.

## 7. Limites

- **Windows NV** em markdown-vault-mcp, qmd, Nouveau/Clouseau, sparfenyuk/mcp-proxy, FastMCP e txtai (S3), e em
  SDK TypeScript do MCP, PouchDB, Zoekt, Pyserini, pg_bigm, ort, n8n e Templater (S6).
- **A régua com fonte cobre 91 fichas:** 36 da S3 (23 delas de fora do catálogo) e 55 da S6. No catálogo, 40 das 169
  entidades de busca e 28 das 184 de stack têm régua. As outras 129 de busca e 156 de stack têm só o que o README diz
  (inventário, §1 e §2).
- **A API do GitHub limitou** os subagentes da S6, e várias datas de commit e de release vieram de feeds e tags ou
  ficaram NV. O MCP do Weaviate foi rebaixado a NV, porque veio só de um resumo de busca.
- **A área de cada item de stack** foi dada por modelos gratuitos, sem fonte primária; os 6 divergentes ficaram sem
  área.
- Nenhuma medição de qualidade em português foi feita aqui; isso é trabalho do spike.
- As estimativas de dias das combinações são minhas, não medidas.
- O catálogo do laço reflete a memória dos modelos; a S2 cobriu 10 temas, não tudo.
- 1032 itens só com nome e uma citação ficaram fora da triagem por decisão do Gustavo.
- Os arquivos de régua copiam citações das fontes; não reli cada fonte.
