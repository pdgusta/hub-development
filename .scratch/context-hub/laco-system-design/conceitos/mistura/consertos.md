# Consertos da mistura, volta 2

Uma linha por conserto de `portas/mistura-1/tech-lead.md` (seção 3) e `portas/mistura-1/ux-revisor.md`. A volta 1
ficou em `mistura-v1.html`. Fonte: `descricao/descricao-do-hub.md`, v3.2.

Conferência própria (a oficial é do QA e do UX revisor):
- `medidas-da-peca` a 320 e a 1280 px: 25 rótulos no desenho (nenhum somado), 20 ligações visíveis, 0 cruzamentos,
  folga mínima de 24,1 px (limite 21), **razão entre grupos 1,68** (era 1,53), contraste sem falha, sem rolagem lateral.
- Tab real: 19 de 19 paradas com foco visível (7 cenários, 9 bairros, 3 pessoas).
- Capturas dos cenários a 1280 x 1000, a 1280 x 720 e a 320 px (moldura de 320 px): a cidade inteira cabe com o cenário
  ligado; a 320, a faixa do desenho rola até o passo atual.

## Tech lead

| # | Conserto | Situação |
|---|---|---|
| 1 | [R5] Linha roxa Checkpoint → Nota de retomada diz que o hook grava | feito: a nota recebe a linha azul **Agentes → Nota de retomada** (quem grava); a do Checkpoint até a nota virou o traço "confere, só lê" (tracejado escuro, fino). A roxa Checkpoint → Agentes saiu do desenho e ficou na ficha (`decisoes.md`, 14). "Agente novo" 6 e "altere" 6 acendem a azul e a de conferir. |
| 2 | [R5] Ferramentas da máquina sem linha | feito, só no cenário: Maestro → Biblioteca do Maestri aparece no passo 4 do "maestro novo", por fora da cidade; na visão geral não há caminho sem cruzar (`decisoes.md`, 15). Os dois ícones do bairro viraram componentes com nome ao passar o mouse e na ficha: a caixa é a Configuração de cada ferramenta; o caderno, a Biblioteca do Maestri. |
| 3 | Cenário "maestro novo", passos 4 a 6 sem linha | feito: 4 acende Maestro → Biblioteca do Maestri, com o número no caderno; 5 acende o Acervo do maestro e a linha do maestro até ele (o registro de uso mora no acervo), com a Disciplina; 6 acende a Disciplina e **Maestro → Gustavo** (pedido de aval, só no cenário), com a frase "No Claude Code, a guarda recusa, o verificador confere e o Gustavo dá o aval". O aval sai do maestro, não do acervo (`decisoes.md`, 16). |
| 4 | Cenário "remova", passos 2 e 3 | feito: 2 acende a troca entre pares (o script lê o estado do outro par); 3 acende Agentes → Vista Markdown no tracejado "a decidir", e a frase diz que por onde o script grava está em aberto. |
| 5 | Selos da rodada 8 | feito: "não verificado: como o Obsidian chega à busca do hub" nas fichas de Portas e de Interfaces (componente e ligação); "a decidir: por onde o Desktop chega à busca" na ligação do Desktop e na Camada de busca. A linha do Obsidian à busca ficou. |
| 6 | Sentido das ligações | feito: Vista Markdown ↔ Sincronizador, Sincronizador ↔ Banco local e Banco local ↔ Outro par, na marcação e no título; a frase de "altere" 4 diz "O sincronizador (ou o plugin) escreve no disco; a vista muda em cerca de 0,2 s". |
| 7 | "O Gustavo edita" 5 e "leia" 4 sem nada novo | feito: no 5 acendem os quarteirões da vista e da busca dentro da miniatura do outro par; no 4 acende de novo Gustavo → Agentes ("o agente avisa o Gustavo"). |
| 8 | Fichas: um componente e quatro selos | feito: "Catálogo de blocos e skill nova iniciativa" na ficha de Conteúdo (dono Gustavo; aciona: agente cria a pasta pela skill; aprova: Gustavo, para mudar a skill; em curso). Selos "a decidir": proteção contra gravar dentro do `_archive/` e aviso de caminho mudado (Raiz); como o erro de uma peça que sumiu chega ao Gustavo (Acervo); o que o agente faz com a porta do banco fora (Porta do banco). |
| 9 | Fonte v3.2 | feito: `mistura.md`, `decisoes.md` e o gerador citam a v3.2; o item 10 das decisões diz "confirmada pela v3.2". |
| 10 | [R5] Vigia → Banco local lê como a vigia agindo | feito: o mesmo traço "confere, só lê" do checkpoint; a legenda diz "confere, só lê". |
| 11 | [Opcional] Marca do Claude Desktop | não feito: uma marca sem linha seria um componente solto, o defeito que este laço corrige; o Desktop fica na ficha "Quem chega" (`decisoes.md`, 20). |

## UX revisor

| # | Conserto | Situação |
|---|---|---|
| 1 | Dois roxos colados até os Agentes | feito: só um roxo chega aos Agentes (o contrato); o do checkpoint saiu (Tech lead, 1). As duas saídas do Contrato agora partem a 31 unidades uma da outra (telhado e base). |
| 2 | Último passo de falha igual aos outros | feito: o número vira um triângulo vermelho; as linhas desse passo ficam vermelhas e tracejadas, os componentes com brilho vermelho, o bairro com contorno vermelho tracejado; a faixa diz "falha ou em aberto". Vale para "edita" 6, "leia" 4, "altere" 7, "remova" 5 e "outro par" 5. |
| 3 | Passos que acendem bairro sem linha | feito em parte: "maestro novo" 4 e 6 e "remova" 2 e 3 ganharam linha (Tech lead, 2 a 4); em todos, o número vai num componente ou numa linha, não no nome do bairro. Não fiz Agentes → Periferia nem Acervo → Gustavo: a primeira não está na descrição; a segunda cruzaria a do maestro, e o aval sai do maestro (`decisoes.md`, 16 e 17). "Agente novo" 3 põe o número na nota de retomada. |
| 4 | Faixa do passo empurra o desenho | feito: com o cenário ligado, a legenda e os botões saem e a faixa fica no lugar deles, presa no alto; a cidade encolhe para caber na altura da janela. Conferido a 1280 x 720: cidade inteira na tela. |
| 5 | Legenda de 13 entradas, duas lógicas de cor | feito: duas linhas com título, "Quem aciona" (agentes, Gustavo, maestro) e "O que corre" (regras, agendador, confere, disco e banco, troca, a decidir, a construir); o maestro passou a verde-azulado, longe do roxo das regras; a vigia deixou de ter cor própria (7 tipos de traço, eram 8). |
| 6 | Halo amarelo do "a decidir" é a linha mais forte | feito: na visão geral o halo é mais claro e mais fino (9 em vez de 13); forte só quando o cenário acende o caminho. |
| 7 | Números de passo sobre nomes | feito: o número procura, em volta do componente ou ao lado da linha, um lugar a pelo menos 6 px de todo texto do desenho (apagado ou não) e dentro da tela. |
| 8 | Tracejado "a decidir" a 10 px de "Vista Markdown" | feito: o nome da vista foi 18 unidades para a direita. |
| 9 | Clique num componente abre a ficha no topo | feito: a ficha rola até o componente clicado e o realça (amarelo forte por 1 s, depois claro). O defeito vinha do foco no botão "Fechar", que rolava a ficha para cima. |
| 10 | A 320, a faixa não segue o passo | feito: a cada passo, a faixa do desenho rola até o número do passo atual, e a página desce se ele estiver fora da tela. |

## O que mudou além da lista

- O nome "Nota de retomada" foi para a direita do quadro (a linha azul chega por baixo) e o Acervo afastou-se 24
  unidades, para manter a folga.
- A legenda foi encurtada para caber em duas linhas a 1280 e a página voltar a caber em 1280 x 1000.

## Acabamento

Pedido em `brief-acabamento.md`, com os pareceres da volta 2 (`portas/mistura-2/tech-lead.md` e `ux-revisor.md`).
Nenhum rótulo novo; a ideia não mudou; a carta não foi tocada.

Conferência própria:
- `medidas-da-peca` a 320 e a 1280 px: 25 rótulos no desenho, 20 ligações visíveis, 0 cruzamentos, folga mínima 24,3 px,
  razão entre grupos 1,66, contraste sem falha, sem rolagem lateral.
- Tab real: 19 de 19 paradas com foco visível.
- Os sete cenários, do primeiro ao último passo (41 passos, a 1280 x 1000): todo passo desenha o seu número, e o número
  do passo atual fica a no máximo 16 unidades de algo aceso nele. Depois de Esc, os sete botões voltam a
  `aria-pressed="false"` e ao fundo claro. A página tem 1000 px de altura.

| Conserto | Situação |
|---|---|
| Brief 1; Tech lead 2; UX 1. Falta o número 5 em "O Gustavo edita" | feito: cada elemento de cenário leva o nome da sua chave (`data-chave`), e o número acha os quarteirões da miniatura; o 5 fica junto deles. |
| Brief 2; UX 2. Botão do cenário segue "ligado" depois de Sair ou Esc | feito: ao sair, todos os botões voltam a `aria-pressed="false"` e ao estilo normal. |
| Brief 3; UX 3. Números longe do que marcam | feito: o lugar do número é procurado em volta da forma do componente (sem o nome), a 14 ou 26 unidades; sem lugar livre, o número encosta no próprio componente, no canto mais longe do nome. Nos casos citados: o 3 de "agente novo" fica na nota, o 6 de "O Gustavo edita" junto da torre, o 5 de "maestro novo" junto do acervo. |
| Brief 4; Tech lead 1. Checkpoint → Agentes | feito, só no cenário: a linha roxa acende em "agente novo" 6 e "altere" 6, com a frase "o checkpoint cobra o agente e confere a nota; o agente a grava". O Contrato fica apagado nesses passos, como o Tech lead sugeriu. |
| UX 4. Clique no vão entre o ícone e o nome abre o bairro no topo | feito: a área de clique de cada componente é a caixa inteira (ícone e nome), sem mudar a caixa medida. Conferido no Edge: o clique no vão cai no componente (Nota de retomada, Obsidian, Sincronizador). |
| UX 5. Página com 1014 px a 1280 x 1000 | feito: menos margem embaixo do desenho e da faixa de cenários; 1000 px. |
| UX, problema 4 (menor, aceito). Linha do maestro à biblioteca contorna a cidade | não feito: é o único caminho sem cruzar, e o UX revisor aceitou o motivo (`decisoes.md`, 15). |
