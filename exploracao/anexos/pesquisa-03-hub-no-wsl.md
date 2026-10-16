---
title: Pesquisa 03 — Hub no WSL: comportamento das ferramentas
data: 2026-10-01
ticket: "Hub no WSL: comportamento"
método: só fontes primárias (docs oficiais, repositórios e issues oficiais), conferidas pelo trecho exato. Nada instalado, nenhum teste rodado.
---

# Pesquisa 03 — Hub no WSL: comportamento das ferramentas

Pergunta: como cada ferramenta se comporta com o hub **dentro do WSL 2** (ext4, acessado do Windows por
`\\wsl$` / `\\wsl.localhost`) e com o hub **no Windows** (NTFS, acessado de dentro do WSL por `/mnt/c`)?

Convenção: "**Fato**" = trecho conferido na fonte primária (citação curta + URL). "**Relato**" = issue ou
fórum oficial com relato de usuário, sem confirmação do fabricante. "**Inferência**" = dedução minha a partir
de fatos citados. "**Não verificado**" = não conferi na fonte primária.

---

## Resumo de uma tela (o que a pesquisa permite afirmar)

1. **A Microsoft recomenda guardar os arquivos no sistema de arquivos do lado de quem trabalha neles**, e
   ambos os cruzamentos (`/mnt/c` a partir do Linux e `\\wsl$` a partir do Windows) usam o protocolo 9P e
   são lentos. O WSL 2 é pior que o WSL 1 justamente em "performance across OS file systems".
2. **Detecção de mudança não atravessa a fronteira de forma confiável, nos dois sentidos:**
   - Linux observando `/mnt/c`: mudanças feitas por apps Windows **não** geram inotify no WSL 2 (issue
     oficial #4739, aberta desde 2019, rótulo `feature`).
   - Windows observando `\\wsl$`: `ReadDirectoryChangesW` não é suportado nesses caminhos (issue oficial
     #7674, aberta, rótulo `feature`). A biblioteca `notify` (Rust, usada pelo grooveseek) e o próprio
     grooveseek dizem que watchers em WSL/rede não são garantidos; chokidar e watchdog mandam usar polling.
3. **Obsidian para Windows com cofre em `\\wsl.localhost`**: há pedido de suporte aberto no fórum oficial
   desde 2020 (movido pela equipe para "Feature requests") e relatos de erro `EISDIR ... watch` ao abrir o
   cofre. A ajuda oficial não menciona WSL. Para o caminho inverso (cofre no NTFS), a ajuda diz que o
   Obsidian "automatically refreshes your vault to keep up with any external changes".
4. **Agentes:**
   - **Claude Code** suporta Windows nativo e WSL 2. A doc do Desktop diz que mexer em arquivos do WSL a
     partir do Windows "goes through a network filesystem, which is slow and breaks file watching". `\\wsl$`
     não conta como caminho de rede, então é aceito como diretório de trabalho. O sandbox só existe no WSL 2.
   - **Codex**: a doc recomenda o agente nativo do Windows e diz que, nele, guardar projetos no NTFS e
     acessá-los do WSL por `/mnt/<drive>` "is more reliable than opening projects directly from the WSL
     filesystem". Há issues abertas (set/2026) do sandbox nativo falhando em workspace `\\wsl.localhost`.
   - **OpenCode** recomenda rodar dentro do WSL e mostra o fluxo com o projeto em `/mnt/c`, com a dica de
     clonar no ext4 "for the smoothest experience".
   - **Maestri** (doc oficial encontrada): tem ambiente **WSL** de primeira classe no Maestri para Windows
     (WSL 1 e 2), via `wsl.exe` e um relay Linux nativo, com caminhos mantidos em formato Linux.
5. **git**: o cruzamento traz três pegadinhas documentadas: fim de linha (Microsoft manda alinhar via
   `.gitattributes`), modo de arquivo (o `core.fileMode` é sondado no clone e pode precisar de `false` quando
   outro ambiente "perde" o bit executável) e `safe.directory` (o Git for Windows registra que, em
   diretórios WSL, "the ownership check fails"). O fsmonitor do git recusa repositórios em rede por padrão.
6. **SSH**:
   - **No WSL 2**, a rede padrão é NAT. Acesso pela LAN exige `netsh portproxy` ou o modo **mirrored**
     (Win 11 22H2+, com regra no firewall Hyper-V). O WSL desliga quando ocioso (padrão de 15 s por
     distribuição e 60 s para a VM, configuráveis). Serviços do systemd "will NOT keep your WSL instance
     alive". Uma nota antiga de release diz que as instâncias terminam no logoff.
   - **No Windows**, o OpenSSH Server é recurso nativo, mantido pelo Windows Update e com regra de
     firewall criada na instalação. Pegadinhas documentadas:
     - chaves de administradores ficam num arquivo próprio com ACL restrita;
     - contas Entra ID não suportam autenticação por chave;
     - sessão aberta por chave não tem credenciais para autenticar para fora;
     - o shell padrão é `cmd.exe`;
     - `git clone` por SSH contra um servidor Windows tem "known issue" com o `cmd` como shell padrão.
   - **Chamar `wsl.exe` de dentro de uma sessão SSH do Windows** (sessão 0) é issue oficial aberta. A
     correção parcial passa por `C:\Program Files\WSL\wsl.exe`.

**O que a pesquisa NÃO permite afirmar** (ver "Lacunas"):
- se o Obsidian atual (v1.13.x) ainda falha em `\\wsl.localhost`;
- desempenho medido de git ou busca no tamanho do hub;
- como Notes, File Tree e busca do Maestri se comportam num workspace WSL;
- se o inotify do Linux vê escritas feitas pelo Windows via `\\wsl$` (é plausível pela arquitetura, mas
  não há doc).

---

## 1. Obsidian (app desktop Windows) com cofre em `\\wsl.localhost\...`

**Documentação oficial (help do Obsidian):**
- A ajuda oficial **não menciona WSL**. Fiz grep no repositório oficial da ajuda (`obsidianmd/obsidian-help`,
  ramo `master`, atualizado em 2026-09-29), pasta `en/`, por WSL, UNC, *network drive*, *file watch*: não há
  nada sobre WSL ou `\\wsl$`.
- **Fato:** o Obsidian acompanha mudanças externas: "Obsidian automatically refreshes your vault to keep up
  with any external changes." ([How Obsidian stores data](https://obsidian.md/help/data-storage))
- **Fato:** para quem usa Sync, a recomendação de local no Windows é "`D:\` or any other non-C, non-network
  drive on your device", depois `C:\Vaults`. ([Switch to Obsidian Sync](https://obsidian.md/help/sync/switch))
- **Fato:** links simbólicos de arquivo: "Changes performed outside of Obsidian aren't watched for, so if you
  change the file directly, Obsidian won't detect the change". ([Symbolic links and junctions](https://obsidian.md/help/symlinks))
  Importa se alguém pensar em "cofre no Windows apontando por symlink para o WSL".

**Fórum oficial (única fonte sobre WSL):**
- **Fato (status):** o tópico "Support for vaults in Windows Subsystem for Linux (WSL)" foi aberto em
  2020-11-15. Um membro da equipe respondeu "I am gonna move this to feature requests". Ele segue **aberto**,
  com 79 posts. O último é de 2026-09-16 ("Happy almost six years with no movement").
  (<https://forum.obsidian.md/t/support-for-vaults-in-windows-subsystem-for-linux-wsl/8580>)
- **Fato (status):** o bug "Can't create or open vault in WSL folder" (2022-03-26) foi **fechado pela equipe**
  como duplicado do pedido acima ("Please search before posting").
  (<https://forum.obsidian.md/t/cant-create-or-open-vault-in-wsl-folder/34688>)
- **Relato:** o erro relatado é
  `Error: EISDIR: illegal operation on a directory, watch '\\wsl.localhost\Ubuntu\home\...'`. Um usuário
  atribui a falha "specifically with the watcher" (post 7, 2021). Outro relata em 2023-03 que o erro persiste
  no Windows 11 + WSL2, embora a pasta `.obsidian` seja criada (post 34). Um terceiro relata em 2022-04 que
  "works fine" num build *dev* do Windows 11 (post 18). Os relatos são **contraditórios**, e nenhum é da equipe.
- **Relato:** a alternativa citada no fórum é rodar o Obsidian **Linux** dentro do WSL via WSLg. Usuários
  relatam problemas de escala em monitores de alta resolução, IME/fontes, colar imagens e GPU (posts 52,
  57, 58, 67, 80).
- **Fato (viabilidade da alternativa):** o Obsidian publica builds Linux (`.deb`, `.AppImage`) nas releases
  oficiais (ex.: v1.13.7, 2026-08-12, <https://github.com/obsidianmd/obsidian-releases/releases>). O WSL
  roda apps GUI Linux "in a fully integrated desktop experience"
  ([Run Linux GUI apps](https://learn.microsoft.com/windows/wsl/tutorials/gui-apps)).
- **Inferência:** o erro `watch` bate com o fato documentado no item 5: `ReadDirectoryChangesW` não é
  suportado em `\\wsl$` (WSL #7674).

**Hub no Windows e Obsidian no Windows:** é o caso nativo. A detecção de mudanças feitas por agentes no WSL
via `/mnt/c` **não está verificada** em fonte primária.
**Inferência:** no WSL 2, `/mnt/c` é servido por um servidor 9P do lado Windows, então as escritas chegam ao
NTFS por um processo Windows e deveriam gerar notificações normais.

---

## 2. Maestri

Fonte primária encontrada: documentação oficial em <https://www.themaestri.app/en/docs/>. Li as 21 páginas e
fiz grep por WSL e Windows.
- **Fato:** "Maestri runs on macOS and Windows." ([Introduction](https://www.themaestri.app/en/docs/intro))
- **Fato:** entre os tipos de ambiente: "WSL — Windows only. A Linux distribution on the same machine. Runs
  through wsl.exe with a native Linux relay. Discovered from the installed distributions."
  ([Environments](https://www.themaestri.app/en/docs/environments))
- **Fato:** "WSL connects a workspace or terminal to a Windows Subsystem for Linux distribution installed on
  the same machine. WSL 1 and WSL 2 both work." Ele é ativado em *Settings > General > Environments >
  WSL workspaces*. (mesma página)
- **Fato (configuração):** a folha WSL tem *Distro* e *User*. "Maestri passes the user per launch. It never
  writes /etc/wsl.conf and never changes the distribution's own default". (mesma página)
- **Fato (funcionamento):** "WSL terminals do not use the TCP Bridge Port. Maestri provisions a native Linux
  relay binary into the distribution". A primeira entrada "can take a moment while WSL starts its virtual
  machine". "Skills are installed per distribution". (mesma página)
- **Fato (caminhos):** "Set the working directory as it exists inside the distribution, such as
  /home/you/project or ~ . Maestri keeps these paths in their Linux form and does not check them against the
  Windows filesystem." (mesma página)
- **Fato (página Windows):** "Point a workspace at a WSL distro, an SSH server, or a Docker container and
  your agents run there. Roles, agent connections, and the maestri CLI go with them."
  (<https://www.themaestri.app/en/windows>)
- **Fato (floors no Windows):** "In Maestri for Windows, a floor is isolated on its own git branch instead"
  (em vez de clone APFS). ([Floors](https://www.themaestri.app/en/docs/floors))
- **Fato (ausência):** as seções "Persistent sessions" e "Shared Maestri behavior" listam SSH, Docker
  Container, Docker Sandbox e Custom Runtime, mas **não** citam WSL. Para persistência local, a doc indica
  "Local (tmux)".
- **Não verificado:**
  - se os nós de Notes, File Tree (diff), Batuta Search e o `#` do Prompt Composer funcionam com workspace
    WSL. A doc do Prompt Composer só cita SSH e container;
  - se um workspace *Local* com pasta `\\wsl.localhost\...` funciona;
  - se o Maestri observa arquivos (watch) nesses casos.

---

## 3. Claude Code, Codex CLI e OpenCode

### 3.1 Claude Code (docs da Anthropic)

- **Fato:** "You can run Claude Code natively on Windows or inside WSL." A tabela diz:
  - Native Windows: sandboxing "Not supported";
  - WSL 2: "Supported";
  - WSL 1: "Not supported".

  ([Setup](https://code.claude.com/docs/en/setup))
- **Fato:** no WSL, "You install and launch `claude` inside the WSL terminal, not from PowerShell or CMD."
  (mesma página)
- **Fato (WSL acessando `/mnt/c`):** "Disk read performance penalties when working across file systems on WSL
  may result in fewer-than-expected matches when using Claude Code on WSL. Search still functions, but returns
  fewer results than on a native filesystem." `claude doctor` mostra Search como OK mesmo assim. As soluções
  são mover para `/home/` ou "Use native Windows instead".
  ([Troubleshooting](https://code.claude.com/docs/en/troubleshooting))
- **Fato (Windows acessando o WSL):** "Use a WSL session when your repository lives inside the distribution's
  filesystem. Working on those files from Windows goes through a network filesystem, which is slow and breaks
  file watching; running the session inside the distribution avoids both."
  ([Claude Code Desktop in WSL](https://code.claude.com/docs/en/desktop-wsl))
- **Fato (Desktop + WSL):**
  - exige WSL 2;
  - um `\\wsl.localhost\...` aberto pelo seletor "reopens inside that distribution";
  - ainda indisponíveis: "the integrated terminal, connectors and plugins, session forking, the file browser
    pane, and file suggestions when you type `@`";
  - "On devices managed by an organization, WSL sessions may be unavailable."

  (mesma página)
- **Fato (CLI nativo com pasta no WSL):** o Claude Code recusa caminhos de rede como diretório de trabalho,
  mas "Mapped drive letters and `\\wsl$` paths don't count as network paths."
  ([Errors](https://code.claude.com/docs/en/errors)) O mesmo vale para symlink de `CLAUDE.md`:
  "`\\wsl$` paths don't count as network paths." ([Memory](https://code.claude.com/docs/en/memory))
  - **Não verificado:** se a regra cobre `\\wsl.localhost` com a mesma redação. A doc só cita `\\wsl$`.
- **Fato (sandbox):** "The sandbox is built into Claude Code and runs on macOS, Linux, and WSL2. Native
  Windows is not supported." ([Sandboxing](https://code.claude.com/docs/en/sandboxing))
- **Fato (políticas separadas):** "By default, WSL reads only the Linux file path at `/etc/claude-code`." Para
  herdar a política do Windows, existe `wslInheritsWindowsSettings: true`.
  ([Admin setup](https://code.claude.com/docs/en/admin-setup))
  - **Inferência:** a configuração e a memória do usuário (`~/.claude`) dentro do WSL ficam na home Linux,
    separadas das do Windows. Não achei frase explícita.
- **Fato (login):** em WSL2, o callback OAuth pode não voltar. Cola-se o código, ou define-se `BROWSER` para o
  navegador do Windows. ([Troubleshoot install](https://code.claude.com/docs/en/troubleshoot-install))

### 3.2 OpenAI Codex (CLI, app e extensão)

- **Fato:** "Use the native Windows sandbox by default. Choose WSL when you need Linux-native tooling, your
  workflow already lives in WSL2, or neither native Windows sandbox mode meets your needs."
  ([Windows](https://developers.openai.com/codex/windows))
- **Fato:** "When you use WSL2, Codex runs inside the Linux environment instead of using the native Windows
  sandbox." "Starting in Codex `0.115`, the Linux sandbox moved to `bubblewrap`, so WSL1 is no longer
  supported." ([WSL](https://developers.openai.com/codex/windows/wsl))
- **Fato (WSL acessando `/mnt/c`):** "Working in Windows-mounted paths like `/mnt/c/...` can be slower than
  working in Windows-native paths. Keep your repositories under your Linux home directory ... for faster I/O
  and fewer symlink and permission issues". (mesma página)
- **Fato (agente nativo e projeto no WSL):** "If you plan to keep using the Windows-native agent, prefer
  storing projects on your Windows filesystem and accessing them from WSL through `/mnt/<drive>/...`. This
  setup is more reliable than opening projects directly from the WSL filesystem."
  ([Windows app](https://learn.chatgpt.com/docs/windows/windows-app.md))
- **Fato:** o agente WSL no app é escolhido em Settings e "doesn't take effect until you restart". (mesma página)
- **Fato (máquina gerenciada):** o sandbox `elevated` depende de "administrator-approved setup", e "Some
  enterprise-managed devices block the required setup steps". O `unelevated` é o fallback.
  ([Windows](https://developers.openai.com/codex/windows))
- **Relato (issues oficiais abertas):**
  - [openai/codex#46640](https://github.com/openai/codex/issues/46640) (2026-09-19, rótulos `bug`,
    `windows-os`, `sandbox`): com o agente nativo e o projeto em `\\wsl.localhost\Ubuntu-24.04\...`, "the
    Windows sandbox attempts to apply Windows ACLs to the WSL UNC workspace and fails before the task starts".
  - [openai/codex#47115](https://github.com/openai/codex/issues/47115) (2026-09-21): "Agent Environment is
    global rather than per-project", o que dificulta misturar projetos Windows e WSL.

### 3.3 OpenCode

- **Fato:** "While OpenCode can run directly on Windows, we recommend using Windows Subsystem for Linux (WSL)
  for the best experience." O motivo: "better file system performance, full terminal support, and
  compatibility with development tools". ([Windows (WSL)](https://opencode.ai/docs/windows-wsl), atualizado em 2026-10-01)
- **Fato (WSL acessando `/mnt/c`):** a doc mostra `cd /mnt/c/Users/YourName/project` e `opencode`, e diz
  "Keep OpenCode running in WSL for projects stored on Windows drives - file access is seamless". Mas
  recomenda: "For the smoothest experience, consider cloning/copying your repo into the WSL filesystem".
  (mesma página)
- **Fato:** "Your OpenCode config and sessions are stored within the WSL environment at
  `~/.local/share/opencode/`". O app Desktop do Windows pode se conectar a um `opencode serve` no WSL. Com
  `--hostname 0.0.0.0`, a doc manda definir `OPENCODE_SERVER_PASSWORD`. (mesma página)
- **Relato (issues oficiais):**
  - [anomalyco/opencode#22215](https://github.com/anomalyco/opencode/issues/22215): com o projeto via
    `\\wsl$\...` no OpenCode nativo, "tools like bash, file search, and git all break". Fechada como
    *not planned*.
  - [#19473](https://github.com/anomalyco/opencode/issues/19473): o Desktop envia caminhos UNC ao servidor
    WSL. Também fechada como *not planned*.
  - O motivo do fechamento não foi verificado.

---

## 4. git atravessando a fronteira

**Desempenho:**
- **Fato:** "Linux process reading Windows files (`/mnt/c/...`) | Slow (cross-filesystem 9P protocol) | Avoid
  for build systems, `node_modules`, git repos". Também: "Windows process reading Linux files (`\\wsl$\...`) |
  Slow ... | Use for occasional file access, not tight loops".
  ([WSL interop](https://learn.microsoft.com/windows/dev-environment/wsl-interop))
- **Fato:** "For the fastest performance speed, store your files in the WSL file system if you are working in a
  Linux command line ... If you're working in a Windows command line ..., store your files in the Windows file
  system." ([Working across file systems](https://learn.microsoft.com/windows/wsl/filesystems))
- **Fato:** o WSL 2 perde do WSL 1 em "Performance across OS file systems". "if you are using Windows
  applications to access Linux files, you will currently achieve faster performance with WSL 1."
  ([Comparing WSL versions](https://learn.microsoft.com/windows/wsl/compare-versions))
- **Não verificado:** números de `git status` ou `git pull` em `/mnt/c` × ext4 no tamanho do hub. Não achei
  medição oficial.

**Fim de linha:**
- **Fato:** "If you are working with the same repository folder between Windows, WSL, or a container, be sure to
  set up consistent line endings." ([Git no WSL](https://learn.microsoft.com/windows/wsl/tutorials/wsl-git))
- **Fato:** a doc do VS Code diz que "adding or modifying a `.gitattributes` file in your repository is the most
  reliable way". Exemplo: `* text=auto eol=lf`. Alternativas: `core.autocrlf input` ou `false`.
  ([VS Code Remote troubleshooting](https://code.visualstudio.com/docs/remote/troubleshooting#_resolving-git-line-ending-issues-in-wsl-resulting-in-many-modified-files))
- **Fato:** com `core.autocrlf=true`, o git usa "`CRLF` line endings in your working directory"
  ([git-config](https://git-scm.com/docs/git-config#Documentation/git-config.txt-coreautocrlf)).
  - **Não verificado:** o valor padrão que o instalador do Git for Windows grava nesta máquina.

**Permissões / file mode:**
- **Fato (git):** `core.fileMode` é sondado no `clone`/`init`. Um repositório criado num FS que respeita o modo
  "may be made accessible from another environment that loses the filemode ... In such a case it may be
  necessary to set this variable to 'false'." ([git-config](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corefileMode))
- **Fato (WSL, `/mnt/c` sem metadata, que é o padrão):** "we translate the effective permissions of the Windows
  user to read/write/execute bits and set them to this as the same value for user, group, and other". O
  `chmod` só afeta o atributo *read-only*. Com a opção `metadata`, o WSL grava `$LXMOD` etc. em atributos NTFS.
  ([File permissions](https://learn.microsoft.com/windows/wsl/file-permissions))
- **Fato (Windows acessando `\\wsl$`):** "Any Windows app accessing Linux files will have the same permissions
  as the default user". Arquivos novos recebem umask `022`. (mesma página)
- **Fato (Git for Windows):** com `core.WSLCompat`, o Git for Windows pode gravar os bits executáveis, desde que
  o volume NTFS esteja montado no WSL "using the appropriate options".
  ([Release notes do Git for Windows](https://github.com/git-for-windows/build-extra/blob/main/ReleaseNotes.md), seção desde v2.41.0)

**`safe.directory`:**
- **Fato (git):** "By default, Git will refuse to even parse a Git config of a repository owned by someone
  else". A opção aceita `%(prefix)/<path>` e `*`. ([git-config safe.directory](https://git-scm.com/docs/git-config#Documentation/git-config.txt-safedirectory))
- **Fato (Git for Windows, PR #3791, 2022):** "When using WSL, the ownership check fails and reports an error
  message." O PR ajustou a mensagem para sugerir `%(prefix)/` a usuários WSL.
  (<https://github.com/git-for-windows/git/pull/3791>)
- **Inferência:** o Git do Windows operando um repositório em `\\wsl.localhost\...` tende a exigir uma entrada
  `safe.directory`. O mesmo vale no sentido inverso, se o dono NTFS não bater com o usuário Linux.
  **Não verificado** nesta máquina.

**fsmonitor e credenciais:**
- **Fato:** "By default, the fsmonitor daemon refuses to work with network-mounted repositories". Com
  `fsmonitor.allowRemote`, o uso "is considered experimental". O socket Unix "is supported by native Mac OS
  and Linux filesystems, but not on network-mounted filesystems, NTFS, or FAT32."
  ([git-fsmonitor--daemon](https://git-scm.com/docs/git-fsmonitor--daemon))
- **Fato:** o Git é instalado e configurado separadamente em cada lado. O GCM pode ser compartilhado, mas
  "any configuration set in WSL Git is NOT respected by GCM (by default)", porque as configurações ficam em
  `%UserProfile%\.gitconfig` e `\\wsl$\distro\home\$USER\.gitconfig`.
  ([Git no WSL](https://learn.microsoft.com/windows/wsl/tutorials/wsl-git))

---

## 5. Indexação/busca sobre Markdown e watchers de arquivo

**Linux observando `/mnt/c` (mudanças feitas pelo Windows):**
- **Fato (issue oficial aberta):** "[WSL2] File changes made by Windows apps on Windows filesystem don't trigger
  notifications for Linux apps". Aberta em 2019-12-06, rótulos `feature`, `wsl2`, sem data de fechamento.
  No corpo da issue: "This did work great on WSL1".
  ([microsoft/WSL#4739](https://github.com/microsoft/WSL/issues/4739))
- **Fato (histórico, WSL 1):** as release notes de 2016 registram "Known issue: Modifying files from Windows
  applications does not generate any events" (build 14926), depois "inotify support for notifications
  generated from Windows applications on DrvFs is now in" (build 14942).
  ([Release notes](https://learn.microsoft.com/windows/wsl/release-notes))
  Isso vale para o WSL 1, não para o WSL 2.

**Windows observando `\\wsl$` (mudanças feitas pelo Linux):**
- **Fato (issue oficial aberta):** "`ReadDirectoryChangesW` method is unsupported on `\\wsl$` paths". Aberta
  em 2021-11-12, rótulo `feature`. ([microsoft/WSL#7674](https://github.com/microsoft/WSL/issues/7674))
- **Fato (VS Code):** "mapped network drives or third party file system drivers are not guaranteed to produce
  file events". ([VS Code wiki: File Watcher Issues](https://github.com/microsoft/vscode/wiki/File-Watcher-Issues))
- **Fato (Microsoft):** "The `\\wsl$\` path is only available when the WSL instance is running ... or use
  `wsl.localhost` which can auto-start the distribution on Windows 11."
  ([WSL interop](https://learn.microsoft.com/windows/dev-environment/wsl-interop))

**Linux observando ext4 com escritas feitas pelo Windows via `\\wsl$`:**
- **Não verificado** em doc oficial.
- **Inferência:** a Microsoft descreve o compartilhamento de "Linux files to Windows with WSL's plan9 server
  implementation" rodando do lado Linux ([WSL open source](https://learn.microsoft.com/windows/wsl/opensource)).
  Assim, as escritas acontecem no ext4 por um processo Linux, e o inotify deveria disparar.

**Bibliotecas de watcher usadas pelas candidatas da §10:**
- **Fato (notify, Rust):** "Network mounted filesystems like NFS may not emit any events for notify to listen
  to. This applies especially to WSL programs watching windows paths ([issue #254]). A workaround is the
  `PollWatcher` backend." ([notify-rs/notify, lib.rs](https://github.com/notify-rs/notify/blob/main/notify/src/lib.rs))
- **Fato (grooveseek):**
  - "`groove serve` runs a `notify`-based file watcher by default";
  - "Local disk is assumed — inotify on WSL / SMB / network shares is not guaranteed";
  - em rajadas com perda de eventos: "Run `rebuild_index` manually after the burst".

  ([grooveseek docs/clients.md](https://github.com/alphabet-h/grooveseek/blob/main/docs/clients.md))
- **Fato (obsidian-hybrid-search):** "**Watcher** uses `chokidar` to detect file changes".
  ([README](https://github.com/flowing-abyss/obsidian-hybrid-search))
  - O chokidar diz: "It is typically necessary to set this [`usePolling`] to `true` to successfully watch
    files over a network". Também aceita `CHOKIDAR_USEPOLLING`.
    ([chokidar README](https://github.com/paulmillr/chokidar))
- **Fato (markdown-vault-mcp):** usa "watchdog-based external-change watcher"
  ([README](https://github.com/pvliesdonk/markdown-vault-mcp)).
  - O watchdog diz: "When you want to watch changes in CIFS, you need to explicitly tell watchdog to use
    `PollingObserver`". ([watchdog README](https://github.com/gorakhargosh/watchdog))
  - **Não verificado:** se o markdown-vault-mcp expõe opção de polling.
- **Inferência:** em qualquer arranjo em que o indexador fique de um lado e o hub do outro, o watcher nativo
  não é confiável. Restam polling, reindexação após `git pull` ou indexador do mesmo lado do hub.

---

## 6. SSH: servido a partir do WSL × OpenSSH Server nativo do Windows

### 6.1 Servindo SSH de dentro do WSL 2

- **Fato (NAT):** "By default, WSL uses a NAT (Network Address Translation) based architecture for
  networking." ([Networking](https://learn.microsoft.com/windows/wsl/networking))
- **Fato (LAN):** acesso de outra máquina "isn't the default case in WSL 2. WSL 2 has a virtualized ethernet
  adapter with its own unique IP address". O exemplo dado é `netsh interface portproxy` apontando para o IP
  do WSL. (mesma página)
  - **Fato:** o IP do WSL 2 é "a unique IP address that will change on restart".
    ([Comparing WSL versions](https://learn.microsoft.com/windows/wsl/compare-versions))
- **Fato (mirrored):**
  - exige Windows 11 22H2+ e `networkingMode=mirrored`;
  - entre os benefícios: "Connect to WSL directly from your local area network (LAN)";
  - para conexões de entrada, a doc manda configurar o **Hyper-V firewall** (`Set-NetFirewallHyperVVMSetting`
    ou `New-NetFirewallHyperVRule`).

  ([Networking](https://learn.microsoft.com/windows/wsl/networking))
  - **Fato:** o padrão de `networkingMode` é `NAT`. No mirrored, `ignoredPorts` "Specifies which ports Linux
    applications can bind to, even if that port is used in Windows".
    ([wsl-config](https://learn.microsoft.com/windows/wsl/wsl-config))
  - **Inferência:** um `sshd` no WSL e o `sshd` do Windows competem pela porta 22 no modo mirrored.
- **Fato (firewall):** a partir do WSL 2.0.9, no Win 11 22H2+, "the Hyper-V firewall feature will be turned on
  by default". ([Networking](https://learn.microsoft.com/windows/wsl/networking))
- **Fato (systemd):** é habilitado com `[boot] systemd=true` em `/etc/wsl.conf`
  ([wsl-config](https://learn.microsoft.com/windows/wsl/wsl-config)). Porém, "systemd services will NOT keep
  your WSL instance alive." ([systemd](https://learn.microsoft.com/windows/wsl/systemd))
- **Fato (desligamento por ociosidade):** a [wsl-config](https://learn.microsoft.com/windows/wsl/wsl-config)
  define:
  - `instanceIdleTimeout`, padrão `15000` ms: "The number of milliseconds that a distro is idle, before it is
    shut down. Set to -1 to disable auto shutdown";
  - `vmIdleTimeout`, padrão `60000` ms: "before it is shut down" (só Windows 11).
- **Fato (logoff, nota antiga):** "WSL instances are now terminated when the user logs off." (Release notes,
  build 20211, Insider de 2020)
  - **Não verificado:** se continua assim na versão atual do WSL.
- **Fato (FAQ):** "Administrator privileges in Windows are required to run OpenSSH in WSL. To run an OpenSSH
  server, run your WSL distribution (i.e. Ubuntu) or Windows Terminal as an administrator."
  ([FAQ](https://learn.microsoft.com/windows/wsl/faq#how-do-i-run-an-openssh-server))
  - O texto é antigo e não explica o motivo. Registro como está.
- **Fato (não inicia no boot por padrão):** a doc só descreve o início por `wsl.exe`/acesso ao
  `\\wsl.localhost` e o comando `[boot] command` "when the WSL instance starts". **Não achei** mecanismo
  oficial de "iniciar o WSL no boot sem logon".
  - **Não verificado.** Há relatos de contornos com serviço Windows e `sleep infinity` em
    [microsoft/WSL#9231](https://github.com/microsoft/WSL/issues/9231).

### 6.2 OpenSSH Server nativo do Windows

- **Fato (suporte):** "This article uses the in-box OpenSSH Feature on Demand in Windows ... Microsoft supports
  and services this version through Windows Update". A instalação "creates and enables a firewall rule named
  `OpenSSH-Server-In-TCP`" na porta 22. O tipo de inicialização Automático é "OPTIONAL but recommended".
  ([Get started with OpenSSH](https://learn.microsoft.com/windows-server/administration/openssh/openssh_install_firstuse))
- **Fato (administradores):** "If the user belongs to the administrator group,
  `%programdata%/ssh/administrators_authorized_keys` is used instead". O arquivo "must only have permission
  entries for the `NT Authority\SYSTEM` account and `BUILTIN\Administrators`".
  ([Server configuration](https://learn.microsoft.com/windows-server/administration/openssh/openssh-server-configuration))
- **Fato (contas):** "Key-based authentication in OpenSSH for Windows works with local Windows accounts and
  Active Directory (domain) accounts. Microsoft Entra ID accounts don't support key-based authentication."
  ([Key management](https://learn.microsoft.com/windows-server/administration/openssh/openssh_keymanagement))
  Também: "Authentication via a Microsoft Entra account isn't currently supported." (Server configuration)
  Isso é relevante se alguma das máquinas usar conta Entra.
- **Fato (credenciais na sessão):** "A remote session opened via key-based authentication doesn't have
  associated user credentials. As a result, the session isn't capable of outbound authentication as the user.
  This behavior is by design." (Key management)
- **Fato (shell):** "The initial default in Windows is the Windows command prompt (cmd.exe)". O shell é
  configurável em `HKLM\SOFTWARE\OpenSSH\DefaultShell`. (Server configuration)
- **Fato (git por SSH contra Windows):** "Note that `git clone user@domain@servermachine:C:/test/myrepo.git`
  does not work due to known issue". Os contornos são PowerShell como DefaultShell ou
  `remote.origin.uploadpack "powershell git-upload-pack"`.
  ([Win32-OpenSSH wiki](https://github.com/PowerShell/Win32-OpenSSH/wiki/Setting-up-a-Git-server-on-Windows-using-Git-for-Windows-and-Win32_OpenSSH))
  - **Não verificado:** se o "known issue" (#895) ainda vale na versão atual do OpenSSH do Windows. A página
    da wiki não tem data visível.
- **Fato (WSL a partir de uma sessão SSH do Windows):** a issue "Store WSL isn't accessible from Session 0"
  diz: "it's not possible to interact with WSL from remote sessions such as ssh or psremote ... `Access is
  denied.`" Ela foi reaberta e segue **aberta**.
  - Em 2023-09, um membro da Microsoft escreveu: "in the latest WSL release (2.0.0) we made a fix ... You can
    run `C:\Program Files\WSL\wsl.exe` to get WSL access even on Session 0. We are working on a future fix
    that will address this for the `wsl.exe` binary as well."
    ([microsoft/WSL#9231](https://github.com/microsoft/WSL/issues/9231))
  - **Não verificado:** se o `C:\Windows\System32\wsl.exe` já funciona na sessão 0 hoje.

### 6.3 Leitura lado a lado (só o que as fontes sustentam)

| Ponto | SSH no WSL 2 | OpenSSH Server do Windows |
|---|---|---|
| Alcançável pela LAN por padrão | Não (NAT; precisa de portproxy ou mirrored + regra Hyper-V) | Sim, regra de firewall criada na instalação |
| Fica no ar sozinho | Não garantido: ociosidade de 15 s/60 s (configurável); systemd não mantém viva; nota antiga de término no logoff | Serviço Windows com início Automático |
| Manutenção | Pacote da distro | Windows Update ("supports and services") |
| Pegadinhas documentadas | IP muda a cada reinício (NAT); conflito de porta no mirrored (inferência) | arquivo de chaves de admin com ACL; Entra ID sem chave; sessão sem credencial de saída; `cmd` como shell; git clone com `cmd` ("known issue"); `wsl.exe` na sessão 0 (issue aberta) |

---

## Lacunas e não verificado

1. **Obsidian v1.13.x em `\\wsl.localhost`:** só há relatos de usuários, contraditórios e o mais recente de
   2023 com o erro. Nenhuma posição atual da equipe além de "feature request" aberto. Confirmar exige teste,
   que não foi pedido.
2. **Maestri em workspace WSL:** não verificado o comportamento de Notes, File Tree/diff, Batuta Search, `#`
   no Prompt Composer e persistência (tmux) com WSL. A doc não cita WSL nessas seções. Também não verificado
   um workspace *Local* apontando para `\\wsl.localhost`.
3. **Claude Code:** a regra "não é caminho de rede" cita `\\wsl$`, não `\\wsl.localhost`. A separação de
   `~/.claude` entre Windows e WSL é inferência.
4. **Codex nativo com projeto no WSL:** há só issues abertas (relatos), sem posição oficial além da
   recomendação de usar `/mnt/<drive>`.
5. **OpenCode nativo com `\\wsl$`:** issues fechadas como *not planned*; motivo não verificado.
6. **Linux vendo escritas do Windows via `\\wsl$`** (inotify em ext4) e **Windows vendo escritas do WSL via
   `/mnt/c`** (`ReadDirectoryChangesW` em NTFS): sem doc oficial. São prováveis pela arquitetura (inferência).
7. **Desempenho:** nenhum número oficial de git ou busca para um repositório de Markdown do tamanho do hub
   em `/mnt/c` × ext4. A Microsoft só qualifica como "Slow".
8. **Valor padrão de `core.autocrlf`** gravado pelo instalador do Git for Windows: não verificado.
9. **`wsl.exe` em sessão SSH (sessão 0)** na versão atual do WSL: não verificado.
10. **Término do WSL no logoff** (nota de 2020): não verificado na versão atual.
11. **Iniciar o WSL no boot sem logon:** não achei mecanismo oficial. Só há contornos de usuários.
12. **markdown-vault-mcp:** não verificado se expõe polling. O README só diz "watchdog-based".
13. **Win32-OpenSSH "known issue" #895** (git clone com `cmd`): não verifiquei se segue válido.

---

## Consultas

**Microsoft Learn (MCP: `microsoft_docs_search` / `microsoft_docs_fetch`)**
1. fetch `learn.microsoft.com/windows/wsl/filesystems`
2. fetch `learn.microsoft.com/windows/wsl/compare-versions`
3. search "WSL inotify file change notifications Windows drives /mnt/c not supported"
4. fetch `learn.microsoft.com/windows/dev-environment/wsl-interop`
5. fetch `learn.microsoft.com/windows/wsl/networking`
6. fetch `learn.microsoft.com/windows/wsl/wsl-config`
7. fetch `learn.microsoft.com/windows/wsl/file-permissions`
8. fetch `learn.microsoft.com/windows/wsl/tutorials/wsl-git`
9. fetch `learn.microsoft.com/windows-server/administration/openssh/openssh_install_firstuse`
10. search "OpenSSH Windows administrators_authorized_keys administrator users key-based authentication DefaultShell sshd_config"
11. search "WSL SSH into WSL distribution from remote computer OpenSSH Windows wsl.exe DefaultShell bash"
12. search "WSL keep distribution running in background start WSL at Windows startup without user logon systemd services idle shutdown"
13. search "Run Linux GUI apps on WSL WSLg Windows 11 integrated desktop experience"

**WebSearch (buscador geral)**

14. "github microsoft/WSL issue inotify /mnt/c WSL2 file changes from Windows not detected"
15. "\\wsl$ file watcher ReadDirectoryChangesW notifications Plan 9 Windows app changes made inside WSL not detected issue"
16. "Obsidian vault on WSL \\wsl.localhost file watching not updating"
17. "help.obsidian.md network drive vault file watcher symbolic links limitations"
18. "Obsidian Windows abrir cofre no WSL erro EISDIR watch" (pt-BR)
19. "Maestri app canvas AI agents terminals official site documentation"
20. "themaestri.app WSL workspace Windows Maestri changelog WSL"
21. "OpenAI Codex CLI Windows WSL support official docs developers.openai.com codex windows"
22. "openai codex github issue windows native project in \\wsl$ path sandbox fails"
23. "opencode github issue WSL \\wsl.localhost path Windows native"
24. "Claude Code native Windows working directory \\wsl.localhost slow file search issue anthropics/claude-code"
25. "git-for-windows \"dubious ownership\" \\wsl.localhost safe.directory issue"
26. "WSL2 mirrored networking inbound SSH from LAN sshd port 22 Hyper-V firewall"
27. "WSL instanceIdleTimeout vmIdleTimeout sshd systemd WSL shuts down idle keep alive official"

**API do GitHub (busca de issues em repositórios oficiais)**

28. `repo:microsoft/WSL "ReadDirectoryChangesW"` → #7674, #216, #2507
29. `repo:microsoft/WSL wsl$ file watcher notification in:title` → 0 resultados
30. `repo:git-for-windows/git safe.directory wsl` → #4817, #3787, PR #3791 etc.
31. `repo:microsoft/WSL wsl.exe OpenSSH server in:title` → #9221 (duplicada de #9231)
32. `repo:microsoft/WSL ssh session wsl in:title is:open` → 0 resultados
33. Leitura direta: microsoft/WSL #4739, #7674, #9221, #9231, #41751; git-for-windows #4817, #3787, PR #3791;
    openai/codex #46640, #47115; anomalyco/opencode #22215, #19473 (HTML, porque a API atingiu o limite).

**Grep em documentação oficial baixada (só leitura)**

34. Repositório `obsidianmd/obsidian-help` (zip do `master`), pasta `en/`: `WSL|Subsystem for Linux|network
    drive|network share|UNC|file.?watch|NAS|mapped drive|external drive|outside (of) Obsidian` e
    `automatically (refresh|detect|update)|external change`.
35. Fórum oficial do Obsidian (JSON do Discourse): tópicos 8580, 34688, 116078.
36. Docs do Maestri (21 páginas em `/en/docs/*`, mais `/en/windows` e `/en/changelog`):
    `WSL|Subsystem|distro|PowerShell|/mnt/|\\wsl|Windows` e `remote workspace|persistent session|watch|refresh`.
37. Docs do Claude Code (219 páginas via `llms.txt`): `wsl`, `wsl.localhost|wsl$|UNC path`,
    `wslInheritsWindowsSettings`.
38. Docs do Codex (`developers.openai.com/codex/windows(.md)`, `/codex/windows/wsl.md`,
    `learn.chatgpt.com/docs/windows/windows-app.md`, `/docs/codex/cli.md`): `wsl`.
39. Docs do OpenCode (`opencode.ai/docs/windows-wsl`).
40. git: `Documentation/config/core.adoc` (`core.fileMode`, `core.autocrlf`), `config/safe.adoc`,
    `config/fsmonitor--daemon.adoc`, `git-fsmonitor--daemon.adoc` (CAVEATS); release notes do Git for
    Windows: `wsl|safe.directory`.
41. VS Code: `docs/remote/troubleshooting.md` (fim de linha, watcher), `docs/remote/wsl.md`, wiki
    `File-Watcher-Issues`.
42. READMEs: markdown-vault-mcp, obsidian-hybrid-search, grooveseek (mais `docs/clients.md` e `Cargo.toml`),
    chokidar, watchdog, notify-rs (`notify/src/lib.rs`).
43. Releases do Obsidian (`obsidianmd/obsidian-releases`): assets Linux.
44. Wiki do Win32-OpenSSH: "Setting up a Git server on Windows using Git for Windows and Win32_OpenSSH".
