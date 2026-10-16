# Rodada 1 — Quadrante (relator)

Tickets lidos por inteiro: 13, 14, 15, 16, 18, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 52, 53, 55. Os tickets 39,
41, 46 (pesquisas, "não é decisão do mapa"), 52, 53 e 55 (laço e portal, fora do mapa) não mudam o spec; o 53 e o 55
já estão certos no "Out of scope" da faixa 7 e da faixa 9. O que decide o spec está em 14, 15, 16, 36, 40, 42, 44 e 45.

Convenções que proponho para a proposta (a aplicar na rodada 2 se os dois concordarem):

- **[núcleo]**: escolha do núcleo sem ticket resolvido. Fica na proposta com esta marca, para o aval do Gustavo.
- **[formato]**: depende do formato da execução. Minutos, dublês, "se couber", "entrega cedo", portas de ensaio por
  faixa e dono de passo do kit ficam marcados assim; onde ajudar, a nota diz o que muda com etapas sequenciais.
- **[ticket aberto: 56]**: o que vem de rodada respondida do laço do system design.

## Mudanças

### Q-1: Guarda do acervo não cobre as propostas nem o registro de uso
- Onde: `spec.md`, Worker 9; `faixas-09-10.md`, faixa 9, Implementation decisions "Guarda do acervo no Claude Code"
  e "no Codex e no Copilot", e Pontos abertos "Que pastas a guarda cobre".
- Texto atual (núcleo): "gravar em `agents/skills/**` ou `agents/maestro/**` pede aval, exceção do maestro em
  `routing.yml`; Codex e Copilot: recusa apontando `agents/maestro/propostas/`".
- Texto proposto: "gravar em `agents/skills/**` pede aval (exceção do maestro em `agents/skills/routing.yml`);
  `agents/maestro/propostas/` fica aberta a todo harness e `agents/maestro/uso/<máquina>.md` é gravado pelo hook de
  uso, fora da guarda; Codex e Copilot: recusa em `agents/skills/**` apontando `agents/maestro/propostas/`". Na parte,
  tirar o ponto aberto e escrever a mesma coisa; fica aberto só se as skills de uso geral fora da família `maestro-*`
  entram na guarda (o ticket 40 fala do acervo, não de toda skill).
- Fonte: ticket 40, Answer, "Guarda": "Codex e Copilot não gravam no acervo e deixam propostas em
  `agents/maestro/propostas/`"; "Quem usa": "registro de uso por máquina em `agents/maestro/uso/<máquina>.md`, gravado
  por hook"; ticket 15, rodada 3: exceção para o maestro em `routing.yml`. (É a D27 do Prisma; concordo.)

### Q-2: GSD sai do arquivo global do Copilot, com cópia
- Onde: `faixas-07-08.md`, faixa 8, user story 11 e Pontos abertos "Contradições achadas", item GSD.
- Texto atual: "quero que o kit trate o que já está em `~/.copilot/copilot-instructions.md` (hoje, as instruções do
  GSD) sem perder nada"; "decidir antes do ticket de construção".
- Texto proposto: story 11: "quero que o kit tire o GSD do arquivo global do Copilot e do escopo global das skills,
  com cópia antes, para que só o contrato e as skills de uso geral fiquem globais". Tirar o item da lista de
  contradições: vale o 15, o mais recente.
- Fonte: ticket 15, rodada 2 (2026-10-15): "o kit tira o GSD do escopo global, com cópia antes"; ticket 42 (2026-10-12)
  e o comentário de 2026-10-12 do 16 ("juntando com o GSD") são anteriores. (D24 do Prisma; concordo.)

### Q-3: Lista "Contradições achadas" da faixa 8 vira decisão
- Onde: `faixas-07-08.md`, faixa 8, Pontos abertos, "Contradições achadas" (três itens).
- Texto atual: três itens "decidir antes do ticket de construção".
- Texto proposto: apagar a lista. O marcador de raiz já está resolvido na própria parte ("vale o 14"); o GSD é a Q-2; a
  ponte do Desktop com escrita é decisão do ticket 11 (o mais recente), e o dono da ponte fica **[formato]** (ver Q-9).
- Fonte: ticket 14, rodada 4 (2026-10-15 08:33): "o kit não cria mais o marcador de raiz"; ticket 36, revisão de
  2026-10-12 da porta do Desktop: "gravar pelo Claude Desktop ... passa a ser decidido em 'Como os agentes gravam'".

### Q-4: Checagem de início sem arquivo da vigia e sem MCP avisa "estado indisponível"
- Onde: `faixas-01-02.md`, faixa 2, Testing decisions, "Hook de início"; `faixas-07-08.md`, faixa 7, user story 20 e
  Testing decisions ("sem o arquivo de estado, a mesma checagem chega pela ferramenta do MCP").
- Texto atual (faixa 2): "nos três casos do 14 (com o arquivo da vigia, sem ele com o MCP, sem os dois), a saída traz o
  estado do sync".
- Texto proposto: "com o arquivo da vigia, a saída traz o estado; sem ele, o estado vem da ferramenta do MCP; sem os
  dois, a saída diz que o estado está indisponível e não afirma que o sync foi conferido". Na faixa 7, acrescentar o
  terceiro caso ao teste.
- Fonte: ticket 14, Answer, "Checagem de início": "no par, o hook lê o arquivo da vigia; sem ele, a ferramenta do MCP";
  bancada de acesso (`bancada-acesso-relatorio.md`, §5): o hook da bancada, sem os dois, avisa "DESCONHECIDO", e o
  teste passou nos três harnesses com essa saída. (D7 do Sextante; concordo.)

### Q-5: Aviso em dobro no Codex: os dois canais ficam, por decisão
- Onde: `spec.md`, Pontos abertos, último item ("Aviso em dobro no Codex"); `faixas-07-08.md`, faixa 7, Pontos abertos,
  "Aviso em dobro no Codex".
- Texto atual: "falta decidir se os dois coexistem ou se um suprime o outro".
- Texto proposto: tirar dos pontos abertos. Escrever na faixa 7: "no Codex, a vigia notifica quando o estado piora (33)
  e o `notify` dispara a notificação do Windows no fim de cada turno com divergência (14); os dois ficam. Suprimir
  repetição dentro de um mesmo estado é detalhe da construção, não decisão".
- Fonte: ticket 33, Answer: "uma vigia a cada 5 min avisa"; ticket 14, rodada 8 (2026-10-15 17:49): "vigia no Codex =
  A (fica a checagem de início e o `notify` com a notificação do Windows)". As duas decisões são explícitas e
  posteriores a qualquer dúvida; nenhuma manda suprimir a outra.

### Q-6: Regra curta nas ferramentas de gravação do MCP: a frase do ticket 36 é obrigatória; o resto é [núcleo]
- Onde: `spec.md`, Worker 5 (c); `faixas-05-06.md`, faixa 5, user story 15 e "Contrato pelo MCP"; `faixas-09-10.md`,
  faixa 10, "Cabeça do contrato no MCP".
- Texto atual (núcleo): "a regra curta ('leia antes, grave com a `base_rev` lida; conflito = releia e refaça') na
  descrição de `write_note`, `edit_note`, `delete_note` e `move_note`".
- Texto proposto (núcleo e partes): "a descrição de cada ferramenta de gravação (`write_note`, `edit_note`,
  `delete_note`, `move_note`) começa por 'antes de gravar, leia `AGENTS.md`' (36) e segue com 'grave com a `base_rev`
  lida; conflito = releia e refaça' [núcleo]".
- Fonte: ticket 36, R33 (2026-10-12): "a descrição de cada ferramenta de gravação leva a regra curta 'antes de gravar,
  leia `AGENTS.md`'"; ticket 41: a descrição das ferramentas é o único canal que chega nos três. A segunda frase não
  está em ticket; cumpre o 11 e o 25, mas é escolha do núcleo. (D10 do Prisma: proposta de resolução.)

### Q-7: Teste dos três harnesses com o MCP pronto entra no núcleo do Worker 5
- Onde: `spec.md`, Worker 5, "Como se prova".
- Texto atual: testes (1) a (8), todos contra o MCP direto.
- Texto proposto: acrescentar "(9) os três harnesses reais, em modo não interativo com HOME de ensaio, citam o que
  receberam do servidor; a requisição do Codex é capturada para ver onde o `instructions` vai; no Copilot CLI, com e sem
  `--allow-all-mcp-server-instructions` **[formato: depende do login de ensaio]**".
- Fonte: ticket 36, Answer, "Para a construção": "o teste dos três harnesses com o MCP pronto (inclui capturar a
  requisição do Codex)"; ticket 41, Answer: "Fechar isso precisa de teste: capturar a requisição". A parte da faixa 5
  já tem o teste; o núcleo não.

### Q-8: Hooks do acervo agem fora do hub, pela variável do Maestri, não pela pasta
- Onde: `faixas-09-10.md`, faixa 9, Implementation decisions "Primeira instrução" e "Registro de uso", e Pontos abertos
  ("Hooks do usuário 'saem na hora fora do hub' (14), mas o acervo serve a todo maestro...").
- Texto atual: ponto aberto, sem resolução.
- Texto proposto: "o hook de início do acervo e o hook de uso são a exceção à regra 'sai na hora fora do hub' (14): o
  primeiro age sempre que `MAESTRI_TERMINAL_ID` existe, em qualquer pasta; o segundo age sempre que uma peça do acervo
  é usada, em qualquer pasta. Os demais hooks do hub (início com a vigia, fim, recusa) seguem o 14". Marcar
  **[núcleo]**: leitura que concilia os dois tickets, para o aval do Gustavo.
- Fonte: ticket 40, R52 (2026-10-12): "hook de início de sessão que só age com `MAESTRI_TERMINAL_ID`"; R38: "todos os
  workspaces vão receber a primeira instrução, os roteando ao hub"; ticket 43: "O que alcança todo workspace, dentro ou
  fora do hub, é o arquivo global de cada harness; reforços possíveis são a skill do acervo e um hook de início de
  sessão que só age quando a variável `MAESTRI_TERMINAL_ID` existe". O ticket 14 (rodada 3) decidiu "o script sai na
  hora quando a pasta não é do hub" para os hooks do hub (início, fim, recusa), sem citar o acervo.

### Q-9: Um dono só para a ponte do Claude Desktop, marcado [formato]
- Onde: `faixas-05-06.md`, faixa 5, Out of scope; `faixas-07-08.md`, faixa 8, user story 37 e "Claude Desktop";
  `faixas-09-10.md`, faixa 10, Out of scope.
- Texto atual: a faixa 5 manda para a 8; a 8 assume e diz "para o MCP do banco e para a busca"; a 10 diz "não tem faixa
  dona"; o núcleo diz Worker 10 (f) "se couber ... geradas e não instaladas".
- Texto proposto: nas três partes, o mesmo texto: "a ponte `mcp-remote` do Claude Desktop (busca e MCP do banco **com
  escrita**, ticket 11) é gerada pelo kit e não instalada; dono: faixa 10, como no núcleo **[formato]**". A faixa 8 fica
  só com a pasta conectada do Cowork, se o formato a mantiver.
- Fonte: ticket 11, Answer (via mapa): "Desktop pela pasta conectada e pelo MCP"; ticket 36, revisão de 2026-10-12;
  ticket 38, grupo D: "o Claude Desktop (chat/work) só chega ao hub por MCP local stdio (ponte `mcp-remote`)". O dono é
  formato. (D11, D25 e D32 do Prisma; concordo com a marca.)

### Q-10: Duas camadas de skills na junction global
- Onde: `faixas-07-08.md`, faixa 8, user stories 15 a 17 e Implementation decisions "Skills"; `spec.md`, Worker 8.
- Texto atual: "cada skill em `agents/skills/<skill>/`, com duas junctions, em `~/.claude/skills` e em
  `~/.agents/skills`".
- Texto proposto: "a junction global (`~/.claude/skills` e `~/.agents/skills`) leva só as skills de uso geral (a busca,
  o FreeLLMAPI, o fluxo do Matt Pocock, a família `maestro-*` e as poucas que servem a qualquer trabalho); as de um
  papel ficam no acervo e entram só na pasta do papel, pela receita de setup". Teste: uma skill de papel não aparece fora
  da pasta do papel.
- Fonte: ticket 15, rodada 2 (2026-10-15 20:42): "A junction global leva só as skills de uso geral ...; as de um papel
  ficam no acervo e entram só na pasta daquele papel". (D26 do Prisma; concordo.) Ponto que fica aberto: como a junction
  liga "só algumas" pastas de `agents/skills/` (uma junction por skill, ou uma pasta `agents/skills/geral/`): não
  decidido, construção.

### Q-11: Marcador de raiz: alinhar as linhas desatualizadas, sem reescrever tickets
- Onde: `faixas-09-10.md`, faixa 9, "Contrato dentro do papel" (já certo); `faixas-01-02.md`, faixa 1 (já certo);
  `spec.md`, Pontos abertos, item "Marcador de raiz".
- Texto atual (núcleo): "os tickets 36 e 40 o põem no kit; a rodada 4 do 14 o tira. Vale o 14 (mais recente): o kit
  não cria marcador."
- Texto proposto: manter, e acrescentar: "o teste do 14 passou em subpasta e em pasta de papel com o `.git` real; o
  ticket 45 (sem `.git`) mostrou o Copilot parando na iniciativa, o que o `.git` resolve". Sem mudança de decisão; só
  fonte do teste para a construção.
- Fonte: ticket 14, bancada de acesso: "`.git` real no lugar do marcador: passou no Codex e no Copilot, em subpasta e
  em pasta de papel"; ticket 45, Answer.

### Q-12: Copilot: `COPILOT_HOME` de ensaio não prova as skills; dizer o que o ensaio prova
- Onde: `spec.md`, Pontos abertos, último item; `faixas-07-08.md`, faixa 8, Pontos abertos "`COPILOT_HOME` no ensaio".
- Texto atual: "o ensaio precisa de outro jeito de isolar o HOME".
- Texto proposto: "no Copilot, o HOME de ensaio por `COPILOT_HOME` prova contrato, MCP e hooks, não as skills de
  `~/.agents/skills`; as skills do Copilot ficam como passo `ready-for-human` no HOME real, ou o ensaio usa
  `COPILOT_SKILLS_DIRS` apontando para a junction de ensaio **[núcleo]**".
- Fonte: ticket 18, Answer: "com `COPILOT_HOME` definido, o CLI deixa de ler `~/.agents/skills` (v1.0.66)"; "Aceita
  pastas extras por `COPILOT_SKILLS_DIRS`". A saída por `COPILOT_SKILLS_DIRS` é escolha minha, não ticket.

### Q-13: Lacunas de dono do ticket 16: as duas que o núcleo resolveu ficam [núcleo]; as três outras seguem abertas
- Onde: `faixas-09-10.md`, faixa 10, Pontos abertos "Lacuna de dono 4", "Lacuna de dono 5", "Lacuna de dono 7"; faixa
  9, Pontos abertos (modelo do verificador; erro de peça sumida).
- Texto atual: "não decidido" nas cinco.
- Texto proposto: lacuna 4 (30 dias): "`limpar-arquivo` na tarefa diária da faixa 10 **[núcleo]**"; lacuna 5 (cabeça):
  "o fork relê o bloco `cabeca:inicio/fim` a cada `initialize`, sem cópia; a faixa 10 só confere tamanho e existência
  **[núcleo]**"; lacunas "registro do aval no contrato", "modelo do verificador da guarda" e "erro de peça citada que
  sumiu": seguem abertas, sem dono, para o Gustavo.
- Fonte: ticket 16, comentário de 2026-10-15 (as cinco lacunas); núcleo, Worker 5 (c) e Worker 10 (b), (d), (g).
  (D8 e D30 do Prisma; concordo com a marca.)

### Q-14: As quatro perguntas do plano ao Gustavo continuam sem resposta
- Onde: toda menção a "pergunta do plano ao Gustavo" (login de ensaio, Docker de ensaio, cópia dos pilotos do vault,
  teste do gemini) nas cinco partes e no núcleo.
- Texto atual: cada parte cita a pergunta como aberta, com redações diferentes.
- Texto proposto: uma nota só no núcleo, em "Further Notes": "A rodada 2 do ticket 16 (Docker de ensaio, login dos
  harnesses no HOME de ensaio, copiar os pilotos do vault, teste do gemini pelo FreeLLMAPI) ficou sem resposta;
  recomendadas A nas quatro. Onde o spec depende delas, está marcado **[formato]**". Nas partes, trocar as redações
  por "pergunta aberta do 16, rodada 2".
- Fonte: ticket 16, comentários de 2026-10-15 ~22h (rodada 2 aberta) e 2026-10-15 ~22h20 ("pode parar"); nenhuma
  resposta registrada.

### Q-15: Formato da execução: o que muda com etapas sequenciais (nota, não decisão)
- Onde: `spec.md`, "Solution", "Further Notes" e todo "Como segue sem esperar as outras faixas".
- Texto atual: "1 hora, 10 workers em paralelo", minutos, dublês, "se couber".
- Texto proposto: não mudar os números; marcar **[formato]** e acrescentar em "Further Notes": "Se cada faixa virar uma
  etapa sequencial (ideia inicial do Gustavo, 16, 2026-10-16): os dublês somem (cada etapa usa a entrega da anterior);
  'entrega cedo no minuto N' vira 'a etapa anterior entrega'; os 'se couber' (validação de frontmatter no MCP, Config
  Doctor, ponte do Desktop) voltam a ser entrega cheia, como os tickets 12, 33 e 11 pedem; as portas de ensaio por
  faixa (5994 a 5997, 8796, 8797, 3939, 3940) podem virar um banco de ensaio só". Ordem sugerida das etapas, se ajudar o
  Gustavo: 1, 4, 5, 3, 6, 2, 7, 9, 10, 8 (o kit por último junta tudo).
- Fonte: protocolo ("digam o que muda com etapas sequenciais"); ticket 16, comentário de 2026-10-16 ~14h35; tickets 12
  (MCP valida igual), 33 (Config Doctor), 11 (Desktop grava). (Cobre S8, S15, P12, P21, P22 da triagem.)

### Q-16: Ticket 56 é aberto: marcar as user stories da faixa 10 que vêm dele
- Onde: `faixas-09-10.md`, faixa 10, user stories 5, 6, 7, 13, 14, 15, 37 e Implementation decisions "Prazo de 30 dias",
  "Cópia de segurança diária".
- Texto atual: "(56, rodada 7)", "(56, rodada 8)" como se fossem decisão.
- Texto proposto: manter as stories, com a marca **[ticket aberto: 56]** e a nota: "os 30 dias aparecem também no 16
  (resolvido), como lacuna de dono; a regra em si só está no 56". Nada se constrói sobre elas antes de o 56 fechar ou de
  uma rodada resolvida registrar as respostas.
- Fonte: protocolo; ticket 16, comentário de 2026-10-15 ("quem confere os 30 dias do `_archive/` e apaga"). (D28 do
  Prisma; concordo com o ajuste.)

## Divergências dos insumos que continuam valendo (dos meus tickets ou da triagem)

- Prisma D24, D26, D27, D8, D30, D11, D25, D32: cobertas acima (Q-2, Q-10, Q-1, Q-13, Q-9).
- Prisma D10: proposta de resolução na Q-6.
- Sextante D7: Q-4. Sextante D8 e D15: Q-15.
- Correções mecânicas da triagem fora dos meus tickets (P1, P2, P4 a P7, P9, P14, P16 a P18, P23, P29, P33, P34; S3,
  S4, S9 a S11, S13, S14): concordo em aplicar na rodada 2 se o Prisma e o Sextante as trouxerem como estão; marco
  [núcleo] onde a triagem já diz "escolha do núcleo" (P3, P8, P15, P19, P29, S12) e [formato] em P1 e P17 (portas).

## O que não mudo (conferido contra os meus tickets)

- Contrato: Claude Code por import no `~/.claude/CLAUDE.md`, Codex e Copilot por link simbólico (36 R28, 42); o Answer
  do 14 resume como "link simbólico", mas o teste do 42 é o import no Claude Code. O spec está certo.
- Hooks no escopo do usuário, `hooks.state` no Codex, só hook de usuário no Copilot, `danger-full-access`,
  `default_tools_approval_mode="approve"`, MCP em 127.0.0.1 com token de variável, proxy com três rotas (14): certos
  no núcleo e nas faixas 2, 5, 6, 7, 8 e 10.
- Fim da resposta por harness e estado da vigia na tela (14): certos nas faixas 2, 7, 8 e 9.
- `claude-md-and-agents-md` ligado pelo kit (40 R51, 14): certo.
- Preset `custom` do Copilot no Maestri (18): certo na faixa 8.
- Cabeça de 2.000 caracteres (36) com o corte de ~3.300 visto no 38: o núcleo escolhe o menor; certo.
