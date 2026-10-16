# Owl-Listener/designer-skills

- URL: https://github.com/Owl-Listener/designer-skills
- Licença: MIT (API do GitHub: MIT; arquivo LICENSE: "MIT License, Copyright (c) 2026 MC Dean").
- Estrelas: 2926 (API do GitHub, consultada em 2026-10-15).
- Última atualização: updated_at 2026-10-15T11:39:06Z; último push de código (pushed_at) 2026-09-05T15:32:50Z; branch padrão main.
- Descrição do repositório (API): "Designer Skills Collection: agentic skills, commands, and plugins for design — from research to systems, UI, interaction, and delivery."
- Tamanho desta parte: 111 skills e 34 comandos em 9 plugins (contagem pela árvore do repositório). O README diz "107 skills" num trecho e "111 skills" na tabela; a árvore confirma 111. O total das cinco coleções, segundo o README, é 273 skills e 76 comandos em 33 plugins; as outras quatro coleções vivem em outros repositórios e não foram fichadas.

## Como instalar

Claude Code (literal do README, passo 2): "In Claude Code, type this and press enter:"

```
/plugin marketplace add Owl-Listener/designer-skills
```

Depois, "Type `/plugin` and press enter, then open the **Discover** tab" e instalar pelo nome, por exemplo `/plugin install ux-strategy@designer-skills`. O README recomenda para a maioria: design-research, ux-strategy, ui-design, design-ops e designer-toolkit (este último tem o roteador /start-here).

Gemini CLI (literal do README):

```
git clone https://github.com/Owl-Listener/designer-skills /tmp/designer-skills
mkdir -p .gemini/extensions
cp -r /tmp/designer-skills/.gemini/extensions/. .gemini/extensions/
```

## Como os plugins se organizam

- Nove plugins locais, cada um numa pasta: `<plugin>/.claude-plugin/plugin.json` (manifesto), `<plugin>/skills/<nome>/SKILL.md` (uma pasta por skill, com frontmatter name e description), `<plugin>/commands/<nome>.md` (frontmatter description e argument-hint) e `<plugin>/README.md`.
- Contagem por plugin: visual-critique (7 skills, 2 comandos); ui-design (19, 5); interaction-design (22, 5); design-systems (11, 3); prototyping-testing (10, 5); design-research (14, 4); ux-strategy (12, 3); design-ops (9, 3); designer-toolkit (7, 4).
- `.claude-plugin/marketplace.json` lista os nove plugins locais (source "./<plugin>") e mais 24 plugins de outros quatro repositórios (git-subdir): ux-pgm-skills (6), design-leadership-skills (6), ai-design-skills (6) e inclusive-design-skills (6). Esses 24 não foram fichados.
- Gemini: `.gemini/extensions/<plugin>/GEMINI.md` mais `gemini-extension.json`. O GEMINI.md é gerado por `scripts/build-gemini.sh`, que concatena os SKILL.md de cada plugin (comandos ficam de fora).
- Manutenção (não é parte das skills): `scripts/` tem o lint do frontmatter, a checagem de runtimes, os geradores de README e INDEX, a checagem do marketplace (com `git ls-remote` opcional, que usa rede) e a extração de notas de release. `.github/workflows/lint.yml` roda em todo push e regenera READMEs e INDEX, falhando se houver diferença. `release.yml` roda em tag `v*` com `contents: write` e cria release com `gh release create`.
- Codex: o repositório não cita Codex (não verificado).

## Riscos gerais da coleção

Uma busca por padrões de risco (rede, instalação, exclusão, MCP, ignorar instruções, sobrescrever) em todos os SKILL.md e comandos não achou nada relevante. Não há script nas skills, nem declaração de ferramenta MCP. São textos em Markdown; o corpo das fichas curtas não foi lido inteiro. Ressalva para a frente: as skills de pesquisa (summarize-interview, empathy-map, user-persona, affinity-diagram, research-repository) leem transcrições e dados que o usuário fornece, e esse conteúdo entra no contexto do modelo. Se forem usadas com dados de cliente ou dados pessoais, vale a regra de dado de cliente da frente.

## Como foi lido

- Lidos: os 111 SKILL.md e os 34 comandos (corpo completo nas fichas completas; só frontmatter nas curtas), o README, a licença, o marketplace.json, os plugin.json de visual-critique e design-systems, os workflows lint.yml e release.yml, o build-gemini.sh e um trecho do check-marketplace.py. Os outros scripts foram vistos só pelo nome e por busca de padrões de risco.
- Não lidos: EVALS.md de behavioural-analytics e qual-quant-triangulation; INDEX.md, CHANGELOG.md e CONTRIBUTING.md; os GEMINI.md gerados; os plugin.json e README.md dos outros plugins.
- Nada foi instalado, clonado ou executado. Os comportamentos descritos são o que o texto diz; não há teste de execução.
- Fichas completas: 58 itens (cor, tipografia, layout, leis de percepção, acessibilidade, visualização de dados, crítica visual, sistemas de design e os quatro formulários de interação pedidos). Fichas curtas: 87 itens (pesquisa, estratégia e demais categorias).

---

**Plugin: visual-critique** (7 skills, 2 comandos)

## critique-affordance
- caminho: `visual-critique/skills/critique-affordance/`
- description: Critique a rendered screen's affordances — what looks clickable, state visibility, CTA clarity, and action discoverability. Use when reviewing an existing screen. For sizing and positioning targets in new work, use `fitts-law` (interaction-design).
- o que faz de verdade: Critica se os elementos interativos de uma tela parecem clicáveis, se os estados (default, hover, focus, disabled, selected) aparecem, se há um CTA principal claro e se as ações são descobríveis (sem depender de hover; ações destrutivas distinguíveis). Cada uma das quatro dimensões recebe observação, problema, correção e veredito pass, minor issue ou major issue. Tom neutro, sem ferramenta de medição.
- como trabalha: Passos: ler a tela; checar cada dimensão com perguntas fixas (Clickability Signals, State Visibility, CTA Clarity, Action Discoverability); registrar observação, problema e correção; dar o veredito; conferir padrões de falha comuns (ghost buttons invisíveis, outline removido, vários CTAs cheios, ações só em hover). Não carrega referências.
- precisa para rodar: Só texto. A skill trabalha sobre uma tela renderizada: o agente precisa receber a imagem ou a descrição da tela. O repositório não declara ferramenta para abrir Figma ou capturar tela.
- riscos: Nenhum visto. Não grava nem acessa rede.
- harness: Claude Code: skill do plugin visual-critique, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/visual-critique/GEMINI.md. Codex: não verificado.
- serve para: Revisar uma tela existente quanto a affordances e descoberta de ações. Para dimensionar alvos em trabalho novo, o repositório indica fitts-law.

## critique-brand-consistency
- caminho: `visual-critique/skills/critique-brand-consistency/`
- description: Critique a rendered screen against mood.md, voice.md, and tokens.md. Use when those brand files exist and you are checking compliance. For defining the visual language itself, use `illustration-style` (ui-design).
- o que faz de verdade: Compara uma tela com três arquivos de referência do projeto: mood.md (personalidade e estética), voice.md (tom e regras de texto) e tokens.md (valores canônicos). Checa três dimensões (Mood, Voice, Token Compliance) e lista cada valor fora do token com o equivalente correto. Se um dos arquivos não existir, a skill registra a falta e pula a dimensão, sem inventar regra de marca.
- como trabalha: Passos: localizar mood.md, voice.md e tokens.md na raiz do projeto (ou onde o designer indicar); ler os três; comparar a tela com cada um; para cada dimensão, apontar divergência e correção; dar veredito. Carrega esses três arquivos do projeto como referência.
- precisa para rodar: Os três arquivos de marca no projeto, com leitura. Sem eles a skill faz só a parte possível. Sem ferramenta de rede ou MCP.
- riscos: Lê arquivos do projeto (mood.md, voice.md, tokens.md). Não grava. Se os arquivos estiverem desatualizados, a crítica segue a versão antiga.
- harness: Claude Code: skill do plugin visual-critique, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/visual-critique/GEMINI.md. Codex: não verificado.
- serve para: Checar se uma tela obedece a uma marca já documentada em arquivos do projeto.

## critique-color
- caminho: `visual-critique/skills/critique-color/`
- description: Critique a rendered screen's colour — contrast ratios, palette coherence, and semantic meaning. Use when reviewing one screen. For a product-wide WCAG audit use `accessibility-audit` (design-systems); for building the palette use `color-system` (ui-design).
- o que faz de verdade: Critica a cor de uma tela em quatro dimensões: contraste (AA: 4,5:1 para texto e 3:1 para texto grande e componentes), coerência da paleta (valores fora de token, vibração entre cores), uso semântico (cor como único indicador de estado, status consistentes) e acessibilidade (daltonismo, modo de alto contraste do Windows). Cada falha recebe a razão de contraste exigida e um token ou par de correção.
- como trabalha: Passos: avaliar cada dimensão com perguntas fixas; registrar observação, problema e correção; dar veredito pass, minor issue ou major issue por dimensão; conferir padrões de falha comuns (link sem sublinhado abaixo de 4,5:1, erro só em vermelho, placeholder com opacidade baixa, hex fora do sistema). Não carrega referências.
- precisa para rodar: Só texto. Precisa da tela (imagem ou descrição com valores de cor). A skill não traz medidor: as razões de contraste são estimadas pelo modelo, não medidas.
- riscos: Precisão: as razões de contraste são estimativas, sem ferramenta de medição. O repositório não indica ferramenta para medir de fato (não verificado).
- harness: Claude Code: skill do plugin visual-critique, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/visual-critique/GEMINI.md. Codex: não verificado.
- serve para: Auditar a cor de uma tela específica. Para auditoria de WCAG no produto inteiro, o repositório indica accessibility-audit.

## critique-composition
- caminho: `visual-critique/skills/critique-composition/`
- description: Critique a rendered screen's composition — balance, whitespace, rhythm, and gestalt grouping. Use when a layout feels off but hierarchy is fine. For emphasis and eye flow specifically, use `critique-visual-hierarchy`.
- o que faz de verdade: Critica a composição de uma tela: equilíbrio do peso visual, uso do espaço em branco (macro e micro), ritmo (repetição e intervalos) e agrupamento gestáltico (proximidade, semelhança, figura-fundo, continuidade, fechamento). Cada dimensão recebe observação, problema, correção e veredito. Foi feita para quando o layout parece torto mesmo com a hierarquia correta.
- como trabalha: Passos: avaliar Balance, Whitespace, Rhythm e Gestalt com perguntas fixas; registrar observação, problema e correção; dar veredito; conferir padrões de falha (duas colunas de peso igual, padding inconsistente, elementos órfãos, divisores demais). Não carrega referências.
- precisa para rodar: Só texto, com a tela (imagem ou descrição).
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin visual-critique, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/visual-critique/GEMINI.md. Codex: não verificado.
- serve para: Diagnosticar um layout que parece errado quando a hierarquia já está certa. Para ênfase e fluxo do olho, o repositório indica critique-visual-hierarchy.

## critique-information-density
- caminho: `visual-critique/skills/critique-information-density/`
- description: Critique a rendered screen's density — cognitive load, content prioritisation, scanning patterns, and progressive disclosure. Use when a screen feels overwhelming. For the underlying choice-count principle, use `hicks-law` (interaction-design).
- o que faz de verdade: Critica a densidade de informação de uma tela: carga cognitiva (quantas decisões o usuário precisa segurar), prioridade de conteúdo (o que importa está visível primeiro), padrão de varredura (F ou Z, rótulos alinhados, números formatados) e divulgação progressiva (o que deveria estar escondido e o que está escondido sem motivo).
- como trabalha: Passos: avaliar cada uma das quatro dimensões com perguntas fixas; registrar observação, problema e correção; dar veredito; conferir padrões de falha (dashboard com todas as métricas, tabela de dez colunas, formulário com todos os campos de uma vez, onboarding que explica antes de agir). Não carrega referências.
- precisa para rodar: Só texto, com a tela.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin visual-critique, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/visual-critique/GEMINI.md. Codex: não verificado.
- serve para: Diagnosticar uma tela que parece sobrecarregada. O princípio por trás (número de escolhas) está em hicks-law.

## /visual-critique:critique-screen (comando)
- caminho: `visual-critique/commands/critique-screen.md`
- description: Run all seven visual critiques on a screen and output a prioritised fix list.
- o que faz de verdade: Roda as sete críticas visuais sobre uma tela (hierarquia, marca, composição, tipografia, cor, affordance e densidade) e devolve uma lista única priorizada: P1 crítico (bloqueia uso ou acessibilidade), P2 importante (degrada a experiência) e P3 polimento. Cada item traz Issue, Dimension e Fix, e fecha com um parágrafo sobre a dimensão mais forte e a mais fraca.
- como trabalha: Passos: executar critique-visual-hierarchy, critique-brand-consistency, critique-composition, critique-typography, critique-color, critique-affordance e critique-information-density, nessa ordem; reunir os achados; priorizar em P1, P2 e P3. Carrega as sete skills como referência.
- precisa para rodar: Só texto. O argument-hint aceita "screen name, Figma URL, or image", mas o repositório não declara ferramenta para abrir Figma: o que chega ao agente é o que o usuário colar (imagem ou descrição). Para a parte de marca, precisa de mood.md, voice.md e tokens.md no projeto; sem eles, essa dimensão é pulada.
- riscos: Nenhum visto. Risco de falsa completude: se só a URL do Figma chegar ao agente, a análise pode sair sem base e parecer completa (comportamento não testado).
- harness: Claude Code: comando /visual-critique:critique-screen (frontmatter description e argument-hint). Gemini CLI: não entra, porque o build só concatena SKILL.md.
- serve para: Rodada completa de crítica de uma tela, com lista de correções priorizada.

## critique-typography
- caminho: `visual-critique/skills/critique-typography/`
- description: Critique a rendered screen's typography — scale usage, readability, consistency, and token compliance. Use when reviewing type on a screen. For defining the scale itself, use `typography-scale` (ui-design).
- o que faz de verdade: Critica a tipografia de uma tela em quatro dimensões: uso da escala (só passos definidos, salto de pelo menos 1,25x entre níveis), legibilidade (corpo de 16px no desktop e 14px no mobile, altura de linha, medida de 45 a 75 caracteres, contraste), consistência (elementos equivalentes com o mesmo estilo, pesos sem variação aleatória) e conformidade com tokens (valores crus no lugar de token).
- como trabalha: Passos: avaliar Scale Usage, Readability, Consistency e Token Compliance; registrar observação, problema e correção, com o nome do token; dar veredito; conferir padrões de falha (deriva de tamanho de 1 a 2px, negrito demais, alinhamento misturado, font-size fixo). Não carrega referências.
- precisa para rodar: Só texto, com a tela. Para checar tokens, precisa também da lista de tokens do projeto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin visual-critique, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/visual-critique/GEMINI.md. Codex: não verificado.
- serve para: Auditar a tipografia de uma tela já existente. Para definir a escala em si, o repositório indica typography-scale.

## /visual-critique:critique-ux (comando)
- caminho: `visual-critique/commands/critique-ux.md`
- description: Run a focused UX critique on a screen — affordances, information density, and hierarchy — and output a prioritised fix list.
- o que faz de verdade: Versão focada da crítica: cobre só hierarquia, affordance e densidade, as três dimensões mais ligadas a bloquear a tarefa. A saída é uma lista priorizada (P1 bloqueia a tarefa ou esconde uma ação obrigatória) com Issue, Dimension e Fix, e uma frase sobre o maior risco funcional da tela.
- como trabalha: Passos: executar critique-visual-hierarchy, critique-affordance e critique-information-density; reunir e priorizar. Carrega essas três skills como referência.
- precisa para rodar: Só texto, com a tela. Vale a mesma ressalva sobre o Figma do critique-screen.
- riscos: Nenhum visto.
- harness: Claude Code: comando /visual-critique:critique-ux (frontmatter description e argument-hint). Gemini CLI: não entra, porque o build só concatena SKILL.md.
- serve para: Feedback rápido sobre uma tela, com foco em conseguir concluir a tarefa.

## critique-visual-hierarchy
- caminho: `visual-critique/skills/critique-visual-hierarchy/`
- description: Critique a rendered screen's hierarchy — entry point, eye flow, weight distribution, and emphasis. Use when attention lands in the wrong place. For establishing hierarchy in new work, use `visual-hierarchy` (ui-design).
- o que faz de verdade: Critica se a hierarquia de uma tela leva o olho para o lugar certo: ponto de entrada (um só elemento dominante, alinhado ao objetivo principal), fluxo do olho (F, Z ou ordem de leitura, sem becos sem saída), peso (diferença de pelo menos 1,5x entre níveis, negrito usado com parcimônia) e ênfase (uma única zona de destaque). Veredito por dimensão.
- como trabalha: Passos: avaliar Entry Point, Eye Flow, Weight e Emphasis com perguntas fixas; registrar observação, problema e correção; dar veredito; conferir padrões de falha (vários primários, hierarquia achatada, falso destaque, CTA enterrado). Não carrega referências.
- precisa para rodar: Só texto, com a tela.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin visual-critique, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/visual-critique/GEMINI.md. Codex: não verificado.
- serve para: Quando a atenção cai no lugar errado. Para compor hierarquia em trabalho novo, o repositório indica visual-hierarchy.

---

**Plugin: ui-design** (19 skills, 5 comandos)

## aesthetic-usability
- caminho: `ui-design/skills/aesthetic-usability/`
- description: Apply the Aesthetic-Usability Effect — polished, consistent interfaces are perceived as more usable and forgive minor friction. Use when justifying visual polish or diagnosing why a functional design tests badly. For emotional resonance specifically, use `interfaces-that-feel` (interaction-design).
- o que faz de verdade: Aplica o efeito de usabilidade estética: interfaces polidas e consistentes são percebidas como mais fáceis de usar e perdoam atritos pequenos. A skill trata consistência como sinal de qualidade (espaçamento, alinhamento, escala de tipo, peso visual) e alerta que o efeito pode mascarar problema real de usabilidade.
- como trabalha: Passos: estabelecer e fazer valer escala de espaçamento e tipo; alinhar ao grid; manter peso visual consistente em ações parecidas; desenhar estados de erro, vazio e carregamento com o mesmo cuidado; auditar inconsistência antes do lançamento. Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto. O próprio texto alerta que o efeito pode esconder problema de estrutura.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Justificar polimento visual ou diagnosticar por que um design funcional testa mal. Para efeito emocional, interfaces-that-feel.

## /ui-design:color-palette (comando)
- caminho: `ui-design/commands/color-palette.md`
- description: Run the full colour workflow — tonal scales, semantic mapping, contrast checks, dark mode, and chart colours — and output a documented palette.
- o que faz de verdade: Roda o fluxo completo de cor: escalas tonais a partir das cores de entrada, mapeamento semântico, checagem de contraste de todas as combinações, mapeamento para dark mode e cores de gráfico. A saída é uma paleta documentada com matriz de contraste e orientação de uso.
- como trabalha: Passos: base tonal e semântica, acessibilidade, dark mode, dados e documentação. Carrega color-system, dark-mode-design e data-visualization. Sugere /design-screen depois para aplicar.
- precisa para rodar: Só texto. Entrada: cores de marca ou requisitos (exemplo do argument-hint: "#3B82F6 primary blue, modern tech feel").
- riscos: Nenhum visto. A checagem de contraste é feita pelo modelo, sem ferramenta.
- harness: Claude Code: comando /ui-design:color-palette (frontmatter description e argument-hint). Gemini CLI: não entra, porque o build só concatena SKILL.md.
- serve para: Gerar uma paleta documentada completa em uma rodada.

## color-system
- caminho: `ui-design/skills/color-system/`
- description: Build a product colour system — tonal scales, semantic roles, and contrast compliance. Use when defining or rebuilding colour from scratch. For dark-mode adaptation use `dark-mode-design`; for chart palettes use `data-visualization`; for multi-brand token architecture use `theming-system` (design-systems).
- o que faz de verdade: Constrói um sistema de cor de produto em quatro camadas: paleta de marca com escala tonal (50 a 950), neutros para texto e superfícies, cores semânticas (sucesso, alerta, erro, informação, cada uma com fundo, texto, borda e ícone) e uma camada estendida (dados, ilustração, gradientes). Exige contraste AA (4,5:1 texto, 3:1 componentes) e não depende só de cor. Recomenda mapear o dark mode desde o início.
- como trabalha: Não tem passos numerados: as seções são camadas do sistema, requisitos de acessibilidade, relações de cor (tons, complementares, análogas, pares neutros) e boas práticas (testar todos os pares de contraste). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto. A skill pede testar todos os pares de contraste, mas não traz ferramenta para isso.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Definir ou refazer a cor do produto do zero. Para adaptar a escuro, dark-mode-design; para gráficos, data-visualization; para várias marcas, theming-system.

## dark-mode-design
- caminho: `ui-design/skills/dark-mode-design/`
- description: Adapt an existing palette to dark mode — surface elevation, contrast rebalancing, and desaturation rules. Use when you already have a light palette to translate. For building the base palette first, use `color-system`.
- o que faz de verdade: Adapta uma paleta clara para o modo escuro, indo além da inversão: superfícies em níveis de elevação com tons mais claros (não sombra), redução geral de luminosidade, saturação das cores primárias reduzida em 10 a 20%, texto em off-white (exemplo #E0E0E0) e bordas sutis. Também cobre imagens (escurecer, variante de ilustração) e contraste de 4,5:1 no corpo do texto.
- como trabalha: Não tem passos numerados: princípios, hierarquia de superfícies (exemplo: fundo #121212 e três níveis mais claros), ajuste de cor, mídia, acessibilidade e boas práticas. Recomenda respeitar prefers-color-scheme e ter alternância manual. Não carrega referências.
- precisa para rodar: Só texto, com a paleta clara como entrada.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Traduzir uma paleta que já existe para escuro. Para construir a base, o repositório indica color-system.

## data-visualization
- caminho: `ui-design/skills/data-visualization/`
- description: Select chart types and design data encodings — marks, axes, labels, and accessible chart styling. Use when presenting data graphically. Owns chart selection and encoding only; the categorical colour ramp itself belongs to `color-system`.
- o que faz de verdade: Escolhe o tipo de gráfico pela tarefa (comparação, tendência no tempo, parte do todo, distribuição, relação) e define o encoding: marcas, eixos, rótulos e legendas. Princípios de tinta de dados, eixo em zero em barras e anotação de insight. Cor em três tipos (sequencial, divergente, categórica) com paletas seguras para daltonismo, e acessibilidade com padrões além da cor e texto alternativo.
- como trabalha: Passos implícitos nas seções: escolher a forma pela tarefa; definir o encoding; cor; acessibilidade; versão responsiva (menos pontos, tabela no celular); boas práticas (testar com dados reais). Não carrega referências. A rampa categórica de cor fica com color-system.
- precisa para rodar: Só texto, com os dados que o gráfico vai mostrar.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Escolher o gráfico certo e definir como ele codifica os dados.

## /ui-design:design-screen (comando)
- caminho: `ui-design/commands/design-screen.md`
- description: Design a complete screen layout from a description or requirements.
- o que faz de verdade: Monta a especificação de uma tela inteira a partir de uma descrição: grid, hierarquia, tipografia, cor, espaçamento, comportamento por breakpoint e dark mode.
- como trabalha: Passos: layout-grid, visual-hierarchy, typography-scale, color-system, spacing-system, responsive-design e dark-mode-design, nessa ordem. Sugere /responsive-audit depois.
- precisa para rodar: Só texto. Entrada: descrição da tela (exemplo do argument-hint: "user profile settings page").
- riscos: Nenhum visto.
- harness: Claude Code: comando /ui-design:design-screen (frontmatter description e argument-hint). Gemini CLI: não entra, porque o build só concatena SKILL.md.
- serve para: Especificar uma tela nova do zero.

## law-of-closure
- caminho: `ui-design/skills/law-of-closure/`
- description: Apply the Law of Closure — the eye completes implied shapes from partial forms. Use when reducing visual weight by dropping borders or letting negative space suggest structure. For explicit containers, use `law-of-common-region`.
- o que faz de verdade: Aplica a Lei do Fechamento: o olho completa formas implícitas. Usa o princípio para tirar peso visual (divisor de borda única, acentos de canto, fundo que some na borda, alinhamento no lugar de grade desenhada) e para ícones minimalistas. Alerta que sem espaço negativo o fechamento não acontece, e que em email ou tabela densa o explícito é melhor.
- como trabalha: Não tem passos numerados: princípio, aplicações (ícones, contêineres implícitos, grid por alinhamento, sinal de rolagem), quando usar borda explícita e boas práticas (remover bordas uma a uma e testar; testar ícones em 16 e 20px; revalidar no dark mode). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Tirar peso visual de bordas e grades sem perder a estrutura. Para contêiner explícito, law-of-common-region.

## law-of-common-region
- caminho: `ui-design/skills/law-of-common-region/`
- description: Apply the Law of Common Region — a shared container, background, or border groups elements regardless of spacing. Use when grouping must survive a tight layout. For grouping by spacing alone, use `law-of-proximity`.
- o que faz de verdade: Aplica a Lei da Região Comum: um contêiner ou fundo compartilhado agrupa os elementos, mesmo com espaçamento irregular. Compara com proximidade (proximidade primeiro, região comum quando é preciso um limite explícito) e lista aplicações (cards, sidebar, modal, seções de formulário, linhas de tabela, tags). Pede o contêiner mais fraco que resolva e no máximo dois níveis de aninhamento.
- como trabalha: Não tem passos numerados: princípio, tabela de comparação com proximidade, aplicações, quando é contraproducente e boas práticas. Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Agrupar elementos que precisam de limite visível, como cards e painéis. Para agrupar só com espaço, law-of-proximity.

## law-of-continuity
- caminho: `ui-design/skills/law-of-continuity/`
- description: Apply the Law of Continuity — the eye follows alignment and unbroken paths. Use when sequencing steps, aligning content, or designing carousels and timelines. For grouping rather than sequencing, use `law-of-proximity`.
- o que faz de verdade: Aplica a Lei da Continuidade: o olho segue alinhamento e caminhos contínuos. Usa para ler na ordem certa (alinhamento à esquerda, eixo de coluna), para sequência (timeline, passos ligados por linha, setas, indicadores de carrossel) e para separar grupos com continuidade interrompida (espaço maior, divisor, recuo). Alerta que desalinhar por poucos pixels interrompe o caminho.
- como trabalha: Não tem passos numerados: princípio, alinhamento, indicadores direcionais, timelines, continuidade interrompida, relação com hierarquia e boas práticas (desenhar o caminho de leitura antes; auditar alinhamento em todos os breakpoints). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Sequenciar passos, alinhar conteúdo, desenhar carrossel e timeline. Para agrupar, law-of-proximity.

## law-of-figure-ground
- caminho: `ui-design/skills/law-of-figure-ground/`
- description: Apply the Law of Figure-Ground — establish which layer is foreground and actionable versus background. Use when designing modals, overlays, and depth. For emphasising one element among peers, use `von-restorff-effect`.
- o que faz de verdade: Aplica a Lei Figura-Fundo: o usuário precisa saber o que é primeiro plano (conteúdo ou ação) e o que é fundo. Ferramentas: elevação e sombra, scrim para modal, contraste e estado selecionado. Lista falhas comuns (modal sem scrim, cards dentro de cards sem diferença de luminância, texto sobre foto sem camada de separação, design sem diferença de superfície) e a inversão de luminância no dark mode.
- como trabalha: Não tem passos numerados: princípio, tabela figura versus fundo, ferramentas, figura ambígua, falhas comuns, dark mode e boas práticas (definir a pilha de superfícies em tokens; testar sem cor). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Modais, overlays e profundidade. Para destacar um item entre pares, von-restorff-effect.

## law-of-proximity
- caminho: `ui-design/skills/law-of-proximity/`
- description: Apply the Law of Proximity — spatial closeness groups elements more strongly than any other cue. Use when spacing alone must carry grouping. For grouping via containers use `law-of-common-region`; via shared appearance use `law-of-similarity`.
- o que faz de verdade: Aplica a Lei da Proximidade: o que está perto se agrupa mais que qualquer outro sinal. Usa o espaço para dizer relação, com a razão entre espaço interno e espaço entre grupos definindo a hierarquia. Exemplos: rótulo perto do campo, título perto do conteúdo, botões perto do que atuam, linha de dados com padding menor que o gap. Aconselha não usar borda para o que o espaço já resolve.
- como trabalha: Não tem passos numerados: princípio, regra da razão, aplicações em tabela, relação com outras leis e boas práticas (escala de espaço consistente, squint test, auditar onde os usuários leem a estrutura errado). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Agrupar com espaçamento, sem contêiner. Para contêiner, law-of-common-region; para aparência comum, law-of-similarity.

## law-of-similarity
- caminho: `ui-design/skills/law-of-similarity/`
- description: Apply the Law of Similarity — shared colour, shape, or size signals that elements belong to one category. Use when signalling relationships across distance. For grouping by position, use `law-of-proximity`.
- o que faz de verdade: Aplica a Lei da Semelhança: forma, cor, tamanho e estilo compartilhados dizem que elementos são da mesma categoria, mesmo longe um do outro. Usa para estado interativo (uma propriedade que só o clicável tem), para categoria e papel (cor reservada a ação destrutiva, status com cor fixa) e para coerência de sistema. Alerta que quem desvia sem motivo sinaliza uma diferença que não existe, e que cor sozinha exclui daltônicos.
- como trabalha: Não tem passos numerados: princípio, relação com proximidade (tabela de conflitos), aplicações (estado interativo, categoria, componentes, gráficos), erros comuns e boas práticas (vocabulário de semelhança em tokens, codificação redundante, testar sem cor). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Sinalizar categoria ou papel de elementos distantes. Para agrupar por posição, law-of-proximity.

## layout-grid
- caminho: `ui-design/skills/layout-grid/`
- description: Define a responsive grid — columns, gutters, margins, and breakpoint behaviour. Use when establishing page structure. For the spacing scale inside components use `spacing-system`; for cross-device behaviour use `responsive-design`.
- o que faz de verdade: Define o grid responsivo: colunas (4 no celular, 8 no tablet, 12 no desktop), gutters de 16, 24 ou 32px, margens de 16px no mobile e 24 a 48px no desktop, e breakpoints de exemplo (375, 768, 1024 e 1440px). Lista tipos de grid (coluna, modular, de linha de base, composto) e padrões de página (full-bleed, contido, assimétrico, grade de cards).
- como trabalha: Não tem passos numerados: anatomia do grid, tipos, comportamento responsivo (fluido, fixo, adaptativo, queda de colunas), padrões e boas práticas. Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Estruturar a página. Os breakpoints de exemplo (768 para tablet) não batem com os de responsive-design (640); vale fixar um só.

## readable-measure
- caminho: `ui-design/skills/readable-measure/`
- description: Set line length and measure for comfortable reading across type sizes and breakpoints. Use when tuning body text. Covers measure only — for the full size and weight scale, use `typography-scale`.
- o que faz de verdade: Define a medida (comprimento da linha) de texto corrido: 45 a 75 caracteres por linha, com 66 citado como ideal. Abaixo de 45 a leitura quebra o ritmo; acima de 75 o olho perde o início da linha seguinte. Indica usar max-width em ch (exemplo: 65ch), com uma tabela por contexto (artigo de 55 a 70, UI de 45 a 65, legenda de 40 a 60, citação de 30 a 45).
- como trabalha: Não tem passos numerados: princípio, medida na prática (ch e contagem real), comportamento responsivo, tabela por contexto e boas práticas. Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Ajustar a largura do texto de corpo. Não cobre escala de tamanho: para isso, typography-scale.

## /ui-design:responsive-audit (comando)
- caminho: `ui-design/commands/responsive-audit.md`
- description: Audit a design's responsive behaviour across breakpoints — layout, touch targets, and content reflow.
- o que faz de verdade: Audita o comportamento responsivo de um design: por breakpoint, grid, escala tipográfica, espaçamento, hierarquia, tamanho mínimo de toque (44px) e reflow de conteúdo. A saída é um relatório com achados por breakpoint e recomendações.
- como trabalha: Passos: breakpoints, grid, tipo, espaçamento, hierarquia, toque e relatório. Carrega responsive-design, layout-grid, typography-scale, spacing-system e visual-hierarchy.
- precisa para rodar: Só texto, com o design ou a descrição dos breakpoints.
- riscos: Nenhum visto.
- harness: Claude Code: comando /ui-design:responsive-audit (frontmatter description e argument-hint). Gemini CLI: não entra, porque o build só concatena SKILL.md.
- serve para: Verificar se um design aguenta vários tamanhos de tela antes do handoff.

## responsive-design
- caminho: `ui-design/skills/responsive-design/`
- description: Design layouts and interactions that adapt across screen sizes and input methods. Use when one design must serve many viewports. For the underlying column grid use `layout-grid`; for OS-specific patterns use `platform-conventions`.
- o que faz de verdade: Desenha layouts e interações que se adaptam a viewports e formas de entrada. Estratégias: fluida, adaptativa, mobile-first e content-first. Breakpoints de referência (375 a 639 telefone, 640 a 1023 tablet, 1024 a 1439 laptop, 1440 ou mais desktop). Padrões de adaptação (queda de colunas, reflow, off-canvas, priority+) e alvos de toque de 44px.
- como trabalha: Não tem passos numerados: estratégias, breakpoints, padrões, adaptação por entrada (toque, mouse, teclado, voz), tipo e imagens fluidas e boas práticas (testar em aparelho real). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Fazer um design servir vários tamanhos de tela. Para o grid em si, layout-grid; para padrões de SO, platform-conventions.

## spacing-system
- caminho: `ui-design/skills/spacing-system/`
- description: Create a spacing scale from a base unit with rules for when each step applies. Use when standardising padding and margins. For page-level columns and gutters, use `layout-grid`.
- o que faz de verdade: Cria uma escala de espaçamento a partir de uma unidade base de 4 ou 8px, com passos nomeados (de 2xs, 2px, a 3xl, 64px). Separa espaçamento por tipo (inset, stack, inline e gap de grid) e por densidade (compacta, confortável, espaçosa). Regra central: itens relacionados ficam mais perto que seções distintas, e nunca se usa valor fora da escala.
- como trabalha: Não tem passos numerados: unidade base, escala, tipos, regras de aplicação, modos de densidade e boas práticas. Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Padronizar padding e margin de um produto. Para colunas e gutters de página, o repositório indica layout-grid.

## /ui-design:type-system (comando)
- caminho: `ui-design/commands/type-system.md`
- description: Build a typography system end to end — scale, weights, line heights, measure, and responsive behaviour.
- o que faz de verdade: Monta um sistema tipográfico completo: escala modular, hierarquia, adaptação por breakpoint, espaçamento de texto, alinhamento à linha de base e guia de uso.
- como trabalha: Passos: scale, hierarchy, responsive, spacing, grid alignment e documentação. Carrega typography-scale, visual-hierarchy, responsive-design, spacing-system e layout-grid. Sugere /design-screen depois.
- precisa para rodar: Só texto. Entrada: fontes ou requisitos (exemplo: "Inter for UI, Merriweather for editorial").
- riscos: Nenhum visto.
- harness: Claude Code: comando /ui-design:type-system (frontmatter description e argument-hint). Gemini CLI: não entra, porque o build só concatena SKILL.md.
- serve para: Criar o sistema tipográfico de uma marca ou produto.

## typography-scale
- caminho: `ui-design/skills/typography-scale/`
- description: Create a modular type scale with size, weight, and line-height relationships. Use when establishing typographic structure. For line length only use `readable-measure`; for judging type on an existing screen use `critique-typography` (visual-critique).
- o que faz de verdade: Cria uma escala tipográfica modular a partir de uma razão (exemplo: 1,25 ou 1,333): caption de 12px, corpo de 16px como base, títulos de 20 a 40px, display de 48 a 64px. Define pesos (400, 500, 600, 700), alturas de linha (1,2 para títulos, 1,5 para corpo, 1,75 para leitura longa) e espaçamento entre letras. Regras: 4 a 5 tamanhos em uso regular e corpo de no mínimo 16px.
- como trabalha: Não tem passos numerados: componentes da escala (tamanho, peso, altura de linha, espaçamento entre letras), pares de fonte, adaptação responsiva e boas práticas. Não carrega referências.
- precisa para rodar: Só texto, com as fontes escolhidas.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Criar a estrutura tipográfica de um produto. Para medida de linha, readable-measure; para julgar uma tela, critique-typography.

## visual-hierarchy
- caminho: `ui-design/skills/visual-hierarchy/`
- description: Establish hierarchy through size, weight, colour, spacing, and position so the eye lands in the intended order. Use when composing new work. For judging an existing screen, use `critique-visual-hierarchy` (visual-critique).
- o que faz de verdade: Estabelece hierarquia visual em trabalho novo, com as ferramentas: tamanho (pelo menos 1,5x entre níveis), peso, cor e contraste, espaço em volta, posição (topo à esquerda em LTR, dobra, F e Z) e densidade (o isolado se destaca, o agrupado é lido como unidade). Define quatro níveis (primário, secundário, terciário, quaternário) e o squint test (com a vista borrada, a hierarquia deve continuar clara).
- como trabalha: Não tem passos numerados: ferramentas, níveis, padrões comuns (hero, card, formulário, navegação) e boas práticas (uma ação principal por tela). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Compor hierarquia de uma tela nova. Para julgar tela existente, critique-visual-hierarchy.

## von-restorff-effect
- caminho: `ui-design/skills/von-restorff-effect/`
- description: Apply the Von Restorff Effect — the element that differs from its neighbours is the one remembered. Use when a single action must dominate. For overall ordering rather than single-element emphasis, use `visual-hierarchy`.
- o que faz de verdade: Aplica o efeito de isolamento: o elemento que difere dos vizinhos é o que se lembra. Serve para uma ação dominante (um botão cheio entre fantasmas, uma linha destacada numa tabela, o preço recomendado). A skill alerta que o efeito só funciona com poucos desvios, que o destaque precisa ser significativo e que é preciso testar em escala de cinza.
- como trabalha: Não tem passos numerados: princípio, dependência do contexto, aplicações em tabela, o que evitar (inflação de isolamento) e boas práticas (decidir antes o elemento principal por tela). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin ui-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/ui-design/GEMINI.md. Codex: não verificado.
- serve para: Dar dominância a uma única ação ou item. Para a ordem geral da página, visual-hierarchy; para a posição na lista, serial-position-effect.

## illustration-style (ficha curta)
- caminho: `ui-design/skills/illustration-style/`
- description: Define an illustration style guide — visual language, colour usage, and application rules. Use when commissioning or standardising illustration. For icons, use `icon-system` (design-systems).
- serve para: Definir um guia de estilo de ilustração: linguagem visual, uso de cor e regras de aplicação. Para ícones, icon-system.

## /ui-design:platform-audit (comando, ficha curta)
- caminho: `ui-design/commands/platform-audit.md`
- description: Audit a design for iOS and Android convention compliance — navigation, controls, typography, and platform-specific gaps.
- serve para: Auditar um design quanto às convenções de iOS e Android: navegação, controles, tipografia e lacunas por plataforma.

## platform-conventions (ficha curta)
- caminho: `ui-design/skills/platform-conventions/`
- description: Design to iOS and Android conventions — what each OS mandates, where they diverge, and when to unify. Use when shipping native apps. For breakpoint adaptation use `responsive-design`; for matching competitor patterns use `jakobs-law` (interaction-design).
- serve para: Desenhar conforme as convenções de iOS e Android: o que cada SO exige, onde divergem e quando unificar.

---

**Plugin: interaction-design** (22 skills, 5 comandos)

## doherty-threshold
- caminho: `interaction-design/skills/doherty-threshold/`
- description: Apply the Doherty Threshold — keep system response under 400ms to preserve user flow. Use when diagnosing perceived slowness or setting a performance budget. For what to show during unavoidable waits, use `loading-states`.
- o que faz de verdade: Aplica o limiar de Doherty: manter a resposta do sistema abaixo de 400ms para não quebrar o fluxo do usuário (a skill atribui o achado a IBM, 1982). Traz uma tabela de percepção por faixa de tempo (até 100ms instantâneo; 400ms a 1s lento; 1s ou mais exige progresso). Quando não é possível cumprir: feedback em 100ms, indicador de carregamento entre 400ms e 3s, progresso acima de 3s, atualização otimista e skeleton no lugar de spinner.
- como trabalha: Não tem passos numerados: princípio, tabela de limiares, onde o limite importa (troca de tela, controles inline, busca, autocomplete), o que fazer quando não cumpre, o que o limiar não é (a própria skill diz que não é lei empírica estrita) e boas práticas (medir em dispositivo e rede reais). Não carrega referências.
- precisa para rodar: Só texto. Medir latência de verdade exige ferramenta fora da skill.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Diagnosticar lentidão percebida e definir orçamento de performance. Para o que mostrar durante a espera, loading-states.

## error-handling-ux
- caminho: `interaction-design/skills/error-handling-ux/`
- description: Design error prevention, detection, and recovery across a product — message content, placement, and escape routes. Use when errors span multiple flows. For validation inside a single form, use `form-design`.
- o que faz de verdade: Desenha o tratamento de erro no produto inteiro, em quatro camadas: prevenção (validação antes do envio, confirmação de ação destrutiva, salvamento automático), detecção (validação em tempo real, erro de rede, timeout, permissão), comunicação (linguagem humana, o que aconteceu, por quê e o que fazer, perto da origem) e recuperação (manter o que o usuário digitou, nova tentativa, caminhos alternativos, desfazer). Traz o formato da mensagem e o tratamento por contexto (formulário, página, rede, resultado vazio, permissão).
- como trabalha: Não tem passos numerados: hierarquia de quatro camadas, formato da mensagem, tratamento por contexto e boas práticas (nunca culpar o usuário; testar caminhos de erro tanto quanto o caminho feliz). Não carrega referências. Para validação dentro de um formulário, form-design.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Erros que atravessam vários fluxos. Erros dentro de um formulário ficam com form-design.

## fitts-law
- caminho: `interaction-design/skills/fitts-law/`
- description: Apply Fitts's Law — target acquisition time depends on size and distance. Use when sizing and positioning controls, especially for touch. For how many controls to show at once, use `hicks-law`.
- o que faz de verdade: Aplica a Lei de Fitts: o tempo para atingir um alvo depende da distância e do tamanho (a skill cita MT = a + b × log2(2D / W)). Dá tamanhos mínimos (44×44pt no Apple HIG, 48×48dp no Material para toque; 24×24px para ponteiro), diz que a área de toque é maior que o ícone (usar padding) e que bordas e cantos da tela funcionam como alvos de tamanho praticamente infinito.
- como trabalha: Não tem passos numerados: princípio, tamanho do alvo, distância (ações perto do conteúdo, confirmação sem atravessar a tela, navegação inferior no celular), o que a lei não cobre (custo cognitivo, gestos) e boas práticas (testar no aparelho). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Dimensionar e posicionar controles, sobretudo para toque. Para quantos controles mostrar, hicks-law.

## form-design
- caminho: `interaction-design/skills/form-design/`
- description: Design a form end to end — field order, grouping, validation, and completion. Use when the artifact is a form. For product-wide error strategy use `error-handling-ux`; for first-run signup use `onboarding-design`.
- o que faz de verdade: Desenha um formulário de ponta a ponta: coluna única, labels persistentes acima do campo, tipo de input pelo dado (até 5 opções em radio, 6 ou mais em select, data em campos segmentados), validação ao sair do campo e não a cada tecla, mensagem de erro abaixo do campo dizendo o que corrigir, progresso em formulários de várias etapas e acessibilidade (label for, aria-describedby, ordem de foco).
- como trabalha: Não tem passos numerados: layout, labels e instruções, tipos de input (tabela), validação, formulários em etapas, acessibilidade e boas práticas (remover campos opcionais, testar com dados reais). Não carrega referências. Para a estratégia de erro no produto inteiro, error-handling-ux.
- precisa para rodar: Só texto, com a lista de campos.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Desenhar um formulário ou revisar um existente.

## hicks-law
- caminho: `interaction-design/skills/hicks-law/`
- description: Apply Hick's Law — decision time grows with the number of simultaneous choices. Use when a screen offers too many options at once. For how many items survive in memory afterwards, use `millers-law`.
- o que faz de verdade: Aplica a Lei de Hick: o tempo de decisão cresce com o número de escolhas simultâneas (a skill cita RT = a + b × log2(n + 1) e avisa que a fórmula serve melhor a escolhas simples). Reduz escolhas por agrupamento, divulgação progressiva e defaults inteligentes, sem tirar funcionalidade. Lembra que opções claras e distintas valem mais que um número pequeno de opções vagas.
- como trabalha: Não tem passos numerados: princípio, fórmula, onde aplicar (menus, barras de ação, onboarding, formulários, tabelas de preço, resultados de busca), erros comuns e boas práticas (agrupar antes de cortar). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Tela ou menu com opções demais de uma vez. Para quantos itens ficam na memória depois, millers-law.

## interfaces-that-feel
- caminho: `interaction-design/skills/interfaces-that-feel/`
- description: Apply an emotional resonance lens to a UI that is technically correct but flat, prescribing changes at the copy, motion, and interaction layer. Use when a design tests fine but lands cold. For the polish-perception argument, use `aesthetic-usability` (ui-design).
- o que faz de verdade: Lente de ressonância emocional para interfaces que estão corretas, mas frias. A skill traduz a intenção em sensação em quatro passos: nomear o estado em que a pessoa está, achar a analogia física, extrair a propriedade de comportamento (peso, resistência, ritmo) e aplicar na camada certa (easing, copy, cor, espaçamento). Traz tom de voz por estado (carregamento, vazio, erro, sucesso, onboarding) e faixas de tempo de movimento.
- como trabalha: Não tem passos numerados: quatro passos de tradução, timing emocional (dar de 300 a 600ms de respiro após erro), voz por estado, movimento como sinal emocional (150 a 300ms para resposta, 400 a 600ms para transição com significado), checklist de revisão e boas práticas. Cita como referência de estética Headspace, How We Feel, Gentler Streak, Amie e Arc Browser, sem análise deles. Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto. Um critério é subjetivo ("feel" humano), e a skill não traz como medi-lo.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Diagnosticar uma tela que testa bem e mesmo assim parece fria. Para o argumento de polimento, aesthetic-usability.

## jakobs-law
- caminho: `interaction-design/skills/jakobs-law/`
- description: Apply Jakob's Law — users expect your product to work like the others they already use. Use when deciding whether to innovate on a familiar pattern. For OS-mandated conventions specifically, use `platform-conventions` (ui-design).
- o que faz de verdade: Aplica a Lei de Jakob: o usuário espera que o produto funcione como os outros que ele já usa. A skill lista convenções fortes (logo no topo à esquerda leva à home, ícone de carrinho leva ao checkout, X fecha, lupa abre busca) e define quando desviar: quando a convenção falha no caso de uso, quando há convenção de domínio ou quando o teste mostra desempenho pior. Desvio sem motivo não se justifica.
- como trabalha: Não tem passos numerados: princípio, onde as convenções são mais fortes, custo do desvio, quando desviar e quando não, aplicação prática (auditar três a cinco concorrentes, pesar por frequência) e boas práticas. Não carrega referências.
- precisa para rodar: Só texto. A pesquisa de concorrentes exige que alguém forneça os produtos ou que o agente os consulte; a skill não define como.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Decidir se um padrão familiar deve ser seguido ou inovado. Para convenções de SO, platform-conventions.

## millers-law
- caminho: `interaction-design/skills/millers-law/`
- description: Apply Miller's Law — chunk information into groups of about four to fit working memory. Use when grouping fields, menu items, or steps. For reducing the number of choices offered, use `hicks-law`.
- o que faz de verdade: Aplica a ideia de agrupar em pedaços (chunking) para caber na memória de trabalho. A skill registra que a regra dos 7 ± 2 de Miller é muito citada e mal aplicada, e que a estimativa mais realista para pedaços significativos (Cowan, 2001) fica perto de 4 ± 1. Orienta a usar estrutura e agrupamento, não contagem fixa: seções em formulários, categorias em menus, telefones formatados, etapas de onboarding em 3 a 5 fases.
- como trabalha: Não tem passos numerados: princípio e seus limites, onde aplicar (navegação, formulários, códigos, tabelas, onboarding, listas de preço), más aplicações e boas práticas (testar recall). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Agrupar campos, itens de menu e etapas. Para reduzir o número de escolhas, hicks-law.

## onboarding-design
- caminho: `interaction-design/skills/onboarding-design/`
- description: Design the first-run experience — activation path, progressive disclosure, and time to first value. Use for a user's very first session. For the mechanics of the signup form itself, use `form-design`.
- o que faz de verdade: Desenha a primeira sessão do usuário: do cadastro até a primeira ação de valor. Objetivos em ordem: chegar ao valor rápido, orientar em vez de ensinar, criar confiança e reduzir atrito de configuração. Padrões: progressivo (dica no contexto), wizard linear, dados de exemplo, tour interativo. Empty state tratado como onboarding. Indica métricas: ativação, tempo até ativação, retenção em 7 e 30 dias.
- como trabalha: Não tem passos numerados: objetivos, padrões com quando usar, empty states, redução de atrito (coletar depois, defaults, SSO), métricas e erros comuns (tour antes de contexto, coletar dados demais). Não carrega referências. Para a mecânica do formulário de cadastro, form-design.
- precisa para rodar: Só texto. As métricas dependem de instrumentação que o produto precisa ter.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Desenhar a primeira sessão de um produto novo ou revisar a atual.

## peak-end-rule
- caminho: `interaction-design/skills/peak-end-rule/`
- description: Apply the Peak-End Rule — a flow is remembered by its most intense moment and its last. Use when designing completion, celebration, or cancellation moments. For sustaining engagement mid-flow, use `zeigarnik-effect`.
- o que faz de verdade: Aplica a regra do pico e do fim: a memória de uma experiência é dominada pelo momento mais intenso e pelo último, e a duração pesa pouco (duration neglect). Orienta a desenhar o pico (conclusão, primeira entrega com valor) e o fim (confirmação clara), e a não terminar em erro ou tela administrativa. Uma recuperação boa pode virar o novo pico.
- como trabalha: Não tem passos numerados: princípio (Kahneman), desenho do pico e do fim, tabela por fluxo (checkout, onboarding, cadastro, erro), picos negativos e boas práticas (mapear o arco emocional, perguntar aos usuários o que lembram). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Desenhar conclusão, celebração e cancelamento. Para manter engajamento no meio do fluxo, zeigarnik-effect.

## serial-position-effect
- caminho: `interaction-design/skills/serial-position-effect/`
- description: Apply the Serial Position Effect — first and last items in a sequence are recalled best. Use when ordering menus, lists, and steps. For emphasising one item regardless of its position, use `von-restorff-effect` (ui-design).
- o que faz de verdade: Aplica o efeito de posição serial: o primeiro e o último item de uma sequência são lembrados melhor, e o meio é esquecido (o "vale"). Orienta a pôr itens críticos de menu e lista nas bordas, a nunca colocar o CTA principal no meio de três opções, e a fazer o último passo de um fluxo ser resolução, não burocracia. Se um item importante não puder mudar de posição, usa distinção visual.
- como trabalha: Não tem passos numerados: princípio, aplicações (navegação, listas, onboarding, notificações, listas de tarefas), relação com outros princípios e boas práticas (mapear criticidade contra posição, repetir o resumo no fim). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Ordenar menus, listas e passos. Para destacar um item independente da posição, von-restorff-effect.

## teslers-law
- caminho: `interaction-design/skills/teslers-law/`
- description: Apply Tesler's Law — every process has irreducible complexity that someone must absorb. Use when deciding whether the product or the user carries it. For reducing apparent choice, use `hicks-law`.
- o que faz de verdade: Aplica a Lei de Tesler: toda aplicação tem complexidade irredutível, que não some, só muda de lugar. A decisão é quem absorve essa complexidade, o produto ou o usuário. A skill separa complexidade inerente (da tarefa) de complexidade extrínseca (do desenho, a eliminar) e traz uma tabela de quem deveria carregar o quê (datas, país e região, nomes de arquivo, configurações). Alerta contra simplificar a ponto de esconder o que o usuário precisa.
- como trabalha: Não tem passos numerados: princípio, dois tipos de complexidade, tabela de absorção, quando não simplificar, aplicações comuns e boas práticas (verificar para onde foi a complexidade removida). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Decidir se a complexidade fica com o produto ou com o usuário. Para reduzir escolhas aparentes, hicks-law.

## zeigarnik-effect
- caminho: `interaction-design/skills/zeigarnik-effect/`
- description: Apply the Zeigarnik Effect — incomplete tasks stay mentally active. Use when designing progress indicators, saved drafts, and return hooks. For the emotional shape of the ending, use `peak-end-rule`.
- o que faz de verdade: Aplica o efeito Zeigarnik: tarefas inacabadas ficam ativas na mente. Serve para indicadores de progresso ("você está 60% pronto"), rascunhos salvos, retomada de fluxo interrompido e lembretes de conclusão. A skill exige salvamento automático antes de qualquer apelo, no máximo dois ou três laços abertos ao mesmo tempo, e lembretes honestos (só de tarefas que o usuário começou).
- como trabalha: Não tem passos numerados: princípio, aplicações (progresso, reengajamento, interrupção, checklists), quando o efeito vira problema e boas práticas. Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto. O próprio texto alerta contra lembretes que pareçam manipulação.
- harness: Claude Code: skill do plugin interaction-design, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/interaction-design/GEMINI.md. Codex: não verificado.
- serve para: Progresso, rascunho salvo e retorno a fluxo interrompido. Para o fim da experiência, peak-end-rule.

## animation-principles (ficha curta)
- caminho: `interaction-design/skills/animation-principles/`
- description: Apply animation principles — easing, staging, follow-through — to one specific UI motion. Use when tuning how an animation feels. For product-wide duration and easing tokens use `motion-system` (design-systems); for a full interaction spec use `micro-interaction-spec`.
- serve para: Ajustar uma animação específica (easing, encenação, continuidade). Para tokens de movimento do produto, motion-system.

## conversational-ux (ficha curta)
- caminho: `interaction-design/skills/conversational-ux/`
- description: Design voice and conversational interfaces — dialog flows, error recovery, and persona. Use when the interface speaks and listens rather than being tapped. For graphical input collection, use `form-design`.
- serve para: Desenhar interfaces de voz e conversa: fluxos de diálogo, recuperação de erro e persona.

## /interaction-design:design-form (comando, ficha curta)
- caminho: `interaction-design/commands/design-form.md`
- description: Design a form end to end — structure, decision points, chunking, validation, errors, and completion.
- serve para: Formulário de ponta a ponta (estrutura, agrupamento, validação, erros e conclusão). A skill de formulário é form-design.

## /interaction-design:design-interaction (comando, ficha curta)
- caminho: `interaction-design/commands/design-interaction.md`
- description: Design a complete interaction flow for a feature or component.
- serve para: Fluxo de interação completo para uma funcionalidade ou componente.

## /interaction-design:design-onboarding (comando, ficha curta)
- caminho: `interaction-design/commands/design-onboarding.md`
- description: Design a first-run experience end to end — activation path, progressive disclosure, and time to first value.
- serve para: Primeira sessão completa: caminho de ativação, divulgação progressiva e tempo até o valor. A skill é onboarding-design.

## /interaction-design:error-flow (comando, ficha curta)
- caminho: `interaction-design/commands/error-flow.md`
- description: Design an error flow end to end — prevention, detection, messaging, and recovery paths.
- serve para: Fluxo de erro completo: prevenção, detecção, mensagem e caminhos de recuperação. A skill é error-handling-ux.

## feedback-patterns (ficha curta)
- caminho: `interaction-design/skills/feedback-patterns/`
- description: Design confirmations, status updates, and notifications that tell users an action registered. Use when the system must acknowledge success or change. For waiting states use `loading-states`; for failures use `error-handling-ux`.
- serve para: Desenhar confirmações, atualizações de status e notificações que mostram que a ação foi registrada.

## gesture-patterns (ficha curta)
- caminho: `interaction-design/skills/gesture-patterns/`
- description: Design gesture interactions for touch and pointer — swipe, drag, long-press, and their discoverability. Use when input is gestural. For OS-standard gestures on iOS and Android, use `platform-conventions` (ui-design).
- serve para: Desenhar gestos de toque e ponteiro (arrastar, deslizar, pressionar longo) e a descoberta deles.

## loading-states (ficha curta)
- caminho: `interaction-design/skills/loading-states/`
- description: Design waiting experiences — spinners, skeletons, optimistic updates, and progressive reveal. Use when content takes time to arrive. For the latency budget itself use `doherty-threshold`; for success confirmation use `feedback-patterns`.
- serve para: Desenhar as esperas: spinner, skeleton, atualização otimista e revelação progressiva.

## /interaction-design:map-states (comando, ficha curta)
- caminho: `interaction-design/commands/map-states.md`
- description: Model a component's states and transitions end to end — states, events, guards, and edge cases.
- serve para: Modelar os estados e transições de um componente: eventos, guardas e casos de borda.

## micro-interaction-spec (ficha curta)
- caminho: `interaction-design/skills/micro-interaction-spec/`
- description: Specify one micro-interaction completely — trigger, rules, feedback, loops, and modes. Use when handing a single interaction to engineering. For motion craft alone use `animation-principles`; for multi-state components use `state-machine`.
- serve para: Especificar uma microinteração completa (gatilho, regras, feedback e modos) para entregar à engenharia.

## navigation-patterns (ficha curta)
- caminho: `interaction-design/skills/navigation-patterns/`
- description: Select and design a navigation pattern — tabs, drawer, hierarchy, or hub — matched to product structure and user tasks. Use when choosing how users move between sections. For the underlying content structure, use `information-architecture` (ux-strategy).
- serve para: Escolher e desenhar o padrão de navegação (abas, gaveta, hierarquia ou hub) adequado ao produto.

## search-ux (ficha curta)
- caminho: `interaction-design/skills/search-ux/`
- description: Design search — query input, zero results, refinement, and result presentation. Use when users retrieve rather than browse. For browse structure, use `navigation-patterns`.
- serve para: Desenhar a busca: entrada da consulta, resultado zero, refinamento e apresentação dos resultados.

## state-machine (ficha curta)
- caminho: `interaction-design/skills/state-machine/`
- description: Model component behaviour as explicit states, events, and transitions. Use when a component has many interacting states that must be exhaustive. For the feel and feedback of a single interaction, use `micro-interaction-spec`.
- serve para: Modelar o comportamento de um componente como estados, eventos e transições explícitos.

---

**Plugin: design-systems** (11 skills, 3 comandos)

## accessibility-audit
- caminho: `design-systems/skills/accessibility-audit/`
- description: Audit an existing interface against WCAG, producing findings with severity ratings and remediation steps. Use when you have a design or build to assess now. Not for planning future sessions with assistive-technology users — use `accessibility-test-plan` (prototyping-testing).
- o que faz de verdade: Audita uma interface existente contra WCAG 2.2, organizada pelos princípios POUR (perceptível, operável, compreensível, robusto). Classifica achados em quatro severidades (crítico, maior, menor, melhoria). Cada achado traz descrição, localização, critério WCAG, severidade, impacto, passos de correção e código de exemplo.
- como trabalha: Não tem passos numerados: princípios, severidades, formato do achado e boas práticas (testar com tecnologias assistivas, auditar em vários dispositivos e navegadores, checar estados interativos, priorizar por impacto). Não carrega referências. Não há ferramenta automática declarada: a auditoria é feita por leitura.
- precisa para rodar: Só texto, com a interface (código, imagem ou descrição). A própria skill pede teste com tecnologia assistiva para validar.
- riscos: Nenhum visto. Sem ferramenta, a auditoria é uma leitura do modelo e pode deixar passar problemas que só aparecem em uso.
- harness: Claude Code: skill do plugin design-systems, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/design-systems/GEMINI.md. Codex: não verificado.
- serve para: Auditar uma interface que já existe, com achados priorizados. Para planejar testes com usuários de tecnologia assistiva, accessibility-test-plan.

## /design-systems:audit-system (comando)
- caminho: `design-systems/commands/audit-system.md`
- description: Run a comprehensive audit of an existing design system for consistency, completeness, and accessibility.
- o que faz de verdade: Audita um sistema de design existente em sete passos: inventário de componentes, tokens e padrões, consistência de nome, completude da documentação, acessibilidade contra WCAG 2.2 AA, cobertura de tokens, suporte a temas e relatório com achados priorizados e roteiro de correção.
- como trabalha: Passos: inventário (component-spec e design-token), naming-convention, documentation-template, accessibility-audit, design-token, theming-system. Carrega essas skills como referência. Sugere /create-component ou /tokenize depois.
- precisa para rodar: Só texto. O inventário depende de o usuário fornecer o sistema (lista, arquivos ou descrição): o repositório não declara leitura de Figma nem de repositório de código.
- riscos: Nenhum visto. Sem acesso ao sistema real, o inventário é só o que o usuário colar.
- harness: Claude Code: comando /design-systems:audit-system (frontmatter description e argument-hint). Gemini CLI: não entra, porque o build só concatena SKILL.md.
- serve para: Auditoria de consistência, completude e acessibilidade de um sistema que já existe.

## component-spec
- caminho: `design-systems/skills/component-spec/`
- description: Specify one component — props, states, variants, accessibility, and usage rules. Use when defining a library component. For the reusable doc scaffold use `documentation-template`; for a problem-solution pattern use `pattern-library`.
- o que faz de verdade: Especifica um componente de biblioteca em oito seções: visão geral (quando usar e quando não usar), anatomia (obrigatórios e opcionais), variantes (tamanho, estilo, layout), props e API (nome, tipo, padrão, obrigatoriedade), estados (default, hover, focus, active, disabled, loading, error), comportamento (interação, animação, casos de borda), acessibilidade (ARIA, teclado, foco) e uso (faça e não faça).
- como trabalha: Segue a estrutura de oito seções, com exemplos para cada variante e estado. Não carrega referências.
- precisa para rodar: Só texto, com o nome e a função do componente.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin design-systems, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/design-systems/GEMINI.md. Codex: não verificado.
- serve para: Especificar um componente da biblioteca antes de implementar.

## /design-systems:create-component (comando)
- caminho: `design-systems/commands/create-component.md`
- description: Scaffold a full component specification end to end — props, states, variants, accessibility, and documentation.
- o que faz de verdade: Gera a especificação completa de um componente: pesquisa de implementações comuns, anatomia, variantes, estados, tokens consumidos, acessibilidade (ARIA, teclado, leitor de tela), nome e documentação.
- como trabalha: Passos: research, anatomia (component-spec), variantes, estados, tokens (design-token), acessibilidade (accessibility-audit), naming-convention e documentação (documentation-template). Carrega essas skills. Sugere /audit-system depois.
- precisa para rodar: Só texto. Entrada: nome do componente (exemplo do argument-hint: "date picker"). O passo de pesquisa usa só o conhecimento do modelo.
- riscos: Nenhum visto.
- harness: Claude Code: comando /design-systems:create-component (frontmatter description e argument-hint). Gemini CLI: não entra, porque o build só concatena SKILL.md.
- serve para: Especificar um componente novo de ponta a ponta.

## design-system-governance
- caminho: `design-systems/skills/design-system-governance/`
- description: Define how the system evolves — contribution model, versioning, deprecation, and change management. Use when multiple teams contribute. For driving uptake use `design-system-adoption` (designer-toolkit); for design file history use `version-control-strategy` (design-ops).
- o que faz de verdade: Define como o sistema evolui: sete perguntas de governança (dono, quem contribui, como se propõe e decide, versionamento, breaking change, deprecação, qualidade), três modelos (centralizado, federado, híbrido), ciclo de contribuição em sete etapas, semver com regras de patch, minor e major, política de deprecação (manter ao menos um ciclo minor) e padrões de qualidade para entrar no sistema.
- como trabalha: Não tem passos numerados: perguntas, modelos de posse, processo de contribuição, versionamento, deprecação, breaking change e padrões de qualidade. Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin design-systems, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/design-systems/GEMINI.md. Codex: não verificado.
- serve para: Governança quando vários times contribuem para o mesmo sistema. Para adoção, design-system-adoption (designer-toolkit).

## design-token
- caminho: `design-systems/skills/design-token/`
- description: Define and organise tokens for colour, spacing, type, and elevation with naming and usage rules. Use when establishing the token layer. For auditing existing usage use `design-token-audit` (designer-toolkit); for multi-brand mapping use `theming-system`.
- o que faz de verdade: Define e organiza tokens em três níveis: globais (valor bruto, como blue-500), alias (semântico, como color-action-primary) e de componente (escopo, como button-color-primary). Cobre cor, espaçamento, tipo, elevação, borda e motion. Propõe o padrão de nome {category}-{property}-{variant}-{state}.
- como trabalha: Não tem passos numerados: categorias, níveis, padrão de nome e boas práticas (começar pelo global, nunca usar valor bruto em componente, versionar tokens). Não carrega referências.
- precisa para rodar: Só texto, com os valores existentes, se houver.
- riscos: Nenhum visto. O padrão de nome aqui difere do de naming-convention ({category}-{property}-{concept}-{variant}-{state}): é preciso escolher um só.
- harness: Claude Code: skill do plugin design-systems, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/design-systems/GEMINI.md. Codex: não verificado.
- serve para: Criar a camada de tokens de um sistema. Para auditar uso existente, design-token-audit (designer-toolkit).

## documentation-template
- caminho: `design-systems/skills/documentation-template/`
- description: Generate a reusable documentation scaffold for components, patterns, or guidelines. Use when standardising how the system is documented. For the content of one component's spec, use `component-spec`.
- o que faz de verdade: Gera um esqueleto de documentação reutilizável para três tipos: componente (título, status, quando usar, anatomia, variantes, props, estados, acessibilidade, tokens, changelog), padrão (problema, contexto, solução, exemplos bons e ruins) e fundação (propósito, princípios, regras, exceções). Define padrões: hierarquia de títulos, sumário em página longa, indicador de maturidade.
- como trabalha: Não tem passos numerados: três tipos de template, padrões e boas práticas (gerar a partir do código quando possível; auditar a atualidade a cada trimestre). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin design-systems, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/design-systems/GEMINI.md. Codex: não verificado.
- serve para: Padronizar como o sistema é documentado. O conteúdo de um componente específico fica com component-spec.

## icon-system
- caminho: `design-systems/skills/icon-system/`
- description: Specify an icon system — grid, sizing, stroke weight, naming, categories, and implementation. Use when standardising iconography. For broader illustration, use `illustration-style` (ui-design).
- o que faz de verdade: Especifica um sistema de ícones: grade base de 24×24px com keylines e largura de traço, tamanhos (de 12-16px até 48px ou mais), estilo (traço, preenchido, duotone), nome no padrão icon-[category]-[name]-[variant] com oito categorias, entrega (SVG, sprite, wrapper, biblioteca no Figma) e acessibilidade (label ou aria-hidden, área de toque de 44px).
- como trabalha: Não tem passos numerados: fundamentos, nome, entrega, acessibilidade e boas práticas (auditar e remover ícones sem uso; versionar com o sistema). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin design-systems, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/design-systems/GEMINI.md. Codex: não verificado.
- serve para: Padronizar a iconografia. Para ilustração ampla, illustration-style (ui-design).

## localization-design
- caminho: `design-systems/skills/localization-design/`
- description: Design for multiple languages, writing directions, and cultural contexts — text expansion, RTL mirroring, and locale formats. Use when shipping beyond one locale. For the words themselves, use `ux-writing` (designer-toolkit).
- o que faz de verdade: Projeta para vários idiomas, direções de escrita e culturas sem redesenhar por idioma. Cobre expansão de texto (alemão de 20 a 35% a mais, finlandês de 30 a 40%), RTL (espelhamento de layout, propriedades lógicas de CSS como margin-inline-start, ícones direcionais espelhados, números em LTR), tipografia de scripts não latinos (sem negrito falso, CJK, indic), cor e ícones com diferença cultural e formatos de data, número e moeda (Intl).
- como trabalha: Não tem passos numerados: expansão, RTL, tipografia, cultura, implicações para o sistema (propriedades lógicas, tokens com nome semântico) e boas práticas (pseudo-localização; testar com RTL e texto longo antes de adicionar o componente). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin design-systems, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/design-systems/GEMINI.md. Codex: não verificado.
- serve para: Preparar componentes e layouts para mais de um idioma. As palavras em si ficam com ux-writing.

## motion-system
- caminho: `design-systems/skills/motion-system/`
- description: Define motion tokens — durations, easing vocabulary, and reduced-motion handling — for consistency product-wide. Use when standardising motion across a system. For crafting one specific animation, use `animation-principles` (interaction-design).
- o que faz de verdade: Define movimento como sistema de tokens: seis durações nomeadas (de 50ms, instantâneo, a 600ms, deliberado; a skill sugere usar de 4 a 6), cinco curvas de easing por uso (standard, decelerate, accelerate, spring, e linear só para loop), regras de coreografia (stagger de 30 a 50ms, sequência de no máximo 500ms) e reduced motion tratado no sistema (duração de 0 ou 1ms quando a preferência estiver ativa).
- como trabalha: Não tem passos numerados: tokens de duração e easing (tabelas), coreografia, reduced motion, implementação em propriedades CSS e princípios a definir por produto. Não carrega referências.
- precisa para rodar: Só texto. Os valores das tabelas são exemplos da skill.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin design-systems, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/design-systems/GEMINI.md. Codex: não verificado.
- serve para: Padronizar movimento entre componentes. Para uma animação específica, animation-principles (interaction-design).

## naming-convention
- caminho: `design-systems/skills/naming-convention/`
- description: Establish naming rules for components, tokens, and layers with patterns and worked examples. Use when names are inconsistent or being set. For what the tokens actually contain, use `design-token`.
- o que faz de verdade: Estabelece regras de nome para componentes, tokens, camadas, arquivos, código e assets. Propõe padrões: componentes como [category]/[name]/[variant]/[state], tokens como {category}-{property}-{concept}-{variant}-{state}, código em kebab-case no CSS, PascalCase no React e camelCase em props, assets como icon-[name]-[size]. Cinco princípios: previsível, consistente, escalável, legível e sem ambiguidade.
- como trabalha: Não tem passos numerados: princípios, padrões por tipo, armadilhas (abreviação que só o autor entende, separadores misturados, nome por aparência) e boas práticas (documentar em uma página, automatizar lint de nome). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto. O padrão de token aqui difere do de design-token: é preciso escolher um só.
- harness: Claude Code: skill do plugin design-systems, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/design-systems/GEMINI.md. Codex: não verificado.
- serve para: Definir ou corrigir nomes de um sistema. O conteúdo dos tokens fica com design-token.

## pattern-library
- caminho: `design-systems/skills/pattern-library/`
- description: Structure a pattern entry — problem context, solution, usage examples, and related patterns. Use when documenting a recurring solution rather than a component. For a single component's API, use `component-spec`.
- o que faz de verdade: Estrutura a entrada de um padrão (solução recorrente, não componente): problema e contexto, solução, anatomia, variantes, comportamento, exemplos bons e anti-padrões, acessibilidade e padrões relacionados. Categorias: navegação, entrada, exibição, feedback, onboarding. Prioriza o problema antes da solução.
- como trabalha: Não tem passos numerados: estrutura da entrada, categorias e boas práticas (incluir anti-padrões reais; conectar padrões entre si). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin design-systems, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/design-systems/GEMINI.md. Codex: não verificado.
- serve para: Documentar uma solução recorrente que não é um componente. Para um componente, component-spec.

## theming-system
- caminho: `design-systems/skills/theming-system/`
- description: Design theming architecture — brand variants, dark mode, and high-contrast — mapped through token layers. Use when one system must serve multiple themes. For a single palette use `color-system` (ui-design); for dark mode craft use `dark-mode-design` (ui-design).
- o que faz de verdade: Desenha a arquitetura de temas: uma biblioteca de componentes que serve vários temas por override de tokens. Camadas: global (paleta crua), semântica (alias que os temas sobrescrevem) e de componente. Tipos de tema: modo de cor (claro, escuro, alto contraste, dimmed), marca (sub-marcas, white-label, sazonal) e densidade. Implementação com propriedades CSS customizadas, arquivos de token por tema e modos de variável do Figma.
- como trabalha: Não tem passos numerados: camadas, tipos de tema, considerações de dark mode, implementação e boas práticas (tokens primeiro; testar cada componente em cada tema). Não carrega referências.
- precisa para rodar: Só texto.
- riscos: Nenhum visto.
- harness: Claude Code: skill do plugin design-systems, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/design-systems/GEMINI.md. Codex: não verificado.
- serve para: Um sistema que precisa servir vários temas. Para uma paleta só, color-system; para dark mode em detalhe, dark-mode-design.

## /design-systems:tokenize (comando)
- caminho: `design-systems/commands/tokenize.md`
- description: Extract tokens from an existing design or stylesheet and organise them — naming, structure, and theme mapping.
- o que faz de verdade: Extrai valores visuais de um CSS ou arquivo de design, deduplica, categoriza, organiza em três níveis (global, semântico, componente), aplica nomes e mapeia temas. A saída é uma especificação de tokens com inventário, hierarquia, mapa de temas e guia de migração.
- como trabalha: Passos: extrair, deduplicar e categorizar (design-token), hierarquia, nomes (naming-convention), temas (theming-system) e documentação (documentation-template). Carrega essas skills. Sugere /audit-system depois.
- precisa para rodar: O arquivo CSS ou de design, colado ou presente no contexto (argument-hint: "CSS file, design file, or description of values"). O repositório não declara ferramenta para ler arquivos de design.
- riscos: Nenhum visto. A extração é de leitura: não grava nem altera o arquivo de origem.
- harness: Claude Code: comando /design-systems:tokenize (frontmatter description e argument-hint). Gemini CLI: não entra, porque o build só concatena SKILL.md.
- serve para: Sair de valores soltos para um sistema de tokens, com guia de migração.

---

**Plugin: prototyping-testing** (10 skills, 5 comandos)

## accessibility-test-plan
- caminho: `prototyping-testing/skills/accessibility-test-plan/`
- description: Plan accessibility testing — assistive technologies, participant criteria, WCAG coverage, and session protocol. Use when scheduling testing with real AT users. Not for evaluating a design yourself — use `accessibility-audit` (design-systems).
- o que faz de verdade: Planeja testes de acessibilidade com tecnologias assistivas e usuários reais. Organiza em quatro camadas: automatizado (axe, Lighthouse, WAVE, que pegam cerca de 30 a 40% dos problemas, segundo a skill), manual (teclado, leitor de tela, zoom de 200% e 400%, alto contraste, movimento reduzido), tecnologias assistivas (VoiceOver, NVDA, TalkBack, controle por voz, switch) e teste com pessoas com deficiência. Traz uma matriz por fluxo e um formato de relatório com critério WCAG.
- como trabalha: Não tem passos numerados: quatro camadas, matriz de teste por fluxo (teclado, VoiceOver, NVDA, zoom 200%, alto contraste, movimento reduzido), checklist WCAG por princípio e nível, formato do relatório e boas práticas. Não carrega referências.
- precisa para rodar: Só texto. Para executar, precisa de leitores de tela e de pessoas recrutadas; a skill não faz isso sozinha.
- riscos: Nenhum visto. A própria skill separa o plano de teste (aqui) da avaliação própria (accessibility-audit).
- harness: Claude Code: skill do plugin prototyping-testing, invocada pelo agente a partir da description. Gemini CLI: texto incluído em .gemini/extensions/prototyping-testing/GEMINI.md. Codex: não verificado.
- serve para: Planejar teste com usuários de tecnologia assistiva. Para avaliar o design por conta própria, accessibility-audit.

## a-b-test-design (ficha curta)
- caminho: `prototyping-testing/skills/a-b-test-design/`
- description: Design an A/B experiment — hypothesis, variants, primary metric, and sample size. Use when a change can be measured quantitatively at scale. For observing behaviour qualitatively, use `test-scenario`.
- serve para: Desenhar um experimento A/B: hipótese, variantes, métrica principal e tamanho de amostra.

## click-test-plan (ficha curta)
- caminho: `prototyping-testing/skills/click-test-plan/`
- description: Design first-click and click tests for findability and navigation. Use when testing whether people can locate something. For full task-based observation, use `test-scenario`.
- serve para: Desenhar testes de primeiro clique e de clique para medir se as pessoas encontram algo.

## concept-selection (ficha curta)
- caminho: `prototyping-testing/skills/concept-selection/`
- description: Choose between competing concepts against criteria fixed in advance, and record what each rejected concept was testing. Use when several directions are alive and one has to win. For picking which problem to work on, use `opportunity-framework` (ux-strategy); for deciding by production traffic, use `a-b-test-design`.
- serve para: Escolher entre conceitos concorrentes por critérios fixados antes, registrando o que cada descartado testava.

## /prototyping-testing:evaluate (comando, ficha curta)
- caminho: `prototyping-testing/commands/evaluate.md`
- description: Run a heuristic evaluation end to end — expert review against heuristics with severity ratings and recommended fixes.
- serve para: Avaliação heurística completa: revisão de especialista com severidade e correções recomendadas.

## /prototyping-testing:experiment (comando, ficha curta)
- caminho: `prototyping-testing/commands/experiment.md`
- description: Design an A/B experiment end to end — hypothesis, variants, primary metric, and sample size.
- serve para: Experimento A/B completo: hipótese, variantes, métrica principal e tamanho de amostra.

## /prototyping-testing:explore-options (comando, ficha curta)
- caminho: `prototyping-testing/commands/explore-options.md`
- description: Run a parallel exploration end to end — frame the decision, build a spread of behaviourally distinct concepts, pressure-test each, and converge with a decision record.
- serve para: Exploração paralela completa: enquadrar a decisão, criar conceitos distintos, testar cada um e fechar com registro de decisão.

## heuristic-evaluation (ficha curta)
- caminho: `prototyping-testing/skills/heuristic-evaluation/`
- description: Run an expert review against Nielsen's heuristics and domain criteria, with severity ratings. Use when you need findings without recruiting participants. For a facilitated team feedback session, use `design-critique` (design-ops).
- serve para: Avaliação de especialista contra heurísticas de Nielsen e critérios de domínio, com severidade. Para sessão de equipe, design-critique.

## parallel-concepts (ficha curta)
- caminho: `prototyping-testing/skills/parallel-concepts/`
- description: Build several genuinely different solutions to the same problem at once, spread across what the user does rather than how it looks. Use when one direction is on the table and the team is about to refine it by default. For choosing between the concepts afterwards, use `concept-selection`.
- serve para: Construir várias soluções realmente diferentes para o mesmo problema, separadas pelo que o usuário faz, não pela aparência.

## /prototyping-testing:prototype-plan (comando, ficha curta)
- caminho: `prototyping-testing/commands/prototype-plan.md`
- description: Create a prototyping and testing plan for a design initiative.
- serve para: Plano de prototipagem e teste para uma iniciativa de design.

## prototype-strategy (ficha curta)
- caminho: `prototyping-testing/skills/prototype-strategy/`
- description: Choose prototype fidelity and method to match the design question and the decision at stake. Use before building a prototype. For what to test once it exists, use `test-scenario`.
- serve para: Escolher fidelidade e método do protótipo para a pergunta de design e a decisão em jogo.

## /prototyping-testing:test-plan (comando, ficha curta)
- caminho: `prototyping-testing/commands/test-plan.md`
- description: Choose a testing method and build the plan around it — method selection, task scenarios, click tests, and accessibility coverage.
- serve para: Escolher o método de teste e montar o plano em torno dele, com tarefas, cliques e cobertura de acessibilidade.

## test-scenario (ficha curta)
- caminho: `prototyping-testing/skills/test-scenario/`
- description: Write realistic usability task scenarios with success criteria and facilitation notes. Use when you have a study and need the tasks. For the surrounding study design, use `usability-test-plan` (design-research).
- serve para: Escrever tarefas realistas de teste de usabilidade, com critérios de sucesso e notas de facilitação.

## user-flow-diagram (ficha curta)
- caminho: `prototyping-testing/skills/user-flow-diagram/`
- description: Diagram screen-level paths, decision points, and branch logic. Use when specifying how a feature is traversed. For the emotional end-to-end arc, use `journey-map` (design-research).
- serve para: Diagramar caminhos por tela, pontos de decisão e lógica de ramificação de uma funcionalidade.

## wireframe-spec (ficha curta)
- caminho: `prototyping-testing/skills/wireframe-spec/`
- description: Specify wireframe layout — content priority, component placement, and annotation. Use when defining structure before visual design. For grid mechanics, use `layout-grid` (ui-design).
- serve para: Especificar a estrutura de um wireframe: prioridade de conteúdo, posição dos componentes e anotações.

---

**Plugin: design-research** (14 skills, 4 comandos)

## affinity-diagram (ficha curta)
- caminho: `design-research/skills/affinity-diagram/`
- description: Cluster many qualitative data points into themes and insight statements. Use when synthesising across multiple sessions or sources. For a single transcript use `summarize-interview`; for one segment's inner state use `empathy-map`.
- serve para: Agrupar muitos dados qualitativos em temas e insights, a partir de várias sessões ou fontes.

## behavioural-analytics (ficha curta)
- caminho: `design-research/skills/behavioural-analytics/`
- description: Read funnels, retention curves, and event data as a designer — separating a design problem from a tracking artefact. Use when handed product data you did not design and asked why people drop off. For choosing what to measure, use `metrics-definition` (ux-strategy); for running a controlled test, use `a-b-test-design` (prototyping-testing).
- serve para: Ler funis, curvas de retenção e eventos como designer, separando problema de design de artefato de tracking.

## card-sort-analysis (ficha curta)
- caminho: `design-research/skills/card-sort-analysis/`
- description: Analyse open or closed card sort results into a proposed grouping and label set. Use after running a sort study. For turning that evidence into a full structure, use `information-architecture` (ux-strategy).
- serve para: Analisar resultados de card sort (aberto ou fechado) em um agrupamento e um conjunto de rótulos.

## diary-study-plan (ficha curta)
- caminho: `design-research/skills/diary-study-plan/`
- description: Design a diary study — prompts, cadence, duration, participant criteria, and analysis frame. Use when behaviour unfolds over days or weeks. For a single-session study, use `usability-test-plan`.
- serve para: Planejar um diary study: prompts, cadência, duração e critérios de participante.

## /design-research:discover (comando, ficha curta)
- caminho: `design-research/commands/discover.md`
- description: Run a full user research cycle — persona creation, empathy mapping, and journey mapping for a product or feature.
- serve para: Ciclo completo de pesquisa: personas, mapa de empatia e jornada para um produto ou funcionalidade.

## empathy-map (ficha curta)
- caminho: `design-research/skills/empathy-map/`
- description: Build a Says, Thinks, Does, Feels map for one user or segment. Use when sharing user understanding quickly. For a composite archetype with goals and behaviours use `user-persona`; for cross-session themes use `affinity-diagram`.
- serve para: Montar o mapa Says, Thinks, Does, Feels de um usuário ou segmento.

## /design-research:interview (comando, ficha curta)
- caminho: `design-research/commands/interview.md`
- description: Prepare an interview script or summarize an interview transcript into structured insights.
- serve para: Preparar o roteiro de uma entrevista ou resumir a transcrição em insights estruturados.

## interview-script (ficha curta)
- caminho: `design-research/skills/interview-script/`
- description: Write a structured interview guide — warm-up, core exploration, and wrap-up. Use before running interviews. For analysing what comes back, use `summarize-interview`.
- serve para: Escrever o roteiro de entrevista (aquecimento, exploração e fechamento) antes de conduzir.

## jobs-to-be-done (ficha curta)
- caminho: `design-research/skills/jobs-to-be-done/`
- description: Map functional, emotional, and social jobs with outcome expectations. Use when reframing decisions around motivation rather than features. For who the user is, use `user-persona`.
- serve para: Mapear jobs funcionais, emocionais e sociais, com expectativas de resultado.

## journey-map (ficha curta)
- caminho: `design-research/skills/journey-map/`
- description: Map one persona's end-to-end experience with stages, touchpoints, emotions, and pain points. Use when improving an existing experience. For the multi-channel ecosystem use `experience-map` (ux-strategy); for screen-level paths use `user-flow-diagram` (prototyping-testing).
- serve para: Mapear a experiência de um persona do início ao fim, com etapas, pontos de contato, emoções e dores.

## qual-quant-triangulation (ficha curta)
- caminho: `design-research/skills/qual-quant-triangulation/`
- description: Reconcile what the numbers say with what users say, and design the study that settles it rather than restates it. Use when behavioural data and research findings point different ways. For reading the data on its own, use `behavioural-analytics`; for synthesising interviews on their own, use `affinity-diagram`.
- serve para: Conciliar o que os números mostram com o que os usuários dizem, e desenhar o estudo que decide a diferença.

## research-repository (ficha curta)
- caminho: `design-research/skills/research-repository/`
- description: Build a repository that makes findings findable, reusable, and cumulative across teams. Use when the same research keeps getting redone. For synthesising one study, use `affinity-diagram`.
- serve para: Montar um repositório de pesquisa que torne os achados encontráveis e reutilizáveis entre times.

## summarize-interview (ficha curta)
- caminho: `design-research/skills/summarize-interview/`
- description: Turn one interview transcript into themes, supporting quotes, and action items. Use immediately after a session. For synthesising many sessions at once, use `affinity-diagram`.
- serve para: Transformar uma transcrição de entrevista em temas, citações e ações, logo após a sessão.

## survey-design (ficha curta)
- caminho: `design-research/skills/survey-design/`
- description: Design unbiased survey instruments — question wording, scales, and sampling — to measure attitudes at scale. Use when you need quantitative breadth. For behavioural experiments, use `a-b-test-design` (prototyping-testing).
- serve para: Desenhar um questionário sem viés (redação, escalas, amostragem) para medir atitudes em escala.

## /design-research:synthesize (comando, ficha curta)
- caminho: `design-research/commands/synthesize.md`
- description: Synthesize research data into affinity diagrams, themes, and actionable insights.
- serve para: Sintetizar dados de pesquisa em diagrama de afinidade, temas e insights acionáveis.

## /design-research:test-plan (comando, ficha curta)
- caminho: `design-research/commands/test-plan.md`
- description: Run the full usability study workflow — research questions, participant criteria, tasks, metrics, and facilitation guide.
- serve para: Estudo de usabilidade completo: perguntas, critérios de participante, tarefas, métricas e roteiro de facilitação.

## usability-test-plan (ficha curta)
- caminho: `design-research/skills/usability-test-plan/`
- description: Design a usability study — research questions, methodology, participant criteria, metrics, and facilitation guide. Use when planning the study as a whole. For writing the task scenarios inside it, use `test-scenario` (prototyping-testing).
- serve para: Planejar um estudo de usabilidade como um todo: perguntas, método, participantes e métricas. Para as tarefas, test-scenario.

## user-persona (ficha curta)
- caminho: `design-research/skills/user-persona/`
- description: Build research-grounded personas with goals, frustrations, and behavioural patterns. Use when decisions need a consistent user reference. For one session's emotional snapshot use `empathy-map`; for motivation framing use `jobs-to-be-done`.
- serve para: Criar personas baseadas em pesquisa, com objetivos, frustrações e padrões de comportamento.

---

**Plugin: ux-strategy** (12 skills, 3 comandos)

## /ux-strategy:benchmark (comando, ficha curta)
- caminho: `ux-strategy/commands/benchmark.md`
- description: Run a competitive benchmark across a set of products — pattern comparison, gap analysis, and opportunity callouts.
- serve para: Benchmark competitivo entre produtos: comparação de padrões, análise de lacunas e oportunidades.

## business-design (ficha curta)
- caminho: `ux-strategy/skills/business-design/`
- description: Read financials, map competitive landscapes, and argue design decisions in the language of value. Use when defending design to commercial stakeholders. For the live negotiation itself, use `design-negotiation` (designer-toolkit).
- serve para: Ler balanços, mapear o cenário competitivo e defender decisões de design na linguagem de valor.

## competitive-analysis (ficha curta)
- caminho: `ux-strategy/skills/competitive-analysis/`
- description: Compare UX patterns, features, strengths, and gaps across rival products. Use when you need to know what others actually do. For deliberately adopting their conventions, use `jakobs-law` (interaction-design).
- serve para: Comparar padrões de UX, funcionalidades, pontos fortes e lacunas entre concorrentes.

## content-strategy (ficha curta)
- caminho: `ux-strategy/skills/content-strategy/`
- description: Define what content a product needs, how it is structured, and who owns it. Use when content itself is the problem. For the words in the interface use `ux-writing` (designer-toolkit); for structural hierarchy use `information-architecture`.
- serve para: Definir qual conteúdo o produto precisa, como ele se estrutura e quem é dono. Para as palavras da interface, ux-writing.

## design-brief (ficha curta)
- caminho: `ux-strategy/skills/design-brief/`
- description: Write a project brief — problem space, constraints, audience, and success criteria. Use at kickoff for one specific project. For long-horizon aspiration use `north-star-vision`; for reusable decision rules use `design-principles`.
- serve para: Escrever o brief de um projeto: espaço do problema, restrições, público e critérios de sucesso.

## design-principles (ficha curta)
- caminho: `ux-strategy/skills/design-principles/`
- description: Define actionable principles that resolve trade-offs when the team disagrees. Use when the same decisions keep getting relitigated. For a single project's framing, use `design-brief`.
- serve para: Definir princípios acionáveis que resolvem trade-offs quando a equipe discorda.

## experience-map (ficha curta)
- caminho: `ux-strategy/skills/experience-map/`
- description: Map the full ecosystem of touchpoints, channels, and relationships across a service. Use when the experience spans more than one product. For one persona's linear journey use `journey-map` (design-research); for backstage operations use `service-blueprint`.
- serve para: Mapear o ecossistema de pontos de contato e canais de um serviço que passa por mais de um produto.

## /ux-strategy:frame-problem (comando, ficha curta)
- caminho: `ux-strategy/commands/frame-problem.md`
- description: Structure an ambiguous design challenge into a clear problem definition with constraints and criteria.
- serve para: Transformar um desafio ambíguo em definição de problema, com restrições e critérios.

## information-architecture (ficha curta)
- caminho: `ux-strategy/skills/information-architecture/`
- description: Design content structure, hierarchy, labelling, and the navigation model. Use when organising what exists. For the UI that exposes it use `navigation-patterns` (interaction-design); for user-generated grouping evidence use `card-sort-analysis` (design-research).
- serve para: Desenhar a estrutura de conteúdo, hierarquia, rótulos e o modelo de navegação.

## metrics-definition (ficha curta)
- caminho: `ux-strategy/skills/metrics-definition/`
- description: Define UX metrics and KPIs that connect design decisions to measurable outcomes. Use when choosing what to measure. For presenting the results afterwards, use `design-impact-reporting` (design-ops).
- serve para: Definir métricas de UX e KPIs que liguem decisões de design a resultados mensuráveis.

## north-star-vision (ficha curta)
- caminho: `ux-strategy/skills/north-star-vision/`
- description: Articulate a long-horizon product vision that aligns teams and anchors strategy. Use when direction is contested or absent. For near-term project scope, use `design-brief`.
- serve para: Articular uma visão de produto de longo prazo que alinhe times, quando a direção está em disputa ou ausente.

## opportunity-framework (ficha curta)
- caminho: `ux-strategy/skills/opportunity-framework/`
- description: Identify, score, and prioritise design opportunities against impact and effort. Use when there are more ideas than capacity. For framing the one you choose, use `design-brief`.
- serve para: Identificar, pontuar e priorizar oportunidades de design por impacto e esforço, quando há mais ideias que capacidade.

## service-blueprint (ficha curta)
- caminho: `ux-strategy/skills/service-blueprint/`
- description: Map service delivery across frontstage actions, backstage processes, and supporting systems. Use when staff and operations are part of the experience. For the customer-visible layer only, use `experience-map`.
- serve para: Mapear a entrega de um serviço: ações visíveis ao cliente, processos de bastidor e sistemas de apoio.

## stakeholder-alignment (ficha curta)
- caminho: `ux-strategy/skills/stakeholder-alignment/`
- description: Build alignment artifacts — responsibility matrices, decision rights, and communication plans. Use when unclear ownership stalls decisions. For persuading in the moment, use `design-negotiation` (designer-toolkit).
- serve para: Montar artefatos de alinhamento: matriz de responsabilidades, direitos de decisão e plano de comunicação.

## /ux-strategy:strategize (comando, ficha curta)
- caminho: `ux-strategy/commands/strategize.md`
- description: Develop a complete UX strategy for a product or feature area.
- serve para: Estratégia completa de UX para um produto ou área de funcionalidade.

---

**Plugin: design-ops** (9 skills, 3 comandos)

## design-critique (ficha curta)
- caminho: `design-ops/skills/design-critique/`
- description: Facilitate a structured team critique — framing, feedback rules, and actionable outcomes. Use when running a session with people in the room. For a solo expert review, use `heuristic-evaluation` (prototyping-testing).
- serve para: Conduzir uma crítica estruturada com a equipe presente. Para revisão individual, heuristic-evaluation.

## design-debt-audit (ficha curta)
- caminho: `design-ops/skills/design-debt-audit/`
- description: Inventory and prioritise accumulated design inconsistencies across a product. Use when drift has built up over time. For token coverage specifically use `design-token-audit` (designer-toolkit); for WCAG gaps use `accessibility-audit` (design-systems).
- serve para: Inventariar e priorizar inconsistências acumuladas num produto. Para cobertura de tokens, design-token-audit.

## design-impact-reporting (ficha curta)
- caminho: `design-ops/skills/design-impact-reporting/`
- description: Communicate design's contribution to business and user outcomes in stakeholder language. Use when reporting results upward. For choosing the metrics in the first place, use `metrics-definition` (ux-strategy).
- serve para: Comunicar a contribuição do design em linguagem de negócio. Para escolher as métricas, metrics-definition.

## design-qa-checklist (ficha curta)
- caminho: `design-ops/skills/design-qa-checklist/`
- description: Build a QA checklist for verifying that a build matches the design. Use at implementation review. For the spec engineers build from, use `handoff-spec`.
- serve para: Checklist para verificar se o build bate com o design, na revisão de implementação.

## design-review-process (ficha curta)
- caminho: `design-ops/skills/design-review-process/`
- description: Establish review gates — criteria, checkpoints, and approval flow. Use when work ships without consistent review. For running one individual session, use `design-critique`.
- serve para: Estabelecer gates de revisão, critérios e fluxo de aprovação quando o trabalho sai sem revisão.

## design-sprint-plan (ficha curta)
- caminho: `design-ops/skills/design-sprint-plan/`
- description: Plan and facilitate a design sprint from challenge framing through prototype testing. Use when compressing discovery into days. For ongoing team cadence, use `team-workflow`.
- serve para: Planejar e conduzir um sprint de design, do enquadramento ao teste de protótipo.

## /design-ops:handoff (comando, ficha curta)
- caminho: `design-ops/commands/handoff.md`
- description: Run the full handoff workflow — specs, measurements, assets, states, and a QA checklist — and output a developer-ready package.
- serve para: Pacote completo de handoff para desenvolvedores, com specs, medidas, assets, estados e checklist de QA.

## handoff-spec (ficha curta)
- caminho: `design-ops/skills/handoff-spec/`
- description: Write the implementation handoff — measurements, behaviours, assets, states, and edge cases. Use when engineering picks up the work. For verifying the result afterwards use `design-qa-checklist`; for reusable library components use `component-spec` (design-systems).
- serve para: Escrever o handoff para engenharia: medidas, comportamentos, estados e casos de borda.

## /design-ops:plan-sprint (comando, ficha curta)
- caminho: `design-ops/commands/plan-sprint.md`
- description: Run a design sprint end to end — challenge framing, schedule, exercises, and prototype test plan.
- serve para: Rodar um sprint de design de ponta a ponta, com enquadramento, cronograma e plano de teste.

## /design-ops:setup-workflow (comando, ficha curta)
- caminho: `design-ops/commands/setup-workflow.md`
- description: Set up a team's operating rhythm end to end — rituals, task flow, tooling, review gates, and version control.
- serve para: Montar o ritmo operacional de uma equipe: rituais, fluxo de tarefas, ferramentas e gates.

## team-workflow (ficha curta)
- caminho: `design-ops/skills/team-workflow/`
- description: Design the team's operating rhythm — task management, collaboration rituals, and tooling. Use when the day-to-day cadence needs structure. For a time-boxed sprint, use `design-sprint-plan`.
- serve para: Desenhar o ritmo de operação da equipe: tarefas, rituais e ferramentas.

## version-control-strategy (ficha curta)
- caminho: `design-ops/skills/version-control-strategy/`
- description: Define version control for design files, components, and libraries — branching, naming, and release. Use when file history is chaotic. For design system contribution rules, use `design-system-governance` (design-systems).
- serve para: Definir versionamento de arquivos, componentes e bibliotecas de design (branches, nomes, releases).

---

**Plugin: designer-toolkit** (7 skills, 4 comandos)

## /designer-toolkit:build-presentation (comando, ficha curta)
- caminho: `designer-toolkit/commands/build-presentation.md`
- description: Build a design presentation end to end — audience framing, narrative structure, and supporting rationale.
- serve para: Montar uma apresentação de design de ponta a ponta: público, narrativa e justificativa.

## case-study (ficha curta)
- caminho: `designer-toolkit/skills/case-study/`
- description: Craft a portfolio case study with narrative arc, process evidence, and outcomes. Use when telling a project's story to an external audience. For an internal stakeholder deck, use `presentation-deck`.
- serve para: Escrever um estudo de caso de portfólio: arco narrativo, evidência de processo e resultados. Para apresentação interna, presentation-deck.

## design-negotiation (ficha curta)
- caminho: `designer-toolkit/skills/design-negotiation/`
- description: Advocate for design quality, scope, and timeline with partners and leadership using evidence and shared goals. Use in the conversation itself. For the commercial vocabulary behind it, use `business-design` (ux-strategy).
- serve para: Defender qualidade, escopo e prazo de design com parceiros e liderança, na própria conversa.

## design-rationale (ficha curta)
- caminho: `designer-toolkit/skills/design-rationale/`
- description: Write rationale connecting decisions to user needs, business goals, and principles. Use when a decision needs defending in writing. For a live conversation, use `design-negotiation`.
- serve para: Escrever por escrito a justificativa de decisões de design, ligada a necessidades, metas e princípios.

## design-system-adoption (ficha curta)
- caminho: `designer-toolkit/skills/design-system-adoption/`
- description: Create adoption strategy and enablement materials to drive design system usage. Use when the system exists but teams ignore it. For contribution and versioning rules, use `design-system-governance` (design-systems).
- serve para: Criar estratégia e material de adoção quando o sistema existe mas os times não o usam.

## design-token-audit (ficha curta)
- caminho: `designer-toolkit/skills/design-token-audit/`
- description: Audit token usage across a product for coverage, drift, and hard-coded values. Use when tokens exist and you suspect they are being bypassed. For defining tokens in the first place, use `design-token` (design-systems).
- serve para: Auditar o uso de tokens num produto: cobertura, desvio e valores fixos colados.

## presentation-deck (ficha curta)
- caminho: `designer-toolkit/skills/presentation-deck/`
- description: Structure a design presentation for a specific audience and decision. Use when presenting internally. For a portfolio narrative use `case-study`; for the written argument use `design-rationale`.
- serve para: Estruturar uma apresentação de design para um público e uma decisão específicos.

## /designer-toolkit:start-here (comando, ficha curta)
- caminho: `designer-toolkit/commands/start-here.md`
- description: Find where to start in the collection — name what you're working on and get routed to one command, the two that follow it, and the stages you can skip.
- serve para: Roteador: diz por onde começar na coleção, com um comando, os dois seguintes e o que pular.

## ux-writing (ficha curta)
- caminho: `designer-toolkit/skills/ux-writing/`
- description: Write interface copy — microcopy, error messages, empty states, and CTAs. Use when the words are the deliverable. For content structure and ownership, use `content-strategy` (ux-strategy).
- serve para: Escrever o texto da interface: microcopy, mensagens de erro, estados vazios e CTAs.

## /designer-toolkit:write-case-study (comando, ficha curta)
- caminho: `designer-toolkit/commands/write-case-study.md`
- description: Build a portfolio case study end to end — project framing, process narrative, outcomes, and visuals.
- serve para: Estudo de caso completo para portfólio: enquadramento, processo, resultados e visuais.

## /designer-toolkit:write-rationale (comando, ficha curta)
- caminho: `designer-toolkit/commands/write-rationale.md`
- description: Write design rationale for a set of decisions, linking each to user needs, business goals, and principles.
- serve para: Justificativa de um conjunto de decisões, ligando cada uma a necessidades, metas e princípios.
