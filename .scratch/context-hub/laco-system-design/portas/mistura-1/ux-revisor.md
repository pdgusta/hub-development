# Parecer do UX revisor, porta da mistura, volta 1

2026-10-15. Peça: `conceitos/mistura/mistura.html` ("A cidade e quem a aciona"). Roteiro:
`suite/skills/regua-da-cidade/como-julgar.md`. Com o relatório do QA (`qa/mistura-1/relatorio.md`) na mão. Antes,
revi as referências da régua (mapa de metrô e mesa de mapas elogiados; cidade radial v2 recusada: "tá tudo poluído…
precisa de distância entre os itens").

## Como medi

Edge via Playwright, servido em `127.0.0.1:8796`. Arquivos ao lado deste parecer:

- `ux-captura-1280.png` (visão geral, 1280 x 1000) e `ux-captura-320.png` (viewport real de 320, página inteira);
- `ux-olho-apertado.png`: a de 1280 reduzida a 320 px e borrada;
- `ux-detalhe-roxos.png`: recorte ampliado da coluna dos Agentes;
- `ux-foco-tab-gustavo.png`, `ux-foco-tab-interfaces.png`: foco com Tab real;
- `ux-ficha-teclado.png`, `ux-ficha-clique-componente.png`: a ficha;
- `ux-cenarios/<cenário>-<passo>.png`: todos os passos dos sete cenários a 1280 (41 capturas);
  `ux-cenario-gustavo-edita-320.png`: o último passo de um cenário a 320.

## Foco com Tab real: passa nas 19 paradas

Tab de verdade nas 19 paradas (7 botões de cenário, 9 bairros, 3 pessoas). As 19 casam `:focus-visible`. Para ver a
mudança, comparei pixel a pixel, dentro da caixa de cada item, a captura antes e depois do foco:

| Paradas | Pixels que mudam | O que se vê |
|---|---|---|
| 7 botões de cenário | 1.442 a 1.802 | contorno do botão |
| 9 bairros | 2.960 a 5.076 | contorno do bairro escuro e mais grosso |
| Maestro, Agentes, Gustavo | 402 a 418 | anel escuro com fundo amarelo-claro (`ux-foco-tab-gustavo.png`) |

A ordem segue a leitura: cenários, bairros de cima para baixo, depois as pessoas, e volta ao início. Enter num bairro
abre a ficha com o foco em "Fechar"; Esc fecha e devolve o foco ao bairro. Num cenário, a seta para a direita avança
o passo. O "não verificado" do QA se resolve: **passa**.

## As regras

- **Linhas sem se cruzar (R1): passa.** Evidência: QA 0 em todas as larguras; no olho, nenhum cruzamento. Mas a
  coluna dos Agentes tem um defeito de leitura: as linhas Contrato → Agentes e Checkpoint → Agentes descem em
  paralelo, **na mesma cor roxa, a uns 10 px uma da outra**, por 170 px (`ux-detalhe-roxos.png`). Leem como uma
  linha dupla; não dá para saber qual vem do Contrato e qual do Checkpoint sem abrir a ficha. As duas saídas do
  Contrato (para o Maestro e para os Agentes) também correm paralelas, a 15 px.
- **Vista mais de cima (R2): passa, no limite.** Evidência: 25 rótulos no desenho (limite exato). No olho apertado,
  os nove bairros se leem como manchas separadas, em três fileiras. O desenho, porém, carrega 20 ligações em 8 cores
  de linha, e a primeira tela tem 47 textos (título, faixa, legenda de 13 entradas em duas linhas, 7 botões). Com o
  B final tinha 10 ligações. Ver "Densidade".
- **Distância entre os itens (R3): passa, no limite.** Evidência: folga mínima de 24,1 px contra 21 (Porta do banco
  e Camada de busca); razão entre grupos de 1,53, a 0,03 do limiar. No olho: o tracejado amarelo do caminho "a
  decidir" desce a uns 10 px do começo do rótulo "Vista Markdown".
- **Nomes (R4) e Papel na cidade (R5):** não é do meu papel.
- **Forma nova (R6): passa.** Evidência: a planta da B continua, mas o que o leitor faz mudou. Agora ele segue a
  linha até quem aciona, e o cenário acende o caminho passo a passo. Não é a B com outra roupa: é outra pergunta
  respondida na mesma planta. Não repete forma recusada (sem centro, sem anéis, sem texto corrido no desenho).

## A leitura dos cenários: dá para seguir sem ler texto?

**Em parte.** Quando o passo acende uma linha, sim; quando acende só um bairro ou um prédio, não.

O que funciona muito bem: a cidade apaga, o passo 1 acende com o número no desenho, os passos se acumulam e o trajeto
se forma (`ux-cenarios/gustavo-edita-6.png`, `agente-novo-6.png`, `pede-alterar-7.png`). Os anteriores ficam acesos
com o número. É a melhor coisa da peça: responde "o que acontece se…" de um jeito que nenhum dos três conceitos
respondia.

| Cenário | Sem ler texto | Onde quebra |
|---|---|---|
| O Gustavo edita um arquivo | sim, até o 4 | 5 não acende nada novo (marca o Outro par, já aceso); 6 ("colisão") só acende a linha da vigia, nada diz "falha" |
| Um agente novo abre sessão | sim | 3 marca o nome do bairro Disciplina, não a checagem nem a vigia (a vigia acende sem linha) |
| Um maestro novo abre sessão | só até o 3 | 4, 5 e 6 acendem Ferramentas, Disciplina e Conteúdo, Acervo e Gustavo sem nenhuma linha: o caminho pula de bairro em bairro e só a frase explica |
| O Gustavo pede: leia | sim, até o 3 | 4 ("a porta avisa, a construir") não acende nada novo |
| O Gustavo pede: altere | sim | 7 (caminho em aberto) se lê bem: o tracejado acende |
| O Gustavo pede: remova | não nos passos 2 e 5 | 2 acende a Periferia e o Outro par sem linha (o script do arquivo morto não tem desenho); 5 acende o Conteúdo e o Gustavo sem linha |
| O outro par altera um arquivo | sim, até o 4 | 5 (colisão) como no primeiro |

Mais três problemas dos cenários:

1. **O fim de cada cenário não se distingue.** Cinco cenários terminam numa falha ou em algo em aberto (colisão, "a
   construir", "a decidir"), mas a marca do último passo é igual à dos outros. Sem ler a faixa, quem olha não sabe
   que ali o caminho falha.
2. **Números em cima de nomes:** o 6 cobre o "V" de "Vigia do sync" (`gustavo-edita-6.png`); o 4 cobre o fim de
   "Ferramentas da máquina" e o 5 encosta em "Disciplina do agente" (`maestro-novo-6.png`); o 3 cobre o "V" de "Vista
   Markdown" (`pede-remover-5.png`).
3. **A faixa do passo empurra o desenho para baixo.** Com um cenário ligado, a faixa entra entre os botões e o
   desenho (uns 60 px), e a fileira de baixo sai da tela a 1280 x 1000: os nomes "Interfaces do Gustavo" e "Periferia
   do par" ficam cortados. Numa tela de notebook comum (uns 700 px de altura útil), o Gustavo e o Obsidian, que abrem
   o primeiro cenário, ficariam fora da tela. A 320, a faixa do desenho não rola até o passo aceso: no último passo
   de "O Gustavo edita", os passos 1, 4 e 5 estão fora da tela (`ux-cenario-gustavo-edita-320.png`).

## Notas

| # | Dimensão | Nota | Por quê |
|---|---|---|---|
| 1 | Linhas (R1) | 3 | sem cruzamento; dois roxos colados a 10 px na coluna dos Agentes, sem como saber qual é qual |
| 2 | Vista de cima (R2) | 3 | 25 rótulos e nove manchas, mas 20 linhas em 8 cores; lê, com esforço |
| 3 | Respiro (R3) | 3 | razão a 0,03 do limiar; números de passo sobre nomes |
| 4 | Nomes (R4) | não é do meu papel | |
| 5 | Papel na cidade (R5) | não é do meu papel | |
| 6 | Forma nova (R6) | 5 | quem aciona e o cenário mudam o que o leitor faz |
| 7 | Hierarquia visual | 4 | o Banco local segura o olhar; mas o caminho "a decidir", com halo amarelo, é a linha mais chamativa da visão geral, mais que as decididas. Nos cenários a hierarquia é ótima (apagado e aceso) |
| 8 | Composição | 3 | cabe exata em 1280 x 1000 (página de 1002 px); com cenário ligado a fileira de baixo sai da tela |
| 9 | Densidade | 3 | 47 textos na primeira tela; legenda de 13 entradas que é preciso ler para decodificar as cores. É o ponto de maior risco diante da recusa da cidade radial ("tá tudo poluído") |
| 10 | Affordance | 4 | foco 19 de 19; botões de cenário claros, com `aria-pressed` e estado escuro; clicar num componente abre a ficha do bairro no topo, não no componente (`ux-ficha-clique-componente.png`: cliquei no Sincronizador, a ficha abre no Banco local) |
| 11 | Cor | 3 | magenta (maestro) e roxo (regras) são vizinhos e correm juntos perto do Maestro; o azul-ardósia da troca é parente do azul dos agentes. A regra "a cor é quem aciona" vale para agentes, Gustavo e maestro, mas vigia, disco e banco, troca e regras são cores de tipo: duas lógicas na mesma legenda |
| 12 | Tipografia | 4 | rótulos e fichas confortáveis; números de passo sobre nomes; a 320 os rótulos do desenho caem para uns 10 px |

## Veredito: **passa** (na minha parte)

R1, R2, R3 e R6 em "passa" e nenhuma dimensão abaixo de 3. **Passa no limite:** cinco dimensões em 3, duas regras no
limite numérico (25 rótulos; razão de 1,53). Os consertos 1 a 6 abaixo baixam o risco de o Gustavo ler a peça como
"poluída", e eu os faria antes de levá-la a ele. Nenhum pede rótulo novo.

## Consertos

1. [Linhas (R1)] Coluna dos Agentes: Contrato → Agentes e Checkpoint → Agentes descem coladas, no mesmo roxo → fundir
   as duas num só traço a partir da muralha (as regras chegam juntas ao agente) ou separar a descida do Checkpoint
   para o outro lado dos Agentes (pela direita, junto da borda de Portas), com pelo menos 30 px entre as duas.
   Evidência: `ux-detalhe-roxos.png`.
2. [Cenários] Último passo de falha ou em aberto → dar a esse número outra forma (losango ou triângulo de aviso, na
   cor de alerta) e acender o elemento em falha com contorno tracejado vermelho, para ler "aqui falha" sem a frase.
   Vale para gustavo-edita 6, pede-ler 4, pede-alterar 7, pede-remover 5 e outro-par 5.
3. [Cenários] Passos que acendem bairro sem linha (maestro-novo 4, 5 e 6; pede-remover 2 e 5; agente-novo 3) →
   acender também uma linha fina, só no estado de cenário (não na visão geral, para não somar ligação), do ator até o
   bairro: Maestro → Ferramentas, Maestro → Disciplina, Acervo → Gustavo (aval), Agentes → Periferia (script do
   arquivo morto). Se não houver ligação de verdade na descrição, combinar com o Tech lead; o que não puder virar
   linha fica com a frase, mas o número deve ir no componente (não no nome do bairro).
4. [Composição] Faixa do passo empurra o desenho → pôr a faixa sobreposta ao topo do desenho (dentro da área vazia
   entre a muralha e os botões, que já tem uns 40 px) ou trocar os botões pela faixa enquanto o cenário está ligado,
   para a cidade não descer. Conferir a 1280 x 720.
5. [Densidade e Cor] Legenda de 13 entradas e duas lógicas de cor → separar a legenda em duas linhas com título curto
   ("quem aciona": agentes, Gustavo, maestro; "o que corre": regras, relógio, vigia, disco e banco, troca, a decidir, a
   construir) e afastar o magenta do maestro do roxo das regras (puxar o maestro para um vinho mais quente ou as
   regras para um índigo). Sem rótulo novo no desenho.
6. [Hierarquia] Caminho "a decidir" com halo amarelo é a linha mais forte da visão geral → baixar o halo para um
   amarelo mais claro e fino na visão geral; manter o halo forte só quando o cenário acende esse caminho.
7. [Respiro (R3)] Números de passo sobre nomes ("Vigia do sync", "Ferramentas da máquina", "Vista Markdown",
   "Disciplina do agente") → posicionar cada número a pelo menos 6 px de qualquer texto, preferindo o lado do traço
   oposto ao rótulo.
8. [Respiro (R3)] Tracejado "a decidir" a 10 px de "Vista Markdown" → descer o tracejado pela esquerda da vitrine ou
   subir o rótulo para cima dela.
9. [Affordance] Clicar num componente abre a ficha no topo do bairro → rolar a ficha até o componente clicado e
   realçá-lo (fundo claro por 1 s), como o `mistura.md` promete ("abre a ficha do bairro já nele").
10. [320 px] Num cenário, a faixa do desenho fica parada no Banco local → rolar a faixa até a marca do passo atual a
    cada passo (com o passo anterior ainda à vista, se couber).

## Não verificado

- Larguras 768 e 1920 com o olho (ficam os números do QA).
- Contraste do estado apagado (é de propósito; os nomes apagados não precisam ser lidos, mas não medi).
- Leitor de tela no anúncio dos passos (`aria-live` existe; não ouvi).
- O conteúdo de cada passo contra a descrição v3.2: é do Tech lead.
