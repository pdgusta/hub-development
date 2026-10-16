---
titulo: O padrão de frontmatter de cada tipo de nota, e como a máquina o impõe
ticket: 12
aberta: 2026-10-15
estado: absorvida
---

Você pediu um padrão de frontmatter para cada tipo possível de nota, imposto de forma mecânica, sem depender de regra
no `AGENTS.md`, e onde a pasta declara que recebe `index.md`. A proposta inteira está em
`rascunhos/12-frontmatter-proposta.md`; o essencial vai aqui.

**Quatro princípios:** o tipo vem do caminho da nota (uma tabela `caminho → tipo` em `agents/frontmatter/paths.yml`),
não da escolha do agente; cada tipo tem um esquema em `agents/frontmatter/<tipo>.yml`, a fonte única; o que dá para
derivar a máquina preenche (`type`, `initiative`, `updated`, o `title` do núcleo e dos índices); campos em inglês,
valores fechados onde há ciclo, sem dado pessoal.

**Campos comuns** (toda nota `.md` do hub, fora `AGENTS.md` e as skills)

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

**Por tipo, além dos comuns** (obrigatórios em negrito)

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

**Como a máquina impõe**

| Onde a nota nasce ou muda | Mecanismo | Fonte |
|---|---|---|
| Agente grava no disco (Claude Code, Codex, Copilot) | hook antes da ferramenta: calcula o arquivo resultante, valida contra o esquema do caminho e **recusa** com a lista do que falta | Claude Code: `PreToolUse` com `permissionDecision: "deny"` (docs de hooks); Codex e Copilot: o mesmo hook já recusou gravação na bancada (ticket 11) |
| Agente grava pelo MCP do banco | o MCP valida e recusa do mesmo jeito | não verificado: entra na versão modificada do MCP |
| Fim de cada resposta | o verificador sem IA varre o que mudou, **preenche o derivável** e devolve o resto ao agente; a resposta não termina enquanto houver falta | Claude Code: `Stop` com `decision: "block"` faz o agente continuar (docs de hooks) |
| Você cria nota no Obsidian | modelo por pasta do Templater: a nota já nasce com o frontmatter do tipo | Templater, "Folder templates": "apply templates based on folder structure... the most specific (deepest) matching folder wins" |
| Você edita no Obsidian | o tipo de cada propriedade é um só no cofre todo, e o verificador da próxima resposta de agente confere | Obsidian, Properties: "Once a property type is assigned to a property name, all properties with that name across your vault will use the same type" |

**Não verificado, para a construção:** o hook calcular o arquivo resultante de uma troca de trecho antes de gravar; o
`Stop` que segura a resposta no Codex e no Copilot; a validação dentro do MCP do banco; gerar a exclusão do sync e da busca
a partir dos marcadores de pasta.

## O padrão de cada tipo de nota
id: padrao-por-tipo
tipo: escolha
recomendada: A

- A: O catálogo acima: campos comuns em toda nota e campos próprios por tipo, com os obrigatórios marcados e valores fechados onde há ciclo. Ajustes de campo você diz em "Algo mais?"
- B: O catálogo acima, mas só com os obrigatórios; os opcionais saem e entram quando o uso pedir
- C: O catálogo acima, e mais um campo comum `status` em toda nota (rascunho, em uso, superada), para filtrar o que está vigente em qualquer pasta

## Como a máquina impõe o padrão
id: imposicao
tipo: escolha
recomendada: A

- A: Em camadas: hook antes da gravação no disco recusa nota fora do esquema (Claude Code, Codex, Copilot); o MCP do banco recusa do mesmo jeito; o verificador no fim de cada resposta preenche o derivável e devolve o resto ao agente, que não encerra a resposta enquanto faltar; no Obsidian, o modelo por pasta do Templater faz a nota nascer com o frontmatter do tipo
- B: Só o verificador no fim de cada resposta (preenche e devolve ao agente), sem hook antes da gravação: menos construção, mas a nota fora do padrão chega a existir no disco até o fim da resposta
- C: Como a A, sem o Templater: notas suas no Obsidian nascem sem frontmatter e o verificador da próxima resposta de agente completa

## Onde a pasta declara que recebe `index.md` e que é local
id: cartao-da-pasta
tipo: escolha
recomendada: A

- A: O `index.md` é o cartão da pasta: o frontmatter dele declara `summary: auto` (o verificador mantém a lista) e `local: true` ou `false` (o marcador da pasta local). O verificador cria o `index.md` sozinho quando a pasta chega a 10 arquivos ou guarda arquivo que a busca não lê; para tornar uma pasta local, cria-se o `index.md` com `local: true`. Um arquivo só por pasta, e a busca acha a descrição dela
- B: Um arquivo marcador separado em cada pasta que precisa (`_pasta.yml`, fora da busca), com `index` e `local`; o `index.md` fica só como sumário
- C: Uma lista central em `agents/frontmatter/pastas.yml` com as pastas que recebem `index.md` e as locais; nada dentro da pasta

## Algo mais?
id: algo-mais
tipo: texto
