# Parecer 24 (Cinzel): segunda leitura

## Rodada curta: evidência do Codex (2026-10-17)

Leitor: 2ª leitura independente do Fiel. Não li o `parecer-24-Cinzel.md`.
Ramo `ticket-24`, ponta 2000575 (evidência sobre a3e0360, merge da `integracao` f640bbd).
Worktree `C:/context-hub-wt/ticket-24`.

**Veredito: PASSA.** Nenhum conserto.

### O que conferi

1. **Modelo pela constante.** `agents/code/test/ponta-a-ponta/24-kit-ao-vivo.test.mjs:21` importa
   `MODELO_CODEX`; `:111` usa `-m MODELO_CODEX`. A constante: `agents/code/test/harness-real.mjs:9`. O comando da
   rodada no relatório (`relatorio-24-kit-de-par-ao-vivo.md:50`) não põe `HUB_MODELO_CODEX`.
   `git grep "HUB_MODELO_CODEX|gpt-6" ticket-24 -- agents`: nenhum teste com harness tem modelo à mão (só docs,
   a bancada do 14 e os presets do Maestri).
2. **Login copiado e apagado.** `evidencia-24/hashes-codex.json`, `usos`: copiado 20:20:59.836Z, apagado
   20:21:07.645Z, `apagado: true`; `pasta_apagada: true`. Bate com o relatório.
3. **Hashes.** As 13 configs reais iguais antes e depois, inclusive `.claude.json` (cc573a…). Bate com
   `relatorio-24:68`.
4. **Sem token nem caminho do usuário.** Os dois `grep` (tokens; `gustavo|delfino|GUSTAV~1|C:/Users|C:\Users`) em
   `evidencia-24/codex` e `hashes-codex.json`: nada. O `erros.txt` traz `%USERPROFILE%`, já trocado.
5. **Ramo contém a integracao.** `git merge-base --is-ancestor integracao ticket-24` → ok.
   `git show --stat 2000575`: só os 4 arquivos de evidência do Codex.
6. **A evidência sustenta o relatório e o critério** (ticket: `codex exec` responde o que só o contrato de
   ensaio sabe; costura: `CODEX_HOME` no Codex, aberto fora do hub).
   - A palavra é aleatória (`24-kit-ao-vivo.test.mjs:58`) e só vai no `AGENTS.md` do hub de ensaio (`:69`). O
     Codex abre em `FORA`, repositório git próprio fora do hub (`:75-78`, `:105`). O pedido proíbe ferramenta, e o
     teste exige `ferramentas: []` (`:174`). `lido.json`: resposta `jacaranda-1b158b` = `palavra`, ferramentas
     vazias. Só a ligação global do kit leva a palavra ao prompt.
   - `CODEX_HOME` seguido: `erros.txt:1` cita `codex_home: ...\hub-ensaio-24-lbeUfV\casa\.codex`; os erros de
     transporte vão a `127.0.0.1:3939/mcp`, a URL que o teste deu ao kit (`:80`). Servidores só registrados, como
     combinado no ticket (08:43).
   - Log `etapas/logs/24-harness-2.log`: 1 pass, 0 fail. Fila: Codex do 22 soltou a trava 17:19:20; o do 24 rodou
     17:20-17:21; o 25 começou 17:22:42. Sem sobreposição.
7. **Junção.** O ramo já contém a `integracao` f640bbd; diff do ticket inteiro: 12 arquivos, só adições. Nada a
   quebrar pela evidência.

Testes leves (TEMP/TMP = `C:/Users/gustavo.delfino/AppData/Local/Temp`, sem `HUB_*`):
`node --test agents/code/test/23-kit.test.mjs agents/code/test/harness-real.test.mjs` → 34 testes, 34 pass,
0 fail. `git status` limpo depois.

### Ressalvas

1. O modelo e a versão (`gpt-6-luna`, Codex 0.162.1) não aparecem na evidência; o `codex exec --json` não os
   registra. A prova é o código e o comando da rodada. Para o radar: gravar `MODELO_CODEX` no `lido.json`.
2. `relatorio-24:50` diz "Trava de 17:21 até o fim", mas o login foi copiado às 17:20:59. Diferença de
   redação; a fila mostra a ordem certa.
3. O aviso "Refusing to create helper binaries under temporary dir" vem do `CODEX_HOME` no `%TEMP%`. Já
   registrado no relatório; não muda a resposta.
