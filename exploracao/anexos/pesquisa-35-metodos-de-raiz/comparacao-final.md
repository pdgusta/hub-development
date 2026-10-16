# Comparação final: métodos conhecidos contra os nove tipos de raiz

Ticket: "Métodos conhecidos de organizar a raiz" (`.scratch/context-hub/issues/35-metodos-de-organizar-a-raiz.md`).
Data: 2026-10-10.

**Base:** só as cinco rodadas do debate entre Astrolabio (métodos de notas pessoais), Cinzel
(sistemas e memória de agentes) e Junco (uso real), em `debate/r1-*.md` a `debate/r5-*.md`. Os três
são agentes Claude Code em Sonnet 5.5, sem subagentes. Eles leram os 15 JSON desta pasta, extraídos
de fonte primária por 15 subagentes Haiku 5.5 com URL fixa. Quando uma linha abaixo cita um método,
a referência é o JSON citado no debate.

## 1. O que os métodos dizem sobre a raiz

| Método | Corta a raiz? | Por qual critério | Uso para o hub (conclusão do debate) |
|---|---|---|---|
| PARA (`01`) | sim: Projects, Areas, Resources, Archives | acionabilidade e prazo: projeto termina, área "continues indefinitely" | é o **único** que sustenta a coluna "Termina?": separa clientes (projeto) de operação contínua (área) |
| Steph Ango (`07`) | quase não: notas na raiz, mais `References`, `Clippings`, `Daily`… | evita decidir pasta, porque a nota "pertence a mais de uma área" | sustenta referência como tipo próprio; contradiz "um lugar só" e não serve de raiz do hub |
| FHS (`08`) | sim | dois eixos: compartilhável × não e estático × variável; o que difere vai para diretórios diferentes | o **achado central**: o que não replica não divide pasta com o que replica. É o critério da pasta não replicada |
| XDG (`09`) | sim: config, data, state, cache, runtime | natureza do dado | config × data sustenta a oficina; o runtime "MAY be subjected to periodic clean-up" sustenta a entrada com limpeza |
| Diretório `.claude` (`15`) | sim | escopo (projeto no git × pessoal na máquina) e caminho fixo lido pelo harness | sustenta a oficina dos agentes e o perfil de máquina fora da réplica |
| Johnny.Decimal (`02`) | sim, por números | índice que liga tudo | repete a cadeia de índices do vault; só o teto de dez por nível aproveita |
| Diátaxis (`06`) | quatro formas de documento | forma do texto | repete o corte por tipo de documento do vault |
| Cline Memory Bank (`10`) | uma pasta por projeto com seis arquivos | função do arquivo | só inspira a nota de retomada; "read ALL" a cada tarefa é o oposto da camada de busca |
| Zettelkasten (`04`), Evergreen (`14`) | não | por conceito, não por projeto | desfazem o isolamento por iniciativa |
| GTD (`05`) | não (só etapas) | capture → clarify | sustenta a **função** da entrada, não uma pasta |
| LYT/ACE (`03`) | não verificado | a fonte não descreve o ACE | sem argumento |
| Memory tool (`12`), Letta (`13`), Basic Memory (`11`) | não nomeiam categorias de topo | — | respondem o que fica dentro de uma unidade, não o corte da raiz |

## 2. Posição final dos três para cada tipo

Os três convergiram nas posições na rodada 5. A última divergência, sobre juntar 3 e 4, terminou
quando Astrolabio mudou de lado na r5.

| # | Tipo | Posição | O que sustenta |
|---|---|---|---|
| 1 | Clientes | **manter** | PARA Projects; FHS (não compartilhável) |
| 2 | Operações contínuas | **manter, separado de 1** | PARA Areas, "continues indefinitely". Compactar em vez de arquivar é regra do hub, não do método |
| 3+4 | Produtos e frentes + Estudo e laboratório | **juntar** em "iniciativas sem cliente" | nenhum método os separa; a iniciativa mora numa casa só (GLOSSARY), e um spike que vira produto não pode mudar de casa |
| 5 | Conhecimento de referência | **manter, sem dado de cliente**; só recebe conteúdo sanitizado, por promoção | PARA Resources; References do Ango; o "estático" do FHS |
| 6 | Oficina dos agentes | **manter**; o **perfil de máquina** vai para uma subpasta não replicada | `.claude` (caminho fixo, escopo); XDG (config × data) |
| 7 | Entrada | **manter, local em cada máquina**, com limite de idade e aviso | XDG runtime com limpeza; GTD dá só a função |
| 8 | Arquivo | **deixa de ser raiz**: vira `_arquivo/` dentro de cada raiz, herdando a declaração de replicação dela | só o PARA tem Archives no topo, e ele não trata replicação; um arquivo único misturaria pasta replicada e não replicada |
| 9 | Pessoal | **condicional**: se não replica, é raiz própria (FHS); se replica e os agentes leem, cai em 3+4 ou 5 | FHS (`/home` opcional); Ango |

**Resultado: seis raízes (1, 2, 3+4, 5, 6, 7) e uma condicional (9).** A nota de retomada mora dentro
da pasta de cada iniciativa, com nome fixo (precedentes: o Cline e as subpastas por projeto do PARA).

## 3. O que ficou para teste (ticket 12)

- **Arquivar por pasta `_arquivo/` ou por propriedade `estado`.** Os três preferem a pasta, com uma
  condição: mover uma pasta com duas máquinas editando não pode virar colisão no sincronizador, e a
  busca precisa filtrar por caminho. Se uma das duas falhar, usa-se a propriedade. Regra comum:
  nunca pasta e campo espelhando a mesma informação.
- **Captura de cliente na máquina errada.** Se a pasta do cliente mora só numa máquina, uma captura
  feita na outra precisa ser promovida pelo SSH ou esperar. Cinzel retirou na r5 a sua versão, que
  dizia "promove na mesma máquina".

## 4. O que nenhum método respondeu

- Pasta não replicada com duas cópias editáveis: o FHS dá o critério, não o mecanismo.
- O destino do que envelhece: `nao_verificado` em oito dos quinze. "Compactar" não vem de nenhum método.
- Organização pensada para agentes: nenhum método de notas foi feito para agente.
- Como a pasta do hub vira o caminho que o harness lê: o `.claude` diz onde o harness lê, não a ponte.
- Controle de leitura por agente ("este agente não pode ler"): não é declarável; só a replicação é.
- Edição concorrente: nenhum dos quinze trata.

## 5. Perguntas que os três deixaram para o Gustavo

1. O SOC STRATA é cliente (tipo 1) ou operação contínua (tipo 2)?
2. Em qual máquina mora cada pasta de cliente?
3. O conteúdo pessoal replica entre as máquinas?
4. Um spike às vezes vira produto? Só confirma a junção de 3 e 4.
