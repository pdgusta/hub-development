# 02: Prova: pastas com ponto aninhadas fora do LiveSync

Type: task
Status: resolved
Etapa: 0 (provas de risco)
Blocked by: None (can start immediately)

**What to build:** A exclusão de tudo que tem ponto, em qualquer nível da árvore, no sincronizador do LiveSync, que no teste do disco e banco vazou para o banco e para o outro disco.

**Fonte:** Ticket 48 (item 6, o vazamento) e ticket 12 (o que tem ponto não replica); bloco do Worker 4. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** None (can start immediately)

- [ ] `projeto/.venv/`, `projeto/.git/`, `clientes/x/.secrets/` e `.oculto/` não chegam ao banco nem ao outro disco com o CLI rodando
- [ ] o mesmo vale na varredura de partida, depois de reiniciar o CLI
- [ ] o relatório diz qual forma de exclusão funcionou e o que vai doer ao ligar com o gerador de exclusões (ticket 06)

## Comments
- 2026-10-16 ~21h25 (maestro): passado à Vela (era da Brasa depois do 01), para andar em paralelo e destravar o 06. Vela e Brasa ligadas no canvas para combinar portas e contêineres; a Vela consulta a worktree `ticket-01` só para leitura.
- 2026-10-16 ~22h35 (Vela): pego (`claimed`). Worktree `C:\context-hub-wt\ticket-02`, ramo `ticket-02`, de `integracao` 3857c98. Prova vai em `agents/code/test/provas/02-pastas-com-ponto/`. Falta: ler 48/12/Worker 4/spike, combinar portas com a Brasa, teste, relatório.
- 2026-10-16 ~23h (Vela): prova verde (12/12) com `.livesync/ignore` (`.*` e `.*/`), E2EE e caminho ofuscado, dois pares (`hub-ensaio-02-a/b`, 5996/5997), CLI rodando e varredura de partida; o vermelho (`-SemExclusao`) reproduz o vazamento do 48. Causa no CLI: `split(path.sep)` na varredura de partida. Módulo reaproveitado da prova 01 (Brasa, 43a4ea9). Contêineres apagados. Commit 6191e40. Relatório: `etapas/00-provas/relatorio-pastas-com-ponto.md`. Falta: revisão do Fiel.
- 2026-10-16 ~23h15 (Vela): Fiel/Fielzinho = **passa** (parecer em `etapas/00-provas/parecer-Vela.md`, seção do ticket 02). Ressalva para a junção com o ticket 05: atualizar a chamada do montador para `agents/code/test/` e repetir a prova. Encaminhado ao Rebite.
- 2026-10-16 20h00 (integrador, Rebite): juntado em `integracao`, commit c8d2267 (merge `--no-ff` de `ticket-02` 6191e40, o HEAD do parecer "passa"). Testes na árvore juntada: `node --test "agents/test/*.test.mjs"` + `instalar.test.mjs` do 03 = 14/14 verdes. A prova 02 (Docker) e a prova 03 (`codex exec`) não foram repetidas: árvores idênticas às revisadas (`git diff ticket-02 HEAD` e `git diff ticket-03 HEAD` vazios nas pastas delas). Ressalvas do parecer: ao juntar o 05, trocar a chamada do montador em `banco.psm1` para `agents/code/test/hub-de-ensaio/montar.mjs` e repetir a prova; na 1ª fase do vermelho vazaram os arquivos já presentes na partida; ausência vista só na janela da prova; só banco novo e envio A→B (sem plugin, segunda máquina, limpeza de vazamento antigo); o cleanup não confere o exit do `compose down`; ignore por máquina, antes da partida, sem negação, reinício após mudança. **Resolvido.**
