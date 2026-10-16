# Vigia pelo nome da conversa — Codex, ticket 14, rodada 7

Teste em 15/10/2026, aproximadamente 16:12–16:23 (São Paulo), por Sonda Codex. CLI **0.161.0**, `gpt-6-luna`, esforço `low`, conversa persistida, permissões **danger-full-access**. Artefatos em `C:\Projetos\bancada-acesso\nome-conversa\`. Sem publicação ou commit.

**Serve se o programa da vigia e o TUI forem clientes do mesmo app-server.** Nesse arranjo, três renomeações chegaram à barra de estado e geraram três títulos OSC sem interação no TUI. **Outra instância independente do app-server, usando apenas o mesmo histórico, não atualizou o TUI local isolado que já estava aberto**, nem depois de um turno novo. Não foi necessário construir um host: usei o app-server e o TUI nativos.

Limite da prova do título: capturei as sequências OSC emitidas ao terminal próprio e o conteúdo da tela de caracteres. **Não inspecionei visualmente uma janela/aba nativa do Windows Terminal ou a decoração de um terminal do Maestri.** Portanto o envio do título está comprovado; a apresentação visual pelo terminal de destino permanece não verificada.

## Como foi executado

Abri um TUI próprio em um pseudoterminal ConPTY de 80 × 24, sem operar outras janelas. O comando inicial usou:

```powershell
codex --no-alt-screen --no-daemon -C C:\Projetos\bancada-acesso\nome-conversa `
  -s danger-full-access -a never -m gpt-6-luna `
  -c 'model_reasoning_effort="low"' -c 'notify=[]' `
  -c 'tui.status_line=["thread-name"]' `
  -c 'tui.terminal_title=["thread-name"]' `
  'Diga somente SONDA-NOME-INICIAL. Nao use ferramentas nem subagentes.'
```

O primeiro turno terminou, e `/status` confirmou a conversa **`01a140fb-0b4a-7762-ba0f-8bdbd54510b6`**. Seu nome inicial gerado foi `Dizer SONDA-NOME-INICIAL`, visível no rodapé e no OSC. Usei `--no-daemon` para isolar esse processo dos serviços do usuário. **O modo padrão com conexão automática a um daemon existente não foi testado**; a conclusão negativa abaixo se refere ao modo local isolado.

O programa externo `rename.py` abriu uma instância stdio de app-server, inicializou o protocolo, chamou `thread/name/set` nessa conversa e conferiu `thread/read`. Cada instância foi encerrada pelo PID. Houve três renomeações válidas com intervalos de 17 e 24 segundos. Durante a observação sem entrada no TUI, nenhuma delas produziu atualização de tela ou título. Um novo turno, respondido com `SONDA-NOME-SEGUNDO`, redesenhou a tela mantendo o nome antigo. Uma nova instância stdio leu o último nome da vigia, confirmando persistência fora da memória do primeiro servidor.

Em seguida iniciei **um servidor local próprio**:

```powershell
codex app-server --listen ws://127.0.0.1:18799 `
  -c 'notify=[]' -c 'sandbox_mode="danger-full-access"'
```

Conectei o TUI nativo ao mesmo servidor:

```powershell
codex --remote ws://127.0.0.1:18799 --no-alt-screen `
  -c 'tui.status_line=["thread-name"]' `
  -c 'tui.terminal_title=["thread-name"]' `
  resume 01a140fb-0b4a-7762-ba0f-8bdbd54510b6
```

A tentativa de abrir a mesma conversa simultaneamente encontrou **“This conversation is open in another app”**. Encerrei normalmente o primeiro TUI com `/exit` e usei `r` no segundo, ambos meus. A retomada carregou o nome persistido da vigia. Não forcei nem alterei locks.

O script externo `ws_rename.mjs`, usando o WebSocket nativo do Node, conectou como **outro cliente do mesmo servidor**, enviou `initialize`/`initialized`, `thread/name/set` e `thread/read`. Não enviou prompts, teclas, comandos de redraw ou `thread/resume`. Três renomeações, separadas por 10 e 26 segundos, atualizaram o TUI já aberto sem interação. Depois de um turno novo, respondido com `SONDA-NOME-REMOTE`, o último nome continuou presente. Um app-server stdio independente também leu esse nome final persistido.

## Tabela caso × resultado

“Título” abaixo significa a sequência **OSC 0** efetivamente capturada; não uma captura visual da moldura da janela do Windows.

| Caso | Disco / `thread/read` | Barra do TUI aberto | Título OSC do TUI | Resultado |
|---|---|---|---|---|
| TUI local, primeiro turno | Conversa persistida; nome `Dizer SONDA-NOME-INICIAL` | Nome inicial | Nome inicial | **Passou**: base válida |
| Outra instância, renomeação 1 | `vigia: ok 16:14:25` | Manteve nome inicial | Manteve nome inicial | **Falhou** para atualização ao vivo |
| Outra instância, renomeação 2 | `vigia: colisao 16:14:42` | Manteve nome inicial | Manteve nome inicial | **Falhou** para atualização ao vivo |
| Outra instância, renomeação 3 | `vigia: desconhecido 16:15:06` | Manteve nome inicial | Manteve nome inicial | **Falhou** para atualização ao vivo |
| TUI local, turno novo após as renomeações | Nova instância ainda leu `vigia: desconhecido 16:15:06` | Continuou `Dizer SONDA-NOME-INICIAL` | Nenhum novo título da vigia | **Falhou** mesmo com novo turno |
| Retomada no TUI `--remote`, após fechar o local | Leu nome persistido | `vigia: desconhecido 16:15:06` | Mesmo nome | **Passou** ao retomar; isso sozinho não provaria atualização ao vivo |
| Segundo cliente no mesmo servidor, renomeação 1 | `vigia: ok 16:17:54` | Atualizou sem interação | `ESC ] 0 ; vigia: ok 16:17:54 BEL` | **Passou** ao vivo |
| Mesmo servidor, renomeação 2 | `vigia: colisao 16:18:04` | Atualizou sem interação | Mesmo nome novo em OSC | **Passou** ao vivo |
| Mesmo servidor, renomeação 3 | `vigia: desconhecido 16:18:30` | Atualizou sem interação | Mesmo nome novo em OSC | **Passou** ao vivo |
| Mesmo servidor, turno novo após renomeações | Nome final persistido, lido por outra instância | Manteve último estado durante/depois do turno | Manteve último título | **Passou** no período observado |
| Hook emitindo OSC diretamente | Não executado | Não verificado | Não verificado | **Opcional não testado** |
| Decoração visual de Windows Terminal/Maestri | — | Não inspecionada nessa interface | Não inspecionada visualmente | **Não verificado**; não confundir com emissão OSC |

As observações negativas valem para a janela de teste; não são afirmação de que a atualização jamais poderia ocorrer por outro evento, retomada ou backend.

## Evidências de tela e protocolo

- `logs\terminal-local.json` e `terminal-remote.json`: saída ANSI original capturada dos dois pseudoterminais, incluindo movimentos do cursor, rodapé e OSC. Os primeiros/últimos nomes não foram apenas respostas de `thread/read`.
- `logs\screen-local.txt` e `screen-remote.txt`: tela reconstruída do fluxo ANSI; o rodapé local permanece antigo e o remoto contém a vigia.
- [Imagem da captura local reconstruída](C:/Projetos/bancada-acesso/nome-conversa/logs/screen-local.png) e [imagem da captura remota reconstruída](C:/Projetos/bancada-acesso/nome-conversa/logs/screen-remote.png). **São reconstruções do terminal capturado, não screenshots nativas de janelas.** A linha superior “OSC titulo” foi acrescentada pelo renderizador para mostrar o último título capturado.
- `logs\titles-local.json` e `titles-remote.json`: títulos extraídos das sequências OSC. Na captura remota aparecem, na ordem, os três estados.
- `logs\rpc-1.json`, `rpc-2.json`, `rpc-3.json`: renomeações via instâncias independentes; `rpc-after-turn.json`: leitura após o turno local.
- `logs\ws-rpc-1.json`, `ws-rpc-2.json`, `ws-rpc-3.json`: requisições e respostas do segundo cliente no mesmo servidor; `rpc-final-read.json`: leitura independente final.
- `logs\final-verification.json`: assertivas confirmaram as três sequências OSC remotas, as leituras correspondentes, o turno novo e a ausência de texto `vigia:` na saída do TUI local capturada.

## Fontes primárias e interpretação

1. [Documentação oficial — conectar o TUI](https://learn.chatgpt.com/docs/app-server#connect-the-cli-terminal-ui): exemplo **`codex --remote ws://127.0.0.1:4500`**, acompanhado do servidor `--listen`. Esse é o caminho documentado usado no teste positivo. A mesma página caracteriza o transporte WebSocket como **“experimental and unsupported”**; isso entra no custo de adotar o arranjo.
2. [Documentação oficial — métodos do app-server](https://learn.chatgpt.com/docs/app-server): `thread/name/set`, trecho **“emits thread/name/updated”**. Define atualização de nome de conversa carregada ou persistida. A documentação não promete que uma instância independente retransmita mudanças a um TUI de outro processo só por compartilhar o histórico.
3. [TUI 0.161.0 — recebimento da notificação](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/tui/src/chatwidget/protocol.rs): o ramo `ServerNotification::ThreadNameUpdated` chama **`self.on_thread_name_updated(...)`**. É compatível com o resultado positivo quando o TUI recebe o evento do mesmo servidor.
4. [TUI 0.161.0 — aplicação do nome](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/tui/src/chatwidget/session_flow.rs): para o ID exibido, atribui `self.thread_name` e chama **`self.refresh_status_surfaces(); self.request_redraw();`**. Isso explica o redraw sem prompt nem teclado; a observação foi confirmada no terminal.
5. [TUI 0.161.0 — superfícies de estado](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/tui/src/chatwidget/status_surfaces.rs): `ThreadName` usa `self.thread_name`. [Emissão do título](https://github.com/openai/codex/blob/rust-v0.161.0/codex-rs/tui/src/terminal_title.rs), trecho **`SetWindowTitle(title)`**, documenta o caminho OSC para stdout terminal. A decoração visual depende do terminal hospedeiro.

A explicação “mudança em outro servidor atualiza o armazenamento, mas não entrega ao TUI local a notificação necessária” é **inferência** apoiada pela diferença entre os dois testes e pelo tratamento de notificação acima. Não fiz tracing completo dos IPCs nem provei ausência de toda forma de sincronização entre processos.

## Serve para a vigia? Custo e mudança na #20244

**Sim, como arranjo com servidor compartilhado**, para atualizar o rodapé e emitir o título; a apresentação visual da aba do terminal de destino ainda deve ser conferida. Um programa lateral pode ler o estado da vigia e chamar `thread/name/set` no **mesmo endpoint** que atende o TUI. Não é preciso implementar outro TUI ou host completo.

O custo é manter o app-server vivo, iniciar/conectar o TUI com `--remote`, identificar a conversa correta e gerenciar reconexão e frequência de atualização. O teste usou somente loopback, sem expor porta de rede. Não foi construída uma integração com o arquivo real da vigia; os três estados foram simulados. Repetir indefinidamente, falha/reconexão, vários TUIs, daemon automático, integração no Maestri e restauração automática do nome original **não foram verificados**.

O nome da conversa vira o estado da vigia também no histórico/listas, substituindo seu título útil. Após parar o programa lateral, o último texto/hora pode permanecer obsoleto; esse arranjo não fornece sozinho uma indicação de falha do atualizador. Esses são custos do mecanismo observado, não defeitos demonstrados neste teste.

**O texto sugerido para a #20244 precisa reconhecer o caminho que agora passou.** Manter o pedido por um item próprio de estado faz sentido para evitar renomear a conversa e para atender TUIs locais sem esse arranjo. Sugestão ao maestro, não publicada:

> We verified on Windows CLI 0.161.0 that a sidecar connected to the same app-server as the native `codex --remote` TUI can call `thread/name/set` and update the footer and terminal-title OSC while idle, without a new turn. A separate app-server over the same persisted history did not update an already-open isolated local TUI, even after another turn. The shared-server route works, but requires that connection setup and replaces the conversation's useful name with status text. Please consider a dedicated externally supplied status item with refresh/stale semantics, without renaming the thread. Is there a supported equivalent for an already-open local TUI?

## Estado final

**Nenhum arquivo global de configuração foi alterado.** Hashes SHA-256 antes/depois iguais, registrados em `logs\globais-antes.json` e `final-verification.json`:

| Arquivo | SHA-256 antes = depois |
|---|---|
| `~/.codex/config.toml` | `a6cae9fa9397b2b3c5757642583146a7584b19abc4809af0604a7514eb397de1` |
| `~/.codex/hooks.json` | `d822fa388c1d2f07207616fc672549aec24eb687cd022b6ff5b8405413590f42` |

Os overrides ficaram nas invocações. Não foi preciso restaurar globais. Há uma conversa persistida de teste com três turnos curtos e o nome final da vigia, além de logs normais do CLI; esse histórico é efeito esperado do teste, distinto de configuração. Não li credenciais nem usei dados de cliente.

Os TUIs foram fechados por `/exit`, com saídas capturadas em `terminal-local-exit.json` e `terminal-remote-exit.json`. Instâncias stdio foram encerradas pelo PID e sua árvore; o servidor WebSocket próprio, PID 94264, também foi encerrado por PID. `logs\processos-fim.json` confirma sete PIDs registrados sem processo vivo e listener 18799 fechado. Não encerrei por nome, não operei outras janelas e não parei serviços do usuário.

Para reconstruir as capturas, instalei `pyte`/`wcwidth` somente em `nome-conversa\vendor`; Pillow já estava disponível. Não houve atualização global do Codex. O aviso de atualização foi pulado. O TUI local registrou falhas de hooks preexistentes com acesso negado; esses hooks não foram modificados, e os turnos e testes de metadados concluíram. Duas tentativas de invocação tiveram erro de quoting e foram corrigidas antes dos ensaios válidos; não foram contadas como resultado de atualização de tela.

No repositório `context-hub`, só este arquivo de entrega foi escrito. Não foi publicada mensagem ou alteração na #20244.
