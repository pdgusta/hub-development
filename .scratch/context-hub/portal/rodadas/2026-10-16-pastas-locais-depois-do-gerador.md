---
titulo: Pastas locais: o que o gerador de exclusões deixou em aberto
ticket: 16
aberta: 2026-10-16
estado: aberta
---

O ticket 06 entrou: o **gerador de exclusões** lê os marcadores (tudo que tem ponto e toda pasta cujo `index.md` diz
`local: true`) e escreve a lista do que não vai ao banco nem à busca. A Vela provou que ele funciona e achou quatro
pontos que ninguém decidiu. Eles pesam no ticket 08 (o banco aguentando o uso real), que a Brasa pega depois do 07; por
isso vêm agora.

**1. Pasta local nova com o sincronizador ligado vaza.** O LiveSync manda o arquivo na hora em que ele aparece, inclusive
o próprio `index.md` com `local: true`, antes de o gerador rodar. A prova só passou porque a pasta nasceu com o
sincronizador parado.

**2. Depois da instalação, quem roda o gerador?** Na instalação é o kit, antes da primeira partida (lição do ticket 02).
Depois, alguém precisa rodar de novo quando um `index.md` muda, e religar o sincronizador se a lista mudou (o LiveSync só
lê a lista ao partir).

**3. Pôr `local: true` numa pasta que já replicou** não apaga o que já está no banco nem na outra máquina. O caminho
contrário funciona sozinho: tirar o `local: true` faz a pasta replicar na próxima partida.

**4. O git.** Já está decidido que a pasta local fica fora do GitHub (glossário; faixa 10, user story 12). Falta o
jeito: o gerador ainda não escreve a exclusão do git.

Um `index.md` com YAML ilegível faz o gerador recusar tudo (não dá para saber se a pasta é local). Isso não é pergunta:
quem chama o gerador (o kit, a vigia) mostra o erro em vez de engolir; ficou anotado nos tickets 16 e 23.

## Como nasce uma pasta local
id: pasta-local-nova
tipo: escolha
recomendada: A

- A: Por um script "nova pasta local" (skill em `agents/skills/`, como a "nova iniciativa"), que para o sincronizador, cria a pasta com o `index.md` `local: true`, roda o gerador e religa; o contrato manda usar o script, e criar à mão fica sujeito ao vazamento
- B: A pasta nasce com ponto no nome (ex.: `.rascunho/`, que nunca replica), ganha o `index.md` `local: true`, o gerador roda e só então ela perde o ponto; sem parar o sincronizador, mas com um passo a mais e um nome provisório
- C: Aceitar o vazamento curto e limpar depois (o que vazou some do banco e da outra máquina na limpeza da pergunta 3)

## Quem roda o gerador depois da instalação
id: quem-roda-o-gerador
tipo: escolha
recomendada: A

- A: A vigia, a cada passada (5 min): roda o gerador; se a lista mudou, religa o sincronizador e avisa; se o gerador recusar (YAML ilegível), vira item da vigia com o caminho; é a rede de segurança para `index.md` editado à mão
- B: Só o script da pergunta 1 e o kit; um `index.md` editado à mão fica sem efeito até o próximo uso do script ou do kit
- C: Uma tarefa agendada própria, separada da vigia, só para o gerador

## Pôr `local: true` numa pasta que já replicou
id: tornar-local
tipo: escolha
recomendada: A

- A: Um passo "tornar local" no mesmo script: para o sincronizador, gera a lista e apaga a pasta do banco pelo CLI do LiveSync, o que tira a cópia da outra máquina e mantém a desta; o 08 prova que a cópia desta máquina não é apagada junto
- B: Não suportar: o verificador recusa pôr `local: true` numa pasta que já replicou e manda criar uma pasta local nova e mover os arquivos para ela
- C: Limpeza à mão, por você, quando acontecer

## Como a pasta local sai do git
id: exclusao-do-git
tipo: escolha
recomendada: A

- A: O mesmo gerador escreve `.git/info/exclude`, que vale só nesta máquina e não é versionado: cada máquina exclui as pastas locais dela, e o nome de uma pasta local não viaja para a outra nem para o GitHub
- B: O gerador escreve no `.gitignore` versionado: o nome das pastas locais das duas máquinas fica no repositório e no GitHub

## Algo mais?
id: algo-mais
tipo: texto
