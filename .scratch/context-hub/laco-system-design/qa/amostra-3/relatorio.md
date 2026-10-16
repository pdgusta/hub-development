# Relatório do QA, porta da amostra, volta 3 (a última)

Testado em 2026-10-15: `amostra/amostra.html` (volta 3, 107 KB). Só medi e relato; não editei a peça. Entre parênteses,
a volta 2.

**Como foi testado:** entrada real do navegador, pelo protocolo de depuração do Edge (mouse, roda, teclado e toque
emulado, sem evento montado por script). Tamanhos: 1280 x 1000, 960 x 800, 1280 x 720, 1920 x 1080 e 320 x 640. As
medidas da peça e os cenários seguem o roteiro das voltas anteriores.

## Resumo

| Item | Resultado |
|---|---|
| **Arrasto com um dedo, mesmos alvos e percurso da volta 2** | **passa**: segue até o fim, erro 0 px (era 12 de 96 px) |
| Toque simples no `+` e no Banco local | passa |
| Nenhuma ficha depois do arrasto | passa |
| Pinça, soltar um dedo, mover o outro | passa, sem salto |
| Cancelamento no meio do arrasto | passa |
| Três (quatro) arrastos seguidos com o botão direito e do meio | passa, sem salto |
| `+` e `-` no centro | passa |
| "Ver tudo" e `0` em 320 | passa (texto de 5 px) |
| Tab real | **23 de 23**, todas com foco visível (24 em 320) |
| Medidas nas 4 larguras | iguais à volta 2; R1, R3 e contraste passam |
| Sete cenários | passam em 1280, 320 e 1920 |
| Cabeçalho a 1280 x 720 | 139 px (era 185) |
| Fileira de cenários a 960 | rola para os lados e chega ao último botão |
| Problemas novos | nenhum atribuível à peça (uma instabilidade do emulador de toque, ver 2) |

## 1. Arrasto com um dedo (o bloqueio da volta 2)

Mesmo roteiro da volta 2: três alvos (fundo do desenho, em cima do Banco local, em cima de um nome), mesmos dois
tamanhos de partida e mais três; 8 passos de 12 x 6 px, e agora também 30 passos de 5 x 3 px em sentido contrário.

| Alvo | 8 passos (pedido 96 x 48) | 30 passos (pedido -150 x -90) | Ficha aberta | `arrastando` durante / depois |
|---|---|---|---|---|
| Fundo do desenho | 96 x 48, erro 0 | -150 x -90, erro 0 | não | sim / não |
| Em cima do Banco local | 96 x 48, erro 0 | -150 x -90, erro 0 | não | sim / não |
| Em cima de um nome | 96 x 48, erro 0 | -150 x -90, erro 0 | não | sim / não |

O resultado é o mesmo nos cinco tamanhos (1280 x 1000, 960 x 800, 1280 x 720, 1920 x 1080 e 320 x 640). A peça
acompanha o dedo por todo o percurso; antes parava depois de 12 px.

## 2. Toque (emulado pelo Edge), o que precisava continuar

| Ação | Resultado nos cinco tamanhos |
|---|---|
| Toque no `+` | aproxima (93 para 117% a 1280; 75 para 94% a 320) |
| Toque no Banco local | abre a ficha já nele |
| Arrasto que termina em cima de um bairro | **não** abre ficha; o toque seguinte abre (em 1280 x 1000, 960 e 1280 x 720; ver observação) |
| `touchCancel` no meio do arrasto | encerra: sem `arrastando`, a vista não anda mais; o toque seguinte abre a ficha |
| Pinça (dois dedos se afastam) | aproxima (93 para 280%; 75 para 225% a 320) |
| Soltar **um** dedo da pinça (lista só o dedo solto) | salto 0 px, nível estável |
| Mover o dedo que ficou 2 px | desloca 2 px |
| Depois mover 20 passos (pedido 80 x 40) | 80 x 40 |
| Soltar o último dedo | sem ficha aberta, nível estável |

**Observação, não atribuível à peça: toque logo depois do arrasto.** Num teste de arrasto seguido de toque no Banco
local com cerca de 150 ms entre os dois, o navegador às vezes não gerou o `click` do segundo toque (não chega nem ao
`document`; só `pointerdown`, `pointerup` e `lostpointercapture`). Aconteceu em tamanhos diferentes a cada rodada e
também na volta 2, em `amostra-v2.html`, ou seja, não é regressão. Com 200 ms ou mais, o primeiro toque depois do
arrasto abriu a ficha em 8 de 8 tentativas, nas duas versões. Parece regra do reconhecedor de gestos do emulador
(toque perto no tempo e no espaço do anterior). Aparelho de verdade não testado.

## 3. Mouse e teclado, de novo

### Arrastos seguidos (botão direito e do meio)

Quatro arrastos seguidos, alternando o sentido (100 x 60 px), apertando em cima do Banco local:

| Tamanho | Salto no aperto | Erro depois do arrasto | Ficha aberta | Rolagem da página | Seleção de texto |
|---|---|---|---|---|---|
| 1280 x 1000 | 0 px | 0 px nos 4 | não | 0 | 0 |
| 960 x 800 | 0 px | 0 px | não | 0 | 0 |
| 1280 x 720 | 0 px | 0 px | não | 0 | 0 |
| 1920 x 1080 | 0 px | 0 px | não | 0 | 0 |
| 320 x 640 | 0 px | 0 px | não | 0 | 0 |

- Botão do meio: idêntico. Botão esquerdo arrastando: a vista não anda e nenhum texto é selecionado (0 caracteres).
- Depois de um arrasto com o botão direito, o clique esquerdo no Banco local abre a ficha já nele e Esc a fecha. Em 320
  a ficha abre como diálogo modal (`role="dialog"`), nos outros tamanhos como painel.
- Em 320, um arrasto esquerdo que começa e termina dentro do mesmo bairro abre a ficha: é o clique que o navegador
  gera quando o botão sobe sobre o mesmo bairro. Nos outros tamanhos não aconteceu. Não é salto; fica registrado.

### Zoom, roda e teclado

| Ação | 1280 x 1000 | 960 x 800 | 1280 x 720 | 1920 x 1080 | 320 x 640 |
|---|---|---|---|---|---|
| Vista inicial | 93% | 72% | 75% | 104% | 75% |
| Ctrl + roda | 93 para 134% | 72 para 103% | 75 para 107% | 104 para 149% | 75 para 107% |
| Ponto sob o mouse se desloca (unid.) | 0 | 0,3 | 0,2 | 0,1 | 0 |
| Shift + roda (só horizontal) | dx 89,7 | dx 116,5 | dx 111,6 | dx 80,8 | dx 111,6 |
| Roda simples (só vertical) | dy 89,7 | dy 116,6 | dy 111,6 | dy 80,8 | dy 111,6 |
| 3 x `+`, 3 x `-`: centro antes e depois | 600, 450 igual | igual | igual | igual | igual |
| Zoom máximo e mínimo | 500% e 35% | 500% e 35% | 500% e 35% | 500% e 35% | 500% e 25% |
| Rolagem da página | 0 | 0 | 0 | 0 | 0 |

### "Ver tudo" (clique real) e `0`

| Tamanho | Nível | Cidade inteira na tela | Itens sob os botões de zoom | Menor texto | Botão e tecla dão a mesma vista |
|---|---|---|---|---|---|
| 1280 x 1000 | 93% | sim | 0 | 17 px | sim |
| 960 x 800 | 72% | sim | 0 | 14 px | sim |
| 1280 x 720 | 66% (60) | sim | 0 | 12 px (11) | sim |
| 1920 x 1080 | 104% | sim | 0 | 20 px | sim |
| 320 x 640 | 25% | sim | 0 | **5 px** | sim |

Em 320 a cidade inteira cabe, mas o texto fica ilegível (5 px); serve para se orientar e aproximar. Captura em
`navegacao/ver-tudo-320x640.png`.

## 4. Cabeçalho a 1280 x 720 e fileira de cenários a 960

| Medida | 1280 x 720 | 960 x 800 | 1280 x 1000 (referência) |
|---|---|---|---|
| Altura do topo (título, cenários) | **139 px** (era 185) | 106 px (106) | 185 px |
| Área do desenho | 581 px (535) | 694 px | 815 px |
| Legenda | recolhida no botão "Legenda" | recolhida | à vista |
| Cenários | 7 botões em 2 linhas, todos visíveis | 7 botões, **3 inteiros** à vista, resto rola | 7 botões em 2 linhas |
| Fileira rola para os lados | não precisa | **sim** (`overflow-x: auto`) | não precisa |
| Último botão alcançável | sim | **sim** (rolando até 773 px) | sim |
| Shift + roda sobre a fileira anda para os lados | n/a | **sim** (0 para 150 px) | n/a |
| Botão "Legenda" aberto | topo 185 px, área 535 px | topo 194 px, área 606 px | n/a |

- A 1280 x 720 o topo ficou 46 px mais baixo e a área do desenho 46 px mais alta. A faixa com a ajuda do mouse ("Arraste
  com o botão direito · Ctrl + roda: zoom ...") aparece à direita do 2º grupo de botões.
- A 960, a fileira rola mas só mostra 3 dos 7 botões; quem não sabe que rola não vê os outros 4. Não medi se há sinal
  de que rola (sombra, corte do último botão visível): isso é leitura visual do UX revisor.
- Capturas: `navegacao/cabecalho-1280x720.png`, `cabecalho-960x800.png`, `fileira-960x800-rolada.png`,
  `legenda-aberta-1280x720.png`, `legenda-aberta-960x800.png`.

## 5. Foco com Tab real

- 1280 x 1000: **23 de 23** paradas, todas com `:focus-visible` verdadeiro e aparência que muda: 7 botões de cenário
  (contorno de 3 px), o desenho (sombra interna de 3 px), 9 bairros (contorno de 1,6 para 3,5 px), 3 pessoas (anel
  amarelo com traço escuro) e 3 botões de zoom (contorno de 3 px).
- 320 x 640: 24 paradas (a mais é o botão "Legenda"), todas com foco visível.
- A ferramenta `medidas-da-peca` continua listando os 12 bairros e pessoas como "sem mudança por script" (não
  reconhece a regra posta no filho); o Tab real é o que vale.

## 6. Medidas da peça e cenários

| Medida (limiar) | 320 | 768 | 1280 | 1920 | Veredito |
|---|---|---|---|---|---|
| R1 cruzamentos (0) | 0 | 0 | 0 | 0 | **passa** |
| R2 rótulos no desenho | 27 | 27 | 27 | 27 | sem teto; poluição fica com o UX |
| R3 folga mínima (>= 1 rótulo) | 18 de 15 | 18 de 15 | 22,3 de 19 | 22,7 de 19 | **passa** |
| R3 razão entre grupos (>= 1,5) | 1,53 | 1,53 | 1,53 | 1,53 | **passa**, por 0,03 |
| Contraste | 41 de 41 | 42 de 42 | 58 de 58 | 58 de 58 | **passa** |
| Focáveis sem nome / tabindex positivo | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | **passa** |
| Rolagem horizontal da página | não | não | não | não | **passa** |
| Códigos internos soltos / links quebrados / rede externa | 0 / nenhum link / nenhuma | | | | **passa** |
| Peso | 107,3 KB (105,8) | | | | nada externo |
| Carga (tempo virtual) | 230 ms | 197 | 227 | 152 | só para comparar |

A planta não mudou: folga e razão são as mesmas da volta 2.

Camada de detalhe (aproximando, a 162 a 186%): 42 de 42 etiquetas com lugar, nenhuma sem lugar no empacotamento,
0 textos sobrepostos nos 9 quadrantes, menor espaço entre dois textos 9,5 a 20 px (igual à volta 2), menor altura de
texto 18 a 21 px.

### Sete cenários (39 passos; 1280, 320 e 1920 iguais)

| Cenário | Passos | Marca = número | Marca dentro da tela | Marca sobre texto | Sair e Esc apagam | Foco volta ao botão | Passo de falha ou em aberto |
|---|---|---|---|---|---|---|---|
| O Gustavo edita um arquivo | 6 | sim | sim | 0 | sim | sim | 6 |
| Um agente novo abre sessão | 6 | sim | sim | 0 | sim | sim | nenhum |
| Um maestro novo abre sessão | 6 | sim | sim | 0 | sim | sim | nenhum |
| O Gustavo pede: leia | 4 | sim | sim | 0 | sim | sim | 4 |
| O Gustavo pede: altere | 7 | sim | sim | 0 | sim | sim | 7 |
| O Gustavo pede: remova | 5 | sim | sim | 0 | sim | sim | 5 |
| O outro par altera um arquivo | 5 | sim | sim | 0 | sim | sim | 5 |

Depois de Sair e de Esc, os sete botões voltam a `aria-pressed="false"`; clicar num botão leva o foco para
"Próximo".

## 7. Não verificado

- **Aparelho de toque de verdade.** Só toque emulado do Edge; a ocasional falha de `click` logo depois de um arrasto
  (item 2) é do emulador nas duas versões, mas só aparelho confirma.
- Leitor de tela (papel de diálogo, `inert`), mouse e roda físicos.
- Se a fileira de cenários a 960 dá sinal visual de que rola, e a leitura visual do cabeçalho a 1280 x 720
  (olho do UX revisor).
- Conteúdo contra a descrição v3.2 (Tech lead). O conteúdo da peça não foi tocado por mim.
- Contraste das etiquetas na camada de detalhe e no estado aceso (a ferramenta mede o repouso).
- break-ui (dados extremos) não pedido.

## Arquivos

- Medidas: `medidas-320|768|1280|1920.json`, `captura-<largura>.png`, `links.json`, `resumo.txt`.
- Entrada real: `navegacao/entrada-real.mjs` (script), `entrada-real.json`, `resumo-entrada-real.txt`.
- Diagnóstico do toque logo depois do arrasto: `navegacao/toque-apos-arrasto*.mjs` e `.json`, `toque-150ms-*.json`.
- Capturas: `navegacao/*.png`.
- Cenários e camada de detalhe: `navegacao/harness.html`, `nav-320|1280|1920.json`; `rodar-navegacao.ps1`.
