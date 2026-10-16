---
title: Relatório de varredura (texto integral do agente)
data: 2026-09-29
origem: subagente da sessão 3be42b76 (Claude Code, workspace TRF3)
aviso: saída de modelo; afirmações principais conferidas na seção 10 da exploração
---

## Resultado: ferramentas com canvas e orquestração de múltiplos agentes (pesquisa em 29/09/2026)

Há duas perguntas separadas: se a ferramenta tem canvas e se ela orquestra agentes. Muitas ferramentas põem vários agentes no canvas lado a lado, mas não deixam um agente conversar com outro nem delegar trabalho. Por isso separei os resultados em grupos. Estrelas e releases foram lidos direto das páginas do GitHub (HTML) em 29/09/2026.

### A. Canvas + orquestração real entre agentes de código (um agente fala com outro, delega ou encadeia)

| Nome | Link | O que é | Canvas? | Orquestra múltiplos agentes? | Plataformas | Licença/preço | Maturidade |
|---|---|---|---|---|---|---|---|
| Maestri | https://www.themaestri.app/en | Canvas infinito nativo: cada terminal é um nó e agentes ligados por uma linha conversam via PTY | Sim | Sim: um agente manda prompt para outro, delega, pergunta e passa o trabalho adiante | macOS 15.4+ (Apple Silicon), Windows 11 x64, Linux x64/arm64 (.deb/AppImage) | Proprietário. Free: 1 workspace. Pro: US$18 pagamento único | Código fechado, sem estrelas. Versão: não verificado |
| AgentGrid | https://agentgrid.sh | Canvas infinito com times de agentes, terminais, browser, notas e git | Sim | Sim: um agente orquestrador cria workers por papel (builder/QA/reviewer/devops) e roda o ciclo build→review→fix→validate | macOS, Windows, Linux | Proprietário. Product Hunt fala em "free options"; você usa suas próprias assinaturas. Preço final: não verificado | Product Hunt: 77 votos, lançado há cerca de 2 meses |
| TermCanvas | https://github.com/blueberrycongee/termcanvas (site termcanvas.com) | Desktop com canvas infinito para terminais e agentes, com worktrees | Sim | Sim: o toolkit "Hydra" tem um terminal Lead que coordena workers isolados | macOS, Linux, Windows | MIT | 406★. v0.39.10 (31/05/2026). Último commit 01/06/2026 |
| Agor (Preset) | https://github.com/preset-io/agor | "Figma para agentes": board 2D multiplayer com sessões e worktrees | Sim (2D, multiplayer) | Sim: teammates persistentes; via MCP os agentes fazem fork, spawn e reportam | Web self-hosted (npm, Homebrew, Docker), multiplataforma | BUSL-1.1 (vira Apache 2.0 em 2029) | 1.412★. v0.15.0 (28/03/2026). Commit 29/09/2026 |
| GraphCode | https://github.com/scgopi/GraphCode | Grafo de sessões de agentes CLI: nós são loops, arestas são handoff/mensagem/spawn | Sim (grafo) | Sim | Só macOS 15+ Apple Silicon | FSL-1.1-MIT | 132★. v0.1.76 (28/09/2026) |
| Catenary | https://thecatenary.app | IDE espacial (Electron) com fios de contexto entre agentes | Sim | Sim: fios passam contexto e instruções. "Maestro mode" com até 10 agentes e aprovação humana | Windows (winget), macOS, Linux | Proprietário freemium. Pro R$85 vitalício no lançamento (R$119 normal) | Repo só de releases: v1.0.5 (13/09/2026), 2★. Autor brasileiro (post no TabNews) |
| OmniRift | https://omnirift.omniforge.com.br / https://github.com/jessefreitas/OmniRift | Canvas open-source (Tauri/Rust) com agentes, PTYs, worktrees e navegador | Sim | Sim: encadeia saída→entrada, tem gates de revisão e um orquestrador "OmniAgent" via MCP/ACP | Repo: Linux, Windows, macOS Apple Silicon. Site cita Linux e Windows | Repo MIT, mas o site vende um Pro (R$14,90/mês ou R$109,90/ano) | 29★. v0.1.153 (03/09/2026) |
| Termscape | https://github.com/kdonev/termscape | Equipe de agentes CLI num canvas infinito, ligados por um hub MCP | Sim | Sim: agentes trocam mensagens, pedem review e criam helpers | macOS, Windows, Linux | MIT | 1★. v0.1.5 (13/09/2026). Commit 27/09/2026 |
| Agent Canvas (prayagtushar) | https://github.com/prayagtushar/agent-canvas | Agentes rodam como processos reais e você desenha as conexões | Sim (tem também uma "office view" em pixel-art) | Sim: "Bus" MCP local com message_peer, claim_task e memória compartilhada | Windows 10/11, macOS, Linux | MIT | 1★. Release: não detectado. Commit 04/09/2026 |
| ccanvas | https://github.com/DevoidSloth/ccanvas | "Excalidraw para vários agentes": terminais, agentes e previews | Sim | Sim: "logic arrows" com gatilhos on success/failure/match e joins AND/OR | Windows, macOS, Linux (Tauri ou web) | Apache-2.0 | 15★. Tag "rubens-version-v1.2.0" (26/09/2026) |
| TerminalX (tmx) | https://txc0ld.github.io/tmx/ | Canvas para Claude Code, Codex e Gemini, com fios entre agentes | Sim | Sim: fios com "auto-pipe" | Mac e Windows | MIT. Programa de early access | 2★. Site diz v0.1.0. Commit 21/05/2026 |
| termcanvas (lout33) | https://github.com/lout33/termcanvas | Canvas macOS sobre tmux, com árvore da frota | Sim | Sim: runtime agentmux (criar filho, conectar peer, delegar) | Só macOS Apple Silicon | MIT | 25★. v0.3.12 (02/08/2026) |

### B. Canvas com vários agentes lado a lado (visão e status, sem comunicação agente-agente documentada)

| Nome | Link | O que é | Canvas? | Orquestra? | Plataformas | Licença | Maturidade |
|---|---|---|---|---|---|---|---|
| Cate | https://github.com/0-AI-UG/cate | IDE em canvas infinito com terminais "agent-aware" | Sim | Parcial: worktree por agente, status e notificações | Win/macOS/Linux | MIT | 2.163★. v2.0.4 (26/09/2026) |
| Collaborator | https://github.com/collabs-inc/collab-public | Terminais, notas e código como tiles num canvas | Sim | Lado a lado | macOS/Windows (PowerShell/WSL2)/Linux | Open source; tipo de licença não verificado | 3.033★. v0.8.4 (16/06/2026) |
| OpenCove | https://github.com/DeadWaveWave/opencove | Canvas para agentes, tarefas e notas | Sim | Lado a lado | macOS/Windows/Linux | MIT | 1.601★. v0.3.3 (12/09/2026) |
| Horizon | https://github.com/peters/horizon | "Terminal board" com GPU num canvas 2D | Sim | Lado a lado | Linux/macOS/Windows | MIT | 713★. v0.2.7 (02/08/2026). Commit 29/09/2026 |
| Prowl | https://github.com/onevcat/Prowl | Central de comando macOS com vista Canvas de terminais vivos | Sim (vista de cards) | Lado a lado, com broadcast de comandos | macOS 26+ | Não verificado | 621★. v2026.9.25 |
| 49 Agents IDE | https://github.com/alpbahadur/49-IDE | IDE 2D para agentes em várias máquinas | Sim | Lado a lado, entre várias máquinas via relay | Web self-host + app macOS | BSL 1.1 | 612★. 0.4.0 (18/08/2026) |
| Vibecraft | https://github.com/rayzhudev/vibecraft | Workspace estilo RTS (jogo de estratégia) para agentes | Sim | Lado a lado | macOS/Windows/Linux | Apache-2.0 | 35★. v0.5.5 (02/03/2026) |
| CanvasTTY | https://github.com/SaneSanders/CanvasTTY | Desktop Electron espacial para PTYs e agentes | Sim | Lado a lado | Linux/Windows/macOS Apple Silicon | MIT | 0★. Commit 22/09/2026 |
| Ona Canvas | https://ona.com/canvas | Canvas para uma frota de agentes na nuvem, com comando por voz | Sim | Sim ("speak once, command many") | Nuvem/browser | Preço não verificado | Lista de espera |
| Replit Agent 4 | https://replit.com/blog/introducing-agent-4-built-for-creativity | Canvas de design com agentes paralelos | Sim | Sim: agentes paralelos por área | Web (nuvem) | Agentes paralelos só nos planos Pro/Enterprise | Lançado em 11/03/2026. Não serve para CLIs locais |

### C. Canvas de workflow e multiagente genérico (não é para agentes de código em terminal)

- Sim (https://github.com/simstudioai/sim): editor visual ReactFlow. Apache-2.0, 29.750★, v0.9.5 (29/09/2026). Roda na nuvem, self-host com Docker ou como app macOS.
- Langflow: MIT, 155.361★, v1.12.3. O suporte a multiagente só vi em fonte secundária.
- Flowise: 55.491★, flowise@3.1.4. Licença não verificada.
- Spine AI (Canvas na nuvem + Medley local-first): https://www.getspine.ai. Preço não verificado.
- MindPal Canvas: fetch bloqueado (429), então não verificado.
- claude-studio: editor DAG para `.claude/`. O repositório citado dá 404, então não verificado.

### D. Adjacentes ou descartados (e por quê)

- **OpenHands Agent Canvas:** "canvas" é só o nome. Não é espacial e é centrado em um único agente. Repo arquivado em 27/07/2026.
- **tldraw offline** (624★, v1.20.0) e **Whiteboard YC W26** (MIT, 2.161★, v0.1.5): são canvases onde os agentes desenham, não orquestradores.
- **Sem canvas** (usam painéis ou kanban): Flashwork (AGPL, painéis e handoff), Agent Teams (kanban com mensagens entre agentes, 2.185★), Mozzie, Nimbalyst (kanban + Excalidraw, 1.798★), vibe-kanban e o CopilotKit open-multi-agent-canvas (é um chat).
- **Não aprofundados:** agents-hub (Reece4000, 0★) e AgentCanvas da Developers Digest (a página deu 404 no fetch).

### Registro de cobertura

**Buscas (25):**
1. infinite canvas multiple AI coding agents terminals orchestration app
2. Maestri canvas AI agents terminals app
3. "canvas" Claude Code agents visual orchestration open source
4. Show HN canvas for running multiple coding agents in parallel
5. spatial canvas … "Figma for AI coding" Agor
6. ferramenta canvas orquestração multi-agente agentes de IA interface visual
7. node-based visual editor multi-agent workflow builder drag and drop LLM agents
8. reddit ClaudeAI app multiple Claude Code instances canvas whiteboard
9. Reddit com filtro de domínio (bloqueado)
10. github topic infinite-canvas ai-agents terminal
11. "agent canvas" desktop app spawn agents connect draw lines
12. HN Show HN spatial canvas terminals agents
13. "infinite canvas" "coding agents" Windows app 2026
14. multi-agent orchestration whiteboard tldraw agents
15. "mission control" canvas parallel AI agents Electron Tauri
16. agentes de código em paralelo canvas infinito terminais aplicativo
17. Product Hunt canvas AI agents orchestrate terminals
18. Spine/Jam/Flora multi-agent canvas
19. comparação AutoGen Studio/CrewAI Studio/Sim/Langflow/Dify
20. canvas agent-to-agent MCP hub coding agents
21. AgentCanvas developersdigest MCP
22. tldraw offline agents
23. Catenary releases
24. grafo/DAG de agentes de código
25. Replit Agent 4 infinite canvas

**Fontes visitadas:**
- Listas: awesome-agent-orchestrators (andyrewlee) e o GitHub topic infinite-canvas.
- Product Hunt: alternativas do Maestri, AgentGrid, Mozzie.
- Hacker News: 49 IDE e Whiteboard YC W26.
- TabNews (Catenary).
- Sites: themaestri.app (/en, /en/windows, /en/linux), agentgrid.sh, ona.com/canvas, omnirift.omniforge.com.br, thecatenary.app, txc0ld.github.io/tmx, getspine.ai, docs do OpenHands, blog do Replit.
- dev.to (claude-studio).
- Páginas GitHub (README, releases e commits) de cerca de 35 repositórios citados acima.

### Limites

- **Reddit:** o domínio está bloqueado para a ferramenta de busca, então não consultei.
- **GitHub:** a API bateu no limite de requisições e não há `gh` instalado. Estrelas, releases e datas vieram do HTML das páginas. A licença de Collaborator, Prowl e Flowise não foi confirmada.
- **Produtos fechados** (Maestri, AgentGrid, Catenary, Ona): as informações vêm só do site do fabricante. Não verifiquei a versão ou data do último release do Maestri nem o preço final do AgentGrid. MindPal e AgentCanvas (Developers Digest) não abriram.
- **Nada foi instalado nem testado.** As plataformas e a orquestração agente-a-agente são o que dizem os READMEs e sites. Vários projetos têm 0–30★ e podem ser experimentais ou abandonados.
- **Datas relativas:** as do Product Hunt e do HN eram relativas ("há 2 meses") e foram convertidas de forma aproximada.
- **Semelhança com o Maestri:** OmniRift e Catenary usam termos muito parecidos com os do Maestri (por exemplo "Maestro mode" e "Floors"). Parecem inspirados nele, mas não investiguei a relação.
