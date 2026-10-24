# Brief do ticket 57 (par B, lenovo-ideapad, 2026-10-24)

Para o **Malho**, construtor do par B. O Gustavo invocou `/implement 57` em 2026-10-24. **Quem te chama agora é o
terminal "Maestro"** no canvas (o maestro abre pelo preset "Maestro" desde o 48; não é mais "Claude Code"). Valem
todas as regras e as "Diferenças do par B" de `etapas/brief-53-par-b.md` (hub ao vivo só leitura, par rodando
intocado, sem junção nem push, retomada e 40%), com estas diferenças: **parta do `main` do hub (3e83b76)**, que já tem
o 48: `git -C C:/context-hub worktree add C:/context-hub-wt/ticket-57 -b ticket-57 main`; e o aviso final vai para
`maestri ask "Maestro" "57 pronto: ..."`.

## O trabalho

- Ticket: `C:/Projetos/context-hub/.scratch/construcao-do-hub/issues/57-skill-freellmapi.md`. Leia inteiro. A lista
  de caixas é o contrato; o que ela deixa à construção (o mecanismo que solta o processo da sessão, onde fica a
  configuração da máquina, o formato do PID e do log) você decide e registra no relatório, com a razão e a fonte.
- Contexto: `C:/Projetos/context-hub/.scratch/context-hub/retomada-maestro-par-b.md`, diário de 2026-10-24 desde
  16:39 (FreeLLMAPI nativo). O jeito de subir hoje está em `C:/freellmapi-data/iniciar.ps1` (leia; ele sai depois da
  junção). Fonte primária do servidor: o clone `C:/Projetos/freellmapi` na v0.11.0 (`Dockerfile`,
  `server/src/lib/config.ts`, `server/src/env.ts`, `server/src/db/index.ts`, `docs/en/install/01-install.md`).
- **Fonte primária antes do mecanismo:** como um processo sobrevive ao fim da sessão do Claude Code, do Codex e do
  Copilot no Windows (job objects, `detached` do Node, `Win32_Process.Create`). Doc externa por `curl` (versão `.md`
  quando houver), nunca subagente web-fetch. Marque "não verificado" o que não conferir.
- Peças do hub para ler e imitar: uma skill com script (`agents/skills/correio/`: `SKILL.md` com `metadata.camada:
  geral`, `correio.mjs`), o par da máquina (`HUB_PAR_ID` ou `.local/par.json`), o roteamento
  (`agents/skills/routing.yml`) e o kit (`kit/par/08-harnesses.mjs`, junction das skills gerais). SKILL.md com a skill
  `writing-for-agents`.

## Não toque

- **O FreeLLMAPI que está no ar** (PID 56572, porta 3001, `C:/freellmapi-data/`): nem parar, nem abrir o banco, nem
  chamar modelo. O A depende dele. Testes só com servidor falso numa porta livre e pastas de ensaio.
- Nenhuma chamada de modelo ao gateway; nenhuma chave em arquivo, log ou relatório.
- Tarefa agendada: nenhuma (é o pedido do Gustavo).

## Fora da construção (fica com o maestro)

- Parar o processo de hoje, ligar pela skill de verdade, conferir pelo A e apagar `C:/freellmapi-data/iniciar.ps1`.
  Deixe no relatório os comandos exatos.

## Como

Igual ao 48: `claimed` no ticket; `tdd`; arquivo de teste sozinho a cada passo; suíte inteira uma vez no fim;
`code-review` sobre o ramo (desde `main`); relatório em `etapas/relatorio-57-skill-freellmapi.md`; comentário no
ticket; `maestri ask "Maestro" "57 pronto: ..."`. Caminho Windows com barra invertida em comando de shell: o bash
desta ferramenta come o `\b` em `printf` e em heredoc de python; grave pelo Edit ou pelo PowerShell. Retomada em
`etapas/retomada-Malho.md`.
