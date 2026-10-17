# Retomada da Vela (construtora do hub)

Limpa em 2026-10-17 ~20h, a pedido do Gustavo. O histórico está nos tickets (`issues/`), nos relatórios
(`etapas/relatorio-*`) e nos pareceres (`etapas/parecer-*`).

## Estado

- **Construção fechada** pelo maestro (2026-10-17 ~20h). Nada aberto comigo; nenhuma worktree minha com mudança.
- Último ticket: **25** (prova do hub inteiro), juntado pelo Rebite em `integracao` ca62332 e resolvido (suíte 370:
  355 pass, 15 skip, 0 fail). Fases 1-7 verdes com Claude e Copilot; Codex nas fases 1 e 2. Codex nas fases 4-7 fora do
  25 por decisão do maestro (provado nos tickets 17, 18, 21, 22; está no "Para rever").

## O que ainda vale (ressalvas do 25, parecer `etapas/parecer-25-Vela.md`, rodada 2)

Não são consertos pedidos; só viram trabalho se o maestro mandar.
1. A pasta `evidencia-25/rodadas/2026-10-17-1248-claude-copilot-f1-2-3` guarda a rodada das 12:59 (fases 2 e 3); o nome
   engana.
2. O `hashes.json` reposto do Codex das 18:00 não tem `modelo`; só a rodada das 19:26 prova o `gpt-6-luna`.
3. `HARNESSES_F<n>` que não cruza com `HARNESSES` deixa a fase vazia e verde; deveria falhar.
4. Cada rodada real da fase 7 suja o `evidencia-22` (volta por `git checkout` à mão).
5. `cliente.ps1` deixa `%TEMP%/hub-ensaio-25-subir-22.log` (sem segredo). O 25-medidor falhou 1 vez em ~16 rodadas.
6. Assumidas: na fase 2 o B é conferido só no `tasks.md`; `write_note` pelos harnesses e reconexão do MCP fora.
7. Fase 7 com 835 MB livres no pico, 135 acima do corte de 700: a mais apertada; fica para a instalação conferir.

A observação do kit (par novo leva minutos para receber o hub) foi do maestro ao ticket 26.

## Como retomar

1. Reler as regras inteiras: `etapas/regras-da-construcao.md`.
2. `maestri list` (revisor Fiel, integrador Rebite, construtores Brasa, Trilho, Cinzel; documentador Lume).
3. Ficar parada até o maestro chamar (`maestri ask "Claude Code" "..."` para responder).
4. Ticket novo: `Status: claimed`, worktree `git -C C:/context-hub worktree add C:/context-hub-wt/ticket-NN -b ticket-NN
   integracao`, skill `tdd`, relatório em `etapas/relatorio-NN-*.md`, revisão do Fiel, depois o Rebite.

## Armadilhas que ainda servem

- Heredoc e `sed` no Git Bash comem `\` (e um `\r` virou CR literal): texto com barra invertida vai pelo Edit/Write.
- Arquivos do repositório voltam com CRLF; troca de várias linhas por `node -e` não casa: usar o Edit (ler antes).
- Trabalho pesado (Docker, suíte, harness real) só com a trava (`etapas/trava-pesada.md`) e a fila
  (`etapas/fila-pesada.md`); prova do 25 pelo `agents/code/test/ponta-a-ponta/25/corredor.ps1` (cria e apaga a trava;
  status em `etapas/logs/25-corredor.status`).
- `node --test` aberto de dentro de outro `node --test` precisa de `delete env.NODE_TEST_CONTEXT`, senão pula tudo e sai 0.
- Não mexer na worktree enquanto o Fiel revisa; avisar antes de commitar.
- Doc externa por `curl` (versão `.md`), nunca subagente web-fetch.
