# Parecer da carta do plano de construção (volta 1)

Revisor: Lente, 2026-10-16. Carta: `carta-plano.html` (Aquarela).
Capturas em `capturas-lente/`: `p-1600-inteira.png` (fatias `-p0` a `-p4`), `p-390-inteira.png` (fatias `-p0` a
`-p9`), e `p-390-q1-meio.png` e `p-390-q1-arrastado.png` (a moldura da pergunta 1 arrastada no celular). Capturei
com o Edge sem cabeça pelo Playwright, com viewport real de 390 px.

## Veredito: volta

No computador, a carta é forte. O ateliê de costura é uma linguagem nova: não lembra o caderno do faroleiro e
fica na família do mapa de metrô sem copiar. A pergunta 1 se lê de relance: a fita métrica dá a ordem, cada fio
nasce no carretel da sua etapa e desce até os nós de quem o usa. Os dois alinhavos tracejados mostram, sem texto,
onde ainda vai exemplo. As quatro perguntas seguem a ordem do brief (problema, desenho, com × sem), e o resumo
final é numerado de 1 a 4. Também acertam a fita com o defeito na 0 ou na 5 (pergunta 2) e o ciclo da ficha
(pergunta 4).

A carta volta por duas razões. No celular, o desenho central da pergunta 1 perde a ligação entre a etapa e o
que ela usa. E os alfinetes dizem que todas as etapas já passaram.

## Fatos (proposta, spec "Como segue sem esperar", ticket 48, ticket 14)

Estão certos:
- A ordem e a coluna "usa de verdade" batem com a tabela da proposta.
- Os dois alinhavos estão no spec: o MCP usa "um `estado.json` de exemplo" da vigia (Worker 5), e a vigia "só lê o
  item `copia_diaria`" da faixa 10 (Worker 7).
- Etapa 0: os bancos copiando nunca foram testados. As pastas com ponto aninhadas vazaram no teste do ticket 48, e o
  `.livesync/ignore` não foi testado. O Codex roda com acesso total porque o sandbox elevado falha, e os hooks só
  foram provados no modo restrito (spec, pontos abertos).
- Ramos de ontem: há trabalho parcial em 01 (2 commits), 02, 03, 07 e 09, nenhum com teste verde, e saem as
  worktrees.
- O "para a hora de cada etapa" bate com a última seção da proposta e com o spec (gemini pelo FreeLLMAPI).
- Nenhum nome de cliente aparece.

## Consertos

1. **[obrigatório · celular] Pergunta 1: a etapa e o que ela usa nunca aparecem juntos.** Em 390 px, a primeira
   vista mostra só a régua e os nomes, com a descrição cortada (`p-390-inteira-p1`, `-p2`). Os fios e a coluna
   "usa de verdade" ficam fora da tela. Ao arrastar, a régua e os nomes saem pela esquerda: os chips aparecem sem
   dizer de que etapa são (`p-390-q1-arrastado`). É justamente o "por quê" que a pergunta 1 pede. Além disso, a
   dica "arraste" fica abaixo da lista de 12 etapas, e quem rola não a vê a tempo.
   Conserto: abaixo de 820 px, pôr os chips de "usa de verdade" dentro do cartão de cada etapa, abaixo da descrição,
   com as mesmas cores e com o alinhavo tracejado. Assim o "por quê" se lê sem arrastar. Os fios podem ficar numa
   moldura que rola, com a dica acima dela. Outra saída: fixar a régua e o nome (`position: sticky`) enquanto se
   arrasta.
2. **[obrigatório · leitura] Os alfinetes dizem que tudo já passou.** A legenda diz "alfinete: passou na revisão e
   foi juntada", e há um alfinete verde entre todas as 12 etapas. Para quem bate o olho, parece que a construção
   já acabou, quando nenhuma etapa começou. Na pergunta 4 acontece o mesmo: a fita marca 0, 1 e 2 como "feitas" e a
   3 como "a de agora", sem dizer que é um exemplo.
   Conserto: dar ao alfinete o sentido de portão, por exemplo "alfinete: a próxima só começa quando esta passar na
   revisão e for juntada". Desenhá-lo vazado ou neutro, e deixar o verde para quando for verdade. Na pergunta 4,
   escrever "por exemplo" acima da fita, ou "se estivéssemos na etapa 3".
3. **[celular] Pergunta 3: a gaveta fica fora da tela.** No quadro "ontem", a gaveta `ontem/faixa-NN` (a resposta
   da pergunta) só aparece arrastando. A primeira vista mostra só os ramos (`p-390-inteira-p5`). No quadro "hoje",
   "a gaveta só se consulta" também fica cortado. Conserto: no celular, pôr a gaveta abaixo dos ramos, com a seta
   "renomeia" descendo.
4. **[fato, leve] Pergunta 2, segundo cartão.** Os exemplos são `.git`, `.env` e `.secrets`. No teste do ticket 48,
   o que vazou foi `projeto/.git` e `.venv`. Conserto: usar os exemplos do teste (`.git`, `.venv`) e, se quiser,
   "o mesmo valeria para um `.secrets`".
5. **[fato, leve] Pergunta 2, porteiros do Codex, "se falhar, atinge".** O cartão lista 5, 7 e 8. A vigia também
   entra no Codex por porteiro: "o kit liga o `notify` do Codex ao meu programa" (Worker 7). E o kit (etapa 10)
   instala todos eles. Conserto: acrescentar "6 vigia" e "10 kit".
6. **[leve · 1600] Chips cortados.** Na coluna "usa de verdade", o chip "MCP" parece cortado na borda direita nas
   etapas 5, 6 e 7 (`p-1600-inteira-p1`). Conserto: dar folga à direita da coluna.
7. **[leve · celular] Pergunta 4: o ciclo vira grade.** Em 390 px, os seis passos ficam em duas linhas de três,
   sem a linha que os liga, e a volta para "a ficha seguinte" se perde (`p-390-inteira-p6`). Conserto: no celular,
   uma coluna com setas para baixo e uma seta de volta ao primeiro passo, ao lado do "12 voltas".

Depois dos consertos 1 e 2, a carta passa. Os itens 3 a 5 são recomendados, e o 6 e o 7 são leves.

## Para o maestro (não é conserto da carta)

No spec, os Workers 3, 4 e 9 dizem "hub de ensaio (Worker 2)" e "proposta do Worker 2". A proposta e a carta põem
o hub de ensaio na etapa 1 (esqueleto, faixa 1), e a retomada (faixa 2) só na etapa 7. Parece a numeração antiga
do plano, mas, se o hub de ensaio fosse mesmo entrega da faixa 2, a ordem mudaria. Vale confirmar.

---

# Volta 2 (2026-10-16): passa

Capturas: `capturas-lente/pv2-1600-inteira.png` (fatias `-p0` a `-p4`) e `pv2-390-inteira.png` (fatias `-p0` a `-p10`).

Os consertos foram conferidos:
1. Celular, pergunta 1: virou uma lista de cartões. Cada um traz a etapa na fita, o nome, a entrega, os chips "usa"
   na cor do fio (com o exemplo tracejado e "o real vem na 6/9") e "nasce aqui" com o carretel. O "por quê" da ordem
   se lê sem arrastar (`pv2-390-inteira-p1` a `-p3`). No computador, o desenho com fios continua igual. **Feito.**
2. Os alfinetes viraram portões vazados, na fita, na legenda e no quadro. Na pergunta 4, a fita diz "exemplo: a de
   agora" e "já feitas" (`pv2-1600-inteira-p0`, `-p3`). **Feito.**
3. A gaveta fica abaixo dos ramos no celular e ao lado deles no computador (`pv2-390-inteira-p6`). **Feito.**
4. Pastas com ponto: `projeto/.git`, `projeto/.venv` e `projeto/.secrets`, como exemplos do que não pode ir. **Feito.**
5. Os porteiros do Codex atingem 5, 6, 7, 8 e 10. **Feito.**
6. Os chips de "usa de verdade" estão inteiros em 1600 px. **Feito.**
7. Celular: o ciclo da pergunta 4 está em coluna, com a linha ligando os passos (`pv2-390-inteira-p7`). **Feito.**

Ressalvas (não seguram a carta):
- O quadro "Leia uma linha" diz: "tudo o que ela usa nasceu numa etapa acima". Não vale para os dois alinhavos,
  cujo real vem depois. O quadro ao lado explica a exceção, mas "quase tudo" ou "fora os dois alinhavos" seria
  mais exato.
- No celular, o ciclo da pergunta 4 não desenha a volta ao primeiro passo; ela fica só no "12 voltas". Aceitável.
- No celular, o quadro "hoje" da pergunta 3 ainda corta "etapa 2" e "a gaveta só se consulta" à direita, mas
  traz a dica de arrastar, e a resposta (a gaveta) já está no quadro de cima.

---

# Depois da aprovação (2026-10-16)

O Gustavo aprovou a carta com uma ressalva para as próximas: a tipografia dos títulos ficou difícil de ler (Bodoni
Moda pesada, com traços finíssimos e itálico vermelho). Esta revisão não apontou isso. A legibilidade dos títulos
entra na régua dos próximos pareceres.
