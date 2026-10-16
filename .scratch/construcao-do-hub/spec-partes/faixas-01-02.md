## Faixa 1: Esqueleto e frontmatter

A árvore do hub e o padrão das notas, impostos por mecanismo: o `AGENTS.md` e seis raízes em inglês, cada iniciativa
nascendo por script com um núcleo de seis arquivos e blocos de um catálogo, frontmatter por tipo dado pelo caminho, o
`index.md` como cartão da pasta, links `par://` só para o que não replica, e um verificador sem IA que preenche o
derivável e devolve o resto ao agente. Inclui as portas de entrada que dependem da árvore (sem `CLAUDE.md`, `.git` na
raiz, cofre do Obsidian na raiz), as lições do vault como restrições de desenho e os workloads piloto. Prova de ponta a
ponta: criar uma iniciativa pelo script dá o núcleo de seis arquivos; o verificador aceita a nota certa e recusa a sem
`status`.

Fontes: tickets 12 (Arquitetura de pastas e frontmatter do hub), 36 (Portas de entrada do hub), 35 (Métodos conhecidos
de organizar a raiz), 01 (Lições do vault), 02 (Workloads piloto), com o que o 14 (Acesso dos agentes: decisão) mudou no
marcador de raiz; catálogo de tipos aceito na rodada 18 do 12 (rascunho `12-frontmatter-proposta.md`), com a conciliação
do `status` da rodada 19.

### User stories

1. Como o Gustavo, quero que a raiz do hub tenha só o `AGENTS.md` e seis raízes em inglês (`clients/`, `operations/`,
   `initiatives/`, `reference/`, `agents/`, `inbox/`), para que cada coisa tenha um lugar certo e previsível.
2. Como o Gustavo, quero que as iniciativas de cliente morem em `clients/<cliente>/<iniciativa>/`, com o nível do cliente
   guardando o que é comum às iniciativas dele, para não repetir o comum em cada frente.
3. Como o Gustavo, quero que o trabalho contínuo, sem fim, more em `operations/<operação>/`, e as iniciativas sem
   cliente (produtos, frentes, estudo, spikes) em `initiatives/<iniciativa>/`, para separar o que termina do que não
   termina.
4. Como o Gustavo, quero que o conhecimento de referência, promovido, more em `reference/<assunto>/`, para que o
   conhecimento geral não fique preso dentro de uma iniciativa.
5. Como o Gustavo, quero uma raiz `inbox/` para captura rápida, de escrita livre, para não precisar decidir o lugar na
   hora de anotar.
6. Como o Gustavo, quero que cada raiz tenha o seu `_archive/`, para que o que termina saia do caminho sem sair do hub.
7. Como o Gustavo, quero que não exista raiz pessoal, para que o pessoal caia em `initiatives/` ou `reference/` e
   replique como o resto.
8. Como um agente, quero que a oficina dos agentes seja a pasta `agents/`, sem ponto, para que ela replique pela sync
   normal e seja lida pelos harnesses.
9. Como um agente, quero achar em `agents/` as skills (`agents/skills/<skill>/`, inclusive a família `maestro-*`), o
   perfil de cada máquina (`agents/machines/<máquina>.md`), as propostas e o uso do acervo do maestro
   (`agents/maestro/propostas/`, `agents/maestro/uso/<máquina>.md`), o catálogo de blocos (`agents/blocks.md`) e os
   esquemas de frontmatter (`agents/frontmatter/`), para saber onde mora cada peça da oficina.
10. Como um agente, quero criar uma iniciativa nova pela skill "nova iniciativa", que roda um script, para que pasta,
    núcleo e blocos nasçam sempre iguais e sem gastar tokens.
11. Como o Gustavo, quero que toda iniciativa nasça com o núcleo de seis arquivos separados por ritmo (`initiative.md`,
    `retomada.md`, `tasks.md`, `decisions.md`, `context.md`, `log/AAAA-MM.md`), para que nenhum arquivo único exploda
    como o `initiative.md` do vault.
12. Como um agente, quero que a ficha (`initiative.md`) traga a descrição, as fontes e os campos `id`, `title`,
    `aliases`, `kind`, `size`, `stage`, `blocks`, `workspace`, `parent`, `related` e `cadence`, para filtrar e achar a
    iniciativa sem abrir todo o resto.
13. Como um agente, quero que `tasks.md` tenha só as pendências abertas, `decisions.md` uma linha por decisão,
    `context.md` só os fatos estáveis e `log/AAAA-MM.md` o diário de um mês, para gravar cada coisa no arquivo do seu
    ritmo.
14. Como a busca, quero que cada arquivo do núcleo tenha `title` com o nome da iniciativa ("Retomada · VOEGOL
    cross-tenant"), para distinguir a retomada de uma iniciativa da de outra.
15. Como o verificador, quero completar o `title` de um arquivo do núcleo que nasceu sem ele (por exemplo, o `log/` de um
    mês novo) a partir do `title` da ficha, para nenhum arquivo do núcleo ficar sem nome.
16. Como um agente aberto na pasta de uma iniciativa, quero que o `AGENTS.md` dela seja só o mapa e as regras próprias,
    para não repetir o contrato da raiz.
17. Como um agente, quero consultar `agents/blocks.md`, com o "entra / não entra" de cada bloco, para escolher onde
    gravar sem perguntar ao Gustavo.
18. Como um agente, quero somar a uma iniciativa existente um bloco do catálogo (`inputs/`, `research/`, `design/`,
    `plans/`, `deliverables/`, `evidence/`, `tools/`, `runs/`, `work/`, `procedures/`, `cases/`, `queries/`,
    `knowledge/`, `notes/`, `labs/`, `other/`) quando o trabalho pedir, para que a pasta cresça conforme o trabalho e não
    por um molde fixo.
19. Como um agente, quero gravar em `other/` o que não cabe em nenhum bloco, dizendo por que (`why_other`), para não
    forçar uma nota num bloco errado.
20. Como o verificador, quero avisar quando três notas parecidas em `other/` pedem um bloco novo, para que o catálogo
    cresça por evidência.
21. Como o Gustavo, quero que a skill "nova iniciativa" e os seus scripts só mudem com supervisão e o meu aval, para que
    nenhum agente a edite a cada uso.
22. Como um agente, quero que o tipo de cada nota venha do caminho (`agents/frontmatter/paths.yml`), nunca da minha
    escolha, para que eu não erre nem invente tipo.
23. Como um agente, quero um esquema por tipo em `agents/frontmatter/<tipo>.yml`, como fonte única de campos
    obrigatórios, opcionais e valores aceitos, para saber exatamente o que a nota precisa.
24. Como o Gustavo, quero que toda nota tenha os campos comuns `title`, `type`, `initiative`, `created`, `updated` e
    `status` (rascunho, em uso, superada), e opcionais `aliases`, `tags` e `related`, para filtrar o vigente em qualquer
    pasta.
25. Como um agente, quero preencher só o que exige juízo (um `stage`, uma `question`, um `outcome`) e deixar a máquina
    preencher o derivável (`type`, `initiative`, `title` do núcleo, `updated`), para gastar menos e errar menos.
26. Como um agente que escreve uma nota de tipo com ciclo (ficha, research, design, plan, deliverable, work, case, lab),
    quero preencher o ciclo em `stage`, para que o `status` comum seja derivado e não brigue com o ciclo do tipo.
27. Como o verificador, quero derivar o `status` comum a partir do `stage` por uma tabela no esquema do tipo, para que o
    filtro do vigente funcione também nos tipos com ciclo.
28. Como o verificador, ao fim de cada resposta de agente, quero varrer o que mudou, preencher o derivável e devolver ao
    agente a lista do que falta, para que a resposta não termine com nota fora do esquema.
29. Como o verificador, quero recusar (devolver ao agente) a nota sem `status` ou com um campo obrigatório faltando ou
    fora dos valores aceitos, dizendo o que falta, para que o agente corrija na mesma resposta.
30. Como o Gustavo, quero criar uma nota no Obsidian sem frontmatter nenhum e que o verificador da próxima resposta de
    agente a complete, para não depender de Templater nem de lembrar o padrão.
31. Como o hook antes da gravação (faixa 6) e como o MCP do banco (faixa 5), quero validar contra os mesmos esquemas e o
    mesmo `paths.yml`, para que as três camadas imponham o mesmo padrão.
32. Como o Gustavo, quero que nenhuma regra de frontmatter more só no `AGENTS.md`, para que agentes menores não fiquem
    livres para "decidir" se seguem o padrão.
33. Como um harness, quero que o `AGENTS.md` e os `SKILL.md` fiquem sem frontmatter do hub, para que a instrução e o
    padrão de skills não sejam quebrados pelo verificador.
34. Como um agente, quero que o frontmatter saia sempre em YAML válido, para que a nota não fique de fora da busca.
35. Como um agente, quero que a busca seja a porta para achar, e o `index.md` exista só onde ela não basta ou onde a pasta
    cresce, para não manter cadeia de índices à mão.
36. Como o verificador, quero criar o `index.md` de uma pasta quando ela chega a 10 arquivos ou guarda arquivo que a busca
    não lê, para que nada fique órfão.
37. Como o verificador, quero manter a lista de um `index.md` com `summary: auto`, preservando o texto livre do topo, para
    que o cartão da pasta nunca fique desatualizado.
38. Como um agente, quero que o `index.md` declare `folder`, `summary` e `local`, para que a busca ache a descrição da
    pasta e o sync saiba se ela replica.
39. Como o Gustavo, quero que tudo replique nas duas máquinas, inclusive o conteúdo de cliente, e que só fique numa
    máquina o que tem ponto no nome (`.git`, `.secrets/`, `.maestri/`, o índice da busca) ou a pasta cujo `index.md` diz
    `local: true`, para que a regra de "o que não replica" seja uma só e visível.
40. Como o Gustavo, quero fazer uma pasta local criando nela um `index.md` com `local: true`, para não editar lista de
    exclusão à mão.
41. Como o script de exclusões, quero gerar a exclusão do sync e da busca a partir dos nomes com ponto e dos `index.md`
    com `local: true`, para que sincronizador e busca respeitem os marcadores sem configuração duplicada.
42. Como um agente, quero que o texto de um anexo (PDF, Word, PowerPoint, Excel, HTML) more num arquivo irmão
    (`proposta-v2.pdf` → `proposta-v2.pdf.md`) com `title`, `source` e `extractor`, para que a busca, que só lê `.md`,
    ache o anexo.
43. Como o verificador, quero dispensar a linha no `index.md` para o anexo que já tem texto irmão, para não descrever duas
    vezes o mesmo arquivo.
44. Como um agente, quero linkar o que replica por link interno normal com o caminho a partir da raiz do cofre, e o que
    não replica (pasta `local: true`, pasta com ponto, fora do hub) por `par://<par_id>/<caminho a partir da raiz do
    hub>`, sem letra de unidade, para que o link funcione nas duas máquinas e diga em qual par mora o destino.
45. Como o verificador, quero conferir os links pelo cartão das pastas e corrigir nos dois sentidos (interno que devia
    ser `par://` e o contrário), avisando o agente, para que nenhum link aponte para o que a outra máquina não tem.
46. Como um agente, ao citar algo de `.secrets/`, quero citar só o nome do arquivo, para que o segredo nunca vaze para uma
    nota que replica.
47. Como o Gustavo, quero `.secrets/` dentro da iniciativa, fora do git, do banco e da busca, e as senhas de contas que
    acessam tenant no KeePass, para que nenhum segredo saia da máquina.
48. Como o Gustavo, quero um teste que prove, antes do primeiro segredo, que um `.secrets/` aninhado não chega ao banco
    nem ao GitHub, porque pastas com ponto aninhadas já vazaram num teste anterior.
49. Como um agente, quero guardar scripts de apoio de uma iniciativa em `tools/` até ganharem testes, dependências ou uso
    de fora (quando viram repositório próprio), para não criar repositório cedo demais.
50. Como um agente de qualquer par, quero o perfil da máquina em `agents/machines/<máquina>.md`, com o nome do arquivo
    igual ao `par_id` dos links, para resolver um link `par://` sem tabela extra.
51. Como os três harnesses abertos na raiz, quero ler o `AGENTS.md` da raiz nativamente, sem nenhum `CLAUDE.md` no hub
    nem acima dele, porque um `CLAUDE.md` acima ou dentro desliga os `AGENTS.md` no Claude Code.
52. Como o Codex ou o Copilot abertos numa subpasta ou na pasta de um papel do Maestri, quero chegar ao `AGENTS.md` da
    raiz pelo `.git` real da raiz, sem marcador de raiz nem `.git` falso.
53. Como a outra máquina, quero que o `.git` de cada máquina fique fora do sync, para que cada par tenha o seu.
54. Como um agente numa sessão fora do hub, quero o contrato em caminho fixo (`C:\context-hub\AGENTS.md`) e as skills em
    `agents/skills/<skill>/`, para que os links e junctions do kit (faixa 8) apontem para um lugar que nunca muda.
55. Como o Gustavo, quero que o cofre do Obsidian seja a raiz do hub, para ver e editar tudo num cofre só.
56. Como um cliente pelo MCP (faixa 5), quero que o `AGENTS.md` da raiz comece por uma cabeça autossuficiente de até
    2.000 caracteres, para que o `instructions` do MCP leve o essencial sem corte.
57. Como o Gustavo, quero que o `AGENTS.md` seja curto e direto, só com o que não está imposto por mecanismo, para que ele
    não vire documento longo e normativo como o do vault.
58. Como o Gustavo, quero que só peçam o meu aval as mudanças no contrato, nos adaptadores e as exclusões ou reescritas
    grandes, para não aprovar cada passo.
59. Como o Gustavo, quero que todo arquivo tenha destino quando envelhece (o log por mês, a retomada sobrescrita, o
    `_archive/` da raiz), para que nada só cresça.
60. Como o Gustavo, quero que cada tipo de informação tenha um lugar só, escrito no catálogo e no esquema, para que dois
    agentes nunca gravem o mesmo fato em dois lugares.
61. Como o Gustavo, quero isolamento por iniciativa com promoção explícita para `reference/`, para que conhecimento geral
    não fique enterrado em `knowledge/` de uma iniciativa.
62. Como um agente, quero que a nota de `inbox/` exija só os campos comuns (o verificador preenche) e que, ao sair do
    `inbox/`, passe a valer o esquema do destino, para a captura ser livre e a nota arrumada depois ser cobrada.
63. Como o script do `_archive/` (faixa 10), quero um esquema `archived` com `archived_at` e `archive_reason`, além do
    esquema de origem, para que a nota arquivada continue válida.
64. Como o Gustavo, quero que o frontmatter não leve dado pessoal (organização, nunca nome ou e-mail de pessoa), para que
    dado pessoal fique nas pastas de origem.
65. Como o Gustavo, quero que esta frente (o context hub) nasça no hub como iniciativa, para que o hub seja casa dele
    mesmo.
66. Como o Gustavo, quero copiar para o hub, quando eu disser, o conteúdo do vault que eu escolher (já desejados:
    `armis-docs`, `armis-brand` e a skill `armis-docx`), e que daí em diante ele seja trabalhado só no hub, para que não
    haja duas casas para o mesmo conteúdo.
67. Como o Gustavo, quero que o vault `ai-operating-system` não ganhe nada do hub (nem ponteiro, nem registro, nem
    mudança), para que ele seja só referência e possa ser superado.
68. Como um agente, quero poder ler o vault como referência direto no disco (ele só existe no notebook), para consultar o
    passado sem tratá-lo como casa.

### Implementation decisions

**Árvore (12, 35, 36)**
- Raiz: `AGENTS.md` e as seis raízes `clients/`, `operations/`, `initiatives/`, `reference/`, `agents/`, `inbox/`; cada
  raiz com o seu `_archive/`; sem raiz pessoal (12). O corte vem do PARA (termina × não termina), do FHS (o que não é
  compartilhável não divide pasta com o que é) e do `.claude`/XDG (caminho fixo) (35).
- Profundidade: dois níveis em `clients/` (`clients/<cliente>/<iniciativa>/`), um nas outras (`operations/<operação>/`,
  `initiatives/<iniciativa>/`, `reference/<assunto>/`); nenhuma porta de entrada depende da profundidade (12, 36).
- `agents/`: `skills/<skill>/` (com a família `maestro-*`; os papéis são peças do acervo), `machines/<máquina>.md` (o
  nome é o `par_id`), `maestro/propostas/`, `maestro/uso/<máquina>.md`, `blocks.md` e `frontmatter/` (`paths.yml` e um
  esquema por tipo) (12). Opcional em cada iniciativa: `maestro/` (12, vinda de 40).
- O hub não tem `CLAUDE.md` em lugar nenhum; o cofre do Obsidian é a raiz; o `.git` fica na raiz de cada máquina e não
  replica (12, 36). O `.git` real da raiz é o que leva Codex e Copilot ao `AGENTS.md` numa subpasta ou pasta de papel; o
  marcador de raiz e o `project_root_markers` saíram (14, rodada 4; comentário de 2026-10-15 no 16). Sem `.git` falso (36).
- A conferência "sem `CLAUDE.md` no hub nem acima dele" é do kit de par (36); esta faixa a entrega como passo do
  instalador da faixa, no contrato do instalador do plano (proposta: idempotente, HOME de ensaio pela variável, simulação).
- Caminho fixo `C:\context-hub\AGENTS.md` e skills em `agents/skills/<skill>/` (36); o hub nasce em `C:\context-hub`
  (04; plano).

**Núcleo e skill "nova iniciativa" (12)**
- Núcleo de seis arquivos: `initiative.md` (ficha, descrição e fontes), `retomada.md` (o estado, sobrescrito; a nota de
  retomada da faixa 2), `tasks.md` (só pendências abertas), `decisions.md` (uma linha por decisão), `context.md` (só fatos
  estáveis) e `log/AAAA-MM.md` (o diário, um arquivo por mês). O `AGENTS.md` da iniciativa é só o mapa e as regras
  próprias.
- A skill "nova iniciativa" cria pasta, núcleo e blocos por script, mecanicamente; escreve o `title` de cada arquivo do
  núcleo com o nome da iniciativa ("Retomada · <nome>") e o `blocks` da ficha. Só muda com supervisão e aval; a guarda que
  impõe isso é a do acervo (faixa 9).
- Entrada do script: a raiz (e, em `clients/`, o cliente), o nome, os campos da ficha que exigem juízo e os blocos
  escolhidos. Saída: a pasta pronta, que o verificador aceita sem devolver nada.

**Catálogo de blocos, `agents/blocks.md` (12)**
- Dezesseis blocos de nome único, nesta ordem: `inputs/`, `research/`, `design/`, `plans/`, `deliverables/`, `evidence/`,
  `tools/`, `runs/` (uma subpasta por execução), `work/` (uma subpasta por agente ou frente), `procedures/`, `cases/`,
  `queries/`, `knowledge/`, `notes/`, `labs/`, `other/`. O texto "entra / não entra" é o texto final da rodada 15 do
  ticket 12, copiado sem mudança. O `AGENTS.md` da raiz cita o catálogo.
- `other/`: com três parecidos, propõe-se um bloco novo (12).
- Scripts de apoio em `tools/` até ganharem testes, dependências ou uso de fora (12).

**Frontmatter por tipo (12, rodadas 17 a 19; catálogo aceito do rascunho `12-frontmatter-proposta.md`)**
- O tipo vem do caminho, por `agents/frontmatter/paths.yml`; cada tipo tem um esquema em `agents/frontmatter/<tipo>.yml`
  (na proposta aceita: JSON Schema escrito em YAML), fonte única para o verificador, o hook da faixa 6 e o MCP da faixa 5.
- Campos em inglês; sem dado pessoal (organização, nunca nome ou e-mail de pessoa).
- Campos comuns em toda nota `.md` do hub (fora `AGENTS.md` e `SKILL.md`): `title`, `type`, `initiative`, `created`,
  `updated`, `status` (rascunho, em uso, superada); opcionais `aliases`, `tags`, `related`. O verificador preenche
  `type`, `initiative`, `title` do núcleo e `updated`. A obrigatoriedade e o valor de `initiative` numa nota fora de
  iniciativa (`reference/`, `inbox/`) ficam para o esquema; exigi-lo só onde o caminho identifica uma iniciativa é
  esclarecimento **[aceita]**, não decisão do 12.
- Nos tipos com ciclo, o ciclo vai em `stage` (quem escreve preenche) e o `status` é derivado pelo verificador por uma
  tabela no esquema; nos outros, quem escreve preenche o `status` (12, rodada 19). Ficha: `stage` com doing, backlog,
  on-hold, done, archived; saem `emoji` e `model`; cliente e raiz não viram campo (12).
- Os 28 tipos (campos próprios, além dos comuns; obrigatórios em negrito; onde a proposta tinha um `status` próprio, ele
  passa a `stage` com os mesmos valores):

| Tipo | Onde | Campos próprios |
|---|---|---|
| `initiative` | `initiative.md` | **`id`**, `aliases`, **`kind`**, **`size`**, **`stage`** (doing, backlog, on-hold, done, archived), **`blocks`**, `workspace`, `parent`, `related`, `cadence` |
| `retomada` | `retomada.md` | **`next_step`**, `blocked_by`, `last_agent` (harness e modelo) |
| `tasks` | `tasks.md` | `open_count` (verificador) |
| `decisions` | `decisions.md` | `last_decision` (verificador) |
| `context` | `context.md` | `reviewed` |
| `log` | `log/AAAA-MM.md` | **`month`** (verificador) |
| `index` | `index.md` | **`folder`**, **`summary`** (`auto`), **`local`** (true, false) |
| `attachment-text` | `<anexo>.md` ao lado do anexo | **`source`**, **`extractor`**, `extracted`, `source_hash` |
| `input` | `inputs/` | **`origin`**, **`received`**, `org` |
| `research` | `research/` | **`question`**, **`stage`** (open, answered, dropped), `sources`, `verified` |
| `design` | `design/` | **`stage`** (draft, proposed, approved, superseded), `superseded_by`, `decision` |
| `plan` | `plans/` | **`stage`** (draft, active, done, dropped), `due`, `owner` |
| `deliverable` | `deliverables/` | **`stage`** (draft, review, delivered), **`audience`** (client, internal), `version`, `delivered` |
| `evidence` | `evidence/` | **`proves`**, **`captured`**, `origin` |
| `tool` | `tools/` (o `README.md` de cada ferramenta) | **`language`**, **`run`**, `repo` |
| `run` | `runs/<execução>/` | **`started`**, **`outcome`** (ok, partial, failed), `ended`, `harness`, `model` |
| `work` | `work/` | **`work_kind`** (brief, handoff, state), **`stage`** (open, closed), `agent` |
| `procedure` | `procedures/` | **`applies_to`**, `last_validated` |
| `case` | `cases/` | **`stage`** (open, closed), **`opened`**, `closed`, `severity` |
| `query` | `queries/` | **`language`**, **`target`**, `last_run` |
| `knowledge` | `knowledge/` | **`topic`**, `verified`, `reviewed` |
| `note` | `notes/` | `topic`, `course` |
| `lab` | `labs/` | **`environment`**, **`stage`** (active, torn-down) |
| `other` | `other/` | **`why_other`** |
| `reference` | `reference/<assunto>/` | **`topic`**, `source`, `reviewed` |
| `inbox` | `inbox/` | só os comuns, preenchidos pelo verificador |
| `machine` | `agents/machines/` | **`machine`**, **`os`**, `role` (par, cliente) |
| `archived` | `_archive/` | o esquema de origem, mais **`archived_at`** e `archive_reason` (o script do arquivo preenche) |

**Imposição (12, rodada 18, C)**
- Três camadas, nenhuma regra só no `AGENTS.md`: o hook antes da gravação recusa a nota fora do esquema nos três
  harnesses (faixa 6); o MCP do banco valida igual (faixa 5); o verificador sem IA no fim de cada resposta preenche o
  derivável e devolve o resto. Sem Templater: nota do Gustavo nasce sem frontmatter e o verificador da próxima resposta de
  agente completa.

**Verificador sem IA (12)**
- Roda no fim de cada resposta de agente, pelo canal de fim de resposta de cada harness (14: Claude Code pelo mod com
  `turn.start` e `classic.Stop`; Copilot pelo hook `agentStop` com a extensão `onAgentStop`; Codex pelo hook `Stop`), e
  também sozinho sobre uma pasta, para teste e manutenção. O registro no evento segue a fronteira do plano: script e
  fragmento de configuração próprios da faixa; a faixa 8 junta os fragmentos.
- Faz: (a) valida cada nota mudada contra o esquema do tipo dado pelo caminho; (b) preenche o derivável; (c) completa o
  `title` do núcleo pela ficha; (d) deriva `status` de `stage`; (e) cria o `index.md` quando a pasta chega a 10 arquivos
  ou guarda arquivo que a busca não lê, e mantém a lista dos que têm `summary: auto`, preservando o texto livre do topo;
  (f) confere os links pelo cartão das pastas e corrige nos dois sentidos, avisando; (g) avisa quando três notas
  parecidas em `other/` pedem bloco novo; (h) devolve ao agente a lista do que falta, e a resposta não termina enquanto
  houver falta.
- Ignora o que tem ponto no nome e não toca `AGENTS.md` nem `SKILL.md`.

**`index.md`, cartão da pasta (12, rodadas 16 a 18)**
- A busca é a porta para achar. O `index.md` existe onde há arquivo que a busca não lê (o obsidian-hybrid-search 0.16.2
  só indexa `.md`) e também em toda pasta que cresce, mesmo só com `.md`, como sumário para navegar sem buscar; o
  verificador o cria e mantém. Declara `summary: auto` e `local: true|false`. O anexo com texto irmão dispensa linha.

**Pasta não replicada (12; glossário)**
- Tudo replica, inclusive conteúdo de cliente. Fica numa máquina só o que tem ponto no nome (`.git`, `.secrets/`,
  `.maestri/`, o índice da busca) e a pasta cujo `index.md` diz `local: true`. Um script gera a exclusão do sync e da
  busca a partir desses marcadores; o sincronizador (faixa 4) e a busca (faixa 3) a consomem. O glossário põe a pasta não
  replicada também fora do GitHub.

**Texto dos anexos (12, rodada 16)**
- Arquivo irmão `<anexo>.md` com `title`, `source` e `extractor` (Docling ou pandoc, com versão); vale para PDF, Word,
  PowerPoint, Excel e HTML; replica e vai ao git.

**Links (12, rodada 20)**
- O que replica: link interno normal com caminho a partir da raiz do cofre ("Absolute path in vault" do Obsidian). O que
  não replica (pasta `local: true`, pasta com ponto, fora do hub): `par://<par_id>/<caminho a partir da raiz do hub>`,
  sem letra de unidade. De `.secrets/`, só o nome do arquivo.

**Segredos (12, rodada 14)**
- `.secrets/` dentro da iniciativa, fora do git e da busca; senhas de contas que acessam tenant no KeePass. A exclusão
  do sync tem de pegar ponto em qualquer nível (`**/.*` e `**/.*/**`; 12 e 16).

**Contrato da raiz (36, 01)**
- O `AGENTS.md` da raiz começa por uma cabeça autossuficiente de até 2.000 caracteres (corte de 2.048 do Claude Code no
  `instructions` do MCP); textos curtos e diretos; aponta para o catálogo e os esquemas, sem repetir regra que o mecanismo
  impõe; o contrato só se edita dentro do hub (42). A seção da regra de retomada é da faixa 2.

**Lições do vault como restrições de desenho (01)**
- Falha se corrige com mecanismo, ou tirando regra, nunca acrescentando regra; cada tipo de informação tem um lugar só;
  todo arquivo tem destino quando envelhece; a porta é a camada de busca e um índice só existe onde a busca não basta;
  aval só para o contrato, os adaptadores e as exclusões ou reescritas grandes; frontmatter com o que a busca ou o
  contrato usam; isolamento por iniciativa com promoção explícita; complexidade conquistada (uma camada só entra se
  resolve um dos cinco critérios); fato, hipótese, decisão e recomendação distintos.

**Workloads piloto (02)**
- Nascem no hub esta frente e o que o Gustavo disser, sem exceção por parentesco, ID ou cliente; a operação SOC STRATA
  fica fora por ora. Conteúdo do vault escolhido pelo Gustavo é copiado e passa a ser trabalhado só no hub; o vault não
  recebe nada. A cópia acontece quando o Gustavo disser.

### Testing decisions

- **Costura:** um hub de ensaio (`C:\context-hub-ensaio` ou uma pasta de teste; o plano propõe o maestro entregá-lo
  pronto antes da hora, na forma do 12 **[formato]**) e um HOME de ensaio pela variável do contrato do instalador; nada em `~/.claude`,
  `~/.codex` ou `~/.copilot` de verdade. Os testes exercem só comportamento externo: o script de criação, o verificador
  chamado sozinho sobre uma pasta, o verificador pelo canal de fim de resposta numa sessão real em modo não interativo
  (`claude -p`, `codex exec`, `copilot -p`) e o script de exclusões.
- **Script de criação:** criar uma iniciativa em `clients/<cliente>/<iniciativa>/` e em `initiatives/<iniciativa>/` dá
  a pasta no nível certo, os seis arquivos do núcleo com frontmatter válido e `title` "<Arquivo> · <nome>" e os blocos
  escolhidos; rodar o verificador logo depois não devolve nada; rodar o script duas vezes não duplica nem sobrescreve.
  O molde não se estende a `agents/` nem a `inbox/`; se `operations/` e `reference/` levam o núcleo inteiro segue
  aberto (12). O `AGENTS.md` da iniciativa é só o mapa e as regras próprias (12); o script não o cria: ele nasce à mão,
  quando a iniciativa tiver regra própria (Gustavo, 2026-10-16).
- **Verificador, casos:** nota certa aceita; nota sem `status` devolvida com o campo que falta; valor fora da lista
  devolvido; `type` e `initiative` preenchidos pelo caminho; `title` do `log/` de mês novo completado pela ficha; `status`
  derivado do `stage`; nota do `inbox/` sem frontmatter completada; nota que sai do `inbox/` cobrada pelo esquema do
  destino; `AGENTS.md`, `SKILL.md` e pastas com ponto intocados; YAML inválido devolvido.
- **Cartão da pasta:** a 10ª nota numa pasta cria o `index.md` com `summary: auto`; um PDF sem texto irmão cria o
  `index.md`; um PDF com texto irmão dispensa a linha; texto livre do topo preservado entre duas passadas.
- **Pasta local e links:** um `index.md` com `local: true` entra na exclusão gerada; um link interno para ela é corrigido
  para `par://`, e um `par://` para pasta que replica volta a link interno, com aviso nos dois casos.
- **Portas:** `claude -p`, `codex exec` e `copilot -p` abertos na raiz do hub de ensaio citam o `AGENTS.md` da raiz; Codex
  e Copilot numa subpasta chegam a ele pelo `.git` da raiz; um `CLAUDE.md` posto acima do hub de ensaio é apontado pela
  conferência do instalador.
- **Segredo aninhado:** um `.secrets/` aninhado é abrangido pela exclusão gerada e não chega ao git do hub de ensaio,
  ao banco nem à busca; a parte "não chega ao banco" roda com o banco de ensaio da faixa 4, com o CLI rodando e na
  varredura de partida (o 48 achou o vazamento de pasta com ponto aninhada nessa varredura).
- **Aceite de ponta a ponta:** numa sessão `claude -p` com HOME de ensaio, aberta na raiz do hub de ensaio, o agente cria
  uma iniciativa pela skill "nova iniciativa" e grava uma nota de `research/` sem `status`; o núcleo de seis arquivos
  existe e é aceito; no fim da resposta o verificador devolve a nota sem `status`, o agente completa, e o verificador a
  aceita.

### Out of scope

- O hook antes da gravação que recusa a nota fora do esquema (faixa 6) e a validação dentro do MCP do banco (faixa 5);
  esta faixa entrega os esquemas que os dois usam.
- Indexar na busca (faixa 3), levar a exclusão ao sincronizador (faixa 4), mover para o `_archive/` e apagar depois de 30
  dias (faixa 10), instalar links simbólicos, junctions e hooks no HOME (faixa 8), a guarda do acervo e o `routing.yml`
  (faixa 9).
- Templater; campo de idioma no frontmatter (a busca decidiu um analisador só, ticket 09).
- Mecanismo de controle de acesso por pasta (fora deste projeto); política de dado de cliente na segunda máquina.
- Qualquer mudança no vault `ai-operating-system`; aposentá-lo; a operação SOC STRATA; copiar conteúdo do vault sem o
  Gustavo dizer.
- A segunda máquina e a instalação de verdade em `C:\context-hub` e nos HOMEs reais sem o aval do Gustavo.

### Pontos abertos para a construção

- Teste antes do primeiro segredo: um `.secrets/` aninhado não chega ao banco nem ao GitHub (exclusão `**/.*` e
  `**/.*/**`). Não verificado.
- Gerar a exclusão do CLI do LiveSync e do obsidian-hybrid-search a partir dos `index.md` com `local: true`: não
  verificado. Se o mesmo script gera a exclusão do git (o glossário põe a pasta local fora do GitHub; o 12 só fala em sync
  e busca); o obsidian-hybrid-search respeita o `.gitignore` (fato lido no pacote 0.16.2), o que pode juntar as duas.
- Tirar `.obsidian-hybrid-search.db` do git e do LiveSync.
- O MCP do banco validar o esquema (versão modificada, faixa 5); o OCR do Docling em português (não verificado) e quem
  dispara a extração do texto dos anexos.
- O nível `clients/<cliente>/` guarda o que é comum às iniciativas do cliente (12, R18, de volta em vigor); a lista
  concreta do que mora ali e o seu padrão seguem abertos. A retomada de trabalho fora de uma iniciativa; a forma de
  `inbox/`.
- Se `operations/` e `reference/` levam o núcleo inteiro.
- Os destinos de `armis-docs`, `armis-brand`, `armis-docx` e desta frente (leitura do 12: `reference/`,
  `agents/skills/`, `initiatives/context-hub/`); as pilhas sugeridas por tipo ajustadas ao `work/`; "criação de
  conteúdo" no `kind`.
- Os `Scripts/` e `Tests/` da VOEGOL quando ela vier ao hub.
- ~~A tabela `stage` → `status`~~: decidida em 2026-10-16 (rodada `ticket-05-perguntas-do-trilho`): rascunho = backlog (ficha), open (research), draft (design, plan, deliverable), proposed, review; em uso = doing, on-hold, done (ficha e plan), answered, approved, active (plan, lab), delivered, open (work, case), closed (case); superada = archived, dropped, superseded, closed (work), torn-down. Na mesma rodada: `operations/<operação>/` não conta como iniciativa (só `clients/<cliente>/<iniciativa>/` e `initiatives/<iniciativa>/` exigem `initiative`); as tarefas (e) a (h) do verificador vão no ticket 27.
- Os valores aceitos de `kind`, `size` e `cadence` (a rodada 14 do 12 tem as tabelas no `.json` da caixa do portal; o
  `cadence` ganhou `weekly`) e o formato de `id`.
- O que conta como "10 arquivos" (subpastas contam? em `runs/`, cada execução é subpasta) e se o PDF com texto irmão
  ainda conta como "arquivo que a busca não lê" para criar o `index.md`.
- Como o verificador sabe "o que mudou": a mudança do agente na resposta e a nota que o Gustavo criou no Obsidian desde a
  última passada.
- O verificador grava no disco sob a garantia "nenhuma gravação sem guarda de versão" (11), sem exceção. Que ele só
  complete campos deriváveis, por troca de trecho, é **[aceita]** e não dispensa a guarda: relê o arquivo logo antes de
  gravar e só troca o trecho se o arquivo ainda é o que leu; se mudou, refaz ou devolve ao agente (o sincronizador
  também grava, 08 e 33). A janela entre releitura e gravação: não verificado. Manter índices e conferir links segue a
  mesma guarda.
- A ordem entre o verificador e o checkpoint da faixa 2 no mesmo fim de resposta.
- A linguagem do verificador e dos scripts: o MCP do es617 é TypeScript (Node 22 ou mais novo) e as peças Python
  (python-frontmatter, PyYAML com `safe_load`) só entram com um processo Python ao lado (16).
- Os nomes das máquinas (`par_id`) e o conteúdo de `agents/machines/<máquina>.md`: o perfil por máquina segue em "Not yet
  specified" no mapa.
- Onde fica o registro do aval de mudança no contrato (lacuna de dono do 16).
- Quando esta prova de conceito vira o hub real em `C:\context-hub` ("Not yet specified" no mapa).
- Se o explorador do Obsidian mostra pastas com ponto: não verificado (12).

## Faixa 2: Retomada e checkpoint

O contrato file-first em funcionamento: cada trabalho tem uma nota de retomada de sete campos, sobrescrita; uma regra no
contrato global manda mantê-la e levar ao hub o que só a memória privada da ferramenta sabe; o mecanismo de fim de
resposta de cada harness obriga o agente a cumprir; a checagem de início de sessão abre a nota. Prova de ponta a ponta:
numa sessão `claude -p` com HOME de ensaio, aberta numa iniciativa do hub de ensaio, o fim da resposta deixa
`retomada.md` com os sete campos; a sessão seguinte começa com a nota no contexto; os dois hooks têm teste automatizado.

Fontes: ticket 10 (Contrato file-first: zonas e checkpoint), com o que o 14 (Acesso dos agentes: decisão) decidiu sobre
fim de resposta e checagem de início, o 11 (Como os agentes gravam no hub) sobre como a nota é gravada, o 08
(Divergência e edição concorrente) sobre a checagem de início e o 12 sobre o lugar e o frontmatter da nota.

### User stories

1. Como o Gustavo, quero que qualquer sessão nova (outro agente, outro modelo, outra máquina) retome um trabalho de onde
   a anterior parou usando só o que está no disco, para não depender de chat nem de memória de ninguém.
2. Como um agente que nunca viu o trabalho, quero que a nota de retomada e o que ela aponta bastem para eu dar o próximo
   passo sem perguntar nada que já foi respondido.
3. Como um agente, quero que a nota tenha sete campos (objetivo, onde parou, próximo passo, decisões com a linha e um
   ponteiro, o que foi tentado e não deu certo, perguntas abertas, arquivos em jogo), para saber o que escrever e o que
   procurar.
4. Como um agente, quero que a nota seja curta e sobrescrita, não acumulada, com o histórico nas decisões e no git, para
   que ela nunca cresça a ponto de não ser lida.
5. Como um agente que lê a nota, quero que ela marque o que é fato e o que é hipótese, para não tratar suposição como
   decisão.
6. Como um agente aberto numa iniciativa, quero achar a nota em `retomada.md` no núcleo da pasta, sem busca, para começar
   na hora.
7. Como a busca e o Gustavo, quero que a nota tenha `title` "Retomada · <iniciativa>" e o frontmatter do tipo `retomada`
   (`next_step` obrigatório, `blocked_by`, `last_agent` com harness e modelo, mais os comuns), para achar e filtrar
   retomadas.
8. Como um agente, quero que o contrato global de cada harness traga a regra de manter a nota em dia, para que a regra me
   chegue em qualquer porta, inclusive dentro de um papel do Maestri, que esconde o `AGENTS.md` do workspace.
9. Como um agente, quero que a regra mande conferir se a memória privada da ferramenta tem contexto exclusivo relevante
   que o hub não tem, e gravá-lo no hub no lugar certo, para que nada importante fique só na minha gaveta pessoal.
10. Como o Gustavo, quero que a memória automática do Claude continue ligada, e que o contrato obrigue a levar ao hub o
    que só ela tem, para não perder o que ela faz bem nem deixar o hub sem esse contexto.
11. Como o Claude Code, quero que um mod de fim de resposta (`turn.start` com `classic.Stop`) devolva a resposta quando a
    nota não reflete o que foi feito ou a memória privada ganhou algo que o hub não tem, e a solte quando a nota foi
    atualizada, para que a regra seja cumprida sem o Gustavo pedir.
12. Como o Copilot, quero o hook `agentStop` junto com a extensão `onAgentStop` (com `--experimental`), ligados juntos,
    para ter o mesmo checkpoint de fim de resposta.
13. Como o Codex, quero o hook `Stop`, que devolve e solta (o "solta" passou quando a nota de retomada muda), para ter o
    mesmo checkpoint.
14. Como o Gustavo, quero que o checkpoint não tenha revisão pós-sessão nem use o FreeLLMAPI (10), para que ele seja
    barato, local e não leia transcrição com dado de cliente. (Checkpoint sem IA nenhuma: **[aceita]**; o 10 exclui só
    esses dois itens, e o 14 não decidiu "sem modelo".)
15. Como qualquer harness numa pasta fora do hub, quero que os hooks de início e de fim saiam na hora, para não pagar nada
    nem ver aviso que não é do hub.
16. Como o Gustavo, quero os hooks no escopo do usuário nos três harnesses, para que valham em toda porta, inclusive na
    pasta de um papel do Maestri.
17. Como o Codex, quero cada hook aprovado de antemão pelo hash em `hooks.state`, posto pelo kit, para não abrir a tela
    `/hooks` na partida.
18. Como o Copilot, quero o hook de usuário (o de projeto exige pasta confiável), para que o checkpoint rode sem passo
    manual.
19. Como uma sessão nova num par, quero que a checagem de início leia o arquivo da vigia e, além do estado do sync, abra a
    nota de retomada do trabalho que a pasta identifica, para começar com a divergência e o estado à vista.
20. Como uma sessão nova num par sem o arquivo da vigia, quero que a checagem caia na ferramenta do MCP como reserva, para
    nunca começar no escuro.
21. Como uma sessão num cliente, quero que a checagem de início use a ferramenta do MCP de um par, porque o cliente não
    tem cópia no disco.
22. Como uma sessão aberta numa pasta que não diz o trabalho (por exemplo, a raiz), quero achar a nota pela camada de
    busca, pelo nome que o Gustavo der, ou perguntar, para não abrir a nota errada.
23. Como um recruta do Maestri, quero que a checagem de início rode com o meu `MAESTRI_TERMINAL_ID`, para que o hook saiba
    em que terminal está.
24. Como o Gustavo, quero que, num harness onde o hook de início falhar, a checagem vire regra no contrato daquele
    harness, para que nenhum harness fique sem ela.
25. Como um agente, quero atualizar a nota existente por troca de trecho no disco, ou regravá-la inteira pelo
    `write_note` do MCP do banco com a versão que li, porque o hook da faixa 6 recusa a regravação inteira no disco.
26. Como um agente com o banco fora do ar, quero seguir trocando trechos no disco, avisar na resposta e anotar a pendência
    na nota de retomada, para que a sessão seguinte saiba o que ficou esperando a porta voltar.
27. Como um agente, quero gravar o estado de trabalho em curso (briefs, handoffs, estado salvo antes de limpar o contexto)
    em `work/` e o "onde a iniciativa parou" só em `retomada.md`, para não ter duas notas de estado.
28. Como o Gustavo, quero que o chat e o scratchpad morram com a sessão e sobrevivam só a nota, as decisões e os arquivos
    do trabalho, para saber o que é descartável.
29. Como o Gustavo, quero saber os furos aceitos do checkpoint (ele não vê o que foi dito no meio de uma resposta longa e
    não roda quando eu interrompo), cobertos só pela regra, para não confiar nele além do que entrega.
30. Como o Gustavo, quero que o contrato não carregue em dobro quando a sessão abre no hub e o arquivo global também
    aponta para ele, para não gastar contexto à toa.
31. Como a faixa 8, quero receber desta faixa o script e o fragmento de configuração de cada hook, sem que ela edite a
    configuração de outra faixa, para juntar tudo no kit.
32. Como o Gustavo, quero que o desenho do contrato valha para o hub pronto, e não seja aplicado às sessões desta frente
    de planejamento, para não misturar o processo do hub com o da prova de conceito.

### Implementation decisions

**Nota de retomada (10, 12)**
- Uma por trabalho (10), no núcleo da iniciativa como `retomada.md` (12). Sete campos: objetivo; onde parou; próximo
  passo; decisões (a linha e um ponteiro); o que foi tentado e não deu certo; perguntas abertas; arquivos em jogo.
  Sobrescrita; marca fato e hipótese. Critério de suficiência: um agente que nunca viu o trabalho, lendo só a nota e o que
  ela aponta, dá o próximo passo sem perguntar o que já foi respondido (10).
- Frontmatter do tipo `retomada`: **`next_step`** (uma frase), `blocked_by`, `last_agent` (harness e modelo), mais os
  comuns; `title` "Retomada · <iniciativa>", escrito pela skill "nova iniciativa" e completado pelo verificador (12).
- Distinta de `work/`, que guarda briefs, handoffs e o estado salvo antes de limpar o contexto, por agente ou frente; o
  "não entra" de `work/` manda o "onde a iniciativa parou" para `retomada.md` (12, catálogo de blocos).

**Regra no contrato global (10, 14)**
- A regra vai no contrato global de cada harness: o `AGENTS.md` da raiz do hub entra por import no `~/.claude/CLAUDE.md`
  do Claude Code e por link simbólico nos arquivos globais do Codex e do Copilot (36 R28, 42, 14; a instalação é da
  faixa 8). Ela manda manter a nota em dia e conferir se a memória
  privada da ferramenta tem contexto exclusivo relevante que o hub não tem, gravando-o no hub no lugar certo. Esta faixa
  escreve essa seção do `AGENTS.md`; o arquivo é da faixa 1.

**Checkpoint de fim de resposta (10, 14)**
- Comportamento: ao fim de cada resposta numa pasta do hub, se a nota não reflete a resposta ou a memória privada ganhou
  algo que o hub não tem, o agente é devolvido para gravar; quando a nota é atualizada, é solto (o "devolve e solta"
  testado na bancada de acesso, 14). Sem revisão pós-sessão nem FreeLLMAPI (10); sem modelo nenhum é **[aceita]** (a
  bancada usou um script sem modelo por escolha própria); a mesma lógica serve aos três canais
  abaixo (o canal muda por harness; usar um script só nos três é escolha de construção, não decisão de ticket).
- Por harness (14): Claude Code pelo mod (`turn.start` com `classic.Stop`); Copilot pelo hook `agentStop` junto com a
  extensão `onAgentStop` (`--experimental`); Codex pelo hook `Stop`, sem correlato de mod (app-server e SDK do Codex de
  reserva). O ticket 10 previa um hook `Stop` no Claude Code; o 14 trocou pelo mod.
- Hooks no escopo do usuário, saindo na hora fora do hub; no Codex, aprovados pelo hash em `hooks.state`; no Copilot, só
  hook de usuário (14). Codex com `danger-full-access` (14).
- Fora: revisão pós-sessão e o FreeLLMAPI no checkpoint; a memória automática do Claude segue ligada (10).
- Furos aceitos, cobertos só pela regra: não vê o meio de uma resposta longa; não roda na interrupção (10).

**Checagem de início de sessão (08, 10, 14)**
- A checagem de início de toda sessão (a de 08: estado do sync e divergência) também abre a nota do trabalho (10). No
  par, o hook lê o arquivo da vigia (faixa 7); sem ele, a ferramenta do MCP; no cliente, a ferramenta do MCP. Onde o hook
  falhar, vira regra no contrato daquele harness. Passou nos três, dentro e fora do Maestri, com o
  `MAESTRI_TERMINAL_ID` do próprio recruta (14).
- Como acha a nota: a pasta onde a sessão abre diz qual é o trabalho; quando não diz, o agente acha pela camada de busca,
  pelo nome que o Gustavo der, ou pergunta (10).

**Como a nota é gravada (11)**
- A nota existe desde a criação da iniciativa, então atualizá-la é troca de trecho no disco ou regravação inteira pelo
  `write_note` do MCP do banco com a versão lida; o hook da faixa 6 recusa a regravação inteira no disco. Com o banco
  fora, a troca de trecho segue, a regravação espera, e o agente avisa na resposta e anota a pendência na nota.

**Fronteiras com outras faixas (plano)**
- Esqueleto e esquema da nota: faixa 1 (usa o hub de ensaio na forma do 12, pronto antes da hora). Arquivo da vigia:
  faixa 7. Ferramenta do MCP de reserva: MCP do banco, faixa 5. Recusa da regravação inteira: faixa 6. Instalação dos
  hooks, do mod e do link do contrato: faixa 8, pelo contrato do instalador; esta faixa entrega script e fragmento de
  configuração próprios e não edita a configuração de outra.

### Testing decisions

- **Costura:** hub de ensaio (`C:\context-hub-ensaio` ou pasta de teste) com uma iniciativa de núcleo completo e HOME de
  ensaio pela variável do contrato do instalador; os harnesses reais em modo não interativo (`claude -p`, `codex exec`,
  `copilot -p`) e os scripts dos hooks chamados com eventos gravados. Só comportamento externo: o que o hook decide
  (devolve ou solta), o que entra no contexto da sessão nova e o que fica no disco.
- **Hook de fim, teste automatizado:** numa resposta que mudou o trabalho e deixou a nota sem refletir a mudança,
  devolve com a instrução de atualizar; depois da atualização, solta; numa pasta fora do hub, sai sem efeito; nos três
  harnesses, o mesmo evento dá a mesma decisão. "Ver se o arquivo mudou" é o critério mecânico proposto, não a
  definição de suficiência do 10; o que fazer numa resposta sem mudança no trabalho e a prevenção de laço seguem
  pendentes (ver Pontos abertos).
- **Hook de início, teste automatizado:** com o arquivo da vigia, a saída traz o estado do sync; sem ele, o estado vem
  da ferramenta do MCP; sem os dois, a saída diz que o estado está indisponível e não afirma que o sync foi conferido
  (14; a bancada de acesso devolveu "DESCONHECIDO" nesse caso, nos três harnesses). Nos três casos traz o conteúdo da
  `retomada.md` da iniciativa onde a sessão abre; aberto na raiz, não abre nota nenhuma e indica busca ou pergunta;
  fora do hub, sai sem efeito. O arquivo da vigia é um modelo de ensaio até a faixa 7 publicar o formato **[formato]**.
- **Banco fora:** com o MCP do banco parado, o agente atualiza a nota por troca de trecho e a pendência aparece nela.
- **Suficiência:** uma sessão nova de outro harness, aberta na mesma iniciativa, recebe a nota no contexto e diz o
  próximo passo da nota sem perguntar o que a nota já responde.
- **Aceite de ponta a ponta:** numa sessão `claude -p` com HOME de ensaio, aberta numa iniciativa do hub de ensaio, o
  agente faz uma tarefa curta; ao fim da resposta, `retomada.md` tem os sete campos e `next_step`; uma segunda sessão
  `claude -p` na mesma pasta começa com a nota no contexto; os testes automatizados dos dois hooks passam. Mesmo roteiro
  com `codex exec` e `copilot -p` onde o login no HOME de ensaio existir.

### Out of scope

- Revisão pós-sessão; FreeLLMAPI no checkpoint; desligar a memória automática do Claude (10).
- Produzir o arquivo da vigia e o estado do sync (faixa 7); a ferramenta do MCP de reserva (faixa 5); a recusa da
  regravação inteira (faixa 6); instalar hooks, mod, extensão e link do contrato no HOME real (faixa 8, e o HOME real só
  com o aval do Gustavo).
- O estado da vigia o tempo todo na tela (mod do Claude Code, `statusLine` do Copilot, `notify` do Codex: faixa 7).
- Aplicar o contrato às sessões desta frente de planejamento (10).
- O hub como lugar que controla harnesses e modelos, incluindo memória de trabalho contra o esquecimento de contexto
  (segundo mapa).

### Pontos abertos para a construção

- O critério mecânico de "a nota não reflete a resposta": o testado foi "solta quando a nota muda"; falta decidir o que
  fazer numa resposta que não mexeu no trabalho (só conversa), para não devolver toda resposta.
- Como um script sem IA sabe que "a memória privada ganhou algo que o hub não tem": quais arquivos de memória cada
  harness tem (a do Claude Code é conhecida; a do Codex e a do Copilot, não verificadas) e se basta ver que mudaram.
- Proteção contra laço de devolução (a resposta devolvida que devolve de novo).
- O mod de fim num Claude Code gerenciado pela empresa (não verificado, 14); o mod rodar em `claude -p` (não verificado).
- A extensão `onAgentStop` do Copilot depende de `--experimental`.
- Os hooks do Codex com acesso total (não verificado, 14); o `codex exec` desta máquina não gravava arquivo com o
  sandbox (erro do Windows), daí o `danger-full-access`.
- Os hooks no escopo do usuário: o teste do 11 usou o de projeto (não verificado, 11).
- Login de Codex e Copilot no HOME de ensaio (pergunta aberta do 16, rodada 2) **[formato]**.
- "Uma nota por trabalho" (10) contra uma `retomada.md` por iniciativa (12): vários trabalhos em paralelo na mesma
  iniciativa (recrutas do Maestri) e a retomada de trabalho fora de uma iniciativa seguem sem decisão.
- O cliente só de leitura não grava a nota de retomada; a gravação do cliente é ligável (11), mas a retomada pelo cliente
  não foi decidida.
- O campo onde entra a pendência com o banco fora (próximo passo, perguntas abertas ou `blocked_by`).
- O formato do arquivo da vigia (fronteira com a faixa 7) e o nome da ferramenta do MCP de reserva (fronteira com a
  faixa 5).
- O tamanho da nota no contexto da sessão nova (curta é regra, não limite).
- A ordem entre o checkpoint e o verificador da faixa 1 no mesmo fim de resposta.
- Onde fica a seção da regra de retomada em relação à cabeça de 2.000 caracteres do `AGENTS.md` (se entra na cabeça que
  o `instructions` do MCP leva aos clientes).
