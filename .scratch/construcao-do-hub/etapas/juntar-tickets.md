# Juntar tickets em `integracao` (integrador, desde 2026-10-16)

O integrador junta em `integracao` cada ticket que passou na revisão, roda os testes e resolve o ticket. O maestro só
orquestra: passa o próximo ticket ao construtor depois do seu aviso. Regras comuns da construção:
`regras-da-construcao.md` (leia inteiras); valem aqui também.

## Quando

Um construtor avisa: "ticket NN passou na revisão, ramo ticket-NN, testes ..., relatório ...". O maestro também pode
pedir uma junção.

## Passos

1. **Confira o parecer** do revisor (`etapas/<etapa>/parecer-<construtor>.md`): a última rodada diz "passa" e o HEAD
   conferido é o do ramo `ticket-NN`, ou os commits depois dele só mexem em evidência ou relatório (confira com
   `git diff <HEAD do parecer> ticket-NN --stat`). Código mudado depois do parecer: não junte; devolva ao construtor
   para pedir nova rodada ao revisor.
2. **Junte** na worktree de junção `C:\context-hub-wt\integracao` (ramo `integracao`; nunca troque de ramo nela):
   ```
   git merge --no-ff ticket-NN -m "Junta ticket NN: <título do ticket>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
   ```
   Conflito: `git merge --abort`, nada resolvido por você; avise o construtor e o maestro com os arquivos em conflito.
3. **Rode os testes** de `integracao` inteiros: todo `*.test.mjs` de `agents/code/test/` (e de `agents/test/` enquanto
   existir), com `node --test "<padrão entre aspas>"`, e os de cada ticket juntado como o relatório dele manda.
   - Comando comum: `node --test "agents/code/test/**/*.test.mjs"`, sem variável (os de harness ficam pulados); com
     `HUB_HARNESS_REAL=1 --test-concurrency=1`, só se o ticket juntado mexe na prova 03, na guarda do 14 ou nos hooks.
   - Teste que chama harness de verdade (`codex exec`, `claude -p`, `copilot -p`), copia login ou sobe Docker: rode só
     se a árvore juntada difere, nos arquivos dele, da que o revisor testou (`git diff ticket-NN HEAD -- <pasta>`);
     se é idêntica, não rode e escreva o porquê. Docker só em `127.0.0.1`, nomes `hub-ensaio-*`, apagados ao fim.
   - Vermelho num teste que o ticket juntado não toca (a máquina está com pouca memória e a suíte inteira pesa): rode o
     arquivo que falhou sozinho três vezes e a suíte de novo com `--test-concurrency=1`. Os dois verdes: mantenha a
     junção, grave o log em `etapas/juncao-NN-suite-falha-*.log` e avise o dono do teste. Qualquer um vermelho: trate
     como teste vermelho (abaixo).
   - Teste vermelho: se o commit de junção é o seu e acabou de nascer, desfaça com `git reset --hard ORIG_HEAD`;
     avise o construtor e o maestro com a saída.
4. **Resolva o ticket**: em `issues/NN-*.md`, `Status: resolved` e um comentário (data, hora, "integrador", hash da
   junção, testes rodados e o resultado, ressalvas do parecer). Lição do relatório ou do parecer que serve a outro
   ticket: um comentário curto no ticket dono, citando a origem.
5. **Registre** uma linha em `etapas/registro-de-juncoes.md` (data, hora, ticket, hash, testes).
6. **Avise**: `maestri ask "Claude Code" "Integrador: ticket NN juntado (<hash>), testes <resultado>; ressalvas: <...>"`.
   Depois avise os outros construtores ativos (`maestri list`) que `integracao` andou para `<hash>`, numa linha.

## O fork do MCP do banco (desde 2026-10-17)

O fork mora no repositório próprio `C:\Projetos\hub-mcp-banco` (decisão do Gustavo). Ele também tem um ramo
`integracao`, criado pelo integrador a partir do `ticket-09` juntado (d2a5a40). Ticket que mexe no fork (10 em diante)
tem ramo `ticket-NN` no fork e no hub; o integrador junta os dois, cada um no seu `integracao`, com o mesmo `--no-ff`, e
roda os testes do fork além da suíte do hub, com
`node --import tsx --test "src/**/*.test.ts"` (o `npm test` do fork no Windows roda 0 testes: aspas simples no cmd;
falso verde; base do upstream: 272 passam, 1 falha). Rode com `TEMP` e `TMP` no caminho longo
(`C:/Users/gustavo.delfino/AppData/Local/Temp`): com o nome curto `GUSTAV~1.DEL` caem 20 testes de caminho. Nunca mexer em `main` do fork (é o upstream).

## Nunca

- Mexer em `main`, nos ramos `tentativa-paralela/*`, nos ramos ou worktrees dos construtores; `git push`; consertar
  código de ticket (quem conserta é o construtor); apagar worktree ou ramo (a limpeza é no fim, a pedido do maestro).
- Mais de um subagente por vez (além dos três Haiku de tarefa simples ou QA, como nas regras); nada global de verdade; `taskkill` por nome.
