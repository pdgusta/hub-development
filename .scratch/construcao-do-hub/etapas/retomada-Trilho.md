# Retomada do Trilho (construtor), gravada em 2026-10-17 ~0h50 (São Paulo)

Leia antes: `etapas/regras-da-construcao.md` (inteiras), o ticket `issues/14-guardas-regravacao-e-ficha.md` e o
relatório `etapas/relatorio-14-guardas.md`. Responda em pt-BR, frases curtas. Sem subagentes. Maestro = "Claude Code";
revisor = "Fiel" (revisa em dupla com o Fielzinho); integrador = "Rebite" (avise o Rebite depois do "passa", não o
maestro).

## Onde estou
- **Ticket 14** (guardas: regravação e ficha), `Status: claimed`. Ramo `ticket-14`, worktree `C:\context-hub-wt\ticket-14`,
  HEAD 6b866fb (com `integracao` 8b9beef juntada em ea4d299).
- Feitos e juntados antes: tickets 04 e 05 (relatório deles: `etapas/01-esqueleto/relatorio.md`).
- **Revisão 1 do 14: VOLTA** (Fiel + Fielzinho, parecer em `etapas/01-esqueleto/parecer-Trilho.md`, seção do 14).

## Ticket 14 juntado (integracao 8d1d785) e resolvido. Próximo: esperar o próximo ticket do maestro
1. **`lerPatch` não fecha a parte no `*** End Patch`.** Em `agents/code/hooks/guardas/patch.mjs`, as linhas depois do
   `*** End Patch` (um LF, CRLF ou dois LF no fim do patch) entram na última parte; um `Update File` com linha vazia
   no fim deixa de casar e vira `final: undefined`, que passa sem conferir a ficha. Reproduzido pelo Fiel tirando o
   `status` de um `context.md`. Conserto: ao ver `*** End Patch`, encerrar a parte atual (`atual = undefined`).
   Testes (TDD, vermelho antes) em `agents/code/test/14-guardas.test.mjs`: patch terminando em `\n`, `\r\n` e `\n\n`,
   no Codex e no `apply_patch` do Copilot (toolArgs como texto do patch: o adaptador lê `a._texto ?? a.input ?? a.patch
   ?? a.command`), tirando o `status` → tem de recusar. Depois **repetir a ponta a ponta só do Codex**:
   `HARNESSES=codex node --test agents/code/test/ponta-a-ponta/14-guardas.test.mjs` e registrar no relatório (o que
   copiou, quando apagou, os hashes, que estão em `evidencia-14/hashes.json`; atenção: a rodada só do Codex regrava
   esse arquivo com só o uso do Codex).
2. **Relatório errado sobre caminho com ponto.** O relatório diz que "caminho com ponto passa", mas a **regravação** ali é
   recusada (só a conferência da ficha é ignorada, porque `analisar` ignora caminho com ponto). Manter o código;
   corrigir o texto do relatório; pôr um teste que fixe: regravar existente em `.../.secrets/x.md` (ou outra pasta com
   ponto) do hub é recusado, e uma nota nova lá sem frontmatter passa.
3. Rodar `node --test "agents/code/test/*.test.mjs"` (hoje 69 verdes), commit, `git merge integracao` se andou, testes
   de novo, e pedir a rodada 2 ao Fiel **com o hash do HEAD**. Depois do passa, avisar o Rebite.

## Decisões e armadilhas
- Código só em `agents/code/` (hooks, test, bin); skill em `agents/skills/`. Nada na raiz (o README saiu, commit 3055de9).
- **Barra invertida some** em heredoc do bash e em `python - <<EOF` com texto JS: para trechos com `\\`, use o Edit.
- **Não use `import()` do arquivo de teste para checar sintaxe**: ele roda os testes (foi assim a rodada acidental do
  Claude). Use `node --check`.
- Ponta a ponta: caminho longo (`realpathSync.native`) por causa do Claude ("suspicious Windows path pattern" com
  `GUSTAV~1.DEL`); o `create` do Copilot não cria pasta; o Codex quer a linha inteira no patch; evidência passa por
  `semCasa` (troca a pasta e o nome do usuário).
- Login de ensaio: aval do Gustavo para a construção inteira (regras, "Onde trabalhar"). Uma sessão por harness, modelo
  barato, apagar a pasta, hashes antes e depois, registrar no relatório.
- No Copilot, saída ≠ 0 no `preToolUse` recusa a chamada: o hook sai sempre 0.
- `research/` tem ciclo (`status` sai do `stage`); para testar "sem status" use `knowledge/`.
- Em `agents/code/**` não há frontmatter (paths.yml `tipo: null`): só a guarda de regravação decide lá.

## Comandos
```
cd C:\context-hub-wt\ticket-14
node --test "agents/code/test/*.test.mjs"
node agents/code/bin/verificar-hub.mjs .
HARNESSES=codex node --test agents/code/test/ponta-a-ponta/14-guardas.test.mjs
```

## Scratchpad
Nada só no scratchpad: o gerador dos casos foi para `agents/code/test/14-guardas/gerar-casos.py` (6b866fb); os logs
das rodadas da ponta a ponta já estão resumidos no relatório e a evidência em `evidencia-14/`.
