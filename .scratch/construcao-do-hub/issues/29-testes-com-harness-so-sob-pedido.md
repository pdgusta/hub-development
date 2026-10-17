# 29: Testes com harness de verdade só sob pedido

Type: task
Status: resolved
Etapa: infraestrutura de teste (fora da sequência)
Blocked by: None (can start immediately)

**What to build:** O `node --test` comum da suíte (`agents/code/test/**`) deixa de chamar o Claude Code, o Codex e o Copilot de verdade. Hoje a prova 03 (`agents/code/test/provas/03-codex-hooks/prova.test.mjs` e `instalar.test.mjs`) e a ponta a ponta do 14 (`agents/code/test/ponta-a-ponta/14-guardas.test.mjs`) rodam sempre: copiam login para pasta de ensaio, gastam cota, regravam os arquivos de evidência versionados e falham quando outra sessão do Codex mexe no `~/.codex/config.toml` real durante a rodada (aconteceu com a Brasa no 07). Esses testes passam a rodar só com uma variável de ambiente (`HUB_HARNESS_REAL=1`) e, sem ela, aparecem como pulados (`skip`) com o motivo. A evidência versionada só é regravada nessas rodadas pedidas. A conferência das pastas reais por hash continua nas rodadas pedidas e passa a dizer, quando falhar, qual arquivo mudou, para distinguir uma escrita do teste de uma escrita de outra sessão aberta.

**Fonte:** Achado da Brasa no ticket 07 (relatório `etapas/relatorio-07-banco-do-par.md`); regra do login no ensaio (`../etapas/regras-da-construcao.md`, "Login dos harnesses no ensaio"). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** None (can start immediately)

- [ ] sem `HUB_HARNESS_REAL`, o `node --test` da suíte inteira não chama nenhum harness, não copia login e não muda arquivo versionado; os testes de harness aparecem como pulados, com o motivo
- [ ] com `HUB_HARNESS_REAL=1`, a prova 03 e a ponta a ponta do 14 rodam como antes e passam
- [ ] quando a conferência por hash falha, a mensagem diz qual arquivo real mudou
- [ ] as regras da construção e o `juntar-tickets.md` dizem quando rodar com a variável (o maestro atualiza)

## Comments

- 2026-10-16 ~21h35 (maestro): publicado pelo achado da Brasa no 07. Dono: a Vela (fez a prova 03), enquanto o 27 está em revisão; a ponta a ponta do 14 é do Trilho, que ela pode consultar.
- 2026-10-16 ~21h40 (maestro): passado à Brasa, que achou o problema e espera a revisão do 07; a Vela ficou com os cinco consertos do 27.
- 2026-10-16 ~21h30, Brasa: peguei (Status claimed). Worktree `C:\context-hub-wt\ticket-29`, ramo `ticket-29`, de `integracao` 8d1d785. Só três arquivos chamam harness: `provas/03-codex-hooks/prova.test.mjs`, `provas/03-codex-hooks/instalar.test.mjs` (o app-server do Codex, sem login) e `ponta-a-ponta/14-guardas.test.mjs`. Plano: um módulo `agents/code/test/harness-real.mjs` (`comHarness(nome, fn)`: sem `HUB_HARNESS_REAL=1`, um `test` pulado com o motivo; com ela, um `describe` com o corpo); tudo que hoje roda no topo desses arquivos (pasta de ensaio, apagar evidência, hashes de antes) vai para dentro do corpo. A conferência por hash diz cada arquivo que mudou, os dois hashes, a hora da gravação e se ela caiu dentro da rodada de algum harness ou fora (outra sessão). Costuras: (1) `node --test` dos três arquivos sem a variável, visto de fora: pulados com o motivo, nenhuma pasta `hub-ensaio-03/14` no TEMP, evidência versionada igual; (2) a mensagem da conferência por hash; (3) com `HUB_HARNESS_REAL=1`, os três de verdade, uma vez no fim (login no ensaio, registrado). Falta: tudo.
- 2026-10-16 ~21h50, Brasa: commits 654c329 (`agents/code/test/harness-real.mjs` com `comHarness` e `relatorioDeHashes`; os três testes de harness embrulhados; teste `agents/code/test/harness-real.test.mjs`, 5 de 5) e 0266761 (evidência da rodada pedida). Suíte sem a variável: 86, 83 passam, 3 pulados com o motivo. Com `HUB_HARNESS_REAL=1 --test-concurrency=1`: 11 de 11; hashes reais iguais; logins apagados. Relatório `etapas/relatorio-29-harness-sob-pedido.md`. Critério 4 é do maestro (sugestão no relatório). Pedi revisão ao Fiel.
- 2026-10-16 ~22h, Brasa: o maestro fez o critério 4 (regras e `juntar-tickets.md`). As pastas `hub-ensaio-14-*` do teste de unidade do 14 já estão consertadas pelo Trilho no `ticket-12` (58b9563): fora do 29. Relatório atualizado.
- 2026-10-16 ~22h20, Brasa: rodada 1 voltou (Fiel e Fielzinho). Consertos em 0da445e, com `integracao` 0a8e17f juntada: o 27 protegido; o teste acha sozinho quem chama harness ou login (sem lista), com contraprova. Suíte sem a variável: 116, 112 passam, 4 pulados, `git status` limpo. Pedida a rodada 2.
- 2026-10-16 ~22h35, Brasa: rodada 2 PASSA (Fiel sozinho; o Fielzinho lê depois, e o que ele achar entra como ressalva). Avisei o Rebite. Ramo `ticket-29` 0da445e.
- 2026-10-16 22h02 (integrador, Rebite): juntado em `integracao`, commit d5e4e16 (merge `--no-ff` de `ticket-29` 0da445e, o HEAD da rodada 2 "passa" do Fiel; árvore juntada idêntica à do ramo). Testes: `node --test "agents/code/test/**/*.test.mjs"` sem `HUB_HARNESS_REAL` = 116, 112 passam, 4 pulados (03 instalar, 03 prova, 14 e 27 ponta a ponta), 0 falhas; `git status` limpo depois. Os testes com harness real não foram rodados: árvore idêntica à revisada (com a variável, 03 e 14 deram 11/11 na rodada 1). Ressalvas: a leitura do Fielzinho na rodada 2 ficou pendente (sem cota); se ele achar algo, vira ressalva. As pastas `%TEMP%\hub-ensaio-*` dos testes sem harness (04, 05, 14, 27) continuam se acumulando, sem dono. **Resolvido.**
