# Contrato pelo MCP: pesquisa

Type: research
Status: resolved

## Question

Um cliente que só alcança o hub pelo MCP de um par recebe o contrato (`AGENTS.md`) por quais canais
do próprio MCP, no Codex, no Copilot CLI e no Copilot do VS Code? Para cada harness, o que a fonte
primária diz sobre: (C) a descrição das ferramentas do MCP chegar ao modelo, com limite de tamanho;
(D) o suporte a "prompts" e "resources" do protocolo MCP, e se algum deles entra no contexto sem ação
do usuário; e o campo `instructions` do servidor (o teste viu que não chega a Codex nem a Copilot;
conferir o que a doc diz). Sem inferência: o que a fonte não disser fica "não verificado", e o que só
um teste resolve fica "precisa de teste". Pedido do Gustavo em 2026-10-12 (resposta à R31 de "Portas
de entrada do hub").

## Comments

- Fatos de partida: grupo C de "Testes das portas de entrada" (`instructions` do MCP só chega ao
  Claude Code, cortado depois de uns 3.300 caracteres) e `exploracao/anexos/pesquisa-37-portas/porta-7-cliente-mcp.md`.
- O teste com o MCP já criado (o fork do es617) fica para um ticket na construção.

## Answer

Pesquisa concluída em 2026-10-12, só com fonte primária (documentação oficial, código aberto, changelog e
especificação do MCP). Nada foi testado. Relatório completo, com citações, listas de "não verificado" e
"precisa de teste" e a tabela harness × canal:
[`pesquisa-41-contrato-pelo-mcp.md`](../../../exploracao/anexos/pesquisa-41-contrato-pelo-mcp.md).

- **Codex CLI (0.161.0):** a documentação diz que o Codex lê o `instructions` e o usa "como orientação do
  servidor". No código, o texto vai na requisição como descrição do grupo ("namespace") das ferramentas do
  servidor, até 512 KiB, ou dentro da descrição da ferramenta de busca de ferramentas quando elas ficam adiadas.
  Isso contradiz o teste só em parte: o texto é enviado, mas como a API da OpenAI mostra essa descrição ao
  modelo não está no código aberto (não verificado), e o modelo não citou os marcadores. Fechar isso precisa de
  teste: capturar a requisição. A descrição das ferramentas passa sem corte. Resources: o modelo tem
  ferramentas para listar e ler, sem inclusão automática. Prompts: sem suporte no cliente MCP do Codex.
- **Copilot CLI:** a referência de comandos confirma o teste: por padrão só as instruções de servidores
  "allowlisted" entram no prompt de sistema; as dos outros são "recuperadas sob demanda". A opção
  `--allow-all-mcp-server-instructions` (desde a 1.0.66) põe as de todos os servidores. O efeito dessa opção
  precisa de teste. Que lista é essa, o limite de tamanho das descrições e o suporte a prompts e resources do MCP
  não estão nas fontes (não verificado).
- **Copilot no VS Code:** o código da extensão põe o `instructions` inteiro no prompt do modo agente, numa tag
  por servidor, se alguma ferramenta do servidor estiver ligada. Não achei corte de tamanho. A descrição das
  ferramentas também vai inteira (só o esquema de parâmetros é cortado em 1.024 caracteres nos modelos `gpt-4*`).
  Resources e prompts exigem ação do usuário (anexar o resource, digitar `/<servidor>.<prompt>`). O teste das
  portas não cobriu o VS Code: precisa de teste.
- **Em todos:** a definição das ferramentas é o único canal que a fonte mostra chegando ao modelo nos três (no
  Copilot CLI, a doc fala de "definições" e "esquemas" das ferramentas, sem citar a descrição). Com a busca de
  ferramentas ligada, essa definição pode ser adiada.

Este ticket não é uma decisão do mapa e não foi registrado em "Decisions so far".
