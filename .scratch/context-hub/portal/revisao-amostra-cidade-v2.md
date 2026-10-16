# System design cidade v2 — Prumo, 2026-10-14

**APROVADA para apresentar ao Gustavo.** Sem bloqueantes ou importantes pendentes nesta amostra. A troca do System design vigente depende do aval dele.

## Pedido e forma

Conferidos o pedido de 20h33 e o brief v2: CouchDB central, peças distribuídas em anéis, vista mais de cima, rótulos associados aos prédios e analogia explicada em cada ficha. Capturas próprias abertas em 1280×800 e 1600×900. Os cinturões são chão, distintos das ruas. Os encostos declarados de “contratos-opção” e “abre” não impedem uso e não reabrem acabamento.

O relatório radial fornecido e seu algoritmo foram conferidos: zero cruzamentos em 1.065 pares de segmentos, túnel sem cruzar ruas, níveis sem inversão, centro sem desvio e 25 etiquetas próximas do próprio dono. O encontro das rotas abertas Desktop/agente é entroncamento. Esses números são da prova do Designer, não uma contagem independente minha.

## Informação e correções resolvidas

As analogias preservam os papéis, com duas correções feitas durante esta revisão:

- **Importante, resolvido — Guarda de versão:** “barra conflito” sugeria recusar a escrita atrasada. O R1 escolhido no ticket 30 e na pesquisa 26 grava como filha da revisão de base e preserva o ramo de conflito. A ficha agora diz “preserva a revisão de base (base_rev) e separa versões em conflito, sem sobrescrever”.
- **Importante, resolvido — MCP só leitura:** “quem vem de fora só consulta” generalizava a restrição e contradizia a rota aberta Desktop grava?. Agora diz “esta porta oferece só consulta”.

Segundo par continua par, GitHub é cópia, túnel local não é tailnet, regras não são pedágio e fronteira de gravação não envolve todos os acessos. Nenhuma outra distorção factual encontrada nas 28 analogias.

## Verificação própria

Nos quatro cenários (file/iframe sandbox allow-scripts × 1280×800/1600×900), comparei os **28 componentes e 30 ligações** com o modelo anterior: nomes, papéis, bairros, subtítulos, selos, origem/destino, palavras e sentidos preservados. Todas as ligações têm rua. O relatório fornecido registra também 124/124 textos.

Abri as 28 fichas em cada cenário por foco/Enter, conferindo título, subtítulos e selo; Esc fecha e devolve foco ao componente correto. Espaço abre, botão direito arrasta, Ctrl+roda amplia e Shift+roda desloca horizontalmente. Sem rolagem do documento, erros JS ou pedidos externos. Fonte Outfit embarcada carregada; mínimo efetivo no mapa **14,07 px em 1280** e **17,40 px em 1600**.

Provas próprias: `revisao-cidade-v2/` e `review_cidade_v2.py` na pasta deste papel. Conferidas também as provas fornecidas de clique após pan/zoom, Tab e enquadrar. Servidor e Edge próprios encerrados; nenhuma escrita na caixa real, alteração de implementação ou repetição de suítes do núcleo.
