# Parecer do UX revisor, porta da amostra, volta 1 (fase 4, etapa 12)

2026-10-15. Peça: `amostra/amostra.html`, com `amostra.md` e `decisoes.md`. Roteiro:
`suite/skills/regua-da-cidade/como-julgar.md`. Relatório do QA: `qa/amostra-1/relatorio.md`. Critério desta porta: R2
sem teto fixo (não poluir); o resto igual.

## Como medi

Edge via Playwright, servido em `127.0.0.1:8798`. Entrada pelo protocolo do navegador (tecla, roda com Ctrl e Shift
segurados, botão direito, do meio e esquerdo apertados e arrastados), não eventos montados no documento. Arquivos ao lado
deste parecer:

- vista inicial: `ux-captura-1280x1000.png`, `ux-captura-1920x1080.png`, `ux-captura-1280x720.png`,
  `ux-captura-960x800.png` (perto da largura de um portal ao lado do terminal), `ux-captura-320x640.png`;
- foco: `ux-foco-tab-7.png` (o desenho focado), `ux-foco-tab-8.png`;
- canvas: `ux-zoom/` (`zoom-centro.png` depois de Ctrl + roda; `zoom-mais3.png` depois de três `+`; os quatro cantos a
  182%; `salto-antes.png` e `salto-depois.png`; `arrasto-esquerdo-seleciona.png`);
- cenários: `ux-cenarios/<cenário>-<passo>.png`, os 39 passos a 1280 x 1000.

## Foco com Tab real: passa nas 23 paradas

As 23 paradas casam `:focus-visible` e mudam na tela: 7 botões de cenário (1.442 a 1.802 px), o desenho (moldura escura
em volta do canvas, 13.183 px), 9 bairros (2.812 a 4.746 px), 3 pessoas com o anel (344 a 349 px), os 3 botões de zoom
(540 a 974 px). Depois de Esc num cenário, os sete botões voltam a `aria-pressed="false"`: o defeito da mistura foi
corrigido. **Passa.**

## O conforto do canvas

| Gesto | O que acontece | Conforto |
|---|---|---|
| Ctrl + roda | aproxima em volta do ponteiro, sem zoom da página; a 140% liga a camada de detalhe | bom |
| Shift + roda | anda só para os lados | bom |
| Roda simples | anda para cima e para baixo; a página não rola | bom |
| Botão direito, primeiro arrasto | anda exatamente o que o mouse andou | bom |
| **Botão direito, arrasto seguinte** | **ao apertar o botão, a vista salta antes de andar**: o Banco local foi de (319, 397) para (513, 901) na tela, uns 200 x 500 px, sem o mouse se mexer | **ruim**: é o gesto principal que o Gustavo pediu |
| Botão do meio | o mesmo do direito, com o mesmo salto | ruim |
| Botão esquerdo, arrastar | não anda e **seleciona o texto** do desenho (426 caracteres em azul, `arrasto-esquerdo-seleciona.png`) | ruim |
| `+` e `−` (foco no desenho) | aproximam, mas **não em volta do centro da tela**: depois de três `+`, a cidade escorrega para baixo e para a direita, e o terço de cima da tela fica vazio (`zoom-mais3.png`) | regular |
| Setas | andam 60 px por toque | bom |
| `0` e "Ver tudo" | voltam à vista inicial | bom |

**O salto, passo a passo** (repete sempre):

1. Abrir a 1280 x 1000.
2. Arrastar com o botão direito de (700, 600) até (500, 450): anda certo.
3. Apertar o botão direito de novo em (700, 600), sem mexer o mouse: a vista salta (`salto-antes.png` →
   `salto-depois.png`).

Acontece também apertando fora de qualquer bairro. No primeiro aperto, o foco foi para o bairro sob o ponteiro (Núcleo
de dados); no segundo, para o desenho ("Planta da cidade do par"). Minha hipótese, para o UI engineer e o Prumo
conferirem: a mudança de foco pelo mouse faz o navegador rolar a área do desenho para mostrar o elemento focado, ou
aciona o "a vista vai até o bairro focado" que devia valer só para o Tab. O QA não pegou porque testou com eventos
montados no documento, que não mudam o foco.

## Conferência do que a mistura aprovada tinha

- Vista inicial a 1280 x 1000 (93%) igual à mistura aprovada, com dois nomes a mais (Agendador do Windows e Biblioteca
  do Maestri) em ícones que estavam sem nome. Não ficou mais carregada: os dois nomes ocupam lugar que já era do ícone.
- Os sete cenários, os 39 passos: cada número aparece e fica junto do que marca (o 5 de "O Gustavo edita" voltou; o 3
  de "agente novo" está na nota). O passo de falha segue com o triângulo vermelho.
- Clicar numa etiqueta, a 182%, abre a ficha nela.

## Problemas novos

1. **O salto ao arrastar** (acima).
2. **`+` e `−` não aproximam em volta do centro** (acima).
3. **O arrasto com o botão esquerdo seleciona texto.**
4. **A 960 x 800, o cabeçalho ocupa 36% da altura** (290 de 800 px): legenda em quatro linhas e os cenários em três
   fileiras (`ux-captura-960x800.png`). A cidade abre cortada em cima (a linha do maestro sai pela borda) e o nome do
   Gustavo fica embaixo dos botões de zoom. A página vai morar num portal ao lado do terminal, que deve ficar perto
   dessa largura.
5. **A 1280 x 720, a vista inicial abre a 60%** para caber inteira, com rótulos de 11 px (mediana de 12 px). Lê, mas
   apertado. A 960 x 800, a vista abre a 75% com 14 a 15 px; a 1920 x 1080, 20 a 21 px.
6. **"Um agente novo", passo 6:** a linha roxa Checkpoint → Agentes, que voltou só no cenário, desce colada à linha roxa
   do Contrato, a uns 10 px (`ux-cenarios/agente-novo-6.png`). É o defeito dos dois roxos colados da mistura volta 1,
   agora só no cenário.
7. **"Um maestro novo", passos 4 a 6:** a linha Maestro → Biblioteca do Maestri desce pelo meio do nome novo
   "Biblioteca do Maestri" (`ux-cenarios/maestro-novo-6.png`).
8. Menor: na camada de detalhe, algumas etiquetas ficam logo abaixo do nome de um componente e parecem dele, não do
   bairro. "Checagem de sessão" fica a uns 12 px embaixo de "Contrato", e "Núcleo da iniciativa e blocos" embaixo da
   Nota de retomada (`ux-zoom/zoom-mais3.png`).

## As regras

- **Linhas sem se cruzar (R1): passa.** QA 0 em todas as larguras; no olho, nenhum cruzamento. Os problemas 6 e 7 são
  de leitura (linha colada, linha sobre nome), só no cenário.
- **Vista mais de cima (R2): passa.** Sem teto, o critério é não poluir. A vista inicial tem 27 rótulos, com o mesmo
  desenho da mistura aprovada mais dois nomes em ícones que já estavam lá. A camada de detalhe só aparece ao
  aproximar, e lá as 40 etiquetas ficam em fileiras arrumadas, sem sobreposição (`ux-zoom/dir-baixo.png`). É o
  "aproximar" que a régua prevê.
- **Distância entre os itens (R3): passa.** Folga mínima de 22,3 px contra 19; razão entre grupos de 1,53 (a mistura
  volta 2 tinha 1,68; caiu com as fileiras mais altas). Na camada de detalhe, o espaço entre etiqueta e nome é de 10,6
  a 12 px. Leio as etiquetas como uma lista de chips do bairro, não como itens do mapa, por isso não aplico a folga de
  item a elas; mas ver o problema 8.
- **Nomes (R4) e Papel na cidade (R5):** não é do meu papel.
- **Forma nova (R6): passa.** O canvas muda o que o leitor faz (aproximar para ver o detalhe) sem mudar a planta
  aprovada.

## Os cenários sem texto

**Os sete se seguem sem ler**, contra seis na mistura volta 2: todos os números presentes e junto do que marcam, e o
passo de falha distinto. Os problemas 6 e 7 atrapalham a leitura de dois passos, mas não a quebram.

## Notas

| # | Dimensão | Nota | Por quê |
|---|---|---|---|
| 1 | Linhas (R1) | 4 | sem cruzamento; no cenário, roxo colado e linha sobre o nome da Biblioteca |
| 2 | Vista de cima (R2) | 5 | igual à aprovada; o detalhe só aparece ao aproximar |
| 3 | Respiro (R3) | 4 | razão de 1,53, de novo perto do limiar |
| 4 | Nomes (R4) | não é do meu papel | |
| 5 | Papel na cidade (R5) | não é do meu papel | |
| 6 | Forma nova (R6) | 5 | a camada de detalhe usa o canvas para o que a régua pedia |
| 7 | Hierarquia visual | 4 | a 1280 e a 1920, ótima; a 960, o cabeçalho pesa mais que a cidade |
| 8 | Composição | 3 | a 960 x 800 a cidade abre cortada, com o Gustavo embaixo dos botões de zoom |
| 9 | Densidade | 3 | a vista inicial segue a da mistura; o cabeçalho tem 58 textos |
| 10 | Affordance (conforto do canvas) | **2** | o arrasto, gesto principal pedido pelo Gustavo, salta a partir do segundo uso; o arrasto esquerdo pinta o texto de azul; `+` desloca a cidade. O resto (roda, Ctrl, Shift, setas, `0`, dica no topo, botões de zoom, foco 23 de 23) é bom |
| 11 | Cor | 4 | igual à mistura aprovada |
| 12 | Tipografia | 3 | 11 px a 1280 x 720; confortável a 1280 x 1000 e acima, e em toda a camada de detalhe |

## Veredito: **volta**

R1, R2, R3 e R6 em "passa", mas o conforto do canvas (Affordance) fica em 2. O arrasto com o botão direito foi o gesto
que o Gustavo pediu para esta página, e hoje ele salta a partir do segundo uso. Os consertos 1 a 3 resolvem a nota; o
4 e o 5 são do lugar em que a página vai morar (o portal estreito).

## Consertos

1. [Affordance] Salto ao arrastar → ao apertar o botão direito ou o do meio, não mudar o foco nem rolar a área do
   desenho: tratar o aperto sem levar o foco (ou focar com `preventScroll`), e fazer a vista ir até o bairro focado só
   quando o foco vier do teclado. Conferir com dois e três arrastos seguidos, com entrada real (protocolo do navegador),
   não com eventos montados. Evidência: `ux-zoom/salto-antes.png` e `salto-depois.png`.
2. [Affordance] `+` e `−` → aproximar em volta do centro da área do desenho (o mesmo que Ctrl + roda faz com o
   ponteiro). Evidência: `ux-zoom/zoom-mais3.png`.
3. [Affordance] Arrasto esquerdo seleciona texto → impedir a seleção de texto no desenho. Opcional, se o Gustavo
   quiser: o arrasto esquerdo também anda, a partir de uns 5 px de movimento; abaixo disso segue sendo clique e abre a
   ficha.
4. [Composição] Cabeçalho a 960 px → abaixo de uns 1.100 px de largura, recolher a legenda no botão "Legenda" (como já
   faz a 320) e pôr os cenários numa fileira só, que rola para os lados. Meta: cabeçalho de no máximo uns 140 px.
   Evidência: `ux-captura-960x800.png`.
5. [Composição e Tipografia] Vista inicial em janelas baixas ou estreitas → enquadrar a vista inicial descontando o
   canto dos botões de zoom (o Gustavo não pode abrir embaixo deles). Abrir "tudo à vista" só se o menor rótulo ficar
   com 13 px ou mais; se não, abrir a 75%, centrado no Banco local, como a 320 já faz. Evidências:
   `ux-captura-960x800.png` e `ux-captura-1280x720.png`.
6. [Linhas] "Um agente novo", passo 6: roxo do Checkpoint colado ao do Contrato → levar a linha do Checkpoint até os
   Agentes pelo outro lado (por dentro da muralha, junto da borda de Portas) ou juntar as duas num traço só a partir da
   muralha. Evidência: `ux-cenarios/agente-novo-6.png`.
7. [Linhas] "Um maestro novo", passos 4 a 6: a linha da Biblioteca corta o nome → entrar no caderno pelo lado direito
   ou por cima, longe do nome. Evidência: `ux-cenarios/maestro-novo-6.png`.
8. [Respiro] Etiquetas logo abaixo do nome de um componente → deixar pelo menos meia altura de rótulo entre a etiqueta
   e o nome mais próximo, ou alinhar as etiquetas pela borda do bairro, para lerem como do bairro.

## Não verificado

- Toque (um dedo, pinça) e mouse físico; testei com entrada real do navegador, que é o mais perto sem aparelho.
- A largura exata do portal do Maestri: usei 960 x 800 como aproximação.
- O conteúdo das fichas e das 40 etiquetas contra a descrição v3.2: é do Tech lead.
- O código (eventos, ARIA): é do Prumo. Passei a ele, pelo parecer, a reprodução do salto.
