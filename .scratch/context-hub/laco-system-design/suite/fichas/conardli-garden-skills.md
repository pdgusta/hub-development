# ConardLi/garden-skills

- URL: https://github.com/ConardLi/garden-skills
- Licença: MIT (arquivo LICENSE, "Copyright (c) 2026")
- Estrelas: 12909 (API, consultada em 2026-10-15)
- Última atualização: `updated_at` 2026-10-15T12:16:32Z; último push 2026-10-11T02:28:13Z (API)
- Descrição do repositório (API): "ConardLi's open-source Skills collection, featuring web design, knowledge retrieval, image generation, and more."
- Versão do marketplace: 0.5.0 (`.claude-plugin/marketplace.json`)

Como instalar (literal do README, seção "Install"):

Opção A, `skills` CLI:
```bash
# Install every skill in the collection (latest)
npx skills add ConardLi/garden-skills

# Install just one skill (latest)
npx skills add ConardLi/garden-skills -s web-design-engineer

# Install globally (~/.skills) instead of per-project (./.skills)
npx skills add ConardLi/garden-skills -s gpt-image-2 --global

# Target a specific agent
npx skills add ConardLi/garden-skills -s kb-retriever -a claude-code
```

Opção B, Claude Code plugin marketplace:
```bash
/plugin marketplace add ConardLi/garden-skills
/plugin install presentation-skills@garden-skills
/plugin install web-design-skills@garden-skills
/plugin install knowledge-base-skills@garden-skills
/plugin install image-generation-skills@garden-skills
/plugin install motion-showreel-skills@garden-skills
/plugin install beautiful-article-skills@garden-skills
```

Opções C (zip fixado nas Releases), D (cópia manual após git clone) e E (git submodule) também estão no README. Compatibilidade declarada no README: Claude Code, Claude.ai, Cursor, Codex CLI, Gemini CLI e OpenCode.

Todas as skills do repositório (6): beautiful-article, gpt-image-2, kb-retriever, motion-showreel, web-design-engineer, web-video-presentation. Não há outras pastas com SKILL.md em `skills/`.

---

## web-design-engineer

- caminho: `skills/web-design-engineer` (versão 1.3.0 no manifest)
- description: "Build or redesign polished browser-rendered visual artifacts with HTML/CSS/JavaScript/React: pages, dashboards, prototypes, slide decks, animations, UI mockups, and data visualizations. Use for visual front-end creation, design-system exploration, design critique, or explicit browser acceptance / QA of a web artifact. Not for back-end, CLI, non-visual coding, source-to-longform article conversion, or narration-driven click-through video presentations."
- o que faz de verdade:
  - Faz artefatos visuais para navegador em HTML/CSS/JS/React (páginas, dashboards, protótipos, slides, animações, mockups, visualizações de dados), com o padrão "stunning, not functional" declarado no SKILL.md.
  - Antes de desenhar, exige contexto: lê o código ou os recursos do usuário, pede assets de marca (logo obrigatório em trabalhos de marca) e declara um sistema de design antes do código.
  - Usa cinco "dials" calibrados (variação visual, intensidade de movimento, densidade de informação, dependência de assets, fidelidade de marca) como variáveis de decisão.
  - Tem catálogo de anti-clichês (gradiente roxo, emoji como ícone, Inter por padrão, dados inventados) e uma crítica de 5 dimensões com nota 0 a 10.
  - Verificação em navegador só quando o usuário pede explicitamente (aceitação, QA, responsividade, regressão visual).
- como trabalha: Passos 0 a 7 no SKILL.md.
  - Passo 0: verificar fatos sobre produtos citados antes de desenhar (WebSearch, segundo o próprio texto).
  - Passos 1 a 3: perguntar conforme o caso, montar o "Design Read" com os cinco dials e declarar o sistema de design. Checkpoint 1: parar e esperar confirmação.
  - Passos 4 e 5: v0 com placeholders (Checkpoint 2) e build completo (Checkpoint 3). Os checkpoints mandam esperar o usuário.
  - Passo 6: lista de conferência; a bateria de navegador só se for pedida.
  - Passo 7: crítica de 5 dimensões quando pedida.
  - Modo "Design Direction Advisor" para pedidos vagos: propõe 3 direções de escolas diferentes.
  - Referências carregadas sob demanda: `design-calibration.md` (Design Read e dials), `redesign-protocol.md` (alterar UI existente), `failure-patterns.md` (padrões de falha), `browser-acceptance.md` (só sob pedido), `block-library.md` e `advanced-patterns.md` (código de blocos), `design-directions.md` (escolas), `style-recipes/<âncora>.md` (uma receita por vez, com `INDEX.md` como índice), `critique-guide.md` (crítica).
- referências, uma linha cada:
  - `references/advanced-patterns.md`: trechos de código prontos (slide 16:9, moldura de iPhone e de navegador, painel Tweaks, motor de timeline, design canvas, dark mode, Chart.js, cores oklch, fontes).
  - `references/block-library.md`: índice curto que aponta para as seções de blocos em `advanced-patterns.md`.
  - `references/browser-acceptance.md`: protocolo de aceitação em navegador (gatilho, viewports padrão, passe automatizado e visual, reparo, relatório), só quando pedido.
  - `references/critique-guide.md`: rubricas das 5 dimensões, pesos por tipo de saída, 10 problemas comuns e formato de crítica.
  - `references/design-calibration.md`: como transformar o briefing em "Design Read" e dials, com presets, resolução de conflitos e ramo "image-first".
  - `references/design-directions.md`: as 6 escolas de design com âncoras e prompts para imagem, usadas pelo Design Direction Advisor.
  - `references/failure-patterns.md`: catálogo de falhas recorrentes de design gerado por IA, com detecção e reparo por tipo de artefato.
  - `references/redesign-protocol.md`: como alterar UI existente (classificar como extensão, preservar ou overhaul; auditoria; contratos protegidos).
  - `references/style-recipes/` (INDEX.md + 25 receitas, por exemplo linear, aesop, pentagram, stripe-press, bloomberg-terminal, muji-kenya-hara): cada receita traz paleta, tipografia, espaçamento, raio, sombra e movimento de um estilo de referência.
- precisa para rodar: só texto. Não há pasta `scripts/`. Na prática, usa WebSearch (Passo 0), navegador do ambiente (só para aceitação), CDNs fixadas para React/Babel (`advanced-patterns.md`) e, para coletar assets de marca, ferramentas citadas no texto (yt-dlp e ffmpeg).
- riscos: nenhum script visto. Pontos de atenção: o SKILL.md manda coletar assets de marca por meio de yt-dlp/ffmpeg e fontes de imprensa (texto de sourcing, sem código); carrega fontes e scripts de CDN (Google Fonts, jsDelivr, unpkg). Nenhuma instrução manda ignorar o usuário; os checkpoints exigem esperar confirmação. Não lido: conteúdo integral de `critique-guide.md`, `failure-patterns.md`, `design-directions.md`, `design-calibration.md`, `redesign-protocol.md`, `advanced-patterns.md` e das 25 receitas (lidos só cabeçalhos e índices).
- harness: manifest declara compat claude-code, claude-ai, cursor, codex-cli, gemini-cli e opencode. Há também `agents/openai.yaml` (formato Codex: display_name, default_prompt e `allow_implicit_invocation: true`). Formato base: pasta com SKILL.md (frontmatter name e description) mais references/.
- serve para: criar ou redesenhar interfaces, protótipos, slides e visualizações em HTML/React com critério de design e crítica estruturada.

---

## web-video-presentation

- caminho: `skills/web-video-presentation`
- description: 把一篇文章或口播稿，做成"看起来像视频"的点击驱动 16:9 网页演示，可选合成口播音频。流程：原始文章 → **一次产出**口播稿 + outline 开发计划 → 用户**一次对齐** 5 件事（稿子 / outline / 主题 / 素材 / 开发模式）→ 网页开发（逐章 / 顺序 / 并行）→ 可选音频合成（provider-agnostic：内置 MiniMax mmx-cli + OpenAI TTS，可换 ElevenLabs / edge-tts / Azure / 自带 TTS）。**outline 只规划节奏与信息密度，不规划动画** —— 动画由章节开发时按 PRINCIPLES + ANTI-AI 法则即时设计。每次点击推进口播稿的一个节拍，每一步独占整屏，进度条平时隐藏只在悬浮时出现。适用场景：用网页做视频（动态 PPT 但不像 PPT）、把口播稿 / 文章变成可交互的解说、为 B 站 / YouTube / 视频号录屏教程、做有电影感的产品 / talk demo。本 Skill 沉淀的是设计方法论 + 协作流程 —— 不绑定任何特定样式 / 字体 / 颜色 —— 因此能复用到任意主题与美学。
- o que faz de verdade:
  - Transforma artigo ou roteiro falado em apresentação web 16:9 (Vite + React + TS) em que cada clique avança uma "step" do narrador, pensada para gravação de tela.
  - Gera `script.md` e `outline.md`, cria o projeto com um de 23 temas e, se o usuário quiser, sintetiza um mp3 por step com TTS.
  - Exige que o usuário alinhe cinco pontos antes de desenvolver (roteiro, outline, tema, materiais, modo de desenvolvimento).
- como trabalha:
  - Fase 1: lê a entrada, gera roteiro e outline e faz autoavaliação por revisor isolado.
  - Parada "Checkpoint Plan": espera o alinhamento dos cinco pontos.
  - Fase 2: roda `scaffold.sh`, escreve o capítulo 1 e para para aceite; depois os demais, em modo capítulo a capítulo, sequencial ou paralelo por subagente.
  - Parada "Checkpoint Audio": pergunta se quer áudio.
  - Fase 3 (opcional): extrai as narrações e sintetiza o áudio.
  - Fase 4: gravação, em modo automático (`?auto=1`) ou manual.
  - Referências carregadas: `SCRIPT-STYLE.md` e `OUTLINE-FORMAT.md` (Fase 1), `CHAPTER-CRAFT.md` a cada capítulo, `THEMES.md` ao escolher ou criar tema, `AUDIO.md` (Fase 3), `RECORDING.md` (Fase 4), `EXAMPLES/` só se travar.
- precisa para rodar:
  - `scripts/scaffold.sh` (bash; usa `npm create vite`, `npm install`, `tsx` e `jq` nos provedores).
  - `templates/scripts/extract-narrations.ts` (TypeScript via tsx) e `synthesize-audio.sh` (bash + jq).
  - Provedores: `minimax.sh` (CLI `mmx-cli`, login com `mmx auth login --api-key`) e `openai.sh` (curl + jq, lê `OPENAI_API_KEY` e `OPENAI_BASE_URL` do ambiente).
  - Outros provedores (ElevenLabs, Azure, Google via gcloud, edge-tts, say) aparecem só como trechos no README.
  - Node/npm, navegador para o servidor de desenvolvimento e ffmpeg/ffprobe para checagem de duração.
- riscos:
  - `scaffold.sh` roda `rm -f` nos arquivos padrão do Vite dentro do diretório alvo, grava `package.json` e aborta se o alvo não estiver vazio.
  - O SKILL.md manda `rm -rf presentation/src/chapters/01-example` (apaga pasta).
  - `synthesize-audio` grava `public/audio/<cap>/<n>.mp3`; `extract-narrations` grava `audio-segments.json`.
  - Rede: npm registry; api.openai.com (ou `OPENAI_BASE_URL`) recebe o texto do roteiro; MiniMax via mmx; Google Fonts; jsDelivr só para prévias no README.
  - A documentação pede colar `sk-xxxxx` na linha de comando, o que deixa a chave no histórico do shell.
  - Nenhuma instrução manda ignorar o usuário; as paradas exigem confirmação. Ressalva: PRINCIPLES.md e PATTERNS.md citados no README não existem na pasta.
  - Não lido por completo: `CHAPTER-CRAFT.md`, `SCRIPT-STYLE.md`, `OUTLINE-FORMAT.md`, `THEMES.md`, `RECORDING.md`, `EXAMPLES/`, os templates `.tsx` e os 23 temas (só por grep).
- harness: manifest declara compat claude-code, claude-ai, cursor, codex-cli, gemini-cli e opencode. Não há pasta `agents/`. O SKILL.md depende de "Agent Teams / subagent" para a autoavaliação, com fallback para checagem própria. Formato: SKILL.md com frontmatter name e description, mais references, scripts e templates.
- serve para: transformar um texto ou roteiro em apresentação web narrada e gravável, passo a passo, com áudio opcional.

---

## gpt-image-2

- caminho: `skills/gpt-image-2`
- description: 面向 GPT Image 2 的图像生成 / 编辑技能。可在 3 种环境下使用：(A) Garden 本地模式，通过 OpenAI 兼容接口直接出图并落盘；(B) Host-Native 模式，把本 Skill 当作提示词工程指引，把渲染好的 prompt 交给宿主 Agent 自带的图像工具出图；(C) Advisor 模式，宿主无任何图像工具时退化为高质量 prompt 顾问。涵盖 18 大类、80+ 个结构化模板，覆盖海报 / UI / 产品 / 信息图 / 学术图 / 技术架构图 / 漫画 / 头像 / 流程板 / 电影分镜 / IP 周边 / 编辑工作流等场景。
- o que faz de verdade:
  - Gera e edita imagens com o modelo GPT Image 2 (ou gateways compatíveis com OpenAI), pelos endpoints `POST /images/generations` e `POST /images/edits`.
  - Tem três modos: A (Garden local, chama a API e salva os arquivos), B (Host-Native, entrega o prompt ao tool de imagem do host) e C (Advisor, só escreve o prompt para o usuário, sem fingir que gerou imagem).
  - Traz templates JSON de prompt por categoria (93 arquivos em `references/`, segundo o agente que leu a pasta; o SKILL.md diz "80+" e o README diz 79).
- como trabalha:
  - Passo 0: roda `node skills/gpt-image-2/scripts/check-mode.js` para escolher o modo. Modo A se `ENABLE_GARDEN_IMAGEGEN` for verdadeiro e houver `OPENAI_API_KEY`; A? se faltar a chave; B ou C caso contrário, conforme haja tool de imagem no host.
  - Depois escolhe a categoria, lê só o template mais próximo, preenche os campos (pergunta só o que muda o resultado), renderiza o prompt, salva em `garden-gpt-image-2/prompt/` e gera ou edita (A), entrega ao host (B) ou ao usuário (C).
  - Carrega `references/prompt-writing.md` para o método e um template por tarefa; os demais só sob demanda.
- precisa para rodar:
  - Scripts em JavaScript ESM para Node, sem dependências (`scripts/package.json`; usa fetch, FormData e Blob nativos).
  - `check-mode.js`: só lê variáveis de ambiente, sem rede. `generate.js`: POST JSON. `edit.js`: POST multipart com imagem e máscara locais. `shared.js`: utilitários.
  - Rede: `OPENAI_BASE_URL` (padrão https://api.openai.com/v1, configurável para qualquer host). Chave: `OPENAI_API_KEY`, lida do ambiente e, se ausente, de `<cwd>/.env`, `<cwd>/.gateway.env` ou `~/.gateway.env`. Modelo: `OPENAI_IMAGE_MODEL` (padrão gpt-image-2). Sem pip e sem npm install.
- riscos:
  - Grava arquivos: prompts em `./garden-gpt-image-2/prompt/` e imagens em `./garden-gpt-image-2/image/` (relativos ao cwd). As opções `--prompt-output`, `--image` e `--output` aceitam qualquer caminho. Não apaga nada.
  - Rede: a chave vai como Bearer para `OPENAI_BASE_URL`, sem validação de host, e o prompt vai ao endpoint. Em `edit.js`, imagens e máscara locais são enviadas. Em `generate.js` e `shared.js`, se a resposta trouxer `url`, o script baixa esse URL sem checar o host.
  - Chave: o código carrega todas as variáveis dos arquivos `.env` e `~/.gateway.env` no ambiente do processo, não só as `OPENAI_*`.
  - Conteúdo: o SKILL.md (linhas 240-241) pergunta se o usuário quer usar "真人照片、名人名字" em personagens, o que envolve pessoas reais e identidade.
  - Instruções: nenhuma manda ignorar o usuário ou outras regras.
  - Não lido por completo: `prompt-writing.md` (só até a linha 200) e o conteúdo dos templates de avatar e retrato.
- harness: manifest declara compat claude-code, claude-ai, cursor, codex-cli, gemini-cli e opencode. Formato: SKILL.md com frontmatter name e description, mais manifest.json. Os comandos usam caminhos relativos ao repositório (`skills/gpt-image-2/...`). O README e o SKILL.md divergem na contagem de templates.
- serve para: gerar ou editar imagens com GPT Image 2 pela própria API, ou montar prompts estruturados para as ferramentas de imagem do host.

---

## beautiful-article

- caminho: `skills/beautiful-article`
- description: 把用户提供的素材（网页 URL / PDF / DOCX / Markdown / 纯文本 / 截图 / 粘贴材料）编辑、设计成一篇美丽的、可离线打开和分享的**单文件 HTML 网页文章**。基于 reacticle 组件协议：不手写裸 HTML/CSS，而用语义组件 + 受主题约束的 Raw 自由层；按 source→规划→双确认→生成→终审→修复的小型 harness 流程推进，默认 100% 信息保留的长文。触发场景：把 URL/PDF/DOCX/文章做成网页文章 / 长文 / briefing / 解释文 / 视觉文章 / 教程 / 审阅复盘 / 方案分析，'render this as a beautiful web article / 把这篇做成网页文章 / 生成一篇可分享的 HTML 长文 / reacticle 文章'。只生成文章，不生成后台、表单、dashboard、产品原型或通用 Web App。
- o que faz de verdade:
  - Transforma material de origem (URL, PDF, DOCX, Markdown, texto, imagens, notas) em um artigo HTML único, offline e por padrão longo, com 100% das informações preservadas.
  - Não gera apps, formulários, dashboards nem protótipos; se o pedido for de aplicação, o SKILL.md manda parar e esclarecer.
  - Escreve sobre a biblioteca reacticle (componentes React semânticos), sem CSS livre por padrão.
- como trabalha:
  - Fases 0 a 8, com três checkpoints em que o agente para e pede decisões ao usuário: tipo de artigo, tema, largura, modo de imagens e capa; depois aprovação da primeira página e modo de desenvolvimento; depois modo de entrega.
  - Fluxo: converter a fonte em `source/source.md`, planejar em `plan/plan.md`, montar o workspace com `scaffold.sh`, escrever a primeira seção e a capa, construir seção a seção, revisar em três visões, reparo mínimo e entrega de `article.html` (PDF opcional).
  - Usa subagentes para revisar a primeira página, cada seção e a revisão final.
  - Referências carregadas sob demanda: `harness.md` (fase 0), `source-to-markdown.md` (fase 1), `article-types.md` e `article-types/<tipo>.md`, `information-density.md`, `plan-template.md`, `theme-selection.md`, `layout.md`, `asset-policy.md`, `cover.md` (planejamento), `section-build.md`, `component-policy.md`, `raw-policy.md`, `scaffold.md`, `html-output.md` (construção), `review-checklist.md` e `repair-policy.md` (revisão), `pdf-output.md` (só se pedir PDF).
- precisa para rodar:
  - `scripts/scaffold.sh` (bash): cria o projeto Vite + React + TS, roda `npm install` e `npm install reacticle@latest`, depois `npx tsc`. Exige npm e rede.
  - `scripts/html-to-pdf.sh` (bash): precisa de Chrome, Chromium, Edge ou Brave instalado, em modo headless.
  - `scripts/source-to-markdown.py` (Python, usa pdfplumber ou pdfminer, python-docx e bs4 quando instalados; baixa URLs com urllib) e `scripts/source-to-markdown-markitdown.py` (Python 3.10+, exige `markitdown[pdf,docx]`).
  - `pdf-print-overrides.css`: CSS injetado no PDF.
  - Pacotes npm do template: react, react-dom, reacticle (sem versão fixa), vite, vite-plugin-singlefile e typescript.
  - Rede: npm e Google Fonts (ao abrir o HTML). Não usa mmx-cli, pandoc nem TTS.
- riscos:
  - `scaffold.sh` cria arquivos no diretório alvo (recusa se não estiver vazio, não apaga nada) e roda `npm install`, o que executa scripts de ciclo de vida de pacotes do registry. `reacticle` está como "latest", sem versão fixa.
  - `html-to-pdf.sh` executa o navegador com `--no-sandbox`, grava o PDF no caminho de saída e apaga só o próprio diretório temporário.
  - Os conversores de fonte acessam a URL informada (urllib com User-Agent de Mozilla) e gravam no `-o` indicado.
  - Template: `Article.tsx` aponta para github.com/ConardLi/garden-skills; `index.html` carrega fonts.googleapis.com e fonts.gstatic.com.
  - Instruções: o SKILL.md manda parar nos checkpoints, o que é compatível com o pedido do usuário; manda usar uma ferramenta de pergunta ("AskQuestion"), que pode não existir no ambiente. Nenhum pedido de credencial e nenhum texto que mande ignorar o usuário.
  - Custo: muitos subagentes e reescritas por design.
  - Não lido: conteúdo completo de `theme-profiles/*.md` (só o `index.json`) e de `article-types/visual-essay.md`.
- harness: formato SKILL.md com pastas (`references/`, `scripts/`, `assets/scaffold-template/`, `theme-profiles/`). manifest.json declara name, category, description, homepage e compat claude-code, claude-ai, cursor, codex-cli, gemini-cli e opencode. Não declara plugin, hooks nem comandos. Depende do pacote npm `reacticle`.
- serve para: gerar artigos HTML longos e compartilháveis a partir de um material, com revisão e checkpoints de decisão.

---

## motion-showreel

- caminho: `skills/motion-showreel`
- description: 用代码制作以图形、文字或界面动画为主的短视频（常见 5–60 秒，纯音乐片最长约 2 分钟），输出 MP4 和可编辑源码：产品宣传短片、动效作品集、UI 动效演示、动态排版与金句卡点、Logo 演绎与片头、生成艺术循环、年代回顾短片。配乐可选：代码合成，或按用户提供的曲子卡点。用户想做这类短视频或动效时使用，例如「做个 15 秒动效视频」「做个 Logo 动画 / 片头」「做个产品宣传短片」「用代码做视频」。不用于：口播讲解类长视频、网页与交互原型、写实人物或实拍内容、剪辑已有视频。
- o que faz de verdade:
  - Faz um motion graphic curto em código (5 a 60 s; até cerca de 2 min só com música): a página expõe `render(t)` determinístico, o Playwright captura quadro a quadro e o ffmpeg monta o MP4.
  - Trilha sonora sintetizada em código (ou música do usuário), usando o mesmo `timeline.js`.
  - Entrega MP4 mais o código-fonte editável. Não serve para narração, páginas web, pessoas realistas ou edição de vídeo existente.
- como trabalha: passos 0 a 7 no SKILL.md.
  - Checa o ambiente, pergunta até 5 itens em uma mensagem, escreve `brief.md` (referência, três estruturas candidatas, estilo, lista de proibições).
  - Faz uma única pausa para o usuário escolher o estilo (se não houver, três direções com um quadro cada).
  - Produz timeline, cenas, testes de determinismo e render; áudio opcional; checagem técnica por programa e revisão visual; entrega.
  - Referências sob demanda: `formats.md` (uso), `styles/INDEX.md` e só 1 ou 2 arquivos de estilo, `craft.md`, `brief-template.md`, `stack.md` (contrato da página), `recipes.md`, `sound.md`, `review.md`, `field-notes.md`.
- precisa para rodar:
  - Node 18+ e ffmpeg/ffprobe no PATH (o SKILL diz para o agente não instalar software de sistema).
  - Dependências npm em `scripts/package.json`: playwright ^1.55.0 e tone 15.1.22; Chromium do Playwright, ou Chrome/Edge instalado.
  - Scripts Node ESM (`.mjs`) e `setup.sh`, `scaffold.sh`, `build.sh` em POSIX sh. Python3 só opcional (beats com librosa).
  - Rede: só no setup (npm e download do Chromium) e em `audio.mjs samples` (baixa de tonejs.github.io). O render usa servidor HTTP local em 127.0.0.1.
- riscos:
  - `setup.sh` roda `npm install` dentro da pasta da skill (ou do projeto, se somente leitura) e `npx playwright install chromium`, que baixa da rede.
  - `audio.mjs samples` e `lib/tone-render.mjs` buscam `https://tonejs.github.io/audio/salamander/` e gravam em `scripts/samples/` (ou `SHOWREEL_SAMPLES`).
  - Remoções: `render.mjs` apaga pasta temporária e arquivo `.lock`; `lib/tone-render.mjs` apaga pasta temporária; `lib/frames.mjs` e `audio.mjs` apagam PNG e arquivos temporários; `inspect.mjs` tem `fs.rmSync(file)` na linha 47 (contexto não lido). Saídas em `out/`, `qa/` e `audio/` dentro do projeto.
  - `scripts/package-lock.json` aponta `resolved` para https://bnpm.byted.org (registro interno; não verificado fora dele).
  - `build.sh` não baixa nada; só renderiza e roda `inspect`.
  - Nenhuma instrução manda ignorar o usuário. A única pausa obrigatória é a aprovação do estilo, que faz parte do fluxo.
  - Não lido por completo: `scripts/audio.mjs` (só grep e cabeçalho), `scripts/test/*`, `scripts/package-lock.json` (só grep), `score.layer.mjs` (só 10 linhas) e os estilos individuais.
- harness: manifest declara compat claude-code, claude-ai, cursor, codex-cli, gemini-cli e opencode. Formato: pasta com SKILL.md (frontmatter name e description), mais `assets/`, `references/` e `scripts/`. O README não declara formato de harness além do nome. O SKILL.md fala em "subagente se o host suportar", com fallback se o harness não tiver.
- serve para: gerar um motion graphic curto em código (MP4 mais fonte), com estilo escolhido entre 28 de referência ou customizado.

---

## kb-retriever

- caminho: `skills/kb-retriever`
- description: 面向本地知识库目录的检索和问答助手。核心流程：(1)分层索引导航 (2)遇到PDF/Excel时必须先读取references学习处理方法 (3)处理文件后再检索。按文件类型组合使用 grep、Read、pdfplumber、pandas 进行渐进式检索，避免整文件加载。用户问题涉及"从知识库目录回答问题/检索信息/查资料"时使用。
- o que faz de verdade:
  - Responde perguntas sobre um diretório local de conhecimento (Markdown/txt, PDF e Excel), sem carregar arquivos inteiros.
  - Navega por arquivos `data_structure.md` em cada nível, escolhe os arquivos mais relevantes e faz busca progressiva (grep e leitura em janelas), com no máximo 5 rodadas.
  - Responde citando fonte (arquivo e posição) e marcando incertezas. Proíbe buscar na web ou em outras fontes fora da base; a base é `knowledge/` por padrão ou o caminho informado.
- como trabalha:
  - Fixa a raiz (`knowledge/` por teste de diretório via shell; se faltar, pergunta).
  - Lê `data_structure.md` por nível e desce só pelos ramos relevantes.
  - Antes de PDF, lê obrigatoriamente `references/pdf_reading.md`; antes de Excel, `references/excel_reading.md` e `references/excel_analysis.md`.
  - Converte PDF para texto em arquivo (pdftotext) e lê Excel com pandas (primeiro `nrows`, depois filtros).
  - Faz grep com caminhos restritos e lê janelas de 200 a 500 linhas.
- precisa para rodar:
  - Um script: `scripts/convert_pdf_to_images.py` (Python; converte cada página de um PDF em PNG a 200 dpi, reduzido para caber em 1000 px, na pasta de saída). Usa pdf2image, que depende do poppler (não citado no script).
  - Pacotes citados nos references: poppler (pdftotext, pdftoppm, pdfimages), pdfplumber, pypdf, pypdfium2, pytesseract (OCR), pdf2image, qpdf (opcional), pandas e openpyxl/xlrd.
  - Ferramentas do agente: grep, leitura com offset/limit, shell e Glob. Sem rede.
- riscos:
  - O script grava `page_N.png` na pasta de saída informada e sobrescreve nomes existentes sem aviso. Não apaga nada e não usa rede.
  - O SKILL.md manda gravar texto extraído de PDF em `output.txt` sem dizer onde, o que pode deixar arquivos gerados dentro da base de conhecimento.
  - Exige shell (`test -d`).
  - A regra "ler references antes de processar" é gate de processo, não de segurança.
  - Nenhuma instrução manda ignorar o usuário; a restrição de não usar web limita a fonte e não contraria o pedido.
  - Não lido: `README.zh-CN.md` (listado, não aberto).
- harness: manifest declara compat claude-code, claude-ai, cursor, codex-cli, gemini-cli e opencode. O README indica instalação em `.claude/skills/` ou `.agents/skills/`. Formato: pasta com SKILL.md (frontmatter name e description), mais `references/` e `scripts/`. Versão 1.0.1 (README).
- serve para: responder perguntas com fontes sobre uma base local mista de Markdown, PDF e Excel, com busca progressiva.

---

## Notas de leitura

- Todos os arquivos foram lidos por download (raw.githubusercontent.com) para uma pasta local de rascunho; nada foi clonado, instalado nem executado.
- As cinco fichas de skills (exceto web-design-engineer) foram escritas a partir de relatórios de subagentes que leram os arquivos; não conferi item a item o conteúdo deles. As descrições são o literal do frontmatter, em chinês, sem tradução.
- `web-design-engineer` foi lida pelo agente principal: SKILL.md inteiro e as referências de nível superior por cabeçalho e seções.
