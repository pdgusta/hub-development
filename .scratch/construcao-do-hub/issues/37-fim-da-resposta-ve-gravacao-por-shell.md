# 37: O fim da resposta vê a gravação feita pelo shell

Type: task
Status: claimed
Etapa: conserto do 18 (fora da sequência)
Blocked by: 18

**What to build:** Desde o conserto do 18 (Vela, e1c5eac), o fim da resposta cobra a nota de retomada só de quem gravou,
pela lista que o hook depois da ferramenta anota. Gravação feita pelo shell (o Bash do Codex, o powershell do Copilot,
o Bash do Claude) não entra nessa lista e escapa da cobrança. Rede: no fim da resposta, comparar o `mtime` dos arquivos
só dentro do `cwd` da sessão desde o início do turno; o que mudou fora da lista vira **aviso** ("gravou pelo shell em
<caminho>; a nota mudou?"), não devolução.

**Fonte:** ressalva 1 da rodada 2 do Fiel no 18 (`../etapas/parecer-18-Vela.md`); proposta da Vela.

**Blocked by:** 18 (Retomada: nota de sete campos, início e fim)

- [ ] arquivo gravado pelo shell dentro do `cwd` no turno gera o aviso, nos três harnesses
- [ ] arquivo fora do `cwd` ou de antes do turno não gera nada
- [ ] o que já está na lista segue como no 18; a suíte segue verde

## Comments

- 2026-10-17 09h05 (maestro, mandato): a ressalva 1 do 18 é aceita como está (o 18 junta assim) e a rede vira este
  ticket. Dono: o primeiro construtor livre.
- 2026-10-17 09:25 (Cinzel): peguei o 37 (`claimed`). Worktree `C:/context-hub-wt/ticket-37`, ramo `ticket-37` do `ticket-18` 31afe63. Costuras com a Vela (dona do núcleo) e o maestro: `../etapas/costuras-37-Cinzel.md`.

- 09:24 (maestro): com o Cinzel até 12h15 (ramo sobre o ticket-18).
