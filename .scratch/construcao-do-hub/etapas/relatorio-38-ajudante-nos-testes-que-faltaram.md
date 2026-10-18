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

- Leves (`logs/trilho-38-leves.log`): 36-pasta-de-ensaio, 38-ensaio-banco, 07-kit-sem-docker, 09-mcp-banco-sem-docker, 28-pastas-locais-sem-docker e o gerador do 06 (usam o ensaio.psm1): 23/23.
- Falha forçada dos sem Docker: cópias dos dois testes com `timeout: 2500` (o pwsh morre no meio). Falharam, e nenhuma
  pasta `hub-ensaio-07-sem-docker-*`/`hub-ensaio-09sd-*` sobrou.
- `16-vigia` 19/19 (`logs/trilho-38-16-vigia.log`). Falha forçada: cópia com o prefixo `hub-ensaio-16f-` e um teste a
  mais que monta um par (daemon falso vivo) e falha: nenhuma pasta sobrou.
- Pesados (com a trava, 11:40 a 11:55): `12-busca`, `12-kit-busca`, `13-gemini` 17/17 (`logs/trilho-38-busca.log`); nenhuma
  pasta nova deles em `%TEMP%` (só as antigas, de 00:01 a 04:14 de 17/10).
- Falha forçada dos pesados (`logs/trilho-38-forcada.log`): cópias com prefixo próprio (`12f`, `12kf`, `13f`, `12pf`,
  `15pf`) e um teste a mais que falha; no 12-kit com o `iniciar.ps1` vivo, no 13 com a busca de pé. Nos ponta a ponta,
  `HUB_HARNESS_REAL=1 HARNESSES=nada`: a busca sobe e o teste cai em `preparar[harness] is not a function`, antes de
  copiar login (`copiado: null`). Os cinco falharam, e nenhuma pasta sobrou. Os `hashes-nada.json` gravados pelo `after`
  foram apagados.

## Fora, e por quê

- **Docker do 08, 09 e 10 não rodou** (maestro, 2026-10-17 ~11h35): só mudou a limpeza, coberta pelo teste novo sem
  Docker; o próximo Docker deles, nas fases do 25, exercita a limpeza.
- **Codex nos testes com harness de verdade** (pedido do maestro, regra nova do Gustavo, 2026-10-17): constante comum
  `MODELO_CODEX = 'gpt-6.1-sol'` em `agents/code/test/harness-real.mjs`, usada nos ponta a ponta 12, 14, 15, 19, 20 e
  27 e na prova 03 (antes `gpt-6-luna`). f61906d. O 22-cliente segue no `gpt-6-astra` (da Brasa, não pedido aqui); o
  17 e o 18 ficam com a Vela. Não rodado com o Codex no 38; sem a variável, os oito aparecem pulados (8/8).
- **17**: juntado durante o 38 (merge 7c87301) já com o `pastaDeEnsaio` (da Vela); nada a trocar. Os dublês dele não seguram pasta.

## Armadilhas

- No PowerShell, `$raiz` e `$Raiz` são a mesma variável: o parâmetro novo dos sem Docker chama `-Pasta`.
- O `09-mcp-banco-sem-docker` confere a recusa pela última linha da saída do passo; com um caminho de ensaio mais
  comprido, a mensagem quebra de linha e o caso falha. A pasta dele usa o prefixo curto `hub-ensaio-09sd-`, sem
  subpasta.
- Em `%TEMP%` há pastas de outros (o Rebite roda a suíte ao mesmo tempo): conferir sobra só pelos prefixos do teste.

## Rodada 2 (parecer r1 do Fiel e do Fielzinho), b854a7e

- `Invoke-Limpeza` em `banco/ensaio.psm1`: cada passo do `finally` roda por conta própria, na ordem; um que lança não
  pula os seguintes; a primeira queda volta no fim.
- 09 e 10: cada instância do MCP para num passo seu (`{ Stop-McpBanco $i }.GetNewClosure()`), e o
  `Remove-EnsaioBanco` vem depois, num passo próprio.
- 08: guardar os registros (com o `New-Item`), descer os pares e apagar a raiz, cada um num passo.
- Testes novos no `38-ensaio-banco` (7/7): o `finally` de verdade do 08, do 09 e do 10, tirado pelo parser do
  PowerShell e rodado com dublês (o `Stop-McpBanco` da primeira instância lança; no 08, o `New-Item` lança). Contraprova:
  com o `finally` antigo do 09 e do 10, os dois casos ficam vermelhos. Mais o `Invoke-Limpeza` sozinho e no formato
  do 09 rodado com `-File`.
- Achado do Lume (pedido do maestro): o comentário do topo de `hub-de-ensaio/conteudo.mjs` dizia que kind, size,
  cadence e stage → status não estavam decididos; agora aponta o esquema do 05 (`agents/frontmatter/initiative.yml`).
- Leves 60/60 (`logs/trilho-38-r2-leves.log`): 36, 38, 07 e 09 sem Docker, 28 sem Docker, gerador do 06, 04, 05-frontmatter.
- Armadilha: a closure do `GetNewClosure()` só enxerga funções globais; as do módulo importado pelo teste são globais
  (Import-Module de script), as definidas no próprio script não. Nos testes, os dublês são `function global:`.
