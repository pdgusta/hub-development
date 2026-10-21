# Retomada da Brasa (construtora)

**Ticket 49** (`issues/49-par-novo-com-o-hub-ja-no-disco.md`), ramo `ticket-49`, worktree `C:/context-hub-wt/ticket-49`,
de `integracao` 7b6c406. Teste escrito e no commit a577265: `agents/code/test/49-par-novo-com-hub.test.ps1`
(`pwsh -NoProfile -File agents/code/test/49-par-novo-com-hub.test.ps1 -Saida <json>`; Docker, portas 5988/5989, ~25 min).
Casos 1-5 medidos às 14h35; relatório `etapas/relatorio-49-par-novo-com-hub.md`.
Estado (pausa, ~15h15): 49 juntado em integracao (e82dd85, até c3f2868; fecha o 50); a suíte do Rebite estava rodando. Relatório com a sequência final do par B. **Pendência:** o ee71863 (só o cabeçalho do teste: casos 3, 4 e 5 são medidas) ficou fora da junção; juntar em integracao com o Rebite (`git merge ticket-49`). Fora disso, nada meu no 49. Parada a pedido do maestro (o Gustavo fechou o note). Antes: o 45 (já juntado). O notebook do par B está fechado e sem nada rodando; só volta a rodar quando o Gustavo falar (Gustavo, 2026-10-18).

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

1. Ler `etapas/regras-da-construcao.md` inteiras, o ticket 49 e esta retomada.
2. Seguir o próximo passo do último comentário do ticket.

## Pausa do par A (2026-10-18 ~15h20, pedido do Gustavo: o notebook vai fechar)

Desativadas as tarefas `hub-sincronizador` e `hub-vigia` (Disable-ScheduledTask); o CLI do par A parado pelo
`Stop-Sincronizador` do kit (.env `C:\hub-transporte\armis00323.env`); o contêiner `hub-banco` parado (`docker stop`;
o volume fica). A suíte do Rebite já tinha terminado (sem trava). Ficaram de pé, sem mexer: os 3 `mcp-banco`
(8796-8798) e a busca (das sessões dos harnesses). Para religar:
`docker start hub-banco; Enable-ScheduledTask -TaskName hub-sincronizador; Enable-ScheduledTask -TaskName hub-vigia`
(o laço religa o CLI em até 1 min).
