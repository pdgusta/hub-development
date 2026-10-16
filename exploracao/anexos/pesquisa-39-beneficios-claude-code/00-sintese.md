---
title: Síntese — benefícios técnicos do Claude Code com o context hub e o Maestri
data: 2026-10-10
origem: Claude Fable 5.1 (orquestrador), ticket 39, a partir dos relatórios 01 a 05 desta pasta
aviso: saída de modelo. Esta síntese só junta o que os relatórios citam de fonte primária; cada afirmação aponta o relatório e a seção. O que é inferência está marcado como tal, e o que nenhum relatório confirmou está em "Não verificado". Os números são medidas internas da Anthropic, direcionais, a preços de outubro de 2026.
---

# Síntese

## 1. A tese em uma frase

Um agente paga duas vezes pelo que não lembra: paga em qualidade, porque recomeça do zero a cada sessão, e paga
em tokens, porque reenvia a conversa inteira a cada turno. O context hub ataca a primeira conta (o que importa
fica em arquivo, no lugar certo, nas duas máquinas); as alavancas da página da Anthropic atacam a segunda; o
Claude Code é onde as duas se encontram; e o Maestri é onde a estratégia de "orquestrador e trabalhadores" vira
prática, com vários terminais no mesmo canvas.

## 2. As três peças (o que cada uma é, com fonte)

- **Claude Code** começa toda sessão com contexto vazio e lê instruções persistentes de `CLAUDE.md`, ou dos
  `AGENTS.md` do repositório quando não há `CLAUDE.md` (02 §1; 02b §1). Carrega skills sob demanda (02 §4),
  obedece hooks em eventos como `Stop` e `SessionStart` (02 §3; 02b §8), delega a subagentes com modelo e
  ferramentas próprios (02 §5), e usa prompt caching automaticamente, por máquina e diretório (02 §9).
- **Context hub**: "a casa única do contexto, com uma cópia completa em cada máquina. A verdade mora num banco,
  que o agente lê e grava; o Gustavo vê o hub pela vista Markdown" (04 §2). Cinco critérios: achar o trecho certo
  sem ler tudo, gravar sem pedir, editar como sempre, nada divergir em silêncio, proteger a edição concorrente
  (04 §1). Decisões fechadas: nota de retomada obrigada por hook `Stop` (04 §4, ticket 10); CouchDB + LiveSync, um
  por par, replicando pela tailnet, clientes só de leitura (ticket 25 e 34); seis raízes; `AGENTS.md` na raiz.
- **Maestri**: "a spatial development workspace that connects AI agents, terminals, notes, and browser portals on
  a visual canvas" (03 §1). Um agente fala com outros por `maestri ask`, em paralelo por `ask --batch`, lê o
  terminal alheio com `check`, divide estado por notas e fichários, agenda rotinas e cria workspaces e floors
  (03 §2 e §3).

## 3. Cada alavanca da Anthropic, e onde ela cai neste conjunto

Ordem da própria página ("in the order to try them", 01 §23). Para cada uma: o que a página diz, o que o Claude
Code expõe, e o que o hub ou o Maestri ganham.

| # | Alavanca (01) | O que a página mede | No Claude Code (02, 02b) | No hub / no Maestri |
|---|---|---|---|---|
| 1 | Prompt caching (01 §2–6) | custo cai 2,7x a 5,3x em loops de agente; leitura a 0,1x (0,05x em Opus 5.5 e Sonnet 5.5; 0,025x em Fable 5.1) | automático; cache por máquina e diretório; três camadas (system, project context, conversation); trocar modelo, fast mode ou ferramentas invalida; editar CLAUDE.md no meio da sessão não vale até `/clear` (02 §9) | hub: `AGENTS.md` curto e estável no prefixo, o que muda vai para o fim ou para arquivo lido sob demanda (inferência, 01 §5). Maestri: terminais no **mesmo diretório** leem o cache uns dos outros; worktrees não (02 §9) |
| 2 | Duração do cache (01 §3) | 1 h compensa com pausas de 5 min a 1 h; Fable 5.1 prefere manter o de 5 min aquecido | 1 h só em assinatura dentro do plano; subagentes ficam em 5 min; `CLAUDE_CODE_PROMPT_CACHE_TTL` (02 §9) | o uso do Gustavo é "a person waits between turns" (01 §3) |
| 3 | Trimming: tool search (01 §7) | 45% com 500 ferramentas; 20% com um MCP do GitHub | definições de MCP adiadas por padrão (02 §6) | muitos conectores ligados = custo; adiar ou restringir por subagente (`mcpServers`) |
| 4 | Dados em arquivo, não no prompt (01 §8) | 25 de 25 certas a um doze avos do custo | o agente lê arquivos por trecho; a camada de busca do hub devolve só a seção (04 §2) | é o critério 1 do hub: "achar o trecho certo sem ler tudo" |
| 5 | Ciclo de vida do contexto (01 §9) | poda nas fronteiras de tarefa: 39%; compactação: 32%; nada em sessão curta | `/clear`, `/compact` com foco, auto-compact, `/context`; o CLAUDE.md é recarregado depois da compactação (02 §10; 02b §6) | o contrato file-first é a poda feita por mecanismo: grava a nota de retomada (hook `Stop`), depois `/clear` (04 §4) |
| 6 | Respostas curtas (01 §10) | 39% menos tokens de saída, 14% do custo | subagentes devolvem resumo; o relatório fica em arquivo (02 §5) | regra de handoff entre agentes do canvas |
| 7 | Batch API (01 §11) | 50% em tudo, até 24 h | não se aplica a sessões interativas | só para varreduras em lote por API direta |
| 8 | Auditoria de prompts (01 §12) | 14% nas duas migrações; "verify twice" custava um terço | CLAUDE.md abaixo de 200 linhas; instruções especializadas em skills (02 §11) | `AGENTS.md`, skills e memórias são prompts: rever a cada troca de modelo |
| 9 | Custo por tarefa, não por token (01 §13) | Opus 5.5 `medium` empata com Fable 5.1 padrão a um quinto do custo ($0.22 contra $1.19) | `/usage` mostra custo e cache; `claude -p` devolve `total_cost_usd` (02 §8, §11) | registrar custo e resultado por tarefa no hub quando o Gustavo pedir medição |
| 10 | Upgrade do modelo (01 §14) | $183 → $63 → $28 por tarefa resolvida na escada Opus; tokenizador novo gera 30% mais tokens | aliases `haiku`, `sonnet`, `opus`, `opusplan`; `/model`, `--model`, `ANTHROPIC_MODEL`, settings (02 §12) | mesmo tier, modelo mais novo, prompts revisados junto |
| 11 | Effort (01 §15, §25) | curva quase plana em pesquisa; `low` recomendado para subagentes; padrões: `high`, exceto Opus 5.5 e Haiku 5.5 em `medium` | `/effort`, `--effort`, `effortLevel`; nos modelos 5.5 e Fable 5.1 trocar effort mantém o cache (02 §13) | busca e indexação em `low`; decisão de desenho em `high`; por terminal no Maestri |
| 12 | Refazer falhas em effort maior (01 §16) | 97% por $0.17 contra 95,3% por $0.29 | precisa de sinal de falha: testes, checagem de links e formato | só onde há verificação objetiva; não em pesquisa ou decisão |
| 13 | Orçamentos e tetos (01 §17) | task budget 44–58%; `max_tokens` 64k; session budget; limite do workspace | `--max-budget-usd` no headless; `/usage` (02 §8, §11) | agente do canvas que não termina é a "cauda de custo" |
| 14 | Tempo decorrido (01 §18) | 47% menos tempo e 60% menos custo em DRACO, com 4,1 pontos a menos | não verificado se o harness injeta | só em varreduras onde velocidade vale mais que nota; não por padrão em pesquisa |
| 15 | Advisor (01 §19) | só compensa se o executor consulta; Haiku e Sonnet não consultaram em 198 perguntas | `opusplan`; ferramenta advisor (02 §12) | medir a taxa de consulta antes de confiar |
| 16 | Orquestrador (01 §20–21) | cerca de metade do custo do modelo de fronteira, 10 a 12 pontos abaixo, só com volume independente | sessão principal + subagentes; `claude -p` por trabalhador (02 §5, §8) | **é o padrão do Maestri**: um terminal planeja, vários executam, `ask --batch`, notas como estado (03 §3). A pergunta-chave: "o trabalho se divide em pedaços independentes?" |
| 17 | Medir na própria carga (01 §22) | método de 4 passos | `/usage`, `total_cost_usd` | só a pedido do Gustavo |

## 4. Os benefícios, enunciados

1. **Mesmo contrato em qualquer máquina e harness.** `AGENTS.md` na raiz do hub é lido pelo Claude Code sem
   configuração fora da pasta (02 §1; 02b §1); cada terminal do Maestri que abre o hub herda o mesmo contrato.
2. **Memória que sobrevive à sessão por mecanismo, não por regra.** O hook `Stop` pode bloquear o fim da resposta
   até a nota de retomada estar gravada (02b §8; ticket 10). O `/clear` deixa de custar informação.
3. **Prefixo estável, cache quente.** O desenho "AGENTS.md curto + busca sob demanda + o que muda no fim" é o
   mesmo que a página de custos recomenda (02 §11) e o que o cache exige (01 §5).
4. **Trecho certo, não arquivo inteiro.** Critério 1 do hub e a alavanca "dados em arquivo" da Anthropic são a
   mesma ideia (01 §8; 04 §1).
5. **Modelo e effort por papel.** Subagentes em `haiku` e `low` para varrer; `opus` ou Fable para decidir; cada
   terminal do Maestri sobe com `--model` e `--effort` próprios (02 §12–13; 01 §25).
6. **Orquestração que compensa onde a página diz que compensa.** Fan-out de pesquisa por fonte, por cliente ou
   por cena (como a pesquisa deste próprio ticket: sete agentes, três modelos) é "volume independente"; grill,
   spec e tickets são cadeia dependente e ficam num modelo só (01 §21).
7. **Custo visível.** `/usage`, `total_cost_usd` e `--max-budget-usd` dão o que a página chama de "measure on
   your own workload" (02 §8, §11; 01 §22).

## 5. Linguagem visual do vídeo (05, três relatórios)

Fundo único quase preto (#0D1117 ou #111), sem textura; paleta curta e semântica: branco para traço e texto,
verde para verificado e ênfase, âmbar para dúvida e número, vermelho só para falha, azul para cache e técnica;
rótulo de seção em mono, caixa-alta pequena, canto superior esquerdo; uma frase-síntese curta por seção, branca
com o final colorido; sem legenda da narração contínua, só texto diegético de 1 a 6 palavras; mockups vetoriais
(terminal, cartão, nota) em vez de gravação; personagens simples (agente com antena, humano de palitos);
números grandes em mono que mudam no lugar; carimbos inclinados para veredictos; dentro da seção, os elementos
se acumulam e trocam por fade; entre seções, corte para o fundo vazio e reconstrução em camadas; 2 a 5 s por
estado, 15 a 40 s por seção; abrir e fechar com a mesma imagem, mudada.

## 6. Não verificado (o que os relatórios não fecharam)

- Se o Maestri abre cada terminal no diretório do hub e como passa `--model` e `--effort` (02 §1, §12–13).
- Se os terminais do Maestri contam como "agent teams" (cerca de 7x mais tokens) ou como sessões separadas (02 §11).
- A tabela de suporte de task budgets e se o Claude Code expõe orçamento por tarefa (01 §17, §26).
- Se o Claude Code injeta tempo decorrido (01 §18).
- Tudo que o WebFetch devolveu resumido e não literal (01 §26; 02b "Não verificado").
- Nada foi testado ou medido nesta pesquisa; os números são da Anthropic.
