# Parecer do ticket 38 (Trilho): o ajudante da pasta de ensaio nos testes que faltaram

## Rodada 1 — 2026-10-17 ~12h05 (leitura do Fiel; Fielzinho repassado, cota volta às 12h15)

Ramo `ticket-38`, HEAD f61906d, depois 7c87301 (só o merge do 17); contém a `integracao`.
**Veredito: VOLTA** em acordo Fiel/Fielzinho (1 conserto, do Fielzinho; a leitura do Fiel não o tinha pego).

### Consertos
1. **No 09 e no 10, uma queda ao parar o MCP pula a limpeza** (Fielzinho; aceito pelo Fiel). `09-mcp-banco.test.ps1:166-169`
   e `10-mcp-banco.test.ps1:215-218`: o `finally` chama `Stop-McpBanco` em laço, sem proteção, antes do
   `Remove-EnsaioBanco`; com `$ErrorActionPreference = 'Stop'`, um `Stop-McpBanco` que lança sai do `finally` e os
   contêineres e a raiz ficam. Reprodução do Fielzinho sem Docker, com o `finally` real extraído e dublês:
   `logs/repro-38-fielzinho.log` (09 e 10: `Remove-EnsaioBanco chamado=False`). Conferido no código pelo Fiel.
   Conserto: parar cada instância por conta própria (`try/catch` guardando a queda) e o `Remove-EnsaioBanco` num
   `finally` próprio, relançando a queda depois; no 08, pôr também a preparação dos registros (`New-Item $registros`)
   fora do caminho da limpeza. Com um caso de teste sem Docker como o do 38-ensaio-banco.

### Conferido
- `antesDeApagar`: ganchos em ordem, antes das pastas, no `after`, no `exit` e na queda no carregamento; gancho que
  lança não segura os outros (2 casos novos no 36). Os ganchos usados são síncronos (`parar` = `taskkill`; no 16,
  `close` e `taskkill`), como o `exit` exige.
- 12-busca, 12-kit-busca, 13-gemini, ponta a ponta 12 e 15, 16-vigia pelo ajudante; o ponta a ponta mantém o caminho
  longo (`realpathSync.native` sobre a pasta do ajudante) e as casas com login seguem saindo por rodada
  (`apagarEnsaio(casa)`).
- `ensaio.psm1`: `New-EnsaioBanco` apaga a raiz quando cai; `Remove-EnsaioBanco` desce cada par e apaga a raiz mesmo
  com queda (teste novo 38-ensaio-banco). 08, 09, 10 com o `try` cedo e a raiz num `finally` próprio.
- `MODELO_CODEX = 'gpt-6.1-sol'` comum nos ponta a ponta e na prova 03 (pedido do maestro 11:41).

### Evidências
- Fiel: 36, 38, 07-kit-sem-docker, 09-mcp-banco-sem-docker, 16-vigia e o detector do 29: 39/39; nenhuma
  `hub-ensaio-*` nova desta rodada em `%TEMP%` (uma `hub-ensaio-09-sem-docker-<PID>` passou e sumiu: o caminho antigo,
  sem `-Pasta`, de outra rodada em `integracao`). `git status` limpo.
- Pesados (12, 13) e falhas forçadas: logs do Trilho (`logs/trilho-38-busca.log`, `logs/trilho-38-forcada.log`); não
  repeti (indexação pesada).

### Ressalvas
- O `rmSync` do ajudante tenta 10 vezes (≈5 s); o `apagarEnsaio` antigo dos ponta a ponta esperava até 10 s em
  EPERM/EBUSY. Com um harness lento para soltar a pasta, a falha agora diz "pasta de ensaio não saiu" no fim.
- Docker de 08, 09, 10 não rodou (aceito pelo maestro; as fases do 25 exercitam).
- Ponta 7c87301 (~12h10): só o merge da `integracao` com o 17 (e7203b4), sem conflito; nenhum arquivo do 38 mudou; o
  17 não usa `mkdtemp`. Fiel: 17, 36, 38 e o detector nessa ponta, 37/37; `git status` limpo. Leitura do Fielzinho sobre 7c87301.

### Acordo
- Fielzinho (`parecer-38-Trilho-fielzinho.md`, 7c87301): VOLTA pelo conserto 1; os dele 14/14 (36, 38, 07sd, 09sd).
  Fiel aceitou na primeira troca.

## Rodada 2 — 2026-10-17 ~13h10 (b854a7e)

**Veredito: PASSA** (Fiel sozinho; Fielzinho sem cota até 17h15, leitura pendente).
- Conserto 1: `Invoke-Limpeza` (ensaio.psm1) roda cada passo por conta própria e relança a primeira queda; 09 e 10
  param cada instância numa closure e derrubam o ensaio depois; o 08 guarda os registros, desce e apaga a raiz em três
  passos. Testes novos rodam o `finally` real (pelo parser) com o `Stop-McpBanco` lançando, com contraprova no antigo.
- Sonda do Fiel: nas closures (`GetNewClosure`), o `Stop-McpBanco` importado pelo teste fica visível (as duas
  instâncias o veem), como no Docker real.
- `conteudo.mjs`: só o comentário (pedido do maestro).
- Fiel: 38, 36, 07-kit-sem-docker, 09-mcp-banco-sem-docker e o detector: 25/25; `git status` limpo.

## Leitura do Fielzinho — rodada 2, 2026-10-17 (após retomada)

Segunda leitura documental da ponta b854a7e, já juntada e resolvida, por orientação do maestro: somente registrar. Conferidos o diff completo 7c87301..b854a7e, o relatório r2, os novos casos do 38-ensaio-banco e o final de logs/trilho-38-r2-leves.log (60 testes, 60 passam, zero falhas).

Concordo com o fechamento do conserto 1: Invoke-Limpeza tenta os passos restantes e relança a primeira queda; 09/10 isolam cada parada do MCP e a remoção; 08 protege também New-Item dos registros e mantém a remoção da raiz como passo separado. Os casos novos extraem os finally reais e injetam as falhas apontadas na r1. Nenhum achado novo nesta leitura do conserto.

Não executei testes nesta retomada. Os 60/60 são evidência do Trilho; os 25/25 e a sonda de escopo das closures são evidência registrada pelo Fiel. Docker continua dispensado nesta rodada, conforme fechamento. Este registro complementa a revisão já encerrada; não reabre o ticket e não altera o veredito do Fiel.
