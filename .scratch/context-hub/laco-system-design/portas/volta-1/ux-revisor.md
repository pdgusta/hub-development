# Parecer do UX revisor, volta 1 (fase 3, porta)

2026-10-15. Peças: `conceitos/volta-1/conceito-a|b|c.html`. Roteiro: `regua-da-cidade/como-julgar.md`. Olhei antes as
referências (mapa de metrô e mesa de mapas elogiados; cidade radial v2 recusada por poluição e falta de distância).

## Como medi

- Capturas próprias, Edge sem cabeça, servidas em `127.0.0.1:8793`:
  - `ux-captura-<a|b|c>-1280.png`: visão geral, 1280 x 1000;
  - `ux-captura-<a|b|c>-320.png`: 320 px de viewport real (Edge via Playwright; o `--window-size=320` do Edge sem
    cabeça não desce a 320 e cortava a página, por isso refiz);
  - `ux-olho-apertado.png`: as três de 1280 reduzidas a 320 px e borradas (teste do olho apertado);
  - `ux-foco-tab-<a|b|c>.png`: depois de dois Tab reais; `ux-ficha-<a|b|c>.png`: Enter no bairro focado.
- Números de cruzamentos, rótulos e folga: do relatório do QA (`qa/volta-1/relatorio.md`), conferidos no olho.

## Foco visível com Tab real (a falha do QA)

**Não se confirma.** Com tecla Tab de verdade (Playwright, Edge), os três conceitos casam `:focus-visible` em todos os
bairros testados, e o contorno do bairro muda para tinta escura, 3,5 px (ver `ux-foco-tab-a.png`: Conteúdo com borda
preta). O QA deu o foco por script, que não liga `:focus-visible`; por isso não viu mudança.

De quebra, com teclado: Enter abre a ficha e o foco vai para "Fechar"; Esc fecha e o foco volta ao bairro de origem.
Os três iguais. Não testei o foco nas pessoas (a regra `.pessoa:focus-visible .corpo` existe no código).

## O que vale para os três (mesmo acabamento)

Os três dividem cabeçalho, legenda, cores de bairro, fonte e ficha. Por isso cor, tipografia e affordance têm as
mesmas notas e os mesmos consertos (6 a 9 da lista de cada um).

- **Cor:** o tipo de cada linha só se sabe pela cor e pela legenda. Buscar, gravar e disco e banco são três azuis
  vizinhos (petróleo, marinho, azul claro); só buscar é mais grossa. Nenhuma linha tem nome no desenho.
- **Affordance:** nada no desenho diz que o bairro abre: a dica "Clique num bairro para abrir a ficha" fica no fim da
  legenda, em cinza pequeno. As estações parecem clicáveis, mas o clique abre o bairro, não a estação.
- **Tipografia:** rótulos em 14 px com bom peso (perto da mesa de mapas elogiada). Legenda e subtítulo em 12 a 14 px
  cinza, mais fracos. Nomes de bairro em caixa alta, 11 px, espaçados: leem, mas são o texto mais miúdo do desenho.
- **320 px:** não há rolagem da página (confere com o QA). O desenho vira uma faixa que se arrasta, mais a lista dos
  bairros embaixo. Mas a primeira vista corta rótulos no meio ("Nota de retom", "Acervo", "Maestr") e o Banco local
  não aparece em nenhum dos três. Só o texto avisa que dá para arrastar.

## Conceito A: Linhas do hub

### Regras

- Linhas sem se cruzar (R1): **passa**. Evidência: QA 0; no olho, nenhum traço cruza outro. A troca entre pares
  atravessa a rede privada desenhada em pé, de lado a lado, o que parece uma barreira, mas não é cruzamento.
- Vista mais de cima (R2): **passa**. Evidência: 23 rótulos no desenho; no olho apertado, os sete bairros são
  manchas separadas, com o ar mais limpo dos três.
- Distância entre os itens (R3): **passa**. Evidência: folga mínima de 23,5 px contra 21 px (Rede privada e Par B,
  a menor margem dos três); razão de 1,81. No olho, "Vista Markdown" fica a 25 px do nome do bairro "Núcleo de dados
  do par" e os dois se leem quase como uma linha só.
- Nomes (R4): não é do meu papel.
- Papel na cidade (R5): não é do meu papel.
- Forma nova (R6): **passa**. Evidência: o teste de troca de acabamento não se aplica entre eles (os três já
  dividem o acabamento); o que muda é a disposição. A é um mapa de linhas, sem centro nem anéis, e não repete
  nenhuma forma recusada. Ressalva: dos três, é o que menos parece uma cidade: com caixas e linhas, lê como diagrama
  de arquitetura com cores de metrô.

### Notas

| Dimensão | Nota | Por quê |
|---|---|---|
| Linhas (R1) | 5 | nenhum cruzamento; linhas retas a 45° |
| Vista de cima (R2) | 5 | 23 rótulos; sete manchas no olho apertado |
| Respiro (R3) | 4 | passa por pouco no par da rede privada; "Vista Markdown" encosta no nome do bairro |
| Nomes (R4) | não é do meu papel | |
| Papel na cidade (R5) | não é do meu papel | |
| Forma nova (R6) | 4 | outra disposição, mas pouco de cidade no desenho |
| Hierarquia visual | 4 | o olho vai ao Banco local (pílula preta) e à linha grossa de buscar; certo |
| Composição | 4 | equilibrada; a rede privada de pé, perpendicular à troca, quebra o fluxo; 150 px vazios embaixo |
| Densidade | 5 | a mais leve dos três |
| Affordance | 3 | ver "o que vale para os três" |
| Cor | 3 | ver "o que vale para os três" |
| Tipografia | 4 | ver "o que vale para os três" |

### Veredito: **passa** (na minha parte: R1, R2, R3 e R6 em "passa"; nenhuma dimensão abaixo de 3)

### Consertos

1. [Respiro (R3)] Fora do par, entre a rede privada e o Par B: 23,5 px, 2,5 px acima do limiar → afastar o Par B
   uns 15 px ou estreitar a rede privada. Evidência: relatório do QA, folga mínima.
2. [Composição] Fora do par: a rede privada está desenhada em pé e a linha de troca a atravessa → deitar a rede
   privada ao longo da linha de troca (como em C), para ler como o trilho por onde a troca passa. Evidência:
   `ux-captura-a-1280.png`.
3. [Respiro (R3)] Núcleo de dados: "Vista Markdown" a 25 px do nome do bairro → subir o nome do bairro para o topo
   da caixa, como nos outros bairros. Evidência: captura de 1280.
4. [Forma nova (R6)] O desenho todo: só caixas arredondadas → dar ao menos ao Banco local, à rede privada e ao Par B
   uma forma de lugar (baldeação grande, trilho, terminal) para a metáfora aparecer sem legenda.
5. [Hierarquia] Camada de busca: o subtítulo diz que buscar "termina na porta do conteúdo", mas a linha para dentro
   de Portas do par, longe do bairro Conteúdo → encostar a estação à borda do Conteúdo ou puxar um trecho claro até
   ele (como a rua clara de B).
6. [Cor] Legenda e linhas: buscar, gravar e disco e banco são três azuis próximos → separar gravar em tom ou
   tracejado e pôr o nome curto da linha uma vez sobre cada traço (buscar, gravar), sem depender só da legenda.
7. [Affordance] Bairros: a dica de clique está no fim da legenda, em cinza → mostrar no desenho que o bairro abre
   (canto com "abrir" ou ícone discreto no nome do bairro, e realce do contorno ao passar o mouse, igual ao do foco).
8. [Tipografia] Nomes de bairro em 11 px, caixa alta → subir para 12 a 13 px, peso semibold; legenda de 12 para
   13 px, em tinta mais escura.
9. [320 px] A faixa abre na ponta esquerda, com rótulos cortados e sem o Banco local → abrir a faixa já rolada até o
   Banco local, ou mostrar o desenho inteiro reduzido como mapa de bolso, e um degradê na borda que mostre que há
   mais à direita. Evidência: `ux-captura-a-320.png`.

## Conceito B: Duas cidades e a estrada

### Regras

- Linhas sem se cruzar (R1): **passa**. Evidência: QA 0; no olho, nenhum cruzamento. Mas a linha do Gustavo e a do
  Obsidian ao Banco local descem em dois verdes paralelos, a 30 px um do outro, até o mesmo prédio: parecem uma linha
  dupla.
- Vista mais de cima (R2): **passa**. Evidência: 23 rótulos. No olho apertado, os bairros se separam, mas a "outra
  cidade" (Par B) vira um bloco grande de retângulos cinza sem nome. E Núcleo de dados e Vigilância quase se fundem
  (15 px entre as caixas).
- Distância entre os itens (R3): **passa**. Evidência: 29,1 px de folga mínima (Sincronizador e Banco local), razão
  de 1,80. No olho: "Agentes" e "Gustavo" encostam no começo das próprias linhas.
- Nomes (R4): não é do meu papel.
- Papel na cidade (R5): não é do meu papel.
- Forma nova (R6): **passa**. Evidência: planta com muralha, quarteirões, estrada e uma segunda cidade igual. Muda a
  pergunta do leitor para "onde mora isso?" e não repete forma recusada.

### Notas

| Dimensão | Nota | Por quê |
|---|---|---|
| Linhas (R1) | 4 | sem cruzamento; os dois verdes paralelos confundem |
| Vista de cima (R2) | 4 | a outra cidade e os seis telhados de Raiz enchem a vista sem rótulo |
| Respiro (R3) | 4 | Núcleo e Vigilância coladas; rótulos de pessoa encostam na linha |
| Nomes (R4) | não é do meu papel | |
| Papel na cidade (R5) | não é do meu papel | |
| Forma nova (R6) | 5 | o mais "cidade" dos três; o Par B igual a este se vê sem legenda |
| Hierarquia visual | 3 | um terço da tela é o Fora do par quase vazio, que puxa o olho antes do núcleo |
| Composição | 3 | peso à direita sem conteúdo; a muralha aperta os bairros à esquerda |
| Densidade | 4 | poucos rótulos, muitas formas sem nome (outra cidade, telhados, caixas de Contrato e Obsidian vazias) |
| Affordance | 3 | ver "o que vale para os três" |
| Cor | 3 | ver "o que vale para os três" |
| Tipografia | 4 | ver "o que vale para os três"; "Rede privada" em pé exige virar a cabeça |

### Veredito: **passa** (na minha parte: R1, R2, R3 e R6 em "passa"; nenhuma dimensão abaixo de 3)

### Consertos

1. [Linhas (R1)] Periferia do par: as duas linhas verdes chegam ao Obsidian lado a lado → trazer o Gustavo pela
   esquerda ou por baixo do prédio, para que o verde dele e o do Obsidian ao Banco local saiam de lados diferentes.
   Evidência: `ux-captura-b-1280.png`.
2. [Hierarquia e Composição] Fora do par: a outra cidade ocupa um terço da largura → reduzir para uma silhueta
   menor (o mesmo traçado em escala, a 50 ou 60%) e devolver a largura aos bairros do par. O detalhe da outra
   cidade vai para a ficha "Fora do par".
3. [Respiro (R3)] Núcleo de dados e Vigilância a 15 px → abrir pelo menos 40 px entre as caixas, a mesma distância
   entre Portas e Conteúdo.
4. [Respiro (R3)] "Agentes" e "Gustavo" encostam no começo das linhas → pôr o rótulo acima da figura, ou começar a
   linha 10 px depois.
5. [Densidade] Contrato e Obsidian são caixas brancas vazias; Raiz são seis telhados soltos → dar a cada prédio uma
   forma que diga o papel (prefeitura, oficina) ou deixá-lo do tamanho do rótulo. Os seis telhados podem virar um
   quarteirão só, com o número na ficha.
6. [Tipografia] "Rede privada" está escrito em pé → deitar a estrada (horizontal, embaixo, por onde passa a troca)
   ou escrever o nome deitado sobre ela.
7. [Cor] Igual ao conserto 6 de A.
8. [Affordance] Igual ao conserto 7 de A.
9. [Tipografia e 320 px] Iguais aos consertos 8 e 9 de A. Evidência: `ux-captura-b-320.png`.

## Conceito C: A cidade em corte

### Regras

- Linhas sem se cruzar (R1): **passa**. Evidência: QA 0; no olho, nenhum cruzamento. Vigiar (laranja) e editar
  (verde) descem em dois L encaixados até o Banco local, a uns 25 px um do outro: passa, mas é o ponto mais
  apertado.
- Vista mais de cima (R2): **passa**. Evidência: 23 rótulos. No olho apertado, Conteúdo, Disciplina e Portas são
  três andares de uma torre só: separam-se pela cor da faixa, não pelo espaço. O teste passa, com a menor folga
  entre manchas dos três.
- Distância entre os itens (R3): **passa**. Evidência: 34,1 px de folga mínima, a maior dos três; razão de 1,85. No
  olho: "Sincronizador" fica a 24 px do nome do bairro "Núcleo de dados do par", embaixo.
- Nomes (R4): não é do meu papel.
- Papel na cidade (R5): não é do meu papel.
- Forma nova (R6): **passa**. Evidência: a vista de lado faz a altura dizer quão perto da verdade cada coisa fica
  (rua, térreo, andares, subsolo). Muda o modo de ler e não repete forma recusada.

### Notas

| Dimensão | Nota | Por quê |
|---|---|---|
| Linhas (R1) | 4 | sem cruzamento; laranja e verde encaixados perto do Banco local |
| Vista de cima (R2) | 4 | os andares se fundem numa torre no olho apertado |
| Respiro (R3) | 4 | a maior folga; "Sincronizador" encosta no nome do bairro |
| Nomes (R4) | não é do meu papel | |
| Papel na cidade (R5) | não é do meu papel | |
| Forma nova (R6) | 5 | a altura carrega sentido; a linha do chão organiza tudo |
| Hierarquia visual | 4 | o chão e o cofre no subsolo dão a leitura de cima para baixo; a Vigilância no alto tem lugar claro |
| Composição | 4 | boa ocupação; a linha laranja longa, do topo ao subsolo, corta meia tela |
| Densidade | 4 | equilibrada; a Disciplina tem só um item numa faixa larga |
| Affordance | 3 | ver "o que vale para os três" |
| Cor | 3 | ver "o que vale para os três" |
| Tipografia | 4 | ver "o que vale para os três" |

### Veredito: **passa** (na minha parte: R1, R2, R3 e R6 em "passa"; nenhuma dimensão abaixo de 3)

### Consertos

1. [Linhas (R1)] Junto ao Banco local: vigiar e editar chegam em dois L encaixados → fazer o verde entrar pela
   direita do Banco local (onde já chega a troca, mais acima) ou pôr a Vigilância em cima do núcleo, para a linha
   laranja descer reta. Evidência: `ux-captura-c-1280.png`.
2. [Vista de cima (R2)] Os três andares encostados → abrir as faixas de laje entre eles (hoje uns 30 px) para 40 a
   50 px, para que cada andar seja uma mancha própria no olho apertado. Evidência: `ux-olho-apertado.png`.
3. [Respiro (R3)] "Sincronizador" a 24 px do nome do bairro → pôr o rótulo à direita da estação, como "Vista
   Markdown", e o nome do bairro no topo da caixa.
4. [Composição] A linha de vigiar cruza a tela do topo ao subsolo → aproximar a Vigilância do núcleo (o alto da
   torre, à direita, sobre a Periferia), encurtando o traço.
5. [Densidade] Disciplina do agente: uma faixa larga com um item → baixar a altura do andar ou pôr ali os outros
   fiscais (Contrato, Guarda do acervo) como salas sem rótulo, com o nome na ficha.
6. [Cor] Igual ao conserto 6 de A.
7. [Affordance] Igual ao conserto 7 de A.
8. [Tipografia e 320 px] Iguais aos consertos 8 e 9 de A. Em 320, o corte não mostra o subsolo; abrir a faixa no
   Banco local. Evidência: `ux-captura-c-320.png`.

## Onde cada um é melhor (sem ranking)

- **A**, em densidade e vista de cima: o olho apertado mais limpo e o menor número de formas.
- **B**, em forma nova: é o único em que a cidade aparece sem legenda (muralha, estrada, a outra cidade igual).
- **C**, em respiro e hierarquia: a maior folga (34,1 px) e a altura que já diz a distância até a verdade.

## Não verificado

- Foco nas três pessoas com Tab real (só testei os quatro primeiros bairros de cada conceito).
- Passar o mouse (título) e o realce ao passar o mouse.
- Larguras 768 e 1920 com o olho; ficam os números do QA.
