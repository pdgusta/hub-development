# emilkowalski/skills

- **URL:** https://github.com/emilkowalski/skills (descrição do repo: "Skills for Designers and Engineers.")
- **Licença:** MIT (arquivo LICENSE, "Copyright (c) 2026 Emil Kowalski").
- **Estrelas:** 46381 (forks 2651, 4 issues abertas). Consultado na API em 2026-10-15.
- **Datas (API):** criado em 2026-03-16; último push em 2026-10-11T13:58:36Z (commit "update readme", branch main); `updated_at` 2026-10-15T12:35:31Z (campo que muda também com metadados, não só com código).
- **Como instalar (literal do README):** `npx skills@latest add emilkowalski/skills`. A forma do vídeo (`emilkowalski/skill`) não foi conferida no repositório; o README traz só a forma acima. O README também cita skills.sh (badge), sem dizer quais agentes o instalador suporta: não verificado.
- **Estrutura:** 15 skills em `skills/<nome>/SKILL.md`, com referências em `.md` ao lado. Não há script, código executável, `package.json` nem configuração de harness. Na raiz: README.md, LICENSE, performance-cheatsheet.md (não é skill), .gitignore, .gitattributes e um arquivo `.pl` de 0 bytes (sem uso aparente; não lido).
- **Formato:** frontmatter YAML com `name` e `description` (e, em 4 skills, `disable-model-invocation: true`). O repositório não cita Codex nem outro harness.
- **Lidos:** README, LICENSE (cabeçalho), performance-cheatsheet.md, os 15 SKILL.md e todas as referências (AUDIT.md, PLAN-TEMPLATE.md, STANDARDS.md, CATALOG.md, API.md, PICKER.md, RECIPES.md de `animate` e de `animate-expo`).
- **Varredura de risco:** nenhum script; nenhum comando de rede nas instruções (só `npx expo install` e `npm install` em exemplos de documentação). Os textos mandam tratar conteúdo do repositório do usuário como dado (regra de defesa, não instrução maliciosa). O scanner de injeção do harness acusou falsos positivos nesses textos.

Skills vistas no vídeo: as 10 estão no repositório. Há 5 a mais: animation-performance, ask-sonner, break-ui, mobile-native, write-swift.

---

## emil-design-eng
- **caminho:** skills/emil-design-eng/
- **no vídeo:** sim
- **description:** This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel great.
- **o que faz de verdade:** Checklist de decisão e polish para UI: se a animação deve existir (pela frequência de uso), qual o propósito, easing (`ease-out` para entrada e saída, curvas customizadas como `cubic-bezier(0.23, 1, 0.32, 1)`), duração abaixo de 300ms, springs, `scale(0.97)` no `:active`, nunca `scale(0)`, `transform-origin` no trigger de popover (modal fica centralizado), só `transform` e `opacity`. Resposta inicial fixa ("I'm ready to help you build interfaces that feel right..."), sem mais nada até haver pergunta.
- **como trabalha:** Sem passos de processo. Só o próprio SKILL.md, sem referências. Exige que a revisão de código saia em tabela Before/After/Why.
- **precisa para rodar:** só texto.
- **riscos:** nenhum visto.
- **harness:** formato Agent Skills (SKILL.md com frontmatter). Codex e outros: não citados no repo.
- **serve para:** guia de decisões de animação e acabamento de UI dentro de uma conversa com o agente.

## animate
- **caminho:** skills/animate/ (referência: RECIPES.md)
- **no vídeo:** sim
- **description:** Build an animation from scratch, making the decisions in the order that determines whether it feels right — should it animate at all, what purpose, which tool, which properties, which curve and duration, how it interrupts, how it exits. Writes the implementation. Use when asked to animate something, add motion, make a component feel alive, or build a transition. For critiquing existing motion use review-animations; for auditing a whole codebase use improve-animations.
- **o que faz de verdade:** Constrói uma animação na ordem de 7 decisões: gate de frequência (ação de 100+/dia não anima), propósito nomeado, ferramenta mais barata (CSS transition, `@starting-style`, WAAPI, Motion), propriedades, easing ou spring, interrupção e saída, reduced motion. Proíbe inventar valores de curva; manda reusar tokens do código existente. Termina com tabela "Never Ship".
- **como trabalha:** Lê o SKILL.md. Carrega RECIPES.md quando o pedido bate com um componente (botão, dropdown, tooltip, modal, drawer, toast, accordion, stagger, hold-to-confirm, tab, scroll reveal, drag, crossfade com blur, WAAPI). Para componente inteiro, manda usar `pick-ui-library`.
- **precisa para rodar:** só texto. As receitas usam CSS e a biblioteca Motion em exemplos.
- **riscos:** nenhum visto.
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** escrever uma animação nova com as decisões justificadas.

## animate-expo
- **caminho:** skills/animate-expo/ (referência: RECIPES.md)
- **no vídeo:** sim
- **description:** Build animations in React Native and Expo, making the decisions in the order that determines whether they feel right — should it animate, which thread it runs on, which properties, spring or timing, how the gesture hands off, how it degrades. Writes the implementation with Reanimated, Gesture Handler, Expo Router and expo-haptics. Use when animating anything in an Expo app, adding gestures, sheets, screen transitions, press feedback or haptics, or fixing motion that stutters on device. For web animation use `animate`.
- **o que faz de verdade:** Versão React Native/Expo do `animate`. Regras: não existe hover; a animação deve rodar na thread de UI (Reanimated, não `Animated` do core); `setState` por frame é proibido; haptic uma vez por ação, no mesmo frame do visual e nunca como único feedback; abas não deslizam (`animation: 'none'`); transição de tela usa a nativa do Expo Router; alvo de toque de 44pt; testar em build de release no aparelho mais lento suportado.
- **como trabalha:** Lê SKILL.md. Carrega RECIPES.md para: press, bottom sheet arrastável, swipe to delete, header que recolhe, entrada de lista, UI sincronizada com teclado (`react-native-keyboard-controller`), indicador de aba, transições de tela, toast, disparo de haptic por limiar.
- **precisa para rodar:** só texto no skill. Os exemplos pedem `react-native-reanimated`, `react-native-worklets`, `react-native-gesture-handler`, `expo-haptics`, `expo-router` e, em um caso, `react-native-keyboard-controller`. Instalação por `npx expo install`. Sem rede e sem script próprio.
- **riscos:** nenhum visto.
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** animação e gestos em app Expo.

## review-animations
- **caminho:** skills/review-animations/ (referência: STANDARDS.md)
- **no vídeo:** sim
- **description:** Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. Default to flagging; approval is earned.
- **disable-model-invocation:** true (só roda quando o usuário pede)
- **o que faz de verdade:** Revisor estrito de código de movimento. Dez padrões não negociáveis, lista de "escalação" que bloqueia (ex.: `transition: all`, `ease-in` em UI, `scale(0)`, animação em atalho de teclado, layout animado), ordem de correção preferida, saída obrigatória em tabela Before/After/Why e veredito Block ou Approve. Recusa revisão de código que não seja de movimento.
- **como trabalha:** Lê o SKILL.md. Carrega STANDARDS.md para citar valores exatos e pede `file:line` em cada achado. Veredito no fim.
- **precisa para rodar:** só texto (lê o código que o usuário indicar).
- **riscos:** nenhum visto.
- **harness:** formato Agent Skills, com flag de invocação manual. Codex e outros: não citados.
- **serve para:** revisar um diff de animação antes de aprovar.

## improve-animations
- **caminho:** skills/improve-animations/ (referências: AUDIT.md, PLAN-TEMPLATE.md)
- **no vídeo:** sim
- **description:** Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained implementation plans for other agents (or cheaper models) to execute. Read-only on source code — it plans improvements, it does not apply them. Use when the user asks to "improve the animations", "audit the motion", "make this app feel better", or wants a roadmap of animation fixes rather than a review of a single diff.
- **o que faz de verdade:** Auditoria de movimento de uma base inteira em 4 fases: reconhecimento (stack, tokens, frequência), auditoria em 8 categorias (com subagentes de leitura em paralelo), triagem com confirmação do usuário, e escrita de planos autocontidos em `plans/NNN-*.md` mais um `plans/README.md`. Níveis `quick`, `standard` e `deep`. Subcomandos: `plan <descrição>`, `execute <plano>` e `reconcile`.
- **como trabalha:** Lê SKILL.md. Carrega AUDIT.md (valores-alvo das 8 categorias) na auditoria e PLAN-TEMPLATE.md na escrita dos planos. Espera escolha do usuário antes de escrever planos.
- **precisa para rodar:** só texto, sem script. O subcomando `execute` depende de subagente e de worktree isolado, que são ferramentas do harness (o repositório não diz quais).
- **riscos:** (1) A regra 1 diz "nunca modifique código-fonte", mas o subcomando `execute` despacha um executor que implementa o plano em worktree isolado; o texto isola a mudança, não a bloqueia. (2) Escreve em `plans/` e cria `plans/README.md`. (3) A regra 4 manda tratar o conteúdo do repositório como dado, e não como instrução (proteção contra injeção, não risco). (4) O scanner de injeção do harness acusou essa regra: falso positivo. (5) O PLAN-TEMPLATE.md tem um caractere de largura zero antes dos cercados de código (observação de formatação).
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** transformar uma auditoria de animação em tarefas que outro agente executa.

## find-animation-opportunities
- **caminho:** skills/find-animation-opportunities/
- **no vídeo:** sim
- **description:** Search a codebase or UI for places that don't animate but should, and reject everything that shouldn't. Read-only; it proposes motion with exact values, it does not implement it. Use when the user asks "what could be animated here?" or wants to "make this feel more alive". For fixing existing animations, use improve-animations or review-animations instead.
- **disable-model-invocation:** não definido no frontmatter
- **o que faz de verdade:** Procura estados que mudam sem transição e cruza cada candidato com um gate de 4 perguntas (frequência, propósito, orçamento de tempo, função). Limita a 5 a 7 sugestões. Obriga a listar 2 a 5 candidatos rejeitados, com a pergunta que os matou.
- **como trabalha:** Só o SKILL.md, sem referências. Passos: recon, varredura por famílias de falha (feedback, estado que aparece sem transição, origem espacial, entradas em grupo, gestos, momentos de "delight"), gate, relatório em três partes (tabela, rejeitados, veredito).
- **precisa para rodar:** só texto. Sugere padrões de busca (grep) mas não executa.
- **riscos:** nenhum visto.
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** achar onde faz sentido animar, e onde não faz.

## animation-vocabulary
- **caminho:** skills/animation-vocabulary/
- **no vídeo:** sim
- **description:** Reverse-lookup glossary that turns a vague description of a web animation or motion effect into its exact term ("the bouncy thing when a popover opens" → Pop in; "the iOS rubber-band scroll" → Rubber-banding). Use when the user asks "what's it called when…", or describes a motion effect without knowing its name and wants the right word to prompt an AI or designer with. For naming an effect, not designing or building one.
- **o que faz de verdade:** Dá o nome técnico de um efeito descrito de forma vaga. O glossário embutido tem cerca de noventa termos em 12 grupos (entradas, sequência, transformações, transições, scroll, feedback, easing, spring, loops, polish, performance, princípios). Regra: citar a definição do glossário sem parafrasear e não inventar termo.
- **como trabalha:** Só o SKILL.md, com o glossário dentro. Formato de resposta: termo em negrito, definição, alternativas com contraste. Diz que espelha uma página `/vocabulary` do projeto do autor (não verificado).
- **precisa para rodar:** só texto.
- **riscos:** nenhum visto.
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** descobrir o nome de um efeito para pedir a um agente ou designer.

## animation-performance (não está no vídeo)
- **caminho:** skills/animation-performance/
- **no vídeo:** não
- **description:** Keep web animations inside the frame budget — animate composite-only properties, keep motion off the main thread when the page is busy, and find the cause when an animation drops frames. Covers the layout/paint/composite pipeline, cheaper property swaps, CSS vs WAAPI vs requestAnimationFrame, Framer Motion's hardware-accelerated path, React re-rendering per frame, inherited CSS variable recalculation, blur cost, and when `will-change` actually helps. Use when an animation is janky, choppy, stutters, or drops frames; when choosing which property to animate; when deciding between CSS and JS animation on performance grounds; or when reaching for `will-change` or GPU layers. For choosing easing, duration, or whether to animate at all use animate; for reviewing motion as a whole use review-animations.
- **o que faz de verdade:** Diagnóstico de animação que trava: tabela de camadas (layout, paint, composite), trocas de propriedade (`width` por `scale()`, `box-shadow` por `filter: drop-shadow()`), thread de cada motor (rAF no main thread; WAAPI e CSS podem ir para a GPU), `setState` por frame no React, variável CSS herdada que força recálculo em filhos, blur acima de 20px e `will-change` só depois de ver o problema.
- **como trabalha:** Só o SKILL.md. Três fases: listar o que anima, diagnosticar em ordem de frequência de causa, relatar com causa, antes e depois e "verificado do código" ou "precisa de gravação em aparelho". Confirmação por DevTools (Performance e Animations) e aparelho intermediário.
- **precisa para rodar:** só texto.
- **riscos:** nenhum visto.
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** achar por que uma animação web trava e qual propriedade trocar.

## apple-design
- **caminho:** skills/apple-design/
- **no vídeo:** sim
- **description:** Apple's approach to interface design and fluid, physical motion, translated for the web. Use when building or reviewing gesture-driven UI, spring animations, drag/swipe/sheet interactions, momentum and interruptible transitions, translucent materials and depth, typography (optical sizing, tracking, leading), reduced-motion, or the design foundations (feedback, spatial consistency, restraint) behind Apple-style interfaces.
- **o que faz de verdade:** Princípios de interface atribuídos a palestras da WWDC (2018, 2020 e 2026): resposta no pointer-down, arraste 1:1 com captura de ponteiro, interruptibilidade a partir do valor atual, springs com `damping` e `response`, handoff de velocidade, projeção de momentum com `decelerationRate` 0,998, rubber-band, materiais com `backdrop-filter`, tracking tipográfico por tamanho, e oito princípios de design.
- **como trabalha:** Só o SKILL.md, sem referências. Organizado em 17 seções numeradas e uma tabela de referência rápida.
- **precisa para rodar:** só texto. Exemplos usam Pointer Events, `requestAnimationFrame` e a biblioteca Motion. As palestras não foram conferidas na fonte primária (não verificado).
- **riscos:** nenhum visto.
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** gestos, springs e materiais em UI web com base em princípios Apple.

## pick-ui-library
- **caminho:** skills/pick-ui-library/
- **no vídeo:** sim
- **description:** Pick the right library for a given frontend task from a curated, opinionated list — numbers, OTP inputs, charts, command menus, virtualization, drag and drop, toasts, state, styling, and more. Only runs when explicitly invoked; it does not trigger on its own.
- **disable-model-invocation:** true
- **o que faz de verdade:** Tabela de tarefa para biblioteca: base-ui (primitivos acessíveis), cmdk, Sonner (toasts), input-otp, Leva ou dialkit, Motion, NumberFlow, torph, Cobe, Satori, shiki, Liveline e recharts, dnd kit, Virtuoso, zustand, clsx, cva, next-themes. Regras: olhar o `package.json` antes e não trocar dependência que o projeto já usa sem pedido.
- **como trabalha:** Só o SKILL.md. Identifica a tarefa, confere dependências instaladas, recomenda uma biblioteca em uma frase e instala se foi pedido.
- **precisa para rodar:** só texto. Pressupõe um projeto frontend com `package.json`.
- **riscos:** nenhum visto. Instala dependências se o usuário pedir, o que é ação de escrita no projeto.
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** escolher uma biblioteca de uma lista fechada, sem menu de opções.

## prototype
- **caminho:** skills/prototype/ (referência: PICKER.md)
- **no vídeo:** sim
- **description:** Build multiple genuinely different versions of a UI piece you describe, rendered behind a visual picker so you can flip through them live and promote the one that feels right. Only runs when explicitly invoked; it does not trigger on its own.
- **disable-model-invocation:** true
- **o que faz de verdade:** Gera de 3 a 5 variantes de um componente que divergem em um eixo nomeado (layout, densidade, movimento, interação), colocadas num picker flutuante escuro. Não toca código de produção. Ao escolher, integra a variante no projeto e apaga a superfície de protótipo, salvo se o usuário pedir para manter.
- **como trabalha:** SKILL.md com seis fases: escopo, reconhecimento, escolha das direções, montagem do picker, verificação (abrir cada variante e, se houver ferramenta de navegador, tirar captura), entrega e promoção. Carrega PICKER.md e copia markup, CSS e JS dele sem alteração.
- **precisa para rodar:** sem script. Monta uma rota de dev server (ex.: `/prototypes/<slug>`) ou um HTML único. A verificação visual exige ferramenta de navegador, que o repositório não define.
- **riscos:** escreve arquivos de protótipo dentro do projeto. A Hard Rule 5 manda apagar a superfície após a escolha sem perguntar, a não ser que o usuário peça para manter.
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** comparar visualmente três ou mais direções de um componente, lado a lado no navegador, com troca instantânea.

## mobile-native (não está no vídeo)
- **caminho:** skills/mobile-native/
- **no vídeo:** não
- **description:** Make a web app feel native on a phone — the small CSS and meta-tag fixes that separate "a website in a browser" from something that feels installed. Covers sticky hover states, tap highlight flashes, the 100vh bug, inputs that zoom the page, laggy taps, pull-to-refresh hijacking scroll, content under the notch, long-press selecting button text, carousels that scroll the wrong way, mismatched status bars, and the rule that you test on real hardware. Use when a web app is being built for or reviewed on mobile, when something "works in Chrome but feels wrong on my phone", when building a PWA, a bottom sheet, a carousel, a full-screen layout, or any touch interaction. For motion itself use animate; for React Native use animate-expo.
- **o que faz de verdade:** Lista de correções de plataforma para web em celular, cada uma com o porquê: hover só com `(hover: hover) and (pointer: fine)`; `-webkit-tap-highlight-color: transparent`; `100dvh` e `100svh`; inputs com 16px (sem `maximum-scale=1`); `touch-action: manipulation`; `overscroll-behavior`; `viewport-fit=cover` com `env(safe-area-inset-*)`; `user-select: none` só em controles; `touch-action: pan-y` em carrossel; `theme-color` por esquema de cor.
- **como trabalha:** Só o SKILL.md, sem referências. Tabela de sintomas, 11 correções, linha de base para projeto novo e tabela "Never Ship". Exige teste em aparelho real.
- **precisa para rodar:** só texto. Cita Tailwind (v3 e v4) e Next.js em exemplos, sem instalar nada.
- **riscos:** nenhum visto.
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** tirar os sinais de "site dentro do navegador" de uma web app no celular.

## break-ui (não está no vídeo)
- **caminho:** skills/break-ui/ (referência: CATALOG.md)
- **no vídeo:** não
- **description:** Try to break a piece of UI by feeding it worst-case data — long names, unbreakable emails, one-letter names, missing fields, huge counts, zero items, long labels, non-Latin text, emoji, extreme numbers — then render it behind a "Demo data / Worst case" toggle and report everything that broke, with the fix for each. Use when the user asks to stress-test, break, or find edge cases in a component or screen, or to "try the worst case". For visual design critique use emil-design-eng; for motion use review-animations.
- **o que faz de verdade:** Cria um conjunto de dados de pior caso plausível (ou o limite real do schema) e o põe atrás de um toggle "Demo data / Worst case", só em dev. Relata quebras por severidade (Broken, Ugly, Fragile) com a correção de cada uma, e para antes de corrigir. A tabela de assinaturas de falha liga o sintoma à causa de CSS (ex.: `min-width: 0`, `flex-shrink: 0`, `Intl.PluralRules`).
- **como trabalha:** Seis fases: mapear campos e limites, montar o pior caso (carrega CATALOG.md, cerca de 75 valores em 9 grupos), ligar o toggle, quebrar em largura real, 320px, zoom 200%, modo escuro e RTL, relatar, corrigir só quando pedido.
- **precisa para rodar:** só texto no skill. Na prática, precisa de acesso ao código para editar fixtures e o toggle, e de ferramenta de navegador para captura (opcional; o skill diz quando inferir).
- **riscos:** escreve fixture e toggle no projeto quando invocado. A regra 4 exige que o toggle fique atrás de gate de dev. Não há comando de rede nem de apagar.
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** achar quebras de layout e de dado com nomes, e-mails e contagens extremos.

## ask-sonner (não está no vídeo)
- **caminho:** skills/ask-sonner/ (referência: API.md)
- **no vídeo:** não
- **description:** Guide to Sonner, the React toast library — install and wire up the Toaster, pick the right toast() call, promise and loading toasts, updating, dismissing and persisting toasts, styling, theming and icons, positioning and multiple toasters. Use when working with Sonner or troubleshooting it — toasts that don't appear, appear twice, lose their styles, ignore Tailwind classes, sit behind a modal, or don't follow dark mode.
- **o que faz de verdade:** Guia de uso e depuração da biblioteca Sonner: um `<Toaster />` na raiz, `toast()` no cliente, escolha da chamada certa, atualização por `id`, persistência com `duration: Infinity`, escada de estilo (defaults, `toastOptions`, `classNames` com `!important`, headless com `toast.custom`), e tabela de sintomas (toast duplicado, tema ignorado, toast atrás de modal).
- **como trabalha:** SKILL.md e API.md (props e defaults de `<Toaster />` e `toast()`). Manda consultar o API.md para nome exato de prop.
- **precisa para rodar:** só texto. Assume React (Next.js em exemplos).
- **riscos:** nenhum visto.
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** configurar e depurar Sonner.

## write-swift (não está no vídeo)
- **caminho:** skills/write-swift/
- **no vídeo:** não
- **description:** How to write modern Swift well — modeling with value types, Swift 6 data-race safety and approachable concurrency (@concurrent, main-actor-by-default, actors, task groups), protocols and generics (some vs any), API design, performance and ARC, Swift Testing, macros, and the modern language features agents don't know about yet. Use when writing, reviewing, or migrating Swift, or when a concurrency error, a hang, a data race, a retain cycle, or a performance problem needs fixing.
- **o que faz de verdade:** Guia de Swift moderno com base no toolchain 6.3 (marca como ⚠ o que é de Swift 6.4, ainda não lançado). Cobre value types, progressão de concorrência (single-thread, async, `@concurrent`, actor), a regra de Swift 6.2 em que `async` não muda de ator, `Sendable`, reentrância de actor, Swift Testing, macros, ARC, `Logger` e migração para Swift 6.
- **como trabalha:** Só o SKILL.md, de 42 KB e sem referências. Seções numeradas de 1 a 16 e tabela de referência rápida. Dá ordem de passos para migração.
- **precisa para rodar:** só texto.
- **riscos:** nenhum visto. As datas de toolchain ("current as of August 2026") e os recursos de 6.4 não foram conferidos no swift.org (não verificado).
- **harness:** formato Agent Skills. Codex e outros: não citados.
- **serve para:** escrever, revisar ou migrar código Swift.
