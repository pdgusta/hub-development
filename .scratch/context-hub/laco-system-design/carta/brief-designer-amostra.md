# Brief do Designer: a carta da amostra (ticket 56, etapa 13)

Do maestro, 2026-10-15. A amostra passou na porta em três voltas (`portas/amostra-3/resultado.md`): QA, UX revisor, Tech
lead e Prumo aprovaram. Etapa 13 do `orquestracao.md`: o Gustavo vê a amostra pronta; a troca do `system-design.html`
só com o aval dele.

## O que existe

- A peça: `.scratch/context-hub/laco-system-design/amostra/amostra.html` (canvas de tela inteira: arrastar com o botão
  direito ou um dedo, Ctrl + roda para zoom, Shift + roda para andar na horizontal, + e −, "Ver tudo"; fichas clicáveis;
  os sete cenários acesos passo a passo). `amostra.md` diz o que mudou em relação à mistura e como navegar.
- É a mistura que ele aprovou "sem alteração", agora como página final, com mais rótulos (o teto de 25 saiu).

## A carta

- Arquivo: `.scratch/context-hub/laco-system-design/amostra/carta.html` (na mesma pasta da peça).
- A amostra no centro, ocupando quase toda a carta e utilizável lá dentro (a navegação do canvas tem de funcionar no
  leitor do portal; confira). Uma faixa curta no topo: o que mudou desde a mistura (o canvas e os gestos que ele pediu, os
  nomes que aparecem ao aproximar) e a pergunta: aprovar a amostra para substituir o `system-design.html` no portal
  "System design" do Maestri, ou recusar com o que mudar. Um "como navegar" de uma linha.
- Nada de laudo; os pareceres ficam fora.

## Cadastro

Entrada nova no `portal/cartas.json`: `id: "amostra-da-cidade"`, `titulo` curto, `arquivo`, `pasta`
(`.scratch/context-hub/laco-system-design/amostra`), `ticket: "56"`, `proposito` em uma frase, `decisao: "em aberto:
aprovar a amostra para substituir o system-design.html ou recusar com o que mudar"`, `situacao: "vigente"`, `mestra:
false` e **`"pede_veredito": true`**. Não abra rodada.

## Regras

- Capturas com o Edge sem cabeça: perfil próprio (`--user-data-dir` único); mate só os `msedge` desse perfil, nunca por
  nome.
- Confira a carta no portal (`http://127.0.0.1:8770/`) em 1280 e 320 px, com arrastar e zoom dentro do leitor.
- Ao terminar: `maestri ask "Claude Code" "pronto: <caminho da carta>"`.
