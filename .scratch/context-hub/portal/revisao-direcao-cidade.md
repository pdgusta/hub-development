# Direção da amostra System design cidade — Prumo, 2026-10-14

**Recomendo a direção cidade 2.5D, com os ajustes abaixo antes de fechar o brief.** É revisão de proposta: não aprova a futura amostra nem autoriza substituir o System design. Li o brief, a recusa original do Gustavo e o modelo de salas/cards/arestas da planta, além do destino do mapa. Não rodei testes nem conferência de entrega nesta rodada.

## Conteúdo nas camadas

**Sim: texto no mapa OU na ficha respeita “mesmo conteúdo”.** O pedido novo pede pouco texto e permite mudar a hierarquia; os subtítulos não precisam continuar na superfície. Mas contar 124 strings não basta: cada texto deve estar associado ao mesmo componente/regra/ligação, e a ficha precisa ser alcançável por clique e teclado. Texto escondido no HTML, sem caminho de leitura, não conta.

Acrescentar à paridade textual uma paridade semântica: lista de componentes com papel/estado, e lista das ligações com origem, destino, sentido e situação. Conferir todas as fichas, incluindo placas, não só a primeira. Uma frase correta na ficha errada ou uma rua com seta invertida passa na contagem e falseia a arquitetura.

## Onde a metáfora precisa de limites

1. **Ilhas = máquinas, não dois servidores centrais.** A ilha menor é resumo de outra máquina com o mesmo papel de par, não subordinada ao notebook. Replicação entre bancos em dois sentidos; GitHub continua cópia por diário/commit + push, sem virar fonte de verdade ou elo obrigatório do sync.
2. **Túnel = junction local.** Manter “junction · todo harness” legível na ficha, com origem maestro-* e destino Agentes. Não usar logo/traçado que sugira VPN ou passagem entre máquinas; tailnet é outro tipo de ligação. A posição do Acervo ao norte não deve sugerir que ele existe apenas no notebook: conservar a informação de réplica nas duas máquinas e registro de uso por máquina.
3. **Muralha não inventa proibição.** Retirar a expressão “o único jeito de entrar”. Ela sugere uma garantia que o desenho não tem: as rotas “agente no disco?” e “Desktop grava?” estão em aberto no modelo. Manter essas rotas distintas e marcadas como abertas; não concluir a decisão pela metáfora. Quem usa são atores externos, mesmo desenhados perto da cidade.
4. **Fronteira de gravação não é portão único de toda edição.** O caminho fork → guarda de versão → CouchDB deve continuar claro; Obsidian ↔ vista ↔ sincronizador ↔ banco é outro caminho. Não fazer o muro indicar que todo acesso ao Markdown passa pelo MCP/guarda.
5. **Placas da ponte são regras do sistema, não condições de travessia.** Máquina desligada não é erro/divergência; colisão de texto segura só a nota, binário mais novo vence; limites/exclusões do banco permanecem disponíveis na ficha. Pode usar a ponte como lugar das placas, explicando seu alcance, sem representar o sync como bloqueado até haver intervenção humana.

## Critérios a acrescentar ao brief

- **Forma de fato nova:** bairros/volumes/espaços devem organizar a leitura como cidade, sem repetir a grade/ordem espacial da planta com prédios por cima. No enquadramento inicial deve ser possível localizar as duas máquinas, a verdade, entradas, acervo e a cópia externa.
- **Topologia verdadeira:** prova das ligações e estados acima; ruas decorativas não podem parecer fluxo de dados. Não depender só de cores para distinguir papéis, aberto, proteção e rede; preservar nome e sentido.
- **Leitura em camadas operável:** todos os prédios/placas com ficha têm nome acessível e Enter/Espaço; Esc fecha e devolve foco; elementos decorativos não entram no Tab. Textos completos cabem na ficha nos dois tamanhos, sem depender de hover ou ficar inacessíveis atrás do mapa. Enquadrar/zoom também por teclado.
- **Legibilidade:** recomendo manter piso de 14 px efetivos para rótulos no enquadramento, em lugar dos 13 px propostos. Não comprimir texto para fingir que cabe; usar nomes curtos na superfície e ficha para o resto. Contraste dos nomes sobre chão/telhado e das ruas deve ser medido com as fontes realmente carregadas; etiquetas de leitura sem inclinação isométrica que prejudique as letras.
- **Canvas estático primeiro:** retirar pontinhos/reflexos contínuos da primeira amostra. O pedido é majoritariamente estático; interação nos prédios já dá vida suficiente. Se houver movimento depois, reduced-motion o desliga, e nenhuma informação depende dele.
- **Provas:** manter rede bloqueada, fontes/logos embutidos, file e iframe opaco, nos dois tamanhos. Além das capturas previstas, testar foco/ficha após pan/zoom e reenquadramento, todas as placas e o enquadramento parado. Não exigir que 124 textos estejam visíveis ao mesmo tempo.

Recomendação de sequência: ajustar o brief e repassar os limites ao subagente que já constrói; mostrar somente a amostra ao Gustavo após revisão. O arquivo vigente permanece intacto até o aval dele. Sem pedido de novo acabamento do portal.
