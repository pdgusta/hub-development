# Relatório do QA, porta da mistura, volta 2

Medido em 2026-10-15: `conceitos/mistura/mistura.html` (volta 2, 81 KB), com `medidas-da-peca` nas larguras 320, 768,
1280 e 1920 e o teste dos sete cenários (`cenarios/`). Só medi e relato; não editei a peça. Entre parênteses, a
volta 1.

**Modo:** marcado. 19 itens (17), 9 grupos, 22 ligações (20), 2 pontos de encontro. Nada adivinhado.

## Números (visão geral)

| Medida (limiar) | 320 | 768 | 1280 | 1920 | Veredito |
|---|---|---|---|---|---|
| R1 cruzamentos fora de encontro (0) | 0 (0) | 0 | 0 (0) | 0 | **passa** |
| R2 rótulos no desenho (máx. 25) | 25 (25) | 25 | 25 (25) | 25 | **passa**, no limite exato |
| R3 folga mínima (>= 1 rótulo) | 18 px de 15 (18) | 14,5 de 12 (14,5) | 24,1 de 21 (24,1) | 24,3 de 21 | **passa** |
| R3 pares abaixo do limiar / sobrepostos | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | **passa** |
| R3 razão entre grupos / dentro (>= 1,5) | 1,67 (1,53) | 1,67 | 1,68 (1,53) | 1,66 | **passa**, com mais margem |
| Contraste | 60 de 60 (58) | 0 falhas | 49 de 49 (47) | 0 falhas | **passa** |
| Focáveis sem nome acessível | 0 | 0 | 0 de 19 (0 de 19) | 0 | **passa** |
| tabindex positivo | 0 | 0 | 0 | 0 | **passa** |
| Rolagem horizontal da página | não | não | não | não | **passa** |
| Códigos internos soltos | 0 | | 0 | | **passa** |
| Links quebrados | nenhum `<a>` no HTML (0) | | | | **passa** |

- Menores folgas (1280): Porta do banco e Camada de busca 24,1 px; Banco local e Vista Markdown 28,2 px; Vista
  Markdown e Sincronizador 29,1 px. Dentro do grupo a mediana caiu de 37 para 30,8 px e o mínimo entre grupos de
  56,5 para 51,9 px: foi isso que subiu a razão.
- Textos visíveis na primeira tela: 49 em 1280 (47). Peso 81,4 KB (73,2), nada externo. Carga virtual 71 ms (69).

## Cenários (`data-cenario`)

Teste por clique nos botões, "Próximo", seta esquerda, "Sair" e Esc, em 1280 e 320 (resultado idêntico). Todos os
43 elementos marcados (37) entram em algum passo.

| Cenário | Passos | Sair e Esc apagam tudo | Foco volta ao botão | Passo de falha ou em aberto |
|---|---|---|---|---|
| O Gustavo edita um arquivo | 6 | sim | sim | 6 |
| Um agente novo abre sessão | 6 | sim | sim | nenhum |
| Um maestro novo abre sessão | 6 | sim | sim | nenhum |
| O Gustavo pede: leia | 4 | sim | sim | 4 |
| O Gustavo pede: altere | 7 | sim | sim | 7 |
| O Gustavo pede: remova | 5 | sim | sim | 5 |
| O outro par altera um arquivo | 5 | sim | sim | 5 |

Mudou na peça (conferido pelo teste):
- O passo de falha ou em aberto ganhou marca própria (triângulo, classe `falha`) e o texto "falha ou em aberto" no
  contador, nos cinco cenários acima. Nenhuma marca numerada cai sobre texto do desenho (0 sobreposições em todos os
  passos).
- Clicar num botão de cenário agora **move o foco para "Próximo"**, e clicar de novo no mesmo botão **reinicia no
  passo 1** (antes ligava e desligava).
- Ligações de ida e volta aparecem com "↔" (vista Markdown e sincronizador, sincronizador e banco, banco e outro par).
- Passos que antes não acendiam nada novo agora acendem: gustavo-edita passo 5 e pede-ler passo 4. Os passos de
  maestro-novo 4, 5 e 6 agora têm ligação acesa (Maestro para Biblioteca do Maestri, para Acervo do maestro, para
  Gustavo). pede-remover passos 2 e 3 também ganharam ligação.

## Problemas novos

1. **Marca numerada some em gustavo-edita, passos 5 e 6.** O passo 5 mostra 4 marcas (devia ter 5) e o passo 6
   mostra 5 (devia ter 6): a marca do passo 5 não foi desenhada. Nos outros 6 cenários, marcas = número do passo.
   Parece ligado ao passo 5, que acende dois elementos sem rótulo (`rect`) e o "Outro par".
2. **Elementos marcados sem rótulo próprio.** Em gustavo-edita passo 5 (dois `rect`), pede-alterar passo 7 e
   pede-remover passo 3 (um `path` cada) o elemento aceso não tem `data-item`, `data-ligacao` nem `data-grupo`.
   Se for decoração de fundo, tudo bem; se for ligação, ficou fora da marcação e a medição de R1 não a vê.
3. Nenhuma outra anomalia: 0 cruzamentos, 0 sobreposição de marca com texto, 0 falhas de contraste.

## Foco

- 19 paradas na ordem do Tab: 7 botões de cenário, 9 bairros, 3 pessoas; todas com nome; 0 tabindex positivo.
- 7 botões mudam ao focar. Os 12 bairros e pessoas não mudaram por script; o CSS tem `.bairro:focus-visible>.zona`
  e `.pessoa:focus-visible .anel`. A ferramenta continua sem reconhecer regra posta no filho (`>`):
  `regra_de_foco_no_css: false`. Leitura: **não verificado**, não falha. O Tab real do UX revisor decide.

## Não verificado

- Foco visível dos 12 bairros e pessoas com Tab real.
- Olho apertado de R2; leitura dos cenários sem texto (UX revisor); conteúdo dos passos contra a descrição v3.2
  (Tech lead; a lista dos elementos acesos por passo está em `cenarios/resumo-cenarios.txt`).
- Contraste no estado aceso e apagado (mede-se o repouso); posição da marca em 320 depois da rolagem da faixa
  (a faixa do desenho rola sozinha; só medi a sobreposição com texto, que deu 0).
- Links montados por JavaScript; break-ui (dados extremos) não pedido.
- Não conferi `consertos.md` item a item: é dos juízes.

## Arquivos

`medidas-320|768|1280|1920.json`, `captura-<largura>.png`, `links.json`, `resumo.txt`;
`cenarios/cenarios-1280.json`, `cenarios/cenarios-320.json`, `cenarios/resumo-cenarios.txt`; script em
`cenarios/harness.html` e `rodar-cenarios.ps1`.
