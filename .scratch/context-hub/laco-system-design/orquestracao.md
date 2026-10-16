# Como o maestro pretende construir e orquestrar o laço do system design

Plano pedido pelo Gustavo em 2026-10-15 (comentário no laço, envio `a490a680…`): "Não inicie nada, só me apresente
aqui no laço como você pretende construir e orquestrar tudo isso." O desenho está na página Laços; este arquivo é o
detalhe de cada etapa. Nada aqui começou.

**Quem decide o quê:** você só aprova a direção visual antes da construção (e a troca final do `system-design.html`).
As outras portas são de agentes: o maestro julga a suíte; o Tech lead e o UX revisor julgam os conceitos e a amostra;
o Prumo revisa o código.

## Fase 1: a suíte de skills de design

1. **Colher as skills do vídeo.** Feito: 8 coleções e perto de 90 skills (`skills-do-video.md`).
2. **Ler na fonte.** Um subagente Haiku 5.5 por coleção (8 em paralelo). Cada um:
   - abre o repositório e confirma URL e licença;
   - lê todo `SKILL.md`, as referências e os scripts;
   - grava uma ficha por skill em `suite/fichas/`: o que faz de verdade, a frase de `description` (é ela que faz o
     agente invocar a skill sozinho), o que precisa para rodar (scripts, rede, pacotes), riscos e se roda no Claude
     Code e no Codex.

   Nada é instalado nessa etapa.
3. **Montar as categorias.** Um agente Sonnet 5.5 lê as fichas e agrupa as skills pelo que fazem. Os nomes das
   categorias saem do conteúdo, não de uma lista pronta. Para cada categoria:
   - o que ela resolve;
   - as skills e onde elas se sobrepõem;
   - qual fica e por quê;
   - quais disputam o mesmo gatilho de invocação.

   Grava `suite/categorias.md`.
4. **Julgar as categorias** (o maestro). Confere:
   - cobertura do que o trabalho pede;
   - sobreposição e conflito de gatilho (duas skills que disparam na mesma situação);
   - segurança: nenhum script sem leitura, nada que chame a rede sem motivo;
   - se a `description` de cada skill descreve bem quando usá-la.

   Se reprovar, devolve com a lista do que ajustar e volta à etapa 3, até 3 voltas.
   O julgamento também separa as skills que servem de **régua**: as que medem gosto, percepção e composição (a
   tastemaker, por exemplo) passam a aplicar a régua junto com os critérios escritos (comentário do Gustavo,
   2026-10-15: "a régua em si também pode ser a utilização de skills adequadas").
5. **Suíte aprovada.** Vira `suite/suite.md` (a lista final, por categoria e com o papel de cada skill) e entra no
   acervo do maestro, para outros visuais e outros projetos.

## Fase 2: a equipe

6. **O texto do hub**, num laço entre o maestro e o Tech lead (o Tech lead sobe primeiro, sozinho).
   - O Tech lead escreve um texto padrão que descreve o hub. A fonte são o mapa, os tickets resolvidos e o glossário.
     O texto traz as peças, o papel de cada uma, as ligações e os fluxos, sem detalhe de implementação, e é feito
     para que qualquer diagrama possa nascer só dele.
   - Cada rodada: o maestro confere contra as decisões fechadas, aponta o que falta, sobra ou contradiz, e o Tech lead
     reescreve. Até 3 rodadas, ou até os dois concordarem.
   - Grava `texto-do-hub.md`. Você recebe o texto final para ler; não precisa aprovar.
7. **Subir a equipe.** Quatro recrutas pelo Maestri, cada um com:
   - um papel novo no acervo do maestro;
   - uma pasta própria em `C:\Projetos\equipe-design\<papel>\`;
   - as skills da suíte que servem ao seu papel, instaladas em `.claude/skills/` da pasta dele (escopo de projeto).
     A invocação é autônoma: a skill entra quando a `description` casa com a tarefa, sem você ou eu chamarmos pelo
     nome.

   Os papéis:
   - **UI engineer:** constrói os conceitos e a amostra.
   - **UX revisor:** mede contra a régua (poluição visual, espaço disputado, disposição, separação lógica) sobre
     capturas reais da tela.
   - **Tech lead:** conhece o hub pelo texto do hub; diz se a peça é congruente com o que o hub é.
   - **QA tester:** testa a peça: larguras de tela, contraste medido, teclado e foco, links, desempenho e capturas.

   O Designer coordena a equipe e entrega no portal, como hoje. O Prumo segue revisor de código. Antes de seguir, o
   maestro confere em cada recruta que as skills aparecem e disparam sozinhas.

## Fase 3: os conceitos de cidade (o laço do centro)

8. **Conceitos.** O UI engineer faz amostras de direção visual: 3 formas de cidade realmente diferentes, lado a lado
   atrás de um seletor. Amostra, não a peça inteira: só o bastante para mostrar a direção, com a régua aplicada.
9. **Porta: Tech lead e UX revisor.** O Tech lead confere a congruência com o texto do hub; o UX revisor, a régua.
   Cada um dá nota por dimensão e uma lista de consertos. Se algum reprovar, volta aos conceitos, até 3 voltas.
10. **Você aprova a direção.** Única parada para você antes de construir: uma carta no portal com os conceitos que
    passaram e o parecer da porta. Você escolhe um, pede mistura ou recusa todos (volta aos conceitos).

## Fase 4: a amostra

11. **Construir a amostra.** O UI engineer constrói a direção aprovada como amostra inicial, numa página à parte, sem
    tocar o `system-design.html`.
12. **Testar e revisar.** O QA tester testa; o UX revisor e o Tech lead revisam; o Prumo revisa o código. Sem
    aprovação dos três, volta a construir, até 3 voltas. Ao bater o teto, o laço para e espera você.
13. **Você vê a amostra pronta.** A troca do `system-design.html` (ou a construção da peça inteira a partir da amostra)
    só com o seu aval.

## Custo estimado (nada gasto ainda além da coleta)

| Fase | Quem | Estimativa |
|---|---|---|
| Ler na fonte | 8 Haiku 5.5 | ~400 mil tokens do Haiku |
| Categorias e julgamento | 1 Sonnet 5.5 + o maestro, até 3 voltas | ~200 mil |
| Texto do hub | Tech lead (Opus 5.5 alto) + o maestro, até 3 rodadas | ~250 mil |
| Subir a equipe e conferir as skills | o maestro | ~50 mil |
| Conceitos e porta, até 3 voltas | UI engineer, UX revisor, Tech lead | ~500 mil |
| Amostra e testes, até 3 voltas | os quatro e o Prumo (Codex) | ~600 mil |

Total de Claude (sem o Haiku e sem o Prumo): perto de **1,6 milhão de tokens** na estimativa. O orçamento configurado é
de **5 milhões** (pedido do Gustavo, 2026-10-15), com até 4 voltas nos conceitos e 6 na amostra; ao bater o orçamento,
o laço para e espera você.
