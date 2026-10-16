# Worker 1: notas

## Volta 1 (2026-10-15)

**Faixa assumida: 1, esqueleto, contrato e frontmatter** (corte candidato do Worker 2, que bate com o meu rascunho).
Decisões cobertas: ticket 12 (seis raízes, `_archive/`, núcleo de seis arquivos, `agents/blocks.md`, esquemas em
`agents/frontmatter/`, `status` e `stage`, `index.md` com `summary: auto` e `local`), ticket 36 (sem `CLAUDE.md` no hub
nem acima, `.git` na raiz; o marcador de raiz saiu em 2026-10-15), ticket 10 (o contrato file-first vai no `AGENTS.md`).

Gravei no plano:
- a minha linha na tabela de faixas;
- três fronteiras: confirmo o hub de ensaio do Worker 2; a assinatura do verificador de frontmatter (usada pelas faixas
  6 e 5, com dublê que sai 0 até eu entregar); o bloco `cabeca:inicio/fim` de até 2.048 caracteres no `AGENTS.md` para
  o `instructions` do MCP (faixa 5);
- "Fica para outra execução": trazer esta frente para o hub ("Not yet specified" no mapa);
- pergunta ao Gustavo: copiar `armis-docs`, `armis-brand` e `armis-docx` nesta execução (ticket 02: "quando o Gustavo
  disser").

Descartei o meu rascunho de corte inteiro: o do Worker 2 chegou antes e é quase igual. Diferenças que eu tinha e
ficam como sugestão: o proxy e o kit de cliente juntos numa faixa (no corte do Worker 2 estão na 10, com manutenção);
um manifesto `agents/kit/hooks.d/` e `mcp.d/` para o kit de par (o Worker 2 propôs `kit/par/<nn>-<faixa>.ps1` e
`hooks/<faixa>/`: serve igual, fico com o dele).

O Worker 8 escreveu nas notas a vigia, mas no plano e no `voltas.md` assumiu a faixa 8 (kit de par); vale o plano.

### Para a próxima volta

- Conferir se a faixa 1 cabe em 1 hora: o `AGENTS.md` é o item mais pesado (conteúdo do contrato, ticket 10 e 11);
  talvez um subagente só para ele, e os esquemas por tipo em paralelo.
- Fechar com os donos das faixas 5 (MCP do banco) e 6 (guardas) a assinatura do verificador, por `maestri ask`.
- Ler o Answer do ticket 12 inteiro para listar os tipos de frontmatter e o ciclo de `stage` sem inventar.

## Volta 2 (2026-10-15)

**Feito: a faixa 1 passou a caber na hora e a seguir a decisão.** Fonte: Answer do 12 (lido inteiro), 36 (2.000
caracteres), a parte da faixa 1 em `../spec-partes/faixas-01-02.md` e os pedidos das faixas 3, 6, 9 e 10 e dos Prumos.

- Sem `agents/bin/` (Prumo): verificador em `agents/frontmatter/verificar.mjs`, exclusões em
  `agents/frontmatter/exclusoes.mjs`, criação de iniciativa na skill `agents/skills/nova-iniciativa/` (o 12 diz que é
  skill). Os dois lugares em `agents/frontmatter/` são proposta minha dentro de pasta decidida.
- Núcleo (a)–(g) na linha; segunda passada: `index.md` automático e `.pdf.md`; outra execução: links `par://`, aviso
  de `other/`, portas com `codex exec`/`copilot -p`.
- Fronteiras novas: interface do verificador (`--checar` com conteúdo pela entrada padrão, sai 0 também para caminho
  sem esquema, pedido dos Workers 6 e 9); exclusões geradas (`.local/exclusoes/livesync.txt` e bloco no `.gitignore`,
  que serve à busca); textos de outras faixas no `AGENTS.md` por `hooks/<nn>/regra-contrato.md`; ordem no fim da
  resposta (verificador antes do checkpoint), a fechar com o Worker 2.
- Apaguei do bloco do Prumo os itens da faixa 1 que absorvi; troquei a linha "1:" do crivo do Prumo 2.
- Antes da hora: pacote `yaml` e as tabelas de `kind`/`size`/`cadence` e blocos tiradas da caixa do portal.
- Duas perguntas ao Gustavo: tabela `stage` → `status`; núcleo em `operations/` e `reference/`.

**Não toquei a spec** (o PROMPT limita a escrita a `planejamento/`). A spec ainda tem `agents/bin/` em `spec.md`
(linhas ~81 e ~123) e em `../issues/01-esqueleto-contrato-e-frontmatter.md`; vale o plano. A linha do Worker 10 também
cita `agents/bin/`; ele disse na volta 2 que segue a faixa 1.

### Não verificado

- Que o obsidian-hybrid-search respeite o bloco gerado no `.gitignore` (fato do Worker 3 no README 0.16.2; não li).
- Que o pacote `yaml` do npm baste para o frontmatter de todas as notas (a escolher na construção; Node não tem YAML).

### Para a próxima volta

- Fechar com o Worker 2 a ordem verificador → checkpoint no fim da resposta e o mod no `-p`.
- Conferir com o Worker 4 se o arquivo de padrões serve ao CLI do LiveSync como está (formato da exclusão dele).
