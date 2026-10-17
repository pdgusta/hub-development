# Ticket 16 — Trilho — parecer do Fiel — leitura intermediária

2026-10-17 ~06h55. Ramo ticket-16, HEAD aa70e98 (contém integracao 9453e3e; a integracao andou depois). Fiel sozinho
(leitura do Fielzinho pendente). Não conta como rodada: o próprio ticket junta só com o 08 e o 10 resolvidos.

## Veredito: a parte construída não tem conserto; o ticket ainda não passa inteiro

Falta para os critérios:
- Critério 1: cenários de binário descartado na passada, arquivo acima de 200 MiB, sincronizador parado, Config Doctor
  travado, e o gerador de exclusões a cada passada (código 2 vira item com o caminho; decisão do Gustavo de
  2026-10-16 20:38). Dependem do 08.
- Critério 5: o `estado_do_hub` real. O 10 passou (06h40); dá para juntá-lo e provar com o MCP lendo o `estado.json`
  que a vigia gravou.
- O item `fim-da-resposta` casado com o hook do 27 (lição do Rebite, 2026-10-16 21h51).

## Conferido
- `node --test agents/code/test/16-vigia.test.mjs`: 9/9 (Fiel). Árvore limpa.
- Docker do Trilho (`logs/trilho-16-docker-4.log`, aa70e98): 16 PASSA, "tudo passou". Inclui o conflito pelo caminho
  decifrado (sem o id cifrado), uma notificação só na passada que piora e o `recuperar` gravando ao lado os bytes da
  versão perdida, com o original mantido e a cópia do banco apagada. Não repeti o Docker: repito na rodada final,
  com o 08 juntado.
- Piora como o maestro decidiu (04:26): item que sobe de nível; item novo conta como ok; resolvido e voltou notifica.
- Troca atômica (`.novo` e rename); os itens dos outros donos ficam.
- b4e7272 (conserto do 12): a skill da busca não cita mais a `read`; diz para ler pela ferramenta do harness. Certo,
  casa com o 12 rodada 3.

## Ressalvas (para a rodada final)
1. **Atualização perdida:** `gravarPassada` e `gravarItem` fazem ler, mudar e gravar sem trava. Se o hook do 27 (ou
   o 31) grava o seu item entre a leitura e o rename da vigia, o item do hook some. O do `fim-da-resposta` é gravado
   uma vez só, na quarta parada; perdido, não volta. Sugestão: reler logo antes do rename e juntar, ou trava por
   arquivo.
2. Um CouchDB que responde 401 (senha errada) cai como "a tarefa de envio não está no _scheduler" e, depois de 15
   min, vira divergência de replicação com motivo errado. O `pedir` devolve undefined para qualquer resposta que não
   seja ok.
3. O `recuperar` replica o banco inteiro para `<db>-recupera` a cada folha descartada. Com várias folhas, várias
   cópias inteiras. Pesa com o hub grande.
