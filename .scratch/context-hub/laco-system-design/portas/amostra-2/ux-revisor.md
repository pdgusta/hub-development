# Parecer do UX revisor, porta da amostra, volta 2

2026-10-15. Peça: `amostra/amostra.html` (volta 2). Conferi primeiro os 8 consertos do meu parecer da volta 1
(`portas/amostra-1/ux-revisor.md`) contra `amostra/consertos.md` e a peça, com entrada real do navegador (Playwright
sobre o Edge: tecla, roda com Ctrl e Shift, botões do mouse, e toque pelo protocolo de depuração). Depois, só o que os
consertos criaram. Relatório do QA: `qa/amostra-2/relatorio.md`.

## Arquivos ao lado deste parecer

- vista inicial: `ux-captura-1280x1000.png`, `ux-captura-960x800.png`, `ux-captura-1280x720.png`,
  `ux-captura-1920x1080.png`, `ux-captura-320x640.png`;
- `ux-960-cenario.png` (cenário ligado a 960 x 800), `ux-960-legenda-aberta.png`;
- `ux-zoom/mais3.png`, `mais3-esq-cima.png`, `mais3-esq-baixo.png` (três `+` com o foco no desenho, e a camada de
  detalhe);
- `ux-cenarios/agente-novo-6.png`, `maestro-novo-6.png`, `gustavo-edita-6.png`.

## Conferência dos consertos da volta 1

| # | Meu conserto | Situação | Como conferi | Aceito? |
|---|---|---|---|---|
| 1 | Salto a partir do segundo arrasto | feito | três arrastos seguidos com o botão direito, apertando no meio da tela, a 1280 x 1000, 960 x 800, 1280 x 720 e 1920 x 1080: 0 px de salto no aperto, e o Banco local anda exatamente o que o mouse andou em cada um (-150 x -90, +120 x +80, -100 x +60) | sim |
| 2 | `+` e `−` em volta do centro | feito | três `+` com o foco no desenho: a cidade aproxima em volta do centro da área, sem faixa vazia (`ux-zoom/mais3.png`) | sim |
| 3 | Arrasto esquerdo seleciona texto | feito | arrasto esquerdo nas quatro janelas: 0 caracteres selecionados | sim |
| 4 | Cabeçalho a 960 x 800 | feito | o desenho começa a 96 px do topo (era 290); legenda no botão "Legenda", cenários numa fileira (`ux-captura-960x800.png`) | sim |
| 5 | Vista inicial fora dos botões; 75% se o nome ficar pequeno | feito | 960 x 800 abre inteira a 73%, menor texto de 14 px; 1280 x 720 abre a 75% no Banco local, 14 px (era 60% e 11 px); 1920 x 1080 a 104%, 20 px; 1280 x 1000 a 93%, 17 px | sim; ver o problema novo 2 |
| 6 | "Agente novo" 6: dois roxos colados | feito de outro jeito: o Checkpoint junta-se ao traço do Contrato e descem num traço só | `ux-cenarios/agente-novo-6.png`: um roxo só desce aos Agentes | sim: é a segunda saída que eu tinha dado |
| 7 | "Maestro novo": linha corta o nome da Biblioteca | feito | a linha entra no caderno pela direita; o nome fica livre (`maestro-novo-6.png`) | sim |
| 8 | Etiquetas coladas embaixo de um nome | feito | a 182%, as etiquetas da Disciplina ficam a uns 25 px de "Contrato" e "Checkpoint", alinhadas pela borda do bairro, e leem como do bairro (`ux-zoom/mais3-esq-cima.png`) | sim |

## Problemas novos

1. **O arrasto com um dedo não anda** (achado do QA, confirmado). Com toque pelo protocolo do Edge, pedi um arrasto
   de 96 x 48 px; o Banco local andou 8 x 4 px e parou. A pinça e o toque simples funcionam (QA). O `amostra.md`
   promete "arrastar com um dedo". Pesa pouco no uso que o Gustavo descreveu (portal na mesa, com mouse), mas a
   página oferece o gesto e ele falha. A causa medida pelo QA (o fim do gesto ligado à perda de captura do ponteiro,
   disparada quando a área toma a captura do elemento tocado) está no relatório dele; é do UI engineer e do Prumo.
2. **A 1280 x 720 o cabeçalho segue com 185 px** (26% da altura), porque a legenda só recolhe abaixo de 1.100 px de
   largura. O nome "Gustavo" fica a uns 7 px dos botões de zoom (`ux-captura-1280x720.png`): fora deles, mas encostado.
3. Menor: a 960 x 800, a fileira de cenários corta o quarto botão no meio ("O Gustavo pede a um agente:"), sem degradê
   nem seta que diga que a fileira continua (`ux-captura-960x800.png`).

## As regras

- **Linhas sem se cruzar (R1): passa.** QA 0; no olho, nenhum cruzamento; os dois casos de leitura dos cenários
  (roxo colado e linha sobre o nome da Biblioteca) foram resolvidos.
- **Vista mais de cima (R2): passa.** A vista inicial é a mesma da volta 1 (27 rótulos, a planta aprovada), e o
  detalhe só aparece ao aproximar, arrumado.
- **Distância entre os itens (R3): passa.** Folga mínima de 22,3 px contra 19; razão de 1,53 (igual à volta 1: a
  planta não mudou).
- **Nomes (R4) e Papel na cidade (R5):** não é do meu papel.
- **Forma nova (R6): passa**, sem mudança.

Foco com Tab real: o QA conferiu as 23 paradas com foco visível nesta volta; eu as conferi na volta 1, e os consertos
não tocaram as regras de foco. Os sete cenários seguem com todos os números junto do que marcam (QA e minhas três
capturas).

## Notas

| # | Dimensão | Nota | Volta 1 | Por quê |
|---|---|---|---|---|
| 1 | Linhas (R1) | 5 | 4 | os dois defeitos de cenário resolvidos |
| 2 | Vista de cima (R2) | 5 | 5 | |
| 3 | Respiro (R3) | 4 | 4 | razão de 1,53, perto do limiar; etiquetas com respiro |
| 4 | Nomes (R4) | não é do meu papel | | |
| 5 | Papel na cidade (R5) | não é do meu papel | | |
| 6 | Forma nova (R6) | 5 | 5 | |
| 7 | Hierarquia visual | 5 | 4 | a 960 o cabeçalho deixou de pesar mais que a cidade |
| 8 | Composição | 4 | 3 | a 960 x 800 a cidade abre inteira; a 1280 x 720 o cabeçalho ainda ocupa um quarto da altura |
| 9 | Densidade | 3 | 3 | a 1280 o cabeçalho segue com os mesmos textos; a 960 ficou leve |
| 10 | Affordance (conforto do canvas) | 3 | 2 | com mouse e teclado ficou bom: arrasto exato, zoom no centro, sem seleção de texto. O arrasto com um dedo não anda |
| 11 | Cor | 4 | 4 | |
| 12 | Tipografia | 4 | 3 | a vista inicial não cai mais abaixo de 14 px; o "Ver tudo" a 320 deixa o texto em 5 px, mas é para se orientar, e a vista inicial ali é de 14 px |

## Veredito: **passa** (na minha parte)

R1, R2, R3 e R6 em "passa" e nenhuma dimensão abaixo de 3. O conforto com mouse e teclado, que era o motivo da volta,
está resolvido. O conserto 1 (o arrasto com um dedo) eu faria mesmo assim, antes de levar a peça ao Gustavo: é um
gesto que a página promete e não cumpre.

## Consertos

1. [Affordance] Arrasto com um dedo para depois de uns 8 a 12 px → não encerrar o gesto quando a perda de captura vem
   da própria área do desenho tomando a captura (ou tomar a captura logo no aperto do dedo, em vez de esperar os 6 px).
   Conferir com toque pelo protocolo do navegador: um arrasto de 96 x 48 px deve andar 96 x 48. Evidência:
   `qa/amostra-2/navegacao/toque.json`; minha medição: 8 x 4 de 96 x 48.
2. [Composição] A 1280 x 720 o cabeçalho ocupa 185 px → recolher a legenda no botão "Legenda" também quando a altura
   da janela for menor que uns 800 px, não só pela largura. Evidência: `ux-captura-1280x720.png`.
3. [Affordance] Fileira de cenários a 960 px corta o botão no meio → um degradê na borda direita da fileira (como o da
   faixa do desenho a 320), para dizer que há mais botões. Evidência: `ux-captura-960x800.png`.

## Não verificado

- Aparelho de toque de verdade; só toque pelo protocolo do Edge.
- Mouse e roda físicos (usei a entrada real do protocolo).
- Leitor de tela no diálogo da ficha a 320.
- O conteúdo (é do Tech lead) e o código (é do Prumo).
