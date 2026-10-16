# Ticket 12: o que falta e rascunho do Answer

Rascunho para o maestro conferir. Base: ticket 12 (Question e comentários até a rodada 16, respondida em 2026-10-15
16:18, envio `d6f47073-e2be-4f3a-9823-23b19bac4350`), arquivos das rodadas e respostas em `portal/`, `map.md`,
`GLOSSARY.md` e os Answers de 02, 09, 10, 33, 36 e 40. Nada foi editado fora deste arquivo.

## 1. O que ainda está aberto

Critério: conta como decidido só o que tem resposta do Gustavo ou rodada absorvida, aqui ou em ticket resolvido.

### 1a. Pontos sem decisão

| # | Onde no ticket | O que falta | Bloqueia resolver? |
|---|---|---|---|
| 1 | Question, linhas 9-10: "como uma pasta se declara **pasta não replicada** (Q15)" | A substância está decidida: tudo replica, inclusive o conteúdo de cliente (rodada 3), e o perfil de máquina vira um arquivo por máquina "sem pasta não replicada" (rodada 6, "ok"). Mas **como uma pasta se declararia** nunca foi perguntado. Hoje o que fica numa máquina só fica pelo ponto no nome (`.secrets/`, `.maestri/`, `.git`), regra decidida em outros tickets ("Revisão do sync e da divergência": vai ao banco tudo "fora pastas com ponto"; "Maestri: padrão e liberdade": "nada com ponto, que não replica"). O glossário ainda diz "Cada pasta declara se é replicada" e "alcançada pela outra máquina por SSH", o que não bate com a árvore. | **Sim, leve.** É parte explícita da Question. Fecha com um ok do Gustavo para a redação do Answer ("não há pasta não replicada; o que fica numa máquina só leva ponto no nome") e talvez um ajuste no termo do glossário (fora deste rascunho). |
| 2 | Question, linha 9: "que frontmatter o hub usa"; rodada 16, apoio "o frontmatter só leva o que a busca ou o contrato usam" | Decidido o frontmatter da ficha (rodadas 14 e 16), do núcleo (`title`, rodada 16) e do texto dos anexos (rodada 16). **Não decidido o das demais notas** (as dos blocos, o `AGENTS.md` da iniciativa e os `index.md`). Só está decidido que o verificador avisa YAML inválido (rodada 16, B herda da A). Achado: com a B da rodada 16, haverá muitos `index.md` e, sem `title`, todos se chamam "index" na busca, o mesmo problema que a rodada 16 resolveu para os 30 `retomada.md`. | **Sim, leve.** Fecha com um ok para "frontmatter livre nas demais notas, só YAML válido" (ou com o `title` dos `index.md` completado pelo verificador). |
| 3 | Question, linha 10 ("O protótipo é um esboço da árvore com notas de exemplo"); `Type: prototype` | Não existe um esboço da árvore final. As cartas cobrem partes: `prototipo-12-ritmos` (núcleo e blocos, **aprovada**, envio `971570e7…`) e `prototipo-12-sumario` (rodada 12, cuja escolha de órfãos foi depois substituída). Nenhuma mostra ficha com `aliases`, `work/`, `.secrets/`, `index.md` da B nem o arquivo irmão dos anexos. Pelo próprio Gustavo, "nem toda rodada precisa de carta" (rodada 12). | **Decisão do Gustavo:** aceitar as cartas como o protótipo (não bloqueia) ou pedir ao Designer o esboço final antes de resolver. A atualização do `system-design.html` já está prevista ao resolver. |
| 4 | Rodada 6 (linha 79): "o nível do cliente guardando o que é comum às iniciativas dele" | O que mora em `clients/<cliente>/` fora das pastas das iniciativas (um `AGENTS.md` do cliente? ficha? `inputs/` comum?) não foi decidido. | Não. Vai para a construção como ponto a decidir na skill "nova iniciativa". |
| 5 | Rodada 11 (núcleo "em toda iniciativa") e rodada 14 (`kind` inclui "operação contínua" e "referência") | Não foi dito com todas as letras que `operations/<operação>/` e `reference/<assunto>/` levam o núcleo de seis arquivos. O levantamento sugere para referência "nenhum bloco: o conteúdo é a pasta", sem dizer se leva o núcleo. | Não, se o Answer registrar a leitura "o núcleo vale em `operations/` e `initiatives/`; em `reference/` fica a confirmar". Recomendo uma linha de ok junto dos itens 1 e 2. |
| 6 | Comentário 2026-10-04 (vindo do "Contrato file-first") e rodada 11 | A nota de retomada da iniciativa é o `retomada.md` (decidido). Sem lugar decidido: a retomada de trabalho que **não é de uma iniciativa** (sessão na raiz, o que cruza iniciativas, trabalho em `agents/`). | Não. Para a construção ou para "Como os agentes gravam no hub" (em curso); sem dono hoje. |
| 7 | Rodada 3 (linhas 53-54): "Consequência a rever na rodada sobre o conteúdo das raízes: a entrada só era local..." | A rodada sobre o conteúdo das raízes não aconteceu. Ficou implícito pela rodada 6 que `inbox/` replica como o resto. Não decidido: forma interna de `inbox/`, limite de idade (proposto em "Métodos conhecidos de organizar a raiz") e quem a esvazia (a pergunta da triagem saiu do "Contrato file-first"). | Não. Para a construção, sem dono. |
| 8 | Comentário 2026-10-02 (vindo de "Workloads piloto") e linha 30 da carta da rodada 8 | Os destinos de `armis-docs`, `armis-brand`, da skill `armis-docx` e desta frente não foram decididos numa rodada. O levantamento os usa como exemplo (`armis-docs` e `armis-brand` como referência; o context-hub como frente de planejamento). A leitura natural é `reference/armis-docs/`, `reference/armis-brand/`, `agents/skills/armis-docx/` e `initiatives/context-hub/`. | Não. Para a construção, com essa leitura como sugestão. |
| 9 | Rodada 16, B: "`index.md` em toda pasta que cresce" | Sem critério de "pasta que cresce" e sem dono do sumário das pastas só de `.md` (à mão, pela skill ou pelo verificador). A lição 4 de "Lições do vault" condena índice mantido à mão e "falha se corrige com mecanismo". | Não bloqueia (a escolha está feita), mas é o ponto de maior risco para a construção. |
| 10 | Rodada 11 (B, "uma pilha sugerida por tipo") e rodada 14 (`kind`) | As pilhas do levantamento (§3) foram aceitas com a B, mas o levantamento tem nove tipos e o `kind` aceito na rodada 14 tem oito: "criação de conteúdo" ficou fora (exemplo real: `animations`). Onde as pilhas moram (no `agents/blocks.md` ou na skill) não foi dito. As pilhas citam ainda "Trabalho de agentes" como `runs/` com briefs e handoffs, o que a rodada 14 mudou para `work/`. | Não. Para a construção: ajustar as pilhas ao `work/` e perguntar só se "criação de conteúdo" volta ao `kind`. |
| 11 | Carta da rodada 8, ponto 3 (linhas 137-138) | Os `Scripts/` e `Tests/` da VOEGOL fora de git: com a rodada 14 (C), têm testes, logo iriam a um repositório próprio que ainda não existe. | Não. É migração, para quando a VOEGOL vier ao hub. |
| 12 | Rodada 12, "algo mais", e rodada 16 (apoio) | Onde o verificador do fim da resposta roda no Codex e no Copilot. | Não. É de "Acesso dos agentes: decisão" (ticket 14, em curso). |

### 1b. Já fechados por outro caminho (não contam como abertos)

- **R13 antiga (o eixo do primeiro nível), suspensa na rodada 1:** substituída pelas seis raízes (rodada 3).
- **Rodadas 9 e 10 do portal, suspensas sem resposta:** substituídas pela rodada 11.
- **Rodada 13 do portal, suspensa:** refeita na rodada 16 (marcada absorvida e substituída).
- **"Ficam para testar aqui: arquivar por pasta ou por propriedade, e captura de cliente na máquina errada"
  (rodada 3, linhas 43-45):** arquivar por pasta ficou decidido (`_archive/` por raiz, rodada 3; movido por script,
  R25 de "Portas de entrada do hub"); a captura na máquina errada deixou de ser problema (rodada 3: tudo vive nas duas
  máquinas).
- **Campo de idioma (comentário 2026-10-14, "decidir aqui o campo e quem o grava"):** saiu em "Camada de busca"
  (um analisador só, sem campo de idioma).
- **"Se o explorador do Obsidian mostra `.agents/`: não verificado" (rodada 3):** perdeu o objeto com `agents/` sem
  ponto (rodada 4).
- **"Não verificado: o Codex e o Copilot lerem o `AGENTS.md` de uma subpasta" (rodada 10):** testado em "Testes das
  portas de entrada" e "Testes do papel do Maestri" (Codex com o marcador de raiz; Copilot chega à iniciativa).
- **"Se o obsidian-hybrid-search lê `.txt` e `.csv`" (não verificado em "Camada de busca"):** a rodada 16 leu o
  código do pacote 0.16.2: só indexa `.md`.
- **Hook nos outros harnesses (rodada 12):** passa ao ticket 14 (item 12 acima).

### 1c. Substituições (a decisão posterior vale)

- Nove tipos de raiz (rodada 2) → seis raízes, sem raiz pessoal (rodada 3).
- `.agents/` com ponto (pedido junto da rodada 3) → `agents/` sem ponto, `AGENTS.md` na raiz (rodada 4).
- `_arquivo/` → `_archive/`; `ventures` → `initiatives` (rodada 5).
- Níveis da rodada 6 → em revisão (rodada 7) → voltam a valer (R30 de "Portas de entrada do hub").
- `agents/roles/` (rodada 6) → papéis como peças da família `maestro-*` em `agents/skills/<skill>/` ("Maestri: padrão
  e liberdade"). Leitura minha: o Answer de 40 não cita `agents/roles/`, mas põe todas as peças, papéis inclusive, em
  `agents/skills/`.
- Rodada 8, A (quatro itens fixos: `README.md`, `retomada.md`, `_archive/`, `maestro/`) → metade fixa reaberta pelo
  Gustavo no chat (2026-10-14 ~18h10; `_archive/` por iniciativa era erro do maestro) → B da rodada 8 descartada →
  rodadas 9 e 10 suspensas → **rodada 11: núcleo de seis arquivos e blocos**.
- Blocos da rodada 11 (`runs/` com briefs e handoffs) → `runs/` só execuções e revisões, bloco novo `work/`, ordem nova
  (rodada 14) → texto final do catálogo (rodada 15).
- Órfãos: rodada 12, A com correção (`index.md` só nas pastas que crescem) → em revisão pela lição 4 → rodada 13
  suspensa → **rodada 16, B**.
- Segredos: "nunca no hub" (levantamento e recomendação A da rodada 14) → `.secrets/` na iniciativa, com as contas que
  acessam tenant no KeePass (rodada 14, B).
- Ficha: `type` do vault → `size`; saem `emoji` e `model` (rodada 14) → ganha `aliases` (rodada 16).

## 2. Rascunho do `## Answer`

```markdown
## Answer

**A árvore do hub tem o `AGENTS.md` e seis raízes em inglês; cada iniciativa nasce com um núcleo de seis arquivos
separados por ritmo e soma blocos de nome único de um catálogo; a busca é a porta para achar, e o `index.md` só
existe onde a busca não lê ou onde a pasta cresce; tudo replica nas duas máquinas, e só o que tem ponto no nome fica
numa máquina só.** Decidido com o Gustavo de 2026-10-10 a 2026-10-15, nas rodadas 3 a 6 (nota "Rodada atual") e 8,
11, 12, 14, 15 e 16 (portal); detalhe nos comentários.

- **Raiz (rodadas 3, 4 e 5):** `AGENTS.md`, `clients/` (iniciativas de cliente), `operations/` (trabalho contínuo),
  `initiatives/` (iniciativas sem cliente: produtos, frentes, estudo, spikes), `reference/` (conhecimento de
  referência), `agents/` (a oficina, sem ponto, para replicar pela sync normal) e `inbox/` (captura). O que termina vai
  para o `_archive/` da própria raiz, movido por script que confere o outro par (R25 de "Portas de entrada do hub").
  Sem raiz pessoal: o pessoal replica e cai em `initiatives/` ou `reference/`. O cofre do Obsidian é a raiz; o hub
  não tem `CLAUDE.md`; o `.git` fica na raiz de cada máquina e não replica ("Portas de entrada do hub", "Revisão do
  sync e da divergência").
- **Profundidade (rodada 6; volta a valer pela R30 de "Portas de entrada do hub"):** dois níveis em `clients/`
  (`clients/<cliente>/<iniciativa>/`, com o nível do cliente para o que é comum às iniciativas dele) e um nas outras
  (`operations/<operação>/`, `initiatives/<iniciativa>/`, `reference/<assunto>/`). Nenhuma porta de entrada depende
  da profundidade.
- **`agents/` (rodadas 6 e 12; "Maestri: padrão e liberdade"):** `agents/skills/<skill>/` (inclusive a família
  `maestro-*`, cada uma com catálogo e um arquivo por peça), `agents/machines/<máquina>.md` (o perfil de cada
  máquina, um arquivo), `agents/maestro/propostas/`, `agents/maestro/uso/<máquina>.md` e `agents/blocks.md`. Os papéis
  são peças do acervo, não uma pasta `agents/roles/`.
- **Núcleo da iniciativa (rodada 11, envio `04e0593a…`; substitui a A da rodada 8):** as sete seções do
  `initiative.md` do vault, cada uma no arquivo do seu ritmo: `initiative.md` (ficha, descrição e fontes),
  `retomada.md` (o estado, sobrescrito; é a nota de retomada do "Contrato file-first"), `tasks.md` (só pendências
  abertas), `decisions.md` (uma linha por decisão), `context.md` (fatos estáveis) e `log/AAAA-MM.md` (diário mensal).
  O `AGENTS.md` da iniciativa é só o mapa e as regras próprias. Opcional: `maestro/`, a personalização do acervo
  ("Maestri: padrão e liberdade"); o Maestri grava `.maestri/roles/` na pasta, e ela fica em cada par.
- **Blocos e catálogo (rodadas 11, 12, 14 e 15):** blocos com um nome só, somados quando o trabalho pede, nesta
  ordem: `inputs/`, `research/`, `design/`, `plans/`, `deliverables/`, `evidence/`, `tools/`, `runs/` (execuções e
  revisões, uma subpasta por execução), `work/` (trabalho em curso dos agentes: briefs, handoffs, estado antes de
  limpar o contexto), `procedures/`, `cases/`, `queries/`, `knowledge/`, `notes/`, `labs/` e `other/` (o que não cabe
  em nenhum; com três parecidos, propõe-se um bloco novo). O texto "entra / não entra" final está no comentário da
  rodada 15 e vira o `agents/blocks.md`, citado pelo `AGENTS.md` da raiz; cada tipo de trabalho tem uma pilha sugerida
  (levantamento, §3). A skill "nova iniciativa" cria pasta, núcleo e blocos por script, sem gastar tokens, e só é
  alterada com supervisão e aval (rodada 12).
- **Ficha, `initiative.md` (rodadas 14 e 16):** `id` (kebab-case, estável), `title`, `aliases` (siglas, nome no Loop,
  nome antigo no vault), `kind` (projeto de cliente, investigação, operação contínua, produto, frente de planejamento,
  spike, estudo, referência), `size` (o `type` do vault: change, initiative, project, study, idea), `status` (doing,
  backlog, on-hold, done, archived), `blocks` (os blocos em uso), `workspace`, `parent`, `related`, `cadence`
  (weekly, monthly, quarterly, none) e `updated_at`. Saem `emoji` e `model`; cliente e raiz não viram campo, o caminho
  já diz. Sem campo de idioma ("Camada de busca": um analisador só).
- **Títulos do núcleo (rodada 16, A):** os arquivos do núcleo ganham `title` com o nome da iniciativa ("Retomada ·
  VOEGOL cross-tenant"); a skill "nova iniciativa" os escreve e o verificador completa o que faltar (o `log/` de um
  mês novo) a partir do `title` da ficha. Motivo: o obsidian-hybrid-search pesa o título 10 vezes e os `aliases` 5
  vezes na busca por palavra, e o caminho da pasta não entra nela.
- **Índices e busca (rodada 16, B; substitui a escolha dos órfãos da rodada 12):** a busca é a porta para achar; o
  catálogo e o mapa do `AGENTS.md` da iniciativa dizem onde gravar. O `index.md` existe na pasta que guarda arquivo
  que a busca não lê (prints, scripts, `.csv`, `.txt`, logs, zip), com uma linha por arquivo, e também em toda pasta
  que cresce, mesmo só com `.md`, como sumário para navegar sem buscar. Fato lido no pacote 0.16.2: o
  obsidian-hybrid-search só indexa `.md`, filtra por pasta e por campo (`kind`, `status`, `blocks`) e respeita o
  `.gitignore`.
- **Texto dos anexos (rodada 16, A):** arquivo irmão ao lado do anexo (`proposta-v2.pdf` → `proposta-v2.pdf.md`),
  com `title`, `source` e `extractor` (Docling ou pandoc, com versão) no frontmatter; vale para PDF, Word, PowerPoint,
  Excel e HTML; replica e vai ao git; o anexo com texto dispensa linha no `index.md`.
- **Verificador (rodadas 12 e 16):** sem IA, no fim de cada resposta; inscreve no `index.md` como "sem descrição" o
  arquivo que a busca não lê e não tem linha, avisa a nota com YAML que a busca rejeitaria e completa os `title` do
  núcleo. No Claude Code, um mod; nos outros harnesses, "Acesso dos agentes: decisão".
- **Segredos (rodada 14, B):** `.secrets/` dentro da iniciativa, fora do git (e por isso fora da busca); senhas de
  contas que acessam tenant ficam no KeePass.
- **Scripts (rodada 14, C):** em `tools/` enquanto são de apoio; viram repositório próprio quando ganham testes,
  dependências ou uso fora da iniciativa.
- **Pasta não replicada, Q15 (rodadas 3 e 6):** por ora tudo vive nas duas máquinas, inclusive o conteúdo de cliente,
  e a árvore não tem pasta não replicada; o perfil de máquina é um arquivo por máquina. Fica numa máquina só apenas o
  que tem ponto no nome (`.git`, `.secrets/`, `.maestri/`), pela regra de "Revisão do sync e da divergência", e o
  índice da busca `.obsidian-hybrid-search.db`. O controle de acesso por pasta fica fora deste projeto (rodada 3).
  [Confirmar com o Gustavo: item 1 do rascunho.]
- **Demais notas:** [a decidir, item 2 do rascunho: proposta "frontmatter livre, só YAML válido"].
- **Protótipo:** as cartas `prototipo-12-ritmos` (núcleo e blocos, aprovada, envio `971570e7…`) e
  `prototipo-12-sumario` (localização, rodada 12). [Confirmar, item 3 do rascunho.]
- **Não verificado, para a construção:**
  - teste antes do primeiro segredo: um `.secrets/` aninhado não chega ao banco nem ao GitHub (o CLI do LiveSync vazou
    pastas com ponto aninhadas em "Teste: disco e banco sem o Obsidian"; exclusão `**/.*` e `**/.*/**`);
  - o OCR do Docling em português, para PDF escaneado; quando e quem dispara a extração dos anexos;
  - tirar `.obsidian-hybrid-search.db` do git e do LiveSync;
  - o critério de "pasta que cresce" e quem mantém o sumário do `index.md` das pastas só de `.md`, por mecanismo
    (lição 4 de "Lições do vault");
  - o que mora no nível `clients/<cliente>/`; a retomada de trabalho fora de uma iniciativa; a forma de `inbox/`;
  - os destinos de `armis-docs`, `armis-brand`, `armis-docx` e desta frente (leitura: `reference/`,
    `agents/skills/`, `initiatives/context-hub/`); as pilhas por tipo ajustadas ao `work/`, e "criação de conteúdo",
    que ficou fora do `kind`;
  - o verificador no Codex e no Copilot ("Acesso dos agentes: decisão").
```

## 3. Linha proposta para o "Decisions so far" do `map.md`

```markdown
- [Arquitetura de pastas e frontmatter do hub](issues/12-arquitetura-de-pastas-e-frontmatter.md): `AGENTS.md` e seis
  raízes em inglês (`clients/` com dois níveis, as outras com um, `_archive/` em cada uma); cada iniciativa nasce com
  um núcleo de seis arquivos por ritmo (`initiative.md` como ficha com `aliases`, `retomada.md`, `tasks.md`,
  `decisions.md`, `context.md`, `log/`) e soma blocos do catálogo `agents/blocks.md`; a busca é a porta, com `index.md`
  onde a busca não lê ou a pasta cresce e texto dos anexos em arquivo irmão `.pdf.md`; `.secrets/` fora do git; tudo
  replica.
```
