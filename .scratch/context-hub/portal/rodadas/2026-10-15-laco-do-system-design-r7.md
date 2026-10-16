---
titulo: O que você faz na prática
ticket: 56
aberta: 2026-10-15
estado: absorvida
---

A descrição nova do hub está escrita (`laco-system-design/descricao/descricao-do-hub.md`), e agora ela passa pelo
teste das perguntas escondidas. O Tech lead não inventou o que só você sabe: são 14 perguntas sobre a sua prática, que
as fontes não dizem. Responda as que quiser, com poucas palavras; a que ficar em branco segue marcada "a decidir com o
Gustavo". Abrir a explicação de cada pergunta mostra por que ela muda o desenho.

## Suas máquinas ficam ligadas juntas no dia a dia? Você desliga, hiberna ou fecha o notebook à noite e fora do expediente?
id: g1
tipo: texto

a troca entre os bancos só acontece com as duas ligadas. Isso define quanto tempo uma mudança espera, quão frequente é "a outra máquina desligada" e quanto cresce o risco de colisão. A fonte só diz que elas "costumam ficar ligadas juntas".

## Quando você pede a um agente para ler, alterar ou remover algo do hub, por onde pede no dia a dia: Claude Code na raiz, um workspace do Maestri, o Claude Desktop, o VS Code, outro?
id: g2
tipo: texto

a porta principal no desenho é a sessão na raiz. Se a sua prática é outra, os cenários e o diagrama de "quem chega" mudam de centro.

## Quando você cria uma nota nova no Obsidian, onde ela deve nascer: em `inbox/`, na pasta da iniciativa aberta, ou onde você clicar?
id: g3
tipo: texto

o Obsidian tem uma pasta padrão para nota nova; o hub não decidiu qual. Nota solta sem lugar vira órfã, que é o que o hub quer evitar.

## "Remova isto" para você quer dizer apagar ou arquivar? E quem decide que uma iniciativa terminou e roda a mudança para o `_archive/`: você, ou o agente quando percebe?
id: g4
tipo: texto

apagar viaja às duas máquinas em segundos e só volta pela cópia do dia; arquivar é um script que confere a outra máquina antes. O cenário "pedir para remover" depende disso.

## Você costuma editar no Obsidian uma nota que um agente está trabalhando ao mesmo tempo?
id: g5
tipo: texto

essa edição concorrente está fora do escopo e sem proteção. Se acontece com frequência, ela volta a pesar no desenho.

## Você aceita que conteúdo de cliente vá para o repositório privado do GitHub na cópia diária, e para os modelos na nuvem que os agentes usam? Há iniciativa de cliente que não pode?
id: g6
tipo: texto

a cópia diária leva toda a vista, inclusive cliente; isso decorre da decisão, mas não foi discutido em separado. Uma resposta "não" cria uma exclusão no git ou uma pasta fora do hub.

## Que arquivos que não são texto (docx, xlsx, imagem, PDF) você edita nas duas máquinas?
id: g7
tipo: texto

na colisão de binário o hub fica com o mais novo sem perguntar, e só a vigia avisa. Se você edita planilhas nas duas, esse caso deixa de ser raro.

## Quem usa hoje um computador sem cópia do hub: só você numa sandbox ou máquina de passagem, ou também agentes de outras pessoas? Com que frequência?
id: g8
tipo: texto

o cliente foi desenhado (porta de leitura, chave temporária), mas sem uso conhecido. A resposta diz se ele entra no diagrama principal ou fica na borda.

## Onde você quer ver um aviso do hub quando está só no Obsidian, sem sessão de agente aberta? A notificação do Windows basta?
id: g9
tipo: texto

hoje os avisos são a notificação, o estado na tela do agente e a checagem de sessão. Quem só usa o Obsidian pode não ver nada além da notificação.

## Quantos agentes costumam trabalhar ao mesmo tempo na mesma iniciativa, na mesma máquina?
id: g10
tipo: texto

é o caso mais comum de edição concorrente dentro de uma máquina. A guarda de versão cobre a porta do banco, mas não a gravação direta no disco, que ainda está em aberto.

## Quem cuida da operação: montar uma máquina nova, revogar a chave de uma máquina devolvida, responder um aviso, religar o que parou? Você mesmo, ou um agente com você vendo?
id: g11
tipo: texto

as fontes dizem o que pode ser feito, não quem faz. A matriz de responsabilidade fica com buracos sem isso.

## Em que situação você ligaria os embeddings do Google na busca?
id: g12
tipo: texto

ligado, o texto indexado vai ao Google e a busca por sentido passa a depender da rede e da cota. O gatilho não foi decidido.

## O que você pede ao Claude Desktop sobre o hub: só perguntas, ou também alterações em notas?
id: g13
tipo: texto

como o Desktop grava está em aberto. Se é só leitura na prática, o caminho fica simples; se altera, precisa da guarda de versão.

## Você quer chegar ao hub pelo celular ou pela web?
id: g14
tipo: texto

hoje nenhum dos dois alcança a rede privada. Seria uma porta nova, com outro caminho de rede.

## Algo mais?
id: algo-mais
tipo: texto
