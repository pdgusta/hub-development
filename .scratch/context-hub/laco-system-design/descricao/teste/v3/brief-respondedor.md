# Brief do respondedor (teste da v3)

Você testa se uma descrição de um sistema basta para responder perguntas sobre ele. Responda em pt-BR.

**Leia só dois arquivos:**
1. `C:/Projetos/context-hub/.scratch/context-hub/laco-system-design/descricao/descricao-do-hub.md` (a descrição);
2. a sua fatia de perguntas (o caminho vem na tarefa).

**Não leia mais nada:** nenhum outro arquivo do repositório, nenhuma busca, nenhuma web. O teste é saber o que a
descrição sozinha responde. Se você usar outra fonte, o teste não vale.

Para cada pergunta da fatia, uma linha JSON em `teste/v3/respostas/<sua fatia>.jsonl` (mesma pasta da descrição):

```json
{"n": 12, "resposta": "...", "secoes": ["8.1", "4"], "situacao": "responde | parcial | nao-diz", "falta": "o que a descrição precisaria dizer, se parcial ou nao-diz"}
```

- `resposta`: de 1 a 5 frases, só com o que a descrição diz. Não complete com o que você acha provável.
- `secoes`: os números das seções da descrição que você usou.
- `situacao`: `responde` se a descrição dá a resposta inteira; `parcial` se dá parte; `nao-diz` se não dá.
- Se a descrição marca o ponto como "a decidir" ou "não verificado", diga isso na resposta: conta como `responde`.

Ao terminar, responda só: o caminho do arquivo e a contagem de responde, parcial e nao-diz.
