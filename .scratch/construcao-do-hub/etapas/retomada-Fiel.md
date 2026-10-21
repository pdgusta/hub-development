# Retomada do Fiel (revisor, Claude Opus 5.5 médio) — 2026-10-18 (pausa)

## Estado atual
- **49 (Brasa):** r1 (até c3f2868) VOLTA em acordo, só relatório/receita do par B; parecer `parecer-49-Brasa.md`,
  2ª leitura `parecer-49-Brasa-segunda-leitura.md`. Brasa e maestro avisados. r2 (ee71863) recebida: 6 consertos no
  relatório; 2ª leitura Sonnet PASSA c/ ressalvas (`parecer-49-Brasa-segunda-leitura-r2.md`: bloco 1 grava autocrlf
  global; throw do bloco depois da espera; §2 "não verificado" na lista da doc). **Veredito r2 dispensado** pelo maestro. **Na volta:** leitura curta de
  `C:/Projetos/context-hub/.scratch/context-hub/instalacao-par-b.md` contra a seção final do relatório do 49
  (receita do par B). Até lá, parado.
- Sonda do passo 3 terminou: 14 com ponto voltaram, a nota ausente ficou " D"; pasta de ensaio apagada.
  nas duas máquinas; Docker antes do Tailscale); mais as do 49: kit do próprio hub `-Passos 04,08,10` depois do git
  (XML do laço e `.git/info/exclude`), checkout só do que tem ponto, autocrlf=true no B.
- **Fielzinho fora.** 2ª leitura por subagente Opus (Sonnet se diff pequeno), um por vez.
- Codex só para testes, `gpt-6-luna` (`MODELO_CODEX`).
- `maestri ask` pode não entrar: `timeout 100 maestri ask ...` e conferir com `maestri check` (grep da frase).
- Brasa ligada a mim (maestro, 2026-10-18).

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
