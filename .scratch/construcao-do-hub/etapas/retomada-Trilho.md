# Retomada do Trilho (construtor), gravada em 2026-10-16 ~22h30 (São Paulo)

Leia antes: `etapas/regras-da-construcao.md` (inteiras; há regra nova "Testes com harness de verdade": desde o ticket 29,
`ponta-a-ponta/` e `provas/03-codex-hooks/` só rodam com `HUB_HARNESS_REAL=1`), o ticket
`issues/12-busca-local-com-aceite.md` (com as respostas do maestro nos Comments) e as fontes: `spec.md` (bloco do
Worker 3) e `spec-partes/faixas-03-04.md` (faixa 3). Responda em pt-BR, frases curtas. Sem subagentes. Maestro =
"Claude Code"; revisor = "Fiel" (em dupla com o Fielzinho); integrador = "Rebite".

## Onde estou
- **Ticket 12** (busca local com aceite), `Status: claimed`. Ramo `ticket-12`, worktree `C:\context-hub-wt\ticket-12`,
  HEAD 616a1c0. Parte de `integracao` 8d1d785; **`integracao` andou para d5e4e16** (27 e 29 juntados): falta
  `git merge integracao`.
- Commits separados pedidos pelo maestro: 58b9563 (testes do 14 apagam as pastas temporárias, mesmo falhando) e 9cb10f4
  (o mesmo no 04 e no 05, com `maxRetries`); pastas antigas `%TEMP%\hub-ensaio-04/05/14-*` apagadas.

## Feito (todos verdes)
- `agents/skills/busca/iniciar.ps1`: roda o gerador de exclusões (recusa dele para tudo, alto), lê
  `.local/exclusoes/busca.env`, `LOCAL_EMBEDDING_MODEL=Snowflake/snowflake-arctic-embed-m-v2.0`,
  `XDG_CACHE_HOME=<hub>\.local\busca\estado`, tira `OPENAI_*`, sobe `node <pacote>\dist\src\cli.js serve --foreground
  --host 127.0.0.1 --port N`. Pacote: `HUB_BUSCA_OHS` ou `<hub>\.local\busca\node_modules\obsidian-hybrid-search`.
  Converte o hub para caminho longo (ver achados).
- `agents/skills/busca/relatorio.mjs [--url] [--consertar]`: indexadas (status), válidas, `faltando` (válidas fora do
  índice, por caminho NFC), `recusadas` [{caminho, erro, no_indice}], modelo, pendentes, consertadas; grava
  `.local/busca/relatorio.json`; código 1 se falta nota. `--consertar` chama o `reindex` incremental do MCP.
- `agents/code/kit/par/03-busca.ps1` (+ `kit/par/busca/package.json` e `package-lock.json`, 0.16.2 fixo): `npm ci` em
  `<hub>\.local\busca`, idempotente por hash do lock e versão instalada, `-WhatIf` (SupportsShouldProcess). Saída JSON
  {hub, mudou, versao, modelo_no_cache}.
- Testes: `agents/code/test/12-busca.test.mjs` (9: palavra, paráfrase sem palavra em comum, nota nova com tempo,
  exclusões com ponto/local na partida e com a busca ligada, relatório, Host estranho + só 127.0.0.1, inglês + .pdf.md +
  binário fora, rajada de 200, segunda partida reaproveitando o índice + --consertar) e
  `agents/code/test/12-kit-busca.test.mjs` (4: -WhatIf, instala pelo lock, segunda rodada não muda, busca sobe com a
  instalação do kit; ~1m45). Medidas em `agents/code/test/12-busca/evidencia/medidas.json` (regravado a cada rodada).
- Medidas: nota nova ~5 s; rajada de 200 ~13-17 s; partida 1 ~11-21 s, partida 2 ~5-7 s.

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
