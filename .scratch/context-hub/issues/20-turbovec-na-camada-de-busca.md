# turbovec na camada de busca

Type: research
Status: resolved

## Question

Qual é o objetivo do repositório `RyanCodrai/turbovec` (https://github.com/RyanCodrai/turbovec), nas
palavras do autor, e esse objetivo tem relação com a camada de busca do hub (achar o trecho certo sem
ler tudo), inteiro ou em parte? Só se houver relação, aplicar os critérios que fizerem sentido para
aquele objetivo (por exemplo: Windows NTFS, pt-BR, índice que acompanha `git pull` e edição externa,
embeddings pelo FreeLLMAPI, MCP) e, se a comparação for justa, comparar com as candidatas da
§10.4.1 e com o zvec-grep ("zvec-grep na camada de busca"). Só pesquisa em fonte primária, sem
clonar nem instalar. Pedido do Gustavo em 2026-10-03.

## Answer

Relatório completo: [`pesquisa-20-turbovec.md`](../../../exploracao/anexos/pesquisa-20-turbovec.md)
(2026-10-03; README, docs e CI do commit `c6cf0ba`, API do GitHub e do PyPI; nada clonado, instalado ou testado).

- **Objetivo, nas palavras do autor:** *"A vector index built on TurboQuant, written in Rust with Python
  bindings"*. É uma biblioteca de índice vetorial, concorrente do FAISS, para RAG em grande escala: *"A 10 million
  document corpus takes 31 GB of RAM as float32. turbovec fits it in 4 GB"*.
- **Relação com a camada de busca:** só indireta. Recebe vetores prontos e devolve ids. Não lê arquivos, não quebra
  Markdown, não gera embeddings, não tem BM25, CLI nem MCP. Seria, no máximo, peça interna de uma camada construída
  pelo hub, e o ganho dele (memória e velocidade com milhões de vetores) não aparece na escala de um hub pessoal.
- **Comparação com a §10.4.1 e o zvec-grep:** não é justa; ele está uma camada abaixo delas.
- **Recomendação do relatório:** não incluir no spike do ticket "Camada de busca". Quem decide é o Gustavo.
