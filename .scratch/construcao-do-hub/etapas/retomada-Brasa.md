# Retomada da Brasa

Atualizada em 2026-10-16 ~21h20. Papel: construtora (regras em `etapas/regras-da-construcao.md`; leia inteiras).
Revisores: Fiel e Fielzinho (dupla). Integrador: Rebite (depois do "passa", `maestri ask "Rebite" ...`). Maestro:
`maestri ask "Claude Code" ...`. Fila: ticket 07 agora, depois o 08 (receita da etapa 2, opção A).

## Ticket 07 (banco do par), Status claimed

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

### Próximo passo exato

1. (feito) teste verde e commit 4967c69. Rodar o teste: `pwsh -NoProfile -File agents/code/test/07-banco.test.ps1` em segundo plano, com log em `.local/07.log` e um laço `until grep saida=`. Contêineres `hub-ensaio-07-a/b`, portas 5994/5995.
2. (21h50, sem commit ainda) item 3 editado na worktree: `ensaio.psm1` ganhou `Start-EnsaioBanco [-Exclusoes {}]`,
   `New-EnsaioBanco -SemSalComum` e `Set-ExclusaoComPonto`; provas 01/02 e o teste do 06 importam o `ensaio.psm1`;
   cópias apagadas (`git rm`). Falta rodar as três (uma de cada vez; logs `.local/prova01.log`, `prova02.log`,
   `06.log`) e o 07 de novo, e commitar. Prova 01: verde (saída 0, 22h). Prova 02 rodando.
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
- Rápidos do repositório: `node --test "agents/code/test/**/*.test.mjs"`.
- Provas: `pwsh -NoProfile -File agents/code/test/provas/01-banco/prova.ps1` e `.../02-pastas-com-ponto/prova.ps1`;
  teste do 06: `pwsh -NoProfile -File agents/code/test/gerar-exclusoes/sincronizador.ps1`.

## Feito antes (fechado)

- Ticket 01 (prova dos dois CouchDB): juntado por Rebite em 45ec3b0. Relatório `etapas/00-provas/relatorio-banco.md`,
  parecer `etapas/00-provas/parecer-Brasa.md`.
