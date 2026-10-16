# Sonda do Dolt

Type: task
Status: wontfix

## Question

Em meio dia, no Windows, sobre um banco Dolt de teste: (a) um trigger BEFORE UPDATE com SIGNAL
recusa gravar com versão velha? (b) dá para criar uma branch a partir de um commit e rodar
DOLT_MERGE com colisão, como a ponte da vista `.md` precisaria? Se os dois passarem, o Dolt sobe de
reserva para candidato; se falharem, continua reserva. Opcional: proposta no "Debate sobre o Dolt",
roda só se o Gustavo quiser. Não trava nenhum ticket.

## Comments

- 2026-10-15 ~14h10: pedido do Gustavo (rodada 6 do laço do system design, "algo mais"): próxima rodada de cada ticket
  em andamento sem bloqueante. **Rodada 1 aberta** (`portal/rodadas/2026-10-15-sonda-do-dolt-r1.md`): fechar sem rodar
  (a sonda já está no Radar de `estrategia-pos-pesquisa.md`, com o gatilho "o CouchDB com LiveSync falhar na
  construção"), rodar agora ou deixar aberto. Recomendada: fechar.
- 2026-10-15 14:17, **rodada 1 respondida** (envio `c9fd6893-efe0-4041-902a-48133fe67e41`): **A, fechar sem rodar.**
  Comentário do Gustavo: "Não era pra ter aberto esse ticket, coloque no radar sem gatilho, só como opção se falhar na
  construção, o que é bem improvável". **Feito:** linha do Dolt no Radar de `estrategia-pos-pesquisa.md` sem gatilho,
  "só como opção se o CouchDB com LiveSync falhar na construção, o que é bem improvável". Ticket fechado como wontfix.
