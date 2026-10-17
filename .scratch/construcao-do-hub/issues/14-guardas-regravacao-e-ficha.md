# 14: Guardas: regravação inteira e ficha fora do esquema

Type: task
Status: resolved
Etapa: 5 (guardas no disco)
Blocked by: 05, 03

**What to build:** O hook antes da ferramenta nos três harnesses: recusa regravar inteiro um arquivo que já existe no hub (com a mensagem que aponta a troca de trecho ou o MCP do banco), deixa passar troca de trecho e arquivo novo, e recusa a nota que ficaria fora do esquema, montando o conteúdo final antes de chamar o verificador. Sai na hora fora do hub.

**Fonte:** Bloco do Worker 6; faixa 6 em `spec-partes/faixas-05-06.md`; tickets 11, 14 e 12; escolha aceita 15. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 05 (Frontmatter imposto: esquemas, verificador e "nova iniciativa"), 03 (Prova: hooks do Codex em acesso total)

- [ ] os casos gravados na bancada passam nos três adaptadores
- [ ] regravar existente é recusado; troca de trecho e arquivo novo passam
- [ ] nota que ficaria sem `status` é recusada
- [ ] fora do hub, o hook não faz nada

## Comments
- 2026-10-16 ~20h20 (maestro): passado ao Trilho, como antecipação da etapa 5 (bloqueios 05 e 03 resolvidos; plano: até 3 agentes, sem depender de peça que não existe). Primeiro commit do ramo, separado: tirar o `README.md` da raiz do hub (decisão do ticket 12: raiz = `AGENTS.md` + seis raízes; era marcador do "Início do hub"), a pedido do maestro pela ressalva do Rebite na junção do 05.

- 2026-10-17 (Trilho): ticket pego, `Status: claimed`. Worktree `C:\context-hub-wt\ticket-14`, ramo `ticket-14`, de
  `integracao` (0d04985). Primeiro commit (3055de9): sai o `README.md` da raiz (ticket 12). Costuras: (1) o hook
  `node agents/code/hooks/guardas/antes-da-ferramenta.mjs <claude|codex|copilot>` com o evento na entrada, alimentado
  pelas entradas gravadas na bancada do ticket 11 (`C:\Projetos\bancada-acesso\gravacao\`); (2) ponta a ponta com
  `claude -p`, `codex exec` e `copilot -p` em HOME de ensaio. Falta: tudo depois do README.
- 2026-10-16 20:24 (maestro): aval do Gustavo para copiar o login dos três harnesses em pasta de ensaio (rodada `2026-10-16-login-dos-harnesses-no-ensaio`, A, vale para a construção inteira); condições em `../etapas/regras-da-construcao.md`.
- 2026-10-17 (Trilho): pronto no ramo `ticket-14` (HEAD ea4d299, `integracao` 8b9beef juntada). 69 testes verdes,
  com os 24 casos gravados na bancada nos três adaptadores; ponta a ponta verde nos três harnesses reais (login de
  ensaio com o aval, hashes iguais antes e depois). Hook e fragmentos em `agents/code/hooks/guardas/`. Relatório:
  `etapas/relatorio-14-guardas.md`. Falta: revisão do Fiel.
- 2026-10-17 ~0h50 (Trilho): revisão 1 (Fiel e Fielzinho): volta, dois consertos (o `lerPatch` não fecha a parte no
  `*** End Patch`; o relatório erra sobre caminho com ponto). Contexto acima de 40%: retomada gravada em
  `etapas/retomada-Trilho.md`, com o próximo passo exato. Falta: os dois consertos e a rodada 2.
- 2026-10-17 ~1h (Trilho): os dois consertos da revisão 1 feitos (commits 73a1917 e 124a643): o patch fecha no
  `*** End Patch`, com teste nos quatro finais no Codex e no Copilot; teste fixa a recusa em caminho com ponto;
  relatório corrigido. Ponta a ponta do Codex repetida, verde, hashes iguais. 71 testes verdes. Falta: revisão 2.
- 2026-10-17 ~1h15 (Trilho): revisão 2 (Fiel e Fielzinho): passa, HEAD 124a643, 71 testes verdes. Ressalva: as pastas
  `%TEMP%\hub-ensaio-14-*` dos testes sem harness se acumulam. Rebite avisado. Falta: junção (Rebite).
- 2026-10-16 21h03 (integrador, Rebite): juntado em `integracao`, commit 8d1d785 (merge `--no-ff` de `ticket-14` 124a643, o HEAD da rodada 2 "passa" de Fiel e Fielzinho; árvore juntada idêntica à do ramo). O primeiro commit do ramo tira o `README.md` da raiz (ordem do maestro). Testes: `node --test` de `agents/code/test/*.test.mjs`, `gerar-exclusoes/*.test.mjs` e `instalar.test.mjs` do 03 = 81/81 verdes. A ponta a ponta nos três harnesses (`ponta-a-ponta/14-guardas.test.mjs`) não foi repetida: árvore idêntica à revisada, e ela pede aval de login. As provas 01, 02, 03 e o sincronizador do 06 também não, pelo mesmo motivo. Ressalva do Fiel: cada `node --test` deixa pastas `%TEMP%\hub-ensaio-14-*` (os testes sem harness não apagam); a minha rodada criou duas e eu as apaguei; as 33 antigas ficaram. O teste ou o kit deveria apagá-las no fim. **Resolvido.**
- 2026-10-17 02h06 (Vela): buraco achado na ponta a ponta do 31 (Claude real): com o arquivo em CRLF e o old_string do Edit em LF, o trocar das guardas (agents/code/hooks/guardas/guarda.mjs) não casava, devolvia final undefined e a gravação passava sem conferência; o Claude Code casa os dois e grava. Conserto no ramo ticket-31 (050fb14): o trocar casa em CRLF como o Claude; teste em 20-acervo.test.mjs; 14-guardas verde.
