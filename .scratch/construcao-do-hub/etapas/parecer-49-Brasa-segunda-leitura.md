# Parecer do 49 (Brasa), 2ª leitura

Revisor independente, 2026-10-18. Só leitura: não rodei Docker nem o teste do 49. Rodei: o parser do PowerShell no
teste (0 erros), `git diff integracao...HEAD` (só o teste, 309 linhas), merge-base = `integracao` 7b6c406, worktree
limpa, `docker ps -a --filter name=hub-ensaio-49` vazio. Não li `parecer-49-Brasa.md`.

## Veredito: volta (só o relatório)

O ensaio passa: os números batem com os registros e o teste mede o que diz. A recomendação para o par B tem quatro
furos que quebrariam o 26 de verdade (consertos 1 a 4). São consertos de texto no relatório (e, depois, na
`instalacao.md`); o código do ramo pode juntar como está.

## O que conferi e bate

- Rodada 1 (`49-rodada-1-lf.log`): 520 de 578 diferentes, 121/121 conflitos, por extensão 76 md, 42 txt, 3 csv; 399
  arquivos do A mudados; espera 33 s, 576/0.
- Rodada 2 (`49-rodada-2-dezoito-lf.log`): 18 diferentes, 16/16, os dois discos intactos, espera 79 s.
- Rodada 3 (`49-rodada-3-casos-1-2.log`): caso 1 0/0, vigia do B ok, 42 s; caso 2 1/0, `disco_a A`, `disco_b B`,
  arquivo só do B chegou ao A, 49 s, 577.
- Casos 4 e 5 (`49-rodada.log`, `49-caso-5-contas.json`): 0/0 com `binario: 400` nas duas vigias; caso 5 1/1, a nota
  diferente nos dois discos, vigia do A com `conflito: 1` e `binario: 400`. Faixa da espera 29 a 79 s: confere.
- Caso 6 (`49-rodada-caso-6.log`, `-r2.log`, `49-medidas-caso-6-r2.json`): 08 antes da semente código 1 com
  `ENOENT ... scandir '...\b\hub\agents\skills'`; 10 código 0; espera 290 s e 226 s, 576/0; `git_depois.status 0`;
  `do_commit` com 16 caminhos (14 com ponto + as 2 notas de `labs/`); 08,10 depois: código 0, 8 skills, 8 caminhos de
  hook, nada quebrado; 0/0 conflitos; vigia A ok, B `informa exclusoes: 1`; 1 falha (diferentes 2).
- O teste: cada caso num ensaio novo; o `finally` derruba o último par (`Remove-EnsaioBanco` → `Uninstall-ParBanco
  -ApagarDados` e apaga a raiz); contêineres `hub-ensaio-49-a/b`; o compose publica em `127.0.0.1:${HUB_BANCO_PORTA}`;
  o kit roda com `-Casa` do ensaio (nada no HOME real); notificador dublê da vigia.
- Pela leitura do kit: 00 só procura `CLAUDE.md` do hub para cima e confere Windows/Node/Python; 03 só cria
  `<hub>\.local\busca` com o lock do kit; 05 sobe o fork, que lê `AGENTS.md` e esquemas a cada sessão/gravação
  (`src/hub.ts` e `main.ts:46` no `integracao` do fork), então subir com o hub vazio é seguro; a espera só lê o disco
  e o leitor. O 04 lê o hub só pelo gerador de exclusões (índices com `local: true`): vazio, nenhuma pasta local.
- O `instalar.ps1` aceita `-Hub` e roda de fora: cada passo é achado por `$PSScriptRoot`; o 03, o 08, o 10 e a espera
  recebem `-Hub`; o 04 e o 05 usam o `HUB_ROOT` do `.env` (não o `-Hub`).

## Consertos

1. **Apagar o clone de fora quebra o sincronizador do B.** O 04 escreve a tarefa do laço apontando o `laco.ps1` da
   pasta de onde o kit rodou: `banco.psm1:371` (`$laco = Join-Path $script:Aqui 'laco.ps1'`) e `:406`; o `laco.ps1`
   importa o `banco.psm1` vizinho, cujo gerador vem do mesmo clone (`banco.psm1:10-11`). Com o kit em
   `C:\Projetos\hub-kit`, o XML aponta para lá; o passo 5 da recomendação ("apagar o clone") faz a tarefa falhar em
   silêncio (o CLI não volta no logon). Mesmo mantido, o laço roda código congelado, fora do hub. Conserto: depois do
   git, rodar o kit **do hub** com `-Passos 04,08,10` (`C:\context-hub\agents\code\kit\par\instalar.ps1`): o 04 é
   idempotente e regrava o XML para o hub; só então registrar a tarefa e apagar o clone. O caso 6 não viu isso porque
   o kit rodou da worktree, que fica.
2. **`git checkout --` de tudo o que falta pode ressuscitar o que o A apagou.** O teste faz `git ls-files -d` e
   `checkout` de tudo (`49-par-novo-com-hub.test.ps1:172-173`); o relatório diz "só no que o banco não traz (o que tem
   ponto)", mas o comando que provou não filtra. No 26, uma nota que o A apagou (ou moveu) depois do último commit
   está no commit e não no banco: o checkout a recria no B, o CLI do B a sobe e ela volta ao A. No ensaio, o A não tinha
   nada fora do commit, por isso não apareceu. Conserto: restringir ao que o LiveSync não replica (um segmento que
   começa com ponto), por exemplo `git ls-files -d -z` filtrado por `(^|/)\.`; o resto que faltar é decisão de quem
   olha o `git status`, nunca checkout cego. Bônus: `-z` evita o caminho entre aspas com acento (hoje o hub não tem
   nenhum; conferido em `C:\context-hub`).
3. **`core.autocrlf=true` no B é condição também do caminho recomendado.** O teste roda o git com
   `-c core.autocrlf=$crlf`, `true` no caso 6 (`:167`, `:280`). Os arquivos que chegam do banco são os bytes do A (CRLF
   nos rastreados). Com `autocrlf=false` no B, o `git status` sai com cada texto modificado, e a cópia diária
   (`copia-diaria.mjs:46`, `git add -A`) gravaria o hub inteiro em CRLF no ramo `par/<B>`. O relatório só cita o
   `autocrlf` no atalho do clone. Conserto: no passo 3, "conferir `git config --get core.autocrlf` = `true` no B antes
   do `git init`".
4. **O achado do `.livesync/` tem a causa errada.** Não é o `.gitignore`: o gerador de exclusões grava em
   `.git/info/exclude` o bloco com `.*` (`gerar-exclusoes.mjs:58-77`), mas só se `.git` existe na hora. No caso 6 o
   gerador rodou (no 04) antes do `git init`, por isso `?? .livesync/`. No A ele já está lá: o
   `C:\context-hub\.git\info\exclude` tem o bloco `.*`, e o `git status` do A **não** mostra `.livesync/` nem
   `.livesync-snapshot.json` (conferido agora; o relatório diz o contrário). Conserto: tirar a proposta de mexer no
   `.gitignore`; no passo 3, rodar o gerador depois do git (o `-Passos 04` do conserto 1 já faz). A cópia diária roda o
   gerador antes do `add -A` (`copia-diaria.mjs:38`), então não comita o `.livesync/`.
5. **O comando da recomendação está incompleto.** `-Hub C:\context-hub -Passos 00,03,04,05,espera` sem `-Casa` recusa
   (`instalar.ps1:19`) e sem `-EnvFile` o 04 e o 05 param (parâmetro obrigatório). E o `C:\context-hub` tem de existir
   vazio (`Longo` faz `Resolve-Path`, `instalar.ps1:25`). Escrever o comando inteiro: `mkdir C:\context-hub`;
   `pwsh C:\Projetos\hub-kit\agents\code\kit\par\instalar.ps1 -Casa $HOME -Hub C:\context-hub -EnvFile <B>.env
   -Passos 00,03,04,05,espera`; seguir para o git só com a linha `o par recebeu o hub` (`convergiu: true`); se o prazo
   acabou, rodar a espera de novo até ela (a espera nunca falha, `espera.mjs:36-39`).
6. **Dizer o que muda na `instalacao.md`** (o Lume escreve; aqui só a lista): §0 linha 2 e §2 (o B não clona em
   `C:\context-hub`; clone de fora); §2 "não verificado" vira o resultado do 49; §4 passo 2 e §7 no B usam o caminho do
   clone de fora; §7 no B só com `-Passos 00,03,04,05` (o `-WhatIf` padrão passa pelo 08, que lê `agents\skills` e
   para com o hub vazio, `08-harnesses.mjs:44-46`, também no `--simular`); §9 no B em duas vezes (kit de fora, git,
   kit do hub com 04,08,10); o passo do git novo entre §10 e §11, com `git remote add origin <url>` (o `fetch <origem>`
   do relatório deixa o B sem remoto nem ramo de acompanhamento); §11 registrar a tarefa do laço só depois do
   conserto 1; §15 tirar "B com o clone já no disco".

## Ressalvas (não seguram)

- Não faltam passos 06, 07 ou 09: o kit só tem 00, 03, 04, 05, 08, 10, `proxy` e `espera` (`instalar.ps1:13`, `:77-84`);
  o gerador do 06 está dentro do 04, a vigia (07/16) é tarefa do 10, o fork (09) é o 05. O `proxy`, se subir, entra com
  o 04,08,10 do hub.
- Nunca rodar o 08 no HOME real antes do git: o `contrato` vem antes do `skills` (`08-harnesses.mjs:297-298`) e pode
  deixar links para um `AGENTS.md` que ainda não existe antes de parar.
- A conta "disco do B igual ao do A" do caso 6 foi mudada (8f7f4a6) sem rodada nova, e as 2 diferentes de `labs/` são
  explicadas "por eliminação" (a falha da r2 não diz os nomes). No 26 a pasta local não está no commit, então não se
  repete; mas no ensaio a `labs/` chegou pelo git com o CLI do B sem a exclusão dela (só a vigia religou o CLI depois);
  se ela subiu ao banco do B nesse meio-tempo, ninguém mediu.
- Rodando `-Casos` padrão (1 a 6), o teste sai 1 por construção: os casos 3, 4 e 5 conferem o comportamento desejado,
  que o LiveSync não tem. É prova, não regressão; vale dizer isso no cabeçalho do teste.
- O "por eliminação" e a espera por tamanho (não hash) seguem como ressalvas do 46.
- Juntar com `integracao`: sem risco (arquivo novo; nenhum executor percorre `*.test.ps1`).
