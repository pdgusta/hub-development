# Parecer do Fiel — ticket 29, testes com harness de verdade só sob pedido (Brasa)

## Rodada 1 — 2026-10-17 — ramo ticket-29 em 0266761

Veredito: **volta**. Fiel e Fielzinho de acordo (parecer-29-Brasa-fielzinho.md).

### Consertos

1. **(Fielzinho; conferido pelo Fiel) A ponta de integracao andou e traz um teste de harness sem proteção.**
   `integracao` está em 0a8e17f (junta do 27), que não é ancestral de 0266761. Lá,
   `agents/code/test/ponta-a-ponta/27-fim-da-resposta.test.mjs` não tem `HUB_HARNESS_REAL`: apaga a evidência na carga
   do módulo (linha 47, `rmSync` de `evidencia-27/<harness>`) e chama `claude.exe`, o Codex e o Copilot (linhas 104 em
   diante). Juntar o 29 como está deixa `node --test "agents/code/test/**/*.test.mjs"` chamar os três harnesses pelo
   27. Conserto: `git merge integracao`, proteger o 27 do mesmo jeito (nada roda nem apaga sem a variável) e ampliar a
   lista de testes com harness e de evidências.
2. **(Fiel) A proteção precisa pegar o próximo teste também.** Hoje ela é uma lista de nomes; o 27 escapou porque nasceu
   depois. Pôr um teste sem harness que procure, em `agents/code/test/**`, chamada a `claude`, `codex` ou `copilot` (ou
   cópia de login) fora da proteção e falhe — ou outra forma que não dependa de lembrar de pôr o nome na lista.

### Para a rodada 2

Hash; suíte sem a variável mostrando os de harness (03, 14, 27) pulados e nenhuma evidência apagada (`git status`
limpo depois); a rodada com `HUB_HARNESS_REAL=1` só se a proteção mudou o caminho real do teste.

Nota: o Fiel não repetiu a rodada com harness real nem leu a evidência regravada do 14 e da 03 nesta rodada.

## Rodada 2 — 2026-10-17 — ramo ticket-29 em 0da445e

Veredito: **passa** (Fiel sozinho; Fielzinho sem cota do Codex até 01:34, leitura dele fica para depois, por ordem do
maestro; se ele achar algo, entra como ressalva para o Rebite).

Evidências (Fiel):
1. integracao 0a8e17f ancestral (merge 1736f46); worktree limpo.
2. O 27 usa `comHarness`; o `rmSync` da evidência do 14 e do 27 está dentro do corpo protegido (linhas 49/50), não na
   carga do módulo. `comHarness` sem a variável registra só um teste pulado, sem rodar o corpo.
3. `node --test "agents/code/test/**/*.test.mjs"` sem `HUB_HARNESS_REAL`: 116 testes, 112 passam, 4 pulados (14, 27,
   03 instalar, 03 prova), 0 falhas, saída 0; `git status` limpo depois. Log `etapas/revisao-29-r2-suite.log`.
4. Conserto 2 (detector sem lista de nomes, `harness-real.test.mjs`): li o relatório e a contraprova da Brasa (teste
   novo sem proteção chamando `claude.exe` deixa dois vermelhos); não repeti a contraprova (exigiria escrever na
   worktree dela).

Ressalva: as pastas `%TEMP%\hub-ensaio-14-*` dos testes sem harness continuam se acumulando (20 agora).
