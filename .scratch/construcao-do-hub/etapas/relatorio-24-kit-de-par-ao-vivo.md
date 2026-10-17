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

## Pendente

- **Rodada 2: Codex**, depois das 12h15, logo depois do Codex do 11:
  `HUB_HARNESS_REAL=1 HARNESSES=codex node --test --test-concurrency=1 agents/code/test/ponta-a-ponta/24-kit-ao-vivo.test.mjs`.
  O que medir: se o Codex segue o `CODEX_HOME` da casa e lê o link `<casa>/.codex/AGENTS.md`.
