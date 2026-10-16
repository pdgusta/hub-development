# Brief do Designer: o esboço da árvore final do hub (ticket 12)

Do maestro, 2026-10-15. Ticket 12 "Arquitetura de pastas e frontmatter", rodada 17, escolha B do Gustavo: "antes de
resolver, o Designer faz um esboço da árvore final com notas de exemplo, numa carta para você aprovar".

## O que está decidido (fontes)

- A árvore inteira, o núcleo, os blocos, a ficha, os índices, os anexos, os segredos: `rascunhos/12-answer-rascunho.md`,
  seção 2 (rascunho do Answer; vale o que está decidido nele).
- O frontmatter de cada tipo de nota e como a máquina o impõe: `rascunhos/12-frontmatter-proposta.md`, com o que o
  Gustavo escolheu na rodada 18 (`issues/12-arquitetura-de-pastas-e-frontmatter.md`, comentário de 17:44): o catálogo
  inteiro **mais um `status` comum em toda nota** (rascunho, em uso, superada); imposição em camadas (hook antes da
  gravação, MCP do banco, verificador no fim) **sem o Templater**; o `index.md` é o cartão da pasta (`summary: auto`,
  `local: true|false`), criado pelo verificador a partir de 10 arquivos ou de arquivo que a busca não lê.
- Pasta local: `index.md` com `local: true` (rodada 17, B); o que tem ponto no nome também fica numa máquina só.

## A carta

- Arquivo: `.scratch/context-hub/prototipos/prototipo-12-arvore.html`.
- **Diagrama no centro:** a árvore do hub de bater o olho, da raiz (`AGENTS.md` e as seis raízes) até uma iniciativa de
  cliente de exemplo, `clients/voegol/cross-tenant/`, com o núcleo, quatro ou cinco blocos em uso (entre eles `work/`,
  `runs/`, `inputs/` com um anexo e o seu `.pdf.md`), o `.secrets/` e um `index.md` de pasta que cresceu. Cite iniciativas
  só pelo nome; nada de dado pessoal.
- **Notas de exemplo:** ao clicar num arquivo, ele abre com o frontmatter real do tipo (preenchido com valores
  plausíveis) e duas ou três linhas de corpo. Marque, em cada campo, quem o preenche: a máquina (derivado do caminho) ou
  quem escreve (agente ou Gustavo). Pelo menos: a ficha `initiative.md` com `aliases`, a `retomada.md`, um `run`, um
  `work` (handoff), um `input` com o anexo e o texto extraído, um `index.md` como cartão da pasta e uma pasta local.
- **O mecanismo, num quadro pequeno:** de onde vem o tipo (o caminho), onde mora o esquema (`agents/frontmatter/`), e as
  três camadas que impõem o padrão (antes da gravação, no MCP, no fim da resposta).
- Pouco texto, como a Mesa de mapas elogiada; dados reais e em escala acertaram na carta `prototipo-12-ritmos`.

## Cadastro

Entrada nova no `portal/cartas.json`: `id: "prototipo-12-arvore"`, `titulo` curto, `arquivo`, `pasta`
(`.scratch/context-hub/prototipos`), `ticket: "12"`, `proposito` em uma frase, `decisao: "em aberto: aprovar o esboço
da árvore final ou recusar com o que mudar"`, `situacao: "vigente"`, `mestra: false` e **`"pede_veredito": true`**. Não
abra rodada: a rodada é do maestro.

## Regras

- Capturas com o Edge sem cabeça: perfil próprio (`--user-data-dir` único); mate só os `msedge` desse perfil, nunca
  `taskkill` por nome.
- Confira a carta no portal (`http://127.0.0.1:8770/`) em 1280 e 320 px.
- Ao terminar: `maestri ask "Claude Code" "pronto: <caminho da carta>"`.
