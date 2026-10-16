---
tipo: resposta
rodada: 2026-10-15-arquitetura-de-pastas-e-frontmatter-r20
ticket: 12
enviada: 2026-10-15T18:15:15-03:00
envio: 70824740-e39a-49df-b73f-9f372b107cbc
estado: lida
substitui:
---

# Resposta: Links para o que só existe numa máquina

## Em que casos o link leva o par na frente
escolha: A, Só quando o destino não replica. Para tudo que replica, link interno normal com o caminho a partir da raiz do cofre ("Absolute path in vault"), que o Obsidian atualiza ao renomear. Para destino numa pasta `local: true`, numa pasta com ponto ou fora do hub, a forma `par://<par_id>/<caminho a partir da raiz do hub>`, sem letra de unidade (cada par sabe onde fica a própria raiz). O verificador confere pelo cartão das pastas e corrige sozinho nos dois sentidos, avisando o agente. De `.secrets/`, só o nome do arquivo, nunca o conteúdo (a recomendada)

## Algo mais?
em branco
