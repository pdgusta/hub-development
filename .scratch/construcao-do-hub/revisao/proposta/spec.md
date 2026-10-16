# Spec: a construção do context hub, primeira execução

Status: ready-for-agent

Fonte: as decisões dos tickets resolvidos do mapa `.scratch/context-hub/map.md` (seção "Decisions so far") e os
comentários do ticket 16 ("Passagem para a construção"). Escrita pelo maestro com subagentes, em 2026-10-15, por
`/to-spec`; os workers corrigem os erros na parte da sua faixa (pedido do Gustavo). Organizada pelas 10 faixas verticais
do plano de execução (`planejamento/plano.md`): cada faixa vira um grupo de tickets de um worker.

Marcas desta proposta (revisão conversada de 2026-10-16, `revisao/acordo.md`): **[núcleo]** = escolha do núcleo sem
ticket resolvido, que pede o aval do Gustavo; **[formato]** = depende do formato da execução (minutos, dublês, "se
couber", portas de ensaio por faixa, dono de passo), que o Gustavo ajusta no plano; **[ticket aberto: 56]** = vem de
rodada respondida do laço do system design, que só continua depois da construção, e fica fora desta construção.

## Problem Statement

O Gustavo trabalha com muitos agentes (Claude Code, Codex, Copilot, Claude Desktop) em duas máquinas Windows, para
vários clientes e iniciativas. O que cada agente sabe se perde entre sessões, entre harnesses e entre máquinas: notas no
vault antigo sem padrão, retomadas que dependem da memória privada de um agente, buscas que não acham, sync que falha em
silêncio, regras escritas no `AGENTS.md` que agentes menores ignoram. Depois de semanas de decisões na prova de conceito,
nada disso existe ainda como coisa que funciona.

## Solution

O hub nasce em `C:\context-hub`: uma árvore de pastas com padrão imposto por mecanismo, que todo agente de qualquer
harness encontra, lê pela busca, grava com segurança e retoma de onde outro parou; um banco por máquina que replica entre
os pares; uma vigia que nunca deixa uma falha passar calada; e kits que montam um par ou ligam um cliente com o mínimo de
passos. Nesta primeira execução (1 hora, 10 workers em paralelo **[formato]**), cada faixa entrega uma fatia funcionando de ponta a
ponta **no par 1 (esta máquina), num hub de ensaio e num HOME de ensaio**; o que exige a segunda máquina, arquivo global
de verdade ou serviço de verdade fica como ticket do Gustavo.

## User Stories

(por faixa: na seção "Faixas" abaixo e, com a lista longa, em `spec-partes/`)

## Implementation Decisions (comuns a todas as faixas)

- **Hub de ensaio e HOME de ensaio.** Toda faixa constrói e testa contra uma cópia de ensaio do hub (na forma decidida
  no ticket 12: seis raízes, duas iniciativas com o núcleo, notas em pt-BR, um binário pequeno) e contra um HOME de ensaio
  apontado por variável de ambiente; nunca contra `~/.claude`, `~/.codex`, `~/.copilot` de verdade. A instalação de verdade
  é um ticket `ready-for-human`, com cópia e hash antes.
- **Contrato do instalador** (proposta do Worker 2, no plano): cada faixa entrega o seu passo do kit de par, idempotente,
  que lê o HOME de ensaio da variável, nunca de `~`, e aceita simulação. A faixa 8 só os enfileira; ninguém espera o kit.
- **Hooks no mesmo evento:** as faixas que registram hooks (retomada, guardas, skills) entregam cada uma o seu script e
  um fragmento de configuração; a faixa 8 junta os fragmentos. Nenhuma faixa edita a configuração de outra.
- **Bancos de ensaio por faixa:** cada faixa que precisa de CouchDB sobe o seu, descartável, em porta própria, pelo mesmo
  compose que a faixa 4 publica primeiro.
- **Ramos e pastas:** cada worker trabalha no seu ramo e na sua pasta (git worktree) do repositório do hub; a junção é
  feita depois da revisão dos dois Prumos.
- **Registro para o painel:** a execução grava eventos para o painel da construção pelo formato de
  `painel/contrato.md`, por hooks de projeto (não globais); o painel só lê.

## Testing Decisions (comuns)

- **Uma costura só, a mais alta:** o comportamento de ponta a ponta, visto de fora, no hub de ensaio com HOME de ensaio,
  exercido pelos harnesses reais em modo não interativo (Claude Code `-p`, Codex `exec`, Copilot `-p`), pelo MCP e pelos
  scripts dos kits. Nada de testar detalhe interno de implementação.
- Cada faixa tem um critério de aceite de ponta a ponta, que o Prumo da construção confere rodando.
- Arte anterior: as bancadas da prova de conceito (`.scratch/context-hub/bancada-*.md`) testaram os mesmos mecanismos
  (hooks que recusam, MCP, LiveSync com dois CouchDB) e servem de modelo de teste.

## Out of Scope (comum)

- A segunda máquina (o notebook) e tudo que só se prova com dois pares físicos: tickets do Gustavo. (A consulta ao TI
  caiu: o TI confirmou que o Tailscale no notebook não tem risco nem conflito com o software corporativo; ticket 16,
  2026-10-16.)
- O que vem só do ticket 56 (prazo de 30 dias do `_archive/`, "remover = arquivar", política de recuperação, "dois dias
  de distância bastam", quem percebe a falha): **[ticket aberto: 56]**, fora desta construção.
- Instalar em arquivo global de verdade ou ligar serviço de verdade sem o aval do Gustavo.
- Migrar o vault e os workspaces existentes do Maestri.
- O portal da prova de conceito e os laços de pesquisa.

## Further Notes

- A execução dura 1 hora no total; o que não couber fica para a próxima execução, anotado no plano. **[formato]**
- Tarefa muito complexa ganha um subagente Fable 5.1 médio. **[formato]**
- **Perguntas da rodada 2 do ticket 16 ainda sem resposta:** login dos harnesses no HOME de ensaio; copiar os pilotos do
  vault; autorização e cota para o teste único do gemini pelo FreeLLMAPI (o desenho "configurado, testado uma vez,
  desligado" é decisão do 09 e não se reabre). A pergunta do Docker de ensaio foi respondida: o Gustavo vai ligar o
  Docker Desktop e criar o repositório privado do hub no GitHub (16, 2026-10-16); isso responde quem prepara, não prova
  que está pronto. Onde o spec depende dessas perguntas, está marcado **[formato]**.
- **Se cada faixa virar uma etapa sequencial** (ideia inicial do Gustavo, 16, 2026-10-16): cada etapa usa a entrega
  real da anterior, e os dublês só ficam onde o real exige a segunda máquina; "entrega cedo no minuto N" vira "a etapa
  anterior entrega"; os "se couber" (validação de frontmatter no MCP, Config Doctor, ponte do Desktop) são requisitos
  dos tickets 12, 33 e 11 e voltam a entrega cheia; as portas de CouchDB de ensaio por faixa (5994 a 5997) podem virar um
  banco de ensaio só. A ordem das etapas é do Gustavo.

## Faixas (user stories, decisões e testes por faixa)

Cada faixa é de um worker e vira um ticket vertical. O texto de cada uma veio do plano de execução que os 12 recrutas
fecharam na volta 1 da rodada Ralph. A lista longa de user stories e as decisões de cada faixa estão nas partes desta
spec, em `spec-partes/` (faixas 1-2: 100 user stories; 3-4: 74; 5-6: 64; 7-8: 72; 9-10: 88), com as contradições entre
tickets que cada parte achou. Os workers corrigem a parte da sua faixa.

**Alcance da marca [formato] nos blocos abaixo:** todos os donos por worker, os minutos, os dublês, as portas de ensaio
por faixa, os "entrega cedo", os "se sobrar" e os cortes de tempo em "O que constrói", "Como se prova" e "Como segue
sem esperar as outras faixas" são referência do plano anterior e dependem do formato da execução; não dispensam os
requisitos dos tickets. A marca não se repete a cada ocorrência.

### Worker 1

**O que constrói (implementation decisions):** **Esqueleto, contrato e frontmatter** (faixa 1 do corte candidato): `C:\context-hub` com `.git` e sem `CLAUDE.md` no hub nem acima; o `AGENTS.md` (contrato file-first, zonas, porta de entrada pela busca, como gravar); as seis raízes em inglês com `_archive/`; `agents/blocks.md`; esquemas por tipo em `agents/frontmatter/`; o verificador; o script que cria iniciativa com o núcleo de seis arquivos e o `index.md` (`summary: auto`, `local`)

**Como se prova (testing decisions, de ponta a ponta):** `agents/bin/nova-iniciativa` cria uma iniciativa de ensaio com o núcleo de seis arquivos; `agents/bin/verificar-frontmatter` aceita a nota certa e recusa a sem `status` ou com `stage` fora do ciclo; um `verificar-hub` passa no hub inteiro (estrutura, frontmatter, nenhum `CLAUDE.md`); testes automatizados

**Como segue sem esperar as outras faixas:** nada; entrega cedo o que os outros chamam: no min 0–10, os nomes e a assinatura do verificador (fronteiras abaixo); até lá, as faixas usam o hub de ensaio e um verificador dublê

### Worker 2

**O que constrói (implementation decisions):** Retomada e checkpoint (ticket 10): nota de retomada de sete campos por trabalho, hook de fim de resposta que a grava e leva ao hub o que só a memória privada sabe, checagem de início de sessão que a abre

**Como se prova (testing decisions, de ponta a ponta):** numa sessão `claude -p` com HOME de ensaio, aberta numa iniciativa do hub de ensaio: o fim da resposta deixa `retomada.md` com os sete campos; a sessão seguinte começa com a nota no contexto; teste automatizado dos dois hooks

**Como segue sem esperar as outras faixas:** o esqueleto de pastas (faixa 1): usa a forma decidida no ticket 12 sobre o hub de ensaio pronto antes da hora; o instalador segue o contrato do kit (faixa 8)

### Worker 3

**O que constrói (implementation decisions):** **Busca** (faixa 3 do corte; Answers dos tickets 09 e 54, lacunas do Prumo para a faixa 3): (a) `kit/par/03-busca.ps1` no contrato do kit: instala o obsidian-hybrid-search **0.16.2 fixo** com `npm install` local em `C:\context-hub\.local\busca\` (nunca `-g`), com `-WhatIf`; (b) `busca/iniciar.ps1` sobe `ohs serve --foreground` em `127.0.0.1:3939` (padrão do README 0.16.2, rota `/mcp`, HTTP sem estado) sobre o hub, com `LOCAL_EMBEDDING_MODEL=Snowflake/snowflake-arctic-embed-m-v2.0` (variável provada na bancada, `bancada-busca/scripts/robusta/ohs-modelo.py`; **não está no README**) e `OBSIDIAN_IGNORE_PATTERNS` com `**/.*/**` e `**/.*` (o que tem ponto, como no LiveSync; mecanismo proposto para o requisito do 12, a conferir) mais o que o gerador de exclusões (atribuído à faixa 1 **[formato]**) gerar para `local: true`; um analisador só, sem campo de idioma; (c) o `.obsidian-hybrid-search.db` (e `-wal`/`-shm`) fora do git e do LiveSync (o `--db` não move o banco, achado da bancada); (d) a configuração do gemini-embedding-001 pelo FreeLLMAPI (`OPENAI_BASE_URL` = `$env:FREELLM_BASE_URL/v1`, nunca `localhost:3001` fixo; `OPENAI_EMBEDDING_MODEL`), escrita em `busca/gemini.env` e **desligada**; testada uma vez num segundo índice, numa cópia do hub de ensaio em porta 3940 (o `--db` não separa índice), se o Gustavo liberar a cota; (e) escreve `HUB_MCP_BUSCA_URL=http://127.0.0.1:3939/mcp` no `.env.modelo` do kit no minuto 5. Ligar no boot (tarefa agendada) fica `ready-for-human`

**Como se prova (testing decisions, de ponta a ponta):** `busca/testes/aceite.mjs` (Node ≥ 22, sem pacote de fora, MCP Streamable HTTP por `fetch`: `initialize` e `tools/call search`) contra o hub de ensaio: uma pergunta em pt-BR por palavra (`fulltext`) e uma por paráfrase sem palavra em comum (`semantic`) acham a nota esperada entre as 3 primeiras **[núcleo]**; uma nota criada no disco durante o teste aparece na busca em até 60 s **[núcleo]** (mede e grava o tempo; a bancada do 09 mediu acerto nos 5 primeiros e posição, sem fixar limite); nada com ponto no caminho nem de pasta `local: true` aparece; `status` mostra indexadas = `.md` válidos, e a lista das recusadas por YAML inválido sai no relatório **[núcleo]**; pedido com `Host` estranho é recusado. Roda duas vezes seguidas (a segunda reaproveita o índice)

**Como segue sem esperar as outras faixas:** hub de ensaio (Worker 2): copio no minuto 0 e escrevo as notas e as perguntas de aceite eu mesmo, sem esperar a faixa 1; exclusão de `local: true` (faixa 1): leio a lista gerada se existir, senão só o padrão de ponto, e entra na segunda passada; kit (faixa 8): só a URL no `.env.modelo` e o meu `03-busca.ps1`; `.gitignore` da raiz (faixa 1): pede a linha `.obsidian-hybrid-search.db*`; atenção, o obsidian-hybrid-search respeita o `.gitignore` por padrão (`OBSIDIAN_RESPECT_GITIGNORE=true`, README 0.16.2), então o que a faixa 1 puser lá também sai da busca; proxy (faixa 10): ela usa a URL; um dublê não é preciso, o servidor de verdade sobe no minuto 10–15; **não verificado** se o TBXark/mcp-proxy repassa o `Host` do cliente (o servidor só aceita os `Host` permitidos): a busca é testada pelo proxy e, se preciso, o `--allowed-host` recebe o `Host` realmente observado, não um endereço ou porta presumido **[núcleo]** (quem configura é **[formato]**); a baixa do modelo arctic (tamanho não medido) começa no minuto 0, em segundo plano; LiveSync (faixa 4): não preciso dele; o tempo "edição no par B → busca no par B" fica para o teste de aceite final, se as duas faixas terminarem

### Worker 4

**O que constrói (implementation decisions):** **Banco e vista `.md`** (faixa 4 do corte; tickets 25, 33, 34, 47, 48 e comentários de 2026-10-13 e 2026-10-14 do 16): par A e par B de ensaio nesta máquina, cada um com o seu CouchDB 3.5.2 (contêineres `hub-ensaio-04-a` e `-b`, portas 5994 e 5995 em 127.0.0.1, usuário e senha de ensaio gerados, nada copiado do spike) e uma replicação de envio em cada um (S3); o sincronizador é o CLI do LiveSync (build do commit `14141446` do spike, sem recompilar), configurado pelo caminho dos testes oficiais (`init-settings`, `remote-add`), um dispositivo por par aceito com `mark-resolved`, **E2EE** (34), com caminho ofuscado como no teste do 48 **[núcleo]**, `syncMaxSizeInMB` 200, exclusão de tudo que tem ponto em qualquer nível pelo `.livesync/ignore` (linhas `.*` e `.*/`; ver fronteira da volta 2); roda em laço no terminal, e a tarefa agendada (requisito do 33) sai como XML **[formato]**. Tudo sobe por `kit/par/04-banco.ps1`. Caminhos da faixa: `kit/par/banco/**`, `kit/par/04-banco.ps1`, `kit/par/env/04.env`, `agents/test/04-banco.ps1`, `execucao/ensaio/banco/`

**Como se prova (testing decisions, de ponta a ponta):** prova: `pwsh agents/test/04-banco.ps1`, em ordem de corte. **Núcleo (min 0–35):** (N1) o kit sobe os dois CouchDB e as duas replicações, e o `_scheduler/docs` de cada um mostra a sua em `running`; (N2) nota criada na pasta A aparece na B, e a editada na B volta à A, em até 30 s, sem texto claro nos documentos crus do CouchDB; (N3) a mesma linha editada nos dois pares com a replicação pausada vira `_conflicts` nos dois CouchDB, sem versão perdida; (N4) `.oculto/x.md`, `.env`, `projeto/.git/config`, `projeto/.venv/x` e `projeto/.secrets/x` não chegam ao banco, com o CLI rodando **e** na varredura de partida depois de reiniciá-lo. **Se sobrar (min 35–50), nesta ordem:** (S1) 60 MiB viaja, 201 MiB não; (S2) colisão de binário deixa a perdida num ramo apagado; (S3) o kit roda de novo sem mudar nada e o `-WhatIf` não grava; (S4) CLI morto e CouchDB fora na partida: o laço religa; (S5) retrato do banco de ensaio (conflito aberto, binário com ramo apagado, `_scheduler/docs` parado) em `execucao/ensaio/banco/`, para as faixas 5 e 7 na próxima execução; (S6) `claude -p` grava na pasta A e chega à B (só com o login de ensaio)

**Como segue sem esperar as outras faixas:** nada para começar. Entrega cedo: no min 0–10, `kit/par/banco/compose.yml` e `kit/par/env/04.env` (fronteira "Banco de ensaio"); no min 15, `execucao/ensaio/banco/scheduler-docs-em-dia.json` e `scheduler-docs-parado.json` tirados do CouchDB de ensaio (pedidos dos Workers 10 e 7), que até lá usam os seus dublês. O hub de ensaio (Worker 2) é o conteúdo das pastas A e B. Detalhe e fontes em `spec-partes/faixas-03-04.md` e na fronteira
"Worker 4 (volta 2)" do plano.

### Worker 5

**O que constrói (implementation decisions):** **MCP do banco com versão** (faixa 5 do corte; Answers dos tickets 25, 30, 11, 34, 14, 41 e comentários de 2026-10-12 do 16): fork local do es617/obsidian-sync-mcp (TypeScript, Node ≥ 22; nesta máquina Node 24) em repositório próprio fora do hub (pergunta abaixo). Muda no fork: (a) **R1**: `read_note` devolve a revisão; `write_note` e `edit_note` exigem `base_rev` e gravam como filha dela (o caminho do `r1.py` do spike, `new_edits=false`, já provado com o plugin no ticket 30), então base velha vira conflito com as duas folhas guardadas, nunca sobrescrita; sem `base_rev`, regravar nota existente é recusado; (b) **conflito visível ao agente** (requisito do 25): nas duas formas, `read_note` de nota em conflito avisa e lista as folhas, e a ferramenta `get_conflicts` lista os conflitos abertos (as duas juntas são **[núcleo]**; o 30 dá a alternativa); (c) **`instructions`**: a cabeça autossuficiente do `AGENTS.md` até 2.000 caracteres (Answer do 36); a forma, o bloco `cabeca:inicio/fim` (Worker 1) lido a cada `initialize`, sem cópia, posto **antes** do texto do upstream para sobreviver ao corte do Claude Code, é **[núcleo]** (fecha a lacuna de dono 5 do 16); a descrição de cada ferramenta de gravação (`write_note`, `edit_note`, `delete_note`, `move_note`) começa por "antes de gravar, leia `AGENTS.md`" (36, R33) e, nas operações cuja API leva `base_rev` (`write_note`, `edit_note`), segue com "grave com a `base_rev` lida; conflito = releia e refaça" **[núcleo]**; a guarda de `delete_note` e `move_note` fica a definir; (d) **ferramenta de estado do hub** (requisito do 14; o nome `estado_do_hub` é **[núcleo]**): devolve o `estado.json` da vigia (esquema do Worker 8), para a checagem de início onde o hook falhar e para o cliente; sem o arquivo, devolve "estado indisponível", nunca estado em ordem; (e) **instâncias**: leitura por padrão e escrita ligável, com guarda de versão e token próprio, são requisitos (11, 14, 34); "duas instâncias por par, em 127.0.0.1, cada uma com o seu token de variável de ambiente, a de escrita reaproveitada atrás da rota `/banco-escrita/mcp` do proxy" é **[núcleo]**; a de leitura é `READ_ONLY=true` (34; já existe no upstream: "disable all write tools", README do es617, cópia do spike), a mesma linha de comando com só essa variável trocada; as duas juntas no mesmo par: não verificado; (f) **E2EE** (34): a frase-senha do `.env` do banco (`COUCHDB_PASSPHRASE` no upstream, 30), ligada depois dos testes sem ela; (g) a gravação chama o verificador de frontmatter (Worker 1) e recusa nota fora do esquema (imposição C do 12, requisito; "se couber" era corte de tempo **[formato]**)

**Como se prova (testing decisions, de ponta a ponta):** testes e2e automáticos (`npm run test:e2e` do fork) contra um CouchDB de ensaio só da faixa em 127.0.0.1:5996, com o MCP em 127.0.0.1:8796 (escrita) e 8797 (leitura): (1) ler e gravar com a revisão lida grava, e a leitura seguinte traz a revisão nova; (2) gravar com revisão velha deixa duas folhas no banco, nenhuma versão some, e a resposta diz "conflito: releia"; (3) `read_note` da nota em conflito avisa, e `get_conflicts` a lista; (4) regravar sem `base_rev` é recusado; (5) a instância de leitura não lista nenhuma ferramenta de gravação e recusa gravar; (6) o `initialize` traz a cabeça do `AGENTS.md` de ensaio e, trocado o arquivo, a sessão nova traz a cabeça nova; (7) `estado_do_hub` devolve o arquivo de exemplo; (8) os testes 1 a 3 de novo com E2EE ligada; (9) os três harnesses reais (Claude Code, Codex, Copilot CLI) em modo não interativo com HOME de ensaio citam o que receberam do servidor; a requisição do Codex é capturada para ver onde o `instructions` vai; no Copilot CLI, com e sem `--allow-all-mcp-server-instructions` (36, 41; o Copilot do VS Code fica com roteiro próprio para o Gustavo) **[formato: login de ensaio]**; os testes unitários do upstream seguem verdes. Mais `kit/par/05-mcp-banco.ps1` no contrato do instalador (Worker 2) e as duas linhas no `.env.modelo`

**Como segue sem esperar as outras faixas:** o banco (faixa 4): não espera; sobe `couchdb:3.5.2` na 5996 pelos nomes do `.env.modelo` do Worker 4 e, quando o `compose.yml` dela chegar, troca por ele; usa o retrato do item 6 dela (conflito aberto e binário com ramo apagado) como caso extra, se chegar a tempo. O `AGENTS.md` (faixa 1): um `AGENTS.md` de ensaio com o bloco `cabeca:` até a faixa 1 entregar. O estado da vigia (faixa 7): um `estado.json` de exemplo no esquema do Worker 8. O verificador (faixa 1): o dublê que sai 0. O kit (faixa 8): só escreve `HUB_MCP_BANCO_URL`, `HUB_MCP_BANCO_TOKEN`, `HUB_MCP_BANCO_LEITURA_URL` e `HUB_MCP_BANCO_LEITURA_TOKEN` no `.env.modelo` no minuto 0–10. As faixas 6 e 10 recebem de mim só nomes: `write_note` com `base_rev`, e as duas URLs

### Worker 6

**O que constrói (implementation decisions):** **Guardas de gravação e leitura no disco** (faixa 6 do corte; Answers dos tickets 11 e 14, "Imposição" do 12): um hook "antes da ferramenta" em `hooks/06-guardas/` (Node ≥ 22, `.mjs`, como a faixa 9), com um adaptador por harness e a mesma decisão: (a) **recusa a regravação inteira de arquivo que já existe** no hub (Write do Claude Code; `Add File` sobre existente, `Delete`+`Add` e `Update` que troca tudo no `apply_patch` do Codex; `create` do Copilot) com a mensagem "use a troca de trecho ou o `write_note` do MCP do banco com a versão lida"; deixa passar troca de trecho e arquivo novo; (b) **recusa nota fora do esquema** (requisito do 12): monta o conteúdo proposto (arquivo novo, ou o atual com a troca aplicada) e chama o verificador da faixa 1 (o adaptador de montar o conteúdo final é **[núcleo]**); (c) **aviso de leitura, sem recusa** (ticket 11, rodadas 3 e 4): guarda por sessão o que a busca devolveu (`PostToolUse` da ferramenta de busca) e o que foi aberto; avisa "leia o trecho que a busca apontou" ou "busque antes", uma vez por arquivo por sessão; (d) **sai na hora fora do hub** (caminho fora de `HUB_ROOT`). Comando de shell fica só no contrato, como decidido

**Como se prova (testing decisions, de ponta a ponta):** testes automáticos (`node --test`) com as entradas reais gravadas na bancada do ticket 11 (`hooks.jsonl` do Codex e os casos do Claude e do Copilot) mais casos novos: os quatro casos da bancada passam nos três adaptadores; nota sem `status` é recusada; leitura grande fora da busca avisa uma vez. De ponta a ponta, com login de ensaio (pergunta do Worker 2): `claude -p`, `codex exec` e `copilot -p` num hub de ensaio, com o fragmento instalado pelo kit no HOME de ensaio, recusam o Write sobre existente e deixam passar o Edit e o arquivo novo; sem login, a mesma prova roda no escopo de projeto, como a bancada fez

**Como segue sem esperar as outras faixas:** o verificador (faixa 1): chama `agents/bin/verificar-frontmatter` pela interface do Worker 1, com o dublê que sai 0 até ela entregar; a busca (faixa 3): só o nome do servidor (`busca`, do `.env` do kit) e a forma da resposta, com uma resposta gravada como dublê; o kit (faixa 8): entrega `fragmento.json` no formato do Worker 8 no minuto 15, sem esperar o kit; o MCP do banco (faixa 5): só o nome `write_note` na mensagem de recusa

### Worker 7

**O que constrói (implementation decisions):** **Vigia e divergência** (faixa 7 do corte; Answers dos tickets 33 "Aviso" e "Divergência", 08, 14 "Checagem de início" e "Estado da vigia na tela", 34 "Segurança"), em `agents/skills/vigia/` (o ticket 12 fixa o conteúdo de `agents/` e não tem `agents/vigia/`; a vigia vai como skill com scripts, como a "nova iniciativa"; caminho a confirmar pelo Prumo) (Node ≥ 22, `.mjs`, como as faixas 6 e 9; `livesync-commonlib` para decifrar, como no ticket 09): (a) `vigia passada`: uma passada lê o CouchDB local (`_scheduler/docs`; conflitos abertos; ramo apagado de binário pela resolução por `mtime`, 48), o disco (arquivo acima de 200 MiB), se o sincronizador está vivo, se o Config Doctor travou o plugin (33) e se o outro par está ligado (o `HUB_OUTRO_PAR_URL` é um sinal **[núcleo]**, não o detector inteiro: URL sem resposta não prova máquina desligada; a vigia distingue máquina desligada, serviço parado com a máquina ligada e estado não verificável, e o incerto nunca vira `ok` nem suprime a divergência de replicação parada; vai, no mínimo, como `informa`, com o motivo; 33); com E2EE, decifra o caminho com a frase-senha do `.env` e cita a nota pelo caminho em claro (34, 48); grava `estado.json` por troca atômica; (b) notificação do Windows **só quando o estado piora** em relação à passada anterior; (c) `vigia recuperar <caminho>` grava a versão perdida do binário num arquivo ao lado; (d) `hooks/07-vigia/`: hook de início de sessão nos três harnesses que injeta o resumo (com o outro par desligado, só a hora da última troca), o programa do `notify` do Codex, o script de `statusLine` do Copilot e `mods/07-vigia/` (Claude Code, estado o tempo todo); (e) a tarefa agendada de 5 min (33) como XML e `kit/par/07-vigia.ps1` só com `-WhatIf` (registrar é `ready-for-human`); na hora, a vigia roda em laço no terminal **[formato]**; (f) o Config Doctor travando o plugin é requisito do 33 (está em (a)); "se couber" era corte de tempo **[formato]**

**Como se prova (testing decisions, de ponta a ponta):** `node --test` com um CouchDB dublê (respostas gravadas) e o disco do hub de ensaio, oito cenários dão o `estado.json` esperado: tudo em ordem; conflito de texto; binário descartado; replicação parada há mais de 15 min com o outro par ligado (`divergencia`); outro par desligado (`informa`, com a hora da última troca); arquivo de 201 MiB (`fsutil file createnew`, rápido); sincronizador parado; item `copia-diaria` da faixa 10 (`informa`, com notificação) **[núcleo]**; sem arquivo da vigia e sem MCP, a checagem de início diz "estado indisponível" (14; bancada de acesso). Estado em `C:\context-hub\.local\vigia\estado.json` (fora do banco e do `.git`), com `nivel` por item (`ok | informa | divergencia`) e o do topo igual ao pior **[núcleo]**. A notificação sai só na passada que piora (notificador dublê; uma real à vista do Gustavo, se ele quiser). `vigia recuperar` devolve os bytes do ramo apagado. Ponta a ponta no CouchDB de ensaio (porta 5997, com E2EE): no retrato da faixa 4, a vigia acusa o conflito e o binário **pelo caminho decifrado**; o hook de início, rodado com a entrada JSON de cada harness, devolve o resumo; o mod e a `statusLine` mostram o estado de um arquivo de exemplo

**Como segue sem esperar as outras faixas:** banco (faixa 4): uso o `.env.modelo` e as portas do Worker 4 desde o minuto 0; até o retrato do item 6 chegar, forjo o conflito e o ramo apagado no meu CouchDB (5997) pela API e começo sem E2EE, ligando a frase-senha antes do fim. Outro par: `HUB_OUTRO_PAR_URL` (no ensaio, o CouchDB B do Worker 4 ou um dublê parado). Kit (faixa 8): entrego `hooks/07-vigia/fragmento.json` no minuto 15, no formato do Worker 8, e o kit liga o `notify` do Codex ao meu programa. Faixa 2: hook de início próprio, separado do da nota. Faixa 10: só leio o item `copia_diaria`. Não espero ninguém

### Worker 8

**O que constrói (implementation decisions):** Portas dos harnesses e kit de par (faixa 8 do corte; tickets 14, 42, 13, 18, 15 e comentários do 16): `kit/par/instalar.ps1` idempotente com `-WhatIf`, cópia e hash antes de tocar, e desfazer. Confere: sem `CLAUDE.md` no hub nem acima, modo de desenvolvedor, Node e Python. Liga: contrato por link simbólico (`~/.codex/AGENTS.md`, `~/.copilot/copilot-instructions.md`) e import no `~/.claude/CLAUDE.md`; skills por junction (`~/.claude/skills`, `~/.agents/skills`), só as de uso geral (a busca, o FreeLLMAPI, o fluxo do Matt Pocock, a família `maestro-*` e as poucas que servem a qualquer trabalho; as de papel entram só na pasta do papel, pela receita de setup; 15); MCP de busca e de banco nos três harnesses (127.0.0.1, token de variável de ambiente, `default_tools_approval_mode="approve"` no Codex); hooks no escopo do usuário juntando os fragmentos das outras faixas (aprovados por hash em `hooks.state` no Codex); Codex `danger-full-access` com `notify`; tira o GSD do escopo global com cópia

**Como se prova (testing decisions, de ponta a ponta):** o kit roda duas vezes num HOME de ensaio (a segunda não muda nada) e desfaz sem sobra; teste automático da forma: cada link aponta para o `AGENTS.md` do hub de ensaio, cada junction expõe só as skills de uso geral de `agents/skills/` (uma skill de papel do hub de ensaio não aparece na junction global; 15), cada config tem as duas linhas de MCP e os hooks juntados; com login de ensaio (pergunta do Worker 2), `claude -p`, `codex exec` e `copilot -p` respondem uma pergunta que só o contrato de ensaio sabe

**Como segue sem esperar as outras faixas:** o `AGENTS.md` (faixa 1) e as skills (faixa 9): usa os do hub de ensaio, com um contrato e uma skill de marca; os MCP (faixas 3 e 5): só a URL e o token, lidos do `.env`, sem esperar o servidor; os hooks e o mod (faixas 2, 6, 7, 9): junta o que estiver em `hooks/<faixa>/` no formato combinado; o que chegar depois entra numa segunda passada do kit, sem refazer nada

### Worker 9

**O que constrói (implementation decisions):** **Skills e acervo do maestro** (faixa 9 do corte; tickets 15, 40, 43, 44 e comentário de 2026-10-12 do 16), tudo em `agents/` do hub: `skills/routing.yml` (gatilho por palavras do pedido, tipo de nota pelo caminho e papel → skill; camada geral e de papel) com as primeiras linhas (a skill do FreeLLMAPI para pesquisa, `armis-docx`, as skills de design por papel da frente da cidade); o hook de entrada sem IA que confere a tabela e injeta "use a skill X"; a família `maestro-*` (`maestro-acervo` é a porta; catálogo curto e um arquivo por peça) com o primeiro lote do Answer do 40 (papéis genéricos sem nome de cliente e o Designer, a partitura de hoje como receita e o arranjo deste workspace, contratos-opção de roteamento de modelos com o FreeLLMAPI, orquestração e onde abrir, o lembrete e a guarda); o hook de início que só age com `MAESTRI_TERMINAL_ID` e manda começar por `maestro-acervo` (age em qualquer pasta, dentro ou fora do hub, como o hook de uso: exceção à regra "sai na hora fora do hub" do 14, que vale para os hooks de início com a vigia, fim e recusa; leitura conciliadora de 14 e 40 **[núcleo]**); a guarda do acervo (Claude Code: antes da ferramenta, gravar no acervo, isto é `agents/skills/maestro-*/`, as skills de papel do acervo e a skill "nova iniciativa" (12), pede aval, com exceção do maestro em `agents/skills/routing.yml` (15); `agents/maestro/` (`propostas/`, `uso/`) fica fora da guarda; Codex e Copilot: recusa no acervo apontando `agents/maestro/propostas/` (40); se as skills de uso geral fora da família entram na guarda: aberto); o registro de uso por hook em `agents/maestro/uso/<máquina>.md`; no fim da resposta, registrar se a skill indicada rodou, sem obrigar

**Como se prova (testing decisions, de ponta a ponta):** testes automatizados dos hooks com a entrada JSON de cada harness: um pedido de pesquisa que não cita o FreeLLMAPI recebe "use a skill" dele (o aceite do ticket 15); sem `MAESTRI_TERMINAL_ID` o hook de início não faz nada, com ele injeta o lembrete; gravar numa peça protegida (uma skill `maestro-*`, uma skill de papel do acervo, a skill "nova iniciativa") dá `ask` no Claude Code e recusa com o caminho de propostas no Codex e no Copilot, **tanto pelo caminho real quanto pelo da junction** e também numa sessão aberta fora do hub (teste pedido no 16; a guarda decide pelo alvo real); gravar em `agents/maestro/propostas/` passa nos três; o maestro grava `routing.yml` e passa; a guarda sobre skills de uso geral fora da família não é testada enquanto o alcance está aberto; usar uma skill vira linha no registro; `routing.yml` passa no esquema e cada `SKILL.md` da família tem `name` e `description` válidos. Ao vivo, com HOME de ensaio: `claude -p` com o pedido de pesquisa mostra a injeção

**Como segue sem esperar as outras faixas:** o hub de ensaio (proposta do Worker 2) para `agents/`; entrega os hooks em `hooks/09-skills/` no formato de fragmento do Worker 8, sem tocar em settings de outra faixa; as junctions são do kit (faixa 8), que liga a minha pasta como ela estiver; o primeiro lote lê o Maestri e o vault só para leitura. Não espera ninguém

### Worker 10

**O que constrói (implementation decisions):** **Manutenção e kit de cliente** (faixa 10 do corte; tickets 33, 34, 36, 14, 11 e comentário de 2026-10-15 do 16, lacunas de dono 4 e 5; o que vinha das rodadas 7 e 8 do 56 está marcado), em `agents/` (a pasta exata dos scripts segue a da faixa 1: `agents/bin/` não está no ticket 12) e `kit/cliente/`: (a) `arquivar <pasta>` (36, R25; 12) move para o `_archive/` da própria raiz como `_archive/<AAAA-MM-DD>--<nome>/` (a data viaja no nome, sem arquivo com ponto **[núcleo]**; não substitui `archived_at` e o esquema de origem do 12), só se o outro par estiver em dia (replicação nos dois sentidos sem atraso de 15 min, lida do `_scheduler/docs`) e sem edição recente na pasta; senão recusa dizendo por quê; (b) `limpar-arquivo` (apagar do `_archive/` o que passou de 30 dias, com `-WhatIf`): o prazo vem só da rodada 7 do 56, **[ticket aberto: 56]**, fora desta construção; o desenho fica como contexto **[núcleo]**; (c) `copia-diaria` (33, 06): no `.git` da raiz, ramo `par/<máquina>`, só `add`, `commit` e `push`, nunca `pull` nem `checkout`; `.gitignore` com `.local/` (estado da vigia e índice da busca ficam fora); falha alto (saída ≠ 0 e item `copia-diaria` no estado da vigia) **[núcleo]**, ligado à pendência "quem percebe a falha" do 56, que não se fecha aqui; (d) `conferir-cabeca`: o bloco `cabeca:inicio/fim` do `AGENTS.md` existe e cabe em 2.000 caracteres (lacuna 5; a atualização em si é o fork relendo o bloco, ver Worker 5 (c) **[núcleo]**); (e) kit de cliente: no par, o TBXark/mcp-proxy com as rotas `/busca/mcp`, `/banco/mcp` (só leitura) e `/banco-escrita/mcp`, um token por rota; no cliente, `ligar-cliente.ps1` grava a linha de MCP com `Authorization: Bearer` de variável de ambiente nos três harnesses, `--allow-all-mcp-server-instructions` no Copilot CLI e o contrato na configuração global, tudo em HOME de ensaio; a porta do proxy vai no `.env` do kit; a busca é testada pelo proxy e, se preciso, o `--allowed-host` recebe o `Host` realmente observado, não presumido **[núcleo]**; (f) a ponte `mcp-remote` (MCP stdio) do Claude Desktop para a busca e para o MCP do banco com escrita (ticket 11, o mais novo; 36, 38), mais a pasta conectada do Cowork com "Folder instructions" apontando o `AGENTS.md`: conteúdo decidido; "geradas e não instaladas", "se couber" e o dono (aqui, faixa 10; as partes dizem o mesmo) são **[formato]**; (g) `kit/par/10-manutencao.ps1` no contrato do kit, registrando a tarefa diária (cópia + cabeça; a limpeza só com o 56) só com `-WhatIf` **[formato]**

**Como se prova (testing decisions, de ponta a ponta):** testes automatizados no hub de ensaio: `arquivar` move com o outro par em dia e recusa com ele atrasado ou com arquivo editado há minutos; (`limpar-arquivo` apaga a pasta de 31 dias e mantém a de 29: **[ticket aberto: 56]**, fora do aceite desta construção); `copia-diaria` gera commit no ramo do par e empurra para um repositório nu local, e com o remoto quebrado sai ≠ 0 e grava a linha no estado; `conferir-cabeca` recusa bloco ausente ou longo. Ponta a ponta do cliente, tudo em 127.0.0.1 no lugar da tailnet: um cliente de ensaio busca pelo proxy, lê pela rota só de leitura, tem a gravação recusada nela, e sem token leva 401; mede se o proxy repassa o `instructions` (não verificado no 14)

**Como segue sem esperar as outras faixas:** busca e banco (faixas 3 e 5): o proxy aponta para as URLs do `.env` do Worker 8; até elas existirem, dois MCP dublês HTTP mínimos (uma ferramenta de busca, uma de leitura e uma de gravação que respeita `READ_ONLY`), trocados pelos reais na segunda passada sem mudar o proxy. Estado do outro par (faixa 4): `arquivar` lê de uma fonte trocável, o `_scheduler/docs` do CouchDB de ensaio ou um JSON de exemplo no mesmo formato desde o minuto 0. Estado da vigia (faixa 7): só acrescento um item `copia-diaria` no formato do Worker 8 (o nível é da vigia). Hub de ensaio do Worker 2. Não espera ninguém

## Pontos abertos achados ao escrever a spec

- Gravação com versão velha: o ticket 11 diz "é recusada, e o agente relê e refaz"; os tickets 25 e 30, "vira conflito, gravada como folha filha". Vale o conflito visível (25, 30), e a resposta ao agente diz "releia e refaça".
- A ponte `mcp-remote` do Claude Desktop: o comentário de 2026-10-12 do ticket 16 diz só leitura; o ticket 11 decidiu que o Desktop grava pelo MCP. Vale o ticket 11.
- Corte do `instructions` no Claude Code: 2.048 caracteres (ticket 36) contra cerca de 3.300 observados (ticket 41). Vale o menor.
- Hooks do Codex provados com `workspace-write`; o ticket 14 decidiu `danger-full-access`: testar os hooks nesse modo.
- Verificador no `Stop` (ticket 12) e fim de resposta do Claude Code pelo mod (ticket 14): o verificador roda onde o fim de resposta roda em cada harness.
- O verificador grava no disco: a garantia "nenhuma gravação sem guarda de versão" (11) vale para ele, sem exceção. Que
  ele só complete campos deriváveis, por troca de trecho, é **[núcleo]** e não dispensa a guarda: ele relê o arquivo
  logo antes de gravar e só troca o trecho se o arquivo ainda é o que leu; se mudou, refaz ou devolve ao agente (o
  sincronizador também grava no disco, 08 e 33). A janela entre a releitura e a gravação: não verificado. Manter
  índices e conferir links (12) seguem a mesma guarda.
- O verificador de frontmatter é da faixa 1; a faixa 6 só o chama.
- Marcador de raiz: os tickets 36 e 40 o põem no kit; a rodada 4 do 14 o tira. Vale o 14 (mais recente): o kit não cria marcador. A bancada do 14 passou com o `.git` real em subpasta e em pasta de papel; o 45 (sem `.git`) viu o Copilot parar na iniciativa, o que o `.git` resolve.
- GSD: o 36, o 42 e o 16 juntam o contrato com o GSD no arquivo global do Copilot; o 15 tira o GSD do escopo global. Vale o 15.
- Desatualizados no mapa: o 08 (30 min e colisão que para a máquina) foi trocado pelo 33 (15 min, só a nota retida); o 37 (hub sem `.git`) pelo 33 (`.git` na raiz); o 18 (VS Code só MCP local sem autenticação) pelo teste do 14 (passou com token).
- Avisos no Codex: a vigia notifica quando o estado piora (33) e o `notify` dispara a notificação do Windows no fim de cada turno com divergência (14, rodada 8); os dois ficam, por decisão. O comportamento combinado é descrito e testado na construção; qualquer política de repetição é **[núcleo]**.
- O `COPILOT_HOME` de ensaio desliga `~/.agents/skills` (18): o ensaio por ele prova contrato, MCP e hooks do Copilot, não as skills; `COPILOT_SKILLS_DIRS` apontando para a junction de ensaio é saída **[núcleo]** a verificar, e não substitui o passo real no HOME de verdade (`ready-for-human`). O MCP do VS Code no escopo do usuário segue sem decisão.
