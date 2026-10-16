---
titulo: O que fazer com a Robusta depois do protótipo
ticket: 09
aberta: 2026-10-14
estado: absorvida
---

O protótipo da Robusta (índice próprio no MCP do banco) ficou pronto em 24 minutos, com 138 mil tokens do Sonnet. Ele
rodou com o mesmo corpus, as mesmas 40 perguntas e o mesmo modelo local (e5-small) do teste do
obsidian-hybrid-search (a ferramenta pronta, OHS). Relatório: `bancada-busca/prototipo-robusta.md`.

**Acertos entre os 5 primeiros resultados:**

| | Robusta | OHS |
|---|---|---|
| Por significado (vetor) | 72,5% | 72,5 a 75% |
| Por palavra | 45 a 53% | 72,5% |
| Híbrida | 65 a 75% | 75% |
| Indexar tudo | 234 a 347 s | 116 s |
| Memória no pico | 1,7 a 1,9 GB | 767 MB |

- **Vetor igual:** com o mesmo modelo, as duas acham o mesmo. A qualidade por significado vem do modelo de embeddings,
  que é escolhido para as duas.
- **Palavra pior:** a Robusta usou o Orama para a busca por palavra; o OHS usa o FTS5 do SQLite. A causa não foi
  investigada, e o FTS5 também cabe na Robusta, que já guarda o índice num SQLite.
- **Tempo e memória:** o código não foi otimizado (lotes sem paralelismo).
- **Atualização pelo banco:** sem a criptografia de ponta a ponta (E2EE), uma edição chega ao índice em 1,4 s. Com ela
  ligada, que é o caso do hub (o CouchDB só guarda pedaços cifrados), o protótipo não lê o texto: precisou de um
  segundo CLI do LiveSync para decifrar, 48 s por vez. Decifrar direto no índice, como o MCP do es617 faz para ler,
  não foi tentado.

O que fica de pé para a Robusta é o alcance: um índice só, junto do banco, servindo as duas máquinas. Esse ganho
depende de ler o banco cifrado direto, que é o ponto não provado.

## O que fazer com a Robusta
id: robusta
tipo: escolha
recomendada: B

- A: Seguir como está: na fase 2 as duas são testadas com os modelos da lista curta, e você decide depois. A busca por palavra da Robusta continua pior
- B: Antes da fase 2, o mesmo subagente faz uma rodada curta de ajuste: troca a busca por palavra pelo FTS5 do SQLite e tenta decifrar o banco direto no índice, pelo caminho do MCP do es617. Depois, a fase 2 com as duas. Estimativa de 80 a 150 mil tokens do Sonnet a mais
- C: Encerrar a Robusta agora: a fase 2 testa só o OHS com os modelos da lista curta, e a busca fica na Leve com alcance (OHS no disco de cada máquina e repasse do MCP na tailnet)

Por que B: o vetor já empatou, então o que decide entre as duas é se a Robusta acha por palavra tão bem quanto o OHS e
se lê o banco cifrado sozinha. São as duas coisas que a B testa, por bem menos do que custou o protótipo.

## Algo mais?
id: algo-mais
tipo: texto
