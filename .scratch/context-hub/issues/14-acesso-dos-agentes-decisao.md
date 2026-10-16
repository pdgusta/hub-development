# Acesso dos agentes: decisão

Type: grilling
Status: resolved
Blocked by: 04, 13, 18, 25, 33, 34, 36, 40, 42, 46

## Question

Como cada agente, nas duas máquinas, carrega o contrato e o MCP do hub (critérios 1 e 3)?

## Comments

- 2026-10-02 (vinda de "Divergência e edição concorrente"): toda sessão de agente, em todo harness,
  começa com uma checagem do estado do sync da máquina (última sync ok, colisão) e mostra o aviso se
  houver divergência. É o único canal que pega o sincronizador parado. Decidir aqui como cada harness
  faz isso (hook de início de sessão ou campo do MCP). Não verificado: hook de início de sessão no
  Codex e no Copilot.
- 2026-10-04 (vinda de "Contrato file-first: zonas e checkpoint"): decidir aqui, por harness: onde
  entra a regra do contrato de retomada (contrato global); o hook ao fim da resposta que obriga a
  manter a nota de retomada e a levar ao hub o que só a memória privada sabe (no Claude Code, `Stop`);
  e a checagem de início de sessão estendida para abrir a nota do trabalho que a pasta identifica.
  Não verificado: equivalentes ao `Stop` no Codex e no Copilot.
- 2026-10-06: passa a esperar "Como a verdade viaja entre as máquinas". O MCP que cada harness carrega
  (o do Fast Note Sync ou o do LiveSync, com transporte e autenticação diferentes) e a origem do estado
  de sync que a checagem de início de sessão lê (o servidor do banco, não mais o git) dependem do
  caminho escolhido. Sem isso, o ticket decidiria em cima de um MCP que talvez não exista no hub.
- 2026-10-06 (conferência da fronteira): passa a esperar "Onde o servidor mora" (o endereço e o
  transporte do MCP do es617 que cada harness carrega) e "Revisão do sync e da divergência com o banco"
  (de onde a checagem de início de sessão lê o estado do sync).
- 2026-10-10 (vinda de "Onde o servidor mora"): S3. Os agentes de um par usam o MCP local
  (`localhost`, com escrita). Os de um cliente usam pela tailnet o MCP de um par, por HTTP com token;
  o padrão é o MCP só de leitura (`READ_ONLY=true`). Decidir aqui como cada harness carrega um e outro.
- 2026-10-10: passa a esperar "Portas de entrada do hub", que diz por onde cada harness chega ao
  hub (raiz, subpasta, papel do Maestri, conector).
- 2026-10-12 (vinda de "Portas de entrada do hub"): passa a esperar também "Maestri: padrão e
  liberdade" (se `claude-md-and-agents-md` é ligado em cada par, e como o papel do Maestri recebe o
  contrato).
- 2026-10-12 (vinda de "Portas de entrada do hub"): passa a esperar também "Testes da porta do
  repositório fora do hub" (contrato e skills do hub no Codex e no Copilot, fora do hub).
- 2026-10-12 (vinda de "Copilot com assinatura Enterprise: pesquisa"): fatos no Answer daquele ticket.
  Pontos para esta decisão: a lista de MCP permitidos da empresa pode barrar o MCP do hub; a política
  `ChatStrictPluginOnlyCustomization` do VS Code bloquearia instruções, skills, hooks e MCP avulsos
  (saída: entregar o hub como plugin); hooks só da empresa; precisa de teste com a conta da empresa
  (`/env` e `/mcp` no CLI, "Developer: Policy Diagnostics" no VS Code).
- 2026-10-12 (vinda de "Maestri: padrão e liberdade", resolvido): `claude-md-and-agents-md` ligado em
  cada par; os três harnesses recebem o contrato dentro de um papel (Claude Code pela opção, Codex pelo
  marcador de raiz, Copilot pelo arquivo global); o Copilot abre na pasta da iniciativa como os outros;
  acervo do maestro como família `maestro-*` ligada por junction.
- 2026-10-12 (vinda de "Revisão do sync e da divergência com o banco", R60): o hub terá um `.git` na
  raiz em cada máquina (cópia de segurança diária no GitHub, um ramo por máquina; não replica). Com ele,
  Codex e Copilot numa subpasta podem achar a raiz e o `AGENTS.md` sem marcador ("Portas de entrada:
  pesquisa" apontou a falta de `.git` como a causa); **não testado** com o hub. Também da R64: um mod do
  Claude Code mostra o estado da vigia de sync o tempo todo na sessão.
- 2026-10-13 (vinda de "Revisão do sync e da divergência com o banco", resolvida):
  confirmados o `.git` na raiz de cada máquina (só cópia de
  segurança) e o mod do Claude Code com o estado da vigia; os dois entram aqui como insumo.
- 2026-10-14 (vinda da peneira da pesquisa ampla, `estrategia-pos-pesquisa.md`, aceita pelo Gustavo): um proxy de
  MCP (TBXark/mcp-proxy, binário Go para Windows; ou 1MCP, CI no Windows) junta o MCP do banco (só leitura para
  clientes) e o MCP de busca num endereço HTTP só, com token, exposto na tailnet. Vira a porta dos clientes se a
  "Camada de busca" escolher a ferramenta pronta no disco com repasse. Não verificado: o proxy repassar
  ferramentas stdio no Windows e a latência pela tailnet.
- 2026-10-14 ~22h55: ticket reservado pelo `/wayfinder`. Levantamento do que já está decidido, por harness, em
  `exploracao/anexos/levantamento-14-acesso-dos-agentes.md` (subagente de leitura, sem fonte nova). Partes que
  dependem de tickets abertos: o MCP de busca e o proxy dos clientes (Camada de busca); a gravação da nota de
  retomada pelo cliente só de leitura e o contrato no Claude Desktop (Como os agentes gravam no hub).
  **Rodada 1 aberta no portal** (`portal/rodadas/2026-10-14-acesso-dos-agentes-decisao-r1.md`). As recomendações são:
  - bancada de acesso por um subagente Opus 5.5 médio (150 a 250 mil tokens), com o que só dá por clique numa lista
    para o Gustavo;
  - MCP do par preso a 127.0.0.1 e com token;
  - checagem de início: no par lê o arquivo da vigia, no cliente uma ferramenta do MCP;
  - fim da resposta: o mesmo script, sem modelo, nos três harnesses;
  - o estado da vigia o tempo todo fica só no Claude Code.
- 2026-10-14 22:47, resposta à rodada 1 (portal, envio `a6d4d0cf-726a-4bf2-ab76-81d29f2b1252`):
  - **MCP do banco no par = A:** preso a 127.0.0.1 e com token, lido de uma variável de ambiente da máquina.
  - **Estado da vigia fora do Claude Code = B** (a recomendada era A): procurar um jeito de mostrar o estado o tempo
    todo também no Codex e no Copilot (pesquisa a mais).
  - **Teste de acesso:** em branco. O Gustavo pediu "especifique melhor essa opção A".
  - **Checagem de início e fim da resposta:** em branco, aguardando a pergunta do teste mais bem especificada.
- 2026-10-14 ~23h05: rodada 2 aberta no portal (`portal/rodadas/2026-10-14-acesso-dos-agentes-decisao-r2.md`). Ela detalha o teste de acesso: 12 testes numa tabela editável, cada um com o que prova, a decisão que alimenta e quem roda. Repete as perguntas da checagem de início e do fim da resposta, agora condicionadas ao teste.
- 2026-10-14 23:36, resposta à rodada 2 (portal, envio `f67ac890-3cef-4f86-b4b6-f2a68d379c0d`; o aviso não chegou
  ao maestro, e a resposta foi achada na caixa quando o Gustavo perguntou):
  - **Os testes:** sem mudanças; o maestro os toma como aceitos, os 12.
  - **Quem roda = A:** um subagente Opus 5.5 médio, agora, com 150 a 250 mil tokens.
  - **Checagem de início = A, com acréscimo:** no par, o hook lê o arquivo da vigia; no cliente, a ferramenta do MCP.
    O Gustavo quer que **a ferramenta do MCP sirva também ao par, como reserva** quando o arquivo da vigia faltar.
    Onde o teste falhar, a checagem vira regra no contrato daquele harness.
  - **Fim da resposta = outra resposta:** "hook claude mod e o correlato de claude mod pros outros harness". No
    Claude Code o fim da resposta é um **mod** (a API de mods do Claude Code, ver "Guarda do acervo: mods e hooks").
    No Codex e no Copilot, o equivalente mais próximo de um mod. O teste ganha esse ponto: o mod de fim no Claude
    Code e a pesquisa e o teste do correlato nos outros dois.
- 2026-10-14 23h45: bancada de acesso lançada (subagente Opus 5.5 médio, em segundo plano); entrega em `C:\Projetos\bancada-acesso\relatorio.md` e cópia em `bancada-acesso-relatorio.md`. O teste do Maestri fica para o maestro rodar; o do VS Code e o da empresa viram lista para o Gustavo.
- 2026-10-15 (~0h40): **bancada de acesso entregue** (subagente Opus 5.5 médio, ~258 mil tokens, 50 min; relatório
  em `bancada-acesso-relatorio.md`, original em `C:\Projetos\bancada-acesso\relatorio.md`). Placar:
  - **Início:** passou no Codex, no Copilot CLI e no Claude Code.
    - Codex: o hook fica aprovado sem `/hooks`, pelo hash posto em `hooks.state`.
    - Copilot: só pelo hook de usuário; o de repositório exige pasta confiável.
  - **Fim da resposta:**
    - Claude Code: um mod (`turn.start` + `classic.Stop`) devolve e solta. Onde a empresa gerencia o Claude Code, o
      `classic.Stop` de plugin pessoal pode não rodar (não verificado).
    - Copilot: o correlato do mod é a extensão do copilot-sdk (`onAgentStop`), que passou mas exige `--experimental`;
      o hook `agentStop` também passou.
    - Codex: não há correlato de código, o plugin só empacota hooks. O `Stop` devolve; o "solta" não foi visto
      porque o `codex exec` não grava arquivo nesta máquina (erro do sandbox do Windows).
  - **Checagem com reserva pelo MCP:** passou nos três e nos três casos (com arquivo, sem arquivo, sem os dois).
  - **`.git` real no lugar do marcador:** passou no Codex e no Copilot, em subpasta e em pasta de papel.
  - **Contrato em dobro:** não duplicou. A prova é forte no Copilot e média no Claude Code.
  - **MCP com token de variável de ambiente:** passou nos três; no `codex exec`, só com aprovação automática.
  - **`--allow-all-mcp-server-instructions` no Copilot:** passou.
  - **Estado da vigia o tempo todo:** o Copilot tem `statusLine` por script (o que aparece na tela não foi
    conferido); o Codex não tem nada alimentado por script.
  - **Teste do Maestri:** pendente com o maestro. `MAESTRI_TERMINAL_ID` chegou, mas com o id do maestro.
  - **VS Code e conta da empresa:** viraram uma lista de 10 passos para o Gustavo.
  - Arquivos globais restaurados e conferidos com diff ou hash.
- 2026-10-15 00:33–00:37: **teste 11 (hooks num terminal do Maestri), rodado pelo maestro** com três recrutas de
  teste na pasta de um papel de mentira (Claude Code, Codex e Copilot CLI). Os recrutas foram dispensados, o MCP de
  teste parado e os globais restaurados (`config.toml igual a copia: True`, hook do Copilot removido).
  - O hook de início rodou nos três, leu o estado do arquivo e entregou a frase-sonda.
  - `MAESTRI_TERMINAL_ID` chegou com o id **do próprio recruta** nos três, diferente do id do maestro (registro em
    `C:\Projetos\bancada-acesso\logs\inicio.log`).
  - O Codex e o Copilot leram a raiz e o papel. O Claude Code leu o papel, mas não o `AGENTS.md` da raiz, como já se
    sabia: a raiz entra pela opção `claude-md-and-agents-md`, decidida em "Maestri: padrão e liberdade" e desligada
    nesta máquina.
  - O Codex abriu sozinho a tela `/hooks` na partida, porque outros hooks do usuário (não os da bancada) pediam
    revisão.
  - O comando de shell do Codex falhou de novo (`helper_unknown_error`), o mesmo erro de sandbox do Windows da
    bancada.
- 2026-10-15 ~0h45: rodada 3 aberta no portal (`portal/rodadas/2026-10-15-acesso-dos-agentes-decisao-r3.md`): o fim no Copilot e no Codex, onde moram os hooks, o marcador de raiz, o estado da vigia na tela e a lista do Gustavo (VS Code e conta da empresa).
- 2026-10-15 07:44, **rodada 3 respondida** (envio `c37fcd98-7761-4257-8dc4-fffc5e74577e`):
  - **Fim da resposta no Copilot: C.** O hook de fim comum e a extensão experimental (`onAgentStop`, com
    `--experimental`), ligados juntos.
  - **Fim da resposta no Codex: B.** Investigar agora o erro de sandbox do Codex nesta máquina, e "pesquisar melhor
    também": um agente **Codex GPT 6.1 Sol médio, com acesso total** (pedido dele), pesquisa e testa. Só então se decide.
  - **Onde moram os hooks: A.** Escopo do usuário nos três harnesses; o script sai na hora quando a pasta não é do hub.
  - **Marcador de raiz:** em branco, "não entendi essa pergunta, refaça". Vai numa rodada nova, explicada.
  - **Estado da vigia na tela:** em branco, com a decisão no comentário: Claude Code pelo mod, Copilot pela barra de
    estado (`statusLine`), Codex na checagem de início e na notificação do Windows como reserva. A pesquisa do Codex
    (item acima) também procura um jeito de mostrar o estado o tempo todo no Codex.
  - **Lista do VS Code e da conta da empresa: A**, mas "quero esse passo a passo como uma rodada de perguntas": vira
    rodada própria, um passo por pergunta, com o resultado de cada um respondido no portal.
- 2026-10-15 ~08h: rodadas 4 (o marcador de raiz, explicado) e 5 (o teste 12 do Gustavo, um passo por pergunta)
  abertas no portal. Brief do recruta Codex pronto em `bancada-acesso-codex-brief.md` (erro de sandbox, o "solta" do
  `Stop`, correlato de mod, estado da vigia no Codex; entrega em `bancada-acesso-codex.md`). O `maestri recruit` com
  `-s danger-full-access -a never` foi **barrado pelo classificador do modo automático** do Claude Code ("Create Unsafe
  Agents"); espera o Gustavo criar o recruta ou liberar.
- 2026-10-15 08:30, **rodada 5 respondida** (teste 12, feito pelo Gustavo; envio `69ac20c7-9a87-46f8-abb7-ee542e9014bb`;
  a resposta traz o Policy Diagnostics inteiro, com dados da conta, e fica só na caixa). Leitura do maestro, conferida
  com `C:\Projetos\bancada-acesso\logs\`:
  - **Política no VS Code:** nenhuma configuração gerenciada; o filtro de política da conta está inativo; das políticas
    só `CopilotSessionSync` está aplicada. Nenhuma das cinco que importam (`ChatHooks`, `ChatMCP`,
    `ChatAllowedMcpServers`, `ChatAllowManagedMcpServersOnly`, `ChatStrictPluginOnlyCustomization`) está aplicada, e
    a conta (Copilot Enterprise) tem MCP habilitado. A consulta de política do runtime do Copilot CLI estourou 3,5 s:
    não verificado por esse caminho.
  - **Hook de usuário no VS Code: passou** (frase completa e linha nova no `inicio.log`). Num chat fora da bancada, o
    script não entregou a frase, como o desenho quer (sai na hora fora do hub).
  - **MCP com token no VS Code: passou.** O VS Code iniciou o servidor com `token_ok=True` e o chat do agente chamou
    `estado_sync` (08:18:53). Não ficou registrado se foi com `${env:BANCADA_MCP_TOKEN}` ou com o token escrito
    (não verificado). Fora da pasta o MCP não aparece, porque o `mcp.json` é do workspace.
  - **Sessão "Copilot CLI" dentro do VS Code:** o hook passou; o MCP do workspace não conectou (só `github-mcp-server`
    e `ide`).
  - **Copilot CLI com a conta da empresa: inconclusivo.** O servidor `bancada` não entrou na sessão. Causa provável,
    erro da instrução do maestro: no PowerShell, `@C:/...` sem aspas é lido como "splatting", e a opção
    `--additional-mcp-config` não chega ao Copilot com o caminho. A mesma conta da empresa no VS Code usou o MCP sem
    bloqueio. O MCP de teste já está parado.
- 2026-10-15 08:33, **rodada 4 respondida** (envio `6f1a336e-dcd8-4c27-9ab9-b342c8e7b44e`): **marcador = A**, o kit não
  cria mais o marcador de raiz; o `.git` da raiz faz o papel dele.
- 2026-10-15 08:48, **rodada 6 respondida** (envio `95823aea-36c2-4efb-88df-acf91c7c41d5`): o Gustavo repetiu o passo com
  aspas. **Copilot CLI com a conta da empresa: passou.** O `bancada` conectou, e o `mcp.log` mostra `tools/call
  estado_sync` com `token_ok=True` (08:47:33). A empresa não barra o MCP do hub no CLI nem no VS Code. MCP de teste
  parado. Do teste 12 só fica não verificado se o `mcp.json` do VS Code aceitou `${env:...}`. Resta no ticket a
  pesquisa do Codex (recruta barrado pelo modo automático, esperando o Gustavo).
- Comando para o Gustavo criar o recruta da pesquisa do Codex (o classificador do modo automático barrou o maestro):
  `! MSYS_NO_PATHCONV=1 maestri recruit "Sonda Codex" --preset "Codex" --command 'codex -m gpt-6.1-sol -c model_reasoning_effort="medium" -s danger-full-access -a never' --dir "C:\Projetos\bancada-acesso"`;
  depois, o maestro manda o brief `bancada-acesso-codex-brief.md` por `maestri ask`.
- 2026-10-15 ~15h50: o Gustavo criou o recruta "Sonda Codex"; o maestro conferiu e confiou os três hooks da bancada
  (`inicio.py` e `fim.py`, locais, só `127.0.0.1`), pulou a atualização do Codex e mandou o brief. **Pesquisa do Codex
  entregue** (`bancada-acesso-codex.md`, CLI 0.161.0, fontes primárias citadas):
  1. **Sandbox no Windows:** causa local achada (erro 32 ao atualizar a ACL de `node_repl.exe` do runtime; mesma cadeia da
     issue #53679, aberta em 2026-10-13). Elevado falha; **não elevado passa** e permite `apply_patch`
     (`-c 'windows.sandbox="unelevated"'`), mas a gravação por shell falha (alias do PowerShell em `WindowsApps`); com
     `danger-full-access` o shell grava, sem isolamento. Reparo do elevado: não verificado.
  2. **Fim da resposta:** o hook `Stop` **solta** o agente quando a nota de retomada muda (passou).
  3. **Correlato de mod:** não há API de módulo dentro do processo; há hooks (`PreToolUse` **vetou** um `apply_patch`, testado),
     `notify` (roda no fim do turno, sem veto), app-server (pedidos de aprovação, não testado o veto) e o SDK.
  4. **Vigia visível o tempo todo:** nenhum item de status por comando (também na 0.162.1); caminho possível: nome da
     conversa pelo app-server em `tui.status_line`/`tui.terminal_title`, não testado de ponta a ponta. Pedido sugerido
     na issue existente #20244 (texto no relatório; nada publicado).
  Nenhum arquivo global alterado (hashes antes = depois). A rodada de resolução vem a seguir.
- 2026-10-15 ~16h: **rodada 7 aberta** (`portal/rodadas/2026-10-15-acesso-dos-agentes-decisao-r7.md`), rascunhada por um
  subagente Opus médio e revisada pelo maestro, para resolver o ticket: como o Codex roda (recomendado: acesso total, com
  a proteção nos hooks e no contrato e o teste do sandbox elevado a cada atualização), fim da resposta e vigia no Codex
  (recomendado: `Stop` e `PreToolUse`, vigia na checagem de início com `notify` de reserva, e comentar na issue #20244 na
  conta do Gustavo) e o endereço dos clientes (recomendado: TBXark/mcp-proxy em cada par, uma porta, uma rota e um token
  por servidor: `/busca/mcp`, `/banco/mcp`, e `/banco-escrita/mcp` se "Como os agentes gravam" ligar a gravação do
  cliente). Fato conferido pelo subagente na documentação do TBXark (USAGE e CONFIGURATION, branch padrão): rotas por
  servidor, `authTokens` por servidor; os endpoints de saúde não pedem token. **Não verificado:** os hooks do Codex com
  acesso total; se o TBXark repassa o `instructions` do MCP; a conta do `gh`. Fontes e rascunho do "Answer" em
  `bancada-acesso-rodada7-fontes.md`.
- 2026-10-15 16:10, **rodada 7 respondida** (envio `b77740b3-465e-44cb-90a7-af09c06e5af3`):
  - **Codex = A:** `danger-full-access` em todo Codex do hub, nas duas máquinas; proteção nos hooks (início, fim, recusa
    antes da ferramenta) e no contrato; o kit roda o teste mínimo do sandbox elevado a cada atualização do Codex e avisa
    quando passar; voltar ao sandbox é decisão do Gustavo;
  - **fim da resposta e vigia no Codex = C** (a recomendada era A): tudo da A (fim pelo `Stop`, recusa pelo `PreToolUse`,
    vigia na checagem de início com o `notify` como reserva, app-server e SDK guardados, e o maestro publica o comentário
    na issue #20244 na conta do Gustavo, conferindo a conta do `gh` antes e mostrando o link depois), **mais um teste do
    caminho pelo nome da conversa**: um programa ao lado do Codex renomeia a conversa com o estado da vigia, e a barra de
    estado e o título do terminal mostram o nome (~1 h do recruta Codex);
  - **endereço dos clientes = A:** TBXark/mcp-proxy em cada par, preso à tailnet, uma porta, rota e token por servidor
    (`/busca/mcp`, `/banco/mcp`); como o ticket 11 (rodada 1) já ligou a gravação do cliente, entra a terceira rota
    `/banco-escrita/mcp` com token próprio.
  **Feito:** brief do teste em `bancada-nome-conversa-brief.md`, para a Sonda Codex; entrega em `bancada-nome-conversa.md`.
  O comentário na #20244 sai depois do teste (o texto pode mudar com o resultado). O ticket resolve com o resultado.
- 2026-10-15 ~16h50, **teste do nome da conversa** (`bancada-nome-conversa.md`, Sonda Codex): uma instância separada do
  app-server muda o nome guardado, mas **não** a tela de um Codex local já aberto (nem depois de um turno; testado com
  `--no-daemon`; o modo com daemon automático não foi testado). Com um app-server compartilhado (`--listen
  ws://127.0.0.1:...`) e o TUI ligado a ele (`codex --remote`), um programa ao lado renomeou três vezes e o rodapé e o OSC do
  título mudaram sem turno. Custo: servidor vivo, TUI sempre `--remote`, achar a conversa, reconexão; o nome da conversa
  vira o estado no histórico; estado velho se o programa parar. Globais intactos. O texto da #20244 mudou
  (`comentario-codex-20244.md`) e o `gh` não está instalado nesta máquina. **Rodada 8 aberta**
  (`portal/rodadas/2026-10-15-acesso-dos-agentes-decisao-r8.md`): adotar ou guardar o servidor compartilhado
  (recomendada: guardar como reserva) e como publicar o comentário (recomendada: o Gustavo cola o texto).
- 2026-10-15 17:49, **rodada 8 respondida** (envio `72be303d-de2e-4539-87f9-3eed4c2584ce`): **vigia no Codex = A** (fica a
  checagem de início e o `notify` com a notificação do Windows; o servidor compartilhado com `codex --remote` fica como
  reserva documentada pelo teste); **comentário na #20244 = C** (a recomendada era A): não publica; o pedido vai ao radar
  (`estrategia-pos-pesquisa.md`), e o maestro confere a #20244 a cada atualização do Codex. Ticket resolvido.

## Answer

**Cada agente carrega o contrato, as skills, os hooks e o MCP do hub assim** (rodadas 1 a 8; testes na bancada de
acesso, no Maestri e com a conta da empresa).

- **Contrato e skills:** o arquivo global de cada harness, por link simbólico; as skills por junction; no Maestri,
  `claude-md-and-agents-md` ligado em cada par ("Maestri: padrão e liberdade"). Codex e Copilot chegam ao `AGENTS.md`
  da raiz numa subpasta ou na pasta de um papel pelo `.git` da raiz; o kit não cria marcador de raiz (rodada 4). O
  contrato não carrega em dobro.
- **Hooks:** no escopo do usuário nos três harnesses, saindo na hora fora do hub (rodada 3). No Codex, o kit deixa cada
  hook aprovado pelo hash em `hooks.state`; no Copilot, só hook de usuário (o de projeto exige pasta confiável; no modo
  `-p`, `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS=true` carrega o de projeto, visto no teste do ticket 11).
- **Checagem de início:** no par, o hook lê o arquivo da vigia; sem ele, a ferramenta do MCP; no cliente, a ferramenta do
  MCP. Onde o hook falhar, vira regra no contrato daquele harness (rodada 2). Passou nos três, dentro e fora do Maestri,
  com o `MAESTRI_TERMINAL_ID` do próprio recruta.
- **Fim da resposta:** Claude Code pelo mod (`turn.start` com `classic.Stop`); Copilot pelo hook `agentStop` junto com a
  extensão `onAgentStop` (`--experimental`) (rodada 3); Codex pelo hook `Stop`, que devolve e solta, sem correlato de mod.
  A recusa antes da ferramenta no Codex é o `PreToolUse` (testado no `apply_patch`). App-server e SDK do Codex ficam como
  reserva.
- **Estado da vigia na tela:** Claude Code pelo mod; Copilot pela `statusLine`; Codex na checagem de início, com o
  `notify` no fim de cada turno disparando a notificação do Windows quando há divergência (rodadas 7 e 8). Testado
  (`bancada-nome-conversa.md`): um programa separado não muda a tela de um Codex local já aberto; com app-server
  compartilhado e o TUI `codex --remote`, renomear a conversa atualiza rodapé e título sem turno; fica como reserva.
  Pedido upstream (#20244) no radar, sem publicar.
- **Codex:** com `danger-full-access` nas duas máquinas (rodada 7), porque o sandbox elevado falha (erro 32 no
  `node_repl.exe`) e o não elevado deixa o agente sem shell. O kit roda o teste mínimo do elevado a cada atualização do
  Codex e avisa quando passar; voltar ao sandbox é decisão do Gustavo. As ferramentas do MCP do hub vão aprovadas de
  antemão (`default_tools_approval_mode="approve"`).
- **MCP no par:** o do banco preso a 127.0.0.1 com token de variável de ambiente (rodada 1); a busca
  (obsidian-hybrid-search) escuta só em 127.0.0.1; os agentes do par usam os dois direto.
- **MCP no cliente (rodada 7):** o TBXark/mcp-proxy em cada par, preso ao endereço da tailnet, uma porta, uma rota e um
  token por servidor: `/busca/mcp`, `/banco/mcp` (só leitura) e `/banco-escrita/mcp` (a gravação ligável decidida em
  "Como os agentes gravam no hub", com token próprio). Token de variável de ambiente no cliente, `Authorization: Bearer`
  nos três harnesses.
- **Conta da empresa:** no VS Code e no Copilot CLI, o MCP com token passou; nenhuma política que barre hooks ou MCP está
  aplicada; sem plugin do hub por ora (rodadas 5 e 6).
- **Não verificado, para a construção:** hooks do Codex com acesso total; o toast pelo `notify`; o TBXark repassar o
  `instructions` do MCP e a latência pela tailnet; `${env:...}` no `mcp.json` do VS Code; o mod de fim num Claude Code
  gerenciado pela empresa; o que a `statusLine` do Copilot mostra; o sandbox elevado na outra máquina; o servidor
  compartilhado do Codex por horas, com queda e no Maestri.
