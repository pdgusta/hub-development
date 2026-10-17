# Retomada do Trilho (construtor), gravada em 2026-10-17 ~00h50 (São Paulo)

Leia antes: `etapas/regras-da-construcao.md` (inteiras), os tickets 12 e 15 (Comments) e os relatórios deles. Responda em pt-BR, frases curtas. Sem
subagentes. Maestro = "Claude Code"; revisor = "Fiel"; integrador = "Rebite".

## Onde estou (2026-10-17 ~00h50, São Paulo)
- Ticket 12: juntado (integracao c5b946a). Ticket 15: rodada 1 do Fiel passa (ramo ticket-15, HEAD c789b9d, worktree
  C:/context-hub-wt/ticket-15); Rebite avisado. Relatórios: etapas/relatorio-12-busca.md e etapas/relatorio-15-aviso-de-leitura.md.
- Pendente nos dois: o ponta a ponta do Codex (limite de uso até 01:34 de 2026-10-17, hora de São Paulo). Aviso
  agendado (sleep em segundo plano) para 01:40.

## Falta (próximo passo exato)
1. Às 01:40: no ticket-12, HUB_HARNESS_REAL=1 HARNESSES=codex node --test --test-concurrency=1
   agents/code/test/ponta-a-ponta/12-busca.test.mjs; no ticket-15, o mesmo com 15-leitura.test.mjs. Um commit só de
   evidência em cada ramo (evidencia-12/codex ou evidencia-15/codex e os hashes); uso de login nos relatórios.
2. Pedir ao Fiel a rodada curta dos dois juntos; depois avisar o Rebite (ele junta e comenta nos tickets).
3. Se falhar: conserto no ramo do ticket. No 15, falha esperada é a leitura por PowerShell não cair no adaptador
   do Codex (leiturasDoShell em agents/code/hooks/leitura/leitura.mjs).
4. Esperar o próximo ticket do maestro.

## Achados (vão para o relatório)
1. **Caminho curto do Windows** (`GUSTAV~1.DEL`): o vigia de arquivos aborta o servidor na primeira mudança
   ("Assertion failed: !_wcsnicmp(filename, dir, dirlen)", libuv `src\win\fs-event.c`). Conserto no `iniciar.ps1`
   (realpathSync.native por `node -p`). O teste usa o `%TEMP%` curto de propósito.
2. **Vigia perde nota logo depois da partida**: gravando 20 notas em pastas novas logo que o MCP responde, 8 ficaram
   fora (medição de depuração); com 300 ms entre gravações, nada se perdeu. O `reindex` incremental recupera.
   Remédio: `relatorio.mjs --consertar` (sugerir ao maestro: a vigia, faixa 7, roda isso a cada passada). Intermitente
   no teste (perdidas 0 nas últimas rodadas).
3. **Cabeçalho quebrado entra no índice no reindex**: o gray-matter guarda o texto em cache; na segunda leitura passa
   vazio. Provado: `m(t)` lança, `m(t)` de novo devolve `{}`. O relatório lista a recusada com `no_indice`.
4. **Índice guarda caminho em NFD** (`busca-por-paráfrase.md`); comparar sempre em NFC.
5. Sem a lista do gerador, a busca leria `inbox/.rascunho-oculto.md` e a pasta `local: true` (provado por mutação);
   `.secrets/` e `.maestri/` saíam só pelo `.gitignore`. A ferramenta não ignora arquivo com ponto sozinha.
6. O servidor faz `GET https://registry.npmjs.org/obsidian-hybrid-search/latest` na partida (checagem de versão);
   `rerank: true` baixaria um modelo de ~570 MB (não usamos).
7. Download (liberado pelo maestro): `npm install` do obsidian-hybrid-search 0.16.2, 261 pacotes, 538 MB em
   node_modules, ~1 min; os scripts de instalação (better-sqlite3, onnxruntime-node, protobufjs) rodaram apesar do aviso
   `allow-scripts` do npm 11. Modelo arctic já estava em `~\.cache\huggingface\Snowflake` (313 MB), nada baixado.

## Falta (próximo passo exato)
1. `git -C C:\context-hub-wt\ticket-12 merge integracao` e rodar `node --test "agents/code/test/*.test.mjs"` (o glob
   não desce em `ponta-a-ponta/` nem `provas/`) e as duas suítes do 12.
2. Respostas do maestro (2026-10-16 22h23): (a) as **linhas de registro do MCP de busca nos três harnesses entram no
   12**, formato de cada harness tirado da documentação oficial com o trecho citado, no molde dos fragmentos do 14
   (`agents/code/hooks/guardas/fragmentos/*.json`) e do 27; (b) o **aceite com harness real entra no 12**, atrás de
   `HUB_HARNESS_REAL=1` (ver `agents/code/test/harness-real.mjs` do 29): confere que o harness chamou a busca e devolveu
   o caminho certo, sem julgar a redação. Login de ensaio pela regra (copiar, hashes antes/depois, apagar, registrar).
3. `agents/skills/busca/SKILL.md` (ferramenta `search`, modos, `relatorio.mjs`; a busca é a porta) e
   `agents/code/kit/par/env/03.env` com `HUB_MCP_BUSCA_URL=http://127.0.0.1:3939/mcp`.
4. Relatório `etapas/relatorio-12-busca.md` (feito, achados, downloads, medidas, usos de login); comentário no ticket.
5. Revisão: `maestri ask "Fiel" "Trilho: ticket 12 pronto para revisão no ramo ticket-12 (HEAD <hash>), relatório
   <caminho>"`. Depois do passa, avisar o Rebite.

## Armadilhas
- **Barra invertida some em heredoc** (bash e `python - <<EOF`): `'\n'` vira quebra real. Use o Edit para trechos com `\`.
- Write num arquivo existente exige Read antes.
- `before()` do node:test roda antes do fim do módulo: constantes usadas nele vêm antes (TDZ).
- Outro construtor pode rodar testes no `%TEMP%` ao mesmo tempo: não apagar `hub-ensaio-*` em massa.
- `timeout` do bash não mata o `node` filho do `pwsh`; no teste, `taskkill /T /F /PID <pid que abri>`.
- No `pwsh`, `\"` dentro de argumento para `node -e` quebra; use aspas simples dentro de aspas duplas.

## Comandos
```
cd C:\context-hub-wt\ticket-12
$env:HUB_BUSCA_OHS = 'C:\Projetos\bancada-busca\ohs\node_modules\obsidian-hybrid-search'   # só leitura, opcional
node --test agents/code/test/12-busca.test.mjs        # ~3-4 min
node --test agents/code/test/12-kit-busca.test.mjs    # ~2 min, sem HUB_BUSCA_OHS
node --test "agents/code/test/*.test.mjs"
```

## Scratchpad
Só depuração descartável (`dbg*.mjs`, `hub-dbg`, `ohs-lock`); o lock já está no repositório. Os achados estão acima.
