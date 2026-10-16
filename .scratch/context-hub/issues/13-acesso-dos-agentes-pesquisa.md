# Acesso dos agentes: pesquisa

Type: research
Status: resolved

## Question

Pela documentação oficial, como Claude Code, Codex e OpenCode, dentro e fora do Maestri, carregam
instruções (contrato), skills e servidores MCP de uma pasta compartilhada, no Windows e no WSL?
Seguir o protocolo da §10.4.

## Answer

Relatório completo: [`pesquisa-13-acesso-dos-agentes.md`](../../../exploracao/anexos/pesquisa-13-acesso-dos-agentes.md)
(2026-10-01, documentação oficial, código e leitura local; nada testado).

- **Contrato:** cada harness tem camada global por usuário. Claude Code: `@caminho` absoluto no
  `~/.claude/CLAUDE.md` (até 4 MiB; doc recomenda < 200 linhas). OpenCode v1: `instructions` no
  `opencode.json` global aceita caminho absoluto (a V2 não resolve `instructions`). Codex: sem import;
  um `~/.codex/AGENTS.md` (ou `CODEX_HOME`), teto de 32 KiB somado. O Claude Code lê `AGENTS.md` desde a
  v2.1.277, mas só sem nenhum `CLAUDE.md` na pasta ou acima.
- **Skills:** nenhuma pasta comum aos três. Codex e OpenCode leem `~/.agents/skills`; Claude Code só
  `~/.claude/skills` (o OpenCode também). Cada skill do hub precisa de duas entradas, como o vault já
  faz. Os três documentam symlink, nenhum junction; aqui o Claude Code carrega 38 skills por junction
  (observado).
- **MCP:** formato e arquivo próprios em cada um; os três aceitam stdio e HTTP. Pontos de
  compartilhamento: `--mcp-config` ou plugin via `CLAUDE_CODE_PLUGIN_DIRS` (Claude Code, leva skills e
  MCP juntos), `OPENCODE_CONFIG` (OpenCode); o Codex não documenta include.
- **Windows × WSL:** instalação no WSL usa o home Linux e não vê a config do Windows; só o Codex
  documenta compartilhar (`CODEX_HOME` em `/mnt/c/...`).
- **Maestri** (themaestri.app): abre o shell na pasta do workspace e digita o comando do preset;
  exporta `MAESTRI_*`; instala skills próprias em `~/.claude/skills` e `~/.agents/skills`; com papel,
  inicia o agente em `<projeto>/.maestri/roles/<id>/` (com `CLAUDE.md`, `AGENTS.md`, `role.json`).
  **Consequência:** com papel, o `AGENTS.md` do workspace deixa de ser lido, então o contrato do hub
  tem de entrar pela camada global de cada harness.
- **Mudanças de nome:** `sst/opencode` agora é `anomalyco/opencode`; a doc do Codex redireciona para
  `learn.chatgpt.com`.
- **Não verificado:** junction no Codex e no OpenCode; import com letra de drive no Claude Code; versão
  do OpenCode instalada; se o Claude Code procura `.mcp.json` em pastas acima.
