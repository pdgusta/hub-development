# Relatório do ticket 25: junção e prova do hub de ensaio inteiro (preparo)

Vela, 2026-10-17. Ramo `ticket-25`, worktree `C:/context-hub-wt/ticket-25`, de `integracao` e98a891. Preparo por
mandato do maestro (08:33): costuras e roteiro sobre o que já está em `integracao`, estendido quando as outras peças
entrarem. Costuras aceitas (09:00): `etapas/costuras-25-Vela.md`.

## Decisões do maestro (09:00)

1. `wsl --shutdown` pelo corredor, só com a trava e sem contêiner `hub-ensaio-*` de outro ticket.
2. Limite de memória só nos contêineres do ensaio. Saiu por `docker update --memory 384m --memory-swap 384m` depois da
   subida (ideia da Brasa, que o usa no 22): não toca o `-f` fixo do `Invoke-Compose` nem o kit. Se o CouchDB cair por
   ele, o relatório diz.
3. Busca em fase separada (junto com os pares não cabe hoje).
4. Agora só o leve; a rodada real pela fila.

## O que se fez (commits 92ee004, cb45dae, 1c30e48, 974d74d)

- `agents/code/test/ponta-a-ponta/25/medidor.ps1`: amostra a cada 2 s a memória livre, a `vmmemWSL`, a soma dos `node`
  do ensaio e (a cada 5 amostras) os contêineres `hub-ensaio-25-*`, com a fase que o orquestrador escreve. Abaixo de
  700 MB livres: `corte.json`, derruba o dono e o ensaio (menos ele mesmo), contêineres, volumes, redes, apaga a trava,
  sai 3. `-Resumo`: a tabela do pico por fase (`resumo.md`).
- `agents/code/test/ponta-a-ponta/25/pares.ps1`: a ponte para o `ensaio.psm1` do 07 e o MCP do 10. Passos `novo`,
  `subir` (só a instância de escrita do MCP do A; limite de memória), `reiniciar`, `recebeu`, `conflito`, `claro`,
  `descer`. O orquestrador lê `ensaio.json`, sem segredo; os objetos com segredo ficam no `ensaio.xml`, só da ponte.
- `agents/code/test/ponta-a-ponta/harnesses.mjs`: o comum das pontas a ponta (login, rodar, resposta, hashes,
  fragmentos). Os testes antigos seguem como estão.
- `agents/code/test/ponta-a-ponta/25-hub-inteiro.test.mjs`: o orquestrador (`comHarness`; `FASES`, `HARNESSES`).
  - Piso de 2.500 MB livres antes de cada fase (espera até 10 min).
  - Fase 1, busca: um hub de ensaio, o `serve` da busca; cada harness acha a nota pela `search`. A busca desce no fim.
  - Fase 2, pares: A e B cifrados, MCP de escrita do A, guarda do 14 nos três. Cada harness tenta regravar inteiro o
    `decisions.md` (a guarda recusa), segue por troca de trecho, e troca um trecho do `tasks.md`; o B recebe; nada em
    claro nos bancos crus.
  - Fase 3, banco reiniciado: o CouchDB do A reinicia, e uma gravação depois ainda chega ao B.
  - Fases 4 a 7 (vigia, retomada, arquivar, cliente): `todo`, com a peça que esperam (16/17, 18, 21, 22/24).
  - No fim: desce os pares, o resumo do medidor e o CSV vão para `evidencia-25/`, hashes dos arquivos de verdade.
- `agents/code/test/ponta-a-ponta/25/corredor.ps1`: destacado; sem trava e sem contêiner alheio, cria a trava,
  `wsl --shutdown`, roda a prova, apaga a trava no fim.

## Testes sem Docker

- `node --test agents/code/test/25-medidor.test.mjs`: 4/4 (amostra e fase; corte derruba dono e ensaio; para sem o
  dono; resumo).
- `node --test agents/code/test/25-pares-sem-docker.test.mjs`: 1/1 (o passo `novo` e o resumo sem segredo).
- A prova aparece pulada sem `HUB_HARNESS_REAL`; o detector do 29 segue verde.

## Primeira rodada real (2026-10-17, janela quieta, só a Brasa e eu)

- **Rodada 1, 09:53-09:57** (fases 1-3, Claude e Copilot): fase 1 (busca) e fase 3 (banco reiniciado) passam. Fase 2
  falhou no Copilot por defeito do teste: os harnesses rodam em fila no mesmo hub A, o Claude já tinha trocado a linha
  de `tasks.md`, e o pedido citava o texto original; o Copilot, com razão, não trocou (a guarda recusou a regravação e
  passou a troca em `decisions.md`, como devia). Conserto 627f1a8: o pedido cita a linha como está na hora.
- **Rodada 2, 09:58-10:01** (fases 2 e 3): passam (2 pass, 0 fail). Os passos com Docker da ponte (`subir`, `recebeu`,
  `claro`, `reiniciar`) funcionaram no primeiro uso, sem conserto. Nada em claro nos bancos crus.
- Evidência fc678b0 (`evidencia-25/`: resumo das duas rodadas, logs `prova-rodada-1.log` e `prova-rodada-2.log`,
  `medida.csv`). Sem contêiner `hub-ensaio-*` e sem pasta `hub-ensaio-25-*` no TEMP ao fim; sem token na evidência.
- Login (aval das regras): Claude `.credentials.json` e os dois campos do Copilot copiados e apagados em cada sessão
  (horas em `hashes-claude-copilot.json`). Hashes das pastas reais iguais antes e depois, menos `~/.claude.json`: esse
  arquivo é regravado pelo Claude Code de verdade das sessões abertas no canvas (o ensaio usa `CLAUDE_CONFIG_DIR`); a
  prova não grava nele.

| Fase | Livre mínimo (MB) | VM do WSL máx. (MB) | node máx. (MB) | Contêineres máx. (MB) | Duração |
|---|---|---|---|---|---|
| busca (rodada 1) | 1831 | 1929 | 1472 | — | 1:44 |
| pares:subir (r2) | 3281 | 2268 | 351 | a 140, b 101 | 0:22 |
| pares (r2) | 2813 | 2392 | 349 | a 182, b 145 | 2:15 |
| banco-reiniciado (r2) | 2676 | 2357 | 223 | a 179, b 137 | 0:12 |
| descer (r2) | 3222 | 2361 | 109 | b 136 | 0:04 |

Leitura: o pico é a busca (node 1,5 GB indexando; livre mínimo 1,8 GB). Os pares com dois CouchDB a 384 MB de limite
ficam abaixo de 200 MB cada. Com a máquina quieta, nada chegou perto do corte de 700 MB.

## Fases 4 a 7 escritas (851dcdc; mandato do maestro ~10h15: contra os ramos, só leitura deles, sem merge)

Puladas com o motivo até a peça entrar na árvore (`FASES` no topo do orquestrador). Ordem de execução: 1, 2, 3, 4, 6
(as que usam os pares), descida dos pares, 5, 7. Cada fase roda sozinha (`garantirPares`).

- **4 vigia (16, 17):** `pares conflito` (base comum que chega ao B, depois A e B mudam com a replicação suspensa, como o
  teste do 16); `pares vigia` (passada com o leitor da vigia e o notificador dublê): `divergencia` com o item pelo
  caminho em claro e uma notificação com o caminho; `pares estado-mcp` (sobe a instância de leitura e chama o
  `estado_do_hub` como um agente): conta o conflito; depois cada harness, com o início do 17, começa a resposta pelo aviso
  e cita a nota; no Codex, o notify chama o notificador uma vez.
- **6 arquivar (21):** por harness, uma pasta `operations/encerrada-<h>` chega ao B; o harness recebe "terminou, arquive
  pela skill" (shell liberado; `HUB_ARQUIVAR_AGORA` 20 min à frente, como o teste do 21); confere `_archive/<dia>--...`,
  `archived_at` (prova que foi pela skill) e o B recebeu. Depois `pares copia`: a cópia diária sai 0 e o ramo
  `par/ensaio-a` está no repositório nu.
- **5 retomada (18):** sem Docker (os pares descem antes; piso 1.500 MB). Por harness, um hub novo com os hooks de
  guardas, vigia e fim da resposta juntos (o que o 18 provou sozinho, aqui com as peças todas): devolve até a nota
  mudar, sete campos; a sessão 2, sem ferramentas, dá o próximo passo da nota.
- **7 cliente (22):** `25/cliente.ps1 subir` roda o `22-proxy.test.ps1 -Manter` (par, três instâncias, busca e proxy);
  o orquestrador roda o `ponta-a-ponta/22-cliente.test.mjs` com os mesmos harnesses; `cliente.ps1 descer` (proxy, busca
  pelo PID gravado pelo 22, instâncias, os dois pares pelo `Uninstall-ParBanco`, pasta). O valor aqui é medir a pilha
  toda junta, a combinação que caiu por memória no 22.
- Teste sem Docker: `25-pares-sem-docker` 2/2 (novo; manutencao com o CLI falso: o .env leva o do A, o outro par visto
  daqui, a máquina, o repositório nu; o leitor configurado; a segunda chamada não refaz). Orquestrador e detector do 29
  verdes. **Deslize de método:** o código da ponte veio antes do teste da manutencao.
- **Corte com várias pilhas (25be145, pedido do maestro):** cada fase que sobe algo grava `pilhas/<nome>.json` na pasta
  do medidor (prefixo dos contêineres e o comando de descer: `pares.ps1 -Acao descer`, `cliente.ps1 -Acao descer`) e o
  apaga ao descer. O medidor mede os contêineres de todos os prefixos registrados e, no corte, derruba o dono, roda o
  descer de cada pilha e tira contêineres, volumes e redes de cada prefixo; o `corte.json` diz o que desceu e com que
  código. Teste sem Docker com duas pilhas (25-medidor 5/5).
- **Riscos, para a rodada real:** os textos da notificação e do `estado_do_hub` foram lidos do
  teste do 16, não vistos; o pedido do arquivar depende de o agente ler a skill (com shell); a fase 7 repete o ponta a
  ponta do 22 por dentro.

## Rodada real das fases 4, 6 e 7 (2026-10-17 tarde; Claude e Copilot; `integracao` e7203b4 juntada em 87634db)

| Rodada | Hora | Piso | O que houve |
|---|---|---|---|
| 1 | 12:48-13:01 | 2.500 MB | a fase 4 esperou 10 min e não começou (máximo 2.040 MB livres; máquina com todos os agentes) |
| 2 | 13:12-13:13 | 1.800 MB | corte em 659 MB na subida dos pares (fase 4) |
| 3 | 13:21-13:39 | 1.800 MB | janela quieta do maestro (3,7 GB livres no começo): fase 4 falhou (abaixo), fase 6 **verde**, fase 7 cortada em 671 MB na subida da pilha do 22 (12 min subindo) |

Livre mínimo por fase na rodada 3 (`etapas/logs/25-medida-elzNVi.csv`): vigia 1.405 MB, pares 1.421, arquivar 1.315,
descida dos pares 1.942, subida do cliente 671 (corte). O maestro viu um serviço do Windows (SrTasks/TiWorker, ~1 GB)
comendo memória na hora.

- **Fase 6 (arquivar): verde** (vale, maestro). Claude e Copilot arquivaram pela skill; o B recebeu cada `index.md`
  com o mesmo hash; a cópia diária fez commit e empurrou para `par/ensaio-a`. Evidência b3fbac2
  (`evidencia-25/arquivar/`).
- **Fase 4 (vigia): defeito da ponte.** Conflito e passada certos (`divergencia` pelo caminho em claro), mas o
  `estado_do_hub` voltou vazio: a ponte apontava o fork na worktree principal `C:/Projetos/hub-mcp-banco`, que ficou no
  ramo `ticket-09`, sem o `estado_do_hub` do 10. Conserto fe0b800: o padrão é a worktree `integracao` do fork
  (`C:/Projetos/hub-mcp-banco-wt/integracao`, com 09, 10 e 11; `dist` em dia, sem recompilar a worktree do
  integrador); `HUB_MCP_BANCO_DIR` segue mandando. Teste sem Docker antes (25-pares-sem-docker: o fork do `.env` tem
  o `estado_do_hub`; vermelho no caminho antigo). A chamada do MCP sem conteúdo agora falha com a resposta inteira, em
  vez de devolver `[null]`. Rodar de novo, com o Docker.
- **Fase 7 (cliente): não coube.** Decisão do maestro: rodar sozinha numa janela própria (só ele e eu no canvas),
  depois do Codex de hoje; se cair no corte de novo, fica para a máquina do Gustavo.
- **Hashes:** o corte mata o node antes do `after`, e o arquivo de hashes não foi regravado. Conferido à mão contra os
  da manhã (`evidencia-25/hashes-claude-copilot.json`): as credenciais não mudaram; `.claude.json` (13:44, depois da
  rodada; as sessões reais do Claude Code o regravam) e `.codex/config.toml` (10:21, antes) mudaram fora da rodada. O
  TAP também perde os subtestes quando o node morre: o resultado por fase sai da evidência e do `corte.json`.
- Pastas do TEMP das três rodadas apagadas à mão (o corte não deixa o `after` rodar); nenhuma tinha login.

## Janela quieta da noite (2026-10-17 17:22-18:23; `integracao` 9f122c2 juntada em a274ea5, com 16, 17, 18, 21, 22, 43)

| Fase | Claude e Copilot | Codex (gpt-6-luna) |
|---|---|---|
| 1 busca | verde (manhã) | **verde** (18:00; c0d2b97) |
| 2 pares | verde (manhã) | **verde** (19:26; 4a60595; antes, 18:09, o A não desceu ao B) |
| 3 banco reiniciado | verde (manhã) | não conta (a fase 3 não abre harness) |
| 4 vigia | **verde** (19:26; 4a60595; antes, 14:06 e 17:22, o A não desceu ao B) | não rodada |
| 5 retomada | **verde** (17:22; 9c5a795) | não rodada |
| 6 arquivar | **verde** (13:21; b3fbac2) | não rodada |
| 7 cliente | **verde** (19:21; b78c49d; o 22-cliente rodou: `# pass 2`, `# skipped 0`; livre mínimo 835 MB). A das 18:15 (cee35c1) não tinha rodado harness | não rodada |

- **Fase 7:** caiu duas vezes por defeito da ponte do cliente, ambos consertados com teste sem Docker antes
  (`25-cliente-sem-docker.test.mjs`): (1) 0aa088b: o `subir` capturava a saída do teste do 22, e os serviços que o
  `-Manter` deixa de pé herdavam o pipe; ficou 28 min parado (parei só aquele PID; a prova desceu tudo). Agora o pwsh
  abre sem `-Redirect*` (com eles, o `Start-Process` herda todos os handles) e grava a saída em arquivo. (2) f5b790b: o
  log ficava dentro da pasta do 22, e o `New-EnsaioBanco` recusa a pasta que já existe. Deslize no caminho: o primeiro
  vermelho do teste rodou o 22 de verdade (a variável do dublê ainda não existia); parei a árvore pelo PID antes do
  Docker e apaguei a pasta.
- **Fase 2 do Codex, pedido:** "sem shell" impedia o Codex de ler o `decisions.md` (ele só lê pelo shell): o Luna mandou
  um patch vazio e o Sol (`gpt-6.1-sol`, tentado pela regra "só se o teste for difícil para o Luna") recusou o passo 1.
  O defeito era do pedido, não do modelo: 8f6f50a deixa o Codex ler pelo shell e gravar só pelo `apply_patch`. Com
  ele, o Luna fez certo (guarda recusou a regravação; trecho trocado), mas o B não recebeu: o mesmo sintoma da fase 4.
- **O A que não desce ao B** (fases 2 e 4): intermitente. Certo de manhã, às 13:21 e às 18:00 (fase 3, 1-2 min depois
  de a 2 subir os pares); falhou às 14:06 (Docker recém-ligado), 17:22 e 18:09 (primeira gravação de uma subida
  nova). Diagnóstico gravado na falha do conflito: 3c1221a, quebrado na 1ª vez (`(try ...)` como valor), consertado em
  5273511 e conferido com dublês. Os logs do CLI somem com a pasta no `descer`. A Brasa (fez o 08, a replicação)
  investiga e reproduz com Docker; a fase 4 e a 2 do Codex esperam esse diagnóstico.
- **Hashes:** credenciais reais sem mudança em todas as rodadas. O `.claude.json` muda pelas sessões reais. Um deslize
  meu: restaurei do git o `hashes-claude-copilot.json` das 17:22 antes de lê-lo; conferido à mão contra o da manhã
  (mudanças todas fora da janela da rodada). Cópias de cada rodada em `etapas/logs/25-*`.

## Revisão parcial (maestro, 2026-10-17 ~18h35)

- Pedida ao Fiel no que está pronto: fases 1-3, 5, 6 e 7 com Claude e Copilot; Codex 1 e 3. A fase 4 e a 2 do Codex
  entram depois, numa rodada curta, com o conserto da descida A→B (Brasa).
- Antes: `integracao` f640bbd (23, 37, 44, docs) juntada em **5489b3a**, sem conflito. Testes leves
  (`harness-real`, `25-*`, `ponta-a-ponta/25-hub-inteiro`, `27-pastas`): 41 pass, 0 fail, 1 skip (o real).

## Rodada 1 parcial do Fiel: VOLTA, e os consertos (2026-10-17 19h)

Parecer: `etapas/parecer-25-Vela.md`. Provado: fases 1, 2, 3, 5 e 6 com Claude e Copilot; fase 1 do Codex.

- **A descida A→B** (fases 4 e 2 do Codex), causa achada pela Brasa (`etapas/diagnostico-25-nota-nao-desce.md`,
  "Resultado da reprodução"): não é replicação morta. Logo depois da subida, o daemon do B leva ao disco a semente
  inteira (523 arquivos, 7 MB) a ~1 arquivo/s, ~6,5 min; a nota nova entra na mesma fila. **fc6b10c:** o `pares.ps1
  subir` só devolve com o B convergido (`25/convergiu.mjs`: cada arquivo que replica do A, pela regra do gerador, com o
  mesmo hash; até 15 min; o tempo vai em `evidencia-25/subida-dos-pares/pares/subir.json`); a fase 2 espera 120 s; o
  `recebeu` que falha guarda o fim dos logs do CLI (somem no `descer`). Teste sem Docker: o passo `convergiu` sobre o
  `novo` (B vazio, depois a cópia do que replica, depois um hash diferente). O `--interval` ficou fora.
- **Conserto 1, fase 7 sem harness. dac76e6:** `25/prova-do-cliente.mjs` roda o 22-cliente sem o `NODE_TEST_CONTEXT`
  e só passa com saída 0, um `# pass` por harness e `# skipped 0`. Teste com um dublê do 22 aberto de dentro de um
  `node --test` (vermelho antes: `# pass NaN`). O `evidencia-22` que o 22-cliente regrava não entra no ramo (volta por
  `git checkout` depois da rodada; o arquivo do 22 não mudou).
- **Conserto 2, evidência sobrescrita. f6a0f21:** cada rodada grava medida, resumo, corte e hashes em
  `evidencia-25/rodadas/<data-hora>-<harnesses>-f<fases>/`, e apaga só a pasta dos harnesses dela. Repostas:
  `rodadas/2026-10-17-1248-claude-copilot-f1-2-3/` (a manhã, das cópias em `etapas/logs/25-*-fases-1-3*`) e
  `rodadas/2026-10-17-1800-codex-f1-2-3/hashes.json` (Codex Luna, `logs/25-codex-luna/`). Tirados da raiz os da
  rodada das 18:15 (cópia em `logs/25-noite-f7-*`).
- **Ressalvas feitas junto:** o modelo do Codex vai nos `usos` (`MODELO_CODEX`); a pilha registrada é gravada ao lado
  e trocada (o medidor não lê JSON pela metade). Ficam como ressalva: a fase 2 confere no B só o `tasks.md`; o
  `cliente.ps1` não apaga o log dele no `%TEMP%`; o 25-medidor intermitente (1 em 4 no laço do Fiel).

## Rodadas da 2ª volta (2026-10-17 19:21-19:33; trava da Vela)

- **19:21, fase 7, Claude e Copilot** (corredor 109808, com `wsl --shutdown`): verde em 4,4 min. O 22-cliente rodou de
  verdade (`evidencia-25/cliente/harnesses/prova.tap`: `# pass 2`, `# skipped 0`). Livre mínimo 835 MB (na fase
  `cliente`; `rodadas/2026-10-17-1921-claude-copilot-f7/resumo.md`). Hashes do 22 (`hashes-do-22-cliente.json` na
  mesma pasta): credenciais iguais, logins apagados. O `evidencia-22` regravado pelo 22 voltou por `git checkout`
  (cópia em `etapas/logs/25-noite-f7-c-evidencia-22/`). Evidência b78c49d.
- **19:26, fases 2 (Codex) e 4 (Claude e Copilot) numa subida só** (corredor 133496, `-SemWsl`,
  `HARNESSES_F2=codex`, `HARNESSES_F4=claude,copilot`; 8cc9da2): as duas verdes em 6 min. O B convergiu em **218 s**
  (530 arquivos; `subida-dos-pares/pares/subir.json`); depois disso a fase 2 do Codex (`gpt-6-luna`) recebeu o
  `tasks.md` com o mesmo hash, e a fase 4 abriu o conflito e a vigia acusou. Livre mínimo 1.690 MB. Hashes: só o
  `.claude.json` mudou (sessões reais; a conferência da prova passou). Evidência 4a60595.
- Depois: `integracao` 56cd23a (24 e evidência do 22) juntada em 4628138.

## O que falta

- Todas as fases verdes com Claude e Copilot (1-3 de manhã, 5, 6, e 4 e 7 às 19h). Codex: fases 1 e 2 verdes.
- **Codex nas fases 4 a 7: fora do 25** (decisão do maestro, 2026-10-17 ~19h45, mandato; vai ao "Para rever"). O Codex
  nessas peças está provado nos tickets de cada uma (17 vigia nas telas, 18 retomada, 21 arquivar e cópia, 22 cliente).
- **Pela ressalva do 11, ainda fora:** o `write_note` pelos harnesses e o MCP reconectando sozinho depois do reinício.
  Hoje a fase 2 grava pelo disco e a 3 confere o sincronizador.
- **Para o kit (observação da Brasa, não defeito):** um par novo leva minutos para receber o hub inteiro (~1 arquivo/s
  no daemon; 218 s a ~6,5 min nesta máquina). A instalação do segundo par deveria dizer isso ou esperar a convergência
  antes de dar o par por pronto. O maestro levou ao ticket 26 (instalação).

## Fica para a instalação de verdade e para a segunda máquina

- Fases 1-3 couberam com a máquina quieta (só dois construtores no canvas): livre mínimo 1.831 MB, na busca. Com todos
  os agentes abertos não foi medido; a busca (indexação, ~1,5 GB de node) é a fase mais pesada, e a ordem por fases
  (indexar e descer a busca antes de subir os pares) fica como regra para a máquina do Gustavo.
- **Fase 7 (cliente, a pilha do 22 inteira):** livre mínimo **835 MB**, só 135 MB acima do corte de 700 MB
  (`rodadas/2026-10-17-1921-claude-copilot-f7/resumo.md`; com `wsl --shutdown` antes e a máquina quieta). É a fase mais
  apertada: na máquina do Gustavo, com outros programas abertos, pode não caber; fica para a instalação conferir.
- **Fase 4 (vigia, com os pares):** livre mínimo **1.690 MB** (`rodadas/2026-10-17-1926-claude-codex-copilot-f2-4/resumo.md`,
  junto com a fase 2; o mínimo veio no `pares:descer`).
