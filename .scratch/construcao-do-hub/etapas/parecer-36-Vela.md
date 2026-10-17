# Ticket 36 — Vela — parecer do Fiel — rodada 1

2026-10-17 ~05h35. Ramo ticket-36, HEAD b8e8b03; contém integracao. Fiel sozinho (Fielzinho sem cota até 06h58;
leitura dele pendente).

## Veredito: VOLTA (1 conserto)

## Conserto
1. **Uma exceção solta num teste apaga as pastas de todos os testes do arquivo, no meio da execução** (Fiel).
   `pasta-de-ensaio.mjs` põe `limparAoSair` em `prependListener('uncaughtException')` e `('unhandledRejection')`.
   Só que o `node:test` não morre com a exceção solta dentro de um teste: ele marca aquele teste como falho e segue.
   A limpeza já rodou, e os testes seguintes acham a pasta (o hub do `before`) apagada.
   Sonda (arquivo temporário na worktree, já apagado): pasta criada no topo; teste 1 joga `setTimeout(() => { throw })`;
   teste 2 confere `existsSync(pasta)` → `✖ a pasta sumiu no meio da execução`. O mesmo vale para uma rejeição solta:
   o teste 4 falha com "sumiu depois da rejeição".
   Efeito: uma falha vira uma cascata de ENOENT nos testes seguintes e esconde a causa. É o oposto do que o ticket
   quer, que é ver a falha.
   Conserto: nesses dois eventos, limpar só quando o processo vai mesmo morrer. Por exemplo, só antes do primeiro
   teste começar (queda no carregamento), tirando os listeners num `before`; ou confiar no `after` e no `exit`.
   Teste que prove: exceção solta num teste, e o teste seguinte ainda acha a pasta; e a queda no carregamento
   continua limpando.

## Conferido
- `node --test --test-concurrency=1` em 36, 04, 05, 05n, 14, 15, 19, 20, 27 (dois) e gerador: 174/174 (Fiel).
  Pastas `hub-ensaio-*` em %TEMP%: 0 antes e 0 depois (as 1325 antigas já tinham sido apagadas por alguém).
- O ajudante apaga da mais nova para a mais velha, cada pasta sozinha, e o `after` falha nomeando a presa.
- Árvore limpa.

## Ressalvas (não bloqueiam)
- Fora, de propósito, como diz o relatório: os ramos abertos (08, 10, 15, 16, 17), o 12 e o 13 e os testes de ponta a
  ponta reais. Cada um adota o ajudante ao ser juntado ou num ticket seguinte.
- `taskkill /F` ninguém pega (escrito no ajudante).

# Rodada 2 — Fiel — 2026-10-17 ~06h35

Ramo ticket-36, HEAD 5b90550.

## Veredito: PASSA

- Conserto: nos dois eventos, limpa só se nenhum teste começou (marca num `beforeEach` da raiz). Quando o arquivo cai
  no carregamento, segue limpando.
- A sonda da rodada 1, repetida: as exceções soltas nos testes 1 e 3 falham só esses testes; os testes 2 e 4 acham a
  pasta. No fim do arquivo a pasta saiu (nenhuma `hub-ensaio-sondafiel-*`).
- `36-pasta-de-ensaio.test.mjs`: 8/8 (Fiel). Árvore limpa. Os 11 arquivos, pelo relatório: 176/176. Só o ajudante
  mudou desde os meus 174/174.
- Ressalva: uma exceção solta num `before` da raiz, antes do primeiro teste, ainda limpa. Mas aí os testes do arquivo
  já caem.
