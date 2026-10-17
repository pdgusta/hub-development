# Retomada do Fiel (revisor, Claude Opus 5.5 médio) — 2026-10-17 ~11h25

Leia nesta ordem: `regras-da-construcao.md` e `revisao-em-dupla.md` (inteiros), o fim de `estado-revisor.md`, este
arquivo. Depois `maestri list`. Caminhos relativos a `C:/Projetos/context-hub/.scratch/construcao-do-hub/etapas/`.

## Quem é quem
- Construtores: Brasa, Vela, Trilho, Cinzel. Integrador: Rebite. Maestro: "Claude Code". Parceiro: Fielzinho (Codex;
  **sem cota até 12h15**; dupla normal quando voltar: repassar na hora, cada um lê sozinho, acordo por maestri ask, eu
  fecho).
- Respondo só ao construtor; ele leva o passa ao Rebite. Achado em ticket já juntado: gravo no parecer e o construtor
  leva ao maestro.

## Nada em curso (pausa da janela quieta, ~11h25)

## Fila ao voltar
1. **Codex depois das 12h15** (rodadas curtas só de evidência, quando os construtores pedirem):
   - 11 (Cinzel) r2: citação e captura do Codex (`parecer-11-Cinzel.md`);
   - 24 (Cinzel) r2: Codex com `CODEX_HOME` da casa (`parecer-24-Cinzel.md`); o resto do 24 já sem conserto;
   - 18 (Vela): Codex real (`parecer-18-Vela.md`).
2. **Leituras do Fielzinho** (quando a cota voltar), repassar com a lista: as desta manhã que fechei sozinho (17 r2,
   11 r1, 18 r1/r2/curtas, 23 r1-r3, 24 r1, 16 final r1/r2) e as atrasadas (28 r2/r3, 12 r3, 35, 33, 09, 36, 10, 16
   intermediária; antigas 13, 32, 30, 20, 15 r1, 12 r1/r2, 29). Cada uma: "Leitura do Fielzinho" no parecer; achado
   em ticket já juntado → o construtor leva ao maestro.
3. Novos pedidos dos construtores.

## Pareceres fechados hoje depois das 07h
| Ticket | Construtor | Parecer | Nota |
|---|---|---|---|
| 08 | Brasa | `parecer-08-Brasa.md` | PASSA com ressalvas; fatia 2 (51/201 MiB) é item do Gustavo (maestro) |
| 15 | Trilho | `parecer-15-Trilho.md` | PASSA em acordo; hífen do MCP vira `_` no Codex |
| 17 | Vela | `parecer-17-Vela.md` | r2 PASSA; junção só depois do 16 |
| 11 | Cinzel | `parecer-11-Cinzel.md` | r1 sem conserto; pende Codex |
| 18 | Vela | `parecer-18-Vela.md` | r2 PASSA c/ ressalvas + curta código + curta evidência PASSA; pende Codex |
| 23 | Cinzel | `parecer-23-Cinzel.md` | r3 PASSA (r2 reaberta por erro meu: não rodei o detector do 29) |
| 24 | Cinzel | `parecer-24-Cinzel.md` | r1 sem conserto; pende Codex |
| 16 | Trilho | `parecer-16-Trilho.md` | final r2 PASSA (texto resolvido não é binário) |

## Lição desta manhã
- **Sempre rodar `agents/code/test/harness-real.test.mjs` (detector do 29) em todo ticket que traz teste novo.** No 23
  passei sem ele, e o 29 ficou vermelho.

## Como reviso
- Rodo os testes do ticket e os vizinhos que ele mexe, e o detector do 29; reproduzo cada achado com sonda em
  `%TEMP%\hub-ensaio-<NN>-fiel-*` (apagar no fim); hub de ensaio por
  `node agents/code/test/hub-de-ensaio/montar.mjs <dest>`.
- Kit (23/24): hashes das configurações reais antes e depois de rodar o teste (settings.json, CLAUDE.md, config.toml,
  hooks.json, AGENTS.md do Codex, config.json, mcp-config.json, copilot-instructions.md e listagens das pastas de
  skills/hooks). O mtime de `~/.claude` muda pelas sessões abertas: normal.
- Fonte do LiveSync: `C:/Projetos/spike-livesync/livesync-src` (commonlib em `node_modules/@vrtmrz/livesync-commonlib/dist`).
- Parecer: veredito, consertos numerados com linha, reprodução e quem achou; ressalvas; evidências. `git status`
  limpo depois. Estado no `estado-revisor.md` a cada passo.

## Regras vivas
- Trabalho pesado: `trava-pesada.md` e `fila-pesada.md`; Docker só o Fiel entre os revisores; um por vez.
- Harness real só com `HUB_HARNESS_REAL=1`.
- maestri ask com `/`; ask longo pode estourar o tempo do comando, mas chega (conferir com `maestri check`).
- Teto: duas voltas; na terceira, passa com ressalvas escritas. Sem subagentes. Nada global de verdade.
- Contexto acima de 40%: no ponto seguro, estado e retomada e "Fiel: salvo para limpar".
