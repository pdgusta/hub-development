# Retomada do Trilho (construtor), gravada em 2026-10-17 ~08h35 (São Paulo)

Leia antes: `etapas/regras-da-construcao.md` (inteiras), `etapas/fila-pesada.md`, os tickets 21 e 16, as costuras
`etapas/costuras-21-Trilho.md` e `etapas/costuras-16-Trilho.md`. Responda em pt-BR, frases curtas. Maestro =
"Claude Code"; revisor = "Fiel"; integrador = "Rebite"; construtores: Brasa, Vela, Cinzel.

## Agora (08:35)
### A. Ticket 21 (arquivar e cópia diária): claimed; código e testes leves prontos; falta o Docker
- Worktree `C:/context-hub-wt/ticket-21`, ramo `ticket-21`, HEAD 22abdd2 (de integracao 9cc878b + ticket-16).
  Relatório quase pronto: `etapas/relatorio-21-arquivar-e-copia.md` (pôr o EPERM nos Achados e o resultado do Docker).
- Feito: `agents/skills/arquivar/` (arquivar.mjs, SKILL.md), `agents/code/bin/{copia-diaria,conferir-cabeca,
  limpar-arquivo}.mjs`, `lib/cabeca.mjs` (verificar-hub usa), `trocarCampos` exportada de `lib/frontmatter.mjs`,
  `kit/par/env/10.env.modelo`. Testes: `node --test agents/code/test/21-*.test.mjs` (cabeça 4, cópia 4, limpar 1,
  arquivar 9) e os afetados 04, 05, 05-nova-iniciativa, 20, 07-kit-sem-docker (75/75 antes do último conserto).
- Docker 1ª rodada (08:05, `logs/trilho-21-docker-1.log`): **o rename da pasta deu EPERM** com o sincronizador
  rodando (um arquivo aberto por outro processo na pasta bloqueia o rename no Windows; `fs.watch` não bloqueia).
  Conserto 22abdd2: espera até 10 s; depois recusa "em uso por outro programa", sem mover (testes com um processo
  segurando um arquivo aberto 1,5 s e 15 s). Se o Docker der "em uso" de novo, o bloqueio é fixo do CLI: aí
  investigar o que ele segura (handle.exe? não instalar nada global) e pensar em parar/religar o sincronizador
  (cuidado: deleção com o CLI parado pode não propagar) ou copiar+apagar; perguntar ao maestro antes.
- Próximo: 2ª rodada `pwsh -NoProfile -File agents/code/test/21-arquivar.test.ps1` na minha vez da fila (depois do
  corredor do 22 da Brasa; ao soltar, avisar quem a fila disser). Verde: relatório, comentário no ticket 21, Fiel.
  Junção só com 08 e 16 resolvidos.

### B. Ticket 16 (vigia): o 08 foi juntado; ligar os cenários do 08 e pedir a rodada final ao Fiel
- Worktree `C:/context-hub-wt/ticket-16`, ramo `ticket-16`, HEAD 24ffb0b (integracao e98a891 junto: o 08 e o 15).
  `node --test agents/code/test/16-vigia.test.mjs` 12/12.
- Maestro (08:2x): ligar os cenários que dependiam do 08: **binário descartado na passada, acima de 200 MiB,
  sincronizador parado, laço** (e, pelo ticket: Config Doctor travado, gerador de exclusões a cada passada com código
  2 virando item com o caminho; decisão de 2026-10-16 20:38). O 08 trouxe: `kit/par/banco/laco.ps1`, mudanças no
  `banco.psm1` (+95), `test/banco/ensaio.psm1` (+53), retratos em `agents/code/test/banco/retrato/`
  (`binario-ramo-apagado.json`, `conflito-aberto.json`, `scheduler-docs-em-dia.json`, `scheduler-docs-parado.json`,
  README). Ler `etapas/relatorio-08-banco-limites.md` e o diff `git diff 3ab8898 24ffb0b -- agents/code/kit
  agents/code/test/banco` antes das costuras. Os retratos servem de dublê na suíte sem Docker.
- Depois: Docker do 16 (com `HUB_MCP_BANCO_DIR=C:/Projetos/hub-mcp-banco-wt/ticket-11` ou o fork na integração, se
  compilado) pela fila; relatório `etapas/relatorio-16-vigia.md`; rodada final do Fiel (parecer
  `etapas/parecer-16-Trilho.md`, leitura intermediária com 3 ressalvas já feitas); com o passa, o Rebite junta o 16 e o
  17 da Vela sai da espera.

### C. Ticket 15: passou no Fiel (parecer-15-Trilho.md); com o Rebite (integracao e2b7607 já tem a rodada 2).

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
