# Porta 5: Obsidian abre o hub e edita os .md direto

Pesquisa em fonte primária, 2026-10-10. Citações literais em inglês (idioma das fontes). Nenhum teste foi rodado.

## Pergunta

Se o Gustavo abre a pasta do hub como cofre no Obsidian (com o LiveSync ligando-a ao CouchDB), o que acontece com: pastas com ponto, arquivos não-.md, cofre aninhado/subpasta, atualização de links ao renomear/mover, sync de renomear/mover pasta e conflito entre máquinas, e uso no celular?

## Respostas (com citações)

### 1. Explorador, arquivos com ponto, não-.md, .obsidian

- Um cofre é uma pasta qualquer com subpastas: "A vault is a folder on your local file system, including any subfolders." Obsidian guarda notas como texto puro e "automatically refreshes your vault to keep up with any external changes." (https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/How%20Obsidian%20stores%20data.md)
- Formatos aceitos: "Markdown: `.md`", "Bases: `.base`", "JSON Canvas: `.canvas`", imagens, áudio, vídeo e "PDF: `.pdf`". "You can extend Obsidian to support other file formats using Community plugins." (https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/Accepted%20file%20formats.md)
- O explorador (plugin de núcleo) lista "notes and other Accepted file formats in your vault". (https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Plugins/File%20explorer.md) A ajuda liga o explorador à lista de formatos aceitos; outros tipos (ex.: .json, .yaml) não constam dela.
- `.obsidian`: "Obsidian creates an `.obsidian` configuration folder in the root folder of the vault, which contains preferences specific to that vault, such as hotkeys, themes, and community plugins." "By default, most operating systems hide folders that start with a period (`.`), so you may need to update the settings for your file manager to see it." Dica: "The `.obsidian/workspace.json` and `.obsidian/workspaces.json` files store the current workspace layout and update whenever you open a new file." (How Obsidian stores data, URL acima)
- A pasta de configuração pode mudar de nome: "In **Override config folder**, type the name of your profile, starting with a period (`.`)." (https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/Configuration%20folder.md)
- Lixeira do Obsidian: "You can send deleted files to a `.trash` folder in your vault." (https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/Manage%20notes.md)

### 2. Cofre aninhado e abrir subpasta

- Abrir qualquer pasta como cofre é suportado: "At the right of **Open folder as vault**, click **Open**. In the file browser, select the folder you want to use as your vault." (https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/Manage%20vaults.md) E: "You can open multiple folders as individual vaults, for example to separate notes for work and school." (How Obsidian stores data). A ajuda, portanto, permite abrir só uma subpasta (ex.: `initiatives/`) como cofre.
- Aninhamento: "Because Internal links are local to a vault, we recommend that you don't create vaults within vaults. Links may not be updated correctly." (How Obsidian stores data)
- O efeito concreto de abrir só uma subpasta sobre links entre raízes não está na fonte (ver "Não verificado").

### 3. Links e renomear/mover

- "Obsidian can automatically update internal links in your vault when you rename a file. If you want to be prompted instead, you can disable it under: Settings → Files and links → Automatically update internal links." (https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Linking%20notes%20and%20files/Internal%20links.md)
- "When you rename a file, Obsidian automatically updates all the links to that file." "You can rename a note or folder without opening it, by using File explorer." (Manage notes, URL acima)
- Mover: "To move a file or folder, you can use drag-and-drop or the context menu." Menu de pasta: "**Move folder to...** moves the folder into another folder." (File explorer, URL acima)
- Mudança fora do explorador do Obsidian: no contexto de symlinks entre dispositivos, "Obsidian will see the move as a deletion and the creation of a new file. It will also _not_ update any links that depended on the path of that file." (https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/Symbolic%20links%20and%20junctions.md). É sobre mover entre dispositivos de disco via explorador do SO, não sobre mover pasta por script; ver "Não verificado".
- Mover uma iniciativa para `_archive/` pelo Obsidian é "Move folder to...", coberto pela ajuda. A ajuda não diz expressamente que os links para arquivos dentro da pasta movida são reescritos.

### 4. LiveSync: o que sincroniza, exclusões, renomear/mover, conflito

- Arquitetura: "When notes are created or modified, Obsidian raises some events. Self-hosted LiveSync catches these events and reflects changes into Local PouchDB. PouchDB automatically or manually replicates changes to remote CouchDB." (https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/tech_info.md)
- Arquivos normais: "Synchronising files: (RegExp) Empty to sync all files. Set filter as a regular expression to limit synchronising files." "Non-Synchronising files: (RegExp) If this is set, any changes to local and remote files that match this will be skipped." "Maximum file size: ... changes to local and remote files that are larger than this will be skipped." (https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/settings.md, seção "5. Selector")
- Ignore files (beta): "(Beta) Use ignore files: ... changes to local files which are matched by the ignore files will be skipped." "Ignore files: Comma separated `.gitignore, .dockerignore`". A tabela de suporte lista "ignore files" como "Beta or experimental", e diz: "They remain disabled by default". (settings.md)
- Arquivos com ponto são recurso à parte: "Enable the synchronisation of hidden files and folders (e.g. settings files, templates, snippets, and themes under `.obsidian`)." (settings.md, seção 7). O guia: "Hidden File Sync is an advanced, optional feature for synchronising hidden files and folders, including selected content below `.obsidian`. It is separate from ordinary note synchronisation and is deliberately left disabled during Rebuild and Fetch setup operations." "The default excludes `node_modules`, `.git`, and Self-hosted LiveSync's own plug-in data." (https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/tips/hidden-file-sync.md)
- Arquivos não-.md: o seletor de arquivos normais vale para todos os arquivos ("Empty to sync all files"). Sobre binários em conflito: "Binary contents differ | Prefer an explicit user selection; semantic merge is unavailable." e "The compatibility implementation currently selects the newer modification time for differing binary conflicts even when the general Always overwrite with a newer file option is disabled." (https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/specs_conflict_resolution.md)
- Renomear/mover arquivo: "A cross-path rename stores the target before logically deleting only the displayed source branch." (specs_conflict_resolution.md). Do commonlib: "`StorageEventManager.appendQueue` receives watcher events, applies target and ignore policies, and queues `CREATE`, `CHANGED`, `DELETE`, or `RENAME` work." (https://raw.githubusercontent.com/vrtmrz/livesync-commonlib/main/docs/storage-events-and-reflection.md). Também: "A rename from a selected path to a rejected path becomes a `DELETE` ... A rename from an excluded path to a selected path becomes a `CREATE`." O tech_info.md acrescenta: "A rename out of the selected files can also become a database deletion while the destination remains on disk."
- Pasta: a doc diz "deletion protection does not promise full support for external folder case changes or convergence of path spelling." (tech_info.md) e "This change does not promise path-case convergence or full folder-rename support." (storage-events-and-reflection.md). Sobre caixa: "Changing the letter case of a directory name is not supported by this handling." (settings.md, "Handle files as Case-Sensitive"). Nenhuma doc consultada descreve "mover pasta" como operação própria.
- Pastas vazias: "Keep empty folder: Should we keep folders that do not have any files inside?" (settings.md)
- Conflito entre máquinas: "Conflict resolution preserves unknown local content and automatically merges only when the available revision history supplies a safe shared base." (settings.md). Tabela: "One side deletes content which the other leaves unchanged | Preserve the deletion." e "One side deletes content which the other modifies | Ask the user." (specs_conflict_resolution.md; a tabela trata de conteúdo dentro do arquivo). "Resolving a conflict writes the selected or merged result on one observed branch and deletes the other observed conflict leaf."
- Fechar o app: "To prevent file and database corruption, please avoid closing Obsidian until all progress indicators have disappeared as much as possible ... This is especially important if you have deleted or renamed files." (https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/README.md)
- Não combinar com outra sync: "Do not enable this plug-in alongside another synchronisation solution (including iCloud and Obsidian Sync)." (README.md)

### 5. Celular

- "Self-hosted LiveSync is a community-developed synchronisation plug-in available on all Obsidian-compatible platforms." (README.md). "Obsidian mobile apps are available for iOS and iPadOS and Android." (https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Getting%20started/Mobile%20app.md)
- Restrição documentada: "Only Secure (HTTPS) connections can be used on Obsidian Mobile." (settings.md) e "Obsidian Mobile requires HTTPS. Plain HTTP is suitable only for a trusted local connection from a desktop device." (https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/quick_setup.md)
- Acesso à `.obsidian` no iOS: "There is no default way to access the `.obsidian` folder on iOS or iPadOS" (Configuration folder, URL acima).

## Não verificado

- Se o explorador do Obsidian mostra ou esconde pastas/arquivos com ponto (`.git`, `.scratch`) e arquivos de tipos fora de "Accepted file formats": a ajuda consultada não diz. (A frase da ajuda sobre arquivos com ponto "excluded from sync" pertence ao Obsidian Sync, produto diferente, e não vale para o LiveSync.)
- Se a atualização automática de links vale para mover/renomear uma pasta inteira (links de fora para notas dentro dela): a ajuda só afirma "When you rename a file, Obsidian automatically updates all the links to that file."
- O efeito de abrir só uma subpasta como cofre sobre links para outras raízes.
- Se, sem Hidden File Sync, o LiveSync ignora pastas com ponto: as docs só descrevem Hidden File Sync como recurso separado e opt-in; não há frase explícita de exclusão por padrão.
- Como o LiveSync trata mover pasta com muitos arquivos (N pares criar+apagar?): não descrito; a doc só cobre rename por arquivo e diz que não promete suporte completo a rename de pasta.
- Comportamento exato quando uma máquina move uma pasta e outra edita um arquivo dentro dela ao mesmo tempo.
- Suporte por plataforma do LiveSync além da frase "all Obsidian-compatible platforms" e da exigência de HTTPS; limites de desempenho no celular.

## Precisa de teste

- Criar `.scratch/`, `.git` e um `.json` no cofre e ver se o explorador os mostra.
- Mover uma pasta de iniciativa para `_archive/` no Obsidian com links entrantes e conferir se os links são reescritos.
- Mesma movimentação com LiveSync em duas máquinas: ver o que aparece no CouchDB e se surge conflito quando a outra máquina edita um arquivo da pasta ao mesmo tempo.
- Mover pasta fora do Obsidian (script) e ver se o LiveSync captura como renomeação ou como apagar+criar.
- Abrir só uma subpasta como cofre e ver o efeito nos links entre raízes.
- Celular: sync de um cofre grande por HTTPS.

## Fontes

- https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/Manage%20vaults.md
- https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/How%20Obsidian%20stores%20data.md
- https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/Accepted%20file%20formats.md
- https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/Configuration%20folder.md
- https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/Manage%20notes.md
- https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Files%20and%20folders/Symbolic%20links%20and%20junctions.md
- https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Linking%20notes%20and%20files/Internal%20links.md
- https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Plugins/File%20explorer.md
- https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Getting%20started/Mobile%20app.md
- https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/README.md
- https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/settings.md
- https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/quick_setup.md
- https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/tech_info.md
- https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/tips/hidden-file-sync.md
- https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/docs/specs_conflict_resolution.md
- https://raw.githubusercontent.com/vrtmrz/livesync-commonlib/main/docs/storage-events-and-reflection.md
