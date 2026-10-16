---
titulo: Quem ajusta a tabela de roteamento
ticket: 15
aberta: 2026-10-15
estado: absorvida
---

Você escolheu as duas camadas de skills. Esta é a última pergunta do ticket. Depois dela, o maestro escreve o Answer e o
resolve.

**O que pesa:**
- O verificador do fim registra se a skill indicada pela tabela rodou. Esse registro mostra a linha que erra: a que
  indicou uma skill que o agente ignorou, ou a que faltou quando o agente usou uma skill por conta própria.
- A tabela é parte do acervo em `agents/skills/`. O ticket "Maestri: padrão e liberdade" decidiu que o Claude Code só
  altera o acervo com o seu aval, e que o Codex e o Copilot só deixam propostas em `agents/maestro/propostas/`.
- **Para a construção, sem pergunta:** onde o hook de entrada não conseguir injetar o aviso (no Codex e no Copilot, não
  verificado), a linha da tabela vira regra no contrato daquele harness, como já se decidiu para a checagem de início. O
  teste de aceite é um pedido de pesquisa que não cita o FreeLLMAPI e, mesmo assim, faz a skill dele disparar.

## Quem ajusta a tabela quando o registro aponta erro
id: ajuste
tipo: escolha
recomendada: A

- A: O maestro junta os erros do registro numa proposta em `agents/maestro/propostas/` (a linha, o que errou, quantas vezes e a correção), e a correção só entra com o seu aval, na mesma guarda do resto do acervo
- B: O maestro corrige a tabela sozinho e avisa em uma linha. Mais rápido, mas a tabela muda sem você ver
- C: Ninguém ajusta pelo registro: a tabela só muda quando você pede

## Algo mais?
id: algo-mais
tipo: texto
