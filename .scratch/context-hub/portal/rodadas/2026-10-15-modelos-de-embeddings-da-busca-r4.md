---
titulo: Modelos de embeddings: qual entra no hub
ticket: 54
aberta: 2026-10-15
estado: absorvida
---

A comparação terminou às 11h46, com 13 dos 15 modelos avaliados (`bancada-busca/fase2-modelos.md`, seção "Rodada 3").
A nota vai de 0 a 1: quanto mais perto de 1, mais vezes a nota certa vem no topo da busca. São só 40 perguntas, então
diferenças de 0,02 a 0,03 são ruído.

**O que os quatro modelos maiores mostraram:** nenhum muda o quadro. O embeddinggemma-2 empata com o
embeddinggemma-300m (0,64 contra 0,63), mas perde nas perguntas com outras palavras e leva o dobro do tempo. O Qwen3
ficou abaixo até do e5-small da fase 1; a causa não foi investigada.

**O quadro:**
- **Melhor de todos:** gemini-embedding-001, pela API do Google: 0,73.
- **Melhores locais:** embeddinggemma-300m (0,63, o melhor local nas perguntas com outras palavras) e
  arctic-embed-m-v2.0 (0,60, cinco vezes mais rápido).
- **Na ferramenta de busca do Obsidian testada (obsidian-hybrid-search):** o arctic é o único que já rodou lá, e deu a
  melhor busca mista de palavra e sentido da bancada (0,63).
- **Fora:** o da Cohere caiu duas vezes (limite da chave de teste e erro do servidor); o da OpenAI não existe no
  gateway.

Onde a busca mora ainda está em aberto (ticket da camada de busca), e a escolha do modelo vale para as duas opções de
lugar.

## Qual modelo
id: modelo
tipo: escolha
recomendada: A

- A: arctic-embed-m-v2.0, local nas duas máquinas: o conteúdo não sai da máquina, responde em 46 ms e é o único já provado no obsidian-hybrid-search; perde uns 0,03 para o embeddinggemma-300m, dentro do ruído
- B: embeddinggemma-300m, local: o melhor local, sobretudo nas perguntas com outras palavras; 228 ms por consulta; não foi testado no obsidian-hybrid-search
- C: gemini-embedding-001, pela API do Google via FreeLLMAPI: o melhor de todos (0,73), mas todo o hub, dado de cliente incluído, vai ao Google para indexar e cada busca depende da rede e da cota do gateway
- D: local como padrão (arctic) e o gemini como segunda opção ligável depois, para as buscas por sentido

## O Qwen3
id: qwen3
tipo: escolha
recomendada: A

- A: Fica de fora sem investigar: mesmo corrigido, ele teria de passar o embeddinggemma-300m, e o tamanho dele (7,5 GB de memória ao indexar) já pesa contra
- B: Investigar a configuração (quantização e preenchimento) e rodar de novo, uns 70 min de máquina sem agente

## Algo mais?
id: algo-mais
tipo: texto
