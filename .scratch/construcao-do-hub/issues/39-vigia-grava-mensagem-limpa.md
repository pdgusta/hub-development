# 39: A vigia grava a mensagem limpa no estado

Type: task
Status: resolved
Etapa: conserto do 16 (fora da sequência)
Blocked by: 16

**What to build:** Quando o kit do banco falha, o item `sincronizador` do `estado.json` leva o erro do PowerShell com
códigos de cor (`\u001b[31;1m...`) e o caminho do `TEMP` no resumo (achado da Vela no 17, com um `par.env` sem
`HUB_OUTRO_PAR_URL`). A tela do 17 já tira as cores, mas o texto vem do 16 (`vigia.mjs` / `kit.ps1`): a vigia passa a
gravar só a mensagem limpa (sem sequências de cor; caminho do `TEMP` trocado por um rótulo ou tirado), em todo item.

**Fonte:** achado da Vela no 17 (2026-10-17 ~11h45).

**Blocked by:** 16 (resolvido)

- [ ] com o kit falhando por falta de `HUB_OUTRO_PAR_URL`, o item do `estado.json` não tem sequência de cor nem caminho do `TEMP`
- [ ] os outros itens também passam pela limpeza
- [ ] a suíte segue verde

## Comments

- 2026-10-17 11h45 (maestro): publicado pelo achado da Vela. Dono: o Trilho (fez o 16), depois do 38.
- 2026-10-17 ~12h30 (Trilho): ramo ticket-39 (4309277). Limpeza em lib/vigia.mjs (todo item: sem cor, TEMP como %TEMP%); kit.ps1 sai só com a mensagem. 16-vigia 21/21 (2 novos), 17 invertido (afirmava a cor), 17+27+21 39/39, 20 22/22. Junta com o 38 sem conflito. Relatório etapas/relatorio-39-vigia-mensagem-limpa.md; revisão pedida ao Fiel.
- 2026-10-17 14h06 (integrador, Rebite): juntado em `integracao`, commit 2d5c528 (merge `--no-ff` de `ticket-39` 4309277, o HEAD da rodada 1 "passa" do Fiel). Testes: suíte `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis, com a trava, junto com o 38, o 39 e a manutenção do 22 (c42ffa0): 285, 275 verdes, 10 pulados, 0 falhas, `git status` limpo (log `etapas/logs/juncao-38-39-22m-suite.log`; Docker Desktop parado pelo maestro na janela quieta, nenhum teste caiu por isso). Ressalva do parecer: só strings de primeiro nível são limpas; o `voltas[].feito` do item `laco` passa como veio (o `resumo` sai limpo). Leitura do Fielzinho pendente. **Resolvido.**
