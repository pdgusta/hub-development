# Brief do juiz (lote 3 do teste)

Você julga respostas dadas por quem leu só a descrição do context hub. Responda em pt-BR.

Leia:
1. a descrição: `C:/Projetos/context-hub/.scratch/context-hub/laco-system-design/descricao/descricao-do-hub.md`;
2. as fontes do que é verdade: `C:/Projetos/context-hub/.scratch/context-hub/map.md` (Decisions so far), os tickets
   resolvidos em `.scratch/context-hub/issues/` (linha `Status: resolved`, seção Answer e comentários de resolução),
   `C:/Projetos/context-hub/GLOSSARY.md`;
3. a sua fatia: as perguntas em `teste/fatias/<fatia>.jsonl` e as respostas em `teste/respostas/<fatia>.jsonl`.

Não leia arquivos de credencial. Não edite nada além do seu arquivo de saída.

Para cada pergunta, uma linha em `teste/julgamento/<fatia>.jsonl`:

```json
{"n": 12, "veredito": "certa | errada | parcial | nao-diz | fonte-nao-diz", "eixo": "atores | componentes | responsabilidade | pertencimento | acoes | cenarios | estado | ligacoes | outro", "motivo": "uma frase", "fonte": "ticket ou seção do mapa"}
```

- `certa`: a resposta bate com as fontes. `errada`: contradiz as fontes (diga onde). `parcial`: certa mas incompleta.
- `nao-diz`: a descrição não respondia, mas as fontes respondem: isso é um buraco da descrição.
- `fonte-nao-diz`: nem as fontes respondem (é "a decidir" ou prática do Gustavo); não conta como falha da descrição.
- `eixo`: em que eixo da descrição está o buraco ou o erro (para `certa`, o eixo que respondeu).

Ao terminar, responda só o caminho e a contagem por veredito.
