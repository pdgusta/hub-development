# Relatório do 49: par novo com o hub já no disco (Brasa, 2026-10-18 ~14h35)

Ramo `ticket-49` (worktree `C:/context-hub-wt/ticket-49`, de `integracao` 7b6c406), último commit ee71863 (r1 do Fiel consertada).
Teste: `agents/code/test/49-par-novo-com-hub.test.ps1` (Docker, portas 5988/5989, contêineres `hub-ensaio-49-a/b`).
Registros em `etapas/logs/`: `49-rodada-1-lf.log`, `49-rodada-2-dezoito-lf.log`, `49-rodada-3-casos-1-2.log`,
`49-rodada.log` (casos 4 e 5) e `49-caso-5-contas.json` (as contas do caso 5, feitas à mão nos pares que ficaram de
pé quando o Maestri reiniciou às ~14h03).

## Como o ensaio monta o 26

O A sobe sozinho pelo passo 04 e semeia o banco dele (578 arquivos do hub de ensaio). O B ganha um `git clone` do hub
do A (mtime de agora, como no 26) e sobe pelo kit (`instalar.ps1 -Passos 04,espera`) com o banco vazio. Depois:
conflitos crus nos dois bancos, gerações de revisão, o que mudou nos dois discos, uma passada da vigia de cada par.

## O que se mediu

| Caso | Disco do B antes do kit | Conflitos (A/B) | Discos | Vigias |
|---|---|---|---|---|
| 3 (rodada 1) | clone em LF (`autocrlf=false`), A em CRLF: 520 de 578 diferentes | 121 / 121 | **399 arquivos do A reescritos** com a versão LF do B | B em divergência (conflitos) |
| 1 (rodada 2) | clone com 18 notas em CRLF e o A com elas em LF | 16 / 16 | os dois intactos | B em divergência (16 conflitos) |
| **1** (rodada 3) | **bytes iguais aos do A** | **0 / 0** | os dois intactos | B ok (a do A não foi medida nesta rodada) |
| 2 (rodada 3) | iguais, mais 1 arquivo só no B e 1 nota alterada no B | 1 / 0 | o arquivo novo chega ao A; cada disco fica com a sua versão da nota | (vigia não medida nesta versão do teste) |
| 4 | iguais; o banco do B puxa o do A antes de o CLI do B partir | 0 / 0 | os dois intactos | **A e B: 400 "binário descartado" cada** |
| 5 | como o 2, com o banco do B puxando antes | 1 / 1 | o arquivo novo chega ao A; cada disco fica com a sua versão | A e B mostram o conflito da nota, e mais 400 "binário descartado" cada |

A espera do kit disse "recebeu" em todos (29 a 79 s; 576 ou 577 arquivos, faltam 0).

## O que isso quer dizer

1. **O LiveSync compara bytes.** Mesmo texto com final de linha diferente é conflito (rodadas 1 e 2). Pior: no caso 3,
   o B mais novo **reescreveu 399 arquivos no disco do A**. Final de linha diferente entre os pares é o maior risco.
2. **Com os bytes iguais, o clone é inócuo** (caso 1 da rodada 3): nenhum conflito, nada reescrito.
3. **Uma diferença real não some calada** (casos 2 e 5): o arquivo só do B chega ao A; a nota alterada vira um
   conflito aberto, cada disco fica com a sua versão, e a vigia mostra o conflito (caso 5, nos dois pares).
4. **Puxar o banco antes do CLI (casos 4 e 5) piora**: zero conflito aberto, mas 400 folhas apagadas nos arquivos que
   o LiveSync trata como binário (`.mjs`, `.json`, `.ps1`...), que a vigia conta como "binário descartado" nos dois
   pares. O conteúdo é o mesmo, mas são 400 falsos alarmes que o Gustavo teria de marcar com `vigia olhei`. Descartado.

## O risco no 26 de verdade

O clone do GitHub traz os bytes do **último commit**, não os do disco do A no momento. O `C:\context-hub` do A tem os
arquivos rastreados em CRLF (`autocrlf=true`), mas o que os agentes gravam depois do commit (node grava em LF) e o que
ainda não foi commitado diferem do clone. Cada diferença vira conflito (nota) ou alarme de binário; e se o Git do B
tiver `autocrlf` diferente do A, o caso 3 se repete (o disco do A reescrito).

## Recomendação para o par B do 26

**B sobe com o `C:\context-hub` vazio e o git chega depois** (o caminho já provado no 46, prova `46-espera-banco`,
6 PASSA):

(Revista depois do parecer do Fiel, r1: `etapas/parecer-49-Brasa.md`.)

**Pré-condições no B:** `git config --global core.autocrlf` é `true`, como no A (com outro valor, o `git status` do B
sai todo modificado e a cópia diária, `git add -A`, comita o hub em outro final de linha); a pasta `C:\context-hub`
existe e está **vazia** (o `instalar.ps1` resolve o caminho e recusa pasta que não existe); o `.env` do B pronto (§3 da
`instalacao.md`).

1. **O kit de fora.** Clonar o hub só para ter o kit: `git clone <url do hub> C:\Projetos\hub-kit`.
2. **Banco, busca, MCP e espera, com a pasta vazia:**
   `pwsh C:\Projetos\hub-kit\agents\code\kit\par\instalar.ps1 -Casa $HOME -Hub C:\context-hub -EnvFile <B>.env -Passos 00,03,04,05,espera`
   (o `-WhatIf` antes, com estes mesmos passos: o 08 para com o hub vazio mesmo simulado). Seguir só depois da linha
   "o par recebeu o hub" da espera. **Não rodar o 08 aqui**: ele para (caso 6), e no HOME real pode deixar links
   quebrados antes de parar.
3. **O git, sem tocar nos arquivos que vieram do banco:**
   ```powershell
   git -C C:\context-hub init -b main
   git -C C:\context-hub remote add origin <url do hub>
   git -C C:\context-hub fetch origin main
   git -C C:\context-hub reset --mixed origin/main          # só o índice
   git -C C:\context-hub branch --set-upstream-to=origin/main
   # do commit, só o que o banco não leva: caminhos com um segmento que começa por ponto (.gitignore, .gitkeep,
   # .claude-plugin/ dos mods). Um checkout de tudo o que falta ressuscitaria a nota que o A apagou depois do commit.
   $f = @(git -C C:\context-hub -c core.quotePath=false ls-files -d | Where-Object { $_ -match '(^|/)\.' })
   if ($f) { git -C C:\context-hub checkout -- @f }
   git -C C:\context-hub status --short                     # só o que o A ainda não commitou
   ```
   Um ` D` no `git status` é nota que o A apagou depois do último commit: não restaurar.
4. **O kit do próprio hub**, agora com o `.git`:
   `pwsh C:\context-hub\agents\code\kit\par\instalar.ps1 -Casa $HOME -Hub C:\context-hub -EnvFile <B>.env -Passos 04,08,10`.
   - O **04** (idempotente) regrava o XML da tarefa do sincronizador com o `laco.ps1` do hub. Rodado do clone de fora,
     o XML aponta para o `laco.ps1` de lá (`banco.psm1:371`, `Join-Path $script:Aqui 'laco.ps1'`). Ele também grava o
     `.git/info/exclude` (`.*` e as pastas `local: true`): o gerador de exclusões só grava esse bloco se o `.git` já
     existe (`gerar-exclusoes.mjs:64`). No passo 2 ele ainda não existia. Sem o bloco, a cópia diária comitaria as pastas
     locais do B no GitHub.
   - O **08** e o **10**, com o hub no disco.
   - Conferir: `.git/info/exclude` com o bloco `# hub:exclusoes:inicio`; o XML `tarefa-sincronizador.xml` (na pasta
     `HUB_BANCO_ESTADO`) aponta `C:\context-hub\agents\code\kit\par\banco\laco.ps1`.
5. **Só então** registrar as tarefas agendadas (§11, com o Gustavo) e apagar `C:\Projetos\hub-kit`.

O passo 4 ficou fora do ensaio: o 04 do kit do próprio hub, o `.git/info/exclude` e o XML depois do git. Eles vêm da
leitura do código, conferida pelo Fiel e pela 2ª leitura dele. O caso 6 rodou os passos 2 e 3 e o `08,10` (do kit de
fora). No passo 3, o caso 6 fez o `checkout` de tudo o que faltava; a receita restringe ao que tem ponto. O passo 3
da receita foi conferido sem Docker (r1, Brasa): hub do `montar.mjs` como origem; um B com os arquivos sem ponto e uma
nota a menos (como se o A a tivesse apagado). Voltaram só o `.gitignore` e os 10 `.gitkeep`; a nota ficou ` D` no
`git status`, sem voltar.

Se o par B já tiver feito o clone em `C:\context-hub`: só seguir se `git config core.autocrlf` for `true` nas duas
máquinas **e** o A não tiver nada fora do commit (`git status` limpo no A logo antes do clone, com o A parado de
escrever); senão, apagar o clone e seguir o caminho acima.

## Sequência final do par B (para copiar)

Na B, em `pwsh`, com o Docker Desktop ligado, a variável de usuário `HUB_MCP_BANCO_TOKEN` posta (§9 da `instalacao.md`)
e o `.env` do B já trazido da A (§3). Preencher as duas primeiras linhas. Cada bloco para se algo falhar; rodar um
bloco por vez e ler a saída antes do próximo.

```powershell
# 0. O que muda de máquina para máquina
$Url  = '<url do repositório privado do hub>'     # o mesmo de onde a A empurra o main
$EnvB = 'C:\hub-transporte\<id do B>.env'         # o .env do B que veio da A
$Hub  = 'C:\context-hub'
$Kit  = 'C:\Projetos\hub-kit'

# 1. Pré-condições: autocrlf igual ao da A, a pasta do hub existe e está vazia, nenhum CLAUDE.md acima dela
git config --global core.autocrlf true
if (Test-Path $Hub) { if (Get-ChildItem -Force $Hub) { throw "$Hub não está vazia: pare (não clonar o hub nela)" } }
else { New-Item -ItemType Directory $Hub | Out-Null }

# 2. O kit de fora: só o código do kit, num clone fora do hub
git clone -b main $Url $Kit
if ($LASTEXITCODE) { throw 'clone do kit falhou' }

# 3. Primeiro o -WhatIf, só com estes passos (o 08 para com o hub vazio, mesmo simulado)
pwsh "$Kit\agents\code\kit\par\instalar.ps1" -Casa $HOME -Hub $Hub -EnvFile $EnvB -Passos 00,03,04,05,espera -WhatIf

# 4. Banco, busca, MCP e espera, com a pasta vazia; segue só com "o par recebeu o hub"
pwsh "$Kit\agents\code\kit\par\instalar.ps1" -Casa $HOME -Hub $Hub -EnvFile $EnvB -Passos 00,03,04,05,espera -PrazoEspera 900 |
    Tee-Object -Variable saida
if ($LASTEXITCODE) { throw 'o kit parou: ler a saída, consertar e rodar o bloco 4 de novo' }
$r = $saida | Where-Object { "$_" -like '{*' } | Select-Object -Last 1 | ConvertFrom-Json
if (-not $r.espera.convergiu) {
    # ainda recebendo: repetir até a linha "o par recebeu o hub: N arquivos do banco no disco"
    node "$Kit\agents\code\kit\par\espera.mjs" --hub $Hub --env $EnvB --segundos 600
    throw 'só siga para o bloco 5 depois de "o par recebeu o hub"'
}

# 5. O git, sem tocar nos arquivos que vieram do banco
git -C $Hub init -q -b main
git -C $Hub remote add origin $Url
git -C $Hub fetch -q origin main
git -C $Hub reset -q --mixed origin/main                 # só o índice
git -C $Hub branch -q --set-upstream-to=origin/main
# do commit, só o que o banco não leva (um segmento com ponto: .gitignore, .gitkeep, .claude-plugin/ dos mods);
# restaurar tudo o que falta ressuscitaria a nota que a A apagou depois do commit
$f = @(git -C $Hub -c core.quotePath=false ls-files -d | Where-Object { $_ -match '(^|/)\.' })
if ($f) { git -C $Hub checkout -- @f }
git -C $Hub status --short   # só o que a A ainda não commitou; um " D" é nota que a A apagou: não restaurar

# 6. O kit do próprio hub: o 04 regrava a tarefa com o laço do hub e o .git/info/exclude; o 08 e o 10 com o hub no disco
pwsh "$Hub\agents\code\kit\par\instalar.ps1" -Casa $HOME -Hub $Hub -EnvFile $EnvB -Passos 04,08,10 -WhatIf
pwsh "$Hub\agents\code\kit\par\instalar.ps1" -Casa $HOME -Hub $Hub -EnvFile $EnvB -Passos 04,08,10
if ($LASTEXITCODE) { throw 'o kit parou: ler a saída, consertar e rodar o bloco 6 de novo' }
# conferir antes das tarefas
$estado = (Get-Content $EnvB | Where-Object { $_ -match '^\s*HUB_BANCO_ESTADO=(.+)$' } | ForEach-Object { $Matches[1].Trim() }) | Select-Object -Last 1
$xmlSinc = Join-Path $estado 'tarefa-sincronizador.xml'
if (-not (Select-String -Quiet -SimpleMatch "$Hub\agents\code\kit\par\banco\laco.ps1" $xmlSinc)) { throw "o XML $xmlSinc não aponta o laço do hub" }
if (-not (Select-String -Quiet -SimpleMatch '# hub:exclusoes:inicio' (Join-Path $Hub '.git\info\exclude'))) { throw 'o .git/info/exclude sem o bloco do hub' }
git -C $Hub status --short   # o .livesync e as pastas local: true não aparecem

# 7. As tarefas agendadas (com o Gustavo; §11)
schtasks /create /tn hub-sincronizador     /xml $xmlSinc
schtasks /create /tn hub-manutencao-diaria /xml "$HOME\.hub-kit\tarefas\hub-manutencao-diaria.xml"
schtasks /create /tn hub-vigia             /xml "$HOME\.hub-kit\tarefas\hub-vigia.xml"

# 8. O clone de fora sai (nada aponta mais para ele)
Remove-Item -Recurse -Force $Kit
```

Do ensaio: os blocos 4 e 5 (o 5 com o `checkout` de tudo o que faltava; o filtro do ponto conferido à parte, sem
Docker) e o `08,10` de fora depois da espera. Só pela leitura: o bloco 6 com o 04 do próprio hub (XML e exclude) e as
conferências dele; o nome `hub-sincronizador` é sugestão (a doc deixa `<nome>`); o 03 e o 05 com a pasta vazia.

## Caso 6: o caminho recomendado, com o kit de fora (pedido do maestro, 14h50)

O kit roda desta worktree (como o `C:\Projetos\hub-kit` do 26) com `-Hub` na pasta vazia do B. Registros:
`49-rodada-caso-6.log` (1ª), `49-rodada-caso-6-r2.log` e `49-medidas-caso-6-r2.json` (2ª), `49-repro-08.log` (o 08 sem
Docker).

- **Antes da semente, o 08 para**: `ENOENT ... scandir '<hub>\agents\skills'` (código 1). Ele lê as skills e os
  fragmentos de hook do hub. O **10 passa** com o hub vazio (só grava os XML com os caminhos).
- **O kit sobe o B e a espera converge**: 290 s (1ª) e 226 s (2ª); 576 arquivos, faltam 0.
- **O git depois** (`init`, `fetch`, `reset --mixed`, `checkout --` de tudo o que falta): `git status` vazio, fora o
  `?? .livesync/` (1ª rodada; a 2ª o deixou fora da conta; causa abaixo). O
  `checkout` trouxe 16 arquivos que o banco não leva: os de nome com ponto (`.gitignore`, `.gitkeep`,
  `agents/code/mods/*/.claude-plugin/plugin.json`) e a pasta local `initiatives/context-hub/labs/` (no ensaio, ela está
  no commit). **Esse passo é necessário no 26**: sem ele, os mods do Claude Code ficam sem o `plugin.json`.
- **Depois da espera, o 08 e o 10 passam** (2ª rodada): 8 junctions de skill, todas com o `SKILL.md`; 8 caminhos do hub
  nos hooks do `settings.json`, todos existentes. Na 1ª rodada, o 08 parou por falta de `HUB_MCP_BUSCA_URL` no `.env`
  do ensaio do banco (o do 26 vem dos modelos do gerador): falha do teste, corrigida em 83344d5. A repro sem Docker
  mostra também que o 08 passa na mesma casa onde tinha parado antes da semente.
- Nenhum conflito nos dois bancos; o disco do A como estava; vigia do A ok, a do B só "informa" (a lista de exclusões
  mudou quando a pasta local chegou pelo git).
- A única falha da 2ª rodada foi da conta, não do caminho: "o disco do B igual ao do A" contou 2 diferentes. Por
  eliminação, são as 2 notas da pasta local `labs/`, a única coisa que o B tem sem vir do banco (o git as traz nos
  bytes do commit). A conta passou a deixar as pastas locais de fora (8f7f4a6), **sem nova rodada**.

**Ordem para o par B** (a receita acima): kit de fora com `-Passos 00,03,04,05,espera` e a pasta vazia; o git; o kit
do próprio hub com `-Passos 04,08,10`; as tarefas; apagar o clone de fora. O 03 (npm em `<hub>\.local\busca`) e o 05
não leem conteúdo do hub (pela leitura; o fork do 05 lê o `AGENTS.md` por sessão, vazio até a espera, sem quebrar). O
10 passa com o hub vazio (rodada), mas vai para depois do git junto com o 08.

**O `.livesync/` no `git status` do caso 6** (causa corrigida pelo parecer do Fiel): veio da ordem, não do
`.gitignore`. O gerador de exclusões grava `.*` no `.git/info/exclude`, mas só se o `.git` já existe; no caso 6 ele
rodou (passo 04) antes do `git init`. O `C:\context-hub` do A tem o bloco (`.*`) e o `git status` dele não mostra o
`.livesync` (conferido). O 04 rodado de novo depois do git (passo 4 da receita) resolve. O c3f2868 (os dois no
`.gitignore`, pedido do Gustavo; ticket 50) fica: é inócuo e cobre o hub sem o bloco.

## O que muda na `agents/code/docs/instalacao.md` para o B

A mudança da doc é de quem o maestro indicar; a lista:
- §0 e §2: o B não clona em `C:\context-hub`; o clone vai para `C:\Projetos\hub-kit`, e a pasta do hub nasce vazia.
- §4 e §7: os comandos do B pelo clone de fora; o `-WhatIf` só com `00,03,04,05` (o 08 para com o hub vazio mesmo
  simulado).
- §9: o B em duas vezes (passos 2 e 4 da receita), com o git entre elas.
- Passo novo do git (passo 3 da receita, com `git remote add origin` e o `checkout` só do que tem ponto) e a
  pré-condição `core.autocrlf=true`.
- §11: registrar as tarefas só depois do passo 4 (o XML com o laço do hub).
- §15: tirar a ressalva "B com o clone já no disco" (resolvida pelo 49).

## O que não foi provado

- O 03 e o 05 com a pasta vazia (só pela leitura: não leem o conteúdo do hub).
- O passo 4 da receita (o 04 do kit do próprio hub depois do git: o XML e o `.git/info/exclude`), só pela leitura.
- A conta do disco do caso 6 depois do ajuste de 8f7f4a6 (sem rodada nova; a sonda do Fiel confirma as 2 notas de
  `labs/`, A em LF e commit em CRLF).
- O teste com os casos padrão sai com código 1 por construção: os casos 3, 4 e 5 medem o que o LiveSync faz com bytes
  diferentes, não são aceite (dito no cabeçalho do teste).
- A vigia do A no caso 1 (bytes iguais) não foi medida na rodada 3; no caso 4 ela não viu conflito.

## Docker e limpeza

Contêineres `hub-ensaio-49-a/b`, volumes, rede e a pasta `%TEMP%\hub-ensaio-49` apagados às ~14h35; os CLIs do ensaio
derrubados pelo `Uninstall-ParBanco`; nenhum processo do ensaio restante. O CLI do par A de verdade (`C:\hub-par`) não
foi tocado. Trava solta às 14h35. Caso 6: trava das 14h50 às ~15h05 e das 15h10 às ~15h20; o próprio teste
derrubou os pares (nenhum contêiner, volume ou pasta `hub-ensaio-49` restante, conferido).
