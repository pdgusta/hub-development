# Relatório do ticket 19: roteamento de skills (Vela)

## Estado

- 2026-10-17: ticket pego; worktree `C:/context-hub-wt/ticket-19` (de `integracao` 0a8e17f; junta d5e4e16 depois).
- Primeiro commit do ramo (d57e36b), pedido do maestro: os testes do 27 apagam as próprias pastas temporárias no fim,
  mesmo falhando (`after` + `rmSync` com novas tentativas, como o Trilho no 04, 05 e 14). Provado com `TEMP` isolado:
  zero pastas sobrando nos dois. Depois, apagadas 25 pastas `%TEMP%\hub-ensaio-*` com mais de 2 horas (21 do `-02-`,
  1 `revisao-04`, 2 `revisao-05`, 1 `revisao-instalador-03`), nenhuma falha; as 937 mais novas ficaram.

## Decisões do maestro (2026-10-17, respostas às perguntas da Vela)

1. A skill do FreeLLMAPI se chama `freellmapi`. O teste usa uma skill de ensaio com esse nome no hub de ensaio (a skill
   de verdade está fora do escopo).
2. `armis-docx` entra na tabela com o nome; o verificador da tabela avisa "skill ausente em agents/skills/" sem recusar.
3. Registro de uso: máquina = `HUB_PAR_ID`; workspace = a pasta da sessão relativa ao hub (fora do hub, o caminho
   absoluto); uma linha de tabela por uso; no Claude Code pelo mod. Codex e Copilot: conferir na doc oficial (curl) se há
   evento de uso de skill; o que não for verificado fica marcado "não verificado".
4. Injeção: Claude Code pelo contexto adicional; Codex pelo `UserPromptSubmit` (testar ao vivo); Copilot pela regra no
   contrato (texto entregue à faixa 1 neste relatório), depois de conferir e citar a doc sobre a saída descartada do
   `userPromptSubmitted`. A extensão `onUserPromptSubmitted` fica anotada como possibilidade para o kit (23).
5. O verificador do fim registra se a skill indicada rodou, sem obrigar, e aponta a linha da tabela: entra no 19, pelo
   hook de fim do 27 (`agents/code/hooks/fim-da-resposta/`), sem bloquear a resposta.
6. Registro do verificador do fim (decisão do maestro, 2026-10-17): uma tabela só em `agents/maestro/uso/<máquina>.md`,
   colunas `data | evento | skill | linha da tabela | rodou | workspace | máquina` (evento: uso ou indicação; rodou:
   sim, não, não verificado). É o arquivo que o spec dá ao hook de uso, fora da guarda do acervo, e replica.

## Docs conferidas (curl, 2026-10-17)

- **Copilot CLI**, "GitHub Copilot hooks reference" (`docs.github.com/api/article/body?pathname=/en/copilot/reference/hooks-configuration`):
  na tabela de eventos, `userPromptSubmitted`: "Optional—`modifiedPrompt` is honored only by SDK programmatic hooks."; na
  nota da seção: "`modifiedPrompt` is only honored by SDK programmatic hooks. Command and HTTP config-file
  `userPromptSubmitted` hooks have their output dropped, including `modifiedPrompt`." Logo, o hook de arquivo não injeta
  nada: Copilot pela regra no contrato. A extensão `onUserPromptSubmitted` (SDK) fica anotada como possibilidade para o
  kit (23). Nenhum evento de uso de skill na referência de hooks; `preToolUse`/`postToolUse` casam por `toolName`, e a
  doc de skills ("Adding agent skills for GitHub Copilot CLI") não nomeia a ferramenta que invoca a skill: **uso de skill
  no Copilot, não verificado**.
- **Codex**, `developers.openai.com/codex/hooks.md`: `UserPromptSubmit`: "Plain text on `stdout` is added as extra
  developer context." e, em JSON, `hookSpecificOutput.additionalContext`: "That `additionalContext` text is added as
  extra developer context." Logo, o Codex injeta pelo hook de entrada (a provar ao vivo). Nenhum evento de skill; a
  tabela "Tool coverage" lista shell, `apply_patch`, MCP e "Other local function tools": **uso de skill no Codex, não
  verificado** (a skill é lida como arquivo; não há gancho próprio).

## Texto da regra no contrato, para a faixa 1 (Copilot CLI, onde o hook de entrada não injeta)

> **Roteamento de skills (Copilot CLI).** O hook de entrada do hub não chega a você neste harness. Antes de começar um
> pedido, leia `agents/skills/routing.yml`: se uma linha casa com o pedido (uma das `palavras` começa uma palavra do
> pedido; um caminho citado cai no `caminho`; o nome do seu papel contém o `papel`), use as `skills` daquela linha
> nesse pedido, a menos que o pedido já cite outra skill.

Onde vai: no `AGENTS.md` da raiz, na parte que vale para o Copilot (a faixa 1 decide o lugar). A extensão
`onUserPromptSubmitted` do SDK do Copilot (vista na bancada de acesso) fica como possibilidade para o kit (ticket 23).

## O que foi construído (ramo `ticket-19`, ponta 52c6328)

- **Tabela** `agents/skills/routing.yml` e **esquema** `agents/skills/routing.schema.yml` (JSON Schema em YAML, no
  subconjunto dos esquemas do hub; `validar` do `lib/frontmatter.mjs` passou a ser exportado e é reusado). Cada linha:
  `id` (o registro aponta por ele), `camada` (geral ou papel), gatilhos `palavras` / `caminho` / `papel` (com mais de
  um, todos precisam casar) e `skills`. Regras além do subconjunto: ao menos um gatilho, `papel` só na camada papel, id
  único. Primeiras linhas: `pesquisa-pelo-freellmapi` (palavras `pesquis`, `research`, `investig`, `levantament` →
  `freellmapi`), `documento-armis` (→ `armis-docx`) e as quatro do retrato da frente da cidade, pelos papéis "Tech lead",
  "UX revisor", "UI engineer" e "QA tester" (nomes das skills lidos das pastas dos recrutas em
  `C:\Projetos\equipe-design\*\.maestri\roles\*\.claude\skills\`, só leitura).
- `agents/code/bin/verificar-roteamento.mjs [--raiz]`: `falta:` recusa (saída 1); skill ausente em `agents/skills/` é
  `aviso:` (decisão 2).
- **Hook de entrada** `agents/code/hooks/roteamento/entrada.mjs <claude|codex|copilot> [--hub]`, sem IA e sem rede
  (só lê a tabela e o `role.json`): casa palavras (começo de palavra, sem acento e sem caixa), caminhos citados no
  pedido (glob) e o papel (nome no `role.json` de `.maestri/roles/<id>/`, onde o Maestri abre o recruta). Linha cuja
  skill o pedido já cita não é injetada (a descrição resolve). Claude Code e Codex: `hookSpecificOutput.additionalContext`
  com "use a skill `X` neste pedido (linha <id>)". Copilot: não escreve nada (doc) e só anota a indicação. Fora do hub,
  sai na hora. Fragmentos em `hooks/roteamento/fragmentos/` (Claude `UserPromptSubmit` de settings, Codex
  `UserPromptSubmit`, Copilot `userPromptSubmitted`).
- **Registro de uso** `agents/maestro/uso/<HUB_PAR_ID>.md` (sem `HUB_PAR_ID`, o nome do computador), criado com os
  campos comuns e a tabela da decisão 6. `hooks/roteamento/uso.mjs` grava a linha `uso` (só skill do acervo: pasta em
  `agents/skills/<nome>/SKILL.md`); no Claude Code, o mod `agents/code/mods/roteamento/` chama no `skill.prompt`
  (`claude plugin validate` passa; o mesmo aviso do 27 sobre Claude Code gerenciado por organização). Age em qualquer
  pasta (exceção do spec). Workspace: pasta da sessão relativa ao hub; fora, o caminho absoluto.
- **Fim da resposta** (decisão 5): o `fim-da-resposta.mjs` do 27 chama `fecharTurno` quando a resposta solta (num
  `try` próprio; nunca bloqueia): cada linha indicada no turno vira `indicação` com `rodou` = `sim`/`não` no Claude Code
  e `não verificado` no Codex e no Copilot. Estado da sessão em `<hub>/.local/roteamento/<sessao>.json`.
- **Regra do contrato para o Copilot**: texto acima, para a faixa 1.

## Testes

- `node --test agents/code/test/19-roteamento.test.mjs`: **16/16** (tabela 2; entrada 7: pesquisa nos dois que
  injetam, pedido que cita a skill ou não casa, papel, caminho, Copilot sem saída, fora do hub; registro e fim 7: uso
  vira linha e passa no verificador de frontmatter, skill fora do acervo não, "sim", "não", "não verificado" no Codex e
  no Copilot, turno sem indicação).
- Suíte inteira sem harness, `node --test "agents/code/test/**/*.test.mjs"` em 52c6328: **128 passam, 0 falham, 5
  pulados** (os de harness real, ticket 29).
- **Ponta a ponta com harness real** (`HUB_HARNESS_REAL=1 node --test agents/code/test/ponta-a-ponta/19-roteamento.test.mjs`;
  evidência sem login em `evidencia-19/`), 2026-10-17:
  - Claude Code (haiku, settings de ensaio com o hook de entrada, mods `roteamento` e `fim-da-resposta` por
    `--plugin-dir`, skill de ensaio `freellmapi` ligada por junction em `CLAUDE_CONFIG_DIR/skills`): com
    `--include-hook-events`, a saída traz "use a skill `freellmapi` neste pedido (linha pesquisa-pelo-freellmapi)"; a
    skill disparou (resposta `ROTEADO-PELO-FREELLMAPI`); o registro tem `uso | freellmapi | pesquisa-pelo-freellmapi |
    sim` e `indicação | freellmapi | pesquisa-pelo-freellmapi | sim`. Verde (01:18:41 → 01:18:56 UTC).
  - Codex (`gpt-6-luna` baixo): a resposta diz "Pela instrução do hub..." e cita `freellmapi` (a injeção chegou);
    registro `indicação | ... | não verificado`. Verde (01:16:41 → 01:17:03).
  - Copilot CLI (`claude-haiku-5.5`): sem injeção (como a doc diz); registro `indicação | ... | não verificado`. Verde
    (01:17:07 → 01:17:57).
- Login no ensaio (rodada `2026-10-16-login-dos-harnesses-no-ensaio`): Claude `.credentials.json` em `CLAUDE_CONFIG_DIR`,
  Codex `auth.json` em `CODEX_HOME`, Copilot só `lastLoggedInUser` e `loggedInUsers`, em `%TEMP%\hub-ensaio-19-*`; as
  três pastas apagadas ao fim da própria rodada (`apagado: true`). Arquivos reais conferidos por hash antes e depois,
  nas duas rodadas: **nenhum mudou** (`hashes-claude.json`, `hashes-codex-copilot.json`).

## O que vai doer / não verificado

- Uso de skill e "rodou" no Codex e no Copilot: **não verificado** (sem evento nas docs; ver "Docs conferidas").
- No Copilot, a indicação depende da regra no contrato (faixa 1) ou da extensão do SDK (kit, 23).
- "Sem rede" do hook de entrada: garantido pelo código (só lê arquivos), não por teste que corte a rede.
- Papel: só quando o Maestri abre o terminal em `.maestri/roles/<id>/` com `role.json`; outro jeito de abrir não acha
  o papel.
- A tabela é lida a cada pedido (sem cache); pequena hoje.
- Gatilho `palavras` por começo de palavra pode casar demais ("pesquis" casa qualquer pedido de pesquisa); o maestro
  ajusta pelo registro (decisão do 15, rodada 3).
- O mod de uso e o do fim são dois `--plugin-dir`; o kit (23) os junta.
