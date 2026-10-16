# Fontes da rodada 7 de "Acesso dos agentes: decisão" (ticket 14)

Nome sugerido no portal: `2026-10-15-acesso-dos-agentes-decisao-r7.md` (a maior existente é a r6).

## Lido

- Ticket 14 inteiro, com os comentários até a entrega da pesquisa do Codex (~15h50).
- `bancada-acesso-codex.md` inteiro; `bancada-acesso-relatorio.md`, seção 8 (MCP com token; no `codex exec` com
  aprovação `never`, a chamada do MCP só passou com `mcp_servers.<id>.default_tools_approval_mode="approve"`).
- Rodadas r1, r3 e r4 do ticket 14 e a lista de títulos da r2; as respostas estão absorvidas nos comentários do ticket.
- Ticket 09 "Camada de busca", `## Answer` (herança: juntar o MCP da busca e o do banco num endereço só; servidor HTTP
  do obsidian-hybrid-search com `--host` e `--allowed-host`, sem autenticação descrita no README).
- Ticket 11 "Como os agentes gravam no hub": aberto (claimed), rodada 1 aberta sem resposta. A opção A da pergunta do
  cliente diz que "como esse MCP chega ao cliente (endereço, junto com a busca) é de Acesso dos agentes: decisão".
- `map.md` (Not yet specified, Out of scope), `estrategia-pos-pesquisa.md` (proxy de MCP como endpoint único na
  tailnet, dono: ticket 14), `exploracao/anexos/levantamento-14-acesso-dos-agentes.md` (lista de decisões abertas).
- Fichas da pesquisa ampla: `laco/sintese/s3/tbxark-mcp-proxy.json` e `laco/sintese/s3/1mcp-agent.json`.
- Memórias das regras de rodada (essencial na opção, conferir decisões, carta, oportunidades, acervo, portal decide).
- `Blocked by` (04, 13, 18, 25, 33, 34, 36, 40, 42, 46): todos resolvidos.

## Fonte primária conferida agora (2026-10-15, branch padrão, não a tag v1.1.0)

- TBXark/mcp-proxy, `docs/USAGE.md`, seção "Endpoints": "For `type: streamable-http`: `https://mcp.example.com/fetch/mcp`"
  (uma rota por servidor, não um endpoint fundido). Seção "Auth": "If `options.authTokens` is set for a server, requests
  must include the token in the `Authorization` header", nas formas `Bearer <token>` e `<token>`. Seção "Health checks":
  `/_healthz` e afins não exigem token e expõem os nomes dos servidores; a doc manda prender o proxy a endereço interno.
- TBXark/mcp-proxy, `docs/CONFIGURATION.md`: `addr` ("Bind address (e.g. `:9090`)"), `authTokens` por servidor e global,
  `toolFilter` (allow/block). O formato mudou ("`authTokens` move into the entry's `options`"); conferir na versão
  instalada.
- 1MCP, README: "`1mcp serve` aggregates your MCP servers"; `docs/en/guide/advanced/authentication.md`: "enables OAuth
  2.1 bearer protection for MCP transport", com painel em `/oauth` e refresh token rotativo de uso único.

## Não verificado (vai para o Answer)

- O TBXark repassar o `instructions` do MCP (o Copilot usa com `--allow-all-mcp-server-instructions`); latência pela
  tailnet; prender o `addr` ao IP da tailnet no Windows.
- Os hooks do Codex rodando com `danger-full-access` (testados só com o não elevado).
- A notificação do Windows pelo `notify` (o `notify` rodou; o toast não).
- O caminho app-server, nome da conversa, barra de estado de ponta a ponta.
- O sandbox elevado na outra máquina do par; o processo que segura o `node_repl.exe`.
- Qual conta está logada no `gh` desta máquina (a opção A da pergunta 2 publica "na sua conta").
- `${env:...}` no `mcp.json` do VS Code; o mod de fim num Claude Code gerenciado pela empresa; o que a `statusLine` do
  Copilot mostra na tela.

## Ficou de fora da rodada, e por quê

- Gravação do cliente e o Claude Desktop: são de "Como os agentes gravam no hub" (rodada 1 aberta). A rodada só
  reserva a rota de escrita no proxy, condicionada a ele.
- Itens 1, 6, 11 e 14 do levantamento (forma do adaptador, cliente e skills, GSD no arquivo global do Copilot, plugin
  para o VS Code): nenhum comentário do ticket os reabriu; o teste da empresa mostrou que nenhuma política barra o MCP
  avulso, então o plugin para o VS Code não é necessário agora. Se o maestro achar que algum ainda está aberto, vai
  numa rodada própria.

## Rascunho do `## Answer` do ticket 14 (com as recomendadas)

## Answer

**Cada agente carrega o contrato, as skills, os hooks e o MCP do hub assim** (rodadas 1 a 7; testes na bancada de
acesso, no Maestri e com a conta da empresa).

- **Contrato e skills:** o arquivo global de cada harness, por link simbólico; as skills por junction; no Maestri,
  `claude-md-and-agents-md` ligado em cada par ("Maestri: padrão e liberdade"). Codex e Copilot chegam ao `AGENTS.md`
  da raiz numa subpasta ou na pasta de um papel pelo `.git` da raiz; o kit não cria marcador de raiz (rodada 4). O
  contrato não carrega em dobro.
- **Hooks:** no escopo do usuário nos três harnesses, saindo na hora fora do hub (rodada 3). No Codex, o kit deixa
  cada hook aprovado pelo hash em `hooks.state`; no Copilot, só hook de usuário (o de projeto exige pasta confiável).
- **Checagem de início:** no par, o hook lê o arquivo da vigia; sem ele, a ferramenta do MCP; no cliente, a ferramenta
  do MCP. Onde o hook falhar, vira regra no contrato daquele harness (rodada 2). Passou nos três, dentro e fora do
  Maestri, com o `MAESTRI_TERMINAL_ID` do próprio recruta.
- **Fim da resposta:** Claude Code pelo mod (`turn.start` com `classic.Stop`); Copilot pelo hook `agentStop` junto com
  a extensão `onAgentStop` (`--experimental`) (rodada 3); Codex pelo hook `Stop`, que devolve e solta, sem correlato de
  mod. A recusa antes da ferramenta no Codex é o `PreToolUse` (testado no `apply_patch`). App-server e SDK do Codex
  ficam como reserva.
- **Estado da vigia na tela:** Claude Code pelo mod; Copilot pela `statusLine`; Codex na checagem de início, com o
  `notify` no fim de cada turno disparando a notificação do Windows quando há divergência. Pedido upstream: comentário
  na issue #20244 do Codex, publicado pelo maestro com o `gh` na conta do Gustavo.
- **Codex:** com `danger-full-access` nas duas máquinas, porque o sandbox elevado falha (erro 32 no `node_repl.exe`,
  issue #53679) e o não elevado deixa o agente sem shell. O kit roda o teste mínimo do elevado a cada atualização do
  Codex e avisa quando passar; voltar ao sandbox é decisão do Gustavo. As ferramentas do MCP do hub vão aprovadas de
  antemão (`default_tools_approval_mode="approve"`).
- **MCP no par:** o do banco preso a 127.0.0.1 com token de variável de ambiente (rodada 1); a busca
  (obsidian-hybrid-search) escuta só em 127.0.0.1; os agentes do par usam os dois direto.
- **MCP no cliente:** o TBXark/mcp-proxy em cada par, preso ao endereço da tailnet, uma porta, uma rota e um token por
  servidor: `/busca/mcp` e `/banco/mcp` (só leitura). Se "Como os agentes gravam no hub" ligar a gravação do cliente,
  ela entra como `/banco-escrita/mcp`, com token próprio. Token de variável de ambiente no cliente, `Authorization:
  Bearer` nos três harnesses.
- **Conta da empresa:** no VS Code e no Copilot CLI, o MCP com token passou; nenhuma política que barre hooks ou MCP
  está aplicada; sem plugin do hub por ora (rodadas 5 e 6).
- **Fica para "Como os agentes gravam no hub":** se o cliente grava (e a nota de retomada nele) e como o Claude Desktop
  grava e recebe o contrato.
- **Não verificado, para a construção:** hooks do Codex com acesso total; o toast pelo `notify`; o TBXark repassar o
  `instructions` do MCP e a latência pela tailnet; `${env:...}` no `mcp.json` do VS Code; o mod de fim num Claude Code
  gerenciado pela empresa; o que a `statusLine` do Copilot mostra; o sandbox elevado na outra máquina.
