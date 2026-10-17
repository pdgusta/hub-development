# Retomada do Rebite (integrador), 2026-10-17 09h10 (antes da janela quieta)

Leia nesta ordem: `regras-da-construcao.md`, `juntar-tickets.md` (inteiros), `registro-de-juncoes.md` (o que já
entrou), `fila-pesada.md`, e esta retomada.

## Estado

- Hub: worktree de junção `C:/context-hub-wt/integracao`, ramo `integracao`, ponta e98a891, limpa.
- Fork do MCP do banco: worktree de junção `C:/Projetos/hub-mcp-banco-wt/integracao`, ramo `integracao`, ponta
  34c3e50. Tem junções (não pastas) em `node_modules` e `lib/livesync-commonlib` para a cópia principal
  `C:/Projetos/hub-mcp-banco`. `git status` nela só com `--ignore-submodules=all`. Nunca mexer em `main` do fork.
- Juntados e resolvidos: 01-10, 12 (com o Codex), 13, 14, 15 (rodada 2 com o Codex, e2b7607), 19, 20 (com o Codex),
  27-36. O 08 entrou em e98a891 (fatia 2 do Docker vira item do Gustavo).
- Leitura do Fielzinho pendente em vários; o que ele achar vira ressalva.
- Nenhuma junção em curso; nenhuma trava minha (a trava das 09h é do Trilho, Docker do 21). Construtores e maestro
  avisados de e98a891.

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

## Em espera (avisados, NÃO juntar ainda)

Ordem do maestro (09h): 16, depois 17, 18; o 11 depois do Codex (12h15); então 23 e 24. Antes de cada um, conferir que
a ponta do ramo é a do parecer (ou que depois dela só entrou evidência ou `git merge integracao`).

- 17 (Vela): passou r2 em 3e8bbc8. Só depois do 16 resolvido; a Vela junta integracao no ramo, testa sobre o
  estado.json real, rodada nova do Fiel, e me avisa de novo (ponta nova).
- 18 (Vela): passou em f36df85; leva o 17 dentro. Depois do 16 e do 17. Ainda vêm commits só de evidência (real
  Claude+Copilot; Codex depois de 12h15). Troca o núcleo do fim do 27 (PostToolUse, fragmentos novos): atenção aos
  testes do 27 e ao 23-kit.
- 23 (Cinzel): passou rodada curta em a9643c6 (antes a419182) (harness-real 7/7, 23-kit 14/14). Só com 11, 15, 17, 18, 20 e 27 resolvidos.
  Na junção, rodar de novo `agents/code/test/23-kit.test.mjs` (lê os fragmentos de 17 e 18 do repositório).
- 11 (Cinzel): espera o Codex das 12h15; ainda não avisado como passado.
- 16 (Trilho): ainda não avisado como passado.

## Em curso (10:20, depois do reinício do Maestri)

- 16 juntado: integracao fce0529 (ticket-16 0332466 = parecer r2 passa; idêntico ao ramo). 16-vigia 19/19 (log
  etapas/logs/juncao-16-vigia.log). Suíte com a trava desde 10:19 em segundo plano, log etapas/logs/juncao-16-suite.log.
  Falta: resolver o 16 (ressalva do laco/exclusoes no parecer; Fielzinho lê depois), registro, avisos; depois o 17 (Vela
  junta integracao no ramo, testa sobre o estado.json real, rodada do Fiel, me avisa). 23 segura até 11, 16, 17 e 18.
- Docker do 16 não repetido: idêntico ao revisado (8ª rodada do Trilho vale; r2 só mexeu em filtro de `descartados()`).
- Maestro: ao soltar a trava da suíte do 16, avisar o Trilho (Docker do 21, 4ª rodada).
- 10:30: 22 avisado pela Brasa (63cbfd5 = parecer r2 PASSA; contém fce0529; sem conflito; sem ramo no fork). Juntar
  depois da suíte do 16 (nunca durante); testes leves: 22-kit-cliente, 22-proxy-sem-docker (harness-real pulado sem
  variável); Docker e harness não repetir (idênticos). Depois suíte com a trava. Pendente após resolver: Codex como
  cliente depois de 12h15 (commit só de evidência, rodada curta do Fiel) e Fielzinho. Conflito add/add do
  kit/par/env/10.env.modelo com o 21: quem for juntado por segundo faz `git merge integracao` no ramo; eu não resolvo.
  Atenção: ramo do 22 contém fce0529; se a suíte do 16 ficar vermelha e eu desfizer, avisar Brasa.
- 10:46: suíte do 16 VERMELHA (229/219/2 falhas no 12-busca: agents/skills/vigia/SKILL.md com YAML inválido, ': ' no
  description). Desfeito: integracao voltou a e98a891. Log etapas/juncao-16-suite-falha-12.log. Trilho avisado (conserto,
  nova rodada do Fiel, ponta nova). Brasa avisada; tirou o 16 do 22.
- 10:55: 22 juntado: integracao 4a47576 (ticket-22 5abe359; difere da revisada 63cbfd5 só nos arquivos do 16).
  22-kit-cliente + 22-proxy-sem-docker 4/4 (log etapas/logs/juncao-22-leves.log). Falta: suíte com a trava (Trilho com
  ela desde 10:46; pedi ao maestro ficar logo depois), resolver o 22 com pendência do Codex (12h15) e Fielzinho, registro,
  avisos. Construtores ainda não avisados de 4a47576.
- Na fila: "janela quieta feita: 22, fatia 2 do 08 e 25 fases 1-3 verdes" — a fatia 2 do 08 passou; se vier commit só
  de evidência do 08, juntar e comentar no ticket 08 (tira a ressalva 1).
- Maestro: sou o 1c da fila, logo depois do Trilho (Docker do 21). Lição do SKILL.md já nas regras.
- 11h: 37 avisado pelo Cinzel (rodada curta passa, ponta f8e12e3, antes 4b695d5; 114/114; feito sobre ticket-18 31afe63): juntar só depois do 18. Mexe em nucleo.mjs, fim-da-resposta.mjs, nota.mjs e nos três fragmentos do fim. Na junção, conferir que a base 18 juntada é a mesma (31afe63 ou a ponta do 18 que entrar) e rodar 14, 18, 27, 37.
- 11:02: trava minha; suíte do 22 em segundo plano (log etapas/logs/juncao-22-suite.log). 16 consertado pelo Trilho (6a0ab17), vai ao Fiel; esperar o passa. Ao soltar: avisar o próximo da fila (ver fila-pesada.md).
- 11:45: 16 passou rodada curta (ponta 6a0ab17; só SKILL.md mudou desde 0332466). Sem conflito com 4a47576, nenhum arquivo em comum. Juntar depois da suíte do 22; rodar 16-vigia e 12-busca (sem trava) e a suíte com a trava (fila item 1: suíte do 16, depois a do 17). Docker não repetir (8ª rodada, idêntico).
- 12:05: 21 avisado pelo Trilho (6b6c65e = parecer r2 + conferência da junção com o 22, PASSA; contém 4a47576 e 6a0ab17;
  10.env.modelo com as duas metades; sem conflito com 4a47576). Contém também fce0529 (minha junção desfeita do 16):
  conteúdo superado pelo 6a0ab17, só polui o histórico; avisar o maestro. Plano: depois da suíte do 22 verde, juntar
  16 (6a0ab17) e 21 (6b6c65e), testes leves (16-vigia, 12-busca, 21-*, 22-kit-cliente, 22-proxy-sem-docker) e UMA
  suíte para os dois, com a trava. Docker do 21 não repetir (4ª verde).
- 11:25: 22 RESOLVIDO (4a47576, 215/206/9). 16 (30b735f) e 21 (fdd3760) juntados; árvore = ticket-21. Suíte dos dois com a trava em segundo plano (log etapas/logs/juncao-16-21-suite.log). Construtores ainda não avisados de 4a47576/fdd3760.
- Maestro: depois da minha suíte, trava livre até 12h15 (aí Codex: Cinzel, Vela, Brasa). Ao resolver o 16, avisar a Vela (ela traz o 16 para o 17 e pede rodada nova ao Fiel).
- Maestro (troca): ao soltar a trava da suíte do 16+21, avisar o Trilho (pesados do 38, ~15 min).
- 22: ponta c1f0fa3 (97693bb, modelo do Codex no 22-cliente, + fdd3760 juntado; difere de integracao só nessa linha). Juntar com a evidência do Codex depois de 12h15 (rodada curta do Fiel); comentar no ticket 22.
- 11:42: 16 e 21 RESOLVIDOS; maestro, Vela (traz 16 ao 17), Brasa, Cinzel avisados; Trilho avisado da trava (38). Nenhuma junção em curso.
- 11:50: Cinzel juntou fdd3760 nos ramos: 23 e05b367, 37 17b1f69, 11 359c8e3 (falta Codex), 24 a52b073 (falta Codex). Na junção de cada um: conferir que depois da ponta do parecer só entrou git merge integracao (git log --first-parent).
- 11:58: 17 juntado (e7203b4; ticket-17 b6ace6b = parecer, árvore igual). Suíte com a trava em segundo plano (log etapas/logs/juncao-17-suite.log). Ao soltar, avisar o Cinzel (Codex do 11). Harness real do 17 não repetir (idêntico, evidência dos três no ramo).
