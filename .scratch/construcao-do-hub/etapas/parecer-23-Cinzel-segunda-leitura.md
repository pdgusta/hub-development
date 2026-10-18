
## Junção 9fcf4cf (2026-10-17)

Veredito: PASSA.

1. Conflito em agents/code/test/harness-real.test.mjs: `git diff 2379d38^2 2379d38` mostra só adições sobre a integracao: SO_APP_SERVER com 23-kit.test.mjs (linhas ~33-43), filtro `!excecao(f)` em COM_HARNESS, e o teste "a exceção do app-server é estreita" (~139). Os dois testes do modelo do 43 seguem no arquivo (comentário "Ticket 43" logo depois). Nada do 23 nem da integracao perdido.
2. `git diff 9fcf4cf^2 9fcf4cf --stat`: 20 arquivos, 1338 inserções, 1 remoção (a linha do filtro em harness-real). Só adições do 23 (kit/par, 23-kit.test.mjs, 8 SKILL.md); nada da integracao (11, 27-pastas) removido.
3. `node --test 23-kit.test.mjs` sozinho, 3 vezes: 20/20, 20/20, 20/20, 0 falhas, sem EPERM em rename (o único "EPERM" nos logs é o nome do teste de falha injetada). Logs: etapas/logs/revisao-23-segunda-sozinho-{1,2,3}.log. Cada rodada levou ~5 min (máquina lenta).
4. `node --test harness-real.test.mjs`: 9/9, 0 falhas.
5. `git status --short` limpo na worktree; nenhuma hub-ensaio-23-* em %TEMP%.

## Conserto ceda444 (2026-10-17)

Veredito: PASSA.

- Os 4 fs.renameSync do casa.mjs (guardar, devolução, gravarRegistro, desfazer) passaram a `renomear` (agents/code/kit/par/kit/casa.mjs:45-59, 88, 119, 134, 189). Sobrou só o rename dentro do helper (casa.mjs:53). Nenhum outro rename em agents/code/kit/**.
- Laço termina sempre: limite de 2 s por Date.now (casa.mjs:48-57), repete só EPERM/EBUSY/EACCES (casa.mjs:47), qualquer outro código sobe na hora. Atomics.wait de 100 ms é aceitável em script síncrono (não trava a thread principal de servidor aqui).
- Testes (agents/code/test/23-kit.test.mjs:497-548): 5 verdes rodados por nome (pass 5, fail 0). Sem o conserto o primeiro rename falharia na hora, então os 4 de "passageiro" ficariam vermelhos e o "não passa" (exige >=1500 ms) também; não executei a versão sem conserto (não edito). Cobrem registro (3 códigos), guardar, devolução, desfazer e a desistência com o original de volta.
- Observação sem peso: a devolução (casa.mjs:119) fica dentro de try/catch que anexa o erro; coerente com o resto.
- `git status --short` da worktree limpo.
