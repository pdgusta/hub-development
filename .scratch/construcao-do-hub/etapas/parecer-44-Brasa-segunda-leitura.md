# Parecer 44 (Brasa), segunda leitura independente

Veredito: VOLTA (um conserto pequeno). Resto passa.

Conferido: `node --test agents/code/test/27-pastas.test.mjs` 23/23 verde; `git status --short` limpo; ensaio apagado.

## Consertos
1. Wikilink com `../` derruba o verificador. `agents/code/bin/lib/pastas.mjs:140` devolve `undefined` quando o alvo começa por `../`; as chamadas sem `nota` (wikilink, linha 210, e `par://`, linha 219) passam esse `undefined` a `naoReplica` (linha 211), que lança `TypeError ... reading 'split'`.
   Reprodução: `corrigirLinks('[[../other/y]]', {raiz, pastas:['other'], nota:'a/n.md'})` lança. Com `[[other/y]]` funciona. Na base a7d1517 isso devolvia texto.
   Conserto: tratar `undefined` nas linhas 210-211 e 219 (`if (rel === undefined) return original`), ou só aplicar o corte `../` quando houver `nota`. Pede teste.

## Passa (reproduzido)
- Código no rótulo `[o \`x\`](other/y.md)`: link lido (falta sem HUB_PAR_ID).
- Crase sem par antes de link: link lido. Crase que pareia com outra mais adiante vira código (igual ao CommonMark).
- Duas crases (``a ` b``): fechamento certo; link depois dele segue lido.
- Código em linha sem link e link vizinho: ok. Linha em branco corta o código: ok.
- `./` na raiz e `../` em a/b: resolvem pela pasta da nota. `../../other` em a/b vira falta certa. Âncora preservada. Nota em pasta local: sem falta.
- `../` que sai do hub: ignorado em silêncio, sem aviso (decisão aceitável, ressalva).
- Com HUB_PAR_ID: `par://PAR1/other/y.md` correto.

## Ressalvas
- Marcador U+E000/U+E001: nota que já traga `U+E000 0 U+E001` troca esse trecho pelo código guardado ou por `undefined` (reproduzido: `"0 [l](...)"` sai `"undefined [l](...)"`), e o texto da nota é reescrito. Improvável, mas é dano ao texto; mais seguro escolher marcador com sufixo aleatório ou ignorar índice fora de `emLinha`.
- Crase escapada (`\``) é tratada como crase de código (CommonMark não trata). Borda rara, sem dano maior.

## Conserto a63cbb7
Veredito: PASSA.
- `git diff dc748bc a63cbb7`: o corte `../` em `alvoNoHub` só vale quando há `nota`; sem nota (wikilink, par://) o alvo segue lido da raiz. Teste novo cobre wikilink, par:// e link Markdown na mesma nota.
- Reprodução refeita (raiz de ensaio apagada): `[[../other/y]]` com nota `a/n.md` não lança mais (devolve falta de HUB_PAR_ID, texto intacto); `par://m/../z.md` não lança.
- Seguem como antes: `./other/y.md` e `../../other/y.md` (de a/b) viram falta certa; `../other/y.md` de a/b resolve para a/other (sem falta); `../../../fora.md` ignorado; `[[other/y]]` igual.
- `node --test agents/code/test/27-pastas.test.mjs` na worktree: 24/24 verde (159 s). `git status --short` limpo.
