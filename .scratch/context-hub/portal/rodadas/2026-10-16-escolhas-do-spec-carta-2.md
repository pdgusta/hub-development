---
titulo: Escolhas do spec, carta 2: vigia e manutenção
ticket: 16
aberta: 2026-10-16
estado: absorvida
carta: escolhas-2-vigia
---

A carta **"escolhas-2-vigia"** explica as seis escolhas desta rodada, na mesma ordem: o problema, a cena e o "com a
escolha × sem ela". Ela foi feita pela Aquarela e revisada pelo Lente, que a passou na segunda volta. Cada pergunta
abaixo é uma folha da carta.

## 1. Onde e como a vigia anota o estado
id: estado-da-vigia
tipo: escolha
recomendada: A

- A: Aceitar: arquivo fixo `.local/vigia/estado.json`, que não viaja para a outra máquina, gravado por troca atômica, com nível por item (ok, informa, divergência) e o geral sempre igual ao pior
- B: Deixar o lugar e a forma para a construção decidir

## 2. A outra máquina está ligada?
id: outra-maquina
tipo: escolha
recomendada: A

- A: Aceitar: o endereço da outra máquina é só um sinal; a vigia separa desligada, serviço parado e incerto; o incerto vira "informa" com o motivo e nunca vira "ok" nem apaga a divergência
- B: Sem resposta do endereço = máquina desligada (mais simples, mas o banco parado com a máquina ligada passa por desligada e a divergência some)

## 3. Quando a cópia diária falha
id: copia-diaria
tipo: escolha
recomendada: A

- A: Aceitar: a falha sai alto (o script termina com erro, a vigia ganha o item "cópia diária" e manda a notificação do Windows); a regra geral de quem percebe as falhas continua para depois da construção
- B: Esperar a regra geral, decidida depois da construção; até lá a cópia pode falhar calada

## 4. A pasta arquivada leva a data no nome
id: data-no-nome
tipo: escolha
recomendada: A

- A: Aceitar: `_archive/AAAA-MM-DD--nome/`, a data viaja com a pasta e as duas máquinas a veem; o campo de data dentro das notas continua
- B: A data fica só dentro das notas, uma a uma

## 5. Limpar o arquivo: desenho guardado
id: limpeza
tipo: escolha
recomendada: A

- A: Aceitar: a limpeza fica desenhada como um passo da tarefa diária que só simula; nada é apagado nesta construção, e o lugar fica pronto para quando o prazo for decidido
- B: Tirar o script do spec agora: sem prazo, não há o que limpar, e ele será desenhado de novo depois

## 6. Aviso em dobro no Codex
id: aviso-codex
tipo: escolha
recomendada: A

- A: Com uma regra: os dois avisos continuam (já é decisão), mas não se repetem enquanto o estado não muda
- B: Sem regra: cada aviso toca pela sua regra; com divergência aberta, um aviso a cada turno do Codex, mais o da vigia
- C: Não decidir agora: a repetição fica como detalhe da construção

## Algo mais?
id: algo-mais
tipo: texto
