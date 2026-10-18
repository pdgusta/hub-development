---
name: maestri-ask-sem-barra-invertida
description: "em maestri ask, caminho com barra invertida perde caracteres (\\t vira tabulação); escrever caminhos com barra normal"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2307bd59-c48b-45de-b1b8-1227bb2316d5
  modified: 2026-10-16T23:02:24.284Z
---

Em `maestri ask`, escreva caminhos com barra normal (`agents/code/test/...`), nunca com barra invertida.

**Why:** em 2026-10-16 o aviso do Rebite à Brasa com `agents\code\test\...` chegou como `agents\code    est\...`: o `\t` virou tabulação. O próprio maestro repetiu o erro na mensagem dele.

**How to apply:** em toda mensagem a recruta ou ao maestro, troque `\` por `/` nos caminhos; o Windows aceita os dois. Ver também [[ask-a-recruta-ocupado]].
