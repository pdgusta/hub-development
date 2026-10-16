# Brief das 4 cartas das escolhas do spec (maestro, 2026-10-16)

Pedido do Gustavo (rodada `2026-10-16-revisao-do-spec-r4`): "divida essas 23 escolhas em 4 cartas visuais, cada uma é
uma rodada. Pode colocar 1 'designer de visuais' pra cada".

## O contexto em três frases

O spec da construção do hub (`C:\Projetos\context-hub\.scratch\construcao-do-hub\spec.md` e `spec-partes\`) acabou de
ser revisto por três revisores, que concordaram em tudo (`revisao\acordo.md`). Sobraram 23 escolhas que o spec fez sem
um ticket resolvido por trás; estão marcadas **[núcleo]** no spec e listadas em `acordo.md`, seção (c). O Gustavo decide
cada uma numa rodada do portal, e a sua carta é o que explica as escolhas da sua rodada.

## O que cada carta faz

- Explica cada escolha da sua lista **na ordem da lista** (a rodada terá uma pergunta por escolha, na mesma ordem):
  qual problema ela resolve, o que a escolha faz, e o que acontece sem ela ou com a alternativa. As alternativas estão no
  spec, no `acordo.md` e na conversa dos revisores (`revisao\conversa\r1..r5-*.md`); se não achar alternativa, mostre "com
  a escolha × sem a escolha". Não invente fato: pergunte ao maestro.
- O que o Gustavo já disse: o diagrama no centro; bater o olho e entender; ícones e palavras-chave, pouco texto;
  elogiou o "mapa de metrô" e a "maré"; recusou o laudo denso e a variação só restilizada de uma carta anterior.
  Cada carta tem linguagem visual própria (as quatro não podem parecer irmãs). Nada de código interno (R18, T1, D3,
  "faixa 7", números de ticket) sem dizer em palavras o que é.
- Lê de cima para baixo sem clique obrigatório. Ao fim, um resumo das escolhas da carta, numeradas como na rodada.

## Quem faz o quê

| Designer | Carta | Escolhas (números da seção c do `acordo.md`) | Arquivo | Porta do http.server |
|---|---|---|---|---|
| Designer | 1. Gravar e ler no banco | 1, 2, 3, 4, 5, 21 | `revisao\cartas\carta-1-banco.html` | 8781 |
| Aquarela | 2. Vigia e manutenção | 6, 7, 8, 9, 10, 22 | `revisao\cartas\carta-2-vigia.html` | 8782 |
| Nanquim | 3. A busca | 11, 12, 13, 23 | `revisao\cartas\carta-3-busca.html` | 8783 |
| Guache | 4. Frontmatter, hooks e acervo | 14, 15, 16, 17, 18, 19, 20 | `revisao\cartas\carta-4-regras.html` | 8784 |

Caminhos relativos a `C:\Projetos\context-hub\.scratch\construcao-do-hub\`.

## Regras desta tarefa (valem sobre o papel onde divergirem)

- O Prumo não está no canvas: o revisor é o da seção "Revisores de UI/UX" abaixo. Sem subagentes.
- Conferência visual como diz o papel, mas com a **sua porta** acima e um `--user-data-dir` só seu
  (`%TEMP%\edge-<seu nome>`); mate só os msedge desse perfil.
- Não edite `cartas.json`, rodadas, tickets nem o spec: o maestro cadastra a carta e escreve a rodada.
- Ao terminar: `maestri ask "Claude Code" "<nome>: carta N pronta em <caminho>, PNG em <caminho>"`.

## Revisores de UI/UX (pedido do Gustavo, 2026-10-16, ~17h15)

- **Lente** revisa o Designer (carta 1) e a Aquarela (carta 2); porta de captura 8791.
- **Esquadro** revisa o Nanquim (carta 3) e o Guache (carta 4); porta de captura 8792.
- Antes de avisar o maestro, o designer pede: `maestri ask "<revisor>" "carta N pronta para revisão em <caminho>"`.
  O revisor grava `revisao/cartas/parecer-carta-N.md` e devolve passa ou volta, com consertos. No máximo duas voltas.
- O aviso ao maestro só sai depois do "passa", com o caminho do parecer.
