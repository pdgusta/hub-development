---
title: magpie × FreeLLMAPI. Substitui, complementa ou não serve?
data: 2026-10-02
origem: subagente de pesquisa (Claude Code), pergunta do Gustavo "O quanto esse magpie pode substituir o 'freellmapi' ou servir em outros casos?"
aviso: saída de modelo. As fontes primárias são o README e o código-fonte do magpie (commit `cac5023` de `yetone/magpie`, baixado como tarball e lido sem compilar), a API do GitHub para metadados e releases, a home de usemagpie.ai (HTML bruto), o README e a doc de API do clone local `C:\Projetos\freellmapi` (commit `ac6d29d`, 16/09/2026) e o `.claude/CLAUDE.md` do `freellmapi-mcp`. Nada foi instalado nem executado, e nenhuma combinação foi testada. O que não foi conferido está marcado como **não verificado**.
---

# magpie × FreeLLMAPI

## Resumo

**Conclusão: o magpie não substitui o FreeLLMAPI. Ele complementa, e só em casos específicos.** Os dois são gateways
locais que falam OpenAI e Anthropic, mas cada um resolve um problema diferente:

- O **FreeLLMAPI** **empilha tiers gratuitos**. Tem 34 provedores e um catálogo assinado de modelos gratuitos.
  Controla RPM, RPD, TPM e TPD por chave antes de enviar, oferece `auto:<perfil>` e `fusion`, e tem `/v1/embeddings`
  com failover que preserva a família do modelo.
- O **magpie** **escolhe o modelo de cada harness**. Edita a configuração de cerca de 30 agentes (Claude Code, Codex,
  Copilot CLI, OpenCode, Gemini CLI…) e reaproveita **assinaturas pagas** (Claude, ChatGPT/Codex, Copilot) como
  provedores. Faz failover reativo e tem grupos de roteamento. **Não tem endpoint de embeddings, não tem catálogo de
  modelos gratuitos e não tem painel multimodelo do tipo `fusion`.**

Para os usos atuais do Gustavo:

| Uso | O magpie atende? |
|---|---|
| Workers do `freellmapi-mcp` (`auto:gsd-fast`, `auto:gsd-smart`) | Só em parte. Falta o controle de cota dos tiers gratuitos e faltam as chains. |
| Checkpoint via `fusion` | Não. O magpie não tem síntese multimodelo. |
| Embeddings do context hub | Não. A rota não existe, e o catálogo descarta modelos de embedding. |
| Trocar o modelo de vários harnesses num lugar só | Sim, e é o forte dele. Esse papel não está coberto hoje. |

## 1. O que o magpie é

> "`magpie` is a single screen that lists each AI agent on your machine and the model it is set to. Click a value,
> pick a model. That is the whole app." ([README](https://github.com/yetone/magpie/blob/cac5023fb7fe47dcd770495e52108a6dad87edfe/README.md))

O magpie é um app de barra de menu, uma TUI (`magpie tui`) e uma CLI, num binário em Go:

> "Under 15 MB with the desktop app (it uses the system webview through Wails …), 7 MB for the terminal-only build.
> macOS, Linux and Windows." (README)

Ele inclui um gateway local:

> "magpie runs a local gateway that speaks OpenAI chat completions, OpenAI Responses and the Anthropic Messages API,
> and forwards to whichever vendor serves the model. Codex, Claude Code, OpenCode and the rest all point at
> `http://127.0.0.1:3425/v1`" (README)

Descrição do repositório: *"Every agent's model. One place. Codex on DeepSeek, Claude Code on Kimi, from the menu bar."*
([API do GitHub](https://api.github.com/repos/yetone/magpie))

O foco declarado é escolher o modelo de cada agente. Agregar cota gratuita não aparece como objetivo.

## 2. Provedores e tiers gratuitos

**Presets.** O README lista *"Anthropic, OpenAI, Gemini, DeepSeek, Kimi, GLM, MiniMax, StepFun, Qwen, Baidu Qianfan,
Tencent Cloud Token Plan, Huawei Cloud MaaS, Volcengine Ark, Mistral, Groq, xAI, OpenRouter, Together, Fireworks,
SiliconFlow, NVIDIA NIM, ModelScope, AiHubMix, PipeLLM, 302.AI, Ollama, LM Studio…"*. No código,
[`internal/provider/presets.go`](https://github.com/yetone/magpie/blob/cac5023fb7fe47dcd770495e52108a6dad87edfe/internal/provider/presets.go)
tem 72 entradas `{ID: …}`, contando subplanos e regiões. Além dessas, aparecem Amazon Bedrock, Ollama Cloud,
OpenCode Go/Zen, Kilo Gateway, ClinePass, Command Code, Vercel AI Gateway e "Jev · Cloudflare Workers AI".

A home de [usemagpie.ai](https://usemagpie.ai/#providers) diz *"Twenty presets — vendors, relays and local servers."*,
número que já não bate com o código.

**Sem preset no magpie, mas com tier gratuito no FreeLLMAPI:** Cerebras, Cohere, HuggingFace e o Cloudflare Workers AI
direto. Comparei com o README do FreeLLMAPI, seção "Supported providers". Esses provedores entrariam como provedor
custom: *"Custom vendors need a name and a base URL."* (README do magpie).

**Tiers gratuitos.** O magpie **não agrega tiers gratuitos como objetivo**. Ele aceita a chave que você colar, seja de
tier gratuito ou pago, e não traz catálogo de cotas gratuitas. O tratamento específico de "free" no código se limita
a três casos:

- **OpenRouter `:free`**: o limite do tier gratuito vale por modelo, não pela conta inteira.
  > "A rate limit on that model is its free-tier limit, while an account-level rest stays on restKey."
  > ([`internal/gateway/fallback.go`](https://github.com/yetone/magpie/blob/cac5023fb7fe47dcd770495e52108a6dad87edfe/internal/gateway/fallback.go))
- **OpenCode Zen free**: o magpie se passa pelo OpenCode para usar esse tier.
  > "OpenCode Zen's free models (-free) are served to OpenCode alone … The user allowed magpie to ask them as OpenCode does"
  > ([`internal/gateway/zenfree.go`](https://github.com/yetone/magpie/blob/cac5023fb7fe47dcd770495e52108a6dad87edfe/internal/gateway/zenfree.go))
- **Kilo Gateway e ClinePass**: modelos gratuitos sem chave (`presets.go`: *"free models with no key"*).

**Assinaturas.** O que o magpie oferece no lugar de cota gratuita é o reaproveitamento de **assinaturas**:

> "Sign in to Claude Code, Codex (ChatGPT) or Copilot and that login shows up as a provider: every other agent can use
> its models through the gateway" (README)

No caso da assinatura Claude, o README admite que contorna o classificador da Anthropic:

> "Anthropic classifies another agent's system prompt as third-party traffic … magpie therefore drives the genuine
> local `claude` binary for every Claude subscription generation." (README, "Signed-in agents as providers")

Sobre a Antigravity: *"Google may suspend an Antigravity account it sees used outside Antigravity"* (idem).

> **Risco:** usar assinaturas por terceiros esbarra nos termos dos provedores. Não conferi os termos da Anthropic nem
> os do Google (**não verificado**).

## 3. API exposta

As rotas registradas estão em
[`internal/gateway/gateway.go` L398-L433](https://github.com/yetone/magpie/blob/cac5023fb7fe47dcd770495e52108a6dad87edfe/internal/gateway/gateway.go#L398-L433):

- `/v1/chat/completions`
- `/v1/responses`
- `/v1/messages`
- `/v1/messages/count_tokens`
- `/v1/images/generations`
- `/v1/images/edits`
- `/v1/videos`
- `/v1beta/models/{call...}` (Gemini)
- `/v1/models`
- `/v1/magpie/quotas`, `/v1/magpie/route` e `/v1/magpie/concurrency`
- `/v1/systemone`

O handler de fallback responde:

> "magpie serves /v1/chat/completions, /v1/responses, /v1/messages, /v1/systemone, /v1/images/generations,
> /v1/images/edits, /v1/videos and /v1beta/models/*"

Portanto, ele é compatível com **OpenAI** (Chat Completions e Responses), com **Anthropic** (Messages e count_tokens)
e com **Gemini**. A tradução entre APIs inclui streaming e tool calls:

> "Requests pass straight through when the vendor speaks the agent's API and are translated otherwise, streaming, tool
> calls and reasoning included." (README)

**Embeddings: não existem.** Não há rota `/v1/embeddings`. O catálogo descarta modelos de embedding de propósito:

> "a model that draws is kept, marked, for Settings → Images; any other that isn't for text (embeddings, speech) is left out"
> ([`internal/catalog/live.go` L282-L283](https://github.com/yetone/magpie/blob/cac5023fb7fe47dcd770495e52108a6dad87edfe/internal/catalog/live.go#L282-L283))

**Autenticação.** No loopback, qualquer chave serve: *"The key is `magpie` (any value works; the gateway only listens
on loopback)"*. Com compartilhamento em LAN, o gateway passa a exigir *gateway keys* nomeadas (README, "Connecting
anything else").

## 4. Roteamento e failover

**Grupos de roteamento.** O agente escolhe `group/<id>`, e o gateway distribui o pedido pelas chaves e contas de
todos os membros.

> "`routing=` is `smart` (the default: of the subscriptions with quota to spare, the one whose allowance renews soonest
> first), `order` …, `rotate` …, `usage` (least used first) or `pace` …" (README, "Routing groups")

Os grupos também aceitam regras **determinísticas** por tamanho, imagem, esforço, agente e horário, e um classificador
opcional de intenção ([`internal/provider/grouprule.go`](https://github.com/yetone/magpie/blob/cac5023fb7fe47dcd770495e52108a6dad87edfe/internal/provider/grouprule.go)).

**Failover reativo.** O magpie muda de candidato quando o provedor falha e deixa quem falhou de castigo por um minuto:

> "The request goes to the next one only while none of the reply has been sent … A provider that just failed that way
> waits at the back of the line for a minute" (`fallback.go`, `fallbackCooldown = time.Minute`)

O 429 é classificado em `failRate` ou `failQuota` pelo corpo da resposta
([`internal/gateway/routing.go`](https://github.com/yetone/magpie/blob/cac5023fb7fe47dcd770495e52108a6dad87edfe/internal/gateway/routing.go)).
Para assinaturas, `/v1/magpie/quotas` informa o saldo restante.

**O que falta, em comparação com o FreeLLMAPI:**

- **Controle proativo de RPM, RPD, TPM e TPD por chave.** Uma busca no código por `RPM`, `RPD` e
  `x-ratelimit-remaining` não achou nada no gateway, só na integração com o GitHub. O FreeLLMAPI tem esse controle:
  *"RPM/RPD/TPM/TPD counters per `(platform, model, key)` that learn providers' reported ceilings"* (README do
  FreeLLMAPI).
- **Síntese multimodelo.** As ocorrências de "judge" no magpie servem para classificar a dificuldade do turno
  (`decide.go`: *"judge the work the message asks for"*). Não existe painel com juiz equivalente ao `fusion`.

## 5. Harnesses que apontam para ele

O README traz uma tabela com cerca de 30 agentes e os arquivos que o magpie edita: Claude Code (`~/.claude/settings.json`),
Claude Desktop, Codex, Gemini CLI, OpenCode, Copilot CLI (`~/.copilot/settings.json`, só o campo `model`), Cursor CLI,
Goose, Crush, Cline CLI, DeepSeek Harness, Hermes Agent e outros. Qualquer cliente com campo de base URL também serve:

| O cliente fala | Base URL | Variáveis |
|---|---|---|
| OpenAI | `http://127.0.0.1:3425/v1` | `OPENAI_BASE_URL`, `OPENAI_API_KEY=magpie` |
| Anthropic | `http://127.0.0.1:3425` | `ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY=magpie` |
| Gemini | `http://127.0.0.1:3425` | `GOOGLE_GEMINI_BASE_URL`, `GEMINI_API_KEY=magpie` |

No Claude Code, o magpie mexe no `settings.json` global:

> "**Claude Code** gets `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN` and the model variables in the `env` block of
> `settings.json`; picking a native model (`opus`, `sonnet`…) removes them and restores whatever was there." (README)

> **Atenção para o `freellmapi-mcp`:** essa edição vale para **todas** as sessões do Claude Code da máquina. A regra R1
> do projeto exige que a sessão principal continue nos modelos Anthropic nativos (`.claude/CLAUDE.md`, "Decisões
> travadas"). Hoje, `tools/fl/` passa a chave **ao processo filho** (`.claude/CLAUDE.md`, "Ambiente"). Usar o magpie
> pela via de configuração global quebraria esse isolamento. A via por variável de ambiente no processo do worker
> continua possível.

O Copilot CLI aparece só com o campo `model`. **Não verificado:** se o Copilot CLI consegue usar modelos que passam
pelo gateway do magpie.

## 6. Licença e maturidade

| | magpie | FreeLLMAPI |
|---|---|---|
| Licença | MIT ([LICENSE](https://github.com/yetone/magpie/blob/cac5023fb7fe47dcd770495e52108a6dad87edfe/LICENSE): "MIT License · Copyright (c) 2026 yetone") | MIT (README: "The router itself stays MIT-licensed and fully free, forever."); o feed de catálogo ao vivo é pago ($19/ano) |
| Criado | 2026-09-23 (primeiro commit em 2026-09-22: "dial: one dial for every coding agent's model") | 2026-04-21 |
| Versão | v0.1.662 (2026-10-02), com **662 releases em ~10 dias** e vários por dia ([magpie-releases](https://github.com/yetone/magpie-releases/releases)) | v0.13.3 (2026-09-30); o clone local está no commit `ac6d29d`, de 16/09 |
| Atividade | 1.243 commits, ~56 contribuidores (contando anônimos), 4.210 stars, 280 forks, 57 issues abertas | 30.096 stars, 4.214 forks, 34 issues abertas |
| Linguagem e runtime | Go, binário único (Wails); imagem Docker distroless | Node 20+, SQLite; Docker, desktop e PM2 |
| Builds | "Mac releases are signed and notarised; the Windows and Linux builds are not signed yet" | `.exe` e `.dmg` nos releases |
| Telemetria | PostHog, um evento por dia, desligável com `DO_NOT_TRACK=1` ou `MAGPIE_NO_STATS=1` (README, "Counting users") | **não verificado** |

Fonte dos números: API do GitHub consultada em 2026-10-02.

O magpie tem **10 dias de vida** e muda muito rápido, com releases de hora em hora e um README extenso já defasado em
relação à home. Isso não é sinal de baixa qualidade, mas indica uma superfície instável para fixar num contrato de
roteamento.

## 7. Tabela magpie × FreeLLMAPI

| Critério | magpie | FreeLLMAPI |
|---|---|---|
| Problema central | Escolher o modelo de cada agente e compartilhar assinaturas | Empilhar tiers gratuitos atrás de um `/v1` |
| Fonte dos modelos | Chaves que o usuário cola, assinaturas logadas, plugins OpenCode, models.dev | Catálogo assinado de 34 provedores, 635 endpoints gratuitos e ~7,4 bi tokens/mês (README do FreeLLMAPI) |
| OpenAI Chat / Responses | Sim / sim | Sim / sim |
| Anthropic Messages | Sim, com `count_tokens` | Sim (`/v1/messages`) |
| Gemini nativo | Sim (`/v1beta`) | Sim (`/v1beta`) |
| **Embeddings** | **Não** (`gateway.go` não tem a rota; `live.go` descarta os modelos) | **Sim**: *"failover never crosses models … embeddings route by **family**"* (`docs/en/api/01-rest-api.md`, seção Embeddings) |
| Imagem e vídeo | Sim | Sim, além de áudio TTS e STT |
| Roteamento | Grupos (`smart`, `order`, `rotate`, `usage`, `pace`), regras determinísticas, classificador de intenção | Seis estratégias, perfis `auto:<nome>` com chains, sticky session de 30 min |
| Failover | Reativo: troca antes do primeiro byte e põe o provedor em cooldown de 1 min; também entre chaves e contas | Reativo em 429/5xx com cooldown e rotação de chave, **mais** controle de cota proativo por chave |
| Painel multimodelo | Não | `fusion` (painel e juiz) |
| Assinaturas pagas como provedor | Sim (Claude, ChatGPT/Codex, Copilot, Devin, Qoder, Grok, Cursor, Gemini Code Assist) | Não (**não verificado**; o README não menciona) |
| Configura os harnesses | Edita a configuração de ~30 agentes, perfis e TUI | Geradores `npx freellmapi setup-*` e launchers `freellmapi launch` |
| MCP | Usa MCP internamente para a ponte com o `claude` | `/mcp` para introspecção de modelos e saúde |
| Observabilidade | Ledger de uso e custo por agente, chave e conta; exportação OTLP e Langfuse | Analytics no dashboard (p50, p95, TTFT) |
| Multimáquina | "Remote magpie" e sync por WebDAV ou S3, cifrado | Acesso pela LAN (**não verificado** em detalhe) |
| Maturidade | 10 dias, v0.1.x | ~5,5 meses, v0.13.x |

## 8. Conclusão por caso de uso

1. **Workers do `freellmapi-mcp` (`auto:gsd-fast`, `auto:gsd-smart`): não substitui.**
   - O contrato depende das chains do FreeLLMAPI e da estratégia `smartest`, e o magpie não tem nenhum dos dois
     (`.claude/CLAUDE.md`, "Chains no FreeLLMAPI").
   - O valor do FreeLLMAPI ali é a cota gratuita somada com controle proativo de limites. O magpie só reage a 429.
   - Um grupo do magpie (`group/…`) com chaves gratuitas de Groq, Mistral, NVIDIA e OpenRouter imitaria uma chain,
     mas sem catálogo de cotas e sem contadores de RPM e RPD. Isso é inferência a partir do código, **não testado**.
2. **Checkpoint com `fusion`: não serve.** O magpie não tem painel com juiz. Um checkpoint de modelo único por um grupo
   funcionaria, mas perderia o painel de 3 ou 4 modelos que o `fl-fusion` exige.
3. **Embeddings do context hub: não serve.** A rota não existe e o catálogo descarta modelos de embedding. O FreeLLMAPI
   continua sendo a opção, ou um provedor de embeddings direto.
4. **Outros casos em que o magpie complementa:**
   - **Painel único de modelo por harness.** Hoje o Gustavo usa Claude Code, Copilot e, antes, OpenCode
     (ticket 04, `.scratch/context-hub/issues/04-windows-ou-wsl.md`). O magpie troca o modelo de todos eles a partir
     de um lugar só e salva perfis (`magpie save` / `magpie use`).
   - **FreeLLMAPI como provedor custom dentro do magpie.** O magpie aceita `url=` (OpenAI) e `anthropic=` (Anthropic)
     num provedor custom, então poderia apontar para `http://localhost:3001/v1` e expor `auto:gsd-fast` nos pickers de
     todos os harnesses. **Não verificado:** se ids com `:`, como `auto:gsd-fast`, passam intactos pelo catálogo do
     magpie. O código corta em `:` só para exibir o nome (`catalog.go` L511: `// ":free", ":batch"`).
   - **Reaproveitar a assinatura Copilot ou ChatGPT em outros agentes.** Existe, mas tem risco de termos de uso.
     **Não avaliado**, e fora do escopo do hub.
   - **Observabilidade.** O ledger por agente e o OTLP para Langfuse poderiam medir o uso de modelos no hub. É
     opcional e não está pedido em nenhum ticket.
5. **Recomendação:** **manter o FreeLLMAPI** como gateway dos workers, do checkpoint e dos embeddings. Tratar o magpie,
   se for o caso, como **ferramenta de conveniência do lado do usuário**, para trocar o modelo dos harnesses. Ele não
   deve entrar no contrato de roteamento nem no desenho do hub enquanto estiver na v0.1.x. Se for testado, usar a via
   por base URL ou provedor custom, nunca a edição global do `~/.claude/settings.json`, que conflita com a R1 do
   `freellmapi-mcp`.

## Fontes

- README do magpie no commit `cac5023`:
  https://github.com/yetone/magpie/blob/cac5023fb7fe47dcd770495e52108a6dad87edfe/README.md
- Código do magpie no mesmo commit:
  - `internal/gateway/gateway.go`
  - `internal/gateway/fallback.go`
  - `internal/gateway/routing.go`
  - `internal/gateway/zenfree.go`
  - `internal/gateway/decide.go`
  - `internal/catalog/live.go`
  - `internal/provider/presets.go`
  - `internal/provider/grouprule.go`
  - `LICENSE`
- Metadados e releases:
  - https://api.github.com/repos/yetone/magpie
  - https://api.github.com/repos/yetone/magpie-releases/releases
  - https://api.github.com/repos/tashfeenahmed/freellmapi (consultas de 2026-10-02)
- Home do magpie: https://usemagpie.ai/#providers (HTML bruto, seção `id="providers"`)
- FreeLLMAPI, no clone local:
  - `C:\Projetos\freellmapi\README.md`
  - `C:\Projetos\freellmapi\docs\en\api\01-rest-api.md` (seção Embeddings)
- `C:\Projetos\freellmapi-mcp\.claude\CLAUDE.md`, seções "Decisões travadas", "Routing de modelos" e "Ambiente"
