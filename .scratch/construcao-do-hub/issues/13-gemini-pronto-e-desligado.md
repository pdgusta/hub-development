# 13: Gemini pronto e desligado

Type: task
Status: ready-for-agent
Etapa: 4 (busca)
Blocked by: 12

**What to build:** A configuração do embedding do gemini pelo FreeLLMAPI escrita e desligada. Pergunta ao Gustavo na hora: autorização e cota para o teste único.

**Fonte:** Ticket 09 (o gemini "configurado, testado uma vez, desligado") e ticket 54; bloco do Worker 3, item (d). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 12 (Busca local com aceite)

- [ ] a configuração existe e está desligada
- [ ] se o Gustavo liberar, um teste único num segundo índice de uma cópia do hub de ensaio, com o resultado gravado

## Comments
- 2026-10-16 ~23h50 (maestro): passado ao Trilho depois do 15 (juntado ac1cd2c). Primeiro commit: o teste do 12 passa a provar o reaproveitamento do índice por evidência, não pelo tempo (falhou sob carga na junção do 15). Teste único do gemini na rodada `2026-10-16-gemini-teste-unico`.
