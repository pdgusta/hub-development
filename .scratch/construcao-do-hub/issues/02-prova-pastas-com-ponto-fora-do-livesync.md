# 02: Prova: pastas com ponto aninhadas fora do LiveSync

Type: task
Status: claimed
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
