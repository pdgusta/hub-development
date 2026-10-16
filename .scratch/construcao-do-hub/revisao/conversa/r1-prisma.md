# Rodada 1: Prisma

Tickets lidos por inteiro: 05, 06, 07, 08, 11, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 47, 48 e o 56 (aberto).
Base: `divergencias-prisma.md` (D1 a D34) e a triagem. Caminhos relativos a `proposta/`.

## O que os meus tickets decidem sobre o spec, em resumo

- **Banco e vista (22, 25, 30, 34):** CouchDB + LiveSync, um CouchDB por par, mestre-mestre, cada par envia as próprias
  mudanças (R62 do 33, que muda o 34). O fork do es617 com `base_rev` e conflito visível é obrigatório antes de usar.
  A faixa 4 da proposta já segue isso bem; não acho nada a mudar nela fora do que o Sextante trouxe.
- **Sync e divergência (33 vence 06, 07 e 08):** CLI do LiveSync como tarefa agendada; 200 MiB; pastas com ponto fora;
  GitHub só cópia diária; divergência = colisão real, 15 min com o outro par ligado, arquivo acima de 200 MiB, binário
  descartado até o Gustavo olhar. Vigia a cada 5 min, notificação quando piora. O núcleo e as partes 4 e 7 seguem isso.
- **Gravação (11, o mais novo, vence 08 na forma):** dois caminhos, troca de trecho no disco e regravação inteira pelo
  `write_note` com a versão lida; hook recusa no disco; banco fora = regravação espera. O "é recusada" do 08 e do 11
  vira "conflito visível + resposta releia e refaça" pelo 25 e 30 (o núcleo já diz isso).
- **E2EE (34, 48):** decidida; o 48 testou E2EE v2 com caminho ofuscado no CLI. Logo, quem lê o CouchDB (MCP e vigia)
  precisa da frase-senha para achar o caminho.
- **56 (aberto):** 30 dias do `_archive/`, "remover" = arquivar, nenhuma iniciativa de cliente vetada no GitHub, dois dias
  de distância bastam, "notificação do Windows basta", nota nova do Obsidian em `inbox/`. Tudo "vem de ticket aberto".

## Mudanças propostas

### Prisma-1: Recusa ou conflito já decidido (faixa 5)
- Onde: `spec-partes/faixas-05-06.md`, faixa 5, Pontos abertos, "Recusa ou conflito gravado".
- Texto atual: "A construção tem de escolher uma forma ... e o maestro confirma com o Gustavo se a folha concorrente fica no banco."
- Texto proposto: tirar dos pontos abertos. Nas Implementation decisions: "Gravação com base velha vira conflito: a versão do agente fica como folha filha da base lida, a outra versão fica intacta, e a resposta ao agente diz 'conflito: releia e refaça'."
- Fonte: 25, Answer ("a gravação leva `base_rev` e vira conflito se a base mudou"); 30, Answer, item 4 (R1 emulada virou conflito visível); núcleo, Pontos abertos. O 11 ("é recusada") é mais novo, mas a própria resposta do 11 cita o `write_note` "com a versão lida" sem mudar o mecanismo do 25; leio o 11 como a garantia e o 25 como a forma.

### Prisma-2: Versão de base em `write_note` e `edit_note` (faixa 5)
- Onde: faixa 5, Pontos abertos, "Versão de base nas outras ferramentas".
- Texto atual: "se anexar ao fim e ao início e a troca de trecho também levam a versão de base ... Não decidido."
- Texto proposto: "`write_note` e `edit_note` exigem `base_rev`; sem ela, regravar nota existente é recusado. Fica aberto só se anexar ao fim e ao início leva base (no spike, agem sobre a versão atual)."
- Fonte: 30, Answer, esforço ("`write_note`/`edit_note` aceitam `base_rev` e gravam como filha dela"); núcleo, Worker 5 (a).

### Prisma-3: Instância só de leitura pelo `READ_ONLY=true` (faixa 5)
- Onde: faixa 5, Pontos abertos, "Instância só de leitura".
- Texto atual: "como o fork fica só de leitura (ferramentas de gravação ausentes ou recusadas) não está decidido".
- Texto proposto: "A instância de leitura é a mesma linha de comando com `READ_ONLY=true` (já existe no upstream: 'disable all write tools'). Teste: não lista ferramenta de gravação e recusa gravar."
- Fonte: 34, Answer ("cada par roda um segundo MCP com `READ_ONLY=true` e token"); núcleo, Worker 5 (e) e teste (5).

### Prisma-4: E2EE no MCP do banco (faixa 5)
- Onde: faixa 5, Pontos abertos, "Cifra do banco"; user stories e Testing decisions.
- Texto atual: "se o banco for cifrado, a senha da cifra também vai ao MCP ... a decisão sobre cifrar é da faixa 4".
- Texto proposto: tirar o ponto aberto. Nova user story: "Como agente, quero que o MCP leia e grave no banco cifrado com a frase-senha do `.env` do par, para que a E2EE não tire a guarda de versão." Teste: os testes de versão de novo com E2EE ligada.
- Fonte: 34, Answer, Segurança ("E2EE do LiveSync"); 30, Answer, Configuração ("E2EE (com a passphrase também no MCP)"); 48, item 11 (E2EE v2 com caminho ofuscado); núcleo, Worker 5 (f) e teste (8).

### Prisma-5: Ferramenta de estado do hub no MCP (faixa 5)
- Onde: faixa 5, user stories e Implementation decisions (ausente).
- Texto atual: nada.
- Texto proposto: user story "Como agente no par sem o arquivo da vigia, ou num cliente, quero ler o estado do hub por uma ferramenta do MCP do banco, para a checagem de início não ficar às cegas." Decisão: "Ferramenta de estado: devolve o estado da vigia (esquema da faixa 7); nome no núcleo, `estado_do_hub`."
- Fonte: 14, Answer, Checagem de início ("no par ... sem ele, a ferramenta do MCP; no cliente, a ferramenta do MCP"); núcleo, Worker 5 (d). O nome é escolha do núcleo.

### Prisma-6: Conflito visível nas duas formas (faixa 5)
- Onde: faixa 5, "Conflito visível ao agente", Pontos abertos "Forma do conflito visível", user story 8.
- Texto atual: "aviso na leitura ou uma ferramenta que lista os conflitos (a escolha entre as duas é da construção)".
- Texto proposto: "`read_note` de nota em conflito avisa e lista as folhas, e uma ferramenta lista os conflitos abertos." Marcar: escolha do núcleo.
- Fonte: 30, Answer, esforço ("aviso no `read_note` ou ferramenta `get_conflicts`", alternativa); 25 ("o conflito visível ao agente", sem forma); núcleo, Worker 5 (b). Escolha do núcleo, pede aval.

### Prisma-7: Cabeça do contrato antes do texto do upstream e relida a cada conexão (faixas 5 e 10)
- Onde: faixa 5, "Contrato pelo MCP", user story 13, Out of scope ("a atualização da cabeça ... faixa 10"), Pontos abertos "De onde vem a cabeça"; faixa 10, Pontos abertos "Lacuna de dono 5".
- Texto atual: "texto fixo na configuração do fork ou lido do `AGENTS.md` do hub. Quem a atualiza é lacuna de dono da faixa 10".
- Texto proposto: "O fork lê o bloco `cabeca:inicio/fim` do `AGENTS.md` a cada `initialize`, sem cópia, e o põe antes do texto do upstream. A faixa 10 só confere se o bloco existe e cabe em 2.000 caracteres." Marcar: escolha do núcleo (a lacuna do 16 não tem ticket que a feche).
- Fonte: 36, R33 (cabeça autossuficiente até 2.000, pelo corte de 2.048); 16, comentário de 2026-10-15 (lacuna de dono 5, aberta); núcleo, Worker 5 (c) e Worker 10 (d).

### Prisma-8: Texto da regra curta nas ferramentas de gravação (faixas 5 e 10; núcleo)
- Onde: `spec.md`, Worker 5 (c); faixa 5, user story 15 e "Contrato pelo MCP"; faixa 10, user story 20.
- Texto atual: núcleo "leia antes, grave com a `base_rev` lida; conflito = releia e refaça", em `write_note`, `edit_note`, `delete_note`, `move_note`; partes "antes de gravar, leia `AGENTS.md`".
- Texto proposto: "Antes de gravar, leia `AGENTS.md`; grave com a `base_rev` lida; conflito = releia e refaça", nas quatro ferramentas, igual no núcleo e nas partes. A primeira frase é a decidida; o resto é escolha do núcleo.
- Fonte: 36, R33 ("a descrição de cada ferramenta de gravação diz 'antes de gravar, leia `AGENTS.md`'"); 41 (a descrição é o único canal que chega ao modelo nos três). Pede aval do Gustavo na parte que soma.

### Prisma-9: Validação de frontmatter no MCP é decisão, "se couber" é formato (núcleo e faixa 5)
- Onde: `spec.md`, Worker 5 (g) "se couber"; faixa 5, user stories 10 a 12.
- Texto atual: núcleo "se couber: a gravação chama o verificador de frontmatter"; parte trata como entrega plena.
- Texto proposto: manter as user stories da parte. No núcleo, tirar o "se couber" do requisito e marcar "depende do formato" só a ordem de entrega.
- Fonte: 12, Answer, Imposição ("o MCP do banco valida igual"); 11, Answer, não verificado ("a validação de frontmatter dentro do MCP do banco").

### Prisma-10: Vigia lê o banco cifrado (faixa 7)
- Onde: faixa 7, user stories 7 a 12 e Testing decisions.
- Texto atual: nada sobre E2EE.
- Texto proposto: user story "Como Gustavo, quero que a vigia cite a nota em conflito e o binário descartado pelo caminho em claro, mesmo com o banco cifrado, para eu saber o que olhar." Teste: os casos de conflito e binário num CouchDB de ensaio com E2EE.
- Fonte: 34 (E2EE); 48, item 11 ("cada documento aparece com caminho cifrado e `size`, `mtime` e `children` zerados"); faixa 4 da proposta, "Para a vigia e a checagem" (o CLI dá o caminho em claro: `ls`, `info`, `cat-rev`); núcleo, Worker 7 (a).

### Prisma-11: Arquivo de estado da vigia (faixa 7)
- Onde: faixa 7, "Arquivo de estado" e Pontos abertos "Arquivo de estado".
- Texto atual: "lugar e esquema estão só como proposta do Worker 8 no plano; o dono desta faixa confirma".
- Texto proposto: "Estado em `C:\context-hub\.local\vigia\estado.json`, fora do banco e do `.git` (tem ponto no caminho), troca atômica, `nivel` por item (`ok | informa | divergencia`) e o do topo igual ao pior." Marcar: escolha do núcleo.
- Fonte: 33, Answer ("um estado curto que a checagem de início de sessão lê"; pastas com ponto fora do banco); 12 (o que tem ponto fica numa máquina); núcleo, Worker 7.

### Prisma-12: Detectores que já têm forma (faixa 7)
- Onde: faixa 7, Pontos abertos, "Detectores sem mecanismo decidido".
- Texto atual: "como a vigia sabe que a outra máquina está ligada na tailnet; como acha os ramos apagados de binário".
- Texto proposto: "Outro par ligado: a vigia testa o endereço do outro par (`HUB_OUTRO_PAR_URL`). Ramo apagado de binário: lido do CouchDB local (ou pelo CLI, com E2EE). Fica aberto só como saber que o Config Doctor travou o plugin."
- Fonte: 48, Answer, item 4 ("a perdida fica num ramo apagado, recuperável por script, também depois da compactação"); núcleo, Worker 7 (a). O teste do outro par é escolha do núcleo.

### Prisma-13: Config Doctor é requisito (faixa 7; núcleo)
- Onde: `spec.md`, Worker 7 (f) "se couber"; faixa 7, user story 15.
- Texto atual: núcleo "se couber: Config Doctor travando o plugin".
- Texto proposto: requisito da vigia, como na parte; "se couber" marcado "depende do formato".
- Fonte: 33, Answer, Aviso ("se o Config Doctor travou o plugin"); 48, item 5 ("o Config Doctor abre e o sync daquele cofre fica parado").

### Prisma-14: Falha da cópia diária (faixas 7 e 10)
- Onde: faixa 7, casos da vigia (ausente); faixa 10, Pontos abertos "Quem percebe a falha da cópia diária" e Fronteira.
- Texto atual: faixa 10 diz nos dois sentidos: "entra no estado da vigia" e "uma decisão só ..., a levar ao Gustavo".
- Texto proposto: deixar só "a cópia diária sai com código ≠ 0 e grava o item `copia-diaria` no estado da vigia; a vigia notifica" e marcar: escolha do núcleo, ligada à pendência "quem percebe a falha" do 56 (aberto). Na faixa 7, o caso de teste correspondente.
- Fonte: 33, Answer (GitHub como cópia diária; nada sobre o aviso da falha); 56, comentário de 2026-10-15 ~16h30 ("uma decisão só, a levar ao Gustavo"; base "notificação do Windows basta", rodada 7); núcleo, Worker 10 (c) e Worker 7. Decisão de verdade do Gustavo.

### Prisma-15: GSD sai do arquivo global do Copilot (faixa 8)
- Onde: faixa 8, user story 11 e Pontos abertos, "Contradições achadas", GSD.
- Texto atual: "quero que o kit trate o que já está em `~/.copilot/copilot-instructions.md` (hoje, as instruções do GSD) sem perder nada"; e "decidir antes do ticket de construção".
- Texto proposto: user story 11: "o kit tira o GSD do arquivo global do Copilot, com cópia antes, e liga o contrato do hub no lugar". Tirar o ponto aberto e escrever "vale o 15".
- Fonte: 15, rodada 2 ("o kit tira o GSD do escopo global, com cópia antes"), mais novo que 36 e 42; núcleo, Pontos abertos. (Ticket do Quadrante; peço que confira.)

### Prisma-16: Junction global só com as skills de uso geral (faixa 8)
- Onde: faixa 8, user stories 15 a 17 e "Skills".
- Texto atual: "cada skill em `agents/skills/<skill>/`, com duas junctions, em `~/.claude/skills` e em `~/.agents/skills`".
- Texto proposto: "A junction global leva só as skills de uso geral; as de papel entram só na pasta do papel, pela receita de setup (faixa 9)." Teste: uma skill de papel não aparece fora da pasta do papel.
- Fonte: 15, rodada 2. (Ticket do Quadrante; a forma da junction com duas camadas é aberta na faixa 9, "Onde as skills de papel moram".)

### Prisma-17: Ponte do Claude Desktop com escrita e com busca, um dono só
- Onde: faixa 5, Out of scope; faixa 8, user story 37 e "Claude Desktop"; faixa 10, Out of scope; `spec.md`, Worker 10 (f).
- Texto atual: faixa 5 manda à faixa 8; faixa 8 liga "para o MCP do banco e para a busca"; faixa 10 diz "não tem faixa dona"; núcleo põe na faixa 10, "se couber", "geradas e não instaladas".
- Texto proposto: o conteúdo igual nas três partes: "ponte `mcp-remote` (MCP stdio) do Claude Desktop para a busca e para o MCP do banco com escrita, mais a pasta conectada no Cowork com 'Folder instructions' apontando o `AGENTS.md`". O dono: "depende do formato".
- Fonte: 11, Answer, Claude Desktop ("pelos dois caminhos ... o MCP do banco com escrita pela ponte `mcp-remote`"; "também usa a busca do hub"); 36, revisão de 2026-10-12 (o "só leitura" cai); núcleo, Pontos abertos ("Vale o ticket 11").

### Prisma-18: Guarda do acervo sem as propostas e o registro de uso (núcleo e faixa 9)
- Onde: `spec.md`, Worker 9 ("gravar em `agents/skills/**` ou `agents/maestro/**` pede aval"); faixa 9, Pontos abertos "Que pastas a guarda cobre".
- Texto atual: núcleo põe `agents/maestro/**` inteiro sob a guarda.
- Texto proposto: "A guarda cobre o acervo (`agents/skills/maestro-*/`, as skills de papel e `agents/maestro/` fora de `propostas/` e `uso/`); `agents/maestro/propostas/` fica aberta ao Codex e ao Copilot; `agents/maestro/uso/` é gravado pelo hook; `routing.yml` tem a exceção do maestro." Fica aberto só se as skills de uso geral fora da família entram na guarda.
- Fonte: 40, Answer, Guarda e Quem usa; 15, rodada 3 (exceção do maestro em `routing.yml`). (Tickets do Quadrante.)

### Prisma-19: User stories da faixa 10 que vêm do 56 aberto
- Onde: faixa 10, user stories 5 a 7, 13 a 15 e 37; "Prazo de 30 dias"; "Cópia de segurança diária" (citam "56, rodada 7" e "56, rodada 8"); `spec.md`, Worker 10 (b).
- Texto atual: "Prazo de 30 dias (56, rodada 7)"; "Nenhuma iniciativa de cliente é vetada no repositório (56, rodada 7)"; "dois dias de distância bastam (56, rodada 8)".
- Texto proposto: marcar cada uma "vem de ticket aberto (56)". Proposta ao maestro: registrar essas respostas num ticket resolvido (ou resolver o 56) antes de construir.
- Fonte: 56, `Status: claimed`; protocolo, "O que vale como decisão". O 16 (resolvido) só tem a lacuna "quem confere os 30 dias do `_archive/` e apaga".

### Prisma-20: Data do arquivamento no nome da pasta (faixa 10)
- Onde: faixa 10, Pontos abertos, "Como o `_archive/` guarda a data".
- Texto atual: "o plano propõe a data no nome da pasta; não decidido".
- Texto proposto: "`_archive/<AAAA-MM-DD>--<nome>/` (a data viaja no nome, sem arquivo com ponto)." Marcar: escolha do núcleo.
- Fonte: 12 (o que tem ponto não replica, então um arquivo de data com ponto não serviria); núcleo, Worker 10 (a).

### Prisma-21: Limpeza dos 30 dias na tarefa diária (faixa 10)
- Onde: faixa 10, Pontos abertos, "Lacuna de dono 4".
- Texto atual: "o plano propõe tarefa diária; não decidido".
- Texto proposto: "`limpar-arquivo` roda na tarefa diária (cópia + limpeza + cabeça), com `-WhatIf`." Marcar: escolha do núcleo; o prazo de 30 dias vem do 56 (Prisma-19).
- Fonte: 16, comentário de 2026-10-15 (lacuna 4, aberta); núcleo, Worker 10 (b) e (g).

### Prisma-22: Duas instâncias do MCP do banco por par (faixas 4 e 10)
- Onde: faixa 10, Pontos abertos "Duas instâncias ... podem ser três por par"; faixa 4, Pontos abertos "Duas instâncias ... inferência" (S14 do Sextante).
- Texto atual: "inferência, não verificado"; "podem ser três por par".
- Texto proposto: "Duas instâncias por par, em 127.0.0.1, cada uma com o seu token: escrita (agentes do par e, pelo proxy, a rota `/banco-escrita/mcp`) e `READ_ONLY=true` (rota `/banco/mcp`). Não verificado: as duas juntas no mesmo par."
- Fonte: 34 (segundo MCP `READ_ONLY=true`); 11, Cliente ("segunda instância do MCP do banco, com escrita e a mesma guarda de versão"); 14, rodada 7 (um token por rota no proxy). Dúvida que deixo à conversa: o "segunda instância" do 11 pode ser lido como terceira; com um token por rota no proxy, duas bastam.

### Prisma-23: `--allowed-host` da busca atrás do proxy (faixa 10)
- Onde: faixa 10, "Proxy de MCP no par" e Testing decisions.
- Texto atual: nada.
- Texto proposto: "A porta do proxy vai no `.env` do kit; a busca aceita o `Host` do proxy (`--allowed-host`) se o proxy repassar o `Host` do cliente (não verificado)." Teste: a busca responde pelo proxy.
- Fonte: 14, Answer ("a busca escuta só em 127.0.0.1"; "não verificado: o TBXark repassar o `instructions`"); núcleo, Worker 3 e Worker 10 (e).

### Prisma-24: Pontos abertos da faixa 6 que o núcleo já fechou
- Onde: faixa 6, Pontos abertos: "Fim de resposta no Claude Code", "Verificador grava sem guarda de versão", "Frontmatter numa troca de trecho".
- Texto atual: os três como "não decidido".
- Texto proposto: "O verificador roda onde o fim de resposta roda (no Claude Code, o mod com `classic.Stop`)"; "o verificador só completa campos deriváveis, por troca de trecho" (escolha do núcleo); "o hook monta o conteúdo proposto (arquivo novo, ou o atual com a troca aplicada) e chama o verificador".
- Fonte: 14, Answer, Fim da resposta; 11, Answer ("Nenhuma gravação sem guarda de versão"); núcleo, Pontos abertos e Worker 6 (b).

### Prisma-25: Detalhes da faixa 7 já no núcleo
- Onde: faixa 7, Pontos abertos "Forma do mod", "Tarefa agendada no ensaio"; Testing decisions ("enquanto o Gustavo não liberar").
- Texto proposto: "Forma do mod" fica aberta (33, R64: "na construção"). Tarefa agendada: "a definição sai como XML e o instalador só com `-WhatIf`; registrar é `ready-for-human`" e marcar "depende do formato".
- Fonte: 33, Answer (tarefa agendada a cada 5 min); núcleo, Worker 7 (e).

## Depende do formato (não decido; o que muda com etapas sequenciais)

- Portas de ensaio (D1, D17: 5986/5987 nas partes contra 5996/5997 no núcleo). Com etapas sequenciais, um CouchDB de
  ensaio só pode servir às faixas 4, 5 e 7, e as portas por faixa deixam de ser necessárias.
- Dono de quem liga o verificador ao fim da resposta (D13: faixas 1, 2 ou 6). Em sequência, a etapa que entrega o mod e
  os hooks de fim liga os dois (checkpoint e verificador) de uma vez.
- Dono da ponte do Desktop (Prisma-17).
- Os "se couber" do núcleo (Prisma-9, Prisma-13): em sequência, cada etapa termina o que o ticket pede antes da próxima.
- Dublês (`estado.json` de exemplo, verificador que sai 0, MCP dublê do proxy): em sequência, a etapa seguinte usa o
  componente real da anterior, e os dublês só ficam onde o real exige a segunda máquina.
