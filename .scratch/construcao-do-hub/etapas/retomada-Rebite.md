# Retomada do Rebite (integrador), 2026-10-17 20h30 (construção fechada)

Leia nesta ordem: `regras-da-construcao.md`, `juntar-tickets.md` (inteiros), `registro-de-juncoes.md` (o que já
entrou), `fila-pesada.md`, e esta retomada.

## Estado

- Construção fechada (maestro, 2026-10-17 ~20h20). Todos os tickets juntados e resolvidos; o último foi o 25.
- Hub: worktree de junção `C:/context-hub-wt/integracao`, ramo `integracao`, ponta **dc514db** (docs 6ª sobre ca62332), limpa, verde (suíte:
  370, 355 verdes, 15 pulados, 0 falhas; log `logs/juncao-25-suite.log`).
- Fork do MCP do banco: worktree de junção `C:/Projetos/hub-mcp-banco-wt/integracao`, ramo `integracao`, ponta
  34c3e50. Tem junções (não pastas) em `node_modules` e `lib/livesync-commonlib` para a cópia principal
  `C:/Projetos/hub-mcp-banco`. `git status` nela só com `--ignore-submodules=all`. Nunca mexer em `main` do fork.
- Nenhuma junção em curso; nenhuma trava minha.

## O que falta

- Junção da documentação quando o Lume pedir (ramo `docs`, worktree `C:/context-hub-wt/docs`). Fora isso, nada:
  esperar ordem do maestro.

## Como retomar

1. Ler os arquivos acima e conferir: `git -C C:/context-hub-wt/integracao status --short` vazio e `log -1` = ca62332
   (ou o que o registro disser depois).
2. `maestri list` para ver maestro, construtores e revisor; esperar aviso.

## Como faço uma junção (resumo do `juntar-tickets.md`, com o que aprendi)

1. Parecer: a última rodada diz "passa" e o HEAD conferido é a ponta do ramo, ou depois dele só entrou
   `git merge integracao` (`git log --first-parent <HEAD do parecer>..ticket-NN`; `git show --cc --format= <merge>`
   vazio = sem resolução à mão).
2. Conflito: `git merge-tree --write-tree --name-only HEAD ticket-NN`; arquivos em comum por `comm -12`. Conflito na
   junção: `git merge --abort` e aviso ao construtor; não resolvo.
3. `git merge --no-ff ticket-NN -m "Junta ticket NN: <título>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`.
   Nunca juntar enquanto uma suíte minha roda na worktree. Depois: `maestri ask "Lume" "ticket NN juntado, <hash>"`.
4. Testes leves do ticket primeiro; a suíte só com a trava (`trava-pesada.md`, `set -o noclobber`, `trap` que apaga),
   pela `fila-pesada.md`, em segundo plano com a saída em `logs/`:
   `env -u HUB_HARNESS_REAL -u HUB_BUSCA_OHS -u HUB_GRAVAR_MEDIDAS -u HUB_LEITURA_GRANDE -u HUB_PAPEL -u HUB_MODELO_CODEX -u FREELLM_BASE_URL -u OPENAI_BASE_URL -u OPENAI_API_KEY node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"`
   (~27-33 min). Ao soltar, avisar quem o maestro mandou ("trava livre, sua vez").
5. Fork (ticket que mexe nele): junta também no `integracao` do fork e roda com TEMP longo:
   `TEMP='C:\Users\gustavo.delfino\AppData\Local\Temp' TMP=... node --import tsx --test "src/**/*.test.ts"`.
6. Harness real e Docker: não repito quando os arquivos são idênticos aos revisados (escrevo o porquê).
7. Vermelho: junção recém-nascida → `git reset --hard ORIG_HEAD` (conferir ORIG_HEAD = HEAD^1) e aviso ao dono; se
   outros ramos já contêm a junção, levar ao maestro.
8. Resolver: `Status: resolved` (sed `0,/^Status: claimed$/s//Status: resolved/`) + comentário (data, hora,
   integrador, hash, testes, ressalvas); linha no `registro-de-juncoes.md`; avisos ao maestro, ao Lume e aos
   construtores (Brasa, Vela, Trilho, Cinzel).

## Junção da documentação (Lume)

Diff só em `agents/code/docs/`; `git merge --no-ff docs -m "Junta documentação: <páginas>"`; rodar `27-pastas` e
`node agents/code/bin/verificar-frontmatter.mjs --raiz <wt> agents/code/docs` (leves); o `12-busca` não roda (desde o 41 a
busca não indexa `agents/code/**`; maestro, 21h25). Sem Fiel.

## Armadilhas

- `maestri ask` com barra invertida: `\t` vira tabulação. Caminhos sempre com `/`.
- `git rev-parse --short A B C` falha; usar sem `--short`.
- Testes de tempo (12-busca, 27-pastas) caem sob carga: suíte sempre com `--test-concurrency=1`.
- `description` de SKILL.md com `: ` sem aspas quebra o YAML e o 12-busca (lição do 16, nas regras).
- Memória baixa: perguntar ao maestro antes de rodar a suíte.
- Windows reinicia às 21h: nada pesado começa depois das 20h.
- O registro e os tickets usam a hora da máquina (-03).
- 21:20 (depois do reinício das 20:57): docs 6ª juntada (dc514db; docs b20bf5f, 11 páginas, só agents/code/docs/). Verificador 0, 27-pastas 24/24 (log logs/juncao-docs-6-27-pastas.log). Falta o 12-busca (pesado, trava): 821 MB livres, perguntei ao maestro.
- 21:25: maestro: 12-busca não roda para docs; docs 6ª registrada verde. integracao em dc514db.

## Sessão de 2026-10-17 ~23h (após reinício)

- Pedido do maestro: juntar 45 (Brasa) e depois 46 (Cinzel, volta curto); ao fim, juntar `integracao` no `main` do
  `C:/context-hub` (decisão do Gustavo, ticket 26), sem push; avisar maestro e Lume (Lume fechado; maestro religa).
- 23:03 45 juntado: 6494a38 (parecer-45-Brasa.md PASSA com 5 ressalvas). Leve 45-duas-maquinas-sem-docker 1/1.
  Aviso ao Lume caiu no shell dele (fechado): reenviar quando religado.
- 23:04 suíte com trava em segundo plano, log logs/juncao-45-suite.log. Próximo: resultado → resolver 45, registro.
- 46 chegou (Cinzel): r2 PASSA em dc4fd1a; ponta dd241ba = só merge de integracao 6494a38 (--cc vazio); merge-tree sem
  conflito. Juntar quando a suíte do 45 acabar; depois leves 46-kit-duas-maquinas + 23-kit e suíte de novo com trava.
- 23:41 suíte do 45 verde (371/356/15/0); 45 resolvido e registrado. 46 juntado: 8c01cfb. Leves do 46 rodando;
  depois a suíte com trava (log logs/juncao-46-suite.log); verde → resolver 46, registro, juntar integracao no main
  do C:/context-hub (fast-forward possível; usar --no-ff), sem push; avisar maestro, Cinzel, Brasa e Lume (reenviar o do 45).
- 2026-10-18 00:12 suíte do 46 verde (390/375/15/0); 46 resolvido. main do C:/context-hub = 7d0c25d (--no-ff de integracao 8c01cfb), sem push.
  Aviso ao Lume enviado (religado pelo maestro). Nada em curso; esperar ordem (docs do Lume com instalacao.md).
- 2026-10-18 00:28 docs 7ª juntada (7b6c406); main fe55b12 (origin/main 7d0c25d: falta o push do Gustavo). Nada em curso.

## Estado ao fechar (2026-10-18, madrugada)

- integracao (C:/context-hub-wt/integracao) = 7b6c406, limpa, verde (última suíte: 46, 390/375/15/0).
- main do C:/context-hub = fe55b12 (junção --no-ff de integracao); origin/main 7d0c25d: o push é do Gustavo.
- Tickets 45 e 46 resolvidos; docs 7ª juntada. Nenhuma trava minha, nada em curso.
- Próxima junção no main: `git log integracao..main` só mostra commits "Junta integracao no main" (normal: o main
  tem os seus merges); não usar `merge-base --is-ancestor main integracao` como trava.
- Ao voltar: ler regras, juntar-tickets, registro e esta retomada; `maestri list`; esperar ordem.

## Sessão de 2026-10-18 (tarde): junção do 49

- Pedido do maestro: juntar 49 (Brasa, ticket-49 até c3f2868; fecha o 50). Parecer VOLTA só no relatório e na ordem
  do par B; código pode juntar. 49 juntado: e82dd85. Suíte com trava em segundo plano, log logs/juncao-49-suite.log.
- Próximo: verde → resolver 49 e 50 (50 com comentário: fechado pelo c3f2868; causa certa no conserto 4 do parecer),
  registro, juntar integracao no main do C:/context-hub (--no-ff, sem push; o main tem untracked que não são meus),
  avisar maestro, Lume e construtores.
- 2026-10-18 ~15h1x PAUSA (o Gustavo fecha o note): suíte do 49 parada no meio pelo maestro (resultado não vale; log
  logs/juncao-49-suite.log incompleto). Trava solta; nenhum node da suíte vivo.
- Estado: junção do 49 até c3f2868 FEITA em integracao (e82dd85, limpa). 49 e 50 ainda não resolvidos; main do
  C:/context-hub não andou (fe55b12).
- Ao voltar: juntar o ee71863 (só o cabeçalho do teste do 49; conferir parecer/diff antes) em integracao; depois a
  suíte de novo com trava (log novo logs/juncao-49-suite-2.log); verde → resolver 49 e 50, registro, main --no-ff
  sem push, avisos. Não tocar no CLI do par A (C:/hub-par) nem no contêiner hub-banco.
