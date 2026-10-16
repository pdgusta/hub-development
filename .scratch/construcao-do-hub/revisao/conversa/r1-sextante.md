# Rodada 1 — Sextante

Tickets lidos por inteiro: 01, 02, 03, 04, 09, 10, 12, 19, 20, 21, 35, 49, 50, 54. Mapa, proposta inteira e insumos lidos. Arquivos dos colegas da rodada 1 lidos. Votos sobre as propostas deles ficam para a rodada 2.

Caminhos abaixo são relativos a `proposta/`. As referências S1 a S15 identificam meu relatório anterior. O protocolo novo substitui a premissa anterior de que o núcleo, sozinho, decide.

## Mudanças propostas

### Sextante-1: Retificar a divergência sobre o nível do cliente
- Onde: `spec-partes/faixas-01-02.md`, faixa 1, story 2 e ponto aberto sobre `clients/<cliente>/`.
- Texto atual: “com o nível do cliente guardando o que é comum às iniciativas dele”; ponto aberto “o que mora no nível `clients/<cliente>/`”.
- Texto proposto: manter a story 2. Esclarecer o ponto aberto: “A função do nível do cliente é guardar o comum às iniciativas. A lista concreta de conteúdos e seu padrão permanecem abertos.” Minha S1 anterior não sustenta retirar essa função da story.
- Fonte: ticket 12, Comments, resposta à R18 (rodada 6): “com o nível do cliente guardando o que é comum às iniciativas dele”; comentário de 2026-10-12: “a R18 sai de revisão”. O Answer deixa aberto “o que mora no nível”, sem revogar aquela função. A leitura integral distingue função decidida e detalhamento aberto.

### Sextante-2: Limitar o teste do núcleo às iniciativas
- Onde: `spec-partes/faixas-01-02.md`, faixa 1, Testing decisions, “Script de criação”.
- Texto atual: “para cada raiz, criar uma iniciativa” dá os seis arquivos e o `AGENTS.md`.
- Texto proposto: “Criar iniciativa em `clients/<cliente>/<iniciativa>/` e `initiatives/<iniciativa>/` produz os seis arquivos do núcleo e os blocos escolhidos. Não estender esse molde a `agents/` ou `inbox/`. Se `operations/` e `reference/` levam o núcleo inteiro permanece aberto. O `AGENTS.md` da iniciativa guarda só mapa e regras próprias; sua criação automática pelo script fica como escolha proposta, se mantida.”
- Fonte: ticket 12, Answer, “Núcleo da iniciativa”; “Para a construção”: “se `operations/` e `reference/` levam o núcleo inteiro”. Comments, rodada 11, aprova o núcleo e separa o mapa. Mantém a parte principal da S2; não transforma a separação do mapa em proibição de criá-lo.

### Sextante-3: Explicitar a pendência do campo de iniciativa fora de iniciativa
- Onde: `spec-partes/faixas-01-02.md`, faixa 1, story 24 e campos comuns.
- Texto atual: story exige `initiative` em “toda nota”; decisão restringe a “dentro de uma iniciativa”.
- Texto proposto: “Campos comuns conforme o catálogo aceito. A condição de obrigatoriedade e o valor de `initiative` em notas fora de iniciativa precisam ser explicitados no esquema. Restringir o campo a caminhos que identificam iniciativa é proposta de esclarecimento, não nova decisão fechada.”
- Fonte: ticket 12, Answer, lista `initiative` entre os comuns e manda derivá-lo pelo caminho; deixa a forma de `inbox/` aberta. Não encontrei nos Comments uma regra geral que resolva referências e capturas sem iniciativa. Minha S5 continua como dúvida; não proponho decidir o esquema nesta conversa.

### Sextante-4: Verificador também preserva gravação concorrente
- Onde: `spec.md`, Pontos abertos, “O verificador grava no disco sem guarda de versão”; `spec-partes/faixas-01-02.md`, faixa 1, Verificador e Pontos abertos; `faixas-05-06.md`, faixa 6, mesmo ponto.
- Texto atual: núcleo: “ele só completa campos deriváveis, por troca de trecho”; a parte pergunta como confere a versão.
- Texto proposto: “O verificador não tem exceção à garantia de preservar mudanças concorrentes. Completar campos deriváveis por troca de trecho é [escolha do núcleo]. A implementação deve conferir a base/trecho atual e recusar ou refazer ao detectar mudança concorrente. Só preencher campo derivável não dispensa essa guarda. A conferência e correção de links e índices também respeita a garantia.”
- Fonte: ticket 11, Answer: “Nenhuma gravação sem guarda de versão”; ticket 12 exige o verificador mecânico, sem abrir exceção à concorrência. O núcleo não é ticket e não pode dispensar garantia. Retifico a classificação da S3: incorporar troca de trecho é proposta do núcleo; a pendência técnica da guarda não desaparece só por isso.

### Sextante-5: Corrigir o teste de segredo aninhado
- Onde: `spec-partes/faixas-01-02.md`, faixa 1, Testing decisions, “Segredo aninhado”.
- Texto atual: segredo “fica fora do git do hub de ensaio e da exclusão gerada”.
- Texto proposto: “O `.secrets/` aninhado é abrangido pela exclusão gerada e não chega ao banco nem ao GitHub; também não aparece na busca.”
- Fonte: ticket 12, Comments, rodada 14 e Answer: “Antes de guardar o primeiro segredo, um teste tem de provar que um `.secrets/` aninhado não chega ao banco nem ao GitHub”; exclusões `**/.*` e `**/.*/**`. S4 confirmada.

### Sextante-6: Não confundir nota sem mudança com nota insuficiente
- Onde: `spec-partes/faixas-01-02.md`, faixa 2, Testing decisions, “Hook de fim”, e Pontos abertos.
- Texto atual: “com a nota sem mudança desde o início da resposta, devolve”.
- Texto proposto: “Num caso em que o trabalho mudou e a nota não o reflete, o checkpoint devolve para atualizar; depois da atualização, solta. Respostas sem mudança no trabalho e prevenção de laço permanecem pendentes. Ver apenas se o arquivo mudou é um critério mecânico proposto, não a definição decidida de suficiência.”
- Fonte: ticket 10, Answer: “quando a nota não reflete a resposta, ou a memória privada ganhou algo que o hub não tem”; ticket 14 provou que solta quando a nota muda, sem decidir o contrário universal. S6 confirmada.

### Sextante-7: Distinguir ausência de revisão pós-sessão de proibição de IA
- Onde: `spec-partes/faixas-01-02.md`, faixa 2, story 14 e “Checkpoint de fim de resposta”.
- Texto atual: “checkpoint não use IA nem o FreeLLMAPI”; “Sem modelo: o 10 tirou a revisão por IA”.
- Texto proposto: “Sem revisão pós-sessão nem FreeLLMAPI no checkpoint (10). Checkpoint sem IA: [escolha do núcleo], se mantida. O verificador de frontmatter continua sem IA por decisão própria do 12. Não apresentar a exclusão da revisão pós-sessão como proibição geral de IA em qualquer hook.”
- Fonte: ticket 10, Comments de 2026-10-04: “não concordo com revisão pós-sessão muito menos com ela sendo pelo freellmapi”; Answer exclui esses dois itens, não toda IA. Ticket 12 decide verificador sem IA. Peço ao Quadrante confirmar se há no 14 uma decisão adicional explícita sobre isso; o Answer do 14 descreve canais, não essa proibição.

### Sextante-8: Informar indisponibilidade quando faltam as duas fontes do início
- Onde: `spec-partes/faixas-01-02.md`, faixa 2, Testing decisions, “Hook de início”; faixa 7, teste correspondente.
- Texto atual: “sem os dois), a saída traz o estado do sync”.
- Texto proposto: “Com a vigia, lê seu estado. Sem ela, usa o MCP. Sem ambos, informa estado indisponível; não afirma que o sync foi conferido. A nota local de retomada pode continuar sendo aberta.” Marcar o terceiro caso como esclarecimento proposto quando sua única base for o comportamento da bancada.
- Fonte: ticket 14, Answer, checagem de início: arquivo da vigia, MCP como reserva. Não há terceira fonte. Quadrante Q-4 informa que a bancada aceita devolveu DESCONHECIDO. S7 confirmada; ausência de fonte não pode virar estado saudável.

### Sextante-9: Corrigir o canal global do Claude Code na faixa de retomada
- Onde: `spec-partes/faixas-01-02.md`, faixa 2, “Regra no contrato global”.
- Texto atual: `AGENTS.md` “ligado por link simbólico ao arquivo global de cada um”.
- Texto proposto: “O contrato entra por import no `~/.claude/CLAUDE.md` do Claude Code e por link simbólico nos arquivos globais do Codex e do Copilot.”
- Fonte: Quadrante r1, conferência dos tickets 36 R28 e 42: import no Claude Code, link simbólico nos outros. A faixa 8 e o núcleo já descrevem isso. É correção de redação da faixa 2, não mudança no canal decidido.

### Sextante-10: Excluir pasta local também da busca do próprio par
- Onde: `spec-partes/faixas-03-04.md`, faixa 3, story 12.
- Texto atual: `local: true` fica “fora da busca da outra máquina”.
- Texto proposto: “Pasta marcada `local: true` fica fora da indexação e dos resultados da busca do próprio par, pela exclusão gerada; tampouco replica ao outro par.”
- Fonte: ticket 12, Comments, rodada 17: marcador “que o sync e a busca respeitam”; Answer: exclusão “do sync e da busca”. Não há exceção para indexação local. S9 confirmada.

### Sextante-11: Cobrir todos os caminhos com ponto nas exclusões da busca
- Onde: `spec-partes/faixas-03-04.md`, faixa 3, “Exclusões da busca”, testes e Pontos abertos.
- Texto atual: exige `.secrets/` e `local: true`; deixa em aberto se a ferramenta ignora sozinha outros nomes com ponto.
- Texto proposto: “A exclusão cobre arquivos e pastas com ponto em qualquer nível, mais os marcadores locais. O aceite exige que nenhum deles apareça. O uso de `OBSIDIAN_IGNORE_PATTERNS` com `**/.*` e `**/.*/**` é a solução proposta pelo núcleo; verificar sua eficácia, sem depender de um comportamento implícito.”
- Fonte: ticket 12, Answer, “Pasta não replicada”; ticket 09, Comments, R90: a exclusão precisa cobrir “arquivos, não só pastas”. S10 confirmada, com a distinção entre requisito e mecanismo.

### Sextante-12: Dono do gerador de exclusões é formato
- Onde: `spec-partes/faixas-03-04.md`, faixas 3 e 4, pontos abertos sobre o dono; núcleo, Worker 3.
- Texto atual: faixa 3 propõe faixa 4; faixa 4 sugere faixa 1; núcleo atribui à faixa 1.
- Texto proposto: “Um gerador único produz as exclusões a partir dos marcadores. Busca e sincronizador consomem o resultado. Responsável e interface por faixa: [depende do formato]. A faixa 1 é a atribuição do plano anterior, não decisão sobre o hub.”
- Fonte: ticket 12 decide o gerador, sem atribuir worker. Protocolo veda decidir donos de execução. Retifico S11: não é correção mecânica que imponha a faixa 1.

### Sextante-13: Marcar os limites de aceite da busca como escolha do núcleo
- Onde: `spec.md`, Worker 3, Como se prova; `spec-partes/faixas-03-04.md`, faixa 3, Testing decisions.
- Texto atual: núcleo exige três primeiros e até 60 s; parte exige cinco primeiros e só mede o tempo.
- Texto proposto: “Proposta de aceite [escolha do núcleo]: nota esperada entre as três primeiras e nota nova visível em até 60 s. A bancada anterior mediu hit@5/MRR; não definiu esses limites de produto. Aplicar o mesmo critério no núcleo e na parte após aval, preservando o gatilho da Robusta decidido no 09.”
- Fonte: ticket 09, Comments, R91: “mede acerto nos 5 primeiros e posição”; Answer: tempo com CLI ligado não verificado e Robusta volta se precisar mostrar gravação em segundos. S12 continua como inconsistência; nenhum número do núcleo vira decisão fechada.

### Sextante-14: Relatório de YAML inválido é proposta concreta de observabilidade
- Onde: `spec-partes/faixas-03-04.md`, faixa 3, story 20, Testing decisions e ponto aberto sobre YAML.
- Texto atual: teste só “registra o que acontece [...] e se isso fica visível”; núcleo exige contagem de válidos e lista de recusadas.
- Texto proposto: “O teste exige a contagem de `.md` válidos indexados e um relatório das notas recusadas por YAML inválido [escolha do núcleo]. Eventual aviso operacional adicional permanece aberto.”
- Fonte: ticket 09, Answer: “Notas com YAML inválido ficam fora do índice”; ticket 12 exige YAML válido por imposição mecânica. Nenhum deles escolhe esse relatório. Retifico S13: não é decisão fechada só porque consta do núcleo.

### Sextante-15: Encerrar a dúvida de formatos de texto da busca já conferida
- Onde: `spec-partes/faixas-03-04.md`, faixa 3, Pontos abertos, “Contradição a fechar”.
- Texto atual: 09 não verificou `.txt` e `.csv`; 12 afirma só `.md`; “Conferir na construção”.
- Texto proposto: “A versão 0.16.2 só indexa `.md`, conferido no ticket 12; conteúdo dos outros formatos precisa da vista textual em Markdown. O teste da construção confirma a configuração instalada, sem reabrir a dúvida factual anterior.”
- Fonte: ticket 12, Comments, rodada 16, fonte do pacote `indexer.js` e `db.js`: “só indexa `.md`”; posterior à lacuna do 09. Answer do 12 repete a restrição.

### Sextante-16: Contagem exata de instâncias do MCP como solução proposta
- Onde: `spec-partes/faixas-03-04.md`, faixa 4, ponto aberto “Duas instâncias”; `faixas-09-10.md`, faixa 10; núcleo, Worker 5.
- Texto atual: inferência não verificada no 34; parte 10 permite três; núcleo fixa duas.
- Texto proposto: “Leitura por padrão e escrita ligável com guarda e credenciais separadas são requisitos. Duas instâncias locais, reutilizando a de escrita do par atrás do proxy, é [escolha do núcleo], compatível com os requisitos; a prova operacional permanece não verificada. Não chamar a contagem exata de decisão explícita enquanto a leitura dos tickets não a demonstrar.”
- Fonte: ticket 34 chama duas instâncias de “inferência, não verificado”; ticket 11 fala de segunda instância com escrita; 14 decide rotas/tokens. Prisma-22 também registra a ambiguidade. Retifico S14: retirar a incerteza operacional ou impor duas por mera precedência do núcleo não cabe no protocolo novo.

### Sextante-17: Separar requisitos do corte de tempo e de responsáveis
- Onde: núcleo, Solution, Further Notes, blocos de workers; partes 01-02 e 03-04, fronteiras, dublês, minutos, cortes e adiamentos.
- Texto atual: execução de uma hora, componentes publicados no minuto N, “se sobrar”, “até lá” com componente provisório.
- Texto proposto: marcar [depende do formato] em prazo, paralelismo, donos, portas por faixa, dublês e adiamentos. Os requisitos decididos continuam obrigatórios, inclusive validação de frontmatter no MCP, Config Doctor e caminhos do Desktop. Se houver etapas sequenciais, usar componentes reais já entregues; não escolher a ordem das etapas nesta revisão.
- Fonte: ticket 16, Comments de 2026-10-16: plano será ajustado depois; protocolo veda decidir formato. Tickets 12, 33 e 11 decidem os requisitos. S8 e S15 confirmadas; mantê-las como dependências, sem impor outro plano.

## Cobertura e precedência dos meus tickets

- 12 prevalece sobre recomendações do 35: seis raízes em inglês, tudo replica salvo marcadores, perfil por máquina replicado, cartões também em pastas que crescem com só Markdown.
- 09 e 54 prevalecem sobre rankings/propostas de 19, 20, 21 e 50: OHS com arctic local; gemini configurado, testado uma vez e desligado; Robusta reserva com gatilhos; rerankers fora, Radar.
- 09 confirma MCP TypeScript/Node >=22. A suposição Python do Answer do 50 não escolhe a stack. Peças Python exigem processo separado, se forem escolhidas.
- 49, último Comment, e 50, método revisto: pesquisa sem perfil auto:pesquisa e sem função web_search. Não transformar a preparação histórica do gateway em requisito novo da construção.
- 02: copiar só o conteúdo escolhido, trabalhar só no hub, sem modificar vault; SOC STRATA fora por ora. Não promovo conteúdo sozinho.
- 04: NTFS e Windows nas duas máquinas, caminho no perfil. WSL foi admitido como possibilidade de pesquisa no 09, não escolhido para substituir a implantação final.

Nenhum teste ou varredura executado. Nenhuma edição na proposta, nos tickets, no mapa ou nos insumos antigos.
