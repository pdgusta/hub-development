---
titulo: Índices e busca, juntos
ticket: 12
aberta: 2026-10-14
estado: absorvida
---

Você perguntou se eu considerei o que já foi decidido. Na rodada anterior, não considerei, e ela contradiz uma
decisão fechada. Em "Lições do vault", ficou decidido que **a porta de entrada é a camada de busca**, e o vault não
repete "uma cadeia de índices mantida à mão como porta de entrada; um índice só existe onde a busca não basta". A
rodada 12 pôs os índices como caminho principal e nem citou a busca. As suas escolhas nela ficam em revisão até
esta rodada.

O que já se sabe sobre onde a busca não basta:
- **Ela não lê imagem.** Os 496 prints do TRF3 e os 286 da VOEGOL são invisíveis para ela sem uma descrição em
  texto.
- **PDF, Word e planilha** só entram com texto extraído (Docling, pandoc), item que a pesquisa ampla deixou para
  este ticket decidir onde mora.
- **Pergunta escrita com outras palavras** acertou de 45% a 65% no teste de bancada, contra 90% a 95% com as
  palavras do texto. A medição com os modelos de embeddings ainda falta, às 21h.
- **Achar não é gravar.** A busca acha o que existe; ela não diz em que bloco gravar um arquivo novo.

## Como índices e busca se dividem
id: indices-e-busca
tipo: escolha
recomendada: A

- A: A busca é a porta para achar. O catálogo de blocos e o mapa do `AGENTS.md` da iniciativa dizem onde gravar. O `index.md` existe só nas pastas que crescem (a sua correção) e descreve, uma linha por item, o que a busca não lê: prints, PDFs, planilhas, subpastas de `runs/`. O verificador do fim da resposta cobra essa linha de todo arquivo que não é texto
- B: Fica como na rodada 12: os índices nas pastas que crescem são o caminho principal, e a busca é complemento
- C: Só a busca, sem `index.md`; o verificador cobra só o texto extraído de cada PDF, Word e planilha, e os prints ficam sem descrição

Por que A: respeita a decisão de que a busca é a porta e põe o índice exatamente onde a busca não basta. A linha
de descrição de um print vira texto que a própria busca indexa, então o índice alimenta a busca em vez de
concorrer com ela; e ela traz outras palavras, que ajudam nas perguntas feitas com sinônimos. O verificador
continua sendo mecanismo, não índice mantido à mão: ele inscreve o arquivo novo como "sem descrição" e avisa. Os
`.md` dispensam índice, porque a busca os lê inteiros.

## Algo mais?
id: algo-mais
tipo: texto

Seguem valendo da rodada 12, porque não conflitam com nada: o catálogo `agents/blocks.md` com a skill "nova
iniciativa" (com scripts e alteração só com o seu aval) e o bloco genérico `other/`. Esta rodada não tem carta: é
simples.
