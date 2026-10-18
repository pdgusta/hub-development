# Parecer do ticket 44 (Brasa): o verificador de pastas não lê link dentro de código

## Rodada 1 (curta) — 2026-10-17 ~17h10 (Fiel + 2ª leitura Sonnet 5.5)

Ramo `ticket-44`, dc748bc (com integracao a7d1517). **Veredito: VOLTA** por 1 conserto, em acordo.

O que confere: código em linha e bloco cercado ficam de fora; link com código no rótulo segue lido; `./` e `../` do
link Markdown lidos da pasta da nota (raiz e pasta funda), `../` que sai do hub fica; âncora, pasta local e `par://` com
`HUB_PAR_ID` certos. Só o `verificar-pastas.mjs` chama `corrigirLinks`. Fiel: 27-pastas + 27-fim-da-resposta +
harness-real 47/47; árvore limpa.

Conserto:
1. (2ª leitura; reproduzido pelo Fiel) **Wikilink com `../` derruba o verificador.** `pastas.mjs:140`: o `alvoNoHub`
   agora devolve `undefined` para `../` também sem `nota` (o wikilink e o caminho do `par://` o chamam sem ela), e o
   wikilink passa esse `undefined` ao `naoReplica` (`pastas.mjs:~211`). Reprodução:
   `corrigirLinks('ver [[../other/y]]', { raiz, pastas: [], nota: 'a/n.md' })` lança `Cannot read properties of
   undefined (reading 'split')`; na base a7d1517 não lançava. Tratar o `undefined` em todos os chamadores (ou limitar
   o "sai do hub" ao caso com `nota`), com teste do wikilink com `../`.

Ressalvas:
- Texto que já traga U+E000…U+E001 com número é trocado pelo marcador (nota real quase nunca traz).
- Crase escapada (`\``) conta como crase (borda).

## Rodada 2 (a63cbb7) — 2026-10-17 ~17h40 (Fiel + 2ª leitura Sonnet 5.5)

`alvoNoHub` (`pastas.mjs:137-147`): o "sai do hub" (`undefined`) só vale com a `nota`; sem ela (wikilink, `par://`) o
alvo segue lido da raiz, como na base. Teste novo "44: wikilink e par:// com ../ não derrubam o verificador". Fiel:
27-pastas + 27-fim-da-resposta 40/40; sondas (`[[../other/y]]`, `par://a/../b.md`, `[[../../../fora]]`) sem erro. 2ª
leitura: reprodução refeita sem erro, casos antigos iguais, 27-pastas 24/24, árvore limpa. **Veredito: PASSA em
acordo.** Ressalvas da r1 seguem (marcador U+E000, crase escapada; wikilink com `../` lido da raiz).
