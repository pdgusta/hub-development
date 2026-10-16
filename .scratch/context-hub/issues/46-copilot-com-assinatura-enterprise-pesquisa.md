# Copilot com assinatura Enterprise: pesquisa

Type: research
Status: resolved

## Question

O Gustavo usa o Copilot (CLI e VS Code) pela assinatura GitHub Enterprise da empresa. Pela fonte
primária: que instruções a organização ou a empresa podem impor ao Copilot (instruções personalizadas
da organização, do repositório, políticas, MCP permitido, modelos permitidos), se elas chegam ao Copilot
CLI e ao do VS Code junto com as do usuário (`~/.copilot/copilot-instructions.md`, `AGENTS.md`), em que
ordem e com que precedência, e se alguma política pode bloquear o que o hub decidiu (arquivo global
ligado ao contrato, skills em `~/.agents/skills`, MCP do hub, hooks). Sem inferência: o que a fonte não
disser fica "não verificado". Pedido do Gustavo em 2026-10-12 (resposta à R59 de "Maestri: padrão e
liberdade").

## Answer

Pesquisa concluída em 2026-10-12, só com fonte primária (docs do GitHub e do VS Code, changelog do Copilot CLI,
ajuda local do CLI 1.0.96). Nada foi testado. Relatório completo, com citações, contradições entre as docs,
"não verificado" e "precisa de teste":
[`pesquisa-46-copilot-enterprise.md`](../../../exploracao/anexos/pesquisa-46-copilot-enterprise.md).

- **Instruções da organização** existem (texto escrito pelo dono da organização no GitHub, só em Business ou
  Enterprise). Pela doc do GitHub, valem só no github.com e **não chegam ao Copilot CLI**. A doc do VS Code diz
  que chegam ao VS Code (configuração ligada por padrão). As duas docs se contradizem; precisa de teste.
- **Ordem:** só o github.com tem ordem (pessoal > repositório > organização, e todas vão juntas). O CLI e o
  VS Code somam tudo, sem regra de quem vence. O contrato do hub nunca é substituído; no máximo ganha texto a mais.
- **A empresa controla o resto por "managed settings"** (um arquivo que vem do GitHub, do registro do Windows ou
  de uma pasta). Ele não trata de instruções nem de skills, mas trata de MCP, permissões, sandbox, plugins e modelo.
- **Maior risco ao desenho: o MCP do hub.** Uma lista de servidores permitidos bloquearia o MCP do hub se ele não
  estivesse nela. Para entrar, o comando teria de ser idêntico e sem variáveis.
- **Risco no VS Code:** uma política de máquina (`ChatStrictPluginOnlyCustomization`) bloqueia de uma vez instruções,
  skills e MCP avulsos do usuário. A saída seria entregar o hub como plugin. Há também políticas de "só hooks da
  empresa", no CLI e no VS Code.
- Agentes e skills da organização chegam ao CLI com a menor prioridade: os do hub, de mesmo nome, vencem.
- **Nesta máquina não há política de máquina** (registro e pastas de política vazios). Há um cache de configurações
  vindas do servidor, ilegível; não se sabe se ele traz regras. O teste 42 já mostrou o contrato e a skill chegando.
- **Para ver sem ser admin:** no CLI, `/env`, `/instructions`, `/mcp`, `/model` e `/settings`; no VS Code, o comando
  **Developer: Policy Diagnostics**; no GitHub, o `managed-settings.json` do repositório `.github-private` da empresa,
  se estiver visível.

Este ticket não é uma decisão do mapa e não foi registrado em "Decisions so far".
