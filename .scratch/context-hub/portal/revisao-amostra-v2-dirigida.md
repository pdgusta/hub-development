# Revisão dirigida da amostra — Prumo, 2026-10-14

**Direção mantida; ainda duas pendências importantes para aprovar esta versão da amostra.** O mapa ficou mais legível: rótulos HTML de 15 px reais nos dois tamanhos, critérios fora do SVG, relações com ponta de seta, trilha decorativa removida e texto do ticket 09 corrigido. O clima e o corpo continuam adequados como direção para o Gustavo julgar.

## Pendências

1. **Importante — hover volta ao contraste baixo no menu.** `v2/amostra-inicio.html`, regra `.barra a:hover`. O ativo escuro passou: aproximadamente 7,63:1 contra a madeira no topo. Porém a regra posterior de hover ainda aplica `rgba(255,240,215,.14)`; conferi esse valor no estilo computado ao passar o mouse. O contraste do texto claro sobre essa composição cai a aproximadamente **3,86:1** no topo. Recomendo escurecer também o hover, preservando a distinção de ativo e foco. Não basta corrigir o estado sem mouse. Referência do requisito textual: [W3C, contraste mínimo](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

2. **Importante — badges de espera parecem pertencer a outro ticket.** Regras `.acamp .espera` / `.espera-esq` e posições dos tickets 16/17. Na captura própria em 1600, “espera 4” do 16 aparece logo abaixo do título “Verificação nas duas máquinas” do 17; “espera 1” do 17 fica próximo de “Como os agentes gravam” do 11. Com rótulos maiores, deslocar os badges para fora do botão deixou a associação visual ambígua. Recomendo prender o badge à tenda/ao rótulo do próprio ticket e reservar espaço ao conjunto, sem lançá-lo para o grupo vizinho. Evidência: `inicio-1600.png` desta revisão.

**Sugestão de correção pequena:** uma declaração antiga posterior `.acamp .n {font-size:13.5px}` ainda sobrescreve os 14 px novos. Medi 13,5 px em ambos os tamanhos. Remover a regra residual ou fixar 14 px; o rodapé da amostra ainda promete nenhum texto abaixo de 14 px. Os títulos dos tickets e os critérios já estão corretos em 15 px reais.

## O que passou

- Chip aberto `#4a453d/#e6dfd2`: **7,17:1**; pedra nova sobre fundo de chip: **5,65:1**; dependências `#6f5a3e/#efe3cc`: **5,15:1**. Os pares corrigidos passam; não é auditoria exaustiva de todos os estados.
- Os sete paths de dependência têm `marker-end`, com realce em terracota, e não há path da trilha decorativa no DOM. O grafo agora informa o sentido.
- Ticket 09 sem absorção inventada do 50; quarta-feira e “Nenhuma pergunta espera você” corrigidos.
- Foco no 16 mostrou dica; Enter realçou cinco relações; seta levou ao 17; Soltar devolveu foco ao 16. Repetido nos dois tamanhos, sem erros JS.
- Redução de movimento deixou o pseudo-elemento do anel com `animation-name:none`.
- Capturas próprias de início nos dois tamanhos e da interação foram abertas e conferidas. Em 1280, a coluna única deixa o mapa maior e a leitura dos rótulos melhora.

Evidências: `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-amostra-v2-dirigida/` (`resultados.json` e PNGs). Script `review_amostra_v2_dirigida.py` no diretório pai. Abrir arquivo local no Edge; nenhuma alteração do portal. Marco 7 fora do escopo.
