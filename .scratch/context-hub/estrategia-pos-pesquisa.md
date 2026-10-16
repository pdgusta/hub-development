# Estratégia depois da pesquisa ampla

Pedido do Gustavo (2026-10-14, chat): traçar a estratégia a partir do resultado da pesquisa ampla
("Pesquisa ampla: lugares e mecanismos de busca", resolvida). Ele vê testes, combinações, oportunidades
de mudar outras partes da stack e de deixar o MCP mais robusto, e não quer perder coisa boa sem trazer
tudo para o barco. Parte vira ticket; parte vira tema para quando o hub já existir.

Visão nova, nas palavras dele: "tratar o context hub como algo que vai não só ser um acervo que
disponibiliza textos e contexto sobre meu trabalho e projetos, mas sim um lugar que controla como
qualquer harness e modelo trabalham da forma que eu definir".

Este arquivo é a proposta do maestro. Nada aqui está decidido até constar de um ticket resolvido ou
de uma resposta registrada abaixo.

## 1. A peneira: três destinos para cada achado

Cada achado da pesquisa (síntese e inventário em `exploracao/anexos/pesquisa-50-*`) vai para um de
três lugares:

| Destino | Critério | Onde fica gravado |
|---|---|---|
| **Agora** | muda uma decisão ainda aberta neste mapa | comentário no ticket dono (ou ticket novo, se não houver dono) |
| **Construção** | peça já confirmada, que só precisa ser montada | comentário em "Passagem para a construção" |
| **Radar** | bom, mas não muda nada agora; tem um gatilho que o traz de volta | seção "Radar" deste arquivo, com o gatilho de cada item |

O inventário inteiro (169 entidades de busca, 184 de stack, 292 conceitos) continua sendo a estante:
nada se perde, porque o radar aponta para ele.

## 2. Primeira passada da peneira (proposta)

### Agora

| Achado | Ticket dono | Por quê |
|---|---|---|
| Teste de bancada obsidian-hybrid-search contra memtomem, no disco, conteúdo real pt e en | Camada de busca | decide entre ferramenta pronta com repasse e índice próprio no MCP do banco |
| Três fatos: embedding multilíngue no FreeLLMAPI; linguagem do MCP do es617; LiveSync e arquivos com ponto | Camada de busca | travam o teste e a escolha do índice |
| A linguagem do MCP do banco decide a stack da construção (em Python, todas as peças têm Windows confirmado) | Camada de busca e Passagem para a construção | o fork do MCP é o centro do hub |
| Um MCP agregador (TBXark/mcp-proxy, 1MCP) como endpoint único na tailnet | Acesso dos agentes: decisão | vira a porta dos clientes e o lugar natural de política |
| Anexos entram na busca por extração (Docling, pandoc) | Camada de busca; Arquitetura de pastas e frontmatter | onde mora o texto extraído e como se marca |
| Idioma por nota (lingua-py) e um campo de idioma no frontmatter | Arquitetura de pastas e frontmatter | o índice escolhe o analisador por nota |
| O watcher precisa aguentar as rajadas do sincronizador | Camada de busca (o teste mede) | o watchdog não filtra eventos duplicados |

### Construção

SDK Python do MCP v2; python-frontmatter e PyYAML com `safe_load`; ripgrep; ONNX Runtime com o
e5-small como reserva local de embeddings; Watchman ou watchdog; o proxy de MCP. Todos com Windows
confirmado na régua.

### Radar

| Tema | Gatilho que o traz de volta |
|---|---|
| Cópia leve para sandbox (Pagefind ou SQLite exportado) | a primeira sandbox de verdade |
| Duas vias de busca juntas (índice no MCP mais ferramenta no disco) | a busca virar caminho crítico do contrato |
| Rerank (bge-reranker-v2-m3; na fase 2 do ticket 54 quase empatou no total e custou 14 s por busca em CPU; o gte-multilingual-reranker piorou) | a busca virar caminho crítico ou uma máquina com GPU (Gustavo, 2026-10-15) |
| Ollama ou ONNX como reserva local do FreeLLMAPI | cota ou queda do FreeLLMAPI atrapalhar o hub |
| Serviço de busca na rede (Meilisearch, OpenSearch) | o volume do hub crescer além do que o índice local aguenta |
| Plugins do Obsidian (Omnisearch, Smart Connections) | conveniência na máquina, quando o Obsidian estiver aberto |
| Template "suite de busca" no acervo do maestro (aprendizados da §6 da síntese) | a real necessidade de outra pesquisa ampla; o Gustavo já tem alterações em mente para a suite e as traz nesse momento |
| Usos do FreeLLMAPI além de embeddings (resumos) | depois que o hub existir |
| Dolt (reserva) e a sonda opcional | sem gatilho: só como opção se o CouchDB com LiveSync falhar na construção, o que é bem improvável (Gustavo, 2026-10-15) |
| Melhorar o recruta Designer partindo do vídeo https://youtu.be/Ysr7oNDajJI (pedido do Gustavo, 2026-10-15; vídeo ainda não assistido nem resumido) | a página Laços pronta (ticket 55); anda junto com o laço do system design |
| Item de estado próprio na barra do Codex (issue openai/codex#20244; texto pronto em `comentario-codex-20244.md`, não publicado; o servidor compartilhado com `codex --remote` é a reserva testada, `bancada-nome-conversa.md`) | cada atualização do Codex: o maestro confere a #20244 (Gustavo, 2026-10-15, ticket 14 rodada 8) |
| **Segundo mapa: o hub controla harnesses e modelos** (as cinco oportunidades da §3) | o hub construído e os cinco critérios verificados (R88, B) |
| claude-mem como referência de desenho: busca em três camadas (índice compacto, contexto, detalhe sob demanda); não instalar, duplica o hub e manda observações para fora (`pesquisa-claude-mem.md`) | o desenho das ferramentas do MCP de busca e do banco, ou o segundo mapa (memória de trabalho do agente) |
| Headroom: compressão local do que o agente lê (`pesquisa-headroom-e-omniroute.md`); o `learn` grava em `CLAUDE.md`/`AGENTS.md` | a cota do Claude travar a construção: teste curto num recruta só, sem telemetria, sem Serena, sem `learn` |
| OmniRoute: gateway com cotas grátis e troca automática de modelo, o mesmo papel do FreeLLMAPI (`pesquisa-headroom-e-omniroute.md`) | o segundo mapa (o hub como gateway de modelos), comparado ao FreeLLMAPI |
| Repositório de código numa pasta `local: true` dentro do hub, com uma linha no `.gitignore` da raiz (não replica, fica fora da busca, só naquela máquina); não testado. Por ora os repositórios ficam fora do hub e recebem contrato e skills pela porta do repositório fora do hub (Gustavo, 2026-10-16) | um caso real de repositório que precise morar junto das notas: testar o `.git` aninhado com o `.git` da raiz, a exclusão do LiveSync e a da busca |
| Workflow de skills "Pstack" para desenvolvimento, do vídeo https://www.youtube.com/watch?v=4wBVuj2an8E (pedido do Gustavo, 2026-10-16; vídeo ainda não assistido nem resumido, conteúdo não verificado). Ideia dele: mesclar o Pstack com as skills do Matt Pocock | pesquisa em fonte primária (o vídeo e o repositório do Pstack) quando o Gustavo pedir; candidato a peça do acervo do maestro (família `maestro-*`, fluxo de desenvolvimento) |
| Claude Code setup (pedido do Gustavo, 2026-10-16; não pesquisado: o que é e a fonte primária estão não verificados) | pesquisa em fonte primária quando o Gustavo pedir |
| Cartographer, CLI v2 (grafo SQLite + `brief` por caminho; pesquisado em `pesquisa-cartographer.md`; o plugin antigo fere "hub sem `CLAUDE.md`" e espalha subagentes) | a construção ter código e etapas sequenciais: testar a CLI v2 entre uma etapa e outra (pede Bun e teste no Windows) |

## 3. A visão nova: o hub como lugar que controla os agentes

Boa parte das peças já está decidida neste mapa, espalhada em tickets:

- **Contrato global** levado a Claude Code, Codex e Copilot por import e links simbólicos ("Portas de
  entrada do hub", "Testes da porta do repositório fora do hub").
- **Skills** do hub em todos os harnesses por junction ("Acesso dos agentes: pesquisa"; "Roteamento de
  skills", aberto).
- **MCP** com `instructions` e descrição das ferramentas como canal que chega aos três harnesses
  ("Contrato pelo MCP: pesquisa").
- **Hooks** de início de sessão e de fim de resposta (checagem do sync, nota de retomada) ("Contrato
  file-first", "Acesso dos agentes: decisão", aberto).
- **Guarda do acervo**: no Claude Code, mod e hook recusam ou pedem aval e podem impor um verificador
  noutro modelo ("Guarda do acervo: mods e hooks").
- **Acervo do maestro**: papéis, setups e contratos-opção como roteamento de modelos ("Maestri: padrão
  e liberdade").

O que a visão acrescenta e ainda não tem ticket (oportunidades, a pesquisar):

- **Política por modelo e por harness:** o que cada modelo pode fazer, em que pasta, com que ferramenta,
  definido num lugar só do hub e aplicado nos três harnesses.
- **O hub como gateway de modelos:** o FreeLLMAPI já serve a API da Anthropic e o `/v1/responses` do
  Codex; apontar os harnesses para um gateway que o hub configura daria controle de qual modelo atende
  cada trabalho (não verificado como política).
- **O MCP como ponto de aplicação:** ferramentas que aplicam regra (gravar só com `base_rev`, só na zona
  certa) em vez de só pedir no contrato.
- **Registro de uso:** quem usou que peça, papel ou modelo (o Maestri não registra; "Guarda do acervo").
- **Uma fonte, vários harnesses:** mudar a regra no hub e ela valer em todos, sem editar cada harness.
- **Memória de trabalho do agente (esquecimento de contexto):** o agente perde decisões já tomadas quando são muitos
  arquivos e eles saem do contexto. Exemplo: em 2026-10-14, a rodada 12 de "Arquitetura de pastas e frontmatter"
  contradisse a lição "a porta é a camada de busca". O Gustavo viu que "tem algumas formas de arrumar isso" e quer
  explorar e implementar no hub, **só na v2**, depois que este estiver pronto (Gustavo, 2026-10-14). Nada
  pesquisado ainda.
- **Uso dos limites do Claude:** o relatório de uso do Claude Code (2026-10-14, últimas 24 h, só desta máquina,
  aproximado) mostrou que:
  - 79% do uso foi com contexto acima de 150 mil tokens;
  - 74% veio de sessões cheias de subagentes;
  - 14% foi de contexto sempre ligado acima de 40 mil tokens (`CLAUDE.md`, ferramentas MCP, skills e memória);
  - 24% veio de subagentes "general-purpose".
  O próprio relatório sugere `/compact` e `/clear` entre tarefas, subagentes com modelo mais barato e prompts mais
  enxutos, e enxugar o contexto sempre ligado (`/context`). O Gustavo quer explorar isso **só na v2** (2026-10-14).
  Nada pesquisado ainda.

## 4. Ordem proposta das decisões

1. A visão entra no destino deste mapa ou fica para depois? **Respondida (B):** segundo mapa.
2. A peneira: o Gustavo confere a primeira passada (move itens entre agora, construção e radar). **Respondida:** aceita como está; itens levados aos tickets donos.
3. Camada de busca: os três fatos e o escopo do teste de bancada.
4. Depois, os tickets abertos na ordem do bloqueio: Como os agentes gravam; Arquitetura de pastas e
   frontmatter; Acesso dos agentes: decisão; Roteamento de skills; Passagem para a construção.

## 5. Respostas

<!-- cada resposta do Gustavo entra aqui, com data, antes de a nota "Rodada atual" ser reescrita -->

- 2026-10-14, **R88 (a visão entra no destino deste mapa?): B.** A visão "o hub controla como harnesses e
  modelos trabalham" vira um **segundo mapa**, que começa quando o hub estiver construído. Este mapa fecha
  como acervo, nos cinco critérios. O que já está decidido aqui (contrato global, skills, instruções do
  MCP, hooks, guarda, acervo do maestro) segue nos tickets de sempre. O que não tem ticket (política por
  modelo e harness, gateway de modelos, MCP aplicando regra, registro de uso, uma fonte para todos os
  harnesses) vai para o radar com o gatilho "hub construído", como semente do segundo mapa.
- 2026-10-14, **R89 (a primeira passada da peneira está certa?): aceita como está.** Sobre o template "suite de
  busca": "só vamos subir para construção quando surgir a real necessidade de outra pesquisa ampla. Eu já tenho em
  mente algumas alterações pra suite de busca, mas fica para quando surgir a real necessidade". Os itens de
  "Agora" e "Construção" viraram comentários nos tickets donos (Camada de busca, Arquitetura de pastas e
  frontmatter, Acesso dos agentes: decisão, Passagem para a construção).
