# Conceitos pelos subagentes Haiku: instruções para o agente que dispara

Pasta: `C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/conceitos` (use barras normais nos caminhos).

## O que fazer

1. Fila: as entradas de `fila.json` (`{"chave", "slug", "mencoes"}`, já em ordem) que ainda não têm
   `respostas/<slug>.json`.
2. Lotes de **25 entradas** por subagente (os cartões são pequenos, ~500 bytes).
3. Subagentes com a ferramenta Agent, **modelo `haiku`**, todos os de uma leva na mesma mensagem (até 20 de cada vez,
   o limite do Claude Code). O tamanho da leva é o que o maestro disser (piloto: 1 subagente).
4. Não leia cartões nem respostas. Confira só a contagem: `ls respostas | wc -l`.
5. Ao fim de cada leva, uma linha em `levas.jsonl`: `{"leva", "subagentes", "itens", "inicio", "fim", "tokens",
   "tokens_por_subagente"}` com os tokens que a ferramenta Agent informar.

## Prompt de cada subagente (troque `<LISTA>` pelos pares `chave -> slug` do lote)

```
Triagem de 25 conceitos. Regras e formato da resposta: leia uma vez
C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/conceitos/prompt.md.
Para cada par abaixo, leia o cartão C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/conceitos/cartoes/<slug>.json
(leia vários numa só mensagem, em paralelo), julgue como o prompt.md manda (sem web) e grave
C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/conceitos/respostas/<slug>.json com exatamente:
{"chave": "<chave>", "modelo": "claude-haiku-5-5", "ts": "<agora, ISO UTC>", "resposta": { ...o objeto JSON do prompt.md... }}
Grave vários numa só mensagem, em paralelo. Responda só "ok" ao final (ou "erro: <chave>: <motivo>").

Pares (chave -> slug): <LISTA>
```

## Regras

- Nada de web; nada de editar outros arquivos.
- Erro de um subagente: a chave volta ao fim da fila uma vez; se falhar de novo, vai para `erros.jsonl`.
- Ao fim da fila: `maestri ask "Claude Code" "Conceitos: N triados em L levas; tokens T; erros E"`.
