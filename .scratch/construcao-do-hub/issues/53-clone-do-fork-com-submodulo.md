# 53: O clone do fork traz o submódulo do LiveSync

Type: task
Status: claimed
Etapa: conserto do 26 (achado na instalação do par B)
Blocked by: nenhum

**What to build:** Achado do maestro do par B em 2026-10-21 ~13h25 (`.scratch/context-hub/retomada-maestro-par-b.md`,
recados ao A). Clonar o fork do MCP do banco a partir do bundle não traz o submódulo `lib/livesync-commonlib`
(público, vrtmrz, fixado em f9f07e97). O passo 05 do kit cai em "build do fork falhou", e o erro real ("Could not
resolve ../lib/livesync-commonlib/...") some porque o `npm run build` do `mcp-banco.psm1` joga a saída fora. No B, o
conserto foi `git -C C:/Projetos/hub-mcp-banco submodule update --init`.

- [ ] roteiro (`.scratch/context-hub/instalacao-par-b.md`, passo 2) e guia (`agents/code/docs/instalacao.md` do hub):
  clone do fork com `--recurse-submodules`, ou `submodule update --init` logo depois
- [ ] o passo 05 confere o submódulo antes do build e, se o build falhar, mostra a saída do `npm run build`
- [ ] teste que falha antes (fork sem submódulo dá erro claro, não "build do fork falhou" sem detalhe)

## Comments

- 2026-10-24 (maestro do A): aberto a partir do recado do B. Sem dono ainda.
- 2026-10-24 (maestro do A): Gustavo: o maestro do B conserta. Dono: maestro do par B.
- 2026-10-24 11h19 (Malho, construtor do par B): claimed. Worktree `C:/context-hub-wt/ticket-53`, ramo `ticket-53` a partir do `main` (70a9f73).
- 2026-10-24 12h00 (Malho): pronto e revisado no ramo `ticket-53` (7e20bee, e4ba4b5), sem junção nem push. O passo 05 recusa o submódulo vazio antes de montar, com o `git -C "<fork>" submodule update --init`; a queda do `npm ci` ou do build traz a saída do npm. Guia §5 e roteiro do par B (sem commit) com `--recurse-submodules`. Teste do 53 (caso 5 do `mcp-banco-sem-docker.ps1`): 23/23. Suíte inteira: 364 passam, 13 falham, nenhuma nos arquivos do ramo (carga e caminhos da máquina A; ver relatório). Relatório: `etapas/relatorio-53-clone-do-fork-com-submodulo.md`.
