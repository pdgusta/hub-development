# Skills do vídeo "Insane Claude Design Skills You Need To Actually Build Beautiful Sites"

Canal AI LABS, 12:55, 2026-08-24 (https://youtu.be/Ysr7oNDajJI). Coleta de 2026-10-15, pedida pelo Gustavo: vídeo
baixado por yt-dlp, um quadro a cada 3 s (258 quadros), dez subagentes Haiku 5.5 com um trecho de ~78 s cada (cerca
de 1 milhão de tokens do Haiku no total). Trechos brutos em `C:\Projetos\laco-video-skills\trechos\`. Juntado pelo
maestro.

**Tudo aqui é o que apareceu na tela. Nada foi lido na fonte ainda:** nomes de repositório sem URL inteira na tela
estão marcados "a confirmar". Instalar skill de terceiros é rodar instrução de terceiros; ler cada uma antes.

## 1. emilkowalski/skill (Emil Kowalski, design engineer): animação e acabamento

Instalação na tela: `npx skills add emilkowalski/skill`. Página "AI Skills for Design Engineers". Curso: animations.dev.

| Skill | O que faz (texto da tela) |
|---|---|
| emil-design-eng | a principal: a filosofia do Emil sobre acabamento de UI, componentes e decisões de animação |
| animate | constrói uma animação do zero, escolhendo curva, duração e propriedades |
| animate-expo | o mesmo para React Native |
| review-animations | revisa as animações de forma estrita, pelas regras do autor |
| improve-animations | audita todas as animações e devolve planos priorizados que qualquer agente executa |
| find-animation-opportunities | acha onde o movimento ajuda de verdade, e o que não animar |
| prototype | constrói várias versões realmente diferentes de uma peça de UI e alterna entre elas ao vivo, num seletor visual |
| animation-vocabulary | as palavras certas para pedir a animação que se quer |
| apple-design | os princípios de interface e movimento da Apple (palestras da WWDC), traduzidos para a web |
| pick-ui-library | faz o agente escolher a biblioteca certa entre as que o autor usa e confia |

## 2. ConardLi/garden-skills: engenheiro de design web

Repositório público (selos: MIT, 10 mil estrelas, 5 skills; URL inteira a confirmar).

| Skill | O que faz |
|---|---|
| web-design-engineer | põe o agente como engenheiro de design de primeira linha; "the bar is stunning, not functional". Fluxo: passo 0 conferir fatos antes de tudo, entender o pedido, reunir contexto de design ("never start from thin air"), construir, verificar (autoconferência e um teste de aceitação no navegador), lista antes de entregar, e uma crítica com nota por dimensão (ex.: 7,6/10). Referências: `critique-guide`, `failure-patterns`, `design-calibration`, `design-directions`, `redesign-protocol`, `browser-acceptance`, `block-library`, `advanced-patterns` e receitas de estilo (Linear, Mailchimp, Monocle, Headspace, mid-century) |
| web-video-presentation | vídeo e apresentação na web |
| gpt-image-2 | geração de imagem e prompts |
| beautiful-article | qualquer fonte vira um artigo bonito |

## 3. elayadesign/ai-design-skills: landing page

| Skill | O que faz |
|---|---|
| landing-page-design | landing page do zero: perguntas de entrada, estrutura, texto de conversão e um sistema visual completo ("uma landing page vence uma intenção"; SEO: o que indexar e o que não) |

O README cita outra skill, de outro repositório, para melhorar um site existente (nome não legível).

## 4. MengTo/Skills (Meng To, aura.build e designcode.io)

Pasta `agent-skills/`. URL a confirmar.

- **web-design:** `build-awwwards-quality-sites`, `landing-page`, `pricing-page`, `add-shader-cursor-trail`, `gsap`,
  `threejs`, `tailwindcss`.
- **ui:** `design-first-ui-prompting` (com artigo e referências).
- **media:** `aura-asset-images`, `unsplash-asset-images`.
- **codex:** `audit-verify-explain-grade-5`, `build-daily-inspiration-sites`, `daily-ui-inspiration-capture`.
- **Fluxos citados:** Video to Super Prompt (gravação de tela vira prompt detalhado), HTML to Interaction Prompts
  (página HTML vira prompts por seção ou animação), Stitched Full Page Capture (captura da página inteira como
  referência), Daily UI Inspiration (navegar, capturar, estudar e gerar prompt num laço).
- **game-development** (fora do nosso uso): `build-isometric-arpg`, `author-game-levels`, `design-action-combat` e
  outras.

## 5. jakubkrehel/skills: revisão de interface por disciplina

Plugin do Claude Code (pasta `.claude-plugin`).

| Skill | O que faz |
|---|---|
| better-interface | revisão que coordena todas as abaixo |
| interface-review | revisa as mudanças não gravadas, o ramo ou um pull request contra todas as skills abaixo; roda pelo nome |
| variant | várias versões realmente diferentes de uma peça de UI atrás de um seletor, na página real, para promover a melhor |
| explain-interface | aponta para uma URL ou captura e explica como algo foi construído |
| better-ui | detalhes de acabamento: raio de borda, sombras, animações, microinterações |
| better-typography | escolha e par de fontes, escala, espaçamento, quebra e corte de texto |
| better-colors | sistema de cores: paleta, nomes, cor com significado, contraste, temas |
| better-accessibility | foco, teclado, ARIA, formulários, leitor de tela, área de toque, movimento |
| better-layout | estrutura, agrupamento, alinhamento, ordem de leitura, revelação progressiva, pontos de quebra |
| better-writing | texto de interface: botões, erros, configurações, estados vazios |

## 6. codeswithroh/tastemaker: gosto ancorado em referência real

"A Claude Code skill that grounds AI-generated UI in real references." Primeira ideia: "Ground in real pixels, not
descriptions": das imagens e URLs de referência, extrai os tokens (`design.json` com cores, raio, espaçamento).
Scripts: `check_contrast.py`, `extract_palette.py`, `generate_palette…`, `recolor_svg.py`, `fetch_icons.py`,
`fetch_photos.py`, `export_favicons.py`, `validate_assets.py`, `check_domains.py`, `test_security.py`.

## 7. Owl-Listener/designer-skills: coleção de design de produto

"Agentic skills, commands, and plugins for design — from research…". Organizada por situação:

- **Começar do zero:** `design-brief`, `/design-research:discover` (personas e jornadas), `north-star-vision`.
- **Pesquisa:** `summarize-interview`, `affinity-diagram`, `jobs-to-be-done`.
- **Tela errada sem saber por quê:** `/visual-critique:critique-screen` (lista priorizada de consertos a partir de uma
  captura); `interfaces-that-feel`.
- **Fluxos:** `form-design`, `onboarding-design`, `error-handling-ux`; `hicks-law` e `millers-law` (por que um passo
  pesa demais).
- **Cor:** `color-system`, `dark-mode-design`, `data-visualization` (paletas de gráfico), `theming-system`,
  `critique-color` (contraste).
- **Acessibilidade:** `accessibility-audit`, `accessibility-test-plan`.

## 8. O conjunto do próprio vídeo (nome do repositório a confirmar)

Aparece como `claude-design-skills` e numa pasta "ai-design-system" (leitura incerta), com um arquivo de licença que
cita o Owl-Listener.

- `screen-critique`: diagnostica uma tela em sete dimensões (hierarquia, composição, tipografia, cor e outras).
- `perception-laws`: as leis da percepção para posicionar, agrupar, ordenar e dar ênfase (não para cor ou tipo).
- `design-review`, `brand-voice`, `landing-page`.
- `marketing-ui`: criatividade primeiro, só para a página de marketing. Regras na tela: quebrar o padrão (fontes,
  layouts e paletas genéricas), `design.md` só depois da primeira versão, um momento marcante por página, animar só
  `transform` e `opacity`, respeitar `prefers-reduced-motion`, imagens reais em vez de marcadores.
- Pastas: `ai-slop-detector`, `clone`, `functional-ui`, `gsap`, `shadcn`.

## Outros itens na tela (não são skills)

- **Claude Design** (app "Design" da Anthropic, beta), onde as skills foram demonstradas, e o painel de skills do
  Claude (enviar uma skill passa por uma checagem de segurança).
- O MCP `htm2design` (importa URL ou HTML para o Design).
- Patrocinadores: Twin (twin.so) e Maia, da Make. Ferramentas citadas: aura.build, dreamcut.ai, three.js.

## O que parece servir ao system design (proposta do maestro, a confirmar lendo cada uma)

- **Para os conceitos (forma e composição):** `perception-laws` (agrupar e ordenar), `better-layout`, `variant` ou
  `prototype` (várias versões realmente diferentes atrás de um seletor, o que casa com "três conceitos"),
  `data-visualization` e `hicks-law`/`millers-law` (quanto cabe na tela).
- **Para a crítica de UI e UX:** `interface-review`/`better-interface`, `screen-critique`,
  `/visual-critique:critique-screen` (sobre captura de tela) e o `critique-guide` do `web-design-engineer`, com nota
  por dimensão.
- **Para construir e verificar:** o fluxo do `web-design-engineer` (conferir fatos, reunir contexto, aceitação no
  navegador), `better-colors` e o `check_contrast.py` do tastemaker, `better-typography`, `better-accessibility`.
- **Fora:** landing page, marketing, animação pesada, jogos, geração de imagem, os patrocinadores.
