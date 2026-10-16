---
tipo: resposta
rodada: 2026-10-15-arquitetura-de-pastas-e-frontmatter-r16
ticket: 12
enviada: 2026-10-15T16:18:24-03:00
envio: d6f47073-e2be-4f3a-9823-23b19bac4350
estado: lida
substitui:
---

# Resposta: Índices, anexos e títulos, com a busca decidida

## Como índices e busca se dividem
escolha: B, Igual à A, mas o `index.md` existe também em toda pasta que cresce, mesmo só com `.md` (a sua correção na rodada "Como o agente acha tudo"), como sumário para navegar sem buscar (a recomendada era A)

## Onde mora o texto extraído dos anexos
escolha: A, Num arquivo irmão, ao lado do anexo: `proposta-v2.pdf` ganha `proposta-v2.pdf.md`, com `title` (o nome do documento), `source` (o arquivo de origem) e `extractor` (Docling ou pandoc, com a versão) no frontmatter. Vale para PDF, Word, PowerPoint, Excel e HTML. Replica para a outra máquina e vai ao git com o resto. O anexo com texto dispensa linha no `index.md` (a recomendada)

## O título das notas do núcleo e os nomes alternativos da iniciativa
escolha: A, Os arquivos do núcleo ganham `title` com o nome da iniciativa ("Retomada · VOEGOL cross-tenant", "Decisões · VOEGOL cross-tenant"). A skill "nova iniciativa" os escreve, e o verificador completa o que faltar, como o `log/` de um mês novo, a partir do `title` da ficha. A ficha ganha o campo `aliases`: siglas, o nome no Loop, o nome antigo no vault (a recomendada)

## Algo mais?
em branco
