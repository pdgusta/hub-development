# S3: a régua do hub nos finalistas (instruções do subagente)

Você verifica 4 finalistas da camada de busca de um "context hub" pessoal contra a régua dele. Responda em pt-BR.
Use WebSearch e WebFetch. Toda resposta precisa de fonte primária (README, documentação oficial, página de release,
código, CI, issue do próprio projeto) com citação literal curta. Resumo de busca, blog ou listagem não conta. O que
você não achar na fonte é "nao_verificado", nunca um chute.

## O hub

Pasta de notas Markdown com frontmatter YAML, editada no Obsidian e por agentes (Claude Code, Codex, Copilot) em duas
máquinas **Windows nativas (NTFS, sem WSL e sem Docker)**. As notas vivem num CouchDB em cada máquina, com replicação
mestre-mestre; o LiveSync mantém pastas e banco em sincronia. Agentes acessam por MCP. Conteúdo em **português e
inglês**. Um gateway local **OpenAI-compatível** (FreeLLMAPI) pode servir embeddings. Alguns clientes acessam pela
tailnet sem cópia; sandboxes não têm tailnet.

## A régua (responda cada campo)

- `windows`: roda nativo no Windows? (binário, instalador, pacote, CI com windows-latest, issue confirmando). "yes" /
  "no" / "only_wsl_or_docker" / "nao_verificado".
- `mcp`: tem servidor MCP próprio ou oficial? transporte (stdio, HTTP)? "yes" / "no" / "third_party" (diga qual) /
  "nao_verificado".
- `portugues`: stemmer/analisador de português, stopwords, remoção de acentos, ou modelo de embeddings multilíngue
  padrão ou configurável. Diga o quê.
- `markdown_frontmatter`: indexa Markdown? usa o frontmatter (filtro, campo)? chunking por título?
- `atualizacao`: como o índice acompanha mudanças no disco (watcher, reconciliação, manual)? Importa porque o LiveSync
  grava arquivos a qualquer momento.
- `embeddings_endpoint`: aceita endpoint OpenAI-compatível (base_url) para embeddings? ou só modelo local? ou não usa
  embeddings?
- `recursos`: memória/disco/runtime exigidos (JVM, Node, Python, binário único) com número se a fonte der.
- `licenca`, `ultimo_release` (data e versão), `atividade` (último commit), `maturidade` (stable/beta/alpha/archived).
- `encaixe`: em que lugar do hub ele serve (disco de cada máquina, dentro do MCP do banco, MCP do banco repassando,
  serviço na rede, cópia leve no cliente) e o principal impedimento, se houver. Até 40 palavras.

## O que fazer

1. Leia `C:/Projetos/context-hub/.scratch/context-hub/laco/sintese/s3-lotes.json`; o seu lote é o índice N (0-based).
2. Para cada item do lote, confira a régua nas fontes. Leia os itens em paralelo quando possível.
3. Grave um arquivo por item em `C:/Projetos/context-hub/.scratch/context-hub/laco/sintese/s3/<nome-em-minúsculas-com-hífens>.json`
   (UTF-8):

```
{"nome": "", "url": "", "papel": "", "windows": "", "mcp": "", "portugues": "", "markdown_frontmatter": "",
 "atualizacao": "", "embeddings_endpoint": "", "recursos": "", "licenca": "", "ultimo_release": "", "atividade": "",
 "maturidade": "", "encaixe": "", "evidencias": [{"campo": "", "url": "", "citacao": ""}], "nao_verificado": []}
```

4. Responda só "ok: <nomes gravados>".
