# Contrato file-first: zonas e checkpoint

Type: prototype
Status: resolved
Blocked by: 01

## Question

Qual é o processo que o hub pronto impõe aos agentes para que qualquer sessão futura (outro agente,
outro modelo, outra máquina) retome um trabalho de onde a anterior parou, só com o que está no disco
(critério 2)? Decidir: (1) o que é "contexto suficiente para retomar"; (2) quando ele é escrito sem o
Gustavo pedir (o checkpoint e seus gatilhos); (3) como a sessão seguinte o acha. As zonas (§9) entram
só para separar o que sobrevive à sessão do que morre com ela; as pastas são de "Arquitetura de pastas
e frontmatter do hub". O FreeLLMAPI entra como opção para o checkpoint (Q13). O ticket desenha o
processo; nada dele é aplicado agora às sessões desta frente. (Reescrita em 2026-10-03, rodada 2.)

## Comments

- 2026-10-03: protótipo de lógica em
  [`prototipo-10-contrato.html`](../prototipos/prototipo-10-contrato.html) (abre com dois cliques;
  tudo em memória). Aplica um rascunho do contrato (quatro zonas da §9 e a tabela "tipo → lugar", com
  dez tipos) à sessão de 2026-10-02 que resolveu "Divergência e edição concorrente", reconstruída a
  partir dos arquivos que ela deixou. Os gatilhos do checkpoint são chaves: regra (sempre ligada), hook
  ao fim de cada resposta (`Stop`, tipo `prompt`) e revisão pós-sessão pelo FreeLLMAPI. Cinco
  roteiros: a sessão como foi; o agente esquece; esquece com hook; interrupção e compactação; fora do
  hub com dado de cliente (hipotético). Base dos gatilhos: documentação oficial de hooks do Claude
  Code, conferida em 2026-10-03.
- 2026-10-03: rodada 1 em `respostas.md`, com quatro perguntas: Q1 o rascunho do contrato; Q2 o
  gatilho do checkpoint; Q3 a memória automática do Claude; Q4 quem esvazia a triagem. Achados do
  protótipo que pesam: na sessão real, uma preferência ficou só na memória privada do Claude; o hook
  `Stop` vê só a última mensagem e não roda em interrupção; a revisão pelo FreeLLMAPI não pode ler
  transcrição com dado de cliente.
- 2026-10-03: o Gustavo pediu outro formato: "não quero ter que estudar o protótipo pra usá-lo"; em vez
  de replicar o acontecimento real, o protótipo deve passar o que o ticket quer comunicar, com
  diagramas, analogias e explicação simples. O simulador foi substituído, no mesmo arquivo, por uma
  página de explicação (zonas como cômodos, o caminho de cada coisa até o lugar, a linha do tempo com
  os furos de cada gatilho, a gaveta pessoal do Claude, a caixa de entrada), terminando nas quatro
  perguntas da rodada 1. A preferência foi para as Notes do mapa.
- 2026-10-03: o Gustavo corrigiu o enquadramento: a primeira versão pensava o contrato só para o fluxo
  do Matt (lugares = ticket, mapa, `respostas.md`), esquecendo que é o contrato do context hub inteiro;
  o fluxo do Matt é só como esta frente constrói e pesquisa a primeira versão. A parte 1 da página e a
  Q1 foram refeitas com os lugares do hub. Ficaram assim: contrato do hub; compartilhado, que só recebe
  por promoção; uma "sala" por iniciativa, com estado e próxima ação como porta de entrada, decisões,
  achados, trabalho e triagem; perfil da máquina; efêmera. Cada iniciativa declara na porta de
  entrada onde ficam as decisões e os achados dela; esta frente declara os tickets. A triagem passou a
  receber só o que sai da sala: promoção, regra ou preferência, skill nova. A Q4 foi ajustada.
- 2026-10-03, resposta à Q1 da rodada 1: "não estão certos, o que estamos criando é o próprio hub em
  si. Não estamos criando uma iniciativa do hub. O 'contrato file-first' nada mais é que um contrato
  que força os agentes a sempre manterem contexto suficiente para sessões futuras (aka outros
  agentes/modelos) retomarem um trabalho iniciado em uma sessão anterior." O Gustavo respondeu só a Q1,
  porque ela "muda tudo talvez": o ticket tinha sido entendido errado. A rodada 1 foi encerrada. A Q2
  (gatilho do checkpoint) e a Q3 (memória automática do Claude) ficam suspensas, para voltar reescritas
  sob a ótica da retomada; a Q4 (triagem) sai. O protótipo será refeito depois que a reformulação for
  confirmada (rodada 2).
- 2026-10-03, resposta à Q1 da rodada 2: "Você entendeu certo dessa vez, porém o contrato file-first
  não é para AGORA. É para quando o context hub estiver PRONTO." Analogia do Gustavo: ele é o patrão
  da sorveteria, o agente é o gerente; pedir um processo para criar sabores novos não é pedir que os
  subordinados já saiam fazendo um sabor. Consequência: o ticket entrega o desenho do contrato, a ser
  construído em "Passagem para a construção"; o primeiro protótipo, que aplicava o contrato à sessão de
  2026-10-02, foi descartado. A pergunta do ticket foi reescrita.
- 2026-10-03: página de explicação refeita no mesmo arquivo, como desenho do processo para o hub
  pronto. A imagem é a passagem de plantão. A página cobre a nota de retomada (sete campos,
  sobrescrita, teste de suficiência), os gatilhos do checkpoint (regra, hook `Stop` e revisão
  pós-sessão, com os furos de cada um) e como a sessão seguinte acha a nota (checagem de início de
  sessão, pasta, busca). Rodada 3 em `respostas.md`: Q1 o que é suficiente; Q2 os gatilhos; Q3 como
  achar.
- 2026-10-04, respostas da rodada 3: Q1 "sim" (nota de retomada com sete campos, sobrescrita, teste de
  suficiência); Q3 "ok" (a checagem de início de sessão abre a nota; a pasta diz o trabalho; busca como
  plano B). Q2: "não concordo com revisão pós-sessão muito menos com ela sendo pelo freellmapi. Acho
  que posso considerar colocar algo na regra global ou do projeto (claude, codex, agentes.md) que force
  o agente a ver se a memória privada tem contexto exclusivo relevante para o andamento do trabalho
  que o hub não tenha. E force o agente a gravar no hub, no lugar certo." A revisão pós-sessão e o
  FreeLLMAPI saem do checkpoint. A memória privada fica ligada, e o contrato obriga a levar ao hub o
  que só ela tem (isso também resolve a pergunta da rodada 1 sobre desligá-la). Fica aberto se o hook
  ao fim da resposta continua como o mecanismo que faz a regra ser cumprida: rodada 4.
- 2026-10-04, resposta da rodada 4: "ok" para regra e hook juntos.

## Answer

Decidido com o Gustavo em 2026-10-04, depois de quatro rodadas. O ticket desenha o processo que o hub
pronto impõe aos agentes; nada dele é aplicado agora às sessões desta frente.

**Objetivo do contrato:** qualquer sessão nova (outro agente, outro modelo, outra máquina) retoma um
trabalho de onde a anterior parou, usando só o que está no disco.

1. **O que é suficiente: a nota de retomada.** Cada trabalho tem uma, curta, com sete campos:
   objetivo, onde parou, próximo passo, decisões (a linha e um ponteiro), o que foi tentado e não deu
   certo, perguntas abertas, arquivos em jogo. É sobrescrita, não acumulada (o histórico fica nas
   decisões e no git). Marca o que é fato e o que é hipótese. Critério: um agente que nunca viu o
   trabalho, lendo só a nota e o que ela aponta, dá o próximo passo sem perguntar nada que já foi
   respondido. Sobrevivem à sessão a nota, as decisões e os arquivos do trabalho; o chat e o
   scratchpad morrem com ela.
2. **Quando é escrita: regra e hook.** A regra vai no contrato global de cada harness (o papel do
   Maestri esconde o `AGENTS.md` do workspace). Ela manda manter a nota em dia e conferir se a memória
   privada da ferramenta tem contexto exclusivo relevante que o hub não tem, gravando-o no hub, no
   lugar certo. O hook ao fim de cada resposta (`Stop`) é o que obriga: quando a nota não reflete a
   resposta, ou a memória privada ganhou algo que o hub não tem, ele faz o agente continuar e gravar.
   Furos aceitos, cobertos só pela regra: o hook não vê o que foi dito no meio de uma resposta longa e
   não roda quando o Gustavo interrompe. **Fora:** revisão pós-sessão e o FreeLLMAPI no checkpoint.
   A memória automática do Claude continua ligada.
3. **Como a sessão seguinte acha a nota:** a checagem de início de sessão (a de "Divergência e edição
   concorrente") também abre a nota do trabalho. A pasta onde a sessão abre diz qual é o trabalho;
   quando não diz, o agente acha a nota pela camada de busca, pelo nome que o Gustavo der, ou pergunta.

Base dos hooks: documentação oficial do Claude Code (`code.claude.com/docs/en/hooks` e
`hooks-guide`), conferida em 2026-10-03. **Não verificado:** hook equivalente ao `Stop` e hook de
início de sessão no Codex e no Copilot (vai para "Acesso dos agentes: decisão").

Para a construção: a regra no contrato global de cada harness; um hook `Stop` (Claude Code) que
confere a nota e a memória privada; a checagem de início de sessão estendida para abrir a nota.

Protótipo: [`prototipo-10-contrato.html`](../prototipos/prototipo-10-contrato.html) (página de
explicação, versão final; as versões anteriores foram descartadas nas rodadas 1 e 2).
