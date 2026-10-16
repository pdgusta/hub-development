## Faixa 7: Vigia e divergência

Entrega: em cada par, uma vigia agendada que acha toda divergência, avisa por notificação do Windows quando o
estado piora e grava um estado curto que cada harness mostra (checagem de início nos três, mod no Claude Code,
`statusLine` no Copilot, `notify` no Codex), mais o comando que recupera a versão perdida de um binário.
Origem: tickets 08 e 33 (o que conta como divergência e como se avisa), 14 (como cada harness mostra o estado).
O ticket 53 (canal de aviso do portal) não entra: ele não decide nada do hub (ver Out of scope).

### User stories

1. Como Gustavo, quero uma vigia em cada máquina, rodando a cada 5 minutos, para que nenhuma divergência fique
   silenciosa.
2. Como Gustavo, quero que o aviso apareça na máquina que travou, para saber onde agir, já que a outra máquina não
   tem como saber de uma mudança que não chegou a ela.
3. Como Gustavo, quero que a vigia leia o estado das replicações do CouchDB local, para saber se esta máquina está
   levando as próprias mudanças à outra.
4. Como Gustavo, quero ser avisado quando esta máquina não leva as próprias mudanças à outra há mais de 15 minutos
   com a outra ligada na tailnet, para não trabalhar achando que as duas estão em dia.
5. Como Gustavo, quero que a outra máquina desligada não conte como divergência nem dispare alarme, para que o aviso
   só apareça quando há algo a fazer.
6. Como agente no início de uma sessão, quero receber a hora da última troca com a outra máquina quando ela está
   desligada, para informar o Gustavo sem alarme.
7. Como Gustavo, quero que todo conflito de texto aberto no banco (`.md`, `.txt`, `.csv`) conte como divergência até
   ser resolvido, para que uma colisão real nunca passe despercebida.
8. Como Gustavo, quero saber que numa colisão de texto só aquela nota fica retida e o resto continua viajando, para
   não achar que a máquina inteira parou.
9. Como Gustavo, quero que um conflito aberto com o Obsidian fechado apareça pela vigia, para não depender de abrir o
   Obsidian para descobrir a colisão.
10. Como Gustavo, quero que a vigia ache o ramo apagado quando o hub resolve sozinho a colisão de um binário (fica a
    versão de `mtime` mais novo), para saber que uma versão foi descartada.
11. Como Gustavo, quero que o binário descartado conte como divergência até eu olhar, para não perder trabalho em
    silêncio (inclusive `.py` e `.json`, que viajam como binário).
12. Como Gustavo, quero um comando que recupere a versão perdida de um binário para um arquivo ao lado do original,
    para escolher qual fica sem apagar nenhuma.
12a. Como Gustavo, quero que a vigia cite a nota em conflito e o binário descartado pelo caminho em claro, mesmo com o
    banco cifrado (E2EE, 34; caminho ofuscado, 48), para eu saber o que olhar.
12b. Como Gustavo, quero que a falha da cópia diária (faixa 10) apareça como item no estado da vigia, com notificação
    (**[aceita]**; ligado à pendência "quem percebe a falha" do 56, que fica fora desta construção), para não descobrir
    só na hora de recuperar.
13. Como Gustavo, quero que a vigia liste todo arquivo acima de 200 MiB, que não viaja, e que isso conte como
    divergência, para saber o que só existe numa máquina.
14. Como Gustavo, quero que a vigia confira se o sincronizador (o CLI do LiveSync) está vivo, para saber quando o elo
    entre disco e banco parou.
15. Como Gustavo, quero que a vigia confira se o Config Doctor do LiveSync travou o plugin, para saber quando o sync
    do Obsidian parou por ele.
16. Como Gustavo, quero uma notificação do Windows quando o estado piora, para ver o problema mesmo sem nenhuma sessão
    de agente aberta.
17. Como Gustavo, quero que a vigia não repita a notificação enquanto o estado não piora, para que o aviso continue
    significando algo.
18. Como agente, quero que a vigia grave um estado curto num arquivo local, para que a checagem de início e as telas
    de cada harness leiam sem consultar o banco.
19. Como agente no par, quero que o hook de início de sessão leia o arquivo da vigia e mostre o aviso quando houver
    divergência, para começar a sessão sabendo do problema.
20. Como agente no par, quero que, faltando o arquivo da vigia, a checagem de início use a ferramenta do MCP como
    reserva, e que, faltando os dois, ela diga "estado indisponível" sem afirmar que o sync foi conferido, para não
    começar às cegas nem com falsa calma.
21. Como agente num cliente, quero que a checagem de início use a ferramenta do MCP do par, para saber do estado sem
    ter vigia própria.
22. Como Gustavo, quero que, onde o hook de início falhar num harness, a checagem vire regra no contrato daquele
    harness, para que nenhum harness fique sem checagem.
23. Como Gustavo, numa sessão do Claude Code, quero um mod que mostre o estado da vigia o tempo todo, para ver a
    divergência sem esperar a próxima sessão.
24. Como Gustavo, numa sessão do Copilot (CLI), quero o estado da vigia na `statusLine`, para ver a divergência
    durante a sessão.
25. Como Gustavo, numa sessão do Codex, quero o estado da vigia na checagem de início e, no fim de cada turno, uma
    notificação do Windows disparada pelo `notify` quando houver divergência, já que o Codex não tem item de status
    alimentado por script.
26. Como agente, quero que os hooks e telas da vigia saiam na hora quando a pasta não é do hub, para que a vigia não
    polua sessões de fora.
27. Como agente aberto num papel do Maestri, quero que a checagem de início rode também ali, para receber o aviso
    dentro de um papel (passou nos três com o `MAESTRI_TERMINAL_ID` do próprio recruta).
28. Como Gustavo, quero que a mesma definição de divergência valha para a vigia, para a checagem e para o glossário,
    para que "divergência" signifique uma coisa só em todo lugar.
29. Como agente que recebe o aviso, quero saber qual nota ou arquivo está em divergência e de que tipo, para resolver
    na sessão com o Gustavo vendo.
30. Como construtor da faixa 8, quero receber os hooks, o mod e as configurações de tela da vigia como fragmentos
    separados, para juntá-los no kit sem editar o que é de outra faixa.

### Implementation decisions

- **Definição de divergência** (08, 33, glossário): três situações e só elas.
  - Colisão real ainda não vista pelo Gustavo: trechos sobrepostos, um lado apaga o que o outro mudou, ou falta a
    versão comum. Texto (`.md`, `.txt`, `.csv`) segura só aquela nota e abre a janela de conflito; conta até ser
    resolvido. Binário fica com o `mtime` mais novo; conta até o Gustavo olhar.
  - Máquina que não leva as próprias mudanças à outra há mais de 15 minutos, com a outra ligada na tailnet. Outra
    desligada não é divergência; só se informa a hora da última troca.
  - Arquivo acima de 200 MiB (`syncMaxSizeInMB`), que não viaja.
  - Mudanças em trechos diferentes da mesma nota não contam; a cópia de conflito aberta (08) é coberta pelo conflito
    aberto no banco.
- **Vigia** (33): uma por máquina, tarefa agendada a cada 5 minutos. Lê:
  - o estado das replicações do CouchDB local (`_scheduler/docs`);
  - os conflitos abertos no banco;
  - os binários descartados (ramos apagados pela resolução automática);
  - os arquivos acima do limite de 200 MiB;
  - se o sincronizador está vivo;
  - se o Config Doctor travou o plugin (requisito do 33, mesmo sem detector verificado);
  - se o outro par está ligado: o núcleo propõe testar `HUB_OUTRO_PAR_URL` (**[aceita]**), mas URL sem resposta não
    prova máquina desligada; a vigia distingue máquina desligada, serviço parado com a máquina ligada e estado não
    verificável; o incerto nunca vira `ok` nem suprime a divergência de replicação parada, e vai, no mínimo, como
    `informa`, com o motivo ("outro par sem resposta; não sei se está desligado") (33, R63; a representação é
    **[aceita]**).
  Com E2EE (34), lê o banco cifrado e cita a nota pelo caminho em claro (48; o CLI dá o caminho: `ls`, `info`,
  `cat-rev`; ler direto ou pelo CLI é escolha técnica).
  Saídas: notificação do Windows quando o estado piora, e um estado curto num arquivo local que a checagem de início
  e as telas leem (33, 14).
- **Comando de recuperar binário** (33, R71): grava a versão perdida num arquivo ao lado do original; nada é apagado.
- **Checagem de início de sessão** (14, rodada 2): no par, o hook de início lê o arquivo da vigia; sem ele, a
  ferramenta do MCP; no cliente, a ferramenta do MCP; sem os dois, "estado indisponível" (a bancada de acesso devolveu
  "DESCONHECIDO" nesse caso). Onde o hook falhar, regra no contrato daquele harness. Hooks no
  escopo do usuário, saindo na hora fora do hub (14, rodada 3). A mesma checagem abre a nota de retomada (faixa 2);
  a faixa 7 entrega só a parte do estado da vigia.
- **Estado na tela, por harness** (14, rodadas 7 e 8):
  - Claude Code: um mod que mostra o estado o tempo todo; a forma (linha de status ou faixa acima do prompt) se
    escolhe na construção (33, R64).
  - Copilot: `statusLine` por script.
  - Codex: a checagem de início e o `notify` no fim de cada turno, que dispara a notificação do Windows quando há
    divergência (14, rodada 8). A vigia também notifica quando o estado piora (33): os dois canais ficam, por decisão;
    o comportamento combinado é descrito e testado na construção, e nenhum dos dois repete o aviso enquanto o estado não
    muda (Gustavo, 2026-10-16). O
    servidor compartilhado com `codex --remote` fica só como reserva documentada.
- **Ferramenta do MCP de estado** (14): a vigia é a fonte do estado; a ferramenta mora no MCP (faixa 5) e serve ao par
  como reserva e ao cliente como canal principal.
- **Entrega à faixa 8** (fronteira combinada no plano): scripts dos hooks e fragmento de configuração por harness numa
  pasta da faixa; o mod numa pasta de mods; instalador próprio idempotente, que lê o HOME de ensaio e aceita
  simulação. Sem editar configuração de outra faixa.
- **Arquivo de estado** (**[aceita]**; o 33 decide "um estado curto que a checagem lê", o 12 que o que tem ponto não
  replica): `C:\context-hub\.local\vigia\estado.json`, fora do banco e do `.git`, gravado por troca atômica, com
  `nivel` por item (`ok | informa | divergencia`) e o do topo igual ao pior, resumo de uma linha, outro par, última
  troca e itens (inclusive `copia-diaria`, da faixa 10).

### Testing decisions

- **Costura:** hub de ensaio (o gerado pelo maestro na forma do ticket 12, com um binário pequeno) e HOME de ensaio;
  CouchDB descartável da faixa em 127.0.0.1:5997, com E2EE (**[formato]**; com etapas sequenciais, um banco de ensaio
  só pode servir às faixas 4, 5 e 7); a vigia roda em laço no terminal; a tarefa agendada de 5 min (33) sai como XML e
  o instalador só com `-WhatIf`; registrar é `ready-for-human` (**[formato]**).
- **Só comportamento externo:** o teste olha o arquivo de estado, a notificação disparada (ou um registro dela em
  modo de ensaio), a saída da checagem de início e o que o comando de recuperar grava. Nada da lógica interna da vigia.
- **Casos da vigia:**
  - conflito de texto forjado no CouchDB de ensaio: o estado vira divergência com a nota citada; as outras notas
    seguem replicando;
  - colisão de binário forjada: a vigia lista o binário descartado; o comando de recuperar grava, ao lado, um arquivo
    com o conteúdo da versão perdida;
  - arquivo acima de 200 MiB no hub de ensaio: listado como divergência;
  - replicação parada há mais de 15 minutos com o outro par de ensaio ligado: divergência; com o outro par desligado:
    só informa, com a hora da última troca, sem notificação;
  - sincronizador de ensaio parado: o estado o aponta;
  - item `copia-diaria` gravado pela faixa 10: `informa`, com notificação (**[aceita]**);
  - os casos de conflito e de binário num CouchDB de ensaio com E2EE: a vigia cita o caminho em claro;
  - mesmo estado em duas passadas seguidas: uma notificação só; estado pior na terceira: nova notificação.
- **Harnesses reais em modo não interativo**, com HOME de ensaio e uma pasta do hub de ensaio:
  - `claude -p`, `codex exec` e `copilot -p` começam a resposta com o aviso quando o estado é divergência, e calados
    quando é ok;
  - sem o arquivo de estado, a mesma checagem chega pela ferramenta do MCP de ensaio; sem o arquivo e sem o MCP, a
    checagem diz "estado indisponível";
  - aberto numa pasta fora do hub, o hook sai na hora e nada aparece.
- **Aceite de ponta a ponta:** com um conflito forjado no CouchDB de ensaio, a vigia avisa por notificação e o estado
  aparece no mod do Claude Code; a checagem de início dos três harnesses mostra o aviso.
- **Nada global real** (Agendador do Windows, `~/.claude`, `~/.codex`, `~/.copilot`, hooks do usuário) sem o aval do
  Gustavo. Globais conferidos por hash antes e depois de cada teste.

### Out of scope

- O sincronizador, o CouchDB, a replicação, o limite de 200 MiB no CLI e no plugin, e a exclusão `**/.*` (faixa 4).
- A conferência de versão ao gravar, no MCP (faixa 5) e no disco (faixa 6); a edição do Gustavo no Obsidian fica sem
  proteção (08).
- A ferramenta do MCP em si (faixa 5): esta faixa só define o que ela devolve sobre a vigia.
- A nota de retomada na checagem de início (faixa 2).
- Instalar hooks, mod e telas nos harnesses (faixa 8 junta os fragmentos).
- A segunda máquina e a tailnet reais: o par B é de ensaio.
- O servidor compartilhado do Codex com `codex --remote` (reserva) e o comentário na issue #20244 do Codex (radar,
  sem publicar).
- A tela de três vias editável para resolver conflito (25, logo depois da construção).
- Resolver colisão automaticamente: o agente resolve na sessão, com o Gustavo vendo.
- O canal de aviso do portal do projeto (ticket 53): fora do mapa, não decide nada do hub; o canal A ficou valendo
  para o portal, não para a vigia.

### Pontos abertos para a construção

- **Não verificado:** notificação do Windows disparada por tarefa agendada (08); o toast pelo `notify` do Codex (14);
  o que a `statusLine` do Copilot mostra de fato na tela (14).
- **Forma do mod** do Claude Code: linha de status ou faixa acima do prompt (33, R64: "na construção").
- **"Piora":** o critério de quando o estado piorou (e portanto notifica) não foi decidido.
- **"Até o Gustavo olhar":** como o binário descartado deixa de contar como divergência não foi decidido.
- **Detectores:** o outro par ligado: `HUB_OUTRO_PAR_URL` é um sinal (**[aceita]**), não o detector inteiro; como
  distinguir desligada de serviço parado fica proposto/aberto, e o incerto vai, no mínimo, como `informa`, com o
  motivo; o ramo apagado de binário, lido
  do CouchDB local ou pelo CLI com E2EE (48); fica sem mecanismo só como saber que o Config Doctor travou o plugin.
- **Avisos no Codex:** a vigia (quando piora, 33) e o `notify` (fim de turno com divergência, 14) coexistem por
  decisão; nenhum dos dois repete o aviso enquanto o estado não muda (Gustavo, 2026-10-16).
- **Acima de 50 MiB** (33, R76): comportamento não testado; conferir na construção junto com a faixa 4.
- **Tarefa agendada no ensaio:** XML e `-WhatIf` no ensaio, registro `ready-for-human` (**[formato]**).

## Faixa 8: Portas dos harnesses e kit de par

Entrega: o kit de par, idempotente e com simulação, que confere a máquina e liga cada harness (Claude Code, Codex,
Copilot CLI e Copilot do VS Code) ao hub: contrato por link simbólico ou import, skills por junction, MCP de busca e
de banco, hooks e telas das outras faixas, e o Codex no modo decidido. Origem: tickets 04, 13, 14, 18, 36, 37, 38, 42,
45, 46 e os comentários do ticket 16 sobre o kit de par.

### User stories

1. Como Gustavo, quero instalar uma máquina como par com um kit só, para não repetir à mão a ligação de cada harness.
2. Como Gustavo, quero rodar o kit duas vezes e a segunda não mudar nada, para poder rodá-lo sempre que algo mudar.
3. Como Gustavo, quero uma simulação do kit que mostra o que ele faria sem tocar em nada, para revisar antes de
   aplicar.
4. Como Gustavo, quero que o kit faça cópia de todo arquivo global antes de tocá-lo, para poder voltar atrás.
5. Como Gustavo, quero que o kit confira que não há `CLAUDE.md` no hub nem em nenhuma pasta acima dele, porque um
   `CLAUDE.md` assim desliga todos os `AGENTS.md` no Claude Code.
6. Como Gustavo, quero que o kit confira o modo de desenvolvedor do Windows, porque o link simbólico depende dele.
7. Como Gustavo, quero que o hub more em `C:\context-hub`, no NTFS, nas duas máquinas, com o caminho no perfil de
   cada máquina e não no contrato, para que todos os harnesses e o Obsidian trabalhem do mesmo lado.
8. Como agente Claude Code fora do hub, quero receber o contrato pelo import absoluto no `~/.claude/CLAUDE.md`, para
   seguir o hub em qualquer pasta.
9. Como agente Codex fora do hub, quero receber o contrato por um link simbólico em `~/.codex/AGENTS.md`, porque o
   Codex não aceita import.
10. Como agente Copilot (CLI e VS Code) fora do hub, quero receber o contrato por um link simbólico em
    `~/.copilot/copilot-instructions.md`, para seguir o hub nos dois Copilots.
11. Como Gustavo, quero que o kit tire o GSD do arquivo global do Copilot (`~/.copilot/copilot-instructions.md`) e do
    escopo global das skills, com cópia antes, e ligue o contrato do hub no lugar, para que só o contrato e as skills
    de uso geral fiquem globais (15, rodada 2, o mais recente; o "juntar os dois" do 36 e do 42 caiu).
12. Como Gustavo, quero editar o contrato só dentro do hub, porque gravar pelo link com uma ferramenta que cria
    arquivo novo troca o link por uma cópia e a edição não chega ao hub.
13. Como Gustavo, quero link simbólico e nunca link físico, porque o físico se solta sem aviso quando uma ferramenta
    troca o arquivo do hub.
14. Como agente, quero receber o contrato uma vez só, mesmo na raiz do hub com o arquivo global também ligado, para
    não gastar contexto em dobro.
15. Como agente Claude Code, quero as skills de uso geral do hub (`agents/skills/<skill>/`) por junction em
    `~/.claude/skills`, para usá-las em qualquer pasta.
16. Como agente Codex ou Copilot, quero as skills de uso geral do hub por junction em `~/.agents/skills`, a pasta que
    os dois leem, para usá-las em qualquer pasta.
16a. Como recruta de um papel, quero que as skills do meu papel entrem só na pasta do papel, pela receita de setup
    (faixa 9), e não na junction global, para não pagar a lista inteira a cada turno (15, rodada 2).
17. Como maestro, quero a família `maestro-*` ligada pelas mesmas junctions, para consultar o acervo em qualquer
    workspace.
18. Como Gustavo, quero que o kit tire o GSD do escopo global, com cópia antes, para que só as skills de uso geral
    fiquem globais.
19. Como agente Claude Code num papel do Maestri, quero `claude-md-and-agents-md` ligado em cada par, para receber o
    `AGENTS.md` do hub apesar do `CLAUDE.md` que o Maestri grava na pasta do papel.
20. Como agente Codex ou Copilot numa subpasta, numa iniciativa ou num papel do Maestri, quero chegar ao `AGENTS.md`
    da raiz pelo `.git` da raiz do hub, sem marcador de raiz.
21. Como agente Claude Code numa subpasta, quero ler a cadeia de `AGENTS.md` até a raiz sozinho.
22. Como agente aberto na raiz do hub, quero ler o `AGENTS.md` da raiz e achar o resto pela busca, porque a sessão na
    raiz é a porta principal.
23. Como agente no par, quero os MCP de busca e de banco ligados nos três harnesses, presos a 127.0.0.1, para ler e
    gravar o hub sem passar pela rede.
24. Como Gustavo, quero o token do MCP do banco numa variável de ambiente da máquina, nunca escrito na configuração,
    para não espalhar segredo.
25. Como agente Codex, quero as ferramentas do MCP do hub aprovadas de antemão, para não travar pedindo aprovação a
    cada chamada.
26. Como Gustavo, quero o Codex do hub com `danger-full-access` nas duas máquinas, porque o sandbox elevado falha nesta
    máquina e o não elevado deixa o agente sem shell.
27. Como Gustavo, quero que o kit rode o teste mínimo do sandbox elevado a cada atualização do Codex e me avise quando
    passar, para eu decidir se volto ao sandbox.
28. Como Gustavo, quero os hooks do hub no escopo do usuário nos três harnesses, saindo na hora fora do hub, para que
    valham em qualquer porta, inclusive dentro de um papel do Maestri.
29. Como Gustavo, quero que o kit deixe cada hook do hub aprovado no Codex pelo hash em `hooks.state`, para que o Codex
    não abra a tela `/hooks` a cada sessão.
30. Como Gustavo, quero só hooks de usuário no Copilot, porque o de projeto exige pasta confiável.
31. Como construtor de outra faixa, quero que o kit junte o meu fragmento de hook por evento, acrescentando sem apagar
    o que já existe, para que hooks de várias faixas convivam no mesmo evento.
32. Como Gustavo, quero que o kit instale o mod do Claude Code (estado da vigia e fim da resposta), para ter as telas
    das faixas 2 e 7.
33. Como Gustavo, quero que o kit ligue no Copilot o hook `agentStop` e a extensão `onAgentStop` (com
    `--experimental`), para o fim da resposta funcionar como decidido.
34. Como Gustavo, quero que o kit ligue no Codex o hook `Stop`, o `PreToolUse` e o `notify`, para fim da resposta,
    recusa antes da ferramenta e aviso da vigia.
35. Como Gustavo, quero que o kit ligue a `statusLine` do Copilot ao estado da vigia.
36. Como Gustavo, quero que o kit rode de novo no fim e pegue os fragmentos que chegaram depois, sem refazer o resto.
37. Como Gustavo no Claude Desktop, quero chegar ao hub pela ponte `mcp-remote` (MCP stdio) para a busca e para o MCP
    do banco com escrita (11) e pela pasta conectada do Cowork com "Folder instructions" apontando o `AGENTS.md`, para
    pedir coisas pelo Desktop. (Quem gera e instala a ponte: o núcleo diz faixa 10; **[formato]**.)
38. Como Gustavo com a conta Copilot Enterprise, quero que o contrato, as skills, os hooks e o MCP do hub funcionem no
    CLI e no VS Code, para usar o hub no trabalho (testado: nenhuma política aplicada barra).
39. Como Gustavo, quero saber como conferir o que a empresa impõe sem ser admin (`/env`, `/instructions`, `/mcp`,
    `/model`, `/settings` no CLI; "Developer: Policy Diagnostics" no VS Code), para ver se uma política nova barrou o
    hub.
40. Como Gustavo, quero o Copilot no Maestri como preset `custom` com o comando `copilot`, porque o Maestri não tem
    preset de Copilot.
41. Como Gustavo, quero que o kit fique só no Windows (WSL fora), para não ter duas configurações por harness.
42. Como Gustavo, quero o teste dos três harnesses com o MCP pronto, capturando a requisição do Codex, para saber o
    que o Codex de fato recebe.

### Implementation decisions

- **Onde o hub mora** (04): `C:\context-hub`, NTFS, nas duas máquinas; o caminho no perfil de cada máquina; WSL fora;
  harnesses do critério 1: Claude Code, Codex, Copilot (VS Code e CLI); OpenCode fora.
- **Kit de par, contrato de instalação** (plano, fronteira combinada): idempotente; lê o HOME de uma variável de ensaio,
  nunca o HOME real, enquanto não houver aval; aceita simulação; cópia antes de tocar (15, para o GSD; o plano estende a
  todo global, com hash e desfazer). Cada faixa entrega o próprio instalador; o kit os enfileira.
- **Conferências do kit** (36, 42, 16): nenhum `CLAUDE.md` no hub nem acima; modo de desenvolvedor do Windows ligado.
  O plano soma Node e Python (o MCP do es617 é Node ≥ 22, ticket 16).
- **Contrato** (14, 36, 42): Claude Code por import absoluto no `~/.claude/CLAUDE.md`; Codex por link simbólico em
  `~/.codex/AGENTS.md`; Copilot (CLI e VS Code) por link simbólico em `~/.copilot/copilot-instructions.md`. Nunca link
  físico. O contrato não carrega em dobro (testado: forte no Copilot, médio no Claude Code). Restrições conhecidas
  (13): Codex soma até 32 KiB; o Claude Code recomenda menos de 200 linhas no `CLAUDE.md`.
- **Skills** (14, 13, 42, 40, 15): cada skill em `agents/skills/<skill>/`. A junction global (`~/.claude/skills` e
  `~/.agents/skills`) leva só as skills de uso geral (a busca, o FreeLLMAPI, o fluxo do Matt Pocock, a família
  `maestro-*` e as poucas que servem a qualquer trabalho); as de um papel ficam no acervo e entram só na pasta daquele
  papel, pela receita de setup (15, rodada 2). O GSD sai do escopo global com cópia (15). Como a junction liga só
  algumas pastas de `agents/skills/`: aberto na faixa 9.
- **Papel do Maestri e subpasta** (14 rodada 4, 40): `claude-md-and-agents-md` ligado em cada par; o kit **não** cria
  marcador de raiz nem `project_root_markers`; o `.git` da raiz do hub (o da cópia de segurança diária, ticket 33) leva
  Codex e Copilot ao `AGENTS.md` da raiz (testado em subpasta e em pasta de papel).
- **MCP no par** (14, rodada 1): MCP do banco em 127.0.0.1 com token de variável de ambiente; busca
  (obsidian-hybrid-search) só em 127.0.0.1; os dois ligados nos três harnesses. No Codex,
  `default_tools_approval_mode="approve"` para as ferramentas do hub. No Copilot CLI, a configuração de usuário é
  `~/.copilot/mcp-config.json` (18). No plano, a URL e o token chegam ao kit por um `.env` modelo.
- **Codex** (14, rodada 7): `danger-full-access` nas duas máquinas; proteção nos hooks e no contrato; teste mínimo do
  sandbox elevado a cada atualização do Codex, com aviso quando passar; voltar ao sandbox é decisão do Gustavo.
- **Hooks** (14, rodada 3): escopo do usuário nos três; o script sai na hora fora do hub. Codex: cada hook aprovado pelo
  hash em `hooks.state`. Copilot: só hook de usuário. O kit junta por evento os fragmentos das faixas 2, 6, 7 e 9,
  acrescentando sem apagar (proposta do plano).
- **Fim da resposta e telas** (14): Claude Code pelo mod (`turn.start` com `classic.Stop`); Copilot pelo hook
  `agentStop` junto com a extensão `onAgentStop` (`--experimental`); Codex pelo hook `Stop`; recusa antes da ferramenta
  no Codex pelo `PreToolUse`; estado da vigia: mod no Claude Code, `statusLine` no Copilot, `notify` no Codex. O
  conteúdo vem das faixas 2, 6 e 7; esta faixa instala.
- **Claude Desktop** (11, 36, 38): ponte `mcp-remote` (MCP stdio) para o MCP do banco com escrita e para a busca;
  pasta conectada no Cowork com "Folder instructions" que apontam o `AGENTS.md` da raiz. O Desktop não recebe o
  `instructions` do MCP (38). O "só de leitura" do comentário de 2026-10-12 do 16 caiu com o 11. Quem gera e instala
  a ponte: o núcleo diz faixa 10, as partes 5 e 10 dizem o mesmo; **[formato]**.
- **Conta da empresa** (14, rodadas 5 e 6; 46; conferido de novo pelo Gustavo em 2026-10-16, ticket 16): sem plugin
  do hub por ora; nenhuma política aplicada barra hooks ou MCP no CLI nem no VS Code nesta máquina (fato desta
  máquina, não garantia para outra nem para política futura); o risco conhecido é a lista de MCP permitidos e a política
  `ChatStrictPluginOnlyCustomization` (saída: entregar o hub como plugin).
- **Maestri** (18): Copilot como preset `custom` com o comando `copilot`.

### Testing decisions

- **Costura:** hub de ensaio (com um `AGENTS.md` de ensaio que traz uma resposta que só ele sabe, uma skill de marca e
  um `.git` na raiz) e HOME de ensaio; os MCP de ensaio pela URL e token do `.env` modelo.
- **Kit idempotente com simulação:**
  - a simulação não muda nenhum arquivo (hash do HOME de ensaio antes = depois) e lista o que faria;
  - a primeira passada liga tudo; a segunda não muda nada;
  - o desfazer volta o HOME de ensaio ao hash de antes, sem sobra;
  - com um `CLAUDE.md` posto acima do hub de ensaio, o kit para e diz onde está;
  - com um `~/.copilot/copilot-instructions.md` de ensaio já ocupado (texto de GSD de mentira), o kit tira o GSD, com
    cópia, e liga o contrato; nada se perde.
  - uma skill de papel do hub de ensaio não aparece na junction global.
- **Forma, por fora:** cada link simbólico aponta para o `AGENTS.md` do hub de ensaio; cada junction para a pasta da
  skill; cada configuração tem as linhas de MCP de busca e de banco, com o token por variável; os hooks juntados mantêm
  os que já estavam; no Codex, os hashes em `hooks.state` batem com os scripts.
- **Harnesses reais em modo não interativo** (`claude -p`, `codex exec`, `copilot -p`), com HOME de ensaio:
  - na raiz do hub de ensaio, numa iniciativa, numa pasta de papel de mentira e num repositório fora do hub, cada um
    responde a pergunta que só o contrato de ensaio sabe;
  - cada um usa a skill de marca;
  - cada um chama uma ferramenta do MCP de ensaio com o token da variável (no `codex exec`, com aprovação automática);
  - o contrato aparece uma vez só;
  - a requisição do Codex com o MCP pronto fica capturada.
- **Copilot do VS Code** e conta da empresa: lista de passos para o Gustavo, no portal, um passo por pergunta (como no
  teste 12 do ticket 14).
- **Aceite de ponta a ponta:** o kit roda idempotente num HOME de ensaio e os três harnesses enxergam contrato, skills e
  MCP.
- **Nada global real** (`~/.claude`, `~/.codex`, `~/.copilot`, `~/.agents`, hooks do usuário, modo de desenvolvedor,
  `trust_level` do Codex) sem o aval do Gustavo; a instalação de verdade é `ready-for-human`.

### Out of scope

- Conteúdo do contrato e esqueleto do hub (faixa 1); conteúdo dos hooks e do mod (faixas 2, 6, 7, 9); skills,
  roteamento e acervo (faixa 9); os servidores MCP (faixas 3 e 5).
- Kit de cliente: TBXark/mcp-proxy, rotas `/busca/mcp`, `/banco/mcp`, `/banco-escrita/mcp`, token de cliente,
  `--allow-all-mcp-server-instructions` e contrato na configuração global do cliente (faixa 10).
- Tailscale, grants, segundo par e Setup URI (outra execução, com o Gustavo).
- WSL e OpenCode (04).
- Plugin do hub para o Copilot (sem plugin por ora, 14).
- Servidor compartilhado do Codex com `codex --remote` (reserva, 14).
- Medir se o agente obedece ao contrato ("chegar não é obedecer", 36, 42): é da verificação dos cinco critérios
  (ticket 17).
- Pendências do ticket 45 com o Gustavo: apagar `C:\teste45` e a entrada `trust_level` que o teste deixou no
  `~/.codex/config.toml`.

### Pontos abertos para a construção

- **Não verificado** (14): hooks do Codex com acesso total; `${env:...}` no `mcp.json` do VS Code; o mod de fim num
  Claude Code gerenciado pela empresa; o sandbox elevado na outra máquina.
- **MCP do Copilot no VS Code no escopo do usuário:** o teste usou o `mcp.json` do workspace (fora da pasta o MCP não
  aparece), e a sessão "Copilot CLI" dentro do VS Code não conectou o MCP do workspace; falta decidir onde o kit põe o
  MCP para o VS Code valer em toda pasta (18 diz que o Agent Host lê o formato portátil; não verificado).
- **`COPILOT_HOME` no ensaio:** com ele definido, o Copilot CLI deixa de ler `~/.agents/skills` (18); o ensaio por
  `COPILOT_HOME` prova contrato, MCP e hooks do Copilot, não as skills. Saída **[aceita]** a verificar:
  `COPILOT_SKILLS_DIRS` apontando para a junction de ensaio (18); o que esse ensaio prova fica registrado, e ele não
  dispensa o passo real no HOME de verdade (`ready-for-human`).
- **Login dos harnesses no HOME de ensaio:** pergunta aberta do 16, rodada 2 **[formato]**.
- **Testes pedidos no ticket 16:** junction com mod (a doc fala de symlink); regras de caminho pegando a gravação pelo
  caminho da junction e pelo real.
- **`copilot skill add <pasta>`** não testado (42).
- **Modo de desenvolvedor desligado:** o kit não pode ligá-lo sem aval; falta decidir se só para e explica.
- **`trust_level` do Codex:** se o kit marca o hub como confiável não foi decidido (45 mostrou que a tela de confiança
  grava no `config.toml`).
- **Precedência registrada (sem contradição aberta):** GSD: vale o 15 (sai, com cópia); ponte do Desktop: vale o 11
  (com escrita), o dono é **[formato]**; marcador de raiz: vale o 14 (o `.git` real basta; testado em subpasta e em
  pasta de papel); a linha do 36 no `map.md` e o Answer do 40 seguem desatualizados nesses pontos.
