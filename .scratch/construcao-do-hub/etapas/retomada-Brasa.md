# Retomada da Brasa

Atualizada em 2026-10-16 ~21h20. Papel: construtora (regras em `etapas/regras-da-construcao.md`; leia inteiras).
Revisores: Fiel e Fielzinho (dupla). Integrador: Rebite (depois do "passa", `maestri ask "Rebite" ...`). Maestro:
`maestri ask "Claude Code" ...`. Fila: ticket 07 agora, depois o 08 (receita da etapa 2, opção A).

## Ticket 29 (testes com harness só sob pedido), Status claimed, enquanto o 07 está em revisão

Se o Fiel devolver o 07: pausar o 29 e voltar ao 07 primeiro (maestro).

- Ramo `ticket-29`, worktree `C:\context-hub-wt\ticket-29`, de `integracao` 8d1d785. Commit 654c329.
- `agents/code/test/harness-real.mjs`: `comHarness(nome, fn)` (sem `HUB_HARNESS_REAL=1`, um teste pulado com o motivo;
  com ela, um `describe`), `relatorioDeHashes({ antes, depois, gravadoEm, rodadas })`.
- O corpo da prova 03 (`prova.test.mjs`, `instalar.test.mjs`) e da ponta a ponta do 14 foi embrulhado em `comHarness`;
  o `after` do 14 usa `relatorioDeHashes` (mtime do arquivo real contra a janela copiadoEm..apagadoEm de cada uso).
- `agents/code/test/harness-real.test.mjs`: costura 1 (os três sem a variável, com HOME/TEMP/APPDATA falsos e PATH só
  com o node: pulados com o motivo, nada criado, evidência igual) e costura 2 (as mensagens). Verde, 5 de 5.
- Suíte inteira sem a variável: 86 testes, 83 passam, 3 pulados (`.local/suite-sem-variavel.log`).
- (~21h50) Rodada de verdade feita: 11 de 11, commit 0266761; relatório `etapas/relatorio-29-harness-sob-pedido.md`;
  revisão pedida ao Fiel. Próximo: consertos do parecer; depois do passa, avisar o Rebite.
- (antes) Próximo: a rodada de verdade (`HUB_HARNESS_REAL=1 node --test --test-concurrency=1` dos três; log
  `.local/harness-real.log`; hashes reais antes em `.local/hashes-reais-antes.txt`), conferir hashes depois, desfazer
  ou commitar a evidência regravada (decidir: é a evidência da rodada pedida, então commitar), relatório
  `etapas/relatorio-29-harness-sob-pedido.md`, revisão ao Fiel.
- Aviso para o relatório: o teste de unidade `agents/code/test/14-guardas.test.mjs` (do Trilho) deixa pastas
  `hub-ensaio-14-*` no TEMP (só hub, sem login).

## Ticket 07 (banco do par), Status claimed

- (~22h50) Rodada 1 VOLTOU (parecer `etapas/02-banco/parecer-Brasa.md`). Consertos na worktree, sem commit ainda:
  `Get-PidSincronizador` confere a linha de comando (CliDb e daemon); `Initialize-Dispositivo` confere o dispositivo
  aceito com o .env (encrypt, passphrase, usePathObfuscation, couchDB_DBNAME, couchDB_USER, porta no couchDB_URI) e
  recusa a divergência; marca `.livesync/hub-aceito` só depois do ACCEPTED, e volta isConfigured a false se falhar.
  Teste sem Docker `agents/code/test/banco/kit-sem-docker.ps1` (CLI falso `cli-falso.cjs`), chamado por
  `agents/code/test/07-kit-sem-docker.test.mjs`: verde. Esperas fixas com folga (120 s). Merge integracao d5e4e16 em
  98a6d6e. Falta: suíte comum, Docker (07, provas 01/02, teste do 06), commit, relatório (seção rodada 2), Fiel.

- (~22h25) Merge de integracao 0a8e17f em e3ff419 (só o merge); rápidos sem harness 106 de 106. Docker do 07 não
  repetido depois deste merge (o Fiel roda o Docker na revisão).
- 29: juntado e resolvido pelo Rebite (integracao d5e4e16). No 07, juntar d5e4e16 antes de passar ao Rebite; daqui em
  diante a suíte comum é `node --test "agents/code/test/**/*.test.mjs"` (os de harness ficam pulados). Fica comigo só o que o Fielzinho achar depois.

- Ramo `ticket-07`, worktree `C:\context-hub-wt\ticket-07`, de `integracao` 8b9beef (com o 06). Commit 4967c69: kit e teste, **verde** (21 PASSA, saída 0; log `.local/07-verde-1.log`).
- Comentário de plano gravado em `issues/07-banco-do-par.md` (20:50).

### Feito (commit 4967c69)

- `agents/code/kit/par/04-banco.ps1`: o passo do kit. `-EnvFile <par.env> [-WhatIf]` sobe ou confere;
  `-Descer [-ApagarDados]` para (com `-ApagarDados`, `down -v` e apaga estado e cli-db).
- `agents/code/kit/par/banco/banco.psm1` (o módulo do kit), `compose.yml`, `couchdb.ini` (cópias da prova 01).
- `agents/code/kit/par/env/04.env.modelo`: os nomes do `.env` (estado do par em `HUB_BANCO_ESTADO`; o `.ini` copiado
  lá; `HUB_BANCO_INI` só é posto no ambiente na hora do compose).
- `agents/code/test/banco/ensaio.psm1`: dois pares de ensaio sobre o kit (`New-EnsaioBanco -Nome`, raiz em
  `%TEMP%\hub-ensaio-<Nome>`), notas, pastas locais pelo gerador, amostra do hub para "nada em claro", leitor.
- `agents/code/test/07-banco.test.ps1`: o teste de ponta a ponta (Docker; fora do `node --test`).

### Próximo passo exato (~21h20)

Em revisão com o Fiel (pedida ~21h20). Rodada final verde, relatório completo. Próximo: aplicar os consertos do
parecer `etapas/parecer-Brasa.md` (o Fiel decide a pasta); depois do passa, avisar o Rebite.

### Antes (~21h05)

0. Feito: 810bbde (provas sobre o módulo), 7fa0e56 (religar o CLI), merge 3babfb2 de integracao 8d1d785; 07 verde
   (24 PASSA, `.local/07-verde-2.log`). Relatório `etapas/relatorio-07-banco-do-par.md` escrito; falta a seção
   "Rodada final" (logs `.local/prova01-2.log`, `prova02-2.log`, `06-2.log`, rodando em fila) e pedir revisão ao Fiel.


1. (feito) teste verde e commit 4967c69. Rodar o teste: `pwsh -NoProfile -File agents/code/test/07-banco.test.ps1` em segundo plano, com log em `.local/07.log` e um laço `until grep saida=`. Contêineres `hub-ensaio-07-a/b`, portas 5994/5995.
2. (sem commit ainda) item 3 editado na worktree: `ensaio.psm1` ganhou `Start-EnsaioBanco [-Exclusoes {}]`,
   `New-EnsaioBanco -SemSalComum` e `Set-ExclusaoComPonto`; provas 01/02 e o teste do 06 importam o `ensaio.psm1`;
   cópias apagadas (`git rm`). Falta rodar as três (uma de cada vez; logs `.local/prova01.log`, `prova02.log`,
   `06.log`) e o 07 de novo, e commitar. Prova 01: verde (saída 0). Prova 02 rodando.
   Caso novo no 07 (item 7, vermelho esperado): rodar o passo de novo religa o CLI só se o gerador disse `mudou`. O
   conserto vai em `Install-ParBanco` (kit/par/banco/banco.psm1): se `Update-Exclusoes` devolve `mudou` e o daemon
   roda, `Stop-Sincronizador` antes de `Start-Sincronizador`.
   `integracao` andou para 8d1d785 (ticket 14): juntar no ramo antes da rodada final.
3. Ressalva 3 do parecer: as provas 01 e 02 (`agents/code/test/provas/0[12]-*/`) e o teste do 06
   (`agents/code/test/gerar-exclusoes/sincronizador.ps1`, que importa o `banco.psm1` da prova 02) passam a importar
   `agents/code/test/banco/ensaio.psm1`; apagar as cópias (`banco.psm1`, `compose.yml`, `couchdb.ini`,
   `04.env.modelo`) das provas; rodar as três de novo (cada uma sobe Docker; uma de cada vez).
   Atenção: a prova 02 usa `Start-Sincronizador -Reiniciar` e `Set-ExclusaoComPonto` (adaptar: o kit não tem
   `-Reiniciar`; parar com `Stop-Sincronizador` e subir de novo com `Start-Sincronizador`, que não refaz o dispositivo).
4. Relatório em `etapas/02-banco/relatorio-07.md` (criar a pasta se não existir; confirmar o lugar com o maestro se
   houver outro padrão), com a seção "o que vai doer ao ligar"; merge de `integracao` se andou; testes de novo; pedir
   revisão ao Fiel; depois do passa, avisar o Rebite.

### Decisões e armadilhas

- O daemon **não pode herdar os handles** de quem chama o kit: com `Start-Process -Redirect*`, quem lê a saída do
  passo trava para sempre (aconteceu às ~21h). Agora sobe por `cmd /c ... > log 2> err` sem `-Redirect*`, e o PID
  gravado é o do `node` filho do `cmd` (por `Win32_Process`).
- O `-WhatIf` funciona (conferido à mão). O retrato da pasta passou a olhar só arquivos.
- O passo roda o gerador de exclusões (`agents/code/bin/gerar-exclusoes.mjs`, ticket 06) antes da primeira partida.
  O hub de ensaio tem uma pasta `local: true` (`initiatives/context-hub/labs`), então a comparação A→B tira as locais.
- Lições da etapa 0 já no módulo: o mesmo sal da E2EE nos dois bancos (`_local` não replica; o kit recusa se o banco
  já tem outro sal); um `couchdb.ini` por par; esperar `_up` sem credencial; a linha `[Done]` vale; `LiveSync active` é
  o sinal de pronto; `HUB_ROOT` sob pasta com ponto é recusado.
- Contêineres: o nome vem do `.env` (o modelo diz `hub-banco`; o ensaio usa `hub-ensaio-07-*`).
- Nunca `taskkill` por nome: o PID está em `<estado>\sincronizador.pid`. Para achar um daemon órfão:
  `Get-CimInstance Win32_Process -Filter "Name='node.exe'"` e filtrar a linha de comando por `hub-ensaio-07`.

### Comandos de teste

- Ticket 07: `pwsh -NoProfile -File agents/code/test/07-banco.test.ps1` (saída 0 = verde).
- Rápidos do repositório (regra provisória do maestro, até o ticket 29 entrar em integracao: fora `ponta-a-ponta/` e
  `provas/03-codex-hooks/`, que chamam harness de verdade): `node --test agents/code/test/04-esqueleto.test.mjs
  agents/code/test/05-frontmatter.test.mjs agents/code/test/05-nova-iniciativa.test.mjs agents/code/test/14-guardas.test.mjs
  agents/code/test/gerar-exclusoes/gerador.test.mjs`. Depois do 29: só com `HUB_HARNESS_REAL=1`.
- Provas: `pwsh -NoProfile -File agents/code/test/provas/01-banco/prova.ps1` e `.../02-pastas-com-ponto/prova.ps1`;
  teste do 06: `pwsh -NoProfile -File agents/code/test/gerar-exclusoes/sincronizador.ps1`.

## Feito antes (fechado)

- Ticket 01 (prova dos dois CouchDB): juntado por Rebite em 45ec3b0. Relatório `etapas/00-provas/relatorio-banco.md`,
  parecer `etapas/00-provas/parecer-Brasa.md`.
