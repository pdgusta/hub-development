# Retomada da Brasa (construtora)

**2026-10-17 ~20h45: construção fechada; nada pendente da Brasa.** Todos os tickets resolvidos, menos o 26 (instalação
de verdade, com o Gustavo). `integracao` em ca62332 (suíte 370: 355 verdes, 15 pulados, 0 falhas). Tickets dela
(01, 07, 08, 22, 29, 42, 43, 44) resolvidos. Sem trava, Docker ou pasta de ensaio dela de pé.

## Ressalvas que um próximo trabalho precisa saber

- **22, evidência do Codex:** o `lido.json` de `agents/code/test/ponta-a-ponta/evidencia-22/codex/` não grava o
  modelo (ressalva do Fiel, para o radar: pôr `MODELO_CODEX` nele). Conferido em ca62332: ainda sem o modelo.
- **08:** PASSA com as ressalvas 3 a 6 do `etapas/parecer-08-Brasa.md`, sem conserto.
- **42:** a prova do realPath pela junction de verdade só o Claude real mostra (ressalva do Fiel).
- **Par novo leva minutos para receber o hub:** logo depois da subida dos pares, o daemon do B escreve a semente
  inteira (~523 arquivos, ~1 arquivo/s, ~6,5 min) e uma nota nova entra na mesma fila. Diagnóstico em
  `etapas/diagnostico-25-nota-nao-desce.md`; o 25 já espera o B convergir (fc6b10c).

## Lições práticas

- `pwsh -File x.ps1 -Fatias 1,2` entrega 12 a um `[int[]]`: usar `pwsh -Command "& 'x.ps1' -Fatias 1,2"`.
- O Docker roda no WSL (`vmmemWSL`), que cresce e não devolve memória. `wsl --shutdown` devolve, só com aval e sem
  ninguém usando Docker. Docker Desktop à mão: `Start-Process "$env:LOCALAPPDATA/Programs/DockerDesktop/Docker Desktop.exe"`.
- Limpeza à mão de pilha cortada: `docker rm -f` não leva volume; usar também `docker volume rm` e `docker network rm`
  dos `hub-ensaio-*`, e matar só os PIDs abertos por você (`taskkill /T /F /PID`).
- O `tar` do PATH do Git Bash é o do MSYS: usar `%SystemRoot%\System32\tar.exe`.
- A worktree do fork do MCP precisa do submódulo `lib/livesync-commonlib` (`git submodule update --init`), senão o
  build falha ("Could not resolve ../lib/livesync-commonlib").
- No `node:test`, o `after` do ajudante `pasta-de-ensaio.mjs` roda antes do `after` do teste: descer os processos no
  `finally` do teste.
- Python em heredoc com caminho do Windows estraga `\t`: usar o Edit e conferir com `grep -a -P '[\x00-\x08]'`.
- Vigia de status: casar só as linhas do processo atual (um "SOLTOU" antigo no fim do arquivo já enganou).
- `@($null).Count` é 1: conferir `$null -ne` antes de contar.
- Medidor de memória: `etapas/logs/medidor-brasa.ps1 -Saida <log> -Parar <arquivo>` (para quando o arquivo existe).

## Como retomar

1. Ler `etapas/regras-da-construcao.md` (inteiras; Codex só para testes, revisão do Fiel com subagente Opus).
2. Aguardar ordem do maestro (`maestri ask "Claude Code" ...`, caminhos com `/`). Não pegar ticket nem trava por conta.
3. O histórico mora nos tickets, relatórios, pareceres e no git.
