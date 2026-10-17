# Relatório do ticket 38: o ajudante da pasta de ensaio nos testes que ficaram de fora do 36

Trilho, 2026-10-17. Ramo `ticket-38`, worktree `C:/context-hub-wt/ticket-38`, de `integracao` 4a47576.

## O que se fez

- **Ajudante** (`agents/code/test/pasta-de-ensaio.mjs`): `antesDeApagar(gancho)`. Os ganchos rodam na ordem em que
  vieram, antes das pastas saírem (no `after`, no `exit` e na queda no carregamento). Servem para parar a busca e os
  dublês, que seguram a pasta no Windows. Um gancho que lança não segura os outros nem as pastas, e a falha diz qual.
  Dois casos novos no `36-pasta-de-ensaio.test.mjs` (pasta presa por processo vivo, liberada pelo gancho num teste que
  falha; gancho que lança). 09b11d8.
- **12-busca, 12-kit-busca, 13-gemini**: `hubDeEnsaio` no lugar do `mkdtemp` + `montar.mjs`; a busca e os dublês param
  no `antesDeApagar`. O `after` do 12-busca ficou só com as medidas. c2eb375.
- **Ponta a ponta 12 e 15**: `pastaDeEnsaio` (com o caminho longo, como antes) e a busca no `antesDeApagar`. A pasta
  guarda as casas com o login copiado: agora sai também se o arquivo cair ou o processo sair no meio. c2eb375.
- **16-vigia** (juntado durante o 38; merge de `integracao` 5a91034): `hubDeEnsaio`/`pastaDeEnsaio`; os dublês
  fecham e o daemon falso sai (`taskkill`) no `antesDeApagar`. e316032.
- **Banco (08, 09, 10)**, c0bcc5e:
  - `New-EnsaioBanco` apaga a raiz e relança quando cai depois de criá-la (o teste ainda não tem o `$ensaio` para o
    `finally`).
  - `Remove-EnsaioBanco` derruba cada par por conta própria e apaga a raiz mesmo quando um falha; relança a primeira
    queda.
  - 09 e 10: o `try` começa logo depois do `New-EnsaioBanco` (a preparação do `.env` e do MCP estava fora dele).
  - 08: no `finally`, a cópia dos registros não segura a limpeza (`-ErrorAction Continue`), e a raiz sai num `finally`
    próprio, mesmo se o `-Descer` lançar.
  - Os `.ps1` sem Docker (`banco/kit-sem-docker.ps1`, `banco/mcp-banco-sem-docker.ps1`) recebem `-Pasta` do teste em
    node, criada por `pastaDeEnsaio`: se o pwsh morrer no meio, o node apaga.
  - Teste novo `38-ensaio-banco.test.mjs`, sem Docker: troca uma função do kit por outra que lança e confere que a raiz
    sai.

## Testes

- `36-pasta-de-ensaio` 10/10; `38-ensaio-banco` 2/2; `07-kit-sem-docker` e `09-mcp-banco-sem-docker` verdes.
- Falha forçada dos sem Docker: cópias dos dois testes com `timeout: 2500` (o pwsh morre no meio). Falharam, e nenhuma
  pasta `hub-ensaio-07-sem-docker-*`/`hub-ensaio-09sd-*` sobrou.
- `16-vigia` 19/19 (`logs/trilho-38-16-vigia.log`). Falha forçada: cópia com o prefixo `hub-ensaio-16f-` e um teste a
  mais que monta um par (daemon falso vivo) e falha: nenhuma pasta sobrou.
- Pesados (com a trava): PREENCHER.

## Fora, e por quê

- **Docker do 08, 09 e 10 não rodou** (maestro, 2026-10-17 ~11h35): só mudou a limpeza, coberta pelo teste novo sem
  Docker; o próximo Docker deles, nas fases do 25, exercita a limpeza.
- **Codex nos testes com harness de verdade** (pedido do maestro, regra nova do Gustavo, 2026-10-17): constante comum
  `MODELO_CODEX = 'gpt-6.1-sol'` em `agents/code/test/harness-real.mjs`, usada nos ponta a ponta 12, 14, 15, 19, 20 e
  27 e na prova 03 (antes `gpt-6-luna`). f61906d. O 22-cliente segue no `gpt-6-astra` (da Brasa, não pedido aqui); o
  17 e o 18 ficam com a Vela. Não rodado com o Codex no 38; sem a variável, os oito aparecem pulados (8/8).
- **17**: ainda não juntado; a troca fica para depois da junção dele (comentário no ticket).

## Armadilhas

- No PowerShell, `$raiz` e `$Raiz` são a mesma variável: o parâmetro novo dos sem Docker chama `-Pasta`.
- O `09-mcp-banco-sem-docker` confere a recusa pela última linha da saída do passo; com um caminho de ensaio mais
  comprido, a mensagem quebra de linha e o caso falha. A pasta dele usa o prefixo curto `hub-ensaio-09sd-`, sem
  subpasta.
- Em `%TEMP%` há pastas de outros (o Rebite roda a suíte ao mesmo tempo): conferir sobra só pelos prefixos do teste.
