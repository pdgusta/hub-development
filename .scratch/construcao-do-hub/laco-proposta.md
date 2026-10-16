# O laço da construção do hub: proposta

Maestro, 2026-10-15 ~21h. Ticket 16 ("Passagem para a construção"). Pedido do Gustavo: 10 agentes Opus 5.5 alto em
paralelo, até 10 subagentes cada, tickets o menos horizontais possível, separação de papéis, sem limite de tokens, limite
de 1 hora, todos conversam, Fable 5.1 médio para tarefa muito complexa, mais 2 Prumos (Claude Opus 5.5 alto). O painel
só mostra; a execução roda sem ele.

## As três fases

1. **Spec.** Você invoca `/to-spec` na sessão do maestro. A fonte são as linhas do `map.md` ("Decisions so far"), os
   Answers dos tickets resolvidos e os comentários do ticket 16 (o que entra no kit de par e no kit de cliente). Sai
   `.scratch/construcao-do-hub/spec.md`. Os 2 Prumos revisam em paralelo: o **Prumo das decisões** confere se cada
   decisão do mapa está na spec, sem nada inventado; o **Prumo da construção** confere se cada parte pode ser
   construída e testada. Você aprova no portal.
2. **Tickets.** Você invoca `/to-tickets`. Saem **fatias verticais**: cada ticket entrega algo que funciona de ponta a
   ponta (exemplo: "uma nota gravada no par A aparece na busca do par A"), nunca uma camada solta ("instalar o
   CouchDB"). Cada ticket tem papel dono, `Blocked by`, critério de aceite verificável e cabe em 1 hora. O que mexe no
   segundo par (o notebook), em arquivo global ou pede o seu aval nasce `ready-for-human`. Os 2 Prumos revisam o
   corte; você aprova no portal. Os tickets ficam em `.scratch/construcao-do-hub/execucao/tickets/`.
3. **Execução.** Você invoca `/implement-spec`. O maestro despacha em ondas: cada ticket sem bloqueio vai para um
   construtor livre. O laço gira até não sobrar ticket que um agente possa fazer.

## Os papéis (12 recrutas Claude Opus 5.5 alto, num andar "Construção" do Maestri)

| Papel | Quantos | Faz | Não faz |
|---|---|---|---|
| Construtor | 7 | pega um ticket por vez e o entrega inteiro, com testes; abre até 10 subagentes (pesquisa, testes, partes paralelas) | integrar no ramo principal, aprovar o próprio trabalho |
| Integrador | 1 | a fila: ordem dos `Blocked by`, ramos, junção, conflitos; avisa o maestro do que destrava | construir ticket |
| Testador de aceite | 1 | roda o critério de aceite de cada ticket já junto com os outros, como quem usa | consertar (devolve ao construtor) |
| Pesquisador de fonte | 1 | confere em fonte primária (README, docs oficiais, versão) o que o construtor vai usar, antes de usar; marca "não verificado" | escrever código do hub |
| Prumo das decisões | 1 | revisa cada ticket entregue contra as decisões e o contrato do hub | escrever código |
| Prumo da construção | 1 | revisa cada ticket entregue como código: correção, testes, segurança | escrever código |

Um ticket só é feito quando passou pelos dois Prumos e pelo testador. O maestro coordena, despacha, conversa com você e
não constrói.

## Regras do laço

- **Onde se constrói:** o hub nasce em `C:\context-hub` (ticket "Windows ou WSL": NTFS em `C:\context-hub` nas duas
  máquinas). Cada construtor trabalha no seu ramo, em pasta própria (git worktree), para dez processos não pisarem um
  no outro.
- **Nada global antes do aval:** o que mexe em `~/.claude`, `~/.codex`, `~/.copilot`, hooks do usuário, serviços ou
  Tailscale é construído e testado num **HOME de ensaio** (`CODEX_HOME`, `COPILOT_HOME` e equivalentes apontando para
  uma pasta de teste). A instalação de verdade é um ticket `ready-for-human`, com cópia e hash antes.
- **1 hora por ticket:** ao bater 60 minutos, o construtor para, grava o estado em `execucao/work/<ticket>.md` e
  devolve. O maestro divide o ticket ou o dá ao Fable.
- **Fable 5.1 médio:** quando um ticket estourar a 1 hora ou for recusado duas vezes pelos Prumos, o construtor abre um
  subagente Fable 5.1 médio só para a parte difícil. O painel mostra.
- **Sem limite de tokens.** Cada agente pode abrir até 10 subagentes ao mesmo tempo.
- **Conversas:** por `maestri ask`. O maestro liga os recrutas entre si pela CLI (`maestri connect "A" "B"`), todos com
  todos, ao criá-los.
- **Registro para o painel, por mecanismo:** hooks de projeto em cada pasta de trabalho (não globais) gravam os eventos
  em `execucao/eventos/<agente>.jsonl`: início e fim de turno, subagente aberto e fechado, mensagem enviada, teste,
  commit, 1 hora. O agente não precisa lembrar de registrar. Formato: `painel/contrato.md`.
- **File-first:** todo estado vive em arquivo; um `/clear` em qualquer recruta não perde nada.

## O que fica de fora do laço

- O segundo par (o notebook): tickets `ready-for-human`, com você.
- A consulta ao TI antes do Tailscale no notebook.

## Não verificado

- Que um recruta criado pela CLI aceite `--model claude-opus-5-5 --effort high` (os parâmetros existem no `claude
  --help`); a troca do Prumo pela CLI foi barrada pelo classificador de permissões desta sessão.
- Hooks de projeto numa git worktree valerem para o Claude Code aberto nela.
- O Agent tool de um recruta aceitar 10 subagentes em paralelo e o modelo Fable com esforço médio.
