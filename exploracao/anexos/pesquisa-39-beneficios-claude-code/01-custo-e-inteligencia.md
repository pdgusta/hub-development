---
title: Custo e inteligência — os conceitos da página da Anthropic
data: 2026-10-10
origem: subagente de pesquisa (Sonnet 5.5), ticket 39
fontes:
  - https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence (158.557 caracteres; lida em 7 chamadas, janelas 0-100.000 e 100.000-fim)
  - https://platform.claude.com/docs/en/about-claude/pricing
  - https://platform.claude.com/docs/en/build-with-claude/effort
aviso: saída de modelo; citações literais em inglês; o que não foi conferido está marcado como **não verificado**.
---

# Custo e inteligência — os conceitos da página da Anthropic

Página: "Optimizing for cost and intelligence". Seções na ordem da página: Start here, Cache repeated context, Trim input and context tokens, Batch work that can wait, Audit prompts against the current model, Trade cost against intelligence (compare, upgrade, effort, re-run, budgets, elapsed time), Combine models (advisor, orchestrator), Measure on your own workload, tabela-resumo de alavancas, Benchmarks referenced, Next steps.

**Nota de método.** O WebFetch passa a página por um modelo pequeno que resume; para obter citações literais precisei de várias chamadas com pedidos específicos. As citações abaixo são o que a ferramenta devolveu como texto literal; a tabela-resumo e o rodapé de benchmarks vieram da janela final (offset 100000), salva em arquivo e lida direto. Palavras entre colchetes são texto de link (a URL foi removida pela ferramenta). Todos os números do relatório aparecem numa citação ou tabela abaixo. A própria página diz que os resultados são internos da Anthropic e direcionais, e que preços e medidas "will drift".

---

## 1. Start here (tabela de situação e ação)

**O que é.** Uma tabela que mapeia a sua situação à alavanca certa, separando "free wins" (reduzem custo sem mexer na qualidade) de "tradeoffs" (trocam custo por inteligência). Serve de índice: em qualquer carga, ligue cache e corte tokens; o resto depende de sintomas medidos.

> "Free wins" cut spend without touching quality: prompt caching, token hygiene, a prompt audit against the model you are running, [batch processing] at 50% off for work that can wait up to 24 hours, and [workspace spend limits] as the backstop.

> "Tradeoffs" exchange cost for intelligence: model choice, effort, output caps and task budgets, an elapsed-time clock, and multi-model architectures.

Tabela (coluna "Where" omitida por conter só links; texto das células literal):

| Your situation | Do this |
| --- | --- |
| Any workload, any model | Turn on prompt caching and trim unneeded tokens; both are free |
| A person waits between turns | Use the 1-hour cache duration once about 1 turn in 20 follows a pause between 5 minutes and an hour and few gaps run over an hour. On Claude Fable 5.1, keep the 5-minute cache warm while pauses run minutes, and buy the 1-hour duration when pauses run toward an hour. On Claude Opus 5.5, keep the 5-minute cache warm instead when only a turn or two in 20 follow a pause of up to about half an hour |
| Costs are too high; quality is fine | Sweep effort down on your current model |
| You are not on the latest model | Upgrade; in Anthropic's measurements each newer model solved at least as many tasks as the one before it, usually for less per solved task |
| You are choosing or switching models | Compare on cost per completed task, not per token |
| Quality isn't good enough | If you lowered effort, restore it; otherwise try the next tier up at `low` effort |
| Attempts end with `stop_reason: max_tokens` | Raise `max_tokens`; 64,000 covered all but 2 of 14,000 turns measured at the default effort, and 128,000 cost nothing extra per solved task |
| You can check outputs (tests, a verifier) | Run everything at low effort and re-run failures at `high`; on the coding benchmark measured, the pass rate held at about half the cost |
| Agent loops with a few very costly runs | Set a task budget (beta; check the support table for which models), a Claude Managed Agents session budget, and a workspace spend limit |
| You want agent runs to finish sooner | Tell the model that time matters, and show it the elapsed time; on DRACO research tasks with Claude Opus 5.5, a single agent took 47% less time at a 60% lower cost on the typical task, with a score 4.1 points lower; on HLE and an internal physics set, the typical task took at most 14% less time, and the physics-set score was 3.0 points lower |
| A lower-cost model stalls only on hard decisions | Add a frontier advisor. It pays off when priced well above the executor and actually consulted, so first price the advisor's model alone at low effort and measure the consult rate |
| The work exceeds one context window | Delegate partitions to cheaper workers |

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): a tabela é um roteiro de diagnóstico, não uma configuração. No Claude Code o usuário só controla parte das alavancas (modelo, effort, o que entra no contexto); cache e orçamento de requisição são do harness. Aplicável como checklist de decisão por ticket; o que o harness expõe de fato é **não verificado** nesta página.

---

## 2. Cache repeated context: por que vem primeiro

**O que é.** Em tarefa agêntica cada turno reenvia a conversa inteira (prompt de sistema, definições de ferramentas, turnos anteriores); o cache faz esse reenvio custar cerca de um décimo. Por isso é a primeira alavanca: sem cache, o custo da tarefa cresce quase com o quadrado do número de turnos.

> Turn on [prompt caching] before any other lever, because every turn of an agentic task resends the entire growing conversation: system prompt, tool definitions, and every prior turn. A 40-turn task sends its first turn 40 times, so task cost grows with roughly the square of turn count. Caching does not stop the resending, but each resend costs about a tenth as much and processes faster: the prefix is billed at the [cache-read rate], a tenth of the input price, and each turn pays the 1.25x cache-write rate only for what is new.

Números de apoio:
- Tabela-resumo (literal): "Cost cut by a factor of 2.7 to 5.3 on agent loops; 83% on the triage run".
- Rodapé 17 (literal, parcial): "median cache-read share 84.2% of all input tokens, upper quartile 91.7%".
- Resumo da ferramenta (**citação literal não obtida**): abaixo de cerca de 80% de leitura de cache, procurar algo que quebra o cache; na DeepResearch Bench II o Claude Fable 5.1 foi de $37.94 para $7.12 por tarefa com cache e o Claude Sonnet 5 de $3.20 para $1.20.

Pricing page (literal): "A cache hit costs 10% of the standard input price, which means caching pays off after one cache read for the 5-minute duration (1.25x write), or after two cache reads for the 1-hour duration (2x write)."

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): se o Claude Code liga o cache sozinho é **não verificado** (a página trata da API). Inferência: arquivos do hub carregados sempre no começo (instruções, memória) devem mudar pouco e não conter dado por requisição; cada agente do canvas tem a sua própria conversa e portanto o seu próprio cache.

---

## 3. Pick the cache duration (5 minutos vs 1 hora)

**O que é.** A escolha entre o cache de 5 minutos (padrão, escrita a 1,25x) e o de 1 hora (escrita a 2x). A de 1 hora compensa quando há pausas de humano entre 5 minutos e 1 hora; com turnos em segundos, o padrão é mais barato.

> If your loop waits on a person between turns, use the [1-hour cache duration]. It costs more to write (2x the input price instead of 1.25x). A miss on either duration bills the whole prefix at the write price instead of the read price, so the longer duration pays off once a few turns per session follow a pause between 5 minutes and an hour.

> More than about 1 gap in 20 falls between 5 minutes and an hour, and gaps over an hour are rare: use the 1-hour duration.

> Turns arrive seconds apart: stay on the 5-minute default. When nothing paused, it cost 15% less than the 1-hour setting on Claude Sonnet 5 and about 15% to 18% less on Claude Opus 5.5.

> On Claude Fable 5.1 the cheapest setting is a different one. Its [cache read] costs 0.025x the input price ($0.25 USD per million tokens) while its cache writes keep the standard multipliers, so a keep-alive request that re-reads the prefix is cheap and the 1-hour duration's write premium is the larger bill. On Claude Fable 5.1, keep the 5-minute cache warm while a person is away for minutes, and buy the 1-hour duration when pauses run toward an hour:

Linha da tabela-resumo (literal): "Cheaper than the 5-minute default once about 1 turn in 20 follows a pause between 5 minutes and an hour and few gaps run over an hour, except on Claude Fable 5.1, where keeping the 5-minute cache warm is cheaper while pauses run minutes and the 1-hour duration wins when pauses run toward an hour, and on Claude Opus 5.5, where keeping the 5-minute cache warm is cheaper when only a turn or two in 20 follow a pause of up to about half an hour; with no pauses the default cost 15% less on Claude Sonnet 5 and about 15% to 18% less on Claude Opus 5.5".

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): o padrão de uso do Gustavo (um humano que lê, decide e responde, com pausas de minutos) é o caso "a person waits between turns". Qual duração o Claude Code usa e se ela é configurável: **não verificado**.

---

## 4. Keep-alive (aquecer o cache sem gerar nada)

**O que é.** Reenviar o pedido anterior com `max_tokens` 0 dentro de 4 minutos mantém o cache de 5 minutos vivo, cobrando só a leitura do cache. Útil quando a leitura de cache é muito barata (Fable 5.1: 0,025x).

> To keep the cache warm, send the previous request again with `max_tokens` set to 0 within 4 minutes of the previous request's start, and every 4 minutes after that, dropping `stream` if it was set. Count from the request's start, not its response's end: the [cache's 5-minute lifetime] runs from the start of the request that wrote or refreshed the entry, so time the response spent generating counts against it. That is the [pre-warming request]: it refreshes the cache's lifetime, generates nothing, and bills only the cache read. Do not change a byte of the prefix, and do not use `max_tokens: 1`, which samples a token for no reason.

Rodapé 16 (literal, parcial): "Anthropic's pre-launch API tests on Claude Opus 5.5 show that a `max_tokens: 0` request writes the cache and that the next request reads it; whether such a request refreshes an existing entry was not measured on Opus 5.5." Resumo da ferramenta (**citação literal não obtida**): a requisição é rejeitada com extended thinking, structured outputs, forced tool choice ou o parâmetro `compaction`.

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): é técnica de quem chama a API diretamente; não se aplica a quem usa o Claude Code pronto, salvo se o harness já faz isso (**não verificado**).

---

## 5. O que quebra o cache

**O que é.** O cache é um casamento exato de prefixo, na ordem ferramentas, prompt de sistema, mensagens. Qualquer mudança no meio invalida tudo que vem depois.

> Several things can break your cache during a task. Anything that changes per request, such as a timestamp or a queue position, placed ahead of the stable prefix turns every request into a full cache write: on the triage run in [Trim input and context tokens], a 25-token status line at the front of the system prompt cost $4.24 USD per run instead of $0.59 USD, more than running with caching off. Keep per-request text in the newest user turn.

> The cache is a byte-exact prefix match over the request in order (tools, then system prompt, then messages), so a change anywhere invalidates everything after it.

Outros quebradores (resumo da ferramenta, **citação literal não obtida**): mudar `effort` ou thinking no meio da sessão; editar o prompt de sistema, mudar o formato de saída, adicionar/remover/reordenar ferramentas; mudar o task budget depois da primeira requisição; limpar contexto em muitas passadas pequenas. Literais de apoio: "If you use context editing, [clear in a few large batches]." (página principal) e, da página de effort, "Changing top-level effort value between requests invalidates prompt caching, so vary it across workloads rather than within a conversation that relies on cache hits. On models that support it, use a per-message effort change instead, which preserves the cache."

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): aplicável por inferência. Trocar de modelo ou de effort no meio de uma sessão longa, ou editar o que é carregado no início (instruções do projeto), reabre a escrita do prefixo inteiro. Para o hub: manter estável o que é carregado de partida e pôr o que muda (rodada atual, status) no fim ou em arquivo lido sob demanda.

---

## 6. Como ligar o cache e verificar

**O que é.** Na API: o cache automático coloca os breakpoints; depois confira se as leituras de cache não caíram e use os diagnósticos de cache.

> Setup takes little work. [Automatic caching] places breakpoints for you; otherwise, the [Claude API skill] that ships with Claude Code can add caching to an existing integration from one prompt.

> Then confirm cache reads have not dropped; if they have, [cache diagnostics] shows where the prefix diverged.

Literal (texto junto do exemplo de código): "In agent loops most input tokens should be cache reads; if `cache_read_input_tokens` is small next to `input_tokens` plus `cache_creation_input_tokens`, check that caching is engaged and that the prefix stays the same between requests."

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): "ligar" vale para quem constrói integração na API; para o Claude Code, se o usuário tem algum controle é **não verificado**. Os campos de `usage` servem de medida se o hub algum dia registrar custo por tarefa.

---

## 7. Trim input and context tokens: tool search

**O que é.** Toda definição de ferramenta é entrada em todo turno; com muitas ferramentas (servidores MCP) o custo explode. Tool search carrega as definições sob demanda.

> Most agent requests carry tokens that never influence the answer. Trimming them rarely costs output quality, although not every lever here saved money when measured.

> Every tool definition attached to a request is input on every turn, and a few MCP servers add up to hundreds of them.

> With every definition loaded, the run cost nearly doubled as the catalog grew, tracking the schema tokens on each request. With tool search it stayed flat at every catalog size, 45% less at 502 tools. Accuracy was 15 to 18 of 20 in every cell either way, and the model never called a wrong tool, so at this scale the catalog costs money, not correctness.

Tabela-resumo (literal): "Tool search | 45% with 500 tool definitions attached; 20% with a GitHub MCP server | None | Neutral". Também: "With caching on, input trimming (image resizing and tool search) took a further 26% off the short run and 21% off the long one."

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): aplica-se se houver muitos servidores MCP conectados (o ambiente atual lista vários conectores). Se o Claude Code já adia o carregamento dessas ferramentas por conta própria é **não verificado** nesta página.

---

## 8. Files API com code execution (dados tabulares)

**O que é.** Em vez de colar uma tabela grande no prompt, subir o arquivo e deixar o modelo consultá-lo por execução de código.

> When the model has to compute over a table, upload it with the [Files API] and let the model query it with [code execution] instead of pasting it in.

> Pasted into the prompt, the table is about 91,000 input tokens on every request, and Claude Sonnet 5 answered 6 of 25 questions correctly. Uploaded, with code execution, it answered all 25, and the run cost about a twelfth as much. Claude Opus 5 showed the same pattern.

Tabela-resumo (literal): "Data files through code execution | 92% on a 25-question data task | A gain, 25 of 25 instead of 6 of 25 | Faster".

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): por inferência, é o princípio "dado grande fica em arquivo e é consultado por código, não colado na conversa". Para o hub: relatórios e tabelas volumosos ficam em arquivo e o agente lê por trecho ou processa com script. A página trata da Files API da Anthropic, não de arquivos locais; a equivalência é do autor deste relatório.

---

## 9. Context lifecycle (context editing, compaction, pruning)

**O que é.** Três formas de não carregar o histórico inteiro: context editing limpa resultados de ferramentas velhos; compaction resume o histórico automaticamente por limiar; pruning é feito por você, trocando resultados grandes e velhos por um extrato de uma linha nas fronteiras de tarefa. Só compensam em sessão longa.

> **Context lifecycle.** [Context editing] clears stale tool results, and [automatic compaction] with its threshold stops long loops from carrying their whole history forward.

> The context levers only pay on a session long enough to need them:

> On the 20-issue run they saved nothing, and context editing cost 74% more. On the long run the prune saved 39% and compaction 32%, while context editing changed nothing.

> The prune is a few lines you write yourself: at each task boundary, replace large stale tool results with a one-line extract.

Tabela-resumo (literal): "Prune stale tool results at task boundaries | 39% on the long triage run (compaction 32%); nothing on short loops | None measured | Neutral". Resumo da ferramenta (não literal) sobre a seção de cache: cada passada de context editing invalida o prefixo a partir do ponto limpo, então limpar em poucos lotes grandes.

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): corresponde ao `/clear` e à compactação do Claude Code; a regra "file-first" do projeto (gravar a decisão no arquivo e depois limpar) é o análogo humano do prune. Se o Claude Code compacta com o mesmo mecanismo da API: **não verificado**. A página avisa que em sessão curta a limpeza não poupa nada.

---

## 10. Ask for shorter answers

**O que é.** Em loop de agente cada token escrito volta como entrada nos turnos seguintes; respostas curtas economizam duas vezes.

> Ask for shorter answers. Output tokens cost five times input tokens on Claude Sonnet 5, and in an agent loop every token the model writes comes back as input on every later turn, so you pay for a long answer again and again.

> The one-line answer used 39% fewer output tokens than the two-line original and cost 14% less per run.

Tabela-resumo (literal): "Ask for shorter answers | 39% of output tokens, 14% of cost on the triage run | None | Faster".

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): aplica-se a relatórios de subagentes (devolver só o resumo) e a handoffs entre agentes no canvas. O ganho de 14% é de um benchmark específico, não transferível como número.

---

## 11. Batch API

**O que é.** Execução assíncrona com 50% de desconto em todos os tokens, com resultado em até 24 horas.

> The [Batch API] takes 50% off every token of a request, including cached ones, in exchange for results arriving any time within 24 hours. Route every request no one is waiting on through a batch, and keep the interactive path for the rest. Batching is the second-largest free lever after caching for unattended agent work

Pricing page (literal): "The Batch API allows asynchronous processing of large volumes of requests with a 50% discount on both input and output tokens." e "These multipliers stack with other pricing modifiers, including the Batch API discount and data residency." Sobre Managed Agents: "Sessions are stateful and interactive. There is no batch mode."

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): só serve para trabalho sem ninguém esperando (varreduras em lote, classificação de muitos documentos) feito por chamada direta à API. Não se aplica a sessões interativas do Claude Code nem a agentes do canvas, que são conversas com estado.

---

## 12. Audit prompts against the current model

**O que é.** Instruções escritas para um modelo antigo ("verify twice", "be maximally thorough", scratchpads manuais) podem custar dinheiro ou precisão num modelo novo. Auditar e remover o texto obsoleto reduz custo e às vezes sobe a acurácia.

> The effect is measurable. On a support-desk evaluation, prompts written for Claude Opus 4.8 cost 36% more per ticket on Claude Opus 5 for no change in accuracy. Running the audit over the same prompts made Opus 5 both cheaper than the unaudited version (by 14%) and more accurate (97% of tickets, up from 92%, a gain outside the noise). On the Claude Sonnet 4.6 to Claude Sonnet 5 migration, the audit took 14% off at the same accuracy:

> The two kinds of stale text have different costs. Instructions the new model follows too literally cost money: removing "verify twice" cut Opus 5's cost per ticket by a third, and removing "be maximally thorough" almost as much. Text that no longer fits the model costs accuracy instead: a retired thinking setting, contradictory rules, and a hand-rolled scratchpad that conflicts with the model's own thinking each restored 7 to 11 points on Opus 5 when removed

Rodapé 14 (literal): "An Anthropic-constructed set of 44 support tickets with deterministic grading".

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): é a alavanca mais diretamente aplicável ao hub, porque AGENTS.md, skills e memórias são "prompts escritos para um modelo". Cada troca de modelo é motivo para revisar instruções de ênfase e de processo. Cuidado: o benchmark mediu 44 tickets de suporte; o ganho no hub não está provado.

---

## 13. Compare models on cost per task

**O que é.** O preço por token engana: um modelo mais capaz faz menos trabalho (menos turnos, menos busca, menos retrabalho). Compare pelo custo por tarefa concluída e olhe a cauda (o décimo mais difícil), não a mediana.

> Price lists are written per token, and per token the frontier model looks expensive: Claude Fable 5.1's per-token price is several times Claude Sonnet 5's. You pay for completed tasks, though, so compare models on cost per completed task. A more capable model finishes a task with less work: fewer turns, less searching, less re-reading of its own context, and less backtracking. The per-token premium is often overwhelmed by doing less of everything.

> On the same subset, which Claude Opus 5.5 and Claude Fable 5.1 both largely saturate and whose scores are not comparable to the public leaderboard, Opus 5.5 at its default, `medium`, matched Fable 5.1 at its default (92.8% against 92.3%, inside run-to-run noise) for about a fifth of the cost per solved task ($0.22 USD against $1.19 USD).

> For most agent workloads, start with Claude Opus 5.5 at its default effort (`medium`), and use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still fall short.

> The ranking flips by workload, and no price list tells you which way. Price every candidate in cost per completed task on your own traffic, including Claude Opus 5.5 at its default effort and the frontier model at reduced effort.

> Price the tail of your workload, not the median: compare models on the hardest tenth of your tasks, not the typical one.

Também literal: "Claude Fable 5.1 at `low` effort solved 88.6% of tasks for $0.54 USD per solved task, against 77.4% for $0.84 USD from Claude Sonnet 5 at its default: 11 more points for 35% less per solved task, despite a per-token price five times higher." Contraexemplo do rodapé 3: "at Fable 5.1's default effort the pair reads the other way, 41% more per solved task than Sonnet 5."

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): o critério é "tarefas resolvidas por real gasto", não "qual modelo é mais barato por token". Para o hub, valeria registrar por tarefa o custo e se passou. A recomendação padrão da página (Opus 5.5 em `medium`) é para a API; o que o Claude Code usa por padrão é **não verificado**.

---

## 14. Upgrade the model

**O que é.** Se você está um ou dois modelos atrás, trocar a string do modelo é a alavanca mais barata; modelos novos tendem a gastar menos por tarefa resolvida. Não é garantido: medir.

> If you are a model or two behind, the cheapest lever is the model string.

> Anthropic prices Claude Opus 4.7, Opus 4.8, and Opus 5 identically per token, so any difference among them comes from how much work each model does per task: priced as a customer is billed, Claude Opus 4.8 solves the same share of tasks as Claude Opus 4.7 for 14% less per solved task, and Claude Opus 5 then solves 12 more points of tasks at 21% more per solved task. Claude Opus 5 at `low` effort beats Opus 4.8's default on this benchmark for about 30% of its cost per solved task, so the cheapest upgrade is the new model at a lower setting.

> Claude Opus 4.7, Opus 4.8, and Opus 5 each spend $8 USD to $15 USD per task but solve 7%, 15%, and 41% of tasks, so cost per solved task falls from $183 USD to $63 USD to $28 USD up the ladder.

> Compare on cost per solved task, not per token: the same text costs about 30% more tokens on Claude 4.7 and later models, so a per-token comparison makes the newer models look more expensive by construction.

Tabela-resumo (literal): "Opus 4.8 to Opus 5: 12 more points at 21% more per solved task (Opus 5 at `low` beats Opus 4.8 for about 30% of the cost); Sonnet 4.6 to Sonnet 5: 15% less per solved task, 5 more points; Fable 5 to Fable 5.1: 43% less per solved task at about the same score".

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): manter os agentes no modelo mais recente do mesmo tier e rever os prompts junto (seção 12). Nota da página: o tokenizador novo gera cerca de 30% mais tokens para o mesmo texto, então comparar por token engana.

---

## 15. Tune effort

**O que é.** `effort` regula quantos tokens o modelo gasta (texto, chamadas de ferramenta e thinking). É a alavanca mais direta e o experimento mais barato; em trabalho de pesquisa e conhecimento a curva custo-acurácia é quase plana.

> Effort is the most direct way to tune a model to your task.

> On the research and knowledge-work benchmarks (WideSearch, DeepWideSearch, BrowseComp, and GDPval, all with Claude Fable 5), the curve of accuracy against cost is nearly flat: `low` gave up 1 to 3 points for a third to a half off the cost per task, `medium` matched the default's accuracy at about 70% to 87% of its cost, and the default bought nothing measurable over `medium` on any of the four.

> Test each level in a separate session: changing top-level effort mid-session invalidates the cache (see [Cache repeated context]) and distorts the comparison.

Tabela-resumo (literal): "Lower effort | Knowledge work: `medium` 13% to 31%, `low` a third to a half; long coding: `medium` about 30% and `low` about two thirds, both against `high` | 1 to 3 points on knowledge work, 2 to 8 on long coding | Faster". Também: "Hard work does not automatically need high effort. On DeepResearch Bench II, Claude Fable 5.1 scored nearly the same at `low`, `medium`, and `high` while the cost per task rose from $4.66 USD to $7.12 USD".

Da página de effort (literal): "Most Claude models default to high effort ...; Claude Opus 5.5 and Claude Haiku 5.5 default to medium." Níveis e suporte na seção 25.

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): aplicável se o Claude Code deixar escolher o effort por sessão ou por subagente (há ferramentas de sessão com "effort" neste ambiente, mas o comportamento exato é **não verificado** nesta página). Pela página, `low` é indicado para subagentes; trocar de effort no meio da sessão quebra o cache, então definir por sessão.

---

## 16. Re-run failures at higher effort

**O que é.** Quando o resultado é verificável (testes, verificador), rode tudo em `low` e refaça só as falhas em `high`.

> When a task's outcome is checkable, the cheapest policy on the effort curve is not a fixed setting: run every task at a low setting and re-run only the failures at a higher one.

> With Claude Opus 5.5 at `low`, 13% of tasks failed; with those re-run at `high`, about 97% passed for about $0.17 USD each, against 95.3% for $0.29 USD running everything at `high`: a slightly higher pass rate for a little over half the cost, counting the failed cheap attempts.

> Two conditions apply. First, you need a failure signal (here, the benchmark's own tests); a checker that passes bad work lets those failures through. Second, every first-pass failure takes two runs' worth of wall-clock time, so the saving is paid for in latency on the failures.

Tabela-resumo (literal): "Re-run failures | About 40% against running everything at `high`, at the same pass rate or slightly better | None | Two runs on the tasks that fail".

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): só onde existe verificação objetiva (testes, checagem de formato e de links). Para pesquisa e decisão de design, sem sinal de falha, não se aplica (a página exige o sinal).

---

## 17. Set budgets and output caps (task budget, max_tokens, session budget)

**O que é.** Uma minoria de execuções gasta várias vezes a mediana. Três controles com funções distintas: task budget (o modelo vê e se economiza), `max_tokens` (teto de segurança por resposta, invisível ao modelo) e session budget em Managed Agents (parada dura em dólares); o limite de gasto do workspace é o último anteparo.

> Most agentic task runs are cheap, but a minority spend many times the median cost on searching, re-verifying, and over-testing.

> A generous budget cut cost per task 44% for about 3 points of pass rate, at the edge of run-to-run noise, and the tightest allowed budget cut it 58% for 6 points.

> Three controls do three different jobs. A task budget saves money, because the model sees it. `max_tokens` is a safety cap: lowering it cut cost per attempt without lowering cost per solved task. On Claude Managed Agents, a session budget is the hard dollar stop behind both. Set all three: a task budget, a high `max_tokens`, and a session cap for the run you never want on a bill, with a workspace spend limit as the final backstop.

> Budgets below the current 20,000-token floor are rejected, and very tight budgets can produce refusal-like behavior.

> On an internal repository-task benchmark, a 16,384-token cap ended about a quarter of Claude Opus 5.5's attempts and 43% of Claude Fable 5.1's, each at its default effort.

> Set `max_tokens` to 64,000 for agentic work, or to 128,000, the maximum, when a single cut-off attempt is costly; at 128,000 Fable 5.1 solved 60.0% for the same cost per solved task.

Task budgets: "in beta (beta header `task-budgets-2026-03-13`) on the most recent models"; "Start near your loop's 90th-percentile token usage, then tighten." Session budgets: "It is platform-enforced, works on any model with a list price, including models where task budgets are not yet available, and combines with the advisory task budget." Tabela-resumo (literal): "Task budget | 44% to 58% | 3 to 6 points | Faster" e "Raising `max_tokens` | None per solved task, but more tasks solved | Gains of up to 22 points on the internal set; none on the public pair | Neutral".

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): o análogo prático é limitar o escopo de cada tarefa de subagente e ter limite de gasto no workspace ou plano. Task budget e session budget são recursos da API e do Managed Agents; se o Claude Code os expõe é **não verificado**. Um agente do Maestri que não termina é o caso da "cauda de custo" descrito.

---

## 18. Show the model elapsed time

**O que é.** O modelo em loop não enxerga relógio. Dizer que o tempo importa e anexar o tempo decorrido à última mensagem do usuário reduz tempo e custo, com perda de nota em pesquisa profunda.

> A model in an agent loop can't see a clock.

> End the task message with a sentence that says time matters, and before each request, add the elapsed time to the end of the newest `user` message.

A frase da página, literal: "Time matters here: do not spend time that can be avoided, and the earlier a correct result is obtained, the better."

> On DRACO, the two changes cut a single agent's time by 47% and its cost by 60% on the typical task.

> Its score was 4.1 points lower (95% interval 2.9 to 5.2 lower).

> On HLE, the same changes cut a single agent's time by 14% and its cost by 9% on the typical question.

> On the physics set, the changes cut its time by 7% and its cost by 4% on the typical problem, and its score was 3.0 points lower (95% interval 0.4 to 5.6 lower).

(Medido com Claude Opus 5.5 em `medium`.) Rodapé 23 (literal, parcial): "The single agent's whole average time saving comes from one problem".

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): vale como instrução em prompts de subagentes de varredura quando perder um pouco de qualidade por velocidade é aceitável; o relógio é implementação do harness (se o Claude Code injeta tempo decorrido é **não verificado**). Pesquisa com fonte primária, regra deste projeto, é o tipo de tarefa em que a nota caiu (DRACO), então não é para ligar por padrão.

---

## 19. Advisor strategy (executor barato escala as decisões difíceis)

**O que é.** Um modelo mais barato conduz o loop e consulta um modelo de fronteira só nas decisões difíceis (escolher abordagem, recuperar de falha). Só compensa se o executor realmente consulta; em vários pares medidos ele quase nunca perguntou.

> In the advisor strategy, a lower-cost executor model runs the agent loop and performs most turns. When it hits a decision that needs deeper judgment, such as choosing an approach or recovering from a failure, it calls a higher-intelligence advisor model for strategic guidance, then continues. Most tokens are billed at executor rates, and only the occasional consultations at advisor rates.

> The second, and the fragile one, is whether the executor actually asks (the consult rate). Neither of those executors asked. In two runs each, Claude Haiku 5.5 and Claude Sonnet 5.5 called the Opus 5.5 advisor on none of the 198 questions, so both pairings scored within run-to-run noise of the executor alone.

> An executor at low effort can stop detecting that it is stuck: a pairing that consults on most tasks at the default effort can fall to consulting on almost none when effort is lowered, and then scores below the executor alone.

> On Chartography, a chart-reading benchmark, a Claude Opus 5.5 executor at `low`, given a Claude Fable 5.1 advisor, consulted it on 1 of 300 tasks and scored 61.7, 7 points below Opus 5.5 alone and beyond run-to-run noise, at about the same cost

> The advisor strategy suits workloads where turns are mostly mechanical but an excellent plan matters: coding agents, computer use, and multistep research pipelines. It fits poorly when every turn genuinely needs frontier capability, when there is nothing to plan (single-turn Q&A), or when your executor is already close to the advisor's capability.

> Whatever the pairing, first price the advisor's model alone at low effort; that is the baseline to beat.

Tabela-resumo (literal): "Advisor | Depends on the capability gap and the consult rate; the coding pairing scored 1.7 points over Claude Opus 5.5 alone at `high` for about 2.1 times the price, about what more effort buys; with Claude Opus 5.5, the chart-reading pairing almost never consulted the advisor and scored 7 points below Opus 5.5 alone | A gain on coding, a loss on chart reading | About one or two extra calls per task". Rodapé 9 (literal): "The advisor configurations added the tool without a prompt asking for consultations, and neither executor called the advisor on any question."

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): no canvas seria um agente barato ligado a outro mais forte que ele consulta; o risco principal (o executor não consultar) é de prompt e de effort, e se mede contando as consultas. Se o Maestri ou o Claude Code oferece algo equivalente à "advisor tool": **não verificado**.

---

## 20. Orchestrator strategy (modelo de fronteira delega trabalho em volume)

**O que é.** O modelo de fronteira segura o loop, decompõe e despacha subtarefas a modelos mais baratos e junta os resultados. Só vale para volume independente, idealmente maior que uma janela de contexto.

> In the orchestrator strategy, the frontier model holds the loop. It decomposes the task, dispatches subtasks to lower-cost worker models, and merges their results. The orchestrator's own transcript stays short because workers absorb the token-heavy exploration, so most tokens are billed at worker rates while the plan and synthesis still come from the frontier model.

> It saved money in only two measured situations. On work a single model could handle alone, the same model at lower effort was cheaper every time.

> Delegation paid on the routine, normally solvable share of the work, the opposite of the intuition that workers are for hard problems.

> An orchestrator buys something only when there is bulk to hand off: many independent pieces, ideally too many for one context window. When the work is one dependent chain, or fits in a single context, the orchestrator pays for a plan, a handoff, and a merge that a single model gets for free.

> If the work is one chain, fits in one context without a long cost tail, or a single model at lower effort already meets your bar, don't build an orchestrator.

Tabela-resumo (literal): "Orchestrator | About half against the frontier model, both beyond one context window and on routine tails (the latter measured on Claude Fable 5) | 10 to 12 points below the frontier model | Much faster on large inputs". Rodapé 8 (literal, parcial): "a 21.6-million-token corpus from 14 public Python package sources with 130 planted defects", com orquestrador Fable 5.1 e "25 concurrent Claude Sonnet 5 workers".

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): é o padrão natural do canvas (um agente líder, vários trabalhadores). Pela página, só compensa em varreduras volumosas e independentes (várias fontes, vários clientes em paralelo); para uma decisão de design (cadeia dependente) a própria página recomenda o mesmo modelo em effort menor. O custo de coordenação do Maestri: **não verificado**.

---

## 21. Combine models: escolher entre advisor e orquestrador

**O que é.** A decisão se resume a uma pergunta: o trabalho se divide em pedaços independentes ou é uma resposta alcançada por uma cadeia de passos dependentes? Sem mistura de dificuldade, um único modelo bem ajustado costuma ser melhor.

> Multi-model architectures fit workloads whose task complexity varies enough that different steps are best served by different models. When your traffic mixes routine work that a smaller model handles reliably with harder steps that need frontier capability, splitting the work keeps frontier intelligence where it matters while most tokens bill at smaller-model rates. When a workload lacks that mix, because its difficulty is uniform or it is one dependent chain, a single well-tuned model is usually the better choice.

Tabela (literal):

| Strategy | Control flow | Frontier model's role | Fits | Frontier cost scales with |
|---|---|---|---|---|
| **Advisor** | Smaller model runs the loop, escalates on demand | Consulted for plans and corrections | Serial work that is hard in spots, such as a coding agent's many turns between a few real decisions | How often the executor gets stuck |
| **Orchestrator** | Frontier model runs the loop, delegates the bulk work | Plans, dispatches, and synthesizes | Work that fans out across genuinely independent files, documents, or cases, especially more than one context window of it | How hard the pieces are to coordinate |

> Most cases come down to one question: does the work split into independent pieces, or is it one answer reached through a chain of dependent steps?

> If you are unsure, don't build anything yet:
> 1. Sweep effort on your current model first. It is the cheapest experiment on this page, and most workloads end there.
> 2. If the sweep shows a gap, price the stronger model alone at low effort. That is the number an advisor pairing has to beat, and the pairings on this page that beat it were the ones whose executor actually consulted.

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): usar a pergunta como critério antes de montar um time de agentes no canvas. Por inferência: o fluxo grill, spec, tickets é cadeia dependente (um modelo, effort ajustado); varreduras por cliente ou por fonte são pedaços independentes (candidatas a orquestrador).

---

## 22. Measure on your own workload (método em 4 passos)

**O que é.** Os números da página são medidas internas que mudam com preços e modelos; o método para repetir na sua carga é fixo.

> The numbers on this page reflect list prices at the time of measurement and will drift as models and prices change. Your escalation rate, how cleanly tasks split, and transcript length move them too. The method stays the same:
>
> 1. Pull a few tasks from production logs, weighted like real traffic, and [write outcome checks] for each: tests pass, ticket closed, row count correct. Record cost per task beside the score: price the five priced token counts in each response's `usage` at their own rates (uncached input, 5-minute and 1-hour cache writes at 1.25x and 2x the input price, cache reads, and output), summed across the task's requests (the [Usage and Cost API] reports the aggregate). On a model priced by prompt length, such as Claude Haiku 5.5, price each request at the rates for its prompt length: a request whose prompt, cache reads and writes included, is over the model's threshold pays the higher prices for all of its tokens (see [Long context pricing]).
> 2. Baseline the model tiers across effort levels, not only the default, and plot score against spend. A multi-model configuration must beat the single model's whole curve.
> 3. If the curve shows a gap effort can't close, add the multi-model strategy that fits and re-run the suite.
> 4. Run the winner in shadow on a traffic slice before cutover, then keep the suite running.

> The following example computes one request's step 1 cost at Claude Opus 5.5's list prices:

Parâmetros do exemplo de código (literal): `INPUT_PER_MTOK = 4.00 # Claude Opus 5.5`, `CACHE_READ_PER_MTOK = 0.20 # 0.05x the input price on Claude Opus 5.5; the multiplier differs by model`, `OUTPUT_PER_MTOK = 20.00`, com escrita de 1 hora a `* 2.00` e de 5 minutos a `* 1.25`. Nota literal: "When the advisor tool or compaction is enabled, some tokens are reported only in `usage.iterations` and not in the top-level totals, so sum over `usage.iterations` instead, pricing `advisor_message` entries at the advisor model's rates."

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): aplicável como método, sem os números: escolher poucas tarefas reais do hub com checagem objetiva, medir custo e resultado por modelo e effort, comparar. Como medir custo por tarefa no Claude Code a página não diz: **não verificado**. Este projeto roda testes e varreduras só a pedido do Gustavo; o método é para quando ele pedir.

---

## 23. Tabela-resumo das alavancas "in the order to try them" (literal)

| Lever | Saving in these runs | Quality cost | Latency |
| --- | --- | --- | --- |
| Prompt caching | Cost cut by a factor of 2.7 to 5.3 on agent loops; 83% on the triage run | None | Faster |
| 1-hour cache duration | (ver seção 3) | None | Stays warm after a pause |
| Input trimming | A further 5 percentage points on the triage run | None | Neutral |
| Prune stale tool results at task boundaries | 39% on the long triage run (compaction 32%); nothing on short loops | None measured | Neutral |
| Tool search | 45% with 500 tool definitions attached; 20% with a GitHub MCP server | None | Neutral |
| Data files through code execution | 92% on a 25-question data task | A gain, 25 of 25 instead of 6 of 25 | Faster |
| Batch API | 50% | None | Results within 24 hours |
| Prompt audit against the current model | 14% on both migrations measured | None; a gain on one | Faster (fewer tool rounds) |
| Upgrade the model | (ver seção 14) | A gain | Neutral |
| Lower effort | (ver seção 15) | 1 to 3 points on knowledge work, 2 to 8 on long coding | Faster |
| Re-run failures | About 40% against running everything at `high`, at the same pass rate or slightly better | None | Two runs on the tasks that fail |
| Task budget | 44% to 58% | 3 to 6 points | Faster |
| Ask for shorter answers | 39% of output tokens, 14% of cost on the triage run | None | Faster |
| Raising `max_tokens` | None per solved task, but more tasks solved | Gains of up to 22 points on the internal set; none on the public pair | Neutral |
| Advisor | (ver seção 19) | A gain on coding, a loss on chart reading | About one or two extra calls per task |
| Orchestrator | (ver seção 20) | 10 to 12 points below the frontier model | Much faster on large inputs |

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): as alavancas sem custo de qualidade (cache, trimming, prompt audit, respostas curtas) são as de maior retorno para o hub; as de troca (effort, budgets, advisor, orquestrador) exigem medida própria.

---

## 24. Modelos atuais, preços e multiplicadores

Da página principal (literal): "From lowest to highest cost and capability, the current models are Claude Haiku 5.5, Claude Sonnet 5.5, Claude Opus 5.5, and Claude Fable 5.1 (the frontier model); [Models overview] has the full lineup and prices."

Tabela de preços da página de pricing (literal; USD por milhão de tokens; modelos aposentados Opus 4.1, Opus 4, Sonnet 4 e Haiku 3.5 omitidos aqui, constam da fonte):

| Model | Base input tokens | 5m cache writes | 1h cache writes | Cache hits and refreshes | Output tokens |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Claude Fable 5.1 | $10 / MTok | $12.50 / MTok | $20 / MTok | $0.25 / MTok<sup>1</sup> | $50 / MTok |
| Claude Mythos 5.1 (limited availability) | $10 / MTok | $12.50 / MTok | $20 / MTok | $0.25 / MTok<sup>1</sup> | $50 / MTok |
| Claude Fable 5 | $10 / MTok | $12.50 / MTok | $20 / MTok | $1 / MTok | $50 / MTok |
| Claude Mythos 5 (limited availability) | $10 / MTok | $12.50 / MTok | $20 / MTok | $1 / MTok | $50 / MTok |
| Claude Opus 5.5 | $4 / MTok | $5 / MTok | $8 / MTok | $0.20 / MTok<sup>2</sup> | $20 / MTok |
| Claude Opus 5 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Opus 4.8 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Opus 4.7 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Opus 4.6 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Opus 4.5 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Sonnet 5.5 | $2 / MTok | $2.50 / MTok | $4 / MTok | $0.10 / MTok<sup>2</sup> | $10 / MTok |
| Claude Sonnet 5 | $2 / MTok<sup>3</sup> | $2.50 / MTok | $4 / MTok | $0.20 / MTok | $10 / MTok<sup>3</sup> |
| Claude Sonnet 4.6 | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Sonnet 4.5 | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Haiku 5.5 (for prompts up to 100,000 tokens) | $0.10 / MTok | $0.125 / MTok | $0.20 / MTok | $0.01 / MTok | $0.50 / MTok |
| Claude Haiku 5.5 (for prompts over 100,000 tokens) | $0.50 / MTok | $0.625 / MTok | $1 / MTok | $0.05 / MTok | $2.50 / MTok |
| Claude Haiku 4.5 | $1 / MTok | $1.25 / MTok | $2 / MTok | $0.10 / MTok | $5 / MTok |

> 1 Cache hits and refreshes on Claude Fable 5.1 and Claude Mythos 5.1 are priced at 0.025x the base input price. 2 Cache hits and refreshes on Claude Opus 5.5 and Claude Sonnet 5.5 are priced at 0.05x the base input price. All other models use the standard 0.1x multiplier. 3 The $2/$10 per million input/output token pricing for Claude Sonnet 5, announced at launch as introductory pricing through August 31, 2026, is now the standard price.

Multiplicadores de cache (pricing page, literal):

| Cache operation | Multiplier | Duration |
| --- | --- | --- |
| 5-minute cache write | 1.25x base input price | Cache valid for 5 minutes |
| 1-hour cache write | 2x base input price | Cache valid for 1 hour |
| Cache read (hit) | 0.1x base input price (0.025x on Claude Fable 5.1 and Claude Mythos 5.1; 0.05x on Claude Opus 5.5 and Claude Sonnet 5.5) | Same duration as the preceding write |

Batch (pricing page, literal, linhas lidas): Claude Fable 5.1 "$5 / MTok" de entrada e "$25 / MTok" de saída; Claude Opus 5.5 "$2 / MTok" e "$10 / MTok"; Claude Opus 5 "$2.50 / MTok" e "$12.50 / MTok". As linhas de Sonnet 5.5, Sonnet 5 e Haiku 5.5 da tabela de batch **não foram lidas**.

Outros (pricing, literal): "For Claude 4.6 and later models, using `inference_geo: "us"` applies a 1.1x pricing multiplier." e "This tokenizer produces approximately 30% more tokens for the same text." (modelos 4.7 e posteriores).

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): serve de base para estimar custo, mas se o plano de assinatura do Gustavo no Claude Code cobra por token a página não diz (**não verificado**). Observação aritmética do autor, derivada da tabela: Opus 5.5 custa $4 de entrada e $20 de saída contra $10 e $50 do Fable 5.1; Sonnet 5.5 custa $2 e $10; Haiku 5.5 custa $0.10 e $0.50 até 100.000 tokens de prompt.

---

## 25. Effort: níveis e suporte (página de effort, literal)

| Level | Description | Typical use case |
| -------- | -------- | -------- |
| `max` | Absolute maximum capability with no constraints on token spending. Available on Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5.5, Claude Sonnet 5, Claude Sonnet 4.6, and Claude Haiku 5.5. | Tasks requiring the deepest possible reasoning and most thorough analysis |
| `xhigh` | Extended capability for long-horizon work. Available on Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5.5, Claude Sonnet 5, and Claude Haiku 5.5. | Long-running agentic and coding tasks (over 30 minutes) with token budgets in the millions |
| `high` | Spends as many tokens as the task needs for excellent results. The default on every model that supports effort except Claude Opus 5.5 and Claude Haiku 5.5. | Complex reasoning, difficult coding problems, agentic tasks |
| `medium` | Balanced approach with moderate token savings. The default on Claude Opus 5.5 and Claude Haiku 5.5. | Agentic tasks that require a balance of speed, cost, and performance |
| `low` | Most efficient. Significant token savings with some capability reduction. | Simpler tasks that need the best speed and lowest costs, such as subagents |

> Effort is a behavioral signal, not a strict token budget.

Mudança de effort no meio da conversa sem perder o cache (beta, literal): "On Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, and Claude Haiku 5.5, use a per-message effort change, which keeps the prompt cache." (beta header `mid-conversation-output-config-2026-07-01`). Recomendação para Opus 5.5 (literal): "Run an effort sweep on your own evals rather than carrying settings over from an earlier model".

A tabela de suporte de task budgets, a que a página principal remete ("check the support table"), fica na página `task-budgets`, que **não foi lida**.

Como se aplica a um harness de agente (Claude Code) com um context hub (arquivos Markdown compartilhados entre máquinas) e um canvas multiagente (Maestri): "low ... such as subagents" é a indicação oficial para agentes auxiliares de varredura; agentes de decisão e síntese ficam em `medium` ou `high`. Definir o nível por sessão (a mudança por mensagem só existe em certos modelos e em beta).

---

## 26. Não verificado

- **Citações parciais.** O WebFetch resume o conteúdo. Onde escrevi "resumo da ferramenta", o texto veio parafraseado e não foi conferido palavra por palavra: lista completa de itens que quebram o cache (exceto os trechos literais citados), a rejeição do keep-alive com thinking, structured outputs, forced tool choice ou `compaction`, os valores da DeepResearch Bench II com e sem cache ($37.94 para $7.12; $3.20 para $1.20) e o limiar "below about 80% cache reads". O 84,2% e o 91,7% estão literais no rodapé 17.
- **Trechos da página principal não lidos literalmente:** o gráfico de cache da seção 2, o benchmark do GitHub MCP (20%), a figura exata do caso "Fable 5 para Fable 5.1" e os detalhes de cada gráfico de advisor além das citações acima.
- **Tabela de batch** da página de pricing: li só as linhas de Fable, Mythos, Opus; não conferi as de Sonnet e Haiku.
- **Páginas ligadas não lidas:** task budgets (tabela de suporte), session budgets, models overview, Usage and Cost API, advisor tool, prompt caching. Limite de 3 buscas extras: usei pricing, effort e uma terceira busca na própria página principal.
- **Tudo sobre o Claude Code e o Maestri.** A página trata da API Messages e do Managed Agents. Não verificado: se o Claude Code liga o cache sozinho e com qual duração, se faz tool search, se deixa escolher o effort por subagente, se existe orçamento por tarefa, se injeta o tempo decorrido, se o Maestri tem advisor ou orquestração com custo contabilizado. As frases "Como se aplica..." marcadas como inferência são do autor, não da Anthropic.
- **Plano de assinatura vs. preço por token.** Não verificado se o uso do Gustavo no Claude Code é cobrado por token.
- **Medidas internas e direcionais.** A própria página avisa que são medidas da Anthropic, a preços da época, e que mudam; nenhuma foi reproduzida.
- **Janela de leitura.** A janela de offset 100000 trouxe exemplos de código em várias linguagens, a tabela-resumo e os rodapés de benchmarks; as seções de advisor, orquestrador e medição foram lidas na primeira janela por pedidos específicos.
