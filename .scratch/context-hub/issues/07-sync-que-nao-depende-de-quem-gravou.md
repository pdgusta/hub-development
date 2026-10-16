# Sync que não depende de quem gravou

Type: research
Status: resolved

## Question

Existe sync pronto que leva para a outra máquina toda edição do hub, inclusive as feitas direto no
disco por qualquer agente, no Windows e no WSL? Candidatas: o modo de git gerenciado do
markdown-vault-mcp (§10.2), o plugin obsidian-git e scripts de auto-commit agendados. Resultado:
adotar uma delas ou criar. Seguir o protocolo da §10.4.

## Answer

Relatório completo: [`pesquisa-07-sync.md`](../../../exploracao/anexos/pesquisa-07-sync.md) (2026-10-01,
fontes primárias e código citados). Resultado: **nenhuma candidata pronta cumpre tudo** (pegar edição
externa, rodar sem ninguém logado, Windows e WSL, avisar o conflito).

- **markdown-vault-mcp (modo gerenciado):** não pega edição externa (commit só dos caminhos que ele
  gravou); pull com rebase sem autostash deve travar com edição externa pendente (não testado); em
  conflito o remoto vence e o local vira `*.conflict-mcp-<ts>.md`; CI só Ubuntu.
- **obsidian-git:** pega edição externa, mas só com o Obsidian aberto; em conflito para e avisa;
  vault no WSL sem suporte oficial.
- **git-sync (simonthum):** commit de tudo, pull, push; se o rebase falha, sai com erro e deixa para o
  humano. Roda em Git Bash e WSL; precisa de agendador e de `syncNewFiles`; avisa só por stdout e
  código de saída. É o mais alinhado com "nada diverge em silêncio".
- **gitwatch:** não confere falha do pull; depende de inotify, que no WSL 2 não vê mudanças do Windows
  em `/mnt/c`.
- **git-auto-sync:** bom no papel, mas relatos de daemon que não commita no Windows; último release 2022.
- **SparkleShare:** sem Windows, fim de vida. **Syncthing / Obsidian Sync / Obsidian Headless:** fora do
  git, registrados só pelo tratamento de conflito.
- **Sugestão do relatório (não decisão):** um sincronizador por máquina no estilo git-sync, disparado
  por intervalo, com o MCP de busca sem ser dono do sync. Em aberto: quem dispara (Agendador do
  Windows ou systemd no WSL) e como a falha vira alerta visível. Isso alimenta "Divergência e edição
  concorrente".
- **Não verificado:** várias instâncias stdio do markdown-vault-mcp no mesmo vault; tarefa agendada sem
  sessão logada.

## Comments

- 2026-10-04 (vinda de "Markdown: vista ou fonte da verdade"): em revisão: as candidatas sincronizam arquivos `.md` pelo git; com a verdade num banco, a pergunta passa a "Sync de banco entre duas máquinas pares".
- 2026-10-13 (vinda de "Revisão do sync e da divergência com o banco", resolvida):
  revisão fechada. O git-sync sai; o sincronizador é o CLI do
  LiveSync como tarefa agendada (no logon, repetindo, uma instância só), que pega o que qualquer agente
  grava no disco sem depender do Obsidian; a falha vira alerta pela vigia de cada máquina.
