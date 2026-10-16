# Guarda do acervo: mods e hooks, pesquisa

Type: research
Status: resolved

## Question

O que um "mod" do Claude Code (e os hooks de que ele depende) consegue fazer como guarda do acervo
do maestro, no uso e na alteração de uma peça? Pela fonte primária: que eventos ele intercepta (por
exemplo, gravar numa pasta do acervo, carregar uma skill), se pode bloquear, avisar, injetar contexto
ou forçar o agente a disparar um subagente com outro modelo antes de seguir; onde mora e como se
instala em cada par; e se Codex e Copilot (CLI e VS Code) têm mecanismo equivalente, para um maestro
rodando neles não passar sem guarda. Inclui o exemplo do Gustavo: um maestro em Opus quer alterar uma
peça; a guarda o obriga a disparar um subagente em Sonnet 5.5 que lista os workspaces que usam a peça
ou detecta se a mudança já roda em algum workspace sem ter virado global. Sem inferência: o que a
fonte não disser fica "não verificado"; o que só um teste resolve, "precisa de teste". Pedido do
Gustavo em 2026-10-12 (resposta à R42 de "Maestri: padrão e liberdade").

## Answer

Relatório completo: [pesquisa-44-guarda-do-acervo.md](../../../exploracao/anexos/pesquisa-44-guarda-do-acervo.md).

- **Mod** é um plugin do Claude Code com funções em JS/TS que rodam dentro dele. Pode desenhar painel e faixa,
  criar comando, e segurar, reescrever ou recusar chamadas de ferramenta, prompts e skills. Exige 2.1.287 ou
  mais nova; a API ainda é "early access".
- **Guarda na alteração:** pega `Edit`/`Write` numa pasta e pode recusar, pedir aval ao Gustavo (`$.ui.ask`) ou
  mandar um aviso para o modelo. O hook de settings faz o mesmo em JSON (`PreToolUse` com `deny`/`ask`), só
  que o filtro por caminho é "best-effort".
- **Guarda no uso:** o mod vê toda skill carregada (`skill.prompt`, por `/nome`, pela ferramenta Skill ou num
  subagente). Os hooks de settings precisam de dois ganchos (`PreToolUse` em `Skill` e `UserPromptExpansion`).
- **Outro modelo, obrigatório:** o hook de settings do tipo `agent` (experimental) aceita `"model"` e é o harness
  que o roda antes da ferramenta, então o Opus não tem como pular. O mod impõe o modelo de qualquer subagente
  (`agent.spawn`) e pode recusar a edição até existir o relatório. Só o texto da recusa, sozinho, apenas instrui.
- **Limite do mod:** cada hook tem 10 s de tempo próprio. Esperar o aval ou chamar um modelo não conta; esperar
  a resposta de um subagente conta. Daí o desenho "recusa, roda o verificador, libera com relatório e aval".
- **Onde instalar:** escopo do usuário (plugin do hub como marketplace local, ou pasta em `~/.claude/skills`).
  Assim vale dentro de um papel do Maestri; posta só na raiz do workspace, a guarda não alcança o papel.
- **Codex:** tem hooks (`PreToolUse` em `apply_patch`, `deny`), mas não tem `ask` em hook nem hooks
  `prompt`/`agent`. A própria doc diz que é "guardrail", não barreira completa.
- **Copilot CLI:** `preToolUse` com `allow`/`deny`/`ask` e regra `--deny-tool='write(PATH)'`, sem hook que chame
  modelo. No VS Code, os hooks estão em Preview e o comportamento muda conforme o harness escolhido.
- **Quem usa a peça:** o Maestri não tem comando que liste. Nos arquivos dele, cada terminal guarda
  `assignedRoleId`, `command` e a pasta. Uso de skill o Maestri não registra; seria preciso um hook de uso
  gravando no hub.
- **Precisa de teste:** junction (a doc fala de symlink), regra pelos dois caminhos no Windows, `$.ui.ask` num
  terminal do Maestri sem ninguém olhando, e o tempo de um hook `agent` em Sonnet.
