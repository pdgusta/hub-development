# Acesso dos agentes: Copilot

Type: research
Status: resolved

## Question

Pela documentação oficial, como o GitHub Copilot carrega instruções (contrato), skills e servidores
MCP de uma pasta compartilhada no Windows, dentro e fora do Maestri? Cobrir o modo agente do Copilot no
VS Code e o Copilot CLI. Mesmo recorte de "Acesso dos agentes: pesquisa", que cobriu Claude Code, Codex
e OpenCode. Seguir o protocolo da §10.4. Nasceu em "Windows ou WSL" (Q4).

## Answer

Relatório completo: [`pesquisa-18-acesso-copilot.md`](../../../exploracao/anexos/pesquisa-18-acesso-copilot.md)
(2026-10-01, docs oficiais, repositório `github/copilot-cli`, changelogs e leitura local; nada testado).

- **Dois Copilots, uma pasta:** o harness Copilot do VS Code roda no Agent Host, com o mesmo runtime
  do Copilot CLI, e lê `~/.copilot` (`COPILOT_HOME` troca a pasta). O agente "Local" antigo lê o perfil
  do VS Code e "will be removed in a future release".
- **Contrato:** a camada global é `~/.copilot/copilot-instructions.md` e
  `~/.copilot/instructions/**/*.instructions.md`. O CLI soma `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` e
  `.github/copilot-instructions.md` da raiz git e da pasta atual, sem precedência definida. Não há
  limite de tamanho documentado.
- **Contrato fora do projeto:** `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` aceita pastas extras, mas a issue
  #3987, aberta, diz que desde a v1.0.66 o `AGENTS.md` dessa pasta não entra. Os imports `@caminho`
  existem, e a doc se contradiz sobre caminho absoluto.
- **Skills:** o CLI lê `~/.copilot/skills` e `~/.agents/skills` (a mesma pasta do Codex), não
  `~/.claude/skills`. Aceita pastas extras por `COPILOT_SKILLS_DIRS`, `skillDirectories` ou
  `copilot skill add`. Segue symlink; junction não é documentada.
- **Armadilha:** com `COPILOT_HOME` definido, o CLI deixa de ler `~/.agents/skills` (v1.0.66). A issue
  #5022 relata que o Agent Host do VS Code define essa variável.
- **MCP:** no CLI, `~/.copilot/mcp-config.json` (usuário) e `.mcp.json` ou `.github/mcp.json`
  (projeto, só em pasta confiável), com stdio, HTTP e SSE. Para compartilhar há
  `--additional-mcp-config`, plugin local (aceita o formato `.claude-plugin`) ou `COPILOT_HOME`. No VS
  Code, o `mcp.json` próprio está obsoleto, e o Agent Host lê o formato portátil. Por ora, só servidores
  locais sem autenticação.
- **Maestri:** não tem preset de Copilot, então ele entra como preset `custom` com o comando
  `copilot`. Com papel, o CLI leria o `AGENTS.md` ou `CLAUDE.md` do papel e os da raiz git, então o
  contrato do workspace não se perde se a pasta for repositório git.
- **Windows:** a config fica em `C:\Users\<user>\.copilot`. O CLI exige PowerShell 6+. A issue #5022
  relata instruções carregadas em dobro no Agent Host (maiúscula da letra do drive).
- **Neste notebook (leitura):** CLI 1.0.80 (o último é o 1.0.91). `~/.copilot` já tem instruções,
  skills e um `mcp-config.json`, e `~/.agents/skills` tem 117 skills em pastas reais.
- **Não verificado:** junction; `@` com caminho absoluto; `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` na
  1.0.91; se o Agent Host herda as variáveis `COPILOT_*` e lê `~/.agents/skills`; o Copilot CLI como
  preset `custom` com papel no Maestri.
