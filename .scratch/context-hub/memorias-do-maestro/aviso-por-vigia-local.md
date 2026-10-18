---
name: aviso-por-vigia-local
description: "Quando o Gustavo pede que algo 'chegue ao maestro', ele pensa num vigia local que lê arquivo e acorda o maestro, não em mensagem empurrada para o chat"
metadata:
  type: feedback
---
Para o portal avisar o maestro de uma resposta nova, o Gustavo imaginava um **vigia do lado do maestro** (Monitor
observando a caixa local) que acorda o maestro, que então lê o arquivo. O time construiu e testou primeiro o portal
mandando `maestri ask` ao chat (canal A), com defeitos de texto preso e "(enviar)" solto.

**Why:** em 2026-10-14 ele disse: "me entenderam errado [...] É só você colocar um vigia pra ficar aguardando minha
alteração lá e esse vigia te acordar [...] seria só você ler algum arquivo local". Deixou o canal A porque já funcionava.

**How to apply:** para integração entre peças locais, preferir o mecanismo mais simples do lado de quem consome (vigia
em arquivo) antes de empurrar mensagens para o terminal de um agente. Na dúvida sobre o mecanismo, perguntar antes de
construir. Ver [[portal-do-projeto]].
