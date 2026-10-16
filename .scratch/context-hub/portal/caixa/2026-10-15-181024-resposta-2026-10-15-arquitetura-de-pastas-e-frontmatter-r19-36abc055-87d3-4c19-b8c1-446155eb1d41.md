---
tipo: resposta
rodada: 2026-10-15-arquitetura-de-pastas-e-frontmatter-r19
ticket: 12
enviada: 2026-10-15T18:10:24-03:00
envio: 36abc055-87d3-4c19-b8c1-446155eb1d41
estado: lida
substitui:
---

# Resposta: O esboço da árvore, e o status comum ao lado do ciclo de cada tipo

## Como o status comum convive com o ciclo de cada tipo
escolha: A, Dois campos: o ciclo do tipo vai em `stage` (quem escreve preenche: aberta, respondida etc.), e o `status` comum (rascunho, em uso, superada) fica em toda nota. Nos tipos com ciclo, o verificador deriva o `status` do `stage` por uma tabela no esquema do tipo (respondida → em uso; abandonada → superada); nos outros, quem escreve preenche o `status`. O filtro "vigente" é o mesmo em qualquer pasta (a recomendada)

## Algo mais?
> Eu estou prevendo algo que vai surgir e é melhor já remediar. Em alguns arquivos podem surgir referências cruzadas e links a arquivos que são 'local: true', ou que referenciam arquivos em pastas com ponto, ou algum caso que não previ ainda. Nesses casos eu acho melhor o link ser do tipo <par_id>/<pasta_raiz>/<subpastas>, ao invés de só './<pasta_raiz>/' ou '~/<pasta_raiz>/' ou até 'C:/<pasta_raiz>/'. Tem até a opção de ser '<par_id>/C:/context-hub/...', ou sei lá. O que acha? Quais casos acha isso útil? Em que cenário seria bom usar essa forma pra links? Todos? nenhum? só quando claramente referencia pastas ou arquivos que o outro par não saberia? É um mistério kk
