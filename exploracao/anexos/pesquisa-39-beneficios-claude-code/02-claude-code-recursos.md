---
title: Claude Code — recursos oficiais que o hub, o Maestri e os conceitos de custo usam
data: 2026-10-10
origem: subagente de pesquisa (Sonnet 5.5), ticket 39
fontes: https://code.claude.com/docs/en/memory ; https://code.claude.com/docs/en/hooks ; https://code.claude.com/docs/en/skills ; https://code.claude.com/docs/en/sub-agents ; https://code.claude.com/docs/en/mcp ; https://code.claude.com/docs/en/costs ; https://code.claude.com/docs/en/model-config ; https://code.claude.com/docs/en/prompt-caching ; https://code.claude.com/docs/en/headless ; https://code.claude.com/docs/en/common-workflows ; https://code.claude.com/docs/en/settings ; https://code.claude.com/docs/en/plugins
aviso: saída de modelo; citações literais em inglês; o que não foi conferido está marcado como **não verificado**.
---

Notas de método:

- Foram feitas 14 buscas (limite do ticket). As páginas `overview` e o índice (`llms.txt`) **não** foram abertos; as 12 páginas acima foram abertas direto.
- As páginas `memory` e `settings` voltaram grandes demais para o buscador (saída truncada); só o início de cada uma foi lido. O que veio delas está citado abaixo; o resto está em "Não verificado".
- `hooks`, `skills`, `sub-agents`, `mcp` e `model-config` foram lidas só nos primeiros 100.000 caracteres (as páginas têm entre 107 mil e 266 mil).
- Nas citações, os links Markdown internos foram removidos para deixar o texto legível; o texto das frases não foi alterado.
- A página "Optimizing for cost and intelligence" **não** foi aberta aqui. A coluna "Conceito de custo relacionado" usa os nomes das alavancas dados no pedido (prompt caching, effort, escolha de modelo, orquestrador/advisor, ciclo de vida do contexto, orçamentos).
- O comando `/cost` não aparece na página de custos atual; a página documenta `/usage` (ver seção 11).

---

## 1. CLAUDE.md e AGENTS.md (memória escrita por você)

(a) CLAUDE.md são instruções persistentes que o Claude Code carrega no início de cada sessão; a página diz que o Claude também pode ler os `AGENTS.md` de um repositório no lugar do CLAUDE.md. As instruções são contexto, não configuração imposta: para bloquear uma ação de verdade a página manda usar um hook PreToolUse.

(b)

> Each Claude Code session begins with a fresh context window.

> CLAUDE.md files: instructions you write to give Claude persistent context. Claude can also read a repository's AGENTS.md files in place of CLAUDE.md

> Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead.

(c) Benefício com o context hub: um `AGENTS.md` na raiz do hub é lido nativamente pelo Claude Code, então a regra "como trabalhar neste hub" vale para qualquer agente que abra o hub, nas duas máquinas, sem configurar nada fora da pasta. Como é contexto e não imposição, regras que precisam ser cumpridas sempre (ex.: gravar a nota de retomada) pedem hook, não só texto (ver seção 3).

(d) Benefício com o Maestri: cada terminal do canvas que abrir o hub como diretório de trabalho herda as mesmas instruções, então vários agentes em paralelo partem do mesmo contrato. **Não verificado** se o Maestri abre cada terminal no diretório do hub; é detalhe do Maestri, não do Claude Code.

(e) Conceito de custo relacionado: ciclo de vida do contexto (o CLAUDE.md entra em todo turno; ver seção 11, "Move instructions from CLAUDE.md to skills"). Também prompt caching: o CLAUDE.md fica na camada "Project context" do cache (seção 9).

---

## 2. Auto memory (anotações que o Claude escreve sozinho)

(a) Memória automática: notas que o Claude grava com base nas suas correções e preferências, por repositório e compartilhadas entre worktrees. Só as primeiras 200 linhas ou 25KB entram no início da sessão.

(b)

> Auto memory: notes Claude writes itself based on your corrections and preferences

> | **Scope** | Project, user, or org | Per repository, shared across worktrees |

> | **Loaded into** | Every session | Every session (first 200 lines or 25KB) |

(c) Benefício com o context hub: serve para preferências de uso do agente, mas **é local de cada máquina** (a página diz "Per repository"; replicação entre computadores **não verificada**). O conhecimento que precisa existir nas duas máquinas e para qualquer agente deve ficar em Markdown no hub, não na auto memory.

(d) Benefício com o Maestri: como é compartilhada entre worktrees do mesmo repositório, terminais paralelos em worktrees diferentes enxergam as mesmas notas. **Não verificado** o caminho de armazenamento e o que acontece com escritas simultâneas.

(e) Conceito de custo relacionado: ciclo de vida do contexto (limite de 200 linhas / 25KB no carregamento).

---

## 3. Hooks (Stop, SessionStart, PreToolUse etc.)

(a) Hooks são comandos (ou chamadas HTTP, ferramentas MCP, prompts, subagentes) que o Claude Code executa em pontos do ciclo de vida. Eles são determinísticos: o Claude Code os roda, não o modelo. Um hook pode bloquear uma ação (exit code 2) e o hook `Stop` pode impedir o Claude de parar.

(b)

> | `SessionStart` | "When a session begins or resumes" |

> | `PreToolUse` | "Before a tool call executes. Can block it" |

> | `Stop` | "When Claude finishes responding" |

> Exit with code 2 to block the action. On events that can block, Claude Code stops the action: a `PreToolUse` hook blocks the tool call, for example, and a `UserPromptSubmit` hook rejects the prompt.

> `Stop` | Yes | Prevents Claude from stopping, continues the conversation

Onde configurar (tabela da página):

> | `~/.claude/settings.json` | All your projects | No, local to your machine |
> | `.claude/settings.json` | Single project | Yes, can be committed to the repo |
> | `.claude/settings.local.json` | Single project | No, gitignored when Claude Code saves a setting to it |

Outros eventos citados na tabela: `PreCompact` ("Before context compaction"), `PostCompact`, `SubagentStop` ("When a subagent finishes"), `SessionEnd` ("When a session terminates"), `InstructionsLoaded` ("When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context"), `WorktreeCreate`.

(c) Benefício com o context hub: um hook `Stop` que sai com código 2 enquanto a nota de retomada não foi gravada obriga o agente a escrever antes de encerrar o turno, o que implementa por mecanismo o critério "um /clear a qualquer momento não perde nada". Um hook `SessionStart` pode injetar no início da sessão o mapa/ticket corrente. **Não verificado**: o formato exato da saída JSON do `SessionStart` e do `Stop` (a página lida foi cortada nessa parte).

(d) Benefício com o Maestri: o mesmo conjunto de hooks (em `.claude/settings.json` dentro do hub) vale para todos os terminais, sem depender de cada agente "lembrar". `SubagentStop` e `PreCompact` permitem registrar o estado do trabalho antes de perder contexto.

(e) Conceito de custo relacionado: ciclo de vida do contexto; a página de custos também usa hook `PreToolUse` para filtrar saída de testes e reduzir tokens ("Offload processing to hooks and skills").

---

## 4. Skills (incluindo `~/.claude/skills`)

(a) Uma skill é uma pasta com um `SKILL.md` (frontmatter + instruções). Só a descrição fica no contexto; o corpo carrega quando a skill é usada, por isso material de referência longo custa pouco até ser necessário.

(b)

> Unlike CLAUDE.md content, a skill's body loads only when it's used, so long reference material costs almost nothing until you need it.

> | Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects on this machine, but not Cowork or cloud sessions |
> | Project | `.claude/skills/<skill-name>/SKILL.md` | Sessions in this repository. Commit it so your team gets it too |

> Add `context: fork` to your frontmatter when you want a skill to run in isolation. Claude Code starts a new subagent of the type set in the `agent` field and gives it the skill content as its prompt.

Campos de frontmatter citados: `name`, `description`, `when_to_use`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model` ("Model to use when this skill is active."), `context`, `agent`, `paths`.

(c) Benefício com o context hub: o fluxo de trabalho do hub (ex.: protocolo de varredura, formato de ticket) pode viver como skill dentro de `.claude/skills/` na pasta do hub e viaja com ele para a outra máquina; a skill pessoal em `~/.claude/skills` não viaja (é "on this machine"). Skill com `context: fork` roda isolada e devolve só o resultado.

(d) Benefício com o Maestri: a skill pode fixar `model:` por tarefa e `allowed-tools`, dando a cada terminal um perfil diferente sem editar o prompt. Atenção: a página de prompt caching diz que uma skill com `model` diferente da sessão é uma troca de modelo (cache perdido naquele turno; seção 9).

(e) Conceito de custo relacionado: ciclo de vida do contexto (carga sob demanda em vez de CLAUDE.md sempre carregado); escolha de modelo (campo `model`); orquestrador (skill em subagente via `context: fork`).

---

## 5. Subagentes (agentes customizados)

(a) Subagentes são assistentes especializados que rodam em janela de contexto própria, com prompt de sistema, ferramentas e permissões próprias. Definidos como arquivos Markdown em `.claude/agents/` (projeto) ou `~/.claude/agents/` (usuário), com `model`, `tools`, `disallowedTools`, `mcpServers` etc. no frontmatter.

(b)

> Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions.

> - **`model`**: Model to use: `sonnet`, `opus`, `haiku`, `fable`, a full model ID such as `claude-opus-5-5`, or `inherit`. When you omit it, Claude Code picks the model in the subagent model order.

> - **`mcpServers`**: MCP servers available to this subagent.

> - **`tools`**: Tools the subagent can use, as a comma-separated string such as `Read, Grep, Bash` or a YAML list. Inherits every tool available to subagents if omitted.

> By default, a subagent can spawn subagents of its own, up to three layers below the main conversation.

Subagentes embutidos: Explore ("A fast, read-only agent optimized for searching and analyzing codebases."), Plan, General-purpose.

(c) Benefício com o context hub: um subagente de busca com `tools: Read, Grep, Glob` (somente leitura) e `model: haiku` pode vasculhar o hub e devolver só o resumo, sem poluir a conversa principal. Pelo campo `mcpServers`, um subagente pode receber o MCP de busca do hub sem que a sessão principal pague o contexto dele.

(d) Benefício com o Maestri: é o equivalente interno ao canvas de "orquestrador + trabalhadores": uma sessão principal delega tarefas verbosas a subagentes de modelo menor. Já os terminais paralelos do Maestri são sessões independentes (cada uma com contexto próprio), o que é outra coisa; os dois mecanismos podem coexistir.

(e) Conceito de custo relacionado: orquestrador/advisor e escolha de modelo (página de custos: "For simple subagent tasks, specify `model: haiku` in your subagent configuration"); ciclo de vida do contexto (saída verbosa fica no subagente).

---

## 6. MCP (escopos e arquivos de configuração)

(a) MCP conecta ferramentas externas. Há três escopos: local (padrão, privado, em `~/.claude.json` sob o caminho do projeto), projeto (arquivo `.mcp.json` na raiz, versionável) e usuário (`~/.claude.json`, todos os projetos). Servidores do `.mcp.json` pedem aprovação em sessões interativas.

(b)

> Project-scoped servers enable team collaboration by storing configurations in a `.mcp.json` file at your project's root directory.

> User-scoped servers are stored in `~/.claude.json` and provide cross-project accessibility, making them available across all projects on your machine while remaining private to your user account.

> claude mcp add --transport http <name> <url>
> claude mcp add [options] <name> -- <command> [args...]

> In `claude -p` runs, Agent SDK sessions, and cloud sessions, Claude Code can't show that prompt: it loads project-scoped servers without asking.

> - `${VAR}`: expands to the value of environment variable `VAR`

(c) Benefício com o context hub: um servidor MCP de busca do hub declarado em `.mcp.json` na raiz do hub é versionado junto e usa `${VAR}` para o caminho, o que ajuda a mesma configuração servir nos dois computadores (caminhos diferentes por máquina via variável de ambiente). Em `claude -p` o servidor do projeto carrega sem pedir aprovação, relevante para automação.

(d) Benefício com o Maestri: todos os terminais abertos no hub enxergam o mesmo `.mcp.json`; para um terminal específico, `--mcp-config` (seção 8) ou `mcpServers` num subagente (seção 5) restringem quem usa o quê.

(e) Conceito de custo relacionado: ciclo de vida do contexto (definições de ferramentas MCP adiadas por padrão: "MCP tool definitions are deferred by default, so only tool names and server instructions enter context until Claude uses a specific tool" — página de custos); prompt caching (conectar/remover servidor pode invalidar o cache quando as ferramentas não são adiadas; seção 9).

---

## 7. Worktrees e sessões paralelas

(a) `claude --worktree <nome>` cria um checkout git separado (outro branch) para uma sessão isolada; repetir em outro terminal com outro nome dá uma segunda sessão paralela sem que as edições colidam. Precisa de ao menos um commit no repositório.

(b)

> Each git worktree is a separate checkout on its own branch, created from an existing commit, so the repository needs at least one commit first.

> claude --worktree feature-auth

> Run the same command with a different name in a second terminal to start an isolated parallel session.

> In a repository with no commits, the command fails with `Failed to resolve base branch "HEAD": git rev-parse failed`.

Retomada: `claude --continue` ("resumes the most recent session in the current directory") e `claude --resume`. A página aponta para "background agents" (`/docs/en/agent-view`) para monitorar sessões paralelas numa tela só (**não lida**).

(c) Benefício com o context hub: o hub é uma pasta de Markdown replicada, não precisa de worktree para ler. Worktrees servem se o hub for um repositório git e dois agentes forem **escrever** ao mesmo tempo; sem isso, as duas escritas disputam os mesmos arquivos. **Não verificado** o comportamento de worktree quando a pasta é replicada entre computadores por outra ferramenta. Neste repositório, aliás, o git ainda não tem commits (git status mostra tudo como não rastreado), então `--worktree` falharia hoje.

(d) Benefício com o Maestri: é o par natural do canvas de terminais paralelos: cada terminal em seu worktree evita colisão de edição, e a página recomenda exatamente "two terminals" para isso.

(e) Conceito de custo relacionado: ciclo de vida do contexto (sessões separadas, contextos separados). Também prompt caching: a página diz que o cache é por máquina e diretório, então sessões em worktrees diferentes não compartilham cache (seção 9, "Cache scope").

---

## 8. Modo headless (`claude -p`) e Agent SDK

(a) `claude -p` roda o Claude Code sem interface, com a mesma ferramenta e laço de agente; o Agent SDK (Python e TypeScript) dá controle programático. Serve para scripts, CI e automações; a saída pode ser `text`, `json` ou `stream-json`, e `--bare` dispensa carga automática de hooks, skills, MCP, auto memory e CLAUDE.md.

(b)

> The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code. It's available as a CLI for scripts and CI/CD, or as Python and TypeScript packages for full programmatic control.

> claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"

> Add `--bare` to reduce startup time by skipping auto-discovery of hooks, skills, custom commands, subagents, installed plugins, MCP servers, auto memory, and CLAUDE.md.

> With `--output-format json`, the response payload includes `total_cost_usd` and a per-model cost breakdown, so scripted callers can track spend without consulting the usage dashboard.

> Use `--continue` to continue the most recent conversation, or `--resume` with a session ID to continue a specific conversation.

Também citado: `--max-budget-usd` ("If the run reaches its `--max-budget-usd` cap, Claude Code stops the remaining background work instead of waiting.").

(c) Benefício com o context hub: tarefas de manutenção do hub (reindexar, gerar resumo, checar links) podem rodar por script ou agendamento, com `--bare` + `--mcp-config`/`--settings` para ser reproduzível nas duas máquinas, e com `--max-budget-usd` como teto de gasto. Isto é **uso programático** do Claude Code, não do Maestri.

(d) Benefício com o Maestri: um terminal pode lançar trabalhadores `claude -p` com modelo e permissões explícitos e ler `total_cost_usd` de cada um, o que dá medição de custo por tarefa. **Não verificado** como o Maestri integra isso.

(e) Conceito de custo relacionado: orçamentos (`--max-budget-usd`, `total_cost_usd`); prompt caching (em `-p` o TTL de uma hora vale para a conversa principal só em assinatura dentro do plano; seção 9).

---

## 9. Prompt caching no Claude Code

(a) O Claude Code usa prompt caching automaticamente: reenvia o contexto inteiro a cada turno e a API reaproveita o prefixo que não mudou, cobrando a releitura pela tarifa de cache. O casamento é exato, então uma mudança no meio do prefixo recalcula tudo depois dela. Quase tudo que muda o prefixo (trocar de modelo, mudar o effort em alguns modelos, ligar fast mode, adicionar/remover ferramentas MCP não adiadas, compactar) custa um turno mais lento e caro.

(b)

> The API caches by matching the start of each request, called the prefix, against content it recently processed. [...] The match is exact, so a change anywhere in the prefix recomputes everything after it.

> | System prompt | Core instructions, tool definitions | The set of loaded tool definitions changes |
> | Project context | CLAUDE.md, auto memory, unscoped rules | Session starts, or after `/clear` or `/compact` |
> | Conversation | Your messages, Claude's responses, tool results | Every turn |

> Pick your model and effort level at the top of a session, then save `/compact` for natural breaks between tasks. The fewer changes you make mid-task, the higher your cache hit rate.

> Each model has its own cache. Switching with /model means the next request reads the entire conversation history with no cache hits, even though the content is identical.

> Editing them mid-session does not invalidate the cache, but the edit also doesn't apply. Claude keeps working with the version that was loaded at session start. The new content loads on the next `/clear`, `/compact`, or restart.

TTL:

> Unless you choose a TTL yourself, Claude Code requests the one-hour TTL only on a Claude subscription within your plan's included usage.

> Subagents fall outside the main-conversation TTL bucket, so they get five minutes even on a subscription until you choose a longer one.

> In Claude Code, the cache is effectively scoped to one machine and directory.

Variáveis: `DISABLE_PROMPT_CACHING` ("Disable for all models"), `CLAUDE_CODE_PROMPT_CACHE_TTL` / `promptCacheTtl` (5m ou 1h), `ENABLE_PROMPT_CACHING_1H=1` ("requests one hour for both buckets"), `FORCE_PROMPT_CACHING_5M=1`.

(c) Benefício com o context hub: o hub não escolhe nada aqui, mas o desenho dele interage com o cache: o `AGENTS.md`/CLAUDE.md do hub fica na camada "Project context" e **editá-lo no meio da sessão não vale até `/clear`, `/compact` ou reinício**; e como o cache é "one machine and directory", as duas máquinas nunca compartilham cache. Manter o `AGENTS.md` estável e curto, e puxar o resto sob demanda (skill, busca), preserva o prefixo.

(d) Benefício com o Maestri: a página diz que sessões paralelas **no mesmo diretório** montam prefixos iguais e leem o cache umas das outras ("Sessions you run in parallel in the same directory build matching prefixes and read each other's cache"), enquanto diretórios diferentes (worktrees) não compartilham. Isso afeta o custo de abrir vários terminais: mesmo diretório e mesmo modelo é mais barato em cache do que worktrees separados. Trocar de modelo no meio de um terminal custa o cache dele.

(e) Conceito de custo relacionado: **prompt caching** (é o próprio conceito); também escolha de modelo e effort (cada um tem seu cache), ciclo de vida do contexto (compactação).

---

## 10. Compactação de contexto (`/compact`, auto-compact, 1M)

(a) A compactação substitui o histórico de mensagens por um resumo, para liberar espaço. Dispara à mão com `/compact` (aceita instruções do que preservar) ou sozinha perto do limite da janela ("auto-compact window"). Há variantes de modelo com janela de 1 milhão de tokens (`sonnet[1m]`, `opus[1m]`).

(b)

> Compaction replaces your message history with a summary.

> Claude Code automatically optimizes costs through prompt caching, which reduces costs for repeated content like system prompts, and auto-compaction, which summarizes conversation history when approaching context limits.

> `/compact Focus on code samples and API usage` tells Claude what to preserve during summarization.

> # Compact instructions
>
> When you are using compact, please focus on test output and code changes

> To choose when its overhead happens, run `/compact` at a natural break in your work, such as between tasks, instead of waiting for auto-compaction to trigger mid-task.

> To keep sessions at a 200K window, set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` in your shell or in a settings file.

> The conversation has grown close to the session's auto-compact window, the threshold where Claude Code summarizes older history to free space.

Eventos de hook: `PreCompact` ("Before context compaction") e `PostCompact` ("After context compaction completes").

(c) Benefício com o context hub: o que importa sobreviver à compactação deve estar em arquivo do hub (file-first), não no chat; o CLAUDE.md/AGENTS.md é recarregado do disco depois da compactação ("It reloads project context from disk"), então regras ali sobrevivem. Um hook `PreCompact` pode gravar a nota de estado antes do resumo.

(d) Benefício com o Maestri: em terminais longos, uma seção "Compact instructions" no CLAUDE.md do hub orienta o que cada agente preserva ao compactar. Janela de 1M permite sessões longas, mas **a página de custos avisa que contexto longo é o principal motivo de gasto** ("Long context").

(e) Conceito de custo relacionado: **ciclo de vida do contexto** (`/clear`, `/compact`, auto-compact, janela de 1M); prompt caching (compactar invalida a camada de conversa).

---

## 11. Custos: `/usage`, estatísticas de cache e como reduzir tokens

(a) A página de custos documenta o comando `/usage` (não `/cost`) com o total da sessão, o consumo por modelo e, desde certa versão, uma linha de estatística do cache. Lista também práticas para reduzir tokens: `/clear` entre tarefas, instruções de compactação, escolha do modelo, adiar ferramentas MCP, hooks e skills no lugar de CLAUDE.md longo, esforço de raciocínio menor e subagentes para operações verbosas.

(b)

> Claude Code charges by API token consumption.

> Across enterprise deployments, the average cost is around $13 per developer per active day and $150-250 per developer per month, with costs remaining below $30 per active day for 90% of users.

> Prompt cache (main):   14 requests · 91% of input tokens from cache · 2 misses (last 6m 10s ago, 310.2k tokens re-cached) · 1 expected rebuild (compaction or tool-result clearing) · warm (1h TTL, last activity 40s ago)

> Clear between tasks: Use `/clear` to start fresh when switching to unrelated work. Stale context wastes tokens on every subsequent message.

> Your CLAUDE.md file is loaded into context at session start. [...] Skills load on-demand only when invoked, so moving specialized instructions into skills keeps your base context smaller. Aim to keep CLAUDE.md under 200 lines by including only essentials.

> Agent teams use approximately 7x more tokens than standard sessions when teammates run in plan mode, because each teammate maintains its own context window and runs as a separate Claude instance.

> Unexpectedly high spend on an API or cloud-provider plan: usually traces back to long sessions that were never cleared or to Opus left as the default model.

(Os dólares da primeira citação são média de implantações corporativas; **não** são previsão para o hub.)

(c) Benefício com o context hub: o próprio critério de custo da página (CLAUDE.md curto, conhecimento sob demanda) coincide com o desenho "AGENTS.md curto + notas em arquivo + busca"; a linha `Prompt cache (main)` do `/usage` permite medir se o hub está sendo lido de forma que preserva o cache.

(d) Benefício com o Maestri: para vários terminais em paralelo, a página alerta que "Agent teams" (um recurso experimental à parte, desligado por padrão) gastam cerca de 7x mais; o mesmo raciocínio vale para N terminais independentes: cada um tem contexto próprio e paga a si mesmo. **Não verificado** se terminais do Maestri se enquadram em "agent teams" (provavelmente não; são sessões separadas).

(e) Conceito de custo relacionado: **orçamentos** (`/usage`, `--max-budget-usd`), ciclo de vida do contexto, escolha de modelo, effort, prompt caching.

---

## 12. Escolha de modelo (`/model`, aliases, `opusplan`, advisor)

(a) O modelo é escolhido por alias (`sonnet`, `opus`, `haiku`, `opusplan`) ou nome completo, em sessão (`/model`), na partida (`--model`), por variável (`ANTHROPIC_MODEL`) ou em settings. `opusplan` usa Opus no modo de planejamento e Sonnet na execução. Uma ferramenta "advisor" permite o modelo da sessão consultar um segundo modelo no meio da tarefa.

(b)

> - **`opusplan`**: Special mode that uses `opus` during plan mode, then switches to `sonnet` for execution

> 1. **During session**: use `/model <alias|name>` to switch immediately, or run `/model` with no argument to open the picker.
> 2. **At startup**: launch with `claude --model <alias|name>`
> 3. **Environment variable**: set `ANTHROPIC_MODEL=<alias|name>`
> 4. **Settings**: configure permanently in your settings file using the `model` field

> For a hybrid approach where Claude decides mid-task when to consult a second model rather than switching at the plan boundary, see the advisor tool.

> Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning.

(c) Benefício com o context hub: o hub pode registrar no `AGENTS.md` qual modelo usar para cada tipo de tarefa (leitura/busca vs. decisão), e o modelo vira configuração de subagente/skill em vez de escolha ad hoc. O comando `/model` no meio da sessão custa o cache (seção 9).

(d) Benefício com o Maestri: é a base da estratégia "orquestrador": cada terminal pode ser iniciado com `claude --model <alias>` diferente (ex.: um terminal Opus para decidir, outros Sonnet/Haiku para executar). **Não verificado** como o Maestri passa a flag `--model` ao abrir um terminal.

(e) Conceito de custo relacionado: **escolha de modelo** e **orquestrador/advisor** (`opusplan` e a ferramenta advisor são as duas formas oficiais de dividir trabalho entre modelos dentro de uma sessão). Os detalhes do advisor (`/advisor`, `advisorModel`, `--advisor`) **não foram lidos**; a página só os menciona.

---

## 13. Effort (nível de esforço de raciocínio)

(a) O effort controla quanto o modelo raciocina por passo (raciocínio adaptativo). Define-se por `/effort`, `--effort`, `CLAUDE_CODE_EFFORT_LEVEL` ou em settings (`effortLevel`). Níveis menores reduzem custo de tokens de pensamento.

(b)

> Effort levels control adaptive reasoning, which lets the model decide whether and how much to think on each step based on task complexity.

> **`/effort`**: run `/effort` with no arguments to open an interactive slider, `/effort` followed by a level name to set it directly, or `/effort auto` to clear your saved level for the active model.

> set `effortLevel` to `low`, `medium`, `high`, or `xhigh` as the default for models without one. `max` isn't accepted as a level in either key

> Thinking tokens are billed as output tokens, and the default budget can be tens of thousands of tokens per request depending on the model.

> On Opus 5.5, Sonnet 5.5, Haiku 5.5, and Fable 5.1 with an API key or a Claude subscription, changing effort keeps the cache, and Claude Code applies the new level without asking.

(c) Benefício com o context hub: tarefas de leitura e indexação do hub toleram effort baixo; decisões de desenho pedem alto. Pode-se fixar `effortLevel` no `.claude/settings.json` do hub para o padrão do projeto.

(d) Benefício com o Maestri: cada terminal pode subir com `--effort` próprio (`claude` ... `--effort`: "pass a level name to set it for a single session when launching Claude Code"), combinando modelo e esforço por papel do agente.

(e) Conceito de custo relacionado: **effort** (é o próprio); prompt caching (em modelos mais antigos, trocar o effort no meio da sessão perde o cache).

---

## 14. Fast mode

(a) Modo rápido: variante de velocidade, com tarifa própria, ligada por `/fast`. A única informação conferida é como ele interage com o cache; a página própria (`/docs/en/fast-mode`) **não foi aberta**.

(b)

> Enabling fast mode adds a request header that is part of the cache key, so the first request Claude Code sends with fast mode on reads the entire conversation history with no cache hits.

> Those uncached input tokens are billed at fast mode rates, which is why turning it on at the start of a session costs less than turning it on deep into a long one.

(c) Benefício com o context hub: nenhum direto e conferido. **Não verificado.**

(d) Benefício com o Maestri: **não verificado** (sem informação sobre uso por terminal).

(e) Conceito de custo relacionado: prompt caching (ligar fast mode no meio de sessão longa é caro); o resto da relação com tarifas e velocidade **não verificado**.

---

## 15. Plugins

(a) Um plugin é um diretório de skills, subagentes, hooks e servidores MCP instalado e carregado como uma unidade, normalmente com manifesto em `.claude-plugin/plugin.json`. Vem de um marketplace (catálogo em `.claude-plugin/marketplace.json`) ou direto de uma pasta com `--plugin-dir`.

(b)

> A Claude Code plugin is a directory of skills, agents, hooks, MCP servers, or other components that Claude Code installs and loads as one unit.

> Skills, subagents, hooks, and MCP servers all work on their own, without a plugin. A skill you save in `~/.claude/skills/`, for example, is available in every project on your machine.

> Context and usage: for each skill, agent, and command that Claude can invoke on its own, the name and description are in Claude's context on every turn so that Claude knows it exists.

> Claude Code never invalidates the cache for a plugin's skills, commands, agents, hooks, monitors, or themes. It appends their content after the existing conversation

Escopos de instalação: "User scope: enabled for you in every project on this computer", "Project scope: enabled for everyone who works in this repository, through the committed `.claude/settings.json`", "Local scope".

(c) Benefício com o context hub: se o hub tiver skills, subagentes, hooks e `.mcp.json` próprios, empacotá-los num plugin dá uma unidade versionada que se instala igual nas duas máquinas. A página diz porém que **não precisa** de plugin para isso: tudo funciona solto dentro de `.claude/` do hub.

(d) Benefício com o Maestri: **não verificado**; o benefício é indireto (mesma configuração em todos os terminais).

(e) Conceito de custo relacionado: ciclo de vida do contexto (nome e descrição de cada skill/agente do plugin entram em todo turno); prompt caching (plugin de skills/agentes/hooks não invalida o cache; plugin com servidor MCP segue as regras do MCP).

---

## 16. Settings (`settings.json`, precedência) e pastas sem código

(a) As configurações vivem em arquivos JSON por escopo. A precedência, do mais forte ao mais fraco: gerenciado (organização), linha de comando (`--settings`), local do projeto, projeto compartilhado, usuário. Uma chave definida num nível mais alto vence a mesma chave definida abaixo.

(b) Do componente de precedência no início da página `settings` (texto do diagrama, não de prosa):

> Managed settings — managed-settings.json, MDM, or the claude.ai console — Your organization

> Command line — claude --settings — You, this session

> Project local — .claude/settings.local.json — You, this project

> Shared project — .claude/settings.json — Everyone in the project

> User — ~/.claude/settings.json — You, every project

Descrição do rótulo do diagrama: "A key set at a higher level overrides the same key set lower down."

Na página de fluxos de trabalho:

> Claude Code works in any directory. Run it inside a notes vault, a documentation folder, or any collection of markdown files to search, edit, and reorganize content the same way you would code.

> Claude reads files fresh on each tool call, so it sees edits you make in another application the next time it reads that file.

Da página de custos (sem aprofundar): permissões em `permissions.allow` / `--allowedTools` e a regra de que um deny de ferramenta inteira ("a bare tool name like `Bash` or `WebFetch`") remove a ferramenta.

(c) Benefício com o context hub: confirmação oficial de que uma pasta de Markdown é um uso suportado ("a notes vault, a documentation folder"), e de que o agente relê o arquivo a cada chamada, então uma edição vinda da outra máquina (replicação) é vista na próxima leitura, sem reiniciar a sessão. O `.claude/settings.json` do hub vale para todos que o abrirem; o `.claude/settings.local.json` fica por máquina, o que serve a caminhos locais.

(d) Benefício com o Maestri: configuração compartilhada no `.claude/settings.json` do hub e ajustes por terminal por `--settings <file-or-json>` (seção 8).

(e) Conceito de custo relacionado: orçamentos e permissões em geral, **nenhum** direto; `env` em settings serve para variáveis de cache e esforço (ex.: a página de prompt caching diz que variáveis podem ir "in the `env` block of managed settings"), mas o bloco `env` do `settings.json` do usuário **não foi lido**.

---

## Não verificado

- Páginas `overview`, índice `llms.txt`, `fast-mode`, `worktrees`, `agent-view`, `context-window`, `advisor`, `sessions`, `agent-sdk/*`, `hooks-guide`, `permissions`, `plugins/components`, `routines`, `scheduled-tasks`, `cross-session-messaging`: **não abertas** (limite de 14 buscas).
- `memory`: sintaxe de import (`@arquivo`) e profundidade máxima, mecanismo exato de leitura do `AGENTS.md` (se importa `@AGENTS.md` do CLAUDE.md ou lê direto), `.claude/rules/` e `paths:`, caminho de armazenamento e configuração da auto memory. A página foi truncada pelo buscador.
- `settings`: chave `env`, bloco `permissions` completo, `modelPricing`, lista de arquivos além da precedência. Truncada.
- `hooks`: formato do JSON de saída de `SessionStart`, `Stop` e `PreCompact` (o que pode ser injetado), campo `stop_hook_active` (anti-laço do `Stop`), timeouts. Página lida só até o caractere 100.000 de 266.639.
- `mcp`: seção "Scale with MCP tool search" (limiar `auto`, variável de configuração) e saída de ferramenta MCP; só as primeiras 100.000 de 119.442 caracteres.
- `sub-agents`: `memory`, `hooks` por subagente, "fork" e ordem de escolha do modelo ("subagent model order"); só os primeiros 100.000 de 108.547 caracteres.
- `skills`: `allowed-tools` e `model` com texto completo (a tabela foi abreviada com "…" na resposta do buscador).
- Se `/cost` ainda existe como comando: a página de custos documenta `/usage`. **Não verificado** se `/cost` é alias.
- A página "Optimizing for cost and intelligence" não foi comparada com nenhum recurso; os mapeamentos de alavancas são os nomes dados no pedido.
- Replicação entre duas máquinas (qualquer ferramenta de sincronização) e o comportamento de CLAUDE.md, auto memory e sessões diante dela: **a documentação oficial lida não trata**.
- Tudo sobre o Maestri (como abre terminais, passa `--model`, `--effort`, diretório): fora do escopo do Claude Code; **não verificado**.
