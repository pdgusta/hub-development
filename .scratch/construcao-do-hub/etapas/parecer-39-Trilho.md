# Parecer do ticket 39 (Trilho): a vigia grava a mensagem limpa no estado

## Rodada 1 — 2026-10-17 ~13h20 (ramo ticket-39, 4309277, contém integracao e7203b4)

**Veredito: PASSA** (Fiel sozinho; Fielzinho sem cota até 17h15, leitura pendente).
- `lib/vigia.mjs` `gravar`: todo campo de texto do item, menos o `id`, sem sequência de cor (CSI inteira, não só SGR)
  e com o TEMP (curto e longo, `\` e `/`, sem caixa) trocado por `%TEMP%`; o `resumo` do topo também; as notificações
  saem do estado gravado. `kit.ps1`: `trap` sai só com a mensagem.
- Conferido que nada usa um campo limpo como caminho: os `caminho` dos itens são relativos ao hub e o `id` fica fora
  (o `recuperar` não perde nada).
- Fiel: 16-vigia, 17, 27, 21-copia-diaria, 20 e o detector: 109/109; `git status` limpo; merge com o `ticket-38`
  sem conflito (`git merge-tree`).

Ressalva: só strings de primeiro nível são limpas; o `voltas[].feito` do item `laco` (array) passa como veio (o
`resumo` dele, que repete a última, sai limpo).
