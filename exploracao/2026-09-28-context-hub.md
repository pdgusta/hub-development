---
title: Exploração — organização do Maestri e context hub
status: exploração encerrada em 2026-09-30; insumo do mapa /wayfinder
iniciada_em: 2026-09-28
atualizado_em: 2026-09-30
origem: sessão Claude Code no workspace TRF3 (maestro)
---

# Exploração — organização do Maestri e context hub

> Rascunho vivo. Registra o levantamento, as ideias e as inclinações do Gustavo.
> Não é especificação: nada aqui foi aprovado para implementação.

## 1. Pedido

Organizar como workspaces e maestros do Maestri são criados e geridos, **arrumar os existentes**
e tratar de *context engineering*. Mesmo algo organizado vira "um monstro" se não houver faxina
manual. Entrega desejada: **fonte da verdade em arquivos + skill própria que executa**.

Dores confirmadas (todas):
- agentes com contexto errado;
- não saber o que existe;
- remontar equipe custa caro;
- contexto inchado;
- **falta de contrato file-first**: é preciso pedir ao modelo que salve o contexto antes do `/clear`.

## 2. Levantamento (2026-09-28)

- **Maestri 0.19.3.** Dados em `~/.maestri`:
  - `manifest.json`: workspaces;
  - `sidebar-layout.json`: barra lateral;
  - `preferences.json`: `agentPresets` (5 padrão, sem modelo) e `rolePresets` (20 papéis, todos com escopo de workspace, nenhum global);
  - `partituras/`: 1 modelo, desatualizado, da equipe VOEGOL;
  - `backups/`: de hora em hora.
- **Workspaces:** SOC, VOEGOL e TRF3 usam a mesma pasta, `C:\Projetos\maestri`. O videos-transcriptor tem pasta própria.
- **Efeitos da pasta compartilhada:**
  - papéis de SOC e VOEGOL misturados em `.maestri/roles`;
  - memória automática do Claude compartilhada (`~/.claude/projects/C--Projetos-maestri`);
  - nenhum CLAUDE.md.
- **Sobras:**
  - 7 pastas de papéis antigas em `ai-operating-system/.maestri/roles`;
  - «Revisor de Texto» registrado sem pasta;
  - bloco "CONTEXTO COMUM" colado em cada papel (pt-BR no SOC, pt-PT no VOEGOL);
  - papéis genéricos (Receptor, Gestor Git, Revisor Cruzado, Scripter) com codinomes e caminhos fixos.
- **Conhecimento de método espalhado:**
  - skills oficiais `maestri-workspace` e `maestri-manager`;
  - plano `~/.claude/plans/vc-o-orquestrador-harmonic-meerkat.md` (elenco GSD do videos-transcriptor);
  - memória `maestri-setup-voegol-cross-tenant.md` (pendente de revisão);
  - `soc-context/cases/PROTOCOLO-PARALELO.md`.
- **O vault `ai-operating-system`** já tem contrato file-first (DEC-0001, DEC-0015) e ciclo de sessão
  com checkpoint automático (`initiative-setup` 0.2, DEC-0018). Mas **não conhece o Maestri**, e o
  adaptador dele não carrega nos workspaces do Maestri. Já existe a iniciativa `trf3-intune`.

## 3. Diagnóstico

O monstro nasce de duas coisas: não há regra de **onde cada coisa nasce e quando morre**, e os
workspaces do Maestri não carregam contrato nenhum. Não é falta de organização inicial.

## 4. Inclinações do Gustavo

- O Maestri é **separado do vault**. O vault vai ser redesenhado, por isso não acoplar agora.
- Preocupação: dois sistemas com regras que divergem. Resposta: fronteira clara. Cada fato tem uma
  casa só, e o outro lado apenas aponta para ela.
- A abordagem A (hub com contrato de fronteira) faz mais sentido. Mas o momento é de **explorar**,
  já sabendo o que vai mudar.
- Quer o context hub numa segunda máquina, usado de qualquer lugar. Inclinado ao **cenário 2**:
  os agentes rodam onde ele está, e o hub fornece e recebe contexto.
- Quer os **arquivos nas duas máquinas, sempre sincronizados, e os modelos interagindo só com a Guild**.
- No hub mora **tudo, inclusive as iniciativas**, com a mecânica do Maestri no lugar mais adequado.

## 5. Mudanças já previstas (o desenho tem de absorvê-las)

| Mudança | O que ela exige desde já |
|---|---|
| Hub em outra máquina | nenhum caminho absoluto no contrato; estado do Maestri reconstruível |
| Redesenho do vault | o hub conhece o vault só por um localizador |
| Guild (índice/busca MCP) | Markdown com frontmatter consistente |
| Novas versões do Maestri | aplicar tudo pela CLI oficial, sem mexer em `~/.maestri` |
| Troca de modelos ou harness | contrato neutro (CLAUDE.md = AGENTS.md); modelo declarado no papel |
| Novos casos de uso | "tipo de workspace" como conceito explícito |

## 6. Ideias em discussão

### 6.1 Três camadas

1. **Conteúdo portátil**, texto em git: registro, papéis, blocos, modelos de equipe, contrato, macetes.
2. **Coisas presas à máquina**, declaradas num perfil por máquina (`machines/<host>.md`): caminhos,
   estado do Maestri, logins, terminais como o Cofre, SDKs.
3. **Estado derivado**, o que o Maestri guarda. Nunca é a verdade: a skill *aplica* e *audita*.

### 6.2 Guild como porta única do contexto — SUBSTITUÍDA em 2026-09-29 (ver seção 9)

- A Guild roda local em cada máquina (índice + escrita). O sync git entre máquinas é feito por ela.
- Toda escrita passa pela Guild: ela verifica a versão, grava, faz commit e sincroniza. Por isso o conflito é detectado.
- Regra: **contexto pela Guild, código pelo disco**, com `deny` nas ferramentas nativas sobre a pasta de contexto.
- Transição: até a Guild existir, os agentes acessam os mesmos arquivos direto, mais git. Depois só muda o caminho de acesso.
- Ressalva: iniciativas de cliente numa segunda máquina dependem da política da ARMIS e dos clientes.
  O desenho deve permitir pastas "só nesta máquina".

### 6.3 Pasta do workspace no Maestri

A pasta do workspace define o que carrega sozinho: diretório de trabalho, CLAUDE.md, memória automática,
`.maestri/roles`, `--from` e floors.

Proposta:
- **uma pasta fina por workspace**, dentro da parte Maestri do hub, apontando para a casa do conteúdo;
- workspaces de software usam o próprio repositório;
- `.maestri/` fica fora do git e é recriado pelo "aplicar".

### 6.4 Transportes considerados (cenário 2)

- **git**: recomendado agora, como verdade e transporte.
- **sincronização de pastas** (Syncthing/OneDrive): descartada, por causa dos conflitos silenciosos.
- **MCP no hub** (Guild): depois, por cima do mesmo repositório.

## 7. Rodada de 2026-09-28 — estrutura do context hub e local da skill

**Pergunta do Gustavo:** o hub fica em `C:\context-hub\`, e o `initiatives/` do vault vai para
`context-hub/context/initiatives/`? E as outras pastas do vault? Onde vive a skill do "aplicar"?

**Esclarecimento:** no esboço anterior, `context/` era **o vault inteiro** (charter, core, decisions,
knowledge, initiatives, operations, skills, templates…), não só `initiatives/`.

**Proposta em discussão:** `C:\context-hub\` é uma pasta-mãe, **não um repositório**. Dentro dela:

```
C:\context-hub\
├── vault\       ← o ai-operating-system atual, inteiro, com o seu git e histórico (redesenho acontece aqui)
├── maestri\     ← repositório novo: mecânica do Maestri
└── machine.md   ← perfil desta máquina (fora do git, ou em maestri\machines\<host>.md)
```

- **Vantagens:**
  - o vault não é mexido agora;
  - o redesenho dele segue independente;
  - a Guild indexa os dois;
  - o sync trata N repositórios.
- **Alternativa:** um repositório só, com o vault movido para dentro. Tem um sync só, mas mexe no
  vault e no histórico dele agora.
- **Repositórios de código** (videos-transcriptor, soc-as-code…) ficam onde estão. Eles têm remoto
  próprio, e o registro só aponta para eles.
- **Caminho:** um caminho curto, fora do OneDrive, para não haver sincronização dupla com git.
  Em cada máquina, o perfil traduz o nome lógico `hub:` para o caminho real.

**Skill do "aplicar":**
- O conteúdo fica único, em `maestri\skills\maestri-hub\`.
- Fica exposto **globalmente** por junction em `~/.claude/skills/maestri-hub` (e o equivalente para o Codex), sem cópia. É o mesmo padrão que o vault usa em `.agents/skills`.
- **Por que global:** workspaces de software abrem em repositórios fora do hub, e uma skill de projeto não seria encontrada lá.
- A lógica determinística fica num script em `maestri\tools\` que chama a CLI `maestri`. A skill é a camada fina de instruções e julgamento.
- O nome não pode colidir com as skills oficiais `maestri-*`, que o app reescreve a cada atualização.
- **Restrição:** `maestri workspace create` exige um terminal com Maestro Mode, então o "aplicar" roda a partir de um maestro.

## 7.1 Rodada de 2026-09-30 — objetivo reescrito e workspace próprio

**Pedido do Gustavo:** melhorar a frase do objetivo, que "não é exatamente isso com essas palavras".
Ele aceita que o context hub fique materialmente num dos computadores, o que tem mais disco, e seja
sincronizado para o outro. Os demais detalhes serão definidos ao longo do planejamento. Esta frente
deve ter um **workspace próprio no Maestri** até tudo estar definido e os contratos funcionando.

**Objetivo proposto (aguarda ajuste do Gustavo):**
> Ter um context hub único, com arquivos Markdown como fonte da verdade, hospedado no computador com
> mais disco e replicado no segundo, de forma que:
> 1. agentes (Claude Code, Codex, OpenCode, dentro ou fora do Maestri), em qualquer das duas máquinas,
>    achem o trecho certo sem ler tudo, por uma camada de busca;
> 2. o que importa seja gravado no lugar certo sem ele pedir, por um contrato file-first com zonas e checkpoint;
> 3. ele continue lendo e editando os mesmos arquivos no Obsidian;
> 4. nada diverja em silêncio entre as máquinas, e dado sensível não vá para onde não deve.

**Workspace aprovado em 2026-09-30:** `Context Hub`, com pasta `C:\Projetos\context-hub` + `git init`.
Esta exploração será o primeiro documento. A pasta serve **só para planejar**; o local real do hub é
uma decisão do planejamento.

**Em aberto:** qual das máquinas tem o disco maior: o notebook da ARMIS ou o outro?

## 7.2 Onde está o contexto desta sessão (levantado em 2026-09-30)

| O quê | Onde | Zona |
|---|---|---|
| Este arquivo | `C:\Projetos\context-hub\exploracao\2026-09-28-context-hub.md` (movido de `C:\Projetos\maestri\_exploracao\` em 2026-09-30) | canônica |
| Relatórios integrais das 3 varreduras | `exploracao\anexos\varredura-{1,2,3}-*.md` (extraídos da transcrição em 2026-09-30) | canônica (anexos) |
| Transcrição da conversa | `~/.claude/projects/C--Projetos-maestri/3be42b76-….jsonl` + pasta de mesmo nome (cerca de 6 MB) | derivada; o Claude Code apaga transcrições antigas (`cleanupPeriodDays`) |
| READMEs e materiais baixados | `%TEMP%\claude\C--Projetos-maestri\3be42b76-…\scratchpad\` | efêmera |
| Memória automática do projeto | `~/.claude/projects/C--Projetos-maestri/memory/`, **compartilhada** com SOC, VOEGOL e SBF | nada desta sessão foi gravado lá |
| Alteração feita fora da exploração | skill renomeada para `matt-code-review` (`~/.agents/skills/`), com backup do lock | — |

## 8. Perguntas em aberto

- Um repositório ou pasta-mãe com vários? (inclinação atual: pasta-mãe)
- ~~Onde fica o trabalho do SOC (`soc-context`)?~~ **Respondido em 2026-09-29:** o SOC é uma iniciativa.
- Política de dados de cliente na segunda máquina.
- Zona "trabalho": sincroniza entre máquinas ou fica só local? A Guild indexa?

## 9. Rodada de 2026-09-29 — como a Guild funciona e o risco de emaranhado

**Pergunta do Gustavo:** mesmo com o vault em disco nas duas máquinas e a Guild como RAG, haverá
casos de escrita direta em disco, outros pela Guild, e muita coisa no scratchpad da sessão.
Isso não vira um emaranhado?

**Correção do desenho (substitui a 6.2):** a Guild **não é porta de escrita nem faz sync**.
- **O disco é a única verdade.** Os agentes gravam sempre no disco (Edit/Write), relendo antes de gravar.
- **A Guild é uma lente de leitura:** observa os arquivos, indexa e responde a buscas por MCP. O índice
  (SQLite) é derivado, fica em cada máquina e é reconstruível. Não se sincroniza.
- **O git sincroniza os arquivos** entre máquinas, a cada checkpoint e por uma routine periódica.
- Cada peça tem uma função só, e nenhuma guarda conteúdo que não esteja no disco.

**Funcionamento da Guild (conceitual, conforme o desenho da outra conversa):**
1. Um watcher detecta o arquivo criado ou alterado.
2. O arquivo é cortado por títulos (seções) e o frontmatter vira metadado.
3. A indexação é híbrida: texto completo (palavras exatas: IDs, cmdlets, nomes de tabela) + embeddings (sentido).
4. A busca por MCP devolve caminho + seção + trecho + pontuação, e não o arquivo inteiro.
5. O agente abre só a seção necessária e, se for alterar, grava no disco. O watcher reindexa.

**Quatro zonas por ciclo de vida (a regra que evita o emaranhado):**

| Zona | Exemplos | Quem grava e quando | Indexada pela Guild | Sincronizada |
|---|---|---|---|---|
| Canônica | initiative.md, decisões, conhecimento, papéis, contrato | o agente dono, no checkpoint, direto no disco | sim | sim (git) |
| Trabalho | case.md, queries, CSVs, prints, scripts, rascunhos | os agentes durante a tarefa | a decidir | a decidir (dado sensível) |
| Efêmera | scratchpad, Temp, Maestri-drops, saídas de teste | qualquer um, a qualquer momento | nunca | nunca |
| Derivada | índice da Guild, `~/.maestri`, memória privada do Claude | ferramentas | — | nunca (é reconstruível) |

- **A única ponte da efêmera para as outras zonas é o checkpoint do contrato**, que promove o que importa.
  O que não foi promovido morre com a sessão, e isso é esperado.
- **O scratchpad nunca é citado como fonte.**
- **A memória privada da ferramenta** é transitória (como já diz a DEC-0015 do vault). Nada importante mora só nela.

> **Aviso (2026-09-29):** a descrição da Guild nesta seção veio da conversa com outro modelo e
> **não bate com o README**. Ver a seção 10.

## 10. Pesquisa de 2026-09-29 — o que a Guild realmente é (com fontes)

### 10.1 Guild — [mathomhaus/guild](https://github.com/mathomhaus/guild)

Verificado no README original em 2026-09-29.

- **O que é:** um binário Go com servidor MCP e SQLite embutido. *"State lives strictly on local host;
  nothing leaves your machine."* O estado fica em `~/.guild/`.
- **Não indexa uma pasta de Markdown.** Tem uma base própria, alimentada pelos agentes por ferramentas
  MCP, com quatro primitivas:
  - **Quest**: tarefa com dependências e claim atômico;
  - **Lore**: conhecimento com tipo (`observation`, `decision`, `research`, `principle`, `idea`) e
    envelhecimento automático (research em 30 dias, decision em 180);
  - **Oath**: os princípios, carregados em toda sessão;
  - **Brief**: o handoff para a próxima sessão.
- **Busca:** BM25 + vetores, fundidos por RRF. **No Windows, o binário pré-compilado faz só busca por
  palavra-chave**, porque a busca vetorial está desativada (`onnxruntime-purego` não suporta Windows).
- **Sync entre máquinas, exportação ou importação:** não são mencionados.
- **Maturidade:** v0.3.2 (2026-05-27), criada em 2026-04, 302 estrelas, último push em 2026-09-14, licença Apache 2.0.
- **Ideia aproveitável:** a seção "Where writes go" separa as escritas por tempo de vida: journal (só
  esta tarefa), lore (outros agentes) e brief (a próxima sessão). O teste que ela propõe é
  *"who else needs this?"*. É o mesmo princípio das zonas da seção 9.
- **Conflito com o file-first:** a Guild seria uma segunda fonte da verdade em SQLite, que não é
  legível no Obsidian nem versionada em git.

**E o guild.ai?** Também foi verificado ([site](https://www.guild.ai), [plataforma](https://www.guild.ai/platform)).
É outro produto: um **serviço na nuvem** que se apresenta como "control plane for AI agents",
com governança, auditoria, custos e um MCP Gateway, voltado a empresas com agentes em produção.
Não é binário local, e não menciona Go, SQLite, indexação de Markdown nem sync de vault.
A descrição da outra conversa ("binário Go local com SQLite, busca híbrida por MCP") corresponde
ao mathomhaus/guild na forma, mas **nenhum dos dois indexa um vault de Markdown**.

### 10.2 O que faz o que foi atribuído à Guild — [pvliesdonk/markdown-vault-mcp](https://github.com/pvliesdonk/markdown-vault-mcp)

Verificado no README original em 2026-09-29.

- Indexa **no lugar** uma pasta de Markdown (`MARKDOWN_VAULT_MCP_SOURCE_DIR`). A identidade do documento é o caminho relativo.
- **Busca híbrida:** SQLite FTS5 (BM25, porter stemming) + embeddings (FastEmbed local, Ollama, OpenAI,
  Voyage ou endpoint compatível), fundidos por RRF. Filtros por frontmatter, cortes por título e
  `read(path, section=heading)`.
- **Reindexação:** incremental, por hash, com reconciliação no arranque. O watcher (`watchdog`) é
  opcional e **é desligado automaticamente quando o pull loop do git está ativo**.
- **Escrita:** as ferramentas de escrita gravam no disco. Há proteção por etag (`if_match`) ao
  sobrescrever, e um modo `READ_ONLY=true` que esconde as ferramentas de escrita.
- **Git gerenciado:** clone, pull loop, um commit por escrita, push adiado e aviso quando o remoto está inacessível.
- **Transporte:** stdio ou HTTP, com bearer ou OIDC.
- **Plataforma e maturidade:** Python 3.11–3.14 em Linux, macOS e Windows. v5.0.0 (2026-09-27),
  criado em 2026-03, 34 estrelas, licença MIT. É uma comunidade pequena com versões maiores rápidas,
  então é preciso fixar a versão.

### 10.4 Protocolo de varredura (2026-09-29)

Contexto: o Gustavo notou que buscas anteriores por "apps com canvas e orquestração multi-agent"
nunca trouxeram o Maestri. A minha primeira "prova" usou o vocabulário do próprio Maestri e foi
**descartada, por viés de confirmação**.

Protocolo adotado:
- requisitos explícitos;
- 12 a 15 consultas no mínimo, com formulações diferentes e em várias línguas;
- fontes nomeadas (GitHub, listas awesome, registros MCP, HN, Reddit, Product Hunt);
- verificação na fonte primária;
- registro de todas as consultas, para auditar a cobertura;
- **teste cego**: quem busca não conhece a resposta esperada.

Três varreduras lançadas em paralelo, por agentes sem o contexto desta conversa (resultados pendentes):
1. **Calibração cega**, com o pedido original do Gustavo. O Maestri aparece?
2. **Camada de contexto sobre Markdown**, contra os requisitos R1–R7.
3. **Ferramentas de memória e contexto para agentes**, e se convivem com o Markdown como fonte.

### 10.4.1 Resultado das varreduras (2026-09-29)

- **Calibração cega:** inconclusiva e descartada. O agente buscou o Maestri pelo nome logo na 2ª consulta.
- **Categoria "memória de agentes" (cerca de 45 ferramentas):** a Guild é da classe "base própria fechada".
  As que se parecem com a Guild e mantêm Markdown como verdade:
  - **akitaonrails/ai-memory**, conferido no README:
    - wiki `.md` em git como fonte da verdade;
    - handoff "claimed exactly once";
    - decaimento sem LLM;
    - servidor próprio para várias máquinas;
    - Windows nativo "Experimental";
    - captura prompts e chamadas de ferramentas por hooks;
    - é memória "deste repositório", não um vault geral;
    - MIT, 8,6 mil estrelas.
  - **seamless:** tarefas + Markdown, 5 estrelas.
  - **beads:** Dolt + git, não é Markdown.
- **Categoria "camada sobre o vault" (47 ferramentas, 45 verificadas pelo agente):** só o
  **markdown-vault-mcp** cumpre R1–R6 no papel.
  - **Correção:** eu tinha dito que ele "roda no Windows". Isso veio de um resumo do WebFetch.
    O README não menciona Windows e o CI é só Ubuntu.
  - **grooveseek**, conferido no README:
    - binário `x86_64-pc-windows-msvc`, com ONNX e SQLite estáticos;
    - cortes por título e filtros de frontmatter;
    - o watcher cobre `git pull`;
    - `bge-m3` para texto não inglês;
    - MIT/Apache-2.0, 8 estrelas;
    - tempos medidos pelo autor num Windows: 3,1–3,6 s pela CLI e cerca de 0,1 s pelo daemon, sem rerank.
  - **obsidian-hybrid-search**, conferido no README:
    - modelo `multilingual-e5-small` offline;
    - filtro de frontmatter na CLI;
    - o banco fica **dentro do vault** por padrão;
    - 107 estrelas.
  - **qmd:** 30 mil estrelas, mas o Windows não é suportado oficialmente (segundo o agente, não conferido).

### 10.4.2 Conclusão da exploração da "Guild"

1. **A Guild não atende o requisito central:** ela não usa o Markdown como fonte. Aproveitam-se os
   conceitos: escritas por tempo de vida (journal/lore/brief), oath e envelhecimento por tipo.
2. **O que se imaginou como "Guild" são dois papéis diferentes**, e nenhuma ferramenta faz bem os dois:
   - (a) **lente de busca sobre o vault**: markdown-vault-mcp, grooveseek, obsidian-hybrid-search;
   - (b) **memória, handoff e tarefas entre sessões**: ai-memory, seamless, beads, ou o próprio
     contrato file-first (zonas + checkpoint) em arquivos.
3. **Próximo passo possível:** um spike no Windows com 2 candidatas de (a), sobre uma **cópia** do
   vault, medindo a qualidade em pt-BR, a instalação e o comportamento com `git pull`.

### 10.4.3 Busca de skills (`find-skills`, 2026-09-30)

Foram 15 consultas no registro skills.sh. O registro ordena por instalações, e as skills do Lark e
da Feishu dominam os resultados. **Nenhuma skill resolve sincronização + busca por agentes.** Isso é
infraestrutura (git + MCP de busca), e skill só ensina o agente a trabalhar sobre ela.
Complementos lidos:
- **kepano/obsidian-skills** (`obsidian-markdown`, `obsidian-cli`, `obsidian-bases`): cerca de 88 mil
  instalações. Ensinam o agente a escrever Markdown do Obsidian corretamente e a usar a CLI oficial.
- **anthropics/skills@mcp-builder**: cerca de 120 mil instalações. Só se for preciso construir um MCP próprio.
- **othmanadi/planning-with-files**: cerca de 45 mil instalações. Planejamento em arquivos com hooks
  (UserPromptSubmit/PreToolUse/Stop/PreCompact). Aborda o "salvar antes do /clear", mas é invasiva
  (hook em toda chamada de ferramenta).
- **karpathy-llm-wiki**, **second-brain**, **obsidian-wiki**: padrões de "LLM wiki" (raw → wiki
  compilada). Sobrepõem-se ao redesenho do vault.
- **mattpocock/skills@obsidian-vault**: descartada. Está presa ao vault pessoal do autor (`/mnt/d/Obsidian Vault/AI Research/`).

### 10.5 Limites do Claude Code relevantes (documentação oficial)

- As regras `deny` de Read/Edit valem para as ferramentas nativas e para comandos de arquivo
  reconhecidos no Bash (`cat`, `sed`…), mas **não para scripts** (Python, Node) que abrem arquivos
  sozinhos. Para bloquear no nível do sistema, é preciso o sandbox.
  ([permissions](https://code.claude.com/docs/en/permissions))
- O CLAUDE.md orienta, mas não obriga (*"not a hard enforcement layer"*). Para impor algo, usa-se hook.
- A memória automática fica em `~/.claude/projects/<projeto>/memory/`, por repositório git (ou pela
  raiz do projeto), e **é local da máquina**, sem compartilhamento entre máquinas. Pode ser desligada
  (`autoMemoryEnabled`) ou redirecionada (`autoMemoryDirectory`). ([memory](https://code.claude.com/docs/en/memory))
- O CLAUDE.md carrega da pasta de trabalho e das pastas acima. Diretórios de `--add-dir` não carregam
  CLAUDE.md, a não ser com `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. `additionalDirectories`
  nos settings só dá acesso a arquivos.

## 11. Encerramento da exploração (2026-09-30)

**Decisão do Gustavo:** esta frente segue **só o fluxo do Matt Pocock** (`/ask-matt`): `/wayfinder` →
`/to-spec` → `/to-tickets` → `/implement`. O caminho superpowers (brainstorming → especificação →
writing-plans) foi encerrado aqui para não manter dois processos sobre as mesmas decisões. O GSD
também não é usado nesta frente.

**Feito:**
- workspace próprio `Context Hub` no Maestri, com pasta `C:\Projetos\context-hub` (git iniciado, sem commits);
- este arquivo movido para cá;
- relatórios integrais das varreduras salvos em `anexos/`.

**Workspaces no Maestri:**
- O workspace de origem desta sessão era o "TRF3". Ele foi renomeado para "context-hub" (fora desta
  sessão), e em 2026-09-30 renomeei-o para **"context-hub (antigo)"**. A pasta dele continua sendo a
  compartilhada, `C:\Projetos\maestri`.
- Criei o workspace novo **"Context Hub"** com pasta `C:\Projetos\context-hub`, na raiz da barra lateral.
- O "context-hub (antigo)" deve ser apagado pela interface depois do `/handoff`, porque a CLI não apaga.

**Próximos passos (só o Gustavo pode invocar estas skills):**
1. `/handoff` na sessão de origem (workspace "context-hub (antigo)"), para semear a sessão nova.
2. Na sessão nova, no workspace `Context Hub`: `/setup-matt-pocock-skills` (sugestão: tracker de Markdown local).
3. `/wayfinder`, com o destino = objetivo da seção 7.1. Candidatos a tickets de decisão:
   - máquina que hospeda o hub (qual tem o disco maior);
   - transporte de sincronização;
   - camada de busca (spike grooveseek × markdown-vault-mcp via `/prototype`);
   - contrato file-first e zonas;
   - modelo de pasta do workspace no Maestri;
   - skill de aplicar e auditar;
   - migração dos 4 workspaces (SOC, VOEGOL, TRF3, videos-transcriptor; agora também SBF);
   - política de dados de cliente;
   - convivência dos frameworks de processo (superpowers, GSD, Matt) fora desta frente;
   - **como as decisões deste repositório chegam ao hub final** (ver §12): este repositório é prova
     de conceito e o hub nasce do zero; falta decidir o que migra, em que forma, e como evitar duas
     casas para o mesmo fato. Até lá, ele existe só nesta máquina, sem remoto;
   - **Windows (`C:\context-hub`) ou WSL** como sistema onde o hub mora (ver §12).

## 12. Rodada de 2026-09-30 — este repositório é prova de conceito

**Decisão do Gustavo:** `C:\Projetos\context-hub` é **só a prova de conceito**. O objetivo final é
criar o hub **do zero** em `C:\context-hub`, **ou dentro do WSL, se for mais viável**. Ele quer achar o
mais adequado às necessidades dele: **nenhuma decisão está fechada**.

- O setup das skills do Matt é feito aqui como se fosse o de verdade (ensaio do que o hub terá).
- Substitui a recomendação anterior (no chat) de tratar este repositório como embrião do hub.
- Setup (`/setup-matt-pocock-skills`): tracker de Markdown local em `.scratch/` (padrão das skills),
  rótulos de triagem padrão, documentação de domínio com contexto único.

