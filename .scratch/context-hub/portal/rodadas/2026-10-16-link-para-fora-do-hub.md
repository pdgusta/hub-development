---
titulo: Link para um arquivo fora do hub
ticket: 16
aberta: 2026-10-16
estado: aberta
---

**A etapa 1 fechou.** O verificador que cuida das pastas (ticket 27) entrou: ele cria o `index.md`, avisa de notas
parecidas em `other/` e corrige os links nos dois sentidos. Um link para o que não replica (pasta `local: true`, pasta
com ponto) vira `par://<máquina>/<caminho a partir da raiz do hub>`, e o contrário volta a link comum.

**O que ficou em aberto.** Em "Arquitetura de pastas" (rodada 14) a regra diz que também o que está **fora do hub** se
linka por `par://<máquina>/<caminho a partir da raiz do hub>`, "sem letra de unidade". Só que um arquivo fora do hub
(por exemplo, um repositório de código em `C:\Projetos\cliente-x\README.md`, já que os repositórios ficam fora do hub)
não tem caminho a partir da raiz do hub. Hoje o verificador deixa esses links como estão. O Fiel e o Fielzinho
apontaram a lacuna.

## Como se linka um arquivo fora do hub
id: link-fora-do-hub
tipo: escolha
recomendada: B

- A: `par://<máquina>/~/<caminho a partir da pasta do usuário>` (ex.: `par://par-1/~/Projetos/cliente-x/README.md`): sem letra de unidade, mas só serve ao que mora dentro da pasta do usuário; um link para `C:\Projetos\...` não caberia
- B: `par://<máquina>/<unidade>/<caminho>` (ex.: `par://par-1/C/Projetos/cliente-x/README.md`): a unidade entra como primeira pasta só para o que está fora do hub, porque lá não há outra âncora; dentro do hub segue sem letra de unidade; o verificador reescreve os links fora do hub para essa forma e avisa
- C: Link para fora do hub não é reescrito: o verificador avisa que o destino só existe nesta máquina e pede que a nota cite o caminho como texto, como já faz com o que está em `.secrets/`

## Algo mais?
id: algo-mais
tipo: texto
