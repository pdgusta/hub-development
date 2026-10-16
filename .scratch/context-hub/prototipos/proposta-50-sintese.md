# Pesquisa ampla: proposta da síntese (etapa 5)

Ticket "Pesquisa ampla: lugares e mecanismos de busca". Refeita em 2026-10-13 a pedido do Gustavo ("melhore suas
propostas, estão rasas; precisam estar à altura de todo o trabalho executado até aqui"). A proposta anterior
(script + texto do maestro, ou 3 capítulos em paralelo) tratava a síntese como redação. Os dados mostram que ela
precisa ser mais que isso.

## O que os dados dizem antes de sintetizar

Números do fim da auditoria. Contagens conferidas por script em `laco/etapas/`.

1. **O catálogo é o que os modelos lembram, não o que existe hoje.** Nenhuma das candidatas que as pesquisas
   anteriores acharam aparece no catálogo: zvec-grep, memtomem, ck, markdown-vault-mcp, grooveseek, grepai, mgrep,
   SeaGOAT, vexor, qmd e basic-memory ficaram de fora. Os mais citados são os motores conhecidos até 2023/2024
   (Meilisearch 1903 menções, Qdrant, Weaviate, Typesense, FAISS, Elasticsearch, Whoosh, Milvus, Chroma). Isso bate com o
   teste de atualidade: nenhum gerador buscou na web. O ticket pede que as candidatas atuais entrem; hoje elas não
   estão.
2. **A régua do hub é quase toda "não se sabe".** Nos 287 projetos de busca, o README não diz se há MCP em 223,
   nem se roda no Windows em 241, nem se lida com português em 242. A conferência foi fiel ao README, e o README não
   responde à régua. Sem uma segunda fonte, a síntese compararia desconhecidos.
3. **Os lugares próprios do hub ficaram vazios.** Lugar × mecanismo concentra-se em "serviço na rede" e "biblioteca"
   (vetorial 85 e 65, texto completo 78 e 56). "Dentro do MCP do banco" tem **0** itens, e "cópia leve no cliente" tem
   2. Esses lugares só existem na arquitetura do hub (CouchDB + LiveSync + MCP em cada par, cliente pela tailnet,
   sandbox sem tailnet), então nenhum README os menciona. Eles precisam ser construídos por raciocínio de arquitetura,
   com as peças do catálogo encaixadas. A contagem não basta.
4. **Há duplicatas de entidade.** Elasticsearch aparece 3 vezes; Whoosh, LanceDB e Typesense, 2 vezes cada (`gh:`,
   `web:` e nome). A junção do laço era por chave, não por entidade.
5. **Os conceitos são o vocabulário de mecanismos, mas são ruidosos.** Busca híbrida (67), BM25 (26), filtro por
   frontmatter, stemming, filtro por metadados, busca vetorial, stemming em português e remoção de acentos dizem o que
   a busca precisa ter. Na amostra auditada, 12,5% eram erros graves.
6. **A comparação das metades** (só nos itens conferidos, então com viés de seleção) mostra quem acerta "útil ou
   não" contra o veredito final:
   - 1 modelo do FreeLLMAPI: 70%;
   - 2 modelos do FreeLLMAPI que concordam: 83%;
   - Haiku: 75%.

   Isso vale para o template da suite de busca: dois modelos gratuitos concordando valem mais que um Haiku sozinho.

## A síntese em cinco partes

### S1. Consolidar o catálogo (script, sem modelo, mais um juiz para os casos difíceis)

- Registro final de cada item: o do Opus quando auditado, senão o do Sonnet, senão o da triagem (marcado "sem
  conferência").
- Resolver entidades entre `gh:`, `web:` e nome (Elasticsearch ×3 vira um, com todas as URLs e menções somadas). Os
  casos ambíguos vão a 1 subagente Sonnet, no papel que o Tear fazia nas ondas.
- Conceitos: agrupar por `concept_en` e manter só os citados por 2 ou mais cartões ou ligados a um projeto do
  catálogo. Os outros ficam listados, fora da síntese.
- Saída: `laco/sintese/catalogo-final.json` e uma tabela por eixo.

### S2. Fechar a lacuna de atualidade (com busca na web, que faltou ao laço)

- Juntar as candidatas das pesquisas anteriores (tickets 19, 20, 21 e a camada de busca), com o que já foi
  verificado sobre elas.
- Varredura dirigida com busca de verdade. Subagentes Claude com WebSearch/WebFetch, disparados por um despachante
  (Osmose), em consultas estreitas que o laço não cobriu:
  - MCP de busca sobre Markdown e cofre do Obsidian;
  - busca local por agente de código (grep semântico);
  - busca dentro do CouchDB (Nouveau/Clouseau, Mango);
  - BM25 com analisador em português;
  - índices embutidos com MCP;
  - lançamentos de 2025 e 2026.
- O que sair entra no catálogo pelo mesmo caminho (cartão com README, conferência Sonnet).

### S3. Verificar a régua nos finalistas (fonte primária além do README)

- Lista curta de 30 a 40 itens: os mais citados de cada célula de lugar × mecanismo, mais as candidatas atuais.
- Para cada um, subagentes com web leem a documentação, os releases e as issues e respondem a régua do hub com
  citação:
  - Windows nativo;
  - MCP (próprio ou de terceiros);
  - português (analisador ou stemmer);
  - licença;
  - último release;
  - como indexa Markdown e frontmatter;
  - custo de memória.
- O que não for achado fica "não verificado".

### S4. Escrever a síntese de arquitetura (o maestro, Opus)

1. **Mapa de lugares × mecanismos**, preenchido com os itens verificados. Os lugares próprios do hub são desenhados a
   partir da arquitetura já decidida:
   - CouchDB em cada par;
   - MCP com `base_rev`;
   - cliente pela tailnet;
   - sandbox sem tailnet.
2. **Matriz de atendimento:** para cada lugar, quem fica atendido em cada situação (agente na máquina, cliente pela
   tailnet, sandbox sem tailnet, tailnet fora do ar), como o ticket pede.
3. **Combinações leves e robustas.** Para cada uma:
   - as peças;
   - onde cada peça mora;
   - o que já vem pronto e o que falta montar (com estimativa em dias);
   - como ela convive com o LiveSync e com a edição concorrente;
   - os riscos;
   - o que um spike precisa provar.
4. **A stack além da busca:** sync, MCP, frontmatter, extração de texto, embeddings locais e o que mais o catálogo
   trouxe, cruzado com as decisões já fechadas no mapa.
5. **Recomendação para o ticket "Camada de busca":** quais combinações vão ao spike e em que ordem. É recomendação; a
   decisão continua sendo do Gustavo, numa rodada.
6. **Aprendizados para o template "suite de busca"** do acervo do maestro:
   - geradores sem busca inventam URLs e ficam presos ao passado;
   - a comparação das metades;
   - o custo medido por etapa;
   - o teto de contexto dos despachantes;
   - o problema do Enter que fica pendente quando o recruta está ocupado.

### S5. Visual (Designer)

- A página da síntese: o mapa, a matriz, as combinações e a stack.
- O painel da usina fecha com a água potável.

## Custo e tempo (estimativas; o que for medido em piloto vem antes de cada leva)

| Parte | Quem | Tokens Claude | Medido? |
|---|---|---|---|
| S1 | script + 1 Sonnet nos ambíguos | ~0,2 milhão Sonnet | não; piloto não precisa (1 agente) |
| S2 | Osmose + ~20 subagentes com web | ~2 a 4 milhões (Sonnet ou Haiku) | não; piloto de 2 consultas antes |
| S3 | Salina + ~8 subagentes com web, 5 itens cada | ~1,5 a 2,5 milhões Sonnet | não; piloto de 5 itens antes |
| S4 | maestro | ~0,3 a 0,5 milhão Opus | não |
| S5 | Designer | ~0,2 milhão Opus | não |

Nenhuma parte com subagentes começa sem o número do piloto mostrado ao Gustavo. Os despachantes param a 40% de
contexto. O FreeLLMAPI não entra em S2 e S3, porque nenhum modelo dele busca na web (teste de atualidade).
