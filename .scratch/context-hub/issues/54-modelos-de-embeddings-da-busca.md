# Modelos de embeddings da busca: pesquisa

Type: research
Status: resolved
Blocked by:

## Question

Que modelos de embeddings servem à camada de busca do hub? O conteúdo é português e inglês, no Windows, rodando
local ou por API, inclusive pelas famílias do FreeLLMAPI. A pesquisa sai em fonte primária: model card,
documentação do provedor e placar oficial. O que conta é qualidade em pt e en, rodar em CPU no Windows, memória,
dimensões, tamanho de contexto, licença, e custo ou cota por API. Termina numa lista curta para **uma** bancada,
com os mesmos corpus, perguntas e scripts do teste de bancada da "Camada de busca".

Insumo de "Camada de busca": o modelo vale igual para as duas opções de onde a busca mora.

## Comments

- 2026-10-14 ~20h30, aberto a pedido do Gustavo. Ele corrigiu o maestro, que tratava a escolha do modelo como uma
  escolha entre os três do teste de bancada: "Pq 'escolha' do modelo de embeddings? Só temos as opções do spike?
  Claro que não". Ao abrir: "abra. Mas faça loop engineering disso".
  - Como roda: o laço da pesquisa ampla ("Montar os scripts do laço", em `laco/`) copiado para
    `laco-embeddings/`, com plano, sementes ocultas e chave de junção próprios.
  - Os modelos do FreeLLMAPI geram; os scripts juntam e param em duas ondas com menos de 5% de novos, depois da
    calibração.
  - O maestro confere na fonte primária a lista que o laço entrega.
  - Sem recruta Claude vigiando os processos.
  - Roda só depois do "pode iniciar", com o orçamento de chamadas dito antes.
  - A parte do gateway do teste de bancada (R93) não roda sozinha hoje: entra na bancada da lista curta.
- 2026-10-14 ~20h20: laço montado em `laco-embeddings/`. Nada chamou modelo ainda.
  - `montar_plano.py` gera o `plano.json`: 36 células = 6 ângulos × pt, en, zh × 2 formulações.
  - `sementes.json` tem 7 sementes ocultas: multilingual-e5-large-instruct, Qwen3-Embedding-0.6B, jina-embeddings-v3,
    nomic-embed-text-v2-moe, snowflake-arctic-embed-l-v2.0, gte-multilingual-base e Serafim (URL desta não
    verificada).
  - O juntador ganhou a chave `hf:org/modelo`, tratada como a `gh:`.
  - Os grupos de gerador são pt-en e zh, com até 120 células novas por onda.
  - `despachante.py --uma-vez`: 148 modelos aptos.
  - Rodada 1 aberta no portal com o orçamento (400 a 700 chamadas, teto recomendado de 1.200 tentativas ou 4 h),
    pedindo o "pode iniciar".
- 2026-10-14 20:36, resposta à rodada 1 (portal, envio `8d21d137-09dd-4a3a-b96b-bc3ffa9823fa`): **aprovado** o
  início, com **teto B, 600 tentativas ou 2 horas**. Comentário: "quero um painel pra tudo isso, como o designer já
  ta ocupado, spawne outro pra criar isso, mas já vá rodando. O painel surge no meio da busca." Um segundo recruta
  designer foi pedido explicitamente, o que vale como aval do custo Claude dele.
- 2026-10-14 ~20h40: o laço foi **iniciado** com teto de 600 tentativas ou 2 horas (despachante, gerador pt-en, gerador zh e juntador, por `Start-Process`, com logs em `laco-embeddings/logs/`). O recruta "Designer Loops" (Opus 5.5, esforço alto) foi recrutado para o painel ao vivo, em `laco-embeddings/painel/`.
- 2026-10-14 ~20h50, primeiros 53 pedidos: 1 aceito, 18 cortados e 15 inválidos. O despachante sorteava modelos que não servem para gerar texto: guardas de segurança, tradutores, modelos de visão e de código, modelos de 1B e de áudio ao vivo. A bancada de 2026-10-13 não conhecia esses modelos, porque o gateway ganhou modelos desde então. Correção: 47 ids em `excluir_manual` no `config.json` (vale no ciclo seguinte do despachante). Não mexi em mais nada.
- 2026-10-14 ~21h: segundo defeito. O `gerador.py` validava o `kind` contra os tipos da pesquisa ampla e recusava as respostas certas, com os tipos `model`, `api` etc. Também: o despachante só lê o `config.json` ao ligar, então o `excluir_manual` não tinha valido. O laço foi parado, `TIPOS` corrigido, os pedidos em voo devolvidos à fila, e os 4 processos religados (PIDs 43992, 57080, 54504, 53064). Cerca de 110 tentativas do teto de 600 se perderam nesses dois defeitos.
- 2026-10-14 ~21h05, pedido do Gustavo no chat: "o teto agora é apenas as 2 horas, as tentativas suba pra 5000 e aumente os workers. Mantenha aquele nível de ondas sem novos itens porém em 15%". Feito: o teto passou a 5.000 tentativas, e as 2 horas continuam contadas desde 20h36, terminando às 22h36. `trabalhadores_por_gerador` foi de 6 para 20 e `gate_novos` de 0,05 para 0,15 (para em duas ondas seguidas abaixo de 15% de novos). Os processos foram religados (PIDs 49308, 56812, 54064, 53908). Os pedidos que estavam em voo nos processos antigos voltam à fila pelo despachante.
- 2026-10-14 ~21h15: painel v1 do Designer Loops em `laco-embeddings/painel/index.html` (metáfora "observatório"). Um atualizador roda `painel_dados.py` a cada 30 s, fora do Claude Code (PID 57424). Pedido ao Designer Loops: ler a linha de parada do `gate_novos` do config, que agora é 15%.
- 2026-10-14 22:16: laço parado pelo teto de **5.000 tentativas** (antes do limite de 2 h; eu tinha dito que o tempo é
  que valeria, e errei). Curva de novos: 100%, 67%, 27%, 20%, 14% (a onda 5 ficou abaixo do gate de 15%, mas o gate
  pede duas seguidas; a onda 6 ficou incompleta e a calibração não rodou). 2.157 itens no catálogo, 142 modelos do
  FreeLLMAPI usados. Às 22h40 o maestro gravou `parar`, encerrou despachante e juntador e escreveu
  `estado/laco_final.json` e o `terminou_em` do `laco.json`. Próximo: conferir o catálogo na fonte primária e montar
  a lista curta.
- 2026-10-14 (~23h30): **conferência na fonte primária** (API pública do Hugging Face; script
  `laco-embeddings/conferir_hf.py`; saídas em `laco-embeddings/verificacao/hf.json`, `hf-ranking.json` e
  `hf-novos.json`):
  - Dos 396 repositórios citados pelo laço (2 menções ou mais, sementes e busca), **só 154 existem**; os 242 outros
    são nomes inventados pelos modelos (por exemplo `openai/text-embedding-ada-002` no HF).
  - Sementes: 6 de 7 achadas, mas as mais novas com pouquíssimas menções (nomic v2 MoE 1, arctic l v2.0 2,
    Qwen3-Embedding-0.6B 8); o Serafim (português) não apareceu.
  - **Achado principal:** o laço puxou para modelos antigos e populares (MiniLM 817 menções, ada-002 497) e quase não
    viu os de 2025 e 2026. A lista do HF por downloads, likes e tendência trouxe vários que o laço não citou:
    embeddinggemma-300m e embeddinggemma-2 (Google), harrier-oss-v1 (Microsoft), granite-embedding multilingual r2
    (IBM), jina v5, pplx-embed, Nemotron-3-Embed e voyage-4-nano. Leitura: os modelos gratuitos que responderam
    conhecem pouco do que saiu depois do treino deles. Bola de neve sobre memória de modelo não substitui a fonte
    primária quando o assunto é recente.
  - Posição de cada modelo no placar MTEB: **não conferida**. A bancada própria (40 perguntas) decide.
- 2026-10-14 (~23h40): rodada 2 aberta no portal (`portal/rodadas/2026-10-14-modelos-de-embeddings-da-busca-r2.md`):
  a lista curta (tabela editável) e o jeito de rodar a fase 2.
- 2026-10-14 23:32, resposta à rodada 2 (portal, envio `65d183a8-88c0-4d6d-994f-a2f995a583a1`):
  - **Lista curta:** sem mudanças nem comentário; o maestro a toma como aceita do jeito que foi proposta. São 15
    modelos: 12 locais com ONNX (e5-small, granite 97m e 311m, harrier 270m e 0.6b, embeddinggemma 300m e 2, arctic
    m v2.0, gte-multilingual-base, e5-large-instruct, bge-m3, Qwen3-Embedding-0.6B) e 3 por API (gemini-embedding-001,
    text-embedding-3-large, embed-v4.0).
  - **Como rodar = A:** duas etapas. Primeiro todos na Robusta, depois os 3 melhores também na ferramenta pronta. Fica
    com o mesmo subagente Opus 5.5 médio do ajuste.
  - **Modelos por API = A:** entram, com a cota orçada antes. O corpus de teste, `armis-docs` incluído, sai para
    Google, OpenAI e Cohere pelo gateway.
  - **Rerankers = A:** bge-reranker-v2-m3 e gte-multilingual-reranker-base por cima dos 20 primeiros resultados do
    modelo escolhido.
  - Fase 2 lançada por SendMessage ao subagente do ajuste. Entrega em `bancada-busca/fase2-modelos.md`.
- 2026-10-15 (~04h30): **fase 2 rodou** (agente `aa5ada2d3595885dc`, ~01h a 03h25); o agente caiu duas vezes por erro de
  API sem escrever o relatório, e o maestro o escreveu dos arquivos brutos: `bancada-busca/fase2-modelos.md`. 9 de 15
  avaliados. Só vetor, MRR com as 124 notas: gemini-embedding-001 0,728; embeddinggemma-300m 0,632; arctic-m-v2 0,600;
  harrier-270m 0,585; gte-multilingual-base 0,543; bge-m3 0,540; granite-311m 0,492; e5-small 0,461; granite-97m
  0,421. No OHS, arctic na híbrida 0,632 (e5: 0,509); granite-311m falhou (ONNX quantizado ausente) e gte anômalo.
  Rerankers: bge quase empata no total com 14 s por busca; gte piora. Fora: 4 locais maiores (sonda OK, não indexados),
  OpenAI (nome errado no gateway), Cohere (limite da chave de teste). **Rodada 3 aberta**
  (`portal/rodadas/2026-10-15-modelos-de-embeddings-da-busca-r3.md`): completar os 6 e o destino dos rerankers.
- 2026-10-15 07:44, **rodada 3 respondida** (envio `ae64bab7-9c5b-4e68-9cae-800d4ebd9f5b`): **completar = A** (o maestro
  dispara os scripts existentes, sem agente Claude: os 4 locais um por vez, OpenAI com o nome certo no gateway, Cohere
  abaixo do limite; depois, rodada para escolher o modelo). **Rerankers = A:** fora do hub agora, no Radar de
  `estrategia-pos-pesquisa.md` com o gatilho "a busca virar caminho crítico ou uma máquina com GPU".
- 2026-10-15 ~07h55: completar disparado (`C:/Projetos/bancada-busca/fase2/completar.sh`, sem agente Claude): Cohere
  com pausa de 15 s entre lotes, em paralelo; os 4 locais um por vez com corte de 150 min (`FILA_LIM_MIN` novo no
  `fila.py`; o corte de 40 min explicava por que não tinham entrado). Logs `api3.log`, `local3.log`, `av3.log`; fim
  em `completar.fim`. **OpenAI:** o gateway não tem a família `text-embedding-3-large` registrada (nem com o id
  `openai/...`, nem a `-small`); a documentação do FreeLLMAPI a põe no GitHub Models. Fica fora até alguém habilitar
  esse provedor no gateway.
  - ~08h05: a Cohere bateu de novo no limite em 336 de 1.862 (os lotes crescem, porque os trechos vão do menor ao
    maior). Relançada à parte (`fase2/cohere.sh`, `api4.log`, `av4.log`, fim em `cohere.fim`) com lotes de 24 e pausa
    de 20 s, uns 35 min.
  - ~09h10: embeddinggemma-2 indexado (41 min, 3,4 GB) e avaliado; e5-large-instruct em curso. A Cohere caiu de novo,
    agora com HTTP 502 "fetch failed" depois de 3 novas tentativas, em 240 de 1.862 trechos: não é mais o limite por
    minuto. Fica parada; causa não investigada.
- 2026-10-15 11h46: **completar terminou** (`completar.fim`). Tabela final de 13 modelos em
  `bancada-busca/fase2-modelos.md`, seção "Rodada 3". Novos, MRR só vetor com as 124 notas: embeddinggemma-2 0,639
  (empata com o embeddinggemma-300m, 0,632, e perde nas paráfrases); harrier-0.6b 0,535; e5-large-instruct 0,491;
  Qwen3-Embedding-0.6B 0,395 (abaixo do e5-small; causa não investigada). Cohere sem avaliação (limite da chave de
  teste e depois HTTP 502); OpenAI fora (família não registrada no gateway). **Rodada 4 aberta**
  (`portal/rodadas/2026-10-15-modelos-de-embeddings-da-busca-r4.md`): escolher o modelo.
- 2026-10-15 12:25, **rodada 4 respondida** (envio `863fb4ee-02be-46a7-aa51-c6fd15dde253`): **modelo = D** (a
  recomendada era A): o arctic-embed-m-v2.0, local, como padrão nas duas máquinas, e o gemini-embedding-001 (API do
  Google pelo FreeLLMAPI) como segunda opção ligável depois, para as buscas por sentido. **Qwen3 = A:** fora, sem
  investigar. Ticket resolvido.

## Answer

**Modelo da camada de busca:** arctic-embed-m-v2.0 (Snowflake), local, como padrão nas duas máquinas; o
gemini-embedding-001, pela API do Google via FreeLLMAPI, entra depois como segunda opção ligável para as buscas por
sentido (decisão do Gustavo, rodada 4, envio `863fb4ee-02be-46a7-aa51-c6fd15dde253`).

Por quê, em números (`bancada-busca/fase2-modelos.md`; 40 perguntas, 124 notas, MRR só vetor): o arctic tem 0,600, a
uns 0,03 do melhor local (embeddinggemma-300m, 0,632, dentro do ruído), responde em 46 ms por consulta e é o único já
rodado no obsidian-hybrid-search, onde deu a melhor busca híbrida da bancada (0,632, contra 0,509 do e5-small). O
gemini é o melhor de todos (0,728) e o melhor nas paráfrases (0,679).

Fica para o ticket da camada de busca e a construção:
- o modelo vale para as duas opções de onde a busca mora;
- "segunda opção ligável": o gatilho e a forma de ligar o gemini não foram decididos; quando ligado, o conteúdo
  indexado sai para o Google e a busca depende da rede e da cota do gateway;
- fora: Qwen3-Embedding-0.6B (abaixo do e5-small, causa não investigada), embed-v4.0 (Cohere, sem avaliação) e
  text-embedding-3-large (não está no gateway); rerankers no Radar (rodada 3).
