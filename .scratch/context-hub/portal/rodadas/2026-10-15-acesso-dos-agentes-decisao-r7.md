---
titulo: Acesso dos agentes: o Codex no hub e o endereço dos clientes
ticket: 14
aberta: 2026-10-15
estado: absorvida
---

A pesquisa do Codex chegou (`bancada-acesso-codex.md`, Codex 0.161.0, com fontes oficiais). Esta rodada fecha o que
falta para resolver o ticket: como o Codex roda no hub, como ficam nele o fim da resposta e o estado da vigia, e o
endereço por onde os clientes chegam ao MCP da busca e ao do banco.

Em que esta rodada se apoia, já decidido:
- hooks no escopo do usuário nos três harnesses, saindo na hora fora do hub (rodada 3 deste ticket);
- no Codex, o estado da vigia fica na checagem de início, com a notificação do Windows como reserva; você pediu que a
  pesquisa procurasse um jeito de mostrá-lo o tempo todo (rodada 3);
- o MCP do banco no par fica preso a 127.0.0.1, com token lido de uma variável de ambiente (rodada 1);
- os clientes (sandbox, máquina de passagem) usam pela tailnet o MCP de um par, só de leitura por padrão, com token, e
  nunca recebem a senha do CouchDB ("Onde o servidor mora");
- a busca é o obsidian-hybrid-search, que já serve MCP por HTTP; juntar o MCP da busca e o do banco num endereço só
  ficou para este ticket ("Camada de busca", resolvida hoje).

**O que a pesquisa do Codex achou:**
- **Por que o Codex não gravava nesta máquina:** o sandbox "elevado" (o modo que a documentação recomenda) falha ao
  ajustar a permissão de um programa do próprio Codex (`node_repl.exe`), que outro processo está segurando. É a
  mesma falha da issue #53679 do Codex, aberta em 13/10, ainda sem correção. Qual processo segura o arquivo não se
  descobriu, e a outra máquina do par não foi testada.
- **Sandbox não elevado:** passa. O `apply_patch` (a ferramenta de edição do Codex) grava, e o hook de fim solta o
  agente quando a nota de retomada muda. Mas o comando de shell falha ao abrir o PowerShell instalado pela loja da
  Microsoft (o atalho em `WindowsApps`). A documentação chama esse modo de "legacy fallback", com isolamento de rede
  mais fraco que o elevado.
- **Acesso total (sem sandbox):** shell e gravação funcionam. Não há isolamento nenhum do sistema.
- **Fim da resposta:** o hook `Stop` devolve o agente quando a nota não foi tocada e o solta quando foi; os dois casos
  passaram. O hook antes da ferramenta (`PreToolUse`) recusou um `apply_patch` de verdade.
- **Correlato de mod:** não existe módulo de código dentro do Codex. Existem, por fora: os hooks (testados), o `notify`
  (roda um programa no fim de cada turno, sem poder vetar; testado), o app-server (um programa ao lado do Codex que
  recebe o fim dos turnos e pode recusar pedidos de aprovação; o veto não foi testado) e o SDK.
- **Vigia o tempo todo:** a barra de estado e o título do terminal do Codex têm lista fechada de itens, sem item
  alimentado por um comando, e a versão nova (0.162.1) não mudou isso. O único caminho seria um programa ao lado do
  Codex renomear a conversa com o estado da vigia, e a barra mostrar o nome. A renomeação passou num teste isolado; o
  caminho inteiro até a tela, não.
- **Pedido ao Codex:** já existe uma issue pedindo exatamente isso, a #20244 ("custom command-backed TUI status line").
  O texto sugerido para comentar lá, em inglês:

  > Please support a command-backed status-line item that refreshes while Codex is idle and working. We need to show
  > local sync health and collision state throughout a session. Built-in thread-name/title items require changing
  > conversation metadata; hook systemMessage and notify are transient. Suggested contract: JSON session context on
  > stdin, one bounded text line on stdout, configurable refresh interval and timeout, last-success value with a stale
  > marker on failure, and explicit trust for the command. Reproduced on Windows CLI 0.161.0; status/title enums are
  > unchanged in 0.162.1. Is there a supported way to supply external status without renaming the thread?

  Em resumo: pede um item da barra de estado alimentado por um comando, com o caso de uso do hub, sem nada de cliente.

**O endereço dos clientes, o que existe:**
- **TBXark/mcp-proxy:** um programa só (binário para Windows), que fica na frente de vários MCP numa porta só. Cada
  servidor ganha uma rota (`/busca/mcp`, `/banco/mcp`), e cada rota aceita um token fixo próprio, no mesmo formato
  `Authorization: Bearer` que os três harnesses já passaram no teste com o MCP do banco.
- **1MCP:** junta as ferramentas de todos num endereço só (`/mcp`), mas a autenticação dele é OAuth 2.1 (painel de
  autorização e token que troca a cada uso), não o token fixo do teste.
- **O servidor HTTP do obsidian-hybrid-search:** o README só fala de restringir o nome do host; autenticação por token
  não aparece nele.

**Por que acesso total no Codex:** é o único modo em que shell e gravação passaram nesta máquina; o elevado espera uma
correção do Codex, e o não elevado deixa o agente sem shell. Os mecanismos do hub (hooks de início, de fim e de recusa)
não dependem do sandbox. Com acesso total eles não foram rodados; a construção confere.

**Por que publicar na #20244:** nenhum caminho de hoje mostra a vigia o tempo todo no Codex, e o pedido já existe;
somar o caso de uso a ele não abre duplicata nem custa nada além de um comentário público na sua conta.

**Por que o TBXark:** usa o mesmo token fixo que os três harnesses já passaram no teste, cobre a falta de autenticação
do servidor da busca (que deixa de ficar exposto) e aceita uma rota a mais, com token próprio, se o cliente puder
gravar. A dúvida antiga do repasse de MCP em stdio no Windows caiu: a busca e o banco já falam HTTP.

## Como o Codex roda no hub
id: codex-modo
tipo: escolha
recomendada: A

- A: Com acesso total (`danger-full-access`) em todo Codex do hub, nas duas máquinas: shell e `apply_patch` gravam (testado), sem isolamento do sistema. A proteção do hub fica nos hooks (início, fim e a recusa antes da ferramenta) e no contrato. O kit roda o teste mínimo do sandbox elevado a cada atualização do Codex e avisa quando ele passar; voltar ao sandbox fica para você decidir nessa hora
- B: Sandbox não elevado (`workspace-write` com `windows.sandbox="unelevated"`): grava pelo `apply_patch`, e o hook de fim solta (testado), mas o shell não abre o PowerShell da loja. Para ter shell, o kit teria de apontar outro PowerShell (o do Windows ou um instalado fora da loja), o que não foi testado. Modo que a documentação chama de legado, com isolamento de rede mais fraco
- C: Antes de decidir, um teste curto pelo recruta Codex: achar o processo que segura o `node_repl.exe` e ver se o sandbox elevado volta; o não elevado com um PowerShell fora da loja; e os hooks rodando com acesso total. Custo estimado: cerca de 1 hora do recruta, na cota do Codex

## O fim da resposta e a vigia no Codex
id: codex-fim-vigia
tipo: escolha
recomendada: A

- A: O fim pelo hook `Stop` (devolve e solta, testado) e a recusa antes da ferramenta pelo `PreToolUse` (testado), sem correlato de mod. A vigia fica na checagem de início, com o `notify` no fim de cada turno como reserva: ele dispara a notificação do Windows quando há divergência (a notificação em si não foi testada). O app-server e o SDK ficam guardados como reserva, se um dia um hook não bastar. E o maestro publica, na sua conta do GitHub, o comentário acima na issue #20244 (a conta logada no `gh` desta máquina não foi conferida; o maestro confere antes e mostra o link depois)
- B: Igual à A, sem publicar nada: o recurso fica só no radar, e o maestro confere a #20244 quando o Codex for atualizado
- C: Igual à A, e mais um teste do caminho pelo nome da conversa: um programa ao lado do Codex renomeia a conversa com o estado da vigia, e a barra de estado e o título do terminal mostram o nome. Custo estimado: cerca de 1 hora do recruta Codex; ninguém sabe se um programa separado alcança o Codex já aberto, e a conversa passa a ter o estado da vigia como nome

## O endereço dos clientes para a busca e o banco
id: endereco-clientes
tipo: escolha
recomendada: A

- A: O TBXark/mcp-proxy em cada par, preso ao endereço da tailnet, numa porta só, com uma rota e um token por servidor: `/busca/mcp` (o obsidian-hybrid-search, que passa a escutar só em 127.0.0.1) e `/banco/mcp` (a instância só de leitura). Se "Como os agentes gravam no hub" ligar a gravação do cliente, ela vira uma terceira rota, `/banco-escrita/mcp`, com outro token. O cliente leva duas entradas de MCP no mesmo endereço, com o token de uma variável de ambiente. Os agentes do próprio par seguem direto nos MCP locais, em 127.0.0.1
- B: O 1MCP em cada par, preso à tailnet: um endereço só (`/mcp`) com as ferramentas da busca e do banco juntas, e a escolha de ferramentas por cliente. A autenticação passa a ser OAuth 2.1 em vez do token fixo testado nos três harnesses
- C: Sem proxy: o cliente aponta para os dois servidores, cada um exposto na tailnet. O MCP do banco só de leitura vai com o token dele; o obsidian-hybrid-search abre para a rede com a opção de host, sem token, até a construção mostrar se ele aceita um. Uma peça a menos

## Algo mais?
id: algo-mais
tipo: texto
