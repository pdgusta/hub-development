# Retomada do Trilho (construtor), gravada em 2026-10-17 ~01h20 (São Paulo)

Leia antes: `etapas/regras-da-construcao.md` (inteiras), os tickets 12, 13 e 15 (Comments) e os relatórios deles. Responda em pt-BR, frases curtas. Sem
subagentes. Maestro = "Claude Code"; revisor = "Fiel"; integrador = "Rebite".

## Onde estou (2026-10-17 ~01h20, São Paulo)
- Tickets 12 e 15: juntados (integracao). Ticket 13 (gemini pronto e desligado): ramo ticket-13, worktree
  C:/context-hub-wt/ticket-13, com integracao 57e85cf juntada (merge 6bfb506). Relatório etapas/relatorio-13-gemini.md.
  Commits: f8b8769 (teste do 12 pelo índice), 32e77b2 (gemini.env e iniciar.ps1 -Gemini, 4 testes com dublê),
  95e37b7 (teste único feito: 62 pedidos ao Google; contêiner parado de novo).
- eb7c941: o teste do 13 fecha todos os dublês. Suíte 172 passam, 8 pulados, 0 falham. Merge de integracao 57e85cf (6bfb506). Revisão do 13 PEDIDA ao Fiel em 2026-10-17 ~02h05 (HEAD 6bfb506); esperar o parecer em etapas/parecer-13-Trilho.md.
- Fiel PASSOU o 13 (rodada 1); passado ao Rebite em 2026-10-17 ~02h05. Próximo: Codex do 12 e do 15 na vez da trava (Brasa, Vela, depois eu).
- Ticket 35 (aval sem parecer registrado): ramo ticket-35, worktree C:/context-hub-wt/ticket-35, commits 140417a d65b18a 0b01cd9, teste do acervo 21/21. Falta: suíte comum com a trava, revisão do Fiel, Rebite. Relatório etapas/relatorio-35-avais.md. O Codex do 12 e do 15 tem prioridade quando a trava vier.
- Pendente: o ponta a ponta do Codex no 12 e no 15 (limite de uso até 01:34). Aviso agendado para 01:40 (pode ter
  se perdido no /clear: conferir a hora e seguir).

## Falta (próximo passo exato)
1. Ler o parecer do Fiel do 13 (etapas/parecer-13-Trilho.md) e aplicar consertos; depois do passa, avisar o Rebite.
2. Codex (depois das 01:34; é harness de verdade: trava pesada em etapas/trava-pesada.md antes, apagar ao fim):
   no ticket-12 (git merge integracao antes), HUB_HARNESS_REAL=1 HARNESSES=codex node --test --test-concurrency=1
   agents/code/test/ponta-a-ponta/12-busca.test.mjs; no ticket-15 (worktree C:/context-hub-wt/ticket-15, merge de
   integracao antes), o mesmo com 15-leitura.test.mjs. Um commit só de evidência em cada ramo (evidencia-NN/codex e os
   hashes); uso de login no relatório de cada um; rodada curta do Fiel dos dois; aviso ao Rebite (ele junta e comenta).
3. Se o Codex do 15 falhar: a leitura por PowerShell não caiu no adaptador (leiturasDoShell em
   agents/code/hooks/leitura/leitura.mjs); conserto no ramo ticket-15.

## Regras novas a lembrar
- Trava pesada (regras): Docker, suíte inteira, indexação da busca, npm install, harness de verdade: conferir
  etapas/trava-pesada.md (se menos de 30 min, esperar), criar com nome/o quê/hora, apagar ao fim. Suíte com
  --test-concurrency=1. Teste só do próprio arquivo dispensa a trava.
- FreeLLMAPI: contêiner freellmapi-freellmapi-1 (docker start/stop, nunca criar), memória livre >= 2 GB antes. Uso do
  dia: docker exec com node e better-sqlite3 em /app/server/data/freeapi.db (MSYS_NO_PATHCONV=1 no Git Bash).
- Script .ps1 sem [CmdletBinding()] não recusa opção desconhecida (vai para $args).

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
