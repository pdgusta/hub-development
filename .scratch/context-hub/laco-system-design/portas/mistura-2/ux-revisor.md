# Parecer do UX revisor, porta da mistura, volta 2

2026-10-15. Peça: `conceitos/mistura/mistura.html` (volta 2). Conferi primeiro os 10 consertos do meu parecer da volta
1 (`portas/mistura-1/ux-revisor.md`) contra `conceitos/mistura/consertos.md` e a peça; depois, só os problemas que os
consertos criaram. Relatório do QA: `qa/mistura-2/relatorio.md`.

## Como medi

Edge via Playwright, servido em `127.0.0.1:8797`. Arquivos ao lado deste parecer:

- `ux-captura-1280.png` (1280 x 1000), `ux-captura-1280x720.png`, `ux-captura-320.png` (viewport real de 320);
- `ux-cenarios/<cenário>-<passo>.png`: os 39 passos dos sete cenários a 1280 x 1000;
- `ux-cenario-720-gustavo-edita-6.png`, `ux-cenario-720-maestro-novo-6.png`: último passo a 1280 x 720;
- `ux-cenario-320-passo1.png`, `ux-cenario-320-passo4.png`: "O Gustavo edita" a 320;
- `ux-foco-tab-maestro.png`; `ux-ficha-clique-componente.png` (clique no ícone do Sincronizador); `ux-apos-esc.png`.

## Foco com Tab real: passa nas 19 paradas

As 19 paradas casam `:focus-visible` e mudam na tela: 7 botões (1.442 a 1.802 px), 9 bairros (2.960 a 5.060 px) e
3 pessoas com o anel amarelo (404 a 409 px). Mesma ordem da volta 1. **Passa.**

## Conferência dos consertos da volta 1

| # | Meu conserto | Situação | Aceito? |
|---|---|---|---|
| 1 | Dois roxos colados até os Agentes | feito: só o roxo do Contrato chega aos Agentes; o do Checkpoint saiu do desenho (foi para a ficha, pelo conserto do Tech lead) | sim. A azul nova (Agentes → Nota de retomada) sobe a 47 px do roxo |
| 2 | Último passo de falha igual aos outros | feito: triângulo vermelho, linha vermelha tracejada, brilho vermelho no componente, contorno tracejado no bairro, "falha ou em aberto" na faixa | sim; nos cinco cenários se lê "aqui falha" sem a frase (`gustavo-edita-6.png`, `pede-remover-5.png`) |
| 3 | Passos que acendem bairro sem linha | feito em parte: "maestro novo" 4 e 6 e "remova" 2 e 3 ganharam linha; sem Agentes → Periferia nem Acervo → Gustavo | sim. Os motivos são bons: a primeira não está na descrição; o aval sai do maestro (`decisoes.md`, 16 e 17) |
| 4 | Faixa do passo empurra o desenho | feito: no cenário, a faixa toma o lugar da legenda e dos botões, e a cidade encolhe para caber | sim; a 1280 x 1000 e a 1280 x 720 a cidade inteira fica na tela (`ux-cenario-720-gustavo-edita-6.png`) |
| 5 | Legenda de 13 entradas, duas lógicas de cor | feito: "Quem aciona" e "O que corre"; maestro em verde-azulado; 7 tipos de traço | sim |
| 6 | Halo amarelo do "a decidir" forte demais | feito: mais claro e fino na visão geral, forte só no cenário | sim; a linha já não é a mais chamativa |
| 7 | Números de passo sobre nomes | feito: o número procura um lugar a pelo menos 6 px de todo texto | sim, sem sobreposição (QA: 0). Mas criou o problema novo 3 |
| 8 | Tracejado a 10 px de "Vista Markdown" | feito: o nome foi para a direita | sim |
| 9 | Clique num componente abre a ficha no topo | feito: clicando no ícone, a ficha rola até o componente e o realça em amarelo (`ux-ficha-clique-componente.png`) | sim. Detalhe: clicando no vão entre o ícone e o nome (dentro da caixa do item), o clique cai no bairro e a ficha abre no topo |
| 10 | A 320, a faixa não segue o passo | feito: a faixa rola até o número do passo atual | sim (`ux-cenario-320-passo1.png`: abre no Gustavo e no Obsidian) |

## Problemas novos

1. **Falta o número 5 em "O Gustavo edita um arquivo".** No passo 5 acendem dois quarteirões da miniatura do outro
   par, mas nenhum número aparece; no passo 6 a sequência vai de 4 para o triângulo 6 (`ux-cenarios/gustavo-edita-5.png`
   e `-6.png`). Confirma o que o QA mediu. Sem o número, quem segue sem ler não sabe o que o passo 5 acendeu: os
   quarteirões novos ficam ao lado do 4, que já estava aceso.
2. **O botão do cenário fica "ligado" depois de sair.** Com "Sair do cenário" ou Esc, o cenário apaga, mas o botão
   continua escuro (o estilo de selecionado) e com `aria-pressed="true"` (`ux-apos-esc.png`; conferido em "leia" e
   "outro par"). Quem olha acha que há um cenário ligado; o leitor de tela anuncia "pressionado". Na volta 1 o estado
   acompanhava (QA da volta 1); é regressão.
3. **Alguns números ficaram longe do que marcam.** A regra dos 6 px funciona, mas o número às vezes vai parar longe
   do componente: o 3 de "agente novo" fica uns 170 px à direita da Nota de retomada, mais perto do Acervo do maestro
   (`agente-novo-6.png`); o triângulo 6 de "O Gustavo edita" fica uns 120 px abaixo da vigia, no meio do bairro vazio
   (`gustavo-edita-6.png`); o 5 de "maestro novo" flutua entre "Nota de retomada" e o Acervo (`maestro-novo-6.png`).
   Não engana muito (o elemento aceso ajuda), mas pede um passo de busca do olho.
4. Menor: no "maestro novo", a linha Maestro → Biblioteca do Maestri contorna a cidade inteira (sobe, corre por cima,
   desce pela direita e volta por baixo) e passa raspando a borda da caixa de Fora do par (`maestro-novo-6.png`).
   Aceito o motivo (`decisoes.md`, 15: só no cenário, sem cruzar), mas é o traço mais longo da peça.
5. Menor: a 1280 x 1000 a página tem 1014 px de altura (14 px de rolagem). O `consertos.md` diz que voltou a caber.

## As regras

- **Linhas sem se cruzar (R1): passa.** QA 0; no olho, nenhum cruzamento e não há mais traços da mesma cor colados.
- **Vista mais de cima (R2): passa**, no limite de 25 rótulos. A visão geral ficou mais calma: legenda em duas linhas
  com título, halo do "a decidir" mais leve, 7 tipos de traço.
- **Distância entre os itens (R3): passa.** Folga mínima de 24,1 px; razão entre grupos de 1,68 (era 1,53, agora com
  margem).
- **Nomes (R4) e Papel na cidade (R5):** não é do meu papel.
- **Forma nova (R6): passa**, sem mudança.

## Os cenários sem texto

**Seis de sete se seguem sem ler**, contra cinco na volta 1. "Um maestro novo" e "remova" agora têm linha em cada
passo, e o passo de falha se vê. O que quebra é o passo 5 de "O Gustavo edita" (problema novo 1), e, mais leve, os
números que caem longe do componente (problema novo 3).

## Notas

| # | Dimensão | Nota | Volta 1 | Por quê |
|---|---|---|---|---|
| 1 | Linhas (R1) | 4 | 3 | os roxos colados saíram; a linha da biblioteca é longa, só no cenário |
| 2 | Vista de cima (R2) | 4 | 3 | legenda organizada, halo calmo, um tipo de traço a menos |
| 3 | Respiro (R3) | 4 | 3 | razão de 1,68; nenhum número sobre texto |
| 4 | Nomes (R4) | não é do meu papel | | |
| 5 | Papel na cidade (R5) | não é do meu papel | | |
| 6 | Forma nova (R6) | 5 | 5 | |
| 7 | Hierarquia visual | 5 | 4 | o "a decidir" deixou de gritar; no cenário, o apagado e o aceso ordenam tudo; a falha em vermelho se destaca |
| 8 | Composição | 4 | 3 | o cenário cabe na tela a 1000 e a 720; 14 px de sobra na visão geral |
| 9 | Densidade | 3 | 3 | 20 linhas na visão geral e 49 textos na primeira tela (eram 47); a legenda ajuda, mas segue sendo muita coisa ao mesmo tempo |
| 10 | Affordance | 3 | 4 | a ficha agora vai ao componente; mas o botão fica "ligado" depois de sair do cenário |
| 11 | Cor | 4 | 3 | maestro afastado das regras; duas famílias na legenda |
| 12 | Tipografia | 4 | 4 | a 1280 x 720, com a cidade encolhida, os rótulos caem para uns 11 px |

## Veredito: **passa** (na minha parte)

R1, R2, R3 e R6 em "passa" e nenhuma dimensão abaixo de 3. Os consertos 1 e 2 são pequenos e eu os faria antes de levar
a peça ao Gustavo: um número que falta e um botão que mente o estado são os dois defeitos que ele pode ver no primeiro
uso.

## Consertos

1. [Cenários] "O Gustavo edita", passo 5: o número não é desenhado → desenhar o 5 junto dos quarteirões da vista e da
   busca na miniatura do outro par (o QA aponta que o passo acende dois `rect` sem marcação; o número deve procurar
   lugar em volta deles). Evidência: `ux-cenarios/gustavo-edita-5.png`.
2. [Affordance] Botão do cenário depois de "Sair" ou Esc: segue escuro e com `aria-pressed="true"` → ao sair, voltar
   `aria-pressed` para `false` e tirar o estilo de selecionado de todos os botões. Evidência: `ux-apos-esc.png`.
3. [Cenários] Números longe do que marcam → limitar a busca de lugar a uns 40 px do componente ou da linha marcada;
   se não houver lugar livre nesse raio, encostar o número no próprio componente (do lado oposto ao nome). Casos:
   "agente novo" 3, "O Gustavo edita" 6, "maestro novo" 5.
4. [Affordance] Clique no vão entre o ícone e o nome do componente abre o bairro no topo → fazer a área de clique do
   item cobrir também o nome (um retângulo transparente que envolva ícone e rótulo).
5. [Composição] A 1280 x 1000 a página tem 1014 px → tirar 14 px (margem de baixo ou o vão entre os botões e a
   muralha), para a visão geral caber sem rolar.

## Não verificado

- Larguras 768 e 1920 com o olho (ficam os números do QA).
- Leitor de tela nos passos (`aria-live`) e no `aria-pressed`: só li o atributo, não ouvi.
- O conteúdo de cada passo contra a descrição v3.2: é do Tech lead.
