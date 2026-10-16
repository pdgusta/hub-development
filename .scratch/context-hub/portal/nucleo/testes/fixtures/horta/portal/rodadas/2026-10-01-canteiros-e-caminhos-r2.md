---
titulo: Como ficam os canteiros
ticket: 03
aberta: 2026-10-01
estado: aberta
carta: mapa-dos-canteiros
---

O terreno comporta oito canteiros em duas fileiras. A carta mostra a disposição proposta.
Falta decidir a largura, o que plantar primeiro e a ordem do mutirão.

## Largura do canteiro
id: largura
tipo: escolha
recomendada: media

- estreito: 90 cm (alcança do meio com um braço)
- media: 1,2 m (padrão das hortas da cidade)
- largo: 1,5 m (mais terra, mais difícil de alcançar)

1,2 m é o que a prefeitura usa e dá para alcançar o meio dos dois lados.

## O que plantar primeiro
id: primeiras
tipo: varias
recomendada: alface, cebolinha

- alface: alface (45 dias)
- cebolinha: cebolinha (60 dias)
- tomate: tomate (precisa de estaca)
- abobora: abóbora (ocupa muito espaço)

Alface e cebolinha dão colheita rápida e animam o mutirão seguinte.

## Ordem das tarefas do mutirão
id: mutirao
tipo: proposta

```json
{
  "colunas": ["tarefa", "quem", "tempo"],
  "linhas": [
    {"id": "limpar", "tarefa": "limpar o terreno", "quem": "todos", "tempo": "2 h"},
    {"id": "montar", "tarefa": "montar os canteiros", "quem": "carpinteiros", "tempo": "3 h"},
    {"id": "placas", "tarefa": "fixar as placas", "quem": "crianças", "tempo": "1 h"}
  ],
  "pode": ["editar", "reordenar", "ligar", "adicionar", "remover"]
}
```

A ordem segue a dependência natural: não dá para montar sem limpar.

## Pode começar o mutirão no sábado?
id: pode-comecar
tipo: aprovar

## Algo mais?
id: algo-mais
tipo: texto
