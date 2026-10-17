# 38: O ajudante da pasta de ensaio nos testes que ficaram de fora do 36

Type: task
Status: claimed
Etapa: infraestrutura de teste (fora da sequência)
Blocked by: 36

**What to build:** O 36 trocou a limpeza das pastas de ensaio pelo ajudante comum `agents/code/test/pasta-de-ensaio.mjs`
em dez arquivos, e deixou de fora os testes dos ramos abertos naquela hora (08, 10, 15 ponta a ponta, 16, 17) e os
pesados (12, 13). 08, 10 e 15 já estão em `integracao`; 16 e 17 entram em seguida. Trocar o ajudante nesses arquivos
(os `.ps1` com `try/finally` e o `New-EnsaioBanco` que apaga a raiz se cair no meio), a começar pelos já juntados.
Depois da troca, rodar com falha forçada e conferir que nenhuma `hub-ensaio-*` nova sobra em `%TEMP%`.

**Fonte:** ticket 36 (relatório `../etapas/relatorio-36-pasta-de-ensaio.md`, "ficaram para depois da junção").

**Blocked by:** 36 (resolvido)

- [ ] os testes de 08, 10, 12, 13 e 15 (ponta a ponta) usam o ajudante comum; com falha forçada, nenhuma pasta sobra
- [ ] 16 e 17 ganham a troca depois de juntados (mesmo ticket ou comentário dizendo que ficou)
- [ ] a suíte segue verde

## Comments

- 2026-10-17 11h20 (maestro): publicado pela pendência do 36. Dono: o Trilho (livre; o 12, 13, 15 e 16 são dele).
