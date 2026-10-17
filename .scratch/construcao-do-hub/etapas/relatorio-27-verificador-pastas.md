# Relatório do ticket 27: o verificador cuida das pastas (Vela)

## Estado

- 2026-10-17: ticket pego; worktree `C:/context-hub-wt/ticket-27` (de `integracao` 8b9beef). Lendo as fontes.
- 2026-10-17: perguntas de fatos ao maestro (par_id, 'parecidas', formato da lista, contagem de 10, quais notas no fim); desenho: núcleo verificar-fim + adaptadores (mod Claude Code, Stop Codex, agentStop Copilot) a partir da bancada de acesso e da prova 03.

## Decisões técnicas do maestro (2026-10-17, resposta às perguntas da Vela)

1. `par_id` desta máquina: variável de ambiente `HUB_PAR_ID`, gravada pelo kit (no ensaio, um nome inventado; os nomes
   reais das máquinas seguem em aberto no spec). Sem ela, o verificador não reescreve e devolve a falta.
2. "Três notas parecidas em `other/`": pelo `why_other`, no hub inteiro (o catálogo de blocos é um só); só aviso.
3. Lista do `index.md` com `summary: auto`: entre `<!-- lista:inicio -->` e `<!-- lista:fim -->`, adotando na primeira
   passada as linhas `- \`x\`: ...` existentes. Descrição: a existente fica; nota `.md` nova entra com o `title`; arquivo
   sem texto entra sem descrição e vira falta ("descreva x"); anexo com texto irmão não ganha linha, só o irmão.
4. "Chega a 10": entradas diretas da pasta (arquivos e subpastas), sem o que tem ponto e sem o próprio `index.md`. "A
   busca não lê": arquivo que não é `.md` e não tem texto irmão.
5. Quando soltar o agente no fim da resposta: foi ao Gustavo (rodada "Fim da resposta: quando soltar o agente"; o spec diz
   que a resposta não termina enquanto houver falta). Provisório: devolve uma vez; na segunda parada seguida, solta e
   registra a falta. Isolado num ponto só do código.
5. **Decidido pelo Gustavo (rodada "Fim da resposta: quando soltar o agente", opção B):** o fim da resposta devolve até
   três vezes seguidas; na quarta parada ainda com falta, solta e registra a falta no `estado.json` da vigia (para
   aparecer no início da próxima sessão e na tela de estado). Substitui o provisório.
- 2026-10-17: retomada gravada em `etapas/retomada-Vela.md` antes do /clear (commit 286236e, 8/8).
6. **Decisão técnica do maestro (2026-10-17):** `agents/frontmatter/**` entra como `tipo: null` no `paths.yml` (oficina,
   como `agents/code/` e `agents/skills/`): sem cartão da pasta, sem pedir descrição dos 30 esquemas. Só essa linha do
   catálogo do 05 mudou. Commit 33194a1; 50/50 (27, gerador, 05 e 04).

## O que foi construído (ramo `ticket-27`)

- **Links `par://`** (5d50370) e **cartão da pasta** (286236e, 33194a1): ver as decisões acima. `agents/code/bin/verificar-pastas.mjs [--raiz <hub>] [--corrigir] <alvos>`, com `lib/pastas.mjs` e `lib/locais.mjs` (o gerador do 06 importa `pastasLocais` daqui).
- **Aviso de `other/`** (efcd0a5): `gruposDeOther` em `lib/pastas.mjs`. Duas notas de `other/` são parecidas quando o `why_other` divide mais da metade das palavras de quatro letras ou mais (sem acento) da mais curta; parecidas encadeadas formam grupo; três ou mais dão um aviso só, que cita três e pede bloco novo em `agents/blocks.md`. Passada única no hub inteiro, qualquer que seja o alvo. Só aviso: não muda a saída.
- **Fim da resposta** (cdcb683 e o commit seguinte): `agents/code/hooks/fim-da-resposta/`.
  - `nucleo.mjs`: `marcar` guarda a hora do começo do turno e zera a conta; `fim` passa o que foi gravado depois da marca (fora do que tem ponto) pelo `verificar-frontmatter --corrigir` e pelo `verificar-pastas --corrigir`, e fica só com as faltas e recusas desses arquivos e dos `index.md` das pastas deles. Sem falta, solta. Com falta, devolve até `DEVOLUCOES_SEGUIDAS = 3` vezes (o ponto único da regra B do Gustavo); na quarta parada, solta e grava o item `fim-da-resposta` (nível `informa`, as faltas, a hora) no `<hub>/.local/vigia/estado.json`, por troca atômica, sem apagar os itens que já estavam; o topo fica o pior. Conta por sessão em `<hub>/.local/fim-da-resposta/<sessao>.json`; registro de cada chamada em `registro.jsonl` ao lado.
  - `fim-da-resposta.mjs <claude|codex|copilot> <marca|fim> [--hub <raiz>]`: lê o evento do harness; devolve com `{"decision":"block","reason":...}` (a mesma forma no Codex e no Copilot; o mod a traduz); fora do hub sai na hora; erro solta e conta no stderr.
  - `fragmentos/codex.json` (`UserPromptSubmit` marca, `Stop` fim) e `fragmentos/copilot.json` (`userPromptSubmitted` marca, `agentStop` fim), com `{{DIR}}` e `{{HUB}}` como os do 14; o kit (23) os junta.
  - `agents/code/mods/fim-da-resposta/` (Claude Code): `turn.start` do laço principal com texto não vazio chama a marca; `classic.Stop` chama o fim e devolve `{ block }`. Acha o script em `<HUB_ROOT>/agents/code/hooks/fim-da-resposta/` (senão `C:/context-hub`). `claude plugin validate` passa.
- **Achado do Copilot CLI (1.0.98):** o `reason` do block volta como prompt novo e dispara `userPromptSubmitted` de novo. Sem cuidado, isso zeraria a conta e moveria a marca, e a falta sumiria calada se o agente não a corrigisse. Conserto: a marca cujo `prompt` é a última devolução é continuação (não marca); o registro diz `continuacao: true`. Testado no núcleo e confirmado na prova real.

## Testes

- `node --test agents/code/test/27-pastas.test.mjs`: 11/11 (links 3, cartão 6, `other/` 2).
- `node --test agents/code/test/27-fim-da-resposta.test.mjs`: 8/8 (Codex e Copilot: três devoluções e a quarta solta para a vigia, e a conta zera no turno seguinte; sem falta solta; continuação do Copilot; falta de nota antiga não prende; fora do hub; estado da vigia guarda os itens e o topo pior).
- Todas as suítes sem harness no ramo, em 8d8f1b9 (com `integracao` 8d1d785 junta): 04 11/11, 05 19/19, 05-nova-iniciativa 4/4, 14 37/37, 27-fim 8/8, 27-pastas 11/11, gerador 7/7: **97/97**.
- **Ponta a ponta com os três harnesses reais** (`agents/code/test/ponta-a-ponta/27-fim-da-resposta.test.mjs`; evidência sem login em `evidencia-27/`): o agente cria uma nota com link para dentro de `.secrets/`; o fim devolve; o agente corrige ("O acesso está em leia-me.txt."); o fim solta "sem falta". Rodada de 2026-10-17 00:15–00:17 UTC: Claude Code (mod por `--plugin-dir`, haiku), Codex (`gpt-6-luna` baixo, `danger-full-access`), Copilot CLI (`claude-haiku-5.5`): os três verdes, uma devolução cada; no Copilot, a marca depois da devolução veio como continuação.

## Uso do login no ensaio (rodada 2026-10-16-login-dos-harnesses-no-ensaio)

- Copiado para `%TEMP%\hub-ensaio-27-*`: Claude `.credentials.json` em `CLAUDE_CONFIG_DIR`; Codex `auth.json` em `CODEX_HOME`; Copilot só `lastLoggedInUser` e `loggedInUsers` (token no cofre, não copiado). Cada pasta apagada ao fim da sua rodada (horários em `evidencia-27/hashes-*.json`, `apagado: true` nas três).
- Hashes (16 primeiros) das pastas reais, antes e depois da rodada dos três: `.claude/.credentials.json` 13644f92d00a3ae9 igual; `.codex/auth.json` 9e42496b5bd73e15 igual; `.claude/settings.json` 411d8d3b13290a5c igual; `.codex/hooks.json` d822fa388c1d2f07 igual; `.copilot/config.json` 283253d40ec4a047 igual; `.copilot/hooks/gsd-session.json` 3382597f61e3a559 igual; `.copilot/hooks/tokenjuice-cli.json` c9d58a20aed33c56 igual; **`.codex/config.toml` a6cae9fa9397b2b3 → 368753447a994364, mudou às 00:15:51 UTC**, durante a rodada do Claude (o Codex de ensaio só começou às 00:16:28, com `CODEX_HOME` de ensaio). Há sessões do Codex de verdade abertas desde 19:34 (os recrutas), com o `CODEX_HOME` real, e o Codex regrava o próprio `config.toml`; o arquivo não traz nada de `hub-ensaio`. Causa provável: essas sessões, não o ensaio. O `after` do teste acusou a mudança (falhou por isso; os três testes de harness passaram).
- Repetição só do Codex (`HARNESSES=codex`, 00:18:17 → 00:18:36 UTC, pasta apagada): verde, e os oito arquivos reais com o mesmo hash antes e depois (`config.toml` 368753447a994364 nos dois). Evidência em `evidencia-27/hashes-codex.json`; a dos três em `hashes-claude-codex-copilot.json`.

## O que vai doer

- O `estado.json` é da vigia (ticket da faixa 7), e ela o regrava inteiro a cada passada: o item `fim-da-resposta` pode ser apagado na passada seguinte. A vigia precisa preservar itens de outros donos (ou ler `.local/fim-da-resposta/`).
- Pasta local nova com o CLI rodando (ver o 06): o link para ela só vira `par://` depois de o `index.md` dela dizer `local: true`.
- `classic.Stop` de plugin instalado não roda onde uma organização gerencia o Claude Code (aviso do `claude plugin validate`): lá, o mod precisa estar listado nas configurações gerenciadas, ou o Claude Code usa um hook `Stop` em `settings.json` com o mesmo script.
- O fim olha o hub inteiro por `mtime` a cada parada: num hub grande, custa uma varredura por parada.
- O aviso de link corrigido sem falta não chega ao agente (só sai quando há devolução); fica no registro.
- `mod` sem `*.test.ts` (`claude plugin test`): a prova dele é a ponta a ponta real.
- **Deslize:** para ler a doc do `agentStop` (docs.github.com/en/copilot/reference/hooks-configuration), usei um subagente de busca na web, contra a regra "sem subagentes". Não mexeu em arquivo; o resultado (formato de entrada e saída, corte do CLI em 8 blocks seguidos) foi conferido na prova real.
