# Revisão em dupla: Fiel e Fielzinho (desde 2026-10-16)

O Gustavo pôs um segundo revisor ao lado do Fiel: o **Fielzinho** (Codex GPT 6-Astra, esforço médio, acesso total).
Desde 2026-10-16 ~20h o **Fiel** é um Claude Opus 5.5 médio (era Codex GPT 6.1 Sol; o Gustavo trocou), e o estado das
revisões dele fica em `etapas/estado-revisor.md`. Os dois cooperam em cada ticket. Duas leituras independentes, de
modelos diferentes, pegam mais do que uma. Regras comuns da construção:
`regras-da-construcao.md`; valem para os dois.

## Fluxo de cada ticket

1. O construtor pede a revisão ao **Fiel**, como antes. O Fiel repassa ao Fielzinho na hora, com o mesmo pedido
   (ramo, relatório, ticket): `maestri ask "Fielzinho" "<etapa>, ticket NN: revise o ramo ticket-NN, relatório <caminho>"`.
2. **Cada um revisa sozinho**, sem ler o parecer do outro: confere o ramo, roda os testes, confere cada evidência do
   relatório contra o ticket, o spec e os tickets resolvidos e procura o que quebraria ao ligar com as outras etapas.
   - O Fiel grava em `etapas/<etapa>/parecer-<construtor>.md` (como hoje).
   - O Fielzinho grava em `etapas/<etapa>/parecer-<construtor>-fielzinho.md`, no mesmo formato (veredito passa ou
     volta, consertos numerados com evidência).
   - Para não pisar um no outro: testes que sobem Docker ou chamam harness de verdade, só o Fiel roda; o Fielzinho lê
     a saída dele, ou roda depois, avisando antes.
3. **Os dois conversam** por `maestri ask` até um acordo: cada achado do outro é aceito, recusado com motivo ou
   ajustado. No máximo duas trocas por rodada de revisão.
4. **O Fiel fecha** a rodada no `parecer-<construtor>.md`: a lista única de consertos (cada um com quem achou) e o
   veredito. "Passa" só com os dois de acordo. Impasse depois das duas trocas: o Fiel escreve as duas posições e pergunta
   ao maestro (`maestri ask "Claude Code" "..."`).
5. O Fiel responde ao construtor, como hoje. Nas voltas de conserto, os dois conferem de novo, pelo mesmo fluxo.
   Continua valendo o teto: duas voltas; na terceira, passa com as ressalvas escritas.

## Os dois nunca

Editam o código do construtor, o spec ou os tickets; usam mais de um subagente por vez (além dos três Haiku de tarefa simples ou QA, como nas regras); gravam algo global de verdade.
