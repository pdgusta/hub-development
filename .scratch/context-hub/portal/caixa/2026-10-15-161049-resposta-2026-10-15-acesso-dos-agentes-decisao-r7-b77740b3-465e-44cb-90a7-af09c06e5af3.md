---
tipo: resposta
rodada: 2026-10-15-acesso-dos-agentes-decisao-r7
ticket: 14
enviada: 2026-10-15T16:10:49-03:00
envio: b77740b3-465e-44cb-90a7-af09c06e5af3
estado: lida
substitui:
---

# Resposta: Acesso dos agentes: o Codex no hub e o endereço dos clientes

## Como o Codex roda no hub
escolha: A, Com acesso total (`danger-full-access`) em todo Codex do hub, nas duas máquinas: shell e `apply_patch` gravam (testado), sem isolamento do sistema. A proteção do hub fica nos hooks (início, fim e a recusa antes da ferramenta) e no contrato. O kit roda o teste mínimo do sandbox elevado a cada atualização do Codex e avisa quando ele passar; voltar ao sandbox fica para você decidir nessa hora (a recomendada)

## O fim da resposta e a vigia no Codex
escolha: C, Igual à A, e mais um teste do caminho pelo nome da conversa: um programa ao lado do Codex renomeia a conversa com o estado da vigia, e a barra de estado e o título do terminal mostram o nome. Custo estimado: cerca de 1 hora do recruta Codex; ninguém sabe se um programa separado alcança o Codex já aberto, e a conversa passa a ter o estado da vigia como nome (a recomendada era A)

## O endereço dos clientes para a busca e o banco
escolha: A, O TBXark/mcp-proxy em cada par, preso ao endereço da tailnet, numa porta só, com uma rota e um token por servidor: `/busca/mcp` (o obsidian-hybrid-search, que passa a escutar só em 127.0.0.1) e `/banco/mcp` (a instância só de leitura). Se "Como os agentes gravam no hub" ligar a gravação do cliente, ela vira uma terceira rota, `/banco-escrita/mcp`, com outro token. O cliente leva duas entradas de MCP no mesmo endereço, com o token de uma variável de ambiente. Os agentes do próprio par seguem direto nos MCP locais, em 127.0.0.1 (a recomendada)

## Algo mais?
em branco
