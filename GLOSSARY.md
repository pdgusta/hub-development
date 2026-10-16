# Context Hub

Vocabulário do context hub do Gustavo: a casa única do contexto que ele e os agentes leem e gravam
nas duas máquinas.

## Language

**Context hub**:
A casa única do contexto, com uma cópia completa em cada máquina. A verdade mora num banco, que o
agente lê e grava; o Gustavo vê o hub pela vista Markdown.
_Avoid_: Guild, vault (o vault `ai-operating-system` é outra coisa)

**Máquina**:
Cada um dos dois computadores do Gustavo (o notebook da ARMIS e a máquina pessoal). As duas são pares.
_Avoid_: hospedeiro, réplica, servidor

**Par**:
Um computador com uma cópia completa e editável do context hub, que trabalha sozinho e troca mudanças
direto com outro par. Nenhum par é a referência dos outros. As duas máquinas são pares, e outros podem
entrar.
_Avoid_: host, servidor, mestre

**Cliente**:
Um computador ou sandbox que usa o context hub através de um par, sem cópia própria. Só funciona com
um par ligado e, por padrão, só lê.
_Avoid_: par (quando não tem cópia), visitante

**Camada de busca**:
O que entrega ao agente o trecho certo do context hub sem que ele leia tudo. Pode também gravar.
_Avoid_: RAG, Guild

**Edição concorrente**:
Duas gravações no mesmo arquivo em que nenhuma vê a outra. Acontece em máquinas diferentes entre um
sync e outro, ou com dois agentes na mesma máquina.
_Avoid_: edição simultânea

**Iniciativa**:
Uma frente de trabalho com identificador estável, estado e próxima ação. É a unidade que mora numa
casa só. Esta frente do context hub é uma iniciativa.
_Avoid_: workload, projeto (quando quer dizer a unidade)

**Raiz**:
Uma das seis pastas do primeiro nível do context hub, cada uma com um comportamento próprio:
`clients/` (iniciativas de cliente), `operations/` (trabalho contínuo, sem fim), `initiatives/`
(iniciativas sem cliente: produtos, frentes, estudo), `reference/` (conhecimento de referência,
promovido), `agents/` (a oficina dos agentes: contrato, skills, papéis) e `inbox/` (captura rápida).
O que termina vai para o `_archive/` da própria raiz. A pasta `initiatives/` guarda só as iniciativas
sem cliente; as de cliente moram em `clients/`.
_Avoid_: área, categoria

**Casa**:
O lugar único onde uma iniciativa é trabalhada. O destino é o context hub ser a casa de tudo; o vault
`ai-operating-system` é só referência e será superado. Quando um conteúdo do vault é copiado para o
hub, a casa dele passa a ser o hub, e o que ficou no vault não conta como segunda casa.
_Avoid_: home, origem

**Vista Markdown**:
Os arquivos `.md` pelos quais o Gustavo vê e edita o context hub (no Obsidian). Não é a verdade: é
gerada a partir do banco, e o que ele edita nela volta para o banco.
_Avoid_: fonte, cópia

**Sincronizador**:
O processo de cada máquina que leva ao banco local o que muda no disco do hub e traz ao disco o que
muda no banco, sem depender do Obsidian aberto. Também grava no disco, e conta como mais um escritor.
_Avoid_: sync (quando quer dizer o processo), plugin

**Colisão real**:
Duas versões de uma nota que o hub não junta sozinho: mudaram o mesmo trecho, uma apagou o que a outra
mudou, ou já não existe a versão comum das duas. Mudanças em trechos diferentes da mesma nota não são
colisão. Na colisão só aquela nota fica retida; o resto continua viajando.
_Avoid_: conflito (quando a junção é automática)

**Divergência**:
Uma colisão real que o Gustavo ainda não viu resolvida (inclusive a de arquivo binário, que o hub
resolve sozinho ficando com a versão mais nova), uma máquina que não consegue levar as próprias
mudanças à outra há mais que o limite enquanto a outra está ligada, ou um arquivo que não viaja por
passar do tamanho máximo. A outra máquina desligada não é divergência. Nunca pode ser silenciosa: o
aviso aparece na máquina que travou.

**Pasta não replicada**:
Parte do context hub que mora numa máquina só e fica fora do sync, do GitHub e da busca da outra máquina: o que
tem ponto no nome (`.git`, `.secrets/`, `.maestri/`) e a pasta cujo `index.md` declara `local: true`. Outra nota a
cita por um link `par://<par_id>/<caminho>`.
_Avoid_: pasta só por SSH

**Nota de retomada**:
O arquivo curto, um por trabalho, que permite a qualquer sessão nova (outro agente, modelo ou máquina)
continuar de onde a anterior parou: objetivo, onde parou, próximo passo, decisões, o que não deu
certo, perguntas abertas, arquivos em jogo. É sobrescrito, não acumulado. Um hook ao fim de cada
resposta obriga o agente a mantê-lo em dia.
_Avoid_: handoff, checkpoint (o checkpoint é o momento de gravar, não o arquivo)

**Porta de entrada**:
Cada caminho pelo qual o Gustavo ou um agente chega ao context hub: sessão na raiz, sessão numa
subpasta, Maestri, Obsidian, Claude Desktop, cliente pelo MCP de um par ou sessão num repositório
fora do hub. A sessão na raiz é a porta principal; cada uma das outras ganha só o que precisa.
_Avoid_: acesso, entrada (a raiz `inbox/` é outra coisa)

**Acervo do maestro**:
O conjunto de peças prontas que o context hub oferece a todo maestro do Maestri, dentro ou fora do hub,
para montar e conduzir um workspace sem redescobrir. São opções, não regras.
_Avoid_: biblioteca (é a do Maestri), templates

**Peça**:
Uma unidade reutilizável do acervo do maestro: um papel, um setup, um contrato-opção e outros tipos.
Cada peça aceita uma versão local por iniciativa.
_Avoid_: item, recurso

**Contrato-opção**:
Uma peça que descreve um jeito recomendado de fazer algo (roteamento de modelos, orquestração, onde
abrir um workspace), para o maestro seguir quando ninguém disser outra coisa. Não obriga.
_Avoid_: regra, política
