# Retomada do Fiel (revisor, Claude Opus 5.5 médio) — 2026-10-17 ~20h

## Estado atual
- **Construção fechada** (maestro, 2026-10-17 ~20h: 25 resolvido). Nada em curso, nada pendente meu.
- Sem trava, Docker, worktree, ensaio ou sonda minha de pé.
- **Fielzinho fora.** A 2ª leitura é sempre um subagente meu Opus 5.5 (um por vez), em worktree destacada própria
  quando o construtor vai mexer na dele; parecer em `parecer-<NN>-<construtor>-segunda-leitura.md`; ele não lê o meu.
- Codex só para testes, `gpt-6-luna` pela constante `MODELO_CODEX` (`agents/code/test/harness-real.mjs`).

## Como retomar
1. Ler inteiros `regras-da-construcao.md` e `revisao-em-dupla.md`; o fim de `estado-revisor.md`; este arquivo.
   Caminhos relativos a `C:/Projetos/context-hub/.scratch/construcao-do-hub/etapas/`.
2. `maestri list`. Esperar pedido novo do maestro ("Claude Code") ou de um construtor.
3. Num pedido: conferir o ramo (contém `integracao`?), rodar os testes do ticket, os vizinhos e o
   `harness-real.test.mjs` (detector de modelo à mão e de harness sem variável); conferir cada evidência contra o
   ticket, o spec e o relatório; procurar o que quebra ao juntar. 2ª leitura por subagente Opus; acordo; parecer em
   `parecer-<NN>-<construtor>.md` (veredito, consertos numerados com evidência, ressalvas); responder só ao construtor
   (`maestri ask`, caminhos com `/`). Teto: duas voltas; na terceira, passa com ressalvas.
4. Estado em `estado-revisor.md` a cada passo.

## Conferências que valem sempre
- Evidência de harness real: o harness rodou de fato (TAP com `# pass` por harness e `# skipped 0`; `usos` não vazio),
  login copiado e apagado, hashes reais antes = depois (só `~/.claude.json` muda pelas sessões abertas), sem token
  (`ghu_|sk-|refresh_token|access_token|Bearer|eyJ`).
- `node --test` filho dentro de teste: tem de tirar o `NODE_TEST_CONTEXT`; com ele herdado, sai 0 sem rodar nada.
- Falha intermitente: repetir 3x (junto e sozinho) antes de cobrar.
- Testes com `TEMP`/`TMP` = `C:/Users/gustavo.delfino/AppData/Local/Temp` (caminho longo); sondas em
  `%TEMP%\hub-ensaio-<NN>-fiel-*`, apagadas no fim.
- Pesado (Docker, suíte inteira, harness real): `trava-pesada.md` e `fila-pesada.md`. Nada global de verdade.
- `maestri ask` a recruta ocupado pode não entrar: conferir com `maestri check` e reenviar com ask novo.
- Contexto acima de 40%: no ponto seguro, atualizar esta retomada e responder "Fiel: salvo para limpar".
