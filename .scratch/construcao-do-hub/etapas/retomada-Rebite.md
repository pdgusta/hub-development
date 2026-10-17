# Retomada do Rebite (integrador), 2026-10-17 07h30

Leia nesta ordem: `regras-da-construcao.md`, `juntar-tickets.md` (inteiros), `registro-de-juncoes.md` (o que já
entrou), `fila-pesada.md`, e esta retomada.

## Estado

- Hub: worktree de junção `C:/context-hub-wt/integracao`, ramo `integracao`, ponta 9cc878b, limpa.
- Fork do MCP do banco: worktree de junção `C:/Projetos/hub-mcp-banco-wt/integracao`, ramo `integracao`, ponta
  34c3e50. Tem junções (não pastas) em `node_modules` e `lib/livesync-commonlib` para a cópia principal
  `C:/Projetos/hub-mcp-banco`. `git status` nela só com `--ignore-submodules=all`. Nunca mexer em `main` do fork.
- Juntados e resolvidos: 01-07, 09, 10, 12 (com o Codex), 13, 14, 15, 19, 20 (com o Codex), 27-36.
- Pendências de evidência depois de resolvidos: Codex do 15 (o Trilho rodou às 07:26; vem como commit só de
  evidência, junto e comento no ticket). Leitura do Fielzinho pendente em vários; o que ele achar vira ressalva.
- Nenhuma junção em curso; nenhuma trava minha.

## Como faço uma junção (resumo do que o juntar-tickets manda, com o que aprendi)

1. Parecer: a última rodada diz "passa" e o HEAD conferido é a ponta do ramo, ou depois dele só entrou
   `git merge integracao` (conferir com `git log --first-parent <HEAD do parecer>..ticket-NN`).
2. Arquivos em comum com `integracao` desde a base: `git diff --name-only $(git merge-base HEAD ticket-NN) ...` nos
   dois lados e `comm -12`; `git merge-tree --write-tree --name-only HEAD ticket-NN` para conflito.
3. `git merge --no-ff ticket-NN -m "Junta ticket NN: <título>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`.
   Nunca juntar enquanto uma suíte minha roda na worktree.
4. Suíte: só com a trava (`etapas/trava-pesada.md`, criar com `set -o noclobber`, apagar no fim por `trap`), na ordem
   de `fila-pesada.md` (tirar-se da fila ao pegar; ao soltar, avisar quem o maestro mandou, por `maestri ask`):
   `env -u HUB_HARNESS_REAL -u HUB_BUSCA_OHS -u HUB_GRAVAR_MEDIDAS -u HUB_LEITURA_GRANDE -u HUB_PAPEL -u FREELLM_BASE_URL -u OPENAI_BASE_URL -u OPENAI_API_KEY node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"`
   (~15 min; em segundo plano, saída inteira em arquivo). Último verde: 210, 202 passam, 8 pulados.
5. Fork (ticket que mexe nele): junta também no `integracao` do fork e roda, com TEMP longo,
   `TEMP='C:\Users\gustavo.delfino\AppData\Local\Temp' TMP=... node --import tsx --test "src/**/*.test.ts"`.
   Base: 273, 272 passam, 1 falha (`vault-local.test.ts`, separador `\`). O `npm test` roda 0 testes no Windows.
6. Harness real e Docker: não repito quando os arquivos são idênticos aos revisados (escrevo o porquê).
7. Vermelho em teste que o ticket não toca: arquivo sozinho 3 vezes e suíte com `--test-concurrency=1`; os dois
   verdes, mantenho e gravo `etapas/juncao-NN-suite-falha-*.log` e aviso o dono; senão desfaço.
8. Resolver: `Status: resolved` + comentário (data, hora, integrador, hash, testes, ressalvas); lições em comentário
   no ticket dono; linha no registro; `maestri ask "Claude Code"`; avisar construtores (Brasa, Vela, Trilho, Cinzel).

## Armadilhas

- `maestri ask` com barra invertida: `\t` vira tabulação. Caminhos sempre com `/`.
- `maestri ask` dentro de laço de fundo: o destinatário programado não muda se o maestro trocar a ordem; avisar antes
  quem não vale.
- Testes de tempo (12-busca, 27-pastas) caem sob carga: por isso a suíte é com `--test-concurrency=1`.
- O registro e os tickets usam a hora da máquina (-03).

## Em curso (07:35)

- Ticket 15 rodada 2 juntado: integracao e2b7607 (ticket-15 em 3d34bd1, parecer passa). 15-leitura 9/9. Falta: suíte
  do hub com a trava (estou no item 6 da fila; maestro aprovou), depois comentário no ticket 15 (já resolved; comentar a
  rodada 2), linha no registro, aviso ao maestro e aos construtores. Nota do hífen do Codex já está nas regras e nos
  tickets 11 e 23 (maestro).
- 07:45: ticket 08 avisado pela Brasa (ponta 514db7a = parecer; PASSA com ressalvas, fatia 2 vira item do Gustavo).
  Sem conflito com e2b7607, nenhum arquivo em comum, sem ramo no fork. Juntar depois que a suíte do 15 acabar; então
  rodar `pwsh -File agents/code/test/banco/kit-sem-docker.ps1` (leve) e a suíte de novo com a trava; Docker não repito
  (arquivos idênticos aos revisados). Ressalvas do fechamento do parecer vão no comentário do ticket.
- 07:50: ticket 17 avisado pela Vela (3e8bbc8, passa r2). NÃO juntar: mandato do maestro, só depois do 16 resolvido;
  aí a Vela junta integracao no ramo, testa sobre o estado.json real, rodada nova do Fiel, e me avisa de novo.
