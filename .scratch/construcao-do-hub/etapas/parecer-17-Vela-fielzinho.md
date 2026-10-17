# Ticket 17 — Vela — parecer independente do Fielzinho

2026-10-17. Ponta conferida: 86c5a88933f55db9a582779a82d2edbbd99a672c. Worktree limpa. Li relatório, costuras 17/16, ticket, spec Worker 7/faixa 7, tela.mjs, fragmentos, mod, testes local/real e biblioteca compartilhada de estado. Não li o parecer do Fiel. Sem subagentes.

## Veredito

**VOLTA por um conserto de código, abaixo.** A integração com a passada real do 16 continua pendente conforme mandato do maestro; não deve ser confundida com o aceite dos exemplos fixos. Fiel fecha o veredito em dupla.

## Conserto 1 — estado parcial vira sincronização em ordem sem nenhuma passada

Evidência própria: `logs/repro-17-fielzinho.mjs` e `logs/repro-17-fielzinho.log`. A sonda usa a biblioteca real do ramo: gravarItem(acervo-peca-sumida) e tirarItem desse item, numa pasta de ensaio. É a mesma sequência suportada por agents/code/bin/verificar-acervo.mjs:29-31. O estado resultante é `{ nivel: "ok", resumo: "tudo em ordem", itens: [] }`, sem passada, pois nenhum processo verificou banco/sincronização.

Ao chamar tela.mjs por fora, obtive:

- início: `Vigia do hub: tudo em ordem (passada às Invalid Date).`
- barra: `hub: em ordem (Invalid Date)`.

Causa: tela.mjs:86-103 e 154-167 confiam na existência de qualquer objeto JSON. O ramo de sucesso não exige uma passada válida; a checagem de antiguidade só roda quando passada existe. A biblioteca compartilhada já permite estados de outros hooks antes da vigia, portanto não é preciso corromper manualmente o arquivo para reproduzir.

Recomendação: distinguir itens locais de uma passada que de fato conferiu a sincronização. Sem passada válida, apresentar estado da sincronização indisponível/não conferido (mantendo os itens relevantes); não mostrar tudo em ordem nem Invalid Date. Aplicar no início e na barra, inclusive à mesma forma recebida pelo MCP. Acrescentar regressão com o estado produzido pela biblioteca, e cobrir data inválida/objeto incompleto sem transformar ausência de prova em ok. O formato combinado admite ausência de passada; não basta exigir que todo produtor invente um horário.

A sonda terminou com saída 0 porque afirma o defeito observado; não é teste de aceite verde. Usa pastaDeEnsaio do ramo, com limpeza pelo ajudante comum. Nenhuma alteração no código do construtor.

## Verificação própria e evidência lida

- `node --test agents/code/test/17-vigia-tela.test.mjs`: 15/15, saída 0. Cobre adaptadores dos três, indisponível sem fontes, reserva MCP com dublê HTTP/SSE, texto velho, notify sem repetição e retorno após ok, fora do hub, barra e comandos dos fragmentos.
- No mod: `claude plugin validate .` passou (aviso apenas de autor ausente); `claude plugin test .`: 2/2. São testes locais, sem sessão de modelo/login.
- `git diff --check 9cc878b..HEAD`: saída 0; árvore limpa depois.
- Li as seis respostas reais versionadas em evidencia-17: divergência cita reuniao.md no início nos três; ausência de fonte aparece como indisponível. O notificador.log do Codex tem uma chamada. O teste real usa notificador dublê.
- Conferência programática de hashes-claude-copilot.json e hashes-codex.json: nenhuma chave de hash mudou, todos os usos com apagado=true. Essas execuções são da Vela; não rodei harness real, Docker ou toast.

## Ressalvas e pendências

1. A passada real do 16 ainda não foi integrada/testada neste ramo; preservar a trava de junção definida no ticket. O teste com arquivo real deve entrar depois do merge, além dos exemplos.
2. Telas interativas do Claude/Copilot e toast real não verificados, conforme relatório. O teste do mod simula process.run e confere a ligação ao status.
3. O resumo reduz qualquer outro_par.situacao diferente de ligado a "a outra máquina não responde" e descarta motivo. Para nao-verificavel, isso pode afirmar mais do que foi apurado. Ressalva por leitura em tela.mjs:98-100/162-164; conferir a representação real do 16 na costura, preservando a incerteza.
4. Notify memoriza id+nivel, não o texto do item. Uma mudança apenas no resumo não avisa de novo; é a assinatura declarada nas costuras. Não trato a passagem de tempo sem mudança de item como nova divergência.

Sem edição de código, spec ou tickets. Enviar ao Fiel para acordo.
