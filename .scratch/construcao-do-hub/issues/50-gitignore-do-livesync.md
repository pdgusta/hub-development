# 50: O .gitignore do hub cobre os arquivos do LiveSync

Type: task
Status: ready-for-agent
Etapa: conserto do 26 (fora da sequência)
Blocked by: 49

**What to build:** Achado da Brasa no 49 (caso 6): com o par de pé, `.livesync/` e `.livesync-snapshot.json` aparecem
como não rastreados (`??`) no `git status` do hub. Acrescentar os dois ao `.gitignore` do hub, com teste (o `git status`
de um hub de ensaio com o par de pé fica limpo).

**Fonte:** relatório do 49 (`../etapas/relatorio-49-par-novo-com-hub.md`).

- [ ] os dois no `.gitignore`; `git status` limpo com o par de pé
- [ ] a suíte segue verde

## Comments

- 2026-10-18 ~15h (maestro): publicado. Dona: a Brasa, depois do 49.
