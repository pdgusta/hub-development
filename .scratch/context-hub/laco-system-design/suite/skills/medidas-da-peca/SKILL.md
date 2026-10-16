---
name: medidas-da-peca
description: "Measure a built HTML/SVG piece with scripts instead of judging by eye: count crossings between lines, minimum distance between items, rendered text contrast, load size and time, broken links, keyboard focus order and missing names, at several screen widths. Use when testing a page or the city diagram, when a review needs numbers, or when an accessibility check asks to measure contrast. Report only; never edit the piece."
---

# Medidas da peça

Mede uma peça HTML/SVG por script, em várias larguras, e devolve números. Só relata: nunca altera a peça.
O julgamento (passa ou falha na régua, nota, consertos) é da `regua-da-cidade`.

## Como rodar

No PowerShell, da pasta do papel (a saída vai para `qa/`):

```powershell
& .claude\skills\medidas-da-peca\rodar.ps1 -Raiz <pasta que contém a peça> -Peca <caminho da peça dentro da raiz> -Saida .\qa
```

- Larguras padrão: 320, 768, 1280 e 1920 px (`-Larguras 320,1280` para escolher). Zoom: 200% em 1280 equivale a
  640 px de largura; 400% equivale a 320 px.
- Saída em `-Saida`: `medidas-<largura>.json`, `captura-<largura>.png` (a primeira tela, 1000 px de altura),
  `links.json` e `resumo.txt`.
- Requer Edge, Python 3 (só para o servidor local) e Node 18 ou mais (para `links.mjs`).

## O que cada medição devolve (`medidas-<largura>.json`)

| Chave | O que mede | Regra da régua |
|---|---|---|
| `cruzamentos` | pares de ligações que se cruzam, fora das pontas e de pontos de encontro; em curva, "suspeita" | R1 |
| `distancias` | menor folga entre itens, altura de rótulo, pares abaixo de 1 rótulo, razão entre grupos e dentro do grupo | R3 |
| `rotulos` | rótulos por desenho SVG, rótulos na primeira tela, lista única de textos, possíveis códigos soltos | R2, R4 |
| `contraste` | razão de contraste de cada texto renderizado contra o fundo efetivo; falhas e não verificados | acessibilidade |
| `teclado` | focáveis na ordem do Tab, sem nome acessível, `tabindex` positivo, sem mudança visível ao focar; `nao_verificado_focus_visible` conta os que têm regra `:focus-visible` no CSS e não mudaram com o foco por script (relate "não verificado", nunca "falha") | acessibilidade |
| `peso_e_tempo` | bytes por tipo, origens externas, tempo até o DOM e até a carga | desempenho |
| `pagina` | largura do documento e se há rolagem horizontal | larguras |

## Como ler

- **Modo marcado x adivinhado.** Se a peça tem `data-item`, `data-grupo`, `data-ligacao` e `data-encontro` (ver
  `regua-da-cidade/regras.md`), a medição usa só o marcado. Sem marcação, adivinha pela forma (traços abertos são
  ligações; caixas e círculos que não contêm outra forma são itens) e o campo `modo` diz isso. Número adivinhado
  pede conferência na captura.
- **Suspeita** de cruzamento: envolve curva, amostrada a cada 3 px; confirmar por olho na captura.
- **Contraste** usa a mesma conta de `contraste/check_contrast.py`. Para conferir um par: `python -I
  contraste/check_contrast.py <texto_hex> <fundo_hex>`. Fundo com imagem ou gradiente fica "não verificado".
- **Tempo** sai do Edge sem cabeça com tempo virtual: serve para comparar versões, não como tempo real.
- **Links** montados por JavaScript não aparecem em `links.json`.

## Regras

- Só relatar; nunca editar a peça. Para dados extremos (nomes longos, zero itens), use `break-ui` numa cópia.
- Saída só em `qa/`. Nada de rede além de `127.0.0.1`. Nada de mouse nem teclado.
- O script abre e fecha o próprio Edge (perfil temporário) e o próprio servidor; nunca mata processo pelo nome.

Origem e detalhes: `LEIA-ME.md`.
