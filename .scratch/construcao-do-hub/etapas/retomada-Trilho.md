# Retomada do Trilho (construtor), gravada em 2026-10-17 ~09h45 (São Paulo), antes da janela quieta da fatia 2

Leia antes: `etapas/regras-da-construcao.md` (inteiras), `etapas/fila-pesada.md`, os tickets 21 e 16, as costuras
`etapas/costuras-21-Trilho.md` e `etapas/costuras-16-Trilho.md`. Responda em pt-BR, frases curtas. Maestro =
"Claude Code"; revisor = "Fiel"; integrador = "Rebite"; construtores: Brasa, Vela, Cinzel.

## Agora (09:45) — sem trava minha; nenhum contêiner nem pasta de ensaio minha sobrando
### A. Ticket 16 (vigia): PASSOU no Fiel (rodada 2, 0332466); entregue ao Rebite
- Ramo `ticket-16`, HEAD 0332466 (integracao e98a891 junta). 19/19; Docker 8ª tudo passou (`logs/trilho-16-docker-8.log`).
- Maestro reenviou ao Rebite depois do reinício do Maestri (o 1º aviso caiu). Antes: o terminal dele respondeu só com o prompt do PowerShell (Claude dele talvez
  fechado na janela quieta). **Ao voltar: `maestri check "Rebite"`; se não chegou, reenviar** o aviso (ramo, 19/19,
  Docker 8ª, relatório `etapas/relatorio-16-vigia.md`, parecer `etapas/parecer-16-Trilho.md`, HUB_MCP_BANCO_DIR =
  `C:/Projetos/hub-mcp-banco-wt/ticket-11`).
### B. Ticket 21: Fiel r1 VOLTA (2 consertos), feitos em f32bd4c; HEAD 5fe3fda (com integracao fce0529)
- Próximo: Docker 4ª rodada na fila 1b (depois da suíte do Rebite, antes das 12h15) para logs/trilho-21-docker-4.log;
  ao soltar, avisar o MAESTRO; verde: pedir a rodada 2 ao Fiel (o Fielzinho lê depois das 12h15).
### B-antes. (Docker 3ª tudo passou; revisão r1 pedida ~10h)
- Worktree `C:/context-hub-wt/ticket-21`, ramo `ticket-21`, HEAD 1c87f9b (9ce2496 + merge do ticket-16 0332466).
- Testes: 21-* e afetados (04, 05, 20, 07-kit-sem-docker) 78/78; Docker `logs/trilho-21-docker-3.log` 9 PASSA.
- Relatório `etapas/relatorio-21-arquivar-e-copia.md` em dia (Achado 3: EPERM pelo fs.watch numa subpasta; arquivo
  por arquivo; estado parcial visível no outro par, fim consistente).
- **Próximo:** `maestri ask "Fiel" "Trilho: ticket 21 pronto para revisão no ramo ticket-21 (1c87f9b), relatório
  etapas/relatorio-21-arquivar-e-copia.md"`. Junção só depois do 16 juntado (`git merge integracao` no 21 então,
  testes leves de novo).
- Comentário no ticket 21: falta registrar o Docker 3ª verde e o pedido ao Fiel.

## Para o maestro (achados soltos)
- Em %TEMP% sobram ~540 `hub-ensaio-27-*` e ~30 `hub-ensaio-20-*` (não são minhas; os testes do 20 e do 27 não limpam).

## Fechados
16 (passou no Fiel, com o Rebite). 12, 13, 33, 35 (juntados). 15 passou no Fiel (3d34bd1), com o Rebite.

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
