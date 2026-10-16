# Varredura de candidatas à camada de busca

Type: research
Status: resolved

## Question

Que ferramentas, além das já conhecidas, podem ser a camada de busca do hub? A varredura segue o
protocolo da §10.4 e tem os requisitos refeitos com as decisões tomadas desde a varredura de
2026-09-29 (`exploracao/anexos/varredura-3-camada-sobre-markdown.md`). O resultado alimenta a
escolha das duas candidatas do spike em "Camada de busca".

Motivo (Gustavo, 2026-10-04): ele quer uma fase de busca de candidatas novas antes do spike. Indício
de lacuna na varredura anterior: o zvec-grep ("busca local para humanos e agentes") e o turbovec
chegaram por fora dela, porque o vocabulário era de "vault Markdown + MCP".

Requisitos (confirmados pelo Gustavo em 2026-10-04, com o pt-BR rebaixado):

- **R1 arquivos no lugar:** a fonte são os `.md` do hub; o índice é derivado, fica fora da pasta ou
  pode ser ignorado pelo git, e se reconstrói em cada máquina.
- **R2 trecho certo:** busca híbrida (palavra + sentido), com retorno por trecho ou título; filtro de
  frontmatter é desejável.
- **R3 MCP:** busca pelo MCP é obrigatória; gravar conferindo a versão é bônus.
- **R4 Windows nativo:** roda local no NTFS (`C:\context-hub`), sem WSL ("Windows ou WSL").
- **R5 edição externa:** o índice acompanha edição direta no disco e `git pull` (watcher ou reconciliação).
- **R6 embeddings:** modelo local ou endpoint compatível com OpenAI (para o FreeLLMAPI).
- **pt-BR não é requisito** (Gustavo, 2026-10-04): registrar o suporte (modelo multilíngue, acento,
  stemmer) como informação, sem eliminar ninguém por isso.
- **R7 viva:** licença aberta, commit nos últimos 6 meses.

Já conhecidas, para marcar e não recontar: as 47 da varredura 3, o zvec-grep e o turbovec.

## Comments

- 2026-10-04: requisitos confirmados na rodada 2 de "Camada de busca", com uma correção do Gustavo:
  "pt-br não é requisito". Varredura lançada; relatório em
  `exploracao/anexos/pesquisa-21-varredura-busca.md`.

## Answer

Relatório completo: [`pesquisa-21-varredura-busca.md`](../../../exploracao/anexos/pesquisa-21-varredura-busca.md)
(2026-10-04; 48 consultas registradas, em 8 línguas, na web, na API do GitHub, no registry de MCP, no
HN e no awesome-mcp-servers; nada clonado, instalado ou executado).

- **A lacuna existia:** o vocabulário "semantic grep / busca local para agentes" trouxe ferramentas
  maduras que a varredura 3 não viu: ck, grepai, mgrep, SeaGOAT e vexor. Foram 19 novas conferidas na
  fonte, 25 de cauda longa só listadas e 24 já conhecidas que reapareceram.
- **Melhor nova: memtomem** (conferido por mim no README, no CI e na API em 2026-10-04):
  - *"Your `.md` files are the source of truth. The DB is a rebuildable cache"*;
  - CI com job em `windows-latest`;
  - modelo padrão `multilingual-e5-small`;
  - guia oficial de sync por git entre máquinas;
  - Apache-2.0, 15 estrelas, criado em 2026-03, README marcado *"Alpha"*.
  - **Não verificado:** se o servidor MCP reindexa sozinho, na partida, o que um `git pull` trouxe;
    se o `BASE_URL` aceita o FreeLLMAPI.
- **ck:** o par maduro do zvec-grep (binário Windows, reconcilia antes de cada busca, índice fora da
  pasta). Contra: só modelos em inglês, sem endpoint compatível com OpenAI, sem frontmatter e sem CI
  em Windows.
- **Recomendação do relatório:** o memtomem entra no spike, como terceira candidata ou no lugar do
  markdown-vault-mcp (mesmo nicho, com o teste em Windows que falta ao outro). O ck fica de reserva do
  zvec-grep. Quem decide é o Gustavo, em "Camada de busca".
