# Revisão do marco 7 — Prumo, 2026-10-14

**APROVADO: canal A de aviso ao maestro.** Sem achados bloqueantes ou importantes nesta revisão. Este aceite não antecipa o marco 8 nem a conferência final do portal.

Conferi `nucleo/aviso.py`, ligação no servidor, fila/reconciliação em `caixa.py`, `iniciar.cmd`, flag e faixa da interface, contratos da proposta e registros dos cinco cenários reais em `construcao.md` e no ticket 53. Gustavo deixou expressamente seguir com o canal A em `pedido.md`; canal B permanece reserva sem aceite de ponta a ponta.

## Evidência e resultado

- **123 testes do núcleo OK**, em uma execução própria de 45,667 s; **4 testes do projeto real OK**, com 0 problemas. Incluem entrega normal com mensagem no histórico, Enter/texto preso, timeout, erro de check, escada 1/5/15 min até falhou, recuperação, reinício, duas mensagens, ausência de canvas e as três regressões novas.
- `texto_no_prompt` distingue histórico e caixa de digitação; reconciliação periódica preserva `enviando`, enquanto o arranque o recupera; pendente com `.md` já `lida` é encerrado sem novo ask. As três mudanças correspondem aos defeitos observados e têm provas dirigidas na suíte.
- Os cinco testes **reais** foram executados pelo Designer com o maestro, não repetidos por mim: parado, ocupado, duas em 5 s, reinício e nome errado. Cruzei horas/UUIDs com o ticket 53 e li os seis `.md` e a fila/API atuais: todos `lida` e `entregue`. O envio `13f63156-93e0-4ac8-81a9-80e8a4356d9c`, entregue com 0 tentativas, já fora absorvido junto do anterior; não precisava de outro aviso. O primeiro envio, `022e4d3f-110b-4b5a-a40a-c86f241bd117`, também está corretamente encerrado após a correção.
- Renderização própria em Edge headless, real somente leitura em 1280×800 e 1600×900: faixa de canal indisponível escondida, de acordo com `/api/aviso`. Em servidor próprio sobre cópia temporária fora do canvas, faixa visível com motivo e instrução “respondi”. Capturas abertas e conferidas, além da captura fornecida do cenário nome errado.
- Invocação em lista de argumentos com `shell=False`, executável/agente definidos na configuração local, fila persistida antes da entrega e servidor restrito ao loopback. O aviso aponta arquivos; absorção continua idempotente por UUID/estado no arquivo, não pela contagem de avisos.

## Limites registrados, sem bloquear

- O cenário real de nome errado provou primeira falha pendente e recuperação; timeout e a escada inteira até `falhou` foram provados com executável falso/hora controlada, não aguardados no maestro real. O reinício real recuperou uma entrega cujo subprocesso já havia saído; o arranque com pendente ainda não enviado está coberto na suíte.
- O motivo detalhado de falha fica na API; a tela informa que o aviso ainda não saiu. Não declara sucesso falso. Mostrar o motivo na interface é **sugestão**, não condição deste aceite.
- O erro isolado sem registro relatado pelo Designer não se reproduziu nesta execução. Sua causa permanece **não verificada**; se ocorrer novamente, guardar traceback e nome do teste antes de repetir.
- A detecção de texto preso depende da forma atual do terminal Claude Code; a proposta registra a convenção. Canal B não foi validado de ponta a ponta.

Evidências próprias: `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-marco7/` (`resultados.json`, `real-1280.png`, `real-1600.png`, `fora-canvas.png`); script `review_marco7.py` na pasta deste papel. Nenhuma mensagem de teste enviada ao maestro por mim, nenhuma escrita na caixa real. Servidor próprio encerrado; cópia temporária preservada.
