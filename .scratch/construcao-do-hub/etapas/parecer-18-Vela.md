# Parecer do ticket 18 (Vela): retomada, nota de sete campos, início e fim

## Rodada 1 — 2026-10-17 ~09h (ramo ticket-18, HEAD b840812; base integracao 9cc878b + ticket-17 3e8bbc8)

Veredito: **VOLTA**, por 1 conserto. Fiel sozinho (Fielzinho sem cota até 12h15; leitura dele pendente). Codex real
pendente (rodada curta depois das 12h15). Junção só depois do 17 e do 16.

### Conferido pelo Fiel

- Árvore limpa antes e depois. `node --test` em 18-retomada, 17-vigia-tela, 04-esqueleto, 05-nova-iniciativa, 27-* e
  harness-real: 91/91.
- `nota.mjs` lido inteiro: iniciativa por caminho (`_` e `.` fora), recruta pelo `MAESTRI_TERMINAL_ID` sem
  `HUB_PAPEL=maestro`, passagem em `work/passagem-<terminal>.md`, sete rótulos, `last_agent` (está no esquema
  `retomada.yml`; `handoff` está no `work.yml`), memória do Claude pelo nome da pasta de projeto (sinal → `-`), corte de
  4.000 no início.
- Real Claude e Copilot 2/2 (`etapas/logs/18-real-1.log`), `apagado: true` nos dois, sem credencial na evidência (o
  único casamento de `eyJ` é base64 de raciocínio cifrado do Copilot, não token).

### Consertos

1. **(Fiel) O fim cobra a nota de quem não gravou: "o que o turno gravou" é qualquer arquivo do hub com mtime depois
   da marca.** `nucleo.mjs` (`mudados`, linhas 45-56) anda pelo hub inteiro, e `conferirRetomada` (nota.mjs) pede a
   nota de toda iniciativa onde apareceu arquivo novo. Com a opção A (sessões paralelas: quem conduz e recrutas), a
   gravação de uma sessão devolve as outras.
   - Sonda (hub do `montar.mjs`): sessão M de quem conduz marca um turno só de conversa; outra sessão grava
     `clients/aurora/migracao-de-tenant/research/do-recruta.md`; `fim(hub, 'sessao-M')` devolve "atualize a nota de
     retomada de clients/aurora/migracao-de-tenant com o que esta resposta fez" (mais as faltas de frontmatter do
     arquivo alheio). M é devolvida três vezes e, na quarta, a falta vai ao `estado.json` da vigia: aviso falso.
   - O mesmo vale para o que o sincronizador (LiveSync) grava vindo da outra máquina, e o `gravarUltimoAgente` carimba
     `last_agent` de quem não escreveu a nota, se outra sessão de quem conduz a mudou no meio.
   - Conserto: a cobrança da nota (e o `last_agent`) só pelo que esta sessão gravou. Por exemplo, os caminhos que o
     próprio harness informa nos eventos de ferramenta da sessão (PostToolUse/postToolUse, como o 15 já lê nos três),
     guardados no arquivo da sessão. Teste: duas sessões no mesmo hub, uma grava, a outra só conversa e solta.

### Ressalvas (não seguram)

1. A raiz (`mudados` por mtime) é do 27, já juntado: as faltas do verificador também caem na sessão errada. Se o
   conserto 1 trocar a fonte no núcleo, resolve os dois; se não, levar ao maestro como ticket seguinte do 27.
2. Copilot só pelo hook `agentStop`, sem a extensão `onAgentStop`; memória privada só a do Claude Code; juntar as
   passagens na nota sem mecanismo; a opção A muda o spec. Os quatro estão declarados para rever com o Gustavo.
3. `ehNota` aceita qualquer `retomada.md` dentro da iniciativa (ex.: `research/retomada.md`) como nota.
