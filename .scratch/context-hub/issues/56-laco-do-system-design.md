# Laço do system design

Type: task
Status: claimed
Blocked by:

## Question

Um laço próprio, acompanhado na página Laços do portal, para refazer o `system-design.html` do zero com a ideia de
cidade e analogia (cada item com seu papel), depois da cidade radial v2 recusada em 2026-10-14 ("tudo poluído… precisa
de distância entre os itens"; critérios na nota do system design no `map.md`). Dois especialistas: um em system design
e diagramas, um em UI e UX. Etapa inicial: absorver o vídeo https://youtu.be/Ysr7oNDajJI ("Insane Claude Design Skills
You Need To Actually Build Beautiful Sites", AI LABS, 12:55, 2026-08-24) para melhorar o recruta Designer. Pedido do
Gustavo, 2026-10-15. Fora do mapa (peça do portal e dos visuais), como os tickets 53 e 55.

## Comments
- 2026-10-15: proposta do laço aberta como rodada 1 no portal
  (`portal/rodadas/2026-10-15-laco-do-system-design-r1.md`).
- 2026-10-15 08:31, rodada 1 respondida (envio `a97e9fe8-5f4a-4235-af13-d8819185c2fb`): perguntas em branco e "não quero
  essa proposta aqui, quero que a proposta já esteja na página de laços". **Feito:** laço `system-design` montado em
  `laco-system-design/` (`laco.json`, `config.json` com os valores recomendados, `estado.json`, `LEIA.md`) e
  registrado no topo de `portal/lacos.json`. Doze nós (as etapas, a régua, o teto e o Designer coordenando), dez
  controles (forma dos especialistas, fonte do vídeo, quantos conceitos, modelo e esforço de cada especialista, harness
  do de UI e UX, voltas, orçamento) e a capacidade de parar. Sem `sinal.txt` até começar: aparece como "estado
  desconhecido". **Rodada 2 aberta** (só "começar?"), que põe o laço em "Espera você".
- 2026-10-15 08:42, comentário do Gustavo no laço inteiro (envio `ce3f8aa5-2ec6-417d-9b1b-31546837c59e`, lido; comentário
  não tem desfecho além de `lida`, §4.5): "o vídeo … é só uma lista de skills que ao usar elas, o agente fica melhor em
  design. … não precisa transcrever, só por yt-dlp e prints do vídeo você consegue colher todas as skills. Quero loop
  disso, cada subagente Haiku 5.5 com um trecho. Com todas as skills em mão, nós revisitamos este laço que você vai
  alterar conforme o resultado da coleta das skills." **Feito:** rodada 2 (começar?) suspensa, porque o laço vai mudar;
  vídeo baixado por yt-dlp em `C:\Projetos\laco-video-skills\` (a legenda automática deu HTTP 429, e ele não quer
  transcrição); 258 quadros, um a cada 3 s; **dez subagentes Haiku 5.5**, um trecho de ~78 s cada, gravam em
  `trechos/trecho-NN.md`. No laço, o nó do vídeo virou "Colher as skills do vídeo" e o controle da fonte do vídeo saiu.
- 2026-10-15 ~09h05: coleta feita. Os dez Haiku gastaram ~1,03 milhão de tokens. Lista juntada pelo maestro em
  `laco-system-design/skills-do-video.md`: 8 coleções (emilkowalski/skill, ConardLi/garden-skills,
  elayadesign/ai-design-skills, MengTo/Skills, jakubkrehel/skills, codeswithroh/tastemaker,
  Owl-Listener/designer-skills e o conjunto do próprio vídeo), perto de 90 skills, só o que apareceu na tela.
  **Laço revisto** (conforme o comentário): depois da coleta, "Ler as skills na fonte" (um subagente por coleção),
  "Você escolhe as skills" (controles `skills_diagramas` e `skills_uiux`, tipo lista, com a sugestão do maestro) e
  "Instalar as skills" (escopo de projeto dos especialistas). Os conceitos saem lado a lado num seletor. Novo controle
  `fonte_modelo` (Haiku por padrão). **Rodada 3 aberta**: seguir até a escolha das skills.
- 2026-10-15 09:11, comentário do Gustavo no laço inteiro (envio `a490a680-d53a-4f6c-99a3-90d5f11e13d4`, lido): não quer
  escolher skills. A leitura deve separar as skills em categorias, com nomes tirados do conteúdo, e o maestro ou outro
  agente julga e devolve em laço até aprovar a suíte de design. Depois sobem agentes com papéis e skills adequadas, de
  invocação autônoma: UI engineer, UX revisor, Tech lead e QA tester. O Tech lead conhece o hub; um laço entre ele e o
  maestro define um texto padrão do hub, que serve de base para qualquer diagrama, com as rodadas definidas pelo
  maestro. Gostou do laço central dos conceitos de cidade, mas o crítico não é ele: a porta é o Tech lead com outro
  revisor. Ele só aprova antes de construir a amostra, vendo amostras de direção visual. "Não inicie nada, só me
  apresente aqui no laço como você pretende construir e orquestrar tudo isso."
  **Feito:** rodada 3 suspensa. Laço reescrito com 17 nós em quatro fases (suíte, equipe, conceitos, amostra) e 13
  controles (modelos, esforço, voltas, orçamento de 1,6 milhão). Plano detalhado em
  `laco-system-design/orquestracao.md`. Sem `sinal.txt`, o laço aparece como "estado desconhecido". **Rodada 4
  aberta:** aprovar o plano.
- 2026-10-15 09:22–09:23, pedidos do Gustavo pela página Laços: **aplicados** com recibo (§4.5; `efeito: aguarda`,
  porque valem na próxima execução): orçamento de 1,6 para **5 milhões** de tokens (envio
  `92397366-3566-4842-982a-c61ce539372e`), voltas da amostra de 3 para **6** (`9fe95ecb-f83f-4d52-8a66-3b91a4f96f9f`),
  voltas dos conceitos de 3 para **4** (`6e4b8f4f-9310-4e97-8579-5295d2f1e9ea`). Comentário no laço (envio
  `f54d093d-856a-4369-b377-5d06cbe877a9`, lido): "a régua em si também pode ser a utilização de skills adequadas (acho
  que a skill taste faz isso)". **Feito:** a régua passa a ser aplicada também por skills da suíte (tastemaker e
  afins, escolhidas no julgamento das categorias); nó e `orquestracao.md` atualizados.
- 2026-10-15 09:33, pedido do Gustavo pela página: esforço da equipe de alto para **médio** (envio
  `89645c07-4385-4cee-91fb-e9569133fa0a`), **aplicado** com recibo (`efeito: aguarda`, vale na próxima execução).
- 2026-10-15 09:34, **rodada 4 respondida** (envio `be448aab-a868-40e5-bc43-c7cc4d4ebda7`): **plano = A**, aprovado; o
  maestro começa pela fase da suíte de skills e segue sozinho até a carta da direção visual.
  **Feito (09h35):** execução `system-design-2026-10-15` aberta no `laco.json`; os quatro pedidos aplicados passaram a
  `efeito: valeu`. Repositórios confirmados pela API do GitHub, todos MIT: `emilkowalski/skills` (o `skill` redireciona),
  `ConardLi/garden-skills`, `elayadesign/ai-design-skills`, `MengTo/Skills`, `jakubkrehel/skills`,
  `codeswithroh/tastemaker`, `Owl-Listener/designer-skills`. O conjunto do próprio vídeo não foi achado ainda.
  **Ler na fonte em curso:** oito Haiku 5.5, um por coleção, gravam em `laco-system-design/suite/fichas/` (sem clonar,
  instalar nem rodar nada).
- 2026-10-15 ~10h: **leitura na fonte feita** (8 Haiku, ~1,24 milhão de tokens do Haiku, acima da estimativa de 400 mil):
  fichas em `laco-system-design/suite/fichas/`. Emil Kowalski: 15 skills, só texto. garden-skills: 6. elayadesign: 1
  (cita `elayadesign/redesign-skill`, não fichada). MengTo: 33 (20 de jogos, em ficha curta). jakubkrehel: 14, entre
  elas a `technical-drawing`, com scripts Node, que pode servir a diagramas. tastemaker: 2 skills e 23 scripts; riscos:
  `recolor_svg.py` regrava sem cópia de segurança, a skill manda rodar `npx shadcn add` e grava memória em
  `~/.tastemaker/`; rede só para uma lista fixa de sites. Owl-Listener: 111 skills e 34 comandos, só texto (outros 24
  plugins do marketplace, de outros repositórios, não lidos). Conjunto do vídeo: repositório não achado; screen-critique
  e perception-laws não existem com esse nome, e os mais próximos são a crítica de tela e as `law-of-*` do Owl-Listener.
  **Montar categorias em curso:** um Sonnet 5.5 grava `suite/categorias.md`.
- 2026-10-15 ~10h25: **categorias v1** (Sonnet 5.5, ~220 mil tokens) em `suite/categorias.md`: 11 categorias com nomes
  tirados do conteúdo; suíte de 24 skills (UI engineer 14, UX revisor 7, Tech lead 2, QA 4). **Julgamento do maestro:
  volta 1** (`suite/julgamento-v1.md`). Skills manuais ficam manuais e são chamadas por "/nome" no ask. Os plugins
  `design:*` do usuário são desligados por pasta de papel. A cópia do `web-design-engineer` é editada: sem esperar o
  usuário e sem o Direction Advisor. O tastemaker sai como skill (fica só o `check_contrast.py`, e as referências do
  Gustavo vão como imagens). Duas skills nossas a escrever: `regua-da-cidade` e `medidas-da-peca` (cruzamentos,
  distâncias, links, peso, contraste). A primeira amostra é estática. A v2 em curso, no mesmo agente.
- 2026-10-15 ~10h20: **categorias v2** (mesmo Sonnet, ~290 mil tokens no total do agente) **aprovadas na volta 2**:
  `suite/suite.md` (25 skills: UI engineer 14, UX revisor 8, Tech lead 3, QA 4; detalhe em `suite/categorias-v2.md`).
  Na aprovação, o maestro fixou os limiares da régua (no máximo 25 rótulos na visão geral; folga de 1 altura de
  rótulo; razão de 1,5 entre o espaço entre grupos e o de dentro do grupo) e as referências: elogiados, o mapa de metrô
  `prototipo-09`, a maré e o portal v2; recusados, o laudo, a cidade radial v2 e a trilha até o cume. Achados: os
  plugins da conta claude.ai carregam como `<nome>@synced`; a `/prototype` pessoal (fluxo Matt Pocock) venceria a do
  Emil, que vira `emil-prototype`. **Fase 2:** papel "Tech lead do hub" criado; recruta "Tech lead" (Opus 5.5, esforço
  médio) em `C:\Projetos\equipe-design\tech-lead`. Lição: o Maestri abre o recruta em `.maestri\roles\<id>\`, e o
  `.claude\settings.json` tem de estar ali antes do Claude subir. Depois de religado, "Setting sources: User settings,
  Shared project settings" e nenhuma skill `design:`, `engineering:`, `productivity:` ou `superpowers:`. Tarefa 1
  enviada: o texto do hub.
- 2026-10-15 ~10h35: **texto do hub aprovado na rodada 2** (`texto-do-hub.md`; conferências em
  `texto-do-hub-conferencia-r1.md` e `-r2.md`). A rodada 1 acrescentou: a busca como porta do conteúdo, a guarda do
  acervo, o registro de uso, os princípios do desenho, o conteúdo inicial, os rótulos curtos e os sete agrupamentos.
  **Subir a equipe, preparação:** um Sonnet copia as 23 skills de fora para `suite/skills/` (commit fixo, LICENSE,
  `ORIGEM.md` com as alterações, `COPIAS.md`); um Opus médio escreve as duas nossas, `regua-da-cidade` (com capturas
  das referências) e `medidas-da-peca` (scripts próprios, testados no mapa de metrô). Lição para os recrutas novos:
  subir o recruta só com o shell, pôr `.claude\` (settings e skills) na pasta `.maestri\roles\<id>\` e só então abrir
  o Claude.
- 2026-10-15 ~10h50: **cópias prontas** (Sonnet, ~250 mil tokens): 23 de 23 em `suite/skills/`, cada uma com
  `LICENSE` e `ORIGEM.md`; resumo em `suite/skills/COPIAS.md`. Tudo lido por inteiro, nada contradisse as fichas.
  Alterações além das decididas:
  - no `web-design-engineer`, "/React" saiu da description;
  - saíram as receitas de estilo, `design-directions.md`, `browser-acceptance.md`, os README e os arquivos de outros
    agentes;
  - as partes em React e com CDN saíram de `advanced-patterns.md`;
  - todo "pergunte ao usuário" virou "registre em `decisoes.md` e siga".

  A `emil-prototype` mantém "a escolha é do usuário" na fase 5. Na equipe, quem escolhe é a porta e, depois, o
  Gustavo na carta, o que está de acordo com o plano.
- 2026-10-15 ~11h05: **skills nossas prontas** (Opus médio, ~180 mil tokens).
  - **`regua-da-cidade`:** regras R1 a R6 com os limiares, nota de 1 a 5 em 12 dimensões, lista de consertos. Quatro
    capturas de referência: metrô, maré, Mesa de mapas, cidade radial v2. Não deu para capturar o laudo, que foi
    substituído pela versão "Super Trunfo", nem a trilha até o cume, porque a página inicial mudou; o motivo está no
    `LEIA.md`.
  - **Critério da porta, decidido pelo maestro:** passa com R1 a R6 em "passa" e nenhuma dimensão abaixo de 3.
  - **`medidas-da-peca`:** `medir.html`/`medir.js` e `rodar.ps1`, com o servidor local dentro, `links.mjs` e
    `check_contrast.py` lido e copiado.
  - **Teste no mapa de metrô (320 e 1280 px):** 48 ligações e 0 cruzamentos; 89 a 90 itens; folga mínima de 1,5 e
    6,3 px; razão entre grupos de 1,86; 37 de 365 textos falham no contraste; 454 KB. Prova numa página de controle
    achou o cruzamento, os links quebrados e o contraste, e bate com o `check_contrast.py`.
  - **Atenção para o UI engineer:** as medidas leem a marcação `data-item`, `data-grupo`, `data-ligacao` e
    `data-encontro`, que toda peça nova precisa ter.
  - **Não verificado:** larguras de 768 e 1920; se o foco por script aciona o `:focus-visible`.
- 2026-10-15 ~11h30: **equipe de pé.** Papéis novos no acervo do workspace: "UI engineer do hub", "UX revisor do hub"
  e "QA tester do hub". Recrutas "UI engineer" (Opus 5.5 médio), "UX revisor" (Opus 5.5 médio) e "QA tester"
  (Sonnet 5.5 médio), em `C:\Projetos\equipe-design\<papel>\`, subidos só com o shell; `.claude\settings.json` e as
  skills do papel copiados para `.maestri\roles\<id>\` antes do Claude. O Tech lead foi religado para carregar as
  dele. **Conferido em `/skills` de cada um:** UI engineer 14, UX revisor 8, Tech lead 3, QA tester 4 skills de
  projeto, as da suíte; nenhuma `design:*`; "Setting sources: User settings, Shared project settings". **Ajuste do
  maestro:** o `settings.json` de cada papel ganhou `skillOverrides` desligando cinco skills pessoais que disputariam
  o gatilho de design (`gsd-sketch`, `gsd-ui-phase`, `gsd-ui-review`, `prototype`, `video-generator`); conferido que
  `prototype` aparece desligada. Lição: no `maestri ask --raw` pelo Git Bash, usar `MSYS_NO_PATHCONV=1` (sem ele,
  `/status` vira caminho) e mandar a seta e o Enter da tela de confiança em envios separados.
  **Fase 3 aberta:** brief da volta 1 em `laco-system-design/conceitos/volta-1/brief.md`; o UI engineer constrói os
  três conceitos. A porta desta fase leva também as medidas do QA (números de cruzamentos e distâncias para o UX
  revisor e o Tech lead), pela tabela de `regua-da-cidade/como-julgar.md`.
- 2026-10-15 ~11h35, pedido do Gustavo no chat ("se livre dos agentes que não estão sendo usados"): **dispensados**
  o Designer Loops (ocioso desde o painel dos embeddings) e o Prumo (ocioso desde o aceite do Laços L3; o estado fica
  em `portal/revisao-estado.md`, e o papel "Revisor do portal" continua no acervo para recrutar de novo na fase 4).
  Ficam o Designer (entrega a carta da direção no portal), o Portal (servidor) e a equipe de quatro.
- 2026-10-15 ~11h51: **volta 1 construída** pelo UI engineer (26 min), em `laco-system-design/conceitos/volta-1/`:
  A, "Linhas do hub" (metrô: lê-se seguindo um trajeto por cor; a linha "buscar" termina na porta do conteúdo); B,
  "Duas cidades e a estrada" (planta de quarteirões, lê-se por lugar; o outro par é a mesma cidade do outro lado da
  rede privada); C, "A cidade em corte" (vista de lado, lê-se pela altura: portas na rua, conteúdo nos andares,
  verdade no subsolo). 23 rótulos na visão geral em cada um; decisões próprias em `decisoes.md`. A medição do autor
  (0 cruzamentos, razão 1,8) não conta para a porta. **Porta aberta:** o QA mede primeiro (`portas/volta-1/brief.md`).
- 2026-10-15 ~12h20: **porta da volta 1** (`portas/volta-1/resultado.md`). QA (`qa/volta-1/relatorio.md`): os três passam
  em cruzamentos (0), rótulos (23), folga (23,5 a 34,1 px), razão entre grupos (1,8) e contraste; o "foco sem mudança"
  dele era limite da medição por script (com Tab real o foco aparece, conferido pelo UX revisor). UX revisor
  (`ux-revisor.md`): **passa** nos três, notas mínimas de 3 em affordance e cor. Tech lead (`tech-lead.md`): **volta**
  nos três, porque as fichas não marcam "a decidir" quatro itens da seção 7 do texto do hub (como os agentes gravam, árvore
  interna, duas instâncias do MCP, carga do contrato); no C, também o papel na cidade: o conteúdo no alto contradiz a
  chave "altura = perto da verdade", e a busca desenhada oposta à porta do banco decide uma opção ainda em teste.
  **Volta 2 aberta** (`conceitos/volta-2/brief.md`): os três seguem com todos os consertos dos dois pareceres.
  Lição para `medidas-da-peca`: foco dado por script não aciona `:focus-visible`; deve sair "não verificado".
- 2026-10-15 ~12h20: **volta 2 construída** (UI engineer, 13 min), em `conceitos/volta-2/`; `consertos.md` lista 32
  consertos: 30 feitos e 2 feitos de outro jeito, com o motivo (nome do bairro em 14 px e caixa normal, não alta; no C,
  andar da disciplina mais baixo em vez de salas sem rótulo, que seriam formas soltas). `medidas-da-peca` corrigida
  (foco com regra `:focus-visible` que não muda por script sai como "não verificado"; nota em `LEIA-ME.md`; cópia do QA
  atualizada). **Porta da volta 2 aberta** (`portas/volta-2/brief.md`): o QA mede primeiro.
- 2026-10-15 ~12h55: **porta da volta 2** (`portas/volta-2/resultado.md`). QA: tudo passa nos três, rótulos em 25 (o
  limite). Tech lead: **passa** nos três (consertos de forma pequenos em B e C). UX revisor: **volta** nos três, por um
  só motivo: com Tab real o foco das três pessoas é invisível (contorno da cor do corpo); já era assim na volta 1 e
  escapou. **Volta 3 aberta** (`conceitos/volta-3/brief.md`), sem rótulo novo. Pendência na `medidas-da-peca`: comparar
  pixels antes e depois de um Tab real (sugestão do UX revisor), não feita; até lá o UX revisor confere com Tab real.
- 2026-10-15 ~13h, pedido do Gustavo no chat: **pausa** no próximo momento oportuno, até a confirmação dele (vai mudar o
  notebook de lugar). O UI engineer termina a volta 3, já em curso; a porta da volta 3 e a carta não são despachadas.
- 2026-10-15 ~13h05: o UI engineer disse que terminou a volta 3, mas em `conceitos/volta-3/` só estão as cópias de
  12h26 dos `.md`, `decisoes.md` e `index.html`, iguais aos da volta 2. Faltam os três `conceito-*.html` e o
  `consertos.md`, e os números que ele relatou são os da volta 2. **Não conferido com ele, por causa da pausa;** ao
  retomar, perguntar onde gravou antes de abrir a porta.
- 2026-10-15 ~13h15, **retomado** ("pode continuar"). Alarme falso: os três `conceito-*.html` da volta 3 estavam
  gravados desde 12h32 (o maestro olhou antes); só faltava o `consertos.md`, que o UI engineer segurava até a medida
  final. Medida dele: 25 rótulos, 0 cruzamentos, razão entre grupos de 1,69 a 2,23, foco visível com Tab real nas 30
  paradas. **Porta da volta 3 aberta** (`portas/volta-3/brief.md`), só sobre os consertos da volta 2.
- 2026-10-15 ~13h45: **porta da volta 3: os três passam** (`portas/volta-3/resultado.md`). QA: tudo passa (25
  rótulos, razão de 1,69 a 2,23). UX revisor: passa nos três, com o foco visível nas 30 paradas pelo Tab real. Tech lead:
  passa nos três. **Acabamento antes da carta** (não é volta nova): consertos pequenos dos dois pareceres, feitos pelo UI
  engineer em `conceitos/final/` (cópia da volta 3), sem rótulo novo. **Carta:** o Designer monta
  `conceitos/final/carta.html` pelo brief `carta/brief-designer.md` e a cadastra no `cartas.json` com
  `pede_veredito: true`; a rodada 5 do ticket, com a escolha, é do maestro. A `medidas-da-peca` segue sem ver a regra de
  foco por script (pendência em `LEIA-ME.md`).
- 2026-10-15 ~13h20: **carta no portal.** Acabamento feito pelo UI engineer em `conceitos/final/` (consertos pequenos
  dos dois pareceres da volta 3; 25 rótulos, 0 cruzamentos, foco visível com Tab real nas 30 paradas). O Designer montou
  `conceitos/final/carta.html` ("Cidade do hub: três direções"), cadastrada no `cartas.json` como
  `direcao-visual-cidade`, com `pede_veredito: true`; capturas em `portal/conferencia/carta-direcao-cidade/`. **Rodada 5
  aberta** (`portal/rodadas/2026-10-15-laco-do-system-design-r5.md`): A, B, C, mistura ou nenhuma; recomendada a B. O
  laço para aqui e espera o Gustavo. Gasto estimado: ~2,4 milhões de 5.
- 2026-10-15 13:47, **rodada 5 respondida** (envio `2db9c105-8f6b-4589-ab00-9ee88d13eea3`): **direção = D, mistura**
  (a recomendada era B). Comentário do Gustavo, em resumo fiel:
  - **B como principal**, mas alguns componentes ficam soltos no meio da cidade; a A representa melhor **quem acessa
    ou é responsável por** cada componente.
  - O Gustavo ligado ao Obsidian está certo; a linha ir direto ao banco está errada: na prática ele **edita a vista
    Markdown**. Outro exemplo: a "disciplina do agente" aparece alheia, sem ligação ao próprio agente, nas três opções.
  - O problema é o texto padrão (nome provisório; ele sugere algo como "context-hub design description"): ele limita o
    entendimento do hub ao que o maestro e o Tech lead decidiram; qualquer agente desenha o que está escrito, não o que
    acontece na prática. O system design deve misturar o técnico e o prático.
  - **Não** é para enfiar os dois exemplos no texto: isso repetiria o problema. A pergunta é: "esta descrição consegue
    ser usada para criar qualquer tipo de diagrama? É rica e genérica o bastante?". Só assim a direção visual não sai
    enviesada.
  - A descrição e o system design devem responder, sem texto corrido no desenho, perguntas como: (1) se o Gustavo
    edita um arquivo (no Obsidian ou no disco), o que acontece; (2) se um agente novo inicia sessão; (3) se um maestro
    novo inicia sessão; (4) se o Gustavo pede a um agente ler, alterar ou remover um arquivo; (5) se o outro par
    altera um arquivo. E também "qual a relação entre X e Y", "quem é responsável por X", "X faz parte do grupo lógico
    de Y". Cerca de 100 perguntas, **não como critério**, mas como fonte para escrever a descrição genérica.
  - "Se isso for um desafio muito complexo pra você, me diz qual caminho sugere."
  **Efeito:** o laço não segue para a amostra. Antes da mistura, a descrição do hub é refeita. O caminho proposto vai
  na rodada 6.
- 2026-10-15 ~14h: carta `direcao-visual-cidade` atualizada (decisão gravada, sem `pede_veredito`). **Rodada 6 aberta**
  (`portal/rodadas/2026-10-15-laco-do-system-design-r6.md`), com a proposta em `laco-system-design/descricao/proposta.md`:
  a descrição do hub como modelo de sete eixos (atores, componentes, responsabilidade, pertencimento, ações práticas,
  cenários, estado de cada afirmação), banco de umas 150 perguntas por vários modelos do FreeLLMAPI com metade escondida
  do autor, teste de respostas por modelos que só leem a descrição, teste de três diagramas; depois a mistura.
  Recomendada A.
- 2026-10-15 13:57, **rodada 6 respondida** (envio `3d827fb8-dafe-44ed-b2b2-f1653dd9ea3f`): **caminho = A**, o laço
  inteiro (a recomendada). Comentário do Gustavo: nem tudo vai ao FreeLLMAPI; parte vai a subagentes **Haiku 5.5 em
  esforço alto**, com tokens ilimitados, até **2 h**, no máximo **20 subagentes por lote**, e o número de lotes o
  maestro decide. **FreeLLMAPI:** 20 workers, até 40 mil tentativas, parando em ondas (duas seguidas com 15% ou menos
  de novos, igual à última) e em 2 h. **Sem painel:** tudo roda em segundo plano. Em "algo mais": seguir com o resto
  do hub enquanto isso roda, gerando a próxima rodada de cada ticket em andamento sem bloqueante, e dizer quais têm
  bloqueante.
- 2026-10-15 ~14h45, **laço da descrição em curso** (`laco-system-design/descricao/plano.md`):
  - etapa 1b: 12 Haiku 5.5 alto, um por lente, 471 perguntas (`perguntas/haiku/`);
  - etapa 1a: gerador pelo FreeLLMAPI montado por um subagente Opus médio (`perguntas/gateway/corrida.py`, 21 modelos
    explícitos, orçamento de 1.500 a 2.950 tentativas, repetidas por Jaccard ponderado 0,50 com as mesmas peças), em
    segundo plano desde ~14h14, fim em `perguntas/gateway/fim.txt`;
  - etapa 2, adiantada para os Haiku: `perguntas/dividir.py` (repetidas por Jaccard 0,6; sorteio por tipo, semente fixa):
    468 únicas, 237 visíveis e 236 escondidas, com as cinco do Gustavo nas escondidas. As do gateway entram depois; a
    parecida com uma visível vai às visíveis, para não vazar no teste;
  - etapa 3: Tech lead escreve `descricao-do-hub.md` nos sete eixos pelo `descricao/brief-tech-lead.md`, sem ver as
    escondidas nem este ticket.
- 2026-10-15 ~15h20: **descrição v1 escrita** pelo Tech lead (`descricao/descricao-do-hub.md`, 767 linhas, sete eixos,
  17 cenários, estado de cada afirmação). **Rodada 7 aberta** (`portal/rodadas/2026-10-15-laco-do-system-design-r7.md`):
  as 14 perguntas sobre a prática do Gustavo (`descricao/perguntas-ao-gustavo.md`). **Teste, lote 2** (10 Haiku que só
  leram a descrição, 236 escondidas): 134 responde, 84 parcial, 18 não diz, pela conta de quem respondeu. Lote 3 (10
  juízes Haiku com as fontes) e lote 4 (três diagramas: sequência, matriz de responsabilidade, mapa de grupos) em curso.
- 2026-10-15 ~15h45: **teste da descrição v1** (`descricao/teste/resumo-volta-1.md`): das 236 escondidas, 134 certas, 49
  parciais, 22 "não diz", 2 erradas, 29 que nem as fontes respondem. Sobre as 207 respondíveis, **65% certas**. Buracos
  por eixo: cenários 20, componentes 16, responsabilidade 10, ações 8, ligações 7, pertencimento 6. Três diagramas só da
  descrição (`teste/diagramas/`): faltou 21, inventou 28, ambíguo 19; a matriz de responsabilidade foi a mais fraca.
  **Volta 2** com o Tech lead (`descricao/brief-tech-lead-v2.md`): consertos por eixo, não por pergunta. O teste da v2 usa
  a metade escondida das perguntas novas do gateway (3.327 únicas por enquanto, ainda rodando), que ninguém viu.
- 2026-10-15 14:50, **rodada 7 respondida** (envio `3dc9cc9e-0c18-4276-835f-8b59f8c1ba8a`), as 14 perguntas da prática;
  transcrição em `descricao/respostas-do-gustavo-v1.md`. Em resumo: as máquinas ficam ligadas juntas; a porta principal é
  a sessão na raiz, mas uma sessão fora do hub, como cliente, deve funcionar igual (MCP da busca e as regras de gravação);
  nota nova no Obsidian nasce sempre em `inbox/` e agentes a põem no lugar; **"remover" = mover para `_archive/` por 30
  dias, depois remover; agente só remove com permissão dele ou depois dos 30 dias**; edição concorrente com agente não
  acontece, e se acontecer aceita a colisão; nenhuma iniciativa de cliente é vetada no repositório privado do GitHub;
  binários: "tínhamos tratado esse caso, você esqueceu" (é a rodada 71 de "Revisão do sync", a vigia avisa e recupera);
  cliente sem cópia = ele ou agentes dele numa sandbox, ou máquina de passagem, frequência indefinida; notificação do
  Windows basta; um agente por iniciativa, às vezes um agente em várias, sem proteção por ora; operação majoritariamente
  por agente com ele vendo; gemini só como opção, nunca obrigatório; Claude Desktop também altera notas e arquivos; celular
  não; "web" é um cliente pela tailnet, já em curso. As respostas entram na descrição v3.
- 2026-10-15 ~15h, **pausa pedida pelo Gustavo** ("na próxima oportunidade"). Erro do maestro: em vez de esperar o fim
  natural, forçou a parada: interrompeu o respondedor da fatia 01 do teste da v2, parou o gerador do gateway com o
  arquivo `PARAR` (fim limpo: 4 ondas, 5.264 únicas, 756 tentativas, `perguntas/gateway/fim.txt`), derrubou o portal e
  dois servidores de sobra (8765 e o 8779 do Designer). O portal voltou ao ar no 8770. Arquivos globais conferidos por
  hash: intactos. Lição na memória do maestro (`pausa-no-proximo-ponto`).
  **Onde parou:** descrição v2 (`descricao/descricao-do-hub.md`, 969 linhas; `consertos-v2.md`); teste da v2 em
  `descricao/teste/v2/` com 9 de 10 fatias respondidas (falta refazer a 01) e os juízes ainda não despachados; respostas
  da prática em `descricao/respostas-do-gustavo-v1.md` e as perguntas 15 e 16 do Tech lead, a incorporar na v3.
- 2026-10-15 ~15h25, **retomado** (o Gustavo mandou retomar). Respondedor da fatia 01 da v2 refeito (Haiku): 9 responde,
  16 parcial, 0 não diz. Os 10 juízes da v2 (Haiku, `teste/v2/brief-juiz.md`) despachados; saída em
  `teste/v2/julgamento/`. Depois: somar o placar e comparar com os 65% da v1.
- 2026-10-15 ~15h45, **teste da v2** (`descricao/teste/resumo-volta-2.md`): 241 escondidas; das 200 respondíveis, 130
  certas (**65%, igual à v1**), 63 parciais, 7 não diz, 0 erradas, 41 que nem as fontes respondem. O "não diz" caiu (22 → 7)
  e as parciais subiram (49 → 63). Buracos por eixo: cenários 29, componentes 11, pertencimento 10, ações 6. **Rodada 8
  aberta** (`portal/rodadas/2026-10-15-laco-do-system-design-r8.md`) com as perguntas 15 e 16. **Volta 3** com o Tech lead
  (`descricao/brief-tech-lead-v3.md`): consertos das parciais por eixo + respostas da rodada 7. Para o teste da v3, sortear
  outra amostra de escondidas ainda não usadas.
- 2026-10-15 ~15h45, **descrição v3 entregue** pelo Tech lead (`descricao/descricao-do-hub.md`, 1.173 linhas; v2 em
  `descricao-do-hub-v2.md`; `consertos-v3.md`): seção 8.0 com 17 regras gerais de comportamento, 8.18 com falhas por
  componente, cenários levados até o fim, respostas da rodada 7 com a marca [R7]. Perguntas novas: 17 (cliente nos modelos
  na nuvem) entrou na rodada 8, que estava aberta; a 18 (cliente grava?) já estava respondida pela rodada 1 do ticket 11
  (gravação ligável) e foi passada ao Tech lead, que a tirou da lista.
  **Teste da v3** em `descricao/teste/v3/`: 240 escondidas novas (20 por tipo, semente 20261016, nenhuma usada na v1 nem na
  v2; restam 1.413 livres), 10 respondedores + 10 juízes Haiku (o brief do juiz agora inclui `respostas-do-gustavo-v1.md`
  e a rodada 1 do ticket 11 como fontes) e três diagramas Haiku em `teste/v3/diagramas/` (o enunciado de cada diagrama
  foi reescrito pelo maestro; o modelo da v1 não ficou anotado).
- 2026-10-15 ~16h10, **teste da v3** (`descricao/teste/resumo-volta-3.md`): das 193 respondíveis, 129 certas (**67%**; v2 65%,
  v1 65%), 56 parciais, 7 não diz, 1 errada. Diagramas (`teste/v3/diagramas/`): sequência F5 I6 A2; matriz F14 I4 A8 (v1
  9/12/11); mapa de grupos F8 I13 A10. **Laço da descrição fechado pelo critério do plano** (etapa 7: 3 voltas; erro e "não
  diz" baixos). Antes da mistura, acabamento curto sem nova volta de teste: **v3.1** com o Tech lead
  (`descricao/brief-tech-lead-v3-1.md`: seção 4 completa, inventei/ambíguo dos diagramas, "Lacunas de dono" para levar
  ao Gustavo). Depois, etapa 8: o conceito da mistura com o UI engineer e a porta.
- 2026-10-15 ~16h30, **v3.1 entregue** pelo Tech lead (`consertos-v3-1.md`): matriz completa com 4.7 (portas), tabela de
  grupo de cada componente, ligações entre grupos, sequência fechada, **seção 13 com 13 lacunas de dono**. **Mistura
  despachada** ao UI engineer (`conceitos/mistura/brief.md`). Triagem das lacunas, para não levar 13 perguntas de uma vez
  ao Gustavo (uma decisão por vez; a mistura as mostra com o selo "a decidir"):
  - já têm dono em rodada ou ticket aberto: 3 (porta do banco fora → ticket 11, depois da r2), 6 (restauração → rodada 8,
    pergunta 16), 11 (como o cliente acha o par → ticket 14, r7 "endereço dos clientes");
  - "quem percebe a falha" de componente: 1 (vigia parada), 2 (hook que falha calado), 8 (cópia diária falha), 13 (empresa
    bloqueia o Tailscale): uma decisão só, a levar ao Gustavo depois das rodadas abertas (base: rodada 7, "notificação do
    Windows basta");
  - mecanismo de manutenção, para a construção (ticket 16): 4 (30 dias do `_archive/`), 5 (cabeça do contrato no MCP),
    7 (registro do aval), 9 (modelo do verificador), 10 (erro de peça citada que sumiu);
  - prática já respondida: 12 (dono do computador do cliente = o Gustavo ou agentes dele, rodada 7, pergunta 8).
- 2026-10-15 16:04, **rodada 8 respondida** (envio `077a19df-18a2-4747-822d-e8d35f07a483`; transcrição em
  `descricao/respostas-do-gustavo-v2.md`):
  - **15, busca:** o Gustavo também busca no hub, pelo Obsidian ou pedindo a um agente; **o Claude Desktop também usa a
    busca do hub** (ganha a ponte do Desktop até a busca). Como o Obsidian chega à busca do hub: não verificado;
  - **16, recuperação:** um agente com ele vendo, ou ele por comando pelo GitHub; **dois dias de distância na cópia
    bastam** (a cópia diária cobre). Fecha a lacuna de dono 6;
  - **17, cliente nos modelos na nuvem:** aceito; nenhuma iniciativa de cliente vetada.
  Passadas ao Tech lead (v3.2 pronta: [R8] em 4.1, 4.5, 8.7, 8.9, 8.15, 10, 11 e 13) e ao UI engineer (a mistura).
- 2026-10-15 ~17h, **mistura entregue** pelo UI engineer (`conceitos/mistura/mistura.html`, `mistura.md`, `decisoes.md`): 25
  rótulos, 20 ligações, 0 cruzamentos, folga 24 px, razão 1,53, Tab 19 de 19, sem rolagem a 320; respostas [R8] incluídas.
  **Porta, volta 1** (`portas/mistura-1/brief.md`, com o contexto inteiro, porque o Tech lead recebeu /clear): o QA mede
  (`qa/mistura-1/`); depois o UX revisor e o Tech lead julgam (o Tech lead contra a descrição v3.2).
- 2026-10-15 ~17h30, **porta da mistura, volta 1** (`portas/mistura-1/resultado.md`): QA tudo passa; UX revisor passa no
  limite (10 consertos); **Tech lead reprova R5** (hook "gravando" a nota, bairro sem linha, vigia lida como agindo no
  banco; 11 consertos). **Volta 2** com o UI engineer (`conceitos/mistura/brief-volta-2.md`).
- 2026-10-15 ~18h, **mistura volta 2** entregue (25 rótulos, 0 cruzamentos, folga 24,1 px, razão 1,68, Tab 19/19;
  `consertos.md`, `decisoes.md` 14 a 21, `mistura-v1.html`). **Porta volta 2** (`portas/mistura-2/brief.md`): QA primeiro.
- 2026-10-15 ~18h30, **porta da mistura, volta 2 = passa** (`portas/mistura-2/resultado.md`): UX revisor passa (densidade e
  affordance 3), Tech lead passa (R4, R5, R6). Acabamento antes da carta com o UI engineer
  (`conceitos/mistura/brief-acabamento.md`); depois a carta do Designer com `pede_veredito`.
- 2026-10-15 ~18h40: carta da mistura pedida ao Designer (`laco-system-design/carta/brief-designer-mistura.md`; id
  `mistura-da-cidade`, com `pede_veredito`), em paralelo ao acabamento do UI engineer.
- 2026-10-15 ~19h, **acabamento da mistura feito** (`consertos.md`, seção Acabamento): 25 rótulos, 0 cruzamentos, folga
  24,3 px, razão 1,66, Tab 19/19, 41 passos dos 7 cenários com número, `aria-pressed` volta a false. Designer avisado.
- 2026-10-15 ~19h20, **carta da mistura no portal** (`conceitos/mistura/carta.html`, id `mistura-da-cidade`, `pede_veredito`):
  a mistura utilizável dentro da carta (cenários funcionando no leitor; capturas em `portal/conferencia/carta-mistura/`).
  Espera Aprovar ou Recusar do Gustavo. Aprovada: fase 4, a amostra (`orquestracao.md`, 11 a 13).
- 2026-10-15 17:17, **carta da mistura aprovada** (envio `8c6e7d3e-4348-43ab-822d-a64f85b4c718`), sem alteração para a
  amostra. Comentário do Gustavo, em resumo fiel: "absolutamente perfeito"; a forma de mostrar cada cenário acertou; e
  **o teto de 25 rótulos sai**: podem existir mais, desde que sigam sem poluição, com a folga e o espaço devidos a cada
  rótulo. Carta atualizada (decisão gravada, sem `pede_veredito`). **Fase 4 começa:** a amostra com o UI engineer
  (`conceitos/mistura/` → `amostra/`).
- 2026-10-15 ~19h40: revisor de código da fase 4 = o Prumo; o Gustavo o cria de novo quando a amostra chegar à revisão.
- 2026-10-15 ~18h20, **amostra entregue** pelo UI engineer (`amostra/amostra.html`): canvas de tela inteira sem rolagem; 27
  rótulos na vista inicial e 40 nomes a mais ao aproximar; 0 cruzamentos, folga 22,3 px, razão 1,53, Tab 23/23, 39 passos
  dos 7 cenários. **Porta da amostra, volta 1** (`portas/amostra-1/brief.md`): QA primeiro; depois UX revisor, Tech lead e
  Prumo (o Gustavo o recria).
- 2026-10-15 ~18h30: QA da amostra pronto (`qa/amostra-1/relatorio.md`, contraste e cenários passam); UX revisor e Tech lead despachados; Prumo sendo recriado pelo Gustavo. UI engineer recebeu /clear a pedido do Gustavo.
- 2026-10-15 ~18h45, **porta da amostra, volta 1 = volta** (`portas/amostra-1/resultado.md`): Tech lead passa; UX revisor
  volta (affordance 2: salto no arrasto, zoom fora do centro, seleção de texto; cabeçalho a 960 px); Prumo volta (3
  bloqueios de toque, pinça e "Ver tudo"). **Volta 2** com o UI engineer (`amostra/brief-volta-2.md`, depois do /clear, a
  partir de `amostra/retomada-ui-engineer.md`).
- 2026-10-15 ~19h20, **amostra volta 2 entregue** (`amostra/consertos.md`, decisões 13-19). **Porta volta 2** (`portas/amostra-2/brief.md`): QA com entrada real primeiro.
- 2026-10-15 ~19h40, **porta da amostra, volta 2 = volta** (`portas/amostra-2/resultado.md`): UX revisor e Tech lead passam; Prumo volta pelo arrasto de um dedo. **Volta 3, a última** (`amostra/brief-volta-3.md`).
- 2026-10-15 ~20h, **amostra volta 3 entregue** (`consertos.md` Volta 3, decisões 20-22). **Porta volta 3** (`portas/amostra-3/brief.md`): QA com entrada real primeiro.
- 2026-10-15 ~20h20, **porta da amostra, volta 3 = passa** (`portas/amostra-3/resultado.md`): QA, UX revisor (affordance 4), Tech lead e Prumo aprovam. Carta da amostra pedida ao Designer (`carta/brief-designer-amostra.md`, id `amostra-da-cidade`, `pede_veredito`).
- 2026-10-15 ~20h40, **carta da amostra no portal** (`amostra/carta.html`, id `amostra-da-cidade`, `pede_veredito`), conferida com mouse real no leitor (arrasto, Ctrl + roda 75% a 178%, Shift + roda, ficha); no leitor a 1280 x 800 abre a 75% centrada no Banco local, e "Ver tudo" mostra a cidade inteira. Toque real não testado.
