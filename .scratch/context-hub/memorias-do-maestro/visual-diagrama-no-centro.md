---
name: visual-diagrama-no-centro
description: "Página visual elogiada pelo Gustavo: diagrama como centro (mapa de metrô do roteamento da pesquisa), texto só em rótulos e chips"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 23513d86-deee-4546-ab74-76dd68ba90ef
  modified: 2026-10-16T21:34:53.717Z
---

O Gustavo elogiou ("preciso elogiar o designer. parabéns") a página `prototipos/prototipo-09-roteamento-da-pesquisa.html` (2026-10-13): linguagem de mapa de metrô, diagramas no centro (princípio, linha de estações com pátio separado, máquina de estados com setas de volta coloridas, curva de saturação), cartões de chips em vez de parágrafos, perguntas no fim com a recomendação.

**Why:** ele pediu "mostre com o Designer, não por texto"; o formato diagrama-primeiro acertou.
**How to apply:** em páginas de rodada, fazer o diagrama carregar a explicação; texto só em rótulos curtos e chips; cada visual com linguagem própria. Relaciona com [[prototipo-e-explicacao]] e [[visuais-pelo-designer]].

Segundo elogio direto do Gustavo (2026-10-13): o painel ao vivo `laco/painel/index.html` ("maré de novos": cada onda do laço vira uma onda do mar rumo à linha de parada dos 5%; medidores de combustível para o teto; matriz de pedidos; osciloscópio). Metáfora visual única que carrega a pergunta principal + números grandes + quase nenhum texto acertou de novo.

Contraexemplo (2026-10-14): a página da síntese da pesquisa ampla (`laco/painel/sintese.html`, "laudo de potabilidade", serifa editorial, 6 seções densas) não agradou: "muita informação", "a fonte eu não curti", "texto demais"; ele entendeu "depois de um tempo lendo cada seção". Regra dele: **"simplificar não é cortar info, é comunicar a mesma coisa porém de uma melhor forma"**. Em páginas de síntese, levar o detalhe para camadas (expandir, passar o mouse, link para o anexo) e não empilhar seções de texto.
A v2 ("mapa do hub": mesma página de 6 seções empilhadas, com outra fonte e outras cores) também foi recusada: "ele só mudou a estilização". Pedir "se reinventar" significa mudar a **forma** de comunicar (estrutura, interação, narrativa), não o acabamento. Na refação, dar `/clear` no Designer e mandar um briefing completo com o que não repetir.

Portal do projeto, 1ª versão (tema "Torre de controle", noite, Big Shoulders + IBM Plex), 2026-10-14: "não gostei da
tipografia, pois não ta legível, as letras estão muito finas [...] não ta aquela fonte gostosa de ler. E também Quero
um design 'aconchegante', mais 'vivo' e mais 'interativo'". Regra: texto corrido com fonte de leitura confortável e
peso suficiente; fonte fina ou condensada só em título grande.

Portal v2 "Mesa de mapas" (dia, papel creme, Nunito Sans 16 px, Fraunces nos títulos), 2026-10-14: "design bom,
aconchegante e gostoso de ler, acertou em cheio". Mas a "trilha até o cume" (triângulos soltos ligados por setas
tracejadas) foi recusada: "triangulos soltos sem sentido nenhum"; pediu reinventar, simplificar e usar mais espaço.
Lição: ícone abstrato espalhado num grafo não comunica caminho; o progresso precisa ler de relance.

System design, 2026-10-14: a amostra "planta técnica em papel vegetal" foi recusada ("você só mudou o estilo, mas o
diagrama está literalmente o mesmo"), mesmo com o pedido dizendo "estilo totalmente diferente, mas mantendo a ideia
de diagrama". Ele quer uma metáfora nova: uma cidade vista de cima em 2.5D, bairros por cor, ícones, pouco texto,
visual clean. Regra reforçada: manter o **conteúdo** não é manter a **disposição**. O desenho tem de ser
reimaginado, e o briefing ao Designer deve dizer isso com todas as letras.

Elogio de 2026-10-14: a carta `prototipo-12-ritmos` ("Como você já faz × como seria ideal"), aprovada com "o design
ficou sensacional parabéns". Ela tem três partes: o `initiative.md` real explodindo em barras proporcionais e virando
seis arquivos por ritmo; os nomes de hoje convergindo para blocos; e a pilha por tipo com exemplos reais. O que
acertou: **dados reais dele, medidos, em escala**, e o antes × depois. Ele também elogiou o levantamento.

Cidade radial v2 (system design), 2026-10-14, recusada: "tá tudo poluído… não dá pra bater o olho e entender.
Precisa de distância entre os itens." Lição: 28 peças com rótulos, ruas, anéis e legenda numa tela só viram poluição,
mesmo sem linhas cruzadas. É preciso respiro entre os itens e menos coisas competindo pelo olhar. Ele quer refazer por
um laço próprio, com um especialista em diagramas de system design e outro em UI e UX (poluição visual, espaço
concorrente, disposição, separação lógica). Ver [[visuais-pelo-designer]].

Mistura da cidade (system design), 2026-10-15, **aprovada sem alteração**: "absolutamente perfeito... você encontrou a
forma perfeita de mostrar cada cenário". Ela veio de uma descrição do hub testada antes (perguntas escondidas, três
voltas) e passou por porta (QA, UX revisor, Tech lead). O que acertou: cenários acesos passo a passo no próprio desenho
(escolher "o Gustavo edita um arquivo" e ver o caminho numerado), cor da linha = quem aciona, nenhum componente solto,
detalhe nas fichas. Ele tirou o teto de 25 rótulos: pode haver mais, desde que folga e separação sigam sem poluição.

Carta `escolhas-2-vigia` (2026-10-16, Aquarela, revisada pelo Lente), aprovada com "perfeito, gostei demais do design
dessa carta": "caderno de aquarela do faroleiro", três tintas para os níveis (ok, informa, divergência), uma folha por
escolha com problema, cena desenhada e "com a escolha × sem ela", resumo numerado no fim na ordem da rodada. Feita com
um designer por carta e um revisor de UI/UX passando em até duas voltas.

Carta `plano-de-construcao` (2026-10-16, Aquarela, "ateliê de costura": fita métrica = etapas, fios = entregas,
alinhavo = exemplo trocado depois), aprovada: "design incrível também. Os designers estão pegando o jeito. Só achei a
tipografia dos títulos difícil de ler". Título decorativo precisa ser legível de relance, não só bonito.

Carta 2 das escolhas do spec, "Vigia e manutenção" (`.scratch/construcao-do-hub/revisao/cartas/carta-2-vigia.html`),
2026-10-16, aprovada: "perfeito, gostei demais do design dessa carta". Linguagem: caderno de aquarela de um faroleiro
(papel creme com grão, pigmentos por filtro SVG, Caveat nos rótulos, Fraunces nos títulos). Três cores para os níveis
(ok, informa, divergência). Uma folha por escolha: problema, cena desenhada, depois "com a escolha × sem ela". No fim,
resumo numerado como na rodada. No celular, a cena fica numa moldura que rola para o lado, com a dica "arraste".

Carta 1 das escolhas do spec, "Gravar e ler no banco" (`.scratch/construcao-do-hub/revisao/cartas/carta-1-banco.html`,
Designer, revisada pelo Lente em duas voltas), 2026-10-16, aprovada: "carta bastante criativa, parabéns". Linguagem:
agência bancária impressa como cédula (papel creme, rosácea e faixas de guilhoché geradas por script, carimbos
vermelhos). Metáfora que carrega o assunto: guichê = MCP do banco, cofre = CouchDB, agente = cliente da agência. Mapa
"A agência" no topo, com um selo numerado onde mora cada escolha; por escolha, o problema numa linha que termina na
pergunta, o desenho com a escolha do spec (quadro firme e carimbo) ao lado das alternativas (quadro tracejado), e a
escolha e a alternativa em legenda abaixo; no fim, um "extrato" numerado como na rodada. Lição da volta 1 do Lente:
desenhar cada opção como desenho próprio, para empilhar no celular, e manter o texto do desenho em pelo menos 12 px.

Carta do plano de construção (`.scratch/construcao-do-hub/revisao/plano/carta-plano.html`, Aquarela, revisada pelo
Lente em duas voltas), 2026-10-16, aprovada: "design incrível também, os designers estão pegando o jeito". Linguagem:
ateliê de costura (fita métrica = etapas, fio colorido = entrega, carretel = onde nasce, nó = onde é usada, alinhavo
tracejado = vai com exemplo, portão entre etapas). **Ressalva do Gustavo: a tipografia dos títulos ficou difícil de
ler** (Bodoni Moda 800, didone de alto contraste, em h1/h2 e títulos de quadro). **Como aplicar:** nos próximos visuais,
título com fonte de leitura fácil (contraste baixo, peso médio); a fonte de efeito, se houver, fica em palavra curta
de destaque, não no título inteiro. Lição do Lente: no celular, a etapa e o que ela usa precisam aparecer juntos, sem
arrastar (virou lista com chips); marcador entre etapas não pode sugerir que tudo já passou (portão vazado, não check).
