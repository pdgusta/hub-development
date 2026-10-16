---
tipo: resposta
rodada: 2026-10-14-acesso-dos-agentes-decisao-r2
ticket: 14
enviada: 2026-10-14T23:36:30-03:00
envio: f67ac890-3cef-4f86-b4b6-f2a68d379c0d
estado: lida
substitui:
---

# Resposta: Acesso dos agentes: o teste em detalhe

## Os testes
em branco

## Quem roda e quanto custa
escolha: A, Um subagente Opus 5.5 médio roda agora os testes de linha de comando, em cerca de 1 hora, com 150 a 250 mil tokens; a lista dos seus testes chega junto com o relatório (a recomendada)

## De onde a checagem de início lê o estado do sync
escolha: A, No par, o hook de início lê o arquivo de estado que a vigia grava a cada 5 min (não depende do MCP estar de pé). No cliente, que não tem vigia, o hook pede o estado a uma ferramenta do MCP. Vale se o teste de início passar nos três; onde falhar, a checagem vira regra no contrato daquele harness (a recomendada)
comentário:
> quero que a ferramenta do mcp também sirva par como fallback

## O hook de fim da resposta
escolha: nenhuma das opções
outra:
> hook claude mod e o correlato de claude mod pros outros harness

## Algo mais?
em branco
