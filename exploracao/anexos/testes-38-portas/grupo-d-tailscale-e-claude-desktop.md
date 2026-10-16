# Testes 38, grupo D: Tailscale e Claude Desktop (2026-10-10 e 11)

Ticket: "Testes das portas de entrada". O Gustavo instalou o Tailscale 1.104.1 no notebook (nó
`armis00323`, tailnet `tail82b4aa.ts.net`, plano Free), trocou a política pela de teste e gerou uma
chave efêmera, não reutilizável, com `tag:cliente`. Claude subiu duas instâncias só de leitura do
es617 na IP da tailnet do notebook: a 8788 é a porta liberada pelo grant e a 8789 é o controle, com o
mesmo serviço.

Política de teste: membros com acesso total; `tag:cliente` só para `tcp:8788` do notebook (alias
`par-notebook`).

## Resultados

| Teste | Resultado |
|---|---|
| Cliente efêmero (contêiner `tailscale/tailscale`, `tag:cliente`) entra na tailnet | entrou como `cliente-teste`, listado como "tagged-devices" |
| Cliente → notebook:8788 | aberta; o MCP responde 401 sem token |
| Cliente → notebook:8789 (mesmo serviço, porta fora do grant) | fechada |
| Cliente → notebook:445 | fechada |
| Notebook (membro) → 8788 e 8789 | as duas abertas |
| Claude Desktop, MCP local por URL (`"type": "http"` no `claude_desktop_config.json`) | ignorado: o app leu o arquivo, mas registrou "no stdio servers connected"; não aparece |
| Claude Desktop, MCP local por ponte stdio (`npx mcp-remote <url> --allow-http --header ...`) | aparece como "Dev local" e as ferramentas funcionam pela tailnet (listou as pastas do cofre). No primeiro início deu "Couldn't start for Cowork and Code sessions. Error: Request timed out"; depois apareceu |
| O `instructions` do MCP chega ao Claude Desktop pela ponte | **não**: o modelo não viu nenhum marcador do `AGENTS.md` de teste |
| Conector remoto com URL `http://...ts.net:8788/mcp` | recusado pelo formulário: "A URL deve começar com https://". O teste com HTTPS (Tailscale Serve) foi pulado a pedido do Gustavo |
| Chat e work no Claude Desktop | são o mesmo modo, não há mais como escolher |
| Tempo até o nó efêmero sumir depois de apagar o contêiner (sem `tailscale logout`) | contêiner apagado às 2026-10-11T03:08:52Z; ainda listado às 03:43:35Z (35 min); fora do `tailscale status` às 2026-10-12T16:57:02Z. O momento exato não foi medido: some entre 35 min e cerca de 38 h |

## O que isso decide

- **O grant por tag e porta funciona:** um cliente efêmero com tag só alcança a porta do MCP.
- **O Claude Desktop (chat/work) só chega ao hub por um MCP local stdio**, que pode ser uma ponte para
  a URL da tailnet. Conector remoto por http é barrado; por https, a doc diz que parte da Anthropic.
- **O contrato do hub não chega ao Claude Desktop pelo MCP**; a porta 6 precisa de outro canal (a
  pesquisa da porta 6 cita as "Folder instructions" do Cowork, não testadas).
- **Um cliente efêmero apagado sem `tailscale logout` some sozinho da tailnet**, mas não na hora:
  ficou pelo menos 35 minutos listado. Quem desliga um cliente de propósito deve dar `logout`.

## Limpeza feita

Configuração do Claude Desktop restaurada do backup (sem servidores MCP). Instâncias e volumes de
teste do es617 removidos; spike parado; notas de teste apagadas do CouchDB; pastas com ponto de
teste apagadas do `cofre-a`; arquivo da chave e cópia da política apagados. **Ficam:** o Tailscale
instalado e logado no notebook, e a política de teste na tailnet (membros com acesso total, então nada
muda para os aparelhos do Gustavo).
