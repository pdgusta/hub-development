# Markdown: vista ou fonte da verdade

Type: grilling
Status: resolved

## Question

O Markdown é a fonte da verdade do hub ou só a vista do Gustavo? Se a verdade passar a outra forma
(um SQLite, por exemplo), o que muda no sync, na divergência, na edição pelo Obsidian e no que as
camadas de busca precisam cumprir?

Reabre a Q5 do mapeamento ("Toda gravação termina como `.md` no disco"), a definição de "Context hub"
no `GLOSSARY.md` e o R1 de "Varredura de candidatas à camada de busca". Tickets apoiados nessa premissa:
"Ponto de encontro do sync", "Sync que não depende de quem gravou", "Divergência e edição concorrente",
"Contrato file-first: zonas e checkpoint", "Camada de busca", "Como os agentes gravam no hub".

## Comments

- 2026-10-04 (vinda de "Camada de busca", rodada 3), Gustavo: "Eu estou aberto ao context-hub ser
  algo diferente de um diretório de markdowns (um sqlite, por exemplo). O markdown é o que eu quero
  que seja disponibilizado para eu ver o context-hub. Ou seja. Eu humano vejo o hub no markdown, mas o
  ideal é o agente ver pela forma mais adequada possível (que pelo visto não é markdown)". Ele não
  queria que "Markdown é a fonte" tivesse virado critério da busca.
- Fato para a decisão: o git não junta arquivo binário linha a linha. O driver `binary` *"Keep the
  version from your branch in the work tree, but leave the path in the conflicted state"*
  ([gitattributes](https://git-scm.com/docs/gitattributes)). Um SQLite como verdade, sincronizado
  pelo git, transforma toda edição nas duas máquinas em conflito do arquivo inteiro.
- Rodada 1 em `respostas.md` (R4).

## Answer

Decidido pelo Gustavo em 2026-10-04 (R4 em `respostas.md`), contra a recomendação (a).

- **A verdade do hub mora num banco** (a forma ainda não está escolhida; SQLite foi só exemplo). O
  agente lê e grava pela forma mais adequada a ele, não pelo `.md`.
- **O Markdown é a vista do Gustavo, e é editável:** ele edita o `.md` (no Obsidian) e a edição
  volta para o banco. A vista é de mão dupla.
- Cai a Q5 do mapeamento ("toda gravação termina como `.md` no disco") e a definição de "Context
  hub" no glossário, que foi refeita.
- **Fica para os próximos tickets:**
  - como o banco sincroniza entre as duas máquinas, já que o git não junta binário;
  - como a vista volta ao banco sem criar duas casas para a mesma informação (lição "cada informação
    tem um lugar só" de "Lições do vault");
  - se o agente ainda pode editar o `.md` direto no disco (critério 3 do destino).
- **Em revisão por causa desta decisão:**
  - "Ponto de encontro do sync";
  - "Sync que não depende de quem gravou";
  - "Divergência e edição concorrente";
  - "Camada de busca" e as pesquisas dela;
  - "Como os agentes gravam no hub";
  - "Arquitetura de pastas e frontmatter do hub".
