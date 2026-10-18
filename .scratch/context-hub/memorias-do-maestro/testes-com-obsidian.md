---
name: testes-com-obsidian
description: "em testes com o Obsidian na máquina do Gustavo, capturar só o monitor principal e nunca automatizar mouse ou teclado; clique é pedido a ele"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8a0a694f-68fe-471b-8e15-59922a4a2a8d
  modified: 2026-10-13T03:40:56.973Z
---

Nos testes do LiveSync (montagem em `C:\Projetos\spike-livesync\`), o Obsidian fica no monitor
principal e o Gustavo usa o segundo monitor para outras coisas. Capturar só o monitor principal
(`tela.ps1`), abrir cofres por `obsidian://open?vault=...` e fechar janela por WM_CLOSE (`janela.ps1`).
Nunca mover mouse nem mandar tecla: quando um modal exige clique (o "Config Doctor" abre depois de
atualizar o plugin e para o sync daquele cofre), pedir ao Gustavo no chat, dizendo a janela e o botão.

**Why:** 2026-10-13, a primeira captura de tela inteira pegou o segundo monitor dele; automatizar
cliques ali podia cair no que ele estava fazendo. Ele clicou nos modais quando pedido, sem objeção.

**How to apply:** qualquer teste que precise ver ou operar o Obsidian. Segredos do spike ficam no
`.env`, lido só por dentro dos scripts (`cdb.py`); o guarda de segredos bloqueia ler o `.env` no shell.
Ver [[headless-edge-para-qa-visual]].
