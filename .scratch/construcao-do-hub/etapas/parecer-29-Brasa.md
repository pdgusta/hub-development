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
