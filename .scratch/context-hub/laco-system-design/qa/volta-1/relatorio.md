# Relatório do QA, volta 1 (fase 3, porta)

Medido em 2026-10-15 com `medidas-da-peca`, larguras 320, 768, 1280 e 1920. Só medi e relato; não editei nada.
Saída por conceito em `conceito-a\`, `conceito-b\` e `conceito-c\` (JSON, capturas, `links.json`, `resumo.txt`).

**Modo da medição:** marcado nos três (a peça tem `data-item`, `data-grupo`, `data-ligacao` e `data-encontro`:
15 itens, 8 grupos, 1 ponto de encontro cada; 11 ligações em A e C, 10 em B). Nada foi adivinhado.

## Resumo (1280 px, visão geral)

| Medida (limiar) | A: mapa de linhas | B: planta com muralha | C: corte da cidade |
|---|---|---|---|
| R1 cruzamentos fora de encontro (0) | 0, **passa** | 0, **passa** | 0, **passa** |
| R2 rótulos no desenho (máx. 25) | 23, **passa** | 23, **passa** | 23, **passa** |
| R3 folga mínima (>= 1 rótulo = 21 px) | 23,5 px, **passa** | 29,1 px, **passa** | 34,1 px, **passa** |
| R3 pares abaixo de 1 rótulo | 0, **passa** | 0, **passa** | 0, **passa** |
| R3 razão entre grupos / dentro (>= 1,5) | 1,81, **passa** | 1,80, **passa** | 1,85, **passa** |
| Contraste (4,5 texto; 3 grande) | 34 de 34, **passa** | 34 de 34, **passa** | 34 de 34, **passa** |
| Foco: itens sem nome acessível | 0, **passa** | 0, **passa** | 0, **passa** |
| Foco: tabindex positivo | 0, **passa** | 0, **passa** | 0, **passa** |
| Foco: muda visivelmente ao focar | 0 de 10, **falha** | 0 de 10, **falha** | 0 de 10, **falha** |
| Links quebrados | 0 (nenhum link no HTML) | 0 (nenhum) | 0 (nenhum) |
| Rolagem horizontal (320 a 1920) | não, **passa** | não, **passa** | não, **passa** |
| Peso (doc., sem recursos externos) | 24,4 KB | 25,9 KB | 25,1 KB |
| Tempo até a carga (virtual) | 73 ms | 62 ms | 36 ms |
| Códigos internos soltos | 0 | 0 | 0 |

## Por largura (folga mínima px / altura do rótulo px / razão entre grupos)

| Largura | A | B | C |
|---|---|---|---|
| 320 | 16,9 / 15 / 1,78 | 21,0 / 15 / 1,81 | 24,8 / 15 / 1,85 |
| 768 | 13,8 / 12 / 1,80 | 17,6 / 12 / 1,82 | 20,2 / 12 / 1,85 |
| 1280 | 23,5 / 21 / 1,81 | 29,1 / 21 / 1,80 | 34,1 / 21 / 1,85 |
| 1920 | 23,5 / 21 / 1,81 | 29,1 / 21 / 1,80 | 34,1 / 21 / 1,85 |

Em todas as larguras a folga ficou acima da altura do rótulo, 0 cruzamentos, 0 pares abaixo do limiar, 0
falhas de contraste. A razão ficou entre 1,78 e 1,85 (limiar 1,5).

## Folga mínima (a mais apertada de cada conceito, 1280 px)

- A: Rede privada e Par B, 23,5 px (só 2,5 px acima do limiar). Depois Nota de retomada e Acervo do maestro, 33,2 px.
- B: Sincronizador e Banco local, 29,1 px.
- C: Rede privada e Par B, 34,1 px.

A é o que tem menos margem sobre o limiar; passa, mas por pouco.

## Falha encontrada (os três)

**Foco sem mudança visível.** Os 10 itens focáveis de cada conceito (grupos `g` com `tabindex=0` e nome "Abrir a
ficha: …") recebem foco pelo teclado, mas a medição não viu mudança de contorno, sombra, fundo, borda, cor ou
traço ao focar. Contra o limiar de acessibilidade (foco visível) é **falha** nos três.
Ressalva: o foco foi dado por script; se a peça usa `:focus-visible` com regra que só vale por Tab real, a medição
pode não enxergar. Confirmar com Tab real na captura é trabalho do UX revisor.

## Observações

- Rótulos: 23 no desenho SVG; 34 textos na primeira tela contando 11 do HTML (título, texto de apoio, legenda).
  A contagem de R2 é por desenho (23). Se o revisor contar o texto de fora do desenho, 34 passa de 25.
- Rótulos únicos: o mesmo conjunto de nomes do hub nos três (Banco local, Sincronizador, Vigia do sync, Camada de
  busca, Porta do banco, etc.), mais "a decidir" marcado. Diferenças: A e C têm "Nota de retomada" e "Checkpoint";
  B tem "Raiz" e "Contrato". Conferir contra o texto do hub (R4) é do Tech lead.
- Legendas das linhas (buscar, gravar, disco e banco, troca entre pares, vigiar, editar (Gustavo), disciplina e
  acervo) aparecem nos três.
- B tem 10 ligações contra 11 de A e C; não confere com falha, só diferença.

## Não verificado

- **Olho apertado de R2** (reduzir a captura e borrar): não rodei; é julgamento visual do UX revisor sobre
  `captura-1280.png`.
- **Links:** não há `<a>` no HTML; links montados por JavaScript não entram em `links.json`.
- **Peso por tipo e origens externas:** 0 recursos externos; só o documento. Tempo é virtual, serve para comparar.
- **Teclado:** só a ordem do Tab por script e o nome acessível. Não testei abrir e fechar a ficha, nem Esc.
- **break-ui** (dados extremos): não rodei nesta etapa; a tarefa pediu só as medidas.
- **Mouse e passar o cursor:** não testado (regra: nada de mouse).

## Arquivos

- `conceito-a\`, `conceito-b\`, `conceito-c\`: `medidas-320|768|1280|1920.json`, `captura-<largura>.png`,
  `links.json`, `resumo.txt`.
