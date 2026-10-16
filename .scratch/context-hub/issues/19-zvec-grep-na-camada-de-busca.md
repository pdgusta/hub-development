# zvec-grep na camada de busca

Type: research
Status: resolved

## Question

Qual é o objetivo do repositório `zvec-ai/zvec-grep`, nas palavras do autor, e esse objetivo tem
relação com a camada de busca do hub (achar o trecho certo sem ler tudo), inteiro ou em parte? Só se
houver relação, aplicar os critérios que fizerem sentido para aquele objetivo (por exemplo: Windows
NTFS, pt-BR, índice que acompanha `git pull` e edição externa, embeddings pelo FreeLLMAPI, MCP) e,
se a comparação for justa, comparar com as candidatas da §10.4.1. Só pesquisa em fonte primária, sem
clonar nem instalar. Pedido do Gustavo em 2026-10-02.

## Comments

- 2026-10-02: o Gustavo corrigiu a ordem: "não faz sentido aplicar os critérios em algo que você não
  sabe o objetivo". Primeiro o objetivo, depois a relação com a busca, e só então os critérios.

## Answer

Relatório completo: [`pesquisa-19-zvec-grep.md`](../../../exploracao/anexos/pesquisa-19-zvec-grep.md)
(2026-10-02; README, docs e código do commit `30c3160`, API do GitHub; nada clonado, instalado ou
testado).

- **Objetivo, nas palavras do autor:** *"the local-first search layer for humans and agents"*, que
  *"unifies ripgrep, BM25, and vector search"*, também para documentação e notas. É o produto de
  busca da equipe do alibaba/zvec.
- **Relação com a camada de busca:** serve só para a **leitura**. Entrega o trecho certo e quebra o
  Markdown por título. Não grava nada: o MCP *"intentionally exposes only search"*.
- **A favor:**
  - Windows nativo, com testes no CI em `windows-latest`;
  - instalador MCP para Claude Code, Codex, Copilot CLI e VS Code;
  - modelos locais multilíngues;
  - reindexação incremental por hash, com watcher e reconciliação a cada hora;
  - Apache-2.0, 3,9 mil estrelas.
- **Contra:**
  - ignora frontmatter (PR #79 aberta);
  - BM25 sem stemming e sem remoção de acento, fraco em pt-BR;
  - o FreeLLMAPI só entra imitando o nome de modelo fixo `text-embedding-v4`, com 1.024 dimensões
    (issue #120);
  - índice em `.zvec-grep\` dentro da pasta, que precisa ir para o `.gitignore`;
  - v0.2.2, com bugs abertos que corrompem ou travam o índice (#140, #158) e um laço de
    re-embedding no Windows (#137);
  - o instalador escreve nos contratos globais dos harnesses (#223).
- **Recomendação do relatório:** entrar como uma das duas candidatas do spike do ticket "Camada de
  busca", contra o markdown-vault-mcp. O spike mediria pt-BR com e sem acento, `git pull` grande,
  frontmatter cru nos trechos e convivência com o contrato do hub. Quem escolhe as candidatas é o
  Gustavo, no ticket "Camada de busca".
