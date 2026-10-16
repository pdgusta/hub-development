# Conferência pelos subagentes Sonnet: instruções para o agente que dispara

Pasta: `C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/conferencia` (use barras normais nos caminhos).

## O que fazer

1. Fila: as entradas de `fila.json` (`{"chave", "slug", "motivo", "fonte"}`) que ainda não têm `respostas/<slug>.json`.
   O maestro roda `preparar_conferencia.py` de novo quando a triagem terminar; releia a fila a cada leva.
2. Lotes de **5 entradas** por subagente.
3. Subagentes com a ferramenta Agent, **modelo `sonnet`** (Claude Sonnet 5.5), todos os de uma leva na mesma
   mensagem (até 20 de cada vez). O tamanho da leva é o que o maestro disser (piloto: 1 subagente com 10 itens,
   ou seja 2 lotes seguidos no mesmo subagente).
4. Não leia pacotes nem respostas; confira só a contagem (`ls respostas | wc -l`).
5. Ao fim de cada leva, uma linha em `levas.jsonl`: `{"leva", "subagentes", "itens", "inicio", "fim", "tokens",
   "tokens_por_subagente"}`.

## Prompt de cada subagente (troque `<LISTA>` pelos pares `chave -> slug` do lote)

```
Conferência de projetos contra a fonte primária. Regras e formato: leia uma vez
C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/conferencia/prompt.md.
Para cada par abaixo, leia C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/conferencia/pacotes/<slug>.json
(vários numa só mensagem, em paralelo), decida como o prompt.md manda, só pelo README do pacote (sem web), e grave
C:/Projetos/context-hub/.scratch/context-hub/laco/etapas/conferencia/respostas/<slug>.json com exatamente:
{"chave": "<chave>", "modelo": "claude-sonnet-5-5", "ts": "<agora, ISO UTC>", "resultado": "<confirma|corrige|rejeita>", "conferencia": { ...o objeto JSON do prompt.md... }}
Grave vários numa só mensagem, em paralelo. Responda só "ok" ao final (ou "erro: <chave>: <motivo>").

Pares (chave -> slug): <LISTA>
```

## Regras

- Nada de web; nada de editar outros arquivos.
- Erro de um subagente: a chave volta ao fim da fila uma vez; se falhar de novo, vai para `erros.jsonl`.
- Ao fim da fila: `maestri ask "Claude Code" "Conferência: N itens em L levas; tokens T; erros E"`.
