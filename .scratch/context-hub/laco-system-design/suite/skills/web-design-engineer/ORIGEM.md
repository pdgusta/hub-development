# Origem: web-design-engineer

- **Repositório:** https://github.com/ConardLi/garden-skills
- **Caminho no repositório:** `skills/web-design-engineer`
- **Commit fixado:** `7a6d5a72e4f44bb4cc0c23c01b3d97205c723b68` (HEAD lido com `git ls-remote` em 2026-10-15; arquivos baixados com `curl` de `raw.githubusercontent.com/ConardLi/garden-skills/7a6d5a72e4f44bb4cc0c23c01b3d97205c723b68/...`)
- **Data da cópia:** 2026-10-15
- **Licença:** MIT, Copyright (c) 2026 (sem nome no arquivo). O `LICENSE` do repositório está nesta pasta.
- **Papel na suíte:** UI engineer
- **Leitura:** SKILL.md, advanced-patterns, block-library, critique-guide, design-calibration, failure-patterns, redesign-protocol, browser-acceptance e README.md inteiros; README.zh-CN, design-directions e style-recipes não lidos (removidos).

## Alterações em relação ao original

Arquivos mantidos: `SKILL.md`, `references/` (`advanced-patterns.md` reduzido, `block-library.md`, `critique-guide.md`, `design-calibration.md`, `failure-patterns.md`, `redesign-protocol.md`).

### Arquivos removidos da cópia (baixados e lidos, salvo onde indicado)
- `references/design-directions.md` (apoio do Direction Advisor; não lido por inteiro, removido).
- `references/style-recipes/` (INDEX.md e 25 receitas; restilizar; não lidas, removidas).
- `references/browser-acceptance.md` (lido inteiro; a aceitação é do QA).
- `README.md` (lido inteiro; propaganda e instalação) e `README.zh-CN.md` (tradução do README; não lido, removido).
- `manifest.json` e `agents/openai.yaml` (metadados de hospedagem Codex/Cursor, sem função aqui).

### Alterações em `SKILL.md`
1. `description`: antigo `...HTML/CSS/JavaScript/React: pages, dashboards, prototypes, slide decks, animations, UI mockups, and data visualizations. Use for visual front-end creation, design-system exploration, design critique, or explicit browser acceptance / QA of a web artifact.` -> novo `...HTML/CSS/JavaScript: pages, dashboards, prototypes, animations, UI mockups, and data visualizations. Use for visual front-end creation and design-system exploration.` (saíram "slide decks", "design critique" e "browser acceptance / QA", como decidido; saiu também "/React", consequência da troca de pilha).
2. Abertura: `HTML/CSS/JavaScript/React` -> `HTML/CSS/JavaScript (plain, no framework)`.
3. Step 0: `ask the user. Don't guess.` -> `record it as "unverified" in decisoes.md and proceed without asserting it. Don't guess.` e acrescentada a frase: nada do hub é pesquisado na web e o passo não se aplica a nomes de peças do hub.
4. Step 1: título `(decide whether to ask based on context)` -> `(do not wait for answers: register assumptions)`; parágrafo novo: onde a tabela diz "ask", gravar a pergunta e a suposição adotada em `decisoes.md` e seguir. Linha "Make me something nice": `Switch to Design Direction Advisor` -> `Pick the most defensible direction from the brief, register it in decisoes.md and proceed`. Bloco "When the request is genuinely vague ... switch into Design Direction Advisor mode" -> "register the chosen direction and the reason in decisoes.md and proceed".
5. Step 2, itens 2 a 5: "proactively ask whether you can review them", "ask which brands or products", "read the single recipe file ... style-recipes", "switch to Design Direction Advisor ... pick a recipe" -> revisar se estiverem no projeto, escolher e registrar as referências, tratar a âncora como referência a analisar (sem biblioteca de receitas), registrar que não há referência.
6. Asset Protocol: `stop and ask the user, don't proceed with a colored rectangle` -> `register the gap in decisoes.md and use an honest "asset pending" placeholder, don't proceed with a colored rectangle`. Placeholder Philosophy: `Missing data -> proactively ask the user for it` -> registrar a lacuna e usar placeholder; `Missing logo -> stop and ask the user` -> registrar e usar placeholder honesto.
7. Step 3: `let the user confirm before proceeding` -> `register it in decisoes.md and proceed`; linha `Anchor / recipe (if any): ... style-recipes/linear.md` -> `Anchor (if any): [reference named in the brief, or "custom"]`; removido o parágrafo sobre colar valores de uma receita.
8. Checkpoint 1: `stop. Tell the user "I plan to use this system. Confirm and I'll start the v0." Then actually wait` -> `Decision 1: ... write the chosen system in decisoes.md (what you chose and why) and start the v0. Do not wait for confirmation.`
9. Checkpoint 2: `Push v0 to the user before continuing` -> `Decision 2: Save the v0 and write in decisoes.md the assumptions it carries, then continue the build. Do not wait for approval.` Step 5: `After v0 is approved` -> `After v0 is saved`.
10. Checkpoint 3: `pause and confirm again` -> `Decision 3: ... register the decision and the reason in decisoes.md and proceed`.
11. Step 6: parágrafo do harness de aceitação em navegador (com `references/browser-acceptance.md`) -> `Browser acceptance ... is not part of this copy: it belongs to the QA role.`
12. Seção inteira "Fallback: Design Direction Advisor" (gatilhos, mecanismo, biblioteca de escolas, "After the user picks") removida.
13. "Technical Specifications": a seção "React + Babel (Inline JSX)" com as três Hard Rules (`styles`, escopo do Babel, `scrollIntoView`) -> `HTML, CSS, SVG and plain JavaScript`: sem framework, sem build, sem CDN, servido localmente; a regra do `scrollIntoView` ficou.
14. File Management: `small JSX files` -> `small JS files`; a nota de templates agora lista só `slide engine, oklch color system, font recommendations`.
15. Variantes de animação: sai `React state`, `useTime` e Popmotion (CDN `unpkg`); ficam CSS, estado simples com setTimeout/rAF e helpers de tempo em JS puro. Aviso `Avoid Framer Motion / GSAP / Lottie unless explicitly requested` -> também Popmotion, sem bibliotecas externas.
16. Dashboards: `Chart.js ... or D3.js ... loaded via CDN` -> `Hand-written SVG and JavaScript (no Chart.js, D3 or CDN in this copy)`.
17. Tweaks Panel: removido `(see the reference implementation)`; "Interactive Prototypes": removido `(see references file)`.
18. Seção "Common CDN Resources" -> "External Resources": só CSS escrito à mão ou recursos guardados no projeto; sem CDN nem fontes remotas.
19. Checklist: removidos o item de React (`const styles`) e o item de aceitação executável; a frase "unless the user explicitly requested executable acceptance" saiu.
20. "Collaborating": `proactively ask for clarification` -> registrar a interpretação adotada em decisoes.md; `Honor checkpoints ... actually wait` -> `Register decisions: ... never announce a wait and then ignore it`. "Content Principles": `ask the user first` -> registrar a sugestão em decisoes.md. `the user can course-correct sooner` -> `the reviewers can course-correct sooner`.
21. Tabela "References Routing": removidas as linhas de browser-acceptance, design-directions, style-recipes e INDEX; a linha de advanced-patterns agora diz `Slide engine, oklch color system, font recommendations`.

### Alterações nas referências
- `references/advanced-patterns.md`: removidas as seções Device Simulation Frames, Tweaks Panel, Animation Timeline Engine, Design Canvas, Dark Mode Toggle e Data Visualization Templates (todas em React/JSX ou com CDN do Chart.js); o sumário foi refeito; o bloco `<link href="https://fonts.googleapis.com/...">` virou `Fonts must be stored inside the project (no hotlink to Google Fonts in this copy).` Ficam Responsive Slide Engine (JS puro), Color System Best Practices (oklch), Font Recommendations e Color x Font Pairing.
- `references/block-library.md`: removidas as 6 linhas da tabela que apontavam para as seções apagadas.
- `references/design-calibration.md`: `ask one focused question. Otherwise...` -> `register the chosen reading and the reason in decisoes.md and proceed. Otherwise...`.
- `references/redesign-protocol.md`: `ask one focused question` -> registrar o modo escolhido e o motivo em decisoes.md; `Ask for authorization when ... protected-contract change` -> registrar em decisoes.md e deixar o contrato intacto; a frase sobre `browser-acceptance.md` -> `Browser acceptance belongs to the QA role and is not part of this copy.`
- `references/critique-guide.md` e `references/failure-patterns.md`: sem alteração.

### Pontos a saber (nada contradiz a ficha)
- `design-calibration.md` menciona gerar imagens com `gpt-image-2` "quando disponível" no ramo opcional image-first; é uma sugestão, a skill não chama rede.
- `SKILL.md` Step 0 manda verificar fatos por pesquisa na web; a alteração 3 exclui o hub.
