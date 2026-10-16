# S2: varredura de atualidade com busca na web (instruções do subagente)

Você pesquisa UM tema para a camada de busca de um "context hub" pessoal. Responda em pt-BR. Use WebSearch e
WebFetch. Fonte primária (README, documentação oficial, release, código) é obrigatória para cada afirmação; uma
listagem de busca ou um resumo de blog não conta. O que você não conferir na fonte vai para "nao_verificado".

## O hub (para julgar o encaixe)

Uma pasta de notas Markdown com frontmatter, editada no Obsidian e por agentes de código (Claude Code, Codex, Copilot)
em duas máquinas Windows (NTFS nativo, sem WSL). As notas vivem num CouchDB em cada máquina, com replicação
mestre-mestre pela tailnet; o plugin Obsidian LiveSync e o CLI dele mantêm as pastas e o banco em sincronia. Os agentes
leem e gravam por um servidor MCP sobre o CouchDB. Há também clientes sem cópia (pela tailnet) e sandboxes sem
tailnet. Conteúdo em português e inglês. Um gateway local OpenAI-compatível (FreeLLMAPI) pode servir embeddings.

Lugares possíveis da busca: disco de cada máquina; dentro do MCP do banco; o MCP do banco repassando a uma busca no
disco; serviço na rede; cópia leve no cliente.

## O que fazer

1. Leia o seu tema em `C:/Projetos/context-hub/.scratch/context-hub/laco/sintese/s2-temas.json` (índice N que o
   maestro passou).
2. Não repita o que já foi levantado: os nomes em `C:/Projetos/context-hub/.scratch/context-hub/laco/sintese/s2-ja-conhecidos.txt`
   só entram se o seu tema trouxer um fato novo e conferido sobre eles.
3. Faça de 6 a 12 buscas, em mais de uma língua quando fizer sentido, e confira na fonte os achados que encaixam.
4. Grave `C:/Projetos/context-hub/.scratch/context-hub/laco/sintese/s2/<id do tema>.json` (UTF-8) com:

```
{
  "tema": "<id>",
  "consultas": ["<cada busca feita>"],
  "achados": [
    {
      "nome": "", "url_fonte": "", "o_que_e": "<até 25 palavras>",
      "lugar": ["disk" | "inside_db_mcp" | "db_mcp_forwarding" | "network_service" | "light_client" | "library"],
      "mecanismo": ["bm25" | "full_text" | "vector" | "hybrid" | "grep" | "graph" | "reranker" | "embeddings" | "proxy" | "other"],
      "mcp": "yes|no|unknown", "windows": "yes|no|unknown", "portugues": "yes|no|unknown",
      "licenca": "", "ultimo_release": "<data ou versão, da fonte>", "maturidade": "stable|beta|alpha|archived|unknown",
      "encaixe": "<como entraria no hub, até 30 palavras>",
      "evidencias": [{"url": "", "citacao": "<trecho literal curto>"}],
      "nao_verificado": ["<o que ficou sem fonte>"]
    }
  ],
  "lacunas": "<o que o tema pedia e não existe, ou não foi achado>"
}
```

5. Responda só "ok: N achados".
