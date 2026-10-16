# Relatório da etapa 1 (Trilho)

## Estado
- 2026-10-16 ~19h30: ticket 04 pego (worktree `C:\context-hub-wt\ticket-04`, ramo `ticket-04`, a partir de
  `integracao` 69cb383).
- 2026-10-16 ~20h15: ticket 04 pronto; revisão 1 do Fiel: volta, com três consertos (relatório, `.git`, `CLAUDE.md`
  em pasta com ponto).
- 2026-10-16 ~20h40: consertos aplicados (commit f485974), 11 testes verdes; pedida a revisão 2.
- 2026-10-16 ~20h50: revisão 2 do Fiel: passa, com ressalva operacional (o ensaio em `C:\context-hub-ensaio` tem a
  cópia antiga dos scripts; usar os do repositório). Maestro avisado.
- 2026-10-16 ~21h: ticket 04 juntado em `integracao` (merge b68f540) e resolvido. Ticket 05 pego (worktree
  `C:\context-hub-wt\ticket-05`, ramo `ticket-05`).
- 2026-10-16 ~22h: o código mudou para `agents/code/` (rodada "onde mora o código", opção C, do Gustavo).
- 2026-10-16 ~22h40: ticket 05 pronto, `integracao` (3857c98, prova 03) juntada no ramo (b7c99c8), 28 testes verdes;
  pedida a revisão ao Fiel.
- 2026-10-16 ~23h10: revisão 1 do Fiel: volta (YAML em mapa flow corrompido ao trocar `type`; cabeçalho sem fechamento
  tratado como nota sem frontmatter; arquivo em pasta com ponto alterado quando passado direto). Consertado no commit
  71d12c1, 32 testes verdes; pedida a revisão 2.
- 2026-10-16 ~23h40: revisão 2 (Fiel e Fielzinho, em dupla): volta (comentário YAML recuado apagado ao trocar `type`;
  nota arquivada lida pela ficha da pasta ativa). Consertado no commit 817f850, 34 testes verdes; pedida a revisão 3.
- 2026-10-16 ~23h55: revisão 3 (Fiel e Fielzinho): passa, sem pendência obrigatória. Ressalva de integração: as provas
  01 e 02 ainda chamam `agents/test/hub-de-ensaio/montar.mjs`; ao juntar o 05, apontar para `agents/code/test/` e
  repetir as provas. Rebite avisado.
- 2026-10-17 ~0h20: a pedido do Rebite, `integracao` (c8d2267, ticket 02) juntada no ramo e o caminho do `montar` na
  prova 02 trocado (commit a18bbed). 34 testes verdes; prova 02 com 12 PASSA. Rodada 4 do Fiel: passa (o Fielzinho lê
  depois). Rebite avisado.
- 2026-10-17: ticket 05 juntado em `integracao` (0d04985) e resolvido pelo Rebite, 37 testes verdes na junção. Espero
  o próximo ticket do maestro (o 06 espera a prova 02, já juntada).

## Onde mora cada peça (opção C: "quem chama")
- O que um agente chama é skill em `agents/skills/<peça>/`: `agents/skills/nova-iniciativa/`.
- O que só o harness ou o kit roda fica em `agents/code/`: `agents/code/bin/` (verificadores e a biblioteca),
  `agents/code/test/` (testes e o hub de ensaio).

## Ticket 04: o que foi entregue (juntado)
- `AGENTS.md` da raiz: começa pelo bloco `<!-- cabeca:inicio -->` ... `<!-- cabeca:fim -->` (1.604 caracteres hoje;
  limite 2.000). A seção da regra de retomada é da faixa 2 e não está escrita.
- As seis raízes (`clients/`, `operations/`, `initiatives/`, `reference/`, `agents/`, `inbox/`), cada uma com
  `_archive/`; em `agents/`: `skills/`, `machines/`, `maestro/propostas/`, `maestro/uso/`, `frontmatter/`, `code/` e
  `blocks.md` (texto final da rodada 15 do ticket 12, sem mudança). As pastas vazias levam `.gitkeep` (com ponto: não
  replica).
- `.gitignore` da raiz: `.local/`, `**/.secrets/`, `**/.maestri/`, `.obsidian/`, `.obsidian-hybrid-search.db*`. O
  gerador de exclusões (ticket 06) completa.
- `agents/code/test/hub-de-ensaio/montar.mjs [destino]` (padrão `C:\context-hub-ensaio`): copia o esqueleto do ramo,
  grava o conteúdo de `conteudo.mjs` e cria `.git` próprio com um commit. Recusa destino com conteúdo.

## Ticket 05: o que foi entregue (ramo `ticket-05`)
- **Esquemas** em `agents/frontmatter/`: `comum.yml` (campos comuns) e um por tipo, os 28 do catálogo aceito do ticket
  12 (JSON Schema escrito em YAML). Nos tipos com ciclo, `x-status-do-stage` é a tabela `stage` → `status` (decidida
  pelo Gustavo em 2026-10-16, "como está"). Na ficha: `kind`, `size` e `cadence` com os valores da rodada 14 (mais
  `weekly`), `id` em kebab-case, `blocks` só com os 16 blocos.
- **`paths.yml`**: caminho → tipo, a primeira regra vence. Sem frontmatter do hub (`tipo: null`): `AGENTS.md`,
  `SKILL.md`, todo `agents/skills/**` e `agents/code/**`. Caminho fora das regras (ex.: `agents/blocks.md`,
  `README.md`, `clients/<cliente>/x.md`, `operations/<op>/x.md`): só os campos comuns, sem `type`, com aviso (decidido).
- **Verificador** `agents/code/bin/verificar-frontmatter.mjs` (assinatura abaixo), com a lógica em
  `agents/code/bin/lib/frontmatter.mjs`, que o `verificar-hub` e a skill também usam. YAML pelo js-yaml 4.1.0 copiado em
  `agents/code/bin/vendor/js-yaml/` (um arquivo, MIT, integridade do npm em `ORIGEM.txt`), sem `npm install`; o
  esquema CORE deixa datas como texto. Validador próprio do subconjunto de JSON Schema usado (`required`,
  `properties`, `enum`, `type`, `pattern`, `minLength`, `minimum`, `format: date`, `items`).
- **O que ele completa** (só o dedutível; escolha 14): `type` (pelo caminho, trocado se errado), `initiative` (o `id`
  da ficha, ou `<cliente>-<iniciativa>` / `<iniciativa>`; só em `clients/<c>/<i>/` e `initiatives/<i>/`, escolha 19;
  `operations/` não conta, decidido), `title` do núcleo pela ficha ("Retomada · <nome>", "Diário AAAA-MM · <nome>"),
  `month` do log, `open_count` (linhas `- [ ]`), `last_decision` (última data em `decisions.md`), `status` pelo
  `stage`, `created` (data de criação do arquivo), `updated` (data da última mudança, se a nota diz mais velha), no
  `inbox/` o `title` (primeiro `#` ou nome do arquivo) e `status: rascunho`, no `index.md` `folder`, `title`,
  `summary: auto`, `local: false`. O `status` dos tipos sem ciclo (núcleo incluso) é de quem escreve.
- **Guarda** (escolha 14): troca só as linhas dos campos deduzidos (o resto do arquivo fica igual, CRLF preservado);
  relê o arquivo logo antes de gravar e, se mudou, refaz sobre o texto novo (até três vezes; depois recusa sem gravar).
  Antes de gravar, o novo frontmatter é relido: se não volta exatamente com os campos esperados (ex.: mapa flow
  `{...}`), recusa sem gravar ("escreva um campo por linha"). Cabeçalho que abre `---` e não fecha é YAML inválido.
  Comentário recuado depois do campo trocado fica; comentário na mesma linha do campo trocado recusa sem gravar.
  A janela entre a releitura e a gravação continua não verificada. `HUB_VERIFICADOR_PAUSA_MS` só existe para o teste.
- **Nota arquivada** (`<raiz>/_archive/AAAA-MM-DD--<nome>/...`): vale o esquema do caminho de origem mais
  `archived_at`; o `type` fica o de origem. A `initiative` e o `title` do núcleo saem da ficha arquivada (a que está
  na mesma pasta `_archive/...`), nunca da pasta ativa homônima.
- **Skill "nova iniciativa"**: `agents/skills/nova-iniciativa/SKILL.md` e `nova-iniciativa.mjs`. Cria a pasta, o núcleo
  de seis arquivos e as pastas dos blocos; não cria o `AGENTS.md` da iniciativa (escolha 20). Confere tudo antes de
  criar (valor fora do catálogo: nada é criado). Rodar de novo só cria o que falta; nada existente é regravado (`wx`).
- **`verificar-hub`** passa a conferir o frontmatter de todo `.md` do hub (sem gravar): recusa o que exige juízo,
  avisa o resto.
- O `README.md` da raiz ganhou os campos comuns, para o `verificar-hub` passar no próprio repositório. Se ele fica no
  hub é decisão do maestro (a raiz decidida tem só `AGENTS.md` e as seis raízes; ele gera aviso).

## Assinaturas
- `node agents/code/bin/verificar-hub.mjs <raiz>` → 0 em ordem, 1 com recusa; linhas `recusa: ...` e `aviso: ...`.
  Recusa: falta de `AGENTS.md`, raiz ou `_archive/`; cabeça ausente ou acima de 2.000 caracteres; `.git` ausente ou
  falso (worktree vale); `CLAUDE.md`/`CLAUDE.local.md` no hub (inclusive pastas com ponto, menos o `.git`) ou acima;
  nota fora do esquema (`recusa: <caminho>: ...`). Avisa: outra entrada na raiz, caminho sem tipo. Um workspace do
  Maestri dentro do hub seria recusado (ticket 36; o maestro mantém a recusa).
- `node agents/code/bin/verificar-frontmatter.mjs [--raiz <hub>] [--corrigir] <arquivo|pasta>...` → 0 se nenhuma
  nota recusa, 1 se alguma. Linhas: `recusa: <caminho>: <falta>; <falta>`, `completou: <caminho>: <campos>`,
  `aviso: <caminho>: ...` (sem `--corrigir`, `aviso: ...: completaria <campos>`). Pastas: só `.md`, sem as com ponto.
  Caminho com ponto em qualquer parte (`.secrets/`, `.maestri/`) fica de fora também passado direto e no `--checar`:
  o arquivo nem é lido, nada é gravado nem cobrado (no `--checar`, o conteúdo da entrada é ignorado). Raiz: `--raiz`, senão `HUB_ROOT`, senão a primeira pasta acima com `agents/frontmatter/paths.yml`. Arquivo fora do
  hub: nada.
- `node agents/code/bin/verificar-frontmatter.mjs --raiz <hub> --checar <caminho no hub>` com o conteúdo proposto na
  entrada padrão: valida como se o dedutível já estivesse completo, não grava; para o hook do ticket 14 e o MCP.
- `node agents/skills/nova-iniciativa/nova-iniciativa.mjs --em clients|initiatives [--cliente <c>] --nome "<Nome>"
  --kind <k> --size <s> --stage <st> [--blocos a,b] [--cadence c] [--aliases a,b] [--pasta <slug>] [--proximo "..."]
  [--raiz <hub>]` → linhas `criou: ...` / `já existe: ...`, ou `recusa: ...` e saída 1.

## Hub de ensaio
- Novo a qualquer hora: `node agents/code/test/hub-de-ensaio/montar.mjs <pasta vazia>`. Os testes montam um por caso
  na pasta temporária.
- **`C:\context-hub-ensaio` está velho** (cópia dos scripts do commit 84aa46a, antes dos consertos do 04 e sem o 05):
  não usar. A remoção foi barrada pela checagem de segurança; quem pode apagar é o Gustavo (só essa pasta).
- Duas iniciativas inventadas: `clients/aurora/migracao-de-tenant/` (cliente inventado) e `initiatives/context-hub/`,
  cada uma com o núcleo de seis arquivos (`log/2026-10.md`) e `title` "<Arquivo> · <nome>".
- Mais: `research/` nas duas (`busca-por-paráfrase.md`, com acento no nome); `inputs/diagrama-do-tenant.png` (PNG 8×8)
  com `inputs/index.md`; `.secrets/leia-me.txt` aninhado (fora do git); `initiatives/context-hub/labs/` com `index.md`
  `local: true`; `reference/sincronizacao/conflitos-de-edicao.md`. Todas as notas passam no verificador.

## Como provar
```
cd C:\context-hub-wt\ticket-05
node --test "agents/code/test/*.test.mjs"
node agents/code/bin/verificar-hub.mjs .
```
34 testes: 11 do 04 (`04-esqueleto.test.mjs`), 19 do verificador (`05-frontmatter.test.mjs`) e 4 da skill
(`05-nova-iniciativa.test.mjs`). No Node 24, `node --test <pasta>` falha; use o padrão entre aspas. A prova 03 (em
`provas/`) não depende de nada daqui; o `instalar.test.mjs` dela segue verde depois da junção.

## Fora (com o porquê)
- **Ticket 27** (decidido pelo Gustavo): criar e manter `index.md`, corrigir links `par://`, avisar três parecidos em
  `other/` e o registro do verificador no fim de resposta dos harnesses.
- **Ticket 06:** a exclusão do que é `local: true`. Hoje `labs/ensaio-do-banco.md` (pasta `local: true`) está no git do
  ensaio.
- **Ticket 14:** o hook antes da gravação, que vai chamar `--checar`. **Ticket 09/10:** o MCP validar igual.
- O aceite de ponta a ponta com `claude -p` (spec da faixa 1) depende do fim de resposta, do ticket 27.
- A conferência "sem `CLAUDE.md`" como passo do instalador fica com o kit de par (tickets 23 e 24).

## Para as próximas etapas
- Esquemas e catálogo: `agents/frontmatter/` (`paths.yml`, `comum.yml`, `<tipo>.yml`).
- Validar conteúdo proposto: `--checar` (acima). Completar no disco: `--corrigir`.
- Bloco da cabeça: entre `<!-- cabeca:inicio -->` e `<!-- cabeca:fim -->`, no começo do `AGENTS.md`.
