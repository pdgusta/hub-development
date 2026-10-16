# Plano de execução da construção do hub

Fonte única do plano, ajustada pelos 12 recrutas na rodada Ralph de planejamento. Ponto de partida:
`../laco-proposta.md` (proposta do maestro) e a resposta do Gustavo à rodada 1 do ticket 16 (2026-10-15 21:08).

## Regras fixas (do Gustavo)

- Trabalho vertical, em grupos lógicos; uma faixa por worker; nenhum worker parado esperando outro.
- A execução inteira dura 1 hora; o que não couber fica para outra execução.
- 10 workers e 2 Prumos (Claude Opus 5.5 alto); até 10 subagentes cada; Fable 5.1 médio para tarefa muito complexa.
- Spec por `/to-spec` e tickets por `/to-tickets`, invocados pelo Gustavo; depois `/implement-spec`.
- Nada global (`~/.claude`, `~/.codex`, `~/.copilot`, hooks do usuário, serviços) sem o aval do Gustavo: HOME de ensaio.
- O hub nasce em `C:\context-hub`.

## Faixas (uma por worker)

| Worker | Faixa vertical | Entrega funcionando ao fim da hora | Usa de outra faixa (e como segue sem esperar) |
|---|---|---|---|
| Worker 1 | **Esqueleto, contrato e frontmatter** (faixa 1; Answers do 12, 36, 01, 02; parte da faixa 1 em `../spec-partes/faixas-01-02.md`). Sem `agents/bin/` (Prumo): os scripts moram onde o 12 manda. **Núcleo que cabe na hora:** (a) a árvore: `AGENTS.md`, as seis raízes com `_archive/`, `agents/{skills,machines,maestro/propostas,maestro/uso,frontmatter}/`, `agents/blocks.md` (texto da rodada 15); `.gitignore` da raiz no min 0 com `.local/`, `.secrets/`, `.maestri/`, `.obsidian-hybrid-search.db*`; (b) `agents/frontmatter/paths.yml` e os 28 esquemas `agents/frontmatter/<tipo>.yml`, com a tabela `stage` → `status` dentro de cada esquema com ciclo; (c) o verificador `agents/frontmatter/verificar.mjs` (Node ≥ 22 com o pacote `yaml`): valida pelo tipo do caminho, preenche o derivável (`type`, `initiative`, `updated`, `title` do núcleo pela ficha), deriva `status` de `stage`, ignora o que tem ponto, `AGENTS.md`, `SKILL.md` e `agents/skills/**`; antes de gravar confere o hash lido (não desfaz gravação do sincronizador nem de outro agente, 08 e 11); (d) a skill `agents/skills/nova-iniciativa/` (SKILL.md e script): pasta no nível certo, núcleo de seis arquivos, `AGENTS.md` da iniciativa e blocos escolhidos, idempotente; (e) `agents/frontmatter/exclusoes.mjs`: gera, a partir do ponto no nome e dos `index.md` com `local: true`, a lista de padrões para o LiveSync (faixa 4) e um bloco gerado no `.gitignore` (que também tira da busca, faixa 3); (f) o `AGENTS.md` com a cabeça de até 2.000 caracteres e as seções "repositório de código mora fora do hub" (33) e "banco fora do ar: a regravação espera e vai para a retomada" (11); o texto de outras faixas entra pelos `hooks/<nn>/regra-contrato.md` na junção; (g) `hooks/01-verificador/fragmento.json`: o verificador no fim da resposta pelo mesmo canal de fim da faixa 2 (14). **Segunda passada (min 40–45, se sobrar):** o `index.md` criado a 10 arquivos ou com arquivo que a busca não lê, com a lista de `summary: auto`; o `.pdf.md` irmão no esquema `attachment-text`. | `pwsh agents/test/01-esqueleto.ps1` numa worktree limpa sai 0: a skill cria uma iniciativa em `clients/` (dois níveis) e em `initiatives/` (um), com o núcleo aceito pelo verificador e o `title` "<Arquivo> · <nome>", e rodar de novo não duplica; o verificador aceita a nota certa, recusa a sem `status` e a com `stage` fora do ciclo, deriva `status`, completa a nota do `inbox/`, deixa intocados `AGENTS.md`, `SKILL.md` e pastas com ponto, e não grava se o arquivo mudou depois da leitura; a cabeça do `AGENTS.md` tem ≤ 2.000 caracteres; um `index.md` com `local: true` e um `.secrets/` aninhado entram na exclusão gerada e no `.gitignore`; nenhum `CLAUDE.md` no hub. A prova pelo fim da resposta numa sessão real (`claude -p`) vale só se o mod da faixa 2 carregar no `-p`; senão o teste chama o verificador com a entrada que o hook recebe. | nada de outra faixa; publica no min 0–10 o `.gitignore`, o `paths.yml` e a interface do verificador (fronteiras abaixo). As outras faixas usam o hub de ensaio e o dublê do verificador até lá |
| Worker 2 | **Retomada e fim da resposta** (Answers dos tickets 10 e 14 "Fim da resposta", 12 "Núcleo" e "Imposição", 11 "banco fora"). Base pronta: a bancada do ticket 14 (`C:\Projetos\bancada-acesso\`: `mods/fim-retomada/`, `extensoes-copilot/fim-retomada/`, `scripts/fim.py`, `relatorio.md` §4), que passou nos três; a faixa a transforma em peça do hub, em Node ≥ 22 (`.mjs`, como 6, 7 e 9). (a) **Decisão comum** `hooks/02-retomada/decidir.mjs`, sem IA: acha a iniciativa subindo da pasta da sessão até um `initiative.md` (fora de iniciativa ou fora do hub: solta, nada faz, porque a retomada fora de iniciativa está em aberto no 12); **devolve o agente uma vez** (respeita `stop_hook_active`) quando o turno mudou arquivo da iniciativa e `retomada.md` não mudou, ou quando a memória privada ganhou arquivo no turno (Claude Code: a pasta `memory/` do projeto; Codex e Copilot: **não verificado** que tenham uma, ficam só com a regra); a mensagem pede os sete campos (objetivo, onde parou, próximo passo, decisões com ponteiro, tentado e não deu, perguntas abertas, arquivos em jogo; fato × hipótese) e, com o banco fora, "anote a regravação pendente" (11). Proposta a conferir pelo Prumo: a bancada devolvia em **todo** turno sem nota tocada; aqui só quando o trabalho mudou ("quando a nota não reflete a resposta", 10). (b) **Três adaptadores**, uma decisão: mod do Claude Code `mods/02-retomada/` (`turn.start` + `classic.Stop`, `.catch` que solta se falhar); hook `Stop` do Codex e hook `agentStop` do Copilot no `fragmento.json` do Worker 8; extensão do Copilot `extensoes-copilot/02-retomada/extension.mjs` (`onUserPromptSubmitted` + `onAgentStop`; lê `workingDirectory`, não `cwd`). (c) **Início:** hook de início nos três que injeta a `retomada.md` da iniciativa da pasta (separado do hook da vigia, faixa 7). (d) **Verificador no fim** (Imposição do 12): o mesmo `Stop` chama o verificador da faixa 1 nos `.md` mudados no turno e devolve ao agente o que falta. (e) **Regra do contrato** em `hooks/02-retomada/regra-contrato.md` (manter a nota; conferir a memória privada e levar ao hub), para a faixa 1 colar | `pwsh agents/test/02-retomada.ps1`: (1) `node --test` da decisão com as entradas reais da bancada (Stop do Codex, `agentStop` e `onAgentStop` do Copilot, `classic.Stop` do mod): turno sem mudança solta; arquivo mudado sem nota devolve; nota tocada solta; `stop_hook_active` solta; fora do hub e fora de iniciativa soltam; memória privada nova devolve com o caminho; nota sem `status` devolve o motivo do verificador; (2) **ao vivo no Claude Code sem tocar `~/.claude`**: `claude -p --plugin-dir mods/02-retomada --settings <fragmento de início>` (o caminho que passou na bancada) no hub de ensaio: pedido que muda `tasks.md` é devolvido e termina com `retomada.md` regravada com os sete campos; a sessão seguinte responde "qual o próximo passo?" com o campo da nota; (3) Codex e Copilot ao vivo só com a resposta à pergunta do login; sem ela, a forma dos fragmentos e da extensão | hub de ensaio: precisa de uma iniciativa com o núcleo de seis arquivos (`initiative.md`, `retomada.md`, `tasks.md`…), copiada no minuto 0; verificador (faixa 1): `HUB_VERIFICADOR`, dublê que sai 0; fragmento e mod ao kit (faixa 8) no minuto 15, no formato do Worker 8, mais a pasta nova `extensoes-copilot/<faixa>/` (o kit liga `--experimental` só no HOME de ensaio, porque ele grava `~/.copilot/settings.json`, bancada §4); regra do contrato à faixa 1 no minuto 20. Não espero ninguém |
| Worker 3 | **Busca** (faixa 3 do corte; Answers dos tickets 09 e 54, lacunas do Prumo para a faixa 3): (a) `kit/par/03-busca.ps1` no contrato do kit: instala o obsidian-hybrid-search **0.16.2 fixo** com `npm install` local em `C:\context-hub\.local\busca\` (nunca `-g`), com `-WhatIf`; (b) `busca/iniciar.ps1` sobe `ohs serve --foreground` em `127.0.0.1:3939` (padrão do README 0.16.2, rota `/mcp`, HTTP sem estado) sobre o hub, com `LOCAL_EMBEDDING_MODEL=Snowflake/snowflake-arctic-embed-m-v2.0` (variável provada na bancada, `bancada-busca/scripts/robusta/ohs-modelo.py`; **não está no README**) e `OBSIDIAN_IGNORE_PATTERNS` com `**/.*/**` e `**/.*` (o que tem ponto, como no LiveSync) mais o que a faixa 1 gerar para `local: true`; um analisador só, sem campo de idioma; (c) o `.obsidian-hybrid-search.db` (e `-wal`/`-shm`) fora do git e do LiveSync (o `--db` não move o banco, achado da bancada); (d) a configuração do gemini-embedding-001 pelo FreeLLMAPI (`OPENAI_BASE_URL` = `$env:FREELLM_BASE_URL/v1`, nunca `localhost:3001` fixo; `OPENAI_EMBEDDING_MODEL`), escrita em `busca/gemini.env` e **desligada**; testada uma vez num segundo índice, numa cópia do hub de ensaio em porta 3940 (o `--db` não separa índice), se o Gustavo liberar a cota; (e) escreve `HUB_MCP_BUSCA_URL=http://127.0.0.1:3939/mcp` no `.env.modelo` do kit no minuto 5. Ligar no boot (tarefa agendada) fica `ready-for-human` | `busca/testes/aceite.mjs` (Node ≥ 22, sem pacote de fora, MCP Streamable HTTP por `fetch`: `initialize` e `tools/call search`) contra o hub de ensaio: uma pergunta em pt-BR por palavra (`fulltext`) e uma por paráfrase sem palavra em comum (`semantic`) acham a nota esperada entre as 3 primeiras; uma nota criada no disco durante o teste aparece na busca em até 60 s (mede e grava o tempo); nada com ponto no caminho aparece; `status` mostra indexadas = `.md` válidos, e a lista das recusadas por YAML inválido sai no relatório; pedido com `Host` estranho é recusado. Roda duas vezes seguidas (a segunda reaproveita o índice) | hub de ensaio (Worker 2): copio no minuto 0 e escrevo as notas e as perguntas de aceite eu mesmo, sem esperar a faixa 1; exclusão de `local: true` (faixa 1): leio a lista gerada se existir, senão só o padrão de ponto, e entra na segunda passada; kit (faixa 8): só a URL no `.env.modelo` e o meu `03-busca.ps1`; proxy (faixa 10): ela usa a URL; um dublê não é preciso, o servidor de verdade sobe no minuto 10–15; LiveSync (faixa 4): não preciso dele; o tempo "edição no par B → busca no par B" fica para o teste de aceite final, se as duas faixas terminarem |
| Worker 4 | **Banco e vista `.md`** (faixa 4 do corte; tickets 25, 33, 34, 47, 48 e comentários de 2026-10-13 e 2026-10-14 do 16): par A e par B de ensaio nesta máquina, cada um com o seu CouchDB 3.5.2 (contêineres `hub-ensaio-04-a` e `-b`, portas 5994 e 5995 em 127.0.0.1, usuário e senha de ensaio gerados, nada copiado do spike) e uma replicação de envio em cada um (S3); o sincronizador é o CLI do LiveSync (build do commit `14141446` do spike, sem recompilar), configurado pelo caminho dos testes oficiais (`init-settings`, `remote-add`), um dispositivo por par aceito com `mark-resolved`, **E2EE com caminho ofuscado** (34), `syncMaxSizeInMB` 200, exclusão de tudo que tem ponto em qualquer nível pelo `.livesync/ignore` (linhas `.*` e `.*/`; ver fronteira da volta 2); roda em laço no terminal, e a tarefa agendada sai como XML. Tudo sobe por `kit/par/04-banco.ps1`. Caminhos da faixa: `kit/par/banco/**`, `kit/par/04-banco.ps1`, `kit/par/env/04.env`, `agents/test/04-banco.ps1`, `execucao/ensaio/banco/` | prova: `pwsh agents/test/04-banco.ps1`, em ordem de corte. **Núcleo (min 0–35):** (N1) o kit sobe os dois CouchDB e as duas replicações, e o `_scheduler/docs` de cada um mostra a sua em `running`; (N2) nota criada na pasta A aparece na B, e a editada na B volta à A, em até 30 s, sem texto claro nos documentos crus do CouchDB; (N3) a mesma linha editada nos dois pares com a replicação pausada vira `_conflicts` nos dois CouchDB, sem versão perdida; (N4) `.oculto/x.md`, `.env`, `projeto/.git/config`, `projeto/.venv/x` e `projeto/.secrets/x` não chegam ao banco, com o CLI rodando **e** na varredura de partida depois de reiniciá-lo. **Se sobrar (min 35–50), nesta ordem:** (S1) 60 MiB viaja, 201 MiB não; (S2) colisão de binário deixa a perdida num ramo apagado; (S3) o kit roda de novo sem mudar nada e o `-WhatIf` não grava; (S4) CLI morto e CouchDB fora na partida: o laço religa; (S5) retrato do banco de ensaio (conflito aberto, binário com ramo apagado, `_scheduler/docs` parado) em `execucao/ensaio/banco/`, para as faixas 5 e 7 na próxima execução; (S6) `claude -p` grava na pasta A e chega à B (só com o login de ensaio) | nada para começar. Entrega cedo: no min 0–10, `kit/par/banco/compose.yml` e `kit/par/env/04.env` (fronteira "Banco de ensaio"); no min 15, `execucao/ensaio/banco/scheduler-docs-em-dia.json` e `scheduler-docs-parado.json` tirados do CouchDB de ensaio (pedidos dos Workers 10 e 7), que até lá usam os seus dublês. O hub de ensaio (Worker 2) é o conteúdo das pastas A e B |
| Worker 5 | **MCP do banco com versão** (faixa 5 do corte; Answers dos tickets 25, 30, 11, 34, 14, 41 e comentários de 2026-10-12 do 16): fork local do es617/obsidian-sync-mcp (TypeScript, Node ≥ 22; nesta máquina Node 24) em repositório próprio fora do hub (pergunta abaixo). Muda no fork: (a) **R1**: `read_note` devolve a revisão; `write_note` e `edit_note` exigem `base_rev` e gravam o documento de metadados com `_rev = base_rev`; se a base não é mais a atual, o próprio CouchDB devolve 409 e nada é gravado ("specified revision is not latest for target document"; "409 Conflict (not saved)", docs.couchdb.org, `api/document/common.html` e `replication/conflicts.html`), e o MCP responde "a nota mudou desde a sua leitura: releia e refaça". É a **recusa** do Answer do 11 (2026-10-15, o mais novo), sem folha a mais para o Gustavo resolver, e mais curta que o `r1.py` do spike: o `new_edits=false` dele é, pela doc, "intended for use only by the replicator" e fica só como reserva, se o Gustavo quiser a versão do agente guardada como folha em conflito (Prumo confere a leitura 11 × 25). Sem `base_rev`, regravar nota existente é recusado; nota nova pelo MCP grava sem `base_rev` só se o caminho não existe; (b) **conflito visível ao agente**: `read_note` de nota em conflito avisa e lista as folhas, e a ferramenta `get_conflicts` lista os conflitos abertos; (c) **`instructions`**: o bloco `cabeca:inicio/fim` do `AGENTS.md` (Worker 1) lido a cada `initialize`, sem cópia, posto **antes** do texto do upstream para sobreviver ao corte do Claude Code, até 2.000 caracteres (Answer do 36); a regra curta ("leia antes, grave com a `base_rev` lida; conflito = releia e refaça") na descrição de `write_note`, `edit_note`, `delete_note` e `move_note`; (d) **ferramenta `estado_do_hub`**: devolve o `estado.json` da vigia (esquema do Worker 8), para a checagem de início onde o hook falhar e para o cliente (14); (e) **duas instâncias por par**, em 127.0.0.1, cada uma com o seu token de variável de ambiente: escrita e `READ_ONLY=true` (já existe no upstream: "disable all write tools", README do es617, cópia do spike), a mesma linha de comando com só essa variável trocada; (f) **E2EE**: a frase-senha do `.env` do banco (`COUCHDB_PASSPHRASE` no upstream), ligada depois dos testes sem ela; (g) se couber: a gravação chama o verificador de frontmatter (Worker 1) e recusa nota fora do esquema (imposição C do 12) | um comando, `pwsh agents/test/05-mcp-banco.ps1` (crivo do Prumo 2), que sobe `hub-ensaio-05-couchdb` em 127.0.0.1:5996 e o MCP em 127.0.0.1:8796 (escrita) e 8797 (leitura), roda os testes e2e do fork e apaga tudo ao fim: (1) ler e gravar com a revisão lida grava, e a leitura seguinte traz a revisão nova; (2) outro escritor muda a nota; gravar com a revisão velha é recusado, o banco não ganha revisão nova, a versão do outro fica intacta e a resposta diz "releia e refaça"; reler e gravar passa; (3) conflito de replicação forjado (`_bulk_docs` com `new_edits=false`, como o replicador faz): `read_note` avisa e lista as folhas, e `get_conflicts` lista a nota; (4) regravar sem `base_rev` é recusado; (5) a instância de leitura não lista nenhuma ferramenta de gravação e recusa gravar; (6) o `initialize` traz a cabeça do `AGENTS.md` de ensaio e, trocado o arquivo, a sessão nova traz a cabeça nova; (7) `estado_do_hub` devolve o arquivo de exemplo; (8) os testes 1 a 3 de novo com E2EE ligada; os testes unitários do upstream seguem verdes. Mais `kit/par/05-mcp-banco.ps1` no contrato do instalador (Worker 2) e as duas linhas no `.env.modelo` | o banco (faixa 4): não espera; sobe `couchdb:3.5.2` na 5996 pelos nomes do `.env.modelo` do Worker 4 e, quando o `compose.yml` dela chegar, troca por ele; usa o retrato do item 6 dela (conflito aberto e binário com ramo apagado) como caso extra, se chegar a tempo. O `AGENTS.md` (faixa 1): um `AGENTS.md` de ensaio com o bloco `cabeca:` até a faixa 1 entregar. O estado da vigia (faixa 7): um `estado.json` de exemplo no esquema do Worker 8. O verificador (faixa 1): o dublê que sai 0. O kit (faixa 8): só escreve `HUB_MCP_BANCO_URL`, `HUB_MCP_BANCO_TOKEN`, `HUB_MCP_BANCO_LEITURA_URL` e `HUB_MCP_BANCO_LEITURA_TOKEN` no `.env.modelo` no minuto 0–10. As faixas 6 e 10 recebem de mim só nomes: `write_note` com `base_rev`, e as duas URLs |
| Worker 6 | **Guardas de gravação e leitura no disco** (faixa 6 do corte; Answers dos tickets 11 e 14, "Imposição" do 12): um hook "antes da ferramenta" em `hooks/06-guardas/` (Node ≥ 22, `.mjs`, como a faixa 9), com um adaptador por harness e a mesma decisão: (a) **recusa a regravação inteira de arquivo que já existe** no hub (Write do Claude Code; `Add File` sobre existente, `Delete`+`Add` e `Update` que troca tudo no `apply_patch` do Codex; `create` do Copilot) com a mensagem "use a troca de trecho ou o `write_note` do MCP do banco com a versão lida"; deixa passar troca de trecho e arquivo novo; (b) **recusa nota fora do esquema**: monta o conteúdo proposto (arquivo novo, ou o atual com a troca aplicada) e chama o verificador da faixa 1; (c) **aviso de leitura, sem recusa** (ticket 11, rodadas 3 e 4): guarda por sessão o que a busca devolveu (`PostToolUse` da ferramenta de busca) e o que foi aberto; avisa "leia o trecho que a busca apontou" ou "busque antes", uma vez por arquivo por sessão; (d) **sai na hora fora do hub** (caminho fora de `HUB_ROOT`). Comando de shell fica só no contrato, como decidido | testes automáticos (`node --test`) com as entradas reais gravadas na bancada do ticket 11 (`hooks.jsonl` do Codex e os casos do Claude e do Copilot) mais casos novos: os quatro casos da bancada passam nos três adaptadores; nota sem `status` é recusada; leitura grande fora da busca avisa uma vez. De ponta a ponta, com login de ensaio (pergunta do Worker 2): `claude -p`, `codex exec` e `copilot -p` num hub de ensaio, com o fragmento instalado pelo kit no HOME de ensaio, recusam o Write sobre existente e deixam passar o Edit e o arquivo novo; sem login, a mesma prova roda no escopo de projeto, como a bancada fez | o verificador (faixa 1): chama `agents/bin/verificar-frontmatter` pela interface do Worker 1, com o dublê que sai 0 até ela entregar; a busca (faixa 3): só o nome do servidor (`busca`, do `.env` do kit) e a forma da resposta, com uma resposta gravada como dublê; o kit (faixa 8): entrega `fragmento.json` no formato do Worker 8 no minuto 15, sem esperar o kit; o MCP do banco (faixa 5): só o nome `write_note` na mensagem de recusa |
| Worker 7 | **Vigia e divergência** (faixa 7 do corte; Answers dos tickets 33 "Aviso" e "Divergência", 08, 14 "Checagem de início" e "Estado da vigia na tela", 34 "Segurança"), em `agents/vigia/` (Node ≥ 22, `.mjs`, como as faixas 6 e 9; `livesync-commonlib` para decifrar, como no ticket 09): (a) `vigia passada`: uma passada lê o CouchDB local (`_scheduler/docs`; conflitos abertos; ramo apagado de binário pela resolução por `mtime`), o disco (arquivo acima de 200 MiB), se o sincronizador está vivo e se o outro par responde; com E2EE, decifra o caminho com a frase-senha do `.env`; grava `estado.json` por troca atômica; (b) notificação do Windows **só quando o estado piora** em relação à passada anterior; (c) `vigia recuperar <caminho>` grava a versão perdida do binário num arquivo ao lado; (d) `hooks/07-vigia/`: hook de início de sessão nos três harnesses que injeta o resumo (com o outro par desligado, só a hora da última troca), o programa do `notify` do Codex, o script de `statusLine` do Copilot e `mods/07-vigia/` (Claude Code, estado o tempo todo); (e) a tarefa agendada de 5 min como XML e `kit/par/07-vigia.ps1` só com `-WhatIf` (registrar é `ready-for-human`); na hora, a vigia roda em laço no terminal; (f) se couber: Config Doctor travando o plugin | `node --test` com um CouchDB dublê (respostas gravadas) e o disco do hub de ensaio, oito cenários dão o `estado.json` esperado: tudo em ordem; conflito de texto; binário descartado; replicação parada há mais de 15 min com o outro par ligado (`divergencia`); outro par desligado (`informa`, com a hora da última troca); arquivo de 201 MiB (`fsutil file createnew`, rápido); sincronizador parado; item `copia_diaria` da faixa 10. A notificação sai só na passada que piora (notificador dublê; uma real à vista do Gustavo, se ele quiser). `vigia recuperar` devolve os bytes do ramo apagado. Ponta a ponta no CouchDB de ensaio (porta 5997, com E2EE): no retrato da faixa 4, a vigia acusa o conflito e o binário **pelo caminho decifrado**; o hook de início, rodado com a entrada JSON de cada harness, devolve o resumo; o mod e a `statusLine` mostram o estado de um arquivo de exemplo | banco (faixa 4): uso o `.env.modelo` e as portas do Worker 4 desde o minuto 0; até o retrato do item 6 chegar, forjo o conflito e o ramo apagado no meu CouchDB (5997) pela API e começo sem E2EE, ligando a frase-senha antes do fim. Outro par: `HUB_OUTRO_PAR_URL` (no ensaio, o CouchDB B do Worker 4 ou um dublê parado). Kit (faixa 8): entrego `hooks/07-vigia/fragmento.json` no minuto 15, no formato do Worker 8, e o kit liga o `notify` do Codex ao meu programa. Faixa 2: hook de início próprio, separado do da nota. Faixa 10: só leio o item `copia_diaria`. Não espero ninguém |
| Worker 8 | **Portas dos harnesses e kit de par** (faixa 8; Answers dos tickets 14, 42, 13, 18, 15 e comentários do 16; a spec, em `spec-partes/faixas-07-08.md`, tem 42 histórias, e na hora cabe só o núcleo abaixo). `kit/par/instalar.ps1` e um passo por parte em `kit/par/08-*.ps1`, todos com a **trava do HOME real** (param com erro sem `HUB_HOME_ENSAIO` ou se ele for o `$HOME` real), `-WhatIf`, idempotentes, com cópia e hash antes de tocar, mais o `desinstalar.ps1`. **Núcleo, nesta ordem:** (1) conferências: nenhum `CLAUDE.md` no hub nem acima; o modo de desenvolvedor (só confere, e se estiver desligado para e explica; nunca liga); Node ≥ 22; (2) o `.env` de ensaio, juntando os `kit/par/env/<nn>.env` das faixas (nome repetido para com erro); (3) contrato: import absoluto em `<ensaio>\.claude\CLAUDE.md`, link simbólico em `<ensaio>\.codex\AGENTS.md` e em `<ensaio>\.copilot\copilot-instructions.md`, nunca físico; o que já houver ali vai para a cópia; (4) skills: uma junction por skill de `agents/skills/` em `<ensaio>\.claude\skills\` e em `<ensaio>\.agents\skills\`; (5) MCP `hub-busca` e `hub-banco` nos três harnesses, com o token por variável (nunca escrito) e `default_tools_approval_mode="approve"` no Codex; (6) hooks: junta por evento os `hooks/<nn>/fragmento.json` sem apagar o que existe; no Codex, o hash de cada hook vai para o `hooks.state`; no Copilot, só hook de usuário; o `codex.notify` do fragmento da faixa 7 vira a linha `notify`; (7) o Codex com `danger-full-access`. **Depois, se o núcleo passar até o min 35:** tirar o GSD do escopo global (no ensaio, um GSD de mentira); o mod do Claude Code de `mods/<nn>/` (onde o Claude Code lê mods: conferir na fonte antes de ligar); a `statusLine` e a extensão `onAgentStop` do Copilot; o teste mínimo do sandbox elevado do Codex, como script que registra o resultado (rodar a cada atualização é tarefa agendada, `ready-for-human`). **Fora da hora:** ver "Fica para outra execução" | `pwsh agents/test/08-kit.ps1` num HOME de ensaio novo: sem `HUB_HOME_ENSAIO`, sai ≠ 0 e não cria nada; o `-WhatIf` não muda nenhum hash; a 1ª passada liga tudo e a 2ª não muda nada; o `desinstalar` volta ao hash de antes; com um `CLAUDE.md` acima do hub de ensaio, para e diz onde está; com o `copilot-instructions.md` já ocupado, o texto antigo fica na cópia. Forma: cada link e cada junction apontam para o hub de ensaio, cada configuração tem `hub-busca` e `hub-banco` com o token por variável, os hooks juntados mantêm os de antes e os hashes do `hooks.state` batem. Ao vivo, só se o login de ensaio for liberado (pergunta do Worker 2): `claude -p` com `CLAUDE_CONFIG_DIR` de ensaio responde a pergunta que só o contrato de ensaio sabe e chama `hub-busca`. Sem login, `claude -p` com `--settings` e `--mcp-config` de ensaio prova os hooks e o MCP (a saída do Prumo 2), e o contrato fica provado só na forma | o `AGENTS.md` de ensaio (com a resposta de marca) e uma skill de marca no hub de ensaio, sem esperar as faixas 1 e 9. URLs e tokens: lê `kit/par/env/03.env` e `05.env`; até eles chegarem, um `08-dubles.env` com as URLs da tabela de portas. Fragmentos das faixas 2, 6, 7 e 9: junta o que existir em `hooks/<nn>/`; no min 0, eu mesmo ponho fragmentos de exemplo (um evento por harness) para testar a junção, e a 2ª passada, no min 45–55, pega os de verdade. Não espera ninguém |
| Worker 9 | **Skills e acervo do maestro** (faixa 9 do corte; tickets 15, 40, 43, 44 e comentário de 2026-10-12 do 16), tudo em `agents/` do hub: `skills/routing.yml` (gatilho por palavras do pedido, tipo de nota pelo caminho e papel → skill; camada geral e de papel) com as primeiras linhas (a skill do FreeLLMAPI para pesquisa, `armis-docx`, as skills de design por papel da frente da cidade); o hook de entrada sem IA que confere a tabela e injeta "use a skill X"; a família `maestro-*` (`maestro-acervo` é a porta; catálogo curto e um arquivo por peça) com o primeiro lote do Answer do 40 (papéis genéricos sem nome de cliente e o Designer, a partitura de hoje como receita e o arranjo deste workspace, contratos-opção de roteamento de modelos com o FreeLLMAPI, orquestração e onde abrir, o lembrete e a guarda); o hook de início que só age com `MAESTRI_TERMINAL_ID` e manda começar por `maestro-acervo`; a guarda do acervo (Answers do 40 e do 44; corrigida na volta 2 pelo Prumo): **arquivo novo passa**; pedem aval só alterar ou apagar peça citada ou usada, catálogo ou descrição de skill, peça com nome ou gatilho parecido com outra e contrato-opção que se diz padrão; exceção do maestro em `routing.yml`. No Claude Code, hook de settings `PreToolUse` (`ask`) e, antes do aval, o **verificador em outro modelo** por hook do tipo `agent` (experimental, aceita `"model"`; Answer do 44) com o relatório no pedido de aval; o mod fica de reserva, porque o filtro por caminho do hook é "best-effort" (44). Codex e Copilot: recusa apontando `agents/maestro/propostas/` (o Codex não tem `ask` nem hook `agent`); o registro de uso por hook em `agents/maestro/uso/<máquina>.md` (no Claude Code, dois ganchos: `PreToolUse` em `Skill` e `UserPromptExpansion`, Answer do 44); no fim da resposta, registrar se a skill indicada rodou, sem obrigar (no Claude Code **por mod**, `turn.start` com `classic.Stop`, em `mods/09-skills/`; Codex pelo hook `Stop`; Copilot pelo `agentStop`; ticket 14, como o Prumo apontou à faixa 2); `verificar-acervo`, que resolve as citações entre peças e, chamado pelo hook de início do maestro, injeta "peça X, citada por Y, sumiu" (lacuna de dono 10 do ticket 16, **proposta**); o modelo do verificador da guarda lido do contrato-opção de roteamento de modelos do primeiro lote, que o Gustavo aprova (lacuna 9, **proposta**) | `pwsh agents/test/09-skills.ps1` (crivo do Prumo 2) roda os testes dos hooks com a entrada JSON de cada harness: um pedido de pesquisa que não cita o FreeLLMAPI recebe "use a skill" dele (o aceite do ticket 15); sem `MAESTRI_TERMINAL_ID` o hook de início não faz nada, com ele injeta o lembrete; uma peça citada que foi apagada aparece no lembrete; criar arquivo novo no acervo passa; alterar uma peça citada dá `ask` no Claude Code, com o relatório do verificador, e recusa com o caminho de propostas no Codex e no Copilot, **tanto pelo caminho real quanto pelo da junction** (teste pedido no 16); o tempo de um hook `agent` em Sonnet medido e gravado (teste do 16); o maestro grava `routing.yml`; usar uma skill vira linha no registro; `routing.yml` passa no esquema e cada `SKILL.md` da família tem `name` e `description` válidos. Ao vivo, com HOME de ensaio: `claude -p` com o pedido de pesquisa mostra a injeção | o hub de ensaio (proposta do Worker 2) para `agents/`; entrega os hooks em `hooks/09-skills/` no formato de fragmento do Worker 8, sem tocar em settings de outra faixa; as junctions são do kit (faixa 8), que liga a minha pasta como ela estiver; o primeiro lote lê o Maestri e o vault só para leitura. Não espera ninguém |
| Worker 10 | **Manutenção e kit de cliente** (faixa 10 do corte; tickets 33, 34, 36, 14, rodada 7 do 56 e comentário de 2026-10-15 do 16, lacunas de dono 4 e 5), em `agents/bin/` e `kit/cliente/`: (a) `arquivar <pasta>` move para o `_archive/` da própria raiz como `_archive/<AAAA-MM-DD>--<nome>/` (a data viaja no nome, sem arquivo com ponto), só se o outro par estiver em dia (replicação nos dois sentidos sem atraso de 15 min, lida do `_scheduler/docs`) e sem edição recente na pasta; senão recusa dizendo por quê; (b) `limpar-arquivo` apaga do `_archive/` o que passou de 30 dias (é o "depois dos 30 dias" da rodada 7 do 56), com `-WhatIf`; (c) `copia-diaria`: no `.git` da raiz, ramo `par/<máquina>`, só `add`, `commit` e `push`, nunca `pull` nem `checkout`; falha alto (saída ≠ 0 e linha no estado da vigia); (d) `conferir-cabeca`: o bloco `cabeca:inicio/fim` do `AGENTS.md` existe e cabe em 2.000 caracteres (lacuna 5; a atualização em si é o fork relendo o bloco, ver fronteiras); (e) kit de cliente: no par, o TBXark/mcp-proxy com as rotas `/busca/mcp`, `/banco/mcp` (só leitura) e `/banco-escrita/mcp`, um token por rota; no cliente, `ligar-cliente.ps1` grava a linha de MCP com `Authorization: Bearer` de variável de ambiente nos três harnesses, `--allow-all-mcp-server-instructions` no Copilot CLI e o contrato na configuração global, tudo em HOME de ensaio; (f) se couber: a linha da ponte `mcp-remote` do Claude Desktop, gerada e não instalada; (g) `kit/par/10-manutencao.ps1` no contrato do kit, registrando a tarefa diária (cópia + limpeza + cabeça) só com `-WhatIf` | testes automatizados no hub de ensaio: `arquivar` move com o outro par em dia e recusa com ele atrasado ou com arquivo editado há minutos; `limpar-arquivo` apaga a pasta de 31 dias e mantém a de 29; `copia-diaria` gera commit no ramo do par e empurra para um repositório nu local, e com o remoto quebrado sai ≠ 0 e grava a linha no estado; `conferir-cabeca` recusa bloco ausente ou longo. Ponta a ponta do cliente, tudo em 127.0.0.1 no lugar da tailnet: um cliente de ensaio busca pelo proxy, lê pela rota só de leitura, tem a gravação recusada nela, e sem token leva 401; mede se o proxy repassa o `instructions` (não verificado no 14) | busca e banco (faixas 3 e 5): o proxy aponta para as URLs do `.env` do Worker 8; até elas existirem, dois MCP dublês HTTP mínimos (uma ferramenta de busca, uma de leitura e uma de gravação que respeita `READ_ONLY`), trocados pelos reais na segunda passada sem mudar o proxy. Estado do outro par (faixa 4): `arquivar` lê de uma fonte trocável, o `_scheduler/docs` do CouchDB de ensaio ou um JSON de exemplo no mesmo formato desde o minuto 0. Estado da vigia (faixa 7): só acrescento um item `copia_diaria` no formato do Worker 8. Hub de ensaio do Worker 2. Não espera ninguém |

### Corte candidato em 10 faixas (Worker 2, volta 1; ajuste à vontade)

Cada faixa é um grupo de decisões do `map.md` que entrega algo funcionando sozinho, no par 1 (esta máquina), em
`C:\context-hub` e em HOME de ensaio. Quem já assumiu outra faixa na sua linha, mantenha a sua e troque aqui.

| # | Faixa | Decisões do mapa | Prova de ponta a ponta |
|---|---|---|---|
| 1 | Esqueleto e frontmatter | 12 (raízes, núcleo de seis arquivos, `agents/blocks.md`, esquemas em `agents/frontmatter/`, `index.md`), 36 (sem `CLAUDE.md` no hub nem acima, `.git` na raiz) | criar uma iniciativa pelo script dá o núcleo de seis arquivos; o verificador aceita a nota certa e recusa a sem `status` |
| 2 | Retomada e checkpoint | 10 | ver a linha do Worker 2 |
| 3 | Busca | 09, 54 (obsidian-hybrid-search, arctic local, MCP HTTP em 127.0.0.1) | uma nota nova no hub de ensaio aparece na busca pelo MCP, em pt-BR, por palavra e por sentido |
| 4 | Banco e vista `.md` | 25, 33, 34, 47, 48 (CouchDB, LiveSync plugin e CLI como sincronizador agendado, 200 MiB, exclusão `**/.*`) | dois CouchDB locais em portas diferentes fazem de par A e par B: nota editada na pasta A aparece na pasta B (o "primeiro teste" do ticket 16, sem a segunda máquina) |
| 5 | MCP do banco com versão | 25, 11, 36, 41 (fork do MCP do es617 com `base_rev`, conflito visível, `instructions` com a cabeça do `AGENTS.md`, regra curta nas descrições de gravação) | regravar com versão velha pelo MCP vira conflito visível; com a versão certa grava |
| 6 | Guardas de gravação no disco | 11, 12 (hook que recusa regravação inteira de arquivo existente, aviso de leitura grande fora da busca, frontmatter imposto por hook) | no Claude Code, Codex e Copilot em HOME de ensaio: `Write` sobre arquivo existente é recusado; troca de trecho passa; nota sem frontmatter válido é recusada |
| 7 | Vigia e divergência | 08, 33 (a cada 5 min: colisão, sync parado há 15 min, binário descartado, arquivo grande; notificação do Windows; mod do Claude Code; recuperar binário) | com um conflito forjado no CouchDB de ensaio, a vigia avisa por notificação e o estado aparece no mod |
| 8 | Portas dos harnesses e kit de par | 14, 18, 42, 13 (link simbólico do contrato, junctions de skills, MCP nos três harnesses, modo de desenvolvedor) e o roteiro do kit | o kit roda idempotente num HOME de ensaio e os três harnesses enxergam contrato, skills e MCP |
| 9 | Skills e acervo do maestro | 15, 40, 44 (`routing.yml`, hook de entrada sem IA, família `maestro-*`, primeiro lote, guarda do acervo, hook de início com `MAESTRI_TERMINAL_ID`, registro de uso) | um prompt que casa com a tabela recebe "use a skill X"; Codex e Copilot são recusados ao gravar no acervo |
| 10 | Manutenção e kit de cliente | 33, 36, 34, 14, 16 (mover para `_archive/` conferindo o outro par, apagar após 30 dias, `.git` de cópia diária, atualizar a cabeça do contrato no MCP, kit de cliente com `mcp-proxy` e rotas) | a pasta movida pelo script vai para `_archive/`; a cópia diária gera commit; o cliente de ensaio busca pelo proxy e não grava |

## Fronteiras combinadas

(o que uma faixa entrega à outra, combinado antes, para ninguém esperar)

Propostas do Worker 2 (volta 1), para os donos confirmarem:
- **Hub de ensaio pronto antes da hora.** O maestro gera, junto com os tickets, `execucao/ensaio/hub/` na forma do
  ticket 12 (seis raízes, duas iniciativas com o núcleo, algumas notas em pt-BR, um binário pequeno). Toda faixa copia
  para a sua worktree e começa no minuto 0, sem esperar a faixa 1.
- **Contrato do instalador.** Cada faixa entrega `kit/par/<nn>-<faixa>.ps1`: idempotente, lê o HOME de
  `$env:HUB_HOME_ENSAIO` (nunca `~`), aceita `-WhatIf`. A faixa 8 só os enfileira; ninguém espera o kit.
- **Hooks no mesmo evento.** Faixas 2, 6 e 9 registram hooks nos mesmos eventos (início, fim, antes da ferramenta,
  entrada). Cada uma grava o seu script em `hooks/<faixa>/` e um fragmento de configuração; a faixa 8 junta os
  fragmentos. Sem editar o arquivo de settings de outra faixa.
- **Banco de ensaio por faixa.** Faixas 4, 5 e 7 sobem cada uma o seu CouchDB descartável em porta própria (portas
  trocadas pelo Worker 4, abaixo), pelo mesmo `compose` que a faixa 4 publica nos primeiros 10 minutos; até lá, imagem
  oficial com `.env` de ensaio.

Propostas do Worker 8 (volta 1), para os donos confirmarem:
- **MCP pelo `.env`, sem combinar porta.** O kit lê `HUB_MCP_BUSCA_URL`, `HUB_MCP_BANCO_URL` e `HUB_MCP_BANCO_TOKEN`
  do `kit/par/.env.modelo`. As faixas 3 e 5 só escrevem ali, nos primeiros 10 minutos, a URL padrão do seu servidor;
  ninguém espera ninguém para a porta.
- **Formato do fragmento de hook** (completa a proposta do Worker 2): `hooks/<faixa>/fragmento.json` com uma chave por
  harness (`claude`, `codex`, `copilot`), cada uma no formato nativo de hooks daquele harness, e o script ao lado. O
  kit junta por evento, acrescentando à lista sem apagar o que já existe; o mod do Claude Code vai em `mods/<faixa>/`.
  Quem não entregar fragmento no começo segue: o kit roda de novo no fim da hora e pega o que chegou.
- **Estado da vigia (para o Worker 7 confirmar):** o arquivo que a checagem de início e o mod leem fica fora do que
  replica (proposta: `C:\context-hub\.local\vigia\estado.json`, gravado por troca atômica), com `nivel`
  (`ok | informa | divergencia`), `resumo` de uma linha, `outro_par`, `ultima_troca` e `itens`. Esquema completo em
  `agentes/Worker 8.md`. As faixas 2 e 7 e a ferramenta reserva do MCP (faixa 5) usam um arquivo de exemplo desde o
  minuto 0.

Worker 8 (volta 2), faixa 8, para as faixas 3, 5, 6, 7 e 10:
- **Nomes dos servidores MCP no par:** `hub-busca` (faixa 3) e `hub-banco` (faixa 5, a instância com escrita). A instância
  `hub-banco-leitura` é só do proxy (faixa 10) e não vai aos harnesses do par. No Claude Code as ferramentas aparecem como
  `mcp__hub-busca__<ferramenta>`: **faixa 6, trocar o casamento `mcp__busca__*` por `mcp__hub-busca__*`**. A forma do nome
  no Codex e no Copilot: não verificado.
- **`.env` por fragmento (proposta do Prumo 2, aceita):** substitui o `.env.modelo` comum da volta 1. Cada faixa grava
  `kit/par/env/<nn>.env` (3: `HUB_MCP_BUSCA_URL`; 5: `HUB_MCP_BANCO_URL` e o nome da variável do token,
  `HUB_MCP_BANCO_TOKEN`, além das duas da instância de leitura para a faixa 10); o kit junta e gera um token de ensaio.
  O `kit/par/banco/.env.modelo` da faixa 4 é do compose e fica à parte.
- **Chaves a mais no fragmento:** `codex.notify` (um programa só, dono faixa 7, que encadeia outro se preciso) e
  `copilot.statusLine` (dono faixa 7). O mod vai em `mods/<nn>/`, com uma linha dizendo o que liga; o kit liga onde a
  fonte primária do Claude Code disser.

Worker 1 (volta 1), para a faixa 1:
- **Confirmo o hub de ensaio do Worker 2** (gerado antes da hora, na forma do ticket 12). A faixa 1 não é dona dele e
  ninguém espera por ela: ao fim, o `verificar-hub` da faixa 1 roda contra o hub de ensaio, e o que divergir vira
  ajuste no próprio hub de ensaio, não nas outras faixas.
- **Verificador de frontmatter, chamado pela faixa 6 (guardas) e pelo MCP do banco (faixa 5)** (volta 2: sem
  `agents/bin/`): `node agents/frontmatter/verificar.mjs --checar <caminho-relativo-à-raiz>` com o conteúdo pela entrada
  padrão (checa antes de gravar, não grava nada); sai 0 (válido, ou caminho sem esquema: `AGENTS.md`, `SKILL.md`,
  `agents/skills/**`, o que tem ponto) ou 1 (inválido, um motivo por linha no stderr). Sem `--checar`, sobre arquivos ou
  uma pasta, é o modo de fim de resposta e de manutenção: preenche o derivável e lista o que falta. A faixa 6 acha o
  comando por `HUB_VERIFICADOR`; o dublê, até o min 20, sai 0 sempre.
- **Exclusões geradas, para as faixas 3 e 4:** `node agents/frontmatter/exclusoes.mjs` grava
  `.local/exclusoes/livesync.txt` (um padrão por linha: `**/.*`, `**/.*/**` e cada pasta com `index.md` `local: true`) e
  reescreve no `.gitignore` só o bloco entre `# exclusoes:inicio` e `# exclusoes:fim`. A faixa 3 não precisa de mais
  nada (o obsidian-hybrid-search respeita o `.gitignore`, Worker 3); a faixa 4 lê o arquivo do LiveSync. Até o min 25, o
  dublê é o arquivo só com os dois padrões de ponto. O `.gitignore` começa com ponto e não replica: cada máquina gera o seu.
- **Textos de outras faixas no `AGENTS.md`:** só a faixa 1 escreve o arquivo; a 2 (regra de retomada) e a 9 (consultar
  o `routing.yml` onde o hook não injeta) entregam `hooks/<nn>/regra-contrato.md`, e a faixa 1 cola na junção do min
  45–55, fora da cabeça (a cabeça é da faixa 1 e fica autossuficiente).
- **Fim da resposta, com a faixa 2:** o verificador e o checkpoint correm no mesmo evento de fim (no Claude Code, o mod
  da faixa 2, ticket 14). Proposta: o verificador antes e o checkpoint depois, para a nota de retomada já sair válida. A
  fechar com o Worker 2.
- **Cabeça do contrato para o `instructions` do MCP (faixa 5):** o `AGENTS.md` abre com um bloco de até 2.000
  caracteres (Answer do 36; Prumo, volta 2) entre `<!-- cabeca:inicio -->` e `<!-- cabeca:fim -->` (o corte do Claude Code, ticket 37). A faixa 5 lê
  esse bloco; enquanto não existir, usa um texto de ensaio.

Worker 9 (volta 1), para a faixa 9 e vizinhas:
- **Confirmo o fragmento de hook do Worker 8**, em `hooks/09-skills/`. Os hooks da faixa 9 são entradas próprias nos
  eventos (entrada, início, antes da ferramenta, depois da ferramenta, fim), nunca regra dentro do script de outra
  faixa. Com a faixa 6 no mesmo "antes da ferramenta": cada uma decide só os seus caminhos (a 9 só `agents/skills/**`
  e `agents/maestro/**`); quando as duas respondem, vale a mais restritiva (recusa > aval > libera; **não
  verificado** que os três harnesses juntam assim; o Pesquisador ou o Prumo confere em fonte primária). Com a faixa 2
  no início e no fim: dois hooks no mesmo evento, cada um com o seu texto; **não verificado** que o contexto de dois
  hooks de início soma no Claude Code, no Codex e no Copilot.
- **Para a faixa 1 (frontmatter):** `agents/skills/*/SKILL.md` segue o frontmatter do padrão de skills (`name`,
  `description`), não os esquemas do hub; as peças do acervo (`agents/skills/maestro-*/**`) também. Peço que os
  esquemas e o `verificar-hub` deixem `agents/skills/**` de fora; a faixa 9 valida os seus próprios arquivos.
- **Para a faixa 1 (contrato):** onde o hook de entrada não injetar (Codex e Copilot, decisão do ticket 15), a linha
  "confira `agents/skills/routing.yml` antes de agir" vira regra no contrato daquele harness. A faixa 9 entrega o texto
  em `hooks/09-skills/regra-contrato.md` no minuto 30; a faixa 1 cola onde couber, ou fica para a segunda passada.
- **(volta 2) Lacunas de dono do ticket 16, ao Worker 10:** a faixa 9 assume a 9 (modelo do verificador: lido do
  contrato-opção de roteamento de modelos, que o Gustavo aprova) e a 10 (peça citada que sumiu: `verificar-acervo` no
  hook de início do maestro), ambas **propostas** para a spec. A 7 (registro do aval de mudança no contrato) a faixa 9
  aceita como mecanismo, se os Workers 1 e 6 concordarem: a guarda da faixa 9 também pede aval ao alterar `AGENTS.md`
  (Lições do vault: aval para o contrato) e, depois da gravação aceita, grava uma linha no registro. **O lugar do registro
  não está decidido** (o ticket 12 não o lista em `agents/`); proposta para a spec: `agents/maestro/avais/<máquina>.md`,
  como o `uso/`.
- **(volta 2) Onde moram os scripts da faixa 9:** seguem a resposta à pergunta do Prumo sobre o código do hub. No hub
  fica só o que é skill (`agents/skills/**`, `routing.yml`, peças do acervo); hooks, mod e testes vão para onde o
  código for. Até a resposta, `hooks/09-skills/` e `mods/09-skills/` na worktree, movidos por `git mv` sem esperar.
- **Linguagem dos hooks da faixa 9:** Node ≥ 22 (`.mjs`, sem pacote de fora), porque o MCP do es617 já exige Node ≥ 22
  no par. Faixas 2 e 6: se todas usarem a mesma, o kit confere uma só dependência.

Worker 10 (volta 1), para as faixas 3, 4, 5 e 7:
- **Faixa 5, cabeça do contrato:** proponho que o fork leia o bloco `cabeca:inicio/fim` do `AGENTS.md` a cada
  `initialize`, sem guardar cópia. Assim "quem atualiza a cabeça quando o `AGENTS.md` muda" (lacuna 5 do 16) é o
  próprio mecanismo, sem script de sincronia; a faixa 10 só confere, na tarefa diária, que o bloco existe e cabe.
  **Divergência a conferir pelo Prumo:** o Answer do 36 diz "até 2.000 caracteres" (margem sob o corte de 2.048); a
  proposta do Worker 1 diz 2.048. Uso 2.000.
- **Faixa 4, estado do outro par:** `arquivar` precisa de "o outro par está em dia": as duas replicações em `running`
  no `_scheduler/docs` e o último checkpoint há menos de 15 min. Peço à faixa 4 um `exemplo-scheduler-docs.json` com
  uma replicação em dia e uma atrasada, nos primeiros 10 minutos; até lá uso um que eu mesmo escrevo pelo formato da
  documentação do CouchDB (não verificado contra o CouchDB do compose).
- **Faixa 7, estado da vigia:** a falha da cópia diária entra como item `{"tipo": "copia_diaria", ...}` em `itens` do
  `estado.json` proposto pelo Worker 8; a vigia decide o nível e a notificação. A faixa 10 não notifica sozinha.
- **Faixas 3 e 5, rotas do proxy:** o proxy só precisa da URL e do token de cada servidor (as variáveis do Worker 8)
  e de um `READ_ONLY=true` numa segunda instância do MCP do banco (Answer do 34). Peço à faixa 5 que a segunda
  instância suba com a mesma linha de comando e só a variável trocada; duas instâncias do es617 por par é inferência
  não verificada no 34.

Worker 6 (volta 1), para a faixa 6 e vizinhas:
- **Confirmo a interface do verificador do Worker 1** (caminho relativo à raiz, conteúdo pela entrada padrão, sai 0 ou
  1 com o motivo no stderr) e o dublê que sai 0. O hook acha o verificador por `HUB_VERIFICADOR`, então o lugar dele
  (`agents/bin/` ou junto de `agents/frontmatter/`, apontado pelo Prumo) não me bloqueia. Peço à faixa 1 que o
  verificador saia 0 para caminho sem esquema (`AGENTS.md`, `SKILL.md`, `agents/skills/**`, pedido do Worker 9), para
  o hook não duplicar essa lista.
- **Confirmo Node ≥ 22 (`.mjs`, sem pacote de fora) e o fragmento do Worker 8**, em `hooks/06-guardas/`. Entrego o
  `fragmento.json` (chaves `claude`, `codex`, `copilot`) no minuto 15, antes do código pronto; o kit pega a versão
  final na segunda passada.
- **Com a faixa 9 no mesmo "antes da ferramenta":** a recusa de regravação inteira vale para todo o hub, inclusive
  `agents/skills/**`; a faixa 9 cuida só de quem pode gravar no acervo. Se as duas recusarem, o agente vê as duas
  mensagens, sem conflito. "Vale a mais restritiva" segue **não verificado** (pedido do Worker 9).
- **Para a faixa 3 (busca), fechado na volta 2 pela fonte primária** (README do obsidian-hybrid-search 0.16.2, `npm
  view obsidian-hybrid-search@0.16.2 readme`, seção "Available MCP tools"): as ferramentas são `search` (por `query`,
  `queries[]` ou `path`) e `read` (uma ou várias notas por caminho relativo ao cofre, conteúdo inteiro, com
  `snippet_length` para cortar); `OBSIDIAN_PREFIX` vazio por padrão, então os nomes ficam sem prefixo. Com o servidor
  chamado `hub-busca` no kit (faixa 8; Worker 5 propôs `hub-banco` e `hub-banco-leitura`, este segue o padrão), o hook
  casa `mcp__hub-busca__search` no Claude Code (Codex e Copilot, nomes de MCP na entrada do hook: **não verificado**).
  O que muda no desenho da faixa: (1) os caminhos que o `search` devolve são **relativos ao cofre**, e o hook os
  resolve contra `HUB_ROOT` antes de comparar com o Read; (2) o `read` da busca também é leitura: sem
  `snippet_length` num arquivo grande, o hook avisa como no Read do disco ("leia o trecho que a busca apontou"); com
  `snippet_length`, calado. A forma do texto devolvido pelo `search` no MCP (JSON ou tabela) **não está no README**:
  peço à faixa 3 uma resposta gravada nos primeiros 15 minutos; até lá o dublê tira do texto todo `*.md` relativo.
- **Para a faixa 2 (retomada):** com o banco fora, a mensagem de recusa da regravação inteira diz "anote a pendência
  na nota de retomada" (ticket 11, rodada 3); só texto, nenhuma dependência de código.
- **"Leitura grande":** a construção mede (ticket 11). Começo com um limite em variável (`HUB_LEITURA_GRANDE`, em
  linhas) e anoto o valor medido no relatório da faixa.
- **Crivo do Prumo 2 (volta 2), faixa 6:** prova num comando só, `pwsh agents/test/06-guardas.ps1` (roda `node --test
  hooks/06-guardas/test/` com os dublês do verificador e da busca; a parte de ponta a ponta com harness só roda com
  `HUB_E2E=1` e login de ensaio, senão é pulada e dita no relatório). Caminhos da faixa: `hooks/06-guardas/**` e
  `agents/test/06-guardas.ps1`; nenhum arquivo comum, só o `fragmento.json`. Estado por sessão do aviso de leitura em
  `.local/guardas/<sessão>.json` (fora do `.git` e do LiveSync pelo ponto, como o estado da vigia).

Worker 3 (volta 1), da faixa 3 para as faixas 1, 8 e 10:
- **Para a faixa 1 (`.gitignore` da raiz):** o índice da busca grava `.obsidian-hybrid-search.db` (e `-wal`, `-shm`) na
  raiz do hub, porque o `--db` não move o banco (achado da bancada). Peço essa linha no `.gitignore` que a faixa 1 cria;
  a regra `**/.*` já o tira do LiveSync. Atenção: o obsidian-hybrid-search respeita o `.gitignore` por padrão
  (`OBSIDIAN_RESPECT_GITIGNORE=true`, README 0.16.2), então o que for para o `.gitignore` também sai da busca.
- **Para a faixa 1 (lista de `local: true`):** se o script que gera a exclusão do sync (lacuna do Prumo para a faixa 1)
  gravar a lista num arquivo de padrões, leio esse mesmo arquivo em `OBSIDIAN_IGNORE_PATTERNS`. Até lá, só o padrão de
  ponto; a lista entra na segunda passada.
- **Para a faixa 8 (kit):** `HUB_MCP_BUSCA_URL=http://127.0.0.1:3939/mcp`, sem token (o servidor só tem a proteção do
  cabeçalho `Host`; o token fica na rota do proxy). O `03-busca.ps1` precisa de Node ≥ 22 (o mesmo do es617).
- **Para a faixa 10 (proxy):** a rota `/busca/mcp` aponta para `127.0.0.1:3939/mcp`. **Não verificado:** se o
  TBXark/mcp-proxy repassa o `Host` do cliente ou põe o do destino; se repassar o do cliente, o servidor recusa. Conserto
  sem esperar: eu subo com `--allowed-host` para o endereço do proxy que a faixa 10 me disser (padrão `127.0.0.1:<porta
  do proxy>`).

Worker 5 (volta 1), faixa 5 (MCP do banco), para as faixas 1, 4, 6, 7, 8 e 10:
- **Confirmo** a cabeça do contrato do Worker 1 (bloco `cabeca:inicio/fim`) com a leitura a cada `initialize` proposta
  pelo Worker 10, até **2.000** caracteres (Answer do 36). Isso fecha a lacuna 5 do 16 pelo próprio mecanismo. No fork,
  a cabeça vem **antes** do texto do upstream: o `MCP_INSTRUCTIONS_FILE` do upstream só **acrescenta** ao fim, é lido
  na partida e derruba o servidor se faltar (README do es617), então não serve como está. O tamanho do texto próprio
  do upstream é não verificado.
- **Confirmo** a ferramenta reserva do Worker 7, com o nome `estado_do_hub`; o caminho vem de `HUB_VIGIA_ESTADO`
  (padrão `C:\context-hub\.local\vigia\estado.json`); sem arquivo, devolve "vigia sem estado neste par".
- **Confirmo** a segunda instância do Worker 10: a mesma linha de comando, só `READ_ONLY=true` e o token trocados. Duas
  instâncias do es617 sobre o mesmo CouchDB não foram testadas; é o teste 5 da faixa.
- **Faixa 6:** a mensagem de recusa cita `write_note` com `base_rev` (o valor que `read_note` devolve). O nome do
  servidor nos harnesses é do kit (faixa 8); proponho `hub-banco` e `hub-banco-leitura`.
- **Faixa 4, E2EE e o R1 (volta 2):** com o R1 pela recusa 409 do CouchDB, o fork não monta pedaço à mão como o
  `r1.py` (que grava texto claro e só vale sem E2EE): os pedaços seguem pelo caminho de gravar (e cifrar) do próprio
  upstream, e só o documento de metadados leva `_rev = base_rev`. Onde o upstream busca a revisão atual antes de
  gravar (provável, não verificado no código) é o ponto a trocar. Se o caminho do upstream esconder o `_rev`, essa é a
  parte que vai ao Fable 5.1 médio.
- **Ritmo da hora (10 subagentes):** min 0–10 clonar, compilar e subir o upstream contra a 5996, `.env.modelo` e
  dublês prontos; min 10–40 em paralelo (a) R1, (b) conflito visível, (c) `instructions` e descrições, (d)
  `estado_do_hub` e a instância de leitura, (e) o roteiro de testes e2e; min 40–50 E2EE e o `05-mcp-banco.ps1`;
  min 50–60 revisão dos Prumos e o estado gravado. A guarda de frontmatter (g) só entra se sobrar tempo.

Worker 4 (volta 1), banco de ensaio (faixas 4, 5 e 7):
- **Portas 5994 a 5997, não 5984.** O compose do spike (`C:\Projetos\spike-livesync\`, que o Worker 8 citou como fonte
  de fixture) usa `127.0.0.1:5984` e guarda os dados dos testes 30 e 48; subir o spike na hora bateria. Ficam: faixa 4,
  5994 (par A) e 5995 (par B); faixa 5, 5996; faixa 7, 5997. Só 127.0.0.1.
- **O `.env` do banco**, publicado pela faixa 4 no minuto 0–10 em `kit/par/env/04.env` (fragmento, como o Prumo 2
  propôs na volta 2; as faixas 5 e 7 usam os mesmos nomes desde o minuto 0): `HUB_COUCHDB_URL`, `HUB_COUCHDB_USER`, `HUB_COUCHDB_PASSWORD`,
  `HUB_COUCHDB_DB` (`hub`), `HUB_E2EE_PASSPHRASE` (de ensaio), `HUB_SYNC_MAX_MB` (200). Imagem `couchdb:3` com a versão
  exata do ticket 48 (3.5.2), `couchdb.ini` do spike sem `[admins]` fixo.
- **E2EE está decidida e muda as faixas 5 e 7** (ticket 34, "Segurança"; o 48, item 11, mostrou que com E2EE v2 o
  caminho fica cifrado no servidor e `size`, `mtime` e `children` zerados). Faixa 5: o fork do MCP recebe a frase-senha
  (o 30 cita "E2EE com a passphrase também no MCP"). Faixa 7: lendo só o `_conflicts`, a vigia sabe que há conflito mas
  não em qual arquivo; para dizer o caminho precisa decifrar (o ticket 09 decifrou no Node com `livesync-commonlib`
  0.1.36). Proposta: as duas testam primeiro sem E2EE e ligam a frase-senha do `.env` antes do fim da hora; o retrato
  do item 6 da faixa 4 sai com E2EE.

Worker 4 (volta 2), da fonte do CLI do LiveSync (`C:\Projetos\spike-livesync\livesync-src`, commit `1414144`, o
mesmo do ticket 48; lido, não executado):
- **Exclusão do que tem ponto: pelo `.livesync/ignore`, não pela regra embutida.** A regra embutida
  (`src/apps/cli/main.ts`, `isTargetFile`) corta o caminho por `path.sep` e descarta se alguma parte começa com ponto.
  No Windows `path.sep` é `\`; se o caminho chega com `/` (a forma do LiveSync), só a primeira parte é vista: o `.git`
  da raiz cai e o `projeto/.git` passa. É exatamente o defeito 8 do ticket 48 (**inferência pela fonte, não
  verificada**; o teste N4 confere). O `.livesync/ignore` (`serviceModules/IgnoreRules.ts`) troca `\` por `/` antes de
  casar, usa minimatch com `dot: true`, põe `**/` na frente de padrão sem barra e `**` atrás de padrão terminado em
  barra. Então as duas linhas `.*` e `.*/` viram `**/.*` e `**/.*/**`, a regra decidida. O arquivo mora em
  `C:\context-hub\.livesync\ignore`, numa pasta com ponto: não replica e é escrito pelo kit em cada par. O formato
  aceita `import: .gitignore` (só esse) e recusa negação (`!`). **Para o dono do script de `local: true`:** o destino
  no CLI é esse arquivo, uma linha `pasta/` por pasta local. Não importar o `.gitignore` inteiro, porque a busca também
  o respeita (Worker 3) e a pasta local continua buscável no próprio par.
- **Para a faixa 7 (vigia), o CLI já decifra.** Comandos do próprio CLI (`main.ts`, ajuda): `ls [prefixo]` lista
  `caminho, tamanho, mtime, revisão[*]`; `info <caminho>` mostra revisão, conflitos e pedaços; `cat-rev` e
  `pull-rev <origem> <destino> <rev>` tiram uma revisão para um arquivo. Com a E2EE, ele dá o caminho em claro (é
  cliente com a frase-senha). Assim o `vigia recuperar` pode ser `pull-rev` para um arquivo ao lado, e o nome do
  arquivo em conflito vem de `ls` e `info`, sem a vigia decifrar sozinha. **Não verificado:** um segundo processo do
  CLI no mesmo banco local com o `daemon` rodando (o banco local é LevelDB, que costuma travar o diretório). Saída:
  a vigia usa um banco local próprio (`--settings` de um segundo dispositivo, `sync` a cada passada), o "segundo CLI"
  que o ticket 09 já citou.
- **Setup URI sem o assistente:** o CLI só aplica (`setup <setupURI>`); quem gera é
  `encodeSettingsToSetupURI(settings, frase)` da `livesync-commonlib`, chamado no teste do próprio CLI
  (`commands/runCommand.unit.spec.ts`). Um script Node do kit gera o URI para o plugin, e a frase-senha vai por outro
  canal (34). Não verificado de ponta a ponta; na hora fica no item S3 do kit, se sobrar.
- **Exemplos do agendador de replicação (Workers 10 e 7):** no min 15, `scheduler-docs-em-dia.json` (as duas
  replicações em `running`) e `scheduler-docs-parado.json` (o CouchDB B parado por um instante) em
  `execucao/ensaio/banco/`, tirados do CouchDB de ensaio. Até lá, cada um usa o dublê que escreveu pela documentação.

Worker 7 (volta 1), faixa 7 (vigia), para as faixas 2, 4, 5, 8 e 10:
- **Confirmo o estado da vigia do Worker 8**, com três ajustes: (1) `itens[].tipo` ganha `copia_diaria` (Worker 10) e
  passa a usar hífen em todos (`copia-diaria`); (2) cada item leva o seu `nivel`, e o `nivel` do topo é o pior deles;
  (3) o mapa dos níveis segue o glossário do ticket 33: `divergencia` para conflito aberto, binário descartado,
  replicação parada há mais de 15 min com o outro par ligado e arquivo acima de 200 MiB; `informa` para outro par
  desligado (com `ultima_troca`). **Proposta minha, não decidida:** sincronizador parado e Config Doctor travado como
  `divergencia` (impedem a troca, e esperar os 15 min atrasaria o aviso); cópia diária falha como `informa` com
  notificação. Caminho `C:\context-hub\.local\vigia\estado.json`: a pasta com ponto fica fora do banco (Worker 4) e
  **também do `.git` de cópia diária** (faixa 10: `.gitignore` com `.local/`).
- **Faixa 2:** a checagem de divergência no início de sessão é um hook **meu**, separado do hook da nota de retomada;
  os dois no mesmo evento, cada um com o seu texto (não verificado que dois contextos de início somam: o mesmo ponto do
  Worker 9).
- **Faixa 5:** a ferramenta reserva da checagem de início (onde não há arquivo da vigia e no cliente) lê o mesmo
  `estado.json` do par e devolve `nivel` e `resumo`; sem arquivo, devolve "vigia sem estado neste par".
- **Faixa 8:** o `notify` do Codex é um programa só por configuração (não verificado na fonte do Codex): ele é da faixa
  7; se outra faixa precisar do `notify`, o meu programa chama a seguinte em cadeia, sem trocar a linha.
- **Faixa 4:** peço no retrato do item 6, além do conflito e do binário com ramo apagado, o `_scheduler/docs` de uma
  replicação parada (gravado como JSON); é o que falta para os oito cenários saírem de dado real.

## Conferência das decisões (Prumo)

Volta 2: as dez faixas contra o `map.md`, os Answers e os comentários do ticket 16. Inventário com a fonte de cada item
em `agentes/Prumo.md`. Dono de cada faixa: absorva na sua linha o que é seu e apague o item daqui. Já absorvidos desde a
volta 1, e por isso fora da lista: gemini e `FREELLM_BASE_URL` (3); `mark-resolved`, 200 MiB, pastas com ponto, 50 MiB
(4); duas instâncias e `estado_do_hub` (5); `statusLine` e `notify` (7); `/banco-escrita/mcp`, ramo por máquina e os 30
dias (10).

**Contraria decisão (corrigir):**
- **Todas as faixas: `kit/`, `hooks/`, `mods/` e `busca/` na raiz do hub** (apontado pelo Prumo 2 e pelo Worker 7,
  conferido pelo Prumo). O ticket 12 fixa a raiz em `AGENTS.md`, as seis raízes e o `agents/` com conteúdo listado; o 33
  manda o repositório de código morar fora do hub; e um `.git` dentro do hub não replica (pasta com ponto), então um
  repositório de código ali dentro chegaria à outra máquina sem histórico. **Recomendação:** o código da construção
  (kits, hooks, mods, vigia, scripts da busca, testes) mora num repositório próprio fora do hub, como o fork do MCP do
  banco (Worker 5): proposta `C:\Projetos\context-hub-codigo`, com as dez worktrees **nele**, e não no `.git` do hub, que
  é só a cópia diária da vista. No hub ficam só o conteúdo e as skills (`AGENTS.md`, as raízes, `agents/skills/**` com os
  scripts que cada skill leva, `agents/frontmatter/`, `blocks.md`, `routing.yml`). Os hooks no escopo do usuário apontam
  para o repositório de código, que o kit de par clona. **Para ninguém esperar:** toda faixa escreve os caminhos de código
  relativos a `$env:HUB_CODIGO` e os de conteúdo relativos a `$env:HUB_ROOT`; a resposta do Gustavo só troca o valor
  dessas duas variáveis. Vai em "Perguntas ao Gustavo".
- **Faixa 6: recusar o `Update File` "que troca tudo" vai além da decisão.** O Answer do 11 recusa no disco o Write do
  Claude Code, criar e regravar do `apply_patch` e criar do Copilot; o `Update File` está na lista do que é seguro (recusa
  quando o próprio trecho mudou). Tire do hook ou registre como decisão nova para a spec.
- **Faixa 7: sincronizador parado como `divergencia` imediata muda o termo do glossário.** Pelo 33, divergência é colisão
  real, arquivo acima de 200 MiB e máquina sem levar as mudanças há mais de 15 min com a outra ligada. Sincronizador
  parado vira divergência pela regra dos 15 min; antes disso, proponho `informa` com notificação. Config Doctor travado
  idem.
- **Cabeça do contrato: 2.000 caracteres, não 2.048.** O Answer do 36 diz "cabeça autossuficiente de até 2.000
  caracteres, pelo corte de 2.048 do Claude Code". Os Workers 5 e 10 já usam 2.000; corrigi a fronteira do Worker 1.

**Nenhuma faixa pega ainda (com a faixa que eu sugiro):**
- Faixa 10: **o `.secrets/` aninhado não chega ao GitHub** (12, "teste antes do primeiro segredo"). A faixa 4 testa o
  banco; ninguém testa o `.git` da cópia diária. Com o `.gitignore` com `**/.*` (o Worker 3 lembra que a busca respeita o
  `.gitignore`), o teste da `copia-diaria` confere que `.secrets/x` não entra no commit.
- Faixa 9: as três lacunas de dono do 16 que o Worker 10 passou: onde fica o registro do aval de mudança no contrato,
  quem escolhe o modelo do verificador da guarda e como o erro de peça citada que sumiu chega ao Gustavo. Precisa do
  "sim" do Worker 9 na linha dele.
- Sem dono, e cabe registrar em "Fica para outra execução": a pasta conectada do Claude Desktop no Cowork, com "Folder
  instructions" apontando o `AGENTS.md` (11); a faixa 10 só gera a linha da ponte `mcp-remote`.

**Fora do mapa, não construir:** o ticket 56 (system design) está `claimed`, não resolvido. Da rodada 7 dele, só os 30
dias do `_archive/` entraram na construção, pelo comentário de 2026-10-15 do 16. "Nota nova do Obsidian nasce em
`inbox/`" e "agente só remove com permissão ou depois dos 30 dias" não estão em ticket resolvido nem no 16. Ninguém
constrói guarda de remoção nem regra de `inbox/` nesta execução.

**Decisões que caíram (não construir):** marcador de raiz e `project_root_markers` (ticket 14, rodada 4; os Answers de 36
e 40 ainda os citam); consulta ao TI antes do Tailscale (Gustavo, 2026-10-14); GitHub como ponto de encontro e o
git-sync (33); "colisão para a máquina inteira" (33); limite de 30 min, agora 15 min (33); Claude Desktop só de leitura
(revisão do 36); "Tailscale fora da construção inicial" (06, revisto por 33 e 34; o servidor SSH segue fora).

**Fora do escopo (não inventar):** controle de acesso por pasta; `freellmapi-mcp`; edição concorrente Obsidian × agente
no mesmo arquivo; o hub controlando harnesses e modelos (segundo mapa); migrar workspaces do Maestri e a automação que
aplica e audita o Maestri; SOC STRATA; qualquer mudança no vault.

## Revisão (Prumo e Prumo 2)

(como e quando cada faixa passa pelos dois, dentro da hora)

### Crivo de construção (Prumo 2, volta 1): toda faixa passa nos oito

1. **Prova num comando só:** `pwsh agents/test/<nn>-<faixa>.ps1` (ou `pytest` equivalente) roda numa worktree limpa,
   sem passo manual, e sai 0 (passou) ou ≠ 0 (falhou, com o motivo). A coluna "Entrega" de cada faixa vira esse teste.
2. **Cabe na hora:** nada que a fonte do mapa estime em dias entra inteiro; a faixa diz o núcleo que cabe e manda o
   resto para "Fica para outra execução". Download, imagem e dependência vêm **antes da hora**.
3. **Nada global:** o diff não tem `~/.claude`, `~/.codex`, `~/.copilot`, `$HOME`/`%USERPROFILE%` fixo,
   `Register-ScheduledTask`/`schtasks`, `New-Service`, `setx`, `HKCU:`; todo HOME vem de `$env:HUB_HOME_ENSAIO`.
4. **Serviço só de ensaio:** contêiner com nome `hub-ensaio-<faixa>-*`, porta em `127.0.0.1` (nunca `0.0.0.0`),
   apagado pelo próprio teste ao fim; nada de `git push` ao GitHub (remote é um repositório local vazio).
5. **Dublê declarado:** o que a faixa usa de outra tem dublê nomeado na fronteira, e o teste do item 1 passa com ele.
6. **Caminhos próprios:** cada faixa só grava nos caminhos que são dela (tabela de donos a fechar na volta 2); arquivo
   comum (`AGENTS.md`, `.env.modelo`, settings) só por fragmento, para a junção do fim não ter conflito.
7. **Sem credencial:** nenhum teste lê ou copia arquivo de login ou token de verdade; token de ensaio é gerado.
8. **Fonte marcada:** comportamento de ferramenta que a faixa assume e não conferiu em fonte primária fica marcado
   "não verificado" no ticket, com o teste que o confere.

### Rito na hora (proposta do Prumo 2, a fechar com o Prumo)

- **Min 0–10:** os Prumos conferem as fronteiras publicadas (nomes, assinaturas, `.env.modelo`) contra o plano.
- **Min 20–40:** cada faixa avisa "pronta para revisão" por `maestri ask` assim que o item 1 passa; o Prumo 2 roda o
  teste numa worktree limpa e passa o crivo; o Prumo confere contra as decisões. Devolução em uma linha, por item.
- **Min 45:** corte: o que não passou nos dois vai para "Fica para outra execução" com o estado gravado.
- **Min 45–55:** junção das faixas aprovadas em ordem fixa (1 primeiro, kit da 8 por último) e o teste de todas juntas.
- **Min 55–60:** estado final gravado; nada novo começa.

### Antes da hora (sem isso, alguém espera no minuto 0)

- **Docker Desktop no ar:** o daemon **não está rodando** nesta máquina (conferido 2026-10-15 ~21h45); faixas 4, 5 e 7
  dependem dele. As imagens do CouchDB baixadas antes.
- Dependências baixadas: modelo arctic-embed-m-v2.0 e obsidian-hybrid-search (faixa 3), o repositório do MCP do es617
  com `npm install` (faixa 5), o CLI do LiveSync (faixa 4).
- `C:\context-hub` criado com o `.git` de cópia diária (só conteúdo) e o hub de ensaio; o repositório de código fora
  do hub (`$env:HUB_CODIGO`, proposta `C:\Projetos\context-hub-codigo`, pergunta ao Gustavo) com as dez worktrees e os
  hooks de evento do painel em cada uma (corrigido na volta 2 pelo aviso do Prumo).
- Faixa 1: o pacote `yaml` do npm instalado em `agents/frontmatter/`; os valores de `kind`, `size` e `cadence` e o texto
  "entra / não entra" dos blocos tirados da caixa do portal (rodadas 14 e 15 do 12) para um arquivo de ensaio.
- Conferidos aqui: Node v24.19.0, Python 3.12.10, git 2.55, ripgrep 14.1.1, modo de desenvolvedor ligado.

### Riscos de tamanho (Prumo 2, volta 1)

- **Faixa 5:** o ticket 26 estima a guarda de revisão do MCP em 1 a 2 dias. Na hora cabe o núcleo (`write_note` com
  `base_rev` que recusa versão velha com conflito visível, mais o `instructions`); candidata a Fable.
  (Worker 5, volta 2) O tamanho cai: a estimativa do 26 era montar a revisão-pai pela biblioteca do LiveSync; com a
  recusa 409 nativa do CouchDB, o núcleo é passar `base_rev` como `_rev` na gravação do metadado e traduzir o 409.
- **Faixa 4:** o ticket 30 estima a montagem em 3 a 3,5 dias. Na hora cabem os dois CouchDB locais replicando e o CLI
  espelhando nos dois sentidos.
  Resposta do Worker 4 (volta 2): a linha da faixa ganhou ordem de corte, com núcleo N1 a N4 até o min 35 e S1 a S6 se sobrar.

### Crivo aplicado às 10 linhas (Prumo 2, volta 2)

Todas as linhas têm prova automatizada (item 1) e dublê declarado (item 5). Faltam três coisas comuns e alguns pontos
por faixa. Dono: absorva na sua linha e apague o item daqui.

**Comum a todas (proposta; sem isso a junção do min 45 trava ou alguém toca o HOME real):**
- **Trava do HOME real (item 3):** todo `kit/**/*.ps1` e todo teste que grava em HOME **para com erro se
  `HUB_HOME_ENSAIO` não estiver definido ou apontar para o `$HOME` real**; não há opção "real" nesta execução. Teste
  próprio na faixa 8: rodar o kit sem a variável sai ≠ 0 e não cria nada.
- **Portas (item 4), uma tabela só, tudo em 127.0.0.1:** 3939 e 3940 busca (3); 5994 e 5995 par A e B (4); 5996 (5);
  5997 (7); 8796 e 8797 MCP do banco escrita e leitura (5); **proposta para a 10, a confirmar:** 8798 proxy, 8790 e 8791
  os dois MCP dublês. Ocupadas fora da construção: 8770 portal, 8771 painel, 5984 spike, 3001 FreeLLMAPI. Contêiner com
  nome `hub-ensaio-<faixa>-*`, apagado pelo próprio teste.
- **Arquivos comuns sem conflito na junção (item 6):** `kit/par/.env.modelo` é escrito por 3, 5, 8 e 10: proposta, cada
  faixa grava `kit/par/env/<nn>.env` e o kit da 8 junta (como os fragmentos de hook). `.gitignore` e `AGENTS.md` são
  só da faixa 1, que já põe no min 0 as linhas pedidas no plano (`.local/`, `.obsidian-hybrid-search.db*`); texto de
  outra faixa para o contrato vem em `hooks/<nn>/regra-contrato.md` (como a 9 propôs). Fora isso, cada faixa grava só
  nos caminhos da sua linha.

**Por faixa:**
- **1:** absorvido (Worker 1, volta 2): sem `agents/bin/`; scripts em `agents/frontmatter/` e na skill.
- **2:** a prova com `claude -p` "com HOME de ensaio" depende de login copiado (item 7) e do mod carregar no `-p`
  (Prumo). Saída sem login: `claude -p --setting-sources project,local --settings <ensaio>.json` (opções conferidas no
  `claude --help`); o mod no `-p` vira teste com resultado registrado, verde ou vermelho.
- **3:** o modelo arctic e o `npm install` do obsidian-hybrid-search vêm antes da hora (item 2); o teste do gemini só
  com o aval já perguntado.
- **4:** absorvido na linha do Worker 4 (volta 2).
- **5:** clonar o es617 e `npm install` antes da hora (item 2); o resto está no ritmo da linha. Se a E2EE não fechar até
  o min 45, entrega R1 sem E2EE, como a linha já diz.
- **6:** a ponta a ponta nos três harnesses depende do login (item 7); sem ele, a prova de escopo de projeto da bancada
  conta como aceite, e o Copilot ao vivo fica `ready-for-human`.
- **7:** escopo largo para uma hora (seis partes, oito cenários, três harnesses e um mod). Ordem de corte proposta:
  (a), (b) e (c) com os oito cenários primeiro; (d) só o hook de início e o mod; `statusLine`, `notify` e (f) cortam
  primeiro. `livesync-commonlib` instalado antes da hora.
- **9:** o hook `agent` em Sonnet chama modelo de verdade (custo pequeno, permitido: sem limite de tokens); fora isso,
  nada a corrigir.
- **10:** o binário do TBXark/mcp-proxy baixado antes da hora (item 2); a porta do proxy e dos dublês na tabela acima.

## Fica para outra execução

- (Worker 1, volta 2) Do verificador: conferir e corrigir links `par://` nos dois sentidos (pede `agents/machines/` e o
  perfil por máquina, que segue em "Not yet specified"); o aviso de três notas parecidas em `other/`; o teste das portas
  com `codex exec` e `copilot -p` lendo o `AGENTS.md` (depende de login no HOME de ensaio; é da prova do kit, faixa 8).

- (Worker 8, volta 2) Da faixa 8: a instalação de verdade no HOME real (com cópia e hash, `ready-for-human`);
  `claude-md-and-agents-md` e o preset `custom` do Copilot no Maestri (configuração global do Maestri); a prova ao vivo de
  `~/.agents/skills` no Codex e no Copilot, que vai ao teste da instalação de verdade (com `COPILOT_HOME` o Copilot não
  lê essa pasta, e o Codex acha a pasta pelo home do sistema; se ele segue um `USERPROFILE` trocado, não verificado); o
  MCP do VS Code no escopo do usuário (sem decisão); a captura da requisição do Codex com o MCP pronto (depende do login
  e dos servidores); a pasta conectada do Claude Desktop com "Folder instructions" (a faixa 10 só gera a ponte); o teste
  do sandbox elevado como tarefa agendada; a pendência do ticket 45 (`C:\teste45` e o `trust_level` do Codex).

- (Worker 1, volta 1) Trazer esta frente (a prova de conceito) para o hub: "Como esta prova de conceito vira o hub
  real" está em "Not yet specified" no mapa.

- (Worker 2, volta 1) O segundo par (notebook), o Tailscale e os grants, a replicação real pela tailnet, o FreeLLMAPI
  nativo no notebook pessoal e a instalação de verdade em `~/.claude`, `~/.codex` e `~/.copilot`: tudo
  `ready-for-human`, com o Gustavo.

- (Worker 4, volta 1) Da faixa 4: o plugin LiveSync no Obsidian (configuração por tela, com `syncMaxSizeInMB` 200 e a
  exclusão; o Setup URI sai pronto do kit se o CLI o gerar, não verificado); registrar de verdade a tarefa agendada do
  sincronizador; a tela de colisão de três vias (ticket 25, "logo depois da construção").

- (Worker 9, volta 2) Da faixa 9: o verificador em outro modelo **fica na hora** (a fonte é o Answer do 44); vai para a
  próxima execução só se o hook `agent` não rodar ou passar do tempo no teste. Ficam: o `$.ui.ask` num terminal do Maestri sem ninguém olhando e os hooks de uso e de início ao vivo no Codex e no Copilot
  (dependem da pergunta de login do Worker 2), ambos `ready-for-human`; e a passagem do GSD para fora do escopo
  global, que é do kit (faixa 8).

- (Worker 10, volta 1) Da faixa 10: a chave efêmera com tag e o grant da tailnet do cliente, o proxy preso ao IP real
  da tailnet, a instalação da ponte do Claude Desktop em `%APPDATA%\Claude` e o registro da tarefa diária de verdade
  no Agendador: `ready-for-human`. As lacunas de dono 7 (registro do aval de mudança no contrato), 9 (modelo do
  verificador) e 10 (erro de peça citada que sumiu) parecem da faixa 9, que já trata aval e peça; a confirmar pelo
  Worker 9.

- (Worker 7, volta 1) Da faixa 7: registrar de verdade a tarefa agendada da vigia; a notificação real em loop no
  Windows do Gustavo; o Config Doctor, se a leitura sem o Obsidian aberto não sair na hora (não verificado como
  detectar); a vigia no segundo par, com o outro par pela tailnet. Todos `ready-for-human` ou próxima execução.

- (Worker 3, volta 1) Da faixa 3: ligar a busca no boot de cada par (tarefa agendada) e o `--host` na interface da
  tailnet: `ready-for-human`; o tempo "edição no outro par → busca" com o LiveSync de verdade; o gemini ligado, que é
  escolha do Gustavo (09). A reserva Robusta continua onde está (`bancada-busca/scripts/robusta/`).

- (Worker 5, volta 1) Da faixa 5: publicar o fork no GitHub e a PR do R1 ao upstream (es617), que são para fora;
  a validação de frontmatter dentro do MCP, se não couber; o MCP do banco no Claude Desktop pela ponte `mcp-remote`
  e o teste dos três harnesses com o MCP pronto, capturando a requisição do Codex (dependem do login de ensaio).

## Perguntas ao Gustavo

- (Worker 8, volta 2) **O GSD no arquivo global do Copilot.** Os tickets 36 e 42 e o comentário de 2026-10-12 do 16
  dizem que o kit junta o contrato com as instruções do GSD em `~/.copilot/copilot-instructions.md`; o 15, mais novo, diz
  que o GSD sai do escopo global, com cópia. Recomendação: vale o 15. O arquivo vira só o link para o `AGENTS.md` e o
  texto do GSD fica na cópia do kit.

- (Prumo, volta 2, levantada pelo Prumo 2) **Onde mora o código do hub (kits, hooks, mods, vigia, scripts, testes)?**
  O ticket 12 fixa a raiz do hub em `AGENTS.md`, seis raízes e `agents/`; o 33 diz que repositório de código mora fora do
  hub. Recomendação: num repositório próprio fora do hub (`C:\Projetos\context-hub-codigo`, só local nesta execução,
  publicado depois com o seu aval), com as worktrees da construção nele; no hub, só o conteúdo e as skills. A
  alternativa é pôr o código dentro de `agents/`, que replica sozinho para a outra máquina, mas leva um estrago de código
  às duas máquinas em segundos e entra como decisão nova sobre a árvore do ticket 12.

- (Worker 2, volta 1) **CouchDB descartável no Docker local conta como "serviço"?** As faixas 4, 5 e 7 precisam de
  CouchDB em porta local, só durante a hora, apagado ao fim. Recomendação: liberar contêineres de ensaio em
  127.0.0.1, sem tarefa agendada de verdade (a tarefa do sincronizador e da vigia roda em laço no terminal).
  - (Worker 4, volta 1) Fato para esta pergunta: **o Docker Desktop está desligado agora** (`docker ps` em
    2026-10-15 não acha o pipe do motor). Então o aval inclui ligar o Docker Desktop antes da hora. Recomendação: o
    Gustavo liga o Docker Desktop antes de a execução começar e o desliga ao fim. A alternativa, o CouchDB nativo do
    Windows, também é serviço e é instalação nova.
- (Worker 2, volta 1) **Login dos harnesses no HOME de ensaio.** Provar que Codex e Copilot leem o contrato num
  `CODEX_HOME`/`COPILOT_HOME` de ensaio pede uma sessão autenticada lá. Recomendação: copiar só o arquivo de login
  para o HOME de ensaio e apagá-lo ao fim; a alternativa é provar só a forma dos arquivos, sem rodar o harness.
  - (Prumo 2, volta 1, regravado na volta 2 porque uma edição simultânea apagou) Terceira saída, sem copiar login: o
    Claude Code tem `--setting-sources project,local`, `--settings <arquivo>` e `--mcp-config` com
    `--strict-mcp-config` (conferido no `claude --help`), então roda com o login atual e hooks e MCP de ensaio sem
    gravar em `~/.claude`; o Codex tem `-c chave=valor` sobre o `config.toml` (`codex --help`), mas hooks por `-c` são
    **não verificados**; o Copilot só tem o `COPILOT_HOME` (não verificado se há outra saída). Recomendação do Prumo 2:
    Claude Code e Codex por essas opções; o Copilot ao vivo `ready-for-human`.
- (Worker 1, volta 1) **Copiar os pilotos já desejados nesta execução?** O ticket 02 diz que `armis-docs`,
  `armis-brand` e a skill `armis-docx` são copiados do vault "quando o Gustavo disser". Recomendação: sim, só cópia
  (o vault não muda), pela faixa 1, depois do esqueleto pronto; se não, ficam para outra execução.
- (Worker 3, volta 1) **Teste único do gemini-embedding-001 pelo FreeLLMAPI nesta hora?** O Answer do 09 pede a
  configuração escrita, testada uma vez num índice ao lado do arctic e deixada desligada. O teste manda as notas do hub
  de ensaio (texto sintético, sem dado de cliente) ao Google e gasta cota do gateway: uma indexação de cerca de 20 notas
  pequenas, da ordem de dezenas de chamadas de embedding (estimativa, não medida). O FreeLLMAPI roda no Docker desta
  máquina, que está desligado (fato do Worker 4). Recomendação: sim, se o Docker já for ligado para as faixas 4, 5 e 7;
  senão a configuração fica escrita e sem teste, e o teste vai para outra execução.
- (Worker 5, volta 1) **Onde mora o fork do MCP do banco?** É código (TypeScript), e o ticket 33 diz que repositório de
  código mora fora do hub. Recomendação: nesta execução, só local, em `C:\Projetos\hub-mcp-banco` (git próprio, clonado
  do es617); publicar no GitHub (fork público ou repositório privado) fica para depois, com o seu aval.
- (Worker 1, volta 2) **Tabela `stage` → `status`.** O 12 decidiu a regra (o verificador deriva `status` de `stage`), não
  a tabela. Recomendação: `rascunho` para backlog, draft, proposed, open; `em uso` para doing, on-hold, active, approved,
  review, delivered, answered; `superada` para done, archived, superseded, dropped, closed, torn-down. Fica nos esquemas
  como dado: trocar depois não muda código.
- (Worker 1, volta 2) **`operations/` e `reference/` levam o núcleo inteiro?** (ponto aberto do 12). Recomendação: sim
  em `operations/` (trabalho contínuo tem retomada e tarefas); em `reference/` só `index.md` e as notas. Até a resposta,
  a skill cria o núcleo em `clients/` e `initiatives/` e aceita as outras duas sem núcleo.

- (Worker 7, execução de 2026-10-15) A faixa 7 inteira: parou no início pelo limite de uso. Ramo `faixa-07` só com o contrato e o dublê do CouchDB; estado no `## Comments` do ticket 07.
- (Worker 3, parada das 21h56) Faixa 3: falta o iniciar.ps1, o 03-busca.ps1, o gemini.env, a linha do .env.modelo e rodar o aceite; estado no ticket 03, ramo faixa-03 (2c70cdb).
