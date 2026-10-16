# Divergências: revisão do Prisma

Progresso: faixas-05-06.md (feita); faixas-07-08.md (feita); faixas-09-10.md (feita). Revisão pronta: 34 divergências

Fontes: "Decisions so far" do `map.md`, o núcleo `spec.md` (com "Pontos abertos achados ao escrever a spec") e os
tickets resolvidos. Quando a parte contradiz o núcleo, o núcleo é a decisão mais recente, salvo nota.

## faixas-05-06.md

### D1: Porta do banco de ensaio do MCP
- Onde: faixas-05-06.md, faixa 5, "Banco de ensaio" e Testing decisions
- O spec diz: "esta faixa sobe o seu CouchDB descartável em 127.0.0.1, porta 5986"
- O que vale: núcleo, Worker 5: "CouchDB de ensaio só da faixa em 127.0.0.1:5996, com o MCP em 127.0.0.1:8796 (escrita) e 8797 (leitura)"
- Tipo: contradiz (e depende do formato da execução)
- Sugestão: trocar 5986 por 5996 e citar as portas 8796 e 8797 do MCP.

### D2: Escolha entre recusa e conflito gravado já feita
- Onde: faixas-05-06.md, faixa 5, Pontos abertos, "Recusa ou conflito gravado"
- O spec diz: "A construção tem de escolher uma forma ... e o maestro confirma com o Gustavo se a folha concorrente fica no banco."
- O que vale: núcleo, Pontos abertos: "Vale o conflito visível (25, 30), e a resposta ao agente diz 'releia e refaça'"; ticket 25: "a gravação leva `base_rev` e vira conflito se a base mudou"
- Tipo: desatualizado
- Sugestão: tirar dos pontos abertos e escrever nas decisões que fica a folha concorrente no banco e a resposta "conflito: releia e refaça".

### D3: Forma do conflito visível já escolhida
- Onde: faixas-05-06.md, faixa 5, "Conflito visível ao agente" e Pontos abertos, "Forma do conflito visível"; user story 8
- O spec diz: "aviso na leitura ou uma ferramenta que lista os conflitos (a escolha entre as duas é da construção)"
- O que vale: núcleo, Worker 5 (b): "`read_note` de nota em conflito avisa e lista as folhas, e a ferramenta `get_conflicts` lista os conflitos abertos" (as duas). O ticket 30 só dá a alternativa; a escolha veio do núcleo, não de ticket.
- Tipo: desatualizado
- Sugestão: fixar as duas formas e tirar o ponto aberto. Dúvida: a escolha está só no núcleo, não num ticket resolvido.

### D4: Versão de base nas outras ferramentas
- Onde: faixas-05-06.md, faixa 5, Pontos abertos, "Versão de base nas outras ferramentas"
- O spec diz: "se anexar ao fim e ao início e a troca de trecho também levam a versão de base ... Não decidido."
- O que vale: ticket 30 (Answer, esforço): "`write_note`/`edit_note` aceitam `base_rev` e gravam como filha dela"; núcleo, Worker 5 (a): "`write_note` e `edit_note` exigem `base_rev`"
- Tipo: desatualizado
- Sugestão: dizer que `write_note` e `edit_note` exigem `base_rev` e deixar aberto só o anexar ao fim e ao início, se for o caso.

### D5: Instância só de leitura já tem forma
- Onde: faixas-05-06.md, faixa 5, Pontos abertos, "Instância só de leitura"
- O spec diz: "como o fork fica só de leitura (ferramentas de gravação ausentes ou recusadas) não está decidido"
- O que vale: ticket 34: "cada par roda um segundo MCP com `READ_ONLY=true` e token"; núcleo, Worker 5 (e): `READ_ONLY=true` "disable all write tools", "a mesma linha de comando com só essa variável trocada"
- Tipo: desatualizado
- Sugestão: decidir pela variável `READ_ONLY=true` do upstream, com o teste (5) do núcleo (nenhuma ferramenta de gravação listada e gravação recusada).

### D6: Cifra do banco já decidida
- Onde: faixas-05-06.md, faixa 5, Pontos abertos, "Cifra do banco"
- O spec diz: "se o banco for cifrado, a senha da cifra também vai ao MCP ... a decisão sobre cifrar é da faixa 4"
- O que vale: ticket 34, Segurança: "E2EE do LiveSync"; núcleo, Worker 5 (f): "E2EE: a frase-senha do `.env` do banco (`COUCHDB_PASSPHRASE`), ligada depois dos testes sem ela", e o teste (8)
- Tipo: falta
- Sugestão: pôr nas decisões e nas user stories que o MCP decifra com a frase-senha do `.env` e repete os testes de versão com E2EE ligada.

### D7: Ferramenta de estado do hub no MCP
- Onde: faixas-05-06.md, faixa 5, user stories e Implementation decisions (ausente)
- O spec diz: nada sobre a ferramenta de estado da vigia
- O que vale: ticket 14, Checagem de início: "no par, o hook lê o arquivo da vigia; sem ele, a ferramenta do MCP; no cliente, a ferramenta do MCP"; núcleo, Worker 5 (d): "ferramenta `estado_do_hub`: devolve o `estado.json` da vigia"
- Tipo: falta
- Sugestão: acrescentar a user story "como agente sem o arquivo da vigia, ou cliente, quero o estado do hub por uma ferramenta do MCP" e o teste (7) do núcleo.

### D8: Quem atualiza a cabeça do contrato
- Onde: faixas-05-06.md, faixa 5, Out of scope ("a atualização da cabeça do contrato no MCP quando o `AGENTS.md` muda: faixa 10") e Pontos abertos, "De onde vem a cabeça do contrato"
- O spec diz: "texto fixo na configuração do fork ou lido do `AGENTS.md` do hub. Quem a atualiza é lacuna de dono da faixa 10"
- O que vale: núcleo, Worker 5 (c): "o bloco `cabeca:inicio/fim` do `AGENTS.md` lido a cada `initialize`, sem cópia, posto antes do texto do upstream"; núcleo, Worker 10 (d): "a atualização em si é o fork relendo o bloco"; a faixa 10 só confere o tamanho (`conferir-cabeca`). Lacuna de dono aberta no ticket 16 (comentário de 2026-10-15).
- Tipo: desatualizado
- Sugestão: a faixa 5 lê o bloco a cada `initialize` e o teste (6) do núcleo prova a troca; tirar do fora do escopo e do ponto aberto. Dúvida: a solução está só no núcleo, não em ticket resolvido.

### D9: Ordem da cabeça no `instructions`
- Onde: faixas-05-06.md, faixa 5, user story 13 e "Contrato pelo MCP"
- O spec diz: "o `instructions` do fork leva a cabeça do `AGENTS.md`, autossuficiente, de até 2.000 caracteres"
- O que vale: núcleo, Worker 5 (c): "posto antes do texto do upstream para sobreviver ao corte do Claude Code"
- Tipo: falta
- Sugestão: dizer na decisão que a cabeça vem antes do texto do upstream.

### D10: Texto da regra curta nas descrições
- Onde: faixas-05-06.md, faixa 5, user story 15 e "Contrato pelo MCP"
- O spec diz: a descrição de cada ferramenta de gravação diz "antes de gravar, leia `AGENTS.md`"
- O que vale: ticket 36 (R33): "a descrição de cada ferramenta de gravação diz 'antes de gravar, leia `AGENTS.md`'" (a parte está certa); o núcleo, Worker 5 (c), põe outro texto: "leia antes, grave com a `base_rev` lida; conflito = releia e refaça", em `write_note`, `edit_note`, `delete_note` e `move_note`
- Tipo: contradiz (entre o núcleo e o ticket 36)
- Sugestão: juntar as duas frases na regra curta e listar as quatro ferramentas na parte; ou corrigir o núcleo. Dúvida: qual texto vale.

### D11: Ponte do Claude Desktop em outra faixa
- Onde: faixas-05-06.md, faixa 5, Out of scope
- O spec diz: "A linha de MCP em cada harness, a ponte `mcp-remote` do Claude Desktop e a aprovação de antemão no Codex: faixa 8."
- O que vale: núcleo, Worker 10 (f): "se couber: as linhas da ponte `mcp-remote` do Claude Desktop para a busca e para o banco com escrita (ticket 11), geradas e não instaladas"
- Tipo: contradiz
- Sugestão: mandar a ponte do Desktop para a faixa 10.

### D12: Validação de frontmatter no MCP é "se couber"
- Onde: faixas-05-06.md, faixa 5, user stories 10 a 12 e Testing decisions ("Frontmatter: nota fora do esquema ... é recusada")
- O spec diz: a validação como entrega plena, com teste de aceite
- O que vale: ticket 12, Imposição: "o MCP do banco valida igual" (decidido; marcado "versão modificada", não verificado); núcleo, Worker 5 (g): "se couber: a gravação chama o verificador de frontmatter"
- Tipo: depende do formato da execução
- Sugestão: com o formato revisto, decidir se a validação no MCP é entrega cheia (como o ticket 12 pede) e alinhar núcleo e parte.

### D13: Verificador de fim de resposta como entrega da faixa 6
- Onde: faixas-05-06.md, faixa 6, abertura, user stories 18 a 23 e "Frontmatter imposto por mecanismo" ("esta faixa os liga aos eventos de antes da gravação e de fim de resposta")
- O spec diz: a faixa 6 liga o verificador sem IA ao fim de cada resposta
- O que vale: núcleo, Worker 6: só (a) a (d), a recusa antes da ferramenta e o aviso de leitura, sem fim de resposta; núcleo, Pontos abertos: "O verificador de frontmatter é da faixa 1; a faixa 6 só o chama" e "o verificador roda onde o fim de resposta roda em cada harness"
- Tipo: sobra (frente ao núcleo)
- Sugestão: dizer quem liga o verificador ao fim da resposta (faixa 1, faixa 2 ou faixa 6) e tirar as user stories 18 a 23 da faixa 6 se não for ela. Dúvida: o núcleo não nomeia o dono.

### D14: Ponto do fim de resposta no Claude Code já resolvido
- Onde: faixas-05-06.md, faixa 6, Pontos abertos, "Fim de resposta no Claude Code"
- O spec diz: "o ticket 12 fala do `Stop`; o ticket 14 escolheu o mod com o `Stop` clássico. Combinar com a faixa 2 um ponto só."
- O que vale: núcleo, Pontos abertos: "o verificador roda onde o fim de resposta roda em cada harness"; ticket 14: "Claude Code pelo mod (`turn.start` com `classic.Stop`)"
- Tipo: desatualizado
- Sugestão: tirar o ponto aberto e dizer que o verificador entra no mod do Claude Code.

### D15: Verificador grava sem guarda de versão
- Onde: faixas-05-06.md, faixa 6, Pontos abertos, "Verificador grava sem guarda de versão"
- O spec diz: "Como isso cumpre 'nenhuma gravação sem guarda de versão' não está decidido."
- O que vale: núcleo, Pontos abertos: "O verificador grava no disco sem guarda de versão: ele só completa campos deriváveis, por troca de trecho."
- Tipo: desatualizado
- Sugestão: trocar o ponto aberto por essa decisão. Dúvida: a decisão está só no núcleo, não em ticket resolvido.

### D16: Frontmatter numa troca de trecho
- Onde: faixas-05-06.md, faixa 6, Pontos abertos, "Frontmatter numa troca de trecho"
- O spec diz: "validar o resultado pede montar o conteúdo final. Não decidido nem testado."
- O que vale: núcleo, Worker 6 (b): "monta o conteúdo proposto (arquivo novo, ou o atual com a troca aplicada) e chama o verificador da faixa 1"
- Tipo: desatualizado
- Sugestão: escrever a decisão do núcleo e deixar aberto só o teste.

## faixas-07-08.md

### D17: Porta do CouchDB de ensaio da vigia
- Onde: faixas-07-08.md, faixa 7, Testing decisions, "Costura"
- O spec diz: "CouchDB descartável da faixa em porta própria (proposta do plano: 5987)"
- O que vale: núcleo, Worker 7: "Ponta a ponta no CouchDB de ensaio (porta 5997, com E2EE)"
- Tipo: contradiz (e depende do formato da execução)
- Sugestão: trocar 5987 por 5997.

### D18: Vigia decifra o caminho com E2EE
- Onde: faixas-07-08.md, faixa 7, user stories 7 a 12 e Testing decisions (ausente)
- O spec diz: nada sobre o banco cifrado
- O que vale: ticket 34, Segurança: "E2EE do LiveSync"; núcleo, Worker 7 (a): "com E2EE, decifra o caminho com a frase-senha do `.env`", e a vigia "acusa o conflito e o binário pelo caminho decifrado"
- Tipo: falta
- Sugestão: acrescentar que a vigia lê o banco cifrado e cita a nota pelo caminho decifrado, com o teste no CouchDB de ensaio com E2EE.

### D19: Arquivo de estado já fixado
- Onde: faixas-07-08.md, faixa 7, "Arquivo de estado" e Pontos abertos, "Arquivo de estado"
- O spec diz: "lugar e esquema estão só como proposta do Worker 8 no plano; o dono desta faixa confirma"
- O que vale: núcleo, Worker 7: "Estado em `C:\context-hub\.local\vigia\estado.json` (fora do banco e do `.git`), com `nivel` por item e o do topo igual ao pior", gravado por troca atômica
- Tipo: desatualizado
- Sugestão: escrever o caminho e o esquema do núcleo e tirar o ponto aberto. Dúvida: está só no núcleo, não em ticket.

### D20: Item da cópia diária no estado da vigia
- Onde: faixas-07-08.md, faixa 7, user stories e Testing decisions, "Casos da vigia" (ausente)
- O spec diz: nada sobre a cópia diária
- O que vale: núcleo, Worker 7: oitavo cenário "item `copia-diaria` da faixa 10 (`informa`, com notificação)"; núcleo, Worker 10 (c): a cópia "falha alto (saída ≠ 0 e item `copia-diaria` no estado da vigia)". O ticket 33 decide a cópia diária, mas não diz como a falha dela aparece.
- Tipo: falta (frente ao núcleo)
- Sugestão: acrescentar a user story e o caso de teste, ou tirar do núcleo. Dúvida: o aviso da falha da cópia não está em ticket resolvido.

### D21: Config Doctor é "se couber"
- Onde: faixas-07-08.md, faixa 7, user story 15 e "Vigia" (lê "se o Config Doctor travou o plugin")
- O spec diz: o Config Doctor como leitura plena da vigia
- O que vale: ticket 33, Aviso: a vigia lê "se o Config Doctor travou o plugin" (decidido); núcleo, Worker 7 (f): "se couber: Config Doctor travando o plugin"
- Tipo: depende do formato da execução
- Sugestão: com o formato revisto, manter o Config Doctor como entrega cheia, como o ticket 33 pede.

### D22: Tarefa agendada no ensaio
- Onde: faixas-07-08.md, faixa 7, Pontos abertos, "Tarefa agendada no ensaio", e Testing decisions ("enquanto o Gustavo não liberar")
- O spec diz: "pergunta do plano ao Gustavo (CouchDB e tarefa de ensaio contam como serviço?)"
- O que vale: núcleo, Worker 7 (e): "a tarefa agendada de 5 min como XML e `kit/par/07-vigia.ps1` só com `-WhatIf` (registrar é `ready-for-human`); na hora, a vigia roda em laço no terminal"
- Tipo: depende do formato da execução
- Sugestão: escrever a forma do núcleo e tirar a pergunta, ou levá-la à revisão do formato.

### D23: Detectores que o núcleo já desenhou
- Onde: faixas-07-08.md, faixa 7, Pontos abertos, "Detectores sem mecanismo decidido"
- O spec diz: "como a vigia sabe que a outra máquina está ligada na tailnet; como acha os ramos apagados de binário"
- O que vale: núcleo, Worker 7 (a): "se o outro par responde" (por `HUB_OUTRO_PAR_URL`) e "ramo apagado de binário pela resolução por `mtime`" lido do CouchDB local; ticket 48: colisão de binário "recuperável por script"
- Tipo: desatualizado
- Sugestão: deixar aberto só o Config Doctor e escrever os outros dois como no núcleo.

### D24: GSD no arquivo global do Copilot já decidido
- Onde: faixas-07-08.md, faixa 8, Pontos abertos, "Contradições achadas", GSD; user story 11
- O spec diz: "decidir antes do ticket de construção": o kit junta os dois ou o GSD sai
- O que vale: núcleo, Pontos abertos: "o 15 tira o GSD do escopo global. Vale o 15"; ticket 15, rodada 2: "o kit tira o GSD do escopo global, com cópia antes"
- Tipo: desatualizado
- Sugestão: dizer que vale o 15 e reescrever a user story 11 como "o kit tira o GSD do arquivo global, com cópia".

### D25: Ponte do Claude Desktop na faixa 8
- Onde: faixas-07-08.md, faixa 8, user story 37 e "Claude Desktop"
- O spec diz: o kit de par liga a "ponte `mcp-remote` (MCP stdio) para o MCP do banco e para a busca"
- O que vale: núcleo, Worker 10 (f): "se couber: as linhas da ponte `mcp-remote` do Claude Desktop para a busca e para o banco com escrita (ticket 11), geradas e não instaladas"; o núcleo do Worker 8 não cita o Desktop
- Tipo: contradiz
- Sugestão: mandar a ponte do Desktop para a faixa 10 e dizer que é "com escrita"; deixar na faixa 8 só a pasta conectada, se for dela.

### D26: Duas camadas de skills
- Onde: faixas-07-08.md, faixa 8, user stories 15 a 17 e "Skills"
- O spec diz: "cada skill em `agents/skills/<skill>/`, com duas junctions, em `~/.claude/skills` e em `~/.agents/skills`"
- O que vale: ticket 15, rodada 2: "A junction global leva só as skills de uso geral ...; as de um papel ficam no acervo e entram só na pasta daquele papel, pela receita de setup"
- Tipo: falta
- Sugestão: dizer que a junction global liga só as skills de uso geral e acrescentar o teste de que uma skill de papel não aparece fora da pasta do papel.

## faixas-09-10.md

### D27: Guarda do acervo cobrindo as propostas
- Onde: faixas-09-10.md, faixa 9, Pontos abertos, "Que pastas a guarda cobre"
- O spec diz: a parte deixa aberto e avisa que "a linha do Worker 9 no plano põe `agents/maestro/**` inteiro sob a guarda, o que recusaria as propostas"
- O que vale: ticket 40, Guarda: "Codex e Copilot não gravam no acervo e deixam propostas em `agents/maestro/propostas/`"; ticket 40, Quem usa: `agents/maestro/uso/<máquina>.md` "gravado por hook". O núcleo, Worker 9, repete o erro: "gravar em `agents/skills/**` ou `agents/maestro/**` pede aval"
- Tipo: contradiz (o núcleo frente ao ticket 40)
- Sugestão: no núcleo e na parte, tirar `agents/maestro/propostas/` e `agents/maestro/uso/` da guarda.

### D28: Decisões vindas de ticket não resolvido
- Onde: faixas-09-10.md, faixa 10, user stories 5 a 7, 13 a 15 e 37; "Prazo de 30 dias" e "Cópia de segurança diária" (citam as rodadas 7 e 8 do 56)
- O spec diz: "Prazo de 30 dias (56, rodada 7)"; "Nenhuma iniciativa de cliente é vetada no repositório (56, rodada 7)"; "dois dias de distância bastam (56, rodada 8)"
- O que vale: o ticket 56, "Laço do system design", está com `Status: claimed`, não resolvido. Pela regra do papel, essas respostas do Gustavo ainda não são decisão fechada. O ticket 16 (resolvido) só traz os 30 dias como lacuna de dono: "quem confere os 30 dias do `_archive/` e apaga"
- Tipo: falta (dúvida: a decisão existe, mas num ticket aberto)
- Sugestão: resolver o ticket 56, ou registrar essas respostas num ticket resolvido, antes de construir; até lá, marcar essas user stories como vindas de rodada respondida em ticket aberto.

### D29: Data no nome da pasta arquivada
- Onde: faixas-09-10.md, faixa 10, Pontos abertos, "Como o `_archive/` guarda a data"
- O spec diz: "o plano propõe a data no nome da pasta; não decidido"
- O que vale: núcleo, Worker 10 (a): "move para o `_archive/` da própria raiz como `_archive/<AAAA-MM-DD>--<nome>/` (a data viaja no nome, sem arquivo com ponto)"
- Tipo: desatualizado
- Sugestão: escrever a forma do núcleo e tirar o ponto aberto.

### D30: Lacunas de dono 4 e 5 já com dono no núcleo
- Onde: faixas-09-10.md, faixa 10, Pontos abertos, "Lacuna de dono 4" e "Lacuna de dono 5"
- O spec diz: "o plano propõe tarefa diária; não decidido" e "o plano propõe o fork reler a cabeça a cada `initialize`, sem cópia; não decidido"
- O que vale: núcleo, Worker 10 (b) e (g): `limpar-arquivo` apaga o que passou de 30 dias, na tarefa diária "(cópia + limpeza + cabeça)"; núcleo, Worker 10 (d): "a atualização em si é o fork relendo o bloco"; núcleo, Worker 5 (c): o bloco lido "a cada `initialize`, sem cópia"
- Tipo: desatualizado
- Sugestão: escrever os dois donos como no núcleo. Dúvida: o dono está só no núcleo; o ticket 16 deixou as lacunas abertas.

### D31: Falha da cópia diária
- Onde: faixas-09-10.md, faixa 10, Pontos abertos, "Quem percebe a falha da cópia diária"
- O spec diz: "uma decisão só (vigia parada, hook calado, cópia diária, Tailscale bloqueado), a levar ao Gustavo depois das rodadas abertas (56)"
- O que vale: núcleo, Worker 10 (c): "falha alto (saída ≠ 0 e item `copia-diaria` no estado da vigia)"; a própria parte, Fronteira: "a falha da cópia diária entra no estado da vigia (faixa 7)". Nenhum ticket resolvido decide isso (ver D20).
- Tipo: contradiz (dentro da parte e frente ao núcleo)
- Sugestão: escolher a forma do núcleo ou levar a pergunta ao Gustavo; não deixar as duas.

### D32: Ponte do Claude Desktop sem faixa
- Onde: faixas-09-10.md, faixa 10, Out of scope, "O Claude Desktop ... não tem faixa dona no corte"
- O spec diz: o Desktop fica fora da faixa 10 e sem dono
- O que vale: núcleo, Worker 10 (f): "se couber: as linhas da ponte `mcp-remote` do Claude Desktop para a busca e para o banco com escrita (ticket 11), geradas e não instaladas". A faixa 5 manda a ponte para a faixa 8 (D11), e a faixa 8 a assume (D25).
- Tipo: contradiz
- Sugestão: um dono só para a ponte do Desktop em todas as partes (o núcleo diz faixa 10).

### D33: Quantas instâncias do MCP do banco por par
- Onde: faixas-09-10.md, faixa 10, Pontos abertos, "Duas instâncias do es617 por par ... podem ser três por par"
- O spec diz: "com a local em 127.0.0.1, podem ser três por par"
- O que vale: núcleo, Worker 5 (e): "duas instâncias por par, em 127.0.0.1, cada uma com o seu token": escrita e `READ_ONLY=true`; o proxy dá um token por rota (ticket 14, rodada 7), então `/banco-escrita/mcp` pode apontar para a instância de escrita do par
- Tipo: desatualizado
- Sugestão: dizer que são duas instâncias e que a rota de escrita do cliente usa a de escrita do par, com o token da rota no proxy. Dúvida: o ticket 11 fala de "segunda instância" com escrita e token próprio, o que pode ser lido como uma terceira.

### D34: `--allowed-host` da busca atrás do proxy
- Onde: faixas-09-10.md, faixa 10, "Proxy de MCP no par" e Testing decisions (ausente)
- O spec diz: nada sobre o `Host` que a busca aceita
- O que vale: núcleo, Worker 10 (e): "a porta do proxy vai no `.env` do kit e a faixa 3 a usa no `--allowed-host`"; núcleo, Worker 3: "não verificado se o TBXark/mcp-proxy repassa o `Host` do cliente"
- Tipo: falta
- Sugestão: acrescentar a porta do proxy no `.env` do kit e o teste de que a busca responde pelo proxy.
