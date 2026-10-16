---
titulo: Por onde cada agente grava, e como a gravação confere a versão
ticket: 11
aberta: 2026-10-15
estado: absorvida
---

Com a busca decidida hoje, este ticket destravou. Ele decide por onde o agente grava (direto no disco, pelo MCP do
banco ou pelos dois) e como cada caminho cumpre a garantia já fixada: nenhuma gravação desfaz outra sem que o agente
veja; se o arquivo mudou desde a leitura, a gravação é recusada, e o agente relê e refaz.

Em que esta rodada se apoia, já decidido:
- o agente "também pode editar direto no disco, com sync para a outra máquina" (critério 3 do destino);
- a verdade mora no CouchDB de cada máquina; o CLI do LiveSync, sempre ligado, leva ao banco em cerca de 2 s o que
  qualquer agente grava no disco, mas essa gravação não confere a versão ("Revisão do sync e da divergência");
- a versão modificada do MCP do banco devolve a versão na leitura e transforma em conflito visível a gravação feita
  sobre uma versão velha; é obrigatória antes de usar o hub ("Como a verdade viaja entre as máquinas");
- a busca (obsidian-hybrid-search) só lê; gravar vai pelo MCP do banco ("Camada de busca");
- hooks moram no escopo do usuário nos três harnesses e saem na hora fora do hub ("Acesso dos agentes: decisão");
- clientes (sandbox, máquina de passagem) usam o MCP de um par pela tailnet, por padrão só de leitura, e nunca
  recebem a senha do CouchDB ("Onde o servidor mora");
- o Claude Desktop lê pela ponte `mcp-remote`, e você pediu que ele "não deve ser proibido de escrever no
  C:/context-hub diretamente" ("Portas de entrada do hub").

**O que cada ferramenta de gravação já confere hoje:**

| Ferramenta | Confere se o arquivo mudou? | Fonte |
|---|---|---|
| Edit do Claude Code (troca um trecho) | sim, pelo conteúdo: só grava se o trecho antigo ainda está no arquivo, igual | documentação oficial do Claude Code, "Edit tool behavior" |
| Write do Claude Code (regrava o arquivo inteiro) | a página não descreve conferência; modelos novos regravam até um arquivo que nem leram | mesma página, "Write tool behavior" |
| `edit_note` do MCP do banco, troca de trecho | sim, recusa texto velho | spike do CouchDB e LiveSync |
| `write_note` do MCP do banco | hoje não; com a versão modificada, sim | spike do CouchDB e LiveSync |
| `apply_patch` do Codex e a edição do Copilot | não verificado | — |
| Comando de shell (`>`, script) | não, em nenhum harness | — |

**Por que gravar pelos dois caminhos:** o disco é o que o critério 3 promete, e a troca de trecho já confere a versão
sozinha. O furo é a regravação inteira; mandá-la ao MCP do banco fecha o furo com um mecanismo (o hook), não com uma
regra a lembrar ("Lições do vault": falha se corrige com mecanismo). Gravação por shell fica coberta só pelo contrato.

**Por que o Desktop pelos dois:** você pediu a gravação direta. O Cowork lê e grava as pastas conectadas ("Claude can
only read and write files in folders you've connected", suporte da Anthropic), mas não se sabe se ele lê o
`AGENTS.md` (a doc fala de "Folder instructions") nem se a ferramenta de arquivo dele confere a versão, e os hooks do
hub não chegam a ele. Pelo MCP, a gravação confere a versão; o `instructions` do MCP não chega ao Desktop, e a
descrição das ferramentas chegar a ele é provável, mas não verificado.

**Por que o cliente com gravação ligável:** o contrato de retomada exige gravar a nota do trabalho, e um cliente só de
leitura perde a nota quando a sessão acaba. Uma segunda instância do MCP com escrita, com token próprio, mantém a
regra de o cliente nunca receber a senha do CouchDB (duas instâncias no mesmo banco já conviveram no teste das portas).

## Por onde o agente grava, nas sessões do Claude Code, do Codex e do Copilot
id: disco-ou-mcp
tipo: escolha
recomendada: A

- A: Pelos dois, cada um no que confere: no disco, só troca de trecho (Edit do Claude Code, `apply_patch` do Codex, a edição do Copilot), que grava só se o trecho antigo ainda está lá; a regravação inteira de um arquivo que já existe no hub vai pelo `write_note` do MCP do banco, com a versão lida. Um hook antes da ferramenta, no escopo do usuário, recusa a regravação inteira no disco e manda usar o MCP. Arquivo novo pode nascer no disco. O que o Codex e o Copilot conferem na troca de trecho é conferido na construção
- B: Pelos dois, com o disco livre e uma guarda por marca: um hook guarda a marca do arquivo (o hash) quando o agente lê e recusa qualquer gravação no disco se a marca mudou, inclusive a regravação inteira. Mais construção, e não se sabe se o Codex e o Copilot deixam um hook ver a leitura
- C: Antes de decidir, um teste curto: o que o Edit e o Write do Claude Code, o `apply_patch` do Codex e a edição do Copilot fazem quando o arquivo muda entre a leitura e a gravação, e se o hook antes da ferramenta recusa a regravação inteira nos três. Custo estimado: 100 a 200 mil tokens de um subagente, cerca de 1 hora; o erro de sandbox do Codex nesta máquina, ainda em pesquisa em "Acesso dos agentes: decisão", pode travar a parte do Codex

## Por onde o Claude Desktop grava
id: desktop
tipo: escolha
recomendada: A

- A: Pelos dois: a pasta `C:\context-hub` conectada no Cowork, para ler e gravar, com "Folder instructions" que mandam ler o `AGENTS.md` da raiz; e o MCP do banco com escrita pela ponte `mcp-remote` (localhost, com token), cuja descrição das ferramentas leva o "antes de gravar, leia `AGENTS.md`". Na pasta conectada, a gravação fica sem a guarda de versão do hub até a construção mostrar o que a ferramenta do Cowork confere
- B: Só pela pasta conectada, com as "Folder instructions"; sem MCP de escrita no Desktop. Mais simples, e a gravação nunca confere a versão pelo hub
- C: Antes de decidir, um teste seu no Desktop: conectar uma pasta de teste, ver se ele segue o `AGENTS.md` dela e o que acontece quando o arquivo muda entre a leitura e a gravação. Custo: cerca de 20 minutos seus, com cliques no app; nenhum token de subagente

## O cliente grava no hub?
id: cliente
tipo: escolha
recomendada: A

- A: Gravação ligável por cliente: o padrão continua só de leitura; quando você quiser, o cliente recebe o token de uma segunda instância do MCP do banco, com escrita e a mesma guarda de versão, exposta só na tailnet. A senha do CouchDB continua só nos pares. Como esse MCP chega ao cliente (endereço, junto com a busca) é de "Acesso dos agentes: decisão"
- B: Só leitura sempre: o cliente não grava, e a nota de retomada de um trabalho feito num cliente se perde quando a sessão acaba; o trabalho que precisa de nota é feito num par

## Algo mais?
id: algo-mais
tipo: texto
