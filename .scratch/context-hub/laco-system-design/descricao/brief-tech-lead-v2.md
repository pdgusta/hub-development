# Brief do Tech lead: descrição, volta 2 (consertos por eixo)

Do maestro, 2026-10-15. O teste da descrição v1 terminou:

- **Perguntas escondidas** (236, respondidas por quem só leu a descrição, julgadas contra as fontes): das 207 que as
  fontes respondem, 134 certas (65%), 49 parciais, 22 "a descrição não diz", 2 erradas. Resumo por eixo, com o motivo e
  a fonte de cada buraco, em `teste/resumo-volta-1.md`. As perguntas não estão lá: só o que faltou.
- **Três diagramas** desenhados só pela descrição: `teste/diagramas/*.md` (sequência de editar uma nota, matriz de
  responsabilidade, mapa de grupos), cada um com o que **faltou**, o que o desenhista **inventou** e o que ficou
  **ambíguo**. A matriz de responsabilidade foi a mais fraca (9 faltou, 12 inventou, 11 ambíguo).

## O que fazer

Reescreva `descricao-do-hub.md` (guarde a v1 como `descricao-do-hub-v1.md`) consertando por **eixo**, não por pergunta:
- cada buraco do resumo diz que eixo falhou; conserte a regra ou a tabela do eixo, de forma que outras perguntas do
  mesmo tipo também passem a ter resposta;
- cada "inventei" e "ambíguo" dos diagramas é uma linha que falta ou se contradiz; resolva a contradição com a fonte;
- as duas erradas: confira contra a fonte citada e corrija;
- a matriz de responsabilidade deve sair completa: todo componente com dono, quem aciona, quem lê e quem só vê, sem
  célula a inventar; onde a fonte não diz, "a decidir com o Gustavo".

Mantenha as mesmas regras do primeiro brief (`brief-tech-lead.md`): fontes, estado de cada afirmação e a lista do que não
ler, que segue valendo (as escondidas, `perguntas/haiku/`, `perguntas/gateway/`, o ticket 56, as rodadas do laço, a
caixa). Pode ler `teste/resumo-volta-1.md` e `teste/diagramas/*.md`; não leia `teste/fatias/`, `teste/respostas/` nem
`teste/julgamento/`.

Se surgir pergunta nova que só o Gustavo responde, acrescente a `perguntas-ao-gustavo.md` como "v2". A rodada com as 14
da v1 já está no portal; as respostas dele chegam depois.

Entrega: `descricao-do-hub.md` (v2) e uma lista curta `consertos-v2.md`, eixo por eixo. Ao terminar:
`maestri ask "Claude Code" "pronto: <caminho>"`.
