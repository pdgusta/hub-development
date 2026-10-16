---
titulo: Modelos de embeddings: o que a comparação mostrou
ticket: 54
aberta: 2026-10-15
estado: absorvida
---

A comparação rodou até ~03h25. O agente caiu duas vezes por erro de API antes de escrever o relatório, então eu o
escrevi a partir dos números gravados (`bancada-busca/fase2-modelos.md`). Nota de 0 a 1 é o MRR: quanto mais perto de
1, mais a nota certa vem no topo.

**O que já dá para ver (9 de 15 modelos):**
- **Melhor de todos:** o gemini-embedding-001, pela API do Google: 0,73 só com vetor, contra 0,46 do e5-small da fase 1.
- **Melhores locais:** embeddinggemma-300m (0,63) e arctic-embed-m-v2.0 (0,60), quase empatados; o arctic responde
  5 vezes mais rápido.
- **No OHS**, o arctic subiu a busca híbrida de 0,51 para 0,63, a melhor híbrida da bancada. Os outros dois que foram
  ao OHS falharam (um por arquivo que não existe no repositório do modelo, outro com resultado anômalo).
- **Rerankers:** o melhor ajuda nas perguntas com outras palavras e atrapalha nas literais, quase empata no total e
  custa 14 s por busca nesta máquina. O outro piora.
- **A híbrida da Robusta fica abaixo do vetor sozinho** nos bons modelos; é a fusão, já vista no ajuste.

**O que ficou de fora (6):** quatro modelos locais maiores (harrier-0.6b, embeddinggemma-2, e5-large-instruct,
Qwen3-Embedding-0.6B) passaram na sonda mas não foram indexados; o da OpenAI falhou porque o gateway usa outro nome
para ele; o da Cohere parou no limite da chave de teste (100 mil tokens por minuto), em 672 de 1.862 trechos.

## O que faltou
id: completar
tipo: escolha
recomendada: A

- A: Completar os 6 com os scripts que já existem, disparados por mim, sem agente Claude: os quatro locais um de cada vez (uns 5 h de máquina, por causa da memória de 15,7 GB), o da OpenAI com o nome certo no gateway e o da Cohere num ritmo abaixo do limite. Depois, uma rodada para escolher o modelo
- B: Escolher o modelo já, com os 9 que rodaram
- C: Completar só os dois por API (minutos) e escolher em seguida; os quatro locais maiores ficam de fora

## Os rerankers
id: rerank
tipo: escolha
recomendada: A

- A: Ficam de fora do hub agora e vão para o Radar, com o gatilho "a busca virar caminho crítico ou uma máquina com GPU"
- B: O bge-reranker-v2-m3 entra como opção ligável só nas buscas por paráfrase, mesmo com 14 s por busca

## Algo mais?
id: algo-mais
tipo: texto
