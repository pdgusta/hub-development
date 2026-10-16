---
title: Vídeo de referência — Matt Pocock's AI workflow (The Hype Kevin)
data: 2026-10-10
origem: subagente de análise de vídeo (Opus 5.5), ticket 39
fontes: https://www.youtube.com/watch?v=Q3uuE2adUT8 ; transcrição do YouTube (en, `Q3uuE2adUT8.en.srt`) e descrição do vídeo; 54 quadros extraídos a cada 10 s (640 px) + 36 quadros densos (4 fps) em três trechos (0:00–0:03, 0:15–0:18, 2:40–2:43) + detecção de mudança de cena com ffmpeg
aviso: saída de modelo; descrição visual feita a partir de quadros estáticos, não do vídeo em movimento; o que não deu para ver fica **não verificado**.
---

# Vídeo de referência — Matt Pocock's AI workflow (The Hype Kevin)

"Ship like the best engineers: Matt Pocock's AI workflow", canal The Hype Kevin, 9:05 (545 s).

**Convenção de quadros.** `f_NNN` é o quadro N da amostragem de 10 em 10 s. Conferido contra a narração e por
PSNR: `f_N` ≈ (N−1)·10 + 5 s (±2 s). Ex.: `f_004` ≈ 0:35, `f_054` ≈ 8:55. Os últimos ~5 s (cartão final)
não caíram em nenhum quadro.

---

## 1. Conteúdo

### 1.1 Tese

O agente já consegue escrever a funcionalidade inteira; o papel do humano são **as decisões**. O fluxo de skills
do Matt Pocock existe para arrancar essas decisões do humano *antes* do código (grilling), fixá-las em
linguagem (glossário), empacotá-las (spec → tickets que cabem numa sessão limpa) e depois verificar e melhorar o
entorno (review em duas mesas, /pr, /retro). O vídeo abre e fecha com a mesma pergunta: "So what are you there
for?" → "The decisions." (0:03 e 8:28–8:30).

Fio condutor: uma única funcionalidade de brinquedo (botão **Pause** num app de assinatura de café) e um caso
limite concreto (o saco de café já embalado quando o cliente pausa no dia 29). O caso volta em quase todas as
seções e é resolvido no fim (8:46–8:54).

### 1.2 Estrutura (capítulos da descrição + rótulo de seção que aparece na tela)

| Tempo | Capítulo (descrição) | Rótulo na tela | Conteúdo |
|---|---|---|---|
| 0:00 | So what are you there for? | YOUR COFFEE BREAK | Gancho: o agente constrói enquanto você toma café; credenciais do Matt; tweet do v1.3 |
| 0:17 | The silent guess | THE SILENT GUESS | "pause" em uma frase; o agente preenche cada lacuna com um palpite; o saco embalado |
| 0:47 | Couldn't you write a longer prompt? | ASK FIRST | Inverter a conversa: o agente entrevista você (grill me) |
| 1:02 | The decision tree in the fog | THE FOG / 46 QUESTIONS | Árvore de decisões na névoa; fronteira; rodada numerada com recomendação; 6/20/46 perguntas |
| 1:54 | One word for one thing | SAY IT ONCE | grill with docs + GLOSSARY.md (pause ≠ skip); /wait-what |
| 2:41 | Questions you can't settle by talking | UNGRILLABLE | Protótipo descartável em sessão nova; você escolhe olhando |
| 2:56 | /to-spec: the destination | THE DESTINATION | Spec: problema, solução, user stories; seams (ideal: uma); issue `ready-for-agent` |
| 3:29 | /to-tickets and the smart zone | ONE TANK EACH | Contexto degrada após ~150K tokens (smart zone, Dex Horthy); fatias verticais; bloqueios; regra tokens ÷ 150.000 |
| 4:08 | The build, one clean head per ticket | CLEAN HEADS | /implement + /clear por ticket, ou /implement-spec (1.3); test-first na seam |
| 4:41 | Review at two desks | TWO DESKS | code-review com dois agentes novos: contra a spec e contra os padrões |
| 5:19 | /pr and merge danger | MERGE DANGER | /pr (adaptado do show-me do Dex Horthy): resumo, evidência antes/depois, Merge Danger |
| 5:40 | /retro | /RETRO | Ler a sessão e sugerir mudanças no entorno (AGENTS.md, lint, padrões); só sugere |
| 6:31 | A real run from Matt's repo | THE REAL ONE | Spec #1641 (41 user stories) → 10 tickets em ~4 min → 28 commits, merge ~2 h depois |
| 7:06 | Isn't this waterfall? | WATERFALL? | Spec é projeção das decisões e some ao fechar a issue; protótipos evitam o waterfall |
| 7:33 | Too defensive for today's models? | TOO DEFENSIVE? | 16 de 27 skills só existem quando digitadas; 660 tokens instalados; skills são removidas quando o harness alcança |
| 8:04 | The one-line skill | ONE LINE | grill-me tem uma linha; grilling tem 28; o valor está nas perguntas |
| 8:28 | Your job | THE GENERAL | Agente = sargento tático, você = general estratégico; o caso do café resolvido; CTA |

### 1.3 O fluxo descrito, na ordem do vídeo (nomes como aparecem)

1. **`/grill-me` → skill `grilling`** (0:53–1:53). Antes de existir código, o agente entrevista você. Mapeia a
   árvore de decisões, pega a **fronteira** (decisões cujo pai já foi resolvido) e pergunta todas numa rodada
   numerada, cada uma com resposta recomendada. Fatos o agente busca no código com um agente auxiliar; decisões
   são suas. Só sai quando a fronteira está vazia e há acordo. Na tela, `/grill-me` é um wrapper de uma linha que
   chama a skill `grilling` (8:07–8:16, `f_050`).
2. **`/grill-with-docs`** (1:54–2:16). A mesma entrevista mantendo um glossário no repo (`GLOSSARY.md` na tela,
   `f_013`–`f_016`): uma linha por termo e as palavras a evitar.
3. **`/wait-what`** (2:33–2:40). Reapresenta a última mensagem do agente em inglês simples, usando o glossário
   (nome legível no quadro denso de 2:40).
4. **Protótipo** (2:41–2:56). Para perguntas "ungrillable" (como deve ser a tela), o agente passa para uma
   sessão nova, gera um protótipo descartável com telas bem diferentes, você escolhe clicando e a resposta volta
   para o grilling.
5. **`/to-spec`** (2:57–3:28). No mesmo chat, sem novas perguntas: problema, solução, lista numerada de user
   stories. Antes, combina as **seams** (onde os testes vão tocar; ideal: uma). Sobe como issue com o rótulo
   `ready-for-agent` (`f_021`).
6. **`/to-tickets`** (3:29–4:07). Fatia a spec em tickets que cabem numa sessão nova (dentro da smart zone),
   cada um atravessando todas as camadas (database → API → tela); dependências explícitas ("Three and four can't
   start until one is done").
7. **`/implement`** por ticket, com `/clear` entre eles, ou **`/implement-spec`** (novo no 1.3): um agente por
   ticket pronto, cada um numa cópia do repo, tudo na mesma branch (4:08–4:40). Sempre test-first na seam. O
   passo de refactor saiu do implement e foi para o review.
8. **`code-review`** em "duas mesas" (4:41–5:18): um agente novo lê o diff contra a spec; outro contra os
   padrões de código e code smells do *Refactoring* (Fowler).
9. **`/pr`** (5:19–5:39): descrição com resumo, evidência antes/depois e seção **Merge Danger** (porta de mão
   única ou dupla; raio de impacto).
10. **`/retro`** (5:40–6:30, novo no 1.3): antes do `/clear`, o agente relê a sessão e sugere mudanças no
    entorno (linha no AGENTS.md, regra de lint, padrões). Não aplica sozinho; você escolhe.

**Research e wayfinder.** O vídeo não descreve uma skill de research nem o `/wayfinder` na narração. "Research"
aparece só como tipo de ticket no caso real: o último ticket "stayed open on purpose as research" (6:46–6:50;
na tela, `#1651 · research · stays open`, `f_041`). `/wayfinder`, `research`, `/handoff`, `/triage`,
`/to-questionnaire`, `/teach` etc. aparecem apenas como blocos no mosaico das 27 skills (`f_048`, ~7:55). Ou
seja, o vídeo **não** apresenta a ordem `/wayfinder → /to-spec → /to-tickets → /implement`; a ordem dele começa
em `/grill-me`.

**Mosaico das 27 skills (`f_048`), leitura a 640 px.** Contornadas sólidas ("11 solid: the agent reaches for
them"): domain-modeling, codebase-design, wizard, pr, prototype, tdd, grilling, code-review, research,
diagnosing-bugs, writing-for-agents. Tracejadas ("16 outline: only when you type them"): /implement-spec,
/triage, /ask-matt, /implement, /handoff, /to-tickets, /to-spec, /improve-codebase-architecture, /retro,
/wayfinder, /setup-matt-pocock-skills, /grill-with-docs, /grill-me, /teach, /to-questionnaire, /wait-what.
(Observação: em `f_033` o PR aparece como `/pr`; no mosaico, `pr` sólido. Não verificado qual é o nome
canônico.)

### 1.4 Frases-chave (transcrição, literais)

- 0:42–0:46: "You wrote one sentence, so it filled every gap with a guess and kept going."
- 1:15–1:20: "finds every decision whose parent is already settled, called the frontier, and asks you all of them in one numbered round."
- 1:31–1:37: "Facts are the agent's job: if the answer is somewhere in the code, it sends a helper agent to go and read it. Decisions are yours."
- 3:26–3:27: "The spec is the destination. The tickets are the journey."
- 3:29–3:32: "Why tickets? Because an agent gets worse the more it's holding."
- 4:44–4:46: "An agent that has written some code thinks it's fine, because it wrote it."
- 6:11–6:14: "A mistake a machine can spot gets a check, full stop"
- 7:19–7:23: "He calls a spec a projection of the decisions made during grilling"
- 8:25–8:27: "The value is in the questions, and only you can answer them."

### 1.5 Por que o fluxo importa (segundo o vídeo)

- Um prompt maior não resolve: você só escreve as decisões em que pensou (0:47–0:53).
- Separar fatos (agente) de decisões (humano) e só codar com a fronteira vazia (1:31–1:42).
- Um termo por coisa reduz a verbosidade e a ambiguidade do agente (2:17–2:22).
- Sessões limpas por ticket protegem a qualidade do raciocínio (smart zone, 3:29–3:40).
- Revisor separado acha o que o autor não vê; modelos seguem mal listas de "não faça" enquanto constroem (4:44–5:11).
- O retro transforma o atrito enterrado na transcrição em melhorias do repo (5:52–6:20).
- Contra "waterfall": a spec é descartável; as decisões vivem no código, nos testes e no glossário (7:13–7:31).
- Contra "defensivo demais": a maioria das skills custa zero até ser chamada (7:44–7:57).

---

## 2. Linguagem visual

**Formato geral.** Explainer 100 % motion graphics 2D, sem gravação de tela real e sem apresentador em
câmera. Só narração em off (o narrador se apresenta como Kevin em 8:55; não aparece em nenhum quadro visto).
Artefatos reais (tweets, issues, PR, SKILL.md) são **recriados** como cartões estilizados, não capturados.

**Fundo e paleta.**
- Fundo único, quase preto azulado, igual em todos os 54 quadros. Nenhuma seção muda o fundo. Em "THE GENERAL"
  (`f_052`–`f_054`) aparece uma grade de pontos muito sutil.
- Traço principal branco-gelo para personagens e linhas.
- Três acentos com papel semântico fixo:
  - **verde**: decidido, correto, solução, agente (`f_009`/`f_010`: nós decididos em verde; caption "Decisions are yours." em verde);
  - **vermelho/rosa**: erro ou palpite ("Your agent **decided.**" `f_004`; "a guess." `f_005`; "worse" `f_022`; linhas `stripe.charges.create` com borda vermelha `f_037`);
  - **âmbar/amarelo**: números, limites e alertas ("10 min" `f_003`; "150K · smart zone" `f_022`; "188,917" `f_022`; caixa "Merge Danger" `f_034`; contador "3" `f_011`).
- Cartões de UI em cinza-azulado escuro, cantos arredondados e borda fina.

**Tipografia.** Três famílias (fontes exatas **não verificadas**):
- monoespaçada para rótulos de seção, código, terminal e nós da árvore;
- sans bold para as legendas-punchline e os títulos de cartão;
- serifada itálica para apartes ("murky" `f_022`; "What does that mean?" no balão, `f_016`; "~ almost nothing in there to copy ~", `f_051`).

O **rótulo de seção** fica sempre no canto superior esquerdo, em monoespaçada caixa-alta cinza, pequeno e com
espaçamento largo (YOUR COFFEE BREAK, THE FOG, ONE TANK EACH…). Funciona como capítulo visível o tempo todo
(todos os quadros).

**Como o texto aparece.**
- **Legenda-punchline**: uma frase curta (2 a 7 palavras) centralizada embaixo. Fica branca com a parte final
  colorida pelo código semântico. Aparece só nos momentos-chave, não como legenda contínua: `f_004`, `f_005`,
  `f_010`, `f_014`, `f_018`, `f_022`, `f_023`, `f_025`, `f_026`, `f_038`, `f_042`, `f_043`, `f_045`, `f_047`,
  `f_054`. Às vezes vem em duas linhas que entram uma depois da outra: em 2:40–2:43 o quadro denso mostra
  "What should the pause screen look like?" e depois "No question card settles it." Entra com fade (`f_023`
  pega a legenda semitransparente). Animação palavra a palavra: **não verificado**.
- **Build progressivo**: listas e checklists ganham um item por vez, sincronizados com a fala. Em 0:00–0:03, o
  checklist "database + api / pause screen / tests / types" ganha um item a cada ~0,5–0,75 s enquanto a barra
  enche.
- **Digitação (typewriter)** em arquivos e código: `AGENTS.md` com "Billing lives in sr…" pela metade (`f_037`);
  linha 6 de `grill-me/SKILL.md` pela metade, "Call the Skill tool with "" (`f_050`).
- **Contadores animados**: "3" a caminho de 46 com a grade de bolinhas enchendo (`f_011`); estrelas "★ 0"
  (`f_049`) → "276,300" (`f_050`); "0 user stories" (`f_040`); "+9,848" linhas (`f_042`), que é provavelmente o
  contador no meio da animação, porque a narração diz "almost fourteen thousand" (**não verificado**).
- Código colorido em estilo IDE, curto (3–6 linhas): `f_028`, `f_029`, `f_052`.

**Ilustração e personagens.**
- Dois personagens fixos, em traço branco "à mão" (contorno levemente irregular):
  - o **humano**, um boneco palito (às vezes com laptop ou caneca de café);
  - o **agente**, uma bolha preta com olhos, um brilho/antena verde em forma de estrela e expressões que mudam: sorriso, zangado, preocupado, olhos em espiral quando o contexto está "turvo" (`f_022`/`f_023`), chapéu de sargento no fim (`f_053`).
- Uma linha fina curva com pontos nas pontas liga o agente ao humano ou a cartões (`f_006`, `f_022`, `f_037`,
  `f_050`).
- **Metáforas visuais recorrentes**, uma por conceito:
  - névoa (blur cinza) = ainda não decidido (`f_007`–`f_009`);
  - árvore de decisões cujos nós ficam verdes quando decididos (`f_009`, `f_010`);
  - luminária com cone de luz = destino/spec (`f_019`–`f_021`);
  - tanque/proveta com camada marrom "murky" acima da linha de 150K = contexto degradado (`f_022`–`f_025`);
  - quatro colunas verticais com as camadas screen/API/database = fatia vertical (`f_024`);
  - escrivaninhas com luminárias = mesas de review (`f_029`–`f_032`);
  - porta com setas nos dois sentidos = porta de mão dupla (`f_034`);
  - cartas de baralho = code smells (`f_031`);
  - chapéu de sargento + "tactical / strategic" (`f_053`).
- **Objetos-âncora que voltam**:
  - o saco de café com etiqueta "1st" e o calendário "PAUSED ON THE 29": `f_004`, `f_005`, `f_034` (antes/depois) e `f_054` (resolução);
  - a árvore de decisões: `f_008`–`f_010`, `f_019`, `f_044`, `f_045`, `f_052`–`f_054`.

**Ênfase (destaques, setas, caixas).**
- Borda verde brilhante (glow) no item em foco ou resolvido: Q1–Q3 (`f_009`), user story 7 (`f_020`),
  "billing module" (`f_021`), tickets com ✓ (`f_024`), `/retro` (`f_036`), "Door: two-way" (`f_043`).
- Esmaecimento do que não importa agora: a mesa "Spec" acesa e Implementer/Standards apagados (`f_032`); cartões
  de perguntas já respondidas em baixa opacidade (`f_010`, `f_012`).
- Riscado (strikethrough) nas regras que viraram checagem automática (`f_038`).
- Sublinhado verde na frase-chave dos tweets (`f_002`, `f_035`, `f_045`).
- Pílulas/etiquetas pequenas: "missing" (`f_030`), "new in 1.3" (`f_027`), "ready-for-agent" (`f_021`),
  "research · stays open" (`f_041`).
- Setas verdes simples: "the seam" (`f_021`), seta subindo até "150K · smart zone" (`f_022`).
- Bordas coloridas por tipo em linhas de log: amarelo = busca desperdiçada, vermelho = chamada errada (`f_037`).

**Transições.**
- Nenhum corte seco perceptível. A detecção de cena do ffmpeg acusa só 3 mudanças acima do limiar 0,1 em 545 s
  e 16 acima de 0,05. As 16 coincidem com as trocas de seção (17,2 s; 62,7; 114,3; 161,8; 176,9; 209,3; 224,1;
  248,4; 281,2; 319,4; 340,8; 377,8; 426,5; 453,9; 508,8 s).
- Entre seções, a cena some por fade para o fundo e os elementos novos entram com fade, um a um. No quadro
  denso de 0:17,25 o novo cenário aparece semitransparente; em 2:41,75 o boneco está a meio fade.
- Dentro de uma seção não há transição: o mesmo "palco" evolui e ganha elementos. Exemplos: o glossário grande
  vira um cartão pequeno no canto (`f_014` → `f_015`); a spec encolhe e vai para a esquerda para abrir espaço à
  seam (`f_020` → `f_021`). Pelos quadros, isso parece reposicionamento animado (morph/slide), mas o movimento
  em si é **não verificado**.

**Câmera.** Enquadramento estático quase o tempo todo. Uma exceção provável: em THE GENERAL a árvore aparece
pequena (`f_052`), grande (`f_053`) e de novo pequena com mais elementos (`f_054`), o que sugere zoom in/out ou
re-layout (**não verificado** se é câmera ou escala dos objetos). Não há pan nem tremor de câmera.

**Ritmo.**
- ~16 "palcos" (seções) em 545 s, média de ~34 s por palco. Variação: ~15 s em ASK FIRST e UNGRILLABLE, ~50 s
  em THE FOG e /RETRO.
- Dentro do palco, algo muda a cada 2–5 s (item, legenda, expressão, contador). Em todo par de quadros
  consecutivos a 10 s há mudança visível de conteúdo.
- Narração densa (~150 palavras/min pela transcrição), sem pausas longas.

**Abertura (primeiros 30 s, `f_001`–`f_003` + quadros densos).**
- Entra do preto: a mesa aparece em fade (0:00).
- O boneco com café está ao lado de um laptop "building feature…" cuja barra e checklist enchem em ~3 s.
- Um cartão "Matt Pocock" entra em fade (≈0:05). O tweet do v1.3 aparece com "v1.3" sublinhado (≈0:15).
- O problema aparece em 0:17 com o mesmo vocabulário visual da explicação inteira.
- Não há título nem logo de canal na abertura (nos quadros vistos).

---

## 3. O que emprestar para o nosso vídeo

1. **Um caso concreto do começo ao fim.** Escolher uma decisão pequena e palpável (o "saco embalado") e
   resolvê-la só no fecho. Evidência: 0:25 → 8:46–8:54; objetos em `f_004`, `f_034`, `f_054`.
2. **Abrir e fechar com a mesma pergunta.** Pergunta no segundo 3, resposta em uma palavra no fim. Evidência:
   0:03 e 8:28–8:30.
3. **Uma metáfora visual por conceito, e reusá-la.** Névoa = indecisão, tanque = contexto, mesas = revisão,
   porta = reversibilidade. A árvore volta cinco vezes como callback. Evidência: `f_007`–`f_010`, `f_022`,
   `f_029`, `f_034`, `f_044`, `f_053`.
4. **Código de cor semântico fixo e mínimo.** Verde = decidido/certo, vermelho = palpite/erro, âmbar =
   número/limite. Nunca usado decorativamente. Evidência: `f_004`, `f_009`, `f_022`, `f_037`.
5. **Rótulo de seção permanente no canto.** Caixa-alta monoespaçada pequena, dá orientação sem tela de título.
   Evidência: todos os quadros (canto superior esquerdo).
6. **Uma legenda-punchline por palco.** Frase de 2 a 7 palavras embaixo, com a parte decisiva colorida; não usar
   legenda contínua. Evidência: `f_010` "Facts are its job. Decisions are yours."; `f_014`; `f_038`; `f_054`.
7. **Palco que evolui em vez de cortes.** Manter a cena e acrescentar ou reposicionar elementos no ritmo da fala;
   trocar de palco só na mudança de seção, com fade pelo fundo escuro. Evidência: detecção de cena (16 trocas
   em 545 s, todas em seções); quadros densos de 0:17 e 2:41.
8. **Build sincronizado com a narração.** Itens de lista, nós da árvore e checks entram um a um quando são
   ditos. Evidência: checklist de 0:00–0:03; Q1–Q3 em `f_009`; tickets em `f_024`.
9. **Atenção por esmaecimento.** Apagar o que não é o foco em vez de pôr setas. Evidência: `f_032` (só a mesa
   Spec acesa), `f_010` e `f_012` (cartões respondidos esmaecidos).
10. **Artefatos reais recriados como cartões limpos.** Tweet, issue, PR e SKILL.md redesenhados na paleta do
    vídeo, com a frase-chave sublinhada em verde e o arquivo digitado ao vivo. Evidência: `f_002`, `f_033`,
    `f_037`, `f_045`, `f_050`.
11. **Números como protagonistas animados.** Contador grande em âmbar ou verde quando o número é o argumento
    (46 perguntas, 188.917 tokens, 276.300 estrelas, 10 tickets). Evidência: `f_011`, `f_022`, `f_049`–`f_050`,
    `f_041`–`f_042`.
12. **Dois personagens simples com expressão.** Humano (boneco palito) e agente (bolha com antena verde); o
    estado do sistema aparece no rosto do agente (olhos em espiral = contexto cheio). Dispensa apresentador.
    Evidência: `f_003`, `f_022`–`f_024`, `f_053`.

---

## 4. Não verificado

- Fontes tipográficas exatas e valores hex das cores (estimados a olho em JPEG 640 px).
- Movimento real entre quadros: se os reposicionamentos (`f_014` → `f_015`, `f_020` → `f_021`, `f_052` →
  `f_054`) são morph/slide/zoom ou cortes suaves; easing e duração dos fades.
- Se as legendas entram palavra a palavra ou frase inteira; se há som, trilha ou efeitos sonoros (o áudio não
  foi analisado).
- Os últimos ~5 s (8:55–9:05, "I'm Kevin… Subscribe"): sem quadro; cartão final, logo ou rosto do narrador não
  vistos.
- "+9,848" na tela (`f_042`) contra "almost fourteen thousand lines" na narração (6:52–6:57): parece o contador
  no meio da animação, mas não confirmei.
- Números citados pelo vídeo (276.300 estrelas, "more stars than React", 1,3M instalações, 660 tokens, 27
  skills, datas de 4/out e 25/set): repassados do vídeo, sem conferir na fonte primária
  (`github.com/mattpocock/skills`, skills.sh).
- Nomes das skills lidos do mosaico `f_048` em baixa resolução, além da diferença `/pr` (`f_033`) × `pr`
  (`f_048`). O vídeo não explica `/wayfinder` nem `research` como skill; a ordem que ele apresenta começa em
  `/grill-me`, não em `/wayfinder`.
- A descrição do vídeo vem truncada na seção "Sources", então a lista de fontes do autor não foi lida.
