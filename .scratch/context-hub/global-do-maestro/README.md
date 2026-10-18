# Configuração global do maestro (para reproduzir noutra máquina)

Inventário feito pelo maestro do par A em 2026-10-17 ~23h40, lendo `~/.claude/` desta máquina (só leitura). Esta pasta
traz cópias do que foi criado aqui; o resto se instala da fonte. **Toda mudança no global real da outra máquina é com o
Gustavo vendo** (regra da frente: nada global sem o aval dele). Faça com `-WhatIf`/olhando antes, e guarde uma cópia do
que estava.

> Ordem com o hub: o kit do hub (passo 08, ticket 26) mexe no mesmo global (contrato, skills de uso geral, MCP, hooks) e
> **tira o GSD**. Ele preserva o que não é dele. Faça os passos abaixo antes ou depois do kit, tanto faz; só não
> instale o GSD na outra máquina (ele sai na instalação do hub).

## 1. Claude Code: `~/.claude/settings.json`

Junte ao `settings.json` de lá as chaves de `settings.trecho.json` (sem apagar o que já houver):
- `model: claude-opus-5-5`, `effortLevel: xhigh`, e em `modelSettings.claude-opus-5-5`: `effortLevel: high` e
  **`autoCompactWindow: 600000`** (o auto-compact em 600k que o Gustavo usa; o maestro não deve passar de 700k);
- `permissions.defaultMode: auto` (modo automático);
- `enabledPlugins: superpowers@claude-plugins-official` (instalar o plugin: `/plugin` no Claude Code);
- `env.CLAUDE_CODE_PLUGIN_DIRS`: as duas pastas de mods (seção 3), **com o caminho real** da máquina (o
  `%USERPROFILE%` do trecho não é expandido pelo Claude Code: troque por `C:\Users\<usuário>`);
- `skillOverrides`: quais skills ficam desligadas (as do GSD foram tiradas do trecho).

## 2. `~/.claude/CLAUDE.md` (global)

Cópia em `CLAUDE.md` desta pasta. Hoje só tem a seção do **graphify** (o gatilho `/graphify`). Junte ao de lá. O kit do
hub acrescenta a linha `@<hub>/AGENTS.md` nesse arquivo e mantém o resto.

## 3. Mods do Claude Code (criados nesta frente)

Copie `mods/contexto-agentes/` e `mods/guarda-de-recrutas/` para `~/.claude/mods/` e aponte o
`CLAUDE_CODE_PLUGIN_DIRS` para as duas (seção 1). Reinicie o Claude Code.
- **contexto-agentes**: lê o `maestri list` e o `maestri check` de cada recruta e mostra ao maestro o contexto (%) de cada
  um (testes em `hooks/parse.test.ts`).
- **guarda-de-recrutas**: barra `maestri role edit/write/assign`, `recruit --replace` e `dismiss` quando o recruta está
  ocupado ou sem handoff; exige `# risco-avaliado: ...` no fim do comando. Regras em `regras-do-maestro.md`.

## 4. Skills

- **Matt Pocock** (o fluxo da frente: `wayfinder`, `to-spec`, `to-tickets`, `implement-spec`, `implement`, `tdd`,
  `research`, `prototype`, `grilling`, `domain-modeling`, `diagnosing-bugs`, `matt-code-review`, `handoff`,
  `writing-for-agents` e as outras; 37 no total): `npx skills add mattpocock/skills -g -a claude-code` (CLI
  `vercel-labs/skills`, `-g` = escopo do usuário; README do `vercel-labs/skills`). Aqui elas moram em
  `~/.agents/skills/` com links em `~/.claude/skills/`, e o registro em `~/.agents/.skill-lock.json`.
- **find-skills**: `npx skills add vercel-labs/skills -g -a claude-code` (não verificado o nome exato da skill no
  pacote; confira com `npx skills list`).
- **Maestri** (`maestri`, `maestri-chat`, `maestri-manager`, `maestri-portal`, `maestri-routines`, `maestri-workspace`): o
  app do Maestri instala e atualiza sozinho ao abrir.
- **Criadas aqui**: `skills/graphify/` e `skills/video-generator/` desta pasta → `~/.claude/skills/`. O
  `video-generator` usa o FreeLLMAPI e o Gemini TTS (memórias `freellmapi-tts-e-transcricao` e
  `gemini-tts-interactions-api`; a chave `GEMINI_API_KEY` é variável de ambiente da máquina, **não está aqui**).

## 5. Subagente

`agents/opus-medium.md` → `~/.claude/agents/` (o trabalhador Opus em esforço médio que o maestro usa para tarefa
fechada com briefing).

## 6. Deste projeto (`C:\Projetos\context-hub\.claude\settings.local.json`, fora do git)

Cópia em `settings.local.do-projeto.json`: a regra que deixa o maestro fazer push **só deste repositório**
(`Bash(git -C C:/Projetos/context-hub push:*)`). Grave igual no `.claude/settings.local.json` do clone de lá (ou
`/permissions` no Claude Code).

## 7. Memória do maestro

Ver `../onboarding-maestro.md`, seção 0: copiar `../memorias-do-maestro/` para
`~/.claude/projects/C--Projetos-context-hub/memory/`.

## 8. O que NÃO levar

O GSD (`~/.claude/gsd-*`, `hooks/gsd-*`, skills e agentes `gsd-*`, a `statusLine` do GSD): sai na instalação do hub.
Nada de `history.jsonl`, `sessions/`, `projects/` (fora a memória), `cache/`, logins.
