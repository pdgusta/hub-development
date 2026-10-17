# 08: Banco: limites e robustez

Type: task
Status: claimed
Etapa: 2 (banco)
Blocked by: 07, 06

**What to build:** O banco aguenta o uso real: exclusões pela lista do gerador, limite de 200 MiB, colisão de binário recuperável, kit idempotente, laço que religa o sincronizador, e um retrato do banco (conflito aberto, binário com ramo apagado, replicação parada) para as etapas seguintes.

**Fonte:** Bloco do Worker 4 (os itens que eram "se sobrar" voltam a ser entrega cheia); tickets 33, 47, 48. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 07 (Banco do par: dois CouchDB, LiveSync e vista `.md`), 06 (Gerador de exclusões)

- [ ] nada com ponto nem `local: true` chega ao banco, com o CLI rodando e na partida
- [ ] arquivo de 60 MiB viaja e o de 201 MiB não
- [ ] colisão de binário deixa a versão perdida num ramo recuperável
- [ ] o kit roda de novo sem mudar nada; com o CLI morto ou o banco fora na partida, o laço religa
- [ ] o retrato do banco está gravado para as etapas 3 e 6

## Comments
- 2026-10-17 03h00 (integrador, Rebite): lição do 07 (parecer do Fiel, `etapas/02-banco/parecer-Brasa.md`): as esperas fixas do teste do banco (30 s para o estado da replicação, 60 s para o controle) falham com a máquina carregada; esperar pelo estado, com folga maior, ou dizer na falha que foi tempo.
- 2026-10-17 ~03h10, Brasa: peguei (Status claimed). Worktree `C:/context-hub-wt/ticket-08`, ramo `ticket-08`, de `integracao` 763813a. Costuras propostas ao maestro (aguardo): (1) teste Docker `agents/code/test/08-banco-limites.test.ps1` pelo passo do kit, pastas e CouchDB crus (ponto e local na partida e rodando; 60/201 MiB; colisão de binário recuperada pelo cat-rev; kit de novo sem mudança); (2) laço `agents/code/kit/par/banco/laco.ps1`, uma volta por chamada, mais o XML da tarefa agendada sem registrar; (3) retrato do banco, local a decidir (proposto `agents/code/test/banco/retrato/`). Falta: tudo.
- 2026-10-17 ~03h15 (maestro, via Brasa): costuras confirmadas. (1) teste Docker `agents/code/test/08-banco-limites.test.ps1`, com esperas pelo estado e falha que diz "tempo"; piso de memória e trava no Docker. (2) laço `agents/code/kit/par/banco/laco.ps1`, uma volta por chamada; o kit só escreve o XML da tarefa agendada, nunca registra. (3) retrato em `agents/code/test/banco/retrato/` (o `execucao/` da raiz é do plano antigo).
