# 29: Testes com harness de verdade só sob pedido

Type: task
Status: ready-for-agent
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
