# Divergências — Sextante

Progresso: faixas-01-02.md e faixas-03-04.md concluídas. 174 user stories e decisões de ambas as partes conferidas. 15 divergências, incluindo dúvidas e dependências do formato da execução.

Fontes: seção “Decisions so far” do mapa; núcleo da spec, inclusive os esclarecimentos finais; Answer e Comments dos tickets resolvidos citados. Revisão documental. Nenhum teste ou varredura executado.

### D1: Conteúdo do nível do cliente tratado como decidido
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-01-02.md`, faixa 1, user story 2.
- O spec diz: “com o nível do cliente guardando o que é comum às iniciativas dele”.
- O que vale: ticket resolvido 12, Answer, “Para a construção”: “o que mora no nível `clients/<cliente>/`” permanece aberto. A profundidade está decidida; esse conteúdo não está.
- Tipo: sobra
- Sugestão: manter a profundidade e apresentar o conteúdo do nível do cliente como decisão pendente.

### D2: Criação do núcleo estendida a todas as raízes
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-01-02.md`, faixa 1, Testing decisions, “Script de criação”.
- O spec diz: “para cada raiz, criar uma iniciativa” dá “os seis arquivos do núcleo” e “o `AGENTS.md` da iniciativa”.
- O que vale: ticket resolvido 12, Answer: “se `operations/` e `reference/` levam o núcleo inteiro” está aberto; “Núcleo da iniciativa” distingue os seis arquivos do `AGENTS.md`, descrito como “só o mapa e as regras próprias”. A própria parte deixa aberta a criação automática desse arquivo. Dúvida: “cada raiz” inclui também `agents/` e `inbox/`? Nenhuma decisão citada lhes dá núcleo de iniciativa.
- Tipo: sobra
- Sugestão: limitar o aceite aos destinos de iniciativa decididos e deixar explícitas as escolhas pendentes sobre outras raízes e criação automática do mapa.

### D3: Guarda do verificador ainda aparece em aberto
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-01-02.md`, faixa 1, “Verificador sem IA” e Pontos abertos, “O verificador grava no disco”.
- O spec diz: “como ele confere a versão para não desfazer gravação do sincronizador ou de outro agente”.
- O que vale: ticket resolvido 11, Answer: “Nenhuma gravação sem guarda de versão”; núcleo `spec.md`, Pontos abertos achados ao escrever a spec: “ele só completa campos deriváveis, por troca de trecho”.
- Tipo: desatualizado
- Sugestão: incorporar a troca de trecho com guarda de versão ao comportamento obrigatório do verificador, deixando abertas apenas as escolhas técnicas restantes.

### D4: Teste de segredo exclui o próprio mecanismo de exclusão
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-01-02.md`, faixa 1, Testing decisions, “Segredo aninhado”.
- O spec diz: “um `.secrets/` aninhado fica fora do git do hub de ensaio e da exclusão gerada”.
- O que vale: ticket resolvido 12, Answer: “um `.secrets/` aninhado não chega ao banco nem ao GitHub (exclusão `**/.*` e `**/.*/**`)”. A exclusão precisa abranger o segredo.
- Tipo: contradiz
- Sugestão: exigir que o segredo seja abrangido pela exclusão gerada e fique fora do git, do banco e da busca.

### D5: Campo de iniciativa obrigatório fora de iniciativa
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-01-02.md`, faixa 1, user story 24 e Implementation decisions, campos comuns.
- O spec diz: “toda nota tenha os campos comuns [...] `initiative`”; depois restringe a “`initiative` (dentro de uma iniciativa)”.
- O que vale: ticket resolvido 12, Answer, “Frontmatter por tipo”: “O derivável a máquina preenche (`type`, `initiative` [...])”; a parte aceita a restrição ao contexto de iniciativa, mas a story não a contém. Dúvida: qual valor a story cobraria de notas de referência ou captura sem iniciativa? A forma de `inbox/` ainda consta como aberta no Answer.
- Tipo: sobra
- Sugestão: explicitar na story que `initiative` só é exigido onde o caminho identifica uma iniciativa.

### D6: Devolução obrigatória em toda resposta sem mudança
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-01-02.md`, faixa 2, Testing decisions, “Hook de fim”.
- O spec diz: “com a nota sem mudança desde o início da resposta, devolve”.
- O que vale: ticket resolvido 10, Answer: “quando a nota não reflete a resposta [...] ele faz o agente continuar e gravar”; ticket resolvido 14, Comments de 2026-10-15: o teste provou que “solta [...] quando a nota de retomada muda”. Isso não decide que uma resposta sem efeito no trabalho exija mudar a nota. A própria parte admite essa lacuna.
- Tipo: sobra
- Sugestão: condicionar o aceite a uma resposta que alterou o trabalho e manter pendente o critério para respostas sem alteração.

### D7: Início sem vigia nem MCP promete estado disponível
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-01-02.md`, faixa 2, Testing decisions, “Hook de início”.
- O spec diz: “nos três casos [...] sem os dois), a saída traz o estado do sync”.
- O que vale: ticket resolvido 14, Answer: “no par, o hook lê o arquivo da vigia; sem ele, a ferramenta do MCP”. Não foi decidida uma terceira fonte que informe o estado atual sem ambos. Dúvida: o aceite pretende apenas informar indisponibilidade? O texto exige o estado sem qualificação.
- Tipo: sobra
- Sugestão: exigir aviso de estado indisponível quando faltarem as duas fontes, sem afirmar que o sync foi conferido.

### D8: Fronteiras e dublês dependem da execução anterior
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-01-02.md`, faixas 1 e 2, fragmentos por faixa, fronteiras e Testing decisions.
- O spec diz: “hub de ensaio [...] pronto antes da hora”; “a faixa 8 junta os fragmentos”; “modelo de ensaio até a faixa 7 publicar o formato”.
- O que vale: ticket resolvido 16, Answer: “10 workers e 2 Prumos”, “a execução inteira em 1 hora”; Comments de 2026-10-16: “recomeço” e revisão da spec antes de recomeçar. Conforme a orientação desta revisão, o formato será revisto.
- Tipo: depende do formato da execução
- Sugestão: conservar os contratos necessários entre componentes e rever responsáveis, dublês e sequência quando o novo formato for escolhido.

### D9: Pasta local só é excluída da busca do outro par
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-03-04.md`, faixa 3, user story 12.
- O spec diz: “fique fora da busca da outra máquina”.
- O que vale: ticket resolvido 12, Answer, “Pasta não replicada”: “um script gera a exclusão do sync e da busca a partir desses marcadores”. A exclusão também vale para a busca do par onde a pasta existe; a Implementation decision da própria faixa assim a descreve.
- Tipo: falta
- Sugestão: exigir que a pasta marcada `local: true` fique fora da indexação e dos resultados também no próprio par.

### D10: Exclusão da busca cobre só parte dos nomes com ponto
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-03-04.md`, faixa 3, Implementation decisions, “Exclusões da busca”, e Pontos abertos.
- O spec diz: “`.secrets/` e as pastas com `index.md` `local: true` saem da busca”; deixa em aberto “se precisa da lista de exclusões” para outros caminhos com ponto.
- O que vale: ticket resolvido 12, Answer, “Pasta não replicada”: os marcadores incluem “o que tem ponto no nome (`.git`, `.secrets/`, `.maestri/`, o índice da busca)” e geram exclusão “do sync e da busca”; núcleo `spec.md`, Worker 3: `OBSIDIAN_IGNORE_PATTERNS` com `**/.*/**` e `**/.*`, além dos marcadores locais.
- Tipo: falta
- Sugestão: exigir explicitamente todos os caminhos com ponto na exclusão e no aceite da busca, sem depender de um comportamento implícito ainda não verificado.

### D11: Dono do script de exclusões continua sem definição
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-03-04.md`, faixa 3, Pontos abertos, “Dono do script”; faixa 4, último ponto aberto.
- O spec diz: “o corte em faixas não o atribui. Proposta: faixa 4 gera”; depois “o Prumo sugere a faixa 1”.
- O que vale: ticket resolvido 12, Answer: “um script gera a exclusão do sync e da busca”; núcleo `spec.md`, Worker 3: “mais o que a faixa 1 gerar para `local: true`” e “exclusão de `local: true` (faixa 1): leio a lista gerada”. O núcleo já dá essa responsabilidade à faixa 1.
- Tipo: desatualizado
- Sugestão: alinhar ambas as faixas ao gerador da faixa 1 e deixar pendente apenas sua interface técnica, sujeita à revisão do formato de execução.

### D12: Aceite da busca diverge do núcleo
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-03-04.md`, faixa 3, Testing decisions, “Pelo MCP, por script” e nota nova.
- O spec diz: “nota esperada entre os cinco primeiros”; “o tempo até aparecer é medido”, sem limite de aceite.
- O que vale: ticket resolvido 09, Answer: o tempo de edição até a busca com o CLI ligado é “não verificado” e a Robusta tem gatilho de visibilidade em segundos; núcleo `spec.md`, Worker 3, Como se prova: nota esperada “entre as 3 primeiras” e nota criada no disco aparece “em até 60 s”. Esses limites vêm do núcleo da execução, não de uma nova decisão fechada no ticket 09.
- Tipo: contradiz
- Sugestão: unificar os critérios da parte e do núcleo, explicitando que os limites de três resultados e 60 segundos são critérios de execução propostos, sujeitos à revisão.

### D13: YAML inválido só é observado no teste
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-03-04.md`, faixa 3, user story 20, Testing decisions e Pontos abertos.
- O spec diz: “o teste registra o que acontece [...] e se isso fica visível”; “falta decidir como isso aparece”.
- O que vale: ticket resolvido 09, Answer: “Notas com YAML inválido ficam fora do índice (12 de 124 na bancada)”; núcleo `spec.md`, Worker 3, Como se prova: “`status` mostra indexadas = `.md` válidos, e a lista das recusadas por YAML inválido sai no relatório”. O núcleo já exige uma saída concreta, que atende à story 20.
- Tipo: desatualizado
- Sugestão: tornar a contagem e a lista de recusadas requisitos do aceite, mantendo aberto apenas um eventual aviso adicional durante a operação.

### D14: Duas instâncias do banco ainda aparecem como mera inferência
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-03-04.md`, faixa 4, Pontos abertos, “Duas instâncias do MCP do es617 por par”.
- O spec diz: “inferência, não verificada (34)”.
- O que vale: ticket resolvido 11, Answer, “Cliente”: “recebe o token de uma segunda instância do MCP do banco, com escrita e a mesma guarda de versão”; ticket resolvido 14, Answer: rotas distintas `/banco/mcp` e `/banco-escrita/mcp`; núcleo `spec.md`, Worker 5: “duas instâncias por par”, escrita e `READ_ONLY=true`.
- Tipo: desatualizado
- Sugestão: apresentar as duas instâncias como arquitetura exigida e manter como não verificada apenas a prova operacional que ainda faltar.

### D15: Prazos e cortes do banco dependem da execução anterior
- Onde: `.scratch/construcao-do-hub/spec-partes/faixas-03-04.md`, faixa 3, stories 21 e 22 e costura; faixa 4, story 36, “Compose de ensaio publicado”, Testing decisions e Out of scope.
- O spec diz: “nos primeiros 10 minutos da hora”; “No minuto 15”; “Se sobrar”; “O resto [...] fica para a próxima execução”; “até lá, o MCP do es617 sem fork”.
- O que vale: ticket resolvido 16, Answer: “10 workers e 2 Prumos”, execução em “1 hora”; Comments de 2026-10-16: “depois da revisão do spec, ajustar o plano de construção”, com etapas sequenciais como ideia ainda aberta. Ticket resolvido 33, Answer, mantém como requisitos o limite de 200 MiB, binários recuperáveis e sincronizador como tarefa agendada; os cortes de tempo não revogam essas entregas.
- Tipo: depende do formato da execução
- Sugestão: rever minutos, responsáveis, dublês, uso provisório do MCP sem fork e adiamentos, preservando todos os requisitos decididos como entregas a concluir.

