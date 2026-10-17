# Parecer do ticket 38 (Trilho): o ajudante da pasta de ensaio nos testes que faltaram

## Rodada 1 — 2026-10-17 ~12h05 (leitura do Fiel; Fielzinho repassado, cota volta às 12h15)

Ramo `ticket-38`, HEAD f61906d; contém a `integracao` (fdd3760). **Leitura do Fiel: PASSA** (provisório até o
acordo com o Fielzinho).

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
