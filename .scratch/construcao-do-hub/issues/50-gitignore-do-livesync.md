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
- 2026-10-18 ~15h35 (Brasa): o Gustavo pediu no terminal da Brasa ("pode adicioná-los"); feito no ramo `ticket-49`,
  commit c3f2868: os dois no `.gitignore` do hub, e o caso 6 do teste do 49 confere o `git status` limpo com o par de
  pé (sem o filtro de `?? .livesync/`; sem nova rodada com Docker). Conferido sem Docker: hub do `montar.mjs` com
  `.livesync/ignore` e `.livesync-snapshot.json` dá `git status` vazio. Junta com o 49.
- 2026-10-18 ~15h55 (Brasa, parecer do Fiel r1): a causa certa do `.livesync/` no `git status` do caso 6 é a ordem. O
  gerador de exclusões só grava `.*` no `.git/info/exclude` se o `.git` já existe, e ali rodou antes do `git init`. O
  `C:\context-hub` do A tem o bloco e não mostra o `.livesync`. O c3f2868 fica (inócuo; cobre um hub sem o bloco). O
  conserto de fundo está na receita do 49 (o 04 de novo depois do git).
