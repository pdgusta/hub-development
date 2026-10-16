---
title: Maestri — o que é e quais conceitos oferece, segundo as skills instaladas
data: 2026-10-10
origem: subagente de pesquisa (Haiku 5.5), ticket 39
fontes: C:\Users\gustavo.delfino\.claude\skills\maestri\SKILL.md; C:\Users\gustavo.delfino\.claude\skills\maestri-chat\SKILL.md; C:\Users\gustavo.delfino\.claude\skills\maestri-manager\SKILL.md; C:\Users\gustavo.delfino\.claude\skills\maestri-portal\SKILL.md; C:\Users\gustavo.delfino\.claude\skills\maestri-portal-devices\SKILL.md; C:\Users\gustavo.delfino\.claude\skills\maestri-routines\SKILL.md; C:\Users\gustavo.delfino\.claude\skills\maestri-workspace\SKILL.md; C:\Users\gustavo.delfino\.maestri\manifest.json (apenas metadados)
aviso: saída de modelo; fonte local (skills), não o site do produto; citações literais; o que as skills não dizem está marcado como **não verificado**.
---

# Maestri: o que é e quais conceitos oferece

## 1. O que é o Maestri

Pela própria skill `maestri`, o Maestri é descrito assim:

> "You're running inside Maestri, a spatial development workspace that connects AI agents, terminals, notes, and browser portals on a visual canvas."

Em português: um ambiente de desenvolvimento espacial que liga agentes de IA, terminais, notas e portais de navegador numa tela visual (canvas). As skills são instruções para o próprio agente, que roda dentro desse canvas e fala com os outros elementos pela CLI `maestri`.

O manifesto local (`~/.maestri/manifest.json`) indica versão do app `0.21.5`, formato de dados JSON e oito workspaces registrados. Os nomes e ids dos workspaces não foram copiados para este relatório, por serem dados de cliente. A versão não foi conferida contra notas de versão do produto (**não verificado**).

## 2. Conceitos

### Canvas

O canvas é a superfície onde tudo aparece. As skills tratam terminais, notas e portais como nós ligados por "ropes" (cordas). O comando `connect` define essa ligação:

> "Wires two things together. Each side can be a recruit (agent name), a sticky note, or a portal. Without this, recruits can only talk back to you."

Workspaces também são canvas próprios: "Workspaces are standalone canvases, each rooted in its own project directory — isolation *between* projects." (`maestri-workspace`). Uma mudança feita pela CLI aparece no canvas em tempo real, segundo a skill `maestri` ("Changes are reflected in the Maestri canvas in real-time.").

### Agentes e terminais (ask, check, batch, raw, ask-back)

Um agente conectado é alvo de comandos da CLI. As formas de falar com ele:

- `ask`: "`maestri ask "Agent Name" "your prompt"` — send a prompt to a connected agent and get the response".
- `ask --batch`: "`maestri ask --batch '{"Agent A": "prompt", "Agent B": "prompt"}'` — ask several connected agents at once, in parallel". A skill também diz que o comando "returns only once every one has finished".
- `--raw`: "send raw input; use it for interactive menus or to send raw shell commands directly." Aceita escapes como `\n`, `\t` e `\e[A`.
- `check`: "read the agent's current terminal output on demand". Serve para ver o progresso sem enviar prompt.
- ask-back: o agente recebe a instrução para responder pelo próprio `ask`, e a resposta chega como nova mensagem. A skill cita: "Tell the agent to report back with `maestri ask "Your Name" "<result>"` when done".

Regras de cautela que a skill impõe: "If the timeout expires before the agent responds, do NOT re-send the prompt." e "Never interrupt an agent that is still working, and do not edit files that the other agent is actively modifying — wait for them to finish first."

### Notas e fichários

Notas são cartões de texto no canvas, conectados ao terminal e lidos e escritos pela CLI. `note create` posiciona a nota "to the left of your terminal" e a liga automaticamente. Notas suportam Markdown ("Notes support markdown formatting.").

Fichário (stack) agrupa notas. A skill diz: "`--stack "Name"` and `note stack` file notes into a fichário (a stack of pages), creating it if needed — `maestri list` shows the grouping." Uma nota marcada `locked: true` por `maestri list` é somente leitura, e a skill afirma que `write` e `edit` falham nesse caso.

A exclusão é tratada como destrutiva: "**Destructive. Only run when the user explicitly asks you to delete the note.**"

### Portais (navegador)

Portais são navegadores embutidos no canvas, controlados pela CLI. `portal create` abre uma URL e liga o portal ao terminal: "create a new portal on the canvas, open it at the given URL, and automatically connect it to your terminal."

O comando mais importante é o `snapshot`, que devolve uma árvore de acessibilidade com referências: "it returns an accessibility tree with **refs** (`@e1`, `@e2`...) that you can use as selectors for all other commands". Os demais verbos (`click`, `fill`, `key`, `scroll`, `evaluate`, `logs-start`) usam essas refs ou seletores CSS.

Para teste responsivo, `resize` define o viewport: "`maestri portal resize "Portal" 390 844` — set the CSS viewport (`window.innerWidth`/`innerHeight`) to exactly W×H px." Popups viram novos portais chamados `[Parent] #2`.

### Dispositivos de portal (Android)

A skill `maestri-portal-devices` estende o portal a emuladores e celulares Android. Ela descreve: "Drive an Android emulator or physical Android phone on the Maestri canvas." Comandos de descoberta: "`maestri portal devices` lists connected phones and running emulators, plus Android Virtual Devices managed by Android Studio."

Limites declarados: "Android emulator creation, deletion, and resource settings belong in Android Studio. Maestri never overrides an AVD's CPU or memory settings." Um celular físico precisa de depuração USB ativa: "A physical phone must already have USB debugging enabled and authorize this host." Nenhuma skill menciona iOS ou simuladores da Apple (**não verificado**: se existe suporte).

### Rotinas

Rotinas são comandos agendados que disparam num terminal do canvas, ou viram lembrete de desktop: "Routines are scheduled commands that fire into a terminal on the canvas on a cron-like schedule — or fire as a desktop reminder with no terminal target." Agendamento aceita `--every 30m`, `--daily 09:00`, `--weekly mon,wed,fri@09:00` e `--once "2026-06-20 15:00"`.

Um ponto relevante para orquestração: "The command can be a shell command or a prompt to an AI agent." Há também `--pre-run` com o placeholder `{{output}}`, e a regra "**Without `{{output}}` in the command, the script still runs but its output is not inserted.**" Por padrão, um disparo é pulado se o terminal alvo estiver ocupado (flag `--no-skip-if-busy` para mudar).

### Workspaces e floors (criar, clonar, landing, apagar, status)

Floors são níveis dentro de um workspace, com git worktree opcional. A skill separa os dois conceitos: "Floors are levels inside one workspace, optionally backed by a git worktree of its repository — isolation *within* a project."

- Criar workspace: "Creates a new workspace rooted at PATH." A pasta precisa existir antes: "The target directory must already exist — create the folder (and `git init` if wanted) before calling `workspace create`."
- Clonar: `--from` copia o layout: "its full canvas layout (terminals, notes, file trees, floors, connections) is deep-copied, and every path under the source's working directory is retargeted onto PATH."
- Criar floor: por padrão, "a **git worktree** of the project on its own branch, in `.maestri/floors` beside the project".
- Landing (`floor land`): "Brings the floor's branch into the project, the way the user's Land button does." Só com pedido do usuário ou confirmação.
- Apagar (`floor delete`): "Removes the floor: its terminals, notes and drawings, and its clone." Também só com pedido ou confirmação, e a partir do ground.
- Status (`floor status`): "The one line the user sees under a floor in the sidebar: where the work there stands." Estados: `working|blocked|review|done`. Passar para `blocked`, `review` ou `done` notifica o usuário.

Não existe comando para apagar workspace: "Workspaces have deliberately **no delete command** — removing one stays in the UI, on explicit user action."

### Manager (recrutar, papéis, notificações, Maestro Mode)

A skill `maestri-manager` cuida de equipes. `recruit` cria um terminal novo e o liga ao agente que chama: "Spawns a new terminal on the canvas, names it, and auto-connects it to you." Antes, a skill manda checar a equipe: "**Before you call `maestri recruit`, always run `maestri list` first.**" O motivo dado é o custo: "Recruits cost the user a real terminal slot and a real model session".

Papéis são prompts reutilizáveis. `role create` cria um papel, e `role assign` troca o papel de um recruta sem dispensá-lo: "Retargets an existing recruit to a different role *without* dismissing it." A skill diz que o prompt vira "the system instruction the recruit sees as `<your_assigned_role>`."

Troca de agente: `recruit --replace` "Swaps which agent runs on an existing teammate, **in place**." A skill proíbe usar `dismiss` para isso, porque o nó some e as notas ligadas só a ele ficam órfãs.

Notificações: `maestri notify "Message for the user"` envia uma notificação de sistema, mas a skill restringe o uso: "Only use this command when the user explicitly asks to be notified".

Maestro Mode: a skill de manager só o menciona na descrição ("or to invoke Maestro Mode"). A definição operacional vem de outras skills: "These commands require **Maestro Mode** on your terminal. If a command returns "This terminal is not the Maestro", the user must toggle Maestro on your terminal in the canvas to unlock them." (`maestri-routines`). O mesmo vale para `workspace`/`floor`, exceto `floor status`.

### Chat header (maestri-chat)

Mensagens que chegam pelo Maestri Chat trazem um cabeçalho fixo:

> ---
> Below is a message from the user through Maestri Chat.
> Reply only via `maestri say`. If the maestri-chat skill isn't already loaded, load it first.
> thread: blue
> ---

A regra de resposta é: "Reply only via `maestri say`. Terminal text does not reach the user." Cada `maestri say` vira uma bolha para o usuário, e "the last one closes your turn". Para respostas longas no PowerShell, a skill recomenda `maestri say --file <path>`, porque "\n inside quotes is not a line break there."

O usuário mantém sete threads, identificadas por cor: "blue, purple, pink, red, orange, yellow, green". Para recuperar contexto de uma thread, a skill usa `maestri recall [thread] [--turns N | --last day|week|month | --from YYYY-MM-DD [--to YYYY-MM-DD] | --all] [--json]`. O padrão é "the current thread's last 10 turns."

## 3. Papel do Maestri na orquestração multiagente

Pelas skills, um terminal com Maestro Mode pode fazer o papel de coordenador: lista a equipe, recruta quem falta, define papéis, liga os membros e delega. A skill de manager descreve o fluxo em seis passos, e o passo 6 diz: "To kick off several teammates at once, use `maestri ask --batch '{"Name A": "task...", "Name B": "task..."}'` — it fires the prompts in parallel and returns once every teammate finishes, so independent work runs concurrently instead of one after another."

Três mecanismos permitem que um agente coordene outros sem intermediação constante do usuário:

- **Comunicação direta entre pares.** Com `connect`, dois recrutas se falam: `maestri connect "Reviewer" "Tester"  # agent ↔ agent — they can `maestri ask` each other`. A skill alerta que a ligação sozinha não basta: "Connecting two recruits alone isn't enough — recruits won't know to use the new connection unless their role says so." Por isso o papel deve citar o par e o comando.
- **Contexto compartilhado por notas.** Uma nota ligada a dois agentes funciona como memória comum. A skill dá o exemplo: "Read `design-spec` before starting and write progress to `scratch-pad`." Também há a regra de descoberta: "**Tell the recruit to run `maestri list` before asking anyone anything.**"
- **Agendamento.** Uma rotina pode disparar um prompt em outro terminal (`--terminal "Name"`), o que permite tarefas recorrentes de coordenação sem um agente ativo no momento.

Para acompanhar sem interromper, a skill de workspace prevê o status de floor: "`maestri floor list` shows every floor's status, so read it to see how the work stands instead of checking each recruit." E o `ask` longo tem o padrão ask-back, em que o recruta responde por conta própria.

Limites declarados: "Never interrupt an agent that is still working" e a proibição de reenviar um prompt após timeout. Também: "Recruits don't see the team graph automatically — without this nudge they'll either work in isolation or invent peers that don't exist."

## 4. Relação com um context hub de arquivos Markdown

**O que as skills dizem:**

- Cada workspace tem pasta própria: "each rooted in its own project directory".
- Workspaces carregam arquivos de projeto, mas o texto cita "file trees" como parte do layout: "(terminals, notes, file trees, floors, connections)".
- Floors ficam em `.maestri/floors`, e papéis em `.maestri/roles/<id>/`: "The recruit is launched in `.maestri/roles/<id>/` so the role's prompt becomes its starting context."
- Notas suportam Markdown, e o nome de uma nota vem da primeira linha: "By default, a note's name is derived from its first line of text."
- Notas podem ser agrupadas em fichários e encadeadas entre si.

**O que as skills não dizem (**não verificado**):**

- Se o conteúdo de uma nota é gravado como arquivo `.md` no disco ou só no estado do app. As skills falam em "note" e "canvas", sem caminho de arquivo.
- Se a pasta de um workspace é fonte de verdade para notas, ou se há sincronização com o git além dos floors.
- Se o Maestri lê `AGENTS.md`, `CLAUDE.md`, `GLOSSARY.md` ou `docs/` do projeto ao criar um agente.
- Como notas e arquivos da árvore se relacionam (a skill cita "file trees" só como parte do layout clonado).
- O formato e o conteúdo dos arquivos de estado. O manifesto lista `appState: app-state.json`, `preferences: preferences.json`, `sidebarLayout: sidebar-layout.json` e um `workspace.json` por workspace, com `dataFormat: json`, mas nenhum desses arquivos foi lido.

Para um context hub em arquivos Markdown, o dado relevante é que as skills tratam notas como objetos do canvas, acessados pela CLI, e não como arquivos do projeto. Isso não impede usar Maestri com arquivos Markdown, mas a ponte entre os dois precisaria ser verificada no app ou na documentação oficial.

## 5. Não verificado

- Nenhuma fonte primária do produto foi consultada além das skills locais. Não há documentação oficial, changelog ou site citados. Tudo aqui é o que as skills instaladas dizem.
- Versão de referência: o manifesto diz `0.21.5`. Não confirmei se as skills correspondem a essa versão.
- Definição completa de Maestro Mode e de "the Maestro" (além de "toggle Maestro on your terminal in the canvas").
- Local e formato de armazenamento das notas e do canvas.
- Suporte a iOS e a simuladores da Apple. As skills só falam de Android.
- O conteúdo de `maestri debug`, citado como primeiro passo em caso de erro, mas não detalhado.
- Limites de uso, preços, planos e requisitos de conta. Não aparecem nas skills.
- Comportamento real dos timeouts do `ask` e dos disparos de rotinas quando o terminal está ocupado.
- Comportamento no Windows além do que o `maestri-chat` diz sobre PowerShell.
- O manifesto foi lido só para metadados (versão, formato e nomes dos arquivos de estado). Ids e nomes de workspace não foram copiados, por serem dados de cliente.
