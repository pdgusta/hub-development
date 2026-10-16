---
titulo: Índices, anexos e títulos, com a busca decidida
ticket: 12
aberta: 2026-10-15
estado: absorvida
---

A rodada "Índices e busca, juntos" ficou suspensa porque você quis decidir a busca primeiro. A "Camada de busca" foi
decidida hoje: o obsidian-hybrid-search, com o modelo arctic local, no disco de cada máquina, lendo os `.md`. Esta
rodada refaz aquela pergunta e junta o que ela deixou pendente: onde mora o texto dos anexos e o que o frontmatter
precisa para a busca achar bem.

Em que esta rodada se apoia, já decidido:
- a porta de entrada é a busca; um índice só existe onde a busca não basta ("Lições do vault");
- o frontmatter só leva o que a busca ou o contrato usam ("Lições do vault");
- o núcleo de seis arquivos (`initiative.md`, `retomada.md`, `tasks.md`, `decisions.md`, `context.md`, `log/AAAA-MM.md`),
  os blocos com nome único, o catálogo `agents/blocks.md`, o bloco `other/` e os campos da ficha (rodadas 11, 12 e 14);
- um verificador sem IA roda no fim de cada resposta (rodada 12). Onde o fim da resposta roda em cada harness é do
  ticket "Acesso dos agentes: decisão", em curso: no Claude Code, um mod;
- o campo de idioma **sai**: a busca usa um analisador só para português e inglês ("Camada de busca").

O que o código do obsidian-hybrid-search 0.16.2 mostra (lido no pacote instalado na bancada e no README):
- **ele só lê `.md`.** Prints, PDF, Word, planilha, `.csv`, `.txt`, logs e scripts não entram na busca;
- **o título pesa muito:** vem do campo `title` do frontmatter ou, sem ele, do nome do arquivo; conta 10 vezes mais
  que o texto na busca por palavra, os `aliases` contam 5 vezes, e o título vai junto de cada trecho na busca por
  sentido. **O caminho da pasta não entra na busca por palavra;**
- ele filtra por pasta e por campo do frontmatter, inclusive listas (`blocks: runs`), e lista as notas de uma pasta
  sem varrer o disco. Os campos `kind`, `status` e `blocks` da ficha viram filtros;
- ele respeita o `.gitignore`, então o `.secrets/` também fica fora da busca;
- nota com YAML inválido fica fora do índice: 12 de 124 na bancada, por dois-pontos sem aspas no `title`;
- o índice é o arquivo `.obsidian-hybrid-search.db` na raiz do hub, um por máquina. A construção o tira do git e do
  LiveSync.

## Como índices e busca se dividem
id: indices-e-busca
tipo: escolha
recomendada: A

- A: A busca é a porta para achar; o catálogo de blocos e o mapa do `AGENTS.md` da iniciativa dizem onde gravar. O `index.md` existe só na pasta que guarda arquivo que a busca não lê (prints, scripts, `.csv`, `.txt`, logs, zip), com uma linha por arquivo dizendo o que é. Pasta só de `.md`, mesmo que cresça, não tem `index.md`. O verificador do fim da resposta inscreve como "sem descrição" o arquivo que a busca não lê e não tem linha, e avisa a nota com YAML que a busca rejeitaria
- B: Igual à A, mas o `index.md` existe também em toda pasta que cresce, mesmo só com `.md` (a sua correção na rodada "Como o agente acha tudo"), como sumário para navegar sem buscar
- C: Só a busca, sem `index.md`. O verificador cobra só o texto dos anexos (pergunta abaixo) e o YAML válido; prints, scripts, `.csv` e `.txt` ficam invisíveis para a busca

Por que A: é o "índice só onde a busca não basta" da lição do vault. A linha de um print vira texto que a própria busca
lê, então o `index.md` alimenta a busca em vez de concorrer com ela, e ainda traz outras palavras, que ajudam nas
perguntas feitas com sinônimos. O seu pedido principal, nenhum arquivo sem nada que o referencie, fica atendido por
mecanismo: todo `.md` está no índice da busca, e todo outro arquivo ganha a linha, nem que seja "sem descrição". Para
ver o que há numa pasta que cresce, como `runs/`, a busca já lista as notas dela por filtro de pasta, sem um sumário
mantido à mão.

## Onde mora o texto extraído dos anexos
id: texto-dos-anexos
tipo: escolha
recomendada: A

- A: Num arquivo irmão, ao lado do anexo: `proposta-v2.pdf` ganha `proposta-v2.pdf.md`, com `title` (o nome do documento), `source` (o arquivo de origem) e `extractor` (Docling ou pandoc, com a versão) no frontmatter. Vale para PDF, Word, PowerPoint, Excel e HTML. Replica para a outra máquina e vai ao git com o resto. O anexo com texto dispensa linha no `index.md`
- B: Numa pasta `extracted/` dentro da iniciativa, que repete o caminho de cada anexo (`extracted/inputs/proposta-v2.pdf.md`), com o mesmo frontmatter da A. Os blocos ficam só com os originais; a busca aponta para o original pelo campo `source`
- C: Fora da vista que replica: cada máquina extrai o texto sozinha, numa pasta fora do git e do LiveSync, e a busca é configurada para lê-la (`OBSIDIAN_INCLUDE_PATTERNS`). Nada dobra no banco nem no GitHub, mas cada máquina gasta o tempo do Docling nos mesmos arquivos, e o texto não tem histórico

Por que A: o resultado da busca leva direto ao original, que é o mesmo nome sem o `.md` final; o verificador acha o
anexo sem texto só olhando a pasta; e nada muda na regra "tudo replica". O texto extraído é pequeno perto do PDF ou
da planilha. Em B, o agente precisa de um pulo a mais; em C, a mesma extração roda duas vezes e pode sair diferente
em cada máquina. **Não verificado:** os idiomas do OCR do Docling para PDF escaneado. Quando e quem dispara a extração
fica para a construção.

## O título das notas do núcleo e os nomes alternativos da iniciativa
id: titulos
tipo: escolha
recomendada: A

- A: Os arquivos do núcleo ganham `title` com o nome da iniciativa ("Retomada · VOEGOL cross-tenant", "Decisões · VOEGOL cross-tenant"). A skill "nova iniciativa" os escreve, e o verificador completa o que faltar, como o `log/` de um mês novo, a partir do `title` da ficha. A ficha ganha o campo `aliases`: siglas, o nome no Loop, o nome antigo no vault
- B: Só a ficha ganha `aliases`. Os arquivos do núcleo ficam sem `title`, e o agente que já sabe a iniciativa filtra a busca pela pasta dela
- C: Nada muda: a ficha fica com os campos da rodada 14, e os arquivos do núcleo, sem frontmatter

Por que A: as 30 iniciativas terão 30 `retomada.md`. Sem `title`, todas têm o título "retomada", e o nome da
iniciativa, que só aparece no caminho, fica fora da busca por palavra. Com o `title`, uma pergunta como "onde parou o
cross-tenant" cai no título, a parte que mais pesa, e o título vai junto de cada trecho na busca por sentido. Os
`aliases` acham a iniciativa pelo nome que você usar na hora. Os dois campos são usados pela busca, como a lição do
vault pede. Em B, a busca sem filtro, que é a porta, continua vendo 30 notas com o mesmo título.

## Algo mais?
id: algo-mais
tipo: texto

Ficam fora desta rodada: onde o fim da resposta roda no Codex e no Copilot, que é do ticket "Acesso dos agentes:
decisão", em curso; e quando a extração dos anexos roda, que é da construção. O SOC STRATA segue fora do hub por ora
("Workloads piloto"). Esta rodada não tem carta: são escolhas simples.
