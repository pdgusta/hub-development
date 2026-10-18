# Relatório do ticket 24 (Cinzel): kit de par ao vivo nos três harnesses

Ramo `ticket-24` (do `ticket-23`, que passou na rodada 2 do Fiel), worktree `C:/context-hub-wt/ticket-24`. Costuras
aceitas pelo maestro: `costuras-24-Cinzel.md`.

## O teste

`agents/code/test/ponta-a-ponta/24-kit-ao-vivo.test.mjs`, atrás de `HUB_HARNESS_REAL=1` (ticket 29).

- **Montagem.** Hub de ensaio, com uma linha a mais no `AGENTS.md` ("Palavra do ensaio: `jacaranda-<sorteio>`") e uma
  skill de marca de uso geral (`marca-24`). O kit roda com `-Passos 08` numa casa de ensaio.
- **Cada harness:** abre num repositório de ensaio fora do hub (`git init`), com a casa no lugar do HOME
  (`USERPROFILE` e `HOME`). O Codex usa `CODEX_HOME=<casa>\.codex`. O login entra na casa só durante a rodada daquele
  harness.
- **Pedido:** "sem usar ferramenta nenhuma: qual é a palavra do ensaio que está escrita nas suas instruções?". As
  ferramentas ficam desligadas: no Claude, `--disallowedTools`; no Copilot, `--deny-tool` mais
  `--allow-all-mcp-server-instructions`.
- **Aceite:** a resposta traz a palavra, e nenhuma ferramenta foi usada.
- **Só registro:** os servidores `hub-*` e a skill de marca.

## Rodada 1: Claude e Copilot (2026-10-17, 09:12 a 09:13)

Trava de 09:12 até o fim; log em `logs/24-harness-1.log`; evidência em
`ponta-a-ponta/evidencia-24/` (no commit). Resultado: **2/2 PASSA**.

| Harness | Resposta | Ferramentas | Servidores do hub | Skill de marca |
| --- | --- | --- | --- | --- |
| Claude Code (`haiku`) | `jacaranda-9889c5` (a palavra) | nenhuma | `hub-busca` e `hub-banco` registrados, `failed` (servidores não sobem, como combinado) | aparece na sessão (`init`) |
| Copilot CLI (`claude-haiku-5.5`) | `jacaranda-9889c5` (a palavra) | nenhuma | `hub-banco` e `hub-busca` carregados (`session.mcp_servers_loaded`) | a saída JSON do `-p` não lista skills: não dá para saber por ela |

- **O que isso prova:**
  - aberto fora do hub, cada harness recebeu o contrato do hub de ensaio pela ligação global do kit: no Claude, o
    import em `<casa>/.claude/CLAUDE.md`; no Copilot, o link simbólico `<casa>/.copilot/copilot-instructions.md`;
  - os dois seguiram a casa como HOME, sem a variável própria (`CLAUDE_CONFIG_DIR`, `COPILOT_HOME`);
  - o Claude leu o `.claude.json` da raiz da casa (os servidores do hub aparecem nele), e a junction da skill de uso
    geral chegou ao Claude.
- **Login** (nas condições do aval):
  - Claude: `%USERPROFILE%\.claude\.credentials.json` → `<casa>\.claude`, de 09:12:39 a 09:12:52, apagado;
  - Copilot: só `lastLoggedInUser` e `loggedInUsers` → `<casa>\.copilot\config.json`, de 09:12:52 a 09:13:22,
    apagado. O token fica no cofre do Windows e não foi copiado.
  - A pasta de ensaio foi apagada (`pasta_apagada: true`).
- **Nada global:** as configurações reais conferidas por hash antes e depois saíram iguais (`settings.json`,
  `CLAUDE.md`, `config.toml`, `hooks.json`, `AGENTS.md` do Codex, `config.json`, `mcp-config.json`,
  `copilot-instructions.md` e os hooks do Copilot). Detalhe em `hashes-claude-copilot.json`.
- **Evidência sem dado da máquina:** os nomes das skills desta máquina saem trocados por `SKILL-DA-MAQUINA`, e a pasta
  do usuário por `%USERPROFILE%`. Nenhum `gsd-` nem `ask-matt` na saída.

## Rodada 2: só o Codex (2026-10-17, 17:20 a 17:21, janela quieta): PASSA

Trava de 17:21 até o fim; `HUB_HARNESS_REAL=1 HARNESSES=codex node --test --test-concurrency=1
agents/code/test/ponta-a-ponta/24-kit-ao-vivo.test.mjs` no ramo `ticket-24` a3e0360 (com a integracao f640bbd); log
`logs/24-harness-2.log` (1/1); evidência no commit 2000575 (`evidencia-24/codex/`, `hashes-codex.json`).

| Harness | Resposta | Ferramentas | Servidores do hub |
| --- | --- | --- | --- |
| Codex 0.162.1 (`gpt-6-luna`, esforço baixo, pelo `MODELO_CODEX` do 43) | `jacaranda-1b158b` (a palavra) | nenhuma | `hub-*` registrados; o transporte cai (`error sending request for url (http://127.0.0.1:3939/mcp)`): os servidores não sobem no ensaio, como combinado |

- **Modelo:** o luna bastou; nada de 6.1-sol (regra do Gustavo, 14h30).
- **O que isso prova:**
  - aberto num repositório fora do hub, o Codex respondeu a palavra que só o contrato do hub de ensaio sabe: leu o
    `AGENTS.md` global pelo link `<casa>/.codex/AGENTS.md` que o kit criou;
  - seguiu o `CODEX_HOME` da casa: o aviso do Codex cita `codex_home: ...\hub-ensaio-24-...\casa\.codex`, e os
    servidores que ele tentou abrir são os do `config.toml` que o kit gravou na casa;
  - o aviso "Refusing to create helper binaries under temporary dir" é do Codex com `CODEX_HOME` dentro do `%TEMP%`; só
    registrado, não muda a resposta.
- **Login** (nas condições do aval): `%USERPROFILE%\.codex\auth.json` → `<casa>\.codex`, de 20:20:59Z a 20:21:07Z
  (17:20 a 17:21 aqui), apagado; a pasta de ensaio foi apagada (`pasta_apagada: true`).
- **Nada global:** as 13 configurações reais conferidas por hash saíram iguais antes e depois, inclusive o
  `~/.claude.json` desta vez (`hashes-codex.json`).
- **Depois da rodada:** `23-kit.test.mjs` + `harness-real.test.mjs` no ramo: 34/34 (`logs/24-23kit-a3e0360.log`).

## Skills da máquina (2026-10-17 ~11h15, 432a927)

O teste usa o ajudante do 11 (`ponta-a-ponta/skills-da-maquina.mjs`, por estrutura). A troca antiga, no texto inteiro,
já tinha mexido na evidência da rodada 1 (Claude e Copilot): palavras comuns dentro das descrições das skills e dos
comandos da máquina (`deep-research` virou `deep-SKILL-DA-MAQUINA`). Só nas listas da máquina; a resposta e o contrato
não. Fica como está; a rodada do Codex já sai com o ajudante.
