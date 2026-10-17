# Relatório do ticket 34: roteamento, uma linha de registro por skill e caminho com barra do Windows (Vela)

Ramo `ticket-34`, worktree `C:/context-hub-wt/ticket-34`, da ponta de `integracao` e82ce65 (2026-10-17 02h25).
Fonte: `parecer-19-Vela.md` (seção "Leitura do Fielzinho") e `parecer-19-Vela-fielzinho.md`.

## O que mudou

1. **Barra do Windows** (cd52173). `caminhosDoPedido` em `agents/code/bin/lib/roteamento.mjs` troca `\` por `/` antes
   do filtro "tem barra ou termina em .md". Antes, `research\dados.json` caía no filtro e não casava o gatilho
   `caminho`; `research\cotas.md` passava só por terminar em `.md`.
2. **Uma linha por skill** (0e39c35). `fecharTurno` em `agents/code/hooks/roteamento/registro.mjs` escreve, para cada
   linha indicada no turno, uma linha de indicação por skill, com o "rodou" de cada uma (`sim`/`não` no Claude Code;
   `não verificado` no Codex e no Copilot, como antes). Antes, as skills que rodaram iam juntas numa célula e as
   indicadas e não usadas sumiam.

## Testes (costuras do 19: hook de entrada; uso + fim da resposta)

Em `agents/code/test/19-roteamento.test.mjs`, os dois testes novos falharam antes do conserto pelo motivo certo:
- "caminho citado com barra do Windows recebe a mesma indicação que com barra comum": antes, contexto vazio.
- "claude: linha com duas skills, uma usada e outra não: uma linha de indicação por skill": antes, só
  `[freellmapi, pesquisa-dupla, sim]`; agora também `[busca, pesquisa-dupla, não]`.
- `node --test agents/code/test/19-roteamento.test.mjs`: 19/19.

Leitores do registro: só a ponta a ponta do 19 (`ponta-a-ponta/19-roteamento.test.mjs`), que confere linhas de uma
skill só (`pesquisa-pelo-freellmapi`); segue compatível. Ponta a ponta com harness real não repetida: o conserto é de
lógica interna, coberto pelas costuras dos scripts; o formato que o harness entrega e recebe não mudou.

## Suíte inteira

2026-10-17, com a trava: `node --test "agents/code/test/**/*.test.mjs"` no ramo ticket-34 em 0e39c35: 193 testes,
185 pass, 0 fail, 8 pulados (harness real). Registro em `etapas/logs/suite-34.log`.
