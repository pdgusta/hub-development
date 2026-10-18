---
name: codex-sem-cota-usa-claude
description: Codex só para testes (gpt-6-luna padrão, gpt-6.1-sol se difícil); execução e revisão no Claude; Fielzinho fora
metadata:
  type: feedback
---

Desde 2026-10-17 ~14h35 (Gustavo): a **execução é do Claude** (construção, revisão, 2ª leitura com subagente Opus 5.5;
Sonnet 5.5 para tarefa menor). O Codex fica **só para os testes** que precisam dele (o Codex como harness: hook, MCP,
kit, ponta a ponta), com **`gpt-6-luna`** por padrão e **`gpt-6.1-sol`** só quando o teste é difícil para o Luna; se
tudo é só teste, tudo no Luna. O Fielzinho (revisor Codex) sai desta execução.

**Why:** a cota do Codex acaba toda hora e parava a execução; o Gustavo não se importa com revisão por outro modelo
nesta execução. Primeiro ele disse "Claude só como tapa-buraco"; corrigiu em seguida ao lembrar que o Codex é preciso
para os testes.

**How to apply:** sem cota, a prova do Codex espera sem segurar o resto. Regra em `etapas/regras-da-construcao.md`;
constante `MODELO_CODEX` (ticket 43). Ver [[autonomia-na-construcao]].
