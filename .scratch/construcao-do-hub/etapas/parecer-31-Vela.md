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
