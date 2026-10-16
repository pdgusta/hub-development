## Faixa 3: Busca

A camada de busca do hub é a "Leve com alcance": o obsidian-hybrid-search, com o modelo arctic-embed-m-v2.0 local, no
disco de cada par, lendo a vista Markdown e servindo a busca por MCP em HTTP (09, 54). Nesta execução a faixa entrega a
busca num par só (esta máquina), sobre o hub de ensaio, com o gemini-embedding-001 configurado, testado uma vez e
desligado.

### User stories

1. Como agente no Claude Code, quero buscar no hub por palavra e receber o trecho certo com o caminho da nota, para não
   ler pastas inteiras (09; critério 1).
2. Como agente no Codex, quero a mesma busca pelo mesmo MCP, para que o critério 1 valha igual nos três harnesses (09, 14).
3. Como agente no Copilot (CLI e modo agente do VS Code), quero a mesma busca pelo mesmo MCP, para que o Copilot não fique
   de fora (04, 14).
4. Como agente, quero achar uma nota escrita com outras palavras que não as da minha pergunta, para que a busca por
   sentido cubra paráfrases e sinônimos (09, 54).
5. Como agente, quero buscar em português e em inglês na mesma consulta e no mesmo índice, sem dizer o idioma, para não
   precisar de dois caminhos (09, rodada 10: um analisador só).
6. Como agente, quero que uma nota nova ou editada no disco apareça na busca sem que ninguém mande reindexar, para que a
   busca reflita o que outro agente acabou de gravar (09).
7. Como agente, quero que uma nota que chegou da outra máquina pelo sincronizador apareça na busca do meu par, para que
   a busca leia a vista viva mesmo com o Obsidian fechado (33, 09).
8. Como agente, quero que uma rajada de muitos arquivos (por exemplo, a varredura de partida do sincronizador) termine
   indexada, para não perder notas numa chegada em massa (09, bancada: 200 de 200).
9. Como agente, quero que o texto extraído de um anexo, no arquivo irmão `.pdf.md`, entre na busca, para achar o
   conteúdo de PDFs e documentos que a busca não lê direto (12).
10. Como agente, quero que o `index.md` de cada pasta (o cartão da pasta) seja achado pela busca, para chegar ao que a
    busca não indexa por ele (12).
11. Como Gustavo, quero que `.secrets/` nunca apareça num resultado de busca, para que senha e segredo não vazem para o
    contexto de um agente (12).
12. Como Gustavo, quero que a pasta cujo `index.md` declara `local: true` fique fora da indexação e dos resultados da
    busca do próprio par, pela mesma lista de exclusão que o sync usa, e não replique ao outro par, para que a pasta não
    replicada não escape por outro caminho (12, rodada 17 e Answer).
13. Como Gustavo, quero que o índice da busca (`.obsidian-hybrid-search.db`, na raiz do hub) não vá ao banco nem ao git,
    para que cada par tenha o seu índice e o arquivo não viaje (09, 12).
14. Como Gustavo, quero que a busca do par escute só em 127.0.0.1, para que nada fora da máquina alcance o servidor sem
    passar pelo proxy com token (14).
15. Como agente de um cliente (sandbox ou máquina de passagem), quero buscar no hub pela rota de busca do proxy do par,
    para usar o hub sem cópia própria (14, 34; o proxy é da faixa 10).
16. Como Gustavo, quero que o modelo de embeddings rode local nas duas máquinas, para que a busca por sentido funcione sem
    rede e sem mandar o conteúdo a terceiros (54).
17. Como Gustavo, quero o gemini-embedding-001 configurado pelo FreeLLMAPI, testado uma vez num índice ao lado do arctic
    e deixado desligado, para ligá-lo depois sem obra nova (09, 54).
18. Como Gustavo, quero que ligar o gemini seja uma escolha minha, explícita, para saber que, ligado, o conteúdo indexado
    vai ao Google e a busca por sentido passa a depender da rede e da cota do gateway (09, 54).
19. Como Gustavo, quero que o frontmatter não ganhe campo de idioma por causa da busca, para que o esquema das notas não
    carregue peso da ferramenta (09).
20. Como Gustavo, quero saber quais notas ficaram fora do índice por YAML inválido, para que nenhuma nota suma da busca em
    silêncio (09: 12 de 124 na bancada; lição "nada some em silêncio").
21. Como maestro, quero instalar a busca pelo fragmento de kit da faixa, idempotente e com HOME de ensaio, para montar a
    busca em qualquer par novo sem passos à mão (16, plano: contrato do instalador).
22. Como maestro, quero que o fragmento de kit entregue a linha de registro do MCP de busca para os três harnesses, para
    que a faixa 8 só a junte, sem editar a configuração de outra faixa (14, plano: fronteiras).
23. Como hook de leitura da faixa 6, quero que as chamadas e os resultados da busca tenham forma estável (nome da
    ferramenta, caminho e trecho devolvidos), para guardar por sessão o que a busca devolveu e avisar a leitura grande
    fora dela (11).
24. Como Gustavo, quero que a busca rode no Windows nativo, sem WSL, no NTFS de `C:\context-hub`, para seguir a regra de
    guardar os arquivos do lado de quem trabalha neles (03, 04).
25. Como Gustavo, quero que a busca não dependa do Obsidian aberto, para que os agentes achem as notas com o cofre
    fechado (33, 09).
26. Como Gustavo, quero o tempo medido de uma edição no disco até ela aparecer na busca, com o sincronizador ligado, para
    saber se o gatilho da Robusta (gravação visível em segundos) foi acionado (09).
27. Como Gustavo, quero a memória ociosa e de pico da busca medidas com o arctic, para saber o custo dela em cada máquina
    (09, bancada com o e5: 767 MB indexando, cerca de 100 MB ocioso).
28. Como Gustavo, quero que a Robusta (índice dentro do MCP do banco) fique guardada como reserva, com os scripts do
    protótipo, para voltar a ela se um gatilho disparar, sem refazer a pesquisa (09).
29. Como agente, quero que a busca por palavra e a busca por sentido saiam fundidas numa resposta só (a híbrida do
    obsidian-hybrid-search), para não escolher o modo a cada pergunta (09, 54: híbrida 0,632 com o arctic).
30. Como Gustavo, quero que o servidor de busca volte sozinho quando cair, para que a porta de entrada do hub não fique
    fechada sem aviso (09: "a busca é a porta"; a forma de religar é ponto aberto).

### Implementation decisions

- **Ferramenta:** obsidian-hybrid-search 0.16.2 (a versão lida e medida), no disco de cada par, indexando a vista
  Markdown em `C:\context-hub` (09, 04). Busca híbrida: palavra pelo FTS5 do SQLite (`unicode61`, sem stemmer) e
  sentido pelo embedding (09).
- **Modelo:** arctic-embed-m-v2.0 (Snowflake), local, padrão nas duas máquinas, como rodou na fase 2 da bancada (54).
  Fora: Qwen3-Embedding-0.6B, embed-v4.0 (Cohere) e text-embedding-3-large; rerankers ficam no Radar (54).
- **Servidor:** o modo HTTP compartilhado do próprio obsidian-hybrid-search (`ohs serve`, com `--host` e
  `--allowed-host`, README 0.16.2, seção "Shared HTTP server"), preso a 127.0.0.1 (09, 14). Os agentes do par o usam
  direto; o cliente chega pela rota de busca do TBXark/mcp-proxy na tailnet, com token próprio (14; o proxy é da faixa 10).
- **Um analisador só** para português e inglês, mais o embedding multilíngue; sem campo de idioma no frontmatter (09).
- **Índice:** o arquivo `.obsidian-hybrid-search.db` na raiz do corpus (a ferramenta ignora o `--db`, bancada do 09).
  Como tem ponto no nome, fica fora do LiveSync (regra `**/.*` e `**/.*/**`, faixa 4) e fora do git (12).
- **Exclusões da busca:** todo arquivo e pasta com ponto no nome, em qualquer nível (`.secrets/`, `.git`, `.maestri/`,
  o índice da busca), mais as pastas com `index.md` `local: true`, saem da busca (12; 09, R90: arquivos, não só
  pastas), pela lista que o gerador de exclusões produz a partir desses marcadores, a mesma que gera a exclusão do
  sync. O mecanismo `OBSIDIAN_IGNORE_PATTERNS` com `**/.*` e `**/.*/**` é a solução proposta pelo núcleo; a sua
  eficácia se verifica, sem depender de comportamento implícito da ferramenta. O gerador é um só; busca e
  sincronizador consomem o resultado; o dono (o núcleo diz faixa 1) é **[formato]**.
- **O que entra:** só `.md` (o obsidian-hybrid-search 0.16.2 só indexa `.md`, ticket 12); o texto de anexo entra pelo
  arquivo irmão `.pdf.md` com `source` e `extractor` (12). Quem dispara a extração não é desta faixa (12, ponto aberto lá).
- **Gemini pronto e desligado:** a faixa escreve a configuração do gemini-embedding-001 pelo FreeLLMAPI, com o nome do
  modelo explícito (nunca `model: auto`) e o endereço do gateway por variável de ambiente (`FREELLM_BASE_URL`, ticket 16),
  num índice ao lado do arctic; roda uma vez e deixa desligado (09). Nesta execução o FreeLLMAPI é o atual, no Docker
  desta máquina; o FreeLLMAPI nativo no notebook pessoal fica para outra execução (16, plano).
- **Reserva com gatilho:** a Robusta (Node, FTS5, decifra o banco cifrado direto no índice pela `livesync-commonlib`,
  alimentada pelo feed de mudanças do CouchDB) fica guardada com os scripts da bancada. Volta se a busca precisar mostrar
  uma gravação em segundos ou se o gemini não rodar ao lado do arctic (09, 50).
- **A busca nativa do CouchDB não serve:** o LiveSync grava pedaços cifrados, então Nouveau, Clouseau e Mango ficam fora
  (50).
- **Fragmento de kit:** idempotente, lê o HOME de `HUB_HOME_ENSAIO`, aceita `-WhatIf`; instala a ferramenta e o modelo,
  escreve a configuração do servidor (127.0.0.1) e a do gemini desligado, e entrega a linha de registro do MCP de busca
  para os três harnesses à faixa 8 (plano: contrato do instalador; 14).
- **Fronteira com a faixa 6:** a forma das chamadas e dos resultados da busca (nome da ferramenta, caminho, trecho) é o
  contrato que o hook de leitura grande usa para saber o que veio da busca (11).
- **Fora da escolha:** memtomem, zvec-grep, ck, turbovec, markdown-vault-mcp; nenhuma decisão as traz (19, 20, 21, 50).

### Testing decisions

- **Costura:** hub de ensaio (cópia do que o maestro gera na forma do ticket 12, com notas em pt-BR e en, duas
  iniciativas com o núcleo, um binário pequeno, um `.secrets/`, uma pasta `local: true`, um `.pdf.md` e uma nota com YAML
  inválido) na worktree da faixa; HOME de ensaio para os três harnesses; servidor de busca em 127.0.0.1 numa porta de
  ensaio. Nada em `~/.claude`, `~/.codex` ou `~/.copilot`.
- **Pelo MCP, por script:** um cliente MCP chama a busca e confere o caminho da nota esperada entre as três primeiras
  (o mesmo critério do núcleo; o limite é **[aceita]**: a bancada do 09 mediu acerto nos 5 primeiros e posição, sem
  fixar limite de produto).
- **Pelos harnesses reais, não interativos:** `claude -p` com HOME de ensaio e o MCP de busca registrado; Codex e Copilot
  CLI do mesmo jeito, se o login no HOME de ensaio for liberado (pergunta do plano). O teste confere que o harness chamou
  a ferramenta de busca e devolveu o caminho certo; não confere a redação da resposta.
- **Comportamentos verificados:**
  - nota nova em pt-BR, criada no disco do hub de ensaio com o servidor ligado, aparece por palavra do texto e por uma
    pergunta escrita com outras palavras, sem comando de reindexar, e o tempo até aparecer só é medido e
    gravado, sem limite de aceite (Gustavo, 2026-10-16); o gatilho da Robusta do 09, "gravação visível em segundos", continua valendo);
  - consulta em inglês acha nota em inglês no mesmo índice;
  - nada com ponto no caminho (`.secrets/`, `.git`, `.maestri/`) nem da pasta `local: true` aparece em resultado;
  - o `.pdf.md` aparece; o binário não;
  - a nota com YAML inválido fica fora do índice (09); o teste exige a contagem de `.md` válidos indexados (`status`) e
    um relatório das notas recusadas por YAML inválido (**[aceita]**; nenhum ticket escolhe esse relatório); um aviso
    operacional além disso segue aberto;
  - rajada de 200 arquivos copiados de uma vez: todos achados, com o tempo medido;
  - o servidor recusa conexão por endereço que não seja 127.0.0.1 (o `--allowed-host`);
  - o gemini: a configuração existe, roda uma vez num índice ao lado do arctic e volta desligada (desenho decidido no
    09); a busca padrão segue no arctic. Antes de rodar, as chamadas são orçadas pelo limite diário do provedor no
    FreeLLMAPI; a autorização e a cota para essa rodada única são pergunta aberta do 16, rodada 2 **[formato]**;
  - o fragmento de kit roda duas vezes sem mudar nada na segunda, e o `-WhatIf` não grava nada.
- **Critério de aceite de ponta a ponta (sem a segunda máquina):** uma nota nova em pt-BR gravada no hub de ensaio
  aparece na busca pelo MCP, por palavra e por sentido, chamada por um harness real em modo não interativo com HOME de
  ensaio, com o servidor só em 127.0.0.1 e o índice fora do banco e do git.

### Out of scope

- O proxy de MCP para clientes (TBXark/mcp-proxy, rotas e tokens) e o kit de cliente: faixa 10 (14).
- Registrar o MCP de busca nos arquivos de cada harness: faixa 8 junta o fragmento (14).
- O hook que avisa leitura grande fora da busca: faixa 6 (11).
- A Robusta construída de verdade: só volta por gatilho (09).
- Ligar o gemini: escolha do Gustavo, sem gatilho decidido (54).
- Rerankers, embeddings melhores, cópia leve para sandbox, serviço de busca na rede, duas vias juntas: Radar, com gatilho
  (09, 54).
- Stemmer de português: um analisador só, sem stemmer (09).
- O FreeLLMAPI nativo no notebook pessoal e a busca pela tailnet entre os pares: outra execução (16, plano).
- A extração de texto dos anexos (Docling, OCR em português): fora desta faixa (12).
- A busca no WSL (04).

### Pontos abertos para a construção

- **Não verificado (09):** autenticação do servidor HTTP do obsidian-hybrid-search (o README só fala do cabeçalho
  Host); se ele roda um segundo índice ao lado do arctic (se não rodar, é gatilho da Robusta); o tempo de uma edição até a
  busca com o CLI do LiveSync ligado.
- **Formatos de texto:** a 0.16.2 só indexa `.md`, conferido na fonte do pacote (`indexer.js`, `db.js`) na rodada 16 do
  12, posterior à lacuna do 09; `.txt` e `.csv` entram na busca só por uma vista textual em Markdown. O teste da
  construção confirma a configuração instalada, sem reabrir a dúvida.
- **Contradição de texto:** o Answer do 09 diz "servindo a busca por MCP em HTTP na tailnet"; o 14, posterior, prende a
  busca a 127.0.0.1 e leva os clientes pelo proxy. Esta spec segue o 14.
- **Notas com YAML inválido:** o relatório da busca (contagem e lista) é o canal **[aceita]** (ver Testing decisions);
  um aviso a mais pelo verificador da faixa 1 ou pela vigia da faixa 7 segue aberto.
- **Como o servidor de busca sobe e volta quando cai** (tarefa agendada, laço no terminal durante a hora): não decidido
  **[formato]**.
- **Se a ferramenta ignora sozinha pastas e arquivos com ponto** ou se precisa da lista de exclusões: não verificado;
  o requisito (nada com ponto na busca) vale de todo jeito (12).
- **Dono do gerador de exclusões** (12 decide o gerador, não o worker): o núcleo o atribui à faixa 1; o dono é
  **[formato]**.
- **Ordem ao subir um par novo:** o sincronizador faz uma varredura de partida em rajada; medir se a reindexação aguenta
  sem duplicar trabalho (09, item 5 da recomendação da pesquisa 50).
- **O gatilho e a forma de ligar o gemini** não foram decididos (54); com o par pessoal fora do ar, o notebook fica sem o
  gemini (16), o que só importa se ele for ligado.

## Faixa 4: Banco e vista `.md`

A verdade do hub mora num banco, e o `.md` é a vista editável do Gustavo, de mão dupla (22). O banco é o do
Self-hosted LiveSync no CouchDB (25), um CouchDB em cada par, com replicação mestre-mestre pela tailnet (34). O
sincronizador é o CLI do LiveSync como tarefa agendada, e o plugin fica no Obsidian como interface e janela de conflito
(33, 48). Nesta execução a faixa prova o "primeiro teste" do ticket 34 sem a segunda máquina: dois CouchDB locais em
portas diferentes fazem de par A e par B.

### User stories

1. Como Gustavo, quero editar um `.md` no Obsidian e ver a edição chegar ao banco, para que a vista seja de mão dupla
   (22, 30).
2. Como Gustavo, quero ver no `.md` o que um agente gravou pelo MCP do banco, em segundos, para que a vista mostre a
   verdade (25, 30: cerca de 0,2 s).
3. Como agente que troca um trecho direto no disco, quero que o sincronizador leve a mudança ao banco sem eu fazer nada,
   para que o sync não dependa de quem gravou (07, 11, 33).
4. Como agente que cria um arquivo novo no disco, quero que ele vá ao banco e à outra máquina, para que o arquivo novo
   tenha o mesmo caminho que a edição (11, 33).
5. Como Gustavo, quero que o disco e o banco fiquem ligados com o Obsidian fechado, para que o hub funcione sem o
   Obsidian aberto (33, 48).
6. Como Gustavo, quero que o Obsidian com o plugin seja só para ver, editar ou resolver conflito, para que fechá-lo não
   pare nada (33).
7. Como Gustavo, quero que cada máquina envie as próprias mudanças à outra, para que o aviso de sync parado nasça na
   máquina que travou (34, R62).
8. Como Gustavo, quero que nenhum par seja a referência do outro, para não depender de uma máquina fixa como host (34).
9. Como Gustavo, quero que o primeiro par nasça nesta máquina e funcione sozinho até o segundo existir, para começar logo
   sem nada a refazer depois (34: S1 até o segundo par).
10. Como Gustavo, quero que uma nota editada na pasta do par A apareça na pasta do par B, e o contrário, para provar a
    replicação entre dois CouchDB antes da segunda máquina (34, 16: primeiro teste).
11. Como Gustavo, quero que, se a replicação entre dois CouchDB falhar no primeiro teste, a volta seja a S1 (um CouchDB
    só), para ter um plano B decidido (34).
12. Como Gustavo, quero que duas edições no mesmo trecho da mesma nota, em pares diferentes, virem colisão real com as
    duas versões guardadas no banco, para que nada seja sobrescrito em silêncio (08, 30, 33).
13. Como Gustavo, quero que uma colisão real de texto segure só aquela nota, para que o resto continue viajando (33).
14. Como Gustavo, quero que mudanças em trechos diferentes da mesma nota se juntem sozinhas, para não ver colisão onde
    não há (08, 33).
15. Como Gustavo, quero que a colisão resolvida num par limpe o aviso no outro, sem conflito fantasma, para não resolver
    duas vezes (30).
16. Como Gustavo, quero ver a colisão no Obsidian (modal, faixa na nota e contador) quando o plugin está aberto, para
    resolver com os olhos na nota (30, 48).
17. Como Gustavo, até a tela de três vias chegar, quero escolher uma das versões e reeditar à mão, sem o "Concat both",
    para não receber texto mutilado (25, 30).
18. Como Gustavo, quero que só `.md`, `.txt` e `.csv` sejam texto, com junção automática, e o resto seja binário, para
    saber o que se junta e o que não (33, 48).
19. Como Gustavo, quero que, numa colisão de binário, a versão mais nova fique e a perdida continue no banco num ramo
    apagado, para que a vigia ache e um comando a recupere (33: R71; 48).
20. Como Gustavo, quero que todo arquivo comum até 200 MiB vá ao banco, no CLI e no plugin, para que docx, xlsx e PDFs
    grandes viajem (33: R68, R76).
21. Como Gustavo, quero que um arquivo acima de 200 MiB fique fora do banco de um jeito que a vigia consiga listar, para
    que o arquivo que não viaja não seja silencioso (33, 48).
22. Como Gustavo, quero que nada com ponto no nome, pasta ou arquivo, em qualquer nível, vá ao banco, para que `.git`,
    `.secrets/`, `.maestri/`, `.venv` e o índice da busca fiquem em cada máquina (12, 16, 33).
23. Como Gustavo, quero que a varredura de partida do CLI também respeite a exclusão de pastas com ponto aninhadas, para
    que o defeito visto no teste (`projeto/.git` e `.venv` vazando) não chegue ao outro par (48).
24. Como Gustavo, quero que a pasta cujo `index.md` diz `local: true` fique fora do banco, pela exclusão gerada a partir
    desses marcadores, para que a pasta não replicada fique numa máquina só (12).
25. Como Gustavo, quero o banco com E2EE do LiveSync, para que o CouchDB e a replicação só levem pedaços cifrados (34, 48).
26. Como Gustavo, quero que a frase-senha da E2EE e o Setup URI viajem por canais separados, para que um vazamento sozinho
    não abra o hub (34).
27. Como Gustavo, quero o CouchDB com senha e alcançável só pela máquina e pela tailnet, nunca pelo Funnel, para que o
    banco não fique exposto (34).
28. Como maestro, quero subir um par novo com o kit de par (script e `.env` modelo: Tailscale, compose CouchDB + MCP,
    replicação, Setup URI), com o mínimo de passos, para que qualquer computador vire par (16, 34).
29. Como maestro, quero que o kit suba o sincronizador antes do plugin em cada máquina, para que o CLI refaça a raiz dos
    arquivos que não conhece uma vez só (33, 48).
30. Como maestro, quero que o kit aceite cada dispositivo novo com `mark-resolved`, para que o CLI não fique recusado
    ("not yet accepted") (33, 48).
31. Como maestro, quero que o kit configure o CLI pelo caminho dos testes oficiais, e não copiando o `data.json` do
    plugin, para não repetir o que falhou no teste (48).
32. Como maestro, quero que o CLI rode como tarefa agendada (no logon, repetindo a cada minuto, sem segunda instância),
    para que ele volte em até 1 minuto depois de cair ou de o CouchDB estar fora na partida (33, 48).
33. Como maestro, quero que o plugin entre num cofre novo por um Setup URI copiado de um par que funciona e depois aponte
    para o CouchDB local, para não passar pelo assistente de dez telas que recria o banco (30, 34).
34. Como maestro, quero que a configuração do plugin deixe Sync Mode = LiveSync, o limite de 200 MiB, a exclusão `**/.*`
    e a E2EE, com o "Hidden File Sync" desligado, para que o cofre não termine o assistente com o sync desligado (30, 33,
    09).
35. Como maestro, quero que o kit seja idempotente, leia o HOME de ensaio e aceite `-WhatIf`, para rodar de novo sem
    estrago e ensaiar sem tocar no global (plano: contrato do instalador).
36. Como faixas 5 e 7, quero o compose de ensaio da faixa 4 publicado nos primeiros 10 minutos da hora, para subir cada
    uma o seu CouchDB descartável em porta própria (5996 e 5997) sem esperar (plano: fronteiras).
37. Como vigia da faixa 7, quero que as replicações sejam tarefas do CouchDB visíveis no estado do agendador de
    replicação, para ler se o sync parou (33).
38. Como vigia da faixa 7, quero que os conflitos abertos e os ramos apagados de binário fiquem no banco e consultáveis,
    para avisar colisão e binário descartado (33).
39. Como checagem de início de sessão, quero saber a hora da última troca com a outra máquina, para informar o agente
    quando a outra está desligada (33: R63).
40. Como Gustavo, quero que o banco guarde o histórico de revisões e as folhas em conflito e as replique com ele, para que
    a colisão exista nos dois pares (25, 30).
41. Como Gustavo, quero que o CLI aguente o CouchDB caindo no meio e um kill, para que uma queda não corrompa o sync (48).
42. Como Gustavo, quero que o hub more no NTFS, em `C:\context-hub`, nas duas máquinas, com o WSL fora, para seguir a
    regra de guardar os arquivos do lado de quem trabalha neles (03, 04).
43. Como Gustavo, quero que plugin e CLI fiquem sempre ligados na mesma pasta (o "jeito 1"), e nunca em revezamento, para
    não criar conflito falso em todo arquivo que o CLI baixou (48).
44. Como agente de um cliente, quero ler o hub pelo MCP de um par sem cópia própria nem credencial do CouchDB, para usar
    o hub de uma sandbox (34; o kit de cliente é da faixa 10).

### Implementation decisions

- **Verdade e vista (22, 25):** a verdade mora no banco do LiveSync no CouchDB. Cada nota é um documento de metadados
  (`children`) mais pedaços com o texto; histórico de revisões e folhas em conflito moram no banco e replicam com ele
  (25, 30). O `.md` no disco é a vista viva de mão dupla.
- **Topologia, S3 (34):** um CouchDB em cada par, mestre-mestre. Cada par dispara a replicação das próprias mudanças para
  o outro (uma tarefa de envio por par), em vez de duas tarefas numa máquina só (34, comentário R62; 33). Até o segundo
  par existir, um par só funciona sozinho (S1, sem nada a refazer). Se o primeiro teste falhar, a volta é a S1.
- **Elos dentro de cada par (33, 48):** o CLI do LiveSync (`daemon`, do commit `14141446`, construído no Windows sem
  compilador) é o sincronizador, sempre ligado; o plugin LiveSync 1.0.35 no Obsidian, quando aberto, é interface e janela
  de conflito. Os dois sempre ligados na mesma pasta (jeito 1 do ticket 48). Os escritores do disco são os agentes, o
  sincronizador e o plugin (33).
- **Servidor:** CouchDB 3.5.2 pelo compose do spike, com o `couchdb-init.ini` do es617 (passa no "Check server
  requirements"), `max_document_size` de 50 MB (o maior pedaço tem cerca de 5,6 MB) (30, 47, 34). Sem `[admins]` fixo
  no `.ini`: usuário e senha de ensaio gerados pelo kit; nada copiado do spike, que tem arquivo de credencial (crivo
  do Prumo 2, item 7). Contêineres `hub-ensaio-04-a` e `hub-ensaio-04-b`. O compose tem o lugar
  do MCP do banco; o fork com `base_rev` é da faixa 5 (25).
- **Tamanho:** `syncMaxSizeInMB` = 200 no CLI e no plugin (33).
- **Texto e binário:** só `.md`, `.txt` e `.csv` são texto, com junção; o resto é binário, guardado em pedaços Base64
  (+33% na primeira versão; versões seguintes reaproveitam pedaços) (33, 48). Colisão de binário: a versão de `mtime`
  mais novo fica, e a perdida fica num ramo apagado, recuperável por script, também depois da compactação (33, 48; o
  comando de recuperar é da faixa 7).
- **Exclusão (12, 16, 33, 09):** nada com ponto no nome, em qualquer nível, vai ao banco: a regra cobre arquivos e pastas
  (`**/.*` e `**/.*/**`, com casamento `dot: true`), no CLI e no plugin; o "Hidden File Sync" do plugin fica desligado.
  No CLI, a regra vai no `.livesync/ignore` da raiz do cofre, com as linhas `.*` e `.*/`: o `IgnoreRules.ts` do CLI
  normaliza para `**/.*` e `**/.*/**`, troca `\` por `/` e casa com `dot: true`. A regra embutida do CLI corta o caminho
  por `path.sep`, o que explica o vazamento das pastas com ponto aninhadas no Windows (48, defeito 8; inferência pela
  fonte, não verificada).
  As pastas com `index.md` `local: true` entram na exclusão por um script que a gera a partir desses marcadores (12).
- **Segurança (34):** senha do CouchDB; E2EE do LiveSync, com a frase-senha também no MCP do banco (30); Setup URI e
  frase-senha por canais separados; tudo só pela tailnet, nunca o Funnel; cada par guarda a cópia completa e a
  frase-senha, e a regra de dado de cliente vale para cada um (34; mapa, Q3).
- **Ordem de subida de um par (33, 48):** CouchDB → banco e parâmetros do LiveSync → CLI configurado pelo caminho dos
  testes oficiais → `mark-resolved` do dispositivo → varredura de partida do CLI → plugin pelo Setup URI apontando para o
  CouchDB local. O MCP do banco sobe depois do banco pronto ou é reiniciado, porque perde o feed quando o banco é recriado
  (30).
- **Sincronizador como tarefa agendada (33, 48):** gatilho no logon e repetido a cada minuto, com "não abrir segunda
  instância"; o "reiniciar se falhar" do Agendador não religa o processo e não é usado.
- **Kit de par, parte do banco (16, 34):** script e `.env` modelo com: Tailscale; compose CouchDB + MCP; replicação;
  Setup URI. O fragmento da faixa segue o contrato do instalador: idempotente, HOME por `HUB_HOME_ENSAIO`, `-WhatIf`.
  A parte do Tailscale (instalar só no Windows, grants, modo unattended na máquina pessoal) entra no kit e é executada
  em outra execução, com o Gustavo (05, 34, plano). Sem consulta ao TI antes do Tailscale no notebook: o TI já
  confirmou que não há risco nem conflito com o software corporativo (16, 2026-10-16).
- **Para a vigia e a checagem (33):** as replicações ficam como tarefas do CouchDB que aparecem no `_scheduler/docs`; os
  conflitos abertos, os ramos apagados de binário e os arquivos acima do limite ficam consultáveis no banco e no disco.
  Com E2EE o caminho no CouchDB é cifrado; o próprio CLI dá o caminho em claro (`ls`, `info <caminho>` com os
  conflitos) e tira uma revisão para arquivo (`pull-rev`, `cat-rev`), o que serve ao comando de recuperar binário. A
  vigia em si é da faixa 7.
- **Compose de ensaio publicado (plano):** nos primeiros 10 minutos da hora (`agents/code/kit/par/banco/compose.yml` e
  `agents/code/kit/par/env/04.env`), para as faixas 5 (porta 5996) e 7 (5997); a faixa 4 usa 5994 (par A) e 5995 (par B), tudo em
  127.0.0.1 (a 5984 é do spike). No minuto 15, exemplos reais do `_scheduler/docs` (em dia e parado) em
  `execucao/ensaio/banco/`, para as faixas 7 e 10.
- **Conferir a versão ao gravar (08, 33):** a garantia fica; no banco ela é do MCP modificado (faixa 5); no disco, do hook
  e da troca de trecho (faixa 6). O sincronizador conta como mais um escritor, e por isso a trava por arquivo não serve
  (08).
- **Caminhos que saíram (06, 07, 23, 24, 25, 31):** o GitHub deixa de ser ponto de encontro e vira só cópia de segurança
  diária (faixa 10); o git-sync sai; CRDTs ficam fora (resolvem colisão em silêncio); o FNS fica fora; o Dolt segue
  reserva nomeada; ferramentas de memória de agentes não servem de hub.

### Testing decisions

- **Costura:** hub de ensaio copiado duas vezes, como pasta A e pasta B; dois CouchDB descartáveis do compose de ensaio
  em 127.0.0.1 (5994 e 5995), com `.env` de ensaio; dois CLI do LiveSync, um por pasta, cada um com o seu banco local;
  uma tarefa de replicação em cada CouchDB enviando ao outro; E2EE ligada com a mesma frase-senha de ensaio. O CLI roda
  em laço no terminal durante a hora, sem tarefa agendada de verdade (pergunta do plano); o kit escreve a definição da
  tarefa e é conferido no `-WhatIf`. Tudo é apagado ao fim.
- **Ordem de corte na hora (risco de tamanho do Prumo 2) [formato]; os requisitos do 33 (200 MiB, binário recuperável,
  sincronizador agendado) seguem obrigatórios em qualquer formato:** núcleo primeiro (dois CouchDB e as duas replicações
  visíveis no agendador; nota A → B e B → A sem texto claro no banco; colisão de texto com as duas folhas; exclusão do
  que tem ponto, com o CLI rodando e na varredura de partida). Se sobrar, nesta ordem: 60 e 201 MiB; colisão de
  binário; o kit de novo sem mudança e o `-WhatIf`; o laço que religa; o retrato para as faixas 5 e 7; o harness real.
  O resto dos comportamentos abaixo fica para a próxima execução. Prova num comando: `pwsh agents/test/04-banco.ps1`.
- **Pelos scripts:** criam, editam, apagam e copiam arquivos nas pastas e consultam os dois CouchDB (documentos,
  conflitos, estado da replicação).
- **Pelos harnesses reais, não interativos (só com o login de ensaio; pergunta aberta do 16, rodada 2 **[formato]**):**
  `claude -p` com HOME de ensaio grava uma troca de trecho e um arquivo novo na pasta A; o teste confere a chegada na
  pasta B. Pelo MCP do banco, quando a faixa 5 entregar o fork; até lá, o MCP do es617 sem fork só para provar o caminho
  banco → disco **[formato]** (com etapas sequenciais, o fork real).
- **O plugin no Obsidian não é exercido por script** (testes com o Obsidian só capturam tela, sem mouse nem teclado):
  a configuração do plugin pelo Setup URI e o modal de colisão ficam como verificação `ready-for-human`, com roteiro.
- **Comportamentos verificados:**
  - edição na pasta A chega à pasta B, e da B à A, com o tempo medido;
  - arquivo novo, exclusão e rajada de arquivos atravessam;
  - mesma linha editada nas duas pastas com a replicação pausada: depois de religar, as duas folhas existem nos dois
    bancos, nenhuma versão some, e o conflito é listável; edições em linhas diferentes se juntam;
  - colisão de binário: a versão mais nova fica nas duas pastas e a perdida está num ramo apagado do banco;
  - arquivo de 60 MiB viaja (prova o limite de 200 acima do padrão de 50); arquivo acima de 200 MiB não viaja e fica
    identificável;
  - arquivo e pasta com ponto, na raiz e aninhados (`projeto/.git`, `.venv`, `.secrets/`, `.obsidian-hybrid-search.db`),
    não vão ao banco, nem com o CLI rodando nem na varredura de partida depois de reiniciar o CLI;
  - pasta com `index.md` `local: true` não vai ao banco;
  - com E2EE, nenhum texto claro de nota aparece nos documentos do CouchDB;
  - CLI morto e CouchDB fora na partida: o laço religa e o sync retoma sem perda;
  - dispositivo novo recusado até o `mark-resolved`, aceito depois;
  - as duas tarefas de replicação aparecem no estado do agendador de replicação de cada CouchDB;
  - o fragmento de kit roda duas vezes sem mudar nada na segunda; o `-WhatIf` não grava nada.
- **Critério de aceite de ponta a ponta (sem a segunda máquina):** com dois CouchDB locais em portas diferentes fazendo
  de par A e par B, uma nota editada na pasta A (por script e por um harness real em modo não interativo) aparece na
  pasta B, e o contrário; uma colisão forjada guarda as duas versões nos dois bancos; nada com ponto no nome atravessa.

### Out of scope

- O fork do MCP do es617 com `base_rev`, o conflito visível ao agente, o `instructions` e as descrições das ferramentas:
  faixa 5 (25, 11, 41).
- A vigia, a notificação do Windows, o mod do Claude Code e o comando de recuperar binário: faixa 7 (33).
- A checagem de início de sessão: faixas 2 e 7 (08, 33).
- O `.git` de cópia de segurança diária, as deploy keys, o `_archive/` e o kit de cliente com `mcp-proxy`: faixa 10 (06,
  33, 34, 14).
- O segundo par (notebook pessoal), o Tailscale instalado de verdade, os grants e a replicação real pela tailnet: outra
  execução, `ready-for-human` (plano).
- A tela de colisão de três vias editável (fork do modal do LiveSync): logo depois da construção, como melhoria (25).
- Edição concorrente entre o Obsidian e um agente no mesmo arquivo (mapa, Q4).
- A pasta não replicada servida por SSH e a operação remota (mapa; 05, 06).
- Dolt (reserva), FNS, CRDTs, git-sync, livesync-bridge (24, 25, 31, 33, 47).
- O WSL (04).
- O GC V3 dos pedaços de binário e o `customChunkSize` (47, 48: não testados).
- Validar o esquema do frontmatter no MCP do banco (12; faixas 1 e 5).

### Pontos abertos para a construção

- **Primeiro teste (34, 16):** "LiveSync com dois CouchDB replicando entre si" é não verificado; inclui a replicação nos
  dois sentidos dos documentos de controle do LiveSync (26, não verificado).
- **Quem cria o banco e os parâmetros do LiveSync no primeiro par** (o assistente do plugin destrói e recria o banco; o
  CLI se configura pelo caminho dos testes oficiais: `init-settings`, `remote-add` com a string de conexão
  `sls+https://...`): não decidido. O Setup URI sem o assistente: o CLI só aplica (`setup <URI>`); gerar é
  `encodeSettingsToSetupURI` da `livesync-commonlib`, que o teste do próprio CLI chama (não verificado de ponta a ponta).
- **Exclusão de pastas com ponto aninhadas na varredura de partida:** o defeito visto no 48; `.livesync/ignore` não foi
  testado, mas existe na fonte do CLI (`IgnoreRules.ts`, ver "Exclusão" acima); a regra precisa ser testada nos dois
  clientes (12, 16, 33, 48).
- **Comportamento acima de 50 MiB com o limite em 200:** testar (33); acima de 200 MiB o arquivo fica fora sem aviso e o
  que cresce além do limite para de sincronizar em silêncio (48): a faixa 7 depende de como identificar esses arquivos.
- **Colisão vista só pelo CLI:** com o plugin fechado, o conflito fica aberto até um `resolve` e só aparece no log (47,
  48); o que o disco mostra nesse intervalo não foi verificado.
- **Convivência longa de plugin e CLI** (horas ou dias), Ctrl+C, cópia vinda do OneDrive, Word e Excel regravando o
  arquivo, plugin com E2EE: não testados (48). A issue aberta #835 do CLI com E2EE (47).
- **Config Doctor:** depois de atualizar o plugin, ele abre e para o sync daquele cofre até alguém responder (48); a vigia
  confere (faixa 7), mas falta decidir se o kit prende a versão do plugin.
- **Forma da tarefa de replicação** (persistente, visível no `_scheduler/docs`): o mecanismo exato não foi verificado.
- **Endereço do CouchDB para a replicação real:** só pela tailnet (34); a forma de prender o CouchDB à interface da
  tailnet não foi decidida.
- **Docker Desktop e Tailscale:** o TI confirmou que o Tailscale no notebook não tem risco nem conflito com o software
  corporativo (16, 2026-10-16), o que fecha a parte corporativa do risco do 05 (MDM, VPN); o conflito com Docker Desktop
  e WSL segue não verificado nesta máquina. O CouchDB tem MSI com opção de serviço como alternativa ao contêiner (26),
  não escolhida.
- **CouchDB descartável no Docker local:** o Gustavo vai ligar o Docker Desktop (16, 2026-10-16); os CouchDB de ensaio
  em contêiner, em 127.0.0.1, dependem só disso. Dúvida ao maestro: o fato diz que ele liga o Docker, não que libera
  contêineres de ensaio; a costura supõe que sim.
- **Portas de ensaio:** 5994 a 5997, fora da 5984 do spike do ticket 30; o kit confere que estão livres antes de subir.
- **Espaço dos binários:** pedaços se acumulam e não saem com a compactação nem ao apagar o arquivo; só o GC V3 (beta,
  manual) os remove (47, 48). Sem decisão de limpeza.
- **Instâncias do MCP do es617 por par:** leitura por padrão e escrita ligável, com guarda de versão e credenciais
  separadas, são requisitos (11, 14, 34). Três instâncias locais: leitura, escrita dos agentes do par e escrita só do cliente,
  separada (Gustavo, 2026-10-16); as três juntas no mesmo par: não verificado (34).
- **Rede do notebook para o GitHub** (porta 22 ou 443), para a cópia de segurança: não verificado (06; faixa 10). O
  repositório privado novo (16, 2026-10-16) leva uma deploy key por máquina, com escrita, só nele (06, mantido pelo 33).
- **Dono do gerador de exclusões** a partir de `local: true` (12): o núcleo o atribui à faixa 1; o dono é **[formato]**.
  O destino no CLI é o `.livesync/ignore` (uma linha `pasta/` por pasta local); sem importar o `.gitignore` inteiro,
  que a busca também lê.
