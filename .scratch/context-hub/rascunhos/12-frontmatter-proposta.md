# Frontmatter por tipo de nota, imposto por mecanismo (proposta para a rodada 18 do ticket 12)

Maestro, 2026-10-15, depois da rodada 17 ("detalhe mais e recomende um padrão para cada tipo possível de nota... você
está banalizando"; "de forma mecânica, para nenhum agente ficar livre para decidir").

## Princípios

1. **O tipo vem do caminho, não do agente.** `clients/x/y/runs/2026-10-15-coleta/relatorio.md` é `run`; quem grava não
   escolhe. Uma tabela `caminho → tipo` mora em `agents/frontmatter/paths.yml`.
2. **Cada tipo tem um esquema** (JSON Schema escrito em YAML) em `agents/frontmatter/<tipo>.yml`: campos obrigatórios,
   opcionais, valores aceitos. É a fonte única; o `AGENTS.md` só aponta para ela.
3. **O derivável a máquina preenche**: `type`, `initiative`, `title` do núcleo, `updated`, `archived_at`. O agente só
   escreve o que exige juízo (um `status`, uma `question`, um `outcome`).
4. **Campos em inglês, valores fechados onde há ciclo** (status com lista fixa), sem dado pessoal (organização, nunca
   nome ou e-mail de pessoa).

## Campos comuns (toda nota `.md` do hub, fora `AGENTS.md` e as skills)

| Campo | Obrigatório | Quem preenche | Para quê |
|---|---|---|---|
| `title` | sim | agente ou verificador (núcleo e índices) | a busca pesa 10× |
| `type` | sim | verificador, pelo caminho | filtro da busca; escolhe o esquema |
| `initiative` | sim dentro de uma iniciativa | verificador, pelo caminho | filtro por iniciativa sem depender da pasta |
| `created` | sim | quem cria (skill, modelo do Templater, verificador) | ordem e idade |
| `updated` | sim | verificador | o que mudou por último |
| `aliases` | não | agente | nomes alternativos (a busca pesa 5×) |
| `tags` | não | agente | assunto transversal |
| `related` | não | agente | links para notas ligadas |

## Por tipo (além dos comuns)

| Tipo | Onde | Campos próprios (obrigatórios em negrito) |
|---|---|---|
| `initiative` (ficha) | `initiative.md` | decidido nas rodadas 14 e 16: **`id`**, `aliases`, **`kind`**, **`size`**, **`status`**, **`blocks`**, `workspace`, `parent`, `related`, `cadence` |
| `retomada` | `retomada.md` | **`next_step`** (uma frase), `blocked_by`, `last_agent` (harness e modelo) |
| `tasks` | `tasks.md` | `open_count` (verificador conta) |
| `decisions` | `decisions.md` | `last_decision` (data, verificador) |
| `context` | `context.md` | `reviewed` (data da última conferência) |
| `log` | `log/AAAA-MM.md` | **`month`** (verificador) |
| `index` | `index.md` de qualquer pasta | **`folder`**, **`summary`** (`auto`: o verificador mantém a lista), **`local`** (true/false) |
| `attachment-text` | `<anexo>.md` ao lado do anexo | decidido na rodada 16: **`source`**, **`extractor`**; mais `extracted` (data) e `source_hash` |
| `input` | `inputs/` | **`origin`** (cliente, reunião, e-mail, sistema), **`received`**, `org` |
| `research` | `research/` | **`question`**, **`status`** (open, answered, dropped), `sources`, `verified` (yes, partial, no) |
| `design` | `design/` | **`status`** (draft, proposed, approved, superseded), `superseded_by`, `decision` (link) |
| `plan` | `plans/` | **`status`** (draft, active, done, dropped), `due`, `owner` (agente ou Gustavo) |
| `deliverable` | `deliverables/` | **`status`** (draft, review, delivered), **`audience`** (client, internal), `version`, `delivered` |
| `evidence` | `evidence/` | **`proves`** (o que demonstra, link), **`captured`**, `origin` |
| `tool` | `tools/` (o `README.md` de cada ferramenta) | **`language`**, **`run`** (como rodar), `repo` (quando vira repositório) |
| `run` | `runs/<execução>/` | **`started`**, **`outcome`** (ok, partial, failed), `ended`, `harness`, `model` |
| `work` | `work/` | **`work_kind`** (brief, handoff, state), **`status`** (open, closed), `agent` |
| `procedure` | `procedures/` | **`applies_to`**, `last_validated` |
| `case` | `cases/` | **`status`** (open, closed), **`opened`**, `closed`, `severity` |
| `query` | `queries/` | **`language`** (kql, sql, outro), **`target`** (o sistema), `last_run` |
| `knowledge` | `knowledge/` | **`topic`**, `verified` (yes, partial, no), `reviewed` |
| `note` | `notes/` | `topic`, `course` |
| `lab` | `labs/` | **`environment`**, **`status`** (active, torn-down) |
| `other` | `other/` | **`why_other`** (por que não cabe em nenhum bloco; o verificador avisa quando três parecidos pedem bloco novo) |
| `reference` | `reference/<assunto>/` | **`topic`**, `source`, `reviewed` |
| `inbox` | `inbox/` | só os comuns, e o verificador preenche; a captura é livre. Ao sair do `inbox/`, a nota passa a valer pelo esquema do destino |
| `machine` | `agents/machines/` | **`machine`**, **`os`**, `role` (par, cliente) |
| `archived` | `_archive/` | o esquema de origem, mais **`archived_at`** e `archive_reason` (o script do arquivo preenche) |

Sem frontmatter do hub: `AGENTS.md` (instrução lida pelos harnesses) e `SKILL.md` (frontmatter do padrão de skills:
`name`, `description`).

## Como a máquina impõe

| Onde a nota nasce ou muda | Mecanismo | Fonte |
|---|---|---|
| Agente grava no disco (Claude Code, Codex, Copilot) | hook antes da ferramenta: calcula o arquivo resultante, valida contra o esquema do caminho e **recusa** com a lista do que falta | Claude Code: `PreToolUse` com `permissionDecision: "deny"` (docs de hooks); Codex e Copilot: o mesmo hook já recusou gravação na bancada (ticket 11) |
| Agente grava pelo MCP do banco | o MCP valida e recusa do mesmo jeito | não verificado: entra na versão modificada do MCP |
| Fim de cada resposta | o verificador sem IA varre o que mudou, **preenche o derivável** e devolve o resto ao agente; a resposta não termina enquanto houver falta | Claude Code: `Stop` com `decision: "block"` faz o agente continuar (docs de hooks) |
| Você cria nota no Obsidian | modelo por pasta do Templater: a nota já nasce com o frontmatter do tipo | Templater, "Folder templates": "apply templates based on folder structure... the most specific (deepest) matching folder wins" |
| Você edita no Obsidian | o tipo de cada propriedade é um só no cofre todo, e o verificador da próxima resposta de agente confere | Obsidian, Properties: "Once a property type is assigned to a property name, all properties with that name across your vault will use the same type" |

## Onde a pasta declara "recebe `index.md`" e "fica local"

Recomendado: **o `index.md` é o cartão da pasta.** O frontmatter dele declara `summary: auto` (o verificador mantém a
lista) e `local: true|false` (o marcador da pasta local que você escolheu na rodada 17). O verificador **cria** o
`index.md` sozinho quando a pasta chega a 10 arquivos ou guarda arquivo que a busca não lê; para fazer uma pasta local,
cria-se o `index.md` com `local: true`, e um script gera a exclusão do sync e da busca a partir desses marcadores. Um
arquivo só por pasta, e a busca acha a descrição dela. **Não verificado:** gerar a exclusão do CLI do LiveSync e do
obsidian-hybrid-search a partir de marcadores.
