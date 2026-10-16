# MengTo/Skills

- **URL:** https://github.com/MengTo/Skills (pasta lida: `agent-skills/`, branch `main`)
- **Licença:** MIT (arquivo `LICENSE`, "Copyright (c) 2026 Meng To")
- **Estrelas:** 6769 (API do GitHub, consultada em 2026-10-15)
- **Última atualização:** `updated_at` 2026-10-15T11:24:05Z; último push (`pushed_at`) 2026-10-06T14:20:26Z
- **Descrição do repo (API):** "Agent skills for designers and builders using Codex, Claude, Cursor, and other AI coding agents"
- **Como instalar (literal do README):** o README não traz comando de instalação. Ele diz: "Use these skills with **Codex**, **Claude Design**, [**Aura Build**](https://aura.build), **Lovable**, and the rest of your agent stack". Na seção "Agent support": "**Claude Code**: reference the relevant skill from `CLAUDE.md`, copy it into a Claude skills setup, or open the `SKILL.md` directly as working context." e "**Codex**: load the relevant `SKILL.md` before acting." O formato é "intentionally plain Markdown and folder-based", com `SKILL.md` obrigatório (frontmatter `name` e `description`).
- **Observação de escopo:** o README lista 176 skills em nove categorias. Esta ficha cobre só as pedidas.

---

## Fichas completas

### build-awwwards-quality-sites

- **caminho:** `agent-skills/web-design/build-awwwards-quality-sites/`
- **description:** "Art-direct and implement distinctive, motion-rich marketing, editorial, portfolio, and landing websites with original reference-inspired imagery, standout heroes, GSAP choreography, one smooth-scroll engine, optional Three.js shaders, honest icon and logo sourcing, photo avatars, accessibility, and performance safeguards. Use when a user asks for an Awwwards-quality, premium, cinematic, interactive, high-concept, or motion-led website, or explicitly requests this visual and motion system."
- **o que faz de verdade:** Dirige a arte e implementa um site com movimento forte (landing, portfólio, editorial). Exige uma direção escrita antes do código, identidade original (não copiar referências), herói com GSAP e uma única engine de scroll suave (Lenis ou Locomotive Scroll, nunca as duas). Three.js só se tiver função. Diz explicitamente que "Awwwards quality" é só meta de qualidade, não prêmio.
- **como trabalha:** 1) direção (tese visual, tipografia, cores, sequência de seções, narrativa de movimento); 2) sistema de assets honesto (ícones via Iconify Solar, logos via Iconify SVG Logos só para empresas reais, Logo Ipsum só para marca fictícia declarada, avatares só com foto); 3) herói com quadro estático completo sem JS; 4) sistema de movimento (GSAP, reduced-motion sem animação); 5) Three.js com propósito (limite de DPR, pausa fora da tela, dispose); 6) checklist de qualidade (rejeita blobs genéricos, wall de logos falso, depoimento falso); 7) validação (build de produção, desktop/mobile, teclado, reduced motion, limpeza de recursos). Não carrega referências: a pasta não tem `REFERENCES.md`.
- **precisa para rodar:** só texto (sem scripts na pasta). Na prática: projeto com build de produção, GSAP e ScrollTrigger, uma engine de scroll (Lenis ou Locomotive), Three.js opcional, acesso à rede para Iconify e fontes de mídia. Pede para "selecionar e nomear pelo menos uma skill de web-design instalada", ou seja, depende de outras skills da coleção. Pasta `assets/` e `demo/` não lidas.
- **riscos:** nenhum visto de escrita ou remoção. Usa mídia de terceiros (Aura.build, quando pedido) e pede proveniência e licença no código. Não manda ignorar o usuário.
- **harness:** Codex (`agents/openai.yaml` com `display_name`, `short_description`, `default_prompt` "Use $build-awwwards-quality-sites ...") e Claude/outros pelo `SKILL.md` (frontmatter `name`/`description`).
- **serve para:** montar um site de landing ou portfólio com direção de arte e movimento forte, com regras de acessibilidade e fallback.

### landing-page

- **caminho:** `agent-skills/web-design/landing-page/`
- **description:** "Use when designing or rewriting a high-converting landing page (single-offer page) for SaaS/apps/services. Covers structure, layout patterns, conversion strategies, copywriting, SEO/AEO, and common pitfalls."
- **o que faz de verdade:** Guia para desenhar ou reescrever uma landing de oferta única ("one offer → one audience → one primary action"). Define a estrutura (acima da dobra: headline, subheadline, CTA, uma prova, imagem; depois problema, benefícios, como funciona, prova, FAQ, CTA final), 4 tipos de layout (A a D), modelos de headline e CTA e checklist de SEO/AEO.
- **como trabalha:** antes de escrever, pede as informações que faltam (CTA principal, oferta, ICP, objeções, fonte de tráfego, provas, tom). Depois trabalha seção por seção. A saída esperada tem 7 itens (outline, copy do herói, benefícios, como funciona, FAQ de 6 a 12 perguntas, SEO/AEO, recomendação de layout). Carrega `REFERENCES.md`, que só tem links (não visitados): um exemplo de skill de copywriting em `coreyhaines31/marketingskills` e a documentação de FAQ schema do Google.
- **precisa para rodar:** só texto. Não tem script nem pacote. Rede só se o agente abrir os links de referência.
- **riscos:** nenhum visto. Não mexe em arquivos. Não manda ignorar o usuário.
- **harness:** `SKILL.md` com frontmatter (Codex, Claude ou qualquer agente que leia Markdown). Sem `agents/openai.yaml`.
- **serve para:** pedir ou revisar a copy e a estrutura de uma landing de conversão.

### pricing-page

- **caminho:** `agent-skills/web-design/pricing-page/`
- **description:** "Use when designing or rewriting a high-converting SaaS pricing page (structure, plan design, copywriting, SEO/AEO, FAQs, layout patterns, experiments). Includes checklists, templates, and common pitfalls."
- **o que faz de verdade:** Guia para uma página de preços de SaaS que "reduz incerteza", não só "mostra preços". Traz estrutura (acima da dobra: headline, toggle mensal/anual, tabela de 3 planos, CTA por plano; abaixo: comparação, FAQ, prova social, seção de segurança para B2B, CTA final), 4 layouts (A a D), cópia de planos e CTAs, checklist de UI e de SEO/AEO.
- **como trabalha:** pede os dados que faltam (oferta, ICP, métrica de valor, planos e preços, objeções, provas, origem do tráfego). Depois segue o checklist de estrutura, de estratégias de conversão e de UI. A saída tem 5 itens (outline, spec da tabela, FAQ, SEO/AEO, layout). `REFERENCES.md` tem só dois links não visitados (o mesmo exemplo de copy e o FAQ schema do Google).
- **precisa para rodar:** só texto. Sem scripts, sem pacotes.
- **riscos:** nenhum visto.
- **harness:** `SKILL.md` com frontmatter. Sem `agents/openai.yaml`.
- **serve para:** desenhar ou revisar uma página de preços de SaaS (planos, copy, FAQ e SEO).

### add-shader-cursor-trail

- **caminho:** `agent-skills/web-design/add-shader-cursor-trail/`
- **description:** "Add the Shaders WebGPU mouse effect used for the Tidal Commons hero: a white twinkling halftone cursor trail driven by ChromaFlow, masked through a DotGrid, finished with chromatic ripples and film grain, and protected by static, touch, accessibility, SSR, and performance fallbacks. Use when a user asks for this shader mouse effect, a halftone cursor trail, an interactive WebGPU hero/contact background, or a reusable cursor-following shader layer in React, Next.js, Vue, Svelte, Solid, or plain web projects."
- **o que faz de verdade:** Adiciona um rastro de cursor em halftone, em WebGPU, com a biblioteca `shaders` (shaders.com). O grafo tem seis nós em ordem fixa (DotGrid, ChromaFlow, dois LinearGradient, CursorRipples, FilmGrain) e dois componentes invisíveis que servem de fonte de dados. Só roda como melhoria progressiva: o fundo estático da seção continua sendo o fallback completo.
- **como trabalha:** 1) inspeciona o framework e a pilha de movimento; 2) instala `shaders` e importa do subcaminho do framework (`shaders/react`, `/vue`, `/svelte`, `/solid`); 3) lê `references/implementation.md` e mantém o grafo e os IDs exatos; 4) em React/Next, copia os arquivos de `assets/react/` (gate leve + módulo pesado com import dinâmico); 5) camada `aria-hidden` atrás do conteúdo; 6) gates: `navigator.gpu`, hover fino, reduced motion, reduced transparency, visibilidade, foco, IntersectionObserver; 7) esconde a camada em reduced motion, coarse pointer e forced colors; 8) valida com lint, build e o script `verify-cursor-trail.mjs`. Carrega `references/implementation.md` (lido). Não lido: `assets/react/` (fora do que foi baixado).
- **precisa para rodar:** pacote npm `shaders` (instalado com o gerenciador do projeto); framework React/Next, Vue, Svelte ou Solid (ou JS puro, seguindo o guia da biblioteca); navegador com WebGPU para verificar o efeito visualmente (não feito por mim). Para o script de validação: Node.js (ES modules, `node:fs/promises`, `node:process`), chamado com três caminhos: `GRAPH_FILE GATE_FILE CSS_FILE`.
- **riscos:** instala dependência de terceiro (`shaders`). O script `verify-cursor-trail.mjs` só lê os três arquivos, faz checagem por regex, não grava e não faz rede (sai com código 2 se faltar argumento). A skill proíbe hotlink para `previews.shaders.com` e `data.shaders.com`. Nenhuma instrução para ignorar o usuário.
- **harness:** Codex (`agents/openai.yaml`) e Claude/outros pelo `SKILL.md`. O `SKILL.md` tem o frontmatter com `description` em aspas.
- **serve para:** trocar o fundo de um hero ou de uma seção de contato por um rastro de cursor em halftone, com fallback.

### gsap

- **caminho:** `agent-skills/web-design/gsap/`
- **description:** "Use when you need to add or debug professional web animations with GSAP (timelines, ScrollTrigger, stagger, transforms) in HTML/CSS/JS/React. Includes patterns for smooth motion, performance, and common pitfalls."
- **o que faz de verdade:** Referência prática da biblioteca GSAP: tweens (`to`, `from`, `fromTo`), timelines com posições, eases, staggers, ScrollTrigger (inline, avançado e `create`). Lista pitfalls (animar propriedades de layout, não limpar em SPA, medir antes de fontes e imagens carregarem) e três receitas (entrada de herói, timeline sequenciada, scroll com scrub e pin).
- **como trabalha:** é consulta: o agente usa os padrões do SKILL.md para escrever ou depurar animação. Pede contexto (site estático ou SPA, pin/scrub, performance, reduced motion). Carrega `REFERENCES.md`, que tem três links para a documentação oficial do GSAP (gsap.to, Timeline, ScrollTrigger), não visitados.
- **precisa para rodar:** biblioteca GSAP no projeto (o SKILL não mostra o comando de instalação); ScrollTrigger como plugin registrado (`gsap.registerPlugin`). Sem script.
- **riscos:** nenhum visto. Não há script nem instrução de escrita.
- **harness:** `SKILL.md` com frontmatter. Sem `agents/openai.yaml`.
- **serve para:** escrever ou depurar animações GSAP (timelines, scroll, stagger) em HTML ou React.

### threejs

- **caminho:** `agent-skills/web-design/threejs/`
- **description:** "Use when building or debugging interactive 3D scenes on the web with Three.js (scene/camera/renderer, lights/materials, GLTF loading, controls, performance). Helpful for designers shipping 3D UI moments."
- **o que faz de verdade:** Guia de cena 3D no navegador com Three.js: modelo mental (Scene, Camera, Renderer, Mesh, luzes, loop com `requestAnimationFrame`), setup, carregamento (GLTFLoader, TextureLoader, DRACOLoader), controles (OrbitControls, PointerLockControls), limpeza (dispose) e pitfalls (resize, DPR alto, vazamento de recursos, texturas grandes, luzes e sombras caras). Tem um exemplo de cubo girando e a regra de reduced motion.
- **como trabalha:** é consulta: o agente usa o modelo mental e as receitas para montar ou depurar uma cena. Pergunta se a cena é decorativa ou funcional, alvo de dispositivo e formatos de asset. `REFERENCES.md` tem um link só (docs do Three.js), não visitado.
- **precisa para rodar:** pacote `three` (usado como `import * as THREE from "three"`); addons como OrbitControls, GLTFLoader e DRACOLoader, que vêm do pacote three. Sem script.
- **riscos:** nenhum visto.
- **harness:** `SKILL.md` com frontmatter. Sem `agents/openai.yaml`.
- **serve para:** montar ou depurar uma cena Three.js em uma página web.

### tailwindcss

- **caminho:** `agent-skills/web-design/tailwindcss/`
- **description:** "Use when designing/implementing UI with Tailwind CSS (layout, typography, responsive, theming, component patterns). Includes quick recipes and conventions for clean, consistent web design."
- **o que faz de verdade:** Convenções de Tailwind: utilitários em HTML/JSX, variantes responsivas e de estado, valores arbitrários com moderação, `dark:` por classe, extração de componentes antes de `@apply`. Pitfalls: classes não geradas em produção (paths de `content`) e classes montadas dinamicamente. Receitas de botão CTA, herói responsivo e mapeamento seguro de classes.
- **como trabalha:** é consulta: o agente aplica as convenções e as receitas. Pergunta framework, sistema de design, dark mode e acessibilidade. `REFERENCES.md` tem um link só (instalação do Tailwind), não visitado.
- **precisa para rodar:** Tailwind no projeto com o pipeline de build que lê os arquivos de `content`. Sem script.
- **riscos:** nenhum visto.
- **harness:** `SKILL.md` com frontmatter. Sem `agents/openai.yaml`.
- **serve para:** montar ou revisar UI com Tailwind, com regras de consistência e responsividade.

### design-first-ui-prompting

- **caminho:** `agent-skills/ui/design-first-ui-prompting/`
- **description:** "Use when you need design-first, spec-driven, skimmable prompts for UI generation. Covers prompt structure, constraints, variations, typography/spacing rules, and iteration workflow for consistent UI outputs."
- **o que faz de verdade:** Um modelo de prompt para gerar UI (GOAL, FORMAT, LAYOUT, TYPE SYSTEM, COLOR + MATERIAL, IMAGERY, COPY exato, CONSTRAINTS, NEGATIVE PROMPT). Regras: travar um sistema e iterar com variantes (uma variável por vez); tipografia em duas passadas (gerar sem texto, depois tipografar no Figma); "cards de constraints". Termina com perguntas para quando o pedido é vago.
- **como trabalha:** é um template e uma checklist. O agente preenche o modelo e itera mudando uma coisa de cada vez. Também pergunta quando o pedido está vago. Carrega `ARTICLE.md` (ensaio em tom de opinião, marcado como "Draft", com indicações de ferramentas e modelos) e `REFERENCES.md` (cinco links: mobbin.com, bentogrids.com, figma community, icon-sets.iconify.design, simpleicons.org; não visitados).
- **precisa para rodar:** só texto. Para seguir as dicas de referência: acesso a Figma e Iconify (opcional). Sem script.
- **riscos:** nenhum visto. O ARTICLE.md cita modelos e ferramentas específicos ("GPT-5.1", "Gemini 3", "Nano Banana Pro", "Superhero") como recomendação. Isso não foi verificado e pode ficar datado. Não manda ignorar o usuário.
- **harness:** `SKILL.md` em Markdown com frontmatter. Sem `agents/openai.yaml`. Serve a qualquer agente que lê texto.
- **serve para:** escrever prompts de geração de UI com layout, tipografia e restrições explícitas.

### aura-asset-images

- **caminho:** `agent-skills/media/aura-asset-images/`
- **description:** "Use when you need high-quality stock-style images from Aura Assets (aura.build/assets) similar to Unsplash for design mockups and marketing: backgrounds, abstract wallpapers, architecture, portraits, and headshots. Includes a workflow for searching by tag on aura.build/assets and returns 5 real image URLs per category plus practical guidance for using different resolutions and aspect ratios."
- **o que faz de verdade:** Dá 25 URLs de imagens prontas do Aura Assets (5 por categoria: backgrounds, abstract, architecture, portraits, headshots), mais orientação de busca por tag (`https://www.aura.build/assets?q=<tag>&order=popular`), troca de `_800w` por `_1600w` ou `_3840w` e tabela de proporções (1:1, 4:5, 3:4, 16:9, 9:16).
- **como trabalha:** o agente abre a página de busca do Aura, escolhe 5 candidatos por categoria e devolve as URLs diretas. Sugere tamanhos de exportação. Não carrega referências nem scripts.
- **precisa para rodar:** só texto. Para buscar de novo: acesso à web (página do aura.build). As URLs já estão fixas no SKILL.md e apontam para o storage do Aura, em um subdomínio Supabase.
- **riscos:** nenhum script nem escrita. Riscos de conteúdo: as URLs são fixas e de terceiros, e a própria skill avisa que variantes podem dar 404. A skill não verifica licença de uso das imagens, e a lista inclui retratos de pessoas reais para headshots. Antes de usar em produção, confirmar a licença no Aura.
- **harness:** `SKILL.md` com frontmatter. Sem `agents/openai.yaml`.
- **serve para:** achar imagens de fundo, arquitetura e retratos no estilo stock para mockups.

### unsplash-asset-images

- **caminho:** `agent-skills/media/unsplash-asset-images/`
- **description:** "Use when you need to pick high-quality Unsplash images for product/design assets (avatars, headshots, portraits, large website backgrounds, and abstract wallpapers) and output real Unsplash URLs plus practical instructions for producing the right resolutions and aspect ratios (1:1, 4:5, 3:4, 16:9, 9:16)."
- **o que faz de verdade:** Dá 25 páginas de fotos do Unsplash (5 por uso: avatares 1:1, headshots 4:5 e 3:4, retratos editoriais, backgrounds 16:9, wallpapers abstratos) com tamanhos sugeridos para cada uso. Diz para usar o botão Download do Unsplash e cortar na ferramenta do usuário. Evita Unsplash+ por padrão.
- **como trabalha:** o agente devolve a URL canônica da página da foto e as proporções e tamanhos do caso de uso. Não carrega referências nem scripts.
- **precisa para rodar:** só texto. Acesso à web só se o agente for buscar outras fotos.
- **riscos:** nenhum script. A skill afirma que as imagens do Unsplash são "generally free to use" e que a atribuição não é obrigatória. Isso é a posição da skill, não foi verificado por mim. Retratos de pessoas reais (headshots, avatares) exigem checagem de uso. Como as URLs são fixas, podem sair do ar.
- **harness:** `SKILL.md` com frontmatter. Sem `agents/openai.yaml`.
- **serve para:** escolher fotos do Unsplash para avatares, headshots, backgrounds e wallpapers, já com o tamanho certo.

### audit-verify-explain-grade-5

- **caminho:** `agent-skills/codex/audit-verify-explain-grade-5/`
- **description:** "Audit work, verify claims with concrete evidence, and explain the result in simple grade-5 language. Use when the user asks to review, audit, check, verify, explain a change, explain a fix, summarize test results, validate whether something works, or translate technical findings into plain language for non-technical readers."
- **o que faz de verdade:** Processo em três etapas para qualquer resposta de revisão: auditar o que mudou, verificar com evidência (ordem: testes e builds, app rodando, logs e capturas, leitura estática, inferência rotulada) e explicar em linguagem simples. Separa fato de julgamento. Não diz "tudo funciona" sem teste do fluxo completo. Para performance, distingue "medido" de "deve melhorar".
- **como trabalha:** 1) audita a fonte da verdade (diff, call sites, testes); 2) verifica pela ordem de evidência e diz o que não foi verificado; 3) explica com frases curtas, termos técnicos definidos e o formato "O que mudou / Por que importa / Como verifiquei / O que ainda não está provado". Termina com o próximo teste útil, se houver. Não carrega referências nem scripts.
- **precisa para rodar:** só texto. Depende do projeto ter o que verificar (testes, build, logs, app).
- **riscos:** nenhum visto. É instrução de processo; não grava nem apaga. Não manda ignorar o usuário.
- **harness:** Codex (`agents/openai.yaml` com `default_prompt` "Use $audit-verify-explain-grade-5 ...") e `SKILL.md` com frontmatter para outros agentes.
- **serve para:** revisar uma mudança, checar uma afirmação de teste e explicar o resultado para quem não é técnico.

### build-daily-inspiration-sites

- **caminho:** `agent-skills/codex/build-daily-inspiration-sites/`
- **description:** "Turn a completed daily UI inspiration capture into exactly five original landing-page builds, one per separate Codex task, using Sites. Use when the user asks to turn the daily inspiration references, a five-item UI prompt pack, or a dated `*-ui-inspiration-capture` article into distinct HTML landing pages while changing the source brands, names, copy, people, numbers, pricing, claims, and imagery."
- **o que faz de verdade:** Pega uma captura de inspiração pronta (5 itens, com `manifest.json`, `content.md` e uma imagem de página inteira por item) e cria cinco landing pages originais, cada uma em uma tarefa separada do Codex, publicadas com o plugin Sites. Manda trocar marca, nomes, copy, pessoas, números, preços e imagens. Mantém só a gramática visual da referência.
- **como trabalha:** 1) valida a captura com `scripts/validate_capture.mjs`; se falhar, para; 2) cria a matriz de originalidade (cinco identidades novas, sem nomes parecidos entre si); 3) monta um brief por item com `references/thread-brief-contract.md` (lido) e anexa uma única imagem de referência; 4) cria as cinco tarefas no Codex (reaproveita se já existir); 5) exige de cada tarefa build de produção, commit só do código validado e deploy privado no Sites; 6) relata o mapeamento referência → marca.
- **precisa para rodar:** Codex com as ferramentas de tarefas (criar, buscar e acompanhar threads); plugin Sites com `sites:sites-building` e `sites:sites-hosting`; o navegador in-app do Codex (a skill proíbe o Chrome); uma pasta de captura pronta gerada pela skill `daily-ui-inspiration-capture`; Node.js para o script `validate_capture.mjs`.
- **riscos:** o script `validate_capture.mjs` só lê o `manifest.json`, confere se os arquivos existem e têm tamanho maior que zero, e imprime JSON na saída padrão. Não grava nem apaga, e não usa rede. Riscos da skill em si: cria tarefas no Codex; faz commit de código; faz deploy no Sites. Diz para "seguir as regras de aprovação do Sites se só houver acesso compartilhado ou público", o que pode levar a publicação compartilhada ou pública (a skill não esclarece o padrão). Manda reaproveitar tarefas existentes que batam com o título. Não manda ignorar o usuário, mas exige que ele peça explicitamente as tarefas separadas.
- **harness:** Codex. Usa `agents/openai.yaml` (`display_name` "Build Daily Inspiration Sites", `default_prompt` com `$build-daily-inspiration-sites`), tarefas de thread do Codex e o plugin Sites. O `SKILL.md` tem frontmatter.
- **serve para:** transformar uma captura diária de cinco referências em cinco sites originais, em tarefas separadas e com deploy privado.

### daily-ui-inspiration-capture

- **caminho:** `agent-skills/codex/daily-ui-inspiration-capture/`
- **description:** "Create a recurring daily UI inspiration capture. Use when the user asks to run, refresh, package, or validate dated UI inspiration bundles, especially for `articles/YYYY-MM-DD-ui-inspiration-capture/` outputs, Framer/Dribbble landing-page inspiration, motion-study screenshots/videos, AI-builder prompts, duplicate checking, or converting a project runbook into repeatable workflow."
- **o que faz de verdade:** Roda uma captura diária de inspiração de UI como pacote de artigo: 5 referências com still, vídeo curto, screenshot de página inteira, cortes por seção contíguos, quadros de movimento (pelo menos 4 quando o vídeo funciona), `content.md` e `manifest.json` com prompts longos para construtor de IA. Checa duplicatas antes de commitar. Não cria `README.md`.
- **como trabalha:** 1) lê o `AGENTS.md` e o runbook do projeto de conteúdo; 2) lê manifestos e artigos anteriores para evitar duplicatas; 3) escolhe as referências (Framer Marketplace de preferência; Dribbble só se der); 4) captura com o navegador in-app do Codex, esperando 2 segundos após cada scroll; 5) corta as seções do screenshot completo; 6) escreve o `content.md` com a estrutura pedida; 7) verifica (duplicateCount 0, 5 itens, arquivos existem, cortes sem buraco de pixels) e faz `git add -f` e commit só da pasta do dia.
- **precisa para rodar:** Codex com o navegador in-app (a skill proíbe o Chrome); captura de vídeo e screenshot de página inteira (ferramenta não incluída na pasta da skill); Node para `scripts/check-ui-inspiration-duplicates.mjs` e `scripts/ui-inspiration-capture-guidelines.md`, que não estão nesta pasta e são do projeto de conteúdo do usuário; git. Não há `references/` nem `scripts/` dentro da pasta da skill.
- **riscos:** `git add -f` e commit no repositório de conteúdo (a skill diz "stage and commit only the files created"). Cria pastas e arquivos com capturas de sites de terceiros, com direito autoral que a skill não discute. Gera prompts longos para copiar a referência, embora a própria skill peça "treat the page as reference, not a template". Não manda ignorar o usuário. Pede para não forçar workarounds frágeis contra WAF.
- **harness:** Codex (`agents/openai.yaml` com `default_prompt` "Use $daily-ui-inspiration-capture to run today's UI inspiration capture."). O `SKILL.md` tem frontmatter.
- **serve para:** rodar a captura diária de inspiração de UI como um pacote de artigo datado, com prompts e verificação.

---

## Resumo de game-development (20 skills, sem ficha completa)

Lidos: nome, `description` do frontmatter e uma linha derivada da description. O corpo dos SKILL.md não foi lido nesta rodada. Os arquivos de `references/`, `scripts/` e `templates/` também não foram lidos.

1. **author-game-levels**
   - description: "Author or revise readable, flat-world Three.js game levels. Use for movement and camera routes, collision and navigation, encounter zones, landmarks, objectives, pickups, motivated lighting, visibility, deterministic level data, or desktop and mobile playthrough verification."
   - linha: criar ou revisar fases em Three.js (rotas, colisão, zonas de encontro, objetivos).
2. **build-game-audio-feedback**
   - description: "Design or implement responsive audio feedback for a Three.js or web game. Use for action sounds, combat layers, music states, spatial audio, mix priorities, mute controls, accessibility, mobile audio unlock, and audio performance."
   - linha: desenhar ou implementar feedback sonoro (ações, combate, música, áudio espacial).
3. **build-game-camera-controls**
   - description: "Implement or tune Three.js game cameras. Use for isometric framing, follow behavior, orbit/zoom limits, occlusion, lock-on, camera shake, touch camera controls, and camera regression tests."
   - linha: implementar ou ajustar câmeras de jogo (isométrica, seguir, lock-on, shake, toque).
4. **build-game-changelog**
   - description: "Design, implement, backfill, audit, and release in-game changelogs with contiguous versioning, deployment provenance, menu-state navigation, accessible toggle, close, and Escape behavior, and responsive release-ledger UI. Use when Codex needs to add or revise a changelog or version screen in a game, reconstruct release history from deployments and Git, define version-bump rules, keep displayed versions synchronized with live builds, or test changelog mechanics across desktop and mobile."
   - linha: criar uma tela de changelog dentro do jogo, com versões e histórico reconstruído do Git.
5. **build-game-inventory**
   - description: "Build or repair game inventory, loot, equipment, tooltips, drag-and-drop, persistence, and progression systems. Use for item schemas, pickup flows, stack rules, equipment slots, atomic swaps, save migration, and no-loss regression testing."
   - linha: construir ou consertar inventário, loot, equipamento e persistência.
6. **build-game-map-editor**
   - description: "Build, extend, or audit production-linked browser map editors for Three.js and isometric games. Use when Codex needs to create a private director view, derive a versioned editor document from authored placements, add outliner, layer, selection, drag, snap, inspector, or camera controls, expose enemy aggro, leash, or patrol overlays, implement local draft import, export, undo, and reset, secure an editor route with IP and password sessions, or validate and release a map editor without mutating live gameplay data."
   - linha: criar ou auditar um editor de mapas no navegador, com rota protegida por IP e senha.
7. **build-game-monster-system**
   - description: "Build, integrate, audit, or refactor rigged monsters for Three.js and web action games. Use for monster asset contracts, procedural or imported creature rigs, semantic joints and sockets, hurtboxes and attack volumes, combat animation states, enemy-runtime adapters, LODs, deterministic review fixtures, and validating that every monster follows one shared system."
   - linha: montar ou auditar monstros com rig, hurtboxes, estados de animação e LODs.
8. **build-hybrid-game-assets**
   - description: "Plan, create, integrate, or audit a hybrid asset pipeline for a Three.js or web game. Use when choosing among imported meshes, procedural 3D geometry, AI-generated reference art, 2D UI media, sprites, VFX, and performance-ready runtime asset delivery."
   - linha: planejar o pipeline de assets de um jogo web (malhas, procedural, arte de referência, sprites, VFX).
9. **build-isometric-arpg**
   - description: "Build or extend a playable isometric action RPG in Three.js, React, or similar web technology. Use for game-loop architecture, camera and movement, zones, combat integration, content data, progression, saves, or production-ready vertical slices."
   - linha: construir ou estender um ARPG isométrico jogável (loop, câmera, zonas, combate, saves).
10. **build-mobile-threejs-games**
    - description: "Build, tune, or test a Three.js game for mobile web. Use for touch movement, action controls, target selection, touch inventory, safe areas, portrait/landscape layouts, responsive HUD, battery/performance budgets, and real mobile browser QA."
    - linha: adaptar ou testar um jogo Three.js para celular (toque, áreas seguras, HUD, bateria).
11. **build-rigged-game-assets**
    - description: "Create, integrate, or audit production-ready rigged 3D characters and monsters with a main model, skeleton, animation library, sockets, collision contracts, separate character equipment, optimized runtime files, catalog media, and an interactive moveset inspector. Use when generating or importing FBX/GLB game actors; defining character-versus-monster asset requirements; separating swords, shields, helmets, armor, or stowed gear; adding idle, walk, run, attack, hit, dodge, block, cast, or death clips; wiring an asset into gameplay; or adding action and equipment controls plus deterministic tests to a game asset catalog."
    - linha: criar ou auditar personagens rigados (FBX/GLB) com clipes, sockets e inspetor de moveset.
12. **build-threejs-enemy-systems**
    - description: "Build or refactor reusable, data-driven enemy archetype and moveset systems for Three.js action games. Use for enemy content schemas, model and rig conventions, combat move timing and contact contracts, runtime state boundaries, placeholder fallbacks, deterministic fixtures, or production playthrough validation."
    - linha: montar sistemas de inimigos orientados a dados (arquétipos, movesets, timing de ataque).
13. **build-vesperfall-review-assets**
    - description: "Build truthful Vesperfall asset-library review pairs from transparent PNG references and live Three.js, FBX, or img2threejs models. Use when adding a character, enemy, prop, or equipment asset to the Vesperfall catalog; creating a card-PNG plus inspector-model treatment; exposing an isolated model or moveset route; or standardizing provenance, grounding, tests, and Codex-browser validation for game art review."
    - linha: criar pares de revisão de assets do catálogo Vesperfall (PNG de referência e modelo ao vivo).
14. **create-game-vfx**
    - description: "Create readable, performance-safe Three.js game visual effects. Use for attacks, impacts, damage feedback, status effects, spell trails, particles, shaders, telegraphs, quality tiers, and reduced-motion alternatives."
    - linha: criar efeitos visuais de jogo legíveis e leves (ataques, impactos, partículas, shaders).
15. **design-action-combat**
    - description: "Design, implement, tune, or test readable tactical action combat for web games. Use for attack timing, guard and dodge windows, hit contact, posture, lock-on, weapons, boss phases, combat feedback, and deterministic combat tests."
    - linha: desenhar ou testar combate de ação tático (timing, guarda, esquiva, boss).
16. **design-game-encounters**
    - description: "Design, implement, tune, or test Three.js action-game encounters. Use for arena layout, enemy composition, spawn pacing, objectives, boss phases, reward cadence, encounter fixtures, and difficulty validation."
    - linha: desenhar ou testar encontros de ação (arenas, composição de inimigos, ritmo de spawn, dificuldade).
17. **optimize-threejs-games**
    - description: "Profile, diagnose, and improve Three.js or WebGL game performance without regressing gameplay. Use for frame-time drops, CPU/GPU pressure, draw calls, texture and geometry budgets, animation loops, adaptive quality, mobile performance, and browser performance verification."
    - linha: perfilar e melhorar a performance de jogos Three.js ou WebGL sem regredir o gameplay.
18. **ship-web-games**
    - description: "Package, deploy, and verify a playable Three.js or web game. Use for release builds, asset delivery, private/public deployment, production smoke tests, browser proof, release notes, rollback readiness, and cleanup of temporary QA resources."
    - linha: empacotar, publicar e verificar um jogo web jogável (build, deploy, smoke test, rollback).
19. **test-playable-web-games**
    - description: "Test a playable browser game end to end with deterministic fixtures and real browser evidence. Use for gameplay QA, regression testing, controls, accessibility, responsive/mobile testing, save flows, console checks, performance smoke tests, and release verification."
    - linha: testar de ponta a ponta um jogo jogável no navegador, com fixtures e evidência real.
20. **tune-enemy-ai**
    - description: "Build, debug, balance, or test combat enemy AI for playable action games. Use for aggro, target selection, navigation, spacing, attack choices, telegraphs, retreats, boss behavior, behavior-state machines, and deterministic AI regression tests."
    - linha: construir, depurar ou balancear a IA de inimigos de combate (aggro, espaçamento, retiradas, boss).

---

## Notas de leitura

- Não lidos nesta rodada: pastas `demo/`, `assets/` e `preview`/imagens de todas as skills; `assets/react/` de `add-shader-cursor-trail`; corpo dos SKILL.md de game-development; `references/`, `scripts/` e `templates/` de game-development.
- Nenhuma skill lida manda ignorar o usuário ou as regras do projeto. Os riscos listados são de efeito (escrita, commit, deploy, direito de imagem, dependência de terceiros), não de desvio de instrução.
- Scripts lidos (`validate_capture.mjs`, `verify-cursor-trail.mjs`): nenhum grava, apaga ou faz rede. Os scripts de game-development não foram lidos, então não há afirmação sobre o efeito deles.
