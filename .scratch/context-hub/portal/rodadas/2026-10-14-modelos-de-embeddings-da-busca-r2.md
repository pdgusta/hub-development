---
titulo: A lista curta dos modelos de embeddings
ticket: 54
aberta: 2026-10-14
estado: absorvida
---

O laço terminou às 22h16, pelo teto de 5.000 tentativas: 2.157 itens no catálogo e 142 modelos do FreeLLMAPI usados.

**A conferência no Hugging Face (fonte primária):**
- Dos 396 modelos citados duas vezes ou mais, só 154 existem; o resto são nomes inventados.
- O laço puxou para modelos antigos e populares e quase não viu os de 2025 e 2026: os modelos gratuitos que responderam
  conhecem pouco do que saiu depois do treino deles. Completei pela lista do próprio Hugging Face (mais baixados, mais
  curtidos e em alta), que trouxe os novos (Google, Microsoft, IBM).
- Não conferi a posição de cada modelo no placar MTEB: quem decide é a nossa bancada, com as 40 perguntas.

**Por que só ONNX:** as duas opções de busca (a ferramenta pronta e a Robusta) rodam o modelo por transformers.js, que
precisa da versão ONNX. Todos os locais abaixo têm uma, oficial ou da comunidade `onnx-community`.

**Fora da lista, de propósito:**
- jina v5 e o reranker jina v3: licença não comercial (cc-by-nc), e o hub é usado no trabalho;
- modelos acima de 1 bilhão de parâmetros: lentos demais em CPU sem GPU;
- modelos só de inglês e os antigos da família MiniLM;
- Serafim: português de Portugal e sem ONNX.

## A lista curta
id: lista
tipo: proposta

```json
{
  "colunas": ["modelo", "tamanho", "licença", "português", "por que entra"],
  "linhas": [
    {"id": "e5-small", "modelo": "intfloat/multilingual-e5-small", "tamanho": "118M", "licença": "MIT", "português": "sim", "por que entra": "a referência: é o que as duas bancadas já usaram"},
    {"id": "granite-97m", "modelo": "ibm-granite/granite-embedding-97m-multilingual-r2", "tamanho": "97M", "licença": "Apache 2.0", "português": "sim (52 línguas)", "por que entra": "o menor e mais novo (abril de 2026), ONNX oficial"},
    {"id": "granite-311m", "modelo": "ibm-granite/granite-embedding-311m-multilingual-r2", "tamanho": "312M", "licença": "Apache 2.0", "português": "sim", "por que entra": "o irmão maior do anterior, ONNX oficial"},
    {"id": "harrier-270m", "modelo": "microsoft/harrier-oss-v1-270m", "tamanho": "268M", "licença": "MIT", "português": "sim (94 línguas)", "por que entra": "novo (março de 2026), da Microsoft"},
    {"id": "gemma-300m", "modelo": "google/embeddinggemma-300m", "tamanho": "303M", "licença": "Gemma (aceitar os termos no Hugging Face)", "português": "multilíngue, português não listado", "por que entra": "também servido pelo FreeLLMAPI"},
    {"id": "gemma-2", "modelo": "google/embeddinggemma-2", "tamanho": "744M", "licença": "Apache 2.0", "português": "multilíngue, português não listado", "por que entra": "o mais novo de todos (setembro de 2026)"},
    {"id": "arctic-m-v2", "modelo": "Snowflake/snowflake-arctic-embed-m-v2.0", "tamanho": "305M", "licença": "Apache 2.0", "português": "sim", "por que entra": "semente da calibração, ONNX oficial"},
    {"id": "gte-ml", "modelo": "Alibaba-NLP/gte-multilingual-base", "tamanho": "305M", "licença": "Apache 2.0", "português": "sim (75 línguas)", "por que entra": "semente, contexto de 8 mil tokens"},
    {"id": "e5-large-instruct", "modelo": "intfloat/multilingual-e5-large-instruct", "tamanho": "560M", "licença": "MIT", "português": "sim", "por que entra": "semente, o maior da família da referência"},
    {"id": "bge-m3", "modelo": "BAAI/bge-m3", "tamanho": "568M", "licença": "MIT", "português": "multilíngue", "por que entra": "o mais citado entre os multilíngues (787 menções); também no FreeLLMAPI"},
    {"id": "qwen3-0.6b", "modelo": "Qwen/Qwen3-Embedding-0.6B", "tamanho": "596M", "licença": "Apache 2.0", "português": "multilíngue", "por que entra": "semente; também no FreeLLMAPI"},
    {"id": "harrier-0.6b", "modelo": "microsoft/harrier-oss-v1-0.6b", "tamanho": "596M", "licença": "MIT", "português": "sim", "por que entra": "o irmão maior do harrier 270M"},
    {"id": "api-gemini", "modelo": "gemini-embedding-001 (API, pelo FreeLLMAPI)", "tamanho": "—", "licença": "termos do Google", "português": "sim", "por que entra": "do Google, servido pelo gateway"},
    {"id": "api-openai", "modelo": "text-embedding-3-large (API, pelo FreeLLMAPI)", "tamanho": "—", "licença": "termos da OpenAI", "português": "sim", "por que entra": "da OpenAI, servido pelo gateway"},
    {"id": "api-cohere", "modelo": "embed-v4.0 (API, pelo FreeLLMAPI)", "tamanho": "—", "licença": "termos da Cohere", "português": "sim", "por que entra": "da Cohere, multilíngue, servido pelo gateway"}
  ],
  "pode": ["editar", "remover", "adicionar"]
}
```

Tire, mude ou acrescente modelos.

## Como rodar a comparação
id: como
tipo: escolha
recomendada: A

- A: Em duas etapas. Primeiro, todos os modelos só na Robusta (o modelo é parâmetro dela; busca por significado e híbrida). Depois, os 3 melhores também na ferramenta pronta, para comparar as duas no mesmo modelo. Mesmo subagente Opus 5.5 médio do ajuste: 100 a 200 mil tokens e umas 3 horas de máquina, rodando sozinho
- B: Todos os modelos nas duas ferramentas: comparação completa, mas o dobro de tempo de máquina (umas 6 horas) e mais tokens
- C: Só os 5 primeiros da lista, nas duas ferramentas

## Os modelos por API
id: api
tipo: escolha
recomendada: A

- A: Entram, com a cota de cada provedor orçada antes de rodar. O corpus de teste (tickets e exploração deste projeto, e o `armis-docs`) sai da máquina para Google, OpenAI e Cohere pelo gateway. Modelo sem cota no dia fica para o dia seguinte
- B: Entram, mas só com os tickets e a exploração; o `armis-docs` sai do corpus de teste nos modelos por API (e a comparação deles com os locais fica em outro corpus)
- C: Não entram: a busca do hub fica só com modelo local

## Rerankers
id: rerankers
tipo: escolha
recomendada: A

- A: Depois de escolhido o modelo, testar dois rerankers por cima dos 20 primeiros resultados: BAAI/bge-reranker-v2-m3 (568M, multilíngue) e Alibaba-NLP/gte-multilingual-reranker-base (306M, português). Um reranker reordena os resultados lendo a pergunta junto com cada trecho; costuma ganhar acerto, mas cada busca fica mais lenta
- B: Sem reranker por enquanto

## Algo mais?
id: algo-mais
tipo: texto
