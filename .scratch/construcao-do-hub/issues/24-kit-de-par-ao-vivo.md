# 24: Kit de par ao vivo nos três harnesses

Type: task
Status: claimed
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
