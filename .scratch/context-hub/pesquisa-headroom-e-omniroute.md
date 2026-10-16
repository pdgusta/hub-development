# Headroom e OmniRoute: o que são e se servem à construção (2026-10-16)

Pedido do Gustavo: "e o headroom e o omniroute?" (mesma pergunta do Cartographer e do claude-mem). Fontes primárias:
README dos repositórios no GitHub (raw, ramo `main`) e a API do GitHub.

## Headroom (`headroomlabs-ai/headroom`)

Cerca de 75 mil estrelas, push em 2026-10-16, Apache-2.0.

**Nas palavras do autor:** "Headroom compresses everything your AI agent reads — tool outputs, logs, RAG chunks, files,
and conversation history — before it reaches the LLM. Same answers, fraction of the tokens. Compression runs on your
machine; no prompt or file content is sent anywhere to be compressed."

- **Formas de uso:** biblioteca, proxy local (`headroom proxy --port 8787`), `headroom wrap claude|codex|copilot|...`
  (desfaz com `headroom unwrap`), servidor MCP, "cross-agent memory" e `headroom learn`, que "mines failed sessions
  and writes corrections to `CLAUDE.local.md` (default, gitignored), `CLAUDE.md`, `AGENTS.md`...".
- **Números do autor** (benchmarks dele, não medidos aqui): 21% a 57% a menos de tokens em quatro cenários; "prose and
  already-dense output compress very little".
- **O `wrap`** sobe o proxy local, "installs Serena for semantic code navigation" e registra o Serena no
  `~/.claude.json` (escopo do projeto por padrão; `--code-memory none` pula).
- **Telemetria:** "An anonymous beacon is on by default" (taxas, contadores, ids de modelo, sistema); "never sends
  prompts, completions, code or file paths"; desliga com `HEADROOM_BEACON=off`.
- **Windows:** pacotes publicados para `win_amd64`; o `wrap` do Copilot tem nota própria para login no Windows.

**Relação com a construção:** é o que mais pode ajudar, porque ontem uma faixa parou por limite de uso do Claude, e
compactar saídas de teste e logs dos agentes poupa cota. Cuidados: (1) ele fica no meio de todo o tráfego do agente,
uma variável a mais justamente quando a construção testa hooks e MCP do hub; (2) o `learn` grava em `CLAUDE.md` e
`AGENTS.md`, e o hub decidiu que não tem `CLAUDE.md` e que mudar o contrato pede aval; (3) a memória entre agentes
duplica o papel do hub, como o claude-mem; (4) não verificado: se funciona com a assinatura do Claude (login) no
Claude Code e o ganho real no tráfego dos nossos agentes.

## OmniRoute (`diegosouzapw/OmniRoute`)

Cerca de 77 mil estrelas, push em 2026-10-16, MIT.

**Nas palavras do autor:** "Free MIT AI gateway: one endpoint, 359 providers (150+ free), 1200+ models ... Works with
Claude Code, Codex, Cursor, OpenCode, Cline & Copilot. Quota-aware auto-fallback, RTK+Caveman compression saves 15-95%
tokens, MCP/A2A, Desktop/PWA." Um endereço local (`http://localhost:20128/v1`) serve todos os clientes; o modelo `auto`
"builds a virtual combo from your connected providers"; "combos" passam ao próximo modelo quando a cota acaba ou o
provedor falha; tem uma pilha de 12 compressores.

**Relação com a construção:** faz o mesmo papel do FreeLLMAPI, que o Gustavo já usa para pesquisa (gateway com cotas
grátis, API da Anthropic e do Codex). Trocar ou somar um gateway agora não ajuda a construção e mexe no caminho dos
modelos durante os testes. O `auto` dele tem o mesmo risco que já levou à regra "nunca `model: auto`" no FreeLLMAPI.
Cabe na oportunidade "o hub como gateway de modelos" do segundo mapa, comparado ao FreeLLMAPI.

## Conclusão do maestro

- **Headroom:** não instalar antes da construção. Se a cota do Claude voltar a travar, vale um teste curto e isolado
  (um recruta só, `HEADROOM_BEACON=off`, `--code-memory none`, nunca `headroom learn`), medindo o ganho real.
- **OmniRoute:** não instalar. Fica para o segundo mapa, comparado ao FreeLLMAPI.
