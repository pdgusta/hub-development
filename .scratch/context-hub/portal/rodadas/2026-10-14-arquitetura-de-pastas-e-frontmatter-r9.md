---
titulo: O que é igual em toda pasta de iniciativa
ticket: 12
aberta: 2026-10-14
estado: suspensa
---

Você escolheu na rodada anterior que cada pasta de iniciativa nasce com um **modelo de subpastas escolhido pelo tipo**
(cliente com entregas, operação contínua, produto com código, pesquisa). Isso continua valendo. Os quatro itens fixos
que eu tinha posto junto, sem mostrar na opção, voltaram a ficar em aberto. Esta rodada decide só eles.

O que já está decidido em outros tickets, e não entra aqui:
- `_archive/` fica **uma vez em cada raiz** (`clients/_archive/`, `operations/_archive/`…), não dentro de cada
  iniciativa. Pôr dentro da iniciativa foi erro meu.
- `maestro/`, com os ajustes do Maestri para aquela iniciativa, existe só quando for usada ("Maestri: padrão e
  liberdade").
- Cada trabalho tem uma **nota de retomada** (onde parou e o próximo passo), num lugar fixo que a sessão aberta na
  pasta acha sem busca ("Contrato file-first"). Só o lugar e o nome dela estão em aberto.

## O que fica igual em toda pasta de iniciativa, seja qual for o modelo
id: fixos
tipo: escolha
recomendada: B

- A: Nada; cada modelo decide tudo, inclusive onde fica a nota de retomada
- B: Só a nota de retomada, sempre como `retomada.md` na pasta da iniciativa; o resto vem do modelo
- C: A nota de retomada (`retomada.md`) e uma ficha (`README.md` com o que é, de quem é e se está ativa); o resto vem do modelo

Por que B: a nota de retomada precisa estar num lugar fixo para a sessão achá-la sem procurar. Com o mesmo nome e o
mesmo lugar em toda iniciativa, isso vale para qualquer modelo. Na opção A, ela mudaria de lugar conforme o modelo, e
o agente teria de saber o modelo antes. A ficha da opção C ajuda a busca, mas pode viver dentro de cada modelo, que
decide se precisa dela.

## Algo mais?
id: algo-mais
tipo: texto
