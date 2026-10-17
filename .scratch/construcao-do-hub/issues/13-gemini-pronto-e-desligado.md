# 13: Gemini pronto e desligado

Type: task
Status: resolved
Etapa: 4 (busca)
Blocked by: 12

**What to build:** A configuração do embedding do gemini pelo FreeLLMAPI escrita e desligada. Pergunta ao Gustavo na hora: autorização e cota para o teste único.

**Fonte:** Ticket 09 (o gemini "configurado, testado uma vez, desligado") e ticket 54; bloco do Worker 3, item (d). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 12 (Busca local com aceite)

- [ ] a configuração existe e está desligada
- [ ] se o Gustavo liberar, um teste único num segundo índice de uma cópia do hub de ensaio, com o resultado gravado

## Comments
- 2026-10-16 ~23h50 (maestro): passado ao Trilho depois do 15 (juntado ac1cd2c). Primeiro commit: o teste do 12 passa a provar o reaproveitamento do índice por evidência, não pelo tempo (falhou sob carga na junção do 15). Teste único do gemini na rodada `2026-10-16-gemini-teste-unico`.
- 2026-10-17 ~01h05 (Trilho): pego (`claimed`). Worktree `C:/context-hub-wt/ticket-13`, ramo `ticket-13`, de `integracao` f83c8f5. Primeiro commit f8b8769 (teste do 12 pelo índice). Sem chamar o FreeLLMAPI até o maestro avisar; Docker não.
- 2026-10-17 ~00h30 (maestro): teste único liberado pelo Gustavo (rodada `gemini-teste-unico`, A, pelo chat), nas condições da rodada (cota conferida antes, parar se passar de um quarto do que resta). Ele liberou ligar o contêiner `freellmapi-freellmapi-1` quando precisar.
- 2026-10-17 ~01h50 (Trilho): config desligada (32e77b2), teste único feito (95e37b7: 62 pedidos ao Google, contêiner parado de novo), dublês fechados (eb7c941). integracao 5d84d76 juntada. Falta: suíte comum (esperando a trava), revisão. Relatório etapas/relatorio-13-gemini.md.
- 2026-10-17 ~02h05 (Trilho): suíte 172 passam, 8 pulados, 0 falham; merge 57e85cf (6bfb506). Revisão pedida ao Fiel.
- 2026-10-17 ~02h05 (Trilho): Fiel rodada 1 PASSA (etapas/parecer-13-Trilho.md). Ressalva: -Gemini no hub padrão reindexaria o índice padrão (uma recusa evitaria acidente). Passado ao Rebite.
- 2026-10-17 02h21 (integrador, Rebite): juntado em `integracao`, commit 236b3ef (merge `--no-ff` de `ticket-13` 6bfb506, o HEAD da rodada 1 "passa" do Fiel; árvore juntada idêntica à do ramo). Testes, com a trava: `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem `HUB_*`, `FREELLM_BASE_URL` nem `OPENAI_*` = 190, 182 verdes, 8 pulados, 0 falhas (11 min); `git status` limpo. O teste único real do gateway não foi repetido (cota; feito com aval do Gustavo, evidência em `13-gemini/evidencia/teste-unico.json`). Ressalvas do parecer: `-Gemini` no hub de verdade reindexaria o índice padrão com o gemini (mesmo `estado` e mesmo banco); uma recusa quando `-Hub` é o hub padrão, ou um banco separado por modelo, evitaria isso; `context_length` de 20 000 do gateway dá um vetor por nota no gemini. A leitura do Fielzinho ficou pendente. **Resolvido.**
