# 04: Esqueleto do hub e hub de ensaio

Type: task
Status: resolved
Etapa: 1 (esqueleto)
Blocked by: None (can start immediately)

**What to build:** A árvore do hub com as seis raízes em inglês e `_archive/` em cada uma, o `AGENTS.md` da raiz (com o bloco da cabeça do contrato) e um `verificar-hub` que confere a estrutura. Entrega também o hub de ensaio, que todas as etapas seguintes usam.

**Fonte:** Bloco do Worker 1 no `spec.md`; faixa 1 em `spec-partes/faixas-01-02.md`; ticket 12. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** None (can start immediately)

- [ ] o `verificar-hub` passa no hub de ensaio e recusa um `CLAUDE.md` no hub ou acima dele
- [ ] o `AGENTS.md` traz o bloco da cabeça com até 2.000 caracteres
- [ ] o hub de ensaio tem duas iniciativas com o núcleo, notas em pt-BR (texto inventado) e um binário pequeno, na forma decidida no ticket 12

## Comments

- 2026-10-16 ~19h30 (Trilho): ticket pego, `Status: claimed`. Worktree `C:\context-hub-wt\ticket-04`, ramo `ticket-04`,
  a partir de `integracao` (69cb383). Costuras (do spec, faixa 1): (1) `node agents/bin/verificar-hub.mjs <raiz>`, saída
  0 ou ≠ 0 com o motivo; (2) `node agents/test/hub-de-ensaio/montar.mjs <destino>`, que monta o hub de ensaio; (3) o
  `AGENTS.md` do ramo, conferido pelo `verificar-hub`. Teste: `node --test agents/test/`. Perguntei ao maestro onde mora
  o código (kit/, hooks/ na raiz?) e se o hub de ensaio por script serve. Falta: tudo.
- 2026-10-16 ~20h15 (Trilho): pronto no ramo `ticket-04` (4 commits), 8 testes verdes (`node --test
  "agents/test/*.test.mjs"`). Os três critérios cobertos por teste. Hub de ensaio montado em `C:\context-hub-ensaio`.
  Provisórios e pendências no relatório da etapa 1 (`etapas/01-esqueleto/relatorio.md`). Falta: revisão do Fiel.
- 2026-10-16 ~20h40 (Trilho): revisão 1 do Fiel: volta (relatório incompleto; hub sem `.git` aceito; `CLAUDE.md` em
  pasta com ponto aceito). Consertado no commit f485974: o `verificar-hub` exige `.git` real com topo na raiz (aceita
  worktree) e procura `CLAUDE.md` em toda pasta menos o `.git`. 11 testes verdes. Relatório completo. Falta: revisão 2.
- 2026-10-16 ~20h50 (Trilho): revisão 2 do Fiel: passa, com ressalva operacional (usar os scripts do repositório, não a
  cópia antiga dentro de `C:\context-hub-ensaio`). Maestro avisado. Falta: junção em `integracao` (maestro).
- 2026-10-16 ~20h55 (maestro): **resolvido.** Parecer do Fiel `etapas/01-esqueleto/parecer-Trilho.md` (rodada 2: passa, com ressalva operacional). Juntado em `integracao` (merge b68f540, worktree de junção `C:\context-hub-wt\integracao`); 11 testes verdes lá. Ressalvas: o ensaio `C:\context-hub-ensaio` guarda a cópia antiga de `agents/bin` e `agents/test` (rodar sempre os scripts do repositório; remontar só em destino vazio); o lugar do código (`agents/bin`, `agents/test` provisórios) espera a rodada `onde-mora-o-codigo-do-hub-r2`; `CLAUDE.md` em `.maestri/` dentro do hub é recusado (ticket 36), a decidir se um workspace do Maestri morar no hub.
