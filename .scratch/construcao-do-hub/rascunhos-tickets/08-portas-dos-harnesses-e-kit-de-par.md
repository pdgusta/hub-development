# Portas dos harnesses e kit de par

Type: task
Status: ready-for-agent
Dono: Worker 8
Com: Prumo 2
Blocked by:

Faixa 8 da spec (`../spec.md`, seção "Faixas", Worker 8). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

Portas dos harnesses e kit de par (faixa 8 do corte; tickets 14, 42, 13, 18, 15 e comentários do 16): `kit/par/instalar.ps1` idempotente com `-WhatIf`, cópia e hash antes de tocar, e desfazer. Confere: sem `CLAUDE.md` no hub nem acima, modo de desenvolvedor, Node e Python. Liga: contrato por link simbólico (`~/.codex/AGENTS.md`, `~/.copilot/copilot-instructions.md`) e import no `~/.claude/CLAUDE.md`; skills por junction (`~/.claude/skills`, `~/.agents/skills`); MCP de busca e de banco nos três harnesses (127.0.0.1, token de variável de ambiente, `default_tools_approval_mode="approve"` no Codex); hooks no escopo do usuário juntando os fragmentos das outras faixas (aprovados por hash em `hooks.state` no Codex); Codex `danger-full-access` com `notify`; tira o GSD do escopo global com cópia

## Critério de aceite (de ponta a ponta)

o kit roda duas vezes num HOME de ensaio (a segunda não muda nada) e desfaz sem sobra; teste automático da forma: cada link aponta para o `AGENTS.md` do hub de ensaio, cada junction para `agents/skills/`, cada config tem as duas linhas de MCP e os hooks juntados; com login de ensaio (pergunta do Worker 2), `claude -p`, `codex exec` e `copilot -p` respondem uma pergunta que só o contrato de ensaio sabe

## Como segue sem esperar

o `AGENTS.md` (faixa 1) e as skills (faixa 9): usa os do hub de ensaio, com um contrato e uma skill de marca; os MCP (faixas 3 e 5): só a URL e o token, lidos do `.env`, sem esperar o servidor; os hooks e o mod (faixas 2, 6, 7, 9): junta o que estiver em `hooks/<faixa>/` no formato combinado; o que chegar depois entra numa segunda passada do kit, sem refazer nada

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments
