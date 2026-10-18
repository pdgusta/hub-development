# 24: Kit de par ao vivo nos três harnesses

Type: task
Status: resolved
Etapa: 10 (kit de par)
Blocked by: 23

**What to build:** Com o kit instalado na pasta de configuração de ensaio, os três harnesses de verdade leem o contrato, as skills e o MCP.

**Fonte:** Bloco do Worker 8, prova com login de ensaio. Pergunta ao Gustavo na hora: login dos harnesses na pasta de ensaio. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 23 (Kit de par: a forma)

- [ ] `claude -p`, `codex exec` e `copilot -p` respondem uma pergunta que só o contrato de ensaio sabe

## Comments
- 2026-10-16 20:24 (maestro): aval do Gustavo para copiar o login dos três harnesses em pasta de ensaio (rodada `2026-10-16-login-dos-harnesses-no-ensaio`, A, vale para a construção inteira); condições em `../etapas/regras-da-construcao.md`.

- 08:42 (maestro): do 23 (Cinzel): o Copilot não tem chave de configuração nem variável para as instruções do servidor MCP; só a opção `--allow-all-mcp-server-instructions` na linha de comando. Quem abre o Copilot (o preset do Maestri, um atalho) tem de passá-la.

- 08:42 (maestro, mandato): começa já com o Cinzel, sobre o `ticket-23` (dele, em revisão): os três harnesses de verdade com o kit instalado na pasta de configuração de ensaio, uma sessão de cada, modelos baratos, pela fila; o Codex depois das 12h15. Junção depois do 23.
- 2026-10-17 08:50 (Cinzel): peguei o 24 (`claimed`), sobre o `ticket-23`. Costuras ao maestro: `../etapas/costuras-24-Cinzel.md`.

- 08:43 (maestro, mandato): costuras do Cinzel aceitas (`../etapas/costuras-24-Cinzel.md`): harness aberto num repositório fora do hub; casa de ensaio no lugar do HOME (USERPROFILE) no Claude e no Copilot, `CODEX_HOME` no Codex; se um harness não seguir o HOME, troca pela variável dele e registra. Login copiado para a casa de ensaio nas condições do aval (hash antes e depois, apagar ao fim). Aceite = responder a palavra do ensaio; skill de marca e servidores MCP só registrados.
- 2026-10-17 09:15 (Cinzel): rodada 1 com harness real: Claude e Copilot PASSA (respondem a palavra do contrato de ensaio, abertos fora do hub, sem ferramenta; nada global; login apagado). Relatório `../etapas/relatorio-24-kit-de-par-ao-vivo.md`. Falta o Codex, depois das 12h15 (depois do 11).
- 2026-10-17 15:25 (Cinzel): aceite com MODELO_CODEX (65cb752); integracao 98a7ced juntada (769f36f), conflito no harness-real.test.mjs resolvido com os dois lados (o teste do app-server do 23 e os do modelo do 43). harness-real 9/9, 23-kit 20/20. Falta o Codex, depois do 23 juntado.
- 2026-10-17 17:20 (Cinzel): integracao f640bbd (18, 37, 23 juntados) no ramo: a3e0360; harness-real 9/9, aceite pulado. Falta o Codex na janela quieta da noite (luna, MODELO_CODEX).
- 2026-10-17 17:30 (Cinzel): rodada 2, só o Codex (0.162.1, gpt-6-luna), 17:20 a 17:21 com a trava, na janela quieta: PASSA (log `../etapas/logs/24-harness-2.log`, evidência 2000575). Respondeu a palavra do contrato de ensaio aberto fora do hub, sem ferramenta, seguindo o CODEX_HOME da casa; hashes reais iguais; login apagado. 23-kit + harness-real 34/34. Rodada 2 ao Fiel quando ele voltar (fora até o fim da janela).
- 2026-10-17 19h22 (integrador, Rebite): juntado em `integracao`, commit a4fa7e3 (merge `--no-ff` de `ticket-24` 2000575, rodada 2 "passa" do Fiel em acordo com a 2ª leitura, na mesma ponta, que já trazia `integracao` f640bbd; sem conflito). Testes: `23-kit + harness-real + 24-kit-ao-vivo + 22-kit-cliente + 22-proxy-sem-docker` 39 verdes, 1 pulado (o ao vivo, sem harness real), log `../etapas/logs/juncao-24-22-leves.log`; suíte `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis, com a trava, junto com a evidência do 22 (56cd23a): 359, 345 verdes, 14 pulados, 0 falhas, `git status` limpo (log `../etapas/logs/juncao-24-22-suite.log`). Harness real não repetido (arquivos idênticos aos revisados). Ressalvas do parecer: modelo e versão do Codex não aparecem na evidência; o relatório diz "trava de 17:21" com login às 17:20:59 (só redação); aviso de "helper binaries" do `CODEX_HOME` em `%TEMP%`. **Resolvido.**
