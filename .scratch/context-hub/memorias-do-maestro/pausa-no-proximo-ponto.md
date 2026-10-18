---
name: pausa-no-proximo-ponto
description: "Pausar 'na próxima oportunidade' = deixar o que roda terminar e não despachar nada novo; nunca matar agentes, servidores ou o portal"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9cf09bdc-5377-4368-b47b-ee80c6a55369
  modified: 2026-10-15T18:01:26.040Z
---

Quando o Gustavo pede para pausar "na próxima oportunidade", o maestro deixa terminar o que já está rodando
(subagentes, recrutas, laços) e só não despacha a etapa seguinte. Não interrompe agente no meio da tarefa, não para
laço com arquivo de parada, não derruba o portal nem servidores. Se algo precisar mesmo parar antes de ele sair, o
maestro pergunta.

**Why:** em 2026-10-15 ~15h, o pedido foi "na próxima oportunidade pause tudo e não deixe nenhum agente rodar nada e não
deixe nada rodar em segundo plano". O maestro leu "agora" e forçou tudo: parou dois subagentes no meio de um teste,
interrompeu a Sonda Codex, encerrou o gerador do gateway uma hora antes, derrubou o portal e dois servidores. O
Gustavo: "mas essas ações não são destrutivas? eu falei 'na próxima oportunidade', não que era pra forçar tudo".

**How to apply:** ao receber pedido de pausa, listar o que roda, esperar cada coisa chegar ao fim natural, gravar a
retomada e só então avisar "pausado". Ver também [[retomada-do-maestro]] e [[nunca-editar-papel-em-uso]].
