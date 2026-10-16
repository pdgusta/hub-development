# Relatório do QA, porta da amostra, volta 2

Testado em 2026-10-15: `amostra/amostra.html` (volta 2, 106 KB). Só medi e relato; não editei a peça. Entre parênteses,
a volta 1.

**Como a navegação foi testada desta vez:** entrada real do navegador, pelo protocolo de depuração do Edge
(`Input.dispatchMouseEvent`, `Input.dispatchKeyEvent`, `Input.dispatchTouchEvent`, com emulação de toque). Nada de
evento montado por script nessa parte. Tamanhos: 1280 x 1000, 960 x 800, 1280 x 720, 1920 x 1080 e 320 x 640.
Eventos montados só ficaram para o teste dos sete cenários e da camada de detalhe (parte 4).

## Resumo

| Item | Resultado |
|---|---|
| Salto no 2º, 3º e 4º arrasto (botão direito e do meio) | **sem salto**, nos 5 tamanhos |
| Ctrl + roda, Shift + roda, roda simples | passam; a página nunca rola |
| `+` e `-` em volta do centro | passa: o centro volta ao mesmo ponto |
| "Ver tudo" e `0` em 320 | **passam**: a cidade inteira cabe, sem ficar sob os botões; texto de 5 px |
| Toque simples (botão e ficha) | passa |
| Pinça e retirada de um dedo | passa, sem salto |
| **Arrasto com um dedo** | **falha**: anda só os primeiros 12 px e para (defeito novo, ver abaixo) |
| Seleção de texto no arrasto esquerdo | passa: 0 caracteres |
| Medidas da peça (4 larguras) | iguais à volta 1; R1 a R3 e contraste passam |
| Sete cenários | passam em 1280, 320 e 1920 |
| Foco com Tab real | **verificado**: 23 de 23 paradas com foco visível |

## 1. Defeito encontrado: arrasto com um dedo para depois de 12 px

**O que acontece.** Com toque (emulado pelo Edge), um dedo que arrasta move a vista uma vez, nos primeiros ~6 px, e
depois a vista para. Pedi 96 x 48 px; a vista andou 12 x 6 px. Aconteceu em todos os pontos de partida que tentei
(fundo do desenho, em cima do Banco local, em cima de um nome) e nos dois tamanhos (1280 e 320).

**Causa, pela sequência de eventos medida:** `pointerdown` e `gotpointercapture` no elemento tocado, primeiro
`pointermove`, então `lostpointercapture`, e a partir daí o toque segue na `main.tela`, mas o gesto já terminou. O
código captura o ponteiro na área (`setPointerCapture`) assim que o arrasto passa de 6 px. O toque já tinha captura
implícita no elemento de baixo; trocar a captura dispara `lostpointercapture` no elemento antigo, que borbulha até a
área, e o tratador de fim de gesto (`solta`, ligado a `lostpointercapture`) encerra o arrasto. Foi o conserto "mesma
limpeza no cancelamento e na perda de captura" que ligou a função a esse evento. No mouse não acontece, porque o botão
direito não tem captura implícita.

**Efeito:** em celular ou tablet, andar pelo desenho com um dedo não funciona de verdade. A pinça com dois dedos e o
toque simples funcionam. O arrasto com um dedo estava na lista "andar" do `amostra.md` e foi dado como conferido nos
consertos; na minha medição não anda.

**Comprovação:** `navegacao/toque.json` e `navegacao/toque-alvos.json` (com a sequência de eventos).

## 2. Navegação do canvas com entrada real

### Arrastos seguidos com o botão direito (e do meio)

Quatro arrastos seguidos, alternando o sentido (100 px e 60 px), apertando em cima do Banco local, medindo a posição
do Banco local antes, no aperto e depois.

| Tamanho | Salto no aperto | Erro depois do arrasto (pedido x obtido) | Ficha aberta | Rolagem da página | Foco |
|---|---|---|---|---|---|
| 1280 x 1000 | 0 px | 0 px nos 4 arrastos | não | 0 | corpo (não vai ao bairro) |
| 960 x 800 | 0 px | 0 px | não | 0 | corpo |
| 1280 x 720 | 0 px | 0 px | não | 0 | corpo |
| 1920 x 1080 | 0 px | 0 px | não | 0 | corpo |
| 320 x 640 | 0 px | 0 px | não | 0 | corpo |

- Botão do meio: resultado idêntico. Seleção de texto depois de cada arrasto: 0 caracteres.
- O salto do segundo arrasto da volta 1 **não aparece mais**.
- Botão esquerdo arrastando: não anda e não seleciona texto (0 caracteres), como o brief manda.
- Depois de um arrasto, o clique esquerdo no Banco local abre a ficha já nele, e o clique no botão do primeiro cenário
  liga o cenário (1280 e 320). Esc fecha a ficha e o foco volta ao bairro.

### Zoom, roda e teclado

| Ação | 1280 x 1000 | 960 x 800 | 1280 x 720 | 1920 x 1080 | 320 x 640 |
|---|---|---|---|---|---|
| Vista inicial | 93% | 72% | 75% | 104% | 75% |
| Ctrl + roda (um passo de 200) | 93 para 134% | 72 para 103% | 75 para 107% | 104 para 149% | 75 para 107% |
| Ponto sob o mouse se desloca (unid.) | 0 | 0,3 | 0 | 0,1 | 0 |
| Shift + roda (só horizontal) | dx 89,7 dy 0 | dx 116,5 dy 0 | dx 111,6 dy 0 | dx 80,8 dy 0 | dx 111,6 dy 0 |
| Roda simples (só vertical) | dy 89,7 | dy 116,6 | dy 111,6 | dy 80,8 | dy 111,6 |
| 3 x `+` depois 3 x `-`: centro antes e depois | 600, 450 igual | igual | igual | igual | igual |
| Setas (60 px de tela) | passam | passam | passam | passam | passam |
| Zoom máximo e mínimo | 500% e 35% | 500% e 35% | 500% e 35% | 500% e 35% | 500% e **25%** |
| Zoom do navegador (`visualViewport.scale`) | 1 | 1 | 1 | 1 | 1 |

Em todos os testes a altura do documento ficou igual à da janela e `scrollY` 0.

### "Ver tudo" (clique real) e `0`

| Tamanho | Nível | A cidade inteira na tela | Itens sob os botões de zoom | Menor texto | Mesma vista pelo botão e pela tecla |
|---|---|---|---|---|---|
| 1280 x 1000 | 93% | sim | 0 | 17 px | sim |
| 960 x 800 | 72% | sim | 0 | 14 px | sim |
| 1280 x 720 | 60% | sim | 0 | **11 px** | sim |
| 1920 x 1080 | 104% | sim | 0 | 20 px | sim |
| **320 x 640** | **25%** | **sim** | 0 | **5 px** | sim |

- Em 320 o conserto funciona (a volta 1 não enquadrava). O preço é texto de 5 px: a cidade inteira cabe, mas não se
  lê; só serve para se orientar e aproximar. Em 1280 x 720, 11 px é leitura apertada.
- A vista de abertura em 320 e em 1280 x 720 não mostra a cidade inteira (75%, centrada no Banco local), por decisão
  da peça (menor nome abaixo de 13 px). Em 960 x 800 abre inteira a 72%, com texto de 14 px.
- Gustavo fora do canto dos botões em todas as vistas iniciais.

### Toque (emulado pelo Edge)

| Ação | 1280 | 960 | 1280 x 720 | 1920 | 320 |
|---|---|---|---|---|---|
| Toque no `+` | aproxima (93 para 117%) | sim | sim | sim | sim |
| Toque no Banco local | abre a ficha | sim | sim | sim | sim |
| **Arrasto com um dedo** | **12 de 96 px, para** | idem | idem | idem | idem |
| Arrasto de um dedo que termina em cima de um bairro | não abre ficha; o toque seguinte abre | | | | idem |
| Pinça (dois dedos se afastam) | aproxima (93 para 280%) | sim | sim | sim | sim (75 para 225%) |
| Tirar um dedo da pinça | salto 0 px | 0 | 0 | 0 | 0 |
| Mover o dedo que ficou 2 px | desloca 2 px; depois 8 x 10 px certo | | | | idem |
| Soltar o último dedo | sem ficha aberta, nível estável | | | | idem |
| Tocar no Banco local depois de pinça | abre a ficha | | | | sim |

- Ficha em 320: abre como diálogo modal (`role="dialog"`, `aria-modal="true"`, topo e desenho `inert`); em 1280, 960,
  1280 x 720 e 1920 é painel de 440 px sem papel de diálogo, não modal. Esc fecha e devolve o foco.
- **Toque emulado não é aparelho:** só o toque do Edge foi usado. Aparelho de verdade não testado.

## 3. Foco com Tab real (1280 x 1000)

23 paradas na ordem do Tab, todas com foco visível:

| Paradas | O que muda ao focar | Veredito |
|---|---|---|
| 1 a 7 (botões de cenário) | contorno de 3 px | passa |
| 8 (o desenho) | sombra interna de 3 px (`.tela:focus-visible`) | passa |
| 9 a 17 (nove bairros) | contorno do bairro de 1,6 para 3,5 px, em tinta escura | **passa** |
| 18 a 20 (três pessoas) | anel preenchido de amarelo, com traço escuro | **passa** |
| 21 a 23 (afastar, aproximar, ver tudo) | contorno de 3 px | passa |

- Os 12 bairros e pessoas que a medição por script deixava "não verificado" estão **verificados** com Tab real: todos
  têm `:focus-visible` verdadeiro e a aparência muda.
- A ferramenta `medidas-da-peca` ainda lista os 12 como "sem mudança por script", sem reconhecer a regra do filho.
  Isso é limite da ferramenta; o Tab real tem a palavra final.

## 4. Medidas da peça e cenários

### Medidas (vista inicial)

| Medida (limiar) | 320 | 768 | 1280 | 1920 | Veredito |
|---|---|---|---|---|---|
| R1 cruzamentos (0) | 0 (0) | 0 | 0 (0) | 0 | **passa** |
| R2 rótulos no desenho | 27 (27) | 27 | 27 (27) | 27 | sem teto; critério de poluição fica com o UX |
| R3 folga mínima (>= 1 rótulo) | 18 de 15 (18) | 18 de 15 | 22,3 de 19 (22,3) | 22,7 de 19 | **passa** |
| R3 razão entre grupos (>= 1,5) | 1,53 (1,53) | 1,53 | 1,53 (1,53) | 1,53 | **passa**, por 0,03 |
| Contraste | 41 de 41 | 42 de 42 | 58 de 58 (58) | 58 de 58 | **passa** |
| Focáveis sem nome / tabindex positivo | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | **passa** |
| Rolagem horizontal | não | não | não | não | **passa** |
| Códigos internos soltos | 0 | 0 | 0 | 0 | **passa** |
| Rede externa | nenhuma | | | | **passa** |
| Peso | 105,8 KB (92,2) | | | | nada externo |
| Carga (tempo virtual) | 190 ms | 205 | 234 (215) | 226 | só para comparar |

- A planta não mudou: folga e razão são as mesmas da volta 1. Links: nenhum `<a>` no HTML.
- Itens marcados: 60 (58), 2 a mais pelas etiquetas novas.

### Camada de detalhe (aproximando, eventos montados)

| Medida | 1280 x 1000 (182%) | 320 x 640 (186%) | 1920 x 1080 (162%) |
|---|---|---|---|
| Etiquetas com lugar / total | 42 de 42 (40) | 42 de 42 | 42 de 42 |
| Sem lugar no empacotamento | nenhuma | nenhuma | nenhuma |
| Textos sobrepostos (9 quadrantes) | 0 | 0 | 0 |
| Menor espaço entre dois textos | 10 px (11,8) | 20 px | 9,5 px (10,6) |
| Menor altura de texto | 21 px | 21 px | 18 px |

- As duas etiquetas novas (Claude Desktop e Cliente) cabem. O menor espaço entre textos na camada de detalhe caiu um
  pouco (de 10,6 para 9,5 px em 1920): continua abaixo de uma altura de rótulo, sem sobreposição. Mesma observação da
  volta 1 para o juiz de R3.

### Sete cenários

Em 1280, 320 e 1920, igual nos três. 39 passos.

| Cenário | Passos | Marca = número do passo | Marca dentro da tela | Marca sobre texto | Sair e Esc apagam | Foco volta ao botão | Passo de falha ou em aberto |
|---|---|---|---|---|---|---|---|
| O Gustavo edita um arquivo | 6 | sim | sim | 0 | sim | sim | 6 |
| Um agente novo abre sessão | 6 | sim | sim | 0 | sim | sim | nenhum |
| Um maestro novo abre sessão | 6 | sim | sim | 0 | sim | sim | nenhum |
| O Gustavo pede: leia | 4 | sim | sim | 0 | sim | sim | 4 |
| O Gustavo pede: altere | 7 | sim | sim | 0 | sim | sim | 7 |
| O Gustavo pede: remova | 5 | sim | sim | 0 | sim | sim | 5 |
| O outro par altera um arquivo | 5 | sim | sim | 0 | sim | sim | 5 |

- Depois de Sair e de Esc, os sete botões voltam a `aria-pressed="false"`; clicar num botão leva o foco para
  "Próximo". O nível de zoom não muda durante o cenário em 1280 e 1920; em 320 fica em 75%.
- Cenários 6 do agente novo e o do maestro novo (itens 6 e 7 dos consertos do UX): a medição não vê cor nem corte de
  nome; a conferência visual é do UX revisor. Contei só que as marcas ficam fora do texto.

## 5. Não verificado

- **Aparelho de toque de verdade.** Só toque emulado do Edge. O defeito do arrasto com um dedo (item 1) vem da ordem
  dos eventos do protocolo; na especificação de eventos de ponteiro a mesma ordem vale em aparelho, mas não provei.
- Leitor de tela (papel de diálogo, `inert`); mouse físico e roda física (usei entrada real do protocolo, não a mão).
- Conteúdo contra a descrição v3.2 e conferência dos consertos item a item: dos juízes. Cor de linha dos dois roxos
  colados e corte do nome da Biblioteca: olho do UX revisor.
- Contraste das etiquetas na camada de detalhe e no estado aceso (a ferramenta mede o repouso).
- Seleção de texto por duplo clique ou por teclado (só testei arrasto).
- break-ui (dados extremos) não pedido.

## Arquivos

- Medidas: `medidas-320|768|1280|1920.json`, `captura-<largura>.png`, `links.json`, `resumo.txt`.
- Entrada real: `navegacao/entrada-real.mjs` (script), `entrada-real.json`, `resumo-entrada-real.txt`, `tab-real.txt`;
  toque: `toque-diag.mjs`, `toque.json`, `toque-alvos.mjs`, `toque-alvos.json`; clique depois de arrasto:
  `clique-real.mjs`, `clique-real.json`.
- Cenários e camada de detalhe (eventos montados): `navegacao/harness.html`, `nav-320|1280|1920.json`;
  `rodar-navegacao.ps1`.
