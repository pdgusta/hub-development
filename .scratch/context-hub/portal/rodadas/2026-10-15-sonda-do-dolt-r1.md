---
titulo: A sonda do Dolt: rodar ou guardar
ticket: 32
aberta: 2026-10-15
estado: absorvida
---

A sonda é um teste de meio dia com um banco Dolt de teste. Ela confere duas coisas: se o banco recusa uma gravação
feita sobre uma versão velha, e se dá para juntar duas mudanças que colidem, como a vista Markdown precisaria. Se as
duas passassem, o Dolt subiria de reserva para candidato.

O que já está decidido: a verdade mora no CouchDB, com o plugin de sync do Obsidian. O Dolt ficou como reserva
nomeada no debate sobre ele, e a sonda foi marcada como opcional, "só se você quiser". Ela já está no Radar da
estratégia, com o gatilho "o CouchDB com o sync do Obsidian falhar na construção". Nenhum outro ticket depende dela.

## O que fazer com a sonda
id: sonda
tipo: escolha
recomendada: A

- A: Fechar o ticket sem rodar: a sonda fica só no Radar e volta se o CouchDB falhar na construção
- B: Rodar agora, em segundo plano, por um subagente: meio dia de máquina e uns 150 mil tokens; o resultado só muda o Dolt de reserva para candidato
- C: Deixar o ticket aberto como está, sem rodar

## Algo mais?
id: algo-mais
tipo: texto
