# Categorias da suíte de design (versão 1)

Base: as 8 fichas de `suite/fichas/`, lidas inteiras, mais `skills-do-video.md` e `orquestracao.md`. Conferi na fonte, com `curl` (só leitura), o SKILL.md de `parallel-concepts`, `concept-selection`, `information-architecture` (Owl-Listener), o de `web-design-engineer` (checkpoints e React) e o frontmatter de 10 skills do Emil (flag de invocação). Nada foi clonado, instalado nem rodado.

Convenções: "(inferência)" marca o que é palpite meu, sem conferência na fonte. `manual` quer dizer `disable-model-invocation: true` no frontmatter: a skill não dispara sozinha.

Três fatos que mexem em tudo:

1. **Várias skills são manuais.** Do Emil: `prototype`, `review-animations`, `pick-ui-library`. Do Jakub: `interface-review`, `variant`, `break`, `state-machine`, `explain-interface`. O plano é invocação autônoma, então essas não disparam. Ou se tira a flag da cópia, ou o briefing manda chamar pelo nome (se isso funciona entre agentes, não sei: ponto em aberto).
2. **Instalar por plugin ou por `npx skills add` traz tudo.** Para ter só as escolhidas, copiar as pastas `skills/<nome>/` para `.claude/skills/` de cada papel. Os comandos das fichas (`/visual-critique:critique-screen` etc.) não são skills e não disparam sozinhos.
3. **O ambiente do maestro já tem skills `design:*`** (`design:design-critique`, `design:accessibility-review`, `design:ux-copy`, `design:design-system`). Se os recrutas herdarem plugins do usuário, essas disparam junto das da suíte. Conferir (ponto em aberto).

---

## Julgar uma tela já pronta, olhando a captura

- **o que resolve:** diz o que está errado numa tela que já existe e devolve lista de consertos. É o trabalho de quem mede contra a régua.
- **skills:**
  - Owl-Listener/critique-visual-hierarchy: ponto de entrada, fluxo do olho, peso, ênfase única
  - Owl-Listener/critique-composition: equilíbrio, espaço em branco, ritmo, agrupamento gestáltico
  - Owl-Listener/critique-information-density: carga cognitiva, prioridade, varredura, revelação progressiva
  - Owl-Listener/critique-affordance: o que parece clicável, estados, CTA, ações descobríveis
  - Owl-Listener/critique-color: contraste, coerência da paleta, cor com significado (contraste estimado)
  - Owl-Listener/critique-typography: escala, legibilidade, consistência, tokens
  - Owl-Listener/critique-brand-consistency: compara tela com mood.md, voice.md, tokens.md do projeto
  - Owl-Listener/critique-screen (comando): roda as sete críticas, lista P1/P2/P3
  - Owl-Listener/critique-ux (comando): hierarquia, affordance e densidade, lista priorizada
  - Owl-Listener/heuristic-evaluation: revisão de especialista contra heurísticas de Nielsen
  - Owl-Listener/design-critique (design-ops): conduz crítica estruturada com a equipe na sala
  - Owl-Listener/design-review-process: define portões e fluxo de aprovação de revisão
  - jakubkrehel/better-interface: revisão cruzada de código por seis disciplinas, `path:line`
  - jakubkrehel/interface-review (manual): revisa um diff ou PR; precisa de git e `gh`
  - ConardLi/web-design-engineer, `critique-guide`: crítica de 5 dimensões, nota 0 a 10
  - codeswithroh/tastemaker, modo `audit`: critica UI existente; faz parte da skill grande
- **sobreposições:** os sete `critique-*` do Owl se complementam e já se citam para desempatar. `better-interface` e `interface-review` fazem revisão parecida, mas sobre código (`path:line`) e não sobre captura. `heuristic-evaluation` e `design-critique` repetem o gatilho "revisar um design". O `critique-guide` do web-design-engineer e o `audit` do tastemaker são a mesma ideia dentro de skills maiores.
- **fica:** os seis `critique-*` do Owl, menos brand-consistency (a lista abaixo). São a única família feita para **captura renderizada**, que é como o UX revisor trabalha. Cada uma tem gatilho estreito ("attention lands in the wrong place", "feels off but hierarchy is fine", "feels overwhelming"). `critique-visual-hierarchy`, `-composition` e `-information-density` cobrem direto "vista de cima", "distância entre os itens" e "poluição visual". `critique-color` e `critique-typography` cobrem o resto da régua visual. `critique-affordance` fica para as telas do portal e para qualquer peça clicável da cidade.
- **sai:**
  - `critique-brand-consistency`: precisa de mood.md, voice.md e tokens.md, que o hub não tem (inferência); sem eles pula a dimensão.
  - Os dois comandos: não disparam sozinhos. O briefing do UX revisor pode mandar rodar as seis em ordem.
  - `better-interface` e `interface-review`: julgam código, não captura. `interface-review` é manual e exige git/`gh`. Dependem ainda das outras `better-*`.
  - `heuristic-evaluation`, `design-critique`, `design-review-process`: são processo e sessão de equipe. O processo do laço já existe no `orquestracao.md`.
  - `critique-guide` e `audit` do tastemaker: ficam dentro das skills de que fazem parte (categorias 4 e 10).
- **gatilhos em conflito:**
  - `critique-composition` ("a layout feels off but hierarchy is fine") x `critique-information-density` ("a screen feels overwhelming"): "a tela está poluída" cai nos dois. Aceitável: o Owl as separa e elas se citam. Resposta única: pedir as duas na mesma rodada.
  - Todas x `design:design-critique` ("review this design", "critique this mockup") do ambiente: briga direta. Evitar desligando o plugin `design` nos recrutas, ou aceitando que ele dispare só no Designer (maestro).
  - Todas x `web-design-engineer` ("design critique"): evitar instalando a web-design-engineer só no UI engineer e as `critique-*` só no UX revisor.
- **riscos:** nenhum script, rede ou escrita. Risco de precisão: as razões de contraste de `critique-color` são estimativas do modelo, "sem ferramenta de medição" (ficha). Risco de falsa completude: o comando aceita URL do Figma sem saber abri-la. Pedir sempre a captura. Todas leem a imagem; a qualidade depende do modelo ler bem a imagem (não verificado).
- **papéis:** UX revisor (as seis).
- **serve de régua?** sim, com limite. Cobrem hierarquia, composição, densidade, cor e tipo, que são a régua em palavras. Não medem: o modelo olha a imagem e julga. Não cobrem **linhas que se cruzam** nem **vista de cima** como escala (inferência: nenhuma das fichas fala de roteamento de linhas).

## Compor a tela pelo modo como o olho agrupa e lê

- **o que resolve:** ajuda a quem constrói a decidir distância, agrupamento, ordem de leitura e destaque. É guia de construção, não de crítica.
- **skills:**
  - Owl-Listener/law-of-proximity: o espaço sozinho agrupa; mais espaço entre grupos
  - Owl-Listener/law-of-common-region: contêiner ou fundo comum agrupa; no máximo dois níveis
  - Owl-Listener/law-of-continuity: o olho segue alinhamento e caminhos sem quebra
  - Owl-Listener/law-of-figure-ground: o que é primeiro plano e o que é fundo
  - Owl-Listener/law-of-similarity: forma e cor iguais dizem "mesma categoria", mesmo longe
  - Owl-Listener/law-of-closure: o olho completa formas; tira peso de bordas
  - Owl-Listener/visual-hierarchy: níveis de tamanho, peso e posição; teste de olho apertado
  - Owl-Listener/von-restorff-effect: o que difere dos vizinhos é lembrado; um destaque só
  - Owl-Listener/hicks-law: tempo de decisão cresce com o número de opções
  - Owl-Listener/millers-law: agrupar em pedaços de uns quatro itens
  - Owl-Listener/serial-position-effect: primeiro e último itens são lembrados; coloque o crítico nas pontas
  - Owl-Listener/aesthetic-usability: interface polida e consistente parece mais fácil de usar
  - Owl-Listener/interfaces-that-feel: lente emocional para tela correta mas fria
  - Owl-Listener/teslers-law: complexidade irredutível; decidir quem a carrega
  - Owl-Listener/jakobs-law: usuários esperam o que já conhecem; quando inovar
  - Owl-Listener/fitts-law: tamanho e distância de alvos, sobretudo toque
  - jakubkrehel/better-layout: agrupamento, alinhamento, ordem de leitura, estrutura que aguenta redimensionar
- **sobreposições:** `law-of-proximity`, `-common-region`, `-similarity`, `-closure` e `-continuity` tratam de agrupar por pistas diferentes; elas se citam entre si ("for grouping via containers use…"). `better-layout` repete agrupamento, alinhamento e ordem de leitura, e ainda testa por redimensionar. `hicks-law` e `millers-law` tratam de "itens demais". `visual-hierarchy` e `von-restorff-effect` tratam de destaque.
- **fica:** `law-of-proximity`, `-common-region`, `-continuity`, `-figure-ground`, `-similarity` e `visual-hierarchy`. Os três primeiros são "distância entre os itens", "linhas sem se cruzar" (o mais perto que existe: continuidade) e agrupamento por região (os bairros). `figure-ground` serve às camadas da cidade (mapa de fundo, linhas, rótulos). `similarity` serve "papel de cada item": cor e forma por papel. `visual-hierarchy` serve a "vista mais de cima". As cinco leis são complementares e o Owl as desempata no próprio texto.
- **sai:**
  - `law-of-closure`: serve a tirar bordas; secundária (inferência), pode entrar se a cidade ficar carregada de molduras.
  - `von-restorff-effect`, `serial-position-effect`: destaque único e ordem em lista; a cidade não tem lista nem ação dominante (inferência).
  - `hicks-law`, `millers-law`: "escolhas demais" é problema de quem escolhe; o diagrama é lido, não clicado. A densidade fica com `critique-information-density`.
  - `aesthetic-usability`, `interfaces-that-feel`, `teslers-law`, `jakobs-law`, `fitts-law`: argumento ou lente, sem regra para o diagrama. `interfaces-that-feel` é subjetiva ("a critério é subjetivo", ficha).
  - `better-layout`: duplica as leis e o `critique-composition`. A parte de testar com largura e idioma diferentes já está em `break-ui` (categoria 8).
- **gatilhos em conflito:**
  - `law-of-proximity` ("spacing alone must carry grouping") x `law-of-common-region` ("grouping must survive a tight layout") x `law-of-similarity` ("signalling relationships across distance"): três jeitos de "agrupar". O Owl os separa por pista. Aceitar que duas disparem juntas.
  - `law-of-*` x `critique-composition` (categoria 1): "agrupamento gestáltico" nos dois. Resolver por papel: leis só no UI engineer; críticas só no UX revisor.
  - `better-layout` x `law-of-proximity`: "grouping, alignment" nos dois. Por isso `better-layout` sai.
- **riscos:** nenhum (texto). Ruído de contexto: cada lei é uma `description` a mais.
- **papéis:** UI engineer.
- **serve de régua?** sim. É a fonte mais próxima de "distância entre os itens", "vista de cima" e "separação lógica", e dá vocabulário ao UX revisor se o maestro quiser citar a lei (inferência). Não mede: orienta.

## Explorar caminhos realmente diferentes e escolher um

- **o que resolve:** construir várias soluções diferentes de verdade para o mesmo problema, colocá-las lado a lado e escolher com critério. Cobre "três conceitos de cidade" e "reinventar a forma".
- **skills:**
  - Owl-Listener/parallel-concepts: soluções que diferem no que o usuário faz, não na aparência
  - Owl-Listener/concept-selection: critérios fixados antes; registra por que cada descartado perdeu
  - emilkowalski/prototype (manual): 3 a 5 variantes atrás de um seletor visual
  - jakubkrehel/variant (manual): três variantes atrás de um seletor, na página real
  - ConardLi/web-design-engineer, modo Direction Advisor: propõe 3 direções de escolas visuais
  - Owl-Listener/explore-options (comando): exploração paralela com registro de decisão
  - Owl-Listener/opportunity-framework: prioriza oportunidades por impacto e esforço
  - Owl-Listener/prototype-strategy: escolhe fidelidade e método do protótipo
  - Owl-Listener/design-sprint-plan: planeja sprint de design
- **sobreposições:** `emilkowalski/prototype` e `jakubkrehel/variant` são quase a mesma coisa (seletor, 3+ variantes, promover e apagar o resto). `parallel-concepts` e o Advisor do web-design-engineer pedem "alternativas", mas o primeiro varia o **comportamento** e o segundo varia a **escola visual**.
- **fica:**
  - `parallel-concepts`: o teste dele é "o usuário faz algo diferente?"; "dois conceitos com mesmos passos e visual diferente são um conceito só". É a régua "reinventar a forma em vez de restilizar" quase palavra por palavra. Ficou só com a ficha curta e o SKILL.md que li; o texto confirma.
  - `concept-selection`: critérios antes da comparação, limiar x troca, "nomear o que o vencedor custa", "nunca enxertar perdedores". Casa com a porta do Tech lead e do UX revisor.
  - `emilkowalski/prototype`: a mecânica do seletor (PICKER.md) e o aviso de que pode ser "um HTML único", que é o nosso caso. Fica **com a flag manual mantida** (ver gatilhos).
- **sai:**
  - `variant`: duplica o `prototype`; exige as `better-*` instaladas para os "gatilhos de escalonamento" (inferência pela ficha).
  - Advisor do web-design-engineer: sugere escolas visuais (Linear, Aesop…); isso é restilizar. Tirar a seção da cópia do UI engineer.
  - `explore-options`: é comando.
  - `opportunity-framework`, `prototype-strategy`, `design-sprint-plan`: processo de produto; o processo do laço já está definido.
- **gatilhos em conflito:**
  - `parallel-concepts` ("one direction is on the table… about to refine it by default") x `prototype` ("multiple genuinely different versions of a UI piece") x `variant`: o mesmo momento. Evitar: o `prototype` fica manual (só mecânica, chamado pelo nome); o `parallel-concepts` é o autônomo. Nunca instalar `variant` junto.
  - `parallel-concepts` x Advisor do web-design-engineer ("give me a few directions"): ver "sai".
  - `concept-selection` ("several directions are alive and one has to win") x `prototype` ("promote the one that feels right"): sem conflito de gatilho, mas o `prototype` apaga a superfície ao escolher sem perguntar (ficha). Mandar manter.
- **riscos:** `prototype` escreve arquivos de protótipo no projeto e apaga a superfície depois (Hard Rule 5). Instalar com a regra trocada por "mantenha sempre as amostras" (editar o texto). Sem rede nem script. `parallel-concepts` e `concept-selection` são só texto.
- **papéis:** UI engineer (`parallel-concepts`, `prototype`); Tech lead (`concept-selection`).
- **serve de régua?** sim, em parte. `parallel-concepts` mede se os conceitos são de fato diferentes (a régua "reinventar"); `concept-selection` obriga a escrever o critério antes. Não mede gosto visual.

## Construir uma página inteira com padrão de qualidade

- **o que resolve:** processo completo de fazer a página: entender o pedido, reunir contexto, construir, conferir e criticar.
- **skills:**
  - ConardLi/web-design-engineer: HTML/CSS/JS/React com crítica, receitas de estilo, anti-clichê
  - codeswithroh/tastemaker: UI ancorada em referência real; paleta, assets e movimento; verifica por scripts
  - codeswithroh/ideagram: ilustração de marca a partir de uma biblioteca unDraw local
  - jakubkrehel/build-design: constrói a UI a partir de Figma ou imagem usando tokens do projeto
  - jakubkrehel/technical-drawing: desenho técnico estático de objeto físico, com visualizador e export
  - MengTo/design-first-ui-prompting: modelo de prompt para gerar UI com restrições
- **sobreposições:** web-design-engineer e tastemaker são concorrentes diretas ("construa/estilize/melhore uma UI"). `build-design` só entra com Figma ou imagem.
- **fica:** `web-design-engineer`, só no UI engineer. É a única que declara o meio que usamos (HTML/CSS/JS, `<title>`, "single file + Tweaks"), traz `failure-patterns`, `redesign-protocol` (classificar como extensão, preservar ou overhaul), `critique-guide` e `browser-acceptance`. Sem script, sem `npx`. Pesos da escolha: é a única fonte de processo que cobre página, painel e visualização.
- **sai:**
  - `tastemaker`: ver riscos; descrição larga demais; passos de rede e memória fora do projeto. Os scripts de leitura (`check_contrast.py`, `anti_slop_scan.py`) viram ferramentas do QA, copiados sem a skill.
  - `ideagram`: ilustração unDraw, o hub não precisa; manda baixar biblioteca à mão.
  - `build-design`: não há Figma nem imagem de design neste laço (inferência).
  - `technical-drawing`: serve a objetos físicos; não à arquitetura do hub (inferência). Pode ser lida como exemplo de visualizador SVG com zoom, ponto em aberto.
  - `design-first-ui-prompting`: prompt para gerador de imagem de UI; ARTICLE.md datado.
- **gatilhos em conflito:**
  - `web-design-engineer` ("Build or redesign polished browser-rendered visual artifacts… design critique") x `tastemaker` ("use whenever the user asks to build, design, style, or improve a UI… trigger even if the user doesn't say design") x `landing-page-design` ("ANY landing page, marketing site, web UI, page section, component, or prototype"): três disparam em qualquer tarefa de UI. Escolher uma: `web-design-engineer`. As outras duas não entram.
  - `web-design-engineer` x `design:*` do ambiente: ver fato 3.
  - Dentro do próprio `web-design-engineer`: três **checkpoints que mandam esperar o usuário** ("actually wait", linhas 148 a 166 do SKILL.md). Num time de agentes isso trava. Solução: o briefing diz que quem responde ao checkpoint é o maestro ou o Designer, ou a cópia ganha uma nota "no laço, confirme com o maestro e siga".
- **riscos:**
  - `web-design-engineer`: sem script. O passo 0 manda pesquisar na web fatos de produtos citados; carrega fontes e React/Babel por CDN. Citar o hub numa busca seria vazamento (inferência): instruir "passo 0 não se aplica ao hub". Menção a `yt-dlp` e `ffmpeg` só para assets de marca; não se aplica.
  - `tastemaker`: grava em `~/.tastemaker/` (profile, histórico de estrutura e de copy), fora do projeto; manda rodar `npx shadcn@latest add …` (código de terceiros); `recolor_svg.py` sobrescreve sem backup; marcador `tastemaker-scan-ignore-file` desliga o scanner; WebSearch/WebFetch "mandatory". Decisão: **não instalar a skill**; copiar só os scripts de leitura depois de relê-los.
  - `ideagram`: grava dentro de `~/.ideagram/undraw/`.
- **papéis:** UI engineer (`web-design-engineer`).
- **serve de régua?** não como skill de construção. O `critique-guide` dá nota por dimensão e o `failure-patterns` lista falhas de design de IA, o que ajuda o UI engineer a se autoconferir. Quem faz a régua é a categoria 1.

## Cor, letra e medidas do sistema visual

- **o que resolve:** definir e checar paleta, tipografia e espaçamento como regras, para o visual ficar consistente.
- **skills:**
  - jakubkrehel/better-colors: rampas, tokens por papel, converte formato, mede contraste de par renderizado
  - jakubkrehel/better-typography: escala, altura de linha, quebra, truncamento, números tabulares
  - Owl-Listener/spacing-system: escala de espaço a partir de uma unidade base
  - Owl-Listener/color-system: escala tonal 50 a 950, cores semânticas, contraste AA
  - Owl-Listener/dark-mode-design: traduz paleta clara para escura
  - Owl-Listener/typography-scale: escala modular com peso e altura de linha
  - Owl-Listener/readable-measure: 45 a 75 caracteres por linha
  - Owl-Listener/layout-grid: colunas, gutters, margens, pontos de quebra
  - Owl-Listener/responsive-design: layout que se adapta a telas e entradas
  - Owl-Listener/data-visualization: escolhe tipo de gráfico, codificação e cor categórica
  - Owl-Listener/icon-system: grade, traço, nome e entrega de ícones
  - jakubkrehel/better-ui: raio, sombra, alinhamento óptico, ícones e movimento, valores exatos
  - ConardLi/web-design-engineer, `style-recipes`: 25 receitas de estilo (Linear, Aesop…)
- **sobreposições:** `better-colors` x `color-system` x `dark-mode-design`; `better-typography` x `typography-scale` x `readable-measure`; `spacing-system` x `layout-grid`. As `better-*` são mais inteiras e se apoiam no sistema do projeto; as do Owl são mais finas e dão números de exemplo. `layout-grid` (768 para tablet) e `responsive-design` (640) discordam de breakpoint (ficha).
- **fica:** `better-colors` (gera e **mede**, e diz "não reporte contraste que não mediu"), `better-typography`, `spacing-system` (a regra "itens relacionados mais perto que seções distintas, nunca valor fora da escala" é "distância entre os itens" quase literal).
- **sai:**
  - `color-system`, `typography-scale`, `readable-measure`, `dark-mode-design`: repetem as `better-*` com números de exemplo; `dark-mode-design` só se o portal pedir modo escuro (inferência).
  - `layout-grid`, `responsive-design`: breakpoints contraditórios; o diagrama não é grade (inferência).
  - `data-visualization`: o diagrama não é gráfico; as cores categóricas das linhas poderiam se beneficiar (ponto em aberto).
  - `icon-system`: sem ícones próprios por ora.
  - `better-ui`: polimento de superfícies que o web-design-engineer já cobre e vale conflito de valor com o Emil (ver categoria 6). Pode entrar nas telas do portal se se quiser (inferência).
  - `style-recipes`: restilizar, contra a régua.
- **gatilhos em conflito:**
  - `better-colors` ("build and check a color system") x `color-system` ("defining or rebuilding colour from scratch"): igual. Só `better-colors`.
  - `better-colors` x `tastemaker/generate_palette`: só se o tastemaker fosse instalado; não é.
  - `better-typography` x `critique-typography` (categoria 1): construir x julgar; ficam em papéis diferentes.
- **riscos:** nenhum. As `better-*` não têm script; `better-colors` pede medição real e não traz ferramenta (por isso o QA recebe `check_contrast.py`).
- **papéis:** UI engineer (`better-colors`, `better-typography`, `spacing-system`); QA tester (`better-colors`, para medir).
- **serve de régua?** não de gosto; sim de rigor. Dão números defensáveis (contraste, escala), mas "distância entre os itens" como régua de percepção vem das leis (categoria 2).

## Acabamento e movimento

- **o que resolve:** decisões de animação, polimento e desempenho de movimento.
- **skills:**
  - emilkowalski/animate: constrói animação na ordem de sete decisões, ferramenta mais barata primeiro
  - emilkowalski/emil-design-eng: filosofia de acabamento e animação, sem passos
  - emilkowalski/review-animations (manual): revisor estrito, veredito Block ou Approve
  - emilkowalski/improve-animations: audita a base e escreve planos em `plans/`
  - emilkowalski/find-animation-opportunities: onde animar e onde não animar
  - emilkowalski/animation-vocabulary: dá nome técnico a um efeito descrito
  - emilkowalski/apple-design: gestos, springs e materiais com base em palestras da Apple
  - emilkowalski/animation-performance: acha por que a animação trava
  - emilkowalski/animate-expo: o mesmo que `animate`, para React Native
  - jakubkrehel/better-ui: raio, sombra e movimento com valores exatos
  - Owl-Listener/animation-principles: easing e encenação de uma animação
  - Owl-Listener/motion-system: tokens de duração e curva do produto
  - Owl-Listener/micro-interaction-spec: especifica uma microinteração para a engenharia
  - MengTo/gsap: padrões de GSAP e ScrollTrigger
  - MengTo/threejs: cena 3D com Three.js
  - MengTo/add-shader-cursor-trail: rastro de cursor em WebGPU
  - MengTo/build-awwwards-quality-sites: site com movimento forte e GSAP
- **sobreposições:** `emil-design-eng`, `better-ui`, `animation-principles` e `apple-design` falam de "polimento e movimento". Os valores se contradizem: `better-ui` manda `scale(0.96)` ao pressionar, `emil-design-eng` manda `scale(0.97)`. `animate`, `animation-principles` e `micro-interaction-spec` tratam de "criar uma animação".
- **fica:**
  - `animate`: ordem de decisões (animar mesmo? ferramenta mais barata: CSS, `@starting-style`, WAAPI), só `transform` e `opacity`, reduced motion. Cabe em HTML sem build.
  - `animation-performance`: diagnóstico de travada (layout, paint, composite) para o QA.
- **sai:**
  - `emil-design-eng`: a `description` é uma frase larga que casa com qualquer UI ("philosophy on UI polish, component design, animation decisions…") e a skill manda uma resposta fixa ("I'm ready to help…") sem fazer mais nada até haver pergunta. Em invocação autônoma isso atrapalha (inferência pela ficha).
  - `better-ui`: ver acima.
  - `review-animations`, `improve-animations`, `find-animation-opportunities`: o primeiro é manual; o segundo grava `plans/` e fala em worktree e subagente; o terceiro serve a uma base de código com estados sem transição, não ao diagrama.
  - `animation-vocabulary`, `apple-design`: vocabulário e gestos; a cidade pode ter zoom e arraste, mas isso não está decidido (ponto em aberto).
  - `animate-expo`: React Native.
  - `animation-principles`, `motion-system`, `micro-interaction-spec`: trazem outro vocabulário de movimento. Duplicam `animate`.
  - `gsap`, `threejs`, `add-shader-cursor-trail`, `build-awwwards-quality-sites`: a restrição é JavaScript puro, sem build. `threejs` e shader pedem `npm` (inferência de que GSAP por CDN seria permitido, mas ninguém decidiu).
- **gatilhos em conflito:**
  - `animate` ("animate something, add motion, make a component feel alive") x `emil-design-eng` x `better-ui`: sai o par que não precisa; fica só `animate`.
  - `animation-performance` ("animation is janky… choppy") x `animate`: o próprio texto de cada uma aponta a outra; aceitável em papéis diferentes.
- **riscos:** nenhum script nem rede. Os exemplos pedem a biblioteca Motion, que é dependência (usar só CSS/WAAPI). `improve-animations` grava `plans/`.
- **papéis:** UI engineer (`animate`); QA tester (`animation-performance`).
- **serve de régua?** não. Não há movimento na régua do system design (inferência: ela fala só de forma e distância). Só pesa se o diagrama animar os fluxos.

## Acessibilidade, teclado e contraste

- **o que resolve:** achar o que um leitor de tela, o teclado ou uma vista fraca não conseguem usar.
- **skills:**
  - jakubkrehel/better-accessibility: WCAG 2.2: teclado, foco, ARIA, formulários, movimento, zoom
  - Owl-Listener/accessibility-audit: audita contra WCAG, achados com severidade e correção
  - Owl-Listener/accessibility-test-plan: planeja teste com tecnologia assistiva e pessoas reais
  - Owl-Listener/critique-color (acessibilidade): contraste e daltonismo de uma tela
  - ConardLi/web-design-engineer, `browser-acceptance.md`: protocolo de aceitação no navegador em vários viewports
  - codeswithroh/tastemaker, `check_contrast.py`: contraste WCAG por par ou matriz, pura computação
  - codeswithroh/tastemaker, `anti_slop_scan.py`: varredura estática de CSS/HTML por clichês de IA (só lê)
- **sobreposições:** `better-accessibility` e `accessibility-audit` fazem o mesmo (revisar interface contra WCAG com severidade). `critique-color` e `better-colors` medem/estimam contraste.
- **fica:**
  - `better-accessibility`: duas passadas (só teclado, depois leitor de tela), critério WCAG por falha, "prefira elemento nativo a ARIA". Mais específica e mais curta que `accessibility-audit`.
  - `check_contrast.py` do tastemaker, **copiado como ferramenta**, para dar a medição que `better-colors` e `critique-color` pedem e não trazem. Antes de copiar, o maestro relê o script (a ficha diz que é cálculo puro, sem rede nem escrita; não verifiquei).
  - `browser-acceptance.md` como texto solto na pasta do QA (ver pontos em aberto).
- **sai:** `accessibility-audit` (duplica), `accessibility-test-plan` (precisa de pessoas e leitores de tela), `anti_slop_scan.py` (checa clichês de IA genéricos como travessão e gradientes; não é a régua deste projeto, inferência).
- **gatilhos em conflito:**
  - `better-accessibility` x `design:accessibility-review` ("audit accessibility", "check a11y") do ambiente: briga. Desligar o plugin `design` nos recrutas.
  - `better-accessibility` ("Reviews and fixes…") x o papel do QA, que só testa: a skill **corrige** quando pede a implementação. Instruir "só relate".
  - `better-accessibility` x `better-colors`: a primeira remete a segunda para medir contraste. Complementares.
- **riscos:** `check_contrast.py` e `anti_slop_scan.py` são Python; o `anti_slop_scan` pula arquivos com o marcador `tastemaker-scan-ignore-file`, então um agente pode burlá-lo (se fosse usado). Resto é texto.
- **papéis:** QA tester (`better-accessibility`, `check_contrast.py`).
- **serve de régua?** não. Mede acessibilidade, não percepção nem gosto. Entra no teste, não na régua.

## Quebrar a peça: dados extremos, larguras e estados

- **o que resolve:** descobrir onde a peça quebra com nome longo, zero itens, tela estreita, zoom, espelhamento e estados raros.
- **skills:**
  - emilkowalski/break-ui: dados de pior caso atrás de um toggle; relata Broken/Ugly/Fragile
  - jakubkrehel/break (manual): renderiza o componente em todo cenário possível numa página temporária
  - jakubkrehel/state-machine (manual): mostra cada estado do componente com dados falsos
  - Owl-Listener/state-machine: modela estados, eventos e transições como especificação
  - Owl-Listener/responsive-audit (comando): audita comportamento por ponto de quebra
  - Owl-Listener/design-qa-checklist: checklist para conferir se o build bate com o design
  - emilkowalski/mobile-native: correções de CSS e meta para web app no celular
  - Owl-Listener/doherty-threshold: resposta do sistema em menos de 400 ms
  - Owl-Listener/localization-design: expansão de texto, RTL, formatos de idioma
- **sobreposições:** `break-ui` e `break` (do Jakub) são a mesma ideia; `break` depende do vocabulário das outras `better-*`. Os dois `state-machine` têm **o mesmo nome e fazem coisas diferentes** (um renderiza estados, o outro especifica).
- **fica:** `break-ui`: tem catálogo próprio (~75 valores em 9 grupos), checa largura real, 320 px, zoom 200%, escuro e RTL, relata por gravidade e **para antes de corrigir**. Autônoma (sem a flag, conferido). Não depende de outras skills.
- **sai:**
  - `break` do Jakub: manual e depende das `better-*`.
  - Os dois `state-machine`: a cidade tem pouco estado; colisão de nome (se um dia entrarem, só um).
  - `responsive-audit`, `design-qa-checklist`: comando e processo; sem design de referência para conferir.
  - `mobile-native`: o portal é local e de mesa (inferência).
  - `doherty-threshold`: latência de sistema; a página é estática.
  - `localization-design`: sem tradução prevista. O mesmo teste de RTL já vem no `break-ui`.
- **gatilhos em conflito:** `break-ui` ("stress-test, break, or find edge cases") x `better-accessibility` ("zoom"): zoom aparece nas duas; o QA verá as duas rodarem. Aceitável, os resultados se somam.
- **riscos:** `break-ui` escreve fixture e toggle no projeto quando roda, "atrás de gate de dev". Combinar: o QA roda numa cópia da peça, nunca na amostra aprovada. Sem rede nem script.
- **papéis:** QA tester (`break-ui`).
- **serve de régua?** não. Testa robustez, não gosto.

## Nomes e textos da interface

- **o que resolve:** rótulos, botões, erros, estados vazios e nomes que digam o que cada coisa é.
- **skills:**
  - jakubkrehel/better-writing: voz e vocabulário únicos, inventário antes, links que descrevem o destino
  - Owl-Listener/ux-writing: microcopy, erros, estados vazios, CTAs
  - Owl-Listener/information-architecture: estrutura de conteúdo, hierarquia e rótulos; "scent" dos nomes
  - Owl-Listener/content-strategy: que conteúdo o produto precisa e quem é dono
  - Owl-Listener/conversational-ux: interfaces de voz e conversa
  - Owl-Listener/error-handling-ux: prevenção e recuperação de erros no produto todo
  - Owl-Listener/form-design: formulário de ponta a ponta
  - Owl-Listener/feedback-patterns: confirmações e avisos
  - Owl-Listener/loading-states: esperas, skeletons, spinner
- **sobreposições:** `better-writing` e `ux-writing` são o mesmo (escrever e revisar texto de interface). `information-architecture` repete "rótulos" e acrescenta pesquisa com usuários.
- **fica:** `better-writing`: pede **inventário antes**, uma voz, um vocabulário, link que descreve o destino. É o mais perto de "nomes que digam o que cada item referencia" (a régua). Serve a quem escreve (UI engineer) e a quem confere (UX revisor, Tech lead).
- **sai:**
  - `ux-writing`: duplica; só ficha curta (não li o corpo).
  - `information-architecture`: o corpo que li fala de card sort, tree test e primeiros cliques, que exigem usuários (processo). A parte "Scent" e "taxonomia" serviria à cidade (ponto em aberto).
  - `content-strategy`, `conversational-ux`, `error-handling-ux`, `form-design`, `feedback-patterns`, `loading-states`: nenhum fluxo de produto no diagrama; talvez o portal use formulário um dia (inferência).
- **gatilhos em conflito:**
  - `better-writing` x `ux-writing` ("microcopy, error messages…") x `design:ux-copy` ("write copy for", "review this error message"): três para o mesmo. Só `better-writing`; desligar o `design` nos recrutas.
  - `better-writing` x `information-architecture` ("labelling"): por isso a segunda sai.
- **riscos:** nenhum.
- **papéis:** UI engineer, UX revisor, Tech lead.
- **serve de régua?** sim, uma parte: "nomes que digam o que cada item referencia". Não mede por número; é regra de texto aplicada à leitura da captura.

## Estudar e copiar uma referência

- **o que resolve:** entender como algo foi feito, extrair tokens de uma referência ou virar uma referência em código ou prompt.
- **skills:**
  - jakubkrehel/explain-interface (manual): explica como um site ou efeito foi feito a partir de URL ou captura
  - codeswithroh/tastemaker, modo `study`: extrai o "DNA" de referência sem copiar pixels
  - jakubkrehel/build-design: constrói a UI a partir de Figma ou imagem
  - MengTo/daily-ui-inspiration-capture: captura diária de inspiração em artigo datado (Codex)
  - MengTo/build-daily-inspiration-sites: transforma captura em cinco sites originais (Codex)
  - MengTo/audit-verify-explain-grade-5: audita, verifica com evidência, explica em linguagem simples
  - Owl-Listener/competitive-analysis: compara padrões de UX entre concorrentes
- **sobreposições:** `explain-interface` e o `study` do tastemaker tratam de "como foi feito / qual a linguagem visual".
- **fica:** nenhuma por ora. A referência do Gustavo (mapa de metrô, maré) pode ser dada como imagem na pasta do UI engineer e do UX revisor (inferência).
- **sai:**
  - `explain-interface`: manual; busca página de terceiros pela rede; pede MCP de navegador ou Playwright.
  - `study` do tastemaker: só existe dentro da skill descartada.
  - `build-design`: sem Figma.
  - As duas de captura diária: Codex, `git add -f`, plugin Sites, direito autoral de capturas.
  - `audit-verify-explain-grade-5`: a `description` dispara em "review, audit, check, verify, explain a change": cairia em toda revisão e brigaria com todas as críticas.
  - `competitive-analysis`: pesquisa de mercado.
- **gatilhos em conflito:** `audit-verify-explain-grade-5` ("review, audit, check, verify…") contra as seis críticas e `break-ui`: conflito forte. Por isso fora.
- **riscos:** `explain-interface` faz `curl` em URL do usuário; as de captura criam tarefas, commits e deploy. Nenhuma instalada.
- **papéis:** nenhum.
- **serve de régua?** o `study` do tastemaker seria o mais próximo de "gosto ancorado em referência" (comentário do Gustavo), mas depende de referências reais; sem script rodado, não confirmo que meça (ver pontos em aberto).

## Páginas de venda e marketing

- **o que resolve:** fazer landing page, preço e site de marca que convertam.
- **skills:**
  - elayadesign/landing-page-design: landing completa com regras visuais rígidas (fontes, raios, fundos)
  - MengTo/landing-page: estrutura, copy e SEO de uma landing de oferta única
  - MengTo/pricing-page: página de preços de SaaS
  - MengTo/build-awwwards-quality-sites: site cinematográfico com GSAP e scroll suave
  - MengTo/add-shader-cursor-trail: rastro de cursor em WebGPU
  - Video/marketing-ui (não encontrada): criatividade primeiro, só marketing
- **sobreposições:** as três de landing disputam o mesmo pedido.
- **fica:** nenhuma.
- **sai:** todas. O trabalho é diagrama e telas internas do portal, não venda.
- **gatilhos em conflito:** `landing-page-design` diz "whenever building, editing, styling, reviewing, or writing copy for ANY landing page, marketing site, web UI, page section, component, or prototype… Always consult it". Dispara em qualquer tarefa e impõe fontes (Geist, Manrope, Poppins; proíbe Inter), fundo escuro fechado e largura de 680 px. Choca com o `web-design-engineer` e com a régua. Nunca instalar de forma autônoma.
- **riscos:** `landing-page-design` sobrescreve defaults do framework e usa tom de regra fixa. `add-shader-cursor-trail` instala o pacote `shaders` via npm.
- **papéis:** nenhum.
- **serve de régua?** não.

---

## Fora da suíte

- **Pesquisa de usuário, estratégia e operação do design (cerca de 60 skills do Owl-Listener: design-research, ux-strategy, design-ops, designer-toolkit, e a parte de testes com pessoas de prototyping-testing).** Pedem entrevistas, personas, métricas, sprints e apresentações. Não há usuário a pesquisar nesta frente. Os dados pessoais exigiriam cuidado (ficha). Exceção estudada: `concept-selection`, que fica.
- **Documentar e governar um design system (`component-spec`, `design-token`, `naming-convention`, `theming-system`, `documentation-template`, `pattern-library`, `design-system-governance`, `design-token-audit`, `tokenize`, `audit-system`, `icon-system`, `motion-system`, `handoff-spec`).** Sistema para vários times; aqui são uma cidade e algumas telas. `design-token` e `naming-convention` ainda propõem padrões de nome que se contradizem.
- **Jogos (20 skills em MengTo/game-development, além de `build-isometric-arpg` e as de Three.js).** Combate, inimigos, inventário, mapa de jogo. O Gustavo marcou como fora do uso. Atenção: `build-game-map-editor` e `author-game-levels` falam em "mapa" e "rota", mas é jogo (conferido só pela `description`).
- **Imagem, vídeo, artigo e base de conhecimento (`gpt-image-2`, `aura-asset-images`, `unsplash-asset-images`, `web-video-presentation`, `motion-showreel`, `beautiful-article`, `kb-retriever`, `ideagram`).** Geram mídia ou respondem sobre arquivos. `gpt-image-2` manda a chave para um host sem validar. `motion-showreel` roda `npm install` e baixa Chromium. O projeto já tem a skill `video-generator`.
- **Biblioteca e plataforma (`tailwindcss`, `pick-ui-library`, `ask-sonner`, `write-swift`, `animate-expo`, `mobile-native`, `gsap`, `threejs`).** Pedem build, framework ou app nativo. A restrição é HTML, CSS, SVG e JS puro, sem build.
- **Processo de inspiração e prompt (`daily-ui-inspiration-capture`, `build-daily-inspiration-sites`, `design-first-ui-prompting`, `audit-verify-explain-grade-5`).** Para Codex, Sites, ou para gerador de imagem. A última dispara em toda revisão e brigaria com as críticas.
- **Skills do vídeo que não existem com esse nome (`screen-critique`, `perception-laws`, `marketing-ui`, `ai-slop-detector`, `clone`, `functional-ui`, `gsap`, `shadcn`, `brand-voice`, `design-review`).** A ficha do conjunto do vídeo não as achou. Os análogos do Owl (`critique-*`, `law-of-*`) entraram no lugar.

## Suíte proposta por papel

A lista é de skills; entre colchetes, o que o papel recebe fora da contagem (texto ou script copiado, sem `description`).

### UI engineer (14)

1. ConardLi/web-design-engineer (sem a seção Direction Advisor; checkpoints respondidos pelo maestro)
2. Owl-Listener/parallel-concepts
3. emilkowalski/prototype (flag manual mantida; sem a regra de apagar a superfície)
4. Owl-Listener/law-of-proximity
5. Owl-Listener/law-of-common-region
6. Owl-Listener/law-of-continuity
7. Owl-Listener/law-of-figure-ground
8. Owl-Listener/law-of-similarity
9. Owl-Listener/visual-hierarchy
10. Owl-Listener/spacing-system
11. jakubkrehel/better-colors
12. jakubkrehel/better-typography
13. emilkowalski/animate
14. jakubkrehel/better-writing

Gatilhos próximos dentro do papel: as cinco leis (o Owl as desempata no texto); `parallel-concepts` x `prototype` (resolvido pela flag manual).

### UX revisor (7)

1. Owl-Listener/critique-visual-hierarchy
2. Owl-Listener/critique-composition
3. Owl-Listener/critique-information-density
4. Owl-Listener/critique-affordance
5. Owl-Listener/critique-color
6. Owl-Listener/critique-typography
7. jakubkrehel/better-writing

Gatilhos próximos: `critique-composition` x `critique-information-density` ("poluição"). Resolvido por pedir as duas.

### Tech lead (2)

1. Owl-Listener/concept-selection
2. jakubkrehel/better-writing

Nenhuma skill do conjunto confere "o papel de cada item faz sentido como cidade" ou "congruente com o hub". Isso fica no texto do hub e no julgamento do Tech lead (ponto em aberto).

### QA tester (4)

1. jakubkrehel/better-accessibility (instruir: só relatar, não corrigir)
2. jakubkrehel/better-colors (medir contraste)
3. emilkowalski/break-ui (rodar numa cópia)
4. emilkowalski/animation-performance

[Fora da contagem: `check_contrast.py` do tastemaker, copiado depois de relido; `references/browser-acceptance.md` do web-design-engineer como texto solto.]
Faltam para o QA: checagem de links e de desempenho de carga. Nenhuma ficha cobre. Ponto em aberto.

**Total de skills distintas na suíte: 24** (14 + 6 críticas do UX revisor + `concept-selection` + `better-accessibility`, `break-ui`, `animation-performance`).

## Pontos em aberto

1. **Skills manuais.** Entre as escolhidas, só `prototype` é manual. Confirmar se um recruta consegue chamar uma skill manual pelo nome por ordem do maestro. Se não, trocar por `variant` (também manual) não resolve; o jeito é tirar a flag da cópia e aceitar o conflito de gatilho com `parallel-concepts`.
2. **Plugins `design:*` do usuário.** Confirmar se os recrutas em `C:\Projetos\equipe-design\<papel>\` herdam esses plugins. Se herdam, `design:design-critique`, `design:accessibility-review` e `design:ux-copy` brigam com as críticas, `better-accessibility` e `better-writing`.
3. **Checkpoints do web-design-engineer.** Os três "esperar o usuário" travam num time. Decidir: editar a cópia ou mandar o maestro responder.
4. **Tastemaker como régua.** O Gustavo citou o tastemaker como skill que mede gosto. Pela ficha, ele **ancora em referência** e mede contraste, clichês e movimento por script, não gosto. Decidir: (a) usar só os scripts de leitura no QA, como proposto; (b) rodar o modo `study` à mão numa pasta de teste com a imagem do mapa de metrô ou da maré; (c) dar as referências elogiadas e recusadas ao UX revisor como imagens. Não rodei nada para saber se (b) funciona.
5. **A régua não está toda coberta.** Nenhuma ficha trata de **linhas que se cruzam** (roteamento) nem de **vista de cima** como escala de zoom. `law-of-continuity` e `visual-hierarchy` chegam perto. Pode pedir regra escrita à mão ou uma checagem por script no DOM/SVG (inferência).
6. **"Faz sentido como cidade".** Candidata: `information-architecture` (taxonomia, rótulos, "scent"). O corpo que li é voltado a pesquisa com usuários. Decidir se entra no Tech lead com a nota "ignore card sort e tree test".
7. **Movimento.** Ninguém decidiu se a cidade anima. Se sim: ler `animate` (RECIPES.md) e decidir se GSAP por CDN é aceito (a restrição diz "JavaScript puro"). Se o mapa tiver zoom e arraste, reavaliar `apple-design`.
8. **Corpos não lidos.** `ux-writing`, `heuristic-evaluation`, `variant` e as demais "fichas curtas" do Owl só tiveram `description` e uma linha. Todas as decisões de saída sobre elas vêm da `description` e de seus cruzamentos de texto.
9. **Medição.** Só `check_contrast.py` do tastemaker mede algo. Decidir se o QA ganha mais ferramentas (medir distância entre nós no DOM, contar cruzamentos de aresta) escritas pelo maestro (inferência).
10. **Copiar pastas, não instalar.** Plugin ou `npx skills add` instala tudo. A cópia por pasta evita as ~100 `description` a mais; mas perde atualização automática. Conferir licença MIT de cada uma ao copiar e manter o LICENSE junto.
