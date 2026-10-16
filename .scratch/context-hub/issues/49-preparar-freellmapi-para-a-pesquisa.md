# Preparar o FreeLLMAPI para a pesquisa da busca

Type: task
Status: resolved

## Question

Deixar o FreeLLMAPI em forma antes de a "Pesquisa ampla: lugares e mecanismos de busca" existir: é a etapa
de montagem (o "pátio") da proposta aprovada na rodada 6 de "Camada de busca"
([proposta](../prototipos/proposta-09-roteamento-da-pesquisa.md), seção 0;
[página](../prototipos/prototipo-09-roteamento-da-pesquisa.html)).

1. **Levantar** o que existe: `/v1/models` (catálogo e `execution_status`), `/api/free-tier` (pools,
   orçamento, `remaining`, `resetAt`), chaves por provedor, a fallback chain e os perfis atuais.
2. **Bancada:** um pedido-padrão curto, com esquema JSON, a cada modelo candidato; medir JSON válido,
   corte, latência, taxa de erro e se a ferramenta `google_search` funciona.
3. **Propor** estratégias melhores para a fallback chain atual: ordem, modelos que saem ou entram,
   diversidade de famílias, pools que se esgotam juntos, perfis por tipo de trabalho (gerar com busca na
   web, juntar, conferir) e o perfil `auto:pesquisa`.

HITL: o agente levanta, roda a bancada e propõe; o Gustavo decide o que vale para o dia a dia e aplica no
painel. Saída: ficha do provedor (`provedor.json`), relatório da bancada e proposta da chain, linkados aqui.
Só roda quando o Gustavo disser "pode iniciar". Fonte do FreeLLMAPI: clone local `C:\Projetos\freellmapi`
(README e `docs/en/api/01-rest-api.md`); nunca `model: auto` sem conferir a cadeia (memória do TTS).

## Answer

O FreeLLMAPI está pronto para a pesquisa ampla, que usa só a fallback chain do perfil `pesquisa`
(`auto:pesquisa`). A chain Default do dia a dia saiu do escopo deste ticket a pedido do Gustavo na rodada
6 ("É pra usar a fallback chain apenas"). As duas `gemini-2.5` que ele já desligou continuam desligadas.

- **Retrato do provedor:** [`provedor.json`](../freellmapi/provedor.json), sem segredos. 185 modelos
  prontos, 32 pools, perfis Default, gsd-fast, gsd-smart e `pesquisa`. Cotas e chain só são lidas com a
  sessão do painel (variável `FREELLM_DASHBOARD_TOKEN`).
- **Bancada:** [relatório](../freellmapi/relatorio-bancada.md), [`bancada.jsonl`](../freellmapi/bancada.jsonl),
  [`qualidade-urls.json`](../freellmapi/qualidade-urls.json) e [`toolcall.jsonl`](../freellmapi/toolcall.jsonl).
  49 de 185 modelos devolvem JSON válido. Sem busca, os modelos inventam URLs: só 65 de 169 existiam.
  10 de 11 geradores fora do Google chamam uma função `web_search` pelo gateway.
- **Regras do Gustavo para a pesquisa:**
  1. todo gerador tem ferramenta de busca;
  2. modelos com cota por token, não por quantidade diária;
  3. o Google entra, respeitando a cota: 20 pedidos por dia por modelo e por chave, 10 chaves, reset às
     04:00 BRT; o laço conta os pedidos e para em 90%.
- **Busca fora do Google:** o gateway não tem; o laço oferece e executa a função `web_search`. O serviço que
  ela chama é um ticket novo, "Serviço de busca da função web_search".
- **Perfil `pesquisa`**, criado pelo Gustavo e conferido no gateway, com 11 modelos de seis famílias, na
  ordem que ele escolheu: gemini-3.1-flash-lite (com orçamento), nemotron-3-super (Ollama),
  llama-3.3-70b-fp8-fast, llama-4-scout e gpt-oss-120b (Cloudflare), gpt-oss-120b (Ollama),
  nemotron-3-super-120b (NVIDIA), Llama 3.3 70B, Mistral Small 3.2 e Qwen3.5 397B (OVH) e
  nemotron-3.5-lightning (NVIDIA).
- **Cuidados para o laço:**
  - uma chamada fixada pode gastar até 4 tentativas de chave no mesmo provedor (o teto precisa contar o
    `X-Fallback-Attempts`);
  - a OVH aguenta uma conversa por minuto;
  - o modelo pode pedir várias buscas seguidas;
  - modelos que raciocinam precisam de `max_tokens` alto;
  - o `google_search` ainda não foi medido (cota).
- **Proposta completa da chain**, com as sugestões da Default que não foram adiante:
  [`proposta-chain.md`](../freellmapi/proposta-chain.md).

## Comments

- 2026-10-13: aberto a partir das rodadas 5 e 6 de "Camada de busca" (correção do Gustavo: a descoberta de
  modelos e a melhoria da chain vêm antes do laço, não dentro dele).
- 2026-10-13: reivindicado. Rodada 1 na nota "Rodada atual": `/api/free-tier` e `/api/fallback` pedem a
  sessão do painel (`requireAuth`; token em `localStorage` `freellmapi_dashboard_token`, 30 dias), não a
  chave unificada. Pergunta: "pode iniciar" e como o agente lê o painel (recomendação: token numa variável
  de usuário `FREELLM_DASHBOARD_TOKEN`, só GET). Bancada proposta: 3 pedidos por modelo `ready`, um pool
  por vez, mais 3 com `google_search` nos Google; nunca `model: auto`.
- 2026-10-13: rodada 1 respondida: **A**, pode iniciar; token do painel na variável de usuário
  `FREELLM_DASHBOARD_TOKEN` (só GET). Bancada como proposta (3 por modelo `ready`, um pool por vez).
- 2026-10-13: levantamento feito ([`provedor.json`](../freellmapi/provedor.json), sem segredos). Bancada,
  1ª passada: 603 chamadas, 49 de 185 modelos com JSON válido ao menos uma vez
  ([`bancada.jsonl`](../freellmapi/bancada.jsonl)). Das 158 URLs únicas citadas sem busca, 60 existem e 91
  dão 404. Repescagem (cota, JSON só no prompt, `max_tokens` 4000, `google_search`) parada pelo Claude Code
  por falta de memória na máquina, faltando 10 das 234 chamadas; não reiniciada. Google, lucidity, orcarouter
  e cohere ficaram em cota o dia todo; o `google_search` ainda não foi medido (cota do Google volta às 04:00 BRT).
- 2026-10-13: [relatório da bancada](../freellmapi/relatorio-bancada.md) e
  [`qualidade-urls.json`](../freellmapi/qualidade-urls.json). Rodada 2 na nota: terminar a bancada depois
  da virada da cota do Google (`google_search`, lucidity, orcarouter, cohere, as 10 que faltaram; ~150
  chamadas) antes de propor a chain (recomendação), ou propor já com o `google_search` "não medido".
- 2026-10-13: rodada 2 respondida (texto livre): (1) todo gerador da pesquisa precisa de ferramenta de
  busca habilitada, porque sem ela inventa da memória e a URL quebra; limitar tanto só atrapalha (muda o
  "geradores sem ferramenta, exceto `google_search`" da proposta); (2) a pesquisa segue hoje, sem os do
  Google, com os modelos de cota por token, não por pedidos por dia; (3) rodar o resto da bancada (as 10
  que faltaram) e ver como fica a chain sem o Google. O Gustavo apontou que a bancada gastou cota diária
  por pedido, coisa que o desenho dela não levou em conta.
- 2026-10-13: o registro do gateway (`GET /api/analytics/requests?platform=google&range=24h`) mostra que as
  únicas chamadas ao Google nas últimas 24 h foram as 80 da bancada (3 com sucesso), e o primeiro 429 veio às
  12:11Z, 6 min depois do início: a bancada gastou a cota diária do Google. As 10 chamadas que faltavam eram
  todas `google_search` no Google e não rodaram. [Proposta da chain sem o Google](../freellmapi/proposta-chain.md):
  perfil `auto:pesquisa` com 10 geradores de 7 famílias (com tools, sem limite de pedidos por dia, URLs
  reais); fora do Google o gateway não tem busca, então ela vira função que o laço executa. Rodada 3 na nota:
  testar tool calling pelo gateway nesses modelos (~24 chamadas, só pools sem limite diário).
- 2026-10-13: correção do Gustavo: ele não disse "cota por token ou por minuto"; a regra dele foi "cota por
  token, não por quantidade diária" (o "por minuto" foi acréscimo meu). Ele pôs mais 3 chaves do Google (10 no
  total) e pediu o Google no fallback, respeitando o limite de cota. A proposta da chain ganhou a faixa do
  Google com orçamento (20 por dia por modelo e chave; o laço para em 90%). Achado: `gemini-2.5-flash` e
  `gemini-2.5-flash-lite`, 1º e 4º da Default, dão 404 ("catalog entry looks stale"). Ressalva não verificada:
  a cota do Gemini é por projeto (memória da frente), e as 7 chaves antigas caíram juntas.
- 2026-10-13: rodada 3 respondida: **A**, testar o tool calling pelo gateway com orçamento fechado (12 modelos
  fora do Google, 2 conversas cada com `web_search` de mentira; no Google, no máximo 6 pedidos no dia). Sem
  objeção aos da NVIDIA e da OVH (limite por minuto), que ficam.
- 2026-10-13: teste de tool calling feito ([`toolcall.jsonl`](../freellmapi/toolcall.jsonl); seção no
  relatório). 10 de 11 modelos fora do Google chamam `web_search` com `query` válida; 7 usaram só as URLs do
  resultado em todas as conversas; saem laguna (502) e agnes (resposta final vazia). Os 2 `google_search`
  deram 429: o gateway tentou 3 chaves em espera em cada um, 8 tentativas no Google contra o teto de 6 que eu
  prometi (o teto era conferido por chamada, e uma chamada gasta até 4). A proposta foi atualizada.
- 2026-10-13: rodada 4 na nota: ordem do perfil `auto:pesquisa` (gemini-3.1-flash-lite com orçamento,
  nemotron-3-super Ollama, llama-3.3-70b-fp8-fast, llama-4-scout, gpt-oss-120b, nemotron-3-super-120b, os
  três da OVH, nemotron-3.5-lightning). Sugestão ao Gustavo: desligar as 7 chaves antigas do Google até 04:00.
- 2026-10-13: rodada 4 respondida: "ok e feito" (A). Conferido por `GET /api/profiles/6/models`: perfil
  `pesquisa` com as 11 linhas propostas ligadas, mas em outra ordem de prioridade (Cloudflare primeiro;
  gemini-3.1-flash-lite em 6º). Como o laço fixa os dois modelos de cada pedido, a ordem só pesa quando ele
  cai para `auto:pesquisa`.
- 2026-10-13: rodada 5 respondida: a ordem do perfil `pesquisa` foi de propósito. Na Default, o Gustavo
  desligou as duas linhas `google/gemini-2.5-flash` e `google/gemini-2.5-flash-lite` (conferido por
  `GET /api/profiles/1/models`) e não reordenou o topo, o que equivale à opção B. O topo agora é glm-4.5-flash
  (zhipu, sem chave) e depois codestral-latest.
- 2026-10-13: rodada 6 respondida: "É pra usar a fallback chain apenas". As sugestões da Default (família
  codestral, 16 plataformas sem chave) saem; ticket resolvido.
- 2026-10-13: revisto pela proposta refeita da pesquisa ampla: a pesquisa não usa o perfil `pesquisa` nem a
  função `web_search`. O laço fixa os modelos no catálogo inteiro, com orçamento por modelo. O levantamento e a
  bancada seguem valendo como base do despachante.
