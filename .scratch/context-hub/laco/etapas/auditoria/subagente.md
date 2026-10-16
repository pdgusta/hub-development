# Instruções do subagente de auditoria (Opus)

Você recebe um número de lote N.

1. Leia uma vez `C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/auditoria/prompt.md` (regras e formato).
2. Leia `C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/auditoria/lotes.json`: é uma lista de lotes; o seu é
   o de índice N (começa em 0). Cada entrada tem `chave`, `slug` e `tipo` (`conferencia` ou `conceito`).
3. Leia os pacotes `C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/auditoria/pacotes/<slug>.json` do lote,
   todos numa só mensagem, em paralelo. Julgue como o prompt.md manda, sem web.
4. Grave, numa só mensagem e em paralelo, em UTF-8:
   - tipo `conferencia`: `.../etapas/auditoria/respostas/<slug>.json`
   - tipo `conceito`: `.../etapas/auditoria/conceitos/<slug>.json`

   com exatamente:
   `{"chave": "<chave>", "modelo": "claude-opus-5-5", "ts": "<agora, ISO UTC>", "tipo": "<tipo>", "resultado": "<concorda|discorda>", "auditoria": { ...o objeto JSON do prompt.md... }}`
5. Responda só "ok" (ou "erro: <chave>: <motivo>").
