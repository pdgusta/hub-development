# Parecer do UX revisor, volta 2 (fase 3, porta)

2026-10-15. Peças: `conceitos/volta-2/conceito-a|b|c.html`. Roteiro: `regua-da-cidade/como-julgar.md`. Conferi
primeiro os consertos do meu parecer da volta 1 contra `consertos.md` e a peça; depois julguei de novo.

## Como medi

- Capturas próprias (Edge via Playwright, servidas em `127.0.0.1:8794`), ao lado deste arquivo:
  - `ux-captura-<a|b|c>-1280.png` (visão geral) e `ux-captura-<a|b|c>-320.png` (viewport real de 320, página
    inteira);
  - `ux-olho-apertado.png`: as três de 1280 reduzidas a 320 px e borradas;
  - `ux-foco-tab-<a|b|c>.png`: depois de dois Tab reais; `ux-foco-tab-pessoa-<a|b|c>.png`: com o foco no último
    item (uma pessoa); `ux-ficha-<a|b|c>.png`: Enter no item focado.
- Números do QA (`qa/volta-2/relatorio.md`), conferidos no olho.

## Foco com Tab real: passa nos bairros, falha nas pessoas (os três)

Percorri com Tab de verdade os 10 itens focáveis de cada conceito (7 bairros e 3 pessoas). Os 10 casam
`:focus-visible` nos três. Para ver se o desenho muda, comparei pixel a pixel a captura antes e depois de cada foco,
dentro da caixa do item:

| Item | A | B | C | O que se vê |
|---|---|---|---|---|
| bairros (7) | 2.637 a 4.431 px mudam | 3.032 a 5.025 | 2.251 a 7.146 | o contorno do bairro escurece e engrossa (1,6 para 3,5 px): **visível** |
| Agentes, Gustavo, Maestro | 112 a 143 px | 133 a 136 | 114 a 132 | quase nada: **não visível** |

Por quê: a regra `.pessoa:focus-visible .corpo` pinta o contorno com `--tinta`, a mesma cor do preenchimento do
corpo (`.corpo{fill:var(--tinta)}`). O boneco só engorda 1,25 px de cada lado. Ver `ux-foco-tab-pessoa-a.png`: o
Maestro está focado e nada o distingue. Ao passar o mouse, acontece o mesmo nas pessoas; nos bairros, o realce
funciona.

**Falha de foco visível em 3 dos 10 itens, nos três conceitos.** Já era assim na volta 1. Lá escrevi "não testei o
foco nas pessoas", e o erro passou por mim. Fica registrado.

O resto do teclado segue certo: Enter abre a ficha e leva o foco a "Fechar"; Esc fecha e devolve o foco ao item.

## Rótulos em 25: a visão geral ficou mais carregada?

Os dois rótulos novos (o nome de buscar e o de gravar sobre os traços) e o sinal ⊕ nos sete bairros:

- **A:** não ficou mais carregada. O olho apertado segue com sete manchas limpas; os nomes das linhas são pequenos,
  em itálico, na cor da linha, e não competem com os nomes dos itens.
- **B:** um pouco mais de tinta, mas sem perder leitura. Os ícones novos (prefeitura, oficina, quarteirão de Raiz)
  entraram no lugar de caixas vazias. O que mais pesa ainda é a miniatura do Par B: blocos cinza sem nome.
- **C:** **sim, ficou mais carregada, mas pelas linhas, não pelos rótulos.** Com o Conteúdo no subsolo, cinco traços
  longos atravessam o prédio de cima a baixo (Maestro, Checkpoint, gravar, vigiar, editar). Dois deles (Maestro e
  Checkpoint) passam pelos andares da Disciplina e das Portas sem parar ali. No olho apertado, os andares se separam
  (as lajes resolveram), mas as verticais costuram a torre.

Folga de rótulos: com 25, qualquer rótulo a mais falha a vista de cima. O que entrar daqui em diante tem que ir para
a ficha ou trocar de lugar com um que sai.

## Conferência dos consertos da volta 1

### Comuns aos três

| Meu conserto | Situação | Aceito? |
|---|---|---|
| Cor: três azuis vizinhos | feito: disco e banco pontilhada cinza-azulada, gravar marinho escuro, nomes de buscar e gravar sobre o traço | sim |
| Affordance: nada diz que o bairro abre | feito: ⊕ no nome, realce ao passar o mouse, legenda em tinta e negrito | sim, nos bairros; nas pessoas, ver o foco acima |
| Tipografia: nome de bairro em 11 px, caixa alta | feito de outro jeito: 14 px semibold, caixa normal | sim; lê melhor que a caixa alta pedida |
| 320 px: rótulos cortados, sem o Banco local | feito: a faixa abre no Banco local, com degradê nas bordas | sim (`ux-captura-<a|b|c>-320.png`: o Banco local aparece nos três) |

### Conceito A

| Meu conserto | Situação | Aceito? |
|---|---|---|
| 1. Rede privada e Par B a 23,5 px | feito: 31 px; a menor folga agora é 29,5 px | sim |
| 2. Rede privada em pé | feito: trilho deitado, com dormentes | sim |
| 3. Nome do Núcleo encostado na Vista Markdown | feito: o nome subiu para o topo | sim; efeito colateral: o nome "Portas do par" desceu para a base da caixa (único bairro com o nome embaixo) |
| 4. Só caixas arredondadas | feito em parte: baldeação de anel duplo, trilho, terminal; os bairros seguem caixas | sim |
| 5. Buscar longe do Conteúdo | feito: a estação fica na borda comum de Portas e Conteúdo | sim |
| 6 a 9 | ver comuns | sim |

### Conceito B

| Meu conserto | Situação | Aceito? |
|---|---|---|
| 1. Dois verdes paralelos até o Obsidian | feito: o Gustavo chega pela esquerda | sim; problema novo: agora o verde do Obsidian e a troca (vinho) descem da base do Banco local lado a lado, a 22 px |
| 2. Outra cidade ocupa um terço | feito: miniatura a 40%, muralha maior | sim |
| 3. Núcleo e Vigilância a 15 px | feito: 40 unidades | sim |
| 4. Nomes de pessoa encostam nas linhas | feito: nome acima, trecho reto antes de virar | sim |
| 5. Caixas vazias e seis telhados soltos | feito: prefeitura, oficina, quarteirão de Raiz | sim; problema novo: Raiz (dentes de serra) e Obsidian (oficina de telhado em serra) ficaram com a mesma silhueta |
| 6. "Rede privada" em pé | feito: deitada, nome embaixo | sim; problema novo: a estrada virou um toco de 105 px dentro de Fora do par, o menor desenho da tela, embora o subtítulo diga "ligadas pela estrada da rede privada" |
| 7 a 9 | ver comuns | sim |

### Conceito C

| Meu conserto | Situação | Aceito? |
|---|---|---|
| 1. Vigiar e editar em L encaixados | feito: vigiar entra por cima, editar pela direita | sim |
| 2. Andares encostados | feito: lajes de 45 a 50 unidades | sim; no olho apertado cada andar é uma faixa |
| 3. "Sincronizador" perto do nome do bairro | feito | sim |
| 4. Linha da vigia longa | feito em parte: a Vigilância foi para o alto, à direita; a linha segue longa porque o cofre desceu | sim, com o motivo dado (a vigia olha de cima; o cofre desceu por pedido do Tech lead) |
| 5. Disciplina com um item numa faixa larga | feito de outro jeito: andar mais baixo, sem salas sem nome | sim; o motivo (sem formas soltas) é da régua |
| 6 a 8 | ver comuns | sim |

## Conceito A: Linhas do hub

### Regras

- Linhas sem se cruzar (R1): **passa**. Evidência: QA 0; no olho, nenhum cruzamento. Vigiar e troca saem do lado
  direito do Banco local a 28 px um do outro, em cores bem distintas; leem como duas linhas.
- Vista mais de cima (R2): **passa**. Evidência: 25 rótulos (no limite); olho apertado com sete manchas separadas;
  não ficou mais carregada.
- Distância entre os itens (R3): **passa**. Evidência: 29,5 px de folga mínima contra 21 px; razão de 2,05 (era
  1,81).
- Nomes (R4): não é do meu papel.
- Papel na cidade (R5): não é do meu papel.
- Forma nova (R6): **passa**. Evidência: mapa de linhas, sem centro nem anéis; o Banco local como baldeação, a rede
  privada como trilho e o Par B como terminal agora dão lugar à metáfora.

### Notas

| Dimensão | Nota | Por quê |
|---|---|---|
| Linhas (R1) | 5 | nenhum cruzamento, saídas distintas |
| Vista de cima (R2) | 5 | sete manchas; os nomes novos não competem |
| Respiro (R3) | 5 | a menor folga subiu para 29,5 px; razão de 2,05 |
| Nomes (R4) | não é do meu papel | |
| Papel na cidade (R5) | não é do meu papel | |
| Forma nova (R6) | 4 | os bairros seguem caixas (é o fundo do mapa; aceito) |
| Hierarquia visual | 4 | o Banco local e a linha grossa de buscar puxam o olho, certo; "Portas do par" com o nome embaixo quebra o padrão |
| Composição | 4 | a Vigilância é uma caixa grande com uma estação na ponta direita; o Conteúdo tem a metade de baixo vazia |
| Densidade | 5 | a mais leve dos três |
| Affordance | **2** | foco invisível nas três pessoas (ver acima); nos bairros, bom |
| Cor | 4 | os azuis se separam; troca, vigiar e editar ainda só pela cor, mas são cores distintas |
| Tipografia | 4 | nomes de bairro bons; os nomes de linha em itálico pequeno ficam no limite do miúdo |

### Veredito: **volta** (Affordance em 2, abaixo de 3)

### Consertos

1. [Affordance] As três pessoas: o contorno de foco é da mesma cor do corpo → ao focar ou passar o mouse, desenhar um
   anel em volta da figura (círculo ou retângulo arredondado, traço `--tinta` de 2,5 px, 4 px afastado do boneco),
   ou trocar o preenchimento do corpo para a cor de destaque. Evidência: `ux-foco-tab-pessoa-a.png`; 112 a 143 px
   mudam, contra 2.637 ou mais nos bairros.
2. [Hierarquia] Portas do par: o nome desceu para a base da caixa → voltar o nome ao topo, do lado esquerdo, e
   deixar buscar entrar pela borda de cima à direita dele. Ou manter embaixo, mas então pôr todos os nomes de bairro
   no mesmo canto.
3. [Composição] Vigilância: a Vigia do sync fica na ponta direita de uma caixa larga → estreitar o bairro até a
   estação, ou centralizar a estação e deixar a linha descer pelo lado direito do Núcleo como hoje.
4. [Composição] Conteúdo: a metade de baixo da caixa fica vazia depois que ela desceu até a busca → aceitável (a
   borda comum é a ideia); se der, subir as duas estações para o meio da caixa.

## Conceito B: Duas cidades e a estrada

### Regras

- Linhas sem se cruzar (R1): **passa**. Evidência: QA 0; no olho, nenhum cruzamento. Problema novo: o verde
  (Obsidian ao Banco local) e o vinho (troca) descem da base do Banco local em paralelo, a 22 px, até a rua.
- Vista mais de cima (R2): **passa**. Evidência: 25 rótulos (no limite); no olho apertado, os bairros se separam e a
  Vigilância já não se funde com o Núcleo. A miniatura do Par B segue como um bloco claro sem nome.
- Distância entre os itens (R3): **passa**. Evidência: 29,1 px; razão de 2,03 (era 1,80). Fora do par fica a 10 px
  da muralha.
- Nomes (R4): não é do meu papel.
- Papel na cidade (R5): não é do meu papel.
- Forma nova (R6): **passa**. Evidência: a planta com muralha, portão, prefeitura, oficina e a outra cidade em
  miniatura segue o mais "cidade" dos três.

### Notas

| Dimensão | Nota | Por quê |
|---|---|---|
| Linhas (R1) | 4 | sem cruzamento; verde e vinho paralelos na saída do Banco local |
| Vista de cima (R2) | 4 | a miniatura cinza do Par B ainda ocupa um quarto da vista sem nome |
| Respiro (R3) | 4 | Fora do par a 10 px da muralha |
| Nomes (R4) | não é do meu papel | |
| Papel na cidade (R5) | não é do meu papel | |
| Forma nova (R6) | 5 | o par como cidade, a outra igual a ele |
| Hierarquia visual | 4 | o núcleo voltou ao centro do olhar; a estrada, que dá nome ao conceito, quase some |
| Composição | 4 | equilibrada; o lado direito ainda pesa pela área clara |
| Densidade | 4 | os ícones novos trocaram caixas vazias por formas com sentido |
| Affordance | **2** | foco invisível nas três pessoas |
| Cor | 4 | como em A |
| Tipografia | 4 | como em A; ⊕ à direita em Periferia e Fora do par, à esquerda nos outros |

### Veredito: **volta** (Affordance em 2, abaixo de 3)

### Consertos

1. [Affordance] As três pessoas: igual ao conserto 1 de A. Evidência: `ux-foco-tab-pessoa-b.png`.
2. [Linhas (R1)] Base do Banco local: verde e vinho descem lado a lado → tirar a troca pelo lado direito do Banco
   local (em direção à Vigilância e depois à rua), ou fazer o verde subir do Obsidian pela esquerda da caixa.
   Evidência: `ux-captura-b-1280.png`.
3. [Hierarquia] Rede privada: um toco de 105 px dentro de Fora do par → fazer a estrada ir de muralha a muralha (da
   saída do par até a miniatura do Par B), na altura da rua, com o nome embaixo: é o elemento que dá nome ao
   conceito.
4. [Densidade] Raiz e Obsidian com a mesma silhueta de dentes de serra → manter a serra só na oficina (Obsidian) e
   dar à Raiz seis telhados de duas águas lado a lado, ou casas de alturas diferentes.
5. [Vista de cima (R2)] Miniatura do Par B: blocos cinza sem nome → tingir de leve os quarteirões com as cores dos
   bairros do par (a 30%), para ler "a mesma cidade" sem rótulo novo.
6. [Respiro (R3)] Fora do par a 10 px da muralha → abrir 30 px ou mais.
7. [Tipografia] O ⊕ fica à direita em Periferia e Fora do par → pôr o sinal sempre antes do nome, à esquerda.
8. [Densidade] Vigilância: a seta para cima lê como "enviar", não como torre de vigia → desenhar uma torre (haste e
   guarita) ou um olho no alto. Não é novo; não pedi na volta 1.

## Conceito C: A cidade em corte

### Regras

- Linhas sem se cruzar (R1): **passa**. Evidência: QA 0; no olho, nenhum cruzamento. Mas as linhas do Maestro e do
  Checkpoint atravessam andares onde não param (Disciplina e Portas), e a do Maestro passa a uns 20 px do fim do
  rótulo "Porta do banco".
- Vista mais de cima (R2): **passa**. Evidência: 25 rótulos (no limite); no olho apertado, cada andar é uma faixa
  própria (as lajes resolveram). É a única das três que ficou mais carregada, pelas cinco verticais longas.
- Distância entre os itens (R3): **passa**. Evidência: 28,9 px (era 34,1); razão de 1,76 (era 1,85), as duas acima
  do limiar e as duas em queda.
- Nomes (R4): não é do meu papel.
- Papel na cidade (R5): não é do meu papel.
- Forma nova (R6): **passa**. Evidência: o corte com a chave "mais fundo, mais perto da verdade" agora vale para
  todos os andares.

### Notas

| Dimensão | Nota | Por quê |
|---|---|---|
| Linhas (R1) | 4 | sem cruzamento; duas linhas atravessam andares sem parar |
| Vista de cima (R2) | 4 | andares separados; verticais costuram a torre |
| Respiro (R3) | 4 | folga e razão caíram; Maestro a 20 px de "Porta do banco" |
| Nomes (R4) | não é do meu papel | |
| Papel na cidade (R5) | não é do meu papel | |
| Forma nova (R6) | 5 | a altura carrega sentido de cima a baixo |
| Hierarquia visual | 4 | o cofre no fundo puxa o olho, certo; de buscar até o Conteúdo, o olho não tem caminho (a linha para no térreo e o Conteúdo fica dois andares abaixo) |
| Composição | 3 | cinco verticais longas cortam a torre; o subtítulo virou três linhas e empurra a legenda |
| Densidade | 3 | com o mesmo número de rótulos, é a que mais traço pede para ler |
| Affordance | **2** | foco invisível nas três pessoas |
| Cor | 4 | como em A |
| Tipografia | 4 | como em A |

### Veredito: **volta** (Affordance em 2, abaixo de 3)

### Consertos

1. [Affordance] As três pessoas: igual ao conserto 1 de A. Evidência: `ux-foco-tab-pessoa-c.png`.
2. [Composição e Densidade] Linhas do Maestro e do Checkpoint atravessam Disciplina e Portas → levá-las por um poço
   à direita do prédio (fora das salas, como um elevador de serviço), descendo junto da parede. Assim nenhum traço
   passa por andar onde não para, e o rótulo "Porta do banco" fica livre.
3. [Hierarquia] De buscar ao Conteúdo: a linha termina no térreo e o Conteúdo está dois andares abaixo → puxar da
   Camada de busca um trecho claro (como a rua clara de B) descendo até o andar do Conteúdo, sem rótulo novo. O
   lugar da busca segue "a decidir"; o trecho só mostra o caminho.
4. [Composição] Subtítulo em três linhas → cortar para duas: "Vista de lado: quanto mais fundo, mais perto da
   verdade. O conteúdo mora no subsolo, junto do cofre." O resto vai para a ficha.

## Onde cada um é melhor (sem ranking)

- **A**, em respiro e vista de cima: a maior razão entre grupos (2,05) e o olho apertado mais limpo.
- **B**, em forma nova: é a cidade que se lê sem legenda, com a outra cidade igual.
- **C**, em hierarquia de sentido: a altura diz a distância até a verdade, e agora vale para todos os andares.

## Não verificado

- Larguras 768 e 1920 com o olho; ficam os números do QA.
- Leitor de tela (só conferi que todo item focável tem nome, pelo QA).

## Para a régua de medir (aviso ao maestro)

A `medidas-da-peca` deixou passar a falha das pessoas nas duas voltas. Na volta 1 ela marcou "falha" pelo motivo
errado (foco por script); na volta 2 marcou "não verificado". Sugestão: com Tab real (tecla, não `.focus()`),
comparar os pixels da caixa do item antes e depois do foco, com um limiar mínimo (por exemplo, 1% da área ou 300 px).
Isso pegaria o caso tinta sobre tinta.
