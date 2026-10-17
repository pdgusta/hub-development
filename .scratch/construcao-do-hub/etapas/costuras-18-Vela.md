# Costuras do ticket 18 (retomada: nota de sete campos, início e fim), propostas pela Vela

2026-10-17 ~07h40. Ramo `ticket-18`, worktree `C:/context-hub-wt/ticket-18`: `integracao` 9cc878b com o `ticket-17`
(86c5a88) juntado. Fontes lidas: ticket 18 e os comentários dele; spec, Worker 2; faixa 2 em
`spec-partes/faixas-01-02.md` (linhas 401 a 595); rascunho `rascunhos/retomada-com-varias-sessoes.md`; o núcleo do fim
da resposta (27) e o `tela.mjs inicio` (17).

## Antes de tudo: a pergunta em aberto (comentário do maestro, 2026-10-16 19h55)

Várias sessões no mesmo trabalho: não achei rodada nem decisão.

- **A (recomendada):** a proposta do maestro, com os sinais que já existem.
  - Quem conduz (sessão sem `MAESTRI_TERMINAL_ID`, ou com `HUB_PAPEL=maestro`, do 20) mantém a `retomada.md`.
  - O recruta (com `MAESTRI_TERMINAL_ID` e sem `HUB_PAPEL=maestro`) mantém a sua **passagem**: os mesmos sete campos,
    só da parte dele, em `<iniciativa>/work/passagem-<terminal>.md`. O `work/` já guarda handoffs por agente
    (catálogo do 12).
  - O início abre a nota e, para o recruta, a passagem dele.
  - Quem conduz absorve as passagens: fica na regra do `AGENTS.md`, sem mecanismo.
- **B:** uma nota só, como o spec diz hoje. A passagem fica para outro ticket. Mais simples; recrutas e maestro
  gravariam na mesma `retomada.md`.

## Costuras (o que o teste olha de fora)

1. **Fim da resposta, a mesma porta do 27.** Um núcleo só, e os mesmos fragmentos dos três harnesses (mod do Claude
   Code, `Stop` do Codex, `agentStop` do Copilot). As faltas da retomada somam-se às do verificador, com a mesma conta de
   três devoluções e o registro na vigia (Gustavo, B).
   - **Regra mecânica (proposta):** para cada iniciativa onde o turno gravou algum arquivo fora da nota, a nota dela
     (a `retomada.md`, ou a passagem, se for A) tem de ter mudado depois da marca do turno. Se não mudou, devolve:
     "atualize a nota de retomada de <iniciativa>".
   - Resposta só de conversa, ou que gravou fora de iniciativa: solta. É o ponto aberto da faixa 2 ("não devolver toda
     resposta").
   - **Os sete campos:** a nota que mudou tem de manter os sete rótulos (Objetivo, Onde parou, Próximo passo, Decisões,
     Tentado e não deu certo, Perguntas abertas, Arquivos em jogo) e o `next_step` no frontmatter. Se faltar, é falta.
   - **`last_agent`:** quando a nota muda, o fim grava `last_agent` com o harness e o modelo, quando o modelo é
     conhecido (o Claude Code pelo transcript, como no 31).
   - **Memória privada:** só a do Claude Code é conhecida (`<CLAUDE_CONFIG_DIR>/projects/*/memory/`). Se mudou depois da
     marca, entra um **aviso** uma vez por mudança ("confira se a memória ganhou algo que o hub não tem e grave no
     hub"), como os avisos do 27, sem gastar devolução. Uma devolução não teria como soltar: o agente não desfaz a
     memória. Codex e Copilot: não verificados, ficam no relatório.
   - **Copilot:** só o hook `agentStop`, sem a extensão `onAgentStop` com `--experimental`. O 27 provou que o hook
     sozinho devolve e solta (com a continuação). Falta o aval para deixar a extensão de fora.
2. **Início da sessão, o mesmo hook do 17** (`tela.mjs inicio`, um `additionalContext` só): depois do estado da vigia,
   vem a nota da iniciativa onde a sessão abre (sobe da pasta até a raiz da iniciativa: `clients/<c>/<i>/`,
   `initiatives/<i>/`, `operations/<o>/`).
   - Aberto na raiz ou numa pasta sem iniciativa: "nenhuma nota aberta; ache o trabalho pela busca, pelo nome que o
     Gustavo der, ou pergunte".
   - Fora do hub: nada (já é assim).
   - Nota longa: corta em ~4.000 caracteres e aponta o caminho. A faixa diz "curta é regra, não limite"; o corte só
     protege o contexto.
3. **Regra no `AGENTS.md`:** uma linha na cabeça (hoje 1.695 de 2.000 caracteres): "ao fim de cada resposta que mexeu
   num trabalho, mantenha a `retomada.md` dele (sete campos) e leve ao hub o que só a sua memória privada sabe". Mais uma
   seção curta fora da cabeça, com os sete campos, fato e hipótese, e o banco fora (troca de trecho e pendência em
   "Perguntas abertas").

## Prova

- **Testes automatizados** (`agents/code/test/18-retomada.test.mjs`), com eventos gravados dos três harnesses:
  - devolve quando o turno gravou na iniciativa sem mexer na nota; solta depois de a nota mudar;
  - só conversa: solta; fora do hub: nada;
  - nota sem um campo: falta; `last_agent` gravado;
  - aviso da memória uma vez;
  - início com a nota (com a vigia, sem a vigia, na raiz, fora).
- **Ponta a ponta real** (fila e trava; molde 27/17), nos três harnesses:
  - sessão 1 numa iniciativa do hub de ensaio, tarefa curta (criar uma nota em `research/`): o fim devolve, o agente
    atualiza a nota, e ela fica com os sete campos e o `next_step`;
  - sessão 2 na mesma pasta: "qual é o próximo passo?" responde pela nota.
- **Fora deste ticket:** banco fora com o MCP parado (pede o fork e o Docker; só regra no `AGENTS.md`); retomada pelo
  cliente; trabalho fora de iniciativa.
