---
name: pesquisa-pelo-freellmapi
description: Pesquisas e varreduras desta frente vão pelo FreeLLMAPI, não por subagentes do Claude; antes de lançar um agente Claude, dizer o custo e pedir aval
metadata:
  type: feedback
---

O Gustavo usa o FreeLLMAPI para não gastar tokens do Claude. Pesquisa, varredura ou levantamento pesado roda
por script com modelos do FreeLLMAPI; o Claude orquestra, confere e escreve o resultado. Um subagente Claude
(Agent, Workflow, Maestri recruta) só roda com aval explícito, depois de eu dizer que vai gastar tokens do
Claude e quanto, mais ou menos.

**Why:** em 2026-10-13 lancei um subagente Claude para o ticket "Serviço de busca da função web_search" logo
depois do "pode iniciar"; ele: "Meu Deus cara então pra q o FreeLLMAPI? Eu estou usando ele justamente pra não
gastar tokens do claude e você dispara isso tudo num agente mano". Parei o agente.

**How to apply:** ao propor como rodar uma pesquisa, a opção recomendada é pelo FreeLLMAPI, com orçamento de
cota ([[cota-antes-de-bancada]]); o "pode iniciar" de um ticket não autoriza gastar tokens do Claude em agente.
