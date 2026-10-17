# Costuras do ticket 24 (Cinzel, 2026-10-17 08:50): kit de par ao vivo nos três harnesses

Sobre o ramo `ticket-24`, que sai do `ticket-23`, ainda em revisão. Teste em
`agents/code/test/ponta-a-ponta/24-kit-ao-vivo.test.mjs`, atrás de `HUB_HARNESS_REAL=1` (ticket 29), pela fila.

## Como proponho

1. **Montagem.** Hub de ensaio (`hubDeEnsaio`), com uma linha a mais no `AGENTS.md`: "Palavra do ensaio:
   `<palavra sorteada>`". O kit roda com `-Passos 08` numa casa de ensaio. Depois entra o login de cada harness,
   pelas regras do aval.
2. **Onde o harness abre: um repositório fora do hub** (uma pasta com `git init`, ao lado). Lá, o contrato só chega
   pela ligação global do kit, e é isso que o ticket mede. Abrir na raiz do hub provaria o `AGENTS.md` do projeto,
   não o kit.
3. **Como cada harness enxerga a casa:** a casa no lugar do HOME (`USERPROFILE` e `HOME`), sem tocar na forma do kit.
   - Claude Code: a casa como HOME, então lê `<casa>/.claude/CLAUDE.md` e `<casa>/.claude.json`. Login:
     `.credentials.json` em `<casa>/.claude`.
   - Codex: `CODEX_HOME=<casa>/.codex`, porque o HOME do Windows pode não valer para ele. Login: `auth.json` lá.
   - Copilot: a casa como HOME, sem `COPILOT_HOME`; com ele, o Copilot deixaria de ler `~/.agents/skills` (18).
     Login: só `lastLoggedInUser` e `loggedInUsers` no `<casa>/.copilot/config.json`. Roda com
     `--allow-all-mcp-server-instructions`.
   - Se um harness não seguir o HOME de ensaio, dá para saber. A pergunta falha, e as pastas reais conferidas por
     hash mostram se ele gravou lá. Aí uso a variável dele (`CLAUDE_CONFIG_DIR`, `COPILOT_HOME`) e registro.
4. **O que conta como passa:** cada um responde a palavra do ensaio, uma sessão de cada. Modelos:
   - Claude: `haiku`;
   - Codex: `gpt-6-luna`, esforço baixo;
   - Copilot: `claude-haiku-5.5`.
   Ferramentas desligadas: o contrato tem de vir no prompt, sem ler arquivo.
5. **O que só registro:** se cada um cita a skill de marca (uma skill geral só do ensaio, pela junction) e se lista os
   servidores `hub-busca` e `hub-banco`. Os servidores não sobem: a chamada de verdade já foi provada no 11 e no 12.
   Não seguro o aceite nisso, porque o critério do ticket é o contrato.
6. **Nada global.** Hash das pastas reais antes e depois (`relatorioDeHashes`). Login apagado ao fim. A pasta de
   ensaio sai inteira. A evidência vai para `ponta-a-ponta/evidencia-24/`, sem a lista de skills da máquina (lição do
   11).
7. **Ordem:** Claude e Copilot pela fila agora; o Codex depois das 12h15, logo depois do Codex do 11.

## Pergunta

1. **A casa como HOME** (`USERPROFILE`), em vez das variáveis de cada harness, para provar a forma real do kit. De
   acordo? A outra saída é `CLAUDE_CONFIG_DIR`, `CODEX_HOME` e `COPILOT_HOME` desde o começo. Ela é mais garantida,
   mas não prova o `.claude.json` na raiz da casa nem o `~/.agents/skills` do Copilot.
