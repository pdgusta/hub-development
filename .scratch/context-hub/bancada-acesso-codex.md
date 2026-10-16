# Codex na bancada de acesso — rodada 3

Data: 2026-10-15. Executor: Sonda Codex. Bancada: `C:\Projetos\bancada-acesso`. CLI instalado: **0.161.0**. Testes com `gpt-6-luna`, esforço `low`, sem subagentes. Fontes consultadas nesta rodada; código fixado na tag da versão instalada, salvo indicação contrária. Não houve commit.

## 1. Falha do sandbox no Windows

**Causa local identificada; contorno parcial com `unelevated`; shell passou sem sandbox.** O erro genérico não era suficiente para concluir que faltava UAC. O log da execução mínima mostrou falha ao atualizar a ACL de um executável do runtime do Codex:

```text
runtime read/execute validation failed: validate runtime read/execute access on
%LOCALAPPDATA%\OpenAI\Codex\runtimes\cua_node\a9ba6825a525118c\bin\node_repl.exe:
open ACL target for root-only update:
O arquivo já está sendo usado por outro processo. (os error 32)
setup refresh completed with errors
setup error: setup refresh had errors
```

Evidência local preservada: `logs\rodada3\sandbox-causa.txt`. O helper iniciou e saiu com erro; portanto esta reprodução não corresponde à falha de iniciar o helper por elevação exigida. Qual processo segura o arquivo: **não verificado**; nenhum processo alheio foi encerrado.

Fontes primárias:

- [Código de validação do runtime, 0.161.0](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/windows-sandbox-rs/src/setup_provisioning/setup_runtime_bin.rs): trecho `runtime read/execute validation failed`. A função percorre o runtime e tenta conceder leitura/execução também aos arquivos existentes.
- [Código da ACL, 0.161.0](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/windows-sandbox-rs/src/acl.rs): trecho `.access_mode(MAXIMUM_ALLOWED)` na abertura para atualização sem herança. O contexto do erro é `open ACL target for root-only update`.
- [Issue #53679](https://github.com/openai/codex/issues/53679), aberta em 13/10/2026: trecho `runtime validation can't open cua_node\…\node_repl.exe (os error 32)`. Relato com a mesma cadeia de erros; não é confirmação de correção pelos mantenedores.
- [Documentação oficial do sandbox Windows](https://learn.chatgpt.com/docs/windows/windows-sandbox): trecho `unelevated is a legacy fallback`. Documenta token restrito do usuário atual e isolamento de rede mais fraco que `elevated`. A documentação atual também descreve MXC; sua disponibilidade nesta máquina **não foi testada**.

Teste mínimo, executado na raiz da bancada:

```powershell
codex -c 'windows.sandbox="elevated"' sandbox -- C:\Windows\System32\cmd.exe /c echo BANCADA-ELEVATED-OK
codex -c 'windows.sandbox="unelevated"' sandbox -- C:\Windows\System32\cmd.exe /c echo BANCADA-UNELEVATED-OK
```

| Teste | Resultado |
|---|---|
| Elevado, comando mínimo | **Falhou**, `helper_unknown_error: setup refresh had errors` |
| Não elevado, mesmo comando | **Passou**, `BANCADA-UNELEVATED-OK` |
| `codex exec`, `workspace-write`, não elevado, `apply_patch` | **Passou**, nota alterada |
| Mesma sessão, gravação por shell | **Falhou**, `CreateProcessAsUserW failed: 5`, caminho do PowerShell sob `WindowsApps` |
| Pedido ao modelo para usar outro `shell` | **Falhou**: a execução continuou usando o alias; não prova que o executável alternativo foi testado pela ferramenta |
| `codex sandbox`, PowerShell do System32, gravação | **Falhou**, acesso negado ao arquivo de saída; a invocação não fixou uma política de escrita equivalente à de `exec` |
| `codex exec`, `danger-full-access`, mesmo alias do PowerShell, gravação | **Passou**, ferramenta saiu com sucesso; arquivo contém `SHELL-OK` |

Houve uma tentativa inicial com a sintaxe antiga `sandbox windows`; na 0.161.0, `windows` virou parte do comando e causou erro de arquivo inexistente. O `codex sandbox --help` local confirmou a sintaxe acima. Esse erro não foi contado como falha do contorno.

Uso curto para repetir o contorno que permitiu `apply_patch`, sem mudar o global:

```powershell
codex exec -s workspace-write -c 'windows.sandbox="unelevated"' '<pedido>'
```

Para a bancada autorizada com acesso total, `codex exec -s danger-full-access '<pedido>'` também permitiu gravar pelo shell. **Isso desativa o isolamento; não é reparo do sandbox elevado.** Não foi aplicada alteração de ACL, renomeação do runtime, reinstalação ou mudança global. Reparar o elevado e resolver o alias no modo não elevado permanecem **não verificados**.

Logs: `sandbox-elevated.txt`, `sandbox-unelevated.txt`, `codex-stop-tocada.txt`, `codex-shell.txt`, `sandbox-shell-direto.txt`, `codex-shell-fullaccess.txt`, todos em `logs\rodada3`.

## 2. Stop libera quando a nota muda

**Passou.** `BANCADA_FIM=1`, hooks originais da bancada pré-aprovados pelos hashes via `-c hooks.state`, `workspace-write` e `windows.sandbox="unelevated"`. O pedido mandou acrescentar uma linha à nota com `apply_patch`. A ferramenta concluiu; a nota passou a conter `codex rodada3 tocou a nota`.

O `logs\fim.log` registrou, para a sessão `01a140a1-731e-7bf0-ad32-b6650f109b61`:

```json
{"resultado":"solto","nota_tocada":true,"stop_hook_active":false,"tinha_marca":true}
```

A marca foi às 14:34:54; o fim às 14:35:18. Não houve devolução intermediária nessa sessão. A liberação ocorreu pela alteração da nota, sem recorrer à guarda de segunda parada. Evidência: `logs\rodada3\codex-stop-tocada.txt` e a própria nota.

Fonte: [Hooks — Stop](https://learn.chatgpt.com/docs/hooks#stop), trecho `automatically creates a new continuation prompt`. A saída `decision: block` solicita continuação; saída zero sem conteúdo permite seguir. O ramo de liberação também está diretamente verificável em `scripts\fim.py`. O teste anterior de devolução não foi repetido nesta rodada.

## 3. Correlato de mod: o que realmente existe

A conclusão anterior deve ser refinada: **não encontrei uma API pública de módulos arbitrários dentro do processo equivalente aos mods citados do Claude**, nas fontes abaixo. Porém há várias integrações externas capazes de executar código ou intervir no fluxo. Ausência universal de API não pode ser provada por esta pesquisa.

| Caminho | Capacidade e limite | Teste nesta máquina |
|---|---|---|
| Hooks de comando | `Stop` continua o agente; `PreToolUse` pode negar chamadas cobertas. Processo externo. | **Passou** nos dois casos |
| Plugin | Distribui skills, MCP/apps e hooks. Empacotar hooks não cria API de código dentro do processo. | **Não testado** instalar plugin; hooks equivalentes testados diretamente |
| `notify` | Executa programa externo ao completar o turno; não recebe uma resposta de veto do programa. | **Passou**, inclusive com saída 2 |
| App-server | Cliente JSON-RPC recebe conclusão de turnos e pedidos de aprovação; pode responder recusando aprovações solicitadas. Não intercepta universalmente toda ação que já foi autorizada. | Inicialização, criação de conversa e alteração de nome **passaram**; veto por aprovação e conclusão ao vivo **não testados** |
| SDK TypeScript | Invólucro do CLI; stream permite reagir a `turn.completed`, e aplicação pode chamar outro `run()`. Não é extensão carregada no TUI existente. | Código conferido; **não testado** instalar/usar SDK |
| MCP / extensões de plugins | Executam as ferramentas que fornecem. Não foi encontrada nas fontes consultadas assinatura geral de fim de turno ou veto de todas as ferramentas por um MCP comum. | **Não testado** construir MCP ou extensão nova |

Fontes primárias e trechos:

- [Hooks — cobertura](https://learn.chatgpt.com/docs/hooks#tool-coverage): `Some specialized tool paths can opt out of the default hook path.` Não tratar hooks como fronteira completa de isolamento. [Saída PreToolUse](https://learn.chatgpt.com/docs/hooks#pretooluse) documenta `permissionDecision: "deny"`.
- [Plugins](https://developers.openai.com/plugins/build/plugins#bundled-mcp-servers-and-lifecycle-hooks): `Lifecycle hooks are supported for plugins installed manually in Codex desktop`. A mesma página declara `extensions.com.openai.hooks`; não declara módulo equivalente ao mod pesquisado.
- [Configuração avançada — notify](https://learn.chatgpt.com/docs/config-file/config-advanced): `currently only agent-turn-complete`. [Implementação 0.161.0](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/hooks/src/legacy_notify.rs), trecho `command.spawn()`: stdout/stderr são descartados e o processo é iniciado sem aguardar seu resultado para vetar o turno.
- [App-server](https://learn.chatgpt.com/docs/app-server): métodos `turn/completed`, `item/commandExecution/requestApproval` e `item/fileChange/requestApproval`. Trecho `Client responds with one of the command execution approval decisions above`. Requer implementar um cliente/host, não apenas instalar um hook no CLI.
- [SDK README 0.161.0](https://github.com/openai/codex/blob/rust-v0.161.0/sdk/typescript/README.md): `It spawns the CLI and exchanges JSONL events over stdin/stdout.` [Eventos](https://github.com/openai/codex/blob/rust-v0.161.0/sdk/typescript/src/events.ts) declara `TurnCompletedEvent`.

Teste concreto de veto: hook `PreToolUse` temporário na bancada, matcher `apply_patch|Edit|Write`, hashes obtidos por `hooks/list` e confiados só pela linha de comando. O agente tentou criar `logs\rodada3\DEVE-FALTAR.txt`; o router registrou `Command blocked by PreToolUse hook: BANCADA-DENY`. O arquivo não existe; resposta final `RECUSADO`. O hook recebeu `tool_name: apply_patch` e os argumentos do patch.

Na mesma sessão, `notify` chamou um script que gravou o payload e saiu com código 2. Recebeu `type: agent-turn-complete`, `client: codex_exec`, IDs, cwd e resposta `RECUSADO`. O JSONL teve um único `turn.completed`, sem continuação. Evidências: `deny-event.json`, `deny-notify-jsonl.txt`, `notify-payload.json`, `deny-command.json`, `hooks-list.txt` e `test_deny_notify.py` em `logs\rodada3`. O arquivo local `.codex\hooks.json` foi restaurado byte a byte em `finally`, comparação **True**.

## 4. Vigia continuamente visível

**Não há item de comando nas listas conferidas. Há título de terminal configurável e nome de conversa alimentável por API; visibilidade dinâmica na TUI não foi comprovada.**

- [Referência de configuração](https://learn.chatgpt.com/docs/config-file/config-reference): `tui.terminal_title` aceita uma lista de identificadores; trecho `Defaults to ["spinner", "project"]`. Isso é um recurso real além da status line.
- [StatusLineItem 0.161.0](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/tui/src/bottom_pane/status_line_setup.rs): trechos `ThreadName` e `ThreadTitle`. [TerminalTitleItem](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/tui/src/bottom_pane/title_setup.rs) também contém `ThreadName` e `Thread`. Nenhum dos dois enums contém item que execute comando ou leia um arquivo arbitrário.
- [Emissão de título](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/tui/src/terminal_title.rs): trecho `execute!(stdout(), SetWindowTitle(title))`. Usa OSC e exige stdout ser terminal; a aceitação final depende do terminal hospedeiro. Não houve captura visual no Maestri.
- [App-server — nomes](https://learn.chatgpt.com/docs/app-server): trecho `emits thread/name/updated`. Testei `thread/start` → `thread/name/set` → `thread/read`: nome lido igual a `vigia: sync ok 23:50 colisao=nao`, e notificação correspondente recebida. Na conversa efêmera, atualização foi recusada com `ephemeral thread does not support metadata updates`. Logs `appserver-name.json` e `appserver-name-persisted.json`.
- [Hooks — campos comuns](https://learn.chatgpt.com/docs/hooks#common-output-fields): `systemMessage` é aviso na UI ou stream de eventos. O hook de veto emitiu `VIGIA-SONDA sync ok 23:50 colisao=nao`, mas essa mensagem não apareceu no JSONL capturado; **exibição na UI não verificada**. Isso não estabelece uma superfície persistente com atualização periódica.
- Notificação externa é possível via `notify` e foi executada, mas toast do Windows e atualização contínua **não foram testados**.

A [última versão estável consultada](https://github.com/openai/codex/releases/tag/rust-v0.162.1) é **0.162.1**. Baixei os dois arquivos de enum dessa tag: são idênticos byte a byte aos da 0.161.0. Portanto atualizar para essa versão não adiciona um item de comando nesses pontos. Não instalei atualização; restante da versão e builds alpha **não verificados**.

Uma configuração candidata seria `-c 'tui.status_line=["thread-name"]' -c 'tui.terminal_title=["thread-name"]'`, com um host atualizando o nome via app-server. **Não foi testado** o encadeamento hook → API do servidor que atende a TUI → redraw, nem atualização por outra instância de app-server. Um hook isolado não ganha automaticamente um canal para o servidor do TUI. Também não foi testado emitir OSC diretamente por um hook; stdout do hook participa do protocolo de saída capturada, então não há evidência de que chegue ao terminal como controle de título.

Vale contribuir com o caso de uso em pedido existente, evitando duplicata: [#20244 — custom command-backed TUI status line](https://github.com/openai/codex/issues/20244), trecho `show custom text, colors, and conditional status information`. Não publiquei nada. Texto sugerido:

> Please support a command-backed status-line item that refreshes while Codex is idle and working. We need to show local sync health and collision state throughout a session. Built-in thread-name/title items require changing conversation metadata; hook systemMessage and notify are transient. Suggested contract: JSON session context on stdin, one bounded text line on stdout, configurable refresh interval and timeout, last-success value with a stale marker on failure, and explicit trust for the command. Reproduced on Windows CLI 0.161.0; status/title enums are unchanged in 0.162.1. Is there a supported way to supply external status without renaming the thread?

## Estado final e limites

**Nenhum arquivo global de configuração foi alterado nesta rodada.** Antes dos testes, copiei `~/.codex/config.toml` e `~/.codex/hooks.json` para `backup-globais\rodada3`; no fim, hashes das cópias e originais coincidiram. Não houve restauração global porque não houve alteração.

| Arquivo | SHA-256 antes = depois / estado |
|---|---|
| `~/.codex/config.toml` | `A6CAE9FA9397B2B3C5757642583146A7584B19ABC4809AF0604A7514EB397DE1` |
| `~/.codex/hooks.json` | `D822FA388C1D2F07207616FC672549AEC24EB687CD022B6FF5B8405413590F42` |
| `~/.claude/settings.json` | Igual, hash registrado no manifesto |
| `~/.claude/CLAUDE.md` | Igual, hash registrado no manifesto |
| `~/.copilot/copilot-instructions.md` | Igual, hash registrado no manifesto |
| `~/.copilot/settings.json` | Ausente antes e depois |

Manifestos completos: `logs\rodada3\globais-antes.json` e `globais-depois.json`, todos os campos `igual=True`. Pastas globais de hooks/extensões de Claude/Copilot não foram escritas. Os testes de sandbox podem atualizar seus próprios logs, marcadores e ACLs; os hashes acima cobrem os arquivos de configuração, não todo o estado do sistema.

Processos abertos foram aguardados ou encerrados pelo PID, com `finally` nos testes app-server. Foi feita busca de descendentes pelos PIDs dos testes; nenhum permaneceu. O processo curto de `notify` também já havia terminado. Evidência: `processos-restantes.json` e log dos testes. Não houve encerramento por nome. A primeira tentativa app-server usou uma opção não aceita (`--ignore-user-config`) e saiu com código 2; foi corrigida após consultar o help. Os testes válidos rodaram com o global intacto e `-c notify=[]`, exceto o teste explícito de notificação.

Ficaram na bancada os logs, fontes, scripts de teste, a linha da nota e o arquivo `shell-fullaccess-ok.txt`. Ficou uma conversa persistida de teste, sem turno de modelo, criada para verificar o nome; isso é histórico de uso, não alteração de configuração. Os demais turnos CLI usaram `--ephemeral`. Não li nem copiei arquivos de credenciais. No repositório `context-hub`, só este arquivo de entrega foi escrito.
