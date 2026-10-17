# 35: Todo aval aprovado é registrado, também sem parecer

Type: task
Status: resolved
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
- 2026-10-17 ~02h35 (Trilho): 140417a, d65b18a, 0b01cd9. Teste do acervo 21/21. Falta: suíte comum (trava), revisão. Relatório etapas/relatorio-35-avais.md.
- 2026-10-17 ~04h40 (Trilho): Fiel PASSA (etapas/parecer-35-Trilho.md). Passado ao Rebite.
- 2026-10-17 04h53 (integrador, Rebite): juntado em `integracao`, commit ef38e4d (merge `--no-ff` de `ticket-35` ebae5ca, o HEAD da rodada 1 "passa" do Fiel; o ramo partia de 3c24d68, sem arquivo em comum). Testes, com a trava, junto com o 33 (33b817a): `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis = 199, 191 verdes, 8 pulados, 0 falhas (16 min); `git status` limpo. Ressalva do parecer: a pendência de um `ask` recusado fica; se o mesmo texto exato for gravado depois por um caminho sem aval, vira registro "aprovado" (igual ao 31 com parecer). A leitura do Fielzinho ficou pendente. **Resolvido.**
