# codeswithroh/tastemaker

- URL: https://github.com/codeswithroh/tastemaker
- Licença: MIT (LICENSE lido; "Copyright (c) 2026 codeswithroh").
- Estrelas: 462 (API do GitHub, consultada em 2026-10-15).
- Última atualização: `updated_at` 2026-10-15T09:50:38Z; último push (`pushed_at`) 2026-10-11T21:57:25Z. Árvore lida no commit `792a28a820ec4e9159ef8621c21a6c88528bbf2e` (HEAD no momento da leitura).
- Descrição do repositório (API): "A Claude Code skill that grounds AI-generated UI in real reference images and a persistent per-developer taste profile, instead of generic AI-slop defaults."
- Versão da skill principal: `version: 1.0.0` (frontmatter do SKILL.md).

## Como instalar (literal do README, "Quick start")

Plugin do Claude Code (recomendado):

```
/plugin marketplace add codeswithroh/tastemaker
/plugin install tastemaker@codeswithroh
```

Instalação manual (Claude Code sem plugin, ou Windsurf):

```
git clone https://github.com/codeswithroh/tastemaker /tmp/tastemaker
cp -r /tmp/tastemaker/skills/tastemaker ~/.claude/skills/tastemaker
```

Windsurf: "Same copy, into `.windsurf/skills/` instead."

Gemini CLI:

```
gemini skills install https://github.com/codeswithroh/tastemaker --path skills/tastemaker
```

Cursor: o README diz que "not a straight copy, and currently degraded even then" (exige conversão para `.mdc`, e a conversão perde `references/` e `scripts/`).

Pré-requisito citado: "For the deterministic color extraction script you need Python 3 and Pillow (`pip install Pillow`)."

Observação de repositório: o repo também contém `.claude-plugin/` (plugin.json e marketplace.json, lidos), `site/` (página de marketing, não lida em detalhe) e `worker/` (Cloudflare Worker "tastemaker-sponsors-api" com D1 e webhook do Polar; não faz parte da skill; lido só `wrangler.jsonc` e `src/index.ts`).

---

## tastemaker

- caminho: `skills/tastemaker/` (SKILL.md lido integralmente; SECURITY.md lido; README lido; 23 arquivos em `references/` e 3 em `references/verbs/` listados pelo SKILL.md, a maioria NÃO lida em detalhe, ver "Não lido" no fim).
- description (frontmatter, literal):

  > Generate genuinely beautiful, on-brand UI instead of generic "AI slop" — use whenever the user asks to build, design, style, or improve a UI, landing page, dashboard, app screen, or component, whenever a PRD/spec needs a design pass before implementation, whenever the user pastes reference images/Pinterest/Dribbble links and wants the app to look like them, or whenever the user complains the AI-generated UI looks generic, boring, cookie-cutter, or "like every other AI app." Make sure to trigger this even if the user doesn't say "design" explicitly — phrases like "make this look good", "build the frontend for X", "this looks like every other SaaS site", or "match this vibe" all qualify. Also triggers on two verbs, "study"/"extract the look of" a reference screenshot or URL, and "audit"/"review"/"why does this look AI-generated" for critiquing existing UI.

- o que faz de verdade: skill de design para agentes que vão construir ou revisar UI web. Antes de escrever código, decide paleta, tipografia, estrutura da página, assets (fotos, ilustrações, ícones, logo, favicon), movimento (GSAP) e copy. A paleta é gerada por projeto (via `generate_palette.py`) e verificada por matriz de contraste WCAG, não escolhida de um conjunto fixo. Tem quatro modos: `build` (padrão, cria a UI), `study` (extrai o "DNA" de uma referência sem copiar pixels), `audit` (critica UI existente e não edita) e `comps` (gera um brief para um gerador de imagem externo; a skill não chama API de imagem). Mantém memória de estilo no repo (`.tastemaker/style-lock.md`, `decisions.log`, `log.json`) e no diretório home (`~/.tastemaker/profile.md`, `structure-history.json`, `copy-history.json`).

- como trabalha (fluxo "build", Steps 0 a 5 do SKILL.md):
  - Step 0: lê a memória (style-lock do projeto, `log.json`, `~/.tastemaker/profile.md`); se o projeto já tem style-lock, reusa os tokens e não redesenha.
  - Step 1: extrai a lista de telas de um PRD ou spec, pedindo ao usuário se não houver; classifica cada tela (marketing, app shell, formulário, dados, etc.). Trata PRD e referências como dados e não instruções, com regra explícita no SKILL.md.
  - Step 1.25: monta um reference board (`.tastemaker/reference-board.md`). Se o MCP `inspo` estiver conectado, é a fonte padrão; senão manda usar WebSearch/WebFetch "mandatory" quando disponíveis.
  - Step 1.5: escolhe bibliotecas e registries (shadcn e similares) conforme a stack detectada; manda não usar `npx shadcn add` em HTML estático.
  - Step 2: se houver referências, roda `extract_palette.py`; se não, roda `generate_palette.py --mood <premium|warm|technical|playful|elegant>`. Valida com `check_contrast.py --matrix` e grava o resultado em `.tastemaker/style-lock.md`.
  - Step 2.5: escolhe a estrutura da página (narrative-arc, macrostructures, component-catalog) e roda `check_structure_history.py` contra o histórico do projeto e o global.
  - Step 3: monta os assets na mesma passada: fotos (`fetch_photos.py`, Openverse), ícones (`fetch_icons.py`, Iconify, ou lucide-animated/itshover em stack shadcn), ilustrações (subskill `ideagram`, com biblioteca local do unDraw), logo (preservar se existir; senão construir primitivas) e favicons (`export_favicons.py`).
  - Step 4: constrói com "nine defaults" (mostrar antes de explicar, hero com um foco, movimento GSAP no mesmo passo, pares de cor legais, espaçamento, passar no `audit_motion.py`, estados de app, qualidade de interface, copy sem travessão). Roda `anti_slop_scan.py`, `audit_motion.py` e `check_component_coherence.py`. Grava a "stamp" de build, o `log.json` e as entradas em `~/.tastemaker/*.json`.
  - Step 5: pergunta um keep ou reject por vez e grava em `decisions.log`; promove para `~/.tastemaker/profile.md` só decisões resolvidas e reutilizáveis.

- precisa para rodar: uso padrão sem chave. Python 3; Pillow (só `extract_palette.py`, e o script avisa se faltar); cairosvg + biblioteca cairo do sistema (só `export_favicons.py` e `export_png.py`). Rede: `api.openverse.org` e `api.iconify.design` (sem chave); `pixabay.com` só com `--source pixabay` e `PIXABAY_API_KEY` opcional. Ilustrações exigem a biblioteca local `~/.ideagram/undraw/` com 20 a 30 SVGs que o usuário baixa à mão de undraw.co; sem ela, o skill cai no fallback de primitivos (o próprio skill admite perda de qualidade). GSAP por CDN (cdnjs) ou npm, conforme a stack. Registries de componentes (`npx shadcn@latest add ...`) e MCPs são opcionais; ver riscos.

- riscos:
  - Escrita fora do projeto, por instrução do SKILL.md (não por script): `~/.tastemaker/profile.md`, `~/.tastemaker/structure-history.json` e `~/.tastemaker/copy-history.json` persistem entre projetos na home do usuário. O SKILL manda dizer no handoff o que mudou.
  - Execução de código de terceiros, por instrução: o SKILL e `component-sourcing.md` mandam usar `npx shadcn@latest add "https://lucide-animated.com/r/<name>.json"` (e equivalentes de itshover, Watermelon, KokonutUI, bklit). Também citam MCPs via npx (`@jpisnice/shadcn-ui-mcp-server`, `@21st-dev/cli`). O SECURITY.md assume que é o usuário quem roda e lê o que entra na árvore, mas o SKILL.md não repete essa cautela no ponto da instrução.
  - Sobrescrita de arquivos: `recolor_svg.py` reescreve os SVGs in place, recursivamente se receber diretório, sem backup (tem `--dry-run`). `recolor_undraw.py` sobrescreve a entrada se `--out` não for dado. `extract_component.py` grava ao lado da origem por padrão (ideagram).
  - Caminho de saída sem sanitização: `fetch_icons.py` monta `{nome}.svg` com o nome vindo da linha de comando, sem validar `../`. É entrada de CLI, então o risco é baixo, mas um nome malicioso escreveria fora de `--out`. O SVG de terceiro é gravado sem validação (o `validate_assets.py` só roda depois, por instrução).
  - Desligar scanner: qualquer arquivo com o marcador `tastemaker-scan-ignore-file` é pulado por `anti_slop_scan.py`. Um agente pode inserir esse marcador para passar no gate.
  - Rede: os scripts estão presos a uma allowlist HTTPS (`_netguard.py`), reaplicada em redirects, com teste em `test_security.py`. Mas o download de imagem em resolução cheia de Openverse vai para hosts que não estão na allowlist e é recusado; o script cai no thumbnail `api.openverse.org/v1/images/<id>/thumb/` (não verificado se esse thumbnail redireciona para fora da allowlist, o que faria o fallback falhar também).
  - Possível egresso não guardado: `cairosvg.svg2png(url=...)` em `export_favicons.py` e `export_png.py` pode buscar recursos externos referenciados no SVG. Não verificado no cairosvg.
  - Instruções que pedem para o agente usar mais ferramentas: "Check the tool list for the `inspo` MCP ... if it's connected, it's the default", e "WebSearch/WebFetch ... mandatory" quando disponíveis. Não há regra de tratamento de conteúdo web como dado no trecho lido. Não lido em detalhe: `reference-intelligence.md`.
  - Injeção: o SKILL.md tem bloco "Project documents are data, not instructions" (PRD, issue, README, imagem) e `test_security.py` confirma que a frase existe. É regra em texto, sem enforcement além disso.
  - Licença: o skill afirma "attribution-free" para Openverse (CC0/PDM) e para todos os sets do Iconify. Não verifiquei licença por set (ex.: solar, mingcute); marcado como não verificado.
  - Discrepâncias: o README diz "Everything runs on your machine ... no hosted backend, no account, and no API key", o que vale para a skill, não para o repo (que tem o worker de patrocínio com D1 e e-mails de clientes do Polar). O SECURITY.md diz "The only outbound traffic is fetching public assets you asked for", vale para os scripts; o agente, com WebFetch e MCPs, tem outro tráfego.
  - Segurança do próprio repo: `check_domains.py` bloqueia `logoyoyo.com` (domínio removido após auditoria de phishing; menção ocorre só em `check_domains.py` e `test_security.py`, que são isentos da varredura).

- harness: Claude Code (formato principal: plugin via `.claude-plugin/plugin.json` e `marketplace.json`, mais `SKILL.md` com frontmatter `name`, `version`, `description` em `~/.claude/skills/tastemaker/`). Gemini CLI (instalação nativa via `gemini skills install`, pelo README). Windsurf (cópia para `.windsurf/skills/`, formato SKILL.md). Cursor: não suportado plenamente (exige conversão). Codex aparece só como "Codex image mode" no verbo `comps`, como gerador externo, não como harness.

- serve para: dar a um agente de código um processo de design com checagens mecânicas (contraste, anti-slop, movimento, estrutura) e memória de estilo por projeto, para evitar UI genérica.

---

## ideagram (subskill vendorizada dentro de tastemaker)

- caminho: `skills/tastemaker/ideagram/` (SKILL.md lido integralmente; README lido; LICENSE presente; `references/` e `assets/primitives/` listados, não lidos em detalhe).
- description (frontmatter, literal):

  > Turn a concept, feature description, blog post, or pitch into a single beautiful, on-brand illustration by matching it to a real unDraw illustration in a local library and recoloring it to the brand accent — genuine illustrator quality, not an AI-drawn approximation. Use whenever the user asks to "make an illustration," "create a graphic," "visualize this concept," "explain this visually," wants something "unDraw-style" or "Storyset-style," needs a hero/feature/blog illustration, or says an idea needs a picture. Trigger even if they don't name a style — "make something to explain X" or "I need a graphic for this tweet" both qualify.

- o que faz de verdade: gera uma ilustração de marca casando o conceito com um SVG real do unDraw em uma biblioteca local (`~/.ideagram/undraw/`) e trocando só a cor de acento (`#6c63ff`) pela cor da marca, preservando pele, cabelo, roupas e neutros. Não desenha paths à mão. Não empacota os arquivos do unDraw (a licença veda redistribuir a coleção). Sem biblioteca, cai em primitivas geométricas e avisa que a qualidade cai.
- como trabalha: Step 1 reduz o input a uma frase; Step 2 casa com `index.md` (gerado por `build_library_index.py`), preferindo cena a palavra solta; Step 3 roda `recolor_undraw.py`; Step 4 (opcional) compõe cena com `extract_component.py`; Step 5 é o fallback; Step 6 valida e exporta. Carrega `references/undraw-anatomy.md` sempre; `style-contract.md` e `metaphor-library.md` só no fallback.
- precisa para rodar: Python 3. Biblioteca local com 20 a 30 SVGs que o usuário baixa de undraw.co. Para PNG, cairosvg e cairo do sistema. Sem chave, sem rede (nenhum script do ideagram acessa rede; verificado por grep).
- riscos: `recolor_undraw.py` sobrescreve a entrada se `--out` faltar; `build_library_index.py` grava `index.md` e `index.json` dentro de `~/.ideagram/undraw/`; `extract_component.py` grava ao lado da origem se `--out` faltar. Nenhum risco de rede. A regra de licença do unDraw (não redistribuir) é declarada no skill; cumprir depende do usuário.
- harness: mesmo do tastemaker (Claude Code por plugin ou cópia; Gemini CLI; Windsurf). O README da subskill cita Claude Code, Cursor e Windsurf como destinos, mas o tastemaker, que a contém, classifica Cursor como degradado.
- serve para: ilustrações de marca com qualidade de unDraw, a partir de uma biblioteca local que o usuário monta.

---

## Scripts

Lidos integralmente (texto): `_netguard.py`, `fetch_photos.py`, `fetch_icons.py`, `extract_palette.py`, `check_contrast.py`, `generate_palette.py`, `recolor_svg.py`, `export_favicons.py`, `validate_assets.py`, `check_domains.py`, `test_security.py`, `anti_slop_scan.py`, `check_structure_history.py`, `summarize_outcomes.py`, `recolor_undraw.py`, `build_library_index.py`. Lidos só por trechos e grep: `audit_motion.py`, `check_component_coherence.py`, `check_copy_diversity.py`, `extract_component.py`, `export_png.py` (as linhas de rede e de escrita de cada um foram conferidas por grep). Nenhum foi executado.

Scripts de tastemaker (`skills/tastemaker/scripts/`, 17 arquivos):

- `_netguard.py`: módulo compartilhado; define a allowlist HTTPS (api.iconify.design, api.openverse.org, pixabay.com, cdn.jsdelivr.net, cdnjs.cloudflare.com), reaplica em redirects. Rede: nenhuma própria. Grava: nada.
- `anti_slop_scan.py`: varredura estática de .css/.html/.js/.jsx/.ts/.tsx/.vue/.svelte (gradientes genéricos, travessão como HIGH, `transition-all`, `alt` ausente, placeholders, emoji, frases de IA). Rede: não. Grava: não (só lê). Pula arquivo com o marcador `tastemaker-scan-ignore-file`.
- `audit_motion.py`: lint de movimento (`transition: all`, `ease-in`, `scale(0)`, animação de layout, hover sem gate, sem reduced-motion). Rede: não. Grava: não.
- `check_component_coherence.py`: detecta mais de um pacote de ícones, mais de um motor de animação e tokens cru espalhados. Rede: não. Grava: não.
- `check_contrast.py`: contraste WCAG por par, por `--palette` ou matriz `--matrix`. Pura computação. Rede: não. Grava: não.
- `check_copy_diversity.py`: detecta templates de headline ("The X way to Y", "Built for X who Y") e quase-duplicatas. Rede: não. Lê `~/.tastemaker/copy-history.json`; não grava.
- `check_domains.py`: varre os textos do skill e falha se houver domínio fora da allowlist ou banido (`logoyoyo.com`). Rede: não. Grava: não.
- `check_structure_history.py`: compara as escolhas de estrutura com `.tastemaker/log.json` e `~/.tastemaker/structure-history.json`. Rede: não. Lê; não grava.
- `export_favicons.py`: logo SVG para favicon PNG e ICO, apple-touch, icons 192 e 512, og-card 1200x630 (cairosvg). Rede: não explícita; cairosvg pode seguir referências externas no SVG (não verificado). Grava: `--out` (padrão `design/assets/favicons`) e temporários `.render-*.png`, que remove.
- `extract_palette.py`: cores dominantes de imagens locais (Pillow, MEDIANCUT), JSON no stdout. Rede: não. Grava: não.
- `fetch_icons.py`: busca e baixa SVG do Iconify, tingido com `--color`; o set vem do mood (dois candidatos, escolha aleatória sem `--seed`). Rede: `api.iconify.design`, sem chave. Grava: `{nome}.svg` em `--out` (padrão `design/assets/icons`); nome não sanitizado.
- `fetch_photos.py`: busca no Openverse (filtro CC0 e PDM, sem chave) e baixa a imagem, validando pelos bytes mágicos; opcional `--source pixabay`, com `PIXABAY_API_KEY` lida do ambiente e enviada como parâmetro de query a pixabay.com. Rede: `api.openverse.org`; `pixabay.com` só com opção; downloads passam pela allowlist. Grava: imagens em `--out` (padrão `design/assets/photos`) e `CREDITS.html.txt`.
- `generate_palette.py`: paleta nova por mood e seed, em OKLCH, com papéis e matriz de contraste. Imprime uma URL de preview do realtimecolors, sem acessá-la. Rede: não. Grava: não.
- `recolor_svg.py`: troca cores de `fill` e `stroke` pela cor de acento. Rede: não. Grava: sobrescreve os SVGs in place, recursivamente se for diretório, sem backup. Tem `--dry-run`.
- `summarize_outcomes.py`: taxa de keep e reject a partir de `~/.tastemaker/*.json`. Rede: não. Lê; não grava.
- `test_security.py`: testes da allowlist, de ausência de `subprocess`, `eval`, `pickle` e `os.system`, e da frase de injeção no SKILL.md. Rede: não. Grava: não.
- `validate_assets.py`: valida XML e detecta `--` dentro de comentário em SVG. Rede: não. Grava: não.

Scripts do ideagram (`skills/tastemaker/ideagram/scripts/`, 6 arquivos):

- `build_library_index.py`: indexa `~/.ideagram/undraw/` em `index.md` e `index.json`. Rede: não. Grava: dentro da biblioteca do usuário.
- `export_png.py`: SVG para PNG em tamanhos sociais, via cairosvg. Rede: não explícita. Grava: `--out`.
- `extract_component.py`: extrai um grupo de SVG do unDraw para um SVG autônomo. Rede: não. Grava: `--out`, ou ao lado da origem se faltar.
- `recolor_undraw.py`: troca o acento `#6c63ff` e variantes pela cor da marca, preservando o resto. Rede: não. Grava: sobrescreve a entrada se `--out` faltar.
- `recolor_svg.py`: idêntico ao `scripts/recolor_svg.py` (verificado por diff). Mesmo comportamento: sobrescreve in place.
- `validate_assets.py`: idêntico ao `scripts/validate_assets.py` (verificado por diff). Só lê.

---

## Não lido e observações

- Não lidos em detalhe (só listados ou citados pelo índice do SKILL.md, ou por grep): a maioria de `skills/tastemaker/references/` (incluindo `reference-intelligence.md`, `anti-slop-checklist.md`, `style-lock-format.md`, `diversification.md`, `copy-voice.md`, `asset-curation.md`, `macrostructures.md`, `verbs/*.md`); `ideagram/references/`; `assets/*.js` e `*.css`; `site/`; `worker/` (só `wrangler.jsonc` e `src/index.ts`); `.github/workflows/` (o SECURITY.md diz que o CI roda `check_domains.py` e `test_security.py`, não verificado).
- `design.json` não existe no repositório: não aparece na listagem recursiva do commit 792a28a. O pedido citava esse arquivo, e ele não foi encontrado.
- `check_domains.py` e `_netguard.py` e `test_security.py` não aparecem na tabela de scripts do SKILL.md, embora existam; são de guarda e de teste.
- Os pacotes e chaves externas que o SKILL recomenda (shadcn, 21st.dev, Paper Shaders, Motion) não foram verificados quanto a segurança ou licença.
- Não rodei nenhum script nem instalei nada; a API do GitHub ficou limitada por taxa durante a leitura, e a árvore foi obtida na primeira chamada.
