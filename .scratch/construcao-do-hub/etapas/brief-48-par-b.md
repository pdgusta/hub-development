# Brief do ticket 48 (par B, lenovo-ideapad, 2026-10-24)

Para o **Malho**. O Gustavo invocou `/implement 48` em 2026-10-24. Valem todas as regras e as "Diferenças do par B"
de `etapas/brief-53-par-b.md` (hub ao vivo só leitura, par rodando intocado, sem junção nem push, retomada e 40%),
com uma diferença: **parta do `main` do hub (a9f1b4d)**, que já tem o 53 e o 54:
`git -C C:/context-hub worktree add C:/context-hub-wt/ticket-48 -b ticket-48 main`.

## O trabalho

- Ticket: `C:/Projetos/context-hub/.scratch/construcao-do-hub/issues/48-correio-entre-maestros.md`. Leia inteiro: a
  pesquisa, as três decisões do Gustavo e o **desenho aprovado** (itens 1 a 6). O desenho é o contrato; o que ele
  deixa à construção (o tipo da nota e o caminho exato, a verificação da rotina com saída vazia) você decide e
  registra no relatório, com a razão.
- Fontes primárias já baixadas (leia antes de usar): `code.claude.com/docs/en/cross-session-messaging.md` e
  `remote-control.md` (`curl -sL`; regra "doc por curl"). O `SendMessage` e o `ListAgents` são ferramentas do
  Claude Code; a skill só diz ao agente como usá-las.
- Peças do hub que você vai tocar ou ler: a vigia (`agents/skills/vigia/`, `agents/code/bin/lib/vigia.mjs`, o
  `gravarItem`/`tirarItem` de itens de outros donos; docs `componentes/vigia.md` e `vigia-nas-telas.md`), o
  catálogo de frontmatter (`agents/frontmatter/paths.yml` e os esquemas), o roteamento de skills
  (`agents/skills/routing.yml`) e o kit (`kit/par/08-harnesses.mjs`, se a skill nova precisar de junction como as
  outras 8).
- **Onde mora:** a skill em `agents/skills/correio/` (é o agente que chama); o que só a vigia ou o kit roda, em
  `agents/code/`.
- Teste que falha antes: com dois pares de ensaio, um recado gravado no arquivo de um par faz a vigia do outro
  acusar o item `correio`, e marcar o "Lido do outro" o tira. Hub de ensaio, nunca o ao vivo.

## Fora da construção (fica com o maestro)

- O preset "Maestro" com Remote Control, reabrir os maestros, o recado de teste entre as duas máquinas e qualquer
  `SendMessage` de verdade. Deixe no relatório os comandos exatos.

## Como

Igual ao 53 e ao 54: `claimed` no ticket; `tdd`; arquivo de teste sozinho a cada passo; suíte inteira uma vez no
fim; `code-review` sobre o ramo (desde `main`); relatório em `etapas/relatorio-48-correio-entre-maestros.md`;
comentário no ticket; `maestri ask "Claude Code" "48 pronto: ..."`. Mudança em contrato, skill ou AGENTS.md: com a
skill `writing-for-agents`. Caminho Windows com barra invertida em comando de shell: cuidado com o `\b` (o bash
desta ferramenta o come em `printf` e em heredoc de python); grave pelo Edit ou pelo PowerShell.
