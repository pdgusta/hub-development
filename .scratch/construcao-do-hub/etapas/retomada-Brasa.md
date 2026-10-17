# Retomada da Brasa

Atualizada em 2026-10-17 ~08h. Papel: construtora. Regras em `etapas/regras-da-construcao.md`: leia inteiras, em
especial "Um trabalho pesado por vez" (a trava `etapas/trava-pesada.md` e a fila `etapas/fila-pesada.md`) e "Testes com
harness de verdade". Um subagente por vez (tarefa leve) e até três Haiku de esforço médio (só tarefa simples ou QA).
- Revisores: Fiel e Fielzinho, em dupla (o Fiel fecha). Integrador: Rebite. Maestro: `maestri ask "Claude Code" ...`.
- `maestri ask`: caminho com `/`, nunca `\`.

## Ticket 22 (proxy e kit de cliente): falta o Docker, os harnesses, o relatório e a revisão

- Ramo `ticket-22`, worktree `C:/context-hub-wt/ticket-22`, de `integracao` 9cc878b. Ponta `a31998d`, árvore limpa.
- Costuras aceitas pelo maestro (comentário no ticket 22). O (4) também: uma sessão de cada harness como cliente,
  depois do Docker verde, com modelos baratos, a trava e o aval de login.
- Fork do MCP do banco: worktree minha `C:/Projetos/hub-mcp-banco-wt/brasa-22`, destacada em `integracao` 34c3e50. A
  `integracao` do fork é do Rebite: não montar nada lá (maestro). O passo 05 faz o `npm ci` e o build nela: pesado, só
  com a trava.

### Feito (testes sem Docker verdes: `node --test agents/code/test/22-kit-cliente.test.mjs agents/code/test/22-proxy-sem-docker.test.mjs`, 4 passam)

- `agents/code/kit/cliente/ligar-cliente.ps1`: liga os três harnesses ao proxy.
  - Bearer pelas variáveis `HUB_PROXY_TOKEN_BUSCA`, `HUB_PROXY_TOKEN_BANCO` e `HUB_PROXY_TOKEN_BANCO_ESCRITA`; o
    `-Escrita` liga a terceira rota.
  - Contrato num bloco marcado em `CLAUDE.md`, `AGENTS.md` e `copilot-instructions.md`. Sem `-Contrato`, lê o
    `AGENTS.md` por `read_note` na rota de leitura.
  - `-Saida` gera o lançador `copilot-hub.cmd`, com `--allow-all-mcp-server-instructions`.
- `agents/code/kit/par/10-proxy.ps1` e `proxy/proxy.psm1`:
  - TBXark/mcp-proxy 1.1.0, com o SHA-256 do pacote e do exe fixos e o `tar` do System32;
  - config com `${VAR}` e `autoReconnect`; pronto = `/_readyz` 200 e cada rota dá 401 sem token;
  - gera a ponte do Desktop (`mcp-remote@0.14.3` com `--header-file`) e a pasta conectada em `<estado>/desktop/`;
  - `env/10.env.modelo` traz `HUB_PROXY_ADDR=127.0.0.1:8790`.
- O MCP falso do teste sem Docker é `agents/code/test/proxy/mcp-falso.mjs`: registra o Host e o Authorization que
  chegam. Medido: o Host que chega à busca é o endereço dela.
- Teste com Docker: `agents/code/test/22-proxy.test.ps1`.
  - Prova o par do 07, o passo 05, a busca real e o passo 10, e um cliente HTTP com os 4 critérios.
  - Mede o `instructions` e roda a ponte do Desktop por stdio, com o npm cache no ensaio.
  - Com `-Manter`, deixa a pilha de pé e grava `%TEMP%\hub-ensaio-22\cliente.json`.
- Ponta a ponta dos harnesses: `agents/code/test/ponta-a-ponta/22-cliente.test.mjs`, só com `HUB_HARNESS_REAL=1`.
  Usa a pilha de pé.
- Corredor `.local/corredor-22.ps1` (cópia em `etapas/logs/`):
  - sai se a trava estiver ocupada; piso de 2 GB; corta abaixo de 700 MB;
  - fases: Docker com `-Manter`, depois os harnesses, e no fim a descida por `.local/limpar-22.ps1`;
  - estado em `etapas/logs/22.status`; logs em `etapas/logs/22-docker.log` e `22-harness.log`.
- Relatório começado: `etapas/relatorio-22-proxy-e-kit-de-cliente.md` (tabela do Docker com FALTA).

### Próximo passo exato

1. **A vez na trava** (08h45). Ponta `806898d` (384 MB por CouchDB por `docker update`, combinado com a Vela; contar a ela o pico medido). Fila: a Vela (real do 18) está com a trava desde 08:28; eu no fim
   da fila (item 5). Quem soltar me avisa; ao soltar a minha, avisar quem o maestro disser (era a Vela).
   - 4 voltas hoje: (1) submódulo do fork não iniciado (feito); (2) sobra da 1ª, o `-Manter` não descia na falha
     (c95a265); (3) volume de dados que sobrou da minha limpeza à mão (`docker rm -f` não leva volume: usar também
     `docker volume rm` e `docker network rm` dos `hub-ensaio-22-*`); (4) CORTADA 08:26 (613 MB) na indexação da
     busca, com os pares e as 3 instâncias de pé.
   - Maestro (08h30): na minha vez, `wsl --shutdown` com a trava e `docker ps` vazio, e a busca indexa antes dos
     pares (feito em bfe6d6a). Se cortar de novo: avisar o maestro com os números; o 22 Docker vira item do Gustavo.
   - Lançar com o desligamento: `Start-Process pwsh -WindowStyle Hidden -ArgumentList '-NoProfile','-File','C:/context-hub-wt/ticket-22/.local/corredor-22.ps1','-Wsl'`.
   - Volta cortada deixa a pilha (sem `cliente.json`): limpar à mão os PIDs do `brasa-22\dist\main.js`, contêineres,
     volumes, redes e `%TEMP%\hub-ensaio-22`.
2. **Se a fase docker falhar:** ler `22-docker.log`, consertar e rodar de novo (`-SoDocker` só para o Docker).
3. **Com tudo verde:**
   - preencher a tabela e o achado do `instructions` no relatório;
   - conferir a evidência em `agents/code/test/ponta-a-ponta/evidencia-22/` (sem token nem pasta do usuário) e fazer o
     commit dela;
   - `git merge integracao` se andou, e os testes sem Docker de novo;
   - pedir a revisão ao Fiel: ramo `ticket-22`, relatório.

## Ticket 08: PASSA com ressalvas; com o Rebite para juntar (avisado ~07h55)

- Ponta `514db7a`. Parecer `etapas/parecer-08-Brasa.md`, seção Fechamento.
- A fatia 2 (51 e 201 MiB) virou item do Gustavo, por decisão do maestro: ela derruba a memória na subida dos pares.
  - Comando dela: o corredor `.local/fatias.ps1 -Fatias '1+2'`, que chama o teste por `-Command`.
- Ressalvas 1 a 6 no parecer, sem conserto.

## Armadilhas

- `pwsh -File x.ps1 -Fatias 1,2` entrega o número 12 a um `[int[]]`: usar `-Command "& 'x.ps1' -Fatias 1,2"`.
- O Docker roda no WSL (`vmmemWSL`), que cresce e não devolve a memória. O `wsl --shutdown` devolve, só com aval e sem
  ninguém usando Docker; o Docker Desktop religa em ~10 s.
- O `tar` no PATH do Git Bash é o do MSYS: usar `%SystemRoot%\System32\tar.exe`.
- No `node:test`, o `after` do ajudante `pasta-de-ensaio.mjs` roda antes do `after` do teste. Por isso, descer os
  processos no `finally` do teste.
- Python em heredoc com caminho do Windows estraga `\t`: usar o Edit e conferir com `grep -a -P '[\x00-\x08]'`.
- Vigia de status: casar só as linhas do corredor atual (um "SOLTOU" antigo no fim do arquivo enganou uma vez).
- Processo longo: em segundo plano e com registro; matar só o PID aberto por mim (`taskkill /T /F /PID`).
- `@($null).Count` é 1: conferir `$null -ne` antes de contar.

## Fechados antes

- Tickets 01, 29 e 07: juntados pelo Rebite.
- Ticket 08: passou; a junção está com o Rebite.
- A worktree do fork precisa do submódulo `lib/livesync-commonlib` (`git submodule update --init`); sem ele o build
  do passo 05 falha ("Could not resolve ../lib/livesync-commonlib"). Feito às 08h16.
