# Regras do maestro: comandos que reiniciam ou removem recrutas

A guarda `guarda-de-recrutas` barrou um comando seu e mandou você ler este arquivo. Leia inteiro antes de repetir.

## O que cada comando faz com o recruta

| Comando | Efeito |
|---|---|
| `maestri role edit` / `role write` | reescreve o papel e **reinicia na hora todos os terminais com aquele papel** |
| `maestri role assign` | troca o papel e reinicia o terminal |
| `maestri recruit --replace` | reinicia o processo no mesmo lugar do canvas |
| `maestri dismiss` | remove o terminal do canvas, e notas e portais ligados só a ele ficam órfãos |

Nos quatro, **a sessão do recruta acaba**: contexto lido, raciocínio em curso e subagentes em voo se perdem. Só o
que ele gravou em arquivo sobrevive.

## Antes de repetir o comando

1. **Você precisa mesmo reiniciar?** Para dar uma instrução nova a um recruta, use `maestri ask "<nome>" "..."` e
   peça que ele grave a regra no próprio arquivo de estado. Editar o papel só vale para recrutas futuros ou entre
   frentes.
2. **O recruta está no meio de um turno?** Então **espere**. A guarda não deixa passar com recruta ocupado: turno em
   andamento, comando ou subagente rodando, mensagem na fila. Volte a tentar quando ele terminar e avisar.
3. **Ele está ocioso, mas com contexto?** Peça um **handoff** antes: que grave em arquivo o estado, o próximo passo
   exato e o que está pela metade, e confirme. O registro dele é o que a sessão nova vai ler.
4. **O que se perde, e quem precisa saber?** Se a perda pesa (trabalho longo, cota cara, subagente em voo), avise o
   usuário antes de seguir.

## Para seguir, depois de avaliar

Repita o comando com um comentário no fim, na mesma linha, dizendo o que você conferiu:

```
maestri role edit "Papel" "velho" "novo"  # risco-avaliado: Fulano ocioso, handoff gravado em estado.md às 12:40
```

A guarda só aceita o comentário quando **nenhum** recruta atingido está ocupado. O comentário fica no transcript como
registro da sua avaliação.
