---
name: rodadas-pelo-chat
description: "Com o portal fechado (RAM curta), as rodadas vão pelo Maestri Chat (thread blue) e a resposta dele vale como resposta no portal"
metadata:
  type: feedback
---
2026-10-17 00h24, Gustavo, pelo Maestri Chat (thread blue): "como estou com memória baixa na RAM vou fechar o edge e vou
responder todas as proximas rodadas aqui nesse chat, pode mandar as abertas aqui também. Pode fechar o portal por
enquanto também" e "se quiser pode usar minha resposta como se eu tivesse respondido a pergunta no portal".

**Why:** o Edge e o portal ocupam RAM numa máquina com a memória comprometida no limite.

**How to apply:** enquanto ele não religar o portal, cada rodada continua escrita em `portal/rodadas/` (arquivo dono,
explicação lá), mas a pergunta vai pelo `maestri say` no thread blue, curta, com as opções e a recomendada; a resposta
dele é absorvida no ticket dono como resposta da rodada (`estado: absorvida`, nota "respondida pelo chat"). O portal
para com Ctrl-C no terminal "Portal" e volta com `.\iniciar.cmd` na pasta do portal. Ver [[portal-decide-terminal-conversa]].
