---
titulo: Quem monta o protótipo da Robusta
ticket: 09
aberta: 2026-10-14
estado: absorvida
---

Você escolheu começar pela Leve com alcance (obsidian-hybrid-search) e fazer já o protótipo de 1 dia da Robusta,
para comparar as duas no mesmo teste.

**O que o protótipo faz:**
- um índice em Node com Orama (stemmer de português) e sqlite-vec;
- alimentado pelas mudanças (`_changes`) do CouchDB do spike do LiveSync, que já existe em
  `C:\Projetos\spike-livesync`;
- mede a reindexação total;
- entra no mesmo teste do obsidian-hybrid-search: mesmo corpus, as 40 perguntas e os mesmos scripts.

O modelo de embeddings das duas vem da lista curta da pesquisa que está rodando agora, para o teste rodar uma vez
só. **Não verificado:** se o CouchDB do spike ainda sobe e se o `_changes` entrega o texto já decifrado com a E2EE
ligada.

Escrever o protótipo é código, não pesquisa, então ele não roda pelos modelos do FreeLLMAPI: gasta tokens do
Claude. A bancada anterior gastou 163 mil tokens do Sonnet.

## Quem monta e quando
id: quem
tipo: escolha
recomendada: A

- A: Um subagente Sonnet 5.5 monta o protótipo agora, em paralelo à pesquisa de embeddings, e roda a comparação quando a lista curta sair. Estimativa de 300 a 500 mil tokens do Sonnet
- B: O mesmo subagente, mas só começa depois da lista curta, para fazer protótipo e comparação de uma vez. Mesma estimativa, um dia a mais de espera
- C: Eu, o maestro, monto nesta sessão. Gasta tokens do Opus e o contexto do maestro, que é o que segura as rodadas

Por que A: o protótipo não depende da lista curta, só a comparação depende. Em paralelo, os dois ficam prontos ao
mesmo tempo.

## Algo mais?
id: algo-mais
tipo: texto
