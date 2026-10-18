# Duas peças visuais: como foi a construção do hub

Pedido do Gustavo (2026-10-17 ~04h40): ao fim da execução, **duas peças visuais que resumam como foi a execução,
cada detalhe**. O maestro decide o que é cada uma (abaixo). Um time por peça: **um Designer e um Revisor**, cada um
com até **2 subagentes** (bons para levantar dados e conferir fatos). As duas peças correm em paralelo.

## As duas peças

**Peça 1: "A construção, ticket a ticket"** (o quê, quem, quando). A construção inteira numa só vista, com o tempo em
escala: do início (2026-10-16, `/implement-spec`) ao fechamento (2026-10-17 20h16, ticket 25 resolvido). Os **44
tickets**: quem construiu, as voltas da revisão (volta/passa), a junção (verde, ou vermelha e desfeita), a resolução.
As dependências entre tickets ("bloqueado por"). Os papéis: construtores (Brasa, Vela, Trilho, Cinzel), revisor (Fiel,
com o Fielzinho até ~14h35), integrador (Rebite), documentador (Lume, desde ~11h55), maestro. Números que importam: 44
tickets, 43 resolvidos, a suíte final (370 testes: 355 verdes, 15 pulados, 0 falhas), quantas junções, quantas voltas.

**Peça 2: "O que atrapalhou e como se resolveu"** (os bastidores). No mesmo eixo de tempo: a **memória livre** da
máquina (o gargalo do dia), a **trava do trabalho pesado** (quem segurava, quanto tempo), as **janelas quietas**, a
**cota do Codex** (quando acabou, a redefinição do Gustavo às 14h25), os **reinícios** (Maestri ~10h05, Windows 21h),
os **achados** que derrubaram algo e o conserto de cada um (ex.: hífen que o Codex troca por sublinhado; caminho curto
do Windows; cabeçalho YAML quebrado; a busca que estourou o prazo com os docs; o rename com EPERM; a nota que não
descia do par A ao B porque o B ainda recebia o hub inteiro), as **regras novas do Gustavo** ao longo do dia (4
construtores; subagentes; Codex só para testes; o documentador) e as **decisões que o maestro tomou pelo mandato**.

## Fontes (só fatos que estão nelas; o que não achar, pergunte ao maestro)

Caminhos relativos a `C:\Projetos\context-hub\.scratch\construcao-do-hub\`:
- `etapas/diario-da-construcao.md`: o diário do maestro, com hora de cada evento (a fonte principal).
- `etapas/registro-de-juncoes.md`: cada junção, com hash e resultado.
- `issues/*.md`: título, `Status:`, `Blocked by:` e os `## Comments` com hora (construção, revisão, junção).
- `etapas/parecer-*.md` e `etapas/relatorio-*.md`: voltas da revisão e o que cada ticket entregou.
- `etapas/logs/`: medidas de memória (`*medida*.csv`, `*.status`), logs de corredor e de junção.
- `etapas/regras-da-construcao.md`: as regras e os "achados comuns".
- `../context-hub/retomada-maestro.md`: "Para rever com o Gustavo" (decisões pelo mandato).
- git: `git -C C:\context-hub log --format="%h %ad %s" --date=iso integracao` (junções com hora) e o log deste
  repositório (`git -C C:\Projetos\context-hub log --format="%h %ad %s" --date=iso`).

Monte primeiro um **arquivo de fatos** (`resumo-visual/fatos-peca-<N>.json`), com a fonte de cada fato (arquivo e
linha, ou hash). A peça só mostra o que está nele. O revisor confere os fatos contra a fonte; fato errado é conserto
obrigatório.

## A régua do gosto do Gustavo (o que ele elogiou e recusou)

- **Diagrama no centro**, pouco texto; texto só em rótulos curtos e chips. Elogiados: o **mapa de metrô** (linhas,
  estações, pátio, setas de volta coloridas) e a **maré** (uma metáfora visual única que carrega a pergunta principal,
  números grandes, quase nenhum texto). Também a carta "como você faz × como seria ideal": **dados reais dele, medidos,
  em escala**.
- **Simplificar não é cortar informação, é comunicar a mesma coisa de um jeito melhor.** O detalhe vai em **camadas**
  (passar o mouse, tocar, expandir), não em seções de texto empilhadas. Recusado: "laudo" denso de seis seções.
- **Linguagem visual própria e ousada** em cada peça; as duas não podem parecer irmãs. "Reinventar" é mudar a forma,
  não o acabamento.
- **Legibilidade:** texto corrido em fonte confortável e com peso (ele aprovou Nunito Sans 16 px e Fraunces nos
  títulos; recusou fontes finas e condensadas no texto). Títulos legíveis de relance, inclusive em 390 px; nada de
  fonte de exibição com contraste extremo ou ornamental.
- Lê de cima para baixo **sem clique obrigatório**; o clique só aprofunda.
- Nunca código interno sem palavras: "ticket 22" pode, mas diga o que ele é ("proxy e kit de cliente"). Nada de dado
  de cliente (só o nome da iniciativa) nem dado pessoal.

## Forma de entrega

- HTML autônomo: `resumo-visual/peca-1-<nome>.html` e `resumo-visual/peca-2-<nome>.html` (CSS e SVG embutidos;
  scripts só de cdnjs.cloudflare.com, cdn.jsdelivr.net/npm ou unpkg.com, com versão exata). Funciona em 1600 px e em
  390 px.
- Conferência visual com o Edge sem cabeça (não pelo painel do Maestri, que congela animação): sirva a pasta com
  `python -m http.server <sua porta> --bind 127.0.0.1` e capture com `msedge.exe --headless=new --disable-gpu
  --user-data-dir=%TEMP%\edge-<seu nome> --window-size=1600,1000 --virtual-time-budget=6000 --screenshot=<png> <url>`.
  Espere o PNG aparecer. **Mate só os msedge com o seu perfil** (filtre `Win32_Process` pela linha de comando com o
  seu `--user-data-dir`), nunca por nome nem "todos". Para 390 px: moldura com `<iframe style="width:390px">`,
  captura em 492 px e recorte dos 390 da esquerda (o Edge sem cabeça não desce de 492). Encerre o servidor depois.
- Portas: Designer da peça 1 8771, Revisor da peça 1 8772, Designer da peça 2 8773, Revisor da peça 2 8774.

## Como o time trabalha

1. O Designer levanta os fatos (subagentes ajudam), propõe ao seu Revisor o **conceito** (a metáfora e o esqueleto, em
   poucas linhas ou um esboço) antes de construir, e incorpora o retorno.
2. Constrói, confere as capturas, pede a revisão.
3. O Revisor captura em 1600 e 390, julga pela régua acima e confere os fatos contra as fontes; grava o parecer em
   `resumo-visual/parecer-peca-<N>.md` (passa ou volta, consertos numerados) e responde ao Designer. No máximo duas
   voltas; na terceira, passa com as ressalvas escritas.
4. Ao passar, o Revisor avisa o maestro: `maestri ask "Claude Code" "<nome>: peça <N> passou, <caminho>"`.

Regras: ninguém edita tickets, retomadas, regras nem o código do hub; só a pasta `resumo-visual/`. Depois de todo
`maestri ask`, confira com `maestri check` se a mensagem saiu do prompt do outro; se ficou parada, mande
`maestri ask "<nome>" --raw "\r"`.
