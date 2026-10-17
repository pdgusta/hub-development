# 35: Todo aval aprovado é registrado, também sem parecer

Type: task
Status: claimed
Etapa: conserto do 31 (fora da sequência)
Blocked by: 31

**What to build:** O critério 1 do 31 pede registro de todo aval aprovado em `agents/maestro/avais/`. Hoje o `ask` de
nome parecido (por exemplo `redator-2.md`) e o da tabela de roteamento sem `HUB_PAPEL` não criam pendência nem parecer,
e o `aval.mjs` só registra quando os dois existem: um aval aprovado nesses casos não deixa arquivo (reproduzido pelo
Fielzinho: `ask`, gravação aprovada, PostToolUse, nenhum arquivo). Conserto: pendência para cada `ask` da guarda do
acervo e registro do aval mesmo sem parecer, dizendo "sem verificador: dispensado", sem inventar parecer.

**Fonte:** `../etapas/parecer-31-Vela.md` (rodada 3, "Ressalva (Fielzinho; aceita pelo Fiel)"). Ticket 31 e a
decisão do Gustavo das três lacunas do acervo (rodada `2026-10-16-acervo-do-maestro-tres-lacunas`). Regras comuns:
`../etapas/regras-da-construcao.md`.

**Blocked by:** 31 (Acervo: registro dos avais, verificador e peça que sumiu)

- [ ] `ask` de nome parecido aprovado: nasce o registro em `agents/maestro/avais/` com "sem verificador: dispensado"
- [ ] `ask` da tabela de roteamento sem `HUB_PAPEL` aprovado: idem
- [ ] os casos com parecer seguem como no 31; a suíte segue verde

## Comments

- 2026-10-17 ~02h25 (maestro): publicado pela ressalva do 31 (Fielzinho, aceita pelo Fiel), como o 30 e o 34. Dono: o
  Trilho, enquanto espera a trava para o Codex do 12 e do 15 (a Vela está no 34).
- 2026-10-17 ~02h30 (Trilho): pego (claimed). Worktree C:/context-hub-wt/ticket-35, ramo ticket-35, de integracao 236b3ef.
