# Triagem, metade Haiku: instruções para o agente que dispara os subagentes

Pasta: `C:/Projetos/context-hub/.scratch/context-hub/laco/etapas` (use barras normais nos caminhos).

## O que fazer

1. Monte a fila: as chaves com `"haiku"` em `triagem/sorteio.json` que ainda não têm arquivo em `triagem/haiku/`.
   O arquivo de uma chave é `triagem/haiku/<slug>.json`, e o cartão é `cartoes/<slug>.json`, com
   `slug = re.sub(r"[^A-Za-z0-9._-]+", "__", chave)[:150]` (Python). Passe a cada subagente os pares `chave -> slug`
   já calculados; ele não calcula nada.
2. Divida a fila em lotes de **5 chaves**.
3. Dispare subagentes com a ferramenta Agent, **modelo `haiku`** (Claude Haiku 5.5), **todos os de uma leva na mesma
   mensagem** para rodarem em paralelo. Leva padrão: o número que o maestro disser (piloto: 2 subagentes; depois,
   na casa das dezenas). Quando uma leva termina, dispare a seguinte até a fila acabar.
4. Não leia os cartões nem as respostas você mesmo (gasta contexto à toa). Confira só que os arquivos apareceram
   (`ls triagem/haiku | wc -l`).
5. Ao final de cada leva, anote em `triagem/haiku-levas.jsonl` uma linha:
   `{"leva": N, "subagentes": S, "itens": I, "inicio": "<ISO>", "fim": "<ISO>", "tokens": <total de tokens que a
   ferramenta Agent informou, somado>}`.

## Prompt de cada subagente (troque `<CHAVES>` pela lista do lote)

```
Triagem de 5 projetos de software. Para cada chave abaixo:
1. Leia C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/triagem/prompt.md (uma vez só; são as regras e o
   formato da resposta).
2. Leia o cartão C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/cartoes/<slug>.json (o slug de cada
   chave vem na lista abaixo). Leia os 5 cartões numa só mensagem, em paralelo. No cartão de um site, o campo
   "readme" é o texto da página.
3. Julgue SÓ pelo campo "readme" do cartão, como manda o prompt.md. Não use a web nem outras fontes.
4. Grave C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/triagem/haiku/<slug>.json com exatamente:
   {"chave": "<chave>", "modelo": "claude-haiku-5-5", "ts": "<agora, ISO UTC>", "resposta": { ...o objeto JSON do prompt.md... }}
   Grave os 5 arquivos numa só mensagem, em paralelo.
Responda só "ok" ao final (ou "erro: <chave>: <motivo>" para a chave que falhar).

Chaves (chave -> slug): <CHAVES>
```

## Regras

- Nada de web. Nada de editar outros arquivos.
- Se um subagente responder erro, ponha a chave de volta no fim da fila uma vez; se falhar de novo, anote em
  `triagem/haiku-erros.jsonl`.
- Quando a fila acabar, avise o maestro com `maestri ask "Claude Code" "Haiku: N itens triados em L levas; tokens T"`.
