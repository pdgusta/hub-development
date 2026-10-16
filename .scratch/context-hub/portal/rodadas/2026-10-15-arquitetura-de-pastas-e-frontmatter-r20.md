---
titulo: Links para o que só existe numa máquina
ticket: 12
aberta: 2026-10-15
estado: absorvida
---

Você previu bem: com pastas `local: true` e pastas com ponto, vão surgir notas que apontam para um arquivo que a outra
máquina não tem. E perguntou em que casos usar uma forma com o par na frente (`<par_id>/<pasta_raiz>/...`).

**O que pesa (fontes do Obsidian):**
- O Obsidian tem três formatos de link interno: "Shortest path when possible", "Relative path to file" e **"Absolute
  path in vault"** ("uses the full path from the vault root"), e atualiza os links sozinho quando um arquivo é renomeado
  ("Automatically update internal links"). Isso só vale para link interno normal.
- Um link interno normal funciona igual nas duas máquinas para tudo que replica, e a busca e os agentes o seguem.
- Para o que não replica, o link normal quebra na outra máquina sem dizer por quê; o leitor nem sabe em que máquina
  procurar. É aí que o par na frente ajuda.
- Letra de unidade (`C:/...`) é frágil: a raiz do hub ainda está em aberto (`C:\context-hub` ou WSL), e cada par pode ter
  a sua.

O par é o nome da máquina no perfil dela em `agents/machines/<máquina>.md`.

## Em que casos o link leva o par na frente
id: links-por-par
tipo: escolha
recomendada: A

- A: Só quando o destino não replica. Para tudo que replica, link interno normal com o caminho a partir da raiz do cofre ("Absolute path in vault"), que o Obsidian atualiza ao renomear. Para destino numa pasta `local: true`, numa pasta com ponto ou fora do hub, a forma `par://<par_id>/<caminho a partir da raiz do hub>`, sem letra de unidade (cada par sabe onde fica a própria raiz). O verificador confere pelo cartão das pastas e corrige sozinho nos dois sentidos, avisando o agente. De `.secrets/`, só o nome do arquivo, nunca o conteúdo
- B: Sempre com o par na frente, em todo link: uniforme, mas o Obsidian deixa de reconhecer os links (sem backlinks, sem atualizar ao renomear, sem grafo), e a busca não os segue
- C: Nunca: só links internos normais; o destino que não replica fica descrito em texto ("no notebook, em ..."), e o verificador avisa o link quebrado

## Algo mais?
id: algo-mais
tipo: texto
