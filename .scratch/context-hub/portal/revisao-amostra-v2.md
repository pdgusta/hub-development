# Revisão da amostra Mesa de mapas — Prumo, 2026-10-14

**Recomendo manter o clima e as três fontes para a direção, mas corrigir esta amostra antes de levá-la ao Gustavo.** O corpo e os títulos ficaram mais confortáveis nas capturas próprias; o mapa central ainda reproduz o problema de letras miúdas que motivou a mudança. Não é aprovação das cinco telas nem aceite estético em nome do Gustavo.

Arquivo revisado: `v2/amostra-inicio.html`. Conferi no Edge headless, abrindo o arquivo local diretamente, com capturas próprias em 1600×900 e 1280×800. Fonte do pedido: `pedido.md`, retorno literal sobre legibilidade, aconchego, vida e interação.

## Importante: corrigir antes de apresentar

1. **Tamanho real do texto do mapa está abaixo do piso.** `amostra-inicio.html:80,92–94,156`: SVG de 900 unidades com `width:100%` encolhe também as letras. Medi `fontSize × getScreenCTM().a`: rótulos de ticket com 15 unidades viram **13,19 px em 1600** e **10,07 px em 1280**; números de 13,5 unidades viram **11,87 e 9,06 px**. Critérios no rodapé do mapa também encolhem. A declaração “nenhum texto abaixo de 14 px” é falsa na apresentação. Recomendação: dar mais área ao mapa/reorganizar as colunas e usar rótulos com tamanho efetivo estável, legíveis na vista inicial. Não depender do futuro zoom para conseguir ler. Há também pouco espaço entre título de Verificação, cume e nós vizinhos; ajustar o arranjo junto do tamanho, sem sobrepor rótulos.

2. **Contraste ainda falha em pares usados.** Chip aberto: `#6b655c` sobre `#e6dfd2` = **4,35:1**; texto de 14 px. Menu ativo clareia a madeira por uma camada branca, reduzindo o contraste do texto claro a aproximadamente **3,3:1** perto do topo, em vez dos 5,10:1 do fundo sem a camada. Dependências `#a99474` sobre mapa `#efe3cc` dão **2,30:1** antes mesmo da opacidade de 0,9, que reduz mais. Recomendação: medir e corrigir estados efetivos (incluindo ativo/hover), não só a paleta base. Texto normal precisa 4,5:1; elementos gráficos necessários à compreensão precisam 3:1 contra a cor adjacente, conforme [W3C: contraste de texto](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) e [W3C: contraste não textual](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html). Terracota, musgo, petróleo e tijolo sobre seus respectivos fundos de chip passaram nos pares medidos (5,26; 4,99; 5,63; 5,57:1). Não fiz auditoria exaustiva de todos os pixels/estados.

3. **Próximo passo e dica do ticket 09 não correspondem aos arquivos.** `amostra-inicio.html:173,218`: “10 tickets, 9 já resolvidos; falta Pesquisa ampla (50) ser absorvida” e “à espera de absorver a pesquisa ampla”. O 50 está `resolved`; o 09 é `claimed` e seus comentários já registram teste de bancada e rodada de continuação autorizada pelo Gustavo. Não inferir absorção pendente a partir de `Blocked by`. Recomendação: corrigir o retrato estático com base nos arquivos e indicar a data/hora do retrato; se o próximo passo não tiver fonte confirmada, dizer “em andamento”, sem inventar o que o agente espera. Na implementação, separar dependência resolvida de eventual ação textual de absorção.

4. **O mapa não mostra a direção das relações, e a trilha contínua sugere outro encadeamento.** `amostra-inicio.html:159–168`: os sete pares de dependência estão declarados, mas os paths não têm ponta de seta. No realce do 16, entram juntos quatro bloqueadores e a relação de saída para o 17, sem distinguir o sentido. A linha marrom contínua é o elemento visual dominante, mas não corresponde ao grafo dos tickets (passa por/entre acampamentos sem que aquilo seja uma dependência). Recomendação: tornar a direção das relações explícita e fazer a leitura dominante seguir o grafo real; retirar ou reduzir a trilha decorativa para que não pareça sequência de execução. O cume pode continuar como destino, sem inventar relações com tickets independentes.

## Sugestões de acabamento

- `amostra-inicio.html:141`: 14/10/2026 é **quarta-feira**, não terça. Corrigir; “Bom dia” também pode ser substituído por uma saudação sem horário na amostra congelada.
- Trocar “Nada espera você” por “Nenhuma pergunta espera você” evita confundir ausência de rodada aberta com resposta ainda aguardando aviso. O estado “salva/aviso pendente” está bem separado visualmente e deve continuar assim.
- Os botões sem ação são aceitáveis para esta amostra declarada. Não usar essa aprovação como prova de zoom, navegação de telas ou abertura real do ticket. A interação implementada é selecionar e explorar dependências; o botão “Abrir o ticket” ainda não abre.
- Na integração, manter o texto longo de decisões em camadas expansíveis, sem transformar o início em uma página extensa; a amostra foi útil para julgar a leitura desse texto.

## O que passou

- Clima claro, tinta escura, corpo Nunito Sans e títulos Fraunces formam uma direção coerente com o pedido de aconchego. Textos fora do SVG estão maiores e mais confortáveis do que na Torre anterior. O Gustavo ainda precisa opinar sobre a preferência estética.
- Nunito Sans, Fraunces e JetBrains Mono carregadas localmente; nenhum pedido HTTP externo no roteiro e nenhum erro JS.
- Selecionar o 16 por Enter abriu placa com os quatro bloqueadores; foram realçadas cinco relações incidentes (quatro de entrada e uma de saída). Seta levou ao 17; Soltar fechou a placa e devolveu foco ao 16. Tooltip por hover e foco existe; não considero comprovada a equivalência em todas as misturas mouse/teclado — a segunda passagem do roteiro registrou dica escondida com o alvo já focado.
- `prefers-reduced-motion: reduce` deixou as duas animações da amostra com `animation-name:none`.
- Bandeja diferencia nenhuma rodada esperando de resposta salva/aviso pendente; critérios não aparecem concluídos por contagem de tickets.

Evidências: `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-amostra-v2/`, com `resultados.json` e PNGs próprios; script `review_amostra_v2.py` no diretório pai. Capturas de início e mapa com seleção foram abertas e conferidas nos dois tamanhos. Sem alteração da amostra ou do portal; marco 7 não revisado nesta rodada.
