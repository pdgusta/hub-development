# Brief da carta do plano de construção (maestro, 2026-10-16)

Para: **Aquarela** (faz) e **Lente** (revisa). Mesmo fluxo das cartas das escolhas: a Aquarela pede a revisão ao Lente
antes de avisar o maestro; até duas voltas; parecer em `revisao/plano/parecer-carta-plano.md`.

## O que a carta explica

A proposta em `C:\Projetos\context-hub\.scratch\construcao-do-hub\revisao\plano\proposta-de-etapas.md` (leia inteira).
O Gustavo vai decidir na rodada, nesta ordem:

1. **A construção em etapas, uma depois da outra, nessa ordem** (etapa 0 de provas de risco, depois as 10 faixas na
   ordem da tabela, e a junção). O desenho central da carta é essa sequência e **por que** cada etapa vem depois da
   outra: o que cada uma usa de verdade da anterior. Confira as dependências no `spec.md`, seção "Como segue sem
   esperar as outras faixas" de cada Worker (Worker N = faixa N); se achar dependência que a tabela não mostra ou que
   contradiz a ordem, avise o maestro antes de desenhar.
2. **A etapa 0 de provas de risco**: o que ela testa e por que vem antes de tudo.
3. **Os ramos de ontem**: guardar como referência e recomeçar cada etapa da ponta de `integracao`.
4. **Como você diz ao maestro como executar cada etapa**: antes de cada etapa, o maestro propõe uma receita (quem
   constrói, quem revisa, qual modelo, quantos no canvas) e o Gustavo ajusta. Mostre como isso acontece no tempo.

Ao fim, o que fica para a hora de cada etapa (as perguntas da última seção da proposta), como um lembrete leve.

## Forma

- O Gustavo aprovou com elogio o seu caderno de aquarela do faroleiro. Esta carta precisa de **linguagem própria e
  nova** (ele quer ser surpreendido; uma variação do caderno seria recusada como "só restilizou"). Ele também já
  elogiou o mapa de metrô e a maré: uma sequência com dependências pede algo nessa família de "caminho que se lê de
  relance", mas invente a sua forma.
- Diagrama no centro, pouco texto, nada de código interno sem palavras ("faixa 7" só ao lado do nome: "a vigia").
- Lê de cima para baixo sem clique obrigatório; resumo final numerado na ordem das perguntas (1 a 4).
- Arquivo: `revisao/plano/carta-plano.html`; PNG em 1400 px e 390 px; porta 8782 e o seu perfil de Edge.
- Não edite `cartas.json`, rodadas, tickets nem o spec. Ao terminar (depois do "passa" do Lente):
  `maestri ask "Claude Code" "Aquarela: carta do plano pronta em <caminho>, parecer em <caminho>"`.
