---
name: absorver-e-pesquisar
description: "Quando o Gustavo pede para \"absorver\" um repositório, é pesquisar e julgar se faz sentido, nunca clonar ou instalar"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f28ff107-b444-46f8-a87f-b5c7e669294d
  modified: 2026-10-02T23:13:53.198Z
---

"Absorver o repo X no workflow Matt" quer dizer: abrir um ticket `research` no mapa e pesquisar em
fonte primária se X faz sentido para o hub. Não clonar, não instalar, não rodar.

**Why:** o Gustavo corrigiu em 2026-10-02: "quando eu digo absorver não quero que clone, quero que
pesquise e veja se faz sentido".

A pesquisa começa pelo **objetivo** da ferramenta, nas palavras do autor. Só depois vem a relação com
o hub, e os critérios só entram se essa relação existir ("não faz sentido aplicar os critérios em algo
que você não sabe o objetivo", 2026-10-02).

**How to apply:** ticket `research` + subagente com a skill "research", lendo README e código pelo
GitHub (raw ou API). Ver [[pesquisar-antes-de-explicar]].
