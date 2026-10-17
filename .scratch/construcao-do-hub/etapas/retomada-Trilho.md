# Retomada do Trilho (construtor), gravada em 2026-10-17 ~05h40 (São Paulo)

Leia antes: `etapas/regras-da-construcao.md` (inteiras; regras novas: até um subagente leve e até três Haiku 5.5 para QA
simples; suíte inteira só na junção, pelo Rebite; fila do pesado em `etapas/fila-pesada.md`), o ticket 16 e o 15
(Comments), `etapas/costuras-16-Trilho.md`. Responda em pt-BR, frases curtas. Maestro = "Claude Code"; revisor =
"Fiel"; integrador = "Rebite"; outros construtores: Brasa (08), Vela (28), Cinzel (09, 10).

## Agora (07:00)
- 16: Docker 4ª rodada tudo passou (06:35). Fiel, leitura intermediária (`etapas/parecer-16-Trilho.md`): parte feita sem
  conserto; três ressalvas, todas feitas: trava por arquivo no estado.json (5709117), 401 vira "não conferida" com o
  código (5709117), uma cópia só no recuperar (5709117, recuperar.ps1 com -Revs/-Destinos separados por |).
  Juntado integracao 9cc878b (o 10): estado_do_hub real no 16-vigia.test.ps1 (3e29a85, MCP 8796-8798 pelo passo 05);
  fim-da-resposta pela lib como o hook grava (HEAD). Sem Docker 12/12.
- Próximo: na trava (depois do Rebite; ao soltar, avisar a Vela): Docker do 16 (5ª rodada: estado_do_hub real e o
  recuperar novo) e o Codex do 15. Depois, relatório e rodada do Fiel. Falta ainda o 08 (cenários e gerador).
- Achado: rodei por engano o 12-busca (pesado) sem trava às ~06h50 (filtro por "vigia"); 2 falhas lá, sem relação
  com o 16 (o 16 só mexe no texto do SKILL.md da busca). Dizer ao maestro.

## Fechados nesta sessão
12 (rodada 3, só a search nos três harnesses), 13, 33 e 35: juntados e resolvidos (integracao 33b817a).

## Em aberto
### A. Ticket 15: falta só o Codex de verdade (prioridade depois das 06:58)
- Worktree `C:/context-hub-wt/ticket-15`, ramo `ticket-15`. Claude e Copilot já passaram (evidência 7ad8dee). O
  Codex bateu no limite de uso ("try again at 6:58 AM").
- Pegar a trava pela fila (entra entre fatias da Brasa; ela solta se eu estiver esperando). Antes: `git merge
  integracao` no ramo (o 12 r3 já está lá; os cherry-picks 46e44d2/c1b6133 têm o mesmo conteúdo).
- `cd C:/context-hub-wt/ticket-15; HUB_HARNESS_REAL=1 HARNESSES=codex node --test --test-concurrency=1
  agents/code/test/ponta-a-ponta/15-leitura.test.mjs` (log em `etapas/logs/`). Conferir `evidencia-15/hashes-codex.json`
  (`apagado: true`, configs iguais; `.claude.json` muda pelas sessões abertas, só registro) e que não há chave na
  evidência. Commit só de evidência. Seção "Rodada de 2026-10-17" do `etapas/relatorio-15-aviso-de-leitura.md`.
  Rodada do Fiel do 15 (o que mudou: 46e44d2, c1b6133, 3bc8c8b e as evidências) e, depois do passa, o Rebite.

### B. Ticket 16: vigia (claimed; código feito, falta o ponta a ponta com Docker passar)
- Worktree `C:/context-hub-wt/ticket-16`, ramo `ticket-16`, de integracao 33b817a; HEAD ff0f362.
- Feito: `agents/skills/vigia/` (`vigia.mjs` com `passada` e `recuperar`, `notificar.ps1`, `recuperar.ps1` pela
  receita da Brasa, `SKILL.md`); `gravarPassada` em `agents/code/bin/lib/vigia.mjs` (itens da vigia com
  `fonte: 'vigia'`, `vistos`, `piorou`); kit: `HUB_VIGIA_LEITOR_DB` e `HUB_VIGIA_OUTRO_PAR_URL` no `04.env.modelo` e o
  leitor no `Install-ParBanco`. Conserto do 12 em commit separado b4e7272 (a skill da busca não cita a `read`): citar
  no relatório.
- Testes: `node --test agents/code/test/16-vigia.test.mjs` 8/8 (dublês HTTP, CLI falso em `agents/code/test/vigia/`).
  Ponta a ponta: `pwsh -NoProfile -File agents/code/test/16-vigia.test.ps1` (Docker, hub-ensaio-16-a/b, 5996/5997,
  pela fila; ao soltar a trava, avisar quem o maestro disser; limpar os contêineres).
- Primeira rodada do Docker (05h20): 6 falhas, todas consertadas em ff0f362, a rodar de novo:
  1. `HUB_OUTRO_PAR_URL` é o B visto de dentro do contêiner (host.docker.internal): a vigia usa
     `HUB_VIGIA_OUTRO_PAR_URL` (no teste, `$ensaio.B.Url`).
  2. `open_revs=all` responde em multipart sem `Accept: application/json` (vigia e teste consertados).
  3. A base da colisão não chegava ao B em 60 s: o hub inteiro ainda replicava; o teste espera o A→B antes.
  4. O JSON do `info` do CLI vem entre linhas de registro: a vigia pega o bloco de `{` a `}` em linhas próprias.
  5. "O daemon apagou o ramo perdedor" falhou, talvez só pelo item 2. Se falhar de novo, o teste forja fiel (receita da
     Brasa) e segue; dizer no relatório se foi forjado. A Brasa ainda não confirmou no Docker que o daemon apaga.
- Depois de verde: relatório `etapas/relatorio-16-vigia.md` (feito, achados acima, Docker, combinado com o Cinzel,
  conserto do 12, o que espera o 08 e o 10), comentário no ticket, revisão do Fiel, Rebite **só com 08 e 10 resolvidos**
  (o Rebite junta depois). Entram quando juntados: cenários do 08 (binário descartado na passada, 200 MiB, sincronizador
  parado, gerador de exclusões a cada passada, item `fim-da-resposta`) e o `estado_do_hub` real do 10 (Cinzel).

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
