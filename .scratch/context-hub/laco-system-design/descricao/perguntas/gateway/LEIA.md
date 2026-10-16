# Gerador de perguntas pelo FreeLLMAPI (etapa 1a do laço da descrição)

Plano em `../../plano.md`. Um processo só (`corrida.py`) faz tudo: roteia cada chamada para um modelo explícito do
gateway (nunca `model: auto`), com teto por dia, ritmo e saúde; roda 20 trabalhadores; fecha cada onda; tira
repetidas; cria a onda seguinte; para sozinho. Os modelos só respondem; o script valida e grava. Só biblioteca padrão
do Python 3.12; chaves nas variáveis `FREELLM_API_KEY` e `FREELLM_DASHBOARD_TOKEN`.

## Como funciona

- **Células:** lente × tipo × formulação = 12 × 12 × 2 = 288 (`prompts.py`). Formulações: `pratica` (situações do dia
  a dia, palavras simples) e `borda` (casos de borda, peça desligada, o que não está decidido).
- **Contexto dos modelos:** `resumo-neutro.md` (escrito do mapa e do glossário, sem o texto atual do hub) e as cinco
  sementes do Gustavo como exemplo de tom. Cada chamada pede de 8 a 15 perguntas em JSON
  (`{"perguntas": [{"pergunta", "tipo", "lente", "cita"}]}`); a lente é sempre a da célula, o tipo fica o do modelo se
  for um dos 12.
- **Onda 1:** as 288 células. **Ondas seguintes:** as 96 células menos cobertas (menos perguntas novas creditadas),
  com até 10 perguntas que já temos naquela lente e tipo, para o modelo escrever outras; o roteador prefere uma família
  de modelo que a célula ainda não usou.
- **Repetidas:** Jaccard ponderado por IDF, limiar 0,50, mais peças e atores citados coincidindo (ver `calibracao.md`).
- **Parada** (o que vier primeiro): duas ondas seguidas com 15% ou menos de perguntas novas; 2 h desde o início;
  40 mil tentativas; cota orçada esgotada (nenhum modelo com folga na próxima hora); arquivo `PARAR`.
- **Orçamento:** `orcamento.md` (21 modelos, 2.950 tentativas no máximo hoje).

## Arquivos

| Arquivo | O que é |
|---|---|
| `perguntas.jsonl` | **a saída**: perguntas únicas, com `vezes`, `modelos` (quantas vezes cada um), `familias`, `celulas`, `variantes` |
| `ondas/onda-N.md` | o relatório de cada onda: taxa de novas, histórico, modelos, únicas por lente e tipo |
| `ondas/onda-N.json` | o plano de cada onda (células e o que já temos) |
| `fim.txt` | aparece quando a corrida termina, com o motivo da parada |
| `livros/chamadas.jsonl` | o livro-razão: cada chamada (modelo, rota, tentativas, latência, estado, perguntas ou erro) |
| `estado/estado.json`, `estado/uso.json`, `estado/pid.txt` | onda atual, histórico, uso por modelo e janela, PID do python |
| `logs/corrida.out.log`, `logs/corrida.err.log` | saída do processo |
| `logs/disparo.txt` | quando, com que comando e com que PID foi disparado |
| `teste/` | o teste curto (3 células × 4 modelos), que serviu também de amostra da calibração |

## Como conferir

```powershell
$g='C:\Projetos\context-hub\.scratch\context-hub\laco-system-design\descricao\perguntas\gateway'
Get-Content "$g\logs\corrida.out.log" -Tail 5; Test-Path "$g\fim.txt"; Get-Process -Id (Get-Content "$g\estado\pid.txt") -ErrorAction SilentlyContinue
```

O último `ondas/onda-N.md` tem a taxa de novas e o histórico. Erros do script aparecem no livro-razão como
`"estado": "erro_do_script"` e no `logs/corrida.err.log`.

## Como parar

Crie o arquivo `PARAR` na pasta (`New-Item "$g\PARAR"`). Nenhuma chamada nova começa; as que estão em voo terminam
(até ~2,5 min), a onda fecha com o que chegou, `perguntas.jsonl` é regravado e `fim.txt` diz "arquivo PARAR". Para
matar na hora, só pelo PID gravado: `Stop-Process -Id (Get-Content "$g\estado\pid.txt")` (nunca por nome); depois
`python juntar.py` refaz `perguntas.jsonl` a partir do livro-razão.

## Retomar

Se o processo cair, rode o mesmo comando de `logs/disparo.txt`: ele retoma a onda em curso (pula as células já
aceitas), com o relógio das 2 h contado do início original. Uma base com `fim` gravado em `estado/estado.json` não
roda de novo.

## Avulsos

- `python juntar.py` — refaz `perguntas.jsonl` do livro-razão (imprime a taxa por onda).
- `python calibrar.py --base teste --por-faixa 12` — lista pares por faixa de similaridade.
- `python corrida.py --teste` — o teste curto, na pasta `teste/` (já rodado; apagar a pasta para repetir).
