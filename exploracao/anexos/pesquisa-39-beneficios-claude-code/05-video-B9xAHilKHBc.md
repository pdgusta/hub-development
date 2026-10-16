---
title: Vídeo de referência — Stop testing your AI agent's code by hand (The Hype Kevin)
data: 2026-10-10
origem: subagente de análise de vídeo (Opus 5.5), ticket 39
fontes: https://www.youtube.com/watch?v=B9xAHilKHBc; transcrição do YouTube (en); 48 quadros extraídos a cada 5 s; burst de transição (2 trechos, 20 quadros)
aviso: saída de modelo; descrição visual feita a partir de quadros estáticos, não do vídeo em movimento; o que não deu para ver fica **não verificado**.
---

# Stop testing your AI agent's code by hand (The Hype Kevin, 239 s)

Convenção de referência: `fNNN` é o quadro extraído a cada 5 s, com tempo aproximado de (NNN−1)×5 s
(f001 ≈ 0:00, f010 ≈ 0:45, f033 ≈ 2:40). Os rótulos em versalete no canto superior esquerdo de cada
cena ("WHAT'S STOPPING YOU?", "THE USUAL WAY" etc.) são citados como aparecem na tela.

## 1. Conteúdo

**Tese.** Escrever código deixou de ser o gargalo; o gargalo é verificar. Quem roda dez agentes vira
"o departamento de QA". A resposta proposta é o framework open source **e2e** (TesterArmy), que mistura,
linha a linha, passos exatos de teste com metas dadas a um agente, memoriza as ações verificadas e as
reexecuta sem chamar o modelo.

**Estrutura (capítulos da descrição, conferidos contra a transcrição):**

| Tempo | Bloco | O que acontece |
|---|---|---|
| 0:00 | Gancho | Pergunta "o que te impede de abrir 50 PRs por dia?"; contador PRS TODAY 0 → 50 |
| 0:10 | Produto | Cartão do repositório e logo "e2e" |
| 0:16 | Problema | O agente diz "everything works"; o humano clica para conferir; carimbo "QA DEPT" |
| 0:33 | Autoridade | Lauren Tan e Matt Pocock sobre verificação (cartões de post) |
| 0:47 | Jeito tradicional | Teste Playwright passo a passo; botão renomeado → teste vermelho |
| 1:12 | Contraponto | "Só usar um agente?" custa chamadas de modelo e não é determinístico |
| 1:28 | Solução | Exemplo do README: `app.open` (exato), `agent.act` (meta), `agent.assert` (juiz), `expect` (checagem exata) |
| 1:54 | Mecanismo | O agente vê a tela como texto, age, vê de novo, dentro de um orçamento de chamadas |
| 2:08 | Memória | Cache das ações; run 2 com 0 chamadas; se a tela muda, o agente volta e acha "Go Pro" |
| 2:40 | Juiz | O assert vê só a tela final, pode ser outro modelo |
| 2:52 | Modelos e infra | OpenRouter, AI Gateway, APIs, modelo local, assinaturas; laptop, CI, navegadores, simuladores |
| 3:23 | Loop do agente | Skill + MCP server + sessão viva; escreve → roda → lê relatório de falha → corrige |
| 3:42 | Fecho | Volta à pergunta inicial; 50 PRs com "receipts", segunda execução a $0,00 |

**A prática recomendada (agentes testando o próprio código).** O agente de código não entrega "funciona";
entrega evidência. Ferramentas: o runner e2e sobre Playwright (web) e simuladores iOS/Android, uma skill
que o agente lê (`.agents/skills/e2e`, visível em f042) e um MCP server com sessão viva do app. Loop:
escreve a feature → `npx e2e run` → abre `.e2e/failures/upgrade.md` (linha, passos, tela) → corrige → roda
de novo (f045). Verificação em duas camadas: checagens exatas determinísticas (`expect`) e um juiz de IA
separado que só vê a tela final, opcionalmente com outro modelo. Custo controlado por memória das ações
verificadas e por orçamento de chamadas.

**Frases-chave (verbatim):**

1. "Writing the code is handled, Claude Code and Codex do that all day. Checking it is where everything piles up." (0:04–0:08)
2. "because "everything works" means nothing until somebody sees it work." (0:24)
3. "Do that for ten agents and congrats, you're the QA department now." (0:29)
4. "either you sit there and watch your agent, or you make it bring you evidence." (0:43)
5. "At that point your test suite is a vibe check." (1:25)
6. "e2e lets you mix both approaches line by line in the same test." (1:28)
7. "Once a check verifies the result, e2e saves exactly what the agent did." (2:10)
8. "You get script speed on every run where nothing changed, and the agent only steps in when something did." (2:35)
9. "so the agent never grades its own homework." (2:49)
10. "Your agent writes the feature, runs the tests, opens the failure report with the exact line, the steps and the screen where it broke, fixes the code and runs the tests again." (3:32–3:40)

## 2. Linguagem visual

**Formato geral.** 100% motion graphics em tela cheia, 16:9 (o arquivo baixado é 854×480, 30 fps). Nenhum
apresentador em câmera, nenhuma gravação de tela real: tudo, inclusive a "página de billing", o editor de
código e o terminal, é reconstruído como mockup vetorial. Narração em off conduz; a tela ilustra frase a
frase.

**Fundo e paleta.** Fundo único quase preto azulado (aprox. #0D1117), sem gradientes, sem textura, igual do
primeiro ao último quadro. Paleta curta e semântica:
- branco/off-white para traço, números e texto principal;
- **verde neon** como cor de "certo/sucesso/ênfase": antena dos agentes, botão "Upgrade to Pro", chips
  "app works ✓", escudo do juiz, carimbo "PASS" e "NO MODEL CALL", palavra destacada nas legendas (f007, f016, f029);
- **amarelo/âmbar** para dúvida e alerta: "?" grande (f006), carimbo "QA DEPT" (f007), chip "AI JUDGE" e
  moldura do valor prorrateado (f023), "fixes the code" (f045);
- **vermelho/rosa** só para falha: carimbo "FAIL" e linha de código com fundo vermelho (f014–f015);
- azul/ciano claro para itens de cache e chips técnicos ("RUN 2", ".e2e/cache", "nothing changed → replay", f028–f032);
- lilás/laranja/ciano em pontilhado só uma vez, para o caminho errático do agente (f018).

**Tipografia.** Três famílias com papéis fixos:
- **monoespaçada** (estilo JetBrains Mono) para rótulos de seção em versalete pequeno e cinza no canto
  superior esquerdo, números grandes ("PRS TODAY 50", "12", "$0.84", "3 / 20", "0", "$0.00"), código,
  chips e legendas de ícones;
- **serifada itálica** para fala de personagem em balões ("everything works ✓", "upgraded it, trust me",
  f006, f034) e para citações ("bring your own agent and infrastructure", f041; "~ built for the bottleneck ~");
- **sans-serif bold** só nas frases-síntese embaixo da cena, em branco com a parte final em verde:
  "Agents build. You click." (f007), "One renamed button, one red test." (f015),
  "Pay for the clicks once." (f029), "The judge only sees the screen." (f034).

**Como o texto aparece.** Texto nunca é legenda da narração inteira; é rótulo, número ou frase-síntese.
Os números grandes trocam de valor no lugar (0 → 50 entre f001 e f002; 12 / $0.84 em f017–f018; 0 em
f030–f032). Chips de pílula com borda fina (verde, âmbar, azul) aparecem como anotações sobre a cena
("same every time", "$0 per run", f013; "from the e2e README", f020). Na citação de Matt Pocock, a parte
"have it provide evidence" ganha sublinhado/realce verde (burst A).

**Ícones e ilustrações.** Personagens desenhados à mão, em traço branco irregular:
- o **agente** é uma gota/cabeça com antena verde e expressão que muda com o enredo (sorri em f001, fica
  em dúvida com reticências em f006, bravo em f016–f018, feliz em f029, preocupado ao lado do juiz em f034);
- o **humano** é um boneco de palitos com laptop (f006–f007, f015, f046);
- o **juiz** é um escudo com rosto neutro (f033–f034); o escudo com ✓ verde marca "verificado" (f023, f027–f032).
Ícones de produto/tecnologia em tiles quadrados arredondados escuros com legenda mono embaixo
(Claude Code, Codex, OpenRouter, Chromium, iOS simulator etc., f002, f037–f041). Avatares reais só
em círculo, e posts de X reproduzidos como cartões (f008–f010).

**Gravações de tela vs. motion graphics.** Não há gravação real. O "app" é um mockup minimalista de
janela (três bolinhas + URL `acme.app/settings/billing`) que volta em quase todas as cenas como cenário
fixo; o cursor é desenhado e clica nele. O código é mostrado em painel escuro com destaque de linha
(fundo verde na linha em execução, vermelho na que falha, âmbar no assert; f012–f015, f021–f023).

**Composição.** Layout em dois blocos lado a lado (mockup do app + painel de código, ou painel de texto
+ app), muito espaço negativo, elementos alinhados a uma grade simples. Cada cena acumula elementos sobre
o mesmo cenário em vez de trocar de tela: em "THE USUAL WAY" (f012–f015) o mesmo app e o mesmo código
ficam, e só mudam o botão (Upgrade to Pro → Go Pro), o realce da linha e os carimbos.

**Transições (bursts).**
- *Burst A, 46,6–47,5 s, 10 fps (VERIFICATION → THE USUAL WAY):* a_01–a_06 cartão de Matt Pocock parado,
  com realce verde em "have it provide evidence" e o post de Lauren esmaecido atrás; a_07–a_09 tela
  **totalmente vazia**, nem o rótulo de seção fica (corte seco para o fundo, ~0,3 s); a_10 o novo rótulo
  "THE USUAL WAY" começa a surgir muito apagado (fade-in). Os elementos da cena nova entram depois
  (f011, 50 s, já mostra app e código montados).
- *Burst B, 15,0–16,8 s, 5 fps (dentro de "WHAT'S STOPPING YOU?"):* b_01–b_02 cartão do repositório;
  b_03 cartão em fade-out; b_04 só a tagline "~ built for the bottleneck ~" fica; b_05 o logo verde "e2e"
  entra com o chip "TesterArmy · open source" ainda transparente; b_06–b_09 estável; b_10 tela vazia
  (corte para "RIGHT NOW").
- Padrão: **dentro** de uma seção, troca de elemento por fade cruzado mantendo o rótulo; **entre** seções,
  corte para fundo vazio e reconstrução em camadas (rótulo → cenário → anotações). A detecção de cena do
  ffmpeg só achou três cortes fortes (47,2 s, 88,5 s, 160,8 s), coerente com transições suaves.

**Movimentos de câmera.** Nenhum zoom, pan ou rotação perceptível nos quadros: enquadramento fixo do começo
ao fim (**não verificado** para micro-movimentos entre quadros). O movimento vem dos objetos: cursor,
carimbos que "batem" inclinados (QA DEPT, FAIL, NO MODEL CALL, PASS), pontilhado que se desenha (f018),
setas do loop (f044–f045).

**Ritmo.** Uma ideia visual por frase da narração, com troca de estado a cada 2–5 s; seções de 15–40 s.
Narração densa (cerca de 3 palavras/s), sem pausas longas. Abre e fecha com a mesma cena (grade de 10 agentes
+ "PRS TODAY 50"), agora com chips "✓ receipt" sob cada agente e "SECOND RUN $0.00" (f048).

**Destaques.** Carimbos inclinados com contorno grosso para veredictos; realce de linha em código; moldura
âmbar no valor que o juiz confere (f023); sublinhado verde na frase-chave da citação; check verde em
círculo sobre cada agente que entregou (f002).

**Apresentador.** Não aparece. Só a voz (narração em inglês, tom informal e irônico: "congrats", "guess who
gets to fix it").

## 3. O que emprestar para o nosso vídeo

1. **Um fundo, uma paleta semântica.** Fundo quase preto fixo; verde = verificado/certo, âmbar = dúvida ou
   juiz, vermelho só para falha. Nenhuma cor decorativa (f001–f048; FAIL em f015, PASS em f032).
2. **Rótulo de seção mono, pequeno, no canto superior esquerdo.** Funciona como capítulo visível e ancora o
   espectador quando a cena se reconstrói ("THE USUAL WAY", "IT MEMORIZES", "THE LOOP"; f011, f027, f042).
3. **Um cenário recorrente, alterado aos poucos.** O mesmo mockup de app atravessa o vídeo e a história
   acontece nele (botão renomeado em f014, Pro ✓ em f021). Para nós: o mesmo "hub" desenhado em todas as cenas.
4. **Mockup, não gravação de tela.** Reconstruir terminal, código e app como vetor limpo, com só as linhas
   que importam (f012, f020, f043). Evita ruído e dado real na tela.
5. **Personagem simples com expressão narrativa.** Um agente desenhado à mão cuja cara muda com o enredo
   (feliz f001, dúvida f006, bravo f016, aliviado f029) e um humano de palitos para o papel do usuário (f007).
6. **Frase-síntese no rodapé, branca com o final em verde.** Uma por seção, curta, depois que a cena já
   provou o ponto ("Agents build. You click.", f007; "Pay for the clicks once.", f029).
7. **Números grandes como personagens.** Contadores em mono que mudam no lugar contam a história de custo e
   volume (PRS TODAY 0→50, f001–f002; MODEL CALLS 12 → 0, f017 → f028; SECOND RUN $0.00, f048).
8. **Carimbos para veredictos.** Selo inclinado com contorno grosso para marcar o desfecho de um passo
   (QA DEPT f007, FAIL f015, NO MODEL CALL f029, PASS f032).
9. **Realçar a linha que está rodando.** Em código, fundo colorido na linha ativa: verde executando, vermelho
   falhou, âmbar sob julgamento (f013–f015, f021–f023).
10. **Transição entre seções = corte para vazio + reconstrução em camadas.** ~0,3 s de fundo limpo, depois
    rótulo em fade, depois elementos (burst A, 47,2 s). Dentro da seção, só fade cruzado (burst B, 15–17 s).
11. **Abrir e fechar com a mesma imagem, mudada.** A grade de 10 agentes volta no fim com recibos e custo zero
    (f001–f002 vs. f046–f048): o fechamento mostra a tese cumprida sem precisar dizê-la.
12. **Autoridade em cartão, com a frase-chave realçada.** Citar fonte primária como cartão do post, com só
    o trecho que importa sublinhado em verde (f010, burst A). Combina com nossa regra de fonte primária.

## 4. Não verificado

- Micro-movimentos de câmera, easing e velocidade exata das animações entre os quadros (vistos só quadros a
  cada 5 s e dois bursts de 1–2 s).
- Se há trilha sonora ou efeitos sonoros (o áudio não foi analisado; só a transcrição).
- Fontes exatas (JetBrains Mono, serifada itálica e sans bold são inferência visual).
- Valores hex das cores (estimados a olho a partir de JPEG comprimido).
- Se o cursor e os carimbos entram com animação de "pancada"/escala ou só aparecem; os quadros mostram só
  o estado final.
- Conteúdo de cenas curtas que caíram entre dois quadros de 5 s.
- Afirmações técnicas sobre o e2e (orçamento de 20 chamadas, providers, simuladores Expo) vêm do vídeo e da
  descrição; não foram conferidas no README nem na documentação do projeto.
