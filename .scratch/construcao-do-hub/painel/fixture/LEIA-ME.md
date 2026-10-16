# Fixture ao vivo da execução (formato do contrato, seção 5)

`node gerar.mjs [--saida <pasta>] [--velocidade 10] [--so-historia [--ate <minuto>]] [--excesso] [--defeitos]`

- Grava em `execucao-fake/` (padrão): `execucao.json`, `tickets/NN-slug.md`, `eventos/<agente>.jsonl`. Sem `agentes/`.
  Apaga e recria a pasta. Nunca grava na pasta real.
- Minuto 0 = agora. Passado (75 min, 1049 linhas) sai na hora com carimbos para trás; o resto (464 linhas, até +40 min)
  entra ao vivo, 6 s reais por minuto simulado (`--velocidade 1` = tempo real).
- Três momentos para captura: `--so-historia --ate -40` (começo), `--ate 0` (meio: estouro, espera, falha), `--ate 30` (fim;
  carimbos no futuro, só para captura).
- Elenco: 5 construtores, 2 revisores, 2 testadores, 1 integrador, 2 Prumos, maestro (13) + Fable (agente próprio, minuto -30).
- Casos plantados: estouro de 1 hora (construtor-4, ticket 04); espera o Gustavo (ticket 20); falha (testador-2 no
  ticket 12, retrabalho ao vivo); Fable chamado no ticket 14; 10 subagentes juntos (construtor-2, ticket 18; `--excesso`
  põe 11); sem sinal (revisor-2 desde o minuto -46; testador-1 após +1); agente encerrado (`fim`: Fable, construtor-5).
- `sinal` a cada minuto, com freio (só se o último evento do agente tem mais de 30 s).
- Ao vivo, o commit do construtor-2 no minuto +16 chega em duas metades (1,5 s entre elas): linha incompleta para testar a tolerância.
- `--defeitos`: linha que não é JSON, tipo novo, linha incompleta no fim, agente fora da lista, ticket com status
  desconhecido e bloqueio inexistente, ciclo de bloqueio entre dois tickets.
- Tipos e estados só os da seção 5 (`ocioso` e `aprovou` não existem; reviso/teste usam `passou_ticket` e `resolveu_ticket`).
