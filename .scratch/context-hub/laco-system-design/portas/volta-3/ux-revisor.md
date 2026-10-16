# Parecer do UX revisor, volta 3 (fase 3, porta, a penúltima)

2026-10-15. Peças: `conceitos/volta-3/conceito-a|b|c.html`. Conferi só os consertos do meu parecer da volta 2
(`portas/volta-2/ux-revisor.md`) contra `consertos.md` e a peça, e o que eles criaram de novo. Não reabri o que já
passou.

## Como medi

- Capturas próprias (Edge via Playwright, servidas em `127.0.0.1:8795`), ao lado deste arquivo:
  `ux-captura-<a|b|c>-1280.png`, `ux-captura-<a|b|c>-320.png` (viewport real de 320, página inteira),
  `ux-olho-apertado.png`, `ux-foco-tab-maestro-<a|b|c>.png` e `ux-foco-tab-agentes-<a|b|c>.png` (pessoa focada com
  Tab real), e dois recortes ampliados: `ux-detalhe-b-periferia.png` e `ux-detalhe-c-poco.png`.
- Foco: Tab de verdade nas 10 paradas de cada conceito; para cada parada, comparei pixel a pixel a captura antes e
  depois do foco, dentro da caixa do item (+8 px).
- Números do QA (`qa/volta-3/relatorio.md`).

## Foco com Tab real: passa nas 30 paradas

| Parada | A | B | C | Volta 2 |
|---|---|---|---|---|
| 7 bairros (px que mudam) | 2.635 a 4.425 | 3.028 a 5.020 | 2.230 a 7.135 | igual |
| Agentes | 458 | 417 | 467 | 112 a 143 nas pessoas |
| Gustavo | 410 | 424 | 435 | |
| Maestro | 421 | 410 | 469 | |

As 10 paradas casam `:focus-visible` nos três. Nas pessoas, o anel escuro com fundo amarelo-claro envolve a figura e
se vê de longe (`ux-foco-tab-maestro-a.png`, `ux-foco-tab-agentes-c.png`). A contagem de pixels é menor que a dos
bairros porque a figura é pequena; o anel é a maior mudança possível ali. Passar o mouse sobre a pessoa dá o mesmo
anel (410 a 469 px). Enter abre a ficha com o foco em "Fechar"; Esc fecha e devolve o foco à pessoa.

Detalhe: em A, o anel do Maestro encosta no começo do rótulo "Maestro" (uns 2 px). Não atrapalha a leitura.

Sobre a régua de medir: o QA marcou "não verificado" pelo script, o que está certo. O campo `sem_mudanca_ao_focar`
do JSON ainda lista os 10 itens; quem ler só esse campo verá 10 falhas que não existem.

## Conferência dos consertos da volta 2

### Comum aos três

| Meu conserto | Situação | Aceito? |
|---|---|---|
| 1. [Affordance] Foco invisível nas pessoas | feito: anel escuro de 2,5 px com fundo amarelo-claro, no foco e ao passar o mouse | sim (tabela acima) |

### Conceito A

| Meu conserto | Situação | Aceito? |
|---|---|---|
| 2. [Hierarquia] Nome de Portas do par na base | feito: o nome voltou ao topo, à esquerda; "buscar" passou para cima da linha | sim |
| 3. [Composição] Vigia na ponta de caixa larga | feito: bairro estreitado até a estação | sim |
| 4. [Composição] Metade de baixo do Conteúdo vazia | feito em parte: estações 15 unidades mais baixas; o motivo (a linha do Checkpoint vem reta do bairro vizinho) é bom | sim |

Problema novo: nenhum. Razão entre grupos caiu de 2,05 para 1,96 com a Vigilância mais estreita; segue folgada.

### Conceito B

| Meu conserto | Situação | Aceito? |
|---|---|---|
| 2. [Linhas] Verde e vinho paralelos na base do Banco local | feito: a troca sai pela direita e desce entre Núcleo e Vigilância; a vigiar entra por cima | sim |
| 3. [Hierarquia] Rede privada como toco | feito: a estrada vai da muralha do par até a miniatura do Par B, na altura da rua | sim; ainda curta (uns 145 px), mas agora liga as duas cidades, que era o ponto |
| 4. [Densidade] Raiz e Obsidian com a mesma serra | feito: Raiz como seis casinhas de alturas diferentes; Obsidian como oficina de duas águas | sim; ver o problema novo 2 |
| 5. [Vista de cima] Miniatura cinza | feito: quarteirões nas cores dos bairros, a 30% | sim; no olho apertado, a miniatura agora lê como "a mesma cidade" |
| 6. [Respiro] Fora do par a 10 px da muralha | feito: 30 unidades | sim |
| 7. [Tipografia] ⊕ à direita | feito: sempre à esquerda, nos três conceitos | sim; ver o problema novo 1 |
| 8. [Densidade] Vigilância como seta | feito: torre com haste, guarita e telhado | sim |

Problemas novos:

1. **A linha verde do Obsidian ao Banco local passa por cima do nome "Periferia do par"**, entre o "P" e o "e"
   (`ux-detalhe-b-periferia.png`; também na captura de 320). Veio do conserto 7: com o ⊕ à esquerda, o nome andou
   para a direita e caiu sob a linha. Nome de bairro cortado por traço: lê, mas com esforço.
2. O Obsidian (casa de duas águas com porta e janela) e o Acervo do maestro (casa de duas águas com porta) ficaram
   com quase a mesma silhueta. Menor; a forma de cada um é assunto do Tech lead.

### Conceito C

| Meu conserto | Situação | Aceito? |
|---|---|---|
| 2. [Composição e Densidade] Maestro e Checkpoint furam andares | feito: o Checkpoint desce por um poço à direita, fora do prédio; o Maestro chega pela rua e desce pela lateral esquerda | sim; nenhum traço passa por andar onde não para, e "Porta do banco" ficou livre |
| 3. [Hierarquia] Da busca ao Conteúdo, sem caminho | feito: poço tracejado amarelo, sem rótulo, da busca até a laje do Conteúdo | sim; o olho agora desce da busca ao Conteúdo |
| 4. [Composição] Subtítulo em três linhas | feito: duas linhas | sim |

Problemas novos:

1. O traço do Checkpoint (cinza) e o da vigia (laranja) descem paralelos, a uns 25 px um do outro, por 340 px
   (`ux-detalhe-c-poco.png`). As cores se separam bem, por isso não confunde; mas é o mesmo tipo de "linha dupla"
   que pedi para desfazer em B.
2. O nome "Conteúdo" foi para a direita do bairro, porque o Acervo do maestro ocupou a esquerda. É o único bairro de
   C com o nome à direita.
3. A razão entre grupos caiu pela terceira volta seguida (1,85, 1,76, 1,69). Passa (limiar 1,5), mas é o C com menos
   margem.

## Conceito A: Linhas do hub

### Regras (só o que os consertos tocaram)

- Linhas sem se cruzar (R1): **passa**. QA 0; no olho, nenhum cruzamento novo.
- Vista mais de cima (R2): **passa**. 25 rótulos; olho apertado com sete manchas.
- Distância entre os itens (R3): **passa**. 29,5 px; razão de 1,96.
- Nomes (R4) e Papel na cidade (R5): não é do meu papel.
- Forma nova (R6): **passa**, sem mudança.

### Notas

| Dimensão | Nota | Volta 2 |
|---|---|---|
| Linhas (R1) | 5 | 5 |
| Vista de cima (R2) | 5 | 5 |
| Respiro (R3) | 5 | 5 |
| Forma nova (R6) | 4 | 4 |
| Hierarquia visual | 5 | 4 (o nome de Portas voltou ao topo) |
| Composição | 4 | 4 (Vigilância resolvida; Conteúdo ainda folgado embaixo, aceito) |
| Densidade | 5 | 5 |
| Affordance | 5 | 2 (foco nas pessoas resolvido) |
| Cor | 4 | 4 |
| Tipografia | 4 | 4 |

### Veredito: **passa**

### Consertos (pequenos, não mudam o veredito)

1. [Affordance] Maestro: o anel de foco encosta no rótulo → afastar o rótulo 6 px da figura, ou o anel 2 px para
   dentro. Evidência: `ux-foco-tab-maestro-a.png`.

## Conceito B: Duas cidades e a estrada

### Regras (só o que os consertos tocaram)

- Linhas sem se cruzar (R1): **passa**. QA 0; a troca e a vigiar não correm mais em paralelo.
- Vista mais de cima (R2): **passa**. 25 rótulos; a miniatura colorida lê como a mesma cidade.
- Distância entre os itens (R3): **passa**. 29,1 px; razão de 2,23 (a maior das três). A linha sobre o nome
  "Periferia do par" não entra na medida de R3 (é traço sobre nome de bairro, não item com item); pesa na
  tipografia.
- Nomes (R4) e Papel na cidade (R5): não é do meu papel.
- Forma nova (R6): **passa**, sem mudança.

### Notas

| Dimensão | Nota | Volta 2 |
|---|---|---|
| Linhas (R1) | 5 | 4 (verde e vinho separados) |
| Vista de cima (R2) | 5 | 4 (miniatura colorida) |
| Respiro (R3) | 5 | 4 (Fora do par afastada) |
| Forma nova (R6) | 5 | 5 |
| Hierarquia visual | 4 | 4 (a estrada aparece; ainda curta) |
| Composição | 4 | 4 |
| Densidade | 4 | 4 (torre e casinhas boas; Obsidian e Acervo parecidos) |
| Affordance | 5 | 2 |
| Cor | 4 | 4 |
| Tipografia | **3** | 4 (a linha verde corta o nome "Periferia do par") |

### Veredito: **passa** (nenhuma dimensão abaixo de 3). O conserto 1 é pequeno e eu o faria antes da carta: um nome
de bairro cortado por linha é o tipo de coisa que o Gustavo vê no primeiro olhar.

### Consertos

1. [Tipografia] Periferia do par: a linha verde do Obsidian ao Banco local passa sobre o "e" do nome → mover o nome
   para a base da caixa, à esquerda (embaixo do Obsidian não há traço), ou fazer a linha descer pela direita da
   oficina. Evidência: `ux-detalhe-b-periferia.png`.
2. [Densidade] Obsidian e Acervo do maestro com a mesma casa → dar ao Acervo a forma de armazém (porta larga de
   galpão, sem janela) e deixar a casa de janela para a oficina. Combinar com o Tech lead, que julga o papel.

## Conceito C: A cidade em corte

### Regras (só o que os consertos tocaram)

- Linhas sem se cruzar (R1): **passa**. QA 0; no olho, nenhum cruzamento. Checkpoint e vigia descem em paralelo,
  em cores distintas.
- Vista mais de cima (R2): **passa**. 25 rótulos; no olho apertado, cada andar é uma faixa e as verticais não
  costuram mais o prédio por dentro.
- Distância entre os itens (R3): **passa**. 28,9 px; razão de 1,69 (em queda, ainda acima de 1,5).
- Nomes (R4) e Papel na cidade (R5): não é do meu papel.
- Forma nova (R6): **passa**, sem mudança.

### Notas

| Dimensão | Nota | Volta 2 |
|---|---|---|
| Linhas (R1) | 4 | 4 (saíram os furos de andar; entrou o paralelo cinza e laranja) |
| Vista de cima (R2) | 5 | 4 (o prédio ficou limpo por dentro) |
| Respiro (R3) | 4 | 4 (razão em queda) |
| Forma nova (R6) | 5 | 5 |
| Hierarquia visual | 5 | 4 (o poço da busca dá o caminho até o Conteúdo) |
| Composição | 4 | 3 (verticais por fora do prédio; subtítulo em duas linhas) |
| Densidade | 4 | 3 |
| Affordance | 5 | 2 |
| Cor | 4 | 4 |
| Tipografia | 4 | 4 (o nome "Conteúdo" à direita quebra o padrão) |

### Veredito: **passa**

### Consertos (pequenos, não mudam o veredito)

1. [Linhas (R1)] Checkpoint e vigia em paralelo, a 25 px → levar o poço do Checkpoint colado à parede do prédio
   (10 px dela) e a linha da vigia pelo meio do vão até a Periferia, para abrir uns 50 px entre os dois. Evidência:
   `ux-detalhe-c-poco.png`.
2. [Tipografia] Conteúdo com o nome à direita → pôr o nome à esquerda, em cima do Acervo do maestro, e o rótulo
   do Acervo logo abaixo do nome do bairro.

## Onde cada um é melhor (sem ranking)

- **A**, em densidade e vista de cima: a mais leve e a que menos mudou para ficar certa.
- **B**, em respiro e forma nova: a maior razão entre grupos (2,23) e a cidade que se lê sem legenda.
- **C**, em hierarquia: a altura diz a distância até a verdade, e agora o caminho da busca até o Conteúdo se vê.

## Não verificado

- Larguras 768 e 1920 com o olho (ficam os números do QA).
- Leitor de tela.
