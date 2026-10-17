# Costuras do ticket 25 (junção e prova do hub de ensaio inteiro), propostas pela Vela

2026-10-17 ~08h50. É um preparo, por mandato do maestro (08:33): costuras e roteiro da prova de ponta a ponta sobre o
que já está em `integracao`, estendido quando as outras peças entrarem. Nada pesado sem a fila. Nada de código antes
do aceite.

Fontes lidas: ticket 25 e os comentários; o antigo 11 (`issues-tentativa-paralela/11-...`); as ressalvas do 11
(`relatorio-11-...`, "Ressalvas para o 25"); as quedas por memória (`relatorio-08-banco-limites.md`, `retomada-Brasa.md`,
`fila-pesada.md`); as costuras do kit (`costuras-23-Cinzel.md`); o que existe em `integracao` e98a891.

## O que a prova tem de mostrar

O percurso do ticket: **um agente grava, o outro par recebe, a busca acha, a vigia acusa, a retomada segura.** Mais o
que o 11 deixou para cá:

- a **regra seguida**: o agente pede uma regravação inteira, a guarda recusa, e ele grava por troca de trecho ou pelo
  `write_note` com a versão lida;
- o **banco cifrado de ponta a ponta pelos harnesses** (o 11 usou o fork em modo local);
- o **banco reiniciado no meio da sessão**: o MCP volta a responder sozinho.

E o que o antigo 11 pedia: os três harnesses, em modo não interativo, fazem o percurso; o kit roda duas vezes sem
mudar nada na segunda e desfaz sem sobra (isso fica com o 23 e o 24; o 25 só usa o kit).

## O que já está em `integracao` e o que entra depois

- **Já está (e98a891):** esqueleto e hub de ensaio (04), frontmatter e nova iniciativa (05), exclusões (06), banco do
  par (07), limites (08), MCP do banco com versão e as três instâncias (09, 10), busca (12), Gemini desligado (13),
  guardas e aviso de leitura (14, 15), roteamento (19, 34), acervo (20, 31, 35), pastas e fim da resposta (27),
  pastas locais (28), links (32, 33), pasta de ensaio (36).
- **Entra depois:** vigia (16), telas (17), retomada (18), arquivar e cópia (21), proxy e kit de cliente (22), kit (23),
  kit ao vivo (24).
- **Como a prova cresce:** cada fase abaixo diz de que ticket depende. A fase que depende de peça ainda fora fica
  pulada, com o motivo na saída ("espera o 16"). Quando a peça entra, a fase liga sozinha: o teste confere se o
  arquivo da peça existe na árvore. Até o 23 entrar, a prova junta os fragmentos à mão, como os ponta a ponta de 14
  a 20; com o 23, chama o kit no HOME de ensaio.

## O risco: memória

Números de hoje (máquina com 16 GB; o WSL limitado a 4 GB pelo `.wslconfig`, com `autoMemoryReclaim=gradual`):

- **Antes de tudo:** 2,7 GB livres às 08h45, com os terminais do Claude Code abertos (os sete maiores somam ~2,8 GB) e o
  antivírus (~1,4 GB).
- **08, 05h11:** de 2.900 para 513 MB livres em 1 minuto, com um arquivo de 60 MiB indo aos dois bancos.
- **08, 07h37:** de 3.183 para 621 MB livres em 2 minutos, ainda na subida dos pares. Depois, a `vmmemWSL` segurou
  2,1 GB até o `wsl --shutdown`.
- **22, 08h26:** cortado com 613 MB livres na indexação da busca, com os dois pares e as três instâncias do MCP de pé.

Leitura: o que mais pesa é a VM do WSL subindo com o Docker e o que roda nela (dois CouchDB), somada ao modelo de
embeddings da busca (`serve` com o arctic-embed carregado; ele indexa e responde no mesmo processo). Os dois juntos não
cabem com os agentes abertos.

## Proposta: a prova por fases, cada uma só com o que precisa

Antes da primeira fase: trava, `docker ps` vazio dos `hub-ensaio-*`, `wsl --shutdown` (o maestro já disse "antes"),
piso de 2,5 GB livres (espera até 10 min; sem chegar, para e avisa). Um hub de ensaio novo (`montar.mjs`), um HOME de
ensaio por harness.

| Fase | Sobe | Prova | Desce no fim | Depende de |
|---|---|---|---|---|
| 1. Busca | `serve` da busca sobre o hub A (indexa) | os três harnesses, um por vez, acham uma nota pela `search` e abrem só o trecho; leitura fora da busca ganha o aviso (15) | o `serve` | 12, 15 |
| 2. Pares | `wsl --shutdown` de novo; CouchDB A e B (cifrados), CLI A e B, só a instância de **escrita** do MCP do par A | cada harness, um por vez: troca de trecho numa nota (disco) e um `write_note` com versão; pede uma regravação inteira e é recusado (regra seguida); B recebe as duas mudanças (arquivo e hash no B); nos bancos crus, nada em claro (`Get-AmostraHub`) | nada ainda | 07, 09, 10, 14 |
| 3. Banco reiniciado | (os mesmos) | numa sessão retomada (`--resume` / `exec resume`): turno 1 grava; o teste reinicia o CouchDB A; turno 2 grava de novo pelo MCP, sem religar nada | nada ainda | 10 |
| 4. Vigia | (os mesmos) | conflito forçado (a mesma nota mudada em A e B com a replicação suspensa); `vigia passada` grava divergência; a sessão nova começa pelo aviso; o `estado_do_hub` conta o mesmo | MCP, CLI, CouchDB, `wsl --shutdown` | 16, 17 |
| 5. Retomada | nada de Docker | a sessão que gravou numa iniciativa é devolvida até a nota mudar; a seguinte começa por ela | — | 18, 27 |
| 6. Arquivar e cópia | CouchDB A sozinho, se a cópia pedir | arquivar uma iniciativa; a cópia diária roda uma vez | tudo | 21 |
| 7. Cliente | proxy + o que ele expõe | um harness como cliente pelo proxy acha e lê | tudo | 22, 24 |

Regras de cada fase:

- **Um harness por vez**, modelo barato, uma sessão por harness e fase, login pelo aval (cópia em
  `%TEMP%\hub-ensaio-25-*`, hash antes e depois, apagar no fim).
- **Descer o que a fase seguinte não usa** antes de ela começar. Entre a 2–4 e a 5, `wsl --shutdown`.
- **Fase independente:** `-Fases 1`, `-Fases 2,3` etc. Uma fase cortada roda de novo sozinha, sem repetir as outras.
  As fases 2 a 4 sobem os pares juntas; a 5 não precisa de Docker (o fim da resposta e o início são locais).
- **Evidência** por fase em `agents/code/test/ponta-a-ponta/evidencia-25/<fase>/<harness>/`, sem token nem pasta do
  usuário.

## O medidor de memória

- Um processo à parte, destacado (`Start-Process`), que amostra a cada 2 s: memória livre, a `vmmemWSL`, a soma dos
  `node` do ensaio (pelo caminho do ensaio na linha de comando), e `docker stats --no-stream` dos `hub-ensaio-25-*` a
  cada 10 s.
- Grava um CSV com a fase corrente (o orquestrador escreve a fase num arquivo; o medidor a lê).
- **Corte:** abaixo de 700 MB livres, grava o motivo, desce o ensaio inteiro (PIDs do ensaio, contêineres, volumes e
  redes `hub-ensaio-25-*`, a pasta) e apaga a trava, como o corredor do 08. Avisa o primeiro da fila.
- No fim, uma tabela por fase: mínimo livre, máximo da `vmmemWSL`, máximo dos `node`, máximo por contêiner, duração.
  É o "pico" que o maestro pediu, e vai no relatório.
- Se uma fase não couber, o relatório diz qual, com os números, e ela vira item para a máquina do Gustavo com menos
  agentes abertos.

## Forma do código

- `agents/code/test/ponta-a-ponta/25-hub-inteiro.test.mjs`: o orquestrador, com `comHarness` (pulado sem
  `HUB_HARNESS_REAL=1`) e `-Fases` por `FASES=1,2`. Usa o ajudante comum de pasta de ensaio e o `preparar` / `rodar`
  dos ponta a ponta de 17 a 20 (tiro os comuns para um módulo, `ponta-a-ponta/harnesses.mjs`, sem mudar os testes
  antigos).
- `agents/code/test/ponta-a-ponta/25/pares.ps1`: a ponte para o `ensaio.psm1` do 07 (`-Subir`, `-Descer`,
  `-ReiniciarA`, `-Conflito`, `-Amostra`), com o estado do ensaio num JSON que o orquestrador lê.
- `agents/code/test/ponta-a-ponta/25/medidor.ps1`: o medidor acima.
- Um corredor destacado (`Start-Process pwsh ...`) lança o orquestrador e o medidor, para uma queda de memória não levar
  o meu terminal junto (a primeira rodada do 08 foi parada pelo Claude Code).
- Teste sem harness e sem Docker do que dá: a ponte com o `cli-falso.cjs` (como o `kit-sem-docker.ps1`), o medidor com
  limites falsos (corte dispara e desce os PIDs dele), a tabela do pico.

## Perguntas ao maestro

1. **`wsl --shutdown` dentro da prova**: no começo e entre as fases (2–4 → 5), sempre com a trava e `docker ps` vazio
   de quem não é do 25. Aval para o corredor fazer isso sozinho?
2. **Limite de memória nos contêineres de ensaio**: um `compose.override.yml` só do ensaio, com `mem_limit` de 384 MB
   por CouchDB. Não muda o kit nem nada global. Aceita? (O `.wslconfig` é do Gustavo; não mexo.)
3. **Busca em fase separada**: a fase 1 prova a busca sem os pares, e as fases 2 a 4 rodam os harnesses sem a
   `hub-busca` na configuração. O percurso fica provado em pedaços, não numa sessão só. Aceita, ou quer uma sessão
   única com tudo junto (que hoje não cabe)?
4. **Ordem do preparo**: agora, só o que não pesa (ponte, medidor, módulo comum, testes sem Docker). A primeira rodada
   real das fases 1 e 2 pela fila, quando o maestro disser.
