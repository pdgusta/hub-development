# Levantamento: como as iniciativas são hoje e o padrão ideal por tipo

Pedido do Gustavo em 2026-10-14, na carta "Núcleo e blocos da iniciativa" (ticket "Arquitetura de pastas e
frontmatter do hub"): olhar o que é de fato iniciativa no vault `ai-operating-system`, em `C:\Projetos` e em
`Documentos\Projetos`, e propor o padrão ideal por TIPO, "baseado em como já faço vs como seria ideal".

**Método.**
- Script de estrutura (`inventario.py`, no scratchpad da sessão): nomes das pastas até o segundo nível, arquivos do
  primeiro nível, contagem por extensão e marcadores (`AGENTS.md`, `CLAUDE.md`, `initiative.md`, `.git`,
  `.planning`…).
- Leitura do conteúdo, a pedido do Gustavo ("você vai precisar ler o conteúdo de algumas pra entender"):
  - o `initiatives/README.md` e o esquema `initiative-schema.md` do vault (a tentativa de padronizar);
  - o tamanho de cada seção dos 13 `initiative.md`, medido por script;
  - três `initiative.md` lidos por amostra: freellmapi-mcp inteiro, e o começo de Contexto, Decisões e
    Atualizações do soc-as-code.
- Nomes de pessoas que aparecem nos arquivos não foram copiados para cá.

## 1. O que é iniciativa, e o que não é

**Iniciativas (30):**

| Tipo de trabalho (proposto aqui) | Iniciativas |
|---|---|
| Projeto de cliente com entrega | TRF3 Intune; VOEGOL cross-tenant; VOEGOL migração de apps; VOEGOL grupos dinâmicos (`C:\Projetos\voegol`); ELEMENTIS M365 (vault e `Documentos\Projetos\ELEMENTIS`); Cloud PKI; relatório SOC da STRATA; gestão de vulnerabilidades da STRATA (`VulnManagement-PBIProject`) |
| Investigação | SBF |
| Operação contínua | SOC STRATA (`C:\Projetos\maestri\soc-context`, `Documentos\Projetos\incident-sops`, `soc-core`) |
| Produto ou ferramenta própria | soc-as-code; playbook de remediação de dispositivos; playbook de remediação de usuários; freellmapi-mcp; videos-transcriptor; agentic-os; os-shell-01; gerador de relatório (`report-generator-workspace`) |
| Frente de planejamento | context-hub (este repositório); o próprio vault como sistema; reverse-engineering |
| Spike ou laboratório | spike-fns; spike-livesync; bancada-busca; ContosoGD; Tests (Bicep) |
| Estudo | certifications-labs; Agent365-Training |
| Referência | `knowledge/armis-docs`, `knowledge/armis-brand`, `assets/` do vault; meta-prompting (biblioteca de prompts) |
| Criação de conteúdo | animations |

**Não são iniciativas:** `Temp`, `deep-seek-01` (vazia), `aos-wt1` e `ai-operating-system.worktrees` (cópias de
trabalho do vault), `benai-skills` e `deepseek-harness` (repositórios de terceiros), `freellmapi` (o gateway de
terceiros que roda aqui), `C:\Projetos\maestri` (casca de workspaces do Maestri; o conteúdo dela é do SOC STRATA e
da VOEGOL), `STRATA` e `Riachuelo` (só documentos soltos do cliente, sem trabalho em curso; a confirmar).

## 2. Como você faz hoje

**O vault tem um padrão, mas só na ficha.** Toda iniciativa tem um `initiative.md` com frontmatter (`type`,
`status`, `model`, `workspace`) e sete seções (Estado, Pendências, Descrição, Contexto, Decisões, Fontes,
Atualizações). O `type` do vault mede **tamanho** (mudança, iniciativa, projeto, estudo, ideia), não o **jeito do
trabalho**, então não diz nada sobre as subpastas. Abaixo da ficha, cada iniciativa improvisou.

**As mesmas coisas, com nomes diferentes:**

| O que é | Nomes usados hoje | Onde |
|---|---|---|
| O que veio de fora (kickoff, PDF do cliente, e-mails, exports) | `context/`, `comunicacao/`, `sources/`, `CSVs/input/` | 9 iniciativas |
| Levantamento e análise | `research/`, `pesquisa/`, `levantamento/`, `discovery/`, `analysis/`, `perfil-consolidado/` | 7 |
| Desenho e especificação | `design/`, `strategy/`, `docs/adr/`, `architecture*.md` soltos | 7 |
| Planos e tarefas | `plans/`, `.planning/` (GSD), `backlog/`, `.scratch/issues/` | 8 |
| Entregáveis | `deliverables/`, `entregaveis/`, `documentos/`, `repasse/`, `outputs/`, `presentation/`, `.docx` soltos na raiz | 9 |
| Evidência (prints, logs, exports de prova) | `prints/`, `levantamento/prints-intune/`, `piloto-autopilot/prints/` | TRF3 (496 PNG), VOEGOL cross-tenant (286 PNG) |
| Trabalho de agentes (briefs, handoffs, execuções, revisões) | `operacao/`, `handoffs/`, `revisao/`, `.gsd/`, `.claude/agents/` | TRF3, VOEGOL cross-tenant, SBF, soc-as-code |
| Scripts de apoio | `tools/`, `Scripts/`, `operacao/scripts/`, `_scripts/` | SBF, TRF3, ELEMENTIS, VOEGOL, incident-sops |
| Operação | `Procedures/`, `Incidents/`, `cases/`, `Queries/`, `queries/`, `kb/`, `Remediations/`, `ClosureTemplates/` | SOC STRATA (três lugares) |

**Problemas que a estrutura de hoje mostra:**
1. **Um assunto, vários nomes, duas línguas.** O agente não sabe onde procurar; a busca acha, mas gravar no lugar
   certo depende de adivinhar.
2. **A ficha virou diário.** O `initiative.md` junta ficha, retomada e histórico; na TRF3, a seção Estado é um
   parágrafo de vários milhares de caracteres. A ficha estável, o "onde parei" e o histórico mudam em ritmos
   diferentes.
3. **O SOC STRATA está em três lugares** (`soc-context`, `incident-sops`, `soc-core`), sem um dono.
4. **Código dentro e fora de git, misturado com notas.** Os `Scripts/` da VOEGOL não estão em git; o SBF tem
   `tools/` e um servidor de apresentação dentro do vault.
5. **Segredos soltos.** `credenciais.txt`, `token-*.txt` e `.env` nas pastas de spike.
6. **Contexto de agente por iniciativa já existe, mas espalhado:** `CLAUDE.md` próprio em ELEMENTIS, incident-sops,
   VulnManagement e os-shell; `AGENTS.md` aqui no context-hub.
7. **Evidência em volume** (centenas de PNG) misturada com o levantamento.

## 2b. O `initiative.md` por dentro: o padrão existe, o arquivo único é que não aguenta

O esquema do vault padroniza bem. A ficha tem frontmatter (`id`, `type`, `status`, `model`, `parent`, `related`,
`cadence`, `workspace`, `updated_at`), seguido de sete seções em ordem fixa: Estado (próxima ação e bloqueios),
Pendências, Descrição, Contexto, Decisões (uma linha datada com escolha e motivo), Fontes e Atualizações (diário
por data, mais novo primeiro). O próprio esquema previa separar um `state.md` "quando o diário dificultar a
leitura", e isso nunca aconteceu.

Tamanho medido de cada `initiative.md`, em milhares de caracteres:

| Iniciativa | Total | Pendências | Contexto | Decisões | Atualizações |
|---|---|---|---|---|---|
| VOEGOL cross-tenant | 337 | 89 (162 itens) | 87 | 67 (149) | 88 (219) |
| soc-as-code | 190 | 24 (72) | 15 | 48 (81) | 89 (226) |
| TRF3 Intune | 181 | 30 (76) | 23 | 12 (32) | 87 (164) |
| device-remediation | 58 | 13 (60) | 3 | 11 (26) | 25 (87) |
| strata-soc-report | 41 | 6 (47) | 10 | 3 (14) | 19 (65) |
| ELEMENTIS | 40 | 8 (23) | 5 | 1 (4) | 19 (54) |
| as outras sete | 2 a 32 | | | | |

O que a leitura mostra:
- **Cada seção tem um ritmo próprio**, e o arquivo único mistura os quatro:
  - a ficha e a descrição quase não mudam;
  - o Estado é sobrescrito;
  - Pendências e Decisões crescem item a item;
  - as Atualizações crescem todo dia e são a maior parte de tudo.
- **O Contexto virou um segundo diário:** fatos com data e esclarecimentos ("em 2026-09-16, o proprietário
  questionou…"), em vez de fatos estáveis.
- **Decisões viraram parágrafos** com o motivo, a fala do proprietário e o que não foi aceito, longe da linha
  "data, escolha, motivo" do esquema.
- **Um agente que só quer o "onde parei"** lê até 337 mil caracteres, ou depende de a busca acertar o trecho.
- Por isso, juntar tudo isso num `AGENTS.md` seria inviável: o `AGENTS.md` é lido inteiro em toda sessão, e a
  regra das portas de entrada é uma cabeça de até 2.000 caracteres.

**O ideal: o mesmo padrão de sete seções, cada uma no seu arquivo e com a sua regra de vida.**

| Hoje, seção do `initiative.md` | Ideal | Regra de vida |
|---|---|---|
| frontmatter, Descrição, Fontes | `initiative.md` (a ficha, curta) | quase não muda |
| Estado | `retomada.md` | sobrescrito a cada sessão (o contrato de retomada) |
| Pendências | `tasks.md` | só o que está aberto; o que fecha vai para o diário |
| Decisões | `decisions.md`: uma linha por decisão, com link para o detalhe quando houver | só cresce, uma linha por vez |
| Contexto | `context.md` | fatos estáveis, reescritos quando mudam; o que tem data vai para o diário |
| Atualizações | `log/AAAA-MM.md`, um arquivo por mês | só cresce, sem um arquivo gigante |

O `AGENTS.md` da iniciativa, quando existir, fica pequeno: o mapa (onde está cada um desses arquivos e os blocos
em uso) e as regras de trabalho próprias daquela iniciativa. Ele aponta para o conteúdo, sem guardá-lo.

## 3. O ideal: blocos que se empilham

Cada linha da tabela de nomes vira **um bloco** com um nome só (em inglês, como as raízes). Uma iniciativa é o
núcleo mais os blocos que usa, e um bloco entra quando o trabalho pede.

| Bloco | Pasta | Substitui |
|---|---|---|
| Entrada | `inputs/` | `context/`, `comunicacao/`, `sources/` |
| Pesquisa | `research/` | `pesquisa/`, `levantamento/`, `discovery/`, `analysis/` |
| Desenho | `design/` (o detalhe das decisões grandes, ligado do `decisions.md`) | `strategy/`, `perfil-consolidado/`, ADRs |
| Planejamento | `plans/` (planos e tickets; as pendências simples ficam no `tasks.md`) | `.planning/`, `backlog/`, `.scratch/` |
| Entregas | `deliverables/` | `entregaveis/`, `documentos/`, `repasse/`, `outputs/` |
| Evidência | `evidence/` | `prints/` |
| Trabalho de agentes | `runs/` (briefs, handoffs, execuções, revisões) | `operacao/`, `handoffs/`, `revisao/` |
| Ferramentas | `tools/` ou `code.md` com o link do repositório | `Scripts/`, `_scripts/` |
| Operação | `procedures/`, `cases/`, `queries/` | `Procedures/`, `Incidents/`, `Queries/` |
| Conhecimento | `knowledge/` | `kb/` |
| Estudo | `notes/`, `labs/` | — |

**Núcleo (em toda iniciativa):** os arquivos da seção 2b, que são o padrão de sete seções do vault separado por
ritmo: `initiative.md`, `retomada.md`, `tasks.md`, `decisions.md`, `context.md` e `log/`. O `AGENTS.md` da
iniciativa é só o mapa e as regras próprias.

**O padrão ideal por tipo (a pilha sugerida ao criar):**

| Tipo | Pilha ideal | Exemplo real |
|---|---|---|
| Projeto de cliente com entrega | Entrada + Pesquisa + Desenho + Entregas + Evidência (+ Trabalho de agentes e Ferramentas quando cresce) | TRF3 já usa quase todos, com outros nomes |
| Investigação | Entrada + Pesquisa + Ferramentas + Evidência + Entregas | SBF |
| Operação contínua | Operação + Conhecimento + Planejamento (o backlog de melhorias) | SOC STRATA, juntando os três lugares |
| Produto ou ferramenta própria | Desenho + Planejamento + Pesquisa + `code.md` | soc-as-code, freellmapi-mcp |
| Frente de planejamento | Planejamento + Desenho + Pesquisa + `GLOSSARY.md` | este repositório |
| Spike ou laboratório | Pesquisa (hipótese e resultado) + Ferramentas, sem segredos | spike-livesync, bancada-busca |
| Estudo | Estudo + Entrada (o material do curso) | certifications-labs |
| Referência | nenhum bloco: o conteúdo é a pasta | armis-docs, armis-brand |
| Criação de conteúdo | Desenho (roteiro) + Entregas + Evidência (os quadros) | animations |

## 4. Em aberto, para as rodadas

- Os nomes de cada bloco e o que vai dentro deles.
- Scripts pequenos de uma iniciativa: ficam em `tools/` no hub ou vão sempre para um repositório próprio, como manda
  a decisão "repositório fora do hub por link"?
- Onde ficam os segredos dos spikes (nunca no hub, que replica).
- O SOC STRATA: uma iniciativa só em `operations/`, com o que hoje está em três pastas.
- O que vira `runs/` frente à pasta `maestro/` já decidida (personalização do Maestri por iniciativa).
