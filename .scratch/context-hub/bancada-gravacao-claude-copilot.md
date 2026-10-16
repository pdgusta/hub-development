# Bancada de gravação: Claude Code e Copilot CLI (ticket 11, rodada 1 = C)

Rodada em 2026-10-15, das 15h27 às 15h34, por um subagente do maestro. Brief em `bancada-gravacao-brief.md`. Aqui ficam
só os dados, sem recomendação. A parte do Codex é de outro executor (`bancada-gravacao-codex.md`).

**Versões e modelos:** Claude Code 2.1.300, modelo `haiku` (o init do transcrito diz `claude-haiku-5-5`); Copilot CLI
1.0.98, modelo `claude-haiku-5.5`.
**Chamadas gastas:** 4 de `claude -p` e 4 de `copilot -p`, uma por caso, sem repetição.
**Pasta:** `C:\Projetos\bancada-acesso\gravacao\claude-copilot\`
- `hook_gravacao.py` é o hook de teste, o mesmo arquivo para os dois harnesses: `pos` muda a nota, `pre` registra e guarda.
- `preparar.py` recria as notas de cada caso.
- `rodar_claude.sh` e `rodar_copilot.sh` rodam cada caso; `ver_claude.py` e `ver_copilot.py` extraem as chamadas.
- `claude\.claude\settings.json` guarda os hooks do Claude Code, em escopo de projeto.
- `copilot\.github\hooks\gravacao.json` guarda os hooks do Copilot, em escopo de repositório (`copilot\` virou um repo
  git próprio).
- Os registros ficam em `logs\hooks.log`, com hora, ferramenta e hash do disco. As saídas completas estão em `saida\`.

A nota de teste tem quatro linhas: título, `linha-a: alfa original`, `linha-b: beta original` e `linha-c: gama original`.

## Placar

| Caso | Claude Code | Copilot CLI |
|---|---|---|
| 1. Troca de trecho, mudança externa em outra linha | **Edit gravou**, e a mudança externa ficou | **edit gravou**, e a mudança externa ficou |
| 2. Troca de trecho, mudança externa no próprio trecho | **Edit recusou** | **edit recusou** |
| 3. Regravação inteira depois da mudança externa | **Write recusou** (o arquivo mudou desde a leitura) | **create recusou**, porque recusa *qualquer* arquivo que já existe |
| 4. Hook antes da ferramenta | **passou**: recusa o Write de arquivo existente, deixa passar o Edit e o arquivo novo | **passou**: recusa o create de arquivo existente, deixa passar o edit e o arquivo novo |
| Extra: regravação inteira de arquivo existente **nunca lido** (no passo 5 do caso 4, na mesma chamada, sem a guarda do hook) | **Write gravou por cima**, sem aviso | **create recusou** (`Path already exists`) |

## Detalhe, caso a caso

| Caso | Ferramenta | O que ficou no disco | O que a ferramenta disse | Resultado |
|---|---|---|---|---|
| 1 | Claude `Edit` | `alfa EXTERNA` + `beta AGENTE`: as duas mudanças ficaram | `has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)` | passou, sem desfazer a mudança externa, e avisou |
| 1 | Copilot `edit` | `alfa EXTERNA` + `beta AGENTE` | `File ...caso1.md updated with changes.`, sem aviso de mudança externa | passou, sem desfazer a mudança externa, e não avisou |
| 2 | Claude `Edit` | `beta EXTERNA`, sem a gravação do agente | `<tool_use_error>File has been modified since read, either by the user or by a linter. Read it again before attempting to write it.</tool_use_error>` | recusou e mandou reler |
| 2 | Copilot `edit` | `beta EXTERNA` | `No match found: old_str not found in ...caso2.md; no changes made; you might want to try again with correct old_str` | recusou por não achar o trecho; não diz que o arquivo mudou |
| 3 | Claude `Write` | `alfa EXTERNA`, o resto original; nada do agente gravado | o mesmo `File has been modified since read ... Read it again before attempting to write it.` | recusou |
| 3 | Copilot `create` | `alfa EXTERNA`, o resto original | `Path ...caso3.md already exists as a file. Use 'view' to check contents then edit it.` | recusou, mas não por conferir versão (ver o extra) |
| 4 | Claude: `Write` em arquivo existente, depois `Edit` no mesmo arquivo, depois `Write` de arquivo novo | o `caso4.md` ficou sem a regravação, só com `gama AGENTE` (do Edit); `caso4-novo.md` foi criado | Write: `PreToolUse:Write hook error: Hook da bancada: regravacao inteira ... recusada; use a troca de trecho ou o MCP do banco.`; Edit: `updated successfully`; Write novo: `File created successfully` | passou: recusou e deixou passar como pedido |
| 4 | Copilot: `create` em arquivo existente, depois `edit`, depois `create` novo | igual ao Claude | create: `Denied by preToolUse hook: Hook da bancada: ...` (`code: denied`); edit: `updated with changes`; create novo: `Created file ...caso4-novo.md with 24 characters` | passou |
| extra | Claude `Write` em `caso3b.md`, existente e não lido | o arquivo inteiro virou `caso3b regravado sem leitura` | `The file ...caso3b.md has been updated successfully.` | **regravou sem conferir nada** |
| extra | Copilot `create` em `caso3b.md`, existente e não lido | intacto | `Path already exists` | recusou |

Observações:
- No Claude Code, nos casos 2 e 3, o hook `PreToolUse` **não registrou** a chamada. A recusa por "modified since read"
  vem antes dos hooks `PreToolUse`. Isso é inferido do log, não está documentado.
- O modelo do Claude, no fim do caso 2, disse que "a linha `beta original` continua no arquivo". Não era verdade: no
  disco estava `beta EXTERNA`. O modelo não relê, então descreve o que leu.
- No Copilot, todo resultado de ferramenta veio com `Additional guidance from postToolUse hooks: GSD: review the tool
  result against the active phase before continuing.` Esse texto vem de um hook `postToolUse` de outra origem (GSD:
  plugin ou config do usuário, **não verificado** qual). Não é da bancada, e não interferiu no teste.
- No Copilot, a única regravação inteira de arquivo existente que sobra é pelo shell. Neste teste o shell estava
  desligado (`--available-tools view edit create`). Pelo `edit`, um `old_str` com o arquivo inteiro também conferiria o
  conteúdo; isso não foi testado.

## Método do ponto de parada (leitura → mudança externa → gravação)

Usei um **hook depois da ferramenta de leitura**. No Claude Code é o `PostToolUse` com matcher `Read`; no Copilot, o
`postToolUse` com matcher `view`. Ele roda `hook_gravacao.py pos`, que muda a nota no disco uma única vez (uma marca
em `logs\estado\` evita nova mudança numa releitura) e registra a hora e o hash antes e depois.

Por que isso garante a ordem:
1. O hook roda depois de a leitura terminar. O conteúdo que a ferramenta devolveu ao modelo é o original: nos oito
   transcritos, o resultado do Read/view mostra `alfa original` / `beta original`.
2. O hook é síncrono. O resultado da leitura só volta ao modelo depois que o hook termina, então o modelo não pode pedir
   a gravação antes da mudança. As fontes: Claude Code, *"By default, hooks block Claude's execution until they
   complete"* (hooks, "Run hooks in the background"); Copilot, `postToolUse` *"can modify the tool result or inject
   additional context for the model"*, o que só é possível antes de o resultado chegar ao modelo.
3. A conferência está no log. O hook `pre`, antes de cada gravação, registra o hash do disco naquele instante, e esse
   hash é igual ao `sha_depois` da mutação. No caso 1 do Claude, por exemplo, a mutação às 15:27:31.490 deixou
   `d513e1f237a0`, e o Edit às 15:27:33.705 encontrou `d513e1f237a0`. Nos casos 2 e 3 do Claude, a recusa veio antes
   do hook `pre`; ali a prova é a mensagem da própria ferramenta ("modified since read").

## Como os hooks foram ligados (só no escopo de projeto)

- **Claude Code:** `claude\.claude\settings.json`, lido porque o `claude -p` roda nessa pasta. Os flags usados:
  `--model haiku --permission-mode acceptEdits --allowedTools "Read,Edit,Write" --disallowedTools "Bash,PowerShell"`.
- **Copilot CLI:** `copilot\.github\hooks\gravacao.json`, num repo git próprio (`git init` em `copilot\`). Os hooks do
  repositório carregaram no modo `-p` com `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS=true`, sem confiar na pasta e sem
  tocar no `~/.copilot/config.json`. Fonte (cli-command-reference): *"Set to `true` to load repository hooks in prompt
  mode (`-p`). Repository hooks also load automatically when the folder is already trusted or `COPILOT_ALLOW_ALL` is
  set."* Isso resolve a falha do teste 2 da bancada de acesso (`repository_untrusted`) para o modo `-p`.
- A guarda do caso 4 vale só para notas `caso4*`, para não mascarar os casos 1 a 3.
- Formato da recusa: no Claude, `hookSpecificOutput.permissionDecision: "deny"`; no Copilot,
  `{"permissionDecision":"deny","permissionDecisionReason":...}`.

## Fontes primárias

**Claude Code**: https://code.claude.com/docs/en/tools-reference e https://code.claude.com/docs/en/hooks, baixadas em
2026-10-15 para `gravacao\claude-copilot\fontes\`.
- Edit tool behavior: *"A file that changed on disk after Claude last read it can still be edited when `old_string`
  matches the current content exactly and unambiguously and Claude Code can read the file without prompting. [...] the
  result notes that the file carries other changes so Claude re-reads it before edits that depend on surrounding
  content. In any other case, such as a stale `old_string` [...], Claude reads the file again before editing."*
  O teste confirmou isso (casos 1 e 2).
- Write tool behavior: *"The Write tool creates a new file or overwrites an existing one with the full content
  provided."* e *"Newer models can overwrite a file they never read this session under the same conditions as
  read-before-edit"*. A página **não descreve** a recusa por "modified since read" no Write. O teste mostrou que a recusa
  existe quando o arquivo foi lido e mudou depois (caso 3). Mostrou também que um modelo novo (haiku 5.5) regrava sem
  conferir nada um arquivo que nunca leu (extra), como a página permite.
- Hooks, PreToolUse: o exemplo de `permissionDecision: "deny"` com `permissionDecisionReason`.

**Copilot CLI**: cópias locais feitas pela bancada de acesso em `C:\Projetos\bancada-acesso\fontes\` (não baixei de
novo; os endereços são os citados naquele relatório).
- hooks-configuration (docs.github.com/en/copilot/reference/hooks-configuration): `preToolUse` *"can allow, deny, or
  modify"*; `permissionDecisionReason` *"Reason shown to the agent. Required when decision is `"deny"`."*; a tabela que
  liga `create` a `Write` e `edit` a `Edit`.
- cli-command-reference: *"`create` | Create new files"*, *"`edit` | Edit files via string replacement"*, e
  `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS`, citado acima.
- Que o `create` recusa arquivo existente e que o `edit` não confere a versão (só o trecho): **não achei na
  documentação**. Isso vem só do teste.

## Estado dos arquivos globais no fim

Nenhum arquivo global foi tocado por esta bancada: os hooks ficaram nas pastas de projeto. Os hashes foram tirados antes
e depois (`logs\globais-antes.sha256` e `logs\globais-depois.sha256`).

| Arquivo | Estado |
|---|---|
| `~/.claude/CLAUDE.md` | mesmo SHA-256 |
| `~/.copilot/hooks/gsd-session.json`, `tokenjuice-cli.json` | mesmo SHA-256; a pasta tem os mesmos dois arquivos |
| `~/.copilot/copilot-instructions.md`, `~/.copilot/mcp-config.json` | mesmo SHA-256 |
| `~/.copilot/settings.json` | continua não existindo |
| `~/.claude/settings.json` | **mudou** (`115bb980...` para `6618a05e...`, mtime 15:28:46). **Não fui eu**, e não restaurei, porque não havia cópia (eu não ia mexer nele) e a mudança pode ser legítima. Às 15:28:45 subiu outra sessão do Claude Code, no projeto `...laco-system-design-descricao-teste-v2`, que não é desta bancada; a minha sessão do caso 3 subiu na mesma janela. As outras três sessões minhas, iguais, não mexeram no arquivo (o mtime seria posterior). Autoria **não verificada**; vale o maestro conferir. |

Ficou fora do restauro, por ser o uso normal: o histórico das sessões `-p` (`~/.claude/projects/C--Projetos-bancada-
acesso-gravacao-claude-copilot-claude`, `~/.copilot/session-state`). O `~/.copilot/config.json` não foi lido nem
tocado. Não abri processo em segundo plano: os oito `-p` terminaram sozinhos (saída 0), e nada foi encerrado por nome.
