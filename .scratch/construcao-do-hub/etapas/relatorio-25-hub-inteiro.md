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

## O que falta

- **Primeira rodada real** (fases 1 a 3, Claude e Copilot; Codex depois das 12h15), pela fila e com o corredor.
  Primeiro uso dos passos com Docker da ponte (`subir`, `recebeu`, `claro`, `reiniciar`): podem pedir conserto.
- **Pela ressalva do 11, ainda fora:** o `write_note` pelos harnesses (o registro do `hub-banco` nos três chega com o 11
  e o 23) e o MCP reconectando sozinho depois do reinício. Hoje a fase 2 grava pelo disco e a 3 confere o sincronizador.
- **As fases 4 a 7**, quando as peças entrarem. O roteiro de cada uma está nas costuras.
- **Junção:** o 25 depende de 13, 21, 22 e 24.

## Fica para a instalação de verdade e para a segunda máquina

(A preencher com a rodada real: o que não coube na memória, por fase, com os números do medidor.)
