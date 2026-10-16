---
titulo: O que fica dentro da pasta de uma iniciativa
ticket: 12
aberta: 2026-10-14
estado: absorvida
carta: prototipo-12-miolo
---

**A pergunta em uma frase:** quando você cria uma iniciativa nova no hub (por exemplo, a próxima frente da VOEGOL),
com que subpastas e arquivos a pasta dela já nasce?

O endereço já está decidido: `clients/voegol/<iniciativa>/`, `operations/soc-strata/`, `initiatives/context-hub/`.
Falta o que vai **dentro**. Hoje cada projeto seu inventou o próprio formato:

```
C:\Projetos\maestri\soc-context\          C:\Projetos\voegol\        C:\Projetos\context-hub\
  backlog/  cases/  kb/  queries/           docs/  outputs/            exploracao/  .scratch/
  results/  project-memory.md               Scripts/  Tests/           docs/adr/  GLOSSARY.md
  SOC_Operations_Manual.md                  README.md                  AGENTS.md
```

Funciona para você, mas um agente que chega a uma pasta não sabe onde está o estado do trabalho, onde estão as
decisões nem onde gravar. O código (como os `Scripts/` da VOEGOL) continua no repositório próprio, fora do hub,
ligado por link, como já foi decidido.

## Com que forma a pasta de uma iniciativa nasce
id: miolo
tipo: escolha
recomendada: A

- A: Quatro itens fixos em todas, mais um modelo de subpastas escolhido pelo tipo da iniciativa
- B: As mesmas subpastas em todas as iniciativas, seja cliente, operação ou pesquisa
- C: Só os quatro itens fixos; as subpastas, cada iniciativa cria quando precisar

**Os quatro itens fixos** (iguais nas opções A e C):
- `README.md`: a ficha, com o que é, de quem é e se está ativa;
- `retomada.md`: onde o trabalho parou e o próximo passo, que a sessão abre sozinha;
- `_archive/`: o que terminou;
- `maestro/`: os ajustes do Maestri para essa iniciativa, opcional.

**Exemplo da opção A**, a mesma ideia com modelos diferentes:

```
operations/soc-strata/      (modelo "operação contínua")
  README.md  retomada.md  _archive/
  runbooks/      ← o manual de operação
  cases/         ← um arquivo por caso
  decisions/     ← como as classificações
  queries/       ← as consultas KQL

clients/voegol/grupos-dinamicos/   (modelo "cliente com entregas")
  README.md  retomada.md  _archive/
  inputs/        ← o que o cliente mandou
  deliverables/  ← o que você entregou
  meetings/      ← atas
  code.md        ← link para o repositório dos scripts
```

Na **opção B**, as duas pastas acima teriam as mesmas subpastas, e várias ficariam vazias. Na **opção C**, cada
uma cria as dela, como hoje: o agente acha o `README.md` e o `retomada.md`, mas o resto muda de pasta para pasta.

Por que A: os seus projetos já mostram tipos diferentes, e a opção A segue o que você pediu para o Maestri, um
acervo de peças prontas. Os nomes das subpastas acima são exemplos; cada modelo é decidido numa rodada própria.
Também fica para uma rodada própria: senhas e tokens, que hoje aparecem soltos nas pastas de spike.

## Algo mais?
id: algo-mais
tipo: texto
