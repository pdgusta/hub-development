# Retomada do Trilho (construtor)

**2026-10-17 ~20h45: construção fechada; nada pendente do Trilho.** Todos os tickets resolvidos, menos o 26
(instalação de verdade, com o Gustavo). `integracao` em ca62332 (suíte 370: 355 verdes, 15 pulados, 0 falhas).
Tickets dele (12, 13, 15, 16, 21, 33, 35, 38, 39, 41) resolvidos. Sem trava, contêiner ou pasta de ensaio dele.
As worktrees `C:/context-hub-wt/ticket-38`, `-39`, `-41` ainda existem (limpeza é do maestro).

## Decisões que valem (para quem mexer na vigia ou na busca)

- Vigia: piora = item sobe de nível em relação à passada anterior; item novo conta como `ok`; desce e volta a subir
  notifica de novo (maestro, ticket 16).
- `estado_do_hub` (10) devolve o JSON e o aviso "a vigia não roda desde <hora>" com passada de mais de 15 min.
- Só a `search` do hub-busca nos três harnesses (12 r3).
- O 41 tirou `agents/code/**` da busca.

## Lições práticas

- No Codex, o nome MCP com hífen chega ao hook com sublinhado (`mcp__hub_busca__search`).
- `HUB_ROOT`/`TEMP` em nome curto (`GUSTAV~1.DEL`) faz o `fs.watch` abortar (libuv `fs-event.c`): usar caminho longo.
- `description` de `SKILL.md` com `: ` solto quebra o YAML e o `12-busca`: quem muda `SKILL.md` roda o `12-busca`.
- Guarda de segredo: comando com o texto `.env` em padrão de grep é recusado inteiro.
- Barra invertida some em heredoc do bash/python (barra-zero vira NUL, barra-t vira tabulação): usar o Edit, ou
  `chr(92)`; conferir com `cat -A`.
- Dublê HTTP no próprio processo do teste: chamar a vigia com `execFile` (assíncrono), nunca `spawnSync`.
- No Windows, `process.exit` logo depois de um `fetch` derruba o node (UV_HANDLE_CLOSING): usar `process.exitCode`.
- Template literal com barra-n em código passado por `-e` vira quebra de linha e o filho não compila.
- Filtro de testes por palavra pode puxar teste pesado (12-busca): rodar os arquivos pelo nome.
- O fork padrão `C:/Projetos/hub-mcp-banco` não tem o `estado_do_hub`: Docker da vigia usa `HUB_MCP_BANCO_DIR`.
- `maestri ask` para recruta ocupado fica na fila dele: conferir com `maestri check`.

## Como retomar

1. Ler `etapas/regras-da-construcao.md` (inteiras).
2. Aguardar ordem do maestro (`maestri ask "Claude Code" ...`, caminhos com `/`). Não pegar ticket nem trava por conta.
3. O histórico mora nos tickets, relatórios, pareceres e no git.
