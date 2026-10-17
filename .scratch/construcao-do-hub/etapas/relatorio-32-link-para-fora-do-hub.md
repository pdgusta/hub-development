# Relatório do ticket 32: o verificador reescreve link para fora do hub

Construtora: Vela. Ramo `ticket-32`, worktree `C:\context-hub-wt\ticket-32`, de `integracao` 5d84d76. 2026-10-17.
Fonte: rodada `2026-10-16-link-para-fora-do-hub` (Gustavo, B).

## O que mudou (94c42ac)

- `agents/code/bin/lib/pastas.mjs`, `corrigirLinks`:
  - Caminho absoluto do Windows (`C:\...`, `C:/...`), `file:///C:/...` (decodificado) e wikilink com unidade, fora do
    hub, viram `[rótulo](par://<HUB_PAR_ID>/<unidade>/<caminho>)`, unidade em maiúscula, âncora mantida, com aviso
    "link para fora do hub virou par://". No wikilink, o rótulo é o apelido ou o nome do arquivo, como no resto.
  - Absoluto para dentro do hub (pelo caminho real, junction resolvida, `relativoAoHub`): perde a unidade. Se replica,
    vira link comum (`[r](caminho)` ou `[[caminho]]`), com aviso; se não replica, `par://<par_id>/<caminho>` sem
    unidade, como já era.
  - `par://<par_id>/<letra>/...` não é desfeito: o hub não tem pasta de uma letra só na raiz, então o primeiro trecho
    de uma letra quer dizer unidade, fora do hub.
  - Sem `HUB_PAR_ID`: não reescreve e devolve a falta "link para fora do hub (...) precisa virar par://, mas falta
    HUB_PAR_ID nesta máquina".
  - `AGENTS.md` e `SKILL.md` seguem de fora (o `verificar-pastas` não os passa ao `corrigirLinks`), coberto pelo teste
    que já existia.
- Antes, `C:\...` e `file:///...` caíam como "externo" (o `C:` parecia esquema de URL) e ficavam como estavam.

## Testes

- `agents/code/test/27-pastas.test.mjs`, 3 testes novos (pela linha de comando, no hub de ensaio): as três formas mais
  uma com âncora em outra unidade viram `par://` com aviso, e a segunda passada não muda nada nem avisa; absoluto para
  dentro do hub fica sem unidade (link comum e `par://` para pasta local); sem `HUB_PAR_ID`, nada muda e a falta volta.
  Vermelho antes, conferido. 27-pastas 17/17.
- Limite conhecido: caminho com espaço só funciona se o link já não casava antes (o padrão de link do 27 não aceita
  espaço no destino); caminho UNC (`\\servidor\...`) e `file://servidor/...` ficam como estão.

## Resultados

- Rodada 1 do Fiel: volta, um conserto. 6beaf15: espaço e parênteses do caminho vão codificados (`%20`, `%28`, `%29`)
  no `par://`, de fora e de dentro do hub; a passada seguinte reconhece o link. Teste novo. 27-pastas 18/18.
