# Serviço de busca da função web_search

Type: research
Status: wontfix

## Question

Que serviço de busca na web a função `web_search` do laço da "Pesquisa ampla: lugares e mecanismos de
busca" chama? Fora do Google, o FreeLLMAPI não tem busca ("Preparar o FreeLLMAPI para a pesquisa da busca"),
e o Gustavo quer todos os geradores com busca, porque sem ela inventam URL. Catálogo de opções com fonte
primária: serviço, cota gratuita e como ela conta (por pedido, por dia, por mês), chave, o que devolve
(título, URL, trecho, página inteira), línguas (pt, en, es, zh, ja, de, ru), se roda local (por exemplo,
um metabuscador próprio) e o limite de uso nos termos. A escolha é do Gustavo.

Só roda quando o Gustavo pedir. Protocolo da §10.4 da exploração.

## Comments

- 2026-10-13: aberto na resolução de "Preparar o FreeLLMAPI para a pesquisa da busca" (regra do Gustavo na
  rodada 2: todo gerador com ferramenta de busca).
- 2026-10-13: o Gustavo pediu para iniciar nesta sessão. Reivindicado; pesquisa entregue a um subagente
  (skill "research", protocolo da §10.4, consulta cega: o brief não cita candidatos). Relatório esperado em
  `exploracao/anexos/pesquisa-51-servico-de-busca-web-search.md`.
- 2026-10-13: o Gustavo reclamou que a pesquisa gastava tokens do Claude ("Eu estou usando ele [o FreeLLMAPI]
  justamente pra não gastar tokens do claude e você dispara isso tudo num agente"). Parei o subagente depois
  da descoberta (19 consultas), antes da verificação nas fontes primárias; nenhum relatório foi gravado. O
  subagente pode ser retomado com o contexto que já tem. Rodada 1 na nota: como refazer pelo FreeLLMAPI.
- 2026-10-13: posto em dúvida pelo Gustavo (a busca sem tool calling forçada; ver o comentário do mesmo dia em
  "Pesquisa ampla: lugares e mecanismos de busca"). Fica parado até a proposta refeita dizer se ele ainda serve.
- 2026-10-13: fora do escopo. Na proposta refeita da pesquisa ampla (aprovada na rodada 3), o laço não força
  tool calling, então a função `web_search` não existe e não há serviço a escolher.
