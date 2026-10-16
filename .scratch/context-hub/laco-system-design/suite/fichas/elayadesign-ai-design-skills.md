# elayadesign/ai-design-skills

- **URL:** https://github.com/elayadesign/ai-design-skills (branch padrão `main`; API lida no HEAD)
- **Licença:** MIT (arquivo `LICENSE`, "Copyright (c) 2026 Elaya"; API: `MIT`)
- **Estrelas:** 2722 (API, `stargazers_count`); 198 forks; 1 issue aberta; repositório público, não arquivado
- **Criado em:** 2026-07-29. **Último push:** 2026-07-29. **Última atualização (API, `updated_at`):** 2026-10-15T12:09:33Z
- **Conteúdo do repositório:** `README.md`, `LICENSE`, `.gitignore` e uma única skill em `skills/landing-page-design/` (só `SKILL.md`, sem referências nem scripts)
- **Repositório de terceiros citado no README para melhorar um site existente:** `elayadesign/redesign-skill` (https://github.com/elayadesign/redesign-skill), licença MIT, 264 estrelas, atualizado em 2026-10-14. Skill dentro dele: `skills/redesign-existing-projects/SKILL.md`. Ficha não feita, por estar fora do escopo deste repositório.

**Como instalar (literal do README):**

Claude Code:
```bash
mkdir -p .claude/skills
git clone https://github.com/elayadesign/ai-design-skills.git /tmp/ai-design-skills
cp -r /tmp/ai-design-skills/skills/<skill-name> .claude/skills/
```
Depois: "Then just ask, in plain language, for what that skill covers."

Cursor:
```bash
mkdir -p .cursor/rules
curl -o .cursor/rules/<skill-name>.md \
  https://raw.githubusercontent.com/elayadesign/ai-design-skills/main/skills/<skill-name>/SKILL.md
```
Ou colar o arquivo em **Settings → Rules for AI**.

Codex / Windsurf / outros: copiar o `SKILL.md` para o arquivo de regras do projeto (tabela do README: Codex `AGENTS.md`; Windsurf `.windsurfrules`; Cline `.clinerules`; genérico: colar no system prompt).

Claude.ai (sem terminal): baixar o `SKILL.md` e enviar a um Project, ou anexar ao chat e dizer "follow this."

---

## landing-page-design

- **caminho:** `skills/landing-page-design/` (arquivo `SKILL.md`, 16528 bytes)
- **description** (literal do frontmatter):
  > Complete system for building high converting landing pages: intake questions, page structure, layout selection, conversion copywriting, SEO, plus strict visual rules for typography, spacing, corner radius, backgrounds, hero layout, icons, and motion. Use this skill whenever building, editing, styling, reviewing, or writing copy for ANY landing page, marketing site, web UI, page section, component, or prototype, even when the user does not mention design, conversion, tokens, or a design system. Always consult it before choosing page sections, headlines, CTAs, fonts, font sizes, spacing values, border radii, background colors, icons, or transitions.

- **o que faz de verdade:**
  - Organiza a criação de landing page em duas partes: A (estratégia e estrutura, com perguntas de intake, ordem de 12 seções, escolha de um de quatro tipos de layout, regras de conversão, copy e SEO/AEO) e B (sistema visual rígido).
  - Parte B fixa valores: fontes permitidas (Geist, Manrope, Geist Mono, Poppins) e proibidas (Inter, Roboto, Arial etc.); escala de texto do Tailwind; 13 valores de espaçamento; raio aninhado (`raio externo − espaço`); fundos planos em paleta escura fechada; gradiente só no texto do título.
  - Traz regras de movimento (curva cúbica `cubic-bezier(0.32,0.72,0,1)`, nav "pill" com morph do hambúrguer, reveal com IntersectionObserver) e uma seção obrigatória de "tagline reveal" com palavras que se acendem ao scroll.
  - Lista anti-padrões de conteúdo (sem Lorem Ipsum, sem "Acme", sem números redondos, sem clichês como "Seamless") e o checklist final de estados e requisitos de entrega.

- **como trabalha:**
  1. Faz intake (perguntas de propósito, público, prova, restrições), em um lote só, e assume o que faltar com uma linha de aviso.
  2. Escolhe um layout (A classic, B long form, C conversão mínima, D comparação) e justifica.
  3. Monta a estrutura de 12 seções, com a ordem de build A6 (hero, benefícios, como funciona, prova, FAQ, CTA final), uma seção por vez.
  4. Aplica a Parte B a cada valor visual antes de escrever código.
  5. Entrega, antes do código, um pacote: outline, copy do hero, benefícios, passos, FAQ (6 a 12), SEO/AEO e recomendação de layout.
  - Referências e scripts: nenhum. O arquivo é único e autocontido. Cita a skill `redesign-existing-projects` (outro repositório) para sites já existentes e diz que ela "defers to this file for every concrete value".

- **precisa para rodar:** só texto. Nenhum script, pacote, MCP ou rede exigidos pela própria skill. As instruções pressupõem Tailwind (classes `text-*`, `rounded-*`, `ease-[...]`) e Framer Motion como opção.

- **riscos:**
  - Nenhum script, nenhuma escrita ou remoção de arquivo, nenhum acesso à rede pela skill.
  - Ponto de atenção (não é risco de segurança): a skill declara que "When a rule here conflicts with a framework default, this file wins" e que "When the user's explicit prompt conflicts with a rule, the user wins". Ou seja, sobrescreve padrões do framework, e cede ao pedido explícito do usuário. Também impõe regras muito opinativas que podem conflitar com o projeto (ex.: "No hyphens in text", proibição de itálico e de font-weight 900, paleta de fundo dark fechada, layout em `max-width: 680px`).
  - Instruções imperativas em tom de regra fixa ("Never", "Always consult it before..."), com a expressão "Always consult it" aplicada a qualquer componente ou página web, mesmo sem menção a design. Pode disparar em tarefas não relacionadas a landing page.

- **harness:** formato de skill com frontmatter YAML (`name`, `description`) para Claude Code (`.claude/skills/<skill-name>/`). A mesma skill é texto puro (Markdown) para Cursor (`.cursor/rules/*.md`), Codex (`AGENTS.md`), Windsurf (`.windsurfrules`), Cline (`.clinerules`), prompt de sistema genérico e Projects do Claude.ai. Nos formatos que não são skill, o frontmatter fica como texto no topo do arquivo.

- **serve para:** construir, revisar ou reestilizar landing pages e componentes web com estrutura de conversão e um sistema visual fechado.
