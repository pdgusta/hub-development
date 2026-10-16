---
titulo: Núcleo e blocos, a partir de como você já trabalha
ticket: 12
aberta: 2026-10-14
estado: absorvida
carta: prototipo-12-ritmos
---

Esta rodada substitui a anterior ("O núcleo e os modelos da pasta de uma iniciativa", suspensa). Ela parte do
levantamento que você pediu: 30 iniciativas no vault, em `C:\Projetos` e em `Documentos\Projetos`. O levantamento
completo está em `exploracao/anexos/levantamento-12-iniciativas.md`.

**O que o levantamento achou:**
- **O `initiative.md` do vault já é um padrão bom:** frontmatter e sete seções (Estado, Pendências, Descrição,
  Contexto, Decisões, Fontes, Atualizações).
- **O arquivo único não aguenta.** O da VOEGOL cross-tenant tem 337 mil caracteres, o soc-as-code tem 190 mil e o
  TRF3 tem 181 mil. A maior parte é diário (Atualizações), pendências e decisões. O próprio esquema previa separar
  um arquivo de estado, e isso nunca aconteceu.
- **Abaixo da ficha, os mesmos assuntos aparecem com nomes diferentes:**
  - o que veio do cliente: `context/`, `comunicacao/`, `sources/`;
  - a pesquisa: `research/`, `pesquisa/`, `levantamento/`, `discovery/`, `analysis/`;
  - as entregas: `deliverables/`, `entregaveis/`, `documentos/`, `repasse/`, `outputs/`.

## O núcleo de toda iniciativa
id: nucleo
tipo: escolha
recomendada: A

- A: As sete seções de hoje, cada uma no seu arquivo: `initiative.md` (ficha, descrição, fontes), `retomada.md` (o Estado, sobrescrito), `tasks.md` (só pendências abertas), `decisions.md` (uma linha por decisão), `context.md` (só fatos estáveis) e `log/AAAA-MM.md` (o diário, um arquivo por mês)
- B: O `initiative.md` como hoje, com tudo, e só o Estado à parte, em `retomada.md`
- C: `initiative.md` (ficha, descrição, contexto, fontes, pendências e decisões) + `retomada.md` + `log/AAAA-MM.md`

Nas três opções, o `AGENTS.md` da iniciativa é **só um mapa** (onde está cada arquivo e quais blocos ela usa) com
as regras próprias dela, e nunca guarda o conteúdo.

Por que A: cada seção muda num ritmo. A ficha quase não muda, o estado é sobrescrito, as pendências fecham, as
decisões e o diário só crescem. Separadas, nenhuma vira um arquivo de 300 mil caracteres. O agente que quer "onde
parei" lê só o `retomada.md`, e quem quer as decisões lê só o `decisions.md`. A B mantém o problema de hoje; a C
alivia, mas pendências e decisões ainda incham a ficha.

## Como o resto da pasta se monta
id: blocos
tipo: escolha
recomendada: B

- A: Um modelo pronto por tipo de trabalho, escolhido ao criar a pasta
- B: Blocos com um nome só, somados conforme o trabalho pede: `inputs/` (o que veio de fora), `research/`, `design/`, `plans/`, `deliverables/`, `evidence/` (prints e logs de prova), `runs/` (briefs, handoffs e revisões de agentes), `tools/` (scripts de apoio), operação (`procedures/`, `cases/`, `queries/`), `knowledge/`, estudo (`notes/`, `labs/`)
- C: Só o núcleo; cada iniciativa cria as subpastas quando precisar

Na opção B, cada tipo de trabalho ganha uma **pilha sugerida** ao criar a pasta, que se pode mudar depois:

| Tipo | Pilha sugerida | Exemplo real |
|---|---|---|
| Projeto de cliente | `inputs/` + `research/` + `design/` + `deliverables/` + `evidence/` | TRF3, VOEGOL cross-tenant |
| Investigação | `inputs/` + `research/` + `tools/` + `evidence/` + `deliverables/` | SBF |
| Operação contínua | `procedures/` + `cases/` + `queries/` + `knowledge/` + `plans/` | SOC STRATA (hoje em três pastas) |
| Produto ou ferramenta própria | `design/` + `plans/` + `research/` + link do repositório | soc-as-code, freellmapi-mcp |
| Frente de planejamento | `plans/` + `design/` + `research/` + glossário | context-hub |
| Spike ou laboratório | `research/` + `tools/`, sem senhas | spike-livesync, bancada-busca |
| Estudo | `notes/` + `labs/` + `inputs/` | certifications-labs |
| Referência | nenhum bloco | armis-docs, armis-brand |

Quando a iniciativa cresce, ganha bloco: o TRF3 de hoje somaria `runs/` (os agentes) e `tools/` (os scripts). Os
nomes estão em inglês, como as raízes do hub.

Por que B: os seus projetos já usam esses blocos, só que cada um com um nome. Um modelo por tipo (A) não cobre
quem mistura, como o SOC STRATA, que é operação com base de conhecimento e backlog.

## Algo mais?
id: algo-mais
tipo: texto

Ficam para rodadas próprias: os scripts pequenos (`tools/` no hub ou sempre num repositório próprio), as senhas dos
spikes e juntar as três pastas do SOC STRATA numa só.
