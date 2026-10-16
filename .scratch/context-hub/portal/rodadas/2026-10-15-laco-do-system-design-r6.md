---
titulo: Como refazer a descrição do hub
ticket: 56
aberta: 2026-10-15
estado: absorvida
---

Não é um desafio grande demais: é um laço como os outros, só que o produto é o texto, e não o desenho. Proposta inteira
em `laco-system-design/descricao/proposta.md`.

**O que eu vejo de errado no texto de hoje:** ele foi escrito a partir das decisões, componente por componente,
e só tem duas coisas: o que existe e o que liga com o quê. Por isso a linha vai do Obsidian ao banco (o caminho
técnico), e não do Gustavo à vista Markdown (o que você faz). Por isso a disciplina do agente fica solta: o texto não diz
quem responde por quê nem onde cada coisa vive. Enfiar os seus dois exemplos consertaria dois sintomas e deixaria a
causa.

**A forma nova:** a descrição vira um modelo com sete eixos: quem age, o que existe, quem é dono e quem só usa, a que
grupo cada coisa pertence e onde vive, o que cada um faz no dia a dia (nas suas palavras, ligado ao caminho técnico), os
cenários passo a passo (com as falhas), e se cada afirmação está decidida, é prática, está a decidir ou não foi
verificada.

**Como evitar que ela só responda o que o autor viu:** umas 150 perguntas de muitos tipos, geradas por vários modelos
com lentes diferentes (você no dia a dia, um agente novo, o maestro, o outro par, as falhas), com as suas cinco como
semente. Metade vai para o Tech lead escrever; a outra metade fica escondida dele. Depois, modelos que só leem a
descrição respondem às escondidas, e cada falha conserta o eixo que faltou, não a pergunta. Por fim, um agente que só
leu a descrição desenha três diagramas de tipos diferentes; se algum não sai, falta eixo. O que só você sabe da prática
vira uma lista curta de perguntas a você.

Depois disso, a cidade da mistura (a B com a responsabilidade da A) nasce da descrição nova.

## O caminho
id: caminho
tipo: escolha
recomendada: A

- A: O laço inteiro: modelo de sete eixos, umas 150 perguntas por vários modelos do FreeLLMAPI, metade escondida, teste de respostas por modelos que só leem a descrição, teste de três diagramas; depois a mistura. Uns 700 mil tokens de Claude e algumas centenas de chamadas do gateway, orçadas antes
- B: Versão curta: o Tech lead reescreve nos sete eixos a partir das suas cinco perguntas e de umas 50 geradas, sem metade escondida e sem teste por outros modelos; depois a mistura. Mais rápido, mas a descrição pode responder só ao que ele viu
- C: Primeiro você responde a uma lista de perguntas práticas (o que você faz, o que espera que aconteça), e só depois a descrição e o laço da opção A

## Algo mais?
id: algo-mais
tipo: texto
