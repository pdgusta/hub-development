---
titulo: Teste do canal de aviso ao maestro
ticket: 53
aberta: 2026-10-14
estado: absorvida
---

Rodada **de teste**: quem responde é o Designer, nos testes da §4.3 da proposta. As respostas exercitam os cinco tipos
de pergunta e o aviso ao maestro, e não decidem nada do context hub. Pode ser respondida e substituída várias vezes.

## Por qual canal o aviso começa
id: canal
tipo: escolha
recomendada: A

- A: Terminal "Portal" no canvas, que manda `maestri ask` ao maestro
- B: Vigia na sessão do maestro, pela ferramenta Monitor
- C: Só a conferência da caixa no começo de cada turno

O canal A não depende de nada aberto na sessão do maestro. O B fica de reserva se o A falhar com o maestro ocupado.

## Que situações o teste cobre
id: situacoes
tipo: varias
recomendada: parado, ocupado, duas, reinicio, nome-errado

- parado: maestro ocioso
- ocupado: maestro no meio de um turno longo
- duas: duas respostas em 5 s
- reinicio: servidor reiniciado com aviso pendente
- nome-errado: nome de agente errado, que vira "falhou" e "tentar de novo"

São as cinco situações da §4.3, todas necessárias para o canal valer.

## A sequência do teste está boa
id: sequencia-ok
tipo: aprovar

A ordem é a da pergunta anterior, uma situação por vez. Depois de cada uma, o maestro confirma no chat do canvas que
recebeu o aviso.

## Ordem e responsável de cada passo
id: passos
tipo: proposta

```json
{
  "colunas": ["passo", "quem", "o que confirma"],
  "linhas": [
    {"id": "p1", "passo": "parado", "quem": "Designer responde, maestro ocioso", "o que confirma": "aviso chega sem o maestro pedir"},
    {"id": "p2", "passo": "ocupado", "quem": "Designer responde no meio de um turno do maestro", "o que confirma": "aviso chega com Enter, sem ficar digitado"},
    {"id": "p3", "passo": "duas em 5 s", "quem": "Designer responde duas vezes", "o que confirma": "dois avisos ou um aviso com os dois arquivos"},
    {"id": "p4", "passo": "reinício", "quem": "Designer reinicia o servidor com aviso pendente", "o que confirma": "aviso pendente sai depois do reinício"},
    {"id": "p5", "passo": "nome errado", "quem": "Designer troca o nome do agente", "o que confirma": "falhou visível e tentar de novo funciona"}
  ],
  "pode": ["editar", "reordenar", "ligar", "adicionar", "remover"]
}
```

## Observações do teste
id: observacoes
tipo: texto
