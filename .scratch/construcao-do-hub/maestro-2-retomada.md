# Retomada do Amigo do Maestro

Leia primeiro `maestro-2.md` (o papel). Estado em 2026-10-15 ~21h35 (relógio da máquina):

## Frente do painel
- Tela e servidor existem (`painel/LEIA.md`); UI engineer ainda em retoques. Servidor 8771 estava desligado.
- Despachado (batch ~21h33): Tech lead ajusta contrato para ler tickets de `.scratch/construcao-do-hub/issues/`
  (convenção `docs/agents/issue-tracker.md`); QA testa já e deixa 8771 de pé com a fixture ao vivo, relatório em
  `painel/qa/`; UX faz o parecer em `painel/portas/ux-revisor.md`. Todos respondem por ask back.
- Tech lead ~21h40: contrato ajustado para issues/ (servidor --tickets; fixture igual). Faltam QA e UX.
- Quando abrir: avisar o Claude Code para cadastrar a carta que aponta para `painel/abrir.html`.
- Designer: de prontidão; só age se o Gustavo aprovar a carta `amostra-da-cidade` (ticket 56) → troca do
  `.scratch/context-hub/system-design.html` pela amostra.

## Rodada Ralph
- Volta 1 terminou (12 linhas no `voltas.md`). `PROMPT.md` ganhou a seção "Da volta 2 em diante: a spec".
- Volta 2 DISPARADA ~21h40 (última; 3 min por recruta). Depois: /to-tickets (Claude Code) e execução.
  Máximo 2 voltas: depois da 2, parar.

## Execução
- Eu coordeno Worker 6 a 10 e o Prumo 2; o Claude Code, Worker 1 a 5 e o Prumo.
- ~21h47: volta 2 terminou (não há volta 3). Execução despachada: Worker 6-10 (ticket NN = N; 11 do Worker 8 depois do 08),
  ordem em `execucao/ordem.md`; Prumo 2 revisa e me avisa "aprovado: faixa-NN". **Eu faço o merge** de cada faixa
  aprovada em `integracao` (C:\context-hub), testes de novo depois.
