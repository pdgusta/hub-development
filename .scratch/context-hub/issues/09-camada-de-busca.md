# Camada de busca

Type: prototype
Status: resolved
Blocked by: 04, 19, 20, 21, 22, 23, 25, 33, 34, 50

## Question

Que camada de busca o hub usa? Spike com duas candidatas sobre uma cópia de conteúdo real, medindo a
qualidade em pt-BR, a instalação e o comportamento com o sync. O FreeLLMAPI entra como opção de
embedding (Q13). A interface do agente é um MCP que busca, grava e mostra o estado do sync (Q12).

## Comments

- 2026-10-02 (vinda de "zvec-grep na camada de busca"): o zvec-grep serve só para a leitura e é
  sugerido como candidata do spike, contra o markdown-vault-mcp, no lugar do grooveseek da exploração
  §11. A escolha das duas candidatas é decisão deste ticket.
- 2026-10-03: o Gustavo pediu para incluir `RyanCodrai/turbovec`. Virou a pesquisa "turbovec na
  camada de busca", que agora bloqueia este ticket; o resultado pode mudar as candidatas do spike.
- 2026-10-04: rodada 1 aberta, com a escolha das duas candidatas do spike. A recomendação é
  markdown-vault-mcp contra zvec-grep, com o grooveseek de reserva. Pergunta em `respostas.md`,
  página em [`prototipo-09-busca.html`](../prototipos/prototipo-09-busca.html). Fonte nova: o
  stemmer porter do SQLite FTS5 é só para inglês ([SQLite FTS5 §4.3.3](https://www.sqlite.org/fts5.html)).
- 2026-10-04, resposta à R1: o Gustavo quer, antes do spike, uma fase de busca de candidatas novas.
  Virou "Varredura de candidatas à camada de busca", que agora bloqueia este ticket. A escolha das
  duas candidatas volta depois dela; a recomendação da rodada 1 fica como ponto de partida.
- 2026-10-04: a "Varredura de candidatas à camada de busca" foi resolvida (memtomem como melhor nova,
  ck como reserva do zvec-grep). Rodada 3 aberta em `respostas.md`: as candidatas do spike.
- 2026-10-04: a R3 (três candidatas no spike) ficou suspensa. O Gustavo reabriu a premissa de que o
  Markdown é a fonte da verdade. Isso virou "Markdown: vista ou fonte da verdade", que agora trava este
  ticket, porque a resposta muda quem pode concorrer.
- 2026-10-04: "Markdown: vista ou fonte da verdade" decidiu que a verdade mora num banco e o `.md` é
  a vista editável do Gustavo. O R1 das varreduras ("a fonte são os `.md`") caiu, e as candidatas da
  R3 foram escolhidas sob ele. Este ticket espera "Banco como verdade com vista Markdown editável".
- 2026-10-06 (vinda de "Como a verdade viaja entre as máquinas"): caminho CouchDB + LiveSync. A busca
  pode indexar a vista `.md` em disco de cada máquina (B1 da pesquisa 26), enquanto a gravação vai
  pelo MCP do banco.
- 2026-10-06 (conferência da fronteira): passa a esperar "Onde o servidor mora" e "Revisão do sync e
  da divergência com o banco". A busca sobre a vista `.md` (B1 da pesquisa 26) só acha o que outra
  máquina gravou se a vista estiver viva com o Obsidian fechado (não verificado); senão entra o espelho
  junto ao servidor (B2), que depende de onde ele mora. O "mostra o estado do sync" da Question também
  depende da revisão. A gravação saiu deste ticket: vai pelo MCP do es617.
- 2026-10-10 (vinda de "Onde o servidor mora"): S3. Cada par tem o próprio CouchDB, então o espelho
  sem Obsidian (B2) pode rodar no próprio par. Os clientes não têm vista em disco: buscam pelo MCP de um
  par. Este ticket ainda espera a revisão do sync.
- 2026-10-13 (vinda de "Revisão do sync e da divergência com o banco", resolvida):
  o sincronizador é o CLI do LiveSync sempre ligado, então a vista
  `.md` de cada par fica viva com o Obsidian fechado, e a busca sobre ela (B1) acha o que a outra
  máquina gravou. Vão ao disco todos os arquivos comuns até 200 MiB, não só `.md`; pastas com ponto
  ficam fora. O estado do sync vem da vigia (estado curto lido pela checagem de sessão).
- 2026-10-13: ticket reivindicado (wayfinder). Rodada 4 na nota "Rodada atual", refeita com o desenho
  de hoje (a rodada 3, três candidatas no spike, ficou suspensa desde "Markdown: vista ou fonte da
  verdade"): R78 o que a busca faz agora (recomendação: só achar, sobre a vista em disco de cada
  máquina, com clientes buscando pela tailnet; busca dentro do fork do MCP do es617 como reserva,
  3 a 7 dias pela pesquisa 26, B3); R79 que arquivos ela precisa achar (recomendação: obrigatório só
  texto, `.md` `.txt` `.csv`; `.docx` `.pdf` `.xlsx` contam ponto, não verificado em nenhuma
  candidata); R80 quem entra no spike (recomendação: zvec-grep contra memtomem, ck de reserva; o
  markdown-vault-mcp sai porque a vantagem dele era gravar, e gravar saiu da busca; antes do spike, uma
  pesquisa curta sobre transporte HTTP para clientes, lugar do índice, disco reescrito pelo
  sincronizador, outros formatos e FreeLLMAPI). Fato que mudou de sinal: o índice do zvec-grep em
  `.zvec-grep\` dentro da pasta não replica, porque pastas com ponto ficam fora do LiveSync ("Testes
  das portas de entrada"). Página: [`prototipo-09-busca-desenho-novo.html`](../prototipos/prototipo-09-busca-desenho-novo.html).
  Esta sessão já resolveu um ticket; este fica para resolver noutra.
- 2026-10-13, respostas da rodada 4:
  - **R78, aberta:** o Gustavo quer entender melhor a distinção e pede uma pesquisa intensa sobre o
    mecanismo de busca, com roteamento a combinar: "Pq exatamente é tão caro a opção B? Se tivermos um
    mecanismo de busca fora do MCP qual o ganho? qual a perda? [...] E se as 2 opções forem viáveis? E se
    tiver mais que 2 opções de lugar pra deixar um mecanismo de busca? E se tivermos um mecanismo que
    agrega mecanismos? O MCP na prática chega ao mecanismo de busca ou realmente serem 2 opções de buscas
    como fallback ou que permitem diferentes clientes que não seriam atendidos por uma das opções (uma
    sandbox que não vai ter como falar com tailnet, ou o tailnet estar indisponível)". Quer agentes com o
    FreeLLMAPI gerando insumos grandes (JSON ou MD) e agentes mais baratos (Sonnet 5.5 ou Haiku 5.5)
    juntando tudo sem excluir, "pra não deixar opções escaparem"; nem tudo precisa ser testado nem ser
    ferramenta pronta ("um conceito e uma ideia muito bem aplicadas nos ajudam a construir algo ou um
    conjunto, leve ou robusto"); a pesquisa não elimina as candidatas atuais. "Vamos pensar melhor em
    como será esse routing pra essa pesquisa."
  - **R79, A:** obrigatório só texto (`.md`, `.txt`, `.csv`); `.docx`, `.pdf`, `.xlsx` contam ponto.
  - **R80, aceita a recomendação com ressalva:** zvec-grep contra memtomem, ck de reserva, pesquisa curta
    antes; "talvez esses testes podem ser rodados em paralelo. Apenas 'o que esses testes respondem' pode
    acabar mudando com o R78".
  - Para a R78, da pesquisa 26 (§5): a opção B custa mais porque o MCP do es617 não busca texto (índice
    "metadata only", FlexSearch removido) e, no CouchDB, o conteúdo está em pedaços e cifrado (E2EE);
    o fork teria de remontar e decifrar cada nota e manter um índice próprio. "M" (3 a 7 dias) é
    estimativa do relatório, não medida.
- 2026-10-13: rodada 5 na nota "Rodada atual", sobre como fazer a pesquisa ampla da R78, abrindo com as
  respostas às perguntas do Gustavo sobre a opção B (custo, ganho e perda da busca fora do MCP, o MCP
  repassando à busca do disco como terceiro lugar, sandbox sem tailnet). R81 o que a pesquisa cobre
  (recomendação: catálogo em três eixos, lugares, mecanismos e combinações; a régua vira coluna, nunca
  filtro; candidatas atuais entram); R82 roteamento (recomendação: seis geradores gratuitos pelo
  FreeLLMAPI, cada um com um ângulo e teste cego; Haiku 5.5 junta sem excluir; Sonnet 5.5 confere na
  fonte primária e só marca; o maestro sintetiza); R83 como os geradores chegam à web (recomendação:
  Gemini com `google_search` pelo gateway nos ângulos de amplitude e harness apontado ao gateway nos de
  leitura de código, com ensaio curto antes). Fontes do FreeLLMAPI (clone local `C:\Projetos\freellmapi`):
  README ("Tool calling & structured outputs"; "Anthropic Messages API [...] so Claude Code and the
  official Anthropic SDKs run against your free pool"; `/v1/responses` "what Codex CLI needs") e
  `docs/en/api/01-rest-api.md` §"Gemini Google Search grounding" (ferramenta `google_search`).
- 2026-10-13, respostas da rodada 5:
  - **R81, ok com mudanças:** "Troque Windows por SO, pois não atender windows não é algo ruim, podemos
    deixar no wsl de cada máquina." Trocar a coluna FreeLLMAPI por "AI Provider" ou "compatível com
    OpenAI". "Quero mais colunas além dessas, só listar isso de cada ferramenta pode nos limitar um pouco."
    Nota: isso abre um caso de uso para o WSL ("Windows ou WSL" deixou o WSL fora até surgir caso de uso):
    o mecanismo de busca pode rodar no WSL de cada máquina.
  - **R82, recusada a forma:** os geradores precisam ficar "bem limitados ao escopo", com proibição
    estrita de tool calling que os deixe escrever livremente. "Não concordo com apenas 6, pois requests
    podem cair, o teto de inferência de quota pode bater, podem mandar resposta picotada. Então nessa
    etapa 1 eu quero um loop engineering melhor construído. Não é só um workflow retilínio e fim. Proponha
    algo melhor e me mostre com o Designer, não por texto. Não se limite a apenas transformar essas 4
    etapas num loop engineering simples. Proponha algo sério". Página fora do portal.
  - **R83, adiada:** "podemos dar um passo atrás e montar nossa 'fallback chain' do freellmapi, não quero
    fechar isso agora. Essa descoberta dos modelos disponíveis, quota, melhoria da fallback chain deve ser
    uma etapa da proposta do R82."
- 2026-10-13: rodada 6 na nota "Rodada atual". Proposta do laço da pesquisa em
  [`proposta-09-roteamento-da-pesquisa.md`](../prototipos/proposta-09-roteamento-da-pesquisa.md), desenhada
  pelo Designer em [`prototipo-09-roteamento-da-pesquisa.html`](../prototipos/prototipo-09-roteamento-da-pesquisa.html).
  R84 o laço serve de base (recomendação: sim); R85 perfil `auto:pesquisa` só para a pesquisa, proposto
  pela bancada da etapa 0 e criado pelo Gustavo no painel (recomendação: sim); R86 parada (recomendação:
  duas ondas com menos de 5% de novos, depois da calibração, mais um teto que o Gustavo escolhe); R87 as
  colunas em dez grupos (recomendação: sim, acrescentar o que faltar). Fatos do FreeLLMAPI usados (clone
  local, `docs/en/api/01-rest-api.md`): `/v1/models?execution_status=`, `/api/free-tier` com `resetAt`,
  perfis `auto:<perfil>`, `X-Fallback-Trail`, modelo `fusion`.
- 2026-10-13, correção do Gustavo à proposta: a etapa 0 "era para ser uma 'etapa' da montagem desse nosso
  loop engineering. Onde você busca os modelos, propõe estratégias melhores no fallback chain atual ANTES
  de começarmos o loop. Claro que dentro do loop pode existir algo parecido". Proposta e R85 corrigidas:
  a preparação do provedor (levantamento, bancada e proposta para a chain atual, aplicada por ele no
  painel) vem antes do laço; no laço fica só uma vigia leve do provedor, que não muda a chain.
- 2026-10-13, respostas da rodada 6: **R84 sim** (o laço proposto é a base); **R85 sim** (preparar o
  provedor antes do laço, no formato corrigido); **R86 sim** (para em duas ondas seguidas com menos de 5%
  de novos, depois da calibração; o valor do teto de segurança, em horas ou tokens, fica para quando a
  pesquisa for iniciada); **R87 sim** (dez grupos de colunas). O Gustavo elogiou a página do Designer.
  Abertos "Preparar o FreeLLMAPI para a pesquisa da busca" (task) e "Pesquisa ampla: lugares e mecanismos
  de busca" (research, depois do anterior); este ticket passa a esperar a pesquisa. A "pesquisa curta" da
  R80 cabe nas colunas da pesquisa ampla; o teste lado a lado (zvec-grep contra memtomem) pode rodar em
  paralelo quando o Gustavo pedir, mas o que ele mede depende da pesquisa (resposta à R80).
- 2026-10-14 (vinda da peneira da pesquisa ampla, `estrategia-pos-pesquisa.md`, aceita pelo Gustavo): entram
  aqui: (1) o teste de bancada obsidian-hybrid-search contra memtomem, no disco, com conteúdo real em pt e en
  (corpus e métricas na §5 da síntese, `exploracao/anexos/pesquisa-50-sintese.md`); (2) os três fatos a
  confirmar antes: embedding multilíngue no FreeLLMAPI, a linguagem do MCP do es617, e se a exclusão do
  LiveSync cobre arquivos com ponto (o índice do obsidian-hybrid-search é o arquivo
  `.obsidian-hybrid-search.db` na raiz); (3) a linguagem do MCP decide a biblioteca do índice próprio (em
  Python, todas as peças têm Windows confirmado); (4) anexos entram pela extração de texto (Docling,
  pandoc), e onde o texto extraído mora é decidido com "Arquitetura de pastas e frontmatter"; (5) o teste
  mede se o vigia do disco aguenta as rajadas do sincronizador (o watchdog não filtra eventos duplicados).
  Ficam no radar, com gatilho: cópia leve para sandbox (primeira sandbox), duas vias juntas (busca virar
  caminho crítico), rerank e embeddings melhores (teste mostrar semântica fraca), serviço na rede (hub
  crescer além do índice local).
- 2026-10-14, rodada (R90, como confirmar os três fatos): **A.** O maestro lê a fonte primária (documentação
  do FreeLLMAPI no clone local, repositório do es617, código do LiveSync); o fato que a leitura não fechar
  vira item do teste de bancada.
- 2026-10-14, **os três fatos, pela leitura da fonte primária (R90, A):**
  1. **Embedding multilíngue no FreeLLMAPI: sim.** `docs/en/api/01-rest-api.md` §Embeddings (clone local
     `C:\Projetos\freellmapi`, commit ac6d29d): `/v1/embeddings` OpenAI-compatível, roteado por família, e
     "failover never crosses models" (o índice nunca recebe vetor de outro modelo). Famílias: `gemini-embedding-001`
     (padrão, 3072, Google), `text-embedding-3-large`/`-small` (GitHub Models), `embed-v4.0` (Cohere), **`bge-m3`**
     (1024, Cloudflare → Hugging Face), `qwen3-embedding-0.6b` (1024, Cloudflare), `nv-embedqa-e5-v5` (NVIDIA),
     `llama-nemotron-embed-1b-v2` e `-vl-` (NVIDIA), **`embeddinggemma-300m`** (768, Cloudflare). O bge-m3 e o
     EmbeddingGemma são os que a pesquisa apontou para português. Não verificado: quais famílias estão ativas na
     instância do Gustavo (chaves) e a cota de cada uma.
  2. **Linguagem do MCP do es617: TypeScript, Node ≥ 22.** `package.json` (v0.10.0, `"engines": {"node": ">=22"}`)
     e a API de linguagens do GitHub (TypeScript 298 mil bytes; último push 2026-10-14). Consequência: um índice
     dentro do MCP do banco seria em Node (Orama com stemmer `pt`, sqlite-vec), e não em Python como a síntese
     supunha; o SDK TypeScript do MCP não tem CI no Windows comprovado (síntese §4). Saída alternativa: um
     processo Python ao lado do MCP. A lista de peças da construção (SDK Python etc.) só vale se houver esse
     processo.
  3. **LiveSync e arquivos com ponto: metade fechada.** O vigia do CLI ignora qualquer trecho de caminho que
     começa com ponto, pasta **ou arquivo**: regex `/(^|[/\])\./` em
     [`CLIStorageEventManagerAdapter.ts`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/src/apps/cli/managers/CLIStorageEventManagerAdapter.ts#L143-L146).
     A varredura de partida lista tudo (`list()` em
     [`platform/node/storage.ts`](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/platform/node/storage.ts#L158-L172),
     sem filtro), e o filtro que ela usa não foi achado na leitura; o teste "Disco e banco sem o Obsidian" viu
     pastas com ponto na raiz ficarem fora e as aninhadas vazarem. **Vai para o teste de bancada:** o arquivo
     `.obsidian-hybrid-search.db` na raiz, com o CLI reiniciado. Na construção, a regra de exclusão precisa
     cobrir arquivos, não só pastas (`**/.*` além de `**/.*/**`; o casamento usa `dot: true`, em
     [`path.ts`](https://github.com/vrtmrz/livesync-commonlib/blob/c81c08b36f136e9b2c733e27d399acb0fc5ccee4/src/string_and_binary/path.ts#L183)).
     O plugin não vê arquivos com ponto, salvo pelo "Hidden File Sync", recurso à parte
     ([`docs/tips/hidden-file-sync.md`](https://github.com/vrtmrz/obsidian-livesync/blob/14141446a14deab3353a8864dee41e44c372d006/docs/tips/hidden-file-sync.md)).
- 2026-10-14, rodada (R91, formato do teste de bancada): **aceita a recomendação.** obsidian-hybrid-search contra
  memtomem, no disco, Windows sem WSL; cópia (fora de cofre) dos tickets, exploração e anexos deste repositório e
  do `armis-docs` do vault; 40 perguntas com resposta conhecida escritas pelo maestro, metade com palavras
  diferentes do texto, e o Gustavo confere 10 por amostra antes de rodar; mede acerto nos 5 primeiros e posição,
  só palavra contra híbrida, três embeddings (e5-small local, EmbeddingGemma e bge-m3 pelo FreeLLMAPI),
  reindexação depois de uma rajada de 200 arquivos, memória e instalação; arquivo com ponto com o CLI do
  LiveSync se o ambiente do teste "Disco e banco sem o Obsidian" ainda existir; roda um recruta Sonnet 5.5 em
  pasta temporária; cota do FreeLLMAPI conferida e chamadas orçadas antes; só roda quando o Gustavo mandar.
  Ao final, o resultado decide entre a ferramenta no disco com repasse e o índice próprio no MCP do banco.
- 2026-10-14, preparo do teste de bancada (nada rodou): 40 perguntas em
  [`bancada-busca/perguntas.md`](../bancada-busca/perguntas.md) (20 literais, 20 paráfrases, 4 em inglês; 10
  marcadas para a amostra do Gustavo); a pasta `bancada-busca/` fica fora do corpus. Corpus: 117 `.md` deste
  repositório (~1,7 MB) e o `armis-docs` do vault (7 `.md` em pt-PT, pt-BR e en, 4 `.docx`, ~30 KB de texto). O
  ambiente do spike do LiveSync existe em `C:\Projetos\spike-livesync` (cofres, CLI, CouchDB), então o item do
  arquivo com ponto pode rodar. O FreeLLMAPI não respondia em `localhost:3001` na hora do preparo; a cota de
  embeddings fica para conferir quando ele estiver no ar.
- 2026-10-14, rodada (R92, amostra das 10 perguntas): **aprovada** pelo Gustavo (no chat; a nota ficou sem a
  resposta). FreeLLMAPI no ar; orçamento dito: bge-m3 e EmbeddingGemma pela Cloudflare (10 mil neurons por dia,
  divididos com o MeloTTS), ~3 mil neurons no teste (bge-m3 a 1.075 por milhão de tokens; o preço do
  EmbeddingGemma não está na página da Cloudflare, não verificado); e5-small local sem cota. Falta o "pode rodar".
- 2026-10-14: **"pode rodar"** do Gustavo. Teste de bancada solto num subagente Sonnet 5.5 em segundo plano. Ele trabalha
  em `C:\Projetos\bancada-busca\` (corpus copiado, índices e instalações locais) e grava o relatório e os
  resultados em `bancada-busca/` (`relatorio.md`, `resultados.json`, `scripts/`). Tetos: ~3 mil neurons e ~0,6
  milhão de tokens.
- 2026-10-14, **teste de bancada, resultado parcial** (relatório em [`bancada-busca/relatorio.md`](../bancada-busca/relatorio.md),
  dados em `resultados.json`; 163 mil tokens Sonnet). O gateway deu 429 na primeira chamada de cada modelo: a cota
  diária da Cloudflare (10 mil neurons, zera às 00:00 UTC) já estava gasta. Por isso nenhuma configuração com
  `bge-m3` ou `embeddinggemma-300m` foi medida (não verificado), e o gasto de neurons foi 0.
  - Acerto nos 5 primeiros / posição média (MRR), nas 40 perguntas: obsidian-hybrid-search só palavra 0,725/0,504;
    híbrida com e5 local 0,750/0,509; memtomem só palavra 0,675/0,439; híbrida com e5 0,800/0,491. As perguntas com
    as palavras do texto acertam de 0,90 a 0,95; as escritas com outras palavras, de 0,45 a 0,65. Cada pergunta vale
    2,5 pontos, então as diferenças entre as ferramentas estão no ruído. Quatro paráfrases em pt erraram em todas
    (sinônimo ausente: "anotações" por vault, "banco versionado" por Dolt, "arrumar diretórios" por organizar a raiz,
    "caixa isolada" por sandbox).
  - Rajada de 200 arquivos: obsidian-hybrid-search achou 200/200 em até 147 s; memtomem indexou em 186 s na segunda
    rodada (111/200 em 300 s na primeira), e o vigia dele só funciona com um cliente MCP conectado.
  - Memória de pico: obsidian-hybrid-search 767 MB indexando e ~100 MB ocioso; memtomem com e5 1,2 GB indexando e
    372 MB ocioso.
  - Instalação: as duas em ~1 min sem WSL. O obsidian-hybrid-search ignora o `--db` (o banco fica na raiz do
    corpus) e pulou 12 anexos por YAML inválido; o memtomem exige `mm init` e trava duas notas pela proteção de
    segredos.
  - **Arquivo com ponto:** com o CLI do LiveSync, o `.obsidian-hybrid-search.db` na raiz não foi ao banco nem na
    varredura de partida nem criado com o CLI rodando (os arquivos comuns foram). Não testados: subpasta e os
    `-wal`/`-shm`.
- 2026-10-14, rodada (R93, como fechar o teste): **A.** Rodar só a parte do gateway (bge-m3 e EmbeddingGemma nas duas
  ferramentas) depois que a cota da Cloudflare zerar (00:00 UTC, 21h em Brasília), com os mesmos corpus, perguntas e
  scripts, ~3 mil neurons e parada no primeiro erro de cota.
- 2026-10-14 ~17h35, comentário do Gustavo pelo portal (envio `12491ded-743f-4850-8250-881048ca7fb0`): "O que falta
  pra destravar esse ticket?" Resposta do maestro no chat, sem decisão nova:
  1. a parte do gateway do teste de bancada (R93 = A), que espera a cota da Cloudflare zerar às 21h;
  2. a rodada final: a ferramenta pronta no disco com repasse, ou o índice próprio no MCP do banco.
  A pergunta de quem dispara o teste às 21h continua aberta.
- 2026-10-14 ~20h20, chat:
  - O maestro disse que a parte do gateway (R93) não trava a decisão principal deste ticket, a ferramenta pronta no
    disco com repasse ou o índice próprio no MCP do banco: os embeddings valem igual para as duas, e escolher o
    modelo cabe na construção.
  - Correção do Gustavo: "Pq 'escolha' do modelo de embeddings? Só temos as opções do spike? Claro que não". Os três
    do teste de bancada (e5-small, bge-m3 e EmbeddingGemma) foram escolhidos pela disponibilidade, não por uma
    pesquisa de quais servem melhor a pt-BR e en no Windows.
  - Proposta: uma pesquisa em fonte primária dos modelos de embeddings, locais e por API, e depois **uma** bancada só
    com os melhores, nos mesmos corpus, perguntas e scripts. A parte do gateway das 21h entra nessa bancada, em vez
    de rodar hoje. Aguarda o ok do Gustavo.
- 2026-10-14 ~20h35: o Gustavo autorizou abrir a decisão principal em paralelo à pesquisa de embeddings. **Rodada 7
  aberta no portal** (`portal/rodadas/2026-10-14-camada-de-busca-r7.md`):
  - **Onde a busca mora.** Recomendação A, Leve com alcance: ferramenta pronta no disco de cada par e proxy de MCP
    na tailnet para os clientes. As alternativas são B, a Robusta (índice próprio no MCP do banco, em Node, 5 a 8
    dias, não medido), e C, que começa com A e faz o protótipo de 1 dia de B para comparar.
  - **Qual ferramenta pronta.** Recomendação: obsidian-hybrid-search.
  - Argumento: o que falha no teste são sinônimos, que o stemmer de português da Robusta também não resolve; quem
    resolve é o embedding, que serve às duas opções.
  - Não verificados na A: o proxy repassar stdio no Windows e a latência pela tailnet.
- 2026-10-14: a escolha do modelo de embeddings virou a pesquisa [Modelos de embeddings da busca](54-modelos-de-embeddings-da-busca.md); a parte do gateway da bancada entra nela.
- 2026-10-14 21:02, resposta à rodada 7 (portal, envio `5ff51ddc-f0eb-417e-a9b6-fc57bfdc193b`):
  - **Onde a busca mora = C.** Começa com A, a Leve com alcance: obsidian-hybrid-search no disco de cada par e o
    proxy de MCP na tailnet. Junto, faz já o protótipo de 1 dia de B, a Robusta: índice próprio no MCP do banco, em
    Node, com Orama e stemmer `pt` mais sqlite-vec, alimentado pelas mudanças do CouchDB. Os dois são comparados no
    mesmo teste antes de fechar. A recomendação era A.
  - **Ferramenta pronta = obsidian-hybrid-search.**
  - O ticket segue aberto até a comparação. O teste de comparação usa os embeddings da lista curta da pesquisa
    "Modelos de embeddings da busca", em vez de rodar duas vezes.
- 2026-10-14 ~21h05: rodada 8 aberta no portal, sobre quem monta o protótipo da Robusta e quando. Recomendação A: um subagente Sonnet 5.5 agora, em paralelo à pesquisa de embeddings, com 300 a 500 mil tokens estimados.
- 2026-10-14 21:18, resposta à rodada 8 (portal, envio `df877739-5e63-4cc6-b641-ee6caabd1b0e`): **A.** Um subagente Sonnet 5.5 monta o protótipo da Robusta agora, em paralelo à pesquisa de embeddings, e roda a comparação quando a lista curta sair (300 a 500 mil tokens estimados). Lançado em segundo plano, com relatório em `bancada-busca/prototipo-robusta.md`.

- 2026-10-14 (~22h): protótipo da Robusta entregue pelo subagente Sonnet (`bancada-busca/prototipo-robusta.md`;
  scripts em `bancada-busca/scripts/robusta/`; trabalho em `C:\Projetos\bancada-busca\robusta\`). Node com Orama
  3.1.18 (stemmer pt), sqlite-vec 0.1.9 e RRF; e5-small local; 124 notas e as 40 perguntas; nenhuma chamada ao
  FreeLLMAPI. Acertos nos 5 primeiros (hit@5) e posição média do acerto (MRR): só palavra 0,45 a 0,53 / 0,21 a 0,39
  (OHS = obsidian-hybrid-search 0,725 / 0,504; causa não investigada); só vetor 0,725 / 0,474 (igual ao OHS com e5);
  híbrida 0,65 a 0,75 / 0,40 a 0,46 (diferença de 1 a 3 acertos é ruído). Indexação total de 234 a 347 s (OHS 116 s),
  pico de 1,7 a 1,9 GB (OHS 767 MB); consulta de 0,5 a 0,7 s para as 40. `_changes` sem E2EE: 4620 documentos lidos
  em 0,75 s, edição no índice em 1,4 s. Com E2EE o consumidor não decifra; decifrar por um segundo CLI do LiveSync
  custou 48 s; decifrar direto no Node não foi tentado. Fase 2 (modelos da lista curta) espera a pesquisa do ticket 54;
  o modelo é parâmetro (`ROBUSTA_MODEL`, `ROBUSTA_DIM`). Não medidos: rajada de 200 arquivos, tamanho do índice,
  repetições.
- 2026-10-14 ~22h15: rodada 9 aberta no portal (`portal/rodadas/2026-10-14-camada-de-busca-r9.md`), sobre o que fazer com a Robusta depois do protótipo. Recomendação B: ajuste curto (FTS5 do SQLite na busca por palavra e decifrar o banco direto no índice, pelo caminho do MCP do es617) antes da fase 2.
- 2026-10-14 22:29, resposta à rodada 9 (portal, envio `22997630-c6b9-4eec-bbac-ac969fa34235`): **B, mas com um subagente Opus 5.5 de esforço médio** (não o Sonnet). Antes da fase 2, ajuste curto na Robusta: busca por palavra pelo FTS5 do SQLite e decifrar o banco cifrado direto no índice, pelo caminho do MCP do es617. Depois, a fase 2 com as duas. Entrega em `bancada-busca/prototipo-robusta-ajuste.md`.
- 2026-10-14 (~23h): ajuste da Robusta entregue pelo subagente Opus 5.5 médio (`bancada-busca/prototipo-robusta-ajuste.md`).
  - **FTS5**, no desenho do OHS (lido em `dist/src/db.js`, `searcher.js` e `indexer.js` do OHS 0.16.2: título, aliases
    e conteúdo, `unicode61`, pesos 10/5/1, termos com prefixo unidos por OR):
    - só palavra: 0,700 / 0,449 (124 arquivos) e 0,700 / 0,495 (sem os 12), contra o OHS 0,725 / 0,504;
    - nas perguntas de palavra, 0,95, igual ao OHS;
    - híbrida RRF: 0,625 / 0,444 e 0,700 / 0,495, contra o OHS 0,750 / 0,509. A fusão do OHS, com quatro listas e
      pesos, não foi reproduzida.
  - **E2EE decifrado no próprio Node**, pela `livesync-commonlib` 0.1.36 (`outgoingDecryptHKDF`, sal em
    `_local/obsidian_livesync_sync_parameters`):
    - reindexação total pelo banco cifrado em 277 s, quase tudo embedding; a decifragem sozinha leva 1,3 s;
    - uma edição chega ao índice em 2,1 s;
    - o texto decifrado é idêntico ao do cofre de teste.
  - **Não verificado:** que o MCP do es617 use as mesmas funções (o código dele não está na máquina). Sem cifra V1,
    compressão, binários nem conflitos.
  - **Próximo:** a fase 2 com as duas, nos modelos da lista curta do ticket 54.
- 2026-10-15: fase 2 de modelos (ticket 54) em `bancada-busca/fase2-modelos.md`: o arctic-embed-m-v2.0 no OHS leva a
  híbrida a 0,875 / 0,632 (e5: 0,750 / 0,509); gemini-embedding-001 é o melhor só vetor na Robusta (0,900 / 0,728). A
  escolha do modelo espera a rodada 3 do ticket 54.
- 2026-10-15 ~14h30: com o modelo escolhido ("Modelos de embeddings da busca", resolvido: arctic local, gemini ligável
  depois), **rodada 10 aberta** (`portal/rodadas/2026-10-15-camada-de-busca-r10.md`), rascunhada por um subagente Opus
  médio e revisada pelo maestro: onde a busca mora (recomendada a Leve com alcance, o obsidian-hybrid-search com o
  arctic no disco de cada máquina, com a Robusta guardada como reserva com gatilho; opção C, um teste curto antes),
  idioma por nota (recomendado: não, um analisador só) e como o gemini fica ligável (recomendado: pronto e desligado).
  Fato novo do README do obsidian-hybrid-search 0.16.2 (seção "Shared HTTP server"): `ohs serve` já serve MCP por HTTP,
  com `--host` e `--allowed-host`. **Não verificado:** autenticação desse servidor HTTP; leitura de `.txt` e `.csv`;
  segundo índice ao lado do arctic. Fontes em `scratchpad/rodada-09-fontes.md` da sessão (resumo no ticket 12 depois).
- 2026-10-15 14:14, **rodada 10 respondida** (envio `2851bfe9-9d62-402f-8b3d-69976f994e60`), as três recomendadas:
  onde = A (Leve com alcance), idioma = A (um analisador só), gemini = A (pronto e desligado). Ticket resolvido.

## Answer

**A camada de busca do hub é a "Leve com alcance":** o obsidian-hybrid-search, com o modelo arctic-embed-m-v2.0 local,
no disco de cada máquina, lendo a vista Markdown e servindo a busca por MCP em HTTP na tailnet (rodada 10, envio
`2851bfe9-9d62-402f-8b3d-69976f994e60`).

- **Por quê:** com o mesmo modelo, a busca por sentido empatou com a Robusta (0,667 contra 0,668 nas mesmas 112 notas);
  a Leve tem a melhor busca mista da bancada (0,632 contra 0,567) e é ferramenta pronta, que já serve MCP por HTTP
  (`ohs serve`, com `--host` e `--allowed-host`, README 0.16.2, seção "Shared HTTP server").
- **Reserva:** o protótipo da Robusta (índice dentro do MCP do banco, lendo o CouchDB cifrado) fica guardado, com os
  scripts, e volta se a busca precisar mostrar uma gravação em segundos ou se o gemini não rodar ao lado do arctic.
- **Idioma:** um analisador só para português e inglês (FTS5 do SQLite, sem stemmer), mais o embedding multilíngue. O
  frontmatter não ganha campo de idioma por causa da busca.
- **Gemini:** a construção escreve a configuração do gemini-embedding-001 pelo FreeLLMAPI e a testa uma vez, num índice
  ao lado do arctic, e o deixa desligado. Ligar é escolha do Gustavo; ligado, o conteúdo indexado vai ao Google e a busca
  por sentido depende da rede e da cota do gateway.
- **Não verificado, para a construção:** autenticação do servidor HTTP do obsidian-hybrid-search (o README só fala do
  cabeçalho Host); se ele lê `.txt` e `.csv`; se roda um segundo índice ao lado do arctic; o tempo de uma edição até a
  busca com o CLI do LiveSync ligado. Notas com YAML inválido ficam fora do índice (12 de 124 na bancada).
- **Herdam:** "Como os agentes gravam no hub" (destravado); "Arquitetura de pastas e frontmatter" (rodada 13, texto
  extraído dos anexos; lista no comentário de 2026-10-15 lá); "Acesso dos agentes: decisão" (juntar o MCP da busca e o
  do banco num endereço só).
