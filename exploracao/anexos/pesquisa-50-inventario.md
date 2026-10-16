# Pesquisa ampla: inventário completo

Gerado por `.scratch/context-hub/laco/inventario.py` (sem modelo). Complementa a síntese (`pesquisa-50-sintese.md`): aqui está **tudo** o que a pesquisa achou e julgou útil, e não só o que a síntese discute. Nada daqui foi apagado dos dados; o que ficou fora está na última seção, com a regra.

**Como ler.**
- *Menções*: quantas vezes os geradores do laço citaram o item (memória dos modelos, não popularidade real).
- *MCP / Win / pt*: o que o README diz (conferência do Sonnet ou auditoria do Opus); "?" = o README não diz.
- *Régua*: arquivo com a régua do hub conferida em fonte primária, com citação (`laco/sintese/s3/` ou `s6/`). Sem arquivo, a régua não foi conferida fora do README.
- *Registro*: quem deu o veredito final (Sonnet na conferência, Opus na auditoria).

Totais: **169 entidades de busca**, **184 de stack**, **292 conceitos**; 68 entidades do catálogo e 23 de fora com régua conferida.

## 1. Busca (169 entidades)

| # | Nome | Menções | Lugar | Mecanismo | MCP | Win | pt | Régua | Registro | URL | Papel |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Meilisearch | 1921 | network_service, disk | full_text, vector, hybrid, embeddings | sim | ? | sim | s3/meilisearch.json | Sonnet | https://github.com/meilisearch/meilisearch | Search engine server with full-text, typo-tolerant and hybrid (semantic + full-text) sear… |
| 2 | Elasticsearch | 1764 | network_service | full_text | ? | ? | ? | s6/elasticsearch.json | Sonnet | https://github.com/elastic/elasticsearch | Distributed search engine (Elasticsearch); README given covers only docs authoring, not f… |
| 3 | Typesense | 1262 | disk, network_service | bm25, full_text, vector, hybrid, embeddings | ? | não | ? | s3/typesense.json | Sonnet | https://github.com/typesense/typesense | Fast typo-tolerant search engine with keyword, vector, hybrid and semantic search; single… |
| 4 | Qdrant | 1252 | network_service | vector, hybrid, embeddings | ? | ? | ? | s3/qdrant.json | Sonnet | https://github.com/qdrant/qdrant | Motor e banco de dados vetorial (Rust) com busca densa, esparsa, hibrida e filtros por pa… |
| 5 | Whoosh | 1236 | library, disk | bm25, full_text | ? | ? | ? | s6/whoosh.json | Opus | https://github.com/mchaput/whoosh | Índice BM25F em disco para busca de texto completo, em Python puro (sem manutenção) |
| 6 | Weaviate | 1155 | network_service | bm25, vector, hybrid, reranker, embeddings | ? | ? | ? | s6/weaviate.json | Sonnet | https://github.com/semi-technologies/weaviate | Vector database for semantic, keyword (BM25), and hybrid search over notes |
| 7 | FAISS | 1149 | library, disk | vector | ? | ? | ? | s6/faiss.json | Opus | https://github.com/facebookresearch/faiss | Library for similarity search and clustering of dense vectors (C++ with Python wrappers),… |
| 8 | Milvus | 929 | network_service | vector, bm25, hybrid | ? | ? | ? | s6/milvus.json | Sonnet | https://github.com/milvus-io/milvus | Distributed vector database with BM25 full-text and hybrid search |
| 9 | Chroma | 755 | library, network_service, disk | vector, embeddings | ? | ? | ? | s6/chroma.json | Sonnet | https://github.com/chroma-core/chroma | Open-source vector database: stores documents and embeddings, queries by similarity with … |
| 10 | Apache Lucene | 663 | library | full_text | ? | ? | ? | s6/apache-lucene.json | Sonnet | https://github.com/apache/lucene | Java full-text engine library to build the hub's keyword index over Markdown notes. |
| 11 | LanceDB | 620 | disk, library | vector, full_text | ? | ? | ? | s3/lancedb.json | Sonnet | https://github.com/lancedb/lancedb | Embedded vector and full-text database for local hybrid search over notes |
| 12 | Solr | 523 | disk, network_service | full_text, vector | ? | ? | ? | s6/apache-solr.json | Sonnet | https://github.com/apache/solr | Standalone search server (full-text and vector) on Lucene that could index the hub's Mark… |
| 13 | OpenSearch | 429 | network_service | full_text, vector | ? | ? | ? | s3/opensearch.json | Opus | https://github.com/opensearch-project/opensearch | Motor de busca e busca vetorial self-hosted para o indice do hub |
| 14 | SQLite-vec | 403 | library, disk | vector | não | sim | ? | s3/sqlite-fts5-sqlite-vec.json | Sonnet | https://github.com/asg017/sqlite-vec | SQLite extension for vector search (vec0 virtual tables, KNN over float/int8/binary vecto… |
| 15 | Annoy | 389 | library, disk | vector | ? | sim | ? | s6/annoy.json | Sonnet | https://github.com/spotify/annoy | Biblioteca C++/Python de busca aproximada de vizinhos mais próximos com índices em arquiv… |
| 16 | sentence-transformers | 378 | library | vector, embeddings, reranker | ? | ? | sim | s6/sentence-transformers.json | Sonnet | https://github.com/ukplab/sentence-transformers | Compute multilingual embeddings and rerank passages for semantic search. |
| 17 | Haystack | 301 | library, network_service | vector | sim | ? | ? | s6/haystack.json | Sonnet | https://github.com/deepset-ai/haystack | Python framework for RAG and semantic search pipelines; Hayhooks can expose pipelines as … |
| 18 | lunr.js | 260 | library | full_text | ? | ? | ? | s6/lunr-js.json | Sonnet | https://github.com/olivernn/lunr.js | Small client-side full-text search library indexing JSON documents, with scoring, fuzzy a… |
| 19 | Xapian | 244 | n/a | n/a | ? | ? | ? | s6/xapian.json | Sonnet | https://github.com/xapian/xapian | Xapian: projeto de busca/indexação com módulos; README só aponta guias, não descreve funç… |
| 20 | pgvector | 210 | inside_db_mcp | vector | ? | sim | ? | s6/pgvector.json | Sonnet | https://github.com/pgvector/pgvector | Vector similarity search extension for PostgreSQL (exact and approximate HNSW/IVFFlat). |
| 21 | HNSWlib | 185 | library, disk | vector | ? | sim | ? | s6/hnswlib.json | Sonnet | https://github.com/nmslib/hnswlib | Approximate nearest-neighbor vector index for hybrid or semantic retrieval over embedding… |
| 22 | LlamaIndex | 139 | library, disk | vector, embeddings, reranker | ? | ? | ? | s6/llamaindex.json | Sonnet | https://github.com/jerryjliu/llama_index | Indexa Markdown e recupera passagens com embeddings e reranking como biblioteca Python |
| 23 | Lucene.NET | 135 | library | full_text | ? | sim | ? | s6/lucene.net.json | Sonnet | https://github.com/apache/lucenenet | .NET full-text search library to build the hub's keyword index if the hub runs on .NET. |
| 24 | Snowball | 135 | library | other | ? | sim | ? | s6/snowball.json | Opus | https://github.com/snowballstem/snowball | Stemmer para normalizar termos em recuperação de informação (compilador Snowball e algori… |
| 25 | Pyserini | 111 | library, network_service | bm25, vector, hybrid, embeddings | sim | ? | ? | s6/pyserini.json | Opus | https://github.com/castorini/pyserini | Python toolkit for BM25 (Lucene/Anserini), learned sparse and dense (Faiss) retrieval, wi… |
| 26 | Bleve | 92 | disk, library | bm25, full_text, vector, hybrid | ? | ? | sim | s6/bleve.json | Sonnet | https://github.com/blevesearch/bleve | Go indexing and search library with BM25/tf-idf, full-text, vector and hybrid (RRF/RSF) s… |
| 27 | FlexSearch | 91 | library, disk | full_text | não | ? | ? | — | Sonnet | https://github.com/nextapps-de/flexsearch | Biblioteca de busca full-text para navegador e Node.js, com índices persistentes (SQLite,… |
| 28 | Gensim | 87 | library | vector | ? | ? | ? | — | Sonnet | https://github.com/rare-technologies/gensim | Biblioteca Python para indexação de documentos e recuperação por similaridade (LSA, LDA, … |
| 29 | Algolia | 85 | network_service | other | ? | ? | ? | — | Sonnet | https://algolia.com/pt-br | Hosted commercial AI search and retrieval platform (SaaS) |
| 30 | FastEmbed | 80 | library | embeddings, vector, reranker | ? | ? | sim | s3/fastembed.json | Sonnet | https://github.com/qdrant/fastembed | Biblioteca Python leve (ONNX, sem GPU) para gerar embeddings densos, esparsos, ColBERT e … |
| 31 | Manticore Search | 59 | network_service, disk | bm25, full_text, vector, hybrid | ? | ? | ? | s3/manticore-search.json | Sonnet | https://github.com/manticoresoftware/manticoresearch | Motor full-text com BM25 e busca hibrida sobre as notas em Markdown |
| 32 | MiniSearch | 57 | library | full_text, fuzzy | não | ? | ? | — | Sonnet | https://github.com/lucaong/minisearch | Motor de busca full-text em memoria (JS) para indexar notas Markdown do hub, com prefixo,… |
| 33 | RediSearch | 54 | network_service | full_text, bm25, vector | ? | ? | ? | — | Sonnet | https://github.com/redisearch/redisearch | Redis module (now built into Redis 8) providing full-text, BM25-ranked and vector search … |
| 34 | Sonic | 52 | network_service | full_text | não | ? | ? | — | Sonnet | https://github.com/valeriansaliou/sonic | Lightweight identifier-index search backend (Sonic Channel TCP protocol), returns IDs for… |
| 35 | Redis | 52 | network_service | vector | ? | ? | ? | — | Sonnet | https://redis.io | Network Redis service with vector search as context retriever for agents |
| 36 | Ripgrep | 48 | disk | grep | ? | sim | ? | s6/ripgrep.json | Sonnet | https://github.com/burntsushi/ripgrep | Fast line-oriented recursive regex search over files on disk, respecting ignore rules. |
| 37 | BGE-M3 / multilingual-e5 | 47 | library | vector, embeddings, reranker | ? | ? | sim | — | Sonnet | https://github.com/flagopen/flagembedding | Multilingual embedding models (BGE-M3: dense, lexical, multi-vector) and rerankers for se… |
| 38 | Fuse.js | 44 | library | bm25, other | ? | ? | ? | — | Sonnet | https://github.com/krisk/fuse | Client-side keyword and fuzzy search library with BM25-style token ranking |
| 39 | Elasticlunr | 43 | library, light_client | full_text | ? | ? | ? | s6/elasticlunr-js.json | Sonnet | https://github.com/weixsong/elasticlunr.js | Client-side full-text index for Markdown notes, offline in the browser or Node. |
| 40 | Quickwit | 38 | network_service | full_text | ? | ? | ? | — | Sonnet | https://github.com/quickwit-oss/quickwit | Motor de busca full-text distribuido sobre armazenamento em nuvem, voltado a logs e trace… |
| 41 | Anserini | 37 | library | other | ? | ? | ? | — | Sonnet | https://github.com/castorini/anserini | Lucene-based Java toolkit for reproducible information retrieval research, with prebuilt … |
| 42 | sentence-transformers/paraphrase-multilingual-Min… | 35 | library | embeddings, vector | ? | ? | sim | — | Opus | https://huggingface.co/sentence-transformers/paraphrase-mul… | Multilingual sentence-embedding model (paraphrase-MiniLM-L12-v2 distilled to 50+ language… |
| 43 | Django Haystack | 35 | library | other | não | ? | ? | — | Sonnet | https://github.com/django-haystack/django-haystack | Modular search abstraction for Django plugging Solr, Elasticsearch, Whoosh or Xapian |
| 44 | pagefind | 30 | library | full_text | ? | ? | ? | s3/pagefind.json | Sonnet | https://github.com/cloudcannon/pagefind | Static full-text search library for sites, no hosting infrastructure needed |
| 45 | RankBM25 | 29 | library | bm25 | não | ? | ? | — | Sonnet | https://pypi.org/project/rank-bm25 | BM25 keyword ranking library (Okapi, BM25L, BM25+, BM25-Adpt, BM25T) for the search layer. |
| 46 | CouchDB-Lucene | 28 | network_service | full_text | não | ? | sim | — | Sonnet | https://github.com/rnewson/couchdb-lucene | Servidor JVM standalone que indexa documentos do CouchDB com Lucene e responde buscas ful… |
| 47 | ZincSearch | 27 | network_service | full_text | ? | ? | ? | — | Opus | https://github.com/zincsearch/zincsearch | Single-binary full-text search engine with Elasticsearch-compatible API and web UI |
| 48 | MiniLM | 23 | library | embeddings | não | ? | ? | — | Sonnet | https://github.com/microsoft/unilm | Umbrella research repo; contains E5 text-embedding models usable for semantic retrieval. |
| 49 | Cohere | 23 | network_service | embeddings, reranker | ? | ? | ? | — | Sonnet | https://cohere.com | Hosted embedding and rerank models for semantic retrieval; private on-prem or VPC deploym… |
| 50 | NMSLIB | 18 | library, network_service | vector | ? | sim | ? | — | Sonnet | https://github.com/nmslib/nmslib | Efficient similarity search library and toolkit for generic and non-metric spaces, with P… |
| 51 | Jina AI | 18 | network_service | embeddings, reranker | sim | ? | ? | — | Sonnet | https://jina.ai | Hosted search foundation: reader, embeddings and reranker APIs, with an MCP server (mcp.j… |
| 52 | Recoll | 17 | disk | full_text | ? | sim | ? | — | Sonnet | https://recoll.org | Desktop full-text search over many document formats, indexed on disk with Xapian |
| 53 | Dense Passage Retriever (DPR) | 17 | library | vector, embeddings | ? | ? | ? | — | Sonnet | https://github.com/facebookresearch/dpr | Dense passage retriever (bi-encoder) training and inference toolkit for open-domain Q&A, … |
| 54 | OpenAI Embedding API | 17 | network_service | embeddings, vector | ? | ? | ? | — | Sonnet | https://platform.openai.com/docs/guides/embeddings | Hosted OpenAI API producing vector embeddings of text for semantic search |
| 55 | Lance (formato de dados do LanceDB) | 16 | library, disk | vector, bm25, hybrid | ? | ? | ? | — | Sonnet | https://github.com/lancedb/lance | Columnar file format providing vector and full-text indexes for local or lakehouse search |
| 56 | ColBERTv2 | 16 | disk, library, network_service | vector, embeddings | ? | ? | ? | — | Sonnet | https://github.com/stanford-futuredata/colbert | Late-interaction BERT retriever with PLAID index and lightweight search server |
| 57 | AnythingLLM | 16 | disk, network_service | other | ? | sim | ? | — | Opus | https://github.com/mintplex-labs/anything-llm | Local RAG over documents as a knowledge base for agents |
| 58 | txtai | 16 | library, network_service | vector, hybrid, graph, embeddings | sim | ? | ? | s3/txtai.json | Sonnet | https://github.com/neuml/txtai | Framework de busca semântica com banco de embeddings (vetorial esparso/denso, grafo, SQL)… |
| 59 | searchd daemon | 16 | network_service, disk | full_text | não | sim | ? | — | Sonnet | https://sphinxsearch.com/docs/current.html | Full-text search server (searchd) with SQL-like queries and real-time indexes |
| 60 | transformers.js | 15 | library | embeddings | ? | ? | ? | — | Sonnet | https://github.com/xenova/transformers.js | Gera embeddings locais em JavaScript para busca semântica nas notas. |
| 61 | Elasticsearch KNN Plugin | 15 | network_service | vector | ? | ? | ? | — | Sonnet | https://github.com/opensearch-project/k-nn | OpenSearch plugin for approximate nearest neighbor (vector) search with filters and aggre… |
| 62 | PyTerrier | 15 | library | bm25, vector, hybrid, reranker, embeddings | ? | sim | ? | — | Sonnet | https://github.com/terrier-org/pyterrier | Biblioteca Python para montar pipelines de indexação e recuperação (esparsa, esparsa apre… |
| 63 | Ollama + Zilliz (PostgreSQL-compatible VectorDB) | 15 | network_service | vector, full_text, hybrid, reranker | ? | ? | ? | — | Opus | https://zilliz.com | Managed cloud vector database (Milvus-based) with hybrid vector, full-text and JSON searc… |
| 64 | NLTK Portuguese Stemmer | 14 | library | other | não | ? | sim | — | Sonnet | https://nltk.org/api/nltk.stem.snowball.html | Stemmer Snowball em Python (inclui portugues) para normalizar termos na busca lexical. |
| 65 | Tantivy | 14 | library | unknown | ? | ? | ? | s3/tantivy-tantivy-py.json, s3/tantivy.json | Sonnet | https://github.com/tantivy-search | Organization page of Tantivy (Rust full-text search library); holds website and helper re… |
| 66 | BM25S | 13 | library, disk | bm25 | ? | ? | ? | — | Sonnet | https://github.com/xhluca/bm25s | Ranking BM25 com índice salvo em disco para busca por palavras-chave. |
| 67 | Tynesense | 13 | network_service | full_text, vector, hybrid | ? | ? | ? | — | Opus | https://typesense.io | Open-source search engine (typo tolerance, filtering, vector/semantic search) served over… |
| 68 | LASER | 12 | library, disk | embeddings | não | ? | sim | — | Sonnet | https://github.com/facebookresearch/laser | Embeddings multilingues de sentencas (pip install laser_encoders), incluindo portugues, p… |
| 69 | SQLite with SQLite-VSS | 12 | library, disk | vector | não | não | ? | — | Sonnet | https://github.com/asg017/sqlite-vss | SQLite extension for vector similarity search based on Faiss (superseded by sqlite-vec) |
| 70 | PyStemmer (Snowball) | 12 | library | other | ? | ? | ? | — | Sonnet | https://github.com/snowballstem/pystemmer | Stemming (Snowball) para ampliar o recall de busca textual |
| 71 | Portuguese Analyzer (Lucene) | 12 | library | full_text | ? | ? | sim | — | Opus | https://lucene.apache.org/core/8_11_0/analyzers-common/org/… | Portuguese analyzer (stop words, stemming) for Lucene indexing and querying |
| 72 | Campo tipo dense_vector | 11 | network_service | vector | ? | ? | ? | — | Sonnet | https://elastic.co/guide/en/elasticsearch/reference/current… | Dense vector field for kNN embedding search inside the search engine |
| 73 | Sentence-BERT multilingual | 11 | disk, library | vector, embeddings | ? | ? | sim | — | Sonnet | https://sbert.net/docs/pretrained_models.html | Multilingual embedding models for Portuguese and English semantic search. |
| 74 | E5 multilingual | 10 | library | embeddings, vector | ? | ? | sim | — | Sonnet | https://huggingface.co/intfloat/multilingual-e5-large | Multilingual dense text embeddings (100 languages) for semantic search; needs query:/pass… |
| 75 | PyLucene | 10 | library | full_text | ? | sim | ? | — | Sonnet | https://lucene.apache.org/pylucene | Python wrapper around Java Lucene for text indexing and search |
| 76 | Instructor | 9 | library | embeddings, vector | não | ? | ? | — | Sonnet | https://github.com/hkunlp/instructor-embedding | Instruction-finetuned text embedding model (Python) to embed notes and queries for semant… |
| 77 | Terrier | 9 | library, network_service | bm25, full_text | não | ? | ? | — | Sonnet | https://terrier.org | Java open source search engine and IR research platform with indexing and BM25F/DFR retri… |
| 78 | Elasticsearch ICU Analysis plugin | 8 | library | full_text | ? | ? | ? | — | Sonnet | https://github.com/elastic/elasticsearch-analysis-icu | ICU analysis plugin for Elasticsearch (Unicode text analysis); repo moved into the main E… |
| 79 | OramaDB | 8 | library | bm25, full_text, vector, hybrid, embeddings | ? | ? | ? | s3/orama.json | Sonnet | https://github.com/oramasearch/orama | JavaScript search engine with full-text (BM25), vector and hybrid search, embeddable as a… |
| 80 | Elastic Stack | 8 | network_service | full_text, other | ? | ? | ? | — | Opus | https://elastic.co/stack | Elastic Stack (Elasticsearch, Kibana, Beats, Logstash): ingest, search, analyze and visua… |
| 81 | Obsidian Local REST API | 7 | network_service | full_text | sim | sim | ? | s3/obsidian-local-rest-api-mcp.json | Sonnet | https://github.com/coddingtonbear/obsidian-local-rest-api | Obsidian plugin exposing the vault to agents via REST API and built-in MCP server, with f… |
| 82 | RAGflow | 7 | network_service | hybrid, reranker, embeddings | ? | sim | ? | — | Sonnet | https://github.com/infiniflow/ragflow | Hybrid RAG engine with reranking for hub document retrieval; heavy, Docker-based |
| 83 | lunr-languages | 7 | library | full_text | ? | ? | sim | — | Sonnet | https://github.com/mihaivalentin/lunr-languages | Multilingual stemming/tokenization extension for Lunr.js keyword search (browser/Node) |
| 84 | RapidFuzz | 7 | library | other | não | sim | ? | — | Sonnet | https://github.com/rapidfuzz/rapidfuzz | Biblioteca Python/C++ de similaridade de strings (fuzzy matching, Levenshtein), usavel em… |
| 85 | TinySearch (Rust) | 7 | library | full_text | não | ? | ? | — | Opus | https://github.com/tinysearch/tinysearch | WASM full-text search index for static websites, built from a JSON file |
| 86 | Obsidian + Smart Connections | 6 | disk | vector, embeddings | ? | ? | ? | — | Sonnet | https://github.com/brianpetro/obsidian-smart-connections | Obsidian plugin for semantic note search and related-note discovery using local embedding… |
| 87 | Stork | 6 | disk, library | full_text | não | ? | ? | — | Sonnet | https://github.com/jameslittle230/stork | Static-site full-text index builder (Rust CLI plus WASM JS front end); marginal for agent… |
| 88 | BAAI/bge-small-en-v1.5 | 6 | library | embeddings, vector | ? | ? | não | — | Sonnet | https://huggingface.co/baai/bge-small-en-v1.5 | Dense embedding model for English passage retrieval (small). |
| 89 | pysolr | 5 | library | other | não | ? | ? | — | Sonnet | https://github.com/django-haystack/pysolr | Python client to index and query an Apache Solr server |
| 90 | rust-bert | 5 | library | embeddings, vector | ? | sim | ? | — | Sonnet | https://github.com/guillaume-be/rust-bert | Gerar embeddings de sentencas localmente em Rust (libtorch ou ONNX) para busca semantica … |
| 91 | TNTSearch | 5 | library, disk | bm25, full_text | ? | ? | sim | — | Sonnet | https://github.com/teamtnt/tntsearch | Pure-PHP full-text search engine with BM25 ranking, fuzzy and boolean search, indexes sto… |
| 92 | multilingual-e5-base | 5 | library | embeddings, vector | não | ? | sim | — | Sonnet | https://huggingface.co/intfloat/multilingual-e5-base | Embeddings multilíngues (inclui português) para recuperação de passagens |
| 93 | tsearch2 / Unaccent | 5 | library | full_text | não | ? | sim | — | Sonnet | https://postgresql.org/docs/current/unaccent.html | PostgreSQL text search dictionary that strips diacritics for accent-insensitive full-text… |
| 94 | SPLADE | 5 | library | other, embeddings | não | ? | ? | — | Sonnet | https://github.com/naver/splade | Modelo neural de recuperação esparsa (expansão lexical via BERT MLM) com treino, indexaçã… |
| 95 | Search-index | 4 | library | full_text | ? | ? | ? | — | Sonnet | https://github.com/fergiemcdowall/search-index | Biblioteca de busca de texto completo persistente para navegador e Node.js, com PUT e QUE… |
| 96 | Groonga | 4 | disk, network_service, library | full_text | ? | ? | ? | — | Sonnet | https://groonga.org | Motor de busca full-text e column store para indexar e consultar Markdown. |
| 97 | E5-small-v2 | 4 | library | vector, embeddings | não | ? | não | — | Sonnet | https://huggingface.co/intfloat/e5-small-v2 | Embeddings densos para busca semântica, apenas em inglês |
| 98 | text-embeddings-inference | 4 | network_service | vector, reranker, embeddings | ? | ? | sim | — | Sonnet | https://github.com/huggingface/text-embeddings-inference | Server for text embedding, re-ranker and sequence classification models; HTTP/gRPC embedd… |
| 99 | SolrNet | 4 | library | full_text, other | não | ? | ? | — | Sonnet | https://github.com/mausch/solrnet | .NET client library for an Apache Solr / SolrCloud server (querying, faceting, highlighti… |
| 100 | pg_bm25 (ParadeDB) | 4 | network_service | bm25, full_text, vector, hybrid | sim | ? | ? | — | Sonnet | https://github.com/paradedb/paradedb | Postgres extension providing BM25 full-text, vector and hybrid search with an MCP integra… |
| 101 | Elastic Cloud | 4 | network_service | full_text, vector | ? | ? | ? | — | Opus | https://elastic.co/cloud/elasticsearch-service | Hosted Elasticsearch service (paid cloud) usable as a remote search backend |
| 102 | Elastic Enterprise Search | 4 | network_service | full_text, vector, hybrid | sim | ? | ? | — | Sonnet | https://elastic.co/enterprise-search | Elasticsearch: hybrid lexical and vector search platform with Agent Builder exposing MCP |
| 103 | Analysis ICU plugin | 4 | library | full_text | ? | ? | ? | — | Sonnet | https://elastic.co/guide/en/elasticsearch/reference/current… | Elasticsearch plugin adding Unicode normalization, case folding, collation and transliter… |
| 104 | Contriever | 4 | library, disk | vector, embeddings | ? | ? | ? | — | Sonnet | https://github.com/facebookresearch/contriever | Pre-trained dense retriever models (Contriever, multilingual mContriever) plus training a… |
| 105 | Jina Embeddings | 4 | network_service, disk | embeddings, vector | ? | ? | sim | — | Opus | https://jina.ai/embeddings | Multilingual embedding models via hosted API, cloud marketplaces or open-weight local dep… |
| 106 | pgvector-python | 3 | library | vector | ? | ? | ? | — | Opus | https://github.com/pgvector/pgvector-python | Python client library for pgvector (Django, SQLAlchemy, Psycopg, asyncpg), with hybrid se… |
| 107 | USearch | 3 | library, disk | vector | ? | sim | ? | — | Sonnet | https://github.com/unum-cloud/usearch | Single-file HNSW vector index library for similarity search, servable from disk via memor… |
| 108 | NLTK Portuguese Stemmers | 3 | library | other | ? | ? | sim | — | Sonnet | https://nltk.org/api/nltk.stem.html | Pacote de stemmers do NLTK (RSLP e Snowball em portugues) para busca lexical. |
| 109 | NLTK SnowballStemmer (módulo) | 3 | library | other | não | ? | sim | — | Sonnet | https://nltk.org/_modules/nltk/stem/snowball.html | Stemmer Snowball em Python (inclui portugues) para normalizar termos na busca lexical. |
| 110 | snowballstemmer | 3 | library | full_text | ? | sim | sim | — | Sonnet | https://pypi.org/project/snowballstemmer | Portuguese stemmer for keyword search normalization of pt-BR text. |
| 111 | Vectara | 3 | network_service | hybrid, reranker | sim | ? | ? | — | Sonnet | https://vectara.com | Managed enterprise RAG platform with hybrid retrieval, reranking and MCP tools over inges… |
| 112 | Voyage AI | 3 | network_service | embeddings, reranker | ? | ? | ? | — | Sonnet | https://voyageai.com | API hospedada de embeddings e rerankers para busca semantica sobre Markdown |
| 113 | Vald | 3 | network_service | vector | ? | ? | ? | — | Sonnet | https://github.com/vdaas/vald | Distributed approximate nearest neighbor dense vector search engine, run on Kubernetes. |
| 114 | GTE-multilingual-small | 3 | library, network_service | embeddings, vector, hybrid | ? | ? | ? | — | Sonnet | https://huggingface.co/alibaba-nlp/gte-multilingual-base | Multilingual (70+ languages) dense and sparse embedding model, 8192 tokens, for retrieval… |
| 115 | mixedbread-ai/mxbai-embed-large-v1 | 3 | library | embeddings, vector | ? | ? | ? | — | Sonnet | https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1 | English sentence embedding model with Matryoshka and binary quantization for retrieval |
| 116 | Khoj | 2 | network_service | other | ? | ? | ? | — | Sonnet | https://github.com/khoj-ai/khoj | Self-hostable personal AI app with semantic search over markdown, pdf, org-mode and other… |
| 117 | pg_bigm | 2 | inside_db_mcp | full_text | ? | ? | ? | s6/pg-bigm.json | Opus | https://github.com/pgbigm/pg_bigm | Bigram (2-gram) index for full text search in PostgreSQL; requires a PostgreSQL server. |
| 118 | Vespa BM25 | 2 | network_service | bm25, vector, hybrid, reranker | ? | ? | ? | — | Sonnet | https://docs.vespa.ai/en/ranking.html | Rank profiles and phased ranking (BM25, vector closeness, ONNX/XGBoost/LightGBM rerankers… |
| 119 | Fdrant | 2 | network_service | vector, hybrid | ? | ? | ? | — | Sonnet | https://drant.dev | Vector and hybrid (dense+sparse, BM25) search engine as a network service for hub notes |
| 120 | Elastic App Search | 2 | network_service | full_text, vector, hybrid, reranker, embeddings | ? | ? | ? | — | Sonnet | https://elastic.co/app-search | Elasticsearch search toolkit page: lexical, vector, hybrid (RRF) and semantic search, ret… |
| 121 | ELK Stack | 2 | network_service | other | ? | ? | ? | — | Sonnet | https://elastic.co/elastic-stack | Elastic Stack (Elasticsearch, Kibana, Beats, Logstash): search and analytics engine plus … |
| 122 | Fess | 2 | network_service | full_text | não | sim | ? | — | Sonnet | https://fess.codelibs.org | Self-hosted full-text search server (crawler, indexer, UI) on OpenSearch |
| 123 | Openensearch | 2 | network_service | vector | ? | ? | ? | — | Sonnet | https://opensearch.project.org | Open-source search and analytics engine (OpenSearch) usable as a network search service, … |
| 124 | pgroonga / PostgreSQL PGroonga | 2 | library | full_text | ? | sim | sim | — | Sonnet | https://pgroonga.github.io | Full-text search extension for PostgreSQL with multilingual tokenization |
| 125 | Sourcegraph | 2 | network_service | full_text | sim | ? | ? | — | Sonnet | https://sourcegraph.com | Exact keyword code search over many repositories, with an MCP server giving agents codeba… |
| 126 | Infinity | 2 | network_service, library | embeddings, reranker, vector | ? | ? | ? | — | Sonnet | https://github.com/michaelfeil/infinity | REST API serving text embeddings and reranking models from HuggingFace |
| 127 | Búsqueda k‑NN aproximada | 2 | network_service | vector, embeddings, hybrid | ? | ? | ? | — | Sonnet | https://elastic.co/guide/en/elasticsearch/reference/current… | Vector kNN search over dense_vector fields for semantic retrieval, approximate or exact |
| 128 | BGE Reranker / Cohere Rerank | 2 | library | reranker | ? | ? | não | — | Sonnet | https://huggingface.co/baai/bge-reranker-base | Cross-encoder reranker for re-ranking top-k retrieved passages (Chinese/English). |
| 129 | rank_bm25 | 2 | library | bm25 | não | ? | ? | — | Sonnet | https://pypi.org/project/rank_bm25 | BM25 keyword ranking library (Okapi, BM25L, BM25+, BM25-Adpt, BM25T) for the search layer. |
| 130 | RavenDB | 2 | network_service | full_text, vector | ? | ? | ? | — | Sonnet | https://ravendb.net | NoSQL document database with built-in full-text and vector search |
| 131 | RAGatouille | 1 | disk, library | vector, embeddings | não | não | ? | — | Sonnet | https://github.com/bclavie/ragatouille | Python library to train, index and query ColBERT late-interaction retrieval, persisting c… |
| 132 | PrivateGPT | 1 | network_service | embeddings | ? | sim | ? | — | Sonnet | https://github.com/imartinez/privategpt | Open-source local API layer with file ingestion, retrieval with citations, embeddings and… |
| 133 | Jina AI Document Store | 1 | library | vector | ? | ? | ? | — | Sonnet | https://github.com/jina-ai/docarray | Python library with typed multimodal document data structures and vector DB connectors (W… |
| 134 | SPTAG | 1 | library | vector | não | sim | ? | — | Sonnet | https://github.com/microsoft/sptag | ANN vector index library (C++/Python wrapper) for nearest-neighbor search over embeddings. |
| 135 | The Platinum Searcher (pt) | 1 | disk | grep | ? | sim | ? | s6/the-platinum-searcher.json | Sonnet | https://github.com/monochromegane/the_platinum_searcher | Fast grep-style file search from the CLI; could scan Markdown notes. |
| 136 | Elasticsearch Learning to Rank plugin | 1 | network_service | reranker | ? | ? | ? | — | Sonnet | https://github.com/o19s/elasticsearch-learning-to-rank | Plugin do Elasticsearch que reranqueia resultados com modelos treinados; exige cluster El… |
| 137 | ripgrep-all | 1 | disk | grep | ? | sim | ? | s6/ripgrep-all.json | Sonnet | https://github.com/phiresky/ripgrep-all | Busca regex com grep também dentro de PDFs, DOCX e anexos. |
| 138 | rum | 1 | network_service | full_text | ? | ? | ? | — | Sonnet | https://github.com/postgrespro/rum | Full-text index with ranking and phrase search, but only inside PostgreSQL. |
| 139 | NVIDIA RAPIDS cuVS | 1 | library | vector | ? | ? | ? | — | Sonnet | https://github.com/rapidsai/cuvs | Motor ANN em GPU para busca vetorial sobre embeddings das notas |
| 140 | Zoekt | 1 | disk, network_service | grep, bm25 | ? | ? | ? | s6/zoekt.json | Opus | https://github.com/sourcegraph/zoekt | Busca por substring e regex com índice de trigramas, voltada a código; API JSON/gRPC |
| 141 | Zinc | 1 | network_service, disk | full_text | não | sim | ? | — | Sonnet | https://github.com/zinclabs/zinc | Motor de busca de texto completo, leve, com API compatível com Elasticsearch, índice em d… |
| 142 | SnowballC R package | 1 | library | other | ? | sim | sim | — | Sonnet | https://cran.r-project.org/web/packages/snowballc/index.html | Portuguese stemmer for normalizing tokens in keyword search indexes. |
| 143 | DanswerM | 1 | network_service | other | sim | ? | ? | — | Sonnet | https://danswer.ai | Self-hosted enterprise search and AI assistant over connected sources, with an MCP server… |
| 144 | Vespa Portuguese Stemmer | 1 | network_service | full_text | ? | ? | ? | — | Sonnet | https://docs.vespa.ai/en/linguistics.html | Tokenize, normalize and stem text in documents and queries (OpenNLP or Lucene linguistics… |
| 145 | Vespa Tensor Import | 1 | network_service | vector, embeddings | ? | ? | ? | — | Sonnet | https://docs.vespa.ai/en/tensor-user-guide.html | Vespa engine: tensor fields with HNSW nearest-neighbor search and ranking |
| 146 | Pipeline | 1 | library | other | ? | ? | ? | — | Sonnet | https://haystack.deepset.ai/docs/latest/pipelines | Orchestrate search/RAG pipelines (retrievers, indexing, LLM components) as directed multi… |
| 147 | Snowflake/snowflake-arctic-embed-l-v2.0 | 1 | disk, library | embeddings, vector | ? | ? | sim | — | Sonnet | https://huggingface.co/snowflake/snowflake-arctic-embed-l-v… | Multilingual embedding model for semantic search and retrieval over hub notes |
| 148 | Snowflake/snowflake-arctic-embed-m-v2.0 | 1 | disk, library | embeddings, vector | ? | ? | sim | — | Sonnet | https://huggingface.co/snowflake/snowflake-arctic-embed-m-v… | Multilingual embedding model for semantic search and retrieval over hub notes |
| 149 | Microsoft Cognitive Search | 1 | network_service | full_text, vector, hybrid | ? | ? | ? | — | Sonnet | https://learn.microsoft.com/en-us/azure/search | Managed cloud search service with full-text, vector, hybrid and multimodal retrieval, plu… |
| 150 | Porter Stemmer (Portuguese) | 1 | library | other | não | ? | não | — | Sonnet | https://tartarus.org/~martin/porterstemmer | Term normalisation (stemming) for keyword indexing; English only, not pt-BR. |
| 151 | Omega | 1 | network_service | full_text | ? | ? | ? | — | Sonnet | https://xapian.org/docs/omega | Omega: Xapian-based website search application (indexer scriptindex, CGI front end); woul… |
| 152 | Danswer | 1 | network_service | hybrid, vector, embeddings | sim | ? | ? | — | Sonnet | https://github.com/danswer-ai/danswer | Onyx (ex-Danswer): self-hosted context layer that indexes 50+ apps with hybrid vector+key… |
| 153 | The Silver Searcher | 1 | disk | grep | ? | sim | ? | s6/the-silver-searcher.json | Sonnet | https://github.com/ggreer/the_silver_searcher | Fast code/text search command-line tool (ack-like grep) that respects .gitignore |
| 154 | GPT-Index | 1 | library, disk | vector, embeddings, reranker | ? | ? | ? | — | Sonnet | https://github.com/jerryjliu/gpt_index | Python framework for indexing documents and retrieval/query with embeddings and vector st… |
| 155 | Ucto Portuguese Stemmer | 1 | disk, library | other | ? | ? | sim | — | Sonnet | https://github.com/languagemachines/ucto | Rule-based tokeniser with Portuguese and English rules; preprocessing for indexing |
| 156 | Solr Node.js | 1 | library | full_text | não | ? | ? | — | Sonnet | https://github.com/lbdremy/solr-node-client | Node.js client library to index and query an Apache Solr server |
| 157 | RankGPT | 1 | library | reranker | ? | ? | ? | — | Sonnet | https://github.com/sunnweiwei/rankgpt | LLM-based re-ranking of retrieved passages (permutation generation, sliding window). |
| 158 | AWS Elasticsearch Service | 1 | network_service | bm25, vector, hybrid, embeddings | sim | ? | ? | — | Sonnet | https://aws.amazon.com/elasticsearch-service | Managed retrieval engine for vector, lexical, and hybrid search |
| 159 | InMemoryBM25Retriever | 1 | library | bm25 | ? | ? | ? | — | Sonnet | https://docs.haystack.deepset.ai/docs/inmemorybm25retriever | Keyword retriever using BM25 over an in-memory document store (Haystack component) |
| 160 | Vespa Embedder | 1 | network_service | vector, embeddings | ? | ? | ? | — | Sonnet | https://docs.vespa.ai/en/embedding.html | Geração de embeddings dentro do Vespa (embedders configuráveis) para busca vetorial. |
| 161 | Vespa Benchmarking | 1 | network_service | other | ? | ? | ? | — | Sonnet | https://docs.vespa.ai/en/performance.html | Vespa performance, sizing and benchmarking guide for the Vespa search engine |
| 162 | Vespa Searcher | 1 | network_service | other | ? | ? | ? | — | Sonnet | https://docs.vespa.ai/en/searcher-development.html | Java Searcher components that process queries and results in the Vespa container |
| 163 | ELSER v2 | 1 | network_service | vector, embeddings | ? | ? | não | — | Sonnet | https://elastic.co/guide/en/machine-learning/current/ml-nlp… | Learned sparse retrieval model in Elasticsearch for semantic search, English only |
| 164 | Elastic Workplace Search | 1 | network_service | vector, hybrid | ? | ? | ? | — | Sonnet | https://elastic.co/workplace-search | Enterprise workplace search over SaaS sources via connectors, built on Elasticsearch |
| 165 | BAAI/bge-base-en-v1.5 | 1 | library | embeddings, vector | ? | ? | não | — | Sonnet | https://huggingface.co/baai/bge-base-en-v1.5 | Dense embedding model for English passage retrieval (base). |
| 166 | Vespa Docker | 1 | network_service | other | ? | ? | ? | — | Sonnet | https://hub.docker.com/r/vespaengine/vespa | Open big data serving engine for search, recommendation and ML inference, run as a Docker… |
| 167 | Portuguese Light Stemmer | 1 | library | full_text | não | ? | sim | — | Sonnet | https://lucene.apache.org/core/8_11_0/analyzers-common/org/… | Lucene Portuguese light stemmer token filter for Portuguese full-text search. |
| 168 | MG4J | 1 | library | bm25, full_text | ? | ? | ? | — | Sonnet | https://mg4j.di.unimi.it | Full-text search engine for indexing and querying large document collections (Java librar… |
| 169 | sqlite-utils | 1 | disk, library | full_text | ? | ? | ? | — | Sonnet | https://sqlite-utils.datasette.io | Python library and CLI to build SQLite databases and enable full-text search (FTS) over t… |

## 2. Stack (184 entidades), por área do hub

Área e encaixe pelo FreeLLMAPI (2 modelos de famílias diferentes; um 3º desempata). *Encaixe*: central, opcional ou improvável para este hub. "Divergente" = os 3 modelos discordaram.

### Sync e CouchDB (18)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| pouchdb | 53 | central | Provides offline database synchronization with CouchDB across multiple machines via Pouch… | s6/pouchdb.json | Sonnet | https://github.com/pouchdb/pouchdb |
| CouchDB | 33 | central | Master-master replication backend for notes | — | Opus | https://github.com/apache/couchdb |
| CouchDB Change Feed | 30 | central | master-master replication for notes | — | Sonnet | https://docs.couchdb.org |
| CouchDB Mango | 26 | central | Filter Markdown notes by YAML frontmatter fields via CouchDB Mango queries | — | Sonnet | https://github.com/apache/couchdb-mango |
| CouchDB Sync | 7 | central | Syncs CouchDB databases between machines with conflict resolution and replication protoco… | — | Sonnet | https://docs.couchdb.org/en/stable/sync.html |
| CouchDB MapReduce Views | 5 | central | Enables efficient indexing and querying of YAML frontmatter/document keys in CouchDB for … | — | Sonnet | https://docs.couchdb.org/en/stable/api/database/views.html |
| CouchDB + PouchDB + Extensiones de Búsqueda | 4 | central | Provides the core HTTP API for managing databases and documents within the CouchDB sync l… | — | Sonnet | https://docs.couchdb.org/en/stable/api/database/common.html |
| couchdb-nano | 3 | central | CouchDB client for reading, writing, and syncing notes database | — | Sonnet | https://github.com/apache/couchdb-nano |
| CouchDB HTTP API | 3 | central | Provides reference API endpoints for CouchDB used by sync layers and agents within the pe… | — | Sonnet | https://docs.couchdb.org/en/stable/api/index.html |
| couchdb-replicator | 3 | central | Handles master-master replication and conflict resolution between the two Windows machine… | — | Sonnet | https://docs.couchdb.org/en/stable/replication/index.html |
| CouchDB View Server | 2 | central | CouchDB replication and views | — | Sonnet | https://couchdb.apache.org/docs/stable/views/index.html |
| Yjs | 1 | central | Conflict-free sync for Obsidian notes via CouchDB replication | — | Sonnet | https://github.com/yjs/yjs |
| CouchDB Attachments | 1 | central | Storing and retrieving binary files associated with Markdown notes in the CouchDB databas… | — | Sonnet | https://docs.couchdb.org/en/stable/api/document/attachments… |
| couchdb‑python | 45 | opcional | Python client for scripting reads and writes against the hub's CouchDB database | — | Sonnet | https://github.com/djc/couchdb-python |
| P2P File Sync (Syncthing) | 2 | opcional | Alternative sync layer for Markdown notes and CouchDB data | — | Sonnet | https://syncthing.net |
| CouchDB Fauxton | 1 | opcional | Web admin interface to inspect and manage the CouchDB database and debug replication conf… | — | Sonnet | https://github.com/apache/couchdb-fauxton |
| Rsync | 1 | opcional | Rsync can be used to back up the hub's folders or synchronize them between machines, but … | — | Sonnet | https://rsync.samba.org |
| CouchDB Change Feed + Kibana (via Logstash + BM25) | 2 | improvável | Ingest and transform CouchDB change feeds for external search indexing or analytics. | — | Sonnet | https://elastic.co/guide/en/logstash/current/index.html |

### MCP (10)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| MCP (Model Context Protocol) | 311 | central | MCP server for agent access to notes and local tools | — | Sonnet | https://modelcontextprotocol.io |
| MCP reference servers | 61 | central | Reference implementations for building the hub's MCP server | s6/modelcontextprotocol-servers.json | Sonnet | https://github.com/modelcontextprotocol/servers |
| FastMCP / mcp-sdk | 23 | central | SDK to build the MCP server that exposes hub notes and tools to AI agents. | s6/modelcontextprotocol-python-sdk.json | Opus | https://github.com/modelcontextprotocol/python-sdk |
| Node.js | 12 | central | Runtime for MCP servers and CLI tools | — | Opus | https://nodejs.org |
| MCP TypeScript SDK | 10 | central | MCP server and client SDK for Node.js | s6/modelcontextprotocol-typescript-sdk.json | Sonnet | https://github.com/modelcontextprotocol/typescript-sdk |
| mcp-server | 6 | central | Supports MCP protocol for agent communication in the hub. | — | Sonnet | https://github.com/modelcontextprotocol/modelcontextprotocol |
| FastMCP | 5 | central | Run the hub's MCP server exposing tools/resources to AI agents | — | Sonnet | https://github.com/jlowin/fastmcp |
| mcp-go | 1 | central | Build MCP servers/clients for AI agents to interact with the hub | — | Sonnet | https://github.com/modelcontextprotocol/go-sdk |
| rmcp (Rust MCP SDK) | 1 | central | The Rust MCP SDK (rmcp) is used to build the MCP server that interfaces with the personal… | — | Sonnet | https://github.com/modelcontextprotocol/rust-sdk |
| TypeDB (com plugin de busca semântica) | 3 | opcional | Typed graph storage for agent memory via MCP | — | Opus | https://vaticle.com/typedb |

### Markdown e frontmatter (32)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| Markdown 解析器（如 gray-matter 或 frontmatter） | 115 | central | Parse and write note front matter for metadata indexing | s6/gray-matter.json | Sonnet | https://github.com/jonschlinkert/gray-matter |
| python‑frontmatter | 114 | central | Parse/write YAML frontmatter for Obsidian notes (multilingual, pt-BR/EN) | s6/python-frontmatter.json | Sonnet | https://github.com/eyeseast/python-frontmatter |
| PyYAML | 93 | central | Parse YAML frontmatter in Obsidian Markdown notes | s6/pyyaml.json | Sonnet | https://github.com/yaml/pyyaml |
| remark | 67 | central | Parse Markdown/YAML frontmatter into AST for chunking by headings before indexing. | — | Sonnet | https://github.com/remarkjs/remark |
| markdown-it | 33 | central | Parses Markdown files to facilitate chunking by headings for indexing or processing. | — | Opus | https://github.com/markdown-it/markdown-it |
| js-yaml | 22 | central | Parse YAML frontmatter in notes for MCP server or Obsidian plugins. | — | Sonnet | https://github.com/nodeca/js-yaml |
| Markdown-it-py | 16 | central | tokenize frontmatter and Markdown for heading-aware chunking in multilingual notes | — | Sonnet | https://github.com/executablebooks/markdown-it-py |
| front-matter | 12 | central | Extract YAML front matter from Markdown notes to get metadata for indexing or filtering. | — | Sonnet | https://github.com/jxson/front-matter |
| mistune | 12 | central | Parse Markdown notes into AST for chunking before indexing. | — | Sonnet | https://github.com/lepture/mistune |
| unified | 11 | central | parse and transform Markdown with frontmatter via remark plugins | — | Sonnet | https://github.com/unifiedjs/unified |
| marked | 7 | central | Parse Markdown notes into HTML or extract content for processing by agents and internal t… | — | Sonnet | https://github.com/markedjs/marked |
| mdast-util-frontmatter | 7 | central | Parse and serialize YAML frontmatter in Markdown notes | — | Sonnet | https://github.com/syntax-tree/mdast-util-frontmatter |
| Goldmark | 7 | central | Parse and process Markdown/YAML frontmatter for note indexing, chunking, or conversion in… | — | Sonnet | https://github.com/yuin/goldmark |
| StrictYAML | 4 | central | Validates YAML frontmatter in Obsidian notes, type-checks fields and preserves comments o… | — | Sonnet | https://strictyaml.readthedocs.io |
| frontmatter (Go) | 4 | central | Parsing YAML frontmatter in Markdown notes | — | Sonnet | https://github.com/adrg/frontmatter |
| micromark | 2 | central | Parse Markdown frontmatter and structural tokens for Obsidian/YAML note chunking | — | Sonnet | https://github.com/micromark/micromark |
| Showdown | 2 | central | Render Markdown to HTML for notes in the hub, compatible with local LLM calls. | — | Sonnet | https://github.com/showdownjs/showdown |
| Whoosh + `Pydantic` (frontmatter) | 2 | central | Validate YAML frontmatter schemas in Python hub scripts | — | Sonnet | https://docs.pydantic.dev/latest |
| cmark-gfm | 2 | central | Parse notes into AST to split by headings and extract frontmatter for downstream processi… | — | Opus | https://github.com/github/cmark-gfm |
| cmark | 1 | central | Parse notes to AST for heading/metadata extraction before indexing | — | Sonnet | https://github.com/commonmark/cmark |
| yaml | 1 | central | Parse and preserve YAML frontmatter in Obsidian notes when agents edit them. | — | Opus | https://github.com/eemeli/yaml |
| Pydantic Core Models | 1 | central | Validate YAML/Markdown frontmatter schemas and process multilingual (pt/EN) data | — | Sonnet | https://docs.pydantic.dev |
| yq | 1 | central | CLI tool to bulk-edit and filter YAML frontmatter in Obsidian notes for agents and script… | — | Sonnet | https://mikefarah.gitbook.io/yq |
| mdast-util-from-markdown | 1 | central | Parse Markdown into mdast for heading-aware chunking | — | Sonnet | https://github.com/syntax-tree/mdast-util-from-markdown |
| Markdig | 8 | opcional | Process Markdown and YAML frontmatter for .NET applications | — | Sonnet | https://github.com/xoofx/markdig |
| Cerberus | 8 | opcional | validate note frontmatter | — | Sonnet | https://docs.python-cerberus.org/en/stable |
| JSON Schema | 5 | opcional | Validates structure of YAML frontmatter in notes and JSON config files using JSON Schema. | — | Sonnet | https://json-schema.org |
| SharpYaml | 4 | opcional | Parse YAML frontmatter in .NET tools | — | Sonnet | https://github.com/xoofx/sharpyaml |
| hexo-front-matter | 1 | opcional | Parse YAML/JSON front matter from Markdown notes to read metadata for indexing. | — | Sonnet | https://github.com/hexojs/hexo-front-matter |
| vfile-matter | 1 | opcional | Parses YAML frontmatter from Markdown notes for metadata extraction and indexing. | — | Sonnet | https://github.com/vfile/vfile-matter |
| Markdown Parser | 1 | opcional | Parses Markdown into an AST for structural manipulation and rendering. | — | Sonnet | https://github.com/commonmark/commonmark-java |
| mistletoe | 1 | opcional | Parse Markdown notes to AST for agent processing or reflow | — | Sonnet | https://github.com/miyuchina/mistletoe |

### Texto em português (PLN) (21)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| spaCy | 314 | central | Portuguese text processing | s6/spacy.json | Sonnet | https://github.com/explosion/spacy |
| stopwords-pt | 8 | central | Supports Portuguese text preprocessing with stopwords for NLP pipelines. | s6/stopwords-pt.json | Sonnet | https://github.com/stopwords-iso/stopwords-pt |
| sentencepiece | 7 | central | Tokenize text for embeddings and NLP tasks | — | Sonnet | https://github.com/google/sentencepiece |
| UDPipe | 4 | central | Normalize Portuguese terms for lexical search | — | Opus | https://github.com/ufal/udpipe |
| lingua-py | 1 | central | Detect language of notes before indexing. | s6/lingua-py.json | Sonnet | https://github.com/pemistahl/lingua-py |
| lingua-rs | 1 | central | Language detection for Portuguese text preprocessing in a personal context hub. | — | Sonnet | https://github.com/pemistahl/lingua-rs |
| Stemming in Hugging Face Tokenizers | 1 | central | Provides fast tokenization for Portuguese/English text before embedding or LLM inference. | — | Sonnet | https://huggingface.co/docs/tokenizers |
| stopword | 1 | central | filter stopwords in Portuguese/English text before indexing | — | Sonnet | https://github.com/fergiemcdowall/stopword |
| Polyglot Portuguese | 1 | central | preprocess Portuguese/English notes for AI agents, enabling entity extraction, language d… | — | Sonnet | https://polyglot.readthedocs.io |
| NLTK | 257 | opcional | Provides Portuguese stemming and tokenization for pre-processing text before indexing or … | — | Sonnet | https://github.com/nltk/nltk |
| Stanza | 40 | opcional | Lemmatize and tokenize Portuguese and English notes for agent tasks or text preprocessing. | — | Sonnet | https://github.com/stanfordnlp/stanza |
| Unidecode | 38 | opcional | Normalize Portuguese text by stripping accents for accent-insensitive matching and indexi… | — | Sonnet | https://github.com/avian2/unidecode |
| natural | 29 | opcional | Provide tokenization, stemming, and language detection for Portuguese and English notes. | — | Opus | https://github.com/naturalnode/natural |
| OpenNLP | 23 | opcional | Portuguese lemmatization, tokenization, and language detection for note preprocessing bef… | — | Opus | https://opennlp.apache.org |
| Flair | 22 | opcional | Provides Portuguese NER, sentiment, POS tagging and embeddings for notes | — | Sonnet | https://github.com/flairnlp/flair |
| ICU | 15 | opcional | Provides Unicode normalization, collation, and text boundary detection for multilingual n… | — | Sonnet | https://github.com/unicode-org/icu |
| MUSE (Multilingual Unsupervised and Supervised Em… | 8 | opcional | MUSE provides multilingual word embeddings and bilingual dictionaries, useful for analyzi… | — | Sonnet | https://github.com/facebookresearch/muse |
| Langdetect | 6 | opcional | Language detection for Portuguese and English text | — | Sonnet | https://github.com/mimino666/langdetect |
| Python-Levenshtein | 2 | opcional | Provides fast Levenshtein distance calculations for typo-tolerant string matching, useful… | — | Sonnet | https://github.com/maxbachmann/python-levenshtein |
| ftfy | 1 | opcional | Fix encoding mojibake in notes before indexing or sync | — | Sonnet | https://github.com/luminosoinsight/python-ftfy |
| BabelNet | 1 | opcional | query expansion for multilingual text (pt/EN) via lexical-semantic network | — | Sonnet | https://babelnet.org |

### Embeddings e rerank (18)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| DistilBERT | 240 | central | Run local embedding and reranker models | — | Opus | https://github.com/huggingface/transformers |
| fastText | 104 | central | Generate Portuguese embeddings for text in the hub | — | Sonnet | https://github.com/facebookresearch/fasttext |
| onnxruntime | 48 | central | ONNX Runtime serves as the underlying inference engine for local embedding models (like t… | s6/onnxruntime.json | Sonnet | https://github.com/microsoft/onnxruntime |
| Tch | 2 | central | Run PyTorch-based embedding models locally for semantic search and reranking. | — | Sonnet | https://github.com/laurentmazare/tch-rs |
| vLLM | 2 | central | hosts embedding models for semantic search via OpenAI-compatible API | — | Sonnet | https://github.com/vllm-project/vllm |
| HuggingFace Tokenizers + Transformers | 2 | central | Runs local embedding models and LLMs for RAG and text processing within the hub. | s6/transformers.json | Sonnet | https://huggingface.co/docs/transformers |
| ort | 1 | central | Run local embedding and reranker models via ONNX Runtime on Windows | s6/ort.json | Sonnet | https://github.com/pykeio/ort |
| Python Embeddings | 1 | central | Run local embedding models and LLMs | — | Opus | https://huggingface.co/docs/transformers/index |
| XLM-RoBERTa | 24 | opcional | Multilingual embeddings for Portuguese/English | — | Opus | https://github.com/facebookresearch/xlm |
| Hugging Face Transformers.js | 7 | opcional | Generate embeddings locally in Obsidian plugins or MCP nodes without a server via ONNX Ru… | — | Sonnet | https://github.com/huggingface/transformers.js |
| Doc2Vec | 6 | opcional | Train legacy document embeddings; may need MCP integration for local LLM use | — | Sonnet | https://radimrehurek.com/gensim/models/doc2vec.html |
| Beir | 2 | opcional | Benchmark retrieval quality (NDCG, recall) against the hub's embedding/reranking layer | — | Opus | https://github.com/beir-cellar/beir |
| ConceptNet Numberbatch | 1 | opcional | Provide pre-computed multilingual word embeddings for NLP tasks involving Portuguese and … | — | Sonnet | https://github.com/commonsense/conceptnet-numberbatch |
| StarSpace | 1 | opcional | Treinar embeddings para entidades como palavras ou documentos, útil para ranking e classi… | — | Sonnet | https://github.com/facebookresearch/starspace |
| SimCSE | 1 | opcional | SimCSE provides pretrained sentence embedding models for semantic search and similarity a… | — | Sonnet | https://github.com/princeton-nlp/simcse |
| GloVe | 20 | improvável | static word vectors, outdated for passage search | — | Opus | https://github.com/stanfordnlp/glove |
| TensorFlow Similarity | 6 | improvável | Train custom embedding models for local similarity search, likely redundant with existing… | — | Sonnet | https://github.com/tensorflow/similarity |
| TensorFlow Ranking | 1 | improvável | none | — | Opus | https://github.com/tensorflow/ranking |

### Modelos locais e gateways (8)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| Ollama | 148 | central | Serve local LLMs and embeddings | s6/ollama.json | Sonnet | https://github.com/ollama/ollama |
| GPT4All | 14 | central | Provides local LLM inference for AI agents and gateway. | s6/gpt4all.json | Sonnet | https://github.com/nomic-ai/gpt4all |
| LocalAI + LangChain | 13 | central | Local LLM/embedding server with built-in RAG and agent capabilities; replaces or augments… | s6/localai.json | Sonnet | https://github.com/go-skynet/localai |
| LiteLLM | 4 | central | Provide a local OpenAI‑compatible LLM gateway for agents and embeddings | — | Sonnet | https://github.com/berriai/litellm |
| Llamafile | 3 | central | Serves as local LLM backend for generation and embeddings used by AI agents. | — | Sonnet | https://github.com/mozilla-ocho/llamafile |
| LlamaStack | 1 | central | Provide local OpenAI-compatible LLM gateway with MCP tool integration | — | Opus | https://github.com/meta-llama/llama-stack |
| llama-cpp-python | 1 | central | Provide local LLM inference via an OpenAI‑compatible API for agents and users. | — | Sonnet | https://github.com/abetlen/llama-cpp-python |
| Azure Cognitive Services | 1 | central | Hosts local LLM servers (Ollama, llama.cpp) for agent workflows in the hub. | — | Sonnet | https://azure.microsoft.com/en-us/services/cognitive-servic… |

### Extração de texto (12)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| Lucene (via Apache Tika) | 41 | central | Extracts text and metadata from various file formats, including PDF and Office documents,… | s6/apache-tika.json | Sonnet | https://github.com/apache/tika |
| pandoc | 34 | central | Converts imported Office/HTML/EPUB documents into Markdown notes before they enter the hu… | s6/pandoc.json | Opus | https://github.com/jgm/pandoc |
| Docling | 6 | central | Convert PDFs/Office docs to Markdown for notes via MCP server integration | s6/docling.json | Sonnet | https://github.com/ds4sd/docling |
| PyMuPDF / MarkItDown | 4 | central | converts PDFs and Office files to Markdown for the vault | — | Sonnet | https://github.com/microsoft/markitdown |
| Jina Reader | 2 | central | Convert web pages, PDFs, Office files to Markdown notes | — | Sonnet | https://github.com/jina-ai/reader |
| Marker | 1 | central | Converts various document formats to Markdown for hub ingestion. | — | Sonnet | https://github.com/vikparuchuri/marker |
| Trafilatura (text extraction) | 1 | central | convert web content to Markdown notes for the hub | — | Sonnet | https://github.com/adbar/trafilatura |
| Unstructured | 13 | opcional | Extract text from PDFs, HTML, Word, and images for LLMs | — | Sonnet | https://github.com/unstructured-io/unstructured |
| Markdownify | 2 | opcional | Converts HTML content from web pages into Markdown format for storage as notes in the hub. | — | Sonnet | https://github.com/matthewwithanm/python-markdownify |
| Pytesseract | 1 | opcional | Extract text from scanned images/PDFs for indexing or agent processing | — | Sonnet | https://github.com/tesseract-ocr/tesseract |
| SimpleDirectoryReader + MarkdownNodeParser | 1 | opcional | Loads various local file formats into LlamaIndex documents for RAG and agentic workflows. | — | Sonnet | https://docs.llamaindex.ai/en/stable/module_guides/loading/… |
| ingest-attachment plugin | 1 | improvável | Extracts text from PDF and Office attachments to be included in the Markdown notes conten… | — | Sonnet | https://elastic.co/guide/en/elasticsearch/plugins/7.10/inge… |

### Bancos e armazenamento (23)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| SQLite | 11 | central | Local structured storage for metadata, indexing, or agent memory outside of CouchDB. | s6/sqlite.json | Sonnet | https://sqlite.org/index.html |
| diskcache | 3 | central | Cache embeddings or expensive results locally using SQLite | — | Sonnet | https://github.com/grantjenks/python-diskcache |
| SurrealDB | 2 | central | Replaces CouchDB with hybrid search and MCP access. | s6/surrealdb.json | Sonnet | https://surrealdb.com |
| rusqlite | 1 | central | SQLite database for local storage and indexing | s6/rusqlite.json | Sonnet | https://github.com/rusqlite/rusqlite |
| ArangoDB Documentation | 1 | central | Hosts ArangoDB documentation, exposing its API for querying and managing data. | — | Sonnet | https://arangodb.com/docs/stable |
| DuckDB | 159 | opcional | Lightweight SQL metadata/indexing store for local note indexing (CSV/Parquet support) | — | Sonnet | https://github.com/duckdb/duckdb |
| Federated Search (ArangoDB) | 11 | opcional | ArangoDB serves as a secondary storage option for the hub, providing a graph-native datab… | — | Opus | https://arangodb.com |
| DocArray | 10 | opcional | vector database for storing and retrieving embeddings | — | Sonnet | https://github.com/docarray/docarray |
| RocksDB | 5 | opcional | Embedded key-value storage for local indexes or state, complementing CouchDB for specific… | — | Sonnet | https://github.com/facebook/rocksdb |
| SQLite Python Bindings | 3 | opcional | Local structured storage for indexing, metadata, or agent memory outside of CouchDB. | — | Sonnet | https://docs.python.org/3/library/sqlite3.html |
| Sled | 2 | opcional | Sled serves as a local, embedded database for storing metadata and indices, complementing… | — | Sonnet | https://github.com/spacejam/sled |
| Peewee | 2 | opcional | Provide ORM layer for a local SQLite/Postgres index database | — | Sonnet | https://docs.peewee-orm.com/en/latest |
| LevelDB | 1 | opcional | Local key-value store for indexing or sync metadata | — | Sonnet | https://github.com/google/leveldb |
| SQLite Node.js Bindings | 1 | opcional | Local SQLite storage for lightweight, non-CouchDB data needs (e.g., agent metadata, cache… | — | Sonnet | https://github.com/mapbox/node-sqlite3 |
| Datasette | 1 | opcional | Exposes SQLite index database via web UI and API for data exploration. | — | Sonnet | https://datasette.io |
| SQLite with SQLite-FTS | 1 | opcional | Provide lightweight local SQLite storage with full-text search via FTS extensions | — | Sonnet | https://github.com/nalgeon/sqlean |
| better-sqlite3 | 1 | opcional | Local SQLite storage for indexing or metadata management within Node.js components. | — | Sonnet | https://github.com/wiselibs/better-sqlite3 |
| shelve | 1 | opcional | Provide a simple Python persistent key‑value store for agent scripts or temporary caches. | — | Sonnet | https://docs.python.org/3/library/shelve.html |
| RethinkDB | 10 | improvável | Provides realtime JSON database with change feeds for push updates. | — | Opus | https://rethinkdb.com |
| Supabase | 4 | improvável | Postgres backend for vector embeddings and storage | — | Sonnet | https://supabase.com |
| Dgraph | 3 | improvável | Store note relations as a graph; too heavy and distributed for a personal local hub. | — | Sonnet | https://dgraph.io |
| Kibana | 2 | improvável | Elasticsearch serves as a high-performance, distributed search and analytics engine for t… | — | Sonnet | https://elastic.co/guide/en/kibana/current/index.html |
| ArangoDB Client Libraries | 1 | improvável | Not needed as the hub specifically uses CouchDB for data storage and replication. | — | Sonnet | https://arangodb.com/docs/stable/drivers |

### Eventos, filas e vigias (14)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| nanomsg | 12 | central | message broker protocol for pub/sub/req-rep in local event handling | — | Sonnet | https://github.com/nanomsg/nanomsg |
| Watchdog | 6 | central | Trigger reindexing on Markdown file changes | s6/watchdog.json | Sonnet | https://github.com/gorakhargosh/watchdog |
| watchman | 2 | central | detect file changes and trigger actions on notes | s6/watchman.json | Opus | https://github.com/facebook/watchman |
| NATS | 72 | opcional | Event bus for local services and agents | — | Sonnet | https://github.com/nats-io/nats-server |
| Logstash | 38 | opcional | process Markdown notes as event streams for AI agents | — | Sonnet | https://elastic.co/de/logstash |
| nng (nanomsg next generation) | 12 | opcional | Inter-process messaging for background jobs | — | Sonnet | https://github.com/nanomsg/nng |
| Joblib | 6 | opcional | Parallelize embedding jobs and cache results to disk | — | Sonnet | https://joblib.readthedocs.io |
| Everything Search Engine | 5 | opcional | Locates files quickly by name, complements CouchDB for file access. | — | Sonnet | https://voidtools.com |
| Celery | 4 | opcional | Celery serves as a distributed task queue for background job processing, enabling asynchr… | — | Sonnet | https://docs.celeryproject.org/en/stable |
| Apache NiFi | 2 | opcional | Processar e distribuir dados de eventos, como notas ou logs. | — | Sonnet | https://nifi.apache.org |
| Chokidar | 1 | opcional | Trigger re-indexing or sync when notes change on disk | — | Sonnet | https://github.com/paulmillr/chokidar |
| NATS + Temporal (for workflows) | 1 | opcional | Orchestrate durable agent workflows and background jobs for note processing. | — | Sonnet | https://temporal.io |
| PyNATS | 6 | improvável | NATS client for hub event streaming and job queue communication. | — | Sonnet | https://github.com/nats-io/nats.py |
| pynng | 5 | improvável | Low-level IPC messaging between Python services if hub adds multiple Python processes | — | Sonnet | https://github.com/codypiersall/pynng |

### Serviço e API (1)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| FastAPI | 218 | opcional | Expose local services, MCP endpoints, or custom API interfaces for the hub components. | — | Sonnet | https://github.com/tiangolo/fastapi |

### Frameworks de agente e RAG (9)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| Mem0 | 5 | central | Provides an intelligent memory layer for AI agents to store and retrieve user preferences… | — | Sonnet | https://github.com/mem0ai/mem0 |
| n8n | 5 | central | Builds and deploys AI agents and workflows, connects to 1500+ integrations | s6/n8n.json | Sonnet | https://github.com/n8n-io/n8n |
| CrewAI / LangGraph | 1 | central | Orchestrate stateful agents with durable execution and memory | — | Sonnet | https://python.langchain.com/docs/langgraph |
| LangChain | 361 | opcional | Orchestrate LLM agents and RAG pipelines to query and update notes. | — | Sonnet | https://github.com/hwchase17/langchain |
| Deepset Cloud | 2 | opcional | RAG framework for agent pipelines and context-engineered agents | — | Sonnet | https://deepset.ai |
| IngestionPipeline | 2 | opcional | Chunks notes, computes embeddings, deduplicates, and upserts into vector store for RAG re… | — | Sonnet | https://docs.llamaindex.ai/en/stable/module_guides/loading/… |
| Pydantic AI | 1 | opcional | Build custom AI agents for the hub | — | Opus | https://github.com/pydantic/pydantic-ai |
| QueryEngine + ResponseSynthesizer | 1 | opcional | LLM-driven response synthesis for agents via MCP, replacing LlamaIndex’s role in this hub | — | Sonnet | https://docs.llamaindex.ai/en/stable/module_guides/querying… |
| Langfuse | 2 | improvável | Trace agent execution steps and LLM calls for debugging/evaluation. | — | Sonnet | https://github.com/langfuse/langfuse |

### Obsidian (6)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| Obsidian (registro de plugins) | 74 | central | Hosts and distributes Obsidian plugins for the hub's agents | — | Sonnet | https://github.com/obsidianmd/obsidian-releases |
| Obsidian Dataview plugin | 27 | central | Provides querying of markdown notes via frontmatter and inline fields within Obsidian vau… | s6/obsidian-dataview.json | Sonnet | https://github.com/blacksmithgu/obsidian-dataview |
| Obsidian API | 4 | central | Type definitions for developing Obsidian plugins to interact with the vault and metadata … | s6/obsidian-api.json | Sonnet | https://github.com/obsidianmd/obsidian-api |
| Obsidian Plugin Samples | 1 | central | Enables Obsidian plugin integration for AI agents (e.g., Claude Code) to extend functiona… | — | Sonnet | https://github.com/obsidianmd/obsidian-sample-plugin |
| Templater | 1 | central | adds template engine for standardized note creation in Obsidian | s6/templater.json | Sonnet | https://silentvoid13.github.io/templater |
| Obsidian Advanced URI | 4 | opcional | Enable external scripts and AI agents to read/write Obsidian notes via URI commands. | — | Sonnet | https://github.com/vinzent03/obsidian-advanced-uri |

### Outros (6)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| Docker Desktop for Windows | 5 | opcional | Run local containers such as CouchDB or search services on Windows | — | Sonnet | https://docker.com/products/docker-desktop |
| configparser | 3 | opcional | Store small script settings in INI files | — | Sonnet | https://docs.python.org/3/library/configparser.html |
| Git | 2 | opcional | Version control backup for notes folder | — | Opus | https://git-scm.com |
| Local Cluster (Docker Compose) | 11 | improvável | not used in hub | — | Sonnet | https://docs.docker.com/compose |
| fzf (fuzzy finder) | 3 | improvável | interactive terminal fuzzy finder for local file search | — | Sonnet | https://github.com/junegunn/fzf |
| Security & Authentication (OpenSearch Security Pl… | 1 | improvável | OpenSearch cluster security, not used in hub | — | Sonnet | https://opensearch.org/docs/latest/security |

### Divergentes (sem maioria) (6)

| Nome | Menções | Encaixe | Uso no hub | Régua | Registro | URL |
|---|---|---|---|---|---|---|
| Fast File Indexer (e.g., `rayon` + `walkdir`) | 3 | opcional | Paralelizar a indexação de arquivos Markdown, se o indexador for escrito em Rust | — | Sonnet | https://github.com/rayon-rs/rayon |
| Dendron VS Code Extension | 3 | opcional | Hierarchical local-first Markdown note-taking/PKM tool as a VS Code extension, with looku… | — | Sonnet | https://marketplace.visualstudio.com/items |
| fd | 2 | opcional | Localizar arquivos por nome no disco, complementar ao grep | — | Sonnet | https://github.com/sharkdp/fd |
| Ingest Pipeline | 11 | improvável | Elasticsearch ingest pipelines transform documents (remove fields, extract values, enrich… | — | Sonnet | https://elastic.co/guide/en/elasticsearch/reference/current… |
| GitJournal | 1 | improvável | Mobile Markdown notes client syncing plain files via Git; sync-side reference only. | — | Sonnet | https://gitjournal.io |
| Azure OpenAI Service (text-embedding-ada-002) | 1 | improvável | hosted OpenAI models (GPT, reasoning, fine-tuning) as a cloud service | — | Sonnet | https://azure.microsoft.com/en-us/services/cognitive-servic… |

## 3. Finalistas com régua que vieram de fora do catálogo (23)

Entraram pela varredura com web (S2) ou pelas pesquisas antigas; o laço não os trouxe.

| Nome | Papel | Régua | URL |
|---|---|---|---|
| 1MCP agent | repasse de MCP | s3/1mcp-agent.json | https://github.com/1mcp-app/agent |
| ck | disco+MCP pronto | s3/ck.json | https://github.com/BeaconBay/ck |
| CouchDB Clouseau/Dreyfus | dentro do banco | s3/couchdb-clouseau-dreyfus.json | https://docs.couchdb.org/en/latest/ddocs/search.html |
| CouchDB Nouveau | dentro do banco | s3/couchdb-nouveau.json | https://docs.couchdb.org/en/latest/ddocs/nouveau.html |
| devrag | disco+MCP pronto | s3/devrag.json | https://github.com/tomohiro-owada/devrag |
| FastMCP proxy/mount | repasse de MCP | s3/fastmcp-proxy-mount.json | https://gofastmcp.com/servers/providers/proxy.md |
| grepai | disco+MCP pronto | s3/grepai.json | https://github.com/yoanbernabeu/grepai |
| kb-index | disco+MCP pronto | s3/kb-index.json | https://github.com/ZhengchenTao/kb-index |
| local-notes-search-mcp | disco+MCP pronto | s3/local-notes-search-mcp.json | https://github.com/Furkiozknn/local-notes-search-mcp |
| LocalVectorSearchMcp | disco+MCP pronto | s3/localvectorsearchmcp.json | https://github.com/DimonSmart/LocalVectorSearchMcp |
| markdown-vault-mcp | disco+MCP pronto | s3/markdown-vault-mcp.json | https://github.com/pvliesdonk/markdown-vault-mcp |
| memtomem | disco+MCP pronto | s3/memtomem.json | https://github.com/memtomem/memtomem |
| Miyo | lado do Obsidian / disco | s3/miyo.json | https://miyo.md |
| obsidian-brain | disco+MCP pronto | s3/obsidian-brain.json | https://github.com/sweir1/obsidian-brain |
| obsidian-hybrid-search | disco+MCP pronto | s3/obsidian-hybrid-search.json | https://github.com/flowing-abyss/obsidian-hybrid-search |
| obsidian-semantic-mcp | disco+MCP pronto | s3/obsidian-semantic-mcp.json | https://github.com/DalecB/obsidian-semantic-mcp |
| Omnisearch | lado do Obsidian | s3/omnisearch.json | https://github.com/scambier/obsidian-omnisearch |
| qmd | disco+MCP pronto | s3/qmd.json | https://github.com/tobi/qmd |
| sparfenyuk/mcp-proxy | repasse de MCP | s3/sparfenyuk-mcp-proxy.json | https://github.com/sparfenyuk/mcp-proxy |
| TBXark/mcp-proxy | repasse de MCP | s3/tbxark-mcp-proxy.json | https://github.com/TBXark/mcp-proxy |
| vault-cortex | disco+MCP pronto | s3/vault-cortex.json | https://github.com/aliasunder/vault-cortex |
| vexor | disco+MCP pronto | s3/vexor.json | https://github.com/scarletkc/vexor |
| zvec-grep | disco+MCP pronto | s3/zvec-grep.json | https://github.com/zvec-ai/zvec-grep |

## 4. Conceitos (292)

Citados por 2 ou mais cartões ou ligados a um projeto do catálogo. Triagem sem fonte primária: na auditoria, 12,5% tinham erro grave.

| Conceito | Cartões | Serve | Ferramentas citadas |
|---|---|---|---|
| hybrid search | 67 | search | FAISS, Elasticsearch, SQLite FTS5, Weaviate, Whoosh, Recoll, Xapian, sentence-t… |
| bm25 | 25 | search | Lucene, Snowflake, whoosh, pysolr, DuckDB, solr, vespa, LangChain |
| frontmatter filtering | 15 | search | FlexSearch, Dendron, sqlite, DuckDB, OpenSearch, AnythingLLM, Lucene.NET, Recoll |
| stemming | 14 | search | Snowball, libstemmer, nltk, snowballstemmer, unicodedata, PostgreSQL Full Text … |
| metadata filtering | 13 | search | Milvus, haystack, Jina, LanceDB, Apache Arrow, Sonic-Frontmatter Filter, Sonic,… |
| vector search | 12 | search | Lucene.NET, ArangoDB, Couchbase Server, Lucene, Meilisearch, solr, Typesense, S… |
| portuguese stemming | 9 | search | Snowball, Meilisearch, Sphinx, Manticore, Porter Stemmer, PorterStemmer, RSLP, … |
| messagepack | 8 | stack | MessagePack, CouchDB, MCP |
| portuguese analyzer | 5 | search | Typesense, Elasticsearch, Whoosh, Snowball |
| offline search | 5 | search | FlexSearch, typesense |
| frontmatter parsing | 4 | search | YamlDotNet, MARP, Solr |
| embeddings | 4 | search | Dendron, sentence-transformers, OpenAI, Elasticsearch, PySpark, Koalas, Annoy, … |
| accent normalization | 3 | search | whoosh |
| accent folding | 3 | search | Typesense, Xapian |
| vector embeddings | 3 | search | ArangoDB, ArangoSearch, sentence-transformers, Orama, Weaviate |
| bm25f | 3 | search | Whoosh |
| federated search | 3 | search | Xapian, Lucene, Elasticsearch, Weaviate |
| couchdb replication | 3 | stack | CouchDB |
| frontmatter schema | 3 | search | Dendron |
| dense retrieval | 3 | search |  |
| frontmatter indexing | 3 | search | Elasticsearch, Recoll, Whoosh |
| inverted index | 3 | search | Elasticsearch |
| html comment metadata | 3 | stack |  |
| faceted search | 3 | search | Haystack, typesense |
| rest api | 3 | stack | Pyramid, MCP |
| reciprocal rank fusion | 3 | search | LangChain |
| lemmatization | 3 | search | NLTK, spaCy |
| unicode normalization | 3 | search | Unicode CLDR, unicode-normalization |
| markdown indexing pipeline | 3 | search | Meilisearch, Whoosh |
| nng | 3 | stack | NNG |
| stemming and lemmatization | 3 | search | NLTK, SpaCy, Snowball Stemmer, spaCy, RSLP |
| search aggregator | 2 | search |  |
| text analyzer | 2 | search | ArangoDB, FlexSearch |
| sentence embeddings | 2 | search | BAAI/bge-small-en |
| change data capture | 2 | stack | CouchDB _changes, NATS JetStream |
| model context protocol | 2 | stack | Claude Code, Codex, GitHub Copilot, modelcontext/mcp, Elasticsearch MCP |
| couchdb indexing | 2 | search | CouchDB, MCP |
| approximate nearest neighbor search | 2 | search | FAISS, cuML |
| neural search | 2 | search | Elasticsearch |
| search result highlighting | 2 | search | Elasticsearch, Apache Solr |
| index templates | 2 | search | Elasticsearch, OpenSearch |
| multilingual embeddings | 2 | search | distiluse-base-multilingual-cased, multilingual-e5, bge-m3 |
| front matter | 2 | stack |  |
| frontmatter | 2 | search | python-frontmatter |
| full-text search | 2 | search | PostgreSQL tsvector, MariaDB |
| hnsw | 2 | search | Manticore, LanceDB |
| real-time index | 2 | search | Sphinx |
| lancaster stemmer | 2 | search | NLTK |
| mcp search server | 2 | stack | Lunary, RAGFlow, MCP |
| markdown frontmatter | 2 | stack |  |
| multilingual search | 2 | search |  |
| request-reply | 2 | stack | NATS, nng, ZeroMQ, nanomsg |
| offline mode | 2 | search | Elasticsearch, weaviate |
| offline search cache | 2 | stack |  |
| accent-insensitive search | 2 | search | Snowball, PostgreSQL Full Text Search |
| snowball stemming | 2 | search | DuckDB |
| user-defined function | 2 | none | PySpark, Snowflake |
| rag | 2 | search | facebookresearch/rag |
| semantic search | 2 | search | Sentence-BERT, FAISS |
| replicated local index | 2 | stack | CouchDB, Tantivy |
| sidecar metadata | 2 | stack |  |
| tantivy | 2 | search | Tantivy |
| python type hints | 2 | stack | mypy |
| vector database | 2 | search | Milvus, FAISS, ChromaDB |
| word embeddings | 2 | search | word2vec, GloVe |
| zettelkasten | 2 | stack | Obsidian, Logseq |
| ai agent integration | 1 | stack | Fuse.js |
| search rules | 1 | search | algolia |
| synonyms | 1 | search | Algolia |
| analyzer | 1 | search | Lucene |
| keyed state backend | 1 | none | Apache Flink, RocksDB |
| ast markdown processing | 1 | search | remark |
| search benchmarking | 1 | search | Elasticlunr |
| llm reranking | 1 | search | BM25Ranker, RankGPT |
| boolean filter | 1 | search | Elasticsearch |
| nats mcp bridge | 1 | stack | NATS |
| mcp server for search | 1 | stack | OpenSearch |
| couchdb change feed sync | 1 | stack | CouchDB |
| changes feed indexing worker | 1 | search | CouchDB, Ollama, Milvus, pgvector |
| couchdb continuous replication | 1 | stack | CouchDB |
| couchdb design documents | 1 | search | CouchDB |
| embeddings storage | 1 | search | CouchDB |
| vector embeddings storage | 1 | search | CouchDB |
| couchdb filtering | 1 | search | CouchDB |
| couchdb full-text indexing | 1 | search | Lucene.NET |
| couchdb mango index | 1 | search | CouchDB |
| couchdb mapreduce view | 1 | search | CouchDB |
| n1ql query language | 1 | search | CouchDB |
| couchdb full-text search | 1 | search | CouchDB |
| couchdb to lucene sync | 1 | search | CouchDB, Lucene |
| couchdb to recoll sync | 1 | stack | Recoll, CouchDB |
| couchdb custom search index | 1 | search | CouchDB |
| couchdb mcp integration | 1 | stack | CouchDB |
| couchdb text analysis | 1 | search | CouchDB |
| couchdb frontmatter filter | 1 | search | CouchDB |
| hybrid search architecture | 1 | search | Whoosh, Tantivy, LanceDB |
| custom frontmatter extraction | 1 | stack | frontmatter, ruamel.yaml |
| custom mcp plugin | 1 | search | Whoosh, Meilisearch, CouchDB, nltk, spaCy |
| data import handler | 1 | search | Solr |
| dense vector field | 1 | search | Elasticsearch |
| custom nlp pipeline | 1 | search | YamlDotNet, Lucene.NET, SBERT |
| duckdb index | 1 | search | DuckDB |
| duckdb-python-udfs | 1 | stack | DuckDB |
| duckdb views | 1 | stack | DuckDB |
| edge ngram | 1 | search | Elasticsearch |
| elasticlunr plugins | 1 | search | Elasticlunr |
| bool query | 1 | search | Elasticsearch |
| elasticsearch cluster coordination | 1 | none | Elasticsearch |
| custom analyzer | 1 | search | Elasticsearch |
| script score | 1 | search | Elasticsearch |
| elasticsearch embedding index | 1 | search | Elasticsearch |
| search filtering | 1 | search | Elasticsearch |
| frontmatter metadata extraction | 1 | search | Elasticsearch |
| hybrid query | 1 | search | Elasticsearch |
| ingest pipeline | 1 | search | Elasticsearch, grok |
| embedding inference | 1 | search | Elasticsearch |
| elasticsearch mapping | 1 | search | Elasticsearch |
| elasticsearch machine learning | 1 | search | Elasticsearch |
| multilingual indexing | 1 | search | Elasticsearch |
| language analyzer | 1 | search | Elasticsearch |
| multi-match bool query | 1 | search | Elasticsearch |
| elasticsearch query dsl | 1 | search | Elasticsearch |
| elasticsearch ingest pipeline | 1 | search | Elasticsearch |
| elasticsearch reindex api | 1 | stack | Elasticsearch |
| hybrid reranking | 1 | search | Elasticsearch |
| script score query | 1 | search | Elasticsearch |
| search highlighting | 1 | search | Elasticsearch |
| term query | 1 | search | Elasticsearch |
| term vectors | 1 | search | Elasticsearch |
| elasticsearch field mappings | 1 | search | Elasticsearch |
| embedded library per agent | 1 | search | Tantivy, Whoosh, sqlite-vec |
| faiss | 1 | search | Faiss |
| faiss flat inner product index | 1 | search | FAISS |
| faiss flat l2 | 1 | search | faiss |
| fastapi mcp | 1 | stack | FastAPI-MCP |
| fastapi wrapper | 1 | stack | FastAPI |
| mcp server | 1 | stack | FastMCP, NATS |
| search api | 1 | stack | FlexSearch, MCP |
| search cli | 1 | search | FlexSearch |
| flexsearch documentation | 1 | none | FlexSearch |
| local index storage | 1 | stack | FlexSearch |
| server-side full-text search library | 1 | search | FlexSearch |
| stopword list | 1 | search | FlexSearch |
| fuse.js embeddings | 1 | search | Fuse.js |
| composable_pipelines | 1 | stack | Haystack |
| filtering_pipeline | 1 | search | Haystack |
| haystack offline mode | 1 | search | Haystack |
| haystack pipeline dsl | 1 | search | haystack |
| realtime index update | 1 | search | Haystack |
| hnsw vector search | 1 | search | tantivy |
| hybrid query dsl | 1 | search | Elasticsearch |
| icu analyzer | 1 | search | ICU4J, ICU4C |
| centralized replicated index with couchdb | 1 | search | CouchDB, MCP server |
| inference processor | 1 | search | Elasticsearch, ELSER |
| ingest script processing | 1 | search | Elasticsearch, Painless |
| json attributes | 1 | search | Manticore |
| kibana data view | 1 | none | Kibana, Elasticsearch |
| knn search | 1 | search | Elasticsearch |
| knn vector search | 1 | search | Lucene, Solr |
| langchain expression language | 1 | search | LangChain |
| markdown loader | 1 | stack | LangChain |
| rag indexing framework (llamaindex, formerly gpt index) | 1 | search | LlamaIndex |
| local offline index | 1 | search | LlamaIndex |
| query engine | 1 | search | LlamaIndex |
| vector store | 1 | search | LlamaIndex |
| local-first sync | 1 | stack | CouchDB, PouchDB |
| local vector index | 1 | search | FAISS, HNSWLib |
| local-search-api | 1 | search | MCP |
| local search with couchdb | 1 | search | couchdb |
| vector database benchmark | 1 | search | Elasticsearch, Weaviate, FAISS |
| local vector store | 1 | search | llamaindex |
| embedding integration | 1 | search | Lucene |
| lucene embeddings | 1 | search | Lucene |
| lucene filters | 1 | search | Lucene |
| lucene frontmatter filter | 1 | search | Apache Lucene |
| lucene index | 1 | search | Lucene |
| local embeddings | 1 | search | Lucene.NET |
| lucene performance tuning | 1 | search | Lucene.NET |
| custom score query | 1 | search | Lucene.Net |
| lucene vector api | 1 | search | Lucene |
| lunr embeddings | 1 | search | lunr |
| lunr pipeline | 1 | search | lunr |
| mango queries | 1 | search | CouchDB |
| markdown parsing | 1 | search | Fuse.js |
| mcp bindings | 1 | stack | FastText, Whoosh, FAISS |
| mcp couchdb adapter | 1 | stack | CouchDB |
| custom hybrid search | 1 | search | whoosh, lucene, MCP |
| filterable attributes | 1 | search | Meilisearch |
| stop words | 1 | search | Meilisearch |
| meilisearch with ai agents | 1 | search | Meilisearch |
| meilisearch-sync | 1 | search | Meilisearch, CouchDB |
| meilisearch windows | 1 | search | Meilisearch |
| metadata filter | 1 | search | MetadataFilterRetriever, LangChain |
| vector index types | 1 | search | Milvus |
| local multilingual embedding models | 1 | search | bge-m3, nomic-embed-text, all-MiniLM-L6-v2, sentence-transformers |
| nats messaging | 1 | stack | NATS |
| nats leaf nodes | 1 | stack | NATS |
| microservices messaging | 1 | stack | NATS |
| nats tuning | 1 | none | NATS Server |
| publish subscribe messaging | 1 | stack | NATS |
| nats security | 1 | none | NATS |
| nats services | 1 | stack | NATS |
| subject wildcards | 1 | stack | NATS |
| pub/sub messaging | 1 | stack | NNG |
| request-reply messaging | 1 | stack | nng |
| obsidian front matter | 1 | stack | Obsidian |
| obsidian graph protocol | 1 | search | Obsidian Graph Protocol, Weaviate, Meilisearch, MCP |
| local embeddings plugin | 1 | search | sentence-transformers, Obsidian |
| local bm25 search | 1 | search | Meilisearch, Whoosh |
| obsidian plugin api | 1 | stack | Obsidian |
| obsidian search | 1 | search | Fuse.js |
| langchain | 1 | search | LangChain, sentence-transformers |
| obsidian-like vscode setup | 1 | stack | Markdown All in One, Front-Matter |
| offline elasticsearch | 1 | search | Elasticsearch, CouchDB |
| offline solr sync | 1 | stack | SolrCloud, CouchDB, MCP |
| opensearch cross-cluster replication | 1 | none | OpenSearch |
| index pruning | 1 | search | OpenSearch |
| opensearch index lifecycle | 1 | none | OpenSearch |
| index templates and ingest pipelines | 1 | search | OpenSearch |
| ingest pipelines | 1 | search | OpenSearch |
| observability | 1 | none | OpenSearch |
| opensearch plugins | 1 | search | OpenSearch |
| opensearch query dsl | 1 | search | OpenSearch |
| elasticsearch hybrid search | 1 | search | Elasticsearch, OpenSearch |
| post-build indexing | 1 | search | Pagefind |
| pandoc json ast | 1 | stack | Pandoc |
| pandoc json metadata | 1 | search | Pandoc |
| postgres hybrid search | 1 | search | pg_vector_search, pg_trgm, pgvector, tsvector |
| distributed text indexing | 1 | search | NATS |
| portuguese stemmer | 1 | search | MiniSearch |
| portuguese icu tokenizer | 1 | search | ICU, Elasticsearch, Whoosh, CouchDB FTS |
| portuguese nlp | 1 | search | Whoosh, langdetect, xlm-roberta |
| stopword filter | 1 | search | Elasticsearch |
| portuese text normalization | 1 | search | RediSearch, Snowball |
| text preprocessing | 1 | search | Haystack |
| attachment text extraction | 1 | search | Apache Tika, Elasticsearch |
| pubsub | 1 | stack | nanomsg |
| pydantic schemas | 1 | stack | Pydantic, MCP |
| pyramid couchdb integration | 1 | stack | Pyramid, CouchDB |
| fuzzy matching | 1 | search | RapidFuzz, portseg, Spark NLP |
| recoll external filters | 1 | search | Recoll |
| document filters | 1 | search | Recoll |
| langchain retriever | 1 | search | Recoll, LangChain |
| sqlite metadata index | 1 | search | Recoll, SQLite |
| redis | 1 | none | Redis |
| vector similarity search | 1 | search | Redis |
| reranking | 1 | search | Pagefind |
| rust search engine with mcp wrapper | 1 | search | tantivy, Deno, Node.js |
| frontmatter schema design | 1 | search | Solr |
| model server | 1 | search | Ollama, LocalAI, vLLM |
| shared_network_index | 1 | stack | Tantivy |
| similarity queries | 1 | search | gensim |
| snowball analyzer | 1 | search | Snowball, Lucene |
| snowball stemmer | 1 | search | Elasticsearch |
| solr analyzers | 1 | search | Solr |
| solr core configuration | 1 | search | Solr |
| dense vector search | 1 | search | Solr |
| solr managed schema api | 1 | search | Solr |
| offline reindexing | 1 | search | Solr |
| solr schema design | 1 | search | Solr |
| solr schema | 1 | search | Solr |
| solr managed schema | 1 | search | solr |
| embedded solr | 1 | search | solr |
| sonic embeddings plugin | 1 | search | Sonic |
| spacy similarity | 1 | search | spaCy |
| metadata_filtering_with_spacy | 1 | stack | spaCy, CouchDB, MCP |
| sqlite with indexing | 1 | search | SQLite |
| sqlite virtual tables | 1 | search | SQLite, FTS5 |
| static site generation | 1 | stack | Pagefind |
| stemming and tokenization | 1 | search | Redis |
| survey pattern | 1 | search | nng |
| fast fields | 1 | search | Tantivy |
| tantivy fast fields | 1 | search | tantivy |
| pandoc text extraction | 1 | search | Pandoc |
| tokenizer | 1 | search | Lucene |
| typesense-embeddings-integration | 1 | search | Typesense |
| search performance tuning | 1 | search | typesense |
| typesense vector search | 1 | search | Typesense |
| vector store index | 1 | search | LlamaIndex |
| vector database mcp server | 1 | search | Weaviate |
| bm25 module | 1 | search | Weaviate |
| vector_db_authz | 1 | none | Weaviate |
| text analysis pipeline | 1 | search | Whoosh |
| text analysis | 1 | search | Whoosh |
| embedding indexer | 1 | search | Whoosh, sentence-transformers |
| whoosh_offline_indexing | 1 | search | whoosh |
| whoosh schema | 1 | search | Whoosh |
| whoosh elasticsearch integration | 1 | search | Whoosh, Elasticsearch |
| windows compatibility | 1 | stack | Fuse.js |
| portuguese word form normalization | 1 | search | libstemmer, Manticore |
| sql-like query language | 1 | search | ZincSearch |
| hybrid indexing | 1 | search | Zotero, Milvus, Chroma |

## 5. A régua com fonte, em resumo (92 arquivos, 91 itens: o Tantivy tem duas fichas na S3)

Primeiras palavras de cada campo; a ficha completa, com as citações, está no arquivo. "nao_verificado" = a fonte primária não respondeu.

| Ficha | Projeto | Windows | MCP | Português | Licença | Último release | Maturidade | Encaixe |
|---|---|---|---|---|---|---|---|---|
| s3/1mcp-agent.json | 1MCP agent | yes (CI de binários com windows-latest e tes… | yes (agrega servidores MCP; expõe streamable… | nao_aplicavel | Apache-2.0 | v0.39.1 no feed de releases (… | beta (0.x, muito at… | Serviço local em cada máquina agregando MCPs para vários agentes, com modo CLI de descoberta progressiva. Impedimento: foco em reduzir tools no contexto, mais … |
| s6/annoy.json | Annoy (spotify/annoy) | yes: CI com windows-latest na matriz (Python… | no | nao_aplicavel: não trata texto, só vetores (… | Apache-2.0 | 1.17.3, 2023-06-14 (PyPI) | stable (sem aviso d… | Biblioteca de vetores dentro do MCP do banco, em cada máquina, para ANN em disco via mmap. Não é busca pronta: exige gerar embeddings, reconstruir o índice e c… |
| s6/apache-lucene.json | Apache Lucene (apache/lucene) | yes: roda em JVM (Java 21 ou superior); repo… | third_party: mirkosertic/MCPLuceneServer (ST… | yes: PortugueseAnalyzer ('Analyzer for Portu… | Apache-2.0 | 10.5.2 (04/10/2026); 10.5.1 e… | stable | Motor lexical em português (stemmer RSLP), mas é biblioteca Java: precisa de embrulho. Cabe dentro de um MCP do banco no disco de cada máquina; sozinha não é s… |
| s6/lucene.net.json | Apache Lucene.NET | yes: biblioteca .NET que roda em Windows; bu… | no: a biblioteca não traz servidor MCP; não … | yes: PortugueseAnalyzer (stopwords em portug… | Apache-2.0 | 4.8.0-beta00018 (2026-06-22, … | beta (4.8, 'still i… | Biblioteca de palavra-chave dentro de um MCP do banco escrito em .NET, no disco de cada máquina. Bom analisador de português; impedimento: nada pronto (sem MCP… |
| s6/apache-solr.json | Apache Solr (apache/solr) | yes: 'Solr is tested on several versions of … | yes (projeto Apache, incubando): apache/solr… | yes: quatro stemmers de português (Snowball,… | Apache-2.0 | 9.11.0 (04/10/2026); 10.0.0 (… | stable | Serviço de busca com português nativo, Windows e MCP Apache próprio, mas pesado: JVM 21 e o MCP exige Java 25 e Docker, vetado no Windows nativo. Cabe como ser… |
| s6/apache-tika.json | Apache Tika | yes (inferido, JVM): projeto Java 17 com wra… | nao_aplicavel | parcial: existe o módulo tika-langdetect (de… | Apache-2.0 | 4.1.0 (2026-09-26 no Maven Ce… | stable | Extrair texto de PDF/Office de anexos antes de ir ao banco, como tika-server local ou jar em cada Windows. Para notas já em Markdown é desnecessário; exige Jav… |
| s6/bleve.json | Bleve (blevesearch/bleve) | yes: CI 'Tests' roda em ubuntu-latest, macos… | no: biblioteca Go e CLI; sem MCP na fonte. | yes: analisador pt pré-pronto (lowercase + s… | Apache-2.0 | v2.6.1 (2026-08-24) | stable | Biblioteca de índice dentro de um MCP do banco escrito em Go, no disco de cada máquina, com pt e híbrido BM25+vetor. Impedimento: sem MCP nem Markdown prontos;… |
| s6/chroma.json | Chroma (chroma-core/chroma) | yes (indício): workflow _python-tests.yml te… | third_party: chroma-core/chroma-mcp, README … | Sem analisador de português. Busca de texto … | Apache-2.0 | 1.5.9 (05 de maio; ano não ex… | stable | Cabe como disco de cada máquina (modo persistente) ou serviço na rede (chroma run), com chroma-mcp de terceiros. Limites: busca lexical só substring/regex, sem… |
| s3/ck.json | ck | yes: releases com ck-0.8.1-x86_64-pc-windows… | yes: 'ck --serve', stdio; ferramentas semant… | Modelos FastEmbed: bge-small (padrão), mxbai… | MIT OR Apache-2.0 | 2026-10-11, 0.8.1 | beta (versão 0.x, r… | Disco de cada máquina, MCP stdio com binário único, bom no Windows. Impedimentos: otimizado para código, modelos provavelmente só em inglês, sem endpoint de em… |
| s3/couchdb-clouseau-dreyfus.json | CouchDB Clouseau/Dreyfus | nao_verificado (docs do CouchDB e README do … | no (recurso do CouchDB acessado por HTTP _se… | yes: analisador 'portuguese' (org.apache.luc… | Apache-2.0 (clousea… | nao_verificado (seção Release… | stable no CouchDB (… | Dentro do banco em cada máquina, sem cópia em disco; lexical PT bom. Impedimento: JVM 21 + Clouseau ao lado do CouchDB no Windows nativo sem confirmação; sem s… |
| s3/couchdb-nouveau.json | CouchDB Nouveau | nao_verificado: a documentação não menciona … | no (recurso do CouchDB; MCP teria de ser esc… | Sim: analisadores por idioma incluem portugu… | nao_verificado nas … | nao_verificado | alpha/experimental:… | Dentro do CouchDB de cada máquina, sem copiar notas. Impedimentos: experimental, JVM extra, notas do LiveSync são chunks (não texto do arquivo), sem semântica … |
| s6/obsidian-dataview.json | Dataview (blacksmithgu/obsidian-datavie… | yes: plugin do Obsidian em JS, manifest com … | nao_aplicavel | nao_aplicavel | MIT | 2025-04-07, 0.5.70 | stable (sem release… | Consulta de frontmatter dentro do Obsidian de cada máquina, sobre a pasta que o LiveSync mantém. Não serve aos agentes via MCP, pois precisa do Obsidian aberto… |
| s3/devrag.json | devrag | yes (binário devrag-windows-x64 no release; … | yes: servidor próprio, stdio (tools search, … | Modelo multilingual-e5-small (ONNX, 384 dim)… | MIT (declarado no R… | v1.4.4, 2026-04-15 | beta (v1.x, 1 mante… | Disco de cada máquina, binário simples no Windows. Impedimentos: reindexa só no boot, sem keyword nem frontmatter, sem endpoint de embeddings. |
| s6/docling.json | Docling (docling-project/docling, antes… | yes: README diz funcionar em Windows, x86_64… | nao_aplicavel | nao_verificado: README cita OCR extenso para… | MIT (código; modelo… | 2026-10-12, v2.138.0 | stable | Extrai PDF, DOCX, PPTX, XLSX e HTML para Markdown no disco de cada máquina, ou via docling-mcp-server (uvx) ao lado do MCP do banco. Fora de CouchDB e LiveSync… |
| s6/elasticsearch.json | elastic/elasticsearch | yes: zip nativo para Windows, com OpenJDK em… | yes (oficial da Elastic): Agent Builder MCP … | yes: analisador `portuguese` com stopwords _… | Tripla: AGPLv3 only… | v9.5.5 (2026-10-06) | stable | Serviço de busca pesado (JVM) na rede ou no disco de uma máquina; português nativo e MCP oficial. Impedimento: peso do runtime e licença AGPL/SSPL/ELv2, exager… |
| s6/elasticlunr-js.json | elasticlunr.js (weixsong) | nao_verificado: é JavaScript (browser/Node),… | no: README não menciona MCP; seria bibliotec… | Padrão inglês (120 stopwords); outros idioma… | MIT | Nenhum release publicado (Git… | beta | Cópia leve no cliente ou dentro de um MCP em Node, para índice pequeno. Impedimentos: autor busca mantenedor, português não nativo, sem releases, sem leitura d… |
| s6/faiss.json | facebookresearch/faiss | yes: faiss-cpu tem wheels win_amd64 no PyPI … | no (biblioteca; MCP de terceiros nao_verific… | nao_aplicavel como texto: só vetores; o idio… | MIT | v1.15.1 (2026-09-16, PyPI fai… | stable | Índice vetorial em disco de cada máquina, dentro do MCP do banco, com vetores do FreeLLMAPI. Impedimento: não faz BM25 nem texto; precisa de outra peça para a … |
| s3/fastembed.json | FastEmbed | yes: CI python-tests.yml roda matriz com win… | no (a biblioteca não tem MCP). third_party o… | Modelo padrão BAAI/bge-small-en-v1.5 (inglês… | Apache-2.0 | v0.9.0 (2026-10-07) | stable (0.x, ativo) | Cópia leve no disco de cada máquina, ou dentro do MCP do banco, para embeddings locais multilíngues (e5) sem rede. Impedimento: modelo padrão é inglês; exige e… |
| s3/fastmcp-proxy-mount.json | FastMCP proxy/mount | nao_verificado (a doc não traz notas de Wind… | yes (biblioteca Python: create_proxy() e ser… | nao_aplicavel | Apache-2.0 | 4.1.0 (PyPI, 2026-10-08) | stable (4.x) | Dentro do MCP do banco: montar o servidor de busca com mount() ou prefixar tools de backends. Exige código Python; não é serviço pronto. |
| s6/gray-matter.json | gray-matter (jonschlinkert/gray-matter) | yes (inferido): biblioteca JavaScript pura, … | nao_aplicavel | nao_verificado: lida com texto UTF-8 via js-… | MIT | 2019-01-11, 4.0.2 (tag); pack… | stable (madura, man… | Parser de frontmatter para um MCP ou script em Node que leia as notas do Obsidian. Conversa com o MCP e o LiveSync só pelos arquivos. Impedimento: depende do j… |
| s3/grepai.json | grepai | yes: instalador PowerShell (install.ps1), bu… | yes: 'grepai mcp-serve', stdio | Depende do modelo de embeddings: padrão nomi… | MIT | 2026-09-10, v0.37.0 | beta (versão 0.x at… | Disco de cada máquina com watcher e MCP stdio, embeddings pelo FreeLLMAPI via endpoint openai. Impedimentos: feito para código (sem título/frontmatter), depend… |
| s6/haystack.json | Haystack (deepset-ai/haystack) | yes: wheel pura Python (py3-none-any, 'Opera… | third_party: Hayhooks (deepset-ai/hayhooks, … | nao_verificado: depende dos componentes esco… | Apache-2.0 | 3.3.0, 2026-10-01 (PyPI) | stable | Orquestrador de RAG que poderia montar a indexação sobre o banco e servir via Hayhooks/MCP. Impedimento: framework grande demais e o hub já decidiu CouchDB, Li… |
| s6/hnswlib.json | hnswlib (nmslib/hnswlib) | yes: o CI roda `pip install .` em windows-la… | no: biblioteca de índice, sem MCP; MCP de te… | nao_aplicavel: só vetores; o idioma vem do m… | Apache-2.0 | v0.9.0 (2026-03-28); README j… | beta | Índice vetorial em memória dentro do MCP do banco, por máquina, reconstruível dos pedaços no CouchDB. Impedimento: só vetores, sem texto, metadados nem busca l… |
| s6/transformers.json | Hugging Face Transformers | yes: doc de instalação cita "On Windows, the… | nao_aplicavel | depende do modelo: carrega qualquer modelo d… | Apache-2.0 | 5.19.0 (2026-10-06) | stable (PyPI: Devel… | Rodar embeddings/rerank multilíngues localmente em Python, fora do FreeLLMAPI. Pesado (PyTorch) para duas máquinas Windows; não fala com CouchDB, LiveSync ou M… |
| s3/kb-index.json | kb-index | yes (por documentação, sem CI): README diz "… | yes: servidor próprio kb-index-mcp; stdio ou… | Sem stemmer/stopwords de português. BM25 via… | MIT | nenhum release/tag publicado;… | beta (classifier "D… | Cópia leve no disco de cada máquina: index.db construído por script e servido por MCP local. Impedimentos: indexador agendado (sem watcher), sem português ling… |
| s3/lancedb.json | LanceDB | yes (wheel win_amd64 no PyPI; CI não verific… | no (sem MCP oficial na página; MCP de tercei… | FTS nativo com stem, stopwords e ascii_foldi… | Apache-2.0 | 0.40.0 (PyPI 2026-10-07); pré… | stable (0.x, releas… | Dentro do MCP do banco, em disco local de cada máquina, com FTS nativo + vetor. Impedimento: formato de dados próprio (pasta Lance) e sem base_url de embedding… |
| s6/llamaindex.json | LlamaIndex (run-llama/llama_index) | yes: wheel py3-none-any (llama-index-core 0.… | third_party: o repositório traz só o cliente… | parcial: MarkdownNodeParser não depende de i… | MIT | v0.14.25 (2026-09-21) | stable | Cola de RAG em Python (corte por título, embeddings pelo FreeLLMAPI, reranking) como biblioteca no serviço de busca. Impedimento: não é servidor nem lê CouchDB… |
| s3/local-notes-search-mcp.json | local-notes-search-mcp | yes (medido pelo autor, sem CI Windows): REA… | yes: servidor próprio, stdio (ferramentas in… | Embeddings multilíngues por padrão: sentence… | MIT | nenhum release/tag publicado | beta/novo (sem rele… | Cópia leve no disco de cada máquina, via stdio. Impedimentos: escritor único SQLite, indexação manual, só vetorial e sem endpoint de embeddings; chunk por linh… |
| s6/localai.json | LocalAI (mudler/LocalAI, antigo go-skyn… | only_wsl_or_docker: o README só traz Quickst… | third_party: LocalAI é cliente MCP (conecta … | nao_aplicavel | MIT | 2026-10-02, v4.11.0 | stable (releases fr… | Seria um segundo gateway OpenAI-compatível de embeddings local, redundante com o FreeLLMAPI. Impedimento: sem binário Windows; exige Docker ou WSL, vetados no … |
| s3/localvectorsearchmcp.json | LocalVectorSearchMcp | yes: CI com matriz ubuntu-latest, windows-la… | yes: servidor próprio, stdio, 18 ferramentas… | Sem stemmer de português; léxico por SQLite … | MIT (página do paco… | v0.1.3, 2026-10-11 (NuGet 0.1… | alpha/beta inicial … | Disco de cada máquina: um servidor stdio por pasta, com watcher e BM25 + vetor via FreeLLMAPI. Impedimentos: .NET 10, 0.1.x recente, um índice por projeto, sem… |
| s6/lunr-js.json | Lunr.js (olivernn/lunr.js) | yes: JavaScript puro, roda em Node ou navega… | no | yes via terceiro: README do lunr diz 'Full t… | MIT | 2.3.9, 2020-08-19 (npm) | stable porém sem ma… | Cópia leve no cliente, ou dentro do MCP do banco em Node, para busca léxica pequena. Impedimento: sem atualização incremental, índice todo em memória e projeto… |
| s3/manticore-search.json | Manticore Search | yes parcial: instalador com binários nativos… | nao_verificado: README e manual não citam MC… | morphology com stem_en/stem_enru e libstemme… | GPLv3 ou posterior | 29.9.0 (data nao_verificado) | stable | Serviço na rede possível; híbrido BM25+vetor com API_URL para o FreeLLMAPI. Impedimentos: Docker para o Buddy no Windows, sem MCP e sem indexação de Markdown. |
| s3/markdown-vault-mcp.json | markdown-vault-mcp | nao_verificado (CI só ubuntu-latest; pyproje… | yes: próprio, stdio (`markdown-vault-mcp ser… | Sem stemmer/stopwords documentados (FTS5 SQL… | MIT | v5.1.0, 7 out 2026 | stable (v5, ativo, … | Serviço/MCP por máquina sobre a pasta, com busca híbrida, filtros de frontmatter e escrita. Impedimentos: Windows nativo não confirmado, escrita concorrente co… |
| s6/whoosh.json | mchaput/whoosh | yes (inferido): biblioteca Pure-Python; sem … | no (MCP de terceiros nao_verificado) | parcial: stemmers Porter, Porter2, Paice Hus… | BSD de duas cláusul… | 2.7.4 (2016-04-04, PyPI) | sem manutenção na p… | Índice BM25 em disco de cada máquina, dentro de um MCP do banco em Python. Impedimento: sem manutenção, sem stemmer de português e sem Markdown. |
| s3/meilisearch.json | Meilisearch | yes: binário meilisearch-windows-amd64.exe n… | yes: MCP embutido no servidor, POST /mcp, tr… | Tokenizador Charabia lista Portuguese no gru… | MIT (Community Edit… | v1.55.0 (2026-10-12) | stable (MCP embutid… | Serviço local em cada máquina (processo Windows), alimentado pelo MCP do banco; ou serviço na rede. Impedimento: ingestão de Markdown/frontmatter é por conta p… |
| s3/memtomem.json | memtomem | yes: CI com windows-latest (test-windows-sha… | yes: servidor próprio memtomem-server, stdio… | Embeddings ONNX multilingual-e5-small (padrã… | Apache-2.0 (CLA exi… | 2026-10-08, v0.6.8 | alpha (README: Alph… | Serviço no disco de cada máquina apontando para a pasta de notas; MCP stdio pronto e embeddings pelo FreeLLMAPI via base_url. Impedimentos: alpha, pt sem token… |
| s6/milvus.json | Milvus (milvus-io/milvus; inclui Milvus… | only_wsl_or_docker (servidor): docs listam W… | third_party: zilliztech/mcp-server-milvus (A… | Sem analisador de português embutido: embuti… | Apache-2.0 | milvus-3.0.2 (20/09/2026, Lat… | stable | Só o Milvus Lite caberia, como índice embarcado em Python no disco de cada máquina; o servidor exige Docker/WSL2, vetado. Sem frontmatter, sem português nativo… |
| s3/miyo.json | Miyo | yes: 'macOS, Windows, or Linux' (app de band… | yes: stdio ('miyo also exposes a stdio MCP s… | parcial: site diz 'Search by meaning across … | nao_verificado (app… | v0.3.2 (data não mostrada) | alpha/beta (v0.3.x,… | Disco de cada máquina, MCP stdio local. Impedimento: aparente código fechado e pré-1.0; modelo de embeddings e endpoint configurável não verificados; Relay é p… |
| s6/modelcontextprotocol-python-sdk.json | modelcontextprotocol/python-sdk | yes: o CI roda em matriz ubuntu-latest e win… | yes: SDK para servidores e clientes MCP; tra… | nao_aplicavel | MIT (LICENSE e READ… | v2.3.0, 2026-10-02 | stable (linha v2, c… | Base para escrever o MCP do banco em Python, ligando o CouchDB (por HTTP) e o FreeLLMAPI; roda nativo no Windows. Impedimento: a v2 mudou a API e exige Python … |
| s6/modelcontextprotocol-servers.json | modelcontextprotocol/servers | yes: o CI tem job test-windows em windows-la… | yes: coleção de servidores MCP de referência… | nao_aplicavel | Transição MIT para … | v1.0.0, 2026-10-11 (pacotes s… | stable no versionam… | Exemplos e ponto de partida para o MCP do banco (Filesystem e Memory como modelos). Não serve de produção, precisa de cmd /c no Windows e não conhece o CouchDB. |
| s6/modelcontextprotocol-typescript-sdk.json | modelcontextprotocol/typescript-sdk | nao_verificado: o CI da main usa só ubuntu-l… | yes: SDK para servidores e clientes MCP, com… | nao_aplicavel | Apache-2.0 para con… | v2.3.1, 2026-10-05 (v1.32.1 t… | stable (v2 'the sta… | Alternativa em Node para o MCP do banco, no mesmo runtime JS do PouchDB/nano falando com o CouchDB. Impedimento: sem CI Windows comprovado; v2 recente, com mig… |
| s6/n8n.json | n8n (n8n-io/n8n) | nao_verificado: o README só mostra Docker no… | nao_aplicavel | nao_aplicavel | Sustainable Use Lic… | n8n@2.44.0, publicado em 2026… | stable (versão 2.x,… | Orquestrador visual de fluxos entre CouchDB, MCP e FreeLLMAPI por webhooks e agendas. Impedimento: início rápido pede Docker, que o hub não tem; a licença limi… |
| s6/gpt4all.json | nomic-ai/gpt4all | yes: instalador gpt4all-installer-win64.exe … | nao_aplicavel | nao_verificado: README e docs nao afirmam su… | MIT | 2025-02-24, v3.10.0 (ordem do… | stable (sem release… | App de chat com LocalDocs sobre pastas; nao entra no pipeline do hub alem de runtime local de LLM. Impedimentos: servidor so em localhost, sem endpoint de embe… |
| s3/obsidian-local-rest-api-mcp.json | Obsidian Local REST API (+MCP) | yes, indireto: plugin do Obsidian; sem prova… | yes: 'The plugin includes a built-in MCP ser… | nao_verificado (sem menção a stemmer/acentos) | MIT | 5.4.0 (6 out, 2026 provável) | stable (v5.x) | Lado do Obsidian em cada máquina, MCP pronto. Impedimento: exige Obsidian aberto; busca lexical simples, sem semântica; sandboxes sem tailnet não alcançam. |
| s6/obsidian-api.json | obsidian-api (obsidianmd/obsidian-api) | yes: pacote de tipos (obsidian.d.ts), indepe… | nao_aplicavel | nao_aplicavel | MIT | nao_verificado (package.json … | stable (mantido pel… | Base para escrever um plugin Obsidian próprio, lendo o MetadataCache em cada máquina. Fala com o Obsidian, não com CouchDB nem MCP. Impedimento: exige o Obsidi… |
| s3/obsidian-brain.json | obsidian-brain | yes (Node 20+; docs citam binários prebuilt … | yes: servidor próprio, stdio, 18 tools (incl… | EMBEDDING_PRESET=multilingual (Xenova/multil… | Apache-2.0 | v1.7.24, 2026-05-16 | stable (v1.7.x, sem… | Disco de cada máquina, como MCP stdio. Impedimento: embeddings só locais/Ollama (sem gateway OpenAI), escreve na pasta (risco com LiveSync), docs focadas em ma… |
| s3/obsidian-hybrid-search.json | obsidian-hybrid-search | yes | yes: próprio, stdio (via npx) e HTTP statele… | Modelo padrão Xenova/multilingual-e5-small (… | MIT | v0.16.2, 12 out (sem ano na p… | beta (0.x, muito at… | Disco de cada máquina, MCP stdio ou HTTP local sobre o vault. Melhor aderência à régua. Impedimentos: banco SQLite dentro do vault (excluir do LiveSync), portu… |
| s3/obsidian-semantic-mcp.json | obsidian-semantic-mcp | yes (Node >=24 via npx; README documenta Win… | yes: servidor próprio, stdio (tools index_st… | Embeddings padrão bge-m3 via Ollama (multilí… | MIT | v0.3.1, 2026-08-06 (early pre… | alpha/beta (README:… | Disco de cada máquina: lê a pasta de notas, índice SQLite descartável. Impedimento: exige Ollama local (sem base_url OpenAI) e Node 24; somente leitura. |
| s6/ollama.json | ollama/ollama | yes: 'Ollama runs as a native Windows applic… | nao_aplicavel | nao_verificado: depende do modelo de embeddi… | MIT | 2026-10-14, v0.40.4 | stable | Alternativa local ao FreeLLMAPI para gerar embeddings e LLM, com base_url OpenAI-compativel; servico local em cada maquina. Impedimento: duplica o gateway ja d… |
| s3/omnisearch.json | Omnisearch | yes, indireto: plugin do Obsidian (que roda … | third_party: obsidian-mcp-server (cyanheads)… | nao_verificado (README só trata chinês; nada… | GPL-3 | 1.31.0 (5 set, ano não mostra… | stable (Gems of the… | Lado do Obsidian em cada máquina, via HTTP local opt-in. Impedimento: exige Obsidian aberto; agentes headless e sandboxes ficam sem; PT sem confirmação. |
| s6/onnxruntime.json | ONNX Runtime (microsoft/onnxruntime) | yes: wheels win_amd64 no PyPI (onnxruntime-1… | nao_aplicavel | nao_aplicavel: é só o runtime; português dep… | MIT | v1.31.0 (2026-10-09) | stable (PyPI: Devel… | Motor local de inferência para embeddings/rerank em ONNX em cada máquina Windows, plano B ao FreeLLMAPI. Não fala com CouchDB nem MCP; precisa de wrapper (Pyth… |
| s3/opensearch.json | OpenSearch | yes (zip nativo com JDK embutido; Windows Se… | yes: opensearch-mcp-server-py (org opensearc… | analisadores nativos 'portuguese' e 'brazili… | Apache-2.0 | 3.9.0 (2026-09-29) | stable | Serviço de rede só se o hub precisar de escala; para duas máquinas é excessivo (JVM, cluster, indexador externo para o LiveSync). Impedimento: peso e ausência … |
| s3/orama.json | Orama | yes (biblioteca JS/TS em Node, navegador, De… | nao_verificado: sem servidor MCP próprio ach… | yes: @orama/stemmers inclui Portuguese (31 i… | Apache-2.0 | 3.1.18 (2025-12-19) | stable | Cópia leve no cliente/sandbox: índice serializado carregado no navegador ou Node sem tailnet. Impedimentos: sem MCP, sem watcher, índice em RAM, precisa de ger… |
| s6/ort.json | ort (pykeio/ort) | nao_verificado: a matriz de plataformas é um… | nao_aplicavel | nao_aplicavel: binding do runtime; português… | MIT OR Apache-2.0 | 2.0.0-rc.14 (2026-10-12, crat… | beta (série 2.0.0-r… | Embeddings/rerank locais dentro de um serviço ou MCP escrito em Rust, sem Python. Só vale se o MCP do banco for Rust; ainda release candidate e Windows não con… |
| s3/pagefind.json | Pagefind | yes (binários x86_64 e aarch64 pc-windows-ms… | nao_verificado: sem MCP achado; não é servid… | yes: stemming para Portuguese (pt, também pt… | MIT | v1.5.2 (2026-04-12) | stable | Cópia leve no cliente/sandbox: bundle estático gerado a partir das notas, servido sem tailnet. Impedimentos: sem busca semântica, sem MCP, regeneração total e … |
| s6/pandoc.json | pandoc | yes: instalador msi, zip, choco e winget, bi… | nao_aplicavel | nao_verificado: conversor de formatos, sem b… | GPL-2.0 (README: GP… | 2026-10-08, 3.12.1 | stable | Importador de docx/html/epub para Markdown, rodando como CLI em cada máquina Windows ou chamado pelo MCP do banco. Não fala com CouchDB, LiveSync nem FreeLLMAP… |
| s6/lingua-py.json | pemistahl/lingua-py | yes: wheels win_amd64 e win_arm64 no PyPI (2… | nao_aplicavel | yes: detecta 75 idiomas, incluindo Portugues… | Apache-2.0 | 2026-03-09, Lingua 2.2.0 | stable | Detecta pt ou en de cada nota antes de indexar, para escolher analisador e stopwords; biblioteca dentro do MCP do banco em cada maquina. Impedimento: acuracia … |
| s6/pg-bigm.json | pg_bigm | nao_verificado: docs testam só Linux e Mac O… | no: extensão de PostgreSQL; sem MCP. | Bigrama independe de idioma: 'supports all P… | PostgreSQL License | v1.2-20250903 (2025-09-02) | stable | Só serviria dentro de um banco PostgreSQL com o texto das notas. O hub usa CouchDB e Windows nativo sem Docker, então não encaixa; impedimento: exige PostgreSQ… |
| s6/pgvector.json | pgvector (pgvector/pgvector) | yes: compila com nmake/MSVC e instala em Pos… | no: extensão de banco, sem MCP; MCP de terce… | nao_aplicavel como busca de texto (só vetore… | PostgreSQL License … | v0.8.7 (2026-10-01) | stable | Só serviria se o hub ganhasse um PostgreSQL por máquina, em paralelo ao CouchDB. Impedimento: segundo banco, sem WSL/Docker, fora do LiveSync; vetores separado… |
| s6/pouchdb.json | pouchdb/pouchdb (Apache PouchDB) | nao_verificado: o CI roda só em ubuntu-lates… | nao_aplicavel | nao_aplicavel | Apache-2.0 (package… | 9.0.0, 2024-06-21 (npm latest… | stable, com release… | Cliente JS que replica com o CouchDB de cada máquina, útil para cópia leve de leitura e para um MCP em Node. Não substitui o LiveSync nem seus pedaços cifrados… |
| s6/pyserini.json | Pyserini | nao_verificado: o guia de instalação cobre s… | yes: servidor MCP próprio (python -m pyserin… | nao_verificado: aceita --language/set_langua… | Apache-2.0 | pyserini-2.4.0 (2026-08-27) | stable (projeto de … | Serviço de busca de pesquisa, não do hub: Java 21, PyTorch e sem Windows nativo documentado. Só como bancada de comparação BM25/denso em outro lugar. |
| s6/python-frontmatter.json | python-frontmatter (eyeseast/python-fro… | yes (inferido): Python puro (>=3.10) com dep… | nao_aplicavel | nao_verificado: o README não fala de idiomas… | MIT | 2026-05-20, v1.3.0 (Now using… | stable (PyPI: Devel… | Leitura e escrita de frontmatter das notas num script ou MCP em Python, conversando com o Obsidian pelos arquivos. Impedimento: usa PyYAML por baixo; regravar … |
| s6/pyyaml.json | PyYAML (yaml/pyyaml) | yes: o PyPI do 6.0.3 traz wheels win_amd64 e… | nao_aplicavel | nao_verificado: biblioteca YAML geral; o REA… | MIT (não confirmado… | 2025-09-25, 6.0.3 | stable (CHANGES já … | Base de YAML sob o python-frontmatter e qualquer script Python que leia o frontmatter das notas. Sem conversa direta com CouchDB ou LiveSync. Impedimento: usar… |
| s3/qdrant.json | Qdrant | yes: asset qdrant-x86_64-pc-windows-msvc.zip… | yes (oficial Qdrant, repositório separado qd… | Vetorial: depende do modelo de embeddings. Í… | Apache-2.0 | v1.19.2 (2026-10-05) | stable | Serviço local em cada máquina Windows (binário) ou na rede, com vetores gerados pelo MCP do banco; MCP oficial é um 'memory' simples. Impedimento: mais um serv… |
| s3/qmd.json | qmd | nao_verificado: README só menciona Windows n… | yes: 'qmd mcp', stdio por padrão; 'qmd mcp -… | BM25 com tokenizador FTS5 'porter unicode61'… | MIT | 2026-08-16, v2.8.3 | stable (versão 2.x,… | Disco de cada máquina via MCP stdio, ou serviço HTTP na rede. Impedimentos: Windows não verificado (CI sem Windows), sem endpoint OpenAI para embeddings, reind… |
| s6/ripgrep.json | ripgrep | yes: binários pré-compilados para Windows (z… | no: o README não menciona MCP; seria preciso… | Unicode sempre ligado, sem stemmer, sem stop… | MIT ou Unlicense (d… | 15.2.0 (2026-07-15) | stable | Grep no disco de cada máquina Windows, sobre a pasta de notas; serve a agentes que precisam de busca literal/regex. Impedimento: sem MCP próprio, sem semântica… |
| s6/ripgrep-all.json | ripgrep-all (rga) | yes: binario msvc na release v0.10.9 (o v0.1… | no: nao ha MCP na fonte (README/repositorio)… | nao_aplicavel como indexador: e grep regex s… | AGPL-3.0-or-later (… | 2025-11-09, v0.10.10 | stable (0.x, ativo) | Disco de cada maquina: grep em PDF/DOCX/anexos fora do banco, sem indice nem MCP. Impedimento: roda sobre arquivos, nao sobre o CouchDB cifrado em pedacos do L… |
| s6/rusqlite.json | rusqlite | yes: feature bundled compila o SQLite junto;… | nao_aplicavel | nao_aplicavel | MIT | v0.40.2, 08 Aug (ano não exib… | stable | Binding para escrever em Rust um MCP/indexador sobre SQLite em cada máquina; features loadable_extension, vtab, load_extension. Impedimento: exige toolchain Ru… |
| s6/sentence-transformers.json | Sentence Transformers (UKPLab/sentence-… | yes: wheel pura Python (py3-none-any) no PyP… | no | yes: 'pretrained models for more than 100 la… | Apache-2.0 | 6.1.0, 2026-09-18 (PyPI) | stable | Gerar embeddings multilíngues e rerank localmente em cada máquina, como alternativa ao FreeLLMAPI, atrás do MCP do banco. Impedimento: PyTorch pesado no Window… |
| s6/snowball.json | Snowball (snowballstem/snowball) | yes, com ressalva: compilador em C99, build … | no: não é serviço; sem MCP. | yes: algoritmo de stemming português, 'aims … | BSD (site: 'Copyrig… | v3.1.1 (2026-06-03, feed); NE… | stable | Peça de normalização (radical em português) dentro do analisador de um índice de palavra-chave; não é motor sozinho. Impedimento: precisa de wrapper na linguag… |
| s6/spacy.json | spaCy (explosion/spaCy) | yes: README lista Windows (Cygwin, MinGW, Vi… | nao_aplicavel | yes: modulo lang/pt com stop words; modelos … | MIT | 2026-08-24, release-v3.8.16 | stable | Pre-processamento PT opcional (tokenizar, lematizar, entidades) antes de indexar. Fala com MCP/CouchDB so por script externo; nao com FreeLLMAPI. Impedimento: … |
| s3/sparfenyuk-mcp-proxy.json | sparfenyuk/mcp-proxy | nao_verificado (README e classifiers PyPI li… | yes (é proxy MCP; stdio->SSE/StreamableHTTP … | nao_aplicavel (não indexa conteúdo) | MIT | v0.13.0 (feed de releases atu… | beta (versão 0.x, a… | Serviço ou processo ao lado do MCP do banco, convertendo stdio<->HTTP para clientes sem stdio. Impedimento: Windows não declarado nem testado em CI. |
| s6/sqlite.json | SQLite | yes: binários nativos x64 oficiais (DLL e fe… | nao_aplicavel | nao_aplicavel | nao_verificado na p… | 3.54.0 (data não exibida na p… | stable | Índice derivado local (FTS/vetores via extensão carregável .dll) em cada máquina, ao lado do CouchDB, sem Docker. Impedimento: não replica; é só índice reconst… |
| s3/sqlite-fts5-sqlite-vec.json | SQLite FTS5 + sqlite-vec | yes | no (nenhum MCP próprio; o MCP seria do hub) | FTS5: unicode61 com remove_diacritics (padrã… | sqlite-vec: Apache-… | v0.1.9 estável (PyPI 2026-03-… | beta (README: pre-v… | Cópia leve dentro do MCP do banco ou no disco de cada máquina: um .db único com BM25 + vetores. Impedimento: pré-v1, sem stemmer de português, reconciliação co… |
| s6/stopwords-pt.json | stopwords-iso/stopwords-pt | yes: sao dados (stopwords-pt.json e .txt), s… | nao_aplicavel | yes: lista de stopwords em portugues, em JSO… | MIT | 2016-10-10, v0.3.0 | stable (dado estati… | Lista de stopwords em pt para o filtro de busca lexical (FTS/BM25) sobre as notas; carregada pelo codigo do MCP do banco. Impedimento: lista de 2016, so portug… |
| s6/surrealdb.json | SurrealDB | yes: instalação nativa por script PowerShell… | yes: servidor MCP citado no README ('MCP (Mo… | nao_verificado | BSL 1.1 no motor; S… | v3.3.0, 28 Sep (ano não exibi… | stable | Alternativa ao CouchDB como banco único (FTS, vetor, grafo, MCP) por máquina. Impedimento: abandona a replicação mestre-mestre do CouchDB/LiveSync, que não é e… |
| s3/tantivy-tantivy-py.json | Tantivy / tantivy-py | yes (README do tantivy: Linux, macOS e Windo… | no | Stemmer de português (enum Language inclui P… | MIT (tantivy e tant… | tantivy 0.26.2 (feed 2026-09-… | stable (0.x, ativo) | Dentro do MCP do banco como motor lexical rápido com stemmer de português; o lado vetorial precisa de outra peça. Impedimento: sem vetores e sem reconciliação … |
| s3/tantivy.json | Tantivy / tantivy-py | yes (README: supports Linux, macOS, and Wind… | no (biblioteca de busca) | Stemmer Portuguese existe no enum Language (… | MIT | tantivy 0.26.2 (crates.io, 20… | stable (versão 0.x) | Componente lexical embutido no MCP do banco, em cada máquina; BM25 com stemmer PT. Impedimento: sem vetores nem ingestão; cobre só metade da busca híbrida. |
| s3/tbxark-mcp-proxy.json | TBXark/mcp-proxy | yes (binário windows_amd64 nos releases; go … | yes (agrega vários servidores MCP; entrada S… | nao_aplicavel | MIT | v1.1.0 (feed de releases atua… | stable (v1.x) | Serviço na rede ou no disco de cada máquina agregando o MCP do banco e outros num único endpoint HTTP. Impedimento: lançar servidores stdio via npx/uvx exige N… |
| s6/templater.json | Templater (SilentVoid13/Templater, plug… | nao_verificado: é plugin do Obsidian (JavaSc… | nao_aplicavel | nao_aplicavel | AGPL-3.0 (README: '… | 2.26.0, 11 Oct (página de rel… | stable | Gera notas com frontmatter padronizado dentro do Obsidian, no disco de cada máquina; agentes via MCP não o usam. Impedimento: executa JavaScript e comandos de … |
| s6/the-silver-searcher.json | The Silver Searcher (ag) | yes, nao oficial: README lista builds diario… | no: sem MCP na fonte; e um CLI | nenhum: grep regex PCRE; sem stemmer, stopwo… | Apache-2.0 | 2.2.0 (tag de 2018-08-07; sem… | stable, mas sem man… | Cliente leve ou disco de cada maquina: grep rapido em pasta de notas. Impedimentos: sem manutencao desde 2020, sem indice nem MCP, sem Windows oficial; ripgrep… |
| s6/the-platinum-searcher.json | the_platinum_searcher | yes: README diz que oferece binários para ma… | no: CLI sem MCP no README. | Lê UTF-8, EUC-JP e Shift_JIS; sem stemmer, s… | MIT | v2.2.0 (2018-09-05) | archived | Grep no disco de cada máquina, redundante com ripgrep. Impedimento: parado desde 2018, sem MCP, sem UTF-16 comprovado; ripgrep cobre o mesmo lugar melhor. |
| s3/txtai.json | txtai | nao_verificado (instalação tem seção Windows… | yes (a API hospeda endpoints MCP e OpenAI-co… | Depende do modelo: o recomendado é all-MiniL… | Apache-2.0 | v9.14.0 (PyPI 2026-10-06) | stable | Serviço na rede ou processo local que expõe MCP próprio e embeddings via gateway. Impedimento: ambiente Python pesado e Windows nativo não confirmado. |
| s3/typesense.json | Typesense | only_wsl_or_docker: docs de instalação cobre… | third_party: avarant/typesense-mcp-server (P… | Campo locale (padrão inglês); stem:true usa … | GPL-3.0 | Version 30.2 (feed de release… | stable | Serviço de rede em Linux/Docker; não roda nas máquinas Windows nativas. Só serviria em outra máquina; impedimento: sem Windows nativo, índice em RAM. |
| s3/vault-cortex.json | vault-cortex | only_wsl_or_docker (servidor roda em contêin… | yes: servidor próprio, HTTP (http://localhos… | Embeddings bge-small-en-v1.5 (inglês) e rera… | MIT | v0.54.13, 2026-10-11 | beta (0.x, muito at… | Serviço em contêiner (rede). No Windows sem Docker não serve. Impedimentos: Docker, embeddings só em inglês sem endpoint, e escreve no vault. |
| s3/vexor.json | vexor | yes | yes: servidor stdio embutido (`vexor mcp`), … | Sem stemmer/stopwords de português. Embeddin… | MIT | v0.30.0, 27 set (página de re… | beta (0.x, ativo) | Disco de cada máquina, MCP stdio local sobre a pasta; embeddings via FreeLLMAPI com provider custom. Impedimento: foco em arquivos/código, sem filtro por front… |
| s6/watchdog.json | watchdog (gorakhargosh/watchdog) | yes: usa ReadDirectoryChangesW no Windows; a… | nao_aplicavel | nao_aplicavel | Apache-2.0 (PyPI e … | 6.0.0, publicado em 2024-11-0… | stable (classifier … | Observador de arquivos em Python em cada máquina: dispara reindexação quando o LiveSync grava notas na pasta. Conversa com LiveSync e Obsidian. Impedimento: nã… |
| s6/watchman.json | Watchman (facebook/watchman) | yes: 'Windows 10 (64-bit) and up'; binário p… | nao_aplicavel | nao_aplicavel | MIT | v2026.10.12.00, publicado em … | stable (releases se… | Daemon que registra mudanças em arquivos e dispara ações por padrão de nome; serviria para reindexar a pasta de notas em cada máquina. Conversa com LiveSync e … |
| s6/weaviate.json | weaviate/weaviate | only_wsl_or_docker: "we don't offer native W… | nao_verificado (só um resumo de busca, sem l… | nao_verificado (tokenização/idioma não confe… | BSD-3-Clause na mai… | v1.40.1 (13 Oct; ano não most… | stable | Serviço de busca na rede com BM25, híbrido e MCP próprio. Impedimento: sem Windows nativo, exige Docker/WSL, que o hub não tem. |
| s6/xapian.json | Xapian (xapian/xapian) | yes: instalável por compilação nativa; o CI … | no: é biblioteca, sem servidor MCP próprio; … | yes: stemmer Snowball de português (pt) e ou… | GPL-2.0-or-later | 2.1.0 (2026-08-13) | stable | Índice lexical em disco de cada máquina, com stemmer pt, dentro do MCP do banco. Impedimento: biblioteca C++ sem MCP nem Markdown; exige cola em código e binár… |
| s6/zoekt.json | Zoekt (sourcegraph/zoekt, fork mantido … | nao_verificado: README so documenta go insta… | no: sem MCP na fonte; expoe JSON API (-rpc, … | Sem stemmer nem stopwords; busca substring/r… | Apache-2.0 | sem releases nem tags no GitH… | stable (sem version… | Servico na rede ou disco de cada maquina, indexando pasta de notas: regex rapido. Impedimentos: foco em repositorios git, sem MCP, Windows nao documentado, ind… |
| s3/zvec-grep.json | zvec-grep | yes | yes: Streamable HTTP em http://127.0.0.1:799… | Sem stemmer documentado. Embeddings multilín… | Apache-2.0 | v0.2.0, 27 ago (sem ano na pá… | beta (v0.2.0 previe… | Disco de cada máquina via daemon e MCP HTTP local. Impedimentos: índice `.zvec-grep` dentro da pasta sincronizada pelo LiveSync (excluir), endpoint de embeddin… |

## 6. O que ficou fora, e por qual regra

Números do ticket da pesquisa ampla; os itens continuam nos arquivos de `laco/`.

| O quê | Quantos | Regra | Onde está |
|---|---|---|---|
| Só nome, citado uma vez | 1032 | decisão do Gustavo: fora da triagem | `catalogo/itens.json` |
| Quarentena (ambíguos sem decisão segura) | 193 | Tear, na limpeza | `catalogo/itens.json` |
| Repositórios inventados (README 404) | 620 | sem fonte | `etapas/cartoes/` |
| Repositórios mortos (URL 404) | 212 | sem fonte | `etapas/cartoes/` |
| Julgados sem uso para o hub | 529 | conferência Sonnet / auditoria Opus | `etapas/conferencia/respostas/` |
| Conceitos com uma citação e sem projeto | 340 | filtro da S1 | `etapas/conceitos/respostas/` |
| Duplicatas juntadas | 122 entidades | junção por nome (S1) e pelo juiz (cobertura) | `sintese/entidades2-decisoes.jsonl` |
