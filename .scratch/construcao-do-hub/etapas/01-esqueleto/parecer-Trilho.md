# Parecer — Trilho — ticket 04

Data: 2026-10-16. Revisor: Fiel. Rodada 1.
Veredito: **volta**.

## Escopo e fontes

Ramo ticket-04, worktree C:/context-hub-wt/ticket-04, HEAD 84aa46a.
Fontes: regras; brief de 01-esqueleto; ticket de construção 04; spec (Worker 1);
spec-partes/faixas-01-02.md (faixa 1); tickets resolvidos 12 e 36.
Não cobre implementação dos tickets 05 e 06.

## Evidências conferidas

- git status --short --branch: apenas ## ticket-04. Ramo correto e limpo.
- git merge-base --is-ancestor integracao HEAD: código 0.
- node --test "agents/test/*.test.mjs": 8 testes, 8 passaram, 0 falhas.
- node agents/bin/verificar-hub.mjs C:/context-hub-ensaio: código 0, saída vazia.
- Hub entregue com .git próprio, seis raízes e _archive, duas iniciativas, núcleo de seis arquivos,
  notas em português e PNG pequeno. Conferidos no código, arquivos do hub e testes.
- Cabeça do AGENTS.md: 1.604 caracteres, abaixo de 2.000.
- agents/blocks.md corresponde à tabela final da rodada 15 do ticket 12.
- Relatório indicado contém apenas a entrada inicial "Em construção".

## Consertos necessários

1. **Concluir o relatório.** etapas/01-esqueleto/relatorio.md só contém título e estado inicial.
   O brief exige entrega, comandos, o que ficou de fora e por quê, nomes, assinatura do
   verificador e caminho do hub de ensaio. Documentar valores provisórios do fixture e
   dependências dos tickets 05/06. labs/index.md tem local: true, mas labs/ensaio-do-banco.md
   está versionado: deixar explícito que a exclusão ainda cabe ao ticket 06.

2. **Recusar hub sem repositório Git próprio.** verificar-hub.mjs não confere .git.
   Reprodução: montei fixture com montar.mjs; renomeei .git para .git-revisao;
   verificar-hub.mjs retornou 0 sem mensagem. O spec exige .git real na raiz, sem marcador
   falso. O teste atual só verifica a existência do caminho criado pelo montar.
   Esse falso positivo quebra a descoberta do contrato em subpastas. Cobrir pela CLI a
   ausência e o marcador inválido. Distinguir a worktree legítima de construção do hub
   de ensaio entregue.

3. **Não dispensar toda pasta oculta da conferência de CLAUDE.md.** memoriasDentro pula
   qualquer entrada iniciada por ponto. Com .git restaurado, criei .oculta/CLAUDE.md:
   verificar-hub.mjs retornou 0 sem mensagem. O ticket 04 exige recusa no hub ou acima;
   o ticket resolvido 36 diz "em lugar nenhum". Exclusão de sync não dispensa esta regra.
   Cobrir pasta oculta aninhada pela CLI, sem entrar nos objetos administrativos do Git.
   Se papéis do Maestri exigirem exceção, obter do maestro a fonte da decisão e registrar
   o alcance; não supor dispensa de toda pasta com ponto.

## Reprodução adicional

Fixture: C:/Users/GUSTAV~1.DEL/AppData/Local/Temp/hub-ensaio-revisao-04-CxPQeu/hub
Sequência: montar -> 0; renomear .git; verificar -> 0; restaurar .git;
criar .oculta/CLAUDE.md; verificar -> 0.
Somente fixture de revisão alterado. Código, spec e tickets não foram editados.
Nenhuma configuração global alterada.

## Ao ligar as etapas

O ensaio serve de base estrutural. Frontmatter imposto, criação geral de iniciativas e
exclusões continuam nos tickets 05/06. Explicitar essas fronteiras no relatório.
A validação de .git e CLAUDE.md precisa proteger a porta de entrada antes da integração.


## Rodada 2 — 2026-10-16

Veredito: **passa com ressalva operacional**.
HEAD conferido: f485974. Ramo ticket-04 limpo. integracao continua ancestral (código 0).
Executei node --test "agents/test/*.test.mjs": 11 passaram, 0 falhas.
Executei o verificar-hub novo contra C:/context-hub-ensaio: código 0.
Os três consertos foram atendidos: relatório completo; Git validado pelo topo real;
pastas ocultas examinadas, exceto .git. Testes cobrem ausência, .git falso, worktree
e .maestri/roles/x/CLAUDE.md. Sem consertos obrigatórios restantes para o ticket 04.

Ressalva para integração: C:/context-hub-ensaio ainda contém agents/bin e agents/test
do commit 84aa46a. Rodar as ferramentas do ramo/repositório integrado, conforme relatório.
O maestro deve garantir que os consumidores não chamem a cópia antiga; um novo destino
vazio pode ser montado pelo montar.mjs, sem remover o ensaio existente.
A exclusão local: true e a validação de frontmatter permanecem nos tickets 06 e 05.
O registro da rodada 1 permanece acima para histórico.

## Atualização de critério — comunicação do maestro, 2026-10-16

Li a nota no topo do spec e as regras atualizadas. Nas próximas revisões:
- O que o agente chama: agents/skills/<peça>/.
- O que só harness, kit ou teste roda: agents/code/ (hooks, mods, kit, bin, test).
- Provas da etapa zero: agents/code/test/provas/<prova>/.
- Nenhuma pasta de código na raiz.
- Novo hub de ensaio em destino vazio, montado com o montar.mjs de integracao.

Conferido: ticket 04 integrado em b68f540. O parecer anterior é histórico;
a nova disposição será exigida nas próximas entregas, incluindo a rodada pendente do ticket 03.


## Ticket 05 — rodada 1 — revisão em andamento (2026-10-16)

Ramo ticket-05, HEAD b7c99c8, inicialmente limpo; integracao é ancestral.
O maestro pediu que esta revisão já iniciada terminasse individualmente;
revisão em dupla começa no próximo pedido. Regras revisao-em-dupla.md lidas integralmente.
Relatório, ticket 05, spec faixa 1, escolhas 14/19/20 e decisão do ticket 16 conferidos.
verificar-hub no repositório: código 0, apenas avisos previstos.
Suíte node --test "agents/code/test/*.test.mjs" ainda em execução.

Achados reproduzidos somente em fixture:
C:/Users/GUSTAV~1.DEL/AppData/Local/Temp/hub-ensaio-revisao-05-OkeKMM/hub

1. YAML flow válido com type errado é aceito com aviso de campo dedutível.
   --corrigir acrescenta type: research depois do mapa {...}, retorna 0 e deixa YAML inválido.
   A chamada seguinte recusa com end of the stream or a document separator is expected.
   Fonte: agents/code/bin/lib/frontmatter.mjs, aplicarTrocas, busca linhas campo: sem
   tratar o mapa flow nem validar novamente o novoTexto. Corpo da nota permanece,
   mas o frontmatter deixa de ser legível pela busca. Além disso, inbox com abertura ---
   sem fechamento recebe outro cabeçalho e retorna 0; o conteúdo quebrado vira corpo.

2. Arquivo explícito initiatives/context-hub/.secrets/nota.md, com texto inventado,
   recebe initiative, created e updated com --corrigir e sai 1 por falta title/status.
   Portanto a área ignorada é alterada. Ignorar pastas com ponto está só no caminhador
   notas; conferir e analisar não aplicam a regra ao caminho explícito.
   Afeta o consumo por arquivo alterado e --checar pelos hooks/MCP.
   O spec manda ignorar pastas com ponto. Teste existente só cobre varredura do hub.

Nenhum código, spec ou ticket editado; somente arquivos temporários de revisão.

### Fechamento da rodada 1 do ticket 05

Veredito: **volta**. Os 28 testes passaram, 0 falhas, código 0.
Comando executado: node --test "agents/code/test/*.test.mjs".
Os critérios cobertos pela suíte estão verdes: nota válida, faltas de juízo, stage inválido,
preenchimento dedutível, edição concorrente antes da releitura, criação e reexecução da skill.
Os esquemas e a tabela stage/status correspondem ao spec. Operations sem initiative,
caminho sem tipo com aviso e transferência de index/links/other/fim ao ticket 27 respeitam
as decisões registradas. Código e skill estão nos lugares exigidos.

Consertos obrigatórios (achados por Fiel):

1. **Preservar YAML válido ao corrigir e recusar cabeçalho quebrado sem gravar.**
   Original reproduzido em initiatives/context-hub/research/fluxo.md:
   ---
   {title: Fluxo, type: errado, initiative: context-hub, created: 2026-10-16, updated: 2026-10-16, question: Pergunta, stage: open, status: rascunho}
   ---
   Corpo preservado.
   Antes: código 0, aviso completaria type. --corrigir: código 0, completou type.
   Depois: código 1, YAML inválido, pois type: research foi inserido depois do mapa flow.
   Validar a transformação antes de gravar. Se a forma YAML não puder ser corrigida por
   trecho com segurança, recusar sem alterar o arquivo, com motivo claro. Cobrir a CLI
   com mapa flow e com campos indentados/multilinha; não normalizar o restante da nota.
   Cobrir também abertura --- sem fechamento: hoje o arquivo inbox/truncada.md contendo
   --- seguido de title: [aberto recebe outro cabeçalho e retorna 0.
   Requisito: YAML válido sempre; YAML inválido devolvido; só trecho derivável muda.

2. **Aplicar a exclusão de caminhos com ponto nas entradas explícitas e em --checar.**
   Reproduzi node agents/code/bin/verificar-frontmatter.mjs --raiz <fixture>
   --corrigir <fixture>/initiatives/context-hub/.secrets/nota.md.
   Texto inicial: Texto privado inventado. O comando gravou frontmatter e retornou 1
   por faltarem title e status. A pasta deveria ser ignorada, como na varredura do hub.
   Centralizar o critério para os consumidores compartilhados e testar CLI com arquivo,
   pasta oculta passada diretamente e conteúdo proposto em --checar. Nenhuma escrita
   nem recusa de esquema nas áreas ignoradas. Não mudar a conferência de CLAUDE.md
   em pastas ocultas: é uma regra distinta, do ticket 04.

Ressalvas sem pedido adicional: a janela entre releitura e escrita continua não verificada,
como no spec; index/links/other/fim seguem no ticket 27; frontmatter no hook e MCP
será validado nas respectivas etapas. Não expandir o ticket 05 para esses itens.

Encaminhado apenas ao Trilho. A próxima solicitação de revisão seguirá em dupla com
Fielzinho, conforme a instrução recebida durante esta rodada.
