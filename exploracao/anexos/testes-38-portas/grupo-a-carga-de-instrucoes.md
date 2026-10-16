# Testes 38, grupo A: carga de instruções (2026-10-10)

Ticket: "Testes das portas de entrada" (`.scratch/context-hub/issues/38-testes-das-portas-de-entrada.md`).

## Método

Hub de teste numa pasta temporária, sem `.git`, sem nenhum `CLAUDE.md`/`AGENTS.md` nas pastas acima.
Cada `AGENTS.md` (ou `CLAUDE.md`) carrega um marcador aleatório; a sessão é perguntada, **sem
ferramentas** (Read, Grep, Glob, Bash e afins negadas no Claude Code; instrução de não ler nem rodar
nada no Codex e no Copilot), quais marcadores estão nas instruções carregadas. Um marcador aleatório
não pode ser adivinhado, então aparecer na resposta é prova de carga.

```
hub/AGENTS.md                                   ROOT-7Q2
hub/clients/AGENTS.md                           CLI-3K9
hub/clients/voegol/AGENTS.md                    VOE-5P1
hub/clients/voegol/app/AGENTS.md                APP-2M8
hub/clients/voegol/app/.maestri/roles/r1/       CLAUDE.md e AGENTS.md: ROLE-6T3 (simula o papel do Maestri)
hub/initiatives/x/AGENTS.md                     INI-8W4
```

Versões: Claude Code 2.1.296 (modelo `claude-haiku-5-5`), codex-cli 0.161.0, GitHub Copilot CLI 1.0.94.

## Resultados

| # | Harness | Onde abriu | Condição | Carregou |
|---|---|---|---|---|
| T1 | Claude Code | raiz | padrão | ROOT |
| T2 | Claude Code | `clients/voegol/app` | padrão | ROOT, CLI, VOE, APP |
| T5 | Claude Code | raiz | depois de `Read` em `initiatives/x/nota.md` | ROOT, INI |
| T6 | Claude Code | raiz | `CLAUDE.md` na pasta **acima** do hub (PAI-9Z1) | só PAI: **nenhum `AGENTS.md`** |
| T3 | Claude Code | pasta do papel (simulada) | padrão | só ROLE |
| T4 | Claude Code | pasta do papel (simulada) | `--settings` com `instructionFiles: claude-md-and-agents-md` | ROOT, CLI, VOE, APP, ROLE |
| T9 | Claude Code | **papel real do Maestri** neste repositório | padrão | `AGENTS.md` do repositório **não** carregou |
| T10 | Claude Code | **papel real do Maestri** neste repositório | `--settings` com `claude-md-and-agents-md` | `AGENTS.md` do repositório **carregou** |
| T7 | Claude Code | fora do hub | `@<caminho absoluto C:/...>` no `~/.claude/CLAUDE.md` | o arquivo importado carregou (GLB-1H5) |
| T8 | Claude Code | fora do hub | skill do hub ligada em `~/.claude/skills/` por **junction** do Windows | a skill foi descoberta |
| C1 | Codex | raiz | padrão | ROOT |
| C2 | Codex | `clients/voegol/app` | padrão (sem `.git`) | só APP |
| C3 | Codex | `clients/voegol/app` | `-c project_root_markers=["HUB.md"]`, com `HUB.md` na raiz | ROOT, CLI, VOE, APP |
| P1 | Copilot CLI | raiz | padrão | ROOT |
| P2 | Copilot CLI | `clients/voegol/app` | padrão (sem `.git`) | APP, VOE (sem ROOT e sem CLI) |
| P3 | Copilot CLI | `clients/voegol/app` | `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` = raiz | APP, VOE (sem efeito) |
| P4 | Copilot CLI | `clients/voegol/app` | `.git` na raiz do hub | ROOT, CLI, VOE, APP |

O `~/.claude/CLAUDE.md` foi restaurado depois do T7 (conferido byte a byte), a junction do T8 foi
removida, e o `.git` do P4 foi apagado.

## O que isso decide

- **Raiz:** os três harnesses leem o `AGENTS.md` da raiz quando a sessão abre nela.
- **Subpasta:** o Claude Code lê toda a cadeia sozinho. O Codex precisa de um marcador de raiz
  (`project_root_markers`) e o Copilot CLI precisa de `.git` na raiz do hub; sem isso, nenhum dos dois
  chega ao `AGENTS.md` da raiz. O comportamento do Copilot sem `.git` (P2) não segue a doc lida.
- **Um `CLAUDE.md` em qualquer pasta acima do hub desliga todos os `AGENTS.md`** (T6). O hub não pode
  morar abaixo de uma pasta com `CLAUDE.md`.
- **Papel do Maestri:** confirmado, real e simulado. O `AGENTS.md` do hub só chega com
  `claude-md-and-agents-md` no `~/.claude/settings.json` (ou num `--settings`).
- **Repositório fora do hub:** import absoluto no `CLAUDE.md` global funciona; skill por junction
  funciona no Claude Code.
- **Subpasta funda:** o `AGENTS.md` de uma subpasta entra quando o agente lê um arquivo ali (T5).

## Não testado neste grupo

Import `@` no `AGENTS.md` do Codex; `--add-dir` com `AGENTS.md` (Codex); se o Maestri regenera os
arquivos do papel a cada início; VS Code com Copilot.
