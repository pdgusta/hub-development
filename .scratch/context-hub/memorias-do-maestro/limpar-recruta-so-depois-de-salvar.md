---
name: limpar-recruta-so-depois-de-salvar
description: /clear num recruta só depois de ele salvar o próprio contexto num arquivo; recuperar pelo /resume se errar
metadata:
  node_type: memory
  type: feedback
  originSessionId: ae4d6d00-291c-40f8-a649-1878f444290c
  modified: 2026-10-15T20:47:25.039Z
---

"Limpe o X" do Gustavo quer dizer: primeiro o recruta grava o próprio contexto (estado, decisões, onde está cada coisa,
armadilhas) num arquivo da frente e copia os arquivos de trabalho do scratchpad da sessão para o repositório; **só
depois** o maestro manda o `/clear`.

**Why:** em 2026-10-15 a mensagem dele chegou embaralhada com o aviso de um recruta, e o maestro limpou o UI engineer na
hora; ele: "APÓS ELE SALVAR O CONTEXTO DELE. NÃO ERA PRA LIMPAR AGORA DO NADA". Recuperado com `/resume` (a sessão
anterior fica no disco), depois salvo em `amostra/retomada-ui-engineer.md` e geradores em `amostra/fontes/`.

**How to apply:** antes de qualquer `/clear` em recruta: pedir o arquivo de retomada e a cópia do scratchpad, esperar a
confirmação, então limpar. Mensagem embaralhada: perguntar antes de agir. Relacionado: [[nunca-editar-papel-em-uso]].
