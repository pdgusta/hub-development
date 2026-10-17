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

## O que falta

- **Codex** nas fases 1-3 (depois das 12h15), pela fila.
- **Rodada real das fases 4 a 7** quando 16+17, 18, 21 e 22 entrarem em `integracao` (então `git merge integracao` no
  ramo ticket-25).
- **Pela ressalva do 11, ainda fora:** o `write_note` pelos harnesses (o registro do `hub-banco` nos três chega com o 11
  e o 23) e o MCP reconectando sozinho depois do reinício. Hoje a fase 2 grava pelo disco e a 3 confere o sincronizador.
- **As fases 4 a 7**, quando as peças entrarem. O roteiro de cada uma está nas costuras.
- **Junção:** o 25 depende de 13, 21, 22 e 24.

## Fica para a instalação de verdade e para a segunda máquina

- Fases 1-3 couberam com a máquina quieta (só dois construtores no canvas): livre mínimo 1.831 MB, na busca. Com todos
  os agentes abertos não foi medido; a busca (indexação, ~1,5 GB de node) é a fase mais pesada, e a ordem por fases
  (indexar e descer a busca antes de subir os pares) fica como regra para a máquina do Gustavo. (Fases 4-7 a medir quando entrarem.)
