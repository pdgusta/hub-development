# Relatório do ticket 31: registro dos avais, verificador escolhido pelo maestro e peça que sumiu

Construtora: Vela. Ramo `ticket-31`, worktree `C:\context-hub-wt\ticket-31`, de `integracao` 5d84d76. 2026-10-17.
Fonte: rodada `2026-10-16-acervo-do-maestro-tres-lacunas` (Gustavo, 1 A, 2 B, 3 A).

## O que mudou

### 1. Modelo do verificador (9cb5ac6, 68deed6)

- `agents/code/hooks/acervo/verificar-mudanca.mjs` exige `--modelo <modelo>` (sem ele, sai 1 e diz como). Roda
  `claude -p --model <modelo>`; nos testes, o comando de `HUB_VERIFICADOR`, que recebe `HUB_VERIFICADOR_MODELO`. O
  parecer grava `modelo`. Saiu o Sonnet fixo do 20. O modelo só aceita letras, números, `.`, `:`, `-`, `[`, `]`
  (vai numa linha de shell).
- A guarda (`guarda.mjs`) lê o modelo do maestro no transcript da sessão (`transcript_path` do evento do Claude Code:
  a última linha `type: assistant` com `message.model`; lê só os últimos 512 KiB). Escolhi o transcript porque a doc
  do Claude Code (hooks, SessionStart input) diz que o `model` do SessionStart "pode faltar, por exemplo depois de
  /clear", e o `/model` troca no meio da sessão.
- `decidir.mjs`: a recusa traz o comando com `--modelo <um modelo diferente do seu (modelo do maestro)>`. Parecer sem
  `modelo` (forma do 20) volta a pedir o verificador. Parecer no mesmo modelo do maestro: recusa ("mesmo modelo do
  maestro"). "Mesmo modelo": mesma família (opus, sonnet, haiku, fable) ou o mesmo nome quando a família não aparece.
  Num modelo diferente: o pedido de aval mostra "Modelos: verificador em X, maestro em Y" e "Recomendação do
  verificador (X)".
- Modelo do maestro não identificado (sem transcript): o pedido de aval segue, dizendo "modelo não identificado".
  Decisão minha; não recusa porque não há como o maestro consertar isso.

### 2. Registro do aval (53c3ac7)

- `agents/code/hooks/acervo/aval.mjs`, ligado no `PostToolUse` do fragmento do Claude Code (`Write|Edit|MultiEdit`).
  A ferramenta só roda depois que o Gustavo aprova o `ask`; aí, se o arquivo ficou igual à mudança que o verificador
  viu (a mesma chave do 20, sobre o arquivo gravado), nasce `agents/maestro/avais/AAAA-MM-DD--<skill>-<peça>.md`
  (`--<skill>` quando a peça é o `SKILL.md`; `-2`, `-3` se repetir no dia): frontmatter comum, decisão (aprovado,
  com a hora), modelo do verificador, modelo do maestro, quem é afetado (o registro de uso), o relatório, o antes e o
  depois em blocos de código. O parecer e a pendência saem (servem a um aval só). Gravação troca atômica.
- Aval recusado: nenhum hook do Claude Code avisa da recusa de um `ask` (o `PermissionDenied` é só do modo auto), então
  fica sem registro. O ticket pede só o aprovado.
- `decidir.mjs`: gravação de agente em `agents/maestro/avais/` é recusada nos três harnesses, mesmo com
  `HUB_PAPEL=maestro`. A pasta nasce no esqueleto (`agents/maestro/avais/.gitkeep`) e replica.

### 3. Peça que sumiu (565c87e)

- `agents/code/bin/verificar-acervo.mjs`: as faltas "cita X, que não existe" (peça ou skill `maestro-*`) viram o item
  `acervo-peca-sumida`, nível `informa`, no `.local/vigia/estado.json`; com a peça de volta, o item sai; sem estado e
  sem falta, não cria o arquivo. Nível `informa` como o item do fim da resposta (27) e o da cópia diária (spec); a
  vigia notifica quando o estado piora.
- `agents/code/bin/lib/vigia.mjs`: `gravarItem` e `tirarItem` (troca atômica, sem apagar os outros itens, topo igual
  ao pior). O núcleo do fim da resposta (27) passou a usá-la. Mudança de comportamento pequena: quando o topo muda, o
  resumo do topo é o do primeiro item no pior nível (antes, o do item que acabou de entrar).

### Peças do acervo (cc8c852)

- `maestro-harnesses/guarda-do-acervo.md` e `maestro-acervo/SKILL.md` contam o verificador escolhido, os avais e a
  peça sumida.

## Testes

- `agents/code/test/20-acervo.test.mjs`, seção "ticket 31" (5 testes novos, pelas linhas de comando e pelos hooks):
  modelo (sem `--modelo` falha; mesmo modelo recusa; outro modelo pede aval e mostra os dois); aval aprovado grava o
  registro, que passa no `verificar-frontmatter`; sem parecer, nada; avais recusados nos três harnesses; peça sumida
  vira item sem apagar os outros e sai quando volta; sem estado, não cria. O teste do 20 do verificador passou a dar
  `--modelo`. 20-acervo 18/18; com o 27-fim-da-resposta, 34/34.
- Ponta a ponta do 20 (`ponta-a-ponta/20-acervo.test.mjs`): confere que a recusa do Claude real traz o modelo lido do
  transcript real (haiku). Rodada: ver abaixo.
- O que não dá para provar com harness real: a aprovação do `ask`. No `-p`, o Claude Code trata o `ask` como recusa
  (doc dos hooks, `permissionDecisionReason`). O registro do aval está provado com o evento `PostToolUse` na forma da
  doc; a prova com o Gustavo clicando fica para quando ele quiser.

## Resultados

- Rodada 1 do Fiel: volta, um conserto. b710f2d: a guarda recusa gravação de agente em `.local/acervo/` (pendências e
  pareceres), nos três harnesses, mesmo com `HUB_PAPEL=maestro`; o agente não forja mais o parecer. Teste novo.
  20-acervo 19/19. Limite de sempre da guarda: ela vê `Write`/`Edit` (e o `apply_patch`, o `create`/`edit`); um
  comando de shell que grave ali não passa por ela.
