# Proposta refeita: o laço da pesquisa ampla (2026-10-13)

Ticket "Pesquisa ampla: lugares e mecanismos de busca", rodadas 1 e 2 da proposta refeita. Substitui as etapas
0 e 2 e a divisão de papéis da [proposta da rodada 6 de "Camada de busca"](proposta-09-roteamento-da-pesquisa.md).
Matriz de células, sementes ocultas, estados do pedido, validação, bola de neve, gate dos 5%, calibração,
conferência, auditoria e colunas do catálogo ficam como lá. Proposta, não decisão: nada roda antes do
"pode iniciar".

## O que mudou (palavras do Gustavo)

- **O roteamento é do laço, não do gateway:** "o routing strategy do freellmapi é bem limitado e vai ficar
  chamando sempre o mesmo modelo até acabar a cota". O laço fixa cada modelo e espalha os pedidos pelo
  catálogo inteiro; o `auto` e as fallback chains saem.
- **Sem tool calling forçado.** O modelo responde do jeito que o provedor serve; quem separa o real do
  inventado é a conferência em fonte primária.
- **O FreeLLMAPI faz o grosso;** o Claude não gera.
- **O controle é dividido:** scripts em paralelo, cada um com o seu livro-razão, tocados por agentes no
  Maestri.

## Papéis

| Papel | Quem | O que toca | O que não faz |
|---|---|---|---|
| Despachante | Claude Opus 5.5, recruta no Maestri | O script do roteamento: relê cotas e status, mantém o orçamento de cada modelo, distribui os pedidos, corta quem caiu | Não lê as respostas dos modelos |
| Geradores (3) | Claude Haiku 5.5, recrutas | Cada um toca o script das suas células: pt/es; en/de/ru; zh/ja | Não escolhe modelo: pede ao despachante |
| Juntador | Claude Sonnet 5.5, recruta | Junta cada onda (chave canônica mais casos ambíguos), cria as células novas da bola de neve e mede o gate dos 5% | Não confere fonte |
| Conferidor | Claude Sonnet 5.5, subagente do maestro | Conferência em fonte primária (etapa 4 da proposta anterior) | Não gera |
| Maestro | Claude Opus 5.5 (esta sessão) | Plano de cobertura, auditoria por amostra (~10%), síntese | Não toca o laço |

Os agentes conversam por arquivos: o livro-razão de cada gerador (JSONL só de acréscimo), a fila do
despachante e o relatório de cada onda. Ninguém precisa ler o livro-razão inteiro.

## O roteamento (o despachante)

Base: [`provedor.json`](../freellmapi/provedor.json) e o
[relatório da bancada](../freellmapi/relatorio-bancada.md).

1. **Universo:** os modelos `ready` de `GET /v1/models` no começo de cada ciclo (185 hoje). Saem os que
   a bancada provou que não servem para isso: os que não são de chat (áudio, TTS, live) e os que deram 404 no
   provedor. O resto entra, inclusive quem só bateu cota hoje.
2. **Orçamento por modelo** (limite × número de chaves), lido de cada linha de `GET /api/fallback`: `rpmLimit`, `rpdLimit`,
   `tpmLimit`, `tpdLimit` e `keyCount`. O despachante usa até 90% do limite diário e conta **cada tentativa
   de chave** (`1 + X-Fallback-Attempts`), porque uma chamada fixada pode gastar até 4 tentativas. Os limites
   por dia valem por janela de cada pool: Google vira às 04:00 BRT, Cloudflare às 21:00 BRT (00:00 UTC), e os
   outros pelo `resetAt` de `/api/free-tier`.
3. **Escolha do par:** cada pedido vai a dois modelos de famílias diferentes e de pools diferentes. Entre os
   que têm orçamento, o despachante sorteia com peso: orçamento restante × taxa de acerto no livro-razão.
   Assim a carga se espalha e nenhum modelo é chamado até secar. Um modelo novo começa com peso médio.
4. **Ritmo por pool:** o paralelismo segue o `rpmLimit` de cada pool. Na bancada: NVIDIA 40/min por chave
   (2 chaves); Groq 30/min; OpenRouter 20/min e 50/dia na conta toda; Mistral 2/min; OVH 2/min por IP;
   Google 15/min e 20/dia por modelo e chave (10 chaves). Cloudflare e Ollama não publicam limite por minuto e
   começam com 2 em voo.
5. **Formato do pedido:** JSON pedido no texto, sem `response_format`, porque o gateway recusa
   `response_format` em parte dos provedores (61 recusas na bancada). Nos modelos que aceitam, o esquema vai
   junto. `max_tokens` 700 nos modelos comuns e 4000 nos que raciocinam: dos 30 cortes, 14 voltaram válidos
   com 4000.
6. **Saúde:** depois de 3 falhas seguidas, o modelo sai até o próximo `resetAt` ou por 15 min. Um 429 tira só
   aquele modelo, não o pool inteiro. A troca de chave fica com o gateway, que roda as chaves de cada modelo;
   o despachante não escolhe chave. A cada ciclo, ele relê `execution_status` e `/api/free-tier`.
7. **Teto de segurança:** o Gustavo escolhe, ao iniciar, um teto em horas ou em pedidos; o despachante para
   ao chegar nele, mesmo sem saturação.

## O que fica igual

Etapas 1 (plano de cobertura), 2 (laço de geração: estados, validação, bola de neve, gate dos 5%,
calibração), 3 (juntar), 4 (conferir), 5 (auditoria por amostra) e 6 (síntese), o painel por onda e as
colunas do catálogo: [proposta anterior](proposta-09-roteamento-da-pesquisa.md).

## O que sai

- O perfil `pesquisa` (11 modelos) como caminho da pesquisa; ele continua no gateway para quem quiser.
- O ticket "Serviço de busca da função web_search": sem tool calling forçado, a função `web_search` do laço
  deixa de existir.
- A etapa 0 dentro desta pesquisa: o levantamento já foi feito ("Preparar o FreeLLMAPI para a pesquisa da
  busca"); o despachante só relê o estado a cada ciclo.
