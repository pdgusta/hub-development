---
title: Vídeo de referência — Claude Mods Are Insane (AI LABS)
data: 2026-10-10
origem: subagente de análise de vídeo (Opus 5.5), ticket 39
fontes: https://www.youtube.com/watch?v=ERNqRK6sMJY; transcrição automática do YouTube (en-orig); 54 quadros extraídos a cada 15 s (14 folhas 2×2), mais 48 quadros densos em três tiras (0:00–0:30 a cada 2 s; 2:00–2:16 e 4:22–4:38 a cada 1 s) e detecção de cortes do ffmpeg (limiar 0,3)
aviso: saída de modelo; descrição visual feita a partir de quadros estáticos, não do vídeo em movimento; o que não deu para ver fica **não verificado**.
---

# Vídeo de referência: Claude Mods Are Insane (AI LABS, 13:28)

**Convenção de tempo dos quadros.** O filtro `fps=1/15` do ffmpeg pega o quadro do meio de cada janela, então
o quadro `fN` fica em cerca de **7,5 s + 15 s × (N−1)**. Exemplos: f1 ≈ 0:07, f18 ≈ 4:22, f54 ≈ 13:22. Conferi a
regra cruzando f1 e f2 com a tira densa de 0:00–0:30, e f3 (0:37, logo da Autometa) com a fala "we're a software company"
em 0:36.

## 1. Conteúdo

### Tese

Os *Claude mods* são plugins que rodam dentro do Claude Code e mudam a interface e o comportamento dele: painel ao lado
do chat, faixa acima da caixa de prompt, redesenho de partes da tela. Diferente de skills e plugins comuns, ficam sempre
ligados. Para mostrar isso, o canal apresenta seis mods que construiu. A descrição fala em sete; contei seis na fala.

### Estrutura (uma linha por segmento)

| Tempo | Segmento |
|---|---|
| 0:00–0:47 | Gancho: "agora você mesmo adiciona o recurso que falta", com a prévia de quatro mods e a apresentação do canal |
| 0:47–2:59 | O que são mods: painel, faixa e redesenho; diferença para skill e plugin; os dois mods nativos (diff e "you should know"); marketplace |
| 2:59–4:00 | Como criar: skill nativa `plugin-authoring`, *hot reload*, mod temporário na sessão e depois "install" |
| 4:00–5:41 | Mod 1, prompt enhancer: reescreve o prompt na própria barra, citando skills instaladas e decisões a confirmar |
| 5:41–5:50 | Pedido de inscrição |
| 5:50–6:39 | Mod 2, direção de design: mostra visualmente cada estilo de design quando o Claude pergunta |
| 6:39–7:54 | Mod 3, rastreador de suposições: faixa "6 assumptions to review", tecla 0, Right/Wrong, reenvio automático |
| 7:54–8:51 | Patrocínio (Runway) |
| 8:51–9:52 | Mod 4, prateleira de ideias: `/idea`, uma prateleira por projeto, persiste, "Send" vira prompt |
| 9:52–10:45 | Mod 5, monitor de sessões: quem espera por você, quem trabalha, quem terminou; `/sessions` |
| 10:45–11:40 | Mod 6, rastreador de sessões na mesma pasta: avisa a segunda sessão do que a primeira está fazendo |
| 11:40–13:01 | Mod 7, "plain-talk": respostas simples, nada de texto entre chamadas de ferramenta, verificação com Haiku, status line |
| 13:01–13:28 | Comunidade paga (AI Labs Pro) e encerramento |

Os mods 6 e 7 podem ser os "sete" da descrição se o rastreador da 10:45 contar à parte. Pela fala, são sete blocos de
mod, dos quais o 5 e o 6 tratam de sessões. A contagem exata fica **não verificada**.

### Afirmações-chave (citações literais da transcrição automática)

1. 00:57: "Claude mods are actually a feature that Anthropic added to Claude Code that lets you modify it and add in new features that Claude Code doesn't already have."
2. 01:13: "A mod lets you change Claude Code's interface by drawing its own panel beside the chat or a strip above the prompt box with buttons and text boxes in it."
3. 01:53: "It's always running and does its job every single time, just like a built-in feature of Claude code."
4. 02:14: "Claude code comes with two built-in mods." (o diff e o "you should know", que liga um agente lateral observador)
5. 03:04: "you'll have a built-in skill called plugin authoring that already knows everything about how to create Claude mods."
6. 03:26: "You need to allow hot reload so that the mod loads as soon as Claude finishes its turn"
7. 03:41: "once Claude is done, the mod only works in this session" (para persistir: "you can just ask Claude to install it for you", 03:52)
8. 07:03: "we created a mod that shows you all the assumptions Claude makes"
9. 10:14: "It shows which sessions are waiting on you, which one is working right now, and which ones are done."
10. 12:28: "it also added a check that uses a Haiku model to make sure the rules are followed."

### O que interessa ao Claude Code (visto nas gravações; afirmação do vídeo, não conferida em documentação)

- **Superfícies de mod**: *pane* (painel lateral), *band* ou *strip* (faixa acima do prompt, com botões e campo de texto),
  redesenho de linhas de ação e da caixa de perguntas (fala de 1:13 a 1:28; mock em f15, 3:37, com "my mod [Run] [Stop]
  type here … reload").
- **Hooks com nome**, mostrados quando o mod recarrega:
  - f31 (7:37): `8 hooks: session.start, prompt.compose, tool.call, classic.Stop, turn.start, turn.complete, command.run, ui.render`
  - f42 (10:22): `3 hooks: session.start, command.run, ui.render`
  - f46 (11:22): `7 hooks: session.start, command.run, prompt.submit, tool.call, turn.complete, session.end, ui.render`
  - f52 (12:52): `8 hooks: … prompt.compose, prompt.attachment, prompt.submit, turn.start, turn.complete, ui.render`
- **Esqueleto de um mod** (mock f14, 3:22): `timer/plugin.json`, `timer/hooks.js`, `timer/strip.js`. Nas gravações
  reais (f18, f37, f45), a skill lê exemplos em `bundled-skills/2.1.294/.../plugin-authoring` (`band.tsx`,
  `band-state.d.ts`, `pane.tsx`, `pane-state.d.ts`, `types/claude-code.d.ts`) e importa `import { atom, read, update } from 'claude-code'`.
- **Desenvolvimento**: `claude --plugin-dir ~/.claude/dev-mods/<uuid>/<mod>` (f21, f40, f42). Mensagem de *hot reload*
  em f49: os mods em `~/.claude/dev-mods/...` recarregam sozinhos quando os arquivos mudam.
- **Comandos e atalhos dos mods**: `/enhance` e o atalho ctrl+x seguido de Tab (f20, 4:52); `/idea` (9:31); `/sessions`
  (f43); tecla 0 com o prompt vazio para abrir as suposições (7:31).
- **Ambiente das gravações**: Claude Code v2.1.294, "Opus 5.5 with medium effort · Claude Max", modo
  `--dangerously-skip-permissions`, "← 2 agents", rodapé com `/remote-control`, `File explorer` e `Rich Input` (f19–f52).
- **Ideias que se aplicam a um hub**: monitor de sessões ("? 1 needs you ● 0 working ✓ 8 done", f42–f43); aviso de
  "Also working in this folder" entre sessões na mesma pasta (f46–f47); prateleira de ideias por projeto que persiste
  (f38–f40); status line do que a sessão está fazendo (12:55).

## 2. Linguagem visual

**Resumo.** São dois regimes. De 0:00 a 4:22 há só motion graphics, uma maquete limpa e escura da própria interface do
Claude Code. A partir de 4:22, gravações de tela reais montadas sobre moldura bordô alternam com remakes curtos em motion
graphics da mesma cena. Não aparece apresentador em nenhum quadro; o vídeo é só narração.

### Fundo e paleta (hex aproximados, lidos de JPEG de 480p)

- **Fundo**: quase preto e neutro, por volta de `#101010`–`#141414`, sem gradiente (f1–f17, intro 0–30 s).
- **Cartões e janelas**: `#1A1A1A`–`#1E1E1E`, borda de 1 px por volta de `#2A2A2A`, raio de canto pequeno, 6–8 px
  (f6, f9, f10, f13).
- **Acento único**: coral ou terracota, por volta de `#D97757`, a cor do Claude. Aparece no asterisco-logo, nos marcadores
  das linhas de ação, no mascote de pixel e nas palavras do spinner, como "Cooking…" e "Noodling…" (f2, f6, f7, f11, f17,
  f28).
- **Cores secundárias, só semânticas**: verde e vermelho de diff, com fundo verde-escuro e vermelho-escuro (f10, 2:22);
  semáforo vermelho, amarelo e verde nas janelas; X rosa e check verde na comparação (tira 2:00–2:16, tiles 2:12–2:14);
  azul nos timestamps de capítulo (f4).
- **Moldura das gravações**: bordô escuro, por volta de `#5A1515`–`#6B1A1A`, visível nas bordas de f18–f52.
- **Realce dentro das gravações**: caixa azul-acinzentada, por volta de `#3A4A66`, atrás das frases-chave do prompt (f18,
  f29, f37, f41, f45); retângulo de contorno branco de cerca de 2 px em volta da linha de resultado (f40, f46).
- **Fora do padrão**: o patrocínio usa a UI do Runway, com botão azul `#2B2BFF` (f33–f35); a página do AI Labs Pro tem
  gradiente rosa e lilás (f53); a tela final é preta com grade branca (f54).

### Tipografia (famílias inferidas, **não verificadas**)

- **Monoespaçada** em tudo que é terminal: prompts, linhas `Bash(...)`, "? for shortcuts". Parece JetBrains Mono ou SF
  Mono. Nomes de ferramenta em negrito e argumentos em peso regular (f6, f11, f14).
- **Sans grotesca** (tipo Inter ou SF Pro) nos rótulos dos motion graphics: "Claude Code", "Claude mods", "skill",
  "plugin", "mod", "the rest". Peso médio, corpo pequeno, cerca de 2–3 % da altura do quadro (f1, f9, f17; intro 6–8 s).
- **Sem títulos grandes** no corpo do vídeo. O único texto grande é o "Thanks for watching" do encerramento, numa sans
  geométrica pesada (f54), e a manchete serifada do site da comunidade (f53).

### Como o texto aparece

- **Não há legenda nem tipografia cinética da narração.** Todo texto em tela é diegético, ou seja, faz parte da UI
  encenada: prompts curtos ("build me a store" em f17, "make me a timer mod" em f14, "add a login page" em f6), palavras de
  spinner, rótulos de linha.
- **Poucas palavras por vez.** Rótulos de 1 a 3 palavras e prompts de até cerca de 6. O texto que não importa vira barra
  cinza arredondada, um *placeholder* (f1, f12, f17, f38; tira 2:00–2:16).
- **Digitação simulada.** Na tira 2:00–2:16, o prompt passa de "/plug" a "/plugin" e abre o menu "Mods built-in on/off".
  Na tira 4:22–4:38, o enhancer troca "add a login page" por "build /login with the auth skill" letra a letra, com o
  rótulo de estado mudando de "rewriting…" para "ready". Um chip de tecla "return ↵" aparece no canto.

### Gravações de tela e motion graphics

- **0:00–4:22**: só motion graphics. A detecção de cortes achou **zero cortes secos entre 1:00 e 4:22** e só dois antes de
  1:00 (0:38 e 0:39, na entrada e na saída do logo da Autometa). Isso sugere uma tela contínua em que os elementos entram,
  saem e se reorganizam, sem corte.
- **A partir de 4:22**: gravação real, recortada e ampliada para o texto ficar legível em 480p, sobre a moldura bordô. O
  deslocamento da moldura muda entre f18 e f19 (bordô à esquerda e embaixo, depois à direita), o que indica pan ou zoom
  animado sobre a gravação (**movimento não verificado**).
- **Alternância**: na tira 4:22–4:38, a gravação aparece em 4:22 e dá lugar em 4:23 a um remake em motion graphics da mesma
  ideia (pasta my-app + "add a login page" + cartão de skills, depois o painel "Prompt Enhancer"). A gravação volta em 4:35.
  O mesmo padrão aparece em f23 (5:37), f28 (6:52), f36 (8:52), f38 (9:22), f44 (10:52), f48 (11:52) e f50 (12:22): cada
  mod tem pelo menos um remake limpo.

### Ícones e ilustrações

- Ícones de linha fina: livro para skill, peça de quebra-cabeça para plugin, controles deslizantes para mod (f9; tira 2:00).
  Também pasta, lâmpada (ideias, f38), arquivo e calendário.
- O mascote de pixel coral (o "caranguejo" do Claude Code) aparece no cabeçalho das janelas (f6, f7) e como "pet" acima do
  prompt (f7, 1:37).
- O asterisco-logo funciona como nó central dos diagramas de fluxo: prompt → asterisco → saídas (f2, f17, f28).
- Na abertura, partículas quadradas orbitam um círculo "Claude Code", com anéis concêntricos se expandindo (intro 6–10 s).
- Avatares genéricos ligados por linhas representam o compartilhamento no marketplace (f12).

### Transições e câmera (inferidas, **não verificadas** em movimento)

- No bloco de motion graphics, a falta de cortes e os estados intermediários das tiras densas indicam montagem incremental.
  Linhas de lista entram uma a uma, mais ou menos uma por segundo: "skill" em 2:01, "plugin" em 2:02, o chip "mod" entra
  pela direita em 2:04 e se encaixa na lista em 2:06. Cartões trocam por fade ou deslize.
- A coluna escolhida ganha um fundo levemente coral quando recebe o check (tile 2:14).
- Na abertura, os anéis que se expandem sugerem um zoom-out (intro 8–10 s). A duração e a curva de easing **não foram
  medidas**.
- Fora isso, não há sinal de câmera 3D nem de parallax.

### Ritmo

- **Bloco de motion graphics**: um conceito a cada 5–15 s, com um elemento novo a cada cerca de 1 s.
- **Bloco de gravações**: corte seco a cada cerca de 5,7 s (mediana de todo o vídeo).
- **Picos de corte**: 8:14–8:31, no patrocínio, um corte a cada 2–4 s; 12:22–12:44, um a cada 1–5 s; e o encerramento,
  13:06–13:15.

### Destaques

- Realce azul de seleção em frases do prompt (f18, f29 "create a Claude mod", f30 "6 assumptions to review", f42
  "1 working", f52 "Your next step:").
- Contorno branco na linha de resultado (f40, f46).
- Cursor do mouse visível, apontando o ponto relevante (f19, f20, f30, f46).
- Nenhuma seta desenhada por cima da gravação. As setas só aparecem dentro dos diagramas de motion graphics (f2, f17).

### Apresentador

Nenhum: não há rosto em nenhum dos 54 quadros nem nas três tiras. A narração é em off.

## 3. O que emprestar para o nosso vídeo

1. **Fundo quase preto, neutro e chapado (`#111`), com um único acento quente (coral `#D97757`).** Verde e vermelho só para
   diff e certo/errado. Evidência: f1–f17, f10, tira 2:12–2:14.
2. **Ilustrar com a própria UI do produto, encenada e limpa**: janela com semáforo, barra de prompt, "? for shortcuts",
   palavras de spinner. Nada de ilustração abstrata genérica. Evidência: intro 0–4 s, f6, f11, f14.
3. **Nenhuma legenda da narração; só texto diegético de 1 a 6 palavras.** A voz explica e a tela mostra a coisa.
   Evidência: f9, f14, f17.
4. **Texto secundário vira barra cinza (`#2A2A2A`) arredondada.** Só a palavra que importa fica legível. Evidência: f1, f12,
  f17, f38.
5. **Montagem incremental numa tela persistente**: um elemento novo a cada cerca de 1 s, sem cortar a cena; um conceito
   por 5–15 s. Evidência: tira 2:00–2:16 e zero cortes secos entre 1:00 e 4:22.
6. **Comparação em colunas com ícone de linha + X/check**, e a coluna vencedora com fundo levemente tingido do acento.
   Evidência: f9, tiles 2:12–2:14.
7. **Alternar gravação real com remake em motion graphics da mesma cena**: cerca de 1 s de prova real, a explicação limpa,
   e de volta à prova. Evidência: tira 4:22–4:38 (gravação, remake de 4:23 a 4:33, gravação em 4:35).
8. **Gravação sempre recortada e ampliada até o texto ficar legível, sobre uma moldura de cor fixa** (bordô escuro), com
   pan ou zoom lento. Evidência: f18–f52 (movimento não verificado).
9. **Realçar na gravação só a frase-chave**, com fundo de seleção azul-acinzentado, e contornar em branco a linha de
   resultado. Nada de setas sobre a gravação. Evidência: f18, f29, f30, f40, f46, f52.
10. **Digitação simulada com rótulo de estado** ("rewriting…" → "ready") e **chip de tecla** ("return ↵") para mostrar
    interação sem mostrar mãos. Evidência: tira 4:22–4:38 e tira 2:00–2:16 ("/plug" → "/plugin").
11. **Marca como nó central dos diagramas**: entrada → logo → saídas, com setas finas cinza de 1 px. Evidência: f2, f17,
    f28.
12. **Acelerar os cortes (2–4 s) só no trecho final ou comercial**, mantendo o corpo explicativo calmo. Evidência:
    detecção de cortes em 8:14–8:31 e 13:06–13:15 contra zero cortes em 1:00–4:22.

## 4. Não verificado

- **Movimento real**: easing, duração das transições, se as entradas são fade, deslize ou morph, e se há zoom ou pan nas
  gravações. Tudo foi inferido de quadros estáticos e da detecção de cortes, que não vê transições suaves.
- **Áudio**: trilha de fundo, efeitos sonoros, voz humana ou sintética. Não analisei o áudio.
- **Famílias tipográficas e hex**: inferidos a olho, de JPEG comprimido em 480p.
- **Ferramenta de animação** usada pelo canal: desconhecida.
- **Afirmações técnicas do vídeo**, não conferidas em documentação oficial: que o `/diff` e o "you should know" são mods
  nativos; o nome e o comportamento da skill `plugin-authoring`; a lista de hooks; o `--plugin-dir` com `dev-mods`; o
  marketplace, que a transcrição automática grafa "claudmod.com" (URL **não verificada**).
- **Número de mods**: a descrição diz sete e a fala mostra blocos de seis ou sete (ver §1).
- **Patrocínio**: a fala diz "code create 15 for 15% off" (8:45), mas a descrição traz "MKTG50" para 50 %. A transcrição
  automática pode ter errado.
- **Trechos fora da amostra**: a amostragem de 15 s pode ter perdido cenas curtas entre os quadros, como cartões de título
  ou chamadas de inscrição por volta de 5:41.
