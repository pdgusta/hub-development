---
title: Pesquisa 07, sync que não depende de quem gravou
data: 2026-10-01
origem: subagente de pesquisa (Claude Code), ticket "Sync que não depende de quem gravou"
aviso: saída de modelo. Cada afirmação traz a fonte primária (README, docs ou código, com arquivo e linha). Nada foi instalado nem testado.
---

# Sync que não depende de quem gravou: levantamento de 01/10/2026

## Resumo (uma tela)

**Pergunta:** existe sync pronto que leve para a outra máquina **toda** edição do hub, inclusive as feitas direto no disco por qualquer processo, no Windows e no WSL?

**Resposta curta:** não há candidata pronta que cumpra tudo junto: pegar edição externa, rodar sem ninguém logado, funcionar no Windows **e** no WSL e avisar o conflito sem perder nada. As peças existem, mas cada uma falha num ponto:

1. **markdown-vault-mcp (modo git gerenciado) não pega edição externa.** O commit cobre só os caminhos que a própria chamada de ferramenta MCP gravou (`_stage_one` faz `git add -- <path>`; o commit é parcial, com pathspec). Uma edição feita direto no disco por Claude Code, Codex ou Obsidian fica suja no working tree. Pela leitura do código e da doc do git (**não testado**), essa sujeira tende a travar o `git rebase` do pull. O resultado é o estado "unsynced", com uma linha `ERROR` no log e um aviso `remote` nas respostas de escrita. No modo gerenciado o file watcher também é desligado. O CI roda só em Ubuntu; no Windows nativo, o modo gerenciado é **não verificado**.
2. **obsidian-git pega edição externa:** o commit faz `git add -A` na pasta do vault. Mas ele só roda com o Obsidian aberto, e todos os automáticos vêm desligados por padrão (intervalo 0). Num conflito, o commit automático para e aparece um aviso (Notice) com "Resolve conflicts and commit manually". Vault no WSL não tem suporte oficial: há workarounds em issues e um pedido de feature aberto (#1078, abr/2026).
3. **git-sync (simonthum) é a mais aderente à exigência "nada diverge em silêncio".** É um script bash que faz commit de tudo, pull e push, e sai com código ≠ 0 e mensagem a qualquer problema ("will cautiously exit with a useful hint or error"). Roda em WSL/Linux e em Git Bash ("Tested on msysgit"). Não tem gatilho próprio (precisa de cron/systemd/Agendador ou do watcher do `contrib`). Por padrão **para diante de arquivo novo** (é preciso ligar `syncNewFiles`). E o aviso é só o código de saída mais o stdout: quem chama precisa transformar isso em alerta.
4. **gitwatch** usa watcher (inotify) e faz commit de tudo. Mas só faz pull quando há commit local (não há pull periódico), não confere a falha do `pull --rebase` e depende de inotify. No WSL 2, alterações feitas por apps Windows em `/mnt/c` não geram eventos (microsoft/WSL#4739, aberta).
5. **git-auto-sync (GitJournal)** cobre o pedido no papel: watcher, poll de 10 min, aborta o rebase em conflito, para e manda notificação do sistema. Mas o daemon no Windows tem relatos de "não faz commit" até 2024 (issue #7, aberta), e o último release é de 2022.
6. **SparkleShare** guarda as duas versões em conflito e notifica, mas o autor desistiu do Windows e o projeto está em fim de vida (issue #2006).
7. **Fora do git:** o Syncthing cria `*.sync-conflict-*` e propaga essas cópias. O Obsidian Sync faz merge por diff-match-patch por padrão, ou cria "Conflicted copy". Existe também o **Obsidian Headless** (`ob sync --continuous`, beta aberto), que roda sem o app.

**Leitura para o ticket:** o padrão que as fontes sustentam é "um único sincronizador por máquina que faz commit de tudo, falha alto e não decide sozinho" (o desenho do git-sync), com gatilho por intervalo. O watcher não é confiável na fronteira Windows↔WSL. Falta escolher quem roda o sincronizador (Agendador do Windows ou systemd no WSL) e transformar a falha em aviso visível. O MCP de busca ficaria em modo sem git ou só de commit, sem ser dono do sync.

## Tabela comparativa

Legenda: S = sim, P = parcial, N = não, NV = não verificado.

| Candidata | Pega edição externa? | Windows nativo | WSL | Gatilho | Conflito | Como avisa | Exige alguém logado/aberto |
|---|---|---|---|---|---|---|---|
| markdown-vault-mcp, modo gerenciado | **N** (commita só os caminhos da própria ferramenta) | NV (CI só Ubuntu; guia do Claude Desktop tem config Windows, mas sem nota sobre git) | S presumível (Linux; CI Ubuntu) | pull por intervalo (600 s) + webhook (só HTTP/SSE); push adiado (30 s) após escrita | rebase; se o mesmo arquivo mudou dos dois lados, o remoto vence e a versão local vira `*.conflict-mcp-<ts>.md` | campo `remote` em toda resposta de escrita; log `ERROR git_remote_unsynced` na transição; `pull.conflict_files` no `git_sync` | o processo do servidor precisa estar rodando |
| obsidian-git | **S** (`git add -A` no vault) | S (exige Git ≥ 2.29 + Credential Manager) | N oficial; P por workaround (issues #141, #1078) | intervalo, ou "após parar de editar" (eventos do vault), ou no boot | merge (padrão) ou rebase; para e pede resolução manual | Notice + barra de status + console; push bloqueado com "Cannot push. You have conflicts" | **S**: Obsidian aberto |
| git-sync (simonthum) | **S** (`git add -u`; `git add -A` com `syncNewFiles`) | P: Git Bash ("Tested on msysgit") | S (bash) | nenhum próprio: cron/agendador; `contrib` tem inotify, fswatch e modd | ff ou rebase; se o rebase falha, **sai com código 1** e deixa o rebase para o humano | stdout + código de saída ≠ 0; modo `check` | depende do agendador escolhido (NV) |
| gitwatch | **S** (`git add --all .`) | P: só cita `inotify-win` em flag (NV) | S, com ressalva: inotify não vê alterações feitas pelo Windows em `/mnt/c` | watcher (inotify; fswatch no Mac) + espera de 2 s | `pull --rebase` opcional (`-R`) e só depois de commit local; falha não tratada no código | só stdout | processo rodando (há unit systemd e plist de launchd) |
| git-auto-sync (GitJournal) | **S** (README: commit de qualquer mudança) | P: binário existe; daemon com relatos de falha (issue #7) | S presumível (binários Linux; NV no WSL) | watcher + poll de 10 min + retomada após suspensão | só rebase; em conflito **aborta e para de sincronizar o repo** | notificação do sistema ("Git Auto Sync - Conflict") | serviço de usuário (NV no Windows) |
| SparkleShare | S (app de pasta sincronizada sobre git) | P: Windows "sempre atrasado", sem binário no último release | NV | watcher + poll | merge; o servidor vence e a versão local vira cópia "(by <autor>)" | notificação "Resolved a file collision" | app aberto (NV) |
| GitDoc (VS Code) | NV | S presumível (extensão) | NV | 30 s após mudanças; pull ao abrir/push | NV no README | NV | **S**: VS Code aberto |
| Syncthing (não git) | S (watcher + varredura completa a cada 1 h) | S (autostart via Agendador ou pasta Startup) | NV | watcher (atraso de 10 s) + varredura | renomeia o perdedor para `<nome>.sync-conflict-<data>-<hora>-<id>.<ext>` | o arquivo de conflito, que é propagado | serviço rodando |
| Obsidian Sync / Headless (não git) | S no Headless (`--continuous` observa mudanças); NV no app | S | NV | contínuo | Markdown: merge automático (padrão) ou "Conflicted copy" | sync log (filtro "Merge Conflicts"); arquivo de conflito | app aberto ou `ob sync --continuous` |

## markdown-vault-mcp (pvliesdonk), modo git gerenciado

Repositório lido no commit `7dec8e4` (29/09/2026).

**Os três modos.** "**Managed** (`GIT_REPO_URL` + `GIT_TOKEN`) The server owns clone, periodic pull, commit, and deferred push." / "**Unmanaged / commit-only** … The server commits writes (one commit per tool call), but never pulls or pushes." ([docs/guides/git-integration.md](https://github.com/pvliesdonk/markdown-vault-mcp/blob/main/docs/guides/git-integration.md#modes))

**Granularidade do commit.** "the commit boundary is the MCP tool call, not the file." (idem, "What a commit covers")

**Ele faz commit de edição feita fora dele? Não.** No código, `_stage_one` faz stage só do caminho da operação: `["git", "-C", root, "add", "--", literal_pathspec(str(path))]` (`src/markdown_vault_mcp/git/strategy.py`, função em 2137, `add` em ~2176-2181). `_commit_staged` (2378) documenta que o commit é parcial: "``git commit`` without a pathspec commits the **whole index** … Naming the operation's paths makes it a *partial* commit, which leaves every other index entry alone." (~2391-2394). Há uma única brecha, também documentada ali: "An external edit landing in that window is committed instead of left dirty" (~2398). Isso vale só para o **mesmo arquivo** que a ferramenta acabou de gravar, na janela entre o stage e o commit. Edição externa em qualquer outro arquivo fica fora.

**O que acontece no pull com edição externa suja (inferência do código + doc do git, não testado).** O pull é `fetch → classify → ff-only → rebase → sibling` (strategy.py ~907). Com histórico divergente vai direto ao `git rebase <ref>` (~1100), sem `--autostash`. A doc do git diz que é o `--autostash` que permite "run rebase on a dirty worktree" ([git-rebase](https://git-scm.com/docs/git-rebase#Documentation/git-rebase.txt---autostash)), e que "`git pull` and `git merge` will stop without doing anything when local uncommitted changes overlap with files that `git pull`/`git merge` may need to update" ([git-merge](https://git-scm.com/docs/git-merge)). Quando o rebase para por algo que não é conflito de conteúdo, o resolvedor não tem caminhos em conflito para tratar e devolve `conflict_resolution_failed` com "HEAD unchanged" (strategy.py ~1157-1167). O comentário no código diz que esse caso alimenta o estado "unsynced" registrado uma vez em `ERROR`. Leitura provável: **edição externa suja + divergência = sync parado**, visível no log, não silencioso. Não confirmei em execução.

**O file watcher é desligado no modo gerenciado.** "`MARKDOWN_VAULT_MCP_FILE_WATCHER` | `true` | … auto-disabled when git pull is active or a webhook can deliver" ([README](https://github.com/pvliesdonk/markdown-vault-mcp#configuration)). O docstring de `_file_watcher.py` (linhas 1-13) diz "Only mounted when … git pull is disabled". A doc do loop diz que o índice é reconciliado "when the two differ" (HEAD × índice) a cada tick. **NV:** se uma edição externa sem commit chega ao índice no modo gerenciado.

**Conflito.** "The local versions that conflicted are preserved as `<basename>.conflict-mcp-<timestamp>.md` siblings … HEAD advances to the remote tip, so the canonical path now reflects the remote (remote wins)." (git-integration.md, "Conflict outcome: Syncthing-style sibling resolution"). O guia [obsidian-everywhere.md](https://github.com/pvliesdonk/markdown-vault-mcp/blob/main/docs/guides/obsidian-everywhere.md) (linha 132) acrescenta "with `conflict_with` frontmatter on both files".

**Como avisa.**
- Em cada escrita: "While the clone is not reaching its remote, each write result carries a `remote` object with `state`, `reason`, `since`, and a `detail` sentence" (git-integration.md, "When the clone stops reaching its remote").
- No log: "Entering that state logs once at `ERROR`: … `git_remote_unsynced kind=push reason=non_fast_forward`". Push recusado: `WARNING … git_push_failed`.
- A própria doc admite o risco de silêncio: "a vault can run for hours, committing locally, before anything reveals that nothing is replicating."

**Windows nativo.** O CI roda só em `ubuntu-latest` (`.github/workflows/ci.yml`). O guia do Claude Desktop tem config Windows (`C:\\Users\\...`) para o modo **leitura**. O passo "Enable git write support" mostra só config com caminhos POSIX. O askpass do git é gerado como `.sh`, e o comentário em `git/_run.py:62-64` diz que "the script only runs under a POSIX shell". Isso sugere dependência do sh do Git for Windows. **NV:** se o modo gerenciado funciona no Windows nativo.

**Webhook.** Existe só em transporte HTTP/SSE: "Under stdio no HTTP server exists, so nothing is mounted".

## obsidian-git (Vinzent03)

Repositório lido no commit `19182f7` (01/10/2026).

**Automáticos.** "There are multiple ways to trigger an automatic commit-and-sync. The default is a basic interval … Another method is to enable "Auto commit-and-sync after stopping file edits"." ([docs/Features.md](https://github.com/Vinzent03/obsidian-git/blob/master/docs/Features.md), linhas 41-45). Padrões em `src/constants.ts:14-17`: `autoSaveInterval: 0`, `autoPushInterval: 0`, `autoPullInterval: 0`, `autoPullOnBoot: false`, ou seja, **tudo desligado de fábrica**. O padrão de pull é `syncMethod: "merge"` (`constants.ts:28`).

**Precisa do Obsidian aberto.** "If you close Obsidian before the interval end, the commit-and-sync will automatically run the next time you start Obsidian." (Features.md:41). É um plugin do Obsidian: sem o app aberto, nada roda.

**Pega edição externa? Sim, no commit.** `commitAll` faz `git add -A` no caminho do vault: `await this.git.add(vaultPath == undefined ? "-A" : ["-A", "--", vaultPath]);` (`src/gitManager/simpleGit.ts:671-674`). Qualquer arquivo alterado no disco entra, seja quem for o autor. O modo "after stopping file edits" é disparado por eventos `this.app.vault.on("modify" | "create" | "delete" | "rename")` (`src/main.ts:275-298`). **NV:** se edição feita fora do Obsidian dispara esses eventos (depende do watcher do próprio Obsidian). O modo por intervalo não depende disso.

**Conflito.**
- Pull com merge ou rebase. A falha vira `GitConflictError` (`simpleGit.ts:829-862`).
- O handler mostra: "Merge conflict in N files. Resolve conflicts and commit manually." (`src/main.ts:689-698`).
- O commit automático para: "Automatic commit stopped because of unresolved conflicts" (`src/gitActions.ts:547-553`).
- O push é bloqueado: "Cannot push. You have conflicts in N files" (`gitActions.ts:826-830`).
- Há também um modo "reset/Other sync service", que só move o HEAD (Tips-and-Tricks.md:37).

**Como avisa.** `displayError` cria `new Notice(...)` se `showErrorNotices` estiver ligado, faz `console.error` e mostra a mensagem na barra de status (`src/main.ts:797-802`). Há ainda marcação de blocos de conflito no editor (`src/editor/conflicts/`).

**Windows.** "Installing GitHub Desktop is **not** enough! You need to install regular Git as well. … Ensure you are using Git 2.29 or higher." ([docs/Installation.md](https://github.com/Vinzent03/obsidian-git/blob/master/docs/Installation.md):21-29). Também é preciso o Git Credential Manager (Authentication.md:25).

**WSL.** A documentação não fala de WSL. O código tem só um comentário: "in case git resides in a different filesystem (eg, WSL)" (`simpleGit.ts:145-146`).
- Issue [#141](https://github.com/Vinzent03/obsidian-git/issues/141) (fechada): o mantenedor diz "I haven't tested it with wsl", e usuários relatam workarounds com wrapper `.cmd` e junction `C:\mnt`.
- Issue [#1078](https://github.com/Vinzent03/obsidian-git/issues/1078) (**aberta**, 30/04/2026): wrapper `.cmd` para git do WSL falha com `spawn EINVAL`.
- Conclusão: vault no WSL não tem suporte oficial.

## git-sync (simonthum)

Repositório lido no commit `b991840` (10/09/2025).

**Proposta.** "It is safe, small, requires nothing but git and bash … It is non-interactive, but will cautiously exit with a useful hint or error if there is any kind of problem." / "resort to manual intervention as soon as something non-trivial occurs." ([README](https://github.com/simonthum/git-sync))

**Plataformas.** "Tested on msysgit and a real bash." Então roda em Git Bash no Windows e em bash no WSL. Há ainda uma implementação em TypeScript ([git-sync-js](https://github.com/tiddly-gittly/git-sync-js), **NV**).

**Pega edição externa? Sim.** O commit padrão é "`git add -u ; git commit -m "changes from $(uname -n) on $(date)"`". Com `syncNewFiles`, vira `git add -A`. **Atenção:** sem `syncNewFiles`, arquivo novo é obstáculo: "Normally you have to commit those yourself … git-sync will exit at stage 3 with an explanation". Agentes criam arquivos novos o tempo todo, então `syncNewFiles` (ou `-n`) é obrigatório no hub.

**Fluxo.** "Relate upstream to ours. If ahead, push. If behind, fast-forward. If diverged, rebase, then push." Os branches precisam ser habilitados uma vez (`branch.$name.sync` ou `-s`).

**Conflito.** Em `git-sync` (script, linhas 426-436): em caso de divergência roda `git rebase`. Se falhar: `__log_msg "Rebasing failed, likely there are conflicting changes. Resolve them and finish the rebase before repeating git-sync."` e `exit 1`. O rebase fica pendente para o humano. As próximas execuções recusam: "The repository must not be in the middle of a rebase".

**Como avisa.** Só stdout (`echo git-sync: $1`, linha 81) e código de saída. O modo `check` "will indicate if synchronization may start … (indicated by text and non-zero exit code)". Transformar isso em notificação fica por conta de quem chama.

**Gatilho.** O script não tem gatilho próprio. O `contrib/` traz `git-sync-on-inotify` (inotify + poll `GIT_SYNC_INTERVAL`, padrão 500 s), `git-sync-on-fswatch` e `modd.conf`. Sobre o modd: "will not poll upstream except on startup". **NV:** rodar via Agendador de Tarefas do Windows ou systemd timer no WSL (não há doc do projeto sobre isso).

## gitwatch

Repositório lido no commit `04735cf` (13/08/2026).

**Requisitos.** "`git` … `inotifywait` (part of inotify-tools)"; no Mac, `fswatch` ([README](https://github.com/gitwatch/gitwatch#requirements)). O único traço de Windows é a flag `-e`: "(useful when using inotify-win, e.g. -e modify,delete,move)" (`gitwatch.sh:103`). **NV** no Windows nativo.

**Pega edição externa? Sim.** "case directory: … `git add --all .` … `git commit -m "Scripted auto-commit on change (<date>)"` … if a remote is defined (with `-r`) do a push after the commit" (README, "What it does").

**Pull.** Só com `-R`: "a 'git pull --rebase <remote>' is done before any push" (`gitwatch.sh:74`). O pull roda **dentro** do bloco que só executa quando há mudança local (`gitwatch.sh:416-442`). Então não há pull periódico: a máquina parada não recebe nada. O retorno do `eval "$PULL_CMD"` não é verificado (`gitwatch.sh:433-437`). Um rebase que falha fica pendente, e o script segue para o push (inferência do código, **não testado**). A flag `-M` evita commit durante merge, mas checa só `MERGE_HEAD` (`gitwatch.sh:152`), não rebase.

**Como avisa.** Só stdout/verbose. Há opção de log das mudanças no commit (`-l`), não de alerta.

**WSL.** inotify funciona no ext4 do WSL. Para arquivos em `/mnt/c` alterados por apps Windows, a issue [microsoft/WSL#4739](https://github.com/microsoft/WSL/issues/4739), "[WSL2] File changes made by Windows apps on Windows filesystem don't trigger notifications for Linux apps", está **aberta** desde 2019. **NV:** se edições feitas pelo Windows via `\\wsl$` em arquivos no ext4 disparam inotify.

## git-auto-sync (GitJournal)

Repositório lido no commit `4c47aba` (23/06/2022). Último push no GitHub em 16/07/2024; último release v1.5 em 10/06/2022.

**Proposta.** "automatically commit changes to your git repo, and always keep that repo up to date. This way you can use any editor with your text files" ([README](https://github.com/GitJournal/git-auto-sync)). Pega edição externa por definição.

**Gatilho.** "This process will monitor the filesystem, poll every 10 minutes, and additionally try to sync on resuming from a suspend."

**Conflito.** "GitAutoSync current only supports rebases … In the case of a rebase conflict, it will abort and stop syncing that repo. It will send a system notification to inform you of the conflict." No código: `rebase --abort` (`common/rebase.go:32`) e `beeep.Alert("Git Auto Sync - Conflict", "Could not rebase for - "+repoPath, ...)` (`common/autosync.go:32`).

**Windows.** Há binário `Windows_x86_64` no release v1.5. O daemon é um serviço via `kardianos/service` com `UserService: true` (`common/service.go`). A issue [#7](https://github.com/GitJournal/git-auto-sync/issues/7) ("Deamon registration fails on Windows 11", **aberta**) tem relatos depois da correção de 1.5: "the daemon appears to start and monitor the folder, but it doesn't actually ever do commits" (30/07/2024). O `sync` manual funciona. O mantenedor: "I've mostly only tested this on MacOS, and Linux."

## SparkleShare

Repositório lido no commit `9b10379` (01/09/2026).

**Situação.** "I don't have an interest in the Windows platform, which explains why the Windows release has always been lagging behind. The final release tag will be `3.38.1`. Though I will not produce any binaries for it." ([issue #2006](https://github.com/hbons/SparkleShare/issues/2006)). O README ainda diz "available for Linux distributions, macOS, and Windows". O autor anuncia uma reescrita em Rust em 2026.

**Conflito.** "UU unmerged, both modified -> Use server's, save ours as a timestamped copy" (`Sparkles/Git/Git.Repository.cs:482-494`). As cópias recebem o sufixo `" (by {0})"` com o nome do autor, ou `(A)`/`(B)` (`:541-546`). O aviso é `AlertNotificationRaised ("Resolved a file collision", "Local and server versions were kept.")` (`SparkleShare/Common/BaseController.cs:477-479`).

## GitDoc (extensão do VS Code)

"automatically commit/push/pull changes on save" / "it will create commits every 30s, _whenever there are actually changes_" / "automatically pull changes from the repo when you 1) open the workspace, and 2) push changes" ([README](https://github.com/lostintangent/gitdoc)). Exige o VS Code aberto. **NV:** se pega mudança feita por outro processo, e como trata conflito (o README não descreve).

## Outras achadas, sem maturidade (registro)

- [Abhiprayaa29/autosync-git](https://github.com/Abhiprayaa29/autosync-git): criado em 24/09/2026, 0 estrelas, README em indonésio. Declara `git pull --rebase --autostash`; em conflito "rebase otomatis diabort, push ditahan, sinkronisasi jeda 120 detik, dan di Windows muncul notifikasi balloon"; log `.autosync.log`; Scheduled Task "jalan tiap login". Interessante como desenho; **não verificado** além do README.
- Rogit-28/Auto-Commit-Local e anuvgupta/git-autosync: apareceram na busca com 0 estrelas. **Não lidos.**

## Alternativas que não são git (só registro)

**Syncthing.** "When a file has been modified on two devices simultaneously and the content actually differs, one of the files will be renamed to `<filename>.sync-conflict-<date>-<time>-<modifiedBy>.<ext>`." / "files are treated as normal files after they are created, so they are propagated between devices." ([docs users/syncing.rst](https://docs.syncthing.net/users/syncing.html#conflicting-changes)). Detecção: "By default the watcher is enabled and full scans are done once per hour … it is possible that some changes aren't picked up by it." Windows: "There is currently no official installer available for Windows", com autostart via Agendador ou pasta Startup ([users/autostart.rst](https://docs.syncthing.net/users/autostart.html)). Não achei na doc orientação sobre sincronizar a pasta `.git` (**NV**).

**Obsidian Sync.** "**Markdown files**: Obsidian Sync merges the changes using Google's diff-match-patch algorithm." A opção "Create conflict file" gera `original-note-name (Conflicted copy device-name YYYYMMDDHHMM).md` (help: [Troubleshoot Obsidian Sync](https://help.obsidian.md/sync/troubleshoot)). Há um sync log com filtro "Merge Conflicts" (Status icon and messages). Plataformas: "Windows, macOS, Linux, Android and iOS". **Obsidian Headless** (beta aberto): `ob sync --continuous` "Run continuously, watching for changes", `--conflict-strategy merge|conflict`. Aviso: "Do not use *both* the desktop app Sync and Headless Sync on the same device" ([Headless Sync](https://help.obsidian.md/sync/headless)). O Obsidian também diz não recomendar outro serviço de sync junto.

## Como cada uma torna visível a divergência

| Candidata | Mecanismo |
|---|---|
| markdown-vault-mcp | resposta da ferramenta (`remote`), log `ERROR` na transição, arquivo irmão `*.conflict-mcp-*`, `pull.conflict_files` |
| obsidian-git | Notice + barra de status + console; marcadores no editor; push bloqueado |
| git-sync | código de saída ≠ 0 + mensagem no stdout; modo `check` |
| gitwatch | só stdout (falha de pull não tratada) |
| git-auto-sync | notificação do sistema + para o repo |
| SparkleShare | notificação + duas cópias "(by …)" |
| Syncthing | arquivo `.sync-conflict-*` (propagado) |
| Obsidian Sync | sync log + merge silencioso (padrão) ou arquivo "Conflicted copy" |

## Lacunas e não verificado

- **markdown-vault-mcp:**
  - comportamento real do pull com edição externa suja (inferido do código e da doc do git, não executado);
  - se o índice enxerga edição externa sem commit no modo gerenciado;
  - modo gerenciado no Windows nativo (CI só Ubuntu; askpass `.sh`);
  - várias instâncias do servidor (uma por sessão de agente em stdio) sobre o mesmo vault, cada uma com seu loop de pull: a doc não trata disso.
- **obsidian-git:**
  - se edição externa dispara o modo "after stopping file edits";
  - qualquer configuração com vault no WSL.
- **git-sync:**
  - uso real com Agendador do Windows ou systemd timer no WSL, e se a tarefa exige sessão logada (não consultei a doc do Agendador);
  - comportamento do `git-sync-on-fswatch` no Windows.
- **gitwatch:**
  - Windows nativo (inotify-win);
  - inotify para escritas vindas do Windows via `\\wsl$` em arquivos no ext4.
- **git-auto-sync:** se o daemon funciona hoje no Windows 11 (os relatos dizem que não, até 2024); comportamento no WSL.
- **GitDoc:** conflito e edição externa.
- **Syncthing:** sincronizar uma árvore com `.git` dentro.
- **Fora do escopo desta leitura:**
  - o quanto o WSL 2 mantém a VM viva para um serviço sem sessão aberta;
  - Git Credential Manager em tarefa agendada sem login.

## Consultas

Buscas na web (WebSearch):
1. `automatic git commit pull push sync folder Windows tool watcher conflict`
2. `git auto sync notes between computers windows daemon "auto commit" github`

Microsoft Learn (microsoft_docs_search):
3. `WSL file system notifications inotify Windows files /mnt/c Linux tools not notified of changes`

API de busca do GitHub (issues):
4. `repo:pvliesdonk/markdown-vault-mcp external commit`
5. `repo:Vinzent03/obsidian-git wsl`
6. `repo:GitJournal/git-auto-sync windows`
7. leitura direta das issues: Vinzent03/obsidian-git #141 e #1078; GitJournal/git-auto-sync #7; hbons/SparkleShare #2006; microsoft/WSL #4739

Leitura de fonte (clone raso no scratchpad, só leitura; grep e sed):
8. pvliesdonk/markdown-vault-mcp: README, `docs/guides/git-integration.md`, `docs/guides/obsidian-everywhere.md`, `docs/guides/claude-desktop.md`, `docs/configuration.md`, `src/markdown_vault_mcp/git/strategy.py`, `git/_run.py`, `_file_watcher.py`, `.github/workflows/ci.yml`; buscas `add|stash|autostash|porcelain|rebase|ff-only`, `autostash|dirty|uncommitted|external edit`, `windows|wsl|win32`, `multiple instances|same vault`
9. Vinzent03/obsidian-git: README, `docs/*.md`, `src/main.ts`, `src/gitActions.ts`, `src/gitManager/simpleGit.ts`, `src/constants.ts`; buscas `conflict|wsl|merge strategy|rebase`, `vault.on|registerEvent`
10. simonthum/git-sync: README, script `git-sync`, `contrib/`
11. gitwatch/gitwatch: README, `gitwatch.sh`; buscas `windows|wsl|inotify|pull|rebase|conflict`
12. GitJournal/git-auto-sync: README, `common/service.go`, `common/rebase.go`, `common/autosync.go`; metadados do release v1.5
13. hbons/SparkleShare: README, `Sparkles/Git/Git.Repository.cs`, `SparkleShare/Common/BaseController.cs`
14. syncthing/docs: `users/syncing.rst`, `users/config.rst`, `users/autostart.rst`, `users/faq-parts/*.rst`
15. obsidianmd/obsidian-help: `en/Obsidian Sync/*.md` (busca `conflict`, `windows`, `continuous`)
16. lostintangent/gitdoc: README (busca `pull|conflict|interval|external`)
17. Abhiprayaa29/autosync-git: README (busca `conflict|abort|notif|windows|autostash`)
18. git/git: `Documentation/git-rebase.adoc` (`--autostash`) e `Documentation/git-merge.adoc` (mudanças não commitadas)
