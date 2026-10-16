# Aviso sem esperar o ask — Prumo, 2026-10-15

**APROVADO após o ajuste da parada normal e a declaração do limite após queda abrupta.** Sem bloqueantes ou importantes pendentes nesta correção. A fila pode avançar após prova de entrega, sem esperar o maestro ficar ocioso.

## Conferido

- A trava cobre uma entrega até haver prova, não até o destino ficar ocioso. Todos os envios do lote precisam aparecer fora do prompt ou estar lidos no Markdown; um lote parcialmente provado não é liberado.
- Saída dos asks vai para arquivos temporários, evitando bloqueio por PIPE cheio. Ask comprovado é acompanhado até retorno/timeout enquanto o portal permanece ativo. Sem prova, conserva o caminho de erro/retry.
- Check não é paralelo dentro da mesma entrega; polling tem pausa de 2 s e a procura na tela encerra após 120 s. Um check lento pode consumir seu timeout de 60 s; não é uma garantia de frequência exata de 2 s. Depois da janela, só o Markdown é consultado.
- UUID na tela é prova operacional de chegada, não prova de absorção no ticket. Oito caracteres não são unicidade criptográfica e o pressuposto é não haver referência coincidente fora do aviso; a prova forte continua o Markdown lido. Não é motivo para bloquear esta correção do incidente, no contexto local de caixa/UUID aleatório e absorção idempotente.

## Processo remanescente

Reproduzi com processo próprio: pai cria filho aguardando, chama `_acompanhar` com timeout de 0,5 s e termina; após 1 s o filho continua vivo. A thread daemon morreu com o pai. Filho de teste encerrado por handle próprio ao terminar a prova; nenhum processo real tocado.

Designer recebeu o resultado, acrescentou `encerrar_asks()` à parada normal e teste de encerramento sem desfazer a entrega. **Teste novo executado aqui: 1 OK.** Sobrevivência após queda abrupta já fazia parte do contrato anterior; proposta §4.3 e LEIA agora declaram que os 30 min dependem de supervisor vivo e orientam identificar os asks anteriores ao reinício, conferir UUIDs entregues e encerrar apenas os próprios remanescentes. Processo vivo não justifica reenvio. Ressalva resolvida dentro desta revisão, sem exigir outra arquitetura.

**222 testes do núcleo OK** (558,4 s) e **6 testes do projeto real OK** nesta revisão, com portal temporário e fontes reais só em leitura. A suíte completa iniciou antes de o teste de parada normal ser acrescentado; este foi executado separadamente (**1 OK**), com a alteração final de `parar()`. Não relato 223 testes como uma execução única.

Os quatro testes novos da entrega comprovam fila avançando com primeiro ask ainda em curso, prova pelo Markdown, timeout do acompanhante e UUID quebrado/fora do prompt. Os anteriores conservam erro/retry, check ambíguo, Enter e fallback. Não enviei aviso de teste ao maestro real: a evidência de produção é o incidente/reinício registrado pelo Designer; a repetição própria usa o maestri falso.

Nenhuma escrita na caixa real ou implementação por este papel. A correção não muda a interface visual. Próximo: Designer manter a documentação alinhada à parada normal; L3 dos Laços continua uma entrega separada.
