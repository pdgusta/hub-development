# S6: a régua do hub na segunda lista (instruções do subagente)

Você vai verificar 4 itens de um "context hub" pessoal contra a régua dele. Responda em pt-BR.

Use WebSearch e WebFetch. Toda resposta precisa de uma fonte primária, com uma citação literal curta. Valem README,
documentação oficial, página de release, código, CI e issue do próprio projeto. Não valem resumo de busca, blog nem
listagem. O que você não achar na fonte é "nao_verificado", nunca um chute.

## O hub

- **Notas:** uma pasta de notas Markdown com frontmatter YAML, editada no Obsidian e por agentes (Claude Code, Codex,
  Copilot).
- **Máquinas:** duas máquinas **Windows nativas (NTFS, sem WSL e sem Docker)**.
- **Banco e sincronia:** as notas vivem num CouchDB em cada máquina, com replicação mestre-mestre. O LiveSync mantém
  pastas e banco em sincronia, gravando as notas no banco em pedaços e cifradas.
- **Acesso dos agentes:** por MCP.
- **Idiomas:** o conteúdo é em **português e inglês**.
- **Embeddings:** um gateway local **OpenAI-compatível** (FreeLLMAPI) pode servi-los.
- **Rede:** alguns clientes acessam pela tailnet, sem cópia; as sandboxes não têm tailnet.

## Antes de tudo: identidade

O nome do item veio da memória de modelos e pode estar errado. **A URL manda.** Confira a URL, diga que projeto ela é
(`nome_canonico`) e verifique esse projeto. Dois casos especiais:
- se a URL não existir, procure o projeto pelo nome e diga isso em `identidade`;
- se o item juntar duas coisas (ex.: "LocalAI + LangChain"), verifique a peça principal e diga qual foi.

## A régua

O campo `serve` do item diz qual régua usar.

**Item de busca (`serve` = "search")**: os mesmos campos da S3.
- `windows`: "yes" / "no" / "only_wsl_or_docker" / "nao_verificado", com o porquê (binário, wheel, CI windows-latest).
- `mcp`: "yes" / "no" / "third_party" (diga qual) / "nao_verificado"; diga também o transporte.
- `portugues`: stemmer ou analisador de português, stopwords, remoção de acentos, ou modelo multilíngue.
- `markdown_frontmatter`: se indexa Markdown, se usa o frontmatter, se divide o texto por título.
- `atualizacao`: watcher, reconciliação ou manual.
- `embeddings_endpoint`: base_url OpenAI-compatível, só modelo local, ou não usa embeddings.
- `recursos`: runtime, memória e disco, com número quando a fonte der.
- `licenca`, `ultimo_release` (data e versão), `atividade` (último commit) e `maturidade` (stable / beta / alpha /
  archived).
- `encaixe`: até 40 palavras. Diga em que lugar do hub ele serve (disco de cada máquina, dentro do MCP do banco, MCP
  do banco repassando, serviço na rede ou cópia leve no cliente) e o principal impedimento.

**Item de stack (`serve` = "stack")**: o campo `area` diz para que parte do hub ele foi lembrado.
- `windows`: igual ao da busca.
- `mcp`: preencha só se a área for `mcp`; nas outras, "nao_aplicavel".
- `portugues`: preencha nas áreas `text_pt`, `embeddings_rerank` e `text_extraction`; nas outras, "nao_aplicavel".
- `markdown_frontmatter`: preencha nas áreas `markdown_frontmatter` e `obsidian`; nas outras, "nao_aplicavel".
- `atualizacao` e `embeddings_endpoint`: "nao_aplicavel", a não ser que o projeto trate disso.
- `recursos`, `licenca`, `ultimo_release`, `atividade` e `maturidade`: iguais aos da busca.
- `encaixe`: até 40 palavras. Diga que papel ele teria na construção do hub, com que peça já decidida ele conversa
  (CouchDB, LiveSync, MCP, FreeLLMAPI, Obsidian) e o principal impedimento.

## O que fazer

1. Leia `C:/Projetos/context-hub/.scratch/context-hub/laco/sintese/s6-lotes.json`. O seu lote é o índice N
   (contado a partir de 0).
2. Para cada item do lote, confira a régua nas fontes. Quando der, leia os itens em paralelo.
3. Grave um arquivo por item em
   `C:/Projetos/context-hub/.scratch/context-hub/laco/sintese/s6/<nome-canonico-em-minusculas-com-hifens>.json`
   (UTF-8), neste formato:

```
{"nome": "<nome no catálogo>", "nome_canonico": "", "chave": "<chave do item>", "url": "", "serve": "", "area": "",
 "identidade": "<ok, ou o que mudou>", "windows": "", "mcp": "", "portugues": "", "markdown_frontmatter": "",
 "atualizacao": "", "embeddings_endpoint": "", "recursos": "", "licenca": "", "ultimo_release": "", "atividade": "",
 "maturidade": "", "encaixe": "", "evidencias": [{"campo": "", "url": "", "citacao": ""}], "nao_verificado": []}
```

4. Responda só "ok: <nomes gravados>".
