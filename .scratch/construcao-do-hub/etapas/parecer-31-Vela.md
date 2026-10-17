# Parecer do Fiel — ticket 31, acervo: avais, verificador escolhido e peça sumida (Vela)

## Rodada 1 — 2026-10-17 — ramo ticket-31 em cc8c852

Veredito: **volta**, por um conserto. Revisado pelo Fiel sozinho; leitura do Fielzinho fica para depois.

Conferido: integracao 5d84d76 ancestral; worktree limpo. Li o ticket 31, `aval.mjs`, o diff de `decidir.mjs`,
`guarda.mjs`, `verificar-mudanca.mjs`, o fragmento PostToolUse, `lib/vigia.mjs` e o `verificar-acervo.mjs`.
`node --test 20-acervo 27-fim-da-resposta`: 34/34. Sonda: Write de agente em `agents/maestro/avais/x.md` → deny.

### Conserto

1. **O agente pode forjar o parecer e pular o verificador.** O parecer mora em `.local/acervo/pareceres/<chave>.json`,
   e o campo `modelo` dele é o que a guarda confere. Nada impede o próprio agente de gravar esse arquivo:
   Write em `<hub>/.local/acervo/pareceres/abc.json` passa sem resposta (reproduzido pelo `guarda.mjs claude`). Com
   a chave que a própria recusa mostra, o agente grava um parecer com `modelo: sonnet` e chega ao aval sem verificador
   nenhum — o que o ticket 31 (2) quer impedir. Recusar gravação de agente em `.local/acervo/` (pareceres e
   pendentes), como já faz com `agents/maestro/avais/`; teste. O shell segue fora da guarda (já declarado).

### Ressalvas (não seguram)

- Sem transcript (modelo do maestro não identificado), a regra "não no mesmo modelo" não se aplica e o pedido de aval
  sai assim mesmo, dizendo "não identificado"; quem decide é o Gustavo, que vê a tela.
- "Aprovado pelo Gustavo" no registro é inferido (a ferramenta rodou depois do ask); em modo que aprova sozinho, o
  registro diria o mesmo.
- `lib/vigia.mjs`: `estado.json` ilegível vira `{}` e a gravação apaga os itens da vigia; dois escritores ao mesmo
  tempo usam o mesmo `.novo`.
- Suíte inteira e ponta a ponta do Claude pendentes da trava (a Vela manda os números).

## Rodada 2 — 2026-10-17 — ramo ticket-31 em b710f2d

Veredito: **passa**. Fiel sozinho (Fielzinho lê depois). `20-acervo`: 19/19; worktree limpo. Sonda: Write de agente em
`.local/acervo/pareceres/abc.json`, mesmo com `HUB_PAPEL=maestro` → deny. Ressalvas da rodada 1 seguem. Suíte inteira
e ponta a ponta do Claude pendentes da trava: se vierem com vermelho, a rodada reabre.

## Rodada 3 (código novo depois do passa) — 2026-10-17 — ramo ticket-31 em 4e420a6

Veredito: **passa com ressalva escrita** (3ª rodada, teto de voltas). Fiel e Fielzinho de acordo
(parecer-31-Vela-fielzinho.md).

Conferido pelo Fiel: diff b710f2d..050fb14 — `trocar` (`guardas/guarda.mjs`) casa o `old_string` em LF com a peça em
CRLF, como o Claude Code, e troca também em CRLF; teste novo no 20-acervo; a asserção do Codex na ponta a ponta olha o
registro da guarda. da4f8fe junta integracao 57e85cf. `20-acervo` + `14-guardas`: 57/57; worktree limpo. Evidência
real (4e420a6) do Claude e do Codex lida pelo Fielzinho: verde, hashes iguais, sem token.

### Ressalva (Fielzinho; aceita pelo Fiel) — conserto para um ticket seguinte

- **Aval sem parecer não é registrado.** O `ask` de nome parecido (`redator-2.md`) e o da tabela sem `HUB_PAPEL` não
  criam pendência nem parecer; o `aval.mjs` só registra quando os dois existem. Reproduzido pelo Fielzinho: `ask`,
  gravação aprovada, PostToolUse → nenhum arquivo em `agents/maestro/avais/`. O critério 1 pede registro de todo aval
  aprovado. Conserto: pendência para cada `ask` e registro do aval mesmo sem parecer (dizendo "sem verificador:
  dispensado"), sem inventar parecer.
