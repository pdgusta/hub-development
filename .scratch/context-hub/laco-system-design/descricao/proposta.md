# Como refazer a descrição do hub (proposta do maestro, rodada 6)

2026-10-15, depois da rodada 5 (ticket 56). O Gustavo pediu uma descrição do hub rica e genérica o bastante para
qualquer diagrama nascer dela, técnica e prática ao mesmo tempo. Ela deve responder perguntas como "se o Gustavo edita
um arquivo, o que acontece?", e as perguntas servem de fonte, não de critério. Nome provisório: **descrição de design
do hub** (o Gustavo sugeriu "context-hub design description" e disse que "texto padrão" não é bom nome).

## O diagnóstico

O `texto-do-hub.md` foi escrito a partir das decisões, componente por componente: tabela de componentes, tabela de
ligações e cinco fluxos. Daí os dois defeitos que o Gustavo apontou:
- **Falta o prático.** A ligação "Obsidian → banco local" é o caminho técnico, mas o que o Gustavo faz é editar a vista
  Markdown. O texto não tem atores fazendo ações, só peças trocando coisas.
- **Falta quem responde por quê.** A "disciplina do agente" virou um grupo de componentes, sem dizer que ela vive
  dentro da sessão do agente e age sobre ele. O texto não tem responsabilidade nem pertencimento.

Enfiar os dois exemplos no texto corrigiria dois sintomas e deixaria a causa. A causa é a forma do texto: ele só tem
dois eixos (componentes e ligações), e um diagrama qualquer pede mais.

## A forma nova: um modelo com sete eixos

A descrição deixa de ser uma lista e passa a ser um modelo, em prosa curta com tabelas, com estes eixos:

1. **Atores:** quem age (o Gustavo, cada tipo de agente, o maestro, o outro par, o cliente, os processos agendados).
2. **Componentes:** o que existe, com papel numa frase (o que já está no texto atual).
3. **Responsabilidade:** quem é dono de cada componente, quem o aciona, quem o lê e quem só o vê.
4. **Pertencimento:** a que grupo lógico cada coisa pertence e por quê (podendo pertencer a mais de um, dito
   explicitamente), e onde ela vive (na máquina, na sessão do agente, fora).
5. **Ações práticas:** o que cada ator faz no dia a dia, com as palavras dele ("edito a nota no Obsidian"), ligadas ao
   caminho técnico que cada ação dispara.
6. **Cenários:** sequências passo a passo, do gatilho ao fim, incluindo falhas ("e se o outro par estiver desligado?").
7. **Estado de cada afirmação:** decidido (com o ticket), na prática (dito pelo Gustavo ou observado), a decidir, não
   verificado.

## Como chegar lá: um laço com perguntas escondidas

1. **Banco de perguntas.** Geradores de vários modelos pelo FreeLLMAPI, cada um com uma lente (o Gustavo no dia a
   dia, um agente novo, o maestro, o outro par, as falhas, a segurança, um leitor que nunca viu o hub), escrevem
   perguntas de muitos tipos: "se X, o que acontece?", "qual a relação entre X e Y?", "quem é responsável por X?", "X
   faz parte do grupo de Y?", "o que X não faz?". As cinco do Gustavo entram como semente. O maestro tira repetidas e
   chega a umas 150. Cota orçada antes.
2. **Duas metades.** Um sorteio separa as perguntas: **metade serve de fonte** para o Tech lead escrever a descrição;
   **metade fica escondida** dele e só serve para testar. É o que evita "enfiar os exemplos no texto": se a descrição só
   responde as perguntas que o autor viu, ela não é genérica.
3. **A descrição.** O Tech lead reescreve nos sete eixos, a partir do mapa, dos tickets resolvidos, do glossário e das
   perguntas da metade visível. O que só o Gustavo sabe (a prática) vira uma lista curta de perguntas a ele, numa rodada,
   em vez de chute.
4. **O teste de "qualquer agente".** Modelos diferentes pelo FreeLLMAPI, que só leem a descrição, respondem às
   perguntas escondidas. O Tech lead confere as respostas contra as fontes: acertou, errou ou "a descrição não diz".
   Cada falha vira um conserto no **eixo** que faltou, não na pergunta. Até 3 voltas, ou até a taxa de "não diz" e de
   erro ficar baixa.
5. **O teste de "qualquer diagrama".** Um agente que só lê a descrição desenha três diagramas de tipos diferentes: a
   sequência de um cenário, uma matriz de quem responde por quê e um mapa de grupos. Se algum não sai, ou sai errado,
   falta eixo.
6. **De volta à cidade.** Com a descrição nova, o UI engineer faz o conceito da mistura (a B como base, com a
   responsabilidade da A), que passa pela porta. A cidade também ganha um jeito de **responder a um cenário sem texto**:
   escolher "o Gustavo edita um arquivo" e ver o caminho aceso na cidade. Isso ainda é proposta; a forma sai do conceito.

## Custo

- Perguntas e respostas pelo FreeLLMAPI: algumas centenas de chamadas, orçadas pelo limite diário de cada provedor
  antes de rodar.
- Tech lead (descrição e conferência, até 3 voltas): perto de 400 mil tokens de Claude. Conceito da mistura e porta: perto
  de 300 mil.
- O laço está em ~2,4 milhões de 5. Cabe no orçamento.
