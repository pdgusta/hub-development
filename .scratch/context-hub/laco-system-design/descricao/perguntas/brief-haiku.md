# Brief dos Haiku do lote 1: perguntas sobre o context hub

Você escreve **perguntas**, não respostas. Elas vão servir de fonte para reescrever a descrição do context hub do
Gustavo (um hub de contexto para ele e para agentes de IA, em duas máquinas) e para testar se a descrição é rica e
genérica o bastante para qualquer diagrama nascer dela. Plano em `../plano.md`.

## O que ler (repositório `C:\Projetos\context-hub`)

- `.scratch/context-hub/map.md` (Destination, Decisions so far, Not yet specified, Out of scope);
- `GLOSSARY.md` na raiz;
- os tickets resolvidos em `.scratch/context-hub/issues/` (linha `Status: resolved`) que tocam a sua lente;
- `sementes.md` desta pasta (as cinco perguntas do Gustavo).

**Não leia** `laco-system-design/texto-do-hub.md`, nada em `laco-system-design/descricao/perguntas/` além deste brief e
das sementes, nem arquivos de credencial (`.env`, `token*`, `auth.json`).

## O que escrever

Um arquivo `perguntas/haiku/<sua-lente>.jsonl`, uma pergunta por linha, entre 25 e 40 perguntas:

```json
{"pergunta": "...", "tipo": "<um dos tipos abaixo>", "lente": "<sua lente>", "cita": ["nomes de componentes ou atores citados"]}
```

Tipos: `se-x` ("Se X, o que acontece?"), `relacao`, `responsavel`, `grupo`, `onde-vive`, `quem-usa`, `o-que-nao-faz`,
`ordem`, `falha`, `quando`, `por-que`, `diferenca`. Use pelo menos seis tipos.

Regras:
- Pergunte como alguém da sua lente perguntaria, com as palavras do dia a dia, não com os termos do glossário quando
  houver jeito mais simples ("edito uma nota" em vez de "gravo na vista Markdown").
- Uma pergunta por coisa; nada de duas perguntas numa linha. Não responda.
- Inclua perguntas difíceis: casos de borda, falhas, o que não está decidido.
- Dado de cliente (STRATA, VOEGOL, AVIANCA, TRF3, SBF): só o nome da iniciativa; nada de nomes de pessoas ou e-mails.
- Nada de códigos internos soltos (T2, C3, R18).

Ao terminar, responda só: o caminho do arquivo e quantas perguntas.
