# Origem: emil-prototype

- **Repositório:** https://github.com/emilkowalski/skills
- **Caminho no repositório:** `skills/prototype`
- **Commit fixado:** `2d228630ba1446365f614a108cb8252f1feda202` (HEAD lido com `git ls-remote` em 2026-10-15; arquivos baixados com `curl` de `raw.githubusercontent.com/emilkowalski/skills/2d228630ba1446365f614a108cb8252f1feda202/...`)
- **Data da cópia:** 2026-10-15
- **Licença:** MIT, Copyright (c) 2026 Emil Kowalski. O `LICENSE` do repositório está nesta pasta.
- **Papel na suíte:** UI engineer (invocação manual: /emil-prototype ...)
- **Leitura:** inteiros.

## Alterações em relação ao original

Arquivos: `SKILL.md` e `PICKER.md` (este sem alteração).

Alterações em `SKILL.md`:
1. Frontmatter `name: prototype` -> `name: emil-prototype` (colisão com a skill pessoal `~/.claude/skills/prototype`). Pasta renomeada do mesmo modo. `description` intacta. **Mantida** a marca `disable-model-invocation: true` (invocação só manual).
2. Hard Rule 5: `Clean up after the choice. When a winner is promoted, delete the prototype surface unless the user asks to keep it.` -> `Never delete a sample without being asked. When a winner is promoted, the prototype surface stays; delete it only if the user asks.`
3. Phase 4: as duas ramificações (`In a project with a dev server` com rota isolada; `No project / static context`) -> `One branch only: a single self-contained HTML file (inline CSS/JS) saved in amostras/ ... No dev server and no route inside a project.`
4. Phase 2: `skip to the standalone branch in Phase 4 and choose a restrained default look` -> `choose a restrained default look` (a ramificação única já é a standalone).
5. Phase 6: `then delete the prototype surface per Hard Rule 5` -> `the prototype surface stays (Hard Rule 5)`.
6. Tabela "Invocation Variants": `keep <variant>` perde `and delete the prototype surface` (agora `the prototype surface stays`); removida a linha `keep <variant>, leave the picker` (redundante).

Mantido como está (não mudei por não constar da decisão): na Phase 5 a skill apresenta o conjunto e "para: a escolha é do usuário"; a mensagem inicial ("I'm ready to build several genuinely different versions...") também fica.
