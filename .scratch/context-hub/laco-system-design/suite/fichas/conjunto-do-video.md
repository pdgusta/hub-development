# Conjunto do vídeo

Vídeo: "Insane Claude Design Skills You Need To Actually Build Beautiful Sites" (AI LABS, 2026-08-24), https://youtu.be/Ysr7oNDajJI

- **Onde foi achado:** a descrição do próprio vídeo (via yt-dlp) lista sete repositórios; o último é `designer-skills`, em https://github.com/Owl-Listener/designer-skills. Os demais são emilkowalski/skills, ConardLi/garden-skills, elayadesign/ai-design-skills, MengTo/Skills, jakubkrehel/skills e codeswithroh/tastemaker.
- **Certeza:** baixa para a correspondência exata. O repositório Owl-Listener/designer-skills existe e é o citado no vídeo, mas os nomes `screen-critique` e `perception-laws` não aparecem na árvore dele. Há um pacote que cobre o mesmo papel do `screen-critique` (plugin `visual-critique`, sete dimensões de crítica). Para `perception-laws` o análogo é a família `ui-design/skills/law-of-*`. Essas equivalências são inferência minha, não o nome do vídeo.
- **Não achados com esses nomes:** `screen-critique`, `perception-laws`, `marketing-ui`, `ai-slop-detector` (há outros repos com esse nome, nenhum com a skill do vídeo), `clone`, `functional-ui`, `gsap`, `shadcn`, `brand-voice`, `design-review` (há `design-review-process`, análogo). A busca por código no GitHub exigiu autenticação e não pôde ser usada. Nenhum arquivo local "claude-design-skills" ou "ai-design-system" foi investigado (fora do escopo, sem acesso ao disco do vídeo).
- **Licença:** MIT, "Copyright (c) 2026 MC Dean" (LICENSE do repo). O arquivo do vídeo citando "owl-listen..." é coerente com o nome da organização Owl-Listener, mas não foi verificado.
- **Estrelas:** 2926 (API do GitHub, consulta de 2026-10-15).
- **Última atualização:** `pushed_at` 2026-09-05; `updated_at` 2026-10-15 (metadados do repo, sem commit novo visível).
- **Como instalar (README, fonte primária):** `/plugin marketplace add Owl-Listener/designer-skills` e depois `/plugin install <plugin>@designer-skills`. O README diz que o marketplace só registra o caminho; a instalação é por plugin escolhido.
- **Tamanho declarado no README:** 273 skills e 76 comandos em 33 plugins, em cinco coleções. A coleção de design prática (esta repo) tem 9 plugins; as outras quatro estão em repos separados (ai-design-skills, ux-pgm-skills, design-leadership-skills, inclusive-design-skills).

---

## critique-screen (comando análogo ao screen-critique)

- caminho: visual-critique/commands/critique-screen.md (comando `/critique-screen`)
- description: "Run all seven visual critiques on a screen and output a prioritised fix list."
- o que faz de verdade: roda sete críticas (hierarquia, marca, composição, tipografia, cor, affordance, densidade de informação) sobre uma tela e devolve uma lista única de correções, ordenada em P1 (crítico, antes de publicar), P2 (importante, no sprint) e P3 (polimento). Cada item traz problema, dimensão e correção. Fecha com um parágrafo sobre a dimensão mais forte e a mais fraca.
- como trabalha: um passo por dimensão, cada um apontando para a skill `critique-*` correspondente; depois junta e ranqueia os achados. Não há passo de renderização nem de medição: a entrada é uma tela, screenshot ou URL de Figma passada pelo usuário.
- precisa para rodar: só texto (comando e skills em Markdown). Na árvore do repo não há scripts para esse pacote.
- riscos: nenhum visto. Em particular, o conteúdo é prompt; a precisão das críticas depende do modelo ler a imagem corretamente. Não foi verificado.
- harness: Claude Code, via plugin `visual-critique` (instalação por marketplace).
- serve para: critica de uma tela já renderizada, com lista de correções priorizada. Não serve para desenhar do zero.

## critique-visual-hierarchy

- caminho: visual-critique/skills/critique-visual-hierarchy/SKILL.md
- description: "Critique a rendered screen's hierarchy — entry point, eye flow, weight distribution, and emphasis. Use when attention lands in the wrong place. For establishing hierarchy in new work, use `visual-hierarchy` (ui-design)."
- o que faz de verdade: avalia se o ponto de entrada da tela é o elemento mais importante, o caminho do olhar, o peso visual (diferença de tamanho de pelo menos 1,5x entre níveis) e a ênfase, que deve ser única por tela. Para cada dimensão pede observação, problema e correção, com nota pass / minor issue / major issue.
- como trabalha: revisão por checklist de quatro dimensões e padrões de falha (hierarquia achatada, CTA enterrado, duas ênfases concorrentes). Saída em texto estruturado.
- precisa para rodar: só texto.
- riscos: nenhum visto. O limiar de 1,5x é regra fixa do texto, não validada.
- harness: Claude Code, plugin `visual-critique`.
- serve para: revisar onde a atenção cai numa tela existente.

## critique-composition

- caminho: visual-critique/skills/critique-composition/SKILL.md
- description: "Critique a rendered screen's composition — balance, whitespace, rhythm, and gestalt grouping. Use when a layout feels off but hierarchy is fine. For emphasis and eye flow specifically, use `critique-visual-hierarchy`."
- o que faz de verdade: avalia equilíbrio, espaço em branco (macro e micro), ritmo e agrupamento gestáltico (proximidade, semelhança, figura/fundo, continuidade, fechamento) em uma tela já renderizada. Mesmo formato de saída das outras críticas (observação, problema, correção, nota).
- como trabalha: checklist por dimensão, com padrões de falha típicos (duas colunas com peso igual, padding inconsistente, elementos órfãos).
- precisa para rodar: só texto.
- riscos: nenhum visto.
- harness: Claude Code, plugin `visual-critique`.
- serve para: diagnosticar um layout que parece errado quando a hierarquia está boa.

## law-of-proximity (análogo a perception-laws; não é a mesma skill)

- caminho: ui-design/skills/law-of-proximity/SKILL.md (a família é ui-design/skills/law-of-*: closure, common-region, continuity, figure-ground, proximity, similarity)
- description: "Apply the Law of Proximity — spatial closeness groups elements more strongly than any other cue. Use when spacing alone must carry grouping. For grouping via containers use `law-of-common-region`; via shared appearance use `law-of-similarity`."
- o que faz de verdade: explica como o espaçamento agrupa elementos (rótulo perto do campo, cabeçalho mais perto do conteúdo que do bloco anterior) e dá regras: espaço maior entre grupos, menor dentro, escala consistente de espaçamento, nada de borda para fazer o trabalho do espaço.
- como trabalha: é guia de construção, não de crítica: aplica a lei ao criar layout e lista padrões (campos de formulário, cartões, grupos de botões, linhas de dados).
- precisa para rodar: só texto.
- riscos: nenhum visto.
- harness: Claude Code, plugin `ui-design`.
- serve para: decidir agrupamento por espaço ao desenhar um layout. Não é a skill "perception-laws" do vídeo: o vídeo cita essa como sendo sobre colocar, agrupar, ordenar e enfatizar, e a família law-of-* cobre isso em partes, uma lei por skill. Equivalência não confirmada.

## design-review-process (análogo a design-review; não é a mesma skill)

- caminho: design-ops/skills/design-review-process/SKILL.md
- description: "Establish review gates — criteria, checkpoints, and approval flow. Use when work ships without consistent review. For running one individual session, use `design-critique`."
- o que faz de verdade: define quatro portões de revisão de design (conceito, design, pré-handoff, QA de implementação), critérios (resolve o problema, usa o sistema, WCAG AA, estados cobertos) e um fluxo de aprovação (autorrevisão, par, líder, stakeholder, desenvolvedor).
- como trabalha: processo de equipe em texto, sem ferramenta. Não critica uma tela: organiza quando a revisão acontece.
- precisa para rodar: só texto.
- riscos: nenhum visto.
- harness: Claude Code, plugin `design-ops`.
- serve para: montar um processo de revisão de design para uma equipe. Não é o "design-review" de crítica visual do vídeo, que não foi encontrado com esse nome.

---

## Não lidos (achados ou citados, sem ficha)

- Demais repos da descrição do vídeo (emilkowalski/skills, ConardLi/garden-skills, elayadesign/ai-design-skills, MengTo/Skills, jakubkrehel/skills, codeswithroh/tastemaker): só listei as árvores. Não lidos.
- Skills do vídeo sem correspondência encontrada: marketing-ui, ai-slop-detector, clone, functional-ui, gsap, shadcn, brand-voice, landing-page. Não lidas.
- Demais coleções Owl-Listener (ai-design-skills, ux-pgm-skills, design-leadership-skills, inclusive-design-skills): só o README da casa e a árvore de ai-design-skills. Não lidas.
