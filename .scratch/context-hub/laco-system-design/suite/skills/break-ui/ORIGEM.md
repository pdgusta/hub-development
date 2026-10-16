# Origem: break-ui

- **Repositório:** https://github.com/emilkowalski/skills
- **Caminho no repositório:** `skills/break-ui`
- **Commit fixado:** `2d228630ba1446365f614a108cb8252f1feda202` (HEAD lido com `git ls-remote` em 2026-10-15; arquivos baixados com `curl` de `raw.githubusercontent.com/emilkowalski/skills/2d228630ba1446365f614a108cb8252f1feda202/...`)
- **Data da cópia:** 2026-10-15
- **Licença:** MIT, Copyright (c) 2026 Emil Kowalski. O `LICENSE` do repositório está nesta pasta.
- **Papel na suíte:** QA tester
- **Leitura:** inteiros.

## Alterações em relação ao original

Arquivos: `SKILL.md` (alterado) e `CATALOG.md` (sem alteração).

Alterações em `SKILL.md` (`description` intacta, sem a flag de invocação manual: o frontmatter nunca teve `disable-model-invocation`):
1. Hard Rule 4: `Gate it behind the dev environment or keep it inside a prototype route.` -> `Keep it only inside the copy of the piece (Hard Rule 7).`
2. Nova Hard Rule 7: `Run only on a copy. Copy the piece to qa/copia/ first and work there. The fixture and the toggle never enter the approved sample, and no file outside qa/copia/ is edited.`
3. Phase 3: as duas ramificações (`In a project with a dev server` com `?data=worst` ou rota; `No project / standalone component`) -> `A single self-contained HTML file in qa/copia/ with the component and both datasets inline. ... No dev server and no route inside the project.`
4. Phase 4: removidos `then at 320px and at the widest layout it supports` e o item `with browser zoom at 200%`; novo texto: `Widths (320, 768, 1280, 1920 px) and zoom are measured by medidas-da-peca, not here`. Ficam contêiner real, modo escuro e RTL.
5. Phase 6: `apply those fixes in the component` -> `apply those fixes in the copy in qa/copia/ (never in the approved sample)`.
6. Mantidos: Hard Rule 5 `Report before fixing` e a Phase 5 `Report and stop` (reporta e para antes de corrigir).
