# Parecer do 49 (Brasa), 2ª leitura, volta r2

Revisor independente, 2026-10-18. Só leitura. Rodei: `git diff c3f2868 ee71863` (só o cabeçalho do teste); uma
prova em pasta temporária dos comandos de git do passo 3; o `Select-String -SimpleMatch` num XML UTF-16 com BOM, como
o do kit. Não rodei Docker nem o teste do 49.

## Veredito: passa (com ressalvas)

Os 6 consertos da r1 estão feitos, certos e completos no relatório. Nada novo quebra na receita.

## Os 6 consertos

1. **Clone de fora e a tarefa do sincronizador: feito.** Passo 4 da receita e bloco 6 da sequência rodam o kit do
   hub com `-Passos 04,08,10`. Conferi no código: `Write-TarefaSincronizador` usa `$script:Aqui` (`banco.psm1:371`,
   `Aqui = $PSScriptRoot`, linha 8), então rodado de `C:\context-hub\...` o XML aponta o laço do hub. Ele só reescreve
   se o texto mudou (`-ceq`), e mudou. O `Install-ParBanco` sempre chega ao último passo (`:445`). O registro das
   tarefas (bloco 7) e o `Remove-Item $Kit` (bloco 8) vêm depois. Também olhei se algo mais fica apontando para o clone
   de fora: o 03 copia a busca para `<hub>\.local\busca`; o 05 usa `HUB_MCP_BANCO_DIR` do `.env`; o 10 grava XML com
   caminhos do `-Hub`. Só o XML do 04 apontava para o clone, e o passo 4 o conserta.
2. **`checkout` de tudo: feito.** O filtro `Where-Object { $_ -match '(^|/)\.' }` roda em pwsh (`-match` sobre cada
   linha). `@(...)` garante array; `checkout -- @f` espalha o array no comando nativo. Provei com origem local: um
   `.gitkeep`, um `.p/q` (pasta com ponto) e uma nota `n/n.md` apagada. `ls-files -d` listou os três; o filtro deixa
   passar só `.gitkeep` e `.p/q`; a nota fica ` D`. O texto "Um ` D` é nota que o A apagou: não restaurar" está no
   relatório e no bloco 5.
3. **`autocrlf`: feito.** Pré-condição e bloco 1 (`git config --global core.autocrlf true`). Ver a ressalva a.
4. **Causa do `.livesync/`: feito.** O relatório diz a ordem (gerador antes do `.git`), tira a culpa do `.gitignore` e
   mantém o c3f2868 como inócuo. O ticket 50 (comentário de ~15h55) diz o mesmo.
5. **Comando completo: feito.** Passo 2 traz `-Casa`, `-Hub`, `-EnvFile`, `-Passos`; pasta vazia criada no bloco 1;
   segue só com "o par recebeu o hub" (`convergiu` existe em `espera.mjs:119/124`; o JSON final do `instalar.ps1`
   leva `espera`, linhas 128-130).
6. **Lista da `instalacao.md`: feita**, com um furo pequeno (ressalva c).

## Passo 3 (comandos de git), em pwsh

Provado numa origem local com `init -b main`, `remote add origin`, `fetch -q origin main`, `reset -q --mixed
origin/main` num ramo ainda sem commit, `branch -q --set-upstream-to=origin/main`: sai `## main...origin/main`, o
arquivo diferente fica ` M`, os ausentes ` D`. A sintaxe pwsh está certa (`@f`, `$Hub` entre aspas não é preciso nos
`-C $Hub` sem espaço). `-c core.quotePath=false` só tira o escape de acento; nome com aspas ou tabulação continuaria
entre aspas, mas o hub não tem nenhum (conferido na r1).

## Passo 4: regrava o XML e grava o exclude com o CLI vivo?

Sim.
- `Install-ParBanco` não tem atalho para "já vivo": o passo de exclusões (`:439`) chama `Update-Exclusoes` sempre
  (`banco.psm1:292`). O `gerar-exclusoes.mjs` grava o bloco no `.git/info/exclude` assim que o `.git` existe (`:60-77`,
  `gravar` incondicional); o campo `mudou` só conta o `.livesync/ignore` e o `busca.env`, não o `exclude`.
- Com o CLI vivo e a lista sem mudança, `Start-Sincronizador` sai cedo (`Get-PidSincronizador`). Se a lista mudou, o
  kit para e religa (`:440-441`). Os dois estão certos.
- O XML é regravado no último passo (item 1). A conferência do bloco 6 (`Select-String -SimpleMatch` no XML, UTF-16
  com BOM) funciona; testei.
- `docker compose -p <contêiner> up -d` do clone do hub não recria o contêiner por causa do caminho (mesmo projeto, mesmo
  `.ini`); não rodei, é leitura.

## Ressalvas (não seguram)

a. O bloco 1 **grava** o `autocrlf` global do B (`git config --global ... true`), em vez de conferir. É o valor que o
   A tem e o 26 é feito com o Gustavo, mas é mudança global: a doc deve dizer "conferir com `--get` e, se for outro,
   perguntar", ou o 26 deve citar essa linha no aval.
b. No bloco 4, depois de `node espera.mjs`, o `throw` dispara sempre, mesmo quando a espera convergiu; quem lê entende
   ("rode o bloco 5 depois de ver a linha"), mas pode confundir. Melhor `Write-Warning` ou conferir o resultado dela.
c. A lista da `instalacao.md` não traz a linha da r1 "§2 'não verificado' vira o resultado do 49". Uma frase a mais
   para o Lume.
d. Seguem sem prova (o relatório já diz): o 04 do kit do hub depois do git, a pasta vazia no 03 e no 05, e a conta do
   disco do caso 6 depois de 8f7f4a6.
e. Juntar com `integracao`: o diff de c3f2868 a ee71863 é só o cabeçalho do teste (comentário), sem risco.
