# Relatório do QA, porta da amostra, volta 1

Testado em 2026-10-15: `amostra/amostra.html` (92 KB). Três coisas: `medidas-da-peca` nas larguras 320, 768, 1280 e
1920; um teste próprio da navegação do canvas, do zoom e dos sete cenários (1280 x 1000, 320 x 640 e 1920 x 1080); e
a leitura do código do canvas para saber o que simular. Só medi e relato; não editei a peça.

**Modo:** marcado. 58 itens (os 40 das etiquetas entram agora como item), 23 ligações, 2 pontos de encontro.

## 1. Medidas da peça (vista inicial)

| Medida (limiar) | 320 | 768 | 1280 | 1920 | Veredito |
|---|---|---|---|---|---|
| R1 cruzamentos fora de encontro (0) | 0 | 0 | 0 | 0 | **passa** |
| R2 rótulos do desenho (sem teto; mistura tinha 25) | 27 | 27 | 27 | 27 | sem número de limite; ver R3 |
| R3 folga mínima (>= 1 rótulo) | 18 px de 15 | 14,9 de 12 | 22,3 de 19 | 22,7 de 19 | **passa** |
| R3 razão entre grupos / dentro (>= 1,5) | 1,53 | 1,53 | 1,53 | 1,53 | **passa**, por 0,03 |
| Contraste | 41 de 41 | 58 de 58 | 58 de 58 | 58 de 58 | **passa** (0 falhas, 0 não verificados) |
| Focáveis sem nome | 0 | 0 | 0 | 0 | **passa** |
| tabindex positivo | 0 | 0 | 0 | 0 | **passa** |
| Rolagem da página | 320 x 1000, sem | sem | sem | sem | **passa** |
| Códigos internos soltos | 0 | 0 | 0 | 0 | **passa** |
| Links quebrados | nenhum `<a>` no HTML (0) | | | | **passa** |
| Rede externa (CDN, fontes, imagens) | nenhuma | | | | **passa** |

- Menores folgas (1280): Porta do banco e Camada de busca 22,3 px; Banco local e Vista Markdown 26,1 px; Vista
  Markdown e Sincronizador 26,5 px. A mediana dentro do grupo é 33,6 px e o mínimo entre grupos 51,3 px.
- Em 320 a vista abre a 75% centrada no Banco local, com texto de 14 px de altura no menor rótulo (15 px de rótulo
  nominal). Com a janela de 640 px de altura, a tela do canvas mede 320 x 515.
- Peso: 92 KB (mistura 81 KB), nada externo. Carga em tempo virtual 215 a 315 ms (mistura 71 ms): quase quatro vezes
  mais lenta, ainda pequena; o custo é a camada de etiquetas, que acha lugar para as 40 uma a uma ao carregar.
- Rótulos no desenho: 27 em todas as larguras (confere com o `amostra.md`). Textos visíveis na primeira tela contando
  o HTML: 58 em 768 a 1920 e 41 em 320 (a faixa estreita deixa parte do texto fora da tela até rolar o desenho).

## 2. Zoom e camada de detalhe

Nível de zoom aproximado: a camada liga em 140%; medi em **182% (1280)**, **183% (320)** e **162% (1920)**, varrendo
a cidade em nove quadrantes por setas.

| Medida | 1280 x 1000 | 320 x 640 | 1920 x 1080 |
|---|---|---|---|
| Camada de detalhe ligada (`perto`) | sim | sim | sim |
| Etiquetas com lugar / total | 40 de 40 | 40 de 40 | 40 de 40 |
| Textos sobrepostos entre si (9 quadrantes) | 0 | 0 | 0 |
| Menor espaço entre dois textos | 11,8 px | 12 px | 10,6 px |
| Menor altura de texto | 21 px | 21 px | 18 px |
| Rolagem da página | 0 | 0 | 0 |

- **Atenção para o juiz de R3:** na camada de detalhe, o menor espaço entre dois textos é 10,6 a 12 px, abaixo da
  altura de um rótulo (19 px na vista inicial; cerca de 30 px aos 160%). Não há sobreposição, mas as etiquetas ficam
  mais coladas aos nomes do que a folga mínima da régua pede para os itens. As etiquetas são texto pequeno, não item
  com bairro; quem decide se a regra vale para elas é a régua, não eu.
- A 140% ou mais, o texto das etiquetas não cai abaixo de 18 px de altura renderizada.
- Tempo de resposta do zoom não medido (tempo virtual).

## 3. Navegação do canvas (eventos sintéticos no próprio navegador)

| Ação | Resultado | Veredito |
|---|---|---|
| Ctrl + roda | aproxima (1 clique de 100 = 1,2x); evento barrado (`preventDefault`), a página não dá zoom | passa |
| Ponto sob o mouse durante o zoom | desloca 0,005 unidade do desenho: fica parado | passa |
| Shift + roda | anda só na horizontal (dx 112 a 155 unid., dy 0) | passa |
| Roda simples | anda na vertical (dy, dx 0); a página não rola | passa |
| Botão direito, arrastar | anda (107 unid. em x e 54 em y no teste); menu de contexto barrado | passa |
| Botão do meio, arrastar | anda | passa |
| Botão esquerdo, arrastar | **não** anda (reservado ao clique nas fichas) | como desenhado |
| Setas (foco no desenho) | andam 60 px de tela por toque | passa |
| `+` e `-` | aproximam e afastam em passos de 1,25x | passa |
| `0` | volta à vista inicial exata (conferi o viewBox) | passa |
| Limites do zoom | 35% a 500% | passa |
| Limite do passeio | 80 setas à direita param com o desenho ainda a meio da tela; 200 à esquerda também | passa |
| Rolagem da página (scrollX e scrollY) | 0 em todos os passos; altura do documento = altura da janela | **passa** |
| Ficha: clicar no bairro e Esc | abre com foco em "Fechar"; Esc fecha e o foco volta ao bairro | passa |
| Cenário ligado, vista | em 1280 e 1920 o nível não muda; a marca do passo fica dentro da tela em todos os passos | passa |

Observações:
- As setas e `+`, `-`, `0` só valem com o foco no próprio desenho (o desenho tem `tabindex=0` e nome). Com o foco
  num botão, as setas passam a mudar o passo do cenário. Isso está no `amostra.md`.
- **Toque (um dedo, pinça): não testado.** O código trata dois dedos e `pointerType=touch`, mas eu não tenho aparelho.
- Roda de verdade e mouse físico não testados: usei eventos sintéticos no mesmo documento, que exercitam os mesmos
  tratadores. O `amostra.md` diz que o autor fez a prova com eventos do protocolo de depuração; não repeti.
- Botão "Ver tudo": não cliquei; testei só `0`, que chama a mesma função de ajuste.

## 4. Os sete cenários

Teste por clique nos botões, "Próximo", seta esquerda, "Sair" e Esc. Resultado igual em 1280, 320 e 1920.

| Cenário | Passos | Marca = número em todos os passos | Marca dentro da tela | Marca sobre texto | Sair e Esc apagam | Foco volta ao botão | Passo de falha |
|---|---|---|---|---|---|---|---|
| O Gustavo edita um arquivo | 6 | sim | sim | 0 | sim | sim | 6 |
| Um agente novo abre sessão | 6 | sim | sim | 0 | sim | sim | nenhum |
| Um maestro novo abre sessão | 6 | sim | sim | 0 | sim | sim | nenhum |
| O Gustavo pede: leia | 4 | sim | sim | 0 | sim | sim | 4 |
| O Gustavo pede: altere | 7 | sim | sim | 0 | sim | sim | 7 |
| O Gustavo pede: remova | 5 | sim | sim | 0 | sim | sim | 5 |
| O outro par altera um arquivo | 5 | sim | sim | 0 | sim | sim | 5 |

- Total: 39 passos, como o `amostra.md` diz.
- O defeito da mistura (marca do passo 5 faltando em "O Gustavo edita um arquivo") **não aparece mais**: 5 marcas no
  passo 5, 6 no passo 6.
- Depois de Esc, os sete botões voltam a `aria-pressed="false"`.
- Clicar num botão leva o foco para "Próximo".
- Em 320 o nível fica em 75% e a vista não saiu do lugar nos passos; a marca ficou dentro da tela em todos.

## 5. Foco

- 23 paradas na ordem do Tab em 1280 e 1920 (7 cenários, o desenho, 9 bairros, 3 pessoas, 3 botões de zoom); 24 em 320
  (a dobra da legenda aparece). Todas com nome; 0 tabindex positivo.
- A medição por script não viu mudança em 12 bairros e pessoas, e a ferramenta ainda não reconhece a regra de foco
  posta no filho (`.bairro:focus-visible>.zona`): `regra_de_foco_no_css: false`. Leitura: **não verificado**, não
  falha. O `amostra.md` afirma 23 de 23 com foco visível por Tab real; não repeti. Quem decide é o UX revisor.

## 6. Não verificado

- Toque (um dedo, pinça) e mouse físico; conforto de uso do canvas (UX revisor).
- Foco visível dos bairros e pessoas com Tab real (acima).
- Se a ordem e o conteúdo dos passos batem com a descrição v3.2 (Tech lead). O conteúdo da peça (fichas, nomes das
  40 etiquetas) não foi conferido por mim.
- Contraste no estado aceso ou apagado, e das etiquetas na camada de detalhe (a ferramenta mede o estado inicial; em
  zoom as etiquetas ficam `display:none` até 140%).
- Olho apertado de R2 sobre a captura. R2 agora sem teto fixo: o critério é não poluir, e isso é julgamento.
- Janela de 1920 x 1080 mostra a vista a 104%; abaixo de 1280 x 800 não medi tela baixa além de 320 x 640.
- break-ui (dados extremos) não pedido.

## Arquivos

- `medidas-320|768|1280|1920.json`, `captura-<largura>.png`, `links.json`, `resumo.txt`.
- `navegacao/nav-1280.json`, `nav-320.json`, `nav-1920.json` (tudo do teste próprio), `navegacao/resumo-navegacao.txt`
  (legível), o script `navegacao/harness.html` e `rodar-navegacao.ps1`.
