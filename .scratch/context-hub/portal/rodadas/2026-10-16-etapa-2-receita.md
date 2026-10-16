---
titulo: Etapa 2 (o banco): receita
ticket: 16
aberta: 2026-10-16
estado: aberta
---

**Onde estamos.** A etapa 0 (as três provas de risco) está completa e juntada: os dois CouchDB replicam com a cifra,
nada com ponto sai do disco pelo LiveSync, e os hooks do Codex funcionam em acesso total. Da etapa 1 (o esqueleto) já
entraram o esqueleto e o frontmatter imposto; faltam o gerador de exclusões (06, com a Vela, em revisão) e o verificador
que cuida das pastas (27, que espera o 06). A Vela pega o 27 quando o 06 entrar, e isso fecha a etapa 1.

**Já antecipado:** o Trilho está na guarda que recusa regravar arquivo inteiro (ticket 14, da etapa 5), já com o seu
aval para usar os harnesses de verdade.

**A etapa 2** constrói o banco de cada par: o 07 (par A e par B de ensaio nesta máquina, cada um com o seu CouchDB, a
replicação, o LiveSync com a cifra e o caminho ofuscado, e a vista `.md`) e depois o 08 (o banco aguentando o uso real:
exclusões pela lista do gerador, limite de 200 MiB, colisão de binário recuperável, kit que pode rodar de novo, laço que
religa o sincronizador). O 08 espera o 07 e o 06.

**O que a Brasa traz:** ela fez a prova 01 e conhece o CouchDB e o CLI do LiveSync por dentro; as três ressalvas do
parecer dela já estão no 07. A revisão segue em dupla: Fiel (agora Claude Opus 5.5 médio) e Fielzinho (Codex). O
Fielzinho ficou sem cota do Codex por um tempo hoje e duas leituras dele estão pendentes (tickets 01 e 05, já
juntados); se faltar de novo, o Fiel revisa sozinho e registra.

## Receita da etapa 2
id: receita-etapa-2
tipo: escolha
recomendada: A

- A: A Brasa (Claude Opus 5.5 médio) faz o 07 e depois o 08, com os bancos de ensaio no Docker em 127.0.0.1 apagados ao fim; revisão em dupla Fiel e Fielzinho; o Rebite junta
- B: A Brasa faz o 07; quando ele entrar, ela segue para o 09 (o MCP do banco, etapa 3) e o 08 vai para quem ficar livre primeiro (Vela ou Trilho), para a etapa 3 andar junto com o fim da etapa 2
- C: Outra receita: escreva no "Algo mais?"

## Algo mais?
id: algo-mais
tipo: texto
