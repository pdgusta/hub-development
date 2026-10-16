# 06: Guardas de gravação no disco

Type: task
Status: claimed
Dono: Worker 6
Com: Prumo 2
Blocked by: None (can start immediately)

Faixa 6 da spec (`../spec.md`, seção "Faixas", Worker 6). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

**Guardas de gravação e leitura no disco** (faixa 6 do corte; Answers dos tickets 11 e 14, "Imposição" do 12): um hook "antes da ferramenta" em `hooks/06-guardas/` (Node ≥ 22, `.mjs`, como a faixa 9), com um adaptador por harness e a mesma decisão: (a) **recusa a regravação inteira de arquivo que já existe** no hub (Write do Claude Code; `Add File` sobre existente, `Delete`+`Add` e `Update` que troca tudo no `apply_patch` do Codex; `create` do Copilot) com a mensagem "use a troca de trecho ou o `write_note` do MCP do banco com a versão lida"; deixa passar troca de trecho e arquivo novo; (b) **recusa nota fora do esquema**: monta o conteúdo proposto (arquivo novo, ou o atual com a troca aplicada) e chama o verificador da faixa 1; (c) **aviso de leitura, sem recusa** (ticket 11, rodadas 3 e 4): guarda por sessão o que a busca devolveu (`PostToolUse` da ferramenta de busca) e o que foi aberto; avisa "leia o trecho que a busca apontou" ou "busque antes", uma vez por arquivo por sessão; (d) **sai na hora fora do hub** (caminho fora de `HUB_ROOT`). Comando de shell fica só no contrato, como decidido

## Critério de aceite (de ponta a ponta)

- [ ] testes automáticos (`node --test`) com as entradas reais gravadas na bancada do ticket 11 (`hooks.jsonl` do Codex e os casos do Claude e do Copilot) mais casos novos: os quatro casos da bancada passam nos três adaptadores; nota sem `status` é recusada; leitura grande fora da busca avisa uma vez. De ponta a ponta, com login de ensaio (pergunta do Worker 2): `claude -p`, `codex exec` e `copilot -p` num hub de ensaio, com o fragmento instalado pelo kit no HOME de ensaio, recusam o Write sobre existente e deixam passar o Edit e o arquivo novo; sem login, a mesma prova roda no escopo de projeto, como a bancada fez

## Como segue sem esperar

o verificador (faixa 1): chama `agents/bin/verificar-frontmatter` pela interface do Worker 1, com o dublê que sai 0 até ela entregar; a busca (faixa 3): só o nome do servidor (`busca`, do `.env` do kit) e a forma da resposta, com uma resposta gravada como dublê; o kit (faixa 8): entrega `fragmento.json` no formato do Worker 8 no minuto 15, sem esperar o kit; o MCP do banco (faixa 5): só o nome `write_note` na mensagem de recusa

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments
