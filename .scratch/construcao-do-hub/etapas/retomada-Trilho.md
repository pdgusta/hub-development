# Retomada do Trilho (construtor), gravada em 2026-10-17 ~09h50 (São Paulo)

Leia antes: `etapas/regras-da-construcao.md` (inteiras), `etapas/fila-pesada.md`, os tickets 21 e 16, as costuras
`etapas/costuras-21-Trilho.md` e `etapas/costuras-16-Trilho.md`. Responda em pt-BR, frases curtas. Maestro =
"Claude Code"; revisor = "Fiel"; integrador = "Rebite"; construtores: Brasa, Vela, Cinzel.

## Agora (09:50)
### A. Ticket 16 (vigia): com o Fiel, rodada final 2 (conserto 0332466)
- Worktree `C:/context-hub-wt/ticket-16`, ramo `ticket-16`, HEAD 0332466 (integracao e98a891 junta). 19/19
  (`node --test agents/code/test/16-vigia.test.mjs`, ~5 min; não editar a skill com a suíte rodando). Docker 8ª
  rodada tudo passou (`logs/trilho-16-docker-8.log`, 280b778; o conserto 0332466 só filtra texto, sem Docker de novo).
- Rodada final do Fiel (parecer-16-Trilho.md): VOLTA por 1: texto resolvido virava binário descartado; feito
  (isPlainText + .canvas). Pedido de nova leitura enviado ~09h48.
- Com o passa: `maestri ask "Rebite" "Trilho: ticket 16 passou ..."` (ramo, testes 19/19 e Docker 8ª, relatório
  `etapas/relatorio-16-vigia.md`, parecer `etapas/parecer-16-Trilho.md`). Junta o 16; o 17 da Vela sai da espera.
### B. Ticket 21: conserto do EPERM 9ce2496; na fila (item 1) para a 3ª rodada do Docker
- Worktree `C:/context-hub-wt/ticket-21`, ramo `ticket-21`, HEAD 9ce2496 (tem o ticket-16 só até 81b4a3d).
- Causa provada: fs.watch do chokidar numa SUBPASTA bloqueia o rename da pasta-mãe no Windows. Conserto: rename;
  com EPERM, arquivo por arquivo e rmdir da árvore velha; arquivo aberto por editor (sem partilha de apagar): devolve
  e recusa. `21-arquivar.test.mjs` 10/10. Relatório atualizado (Achado 3; maestro pediu: estado parcial visível no
  outro par durante a mudança, fim consistente).
- Próximo: na vez (Brasa tem a trava, 09:16), `git merge ticket-16` no 21 se o 16 passou (ou integracao, se o 16 já
  foi juntado), testes leves 21-* e afetados, Docker `pwsh -NoProfile -File agents/code/test/21-arquivar.test.ps1`
  > `etapas/logs/trilho-21-docker-3.log` (nome novo! não sobrescrever). Soltar a trava e avisar quem a fila disser.
  Verde: relatório, comentário no 21, Fiel.

## Fechados
12, 13, 33, 35 (juntados). 15 passou no Fiel (3d34bd1), com o Rebite.

## Decisões desta sessão
- Piora = item sobe de nível em relação à passada anterior; item novo conta como `ok`; desce e volta a subir notifica
  de novo (maestro, no ticket 16).
- Estado velho: o `estado_do_hub` (Cinzel, 10) devolve o JSON e o aviso "a vigia não roda desde <hora>" com passada de
  mais de 15 min; tira `vistos`.
- Só a `search` do hub-busca nos três harnesses (12 r3, opção A do maestro).

## Armadilhas
- Guarda de segredo: comando com o texto `.env` em padrão de grep é recusado inteiro (heredoc junto se perde).
- Barra invertida some em heredoc do bash/python: use o Edit para trechos com `\`.
- `maestri ask` para recruta ocupado fica na fila dele: conferir com `maestri check`.
- Dublê HTTP no próprio processo do teste: chamar a vigia com `execFile` (assíncrono), nunca `spawnSync`.
- Write num arquivo existente exige Read antes.
- Python em heredoc come barras invertidas (barra-zero vira NUL, barra-t vira tabulação). Trecho com barra invertida: Edit, ou chr(92); depois cat -A para conferir.
- No Windows, `process.exit` logo depois de um `fetch` derruba o node (UV_HANDLE_CLOSING): use `process.exitCode`.
- No Codex, o nome MCP com hífen chega ao hook com sublinhado (`mcp__hub_busca__search`).
- O fork padrão `C:/Projetos/hub-mcp-banco` não tem o `estado_do_hub`: o Docker do 16 usa `HUB_MCP_BANCO_DIR`.
- Template literal com barra-n dentro de código passado por -e: vira quebra de linha e o filho não compila (o teste trava).
- Filtro de testes por palavra pode puxar teste pesado (12-busca): rode os arquivos pelo nome.
