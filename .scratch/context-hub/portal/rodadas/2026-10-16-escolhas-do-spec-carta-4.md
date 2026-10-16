---
titulo: Escolhas do spec, carta 4: ficha, porteiros e acervo
ticket: 16
aberta: 2026-10-16
estado: absorvida
carta: escolhas-4-regras
---

A carta **"escolhas-4-regras"** é um manual de montagem das regras que o hub impõe sozinho: quem completa a ficha da
nota (o frontmatter), quem barra a gravação errada e quem guarda as skills do maestro. São sete escolhas, na mesma
ordem desta rodada. Ela foi feita pelo Guache e revisada pelo Esquadro, que a passou na segunda volta.

## 1. O verificador só preenche o que dá para deduzir
id: verificador
tipo: escolha
recomendada: A

- A: Aceitar: lê, relê logo antes de gravar e troca só a ficha (tipo, iniciativa, título, data de mudança); se a nota mudou no meio, refaz ou devolve ao agente, e a sua edição fica inteira
- B: Regravar o arquivo inteiro (mais simples, mas pode apagar a sua edição ou o que o sincronizador acabou de trazer)

## 2. O porteiro monta a nota final antes de conferir a ficha
id: porteiro
tipo: escolha
recomendada: A

- A: Aceitar: nota atual + o pedaço trocado = nota final, e o verificador confere essa nota; arquivo novo é conferido direto
- B: O porteiro olha só o pedaço trocado (sem a ficha à vista, ele barra toda troca ou deixa passar sem conferir)

## 3. A conferência do fim da resposta é um script, sem IA
id: fim-sem-ia
tipo: escolha
recomendada: A

- A: Aceitar: um script pergunta "a nota de retomada mudou?"; se mudou, solta, se não, devolve ao agente (local, de graça, na hora, mas não julga se a nota ficou boa)
- B: Um modelo de IA lê a conversa e a nota e julga se basta (julga a qualidade, mas custa, demora e manda a conversa, com dado de cliente, para o modelo)

## 4. O lembrete e a guarda do acervo valem em qualquer pasta
id: acervo-qualquer-pasta
tipo: escolha
recomendada: A

- A: Aceitar: fora do hub, o lembrete "comece pelo acervo" chega ao maestro e a guarda olha o arquivo real, então gravar no acervo pelo atalho também pede o seu aval (exceção à regra "fora do hub, o porteiro sai na hora")
- B: Regra geral para tudo: fora do hub os porteiros não agem, o lembrete não chega e a gravação pelo atalho passa sem aval

## 5. Testar as skills do Copilot no ensaio por uma lista extra
id: skills-copilot
tipo: escolha
recomendada: A

- A: Aceitar: no ensaio, o Copilot acha as skills por uma lista extra de pastas (a variável `COPILOT_SKILLS_DIRS`), que prova o caminho extra; a instalação de verdade ainda fica com você
- B: Sem teste no ensaio: a primeira prova das skills do Copilot é na instalação de verdade

## 6. O campo "iniciativa" só é cobrado em nota de iniciativa
id: campo-iniciativa
tipo: escolha
recomendada: A

- A: Aceitar: em nota de iniciativa o verificador preenche; em referência e em entrada fica dispensado, e o esquema de cada tipo dá a palavra final
- B: Cobrado em toda nota (referência e captura rápida esbarram na ficha, recusadas ou com valor inventado)

## 7. "Nova iniciativa" já cria o mapa da iniciativa
id: mapa-iniciativa
tipo: escolha
recomendada: A

- A: Aceitar: o script "nova iniciativa" cria, com os seis arquivos do núcleo, o `AGENTS.md` da iniciativa, e o agente sempre acha o mapa local
- B: À mão, quando precisar: o mapa só nasce quando houver regra própria, e depende de alguém lembrar de criar

## Algo mais?
id: algo-mais
tipo: texto
