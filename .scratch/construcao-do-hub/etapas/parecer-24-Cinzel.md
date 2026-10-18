# Parecer do ticket 24 (Cinzel): kit de par ao vivo nos três harnesses

## Rodada 1 — 2026-10-17 ~11h (ramo ticket-24, 7d3753b, do ticket-23 f304e6c)

Veredito: **sem conserto próprio; aceite final pendente** do Codex (rodada 2, depois das 12h15) e do conserto 2 do
23 (o 24 herda o vermelho do detector do 29: `harness-real.test.mjs` 4/6 neste ramo). Fiel sozinho.

- Teste ponta a ponta lido: palavra sorteada só no `AGENTS.md` do hub de ensaio; harness aberto num repositório fora
  do hub, sem pasta-mãe com contrato; ferramentas negadas; casa como `USERPROFILE`/`HOME`; login copiado e apagado.
- Evidência: Claude e Copilot respondem `jacaranda-9889c5` sem ferramenta; no Claude, os servidores do hub vêm do
  `.claude.json` da casa e a skill de marca aparece no `init`. `apagado: true`, `pasta_apagada: true`. Sem segredo (o
  único casamento é o nome do arquivo `.copilot/hooks/gsd-session.json` nos hashes).
- Sem harness, o 24 aparece pulado.

## Leitura do Fielzinho — 2026-10-17

**Rodada 1 sem achado próprio novo; aceite dos três continua pendente do Codex.** Conferidos ticket, relatório, teste e os lido.json de Claude/Copilot: ambos respondem jacaranda-9889c5, sem ferramenta, saída 0. A palavra é sorteada e escrita só no contrato do hub; o pedido não a entrega, e a sessão abre no repositório irmão, fora do hub. Registro dos MCP e da skill segue o escopo aceito pelo maestro, sem exigir chamada aos servidores nessa prova.

O arquivo hashes-claude-copilot.json tem pares antes/depois iguais e registra login apagado nos dois e pasta_apagada=true. É leitura da evidência existente, não nova prova de limpeza na máquina. A limitação da sanitização antiga das listas de skills está descrita no relatório.

Conferência local na worktree ticket-24 a52b073, sem HUB_HARNESS_REAL: o arquivo 24-kit-ao-vivo.test.mjs aparece pulado (1 skip, 0 falhas, saída 0); diff --check e árvore limpa. Nenhum harness real ou Docker executado por mim. O achado novo no mecanismo de cópia/desfazer do 23 foi enviado ao Fiel no parecer daquele ticket; também importa ao instalador herdado pelo 24, sem duplicar a cobrança aqui.

## Merge do conserto do 23 (5680b77) — 2026-10-17 ~13h45 (Fiel sozinho; Fielzinho sem cota até 17h15)
- O 24 traz o 23 488b377 (o `mudar` que não perde o original). Fiel: `23-kit` e o detector nessa ponta, 27/27. A
  `integracao` andou (38, 39, 22 manutenção, c42ffa0): `git merge-tree` limpo; juntar antes do Rebite.
- Leitura do Fielzinho da r1 sem achado próprio (no fim deste parecer). Pende só o Codex (depois das 17h15).

## Rodada 2: evidência do Codex — 2026-10-17 ~18h30 (Fiel + 2ª leitura Opus)

Ramo `ticket-24`, ponta 2000575 (evidência sobre a3e0360, que junta `integracao` f640bbd). **Veredito: PASSA, em
acordo com a 2ª leitura** (`parecer-24-Cinzel-segunda-leitura.md`). Sem conserto. Aceite dos três harnesses fechado.
- Modelo: `-m MODELO_CODEX` (`24-kit-ao-vivo.test.mjs:111`), sem `HUB_MODELO_CODEX` na rodada.
- Evidência: `lido.json` resposta = palavra `jacaranda-1b158b`, ferramentas vazias; `erros.txt` cita
  `codex_home ...\casa\.codex` e o transporte para `127.0.0.1:3939` (o `config.toml` do kit na casa). Log
  `logs/24-harness-2.log` 1/1.
- Login: copiado 20:20:59Z, apagado 20:21:07Z; `pasta_apagada: true`; 13 hashes reais iguais, inclusive
  `~/.claude.json`. Grep de token: nada.
- Fiel: `23-kit + harness-real + 24-kit-ao-vivo` 34/34 + 1 pulado; `git status` limpo.
- Ressalvas: modelo e versão do Codex não aparecem na evidência; o relatório diz "trava de 17:21" com login às
  17:20:59 (só redação); aviso de "helper binaries" do `CODEX_HOME` em `%TEMP%` já registrado.
- Cinzel fora do canvas: veredito vai ao Rebite e ao maestro.
