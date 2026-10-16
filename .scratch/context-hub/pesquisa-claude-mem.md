# claude-mem: o que é e se serve à construção (2026-10-16)

Pedido do Gustavo: "e o claude mem?" (mesma pergunta do Cartographer: como ajuda na execução e se dá para instalar
agora). Fonte primária: README do repositório `thedotmack/claude-mem` (raw do GitHub, ramo `main`) e a API do GitHub
(cerca de 101 mil estrelas, push em 2026-10-16, licença Apache-2.0, não arquivado).

## O que é, nas palavras do autor

"Persistent memory compression system built for Claude Code." "Claude-Mem seamlessly preserves context across sessions
by automatically capturing tool usage observations, generating semantic summaries, and making them available to future
sessions."

- **Peças:** hooks de ciclo de vida (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, SessionEnd), um
  serviço local ("Worker Service - Local HTTP API with web viewer UI and search endpoints, managed by Bun"), banco
  SQLite, Chroma para busca híbrida, a skill `mem-search` e 4 ferramentas MCP.
- **Busca em três camadas:** `search` devolve um índice compacto com ids (cerca de 50 a 100 tokens por resultado),
  `timeline` dá o contexto em volta, `get_observations` traz o detalhe só dos ids filtrados ("~10x token savings").
- **Quem resume:** depois de instalar, pede login no navegador e oferece o "claude-mem observer" hospedado (30 dias
  grátis), "your own OpenRouter or Gemini key, or your Anthropic plan". Tem "Cloud Sync" para o cmem.ai. Dá para pular
  o login com `--provider` ou `CLAUDE_MEM_ONLINE_OPTIN=false`.
- **Instala:** `npx claude-mem install` ou `/plugin marketplace add thedotmack/claude-mem`. Configuração em
  `~/.claude-mem/settings.json`; no Windows põe um executável em `%LOCALAPPDATA%\claude-mem\bin` e no Path do usuário.
  Também instala para Codex (via T3 Code), OpenCode e outros. Bun e uv são instalados sozinhos se faltarem.

## Relação com o hub e a construção

- **Faz o mesmo trabalho que o hub, por outro caminho.** "Lições do vault" e "Contrato file-first" decidiram que cada
  informação tem um lugar só, que a retomada mora numa nota no hub (não na memória privada do agente) e que o hook de
  fim leva ao hub o que só a memória privada sabe. O claude-mem cria uma segunda memória, privada, em
  `~/.claude-mem`, por máquina, fora do banco que replica entre os pares.
- **Disputa os mesmos ganchos.** Registra hooks em seis eventos do Claude Code no escopo do usuário, os mesmos em que o
  hub põe início de sessão, roteamento de skills, recusa antes da ferramenta e fim de resposta. É mudança global, e
  dois donos no mesmo evento complicam os testes da construção.
- **Dado de cliente.** O observador padrão é hospedado e há sincronização com o cmem.ai: observações do uso de
  ferramentas sairiam da máquina, inclusive de trabalho com STRATA, VOEGOL, AVIANCA, TRF3 e SBF. Com o plano da
  Anthropic como provedor, gasta a cota do Claude.
- **O que vale aproveitar:** a busca em três camadas (índice compacto, contexto, detalhe sob demanda) é um bom molde
  para as ferramentas do MCP de busca e do MCP do banco do hub, que precisam caber no contexto do agente.
- **Não verificado:** como os hooks dele convivem com o mod e os hooks do hub; o comportamento sem login.

## Conclusão do maestro

Não instalar, nem agora nem na construção: ele duplica o papel do hub, mexe nos mesmos hooks globais e, no modo padrão,
manda observações para fora. Fica no radar como referência de desenho (a busca em três camadas), para o segundo mapa
(memória de trabalho do agente).
