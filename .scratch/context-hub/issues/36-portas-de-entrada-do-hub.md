# Portas de entrada do hub

Type: grilling
Status: resolved
Blocked by: 37, 38, 41

## Question

Por quais portas o Gustavo e os agentes chegam ao context hub (sessão de harness na raiz ou numa
subpasta, workspace e papel do Maestri, Obsidian, Claude com acesso só por conector, cliente pelo MCP
de um par, sessão num repositório de código fora do hub e outras que surgirem), e o que cada porta
exige da árvore: onde a sessão abre, o que carrega sozinha e como acha o resto? A lista fica aberta:
o Gustavo ainda vai explorar casos novos.

## Comments

- 2026-10-10: aberto a pedido do Gustavo na resposta à R19 de "Arquitetura de pastas e frontmatter
  do hub": antes de decidir o que fica dentro da pasta de uma iniciativa (R19), e talvez revendo os
  níveis (R18), ele quer pensar em todas as formas de chegar ao hub. Ele hoje abre o harness na raiz
  do vault para chegar ao `CLAUDE.md`/`AGENTS.md` e acha que fará o mesmo na raiz do hub, achando o
  resto pela busca; não sabe se vai precisar de sessão limitada a uma subpasta. Quer que a
  padronização de como usa o Maestri e de como o maestro orquestra more no hub, mesmo quando o
  trabalho roda fora dele.
- Fatos de partida, com fonte:
  - Claude Code lê os `AGENTS.md` da pasta onde abre e das de cima, só se nenhum `CLAUDE.md` conta;
    a opção `claude-md-and-agents-md` (em `pluginConfigs` de `~/.claude/settings.json`) lê os dois
    juntos (`code.claude.com/docs/en/memory.md`, "Choose which instruction files load").
  - O papel do Maestri abre o agente em `<workspace>/.maestri/roles/<id>/`, que tem `CLAUDE.md`,
    `AGENTS.md` e `role.json` (conferido no disco deste repositório). Pelo item acima, esse `CLAUDE.md`
    faz o Claude Code ignorar o `AGENTS.md` do hub, salvo com `claude-md-and-agents-md` (inferência
    pela doc, não testada).
- 2026-10-10, resposta à R20 (rodada 1): o Gustavo não quer nada por inferência; cada porta da
  lista passa por pesquisa. Virou "Portas de entrada: pesquisa", que agora bloqueia este ticket. Ele
  não respondeu ainda o que é o "Claude (com work)"; a pesquisa da porta 6 cobre app, claude.ai,
  Cowork e conectores.
- 2026-10-10 (vinda de "Portas de entrada: pesquisa"): fatos por porta no Answer daquele ticket.
  Rodada 2 aberta na nota "Rodada atual" (R21: o que fazer com os pontos que só um teste resolve).
- 2026-10-10, resposta à R21 (rodada 2): testes A, B, C e D aprovados, sem consulta ao TI. Virou
  "Testes das portas de entrada", que agora bloqueia este ticket. "Claude (com work)" = modo chat do
  Claude Desktop, que junta chat e work (Cowork), fora do modo Code: é a porta 6.
- 2026-10-11: os testes A a D rodaram (falta só o tempo do nó efêmero em "Testes das portas de
  entrada"). Próximo passo ao retomar: fechar aquele ticket e abrir a rodada 3 daqui com os fatos dos
  quatro grupos (`exploracao/anexos/testes-38-portas/`), voltando à pergunta da porta principal (R20).
- 2026-10-12: "Testes das portas de entrada" resolvido (o nó efêmero saiu da tailnet); este ticket
  está desbloqueado. Fatos dos quatro grupos no Answer daquele ticket.
- 2026-10-12: rodada 3 aberta na nota "Rodada atual" (R22 porta principal; R23 subpasta; R24
  Maestri; R25 Obsidian e `_archive/`; R26 Claude Desktop; R27 cliente pelo MCP; R28 repositório fora
  do hub; R29 níveis da R18). Recomendações: raiz como porta principal e nenhum `CLAUDE.md` no hub;
  subpasta com Claude Code e Codex (marcador), Copilot só na raiz, sem `.git` falso;
  `claude-md-and-agents-md` em cada par e papéis/partituras com fonte em `agents/`; `_archive/` movido
  por script que confere o outro par; Desktop só de leitura; `AGENTS.md` com cabeça autossuficiente de
  até 2.000 caracteres; caminho fixo do `AGENTS.md` e `agents/skills/<skill>/`; R18 volta a valer.
- 2026-10-12, respostas da rodada 3:
  - **R22, ok:** a sessão aberta na raiz do hub é a porta principal; as outras são secundárias e cada
    uma ganha só o que precisa. O hub não tem `CLAUDE.md` em lugar nenhum, e o kit de par confere.
  - **R23, B:** sessão em subpasta com Claude Code e Codex (marcador na raiz e
    `project_root_markers`, pelo kit de par); Copilot só na raiz; sem `.git` falso no hub.
  - **R24, aberta em ticket próprio:** o Gustavo quer definir até onde o Maestri segue padrão e onde
    ele fica livre, porque haverá muitas variantes. Virou "Maestri: padrão e liberdade", que passa a
    bloquear "Arquitetura de pastas e frontmatter do hub" e "Acesso dos agentes: decisão". Esta porta
    sai daqui.
  - **R25, A:** o cofre do Obsidian é a raiz do hub; mantém `_archive/` em cada raiz, e mover para
    ele é por um script que antes confere se o outro par está em dia e sem edição recente.
  - **R26, A:** o Claude Desktop (chat/work) entra na construção só de leitura, pela ponte
    `mcp-remote`; gravar por ele seria um ticket futuro, se o Gustavo quiser.
  - **R27, em aberto:** o Gustavo quer explorar opções para o contrato chegar a clientes pelo MCP;
    se preciso, um ticket explora isso com o MCP já criado e ajusta o MCP. Rodada 4 (R31).
  - **R28, ok com ressalva:** caminho fixo `C:\context-hub\AGENTS.md` e skills em
    `agents/skills/<skill>/`, ligadas sem cópia; mas o Gustavo quer testar e explorar melhor. Rodada 4
    (R32).
  - **R29, não entendida:** a pergunta citou R18 e R19 sem dizer o que eram. Refeita na rodada 4
    (R30).
- 2026-10-12: rodada 4 aberta na nota "Rodada atual" (R30 níveis de pasta, R31 contrato para
  clientes pelo MCP, R32 testes da porta do repositório fora do hub).
- 2026-10-12, respostas da rodada 4 (todas "ok"):
  - **R30:** a profundidade de pastas da R18 de "Arquitetura de pastas e frontmatter do hub" sai de
    revisão; a R19 volta a ser a próxima pergunta de lá.
  - **R31:** pesquisa curta antes de escolher como o contrato chega a clientes pelo MCP. Virou
    "Contrato pelo MCP: pesquisa", que agora bloqueia este ticket (a porta do cliente pelo MCP espera
    por ela). O teste com o MCP criado fica para a construção.
  - **R32:** aberto "Testes da porta do repositório fora do hub" (cinco pontos), que bloqueia "Acesso
    dos agentes: decisão". O que a árvore garante para esta porta (caminho fixo do `AGENTS.md` e
    `agents/skills/<skill>/`) está decidido.
- 2026-10-12 (vinda de "Contrato pelo MCP: pesquisa"): a descrição das ferramentas chega ao modelo nos
  três harnesses; o `instructions` chega inteiro ao Copilot do VS Code, só sob demanda ao Copilot CLI
  (salvo `--allow-all-mcp-server-instructions`) e vai na requisição do Codex sem efeito confirmado.
  Rodada 5 aberta na nota "Rodada atual" (R33: por quais canais o contrato chega a um cliente pelo MCP).
- 2026-10-12, resposta da rodada 5:
  - **R33, ok (C):** o contrato chega a um cliente pelo MCP por três canais juntos: o `instructions`
    do fork leva o começo do `AGENTS.md` (até 2.000 caracteres, autossuficiente); a descrição de cada
    ferramenta de gravação leva a regra curta "antes de gravar, leia `AGENTS.md`"; e, onde der para
    instalar, o kit de cliente liga `--allow-all-mcp-server-instructions` no Copilot CLI e põe o
    contrato na configuração global do harness. O teste dos três harnesses com o MCP pronto (inclui
    capturar a requisição do Codex) vira ticket da construção. Com isso todas as portas deste ticket
    estão decididas; falta só registrar a resolução (próxima sessão, regra de um ticket por sessão).

## Answer

Fechado em 2026-10-12 com as rodadas 3 a 5 (detalhe nos comentários acima). Cada porta ganha só o que
precisa; fatos em "Portas de entrada: pesquisa", "Testes das portas de entrada", "Contrato pelo MCP:
pesquisa" e "Testes da porta do repositório fora do hub".

- **Porta principal, sessão na raiz do hub (R22):** é por ela que o Gustavo e os agentes chegam; os
  três harnesses leem o `AGENTS.md` da raiz e acham o resto pela busca. O hub não tem `CLAUDE.md` em
  lugar nenhum (um `CLAUDE.md` acima ou dentro desliga os `AGENTS.md` no Claude Code), e o kit de par
  confere isso.
- **Sessão numa subpasta (R23):** Claude Code e Codex, com um marcador na raiz do hub e
  `project_root_markers` no Codex, postos pelo kit de par; o Copilot só abre na raiz; nada de `.git`
  falso no hub.
- **Maestri, workspace e papel (R24):** saiu daqui para "Maestri: padrão e liberdade".
- **Obsidian (R25):** o cofre é a raiz do hub. Cada raiz mantém seu `_archive/`, e mover para ele é
  por um script que antes confere se o outro par está em dia e sem edição recente (o LiveSync não
  garante mover pasta com a outra máquina editando).
- **Claude Desktop, chat e work (R26):** entra só de leitura, pela ponte `mcp-remote` (MCP stdio); não
  recebe o contrato por arquivo.
- **Cliente pelo MCP de um par (R33):** o contrato chega por três canais juntos: o `instructions` do
  fork leva o começo do `AGENTS.md` (cabeça autossuficiente de até 2.000 caracteres, pelo corte de
  2.048 do Claude Code); a descrição de cada ferramenta de gravação diz "antes de gravar, leia
  `AGENTS.md`"; e, onde der para instalar, o kit de cliente liga `--allow-all-mcp-server-instructions`
  no Copilot CLI e põe o contrato na configuração global do harness.
- **Sessão num repositório fora do hub (R28, R32):** caminho fixo `C:\context-hub\AGENTS.md` e skills
  em `agents/skills/<skill>/`. O contrato chega por import no `~/.claude/CLAUDE.md` e por link
  simbólico em `~/.codex/AGENTS.md` e `~/.copilot/copilot-instructions.md` (que hoje tem o GSD; o kit
  junta os dois); as skills por junction em `~/.claude/skills` e `~/.agents/skills`. Link físico não
  serve, o simbólico pede o modo de desenvolvedor do Windows, e o contrato só se edita dentro do hub.
- **Lista aberta:** porta nova que surgir entra como ticket novo no mapa, com a mesma regra (só o que
  ela precisa).
- **Para a construção** (anotado em "Passagem para a construção"): as conferências e ligações do kit
  de par e do kit de cliente acima, o script do `_archive/`, a ponte do Desktop e o teste dos três
  harnesses com o MCP pronto (inclui capturar a requisição do Codex). Chegar não é obedecer: no teste
  do VS Code o contrato chegou e a regra não foi seguida, o que a verificação dos cinco critérios
  precisa medir.

- 2026-10-12, revisão da porta do Claude Desktop (depois de resolvido): vendo o visual do mapeamento,
  o Gustavo disse que vai pedir coisas pelo Claude Desktop e que ele "não deve ser proibido de escrever
  no C:/context-hub diretamente". A parte "só de leitura" da R26 cai; "gravar pelo Claude Desktop" sai do
  fora do escopo e passa a ser decidido em "Como os agentes gravam no hub". A leitura pela ponte
  `mcp-remote` continua.
- 2026-10-12, revisão da sessão em subpasta (vinda de "Maestri: padrão e liberdade", R57): o Copilot
  também abre na pasta da iniciativa; o contrato da raiz chega a ele pelo arquivo global
  (`~/.copilot/copilot-instructions.md` ligado ao hub), e na pasta ele recebe o `AGENTS.md` da
  iniciativa. "Copilot só na raiz" da R23 cai. Continua sem `.git` falso no hub.
