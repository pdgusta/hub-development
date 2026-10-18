# Relatório do ticket 44: o verificador de pastas não lê link dentro de código, e lê o ../ da pasta da nota

Brasa, 2026-10-17. Ramo `ticket-44`, worktree `C:/context-hub-wt/ticket-44`, de `integracao` 98a7ced, com a7d1517
juntada (a doc do 11).

## O que mudou

- `agents/code/bin/lib/pastas.mjs`, `corrigirLinks`:
  - **Código em linha.** O bloco cercado já ficava de fora. Agora o código em linha também fica: `CODIGO_EM_LINHA`
    acha o trecho (as mesmas crases fecham, sem atravessar linha em branco, como no CommonMark). Ele sai por um
    marcador (dois caracteres de uso privado, U+E000 e U+E001, com o número) antes da troca e volta igual depois,
    no texto e nas mensagens.
  - Por que um marcador e não cortar o texto: um link com código no rótulo (`[o `x`](y.md)`) segue sendo um link de
    verdade. Cortado, ele se perderia.
  - **`./` e `../`.** `corrigirLinks` recebe `nota`, o caminho da nota a partir da raiz. O `alvoNoHub` lê da pasta
    da nota o link Markdown que começa por `./` ou `../`, com `path.posix.join`. O `..` some, e o `naoReplica` não
    o toma mais por "parte com ponto".
  - O que replica fica como está (o link relativo não é reescrito). O que não replica vira
    `par://<par>/<caminho pela raiz>`. O que sai do hub fica, sem falta.
  - Wikilink não mudou (ver Ressalvas).
- `agents/code/bin/verificar-pastas.mjs`: passa `nota: rel`.
- `agents/code/docs/componentes/pastas-e-links.md`:
  - "Links": o código em linha também fica de fora, e há uma linha nova na tabela para o `./` e o `../`.
  - §7: saem a divergência do `..` (do Lume) e a ressalva 2 do parecer do 33. Entra a ressalva do wikilink.

## Testes (`agents/code/test/27-pastas.test.mjs`, pela linha de comando, no hub de ensaio)

- `44: link dentro de código (em linha ou bloco cercado) é texto...`. Usa uma tabela com `` `[Open in Obsidian](...)` ``
  (o caso da suíte) e código em linha com uma, com duas crases e com o wikilink. Cobre também os blocos ``` e ~~~,
  mais dois links de verdade fora do código, um deles com código no rótulo.
  - Sem `HUB_PAR_ID`: só as duas faltas dos links de fora, e o texto fica intacto.
  - Com `HUB_PAR_ID`: só os de fora viram `par://`.
  - Vermelho antes: 3 faltas e 2 avisos a mais, todos de código em linha.
- `44: link Markdown com ./ ou ../ resolve da pasta da nota...`. A nota fica em `initiatives/context-hub/notas/`, com
  quatro links:
  - `../decisions.md` (replica): fica;
  - `./vizinha.md#topo` (replica): fica;
  - `../labs/ensaio-do-banco.md` (pasta local): falta sem `HUB_PAR_ID`; com ela, `par://maquina-a/initiatives/context-hub/labs/ensaio-do-banco.md`;
  - `../../../../fora.md` (sai do hub): fica.
  - Vermelho antes: os três que não são do labs davam falta "precisa virar par://".
- `node --test agents/code/test/27-pastas.test.mjs agents/code/test/27-fim-da-resposta.test.mjs`: 39 passam, 0 falham (ponta dc748bc).
  Entre os 23 do `27-pastas` está "onde o catálogo diz tipo null não nasce cartão", o que caiu na suíte: ele lê
  `agents/code/docs/`.
- A suíte inteira roda na junção, com o Rebite.

## Ressalvas

- Wikilink com `./` ou `../` segue lido da raiz. O ticket pediu o link Markdown, e o Obsidian lê o wikilink pelo nome
  (anotado na §7 da página).
- Código em linha que atravessa uma linha de tabela ou de lista: o CommonMark corta antes, e a regex só para na linha
  em branco. Numa nota real, uma crase sem par numa linha casaria com a crase da linha seguinte do mesmo parágrafo. O
  efeito seria só deixar de ler um link entre as duas.

## Rodada 1 do Fiel: VOLTA por 1 conserto (feito, a63cbb7)

- Wikilink com `../` derrubava o verificador: o `alvoNoHub` devolvia `undefined` para `../` também sem a nota, e o
  wikilink o passava ao `naoReplica`. Agora o "sai do hub" só vale com a nota (link Markdown com `./` ou `../`).
  Sem ela (wikilink, `par://`), o alvo segue lido da raiz, como na base.
- Teste novo `44: wikilink e par:// com ../ não derrubam o verificador...`: vermelho antes (TypeError no
  `naoReplica`), verde depois. 27-pastas + 27-fim-da-resposta: 40/40.
