## Faixa 5: MCP do banco com versão

O agente lê e grava a verdade do hub pelo MCP do banco, um fork nosso do MCP do es617 (obsidian-sync-mcp, TypeScript,
Node 22 ou mais novo) sobre o CouchDB do LiveSync. O fork devolve a versão lida, confere a versão na gravação, mostra o
conflito ao agente, valida o frontmatter e leva o contrato ao cliente pelo próprio protocolo. Prova de ponta a ponta:
regravar com versão velha pelo MCP vira conflito visível; com a versão certa, grava.

### User stories

1. Como agente (Claude Code, Codex ou Copilot), quero que a leitura de uma nota pelo MCP do banco me devolva, junto com o
   texto, a versão (revisão) que li, para poder gravar depois provando de qual versão parti.
2. Como agente, quero regravar uma nota existente inteira pela ferramenta de gravação do MCP informando a versão que li,
   para que a regravação inteira passe pelo único caminho que confere versão.
3. Como agente, quero que a gravação com a versão que ainda é a atual seja aceita e chegue ao `.md` no disco pela vista
   do LiveSync, para seguir o trabalho sem passo extra.
4. Como agente, quero que a gravação com uma versão que já não é a atual não apague a outra versão e me volte como
   conflito explícito, para eu reler e refazer em vez de desfazer o trabalho de alguém sem ver.
5. Como Gustavo, quero que nenhuma gravação de agente pelo MCP desfaça a de outro escritor (eu no Obsidian, outro agente,
   o sincronizador, a outra máquina) sem que alguém veja, para que nada divirja em silêncio (critérios 4 e 5).
6. Como Gustavo, quero que o conflito criado por uma gravação atrasada do agente apareça para mim no Obsidian (aviso do
   LiveSync) sem tocar na versão que já estava lá, para eu escolher a versão certa.
7. Como agente, quero que a leitura de uma nota com conflito aberto me avise do conflito, em vez de me devolver só a
   versão vencedora calada, para eu não gravar por cima de uma colisão que ainda não foi resolvida.
8. Como agente, quero um jeito de saber quais notas estão em conflito (aviso na leitura ou ferramenta própria), para
   tratar a colisão antes de continuar.
9. Como agente, quero que a troca de trecho pelo MCP com texto que já não existe na nota seja recusada, para que a
   edição parcial também não desfaça mudança alheia.
10. Como agente que cria ou regrava uma nota pelo MCP, quero que o MCP recuse a nota cujo frontmatter não cumpre o
    esquema do tipo que o caminho dá, com uma mensagem que diga o que falta, para corrigir na hora.
11. Como agente, quero que o MCP valide o frontmatter com os mesmos esquemas do hub (tipo pelo caminho, um esquema por
    tipo, campos comuns), para que a regra seja a mesma no disco e no banco.
12. Como agente, quero que o `AGENTS.md` e os `SKILL.md` gravados pelo MCP não sejam cobrados de frontmatter do hub, como
    no disco.
13. Como cliente que só alcança o hub pelo MCP de um par, quero receber no início da conexão a cabeça do `AGENTS.md`
    (até 2.000 caracteres, autossuficiente), para conhecer o contrato sem ter o arquivo.
14. Como Claude Code, quero que a cabeça do contrato caiba no corte de 2.048 caracteres do `instructions`, para que ela
    chegue inteira.
15. Como agente em qualquer dos três harnesses, quero que a descrição de cada ferramenta de gravação diga "antes de
    gravar, leia `AGENTS.md`", porque a descrição das ferramentas é o único canal que a fonte mostra chegando ao modelo
    nos três.
16. Como Copilot CLI, quero poder receber o `instructions` do servidor no prompt de sistema quando o kit de cliente ligar
    a opção que permite as instruções de todos os servidores, para ter o contrato sem pedir.
17. Como Copilot no VS Code, quero receber o `instructions` inteiro no modo agente quando uma ferramenta do servidor
    estiver ligada.
18. Como agente no par, quero falar com o MCP do banco em 127.0.0.1, com token lido de variável de ambiente, para que
    ninguém de fora da máquina grave no banco.
19. Como Gustavo, quero que o MCP do banco recuse quem chega sem o token, para que o banco não fique aberto a qualquer
    processo local.
20. Como cliente, quero por padrão uma instância do MCP do banco só de leitura, para consultar o hub sem risco de gravar.
21. Como Gustavo, quero poder ligar a gravação de um cliente dando a ele o token de uma segunda instância do MCP do
    banco, com escrita e a mesma guarda de versão, para que o cliente grave sem furar a garantia.
22. Como Gustavo, quero que a senha do CouchDB fique só nos pares e nunca chegue ao cliente, para que o cliente dependa
    do MCP e da guarda dele.
23. Como Claude Desktop, quero gravar pelo MCP do banco com escrita, pela ponte stdio, com a mesma guarda de versão, para
    regravar notas inteiras sem perder a edição de outro.
24. Como Codex, quero que as ferramentas do MCP do hub venham aprovadas de antemão, para gravar sem pedido de permissão
    a cada chamada.
25. Como agente, quero que a resposta de conflito diga em texto o que fazer (reler e refazer), para que até um modelo
    menor siga o caminho certo.
26. Como agente, quero que, com o MCP do banco fora do ar, a regravação inteira espere a porta voltar, eu avise na
    resposta e anote a pendência na nota de retomada, para que nada seja gravado sem guarda de versão.
27. Como Gustavo, quero que o fork seja exercido nos três harnesses reais com o MCP pronto, capturando a requisição do
    Codex, para saber o que de fato chega a cada modelo.
28. Como Gustavo, quero saber se o contrato que chegou foi seguido, porque chegar não é obedecer (no teste do VS Code o
    contrato chegou e a regra não foi seguida).

### Implementation decisions

- **Forma do banco (ticket 25):** a do LiveSync no CouchDB. Cada nota é um documento de metadados mais pedaços com o
  texto; histórico de revisões e folhas em conflito moram no banco e replicam com ele. A vista `.md` em cada máquina é
  do LiveSync (faixa 4).
- **Fork do MCP do es617 (tickets 25 e 30):** obrigatório antes de usar. Dois acréscimos:
  - **leitura com versão:** a ferramenta de leitura devolve a revisão lida;
  - **gravação com versão:** as ferramentas de gravação e de troca de trecho aceitam a revisão de base e gravam como
    filha dela; se a base mudou, a gravação vira conflito no banco em vez de apagar a outra versão. O lado do CouchDB e
    do plugin foi provado por emulação no spike: a gravação atrasada virou conflito e o plugin abriu o aviso ao
    Gustavo sem tocar na versão da outra "máquina" (ticket 30). O gancho de revisão de base da biblioteca comum do
    LiveSync vem da pesquisa de montagem e não foi conferido no código (ticket 30).
- **Conflito visível ao agente (tickets 25 e 30):** hoje a leitura devolve só a versão vencedora, sem aviso, e grava
  sobre ela. O fork passa a mostrar o conflito: aviso na leitura ou uma ferramenta que lista os conflitos (a escolha
  entre as duas é da construção; ver pontos abertos).
- **Comportamento que já existe e fica (ticket 30):** a troca de trecho por substituição já recusa texto velho; anexar
  ao fim e ao início agem sobre a versão atual.
- **Papel do MCP na gravação (ticket 11):** a regravação inteira de arquivo existente vai pela ferramenta de gravação
  do MCP do banco, com a versão lida. O hook de disco da faixa 6 manda para cá. Arquivo novo nasce no disco.
- **Garantia (tickets 08 e 11):** nenhuma gravação desfaz outra sem que o agente veja; se a nota mudou desde a leitura,
  o agente relê e refaz.
- **Validação de frontmatter (ticket 12, rodada 18):** o MCP do banco valida como o hook antes da gravação: o tipo vem
  do caminho (`agents/frontmatter/paths.yml`), nunca de quem grava; um esquema por tipo em `agents/frontmatter/`; campos
  comuns `title`, `type`, `initiative`, `created`, `updated`, `status` (rascunho, em uso, superada) e, opcionais,
  `aliases`, `tags`, `related`; nos tipos com ciclo, `stage`, com o `status` derivado por tabela no esquema. Sem
  frontmatter do hub: `AGENTS.md` e `SKILL.md`. Os esquemas e o catálogo dos 28 tipos são da faixa 1; esta faixa os
  consome. O ticket 12 marca a validação dentro do MCP como "versão modificada", não verificada.
- **Contrato pelo MCP (tickets 36 e 41):** três canais juntos:
  - o `instructions` do fork leva a cabeça do `AGENTS.md`, autossuficiente, de até 2.000 caracteres (pelo corte de
    2.048 do Claude Code);
  - a descrição de cada ferramenta de gravação diz "antes de gravar, leia `AGENTS.md`";
  - o kit de cliente liga a opção de instruções de todos os servidores no Copilot CLI e põe o contrato na configuração
    global do harness (faixa 10).
  O que a fonte diz de cada harness (ticket 41): Claude Code recebe o `instructions` cortado; Copilot do VS Code o põe
  inteiro no modo agente, com uma ferramenta do servidor ligada; Copilot CLI só o põe por padrão para servidores de uma
  lista, e os outros sob demanda (ou todos, com a opção, desde a 1.0.66); o Codex o envia na requisição como descrição do
  grupo de ferramentas, sem efeito confirmado. A descrição das ferramentas passa sem corte no Codex e inteira no VS Code.
- **Rede e acesso no par (ticket 14, rodada 1):** o MCP do banco preso a 127.0.0.1, com token de variável de ambiente;
  os agentes do par o usam direto. No Codex, as ferramentas do MCP do hub vão aprovadas de antemão (o kit, faixa 8).
- **Instâncias (tickets 11, 14 e 34):** por par, uma instância só de leitura (a padrão do cliente) e uma com escrita,
  com token próprio e a mesma guarda de versão, para o cliente com gravação ligada. As rotas no proxy da tailnet (busca,
  banco só leitura, banco com escrita) são da faixa 10. A senha do CouchDB fica só nos pares.
- **Claude Desktop (ticket 11, rodada 1):** grava também pelo MCP do banco com escrita, pela ponte `mcp-remote` (MCP
  stdio); o `instructions` não chega a ele.
- **Banco fora do ar (ticket 11, rodada 3):** a regravação inteira espera; o agente avisa na resposta e anota a
  pendência na nota de retomada. O MCP não oferece caminho de gravação sem guarda.
- **Banco de ensaio (plano, fronteiras combinadas, proposta a confirmar):** esta faixa sobe o seu CouchDB descartável em
  127.0.0.1, porta 5986, pelo compose que a faixa 4 publica; até lá, a imagem oficial com um `.env` de ensaio.

### Testing decisions

Só comportamento externo, visto de fora do MCP: o que a ferramenta responde, o que fica no banco e o que aparece na vista
`.md`. A costura é o hub de ensaio (a forma do ticket 12, com duas iniciativas e notas em pt-BR) mais o HOME de ensaio
mais o banco de ensaio da faixa (CouchDB na porta 5986), exercidos pelo MCP direto e pelos harnesses reais em modo não
interativo: `claude -p`, `codex exec` e `copilot -p`, todos com HOME de ensaio, nunca com `~/.claude`, `~/.codex` ou
`~/.copilot`.

- **Aceite de ponta a ponta (a prova da faixa):** ler uma nota pelo MCP e guardar a versão; mudar a nota por outro
  escritor (outra gravação pelo MCP ou edição na vista `.md` levada ao banco); regravar com a versão velha: a resposta é
  de conflito, a versão do outro escritor continua intacta no banco e na vista, e o banco guarda as duas folhas. Reler e
  regravar com a versão nova: grava e aparece na vista `.md`.
- Leitura de nota com conflito aberto: o agente recebe o aviso (ou a nota aparece na lista de conflitos).
- Troca de trecho com texto velho: recusada; anexar: age sobre a versão atual.
- Frontmatter: nota fora do esquema do tipo do caminho é recusada com mensagem do que falta; a nota certa grava;
  `AGENTS.md` e `SKILL.md` gravam sem frontmatter do hub.
- Acesso: sem token, recusado; o serviço não responde em outra interface que não 127.0.0.1; a instância só de leitura
  não grava.
- Contrato: a resposta de inicialização traz no `instructions` a cabeça do `AGENTS.md` do hub de ensaio, com até 2.000
  caracteres; a descrição de cada ferramenta de gravação traz a regra curta.
- Os três harnesses com o MCP pronto (tickets 36 e 41): pedir a cada um que cite o que recebeu do servidor; no Codex,
  capturar a requisição para ver onde o `instructions` vai; no Copilot CLI, com e sem a opção de instruções de todos os
  servidores. O Copilot do VS Code não roda em modo não interativo: fica como teste a pedir ao Gustavo.
- Regra seguida: num dos harnesses, pedir uma regravação inteira e conferir se o agente leu o `AGENTS.md` antes, para a
  verificação dos cinco critérios ter a primeira medida.
- Banco recriado ou reiniciado durante a sessão: registrar se o MCP volta a responder sozinho (no spike, ele perdia o
  feed e pedia restart; ver pontos abertos).

### Out of scope

- A tela de colisão com três vias e resultado editável, fork do aviso do LiveSync: logo depois da construção, não como
  condição para começar (ticket 25).
- O CouchDB, o LiveSync (plugin e CLI), a replicação entre pares e o limite de 200 MiB: faixa 4.
- O hook de disco que recusa a regravação inteira e manda para o MCP: faixa 6.
- O proxy da tailnet com rotas e tokens para clientes, o kit de cliente e a atualização da cabeça do contrato no MCP
  quando o `AGENTS.md` muda: faixa 10.
- A linha de MCP em cada harness, a ponte `mcp-remote` do Claude Desktop e a aprovação de antemão no Codex: faixa 8.
- A busca (obsidian-hybrid-search) e o índice dentro do MCP do banco, que é a reserva "Robusta": faixa 3 e radar.
- Os esquemas de frontmatter e o catálogo dos tipos: faixa 1.
- A segunda máquina, a tailnet e o Tailscale de verdade: outra execução.
- A edição concorrente entre o Obsidian e um agente no mesmo arquivo (fora do mapa).

### Pontos abertos para a construção

- **Recusa ou conflito gravado:** o ticket 11 diz que a gravação com base velha "é recusada, e o agente relê e refaz";
  os tickets 25 e 30 dizem que ela "vira conflito", gravada como folha filha da base velha e mostrada ao Gustavo. A
  construção tem de escolher uma forma que cumpra as duas leituras (por exemplo, resposta de conflito ao agente), e o
  maestro confirma com o Gustavo se a folha concorrente fica no banco.
- **Forma do conflito visível:** aviso na leitura, ferramenta que lista conflitos, ou as duas (ticket 30).
- **Versão de base nas outras ferramentas:** se anexar ao fim e ao início e a troca de trecho também levam a versão de
  base, ou só a regravação inteira. Não decidido.
- **Gancho de revisão de base da biblioteca do LiveSync:** não conferido no código; o efeito num CouchDB remoto também
  não (ticket 26).
- **Corte do `instructions` no Claude Code:** a decisão usa 2.048 caracteres (ticket 36), e os testes das portas viram
  o corte depois de uns 3.300 (ticket 41). Medir; a cabeça de 2.000 vale nos dois casos.
- **De onde vem a cabeça do contrato:** texto fixo na configuração do fork ou lido do `AGENTS.md` do hub. Quem a atualiza
  é lacuna de dono da faixa 10 (ticket 16).
- **Codex:** como a API mostra ao modelo a descrição do grupo de ferramentas, não verificado; capturar a requisição
  (ticket 41).
- **Copilot CLI:** o efeito da opção de instruções de todos os servidores, que lista é a de servidores permitidos, o
  limite de tamanho das descrições e o suporte a prompts e resources: não verificados (ticket 41).
- **Busca de ferramentas adiada:** com ela ligada, a definição das ferramentas pode ser adiada, e a regra curta nas
  descrições pode não chegar a tempo (ticket 41). Medir nos três.
- **Claude Desktop:** se a descrição das ferramentas do MCP chega a ele pela ponte; não verificado (ticket 11).
- **Validador de frontmatter em dois lugares:** o MCP é TypeScript e as peças com Windows confirmado da peneira
  (python-frontmatter, PyYAML) só entram com um processo Python ao lado (ticket 16). Decidir como hook e MCP usam os
  mesmos esquemas sem dois validadores que divirjam.
- **Nota nova pelo MCP:** arquivo novo nasce no disco (ticket 11); se o MCP aceita criar nota sem versão de base, e com
  que validação, não está decidido.
- **MCP depois de o banco ser recriado:** no spike ele perdia o feed e pedia restart (ticket 30); decidir se o fork
  reconecta sozinho ou se a vigia avisa.
- **Instância só de leitura:** como o fork fica só de leitura (ferramentas de gravação ausentes ou recusadas) não está
  decidido.
- **Cifra do banco:** se o banco for cifrado, a senha da cifra também vai ao MCP (ticket 30); a decisão sobre cifrar é
  da faixa 4.
- **Compactação do CouchDB:** apaga as revisões antigas; o rastro de uma gravação perdida some com ela (ticket 30). Com o
  conflito visível isso deixa de ser a única defesa, mas a política de compactação não foi decidida.
- **Proxy da tailnet repassar o `instructions`** e a latência pela tailnet: não verificados (ticket 14), faixa 10.
- **Login dos harnesses no HOME de ensaio:** pergunta do plano ao Gustavo, ainda aberta; sem ela, a prova nos três
  harnesses pode ficar só na forma dos arquivos.


## Faixa 6: Guardas de gravação no disco

No disco, o agente só troca trecho e cria arquivo novo. Um hook antes da ferramenta, no escopo do usuário dos três
harnesses, recusa a regravação inteira de arquivo existente e manda usar o MCP do banco; o mesmo ponto recusa a nota
fora do esquema de frontmatter; um verificador sem IA no fim de cada resposta completa o derivável e devolve o resto; um
segundo hook avisa, sem recusar, a leitura grande que não veio da busca. Prova de ponta a ponta: no Claude Code, Codex
e Copilot em HOME de ensaio, a regravação inteira de arquivo existente é recusada, a troca de trecho passa e a nota sem
frontmatter válido é recusada.

### User stories

1. Como Gustavo, quero que nenhum agente regrave inteiro, pelo disco, um arquivo do hub que já existe, para que a
   regravação sem conferir versão não apague a mudança de outro escritor.
2. Como agente no Claude Code, quero que o Write sobre um arquivo existente do hub seja recusado antes de rodar, com uma
   mensagem que mande usar a troca de trecho ou a gravação do MCP do banco com a versão lida, porque o Write regrava sem
   aviso um arquivo que nunca li.
3. Como agente no Codex, quero que o `apply_patch` que cria por cima de um arquivo existente (o `Add File` sobre
   existente) seja recusado, porque ele sobrescreve sem aviso.
4. Como agente no Codex, quero que o `apply_patch` que regrava o arquivo inteiro (apagar e recriar, ou trocar todas as
   linhas) seja recusado, para que a regravação inteira não entre disfarçada de patch.
5. Como agente no Copilot, quero que o `create` sobre arquivo existente seja recusado pelo hook do hub com a mensagem do
   hub, e não só pela recusa nativa da ferramenta, para receber o caminho certo (o MCP do banco).
6. Como agente nos três harnesses, quero que a troca de trecho (Edit do Claude Code, `edit` do Copilot, `Update File`
   parcial do Codex) passe pelo hook, porque ela é segura nos três: grava mantendo a mudança alheia em outra linha e
   recusa quando o próprio trecho mudou.
7. Como agente nos três harnesses, quero criar arquivo novo no disco sem recusa, porque arquivo novo nasce no disco.
8. Como agente, quero que os hooks do hub saiam na hora quando eu trabalho fora do hub, para que a guarda não atrapalhe
   outros repositórios.
9. Como agente dentro de um papel do Maestri, quero que a guarda valha também ali, por isso os hooks moram no escopo do
   usuário e não no projeto.
10. Como Gustavo, quero os hooks do hub no escopo do usuário nos três harnesses, para que uma sessão aberta em qualquer
    pasta do hub (raiz, subpasta, papel) esteja coberta.
11. Como Gustavo, quero que no Codex cada hook do hub fique aprovado pelo hash, para que ele rode sem pedido a cada
    sessão.
12. Como Gustavo, quero que no Copilot a guarda seja hook de usuário, porque o de projeto exige pasta confiável.
13. Como Gustavo, quero que a guarda do Codex funcione com o acesso total decidido para as duas máquinas, e não só no
    sandbox em que foi testada.
14. Como agente, quero que, com o MCP do banco fora do ar, a troca de trecho no disco continue e a regravação inteira
    espere a porta voltar, com aviso na resposta e a pendência na nota de retomada, para que nada seja gravado sem
    guarda de versão.
15. Como agente que cria uma nota no hub, quero que o hook antes da gravação recuse a nota cujo frontmatter não cumpre o
    esquema do tipo que o caminho dá, com mensagem do que falta, para corrigir antes de gravar.
16. Como agente, quero que o tipo da nota venha do caminho, nunca de mim, para que eu não possa escolher um tipo mais
    frouxo.
17. Como agente, quero que o `AGENTS.md` e os `SKILL.md` passem sem frontmatter do hub.
18. Como agente, quero que os campos que a máquina deriva (`type`, `initiative`, o `title` do núcleo, `updated`) sejam
    preenchidos pelo verificador, para não perder tempo com o que a máquina sabe.
19. Como agente, quero que o verificador sem IA rode no fim de cada resposta, preencha o derivável e me devolva o que só
    eu posso completar, para que a nota fique certa sem depender de eu lembrar a regra.
20. Como agente em tipo com ciclo (ficha, research, design, plan, deliverable, work, case, lab), quero preencher só o
    `stage`, e o verificador derivar o `status` pela tabela do esquema.
21. Como Gustavo, quero que a nota que eu crio no Obsidian, sem frontmatter, seja completada pelo verificador na próxima
    resposta de agente, porque não haverá Templater.
22. Como Gustavo, quero que nenhuma regra de frontmatter more só no `AGENTS.md`, porque regra em texto já se provou inútil
    para agentes menores.
23. Como agente, quero que o título do núcleo da iniciativa venha com o nome dela ("Retomada · VOEGOL cross-tenant"),
    completado pelo verificador a partir da ficha.
24. Como agente que abre um arquivo grande do hub sem ter buscado nada na sessão, quero receber o aviso "busque antes",
    sem recusa, para economizar contexto pela busca.
25. Como agente que veio da busca e lê inteiro um arquivo grande que ela apontou, quero receber o aviso "leia o trecho que
    a busca apontou".
26. Como agente que veio da busca e lê só um trecho, quero ficar sem aviso nenhum.
27. Como agente, quero receber o aviso de leitura no máximo uma vez por arquivo por sessão, para que ele não vire ruído.
28. Como hook de leitura, quero guardar por sessão o que a busca devolveu e o que foi aberto, para decidir qual aviso dar.
29. Como Gustavo, quero que o tamanho de "arquivo grande" seja medido na construção, e não chutado.
30. Como agente no Codex ou no Copilot, que leio por comando de shell, quero saber se o aviso de leitura me alcança, para
    o contrato cobrir o que o hook não cobre.
31. Como Gustavo, quero que regravação por comando de shell (redirecionamento, script) fique coberta pelo contrato, porque
    o hook não a vê.
32. Como maestro, quero que os hooks desta faixa convivam com os das faixas 2 e 9 nos mesmos eventos (início, fim, antes
    da ferramenta, entrada), cada um no seu script e fragmento de configuração, para que ninguém edite o arquivo de
    configuração do outro.
33. Como Gustavo, quero que a instalação dos hooks seja idempotente e rode primeiro num HOME de ensaio, porque nada global
    entra sem o meu aval.
34. Como Gustavo, quero que os hooks do hub convivam com os hooks que já tenho no usuário (no Copilot há hooks de outras
    origens), para que instalar a guarda não desligue o resto.
35. Como Claude Desktop, quero gravar pela pasta conectada do Cowork, sabendo que ali a guarda de versão do hub não vale
    até a construção mostrar o que a ferramenta do Cowork confere.
36. Como Gustavo, quero que a recusa explique o caminho certo em texto, porque só o texto da recusa, sozinho, apenas
    instrui; o mecanismo é o que recusa.

### Implementation decisions

- **Divisão dos caminhos de gravação (ticket 11, rodada 2):** no disco, só troca de trecho; a regravação inteira de
  arquivo existente vai pela gravação do MCP do banco com a versão lida (faixa 5); arquivo novo nasce no disco.
  Comando de shell fica coberto só pelo contrato.
- **Hook de recusa da regravação inteira (ticket 11):** antes da ferramenta, dentro do hub, recusa e manda usar o MCP:
  - Claude Code: Write sobre arquivo existente;
  - Codex: `apply_patch` que cria sobre existente ou regrava o arquivo inteiro;
  - Copilot: `create` sobre existente.
  Deixa passar: Edit, `edit`, `Update File` parcial e criação de arquivo novo. Formato da recusa provado na bancada:
  decisão `deny` com motivo no Claude Code e no Copilot (no Copilot o motivo é obrigatório e é mostrado ao agente);
  `deny` no `PreToolUse` do Codex, que lê o patch no campo de comando da entrada da ferramenta.
- **O que o teste mostrou e sustenta o desenho (ticket 11; bancadas de gravação):** a troca de trecho grava mantendo a
  mudança alheia em outra linha e recusa quando o próprio trecho mudou nos três; o Write do Claude Code recusa arquivo
  lido e depois mudado, mas regrava sem aviso arquivo existente nunca lido; o `create` do Copilot recusa qualquer
  existente; o `Add File` do Codex sobrescreve sem aviso. O classificador do Codex da bancada (criar sobre existente,
  apagar existente, `Update` que remove todas as linhas) é de bancada, com heurística por número de linhas, e não é
  política pronta.
- **Escopo e instalação (ticket 14, rodada 3; ticket 44):** hooks no escopo do usuário nos três harnesses, saindo na hora
  fora do hub; assim valem dentro de um papel do Maestri (posta só na raiz do workspace, a guarda não alcança o papel).
  No Codex, o kit deixa cada hook aprovado pelo hash no estado de hooks; no Copilot, só hook de usuário. No Claude Code,
  o hook de settings faz a recusa; o mod (plugin com funções que seguram ou recusam chamadas de ferramenta) também pode,
  e exige a versão 2.1.287 ou mais nova, com API "early access" (ticket 44).
- **Poderes de cada harness (ticket 44):** Claude Code recusa ou pede aval (`deny`/`ask`), com filtro por caminho
  "best-effort" no hook de settings; Codex só recusa, sem `ask` nem hook que chame modelo, e a própria doc o chama de
  "guardrail", não barreira completa; Copilot CLI recusa ou pergunta, sem hook que chame modelo; no VS Code os hooks
  estão em Preview. Esta faixa usa só a recusa, que existe nos três.
- **Codex com acesso total (ticket 14, rodada 7):** a configuração decidida é `danger-full-access` nas duas máquinas; a
  bancada provou o hook com `workspace-write` e sandbox não elevado.
- **Hook de aviso de leitura (ticket 11, rodadas 3 e 4):** avisa, sem recusar, uma vez por arquivo por sessão: veio da
  busca e lê um trecho, calado; veio da busca e lê inteiro um arquivo grande, "leia o trecho que a busca apontou"; não
  veio de nenhuma busca, "busque antes". Guarda por sessão o que a busca devolveu (no Claude Code, o hook depois da
  ferramenta recebe a resposta da ferramenta) e o que foi aberto. A busca é o MCP do obsidian-hybrid-search (faixa 3).
  O tamanho de "grande", a construção mede.
- **Frontmatter imposto por mecanismo (ticket 12, rodada 18, C):** três camadas, nenhuma só no `AGENTS.md`:
  - hook antes da gravação recusa a nota fora do esquema (Claude Code, Codex e Copilot);
  - o MCP do banco valida igual (faixa 5);
  - verificador sem IA no fim de cada resposta preenche o derivável (`type`, `initiative`, `title` do núcleo,
    `updated`) e devolve o resto ao agente. Sem Templater: a nota do Gustavo nasce sem frontmatter e o verificador da
    próxima resposta de agente a completa.
  O tipo vem do caminho (`agents/frontmatter/paths.yml`); um esquema por tipo em `agents/frontmatter/`; campos comuns
  `title`, `type`, `initiative`, `created`, `updated`, `status` (rascunho, em uso, superada), opcionais `aliases`,
  `tags`, `related`; nos tipos com ciclo, `stage` preenchido por quem escreve e `status` derivado pela tabela do
  esquema. Sem frontmatter do hub: `AGENTS.md` e `SKILL.md`. O `title` do núcleo leva o nome da iniciativa (ticket 12,
  rodada 16). Esquemas, catálogo e o verificador que aceita ou recusa uma nota são da faixa 1; esta faixa os liga aos
  eventos de antes da gravação e de fim de resposta.
- **Fim de resposta em cada harness (ticket 14, rodada 3):** Claude Code pelo mod (início de turno com o `Stop`
  clássico); Copilot pelo hook de parada do agente junto com a extensão de parada (`--experimental`); Codex pelo hook
  `Stop`, que devolve e solta. O verificador entra nesse mesmo ponto, que a faixa 2 também usa.
- **Banco fora do ar (ticket 11, rodada 3):** a troca de trecho segue no disco; a regravação inteira espera; aviso na
  resposta e pendência na nota de retomada.
- **Claude Desktop (ticket 11, rodada 1):** grava pela pasta conectada do Cowork, com "Folder instructions" apontando o
  `AGENTS.md` da raiz, e pelo MCP do banco; na pasta conectada, sem a guarda de versão do hub até a construção mostrar o
  que a ferramenta do Cowork confere.
- **Fronteiras com outras faixas (plano, propostas a confirmar pelos donos):** cada faixa grava o seu script de hook e um
  fragmento de configuração; a faixa 8 junta os fragmentos e enfileira os instaladores; o instalador desta faixa é
  idempotente, lê o HOME da variável de HOME de ensaio (nunca `~`) e aceita simulação.

### Testing decisions

Só comportamento externo: o que a ferramenta do harness responde e o que fica no disco. A costura é o hub de ensaio (a
forma do ticket 12) mais o HOME de ensaio de cada harness (hooks no escopo do usuário dele, nunca nos globais de
verdade) mais o banco de ensaio da faixa 5 para o caminho do MCP, exercidos pelos harnesses reais em modo não interativo:
`claude -p`, `codex exec` (com o acesso total decidido) e `copilot -p`. Para garantir a ordem leitura, mudança externa,
gravação, vale o método da bancada: um hook depois da leitura (Claude Code e Copilot) ou antes do `apply_patch` (Codex)
muda a nota uma vez, de forma síncrona, e registra o hash.

- **Aceite de ponta a ponta (a prova da faixa):** nos três harnesses, com os hooks no escopo do usuário do HOME de
  ensaio: a regravação inteira de arquivo existente é recusada com a mensagem do hub; a troca de trecho passa e preserva
  a mudança alheia em outra linha; arquivo novo é criado; nota nova sem frontmatter válido é recusada; a mesma nota com
  o frontmatter certo é aceita.
- Codex: criar sobre existente, apagar e recriar, e `Update` que troca todas as linhas são recusados; `Update` parcial
  passa.
- Fora do hub: a mesma regravação inteira numa pasta fora do hub de ensaio passa, e o hook sai sem efeito.
- Arquivo existente nunca lido no Claude Code: o Write é recusado pelo hook (o furo que a bancada achou).
- Verificador no fim da resposta: uma nota gravada sem os campos deriváveis sai da resposta com eles preenchidos; o que
  falta e só o agente sabe volta ao agente; num tipo com ciclo, o `status` sai derivado do `stage`.
- Nota do Gustavo: um arquivo posto no hub de ensaio sem frontmatter (como o Obsidian faria) é completado na resposta
  seguinte de um agente.
- `AGENTS.md` e `SKILL.md` gravam sem frontmatter do hub.
- Aviso de leitura no Claude Code: abrir inteiro um arquivo grande sem busca dá "busque antes"; buscar e abrir inteiro o
  arquivo apontado dá "leia o trecho"; buscar e abrir um trecho não dá aviso; abrir o mesmo arquivo de novo na sessão
  não repete o aviso; nenhuma das leituras é recusada. No Codex e no Copilot, medir se a leitura por shell é alcançável.
- Banco fora: com o MCP do banco desligado, a troca de trecho passa e a regravação inteira continua recusada no disco.
- Os globais de verdade (`~/.claude`, `~/.codex`, `~/.copilot`) conferidos por hash antes e depois de cada teste.

### Out of scope

- A guarda do acervo do maestro (recusa de gravação no acervo para Codex e Copilot, aval no Claude Code, verificador em
  outro modelo, registro de uso): faixa 9. Daqui do ticket 44 vale só o que os hooks e o mod conseguem recusar.
- O hook de fim de resposta da nota de retomada e a checagem de início: faixa 2.
- A instalação de verdade em `~/.claude`, `~/.codex` e `~/.copilot` e o kit de par que junta os fragmentos: faixa 8 e,
  nos globais, outra execução com o aval do Gustavo.
- O MCP do banco, a versão lida e o conflito visível: faixa 5.
- Os esquemas por tipo, o catálogo `agents/blocks.md`, o `index.md` como cartão da pasta (`summary: auto`, `local`) e a
  conferência dos links `par://`: faixa 1, salvo se o dono do verificador combinar outra divisão.
- Regravação por comando de shell: coberta só pelo contrato.
- O Templater no Obsidian: descartado (ticket 12, rodada 18).
- A busca como porta única de leitura: descartada; a busca é a porta de entrada, não a única (ticket 11, rodada 3).

### Pontos abertos para a construção

- **Hooks no escopo do usuário:** não verificados nos três; o teste usou o escopo de projeto (ticket 11).
- **Hooks do Codex com acesso total:** não verificados (ticket 14); a bancada usou `workspace-write` e sandbox não
  elevado.
- **Classificador do `apply_patch`:** a política real do Codex ainda não existe. Não testados: mover arquivo, vários
  caminhos num patch, links, arquivo vazio, apagar e criar em chamadas separadas. A recusa de apagar arquivo existente
  também recusaria apagamentos legítimos: decidir se apagar entra na guarda.
- **Filtro por caminho:** "best-effort" no hook de settings do Claude Code (ticket 44); conferir que a guarda pega a
  gravação pelo caminho real e por junction ou link simbólico (o ticket 16 pede esse teste para o acervo).
- **Copilot no VS Code:** se o hook de usuário em `~/.copilot` vale nele, com hooks em Preview e comportamento que muda
  conforme o harness; não verificado.
- **Frontmatter numa troca de trecho:** o hook antes da gravação vê só o trecho; validar o resultado pede montar o
  conteúdo final. Não decidido nem testado.
- **Hook antes da gravação e campos deriváveis:** o hook recusa a nota fora do esquema e o verificador preenche o
  derivável depois; decidir o que o hook cobra de uma nota nova a que ainda faltam `type`, `initiative` e `updated`.
- **Verificador grava sem guarda de versão:** ao completar no fim da resposta uma nota existente (inclusive a do Gustavo,
  que pode estar aberta no Obsidian), ele grava no disco fora das ferramentas do agente. Como isso cumpre "nenhuma
  gravação sem guarda de versão" não está decidido.
- **Fim de resposta no Claude Code:** o ticket 12 fala do `Stop`; o ticket 14 escolheu o mod com o `Stop` clássico.
  Combinar com a faixa 2 um ponto só.
- **Aviso de leitura no Codex e no Copilot:** eles leem por comando de shell; não verificado (ticket 11). Se o hook não
  alcançar, decidir se o aviso vira regra no contrato daquele harness.
- **Tamanho de "arquivo grande":** a construção mede (ticket 11).
- **Ferramenta do Cowork:** o que confere ao gravar na pasta conectada; não verificado (ticket 11).
- **Mod do Claude Code:** tempo próprio de 10 s por hook; API "early access"; o mod de fim num Claude Code gerenciado pela
  empresa não verificado (tickets 14 e 44).
- **Convivência com hooks existentes:** no Copilot já há hooks de usuário de outras origens (um deles injeta texto em todo
  resultado de ferramenta); a instalação não pode desligá-los. Origem do hook do GSD no Copilot: não verificada.
- **Login dos harnesses no HOME de ensaio:** pergunta do plano ao Gustavo, ainda aberta.
