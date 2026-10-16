# Arquitetura de pastas e frontmatter do hub

Type: prototype
Status: resolved
Blocked by: 02, 10, 25, 34, 35, 36, 40

## Question

Que árvore de pastas e que frontmatter o hub usa, incluindo como uma pasta se declara **pasta não
replicada** (Q15)? O protótipo é um esboço da árvore com notas de exemplo. Leva em conta as lições do
vault.

## Comments

- 2026-10-02 (vinda de "Workloads piloto"): a árvore precisa receber, nas primeiras fases, cópias de
  `knowledge/armis-docs`, `knowledge/armis-brand` e da skill `armis-docx` do vault, que passam a ser
  trabalhadas e melhoradas no hub. O hub é a casa de tudo; não há ponteiro nem registro do vault.
- 2026-10-04 (vinda de "Contrato file-first: zonas e checkpoint"): cada trabalho tem uma nota de
  retomada num lugar fixo, que a pasta onde a sessão abre permite achar sem busca. A árvore decide
  onde ela fica e o frontmatter dela.
- 2026-10-04 (vinda de "Markdown: vista ou fonte da verdade"): em revisão: a verdade mora num banco; a árvore de pastas e o frontmatter passam a descrever a vista Markdown, e o modelo do banco é outra pergunta.
- 2026-10-06 (conferência da fronteira): passa a esperar "Onde o servidor mora". Com a verdade no
  banco, como uma pasta fica de fora da outra máquina depende da topologia: num servidor central ela
  fica fora do banco; com um CouchDB por máquina (S3) pode ser replicação filtrada; numa VPS (S4) o dado
  de cliente sai das máquinas, o que pode mudar quais pastas entram no banco.
- 2026-10-10 (vinda de "Onde o servidor mora"): S3, um CouchDB por par. A pasta não replicada pode
  ser uma replicação filtrada entre pares (a replicação do CouchDB aceita filtro) ou ficar fora do banco.
- 2026-10-10: rodada 1 aberta na nota "Rodada atual" do Maestri (R13, o eixo do primeiro nível:
  por iniciativa, por tipo, por zona ou quase plana). Recomendação: por iniciativa. Página em
  [`prototipo-12-pastas.html`](../prototipos/prototipo-12-pastas.html). Próximas rodadas: dentro da
  pasta da iniciativa; frontmatter; pasta não replicada (o filtro por caminho no LiveSync e na
  replicação do CouchDB não foi verificado).
- 2026-10-10, resposta à R13 (rodada 1): o Gustavo não entendeu o que a pergunta decidia; quatro
  opções soltas, sem nexo com o uso real dele, para uma escolha importante. Quer primeiro descobrir os
  tipos de pasta de nível raiz, com sugestões. A escolha do eixo fica suspensa. Rodada 2 aberta na nota
  "Rodada atual": inventário de tipos de raiz tirados do que ele usa hoje (pastas de projeto, iniciativas
  do vault, workspaces do Maestri); a página foi refeita para essa descoberta.
- 2026-10-10, resposta à R14 (rodada 2): o Gustavo gostou dos nove tipos de raiz (clientes, operações
  contínuas, produtos e frentes próprias, estudo e laboratório, conhecimento de referência, oficina dos
  agentes, entrada, arquivo, pessoal?) e quer antes uma comparação com métodos conhecidos. Virou a
  pesquisa "Métodos conhecidos de organizar a raiz", que agora bloqueia este ticket.
- 2026-10-10 (vinda de "Métodos conhecidos de organizar a raiz"): proposta de seis raízes mais o
  pessoal condicional, `_arquivo/` dentro de cada raiz. Rodada 3 aberta na nota "Rodada atual" (R15).
  Ficam para testar aqui: arquivar por pasta ou por propriedade, e captura de cliente na máquina
  errada.
- 2026-10-10, resposta à R15 (rodada 3): **fechadas as seis raízes**: clientes, operações
  contínuas, iniciativas sem cliente, conhecimento de referência, oficina dos agentes e entrada;
  `_arquivo/` dentro de cada uma. Fatos do Gustavo: o SOC STRATA é operação contínua; **por enquanto
  tudo vive nas duas máquinas, inclusive o conteúdo de cliente** (ele trabalha com cliente também na
  máquina pessoal); o pessoal replica, então não há raiz pessoal (cai em iniciativas sem cliente ou
  referência); spike às vezes vira produto (confirma a junção). Um mecanismo de controle de acesso por
  pasta (na camada de busca, como guardrail no AGENTS.md ou outro) virá depois, fora deste projeto e
  sem ticket. Consequência a rever na rodada sobre o conteúdo das raízes: a entrada só era local por
  causa da captura de cliente na máquina errada, que deixou de ser problema.
- Pedido junto: a oficina dos agentes vira `.agents/` com um `AGENTS.md`, funcional desde a criação.
  Conferido em fonte primária antes da rodada 4:
  - Claude Code (`code.claude.com/docs/en/memory.md`, seção "When Claude Code reads AGENTS.md"): lê
    o `AGENTS.md` do diretório de trabalho e dos de cima quando não há `CLAUDE.md` contando (v2.1.277
    ou mais nova); **"Not read: ... anything under a `.agents/` directory"**. O `~/.claude/CLAUDE.md`
    não conta e carrega junto.
  - LiveSync (`docs/tips/hidden-file-sync.md`): pastas que começam com ponto só replicam pela Hidden
    File Sync, "an advanced, optional feature ... separate from ordinary note synchronisation",
    desligada durante Rebuild e Fetch, com padrões de alvo por regex.
  - Obsidian (`How Obsidian stores data.md` do obsidian-help): só diz que o sistema operacional
    esconde pastas com ponto. Se o explorador do Obsidian mostra `.agents/`: **não verificado**.
  Rodada 4 aberta na nota "Rodada atual" (R16: onde fica o `AGENTS.md` e o nome da pasta da oficina).
- 2026-10-10, resposta à R16 (rodada 4): **A**. O `AGENTS.md` fica na raiz do hub (lido
  nativamente pelo Claude Code desde a criação, quando a sessão abre dentro do hub) e a oficina dos
  agentes é a pasta `agents/`, sem ponto, que replica pela sync normal do LiveSync. Sessões fora do hub
  continuam recebendo o contrato pela camada global de cada harness. Rodada 5 aberta na nota "Rodada
  atual" (R17: nomes das seis raízes).
- 2026-10-10, resposta à R17 (rodada 5): **nomes em inglês**. Raiz do hub: `AGENTS.md`,
  `clients/`, `operations/`, `initiatives/` (iniciativas sem cliente; o Gustavo trocou `ventures`
  por `initiatives`), `reference/`, `agents/`, `inbox/`, e `_archive/` dentro de cada raiz. Como a
  palavra "iniciativa" do glossário também cobre as de cliente, o glossário ganhou o termo **Raiz**,
  que diz onde cada iniciativa mora. Rodada 6 aberta na nota "Rodada atual" (R18: quantos níveis até
  a pasta de uma iniciativa).
- 2026-10-10, resposta à R18 (rodada 6): ok. **Dois níveis em `clients/`**
  (`clients/<cliente>/<iniciativa>/`, com o nível do cliente guardando o que é comum às iniciativas
  dele) e **um nível nas outras raízes** (`operations/<operação>/`, `initiatives/<iniciativa>/`,
  `reference/<assunto>/`); `agents/` por tipo de peça (`skills/`, `roles/`, `machines/<máquina>.md`).
  Com tudo replicando, o perfil de máquina é um arquivo por máquina, sem pasta não replicada. Rodada 7
  aberta (R19: o que fica dentro da pasta de uma iniciativa).
- 2026-10-10, resposta à R19 (rodada 7): suspensa. Antes de decidir o que fica dentro da pasta
  de uma iniciativa, e talvez revendo a R18, o Gustavo quer pensar em todas as formas de chegar ao hub.
  Virou "Portas de entrada do hub", que agora bloqueia o resto deste ticket. Ficam valendo as rodadas 3
  a 5 (seis raízes, nomes em inglês, `AGENTS.md` na raiz, oficina em `agents/`); a R18 (níveis) fica
  em revisão até as portas. Ticket liberado (open) enquanto espera.
- 2026-10-12 (vinda de "Portas de entrada do hub"): passa a esperar também "Maestri: padrão e
  liberdade", que decide onde moram papéis e partituras (hoje previstos em `agents/roles/`).
- 2026-10-12 (vinda de "Portas de entrada do hub", resposta à R30): **a R18 sai de revisão**. Dois
  níveis em `clients/` e um nas outras raízes voltam a valer; nenhuma porta depende da profundidade.
  A R19 (o que fica dentro da pasta de uma iniciativa) volta a ser a próxima pergunta daqui. Decidido
  também nas portas: cofre do Obsidian na raiz; `_archive/` mantido, movido por script que confere o
  outro par; nenhum `CLAUDE.md` no hub; marcador de raiz para o Codex; `AGENTS.md` em caminho fixo e
  skills em `agents/skills/<skill>/`.
- 2026-10-12 (vinda de "Maestri: padrão e liberdade", resolvido): a árvore precisa acomodar
  `agents/skills/maestro-*/` (catálogo e um arquivo por peça), `agents/maestro/propostas/`,
  `agents/maestro/uso/<máquina>.md` e uma pasta `maestro/` opcional dentro de cada iniciativa (a
  personalização local; nada com ponto, que não replica). O workspace de uma iniciativa abre na pasta
  dela, e o Maestri grava `.maestri/roles/` ali (fica em cada par).
- 2026-10-14 (vinda da peneira da pesquisa ampla, `estrategia-pos-pesquisa.md`, aceita pelo Gustavo): a busca
  pode escolher o analisador por idioma de cada nota; o lingua-py detecta pt e en offline (wheels Windows), e o
  resultado pode ir para um campo do frontmatter. A precisão cai em texto curto e em nota que mistura os dois
  idiomas. Decidir aqui o campo e quem o grava. Também daqui: onde mora o texto extraído dos anexos (docx, pdf,
  xlsx) que a busca indexa (Docling, pandoc), junto com "Camada de busca".
- 2026-10-14 ~17h30, comentário do Gustavo pelo portal (envio `13ceb50f-d0ab-4f74-912f-e265fe79ac06`): "vamos
  iniciar esse". Ticket em andamento (claimed). Próxima rodada: a R19, o que fica dentro da pasta de uma iniciativa.
- 2026-10-14 ~17h45: **rodada 8 aberta no portal** (`portal/rodadas/2026-10-14-arquitetura-de-pastas-e-frontmatter-r8.md`),
  a primeira rodada real fora da nota "Rodada atual". É a R19 reaberta: o que fica dentro da pasta de uma iniciativa.
  - Recomendação: um núcleo pequeno em toda iniciativa (`README.md` como ficha, `retomada.md`, `_archive/`,
    `maestro/` opcional) mais modelos prontos por tipo, escolhidos ao criar a pasta (cliente com entregas,
    produto com código, operação contínua, pesquisa ou spike).
  - A pergunta parte das pastas reais de `C:\Projetos`, por causa da lição da R13.
  - Fica para uma rodada própria: senhas e tokens soltos nas pastas de spike.
  - Página visual pedida ao Designer (subagente, em paralelo ao marco 8).
- 2026-10-14, resposta à rodada 8 (portal, envio `944cb514-deff-4bb0-9f47-81b93a86b1f4`, 17:33): nenhuma escolha;
  comentário "explique melhor sua pergunta". A rodada foi reescrita no mesmo arquivo:
  - a pergunta em uma frase: com que subpastas e arquivos a pasta de uma iniciativa nova já nasce;
  - as árvores reais de hoje (`soc-context`, `voegol`, `context-hub`);
  - o que um agente perde sem forma fixa;
  - exemplos de árvore na opção A para o SOC STRATA e para uma frente da VOEGOL.
  A recomendação continua A.
- 2026-10-14, resposta à rodada 8 reescrita (portal, envio `65ca59e5-e284-4bed-ac34-83105da2b850`, 17:38): **A.**
  - Toda pasta de iniciativa nasce com quatro itens fixos: `README.md` (a ficha), `retomada.md`, `_archive/` e
    `maestro/` (opcional).
  - Junto, um modelo de subpastas escolhido pelo tipo da iniciativa, cada modelo uma peça do acervo.
  - Os nomes das subpastas da rodada eram exemplos. Cada modelo, e quais modelos existem, vem em rodada própria;
    também ficam por decidir o frontmatter da ficha e as senhas e tokens soltos.
  - O comentário dele sobre o portal foi para o Designer: rodada editada não volta a "aguardando você", e o portal
    reinicia sozinho enquanto ele escreve.
  - Rodada marcada `absorvida`.
- 2026-10-14, carta da rodada 8 pronta (Designer): [`prototipo-12-miolo.html`](../prototipos/prototipo-12-miolo.html),
  ligada à rodada como registro. Pontos que a carta interpretou, para a rodada dos modelos:
  1. os destinos no hub e o tipo de modelo do `context-hub` e do `videos-transcriptor` foram inferidos;
  2. os spikes (`spike-fns`, `spike-livesync`) viraram uma coluna só;
  3. os `Scripts/` e `Tests/` da VOEGOL estão fora de git: o código vai para um repositório fora do hub, mas esse
     repositório ainda não existe, e onde ficam na opção A está em aberto.
- 2026-10-14 ~18h10, Gustavo no chat: "não concordo com essas 4 pastas fixas, inclusive nem sabia que eram essas".
  **A metade fixa da resposta A volta a ficar em aberto.** Fica valendo só o modelo de subpastas por tipo de
  iniciativa. Conferência do maestro sobre a origem dos quatro itens:
  - `retomada.md`: o "Contrato file-first" decidiu uma nota de retomada por trabalho, num lugar que a pasta permite
    achar sem busca; o lugar é deste ticket;
  - `README.md` como ficha: só proposta do maestro, sem decisão anterior;
  - `_archive/`: **erro do maestro.** A rodada 3 decidiu `_archive/` dentro de cada raiz, não de cada iniciativa;
  - `maestro/`: "Maestri: padrão e liberdade" decidiu uma pasta `maestro/` opcional dentro de cada iniciativa.
  Lição: os itens fixos ficaram no "por quê", que só aparece ao expandir, e não na opção. Ele escolheu sem vê-los.
- 2026-10-14 ~18h20: **rodada 9 aberta no portal**
  (`portal/rodadas/2026-10-14-arquitetura-de-pastas-e-frontmatter-r9.md`): o que fica igual em toda pasta de
  iniciativa.
  - Opções: nada (A); só `retomada.md` (B, recomendada); `retomada.md` e `README.md` (C).
  - A rodada deixa explícito o que já está decidido em outros tickets: `_archive/` por raiz e `maestro/` opcional.
  - A recomendação mudou da que dei no chat ("nada fixo"): a nota de retomada precisa de lugar fixo para ser
    achada sem busca.
- 2026-10-14 ~18h50, comentário do Gustavo na carta "Miolo da iniciativa" (envio `89cdd579-4517-4505-9a6b-0e879e992bca`):
  "melhore sua proposta de núcleo e opções de 'modelo pronto por tipo'. A opção B já é descartada, Sugira outra no
  lugar da B". **B da rodada 8 descartada**: um esqueleto único para todas as iniciativas. A rodada 9 foi suspensa,
  sem resposta, e a **rodada 10 foi aberta** (`portal/rodadas/…-r10.md`) com duas perguntas:
  1. Núcleo, várias escolhas. Recomendados: `retomada.md` e um `AGENTS.md` da iniciativa com a ficha no topo.
     Também na lista: `README.md` só com a ficha, `decisions.md` e `GLOSSARY.md`.
  2. Forma do resto da pasta. A é um modelo por tipo. **B, nova:** blocos combináveis do acervo (entregas,
     planejamento, operação, conhecimento, pesquisa, código), escolhidos ao criar e somados depois, recomendada
     porque as pastas reais misturam tipos. C é só o núcleo, sem acervo.
  - Não verificado com o hub: o Codex e o Copilot lerem o `AGENTS.md` de uma subpasta.
  - Carta nova pedida ao Designer.
- 2026-10-14: carta da rodada 10 ligada: [`prototipo-12-blocos.html`](../prototipos/prototipo-12-blocos.html) (núcleo como placa-base; blocos encaixados; o molde de cada iniciativa na opção A foi escolha do Designer).
- 2026-10-14 ~19h05, comentário do Gustavo na carta "Núcleo e blocos da iniciativa" (envio `46a21493-c505-4269-a88e-d5c9b7fe41f9`):
  "ficou bem, bem, bem melhor"; ele está **inclinado à B** (blocos empilhados), mas pede antes um **levantamento**:
  - o que é de fato iniciativa no vault antigo (`ai-operating-system`), em `C:\Projetos` e em `Documentos\Projetos`;
  - qual o padrão ideal por TIPO de iniciativa, "baseado em como já faço vs como seria ideal".
  A rodada 10 fica aberta esperando o levantamento.
- 2026-10-14 ~19h40: levantamento feito, em
  [`exploracao/anexos/levantamento-12-iniciativas.md`](../../../exploracao/anexos/levantamento-12-iniciativas.md).
  No meio dele, o Gustavo pediu: "você vai precisar ler o conteúdo de algumas pra entender [...] tentar colocar
  tudo que tinha nos initiative.md dentro dos AGENTS.md, vai ficar inviável". Achados:
  - **30 iniciativas** em nove tipos de trabalho. O tipo do vault (mudança, iniciativa, projeto) mede tamanho, não
    o jeito do trabalho.
  - **Os mesmos assuntos aparecem com nomes diferentes:**
    - entrada: `context/`, `comunicacao/`, `sources/`;
    - pesquisa: `research/`, `pesquisa/`, `levantamento/`, `discovery/`, `analysis/`;
    - entregas: `deliverables/`, `entregaveis/`, `documentos/`, `repasse/`, `outputs/`.
  - **O `initiative.md` do vault já padroniza** (frontmatter e sete seções), mas o arquivo único explode: VOEGOL
    cross-tenant com 337 mil caracteres, soc-as-code com 190 mil e TRF3 com 181 mil, a maior parte em Atualizações,
    Pendências e Decisões.
  - **Proposta revista:**
    - o núcleo vira o padrão de sete seções separado por ritmo: `initiative.md` (a ficha), `retomada.md`,
      `tasks.md`, `decisions.md`, `context.md` e `log/AAAA-MM.md`;
    - o `AGENTS.md` da iniciativa é só o mapa e as regras próprias;
    - os blocos ficam com um nome só: `inputs/`, `research/`, `design/`, `plans/`, `deliverables/`, `evidence/`,
      `runs/`, `tools/`, a operação, `knowledge/` e o estudo;
    - cada tipo de trabalho ganha uma pilha sugerida.
  - A rodada 10 foi suspensa, sem resposta; a rodada 11 foi aberta com isso.
- 2026-10-14 ~19h50, a carta "Miolo da iniciativa" foi **recusada** pelo Gustavo no portal (envio `25ee8c4c-a424-4518-879e-a8ad381d5633`):
  "uma nova carta ja substituiu essa, vocês deviam ter recusado automaticamente". Pedido ao Designer:
  - marcar como substituída a carta "Miolo da iniciativa", e a "Núcleo e blocos da iniciativa" quando a da rodada
    11 chegar;
  - fazer o portal tirar uma carta da lista de vigentes, sozinho, quando outra a substituir.
- 2026-10-14: carta da rodada 11 ligada: [`prototipo-12-ritmos.html`](../prototipos/prototipo-12-ritmos.html), "Como você já faz × como seria ideal" (substitui a prototipo-12-blocos).
- 2026-10-14, resposta à rodada 11 (portal, envio `04e0593a-6eeb-4680-bbee-c7da82e138c8`, 19:26):
  - **Núcleo = A.** As sete seções do `initiative.md` do vault, cada uma no seu arquivo:
    - `initiative.md`: ficha, descrição e fontes;
    - `retomada.md`: o estado, sobrescrito;
    - `tasks.md`: só as pendências abertas;
    - `decisions.md`: uma linha por decisão;
    - `context.md`: só os fatos estáveis;
    - `log/AAAA-MM.md`: o diário, um arquivo por mês.
    O `AGENTS.md` da iniciativa é só o mapa e as regras próprias.
  - **Resto da pasta = B.** Blocos com um nome só, somados conforme o trabalho pede, e uma pilha sugerida por tipo:
    `inputs/`, `research/`, `design/`, `plans/`, `deliverables/`, `evidence/`, `runs/`, `tools/`, operação
    (`procedures/`, `cases/`, `queries/`), `knowledge/` e estudo (`notes/`, `labs/`).
  - Requisitos novos do comentário dele:
    1. Uma descrição breve de cada bloco num lugar que o agente consulta para escolher o bloco.
    2. Um bloco genérico para o que não se encaixa em nenhum.
    3. Tudo achável a partir do `AGENTS.md` em poucos pulos, sem listar todos os arquivos das subpastas.
    4. **O principal:** um mecanismo que não deixe arquivo sem nada que o referencie. Um link para o bloco no
       `AGENTS.md` não basta quando o bloco cresce e um arquivo relevante fica fundo.
  - Elogio: "A carta prototipo-12-ritmos ta perfeita [...] parabéns. Tanto ao seu levantamento quanto ao design."
  - Pergunta dele: qual a estratégia para isso ser utilizável e fácil de os agentes consumirem e se localizarem.
  - Rodada 11 marcada `absorvida`. A rodada 12 traz a estratégia de localização e o mecanismo contra órfãos.
- 2026-10-14 ~19h35: **rodada 12 aberta** (`portal/rodadas/…-r12.md`): a estratégia de localização em quatro pulos (o `AGENTS.md` da raiz, o `index.md` de cada raiz, o `AGENTS.md` da iniciativa e o `index.md` de cada pasta). Três perguntas: o catálogo de blocos (recomendado: `agents/blocks.md` e uma skill "nova iniciativa"), o bloco genérico (recomendado: `misc/`, com regra de promoção) e os órfãos (recomendado: `index.md` em toda pasta e um verificador sem IA no hook do fim da resposta, que inscreve o órfão como "sem descrição"). Carta pedida ao Designer.
- 2026-10-14 19:27, carta "Como você já faz × como seria ideal" (`prototipo-12-ritmos`) **aprovada** pelo Gustavo no portal (envio `971570e7-b34a-4831-b5ef-e16c52544083`): "o design ficou sensacional parabéns".
- 2026-10-14: carta da rodada 12 ligada: [`prototipo-12-sumario.html`](../prototipos/prototipo-12-sumario.html), "O agente acha tudo · nada fica órfão".
- 2026-10-14, resposta à rodada 12 (portal, envio `1f640d48-f607-4267-8aa6-a98b387b00a6`, 19:52):
  - **Catálogo = A** (`agents/blocks.md`, citado pelo `AGENTS.md` da raiz, mais a skill "nova iniciativa"). Do
    comentário dele:
    - a skill já leva scripts que criam a pasta, o núcleo e os blocos mecanicamente, sem gastar tokens;
    - a skill **não pode ser alterada por qualquer agente**, só sob supervisão e aprovação. Ele já sofreu com o
      Copilot editando a skill do ai-soc-report a cada uso. Combina com a guarda decidida em "Maestri: padrão e
      liberdade".
  - **Bloco genérico = B, `other/`**, com a regra de promover a bloco novo quando três parecidos se juntam.
  - **Órfãos = A, com correção:** `index.md` não em toda pasta, só nas pastas que crescem em número de arquivos.
    - Exemplo: `runs/` com `run-01/`, `run-02/`… tem `index.md`.
    - Uma pasta com três subpastas, das quais só uma cresce, tem o `index.md` nessa subpasta.
  - Algo mais:
    - nem toda rodada precisa de carta; rodadas simples dispensam a visualização;
    - a carta trocou a ordem das perguntas;
    - o hook equivalente nos outros harnesses segue em aberto; no Claude, pode ser um mod.
    - Ele perguntou se trocar a busca por `index.md` é ruim, e se o maestro considerou o que já foi decidido e as
      oportunidades da pesquisa ampla.
  - **Conferência do maestro: não considerou.** A rodada 12 contradiz a lição 4 de "Lições do vault": "Uma cadeia de
    índices mantida à mão como porta de entrada. A porta é a camada de busca; um índice só existe onde a busca não
    basta." Ela também não citou a camada de busca, decidida como porta de entrada (Q4 de "Lições do vault" e
    critério 1), nem os itens da peneira da pesquisa ampla que caem neste ticket (texto extraído dos anexos, campo
    de idioma no frontmatter).
  - A rodada 12 foi marcada `absorvida`. A escolha dos órfãos fica **em revisão** até a rodada 13, que reconcilia os
    índices com a busca. O catálogo e o `other/` seguem valendo, porque não conflitam com nada.
- 2026-10-14 ~20h05: **rodada 13 aberta** (`portal/rodadas/…-r13.md`, sem carta, por ser simples). Recomendação A:
  a busca é a porta para achar; o catálogo e o mapa do `AGENTS.md` dizem onde gravar; o `index.md` fica só nas pastas
  que crescem e descreve o que a busca não lê (prints, PDFs, planilhas, subpastas de `runs/`); o verificador cobra essa
  linha de todo arquivo que não é texto.
- 2026-10-14, resposta à rodada 13 (portal, envio `93dcbcbb-f053-4b44-a109-1f02eaa89d57`, 20:01): sem escolha.
  Pergunta dele: "Acho que não tem como tomar essa decisão nesse ticket sem fecharmos e decidirmos tudo sobre o
  mecanismo de busca. Concorda ou acha que podemos decidir algo agora que não depende [...] do mecanismo de busca?"
  Resposta do maestro no chat:
  - Concorda em parte. Dependem da "Camada de busca": como índices e busca se dividem, onde mora o texto extraído
    dos anexos e o campo de idioma no frontmatter.
  - Não dependem: o conteúdo de cada bloco, o frontmatter da ficha (fora o idioma), os segredos dos spikes, os
    scripts (`tools/` ou repositório próprio) e juntar o SOC STRATA.
  - Proposta: rodada 13 suspensa até a decisão da busca, e as rodadas seguintes só com o que não depende dela.
    Aguarda o ok do Gustavo.
- 2026-10-14 ~20h15: rodada 13 suspensa (depende da "Camada de busca", como o texto extraído e o campo de idioma).
  **Rodada 14 aberta**, só com o que não depende da busca:
  - o que entra em cada bloco (tabela editável que vira o `agents/blocks.md`);
  - os campos da ficha (tabela editável: entram `kind`, o tipo de trabalho, e `blocks`; o `type` do vault vira
    `size`; saem `emoji` e `model`);
  - os segredos (recomendação A: nunca no hub, KeePass com variável de ambiente; pastas com ponto aninhadas vazaram
    no teste "Disco e banco sem o Obsidian");
  - os scripts (recomendação C: `tools/` até ganharem testes ou dependências, depois repositório próprio).
  O SOC STRATA ficou fora: "Workloads piloto" o deixou fora por ora.
- 2026-10-14, resposta à rodada 14 (portal, envio `cf455bcf-30f0-48fe-aa85-17ad92f610de`, 20:51). Versão completa das
  tabelas no `.json` irmão, em `portal/caixa/`.
  - **Blocos aceitos, com mudanças:**
    - `runs/` passa a "execuções e revisões, uma subpasta por execução";
    - bloco novo **`work/`**: "trabalho de agentes: briefs, handoffs, contexto antes de clear". O "não entra" ficou em
      branco, e ele pediu que o maestro sugira o "não entra" e melhore o "entra";
    - ordem: `inputs/`, `research/`, `design/`, `plans/`, `deliverables/`, `evidence/`, `tools/`, `runs/`, `work/`,
      `procedures/`, `cases/`, `queries/`, `knowledge/`, `notes/`, `labs/`, `other/`.
  - **Ficha aceita**, com `cadence` ganhando `weekly`. Campos: `id`, `title`, `kind`, `size`, `status`, `blocks`,
    `workspace`, `parent`, `related`, `cadence`, `updated_at`.
  - **Segredos = B, `.secrets/`** dentro da iniciativa, fora do `.git`. Ressalva dele: as senhas de **contas que
    acessam tenant** ficam no KeePass.
    - **Condição para a construção:** o teste "Disco e banco sem o Obsidian" viu pastas com ponto aninhadas vazarem
      para o banco. A regra de exclusão do LiveSync tem de cobrir `.secrets/` em qualquer nível (`**/.*` e `**/.*/**`,
      como já anotado na "Camada de busca"). Antes de guardar o primeiro segredo, um teste tem de provar que um
      `.secrets/` aninhado não chega ao banco nem ao GitHub.
  - **Scripts = C:** `tools/` enquanto são de apoio; viram repositório próprio quando ganham testes, dependências ou
    uso fora da iniciativa.
  - Rodada 14 marcada `absorvida`. A rodada 15 traz o texto do `work/`.
- 2026-10-14, resposta à rodada 15 (portal, envio `95390abf-039d-4bc5-94d4-7a5d4e76ce89`, 20:54): o texto do `work/` foi
  aceito, com um ajuste: tirar a referência ao portal, porque "um novo agente iria querer entender o que é esse
  portal". O "entra" e o "não entra" são só uma descrição rápida para o agente saber se o bloco o atende. Ele pediu
  para conferir os outros blocos pelo mesmo critério. A conferência achou mais duas referências que só fazem
  sentido nesta conversa:
  - `labs/` "não entra: senhas (ver a pergunta dos segredos)";
  - "a personalização do Maestri", nome de ferramenta sem explicação, em `runs/` e `work/`.
  Os nomes do núcleo (`tasks.md`, `retomada.md`, `decisions.md`) ficam, porque o catálogo os define antes dos blocos.
  **Texto final do catálogo de blocos** (vira o `agents/blocks.md`):

  | Bloco | Entra | Não entra |
  |---|---|---|
  | `inputs/` | o que veio de fora: kickoff, PDF e planilha do cliente, e-mails, exports | o que você produziu a partir disso (vai para `research/` ou `deliverables/`) |
  | `research/` | levantamento, pesquisa, análise, discovery, comparação de opções | a decisão tomada (`decisions.md`) e o desenho final (`design/`) |
  | `design/` | arquitetura, especificação, desenho da solução, o detalhe de uma decisão grande | planos de execução (`plans/`) |
  | `plans/` | planos, roteiros, tickets e backlog maior que o `tasks.md` | a pendência simples do dia (`tasks.md`) |
  | `deliverables/` | o que é entregue, com versão no nome: documentos, relatórios, apresentações | rascunhos de trabalho (`research/` ou `design/`) |
  | `evidence/` | prints, logs e exports que provam um fato | imagens de documento entregue (`deliverables/`) |
  | `tools/` | scripts de apoio desta iniciativa | código de produto, que mora no repositório próprio |
  | `runs/` | execuções e revisões, uma subpasta por execução | o trabalho em curso de um agente (`work/`) e os ajustes do orquestrador de agentes para a iniciativa (`maestro/`) |
  | `work/` | o trabalho em curso dos agentes: briefs para recrutas e subagentes, handoffs entre sessões, o estado salvo antes de limpar o contexto, notas de trabalho de um agente; uma subpasta por agente ou frente | onde a iniciativa parou (`retomada.md`), decisões (`decisions.md`), resultados de execuções e revisões (`runs/`), entregas (`deliverables/`), os ajustes do orquestrador de agentes (`maestro/`) |
  | `procedures/` | runbooks, SOPs, passo a passo de operação | o registro de cada caso (`cases/`) |
  | `cases/` | um arquivo por caso ou incidente | o procedimento genérico (`procedures/`) |
  | `queries/` | consultas salvas (KQL, SQL) e seus resultados de referência | scripts (`tools/`) |
  | `knowledge/` | base de conhecimento própria da iniciativa | conhecimento geral, que vai para a raiz `reference/` |
  | `notes/` | anotações de estudo | o material do curso (`inputs/`) |
  | `labs/` | exercícios e ambientes de laboratório | senhas e tokens (vão para `.secrets/`) |
  | `other/` | o que não cabe em nenhum bloco; com três parecidos, propõe-se um bloco novo | o que cabe num bloco existente |
- 2026-10-14 ~21h25: o restante deste ticket espera a "Camada de busca": a rodada 13 (índices e busca), onde mora o texto extraído dos anexos e o campo de idioma no frontmatter.
- 2026-10-15 ~14h30: o que este ticket espera da rodada 10 da "Camada de busca" (onde a busca mora; lido por um
  subagente, conferido pelo maestro):
  1. a rodada 13 suspensa (como índices e busca se dividem): o que a busca lê depende de onde ela mora; o
     obsidian-hybrid-search lê `.md`, e `.txt` e `.csv` não foram verificados;
  2. onde mora o texto extraído dos anexos (docx, pdf, xlsx): na Leve, ele teria de ser um arquivo no disco; na Robusta,
     poderia ficar só no índice;
  3. o campo de idioma no frontmatter: sai se a rodada 10 decidir "um analisador só";
  4. efeitos da Leve, se ela vencer (consequências lidas, não decisões): o índice `.obsidian-hybrid-search.db` na raiz
     do hub; nota com YAML inválido fica de fora da busca (12 de 124 na bancada), então a ficha precisa de YAML
     válido; o obsidian-hybrid-search pesa `title` e `aliases`, e a ficha da rodada 14 tem `title` e não `aliases`.
- 2026-10-15 ~15h: **rodada 16 aberta** (`portal/rodadas/2026-10-15-arquitetura-de-pastas-e-frontmatter-r16.md`),
  rascunhada por um subagente Opus médio e revisada pelo maestro; refaz a 13 (marcada absorvida, substituída) com a busca
  decidida: como índices e busca se dividem (recomendada: `index.md` só na pasta com arquivo que a busca não lê; a B
  preserva a correção do Gustavo na rodada 12, `index.md` em toda pasta que cresce), onde mora o texto dos anexos
  (recomendado: arquivo irmão `nome.pdf.md`) e `title` nas notas do núcleo com `aliases` na ficha (recomendado). Fato
  lido no pacote do obsidian-hybrid-search 0.16.2 da bancada (`indexer.js`, `db.js`): só indexa `.md`; título pesa 10 e
  `aliases` 5 na busca por palavra; o caminho da pasta não entra na busca por palavra; respeita o `.gitignore`. **Não
  verificado:** o OCR do Docling em português.
- 2026-10-15 16:18, **rodada 16 respondida** (envio `d6f47073-e2be-4f3a-9823-23b19bac4350`):
  - **índices e busca = B** (a recomendada era A): como a A (a busca é a porta; `index.md` onde há arquivo que a busca não
    lê), e **o `index.md` existe também em toda pasta que cresce, mesmo só com `.md`**, como sumário para navegar sem
    buscar (mantém a correção dele na rodada 12);
  - **texto dos anexos = A:** arquivo irmão ao lado do anexo (`proposta-v2.pdf` → `proposta-v2.pdf.md`), com `title`,
    `source` e `extractor` (Docling ou pandoc, com versão) no frontmatter; vale para PDF, Word, PowerPoint, Excel e HTML;
    replica e vai ao git; o anexo com texto dispensa linha no `index.md`;
  - **títulos = A:** os arquivos do núcleo ganham `title` com o nome da iniciativa ("Retomada · VOEGOL cross-tenant"); a
    skill "nova iniciativa" escreve e o verificador completa o que faltar (ex.: `log/` de mês novo) a partir do `title` da
    ficha; a ficha ganha `aliases` (siglas, nome no Loop, nome antigo no vault).
- 2026-10-15 ~16h40: rascunho do Answer por um subagente Opus médio (`rascunhos/12-answer-rascunho.md`: 12 pontos abertos,
  os já fechados por outro caminho e as substituições). Bloqueiam resolver: como uma pasta se declara não replicada (a
  Question pede; o glossário ainda diz "cada pasta declara" e "por SSH"), o frontmatter das demais notas (os `index.md`
  da B apareceriam todos como "index" na busca) e o protótipo pedido na Question. Maior risco para a construção: quem
  mantém os `index.md` das pastas só de `.md` e o critério de "pasta que cresce" (lição 4: índice à mão desatualiza).
  **Rodada 17 aberta** (`portal/rodadas/2026-10-15-arquitetura-de-pastas-e-frontmatter-r17.md`) com esses quatro. Os
  outros oito vão à construção como pontos a decidir ou não verificados (lista no rascunho).
- 2026-10-15 17:29, **rodada 17 respondida** (envio `49346806-5951-4cb7-8c1b-559853db6eb0`):
  - **pasta local = B** (a recomendada era A): além do ponto no nome, uma pasta pode se declarar local por um arquivo
    marcador dentro dela, que o sync e a busca respeitam;
  - **frontmatter das demais notas: sem escolha.** "Detalhe mais e recomende um padrão para cada tipo possível de nota.
    Pois frontmatter é algo muito útil e você está banalizando";
  - **dono do sumário = A** (o verificador mantém a lista de cada `index.md`; texto livre no topo; a partir de 10
    arquivos), com dois pedidos: uma recomendação de **onde fica definido na pasta que ela recebe `index.md`**, e, junto
    com o padrão de frontmatter, se dá para fazer isso **de forma mecânica, para nenhum agente ficar livre para "decidir"
    se segue o padrão** ("regrinhas no AGENTS.md já se provaram às vezes inúteis para agentes menores");
  - **protótipo = B** (a recomendada era A): antes de resolver, o Designer faz um esboço da árvore final com notas de
    exemplo (ficha com `aliases`, `work/`, `.secrets/`, os `index.md`, o texto dos anexos), numa carta para aprovar.
  **Próximo:** proposta de frontmatter por tipo de nota, com imposição mecânica (validação na gravação e no verificador),
  e onde a pasta declara "recebe `index.md`" e "local" (o mesmo mecanismo de marcador, de preferência); vira rodada 18.
  Depois, o esboço do Designer com o padrão decidido.
- 2026-10-15 ~18h, **rodada 18 aberta** (`portal/rodadas/2026-10-15-arquitetura-de-pastas-e-frontmatter-r18.md`; proposta
  inteira em `rascunhos/12-frontmatter-proposta.md`): frontmatter por tipo (campos comuns + 28 tipos, tipo pelo caminho,
  esquemas em `agents/frontmatter/`), imposição em camadas (hook antes da gravação, MCP, verificador no fim com `Stop`,
  Templater por pasta no Obsidian) e o `index.md` como cartão da pasta (`summary: auto`, `local`). Fontes conferidas: docs
  de hooks do Claude Code (`PreToolUse` deny, `Stop` block), Templater "Folder templates", Obsidian "Properties" (tipo
  único por nome no cofre). Depois: o esboço do Designer (rodada 17, B) com o padrão decidido.
- 2026-10-15 17:44, **rodada 18 respondida** (envio `6c08cecb-e0bd-4573-b20a-eed63c5ead4f`):
  - **padrão por tipo = A + C:** o catálogo da proposta (`rascunhos/12-frontmatter-proposta.md`: campos comuns e 28
    tipos) e mais um `status` comum em toda nota (rascunho, em uso, superada) para filtrar o vigente em qualquer pasta.
    **A conciliar:** vários tipos já têm `status` próprio com outros valores (research, design, plan, deliverable, work,
    case, lab, a ficha);
  - **imposição = C:** como a A (hook antes da gravação, MCP do banco, verificador no fim que preenche e devolve ao
    agente), **sem o Templater**: notas do Gustavo no Obsidian nascem sem frontmatter e o verificador da próxima resposta
    de agente completa;
  - **cartão da pasta = A:** o `index.md` declara `summary: auto` e `local: true|false`; o verificador o cria a partir de
    10 arquivos ou de arquivo que a busca não lê; pasta local = `index.md` com `local: true`.
  **Próximo:** o esboço da árvore pelo Designer (rodada 17, B), com o padrão decidido; a conciliação do `status` vai na
  rodada que acompanha a carta.
- 2026-10-15 ~19h: esboço da árvore final pedido ao Designer (`rascunhos/12-brief-esboco.md`; carta `prototipo-12-arvore` em `prototipos/`, com `pede_veredito`). A rodada 19 acompanha a carta: conciliar o `status` comum com o ciclo próprio de cada tipo.
- 2026-10-15 17:54: carta `prototipo-12-sumario` **aprovada** pelo Gustavo (envio `854291c3-6b31-40dc-a29b-61c95edbbe03`): "esse design já foi usado, só vou aprovar de novo pois está bem bonito". Decisão da carta atualizada (a escolha dos órfãos foi substituída pela rodada 16).
- 2026-10-15 ~19h10: **carta `prototipo-12-arvore` no portal** (esboço da árvore, `pede_veredito`; capturas em `portal/conferencia/carta-12-arvore/`) e **rodada 19 aberta** (`portal/rodadas/2026-10-15-arquitetura-de-pastas-e-frontmatter-r19.md`): `stage` + `status` derivado (recomendada A).
- 2026-10-15 18:10, **rodada 19 respondida** (envio `36abc055-87d3-4c19-b8c1-446155eb1d41`): **status e ciclo = A**
  (a recomendada): o ciclo do tipo vai em `stage` (quem escreve preenche); o `status` comum (rascunho, em uso, superada)
  fica em toda nota; nos tipos com ciclo, o verificador deriva o `status` do `stage` por uma tabela no esquema do tipo;
  nos outros, quem escreve preenche. A ficha da iniciativa entra na regra (o `status` dela vira `stage`).
  **Algo mais:** links para o que não replica (pasta `local: true`, pasta com ponto, outros casos): ele sugere a forma
  `<par_id>/<pasta_raiz>/<subpastas>` em vez de `./`, `~/` ou `C:/`, e pergunta em que casos usar → rodada 20. A carta
  `prototipo-12-arvore` ainda espera veredito.
  **Rodada 20 aberta** (`portal/rodadas/2026-10-15-arquitetura-de-pastas-e-frontmatter-r20.md`): links para o que não replica (recomendada A: `par://<par_id>/<caminho>` só quando o destino não replica; link interno normal com caminho absoluto no cofre para o resto; o verificador corrige). Fonte: Obsidian help, "Settings" (New link format) e "Internal links".
- 2026-10-15 18:15, **rodada 20 respondida** (envio `70824740-e39a-49df-b73f-9f372b107cbc`): **links = A** (a recomendada):
  o par na frente só quando o destino não replica. Para o que replica, link interno normal com o caminho a partir da raiz
  do cofre (Obsidian "Absolute path in vault"); para destino em pasta `local: true`, pasta com ponto ou fora do hub,
  `par://<par_id>/<caminho a partir da raiz do hub>`, sem letra de unidade; o verificador confere pelo cartão das pastas
  e corrige nos dois sentidos, avisando o agente; de `.secrets/`, só o nome do arquivo. Falta só o veredito da carta
  `prototipo-12-arvore` para resolver o ticket.
- 2026-10-15 20:32, **carta `prototipo-12-arvore` aprovada** (envio `0011c856-1d7f-4533-893c-dcd8d816d458`), sem
  comentário. Ticket resolvido.

## Answer

**A árvore do hub tem o `AGENTS.md` e seis raízes em inglês; cada iniciativa nasce com um núcleo de seis arquivos
separados por ritmo e soma blocos de nome único de um catálogo; a busca é a porta para achar; toda nota tem frontmatter
do tipo que o caminho dá, imposto por mecanismo; o `index.md` é o cartão da pasta; tudo replica, e só fica numa máquina
o que tem ponto no nome ou um `index.md` com `local: true`.** Decidido com o Gustavo de 2026-10-10 a 2026-10-15, nas
rodadas 3 a 6 (nota "Rodada atual") e 8, 11, 12 e 14 a 20 (portal); esboço aprovado na carta `prototipo-12-arvore`.

- **Raiz (rodadas 3, 4 e 5):** `AGENTS.md`, `clients/` (iniciativas de cliente), `operations/` (trabalho contínuo),
  `initiatives/` (iniciativas sem cliente: produtos, frentes, estudo, spikes), `reference/` (conhecimento de
  referência), `agents/` (a oficina, sem ponto, para replicar pela sync normal) e `inbox/` (captura). O que termina vai
  para o `_archive/` da própria raiz, movido por script que confere o outro par ("Portas de entrada do hub"). Sem raiz
  pessoal. O cofre do Obsidian é a raiz; o hub não tem `CLAUDE.md`; o `.git` fica na raiz de cada máquina e não replica.
- **Profundidade (rodada 6, confirmada em "Portas de entrada do hub"):** dois níveis em `clients/`
  (`clients/<cliente>/<iniciativa>/`) e um nas outras (`operations/<operação>/`, `initiatives/<iniciativa>/`,
  `reference/<assunto>/`). Nenhuma porta de entrada depende da profundidade.
- **`agents/` (rodadas 6, 12 e 18; "Maestri: padrão e liberdade"):** `agents/skills/<skill>/` (inclusive a família
  `maestro-*`; os papéis são peças do acervo), `agents/machines/<máquina>.md` (perfil de cada máquina; o nome é o
  `par_id` dos links), `agents/maestro/propostas/`, `agents/maestro/uso/<máquina>.md`, `agents/blocks.md` e
  `agents/frontmatter/` (`paths.yml` e um esquema por tipo).
- **Núcleo da iniciativa (rodada 11):** `initiative.md` (ficha), `retomada.md` (o estado, sobrescrito; a nota de
  retomada do "Contrato file-first"), `tasks.md`, `decisions.md`, `context.md` e `log/AAAA-MM.md`. O `AGENTS.md` da
  iniciativa é só o mapa e as regras próprias. Opcional: `maestro/` ("Maestri: padrão e liberdade").
- **Blocos e catálogo (rodadas 11, 12, 14 e 15):** `inputs/`, `research/`, `design/`, `plans/`, `deliverables/`,
  `evidence/`, `tools/`, `runs/`, `work/`, `procedures/`, `cases/`, `queries/`, `knowledge/`, `notes/`, `labs/` e
  `other/`; o texto "entra / não entra" da rodada 15 vira o `agents/blocks.md`. A skill "nova iniciativa" cria pasta,
  núcleo e blocos por script e só muda com supervisão e aval.
- **Ficha, `initiative.md` (rodadas 14, 16 e 19):** `id`, `title`, `aliases` (siglas, nome no Loop, nome antigo no
  vault), `kind`, `size`, `stage` (doing, backlog, on-hold, done, archived), `blocks`, `workspace`, `parent`, `related`,
  `cadence` e os campos comuns. Saem `emoji` e `model`; cliente e raiz não viram campo.
- **Frontmatter por tipo (rodadas 17, 18 e 19; catálogo em `rascunhos/12-frontmatter-proposta.md`):** o tipo vem do
  caminho (`agents/frontmatter/paths.yml`), nunca de quem grava; cada tipo tem um esquema em
  `agents/frontmatter/<tipo>.yml`. Campos comuns em toda nota: `title`, `type`, `initiative`, `created`, `updated`,
  `status` (rascunho, em uso, superada) e, opcionais, `aliases`, `tags`, `related`. Os 28 tipos da proposta somam os
  campos próprios. Nos tipos com ciclo (ficha, research, design, plan, deliverable, work, case, lab), o ciclo vai em
  `stage`, preenchido por quem escreve, e o verificador deriva o `status` por uma tabela no esquema. O derivável a
  máquina preenche (`type`, `initiative`, `title` do núcleo, `updated`). Sem frontmatter do hub: `AGENTS.md` e
  `SKILL.md`.
- **Imposição (rodada 18, C):** hook antes da gravação recusa a nota fora do esquema (Claude Code, Codex e Copilot); o
  MCP do banco valida igual; o verificador sem IA, no fim de cada resposta (`Stop`), preenche o derivável e devolve o
  resto ao agente. Sem Templater: nota do Gustavo no Obsidian nasce sem frontmatter e o verificador da próxima resposta
  de agente completa. Nenhuma regra disso mora só no `AGENTS.md`.
- **Títulos do núcleo (rodada 16, A):** `title` com o nome da iniciativa ("Retomada · VOEGOL cross-tenant"); a skill
  escreve e o verificador completa a partir do `title` da ficha.
- **Índices e busca (rodadas 16, B, e 17 e 18, A):** a busca é a porta. O `index.md` é o cartão da pasta: declara
  `summary: auto` (o verificador mantém a lista, com texto livre no topo) e `local: true|false`. O verificador o cria
  quando a pasta chega a 10 arquivos ou guarda arquivo que a busca não lê (o obsidian-hybrid-search 0.16.2 só indexa
  `.md`).
- **Texto dos anexos (rodada 16, A):** arquivo irmão (`proposta-v2.pdf` → `proposta-v2.pdf.md`) com `source` e
  `extractor`; replica e vai ao git; dispensa linha no `index.md`.
- **Pasta não replicada, Q15 (rodadas 3, 6, 17 e 18):** tudo replica nas duas máquinas, inclusive o conteúdo de
  cliente. Fica numa máquina só o que tem ponto no nome (`.git`, `.secrets/`, `.maestri/`, o índice da busca) e a pasta
  cujo `index.md` diz `local: true`; um script gera a exclusão do sync e da busca a partir desses marcadores.
- **Links (rodada 20, A):** para o que replica, link interno normal com o caminho a partir da raiz do cofre ("Absolute
  path in vault"); para destino que não replica, `par://<par_id>/<caminho a partir da raiz do hub>`, sem letra de
  unidade; o verificador confere pelo cartão das pastas e corrige nos dois sentidos; de `.secrets/`, só o nome.
- **Segredos (rodada 14, B):** `.secrets/` dentro da iniciativa, fora do git e da busca; senhas de contas que acessam
  tenant ficam no KeePass. **Scripts (rodada 14, C):** em `tools/` até ganharem testes, dependências ou uso de fora.
- **Protótipo:** carta `prototipo-12-arvore` (aprovada), mais `prototipo-12-ritmos` e `prototipo-12-sumario`.
- **Para a construção (pontos abertos menores e não verificados):**
  - teste antes do primeiro segredo: um `.secrets/` aninhado não chega ao banco nem ao GitHub (exclusão `**/.*` e
    `**/.*/**`); gerar a exclusão do LiveSync e da busca a partir dos `index.md` com `local: true`;
  - o MCP do banco validar o esquema (versão modificada); o OCR do Docling em português e quem dispara a extração;
  - tirar `.obsidian-hybrid-search.db` do git e do LiveSync;
  - o que mora no nível `clients/<cliente>/`; a retomada de trabalho fora de uma iniciativa; a forma de `inbox/`;
  - se `operations/` e `reference/` levam o núcleo inteiro;
  - os destinos de `armis-docs`, `armis-brand`, `armis-docx` e desta frente (leitura: `reference/`,
    `agents/skills/`, `initiatives/context-hub/`); as pilhas por tipo ajustadas ao `work/`; "criação de conteúdo" no
    `kind`;
  - os `Scripts/` e `Tests/` da VOEGOL quando ela vier ao hub.
- 2026-10-16 19:12 (ticket 16, rodada `2026-10-16-onde-mora-o-codigo-do-hub-r2`, Gustavo): o conteúdo de `agents/` ganha `agents/code/` para o código do próprio hub que só o harness ou o kit roda (hooks, mods, kit de par, verificador, testes); o que um agente chama fica como skill em `agents/skills/<peça>/`.
- 2026-10-16 19:21 (ticket 16, rodada `2026-10-16-ticket-05-perguntas-do-trilho`, Gustavo): a tabela `stage` → `status` que faltava (rascunho / em uso / superada por tipo com ciclo, texto no spec da construção, faixa 1) e `operations/<operação>/` sem `initiative` (não é iniciativa).
