# Parecer do 49 (Brasa), rodada curta — Fiel, 2026-10-18

Ramo `ticket-49` até c3f2868 (contém `integracao` 7b6c406). Relatório `etapas/relatorio-49-par-novo-com-hub.md`.
2ª leitura: subagente Opus, `parecer-49-Brasa-segunda-leitura.md`. Acordo nos dois.

## Veredito: VOLTA (só o relatório e a ordem para o B). O código pode juntar como está.

O ensaio mede o que diz. Cada número do relatório bate com os registros (121/121, 399 reescritos, 16/16, 0/0, 1/0,
400 binários, caso 6: 08 ENOENT antes, 10 passa, espera 290/226 s, `git status` 0, 16 do checkout, 08/10 depois).
Sem verde falso. c3f2868 é inócuo e fecha o 50. O que volta é a receita do par B: seguida ao pé da letra, quebra.

## O que o Fiel rodou

- Leves: `gerar-exclusoes/gerador`, `12-busca`, `harness-real`: 26/26, 0 pulado.
- Sonda sem Docker (montar.mjs + clone `autocrlf=true`): 19 arquivos diferem do A, entre eles as 2 notas de `labs/`
  (A em LF, commit em CRLF). Confirma as "2 diferentes" do caso 6 r2; a conta de 8f7f4a6 está certa.
- Sonda do c3f2868: hub do montar.mjs com `.livesync/ignore` e `.livesync-snapshot.json`: `git status` vazio.
- Sem Docker; sondas em `%TEMP%\hub-ensaio-49-fiel-*`, apagadas.

## Consertos (no relatório; e o que for para o 26)

1. **O clone de fora não pode ser apagado: o sincronizador do B aponta para ele** (2ª leitura; Fiel conferiu).
   `banco.psm1:371`: `$laco = Join-Path $script:Aqui 'laco.ps1'`, gravado no XML da tarefa (`:406`). Rodado do
   `C:\Projetos\hub-kit`, a tarefa chama o laço de lá. Ordem certa: depois do git, rodar o kit **do próprio hub**
   com `-Passos 04,08,10` (o 04 é idempotente e regrava o XML com o caminho do hub); só então registrar a tarefa e
   apagar o clone. Escrever isso no passo 5 da recomendação e na "Ordem para o par B".
2. **O checkout "só do que falta" ressuscita o que o A apagou** (2ª leitura). O teste faz `git ls-files -d` e
   `checkout` de tudo (`49-par-novo-com-hub.test.ps1:172-173`). Uma nota que o A apagou depois do último commit volta
   no B e o LiveSync a devolve ao A. A receita do 26 deve restringir ao que o banco não leva: caminhos com um
   segmento começando por ponto (ex.: `git ls-files -d -z` filtrado por `(^|/)\.`). O relatório diz "o que tem
   ponto", mas o comando do teste não faz isso.
3. **`core.autocrlf=true` no B é condição também do caminho recomendado** (2ª leitura). Com outro valor, o
   `git status` do B sai todo modificado e a cópia diária (`git add -A`) comita o hub em outro final de linha. Hoje o
   relatório só põe essa condição no caminho "se já clonou". Pôr como pré-condição do passo 3.
4. **A causa do `.livesync/` no `git status` está errada** (2ª leitura; Fiel conferiu). O gerador de exclusões grava
   `.*` e as pastas locais no `.git/info/exclude` (`gerar-exclusoes.mjs:65`), mas só se o `.git` já existe. No caso 6
   ele rodou (passo 04) antes do `git init`. No `C:\context-hub` do A, o `.git/info/exclude` tem `.*` (linha 9) e o
   `git status` não mostra `.livesync` (conferido). Corrigir o "achado à parte": o A não tem o problema. Mais grave
   que o `??`: sem o exclude, as **pastas `local: true` do B ficam fora do `.git/info/exclude`** e a cópia diária as
   comitaria no GitHub. O 04 rodado de novo depois do git (conserto 1) resolve. O c3f2868 fica (inócuo, pedido do
   Gustavo; fecha o 50), mas o ticket 50 e o relatório devem dizer a causa certa.
5. **O comando do passo 1 está incompleto** (2ª leitura). Falta `-Casa $HOME` (sem ele o kit recusa,
   `instalar.ps1:19`) e `-EnvFile <par B>.env` (o 04 e o 05 o exigem). O `C:\context-hub` vazio tem de existir antes
   (`Longo` faz `Resolve-Path`). Seguir para o git só com a linha "o par recebeu o hub" da espera.
6. **Listar o que muda na `agents/code/docs/instalacao.md` para o B** (2ª leitura): §0/§2 (o B não clona em
   `C:\context-hub`); §4/§7 (comandos pelo clone de fora; `-WhatIf` só com `00,03,04,05`, pois o 08 para com o hub
   vazio mesmo simulado); §9 (o B em duas vezes); passo novo do git (com `git remote add origin`); §11 (registrar a
   tarefa só depois do conserto 1); §15 (tirar "B com o clone já no disco"). Basta a lista no relatório; a mudança da
   doc é de quem o maestro indicar.

## Ressalvas (não seguram)

- O 03 e o 05 com a pasta vazia não rodaram (só leitura; ninguém lê conteúdo do hub; o 03 cria `.local\busca`, com
  ponto). O fork do 05 lê o `AGENTS.md` por sessão: vazio até a espera, sem quebrar.
- Nunca rodar o 08 no HOME real antes do git: ele pode deixar links quebrados antes de parar.
- O teste com os casos padrão sai 1 por construção (casos 3, 4 e 5 conferem o que o LiveSync não faz): dizer no
  cabeçalho que esses casos são medidas, não aceite.
- Juntar com `integracao` sem risco: um teste novo (nenhum executor percorre `*.test.ps1`) e 3 linhas no `.gitignore`.
