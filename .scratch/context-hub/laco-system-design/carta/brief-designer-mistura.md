# Brief do Designer: a carta da mistura

Do maestro, 2026-10-15. Ticket 56 (laço do system design), etapa 10 do `orquestracao.md`: a parada do Gustavo antes de
construir, agora com a direção que ele pediu.

## O que existe

- Na carta anterior (`direcao-visual-cidade`, em `conceitos/final/`), o Gustavo escolheu a **mistura**: a B ("Duas
  cidades e a estrada") como base e, da A ("Linhas do hub"), quem acessa ou é responsável por cada componente. Antes, a
  descrição do hub foi refeita (`descricao/descricao-do-hub.md`, v3.2) e testada em três voltas de perguntas escondidas.
- A peça: `.scratch/context-hub/laco-system-design/conceitos/mistura/mistura.html`, com `mistura.md` (ideia, tabela de
  papéis, o que veio da B e da A, como se lê um cenário). O UI engineer está fazendo um acabamento pequeno nela agora;
  eu aviso quando terminar, e a carta a carrega como estiver.
- A porta: passou na volta 2 (`portas/mistura-2/resultado.md`; volta 1 em `portas/mistura-1/resultado.md`).
- Sete cenários respondidos sem texto corrido: escolher um e ver o caminho aceso, passo a passo (os cinco que o Gustavo
  pediu: ele edita um arquivo; agente novo; maestro novo; ele pede ler, alterar ou remover; o outro par altera).

## A carta

- Arquivo: `.scratch/context-hub/laco-system-design/conceitos/mistura/carta.html` (na mesma pasta da peça).
- Diagrama no centro: a mistura grande, utilizável dentro da carta (os cenários funcionando). Pouco texto: a ideia em
  uma frase; o que mudou em relação à B e à A, ligado ao que ele pediu (nenhum componente solto, quem acessa e quem
  responde por cada um, a vista Markdown como a porta dele, a disciplina ligada ao agente); um convite a experimentar
  dois ou três cenários.
- Uma linha no topo: passou na porta em duas voltas (QA, UX revisor e Tech lead); se ele aprovar, o próximo passo é a
  amostra em página à parte, sem tocar o `system-design.html`; se recusar, diz o que mudar.
- Nada de laudo; notas e pareceres ficam fora (quem quiser abre os arquivos da porta).

## Cadastro

Entrada nova no `portal/cartas.json`: `id: "mistura-da-cidade"`, `titulo` curto, `arquivo` e `pasta`
(`.scratch/context-hub/laco-system-design/conceitos/mistura`), `ticket: "56"`, `proposito` em uma frase, `decisao: "em
aberto: aprovar a mistura como direção ou recusar com o que mudar"`, `situacao: "vigente"`, `mestra: false` e
**`"pede_veredito": true`**. A carta `direcao-visual-cidade` continua como está (a decisão dela já está gravada). Não abra
rodada.

## Regras

- Capturas com o Edge sem cabeça: perfil próprio (`--user-data-dir` único); mate só os `msedge` desse perfil, nunca
  `taskkill` por nome.
- Confira a carta no portal (`http://127.0.0.1:8770/`) em 1280 e 320 px.
- Ao terminar: `maestri ask "Claude Code" "pronto: <caminho da carta>"`.
