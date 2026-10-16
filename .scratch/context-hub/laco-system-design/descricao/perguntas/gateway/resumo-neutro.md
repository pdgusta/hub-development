# O context hub em poucas linhas (resumo neutro para os geradores de perguntas)

Escrito em 2026-10-15 a partir do mapa da frente (destino e decisões já tomadas) e do glossário. Serve só de contexto
para quem vai escrever perguntas; não é a descrição do hub.

## O que é

O context hub é a casa única do contexto de trabalho do Gustavo: notas, decisões, iniciativas, instruções e peças
para agentes de IA. Ele e os agentes leem e gravam nele. Existe uma cópia completa em cada uma das duas máquinas do
Gustavo (o notebook do trabalho e a máquina pessoal), e as duas são **pares**: nenhuma manda na outra, cada uma
trabalha sozinha e troca mudanças direto com a outra. Outros pares podem entrar depois.

O hub supera um cofre antigo de notas (o vault), que fica só como referência: o que é copiado de lá passa a ser
trabalhado só no hub.

## Quem usa

- **O Gustavo**, que vê e edita o hub como arquivos Markdown no Obsidian, ou direto no disco.
- **Agentes de código** (Claude Code, Codex, Copilot no VS Code e na linha de comando, Claude Desktop), em qualquer
  das duas máquinas, dentro ou fora do Maestri.
- **O maestro do Maestri**: um agente que monta e conduz equipes de outros agentes (recrutas) num canvas.
- **Clientes**: um computador ou sandbox sem cópia própria, que usa o hub através de um par ligado e, por padrão, só lê.

## As peças, com os nomes que aparecem nas decisões

- **Banco**: a verdade mora num banco (CouchDB), um em cada par, que se replicam nos dois sentidos pela rede privada
  entre as máquinas (Tailscale).
- **Vista Markdown**: os arquivos `.md` que o Gustavo edita no Obsidian. São gerados do banco, e o que ele edita volta
  para o banco.
- **Sincronizador**: em cada máquina, o processo que leva ao banco local o que muda no disco e traz ao disco o que
  muda no banco, sem depender do Obsidian aberto (o LiveSync: plugin do Obsidian e uma versão de linha de comando
  rodando como tarefa agendada). Ele também grava no disco, e conta como mais um escritor. Leva todo arquivo comum até
  200 MiB; pastas com ponto no nome não viajam.
- **MCP do banco**: o servidor pelo qual os agentes leem e gravam no banco. Cada gravação confere a versão que o agente
  leu; se outra pessoa mudou a nota no meio, vira conflito visível em vez de sobrescrever.
- **Camada de busca**: o que entrega ao agente o trecho certo sem ele ler tudo. Ainda em escolha entre duas
  ferramentas; os embeddings rodam localmente nas duas máquinas.
- **Colisão real e divergência**: duas versões de uma nota que o hub não junta sozinho ficam retidas, só aquela nota;
  o resto continua viajando. Divergência é colisão que o Gustavo ainda não viu resolvida, uma máquina que não consegue
  enviar as suas mudanças há mais que o limite com a outra ligada, ou um arquivo grande demais para viajar. Nunca pode
  ser silenciosa.
- **Vigia**: a cada 5 minutos confere e avisa (notificação do Windows) colisão, sync parado há 15 minutos, binário
  descartado e arquivo grande. Também há uma checagem no início de cada sessão de agente.
- **Tela de três vias**: para o Gustavo resolver uma colisão vendo as duas versões e a comum.
- **GitHub privado**: cópia de segurança diária do hub.
- **Pasta não replicada**: parte do hub que mora numa máquina só, fora do sync e do GitHub, alcançada pela outra por
  SSH. A busca da outra máquina não a vê.
- **Contrato do hub**: as instruções para os agentes (um `AGENTS.md` na raiz), levado a cada harness pelo arquivo global
  dele (com link simbólico), mais as skills em duas pastas globais. O contrato é file-first: o que importa é gravado
  no lugar certo sem o Gustavo pedir.
- **Nota de retomada**: um arquivo curto por trabalho (objetivo, onde parou, próximo passo, decisões, o que não deu
  certo, perguntas abertas, arquivos em jogo), sobrescrito, que permite a qualquer sessão nova continuar. Um hook ao
  fim de cada resposta do agente obriga a mantê-la em dia; a checagem de início de sessão a abre.
- **Portas de entrada**: os caminhos para chegar ao hub: sessão na raiz (a principal), sessão numa subpasta, Maestri,
  Obsidian, Claude Desktop, cliente pelo MCP de um par, sessão num repositório fora do hub.
- **Raízes**: as seis pastas do primeiro nível: `clients/` (iniciativas de cliente), `operations/` (trabalho contínuo),
  `initiatives/` (iniciativas sem cliente), `reference/` (conhecimento de referência), `agents/` (contrato, skills,
  papéis) e `inbox/` (captura rápida). O que termina vai para o `_archive/` da própria raiz.
- **Iniciativa e casa**: iniciativa é uma frente de trabalho com identificador, estado e próxima ação; cada uma mora
  numa casa só. Exemplos de iniciativas de cliente: STRATA, VOEGOL, AVIANCA, TRF3, SBF.
- **Acervo do maestro**: peças prontas (papéis, setups, contratos-opção e outras) que o hub oferece a todo maestro, como
  opção e não como regra, numa família de skills. Alterar o acervo pede aval do Gustavo, imposto por uma guarda.

## Os cinco critérios que o hub tem de cumprir

1. Agentes em qualquer máquina acham o trecho certo sem ler tudo.
2. O que importa é gravado no lugar certo sem o Gustavo pedir.
3. Os `.md` continuam editáveis no Obsidian, a busca está sempre acessível ao agente, e o agente também pode editar
   direto no disco, com sync para a outra máquina.
4. Nada diverge em silêncio entre as máquinas.
5. Existe proteção para a edição concorrente (duas gravações no mesmo arquivo em que nenhuma vê a outra).
