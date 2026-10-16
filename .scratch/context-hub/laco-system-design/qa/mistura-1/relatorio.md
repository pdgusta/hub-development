# Relatório do QA, porta da mistura, volta 1

Medido em 2026-10-15: `conceitos/mistura/mistura.html`, com `medidas-da-peca` nas larguras 320, 768, 1280 e 1920,
mais um teste dos sete cenários (`cenarios/`). Só medi e relato; não editei a peça.

**Modo:** marcado (17 itens, 9 grupos, 20 ligações, 2 pontos de encontro). Nada adivinhado.

## Números (visão geral)

| Medida (limiar) | 320 | 768 | 1280 | 1920 | Veredito |
|---|---|---|---|---|---|
| R1 cruzamentos fora de encontro (0) | 0 | 0 | 0 | 0 | **passa** |
| R2 rótulos no desenho (máx. 25) | 25 | 25 | 25 | 25 | **passa**, no limite exato |
| R3 folga mínima (>= 1 rótulo) | 18 px (15) | 14,5 (12) | 24,1 (21) | 24,3 (21) | **passa** |
| R3 pares abaixo de 1 rótulo / sobrepostos | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | **passa** |
| R3 razão entre grupos / dentro (>= 1,5) | 1,53 | 1,53 | 1,53 | 1,53 | **passa**, por 0,03 |
| Contraste (47 textos) | 0 falhas | 0 | 0 | 0 | **passa** |
| Focáveis sem nome acessível | 0 de 19 | 0 | 0 | 0 | **passa** |
| tabindex positivo | 0 | 0 | 0 | 0 | **passa** |
| Rolagem horizontal da página | não | não | não | não | **passa** |
| Códigos internos soltos | 0 | | | | **passa** |
| Links quebrados | 0 (nenhum `<a>` escrito no HTML) | | | | **passa** |

Menores folgas (1280): Porta do banco e Camada de busca 24,1 px; Banco local e Vista Markdown 28,2 px; Contrato e
Checkpoint 37 px. Entre grupos o mínimo é 56,5 px; dentro do grupo a mediana é 37 px.

Rótulos: os 25 textos do desenho; 47 textos visíveis na primeira tela contando o HTML (título, faixa, legenda e os
7 botões de cenário). Peso: 73 KB, nada externo. Carga (tempo virtual): 69 ms.

## Cenários (`data-cenario`)

Teste feito com clique nos botões, "Próximo", seta esquerda, "Sair" e Esc, em 1280 e em 320 (resultado idêntico).

| Cenário | Passos | Marcas numeradas | Sair e Esc apagam tudo | Foco volta ao botão |
|---|---|---|---|---|
| O Gustavo edita um arquivo | 6 | 1 a 6 | sim | sim |
| Um agente novo abre sessão | 6 | 1 a 6 | sim | sim |
| Um maestro novo abre sessão | 6 | 1 a 6 | sim | sim |
| O Gustavo pede: leia | 4 | 1 a 4 | sim | sim |
| O Gustavo pede: altere | 7 | 1 a 7 | sim | sim |
| O Gustavo pede: remova | 5 | 1 a 5 | sim | sim |
| O outro par altera um arquivo | 5 | 1 a 5 | sim | sim |

- Cada cenário acende o passo 1 e acumula; ao sair, 0 elementos acesos, 0 marcas, painel oculto, corpo sem o estado
  de cenário. O botão do mesmo cenário liga e desliga. A seta esquerda volta um passo. `aria-pressed` acompanha.
- Todos os 37 elementos com `data-cenario` entram em algum passo; nenhum passo ficou com 0 elementos novos marcados.
- **Passos que não acendem nada novo na tela** (a marca numerada cai num elemento que já estava aceso):
  gustavo-edita passo 5 ("Lá, o disco atualiza…" marca "Outro par"); pede-ler passo 4 (marca "Porta do banco").
  Servem só pelo número e pela frase.
- **Passos que acendem componente sem linha** (nenhuma ligação nova acesa): maestro-novo passos 4 ("Ferramentas
  da máquina"), 5 ("Disciplina do agente" e "Conteúdo") e 6 ("Acervo do maestro" e "Gustavo");
  pede-remover passos 2 ("Periferia do par", "Outro par") e 5 ("Conteúdo", "Gustavo"). Para o juiz: conferir se o
  caminho se lê assim, ou se falta ligação marcada.
- Passos finais que mostram falha ou algo em aberto: gustavo-edita 6 (colisão), pede-ler 4 ("a construir"),
  pede-alterar 7 ("caminho em aberto"), pede-remover 5 ("a decidir"), outro-par 5 (colisão).
- Ordem dos passos por cenário está em `cenarios/resumo-cenarios.txt` (lista de elementos acesos por passo), para o
  Tech lead conferir contra a descrição v3.2. Não conferi o conteúdo contra a descrição: é dele.

## Foco

- Ordem do Tab: 7 botões de cenário, depois 9 bairros e 3 pessoas (19 paradas), todos com nome ("Abrir a ficha: …").
- Os 7 botões mudam ao focar (contorno). Os 12 bairros e pessoas **não mudaram por script**.
- O CSS tem `.bairro:focus-visible>.zona` e `.pessoa:focus-visible .anel` (regra no filho). A medição marcou
  `regra_de_foco_no_css: false`, o mesmo defeito da ferramenta visto nas voltas 2 e 3 dos conceitos (a regra com
  `>` ou posta no filho não é reconhecida). Leitura: **não verificado**, não falha. Tab real do UX revisor decide.

## Observações

- No 320 a faixa do desenho tem rolagem própria (`.palco` com `overflow-x:auto`) e abre centrada no Banco local; a
  página em si não rola de lado (documento 305 px). Quem cortar a leitura da cidade em 320 deve saber que parte do
  desenho fica fora da tela até rolar a faixa.
- Folga e razão estão perto do limite (R2 em 25 exatos; R3 razão em 1,53 contra 1,5). Qualquer rótulo ou item a
  mais pode derrubar.

## Não verificado

- Foco visível dos bairros e pessoas com Tab real (acima).
- Olho apertado de R2 (reduzir e borrar); leitura dos cenários "sem ler texto"; conteúdo dos passos contra a
  descrição v3.2; abrir ficha e Esc na ficha.
- Contraste dos elementos no estado aceso/apagado (mede-se o estado de repouso; o apagado pode reduzir opacidade).
- Links montados por JavaScript; break-ui (dados extremos) não pedido.

## Arquivos

- `medidas-320|768|1280|1920.json`, `captura-<largura>.png`, `links.json`, `resumo.txt`.
- `cenarios/cenarios-1280.json`, `cenarios/cenarios-320.json`, `cenarios/resumo-cenarios.txt`, e o script usado
  (`cenarios/harness.html`, `rodar-cenarios.ps1`).
