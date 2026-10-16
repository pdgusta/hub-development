# Amostra System design cidade 2.5D — Prumo, 2026-10-14

**APROVADA para apresentar ao Gustavo.** Sem bloqueantes ou importantes pendentes nesta amostra. O System design vigente só deve ser substituído depois do aval dele; este parecer não decide a preferência estética do Gustavo.

## Forma e fatos

Agora a forma mudou: volumes isométricos, bairros, ruas, canal e ilha do segundo par reorganizam a arquitetura em uma cidade; não é a grade da planta anterior revestida com outro estilo. Nomes/logos sustentam a superfície, com subtítulos e regras nas fichas. Capturas fornecidas e próprias abertas em 1280×800 e 1600×900.

Conferi os limites da metáfora: segundo par não é subordinado ao notebook, ponte mostra os dois sentidos, GitHub continua cópia/diário, Acervo conserva a réplica nas duas máquinas, junction fica distinta da tailnet. Não há muralha de acesso exclusivo; Desktop/agente no disco continuam rotas abertas até a Vista. A fronteira destaca fork → guarda → banco, sem abranger o caminho inteiro do Obsidian/sincronizador. Regras são um quadro clicável, não um pedágio da ponte. Estado estático atende ao brief.

## Conteúdo e camadas

O relatório fornecido conserva os 124 textos e abre as 28 fichas, além da comparação estrutural. Minha prova independente comparou **28 componentes** com nomes, papéis, bairros, subtítulos, selos e fronteira, e **30 arestas** com origem, destino, palavra, tipo e indicadores de sentido, contra o modelo da planta. Traçados novos não foram exigidos iguais aos antigos. Os 30 ids têm rua correspondente.

Nas quatro combinações de modo/tamanho, abri as 28 fichas pelo teclado e confirmei título, todos os subtítulos e selo do componente; Esc fechou e devolveu o foco ao componente certo. Informação movida para ficha permanece alcançável. **“até 200 MiB” e “commit + push” estão no mapa final; “pode fechar” e “+ Copilot” ficam só nas fichas** e foram conferidos lá. Essa redução da superfície está dentro da regra de camadas aprovada no brief.

## Provas de uso e funcionamento local

- Execução própria em **file e iframe sandbox allow-scripts**, 1280×800 e 1600×900: sem rolagem do documento, direito arrasta, Ctrl+roda amplia, Shift+roda desloca horizontalmente, Enter/Espaço abre ficha e Esc devolve foco.
- Menor fonte efetiva do mapa no enquadramento: **14,40 px em 1280**, **16,67 px em 1600**. Outfit embarcada carregada; **zero pedidos externos e zero erros JS** no roteiro.
- Conferi também código e relatório fornecido de cliques nos 28 alvos depois de pan/zoom, chão sem abrir ficha, Tab, enquadrar e acesso aos focados. A prova própria de todas as fichas foi por foco/Enter; não a confundi com a medição de cliques do Designer.
- Cadastro conferido: planta histórica com decisão de recusa, cidade explicitamente amostra, sem substitui/mestra/ticket. Sem autorização antecipada de troca do arquivo vigente.

Provas próprias: `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-cidade/` (`resultados.json`, capturas); script `review_cidade.py` na pasta deste papel. Servidor e navegadores próprios encerrados. Nenhuma escrita na caixa real, nenhuma alteração de implementação, nenhuma repetição de suítes do núcleo para esta amostra autônoma.
