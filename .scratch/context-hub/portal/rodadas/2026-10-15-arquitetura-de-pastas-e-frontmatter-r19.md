---
titulo: O esboço da árvore, e o status comum ao lado do ciclo de cada tipo
ticket: 12
aberta: 2026-10-15
estado: absorvida
carta: prototipo-12-arvore
---

O esboço da árvore final que você pediu está na carta **"prototipo-12-arvore"**: da raiz até uma iniciativa de exemplo
(`clients/voegol/cross-tenant/`), cada arquivo abre com o frontmatter real do tipo, e cada campo mostra quem o preenche
(a máquina, pelo caminho, ou quem escreve). Valores como versões, contagens e datas são só de exemplo. Aprove ou recuse a
carta lá; esta rodada decide o único ponto que a carta deixou "a conciliar".

**O conflito:** na rodada anterior você pediu um `status` comum em toda nota (rascunho, em uso, superada), para filtrar o
vigente em qualquer pasta. Mas vários tipos já têm um ciclo próprio com outros valores: pesquisa (aberta, respondida,
abandonada), design, plano, entrega, trabalho dos agentes, caso, laboratório e a ficha da iniciativa (doing, backlog,
on-hold, done, archived). Um campo só não cabe os dois.

## Como o status comum convive com o ciclo de cada tipo
id: status-e-ciclo
tipo: escolha
recomendada: A

- A: Dois campos: o ciclo do tipo vai em `stage` (quem escreve preenche: aberta, respondida etc.), e o `status` comum (rascunho, em uso, superada) fica em toda nota. Nos tipos com ciclo, o verificador deriva o `status` do `stage` por uma tabela no esquema do tipo (respondida → em uso; abandonada → superada); nos outros, quem escreve preenche o `status`. O filtro "vigente" é o mesmo em qualquer pasta
- B: Um campo só, `status`: nos tipos com ciclo, os valores do tipo; nos outros, rascunho, em uso, superada. Cada esquema marca quais dos seus valores contam como vigentes, e a busca filtra o vigente por essa marca. Menos campos, mas o filtro depende do tipo
- C: Dois campos preenchidos à mão, `stage` e `status`, sem derivação: mais simples de construir, mas os dois podem se contradizer

## Algo mais?
id: algo-mais
tipo: texto
