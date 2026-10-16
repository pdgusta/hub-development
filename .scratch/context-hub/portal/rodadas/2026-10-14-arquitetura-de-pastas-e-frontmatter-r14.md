---
titulo: O que entra em cada bloco, a ficha, segredos e scripts
ticket: 12
aberta: 2026-10-14
estado: absorvida
---

Só o que não depende da camada de busca. A rodada "Índices e busca, juntos" ficou suspensa até a busca ser
decidida, junto com o texto extraído dos anexos e o campo de idioma.

Em que esta rodada se apoia, já decidido:
- as raízes e os níveis do hub (rodadas 3 a 6);
- o núcleo de seis arquivos e os blocos com nome único (rodada 11);
- o catálogo `agents/blocks.md` com a skill "nova iniciativa" e o bloco `other/` (rodada 12);
- tudo replica entre as duas máquinas, inclusive cliente (rodada 3);
- o hub tem um `.git` na raiz, que vai ao GitHub como cópia de segurança ("Revisão do sync e da divergência").

O SOC STRATA ficou fora desta rodada: "Workloads piloto" o deixou fora do hub por ora.

## O que entra em cada bloco
id: blocos
tipo: proposta

```json
{
  "colunas": ["bloco", "entra", "não entra"],
  "linhas": [
    {"id": "inputs", "bloco": "inputs/", "entra": "o que veio de fora: kickoff, PDF e planilha do cliente, e-mails, exports", "não entra": "o que você produziu a partir disso (vai para research/ ou deliverables/)"},
    {"id": "research", "bloco": "research/", "entra": "levantamento, pesquisa, análise, discovery, comparação de opções", "não entra": "a decisão tomada (vai para decisions.md) e o desenho final (design/)"},
    {"id": "design", "bloco": "design/", "entra": "arquitetura, especificação, desenho da solução, o detalhe de uma decisão grande", "não entra": "planos de execução (plans/)"},
    {"id": "plans", "bloco": "plans/", "entra": "planos, roteiros, tickets e backlog maior que o tasks.md", "não entra": "a pendência simples do dia (tasks.md)"},
    {"id": "deliverables", "bloco": "deliverables/", "entra": "o que é entregue, com versão no nome: documentos, relatórios, apresentações", "não entra": "rascunhos de trabalho (research/ ou design/)"},
    {"id": "evidence", "bloco": "evidence/", "entra": "prints, logs e exports que provam um fato", "não entra": "imagens de documento entregue (deliverables/)"},
    {"id": "runs", "bloco": "runs/", "entra": "trabalho de agentes: briefs, handoffs, execuções e revisões, uma subpasta por execução", "não entra": "a personalização do Maestri (maestro/)"},
    {"id": "tools", "bloco": "tools/", "entra": "scripts de apoio desta iniciativa", "não entra": "código de produto, que mora no repositório próprio"},
    {"id": "procedures", "bloco": "procedures/", "entra": "runbooks, SOPs, passo a passo de operação", "não entra": "o registro de cada caso (cases/)"},
    {"id": "cases", "bloco": "cases/", "entra": "um arquivo por caso ou incidente", "não entra": "o procedimento genérico (procedures/)"},
    {"id": "queries", "bloco": "queries/", "entra": "consultas salvas (KQL, SQL) e seus resultados de referência", "não entra": "scripts (tools/)"},
    {"id": "knowledge", "bloco": "knowledge/", "entra": "base de conhecimento própria da iniciativa", "não entra": "conhecimento geral, que vai para a raiz reference/"},
    {"id": "notes", "bloco": "notes/", "entra": "anotações de estudo", "não entra": "o material do curso (inputs/)"},
    {"id": "labs", "bloco": "labs/", "entra": "exercícios e ambientes de laboratório", "não entra": "senhas (ver a pergunta dos segredos)"},
    {"id": "other", "bloco": "other/", "entra": "o que não cabe em nenhum bloco; com três parecidos, propõe-se um bloco novo", "não entra": "o que cabe num bloco existente"}
  ],
  "pode": ["editar", "reordenar", "adicionar", "remover"]
}
```

Edite o texto de qualquer linha, troque a ordem, acrescente ou tire blocos. Isso vira o `agents/blocks.md`.

## Os campos da ficha (`initiative.md`)
id: ficha
tipo: proposta

```json
{
  "colunas": ["campo", "valores", "de onde vem"],
  "linhas": [
    {"id": "id", "campo": "id", "valores": "kebab-case, estável", "de onde vem": "vault, igual"},
    {"id": "title", "campo": "title", "valores": "nome usado fora (Loop, cliente)", "de onde vem": "vault, igual"},
    {"id": "kind", "campo": "kind", "valores": "projeto de cliente, investigação, operação contínua, produto, frente de planejamento, spike, estudo, referência", "de onde vem": "novo: o tipo de trabalho que escolhe a pilha de blocos"},
    {"id": "size", "campo": "size", "valores": "change, initiative, project, study, idea", "de onde vem": "vault: o type de hoje, que mede tamanho"},
    {"id": "status", "campo": "status", "valores": "doing, backlog, on-hold, done, archived", "de onde vem": "vault, igual"},
    {"id": "blocks", "campo": "blocks", "valores": "lista dos blocos em uso", "de onde vem": "novo: o verificador e o mapa do AGENTS.md leem daqui"},
    {"id": "workspace", "campo": "workspace", "valores": "onde mais o trabalho vive (Loop, repositório)", "de onde vem": "vault, igual"},
    {"id": "parent", "campo": "parent", "valores": "id da iniciativa mãe", "de onde vem": "vault, igual"},
    {"id": "related", "campo": "related", "valores": "ids relacionados", "de onde vem": "vault, igual"},
    {"id": "cadence", "campo": "cadence", "valores": "monthly, quarterly, none", "de onde vem": "vault, igual"},
    {"id": "updated_at", "campo": "updated_at", "valores": "AAAA-MM-DD", "de onde vem": "vault, igual"}
  ],
  "pode": ["editar", "reordenar", "adicionar", "remover"]
}
```

Saem do vault: `emoji` (fica derivado do `size`) e `model` (hybrid, internal, external). O `model` dizia se o
vault guardava tudo ou só o localizador; no hub, o trabalho mora na iniciativa, e o que vive fora vai no
`workspace`. O cliente e a raiz não viram campo: o caminho já diz (`clients/voegol/…`).

## Onde ficam senhas e tokens
id: segredos
tipo: escolha
recomendada: A

- A: Nunca no hub. Ficam no KeePass que você já usa (visto no TRF3); o hub guarda só o nome da entrada, e o script lê a senha de uma variável de ambiente da máquina
- B: Numa pasta com ponto, `.secrets/`, dentro da iniciativa, fora do `.git`, contando que o LiveSync ignora pastas com ponto
- C: No arquivo `.env` de cada spike, como hoje, só com o `.gitignore`

Por que A: tudo no hub replica para a outra máquina e para o banco, e o `.git` da raiz vai ao GitHub. A B depende
de o LiveSync ignorar pastas com ponto, e o teste "Disco e banco sem o Obsidian" viu **pastas com ponto aninhadas
vazarem** para o banco. A C é o que existe hoje (`credenciais.txt`, `token-*.txt`, `.env` nas pastas de spike) e
replicaria tudo. Não verificado: um jeito de o agente ler o KeePass direto; por isso a variável de ambiente.

## Scripts de apoio
id: scripts
tipo: escolha
recomendada: C

- A: Sempre em `tools/`, dentro da iniciativa no hub
- B: Sempre num repositório próprio, fora do hub, mesmo quando é um script só
- C: Em `tools/` enquanto são scripts de apoio; viram repositório próprio quando ganham testes, dependências ou uso fora da iniciativa

Por que C: um script de uma vez (como os `Scripts/` da VOEGOL, hoje fora de git) fica perto do trabalho, versionado
pelo `.git` da raiz. Quando vira ferramenta de verdade, como o `tools/` do SBF com 38 arquivos Python, ganha
repositório, como o código de produto já faz.

## Algo mais?
id: algo-mais
tipo: texto
