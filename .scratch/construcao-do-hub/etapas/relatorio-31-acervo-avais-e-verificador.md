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

## Ponta a ponta real (2026-10-17, trava pesada)

- 1ª rodada (01:58, ramo ticket-31 em b710f2d): **Claude falhou com achado sério**: a peça
  `maestro-papeis/redator.md` foi gravada. O hub de ensaio sai em CRLF (checkout no Windows) e o `old_string` do
  Edit veio em LF; o `trocar` das guardas (`hooks/guardas/guarda.mjs`, do 14) não casava, devolvia `final`
  undefined, e a guarda do acervo deixava passar ("a troca não casa: a ferramenta falha sozinha"); o Claude Code casa os
  dois e grava. Buraco do 14/20, não do 31. A prova do Codex do 20 (ramo ticket-20) também falhou, mas só na asserção:
  a guarda recusou as duas gravações (registro), e o `codex exec --json` não mostra a gravação recusada nem o motivo.
- Conserto 050fb14 (aval do maestro): o `trocar` casa o `old_string` em LF com o arquivo em CRLF, como o Claude
  Code; teste novo em 20-acervo (vermelho antes); 20-acervo e 14-guardas 57/57. A asserção do Codex passou a olhar o
  motivo no registro da guarda (Copilot segue pelo stdout). Comentário no ticket 14. `integracao` 57e85cf juntada
  (da4f8fe).
- 2ª rodada (02:09, HARNESSES=claude,codex, em da4f8fe): **verde nos dois** (2/2). Claude: a troca recusada esperando
  o verificador, com "que não o seu (claude-haiku-5-5)" lido do transcript real; o nome parecido pediu aval. Codex: as
  duas gravações recusadas apontando `agents/maestro/propostas/`; a proposta gravada. Login copiado
  (`.credentials.json` em CLAUDE_CONFIG_DIR; `auth.json` em CODEX_HOME de ensaio), apagado ao fim de cada sessão;
  hashes das pastas reais antes e depois iguais; nada de token na evidência. Evidência em
  `agents/code/test/ponta-a-ponta/evidencia-20/{claude,codex}/` e `hashes-claude-codex.json`
  (4e420a6).
- Rodada 3 do Fiel: PASSA (CRLF ok, 57/57), com ressalva do Fielzinho: o ask de nome parecido e o da tabela não criam pendência, então o aval aprovado nesses casos fica sem registro em agents/maestro/avais/ (critério 1). Levada ao maestro.
