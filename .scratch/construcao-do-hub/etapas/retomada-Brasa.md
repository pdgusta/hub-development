# Retomada da Brasa (construtora)

**Ticket 45** (`issues/45-banco-entre-duas-maquinas.md`), ramo `ticket-45`, worktree `C:\context-hub-wt\ticket-45`,
de `integracao` dc514db; pronto para revisão em 02dabc4 (2026-10-17 ~22h45), esperando o Fiel. Relatório:
`etapas/relatorio-45-banco-entre-duas-maquinas.md`. Estado e próximo passo: o `## Comments` do ticket (fonte única). Combinado com o Cinzel
(46): `etapas/logs/46-combinado-brasa.md` (Brasa toca compose, 04-banco, banco.psm1, 04.env.modelo, gerador; o
gerador escreve HUB_PAR_ID; nada no instalar.ps1).

## Lições práticas

- `pwsh -File x.ps1 -Fatias 1,2` entrega 12 a um `[int[]]`: usar `pwsh -Command "& 'x.ps1' -Fatias 1,2"`.
- O Docker roda no WSL (`vmmemWSL`), que cresce e não devolve memória. `wsl --shutdown` só com aval.
- Limpeza à mão de pilha cortada: `docker rm -f` não leva volume; usar `docker volume rm` e `docker network rm`
  dos `hub-ensaio-*`, e matar só os PIDs abertos por você (`taskkill /T /F /PID`).
- O `tar` do PATH do Git Bash é o do MSYS: usar `%SystemRoot%\System32\tar.exe`.
- No `node:test`, o `after` do `pasta-de-ensaio.mjs` roda antes do `after` do teste: descer processos no `finally`.
- Python em heredoc com caminho do Windows estraga `\t`: usar o Edit.
- `@($null).Count` é 1.
- `maestri ask` espera a resposta: rodar em segundo plano.

## Como retomar

1. Ler `etapas/regras-da-construcao.md` inteiras, o ticket 45 e esta retomada.
2. Seguir o próximo passo do último comentário do ticket.
