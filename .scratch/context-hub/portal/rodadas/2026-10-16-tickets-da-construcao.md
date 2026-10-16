---
titulo: Os tickets da construção
ticket: 16
aberta: 2026-10-16
estado: absorvida
---

O `/to-tickets` quebrou o spec revisto em **26 tickets**, fatias que cada uma funciona de ponta a ponta e cabe numa
sessão só. Cada ticket diz quais outros ele espera (os bloqueios); é esse grafo que o `/implement-spec` vai seguir. A
lista completa, com o que cada um entrega, está em `.scratch/construcao-do-hub/rascunhos/tickets-proposta.md`. Os 11
tickets de hoje (do plano de 1 hora) vão para uma pasta à parte quando estes forem publicados.

| # | Ticket | Espera |
|---|---|---|
| 01 | Prova: dois CouchDB replicando com o LiveSync | nenhum |
| 02 | Prova: pastas com ponto aninhadas fora do LiveSync | nenhum |
| 03 | Prova: hooks do Codex em acesso total | nenhum |
| 04 | Esqueleto do hub e hub de ensaio | nenhum |
| 05 | Frontmatter imposto: esquemas, verificador e "nova iniciativa" | 04 |
| 06 | Gerador de exclusões | 04, 02 |
| 07 | Banco do par: dois CouchDB, LiveSync e vista `.md` | 01, 04 |
| 08 | Banco: limites e robustez | 07, 06 |
| 09 | MCP do banco: gravar com versão e conflito à vista | 07 |
| 10 | MCP do banco: três instâncias, cabeça, regra curta e estado | 09, 05 |
| 11 | MCP do banco pelos três harnesses | 10, 03 |
| 12 | Busca local com aceite | 04, 06 |
| 13 | Gemini pronto e desligado | 12 |
| 14 | Guardas: regravação inteira e ficha fora do esquema | 05, 03 |
| 15 | Guardas: aviso de leitura fora da busca | 14, 12 |
| 16 | Vigia: passada, estado e notificação | 08, 10 |
| 17 | Vigia nas telas dos harnesses | 16, 03 |
| 18 | Retomada: nota de sete campos, início e fim | 04, 17, 03 |
| 19 | Roteamento de skills | 04 |
| 20 | Acervo do maestro e a guarda dele | 19, 03 |
| 21 | Arquivar e cópia diária | 08, 16 |
| 22 | Proxy e kit de cliente | 10, 12 |
| 23 | Kit de par: a forma | 11, 15, 17, 18, 20 |
| 24 | Kit de par ao vivo nos três harnesses | 23 |
| 25 | Junção e prova do hub de ensaio inteiro | 13, 21, 22, 24 |
| 26 | Instalação de verdade no par 1 (com você) | 25 |

Com o teto de 3 agentes, a fronteira começa com 01 a 04; logo depois do esqueleto entram o roteamento de skills e a
busca. As perguntas de login, cota do gemini, instalação e as três lacunas de dono ficam dentro dos tickets que as usam.

## O tamanho dos tickets
id: granularidade
tipo: escolha
recomendada: A

- A: Está certo: 26 fatias, cada uma de uma sessão
- B: Grosso demais: quebrar mais (diga quais no "Algo mais?")
- C: Fino demais: juntar (diga quais no "Algo mais?")

## Os bloqueios
id: bloqueios
tipo: escolha
recomendada: A

- A: Estão certos: cada ticket só espera o que de fato o trava
- B: Algum bloqueio está errado (diga qual no "Algo mais?")

## Algo mais?
id: algo-mais
tipo: texto
