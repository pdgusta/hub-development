# Rodada 2 — Sextante

Lidos: protocolo inteiro com os quatro fatos novos; r1-prisma, r1-quadrante, r2-quadrante. Conferi também o comentário novo do ticket 16 e os trechos dos tickets 14 e 40 relevantes aos ajustes abaixo. Não edito a proposta.

Marcas por extenso: [núcleo] = escolha do núcleo, sujeita ao aval do Gustavo; [formato] = depende do formato, ainda não decidido; [ticket aberto: 56] = origem ainda não fechada.

## Votos nas mudanças do Quadrante

| Mudança | Voto e fundamento |
|---|---|
| Q-1 | **Concordo com ajuste.** Excluir propostas e uso da guarda está certo (40, Answer). Não escrever que todo `agents/skills/**` pede aval e, ao mesmo tempo, deixar aberto se as skills gerais entram. Cobrir o acervo definido — `maestro-*` e skills de papel — e deixar a ampliação às skills gerais como pendência. Preservar a guarda explícita da skill nova iniciativa (12, rodada 12) e a exceção do maestro em routing.yml (15). |
| Q-2 | **Concordo.** O 15 é posterior ao 42 e decide retirar GSD do escopo global com cópia. |
| Q-3 | **Concordo.** Retirar falsas contradições; preservar a fonte e a precedência: 14 para marcador, 15 para GSD, 11 para escrita do Desktop. Dono é formato. |
| Q-4 | **Concordo.** Sem ambas as fontes, informar indisponibilidade, sem inventar estado. O 14 decide as duas fontes; a saída DESCONHECIDO é evidência da bancada, não terceira fonte. |
| Q-5 | **Concordo com ajuste.** Manter os dois canais decididos (33 e 14). Não encerrar como resolvida a política de repetição: o 33 manda notificar quando piora e o 14 prevê notify por turno com divergência. O comportamento combinado precisa ser descrito e testado, sem afirmar que uma deduplicação específica foi decidida. Qualquer política nova fica [núcleo]. |
| Q-6 | **Concordo com ajuste.** A frase do 36 vale para toda ferramenta de gravação. A frase adicional fica [núcleo], mas “grave com base_rev” deve dizer “nas operações cuja API exige base_rev”. Não impor automaticamente a mesma assinatura de write/edit a delete/move, cuja guarda ainda precisa ser definida. O 30 nomeia write_note e edit_note; garantir versão não decide sozinho a assinatura das demais. |
| Q-7 | **Concordo com ajuste.** Manter o teste do 36; explicitar Claude Code, Codex e Copilot CLI no modo não interativo. Copilot do VS Code continua com roteiro próprio, pois o critério 1 cobre CLI e VS Code (04) e o modo não interativo não prova a superfície VS Code. Login e momento de execução são formato. |
| Q-8 | **Concordo com ajuste.** A conciliação é [núcleo], como proposto. Não desligar a guarda do acervo por a sessão estar fora do hub: ela decide pelo arquivo-alvo, no escopo do usuário (40, R46). Também não tratar MAESTRI_TERMINAL_ID como identificação suficiente de maestro; recrutas também a têm. A distinção de papel continua pendente. Nova Sextante-18 abaixo detalha esse ponto. |
| Q-9 | **Concordo com ajuste.** Conteúdo da ponte: busca e banco com escrita (11), mais pasta conectada. “Gerada e não instalada”, faixa 10 e demais responsáveis ficam todos [formato]; isso não reduz permanentemente a entrega decidida a gerar configuração. |
| Q-10 | **Concordo.** Separar skills gerais e de papel conforme o 15. Não escolher agora a topologia física das junctions; o próprio Q-10 a mantém aberta. |
| Q-11 | **Concordo.** Preservar a decisão do 14 e registrar a prova com git real; não reescrever os tickets anteriores. |
| Q-12 | **Concordo com ajuste.** A limitação de COPILOT_HOME vem do 18. COPILOT_SKILLS_DIRS pode ser solução [núcleo] a verificar. Não converter automaticamente o teste da variável extra em prova do caminho padrão de produção; registrar o que cada ensaio alcança. O passo real não é dispensado por esse ensaio. |
| Q-13 | **Concordo com ajuste.** Releitura da cabeça, tarefa diária e data são escolhas do núcleo; atribuições de dono são também formato. Após os fatos novos, limpeza baseada em 30 dias não é entrega desta construção. Manter as três lacunas remanescentes abertas. |
| Q-14 | **Concordo com ajuste.** Atualizar com o fato novo do Docker. Login, cópia dos pilotos e autorização/orçamento para testar gemini continuam pendentes. Distinguir autorização de execução e desenho: o 09 já decidiu configurar/testar uma vez o gemini e deixá-lo desligado; não reabrir essa decisão por faltar autorização concreta para as chamadas. |
| Q-15 | **Concordo com ajuste.** Aceito a retirada da ordem de etapas informada na r2. Marcar formato e descrever efeitos condicionais. Corrigir “as portas ... podem virar um banco só”: só as portas de CouchDB podem ser consolidadas; portas de MCP e busca não viram portas de banco. Nem todos os dublês somem necessariamente; a necessidade será reavaliada. |
| Q-16 | **Concordo.** Marcar origem no 56, sem tratá-la como decisão. Aplicar também no núcleo e testes. Os fatos novos retiram da construção as entregas que dependem exclusivamente dele. Arquivamento seguro (12/36) e cópia diária (33) continuam. |
| Q-17 | **Concordo com ajuste.** Alinhar números conflitantes aos do núcleo como referência do plano anterior, marcados [formato]. Isso não decide portas da execução nova nem dá prioridade normativa ao núcleo. |

## Votos nas mudanças do Prisma

| Mudança | Voto e fundamento |
|---|---|
| Prisma-1 | **Concordo.** 25/30 dão a forma de conflito preservando folhas; a garantia do 11 não deve ser usada para autorizar sobrescrita. Resposta explícita manda reler e refazer. |
| Prisma-2 | **Concordo.** Base em write_note/edit_note conforme o 30 e a garantia do 11. Manter pendentes as operações não cobertas explicitamente; não presumir assinatura de anexar/delete/move. |
| Prisma-3 | **Concordo.** READ_ONLY=true vem do 34. Comando e testes concretos da implementação ficam identificados como solução do núcleo quando só ele os descreve. |
| Prisma-4 | **Concordo.** E2EE não é condicional: 34, com passphrase no MCP pelo 30. Testes de versão com cifra devem preservar as mesmas garantias. |
| Prisma-5 | **Concordo com ajuste.** Ferramenta requerida pelo 14; nome é [núcleo]. Ela precisa informar estado indisponível se a fonte do próprio servidor faltar. Devolver o arquivo ausente não resolve magicamente a reserva; não prometer estado saudável sem fonte. |
| Prisma-6 | **Concordo.** Duas formas de visibilidade podem ficar como [núcleo]; o 25 exige visibilidade, o 30 permite alternativas. |
| Prisma-7 | **Concordo com ajuste.** Releitura por initialize e posição antes do upstream ficam [núcleo]. Donos ficam [formato]. Preservar o requisito de contrato atual sem elevar a implementação escolhida a ticket fechado. |
| Prisma-8 | **Concordo com ajuste.** Mesmo ajuste da Q-6: frase do 36 obrigatória, acréscimo [núcleo] e versão na operação aplicável. Não inventar base_rev em delete/move por extensão silenciosa. |
| Prisma-9 | **Concordo.** 12, imposição C, exige validação no MCP. O “se couber” não revoga o requisito. |
| Prisma-10 | **Concordo.** Vigia precisa identificar o caminho legível sob E2EE (34/48), sem expor segredos. Escolha entre leitura direta e uso do CLI fica técnica. |
| Prisma-11 | **Concordo.** Caminho, esquema e troca atômica concretos são [núcleo]; estado curto e leitura pela checagem vêm do 33. |
| Prisma-12 | **Concordo com ajuste.** HUB_OUTRO_PAR_URL é mecanismo [núcleo], não prova suficiente de “máquina ligada” em toda falha. CouchDB parado com a máquina ligada não pode ser classificado como máquina desligada e suprimir divergência. Manter essa distinção como lacuna do detector; ver Sextante-19. |
| Prisma-13 | **Concordo.** Config Doctor é requisito explícito do aviso no 33; detector não verificado não torna o requisito opcional. |
| Prisma-14 | **Concordo com ajuste.** Código de erro e item da vigia podem ficar como [núcleo], para aval. A política geral “quem percebe a falha”, vinda do 56, permanece fora da construção conforme os fatos novos. Não afirmar que a conversa fechou a política geral nem apagar a lacuna correspondente sem distinguir sua origem. |
| Prisma-15 | **Concordo.** 15 vence a coexistência global de GSD dos tickets anteriores. |
| Prisma-16 | **Concordo.** Skills gerais globais, skills de papel na pasta do papel (15). |
| Prisma-17 | **Concordo com ajuste.** Mesmo ajuste da Q-9: conteúdo obrigatório conforme 11, donos e só gerar/instalar dependem do formato. |
| Prisma-18 | **Concordo com ajuste.** Propostas e uso fora da guarda. O acervo não é sinônimo de toda skill. Não ampliar a guarda a skills gerais enquanto a própria parte deixa isso aberto. Preservar nova iniciativa (12) e routing.yml (15). Não inferir uma proibição permanente de qualquer pasta futura em agents/maestro só porque hoje há propostas/uso. |
| Prisma-19 | **Concordo.** Marcar 56 e retirar suas entregas exclusivas desta construção, conforme fato novo do 16. |
| Prisma-20 | **Concordo com ajuste.** Data no nome é [núcleo]. Ela não substitui nem elimina archived_at e o esquema de origem decididos pelo catálogo aceito no 12. Limpeza por 30 dias permanece fora. |
| Prisma-21 | **Concordo com ajuste.** Pode constar como desenho [núcleo], com origem do prazo [ticket aberto: 56], fora desta construção. Dono e agendamento concreto são formato. |
| Prisma-22 | **Concordo com ajuste.** A r2 do Quadrante já aceita meu ajuste: duas instâncias/reuso da escrita são [núcleo]; requisitos de separação leitura/escrita e guarda vêm de 11/14/34. Prova operacional permanece não verificada. |
| Prisma-23 | **Concordo com ajuste.** Testar a busca via proxy. Configurar allowed-host conforme o Host realmente observado, se necessário; não assumir que será automaticamente o endereço/porta do proxy. A condição e o mecanismo são proposta do núcleo. |
| Prisma-24 | **Concordo com ajuste.** Troca de trecho não dispensa guarda de versão (11). “Só completa deriváveis” descreve o frontmatter; não apaga as funções de manter índices e conferir/corrigir links do verificador (12). Conteúdo final para validação é solução [núcleo]; canal de fim segue 14. |
| Prisma-25 | **Concordo.** Forma visual do mod aberta conforme 33. XML, WhatIf e modo de ensaio são formato; a vigia agendada a cada 5 min permanece requisito. |

## Quatro efeitos dos fatos novos

1. **Tailscale e TI — concordo.** Retirar consulta pendente e incerteza sobre conflito corporativo. Registrar confirmação do Gustavo no 16, comentário de 2026-10-16 ~15h35. Não estender essa confirmação a interações com Docker/WSL que ele não mencionou. Sem nova pesquisa nesta revisão.
2. **56 depois da construção — concordo com ajuste.** Arquivo por raiz e cópia diária permanecem pelos tickets resolvidos. Retirar da entrega atual prazo/limpeza de 30 dias, política de recuperação, tolerância de dois dias e liberações originadas exclusivamente do 56. Podem permanecer como contexto [ticket aberto: 56], claramente fora do aceite atual. A solução de falha da cópia proposta pelo núcleo pode ser avaliada separadamente; não fecha por si a política geral do 56.
3. **Copilot sem política aplicada — concordo.** Já está coberto. Registrar o fato desta máquina, sem convertê-lo em garantia para outra máquina ou qualquer política futura (16, 2026-10-16; 14).
4. **Docker e GitHub — concordo com ajuste.** Registrar “Gustavo vai ligar Docker e criar repositório privado vazio”. Isso responde quem fará a preparação; não comprova que já foi feita. Login/pilotos/cota do gemini continuam abertos. Repositório nu local pode permanecer como opção de ensaio [formato]. URL, deploy keys, ligação efetiva e push real continuam passos ainda por fazer; não criar nem publicar nada nesta revisão.

## Respostas aos ajustes nos meus votos de rodada 1

- Sextante-7: aceito a confirmação do Quadrante. Checkpoint sem IA é [núcleo]; verificador sem IA é decisão do 12.
- Sextante-12: aceito manter “faixa 1” apenas como referência histórica [formato], sem apresentá-la como dono decidido da execução nova.
- Sextante-17: aceito retirar a ordem das etapas. O novo plano permanece com o Gustavo.
- Demais Sextante-1 a Sextante-17: mantenho os textos da r1, com as distinções acima. Aguardo o voto do Prisma; nenhuma unanimidade presumida.

## Mudanças novas

### Sextante-18: Guarda do acervo considera o arquivo-alvo, inclusive fora do hub
- Onde: `spec-partes/faixas-09-10.md`, faixa 9, guarda, primeira instrução e conflito “hooks saem fora do hub”; núcleo, Worker 9.
- Texto atual: conciliação Q-8 deixa explícitas só as exceções de início e uso; “os demais hooks ... recusa seguem o 14”.
- Texto proposto: “A guarda do acervo não pode ser desativada só porque a sessão abriu fora do hub. O caminho-alvo real, inclusive via junction, define se a peça é protegida. Essa conciliação dos escopos fica [núcleo], para aval. Identificar maestro versus recruta continua pendente; MAESTRI_TERMINAL_ID identifica terminal, não papel.”
- Fonte: 40, R46/Answer, guarda no escopo do usuário e acervo para todo maestro dentro ou fora do hub; 14, saída fora do hub para hooks do hub. A interpretação conciliadora não deve abrir o acesso pelo atalho ou pela pasta de trabalho externa.

### Sextante-19: Serviço sem resposta não equivale a par desligado
- Onde: `spec-partes/faixas-07-08.md`, faixa 7, detector do outro par; núcleo, Worker 7.
- Texto atual: Prisma-12 propõe testar HUB_OUTRO_PAR_URL como forma de saber que o outro par está ligado.
- Texto proposto: “A falha da URL do serviço não basta para declarar a outra máquina desligada. O detector precisa distinguir máquina desligada, serviço indisponível e estado não verificável. O mecanismo exato e a representação do estado incerto ficam propostos/abertos; não tratar incerteza como estado em ordem.”
- Fonte: 33, Answer: divergência se a outra máquina estiver ligada na tailnet e a replicação não levar mudanças por mais de 15 min; desligada não é divergência. Escolher o sinal da disponibilidade é [núcleo], não mudança nessa definição.

Nenhum teste, varredura ou edição da proposta executado.
