# Lições — Sextante

## O que funcionou

- As cinco rodadas tiveram funções distintas. Propor, votar, conferir a aplicação, conferir o restante e fechar. Isso separou acordo verbal de texto realmente aplicado.
- A divisão dos tickets deu a cada revisor uma base própria. A leitura integral trouxe decisões que o mapa e o Answer resumiam demais.
- Os arquivos por pessoa e por rodada evitaram sobrescrita. Permitiram retomar sem depender do chat.
- Um relator único manteve uma proposta coerente. Os revisores puderam apontar erros sem disputar a edição.
- Os ids permitiram acompanhar ajustes e retificações. Uma divergência inicial pôde ser retirada com fonte, sem apagar o histórico.
- O diff entre antes/ e proposta/ revelou falhas de propagação. Uma decisão corrigida na parte ainda podia estar errada no resumo ou no teste.
- As marcas de origem foram essenciais. Ticket resolvido, escolha do núcleo, formato e ticket aberto não têm a mesma autoridade.

## O que atrapalhou

- Cinco rodadas com votação completa repetiram bastante conteúdo. Depois do primeiro acordo, o valor maior veio da conferência do texto aplicado.
- A divisão por quantidade de tickets não equilibrou o volume. Alguns tickets tinham históricos longos de pesquisa e muitas mudanças de rumo.
- Núcleo e partes repetiam requisitos e testes. Corrigir um lugar não corrigia os outros.
- Listas de “aplicado” davam uma sensação de fechamento antes da conferência. Ainda restavam testes antigos e marcas ausentes.
- “Concordo com ajuste” exigiu cuidado. Não basta contar como concordância; o texto do ajuste precisa ser incorporado e conferido.
- Avisos pelo Maestri podiam aguardar retorno. O arquivo gravado foi a referência confiável do progresso.
- O bloqueio inicial do terminal impediu até leitura. Foi necessário informar o erro exato. Repetir a revisão sem acesso não produziria evidência.

## Armadilhas encontradas

- O nível do cliente parecia indefinido no Answer. Os Comments já tinham aprovado sua função. Só o conteúdo concreto estava aberto. Minha primeira divergência confundiu essas duas coisas.
- Ticket resolvido de pesquisa não transforma toda recomendação em decisão de produto. Um resultado de bancada também não escolhe sozinho o desenho final.
- “Não verificado” pode qualificar a implementação de um requisito já decidido. Não significa que o requisito seja opcional.
- O núcleo da spec continha escolhas sem ticket. Alinhar a parte ao núcleo podia esconder essa origem.
- O ticket aberto tinha respostas aproveitáveis, mas não decisões fechadas pelo processo adotado. Era preciso preservar a origem e o adiamento.
- O corte de uma hora transformava requisitos em “se couber”. O prazo não revogava a validação no MCP nem a leitura do Config Doctor.
- O checkpoint excluía revisão pós-sessão e FreeLLMAPI. Isso não equivalia a uma decisão geral contra IA.
- Nota sem mudança não é necessariamente nota insuficiente. O teste mecânico não substitui o critério de retomada.
- Troca de trecho num script não herda a guarda da ferramenta do agente. Reler antes de gravar ainda deixa uma janela de concorrência a verificar.
- URL sem resposta não prova que a máquina está desligada. Confundir os estados pode esconder divergência.
- A guarda precisava considerar o arquivo-alvo e as junctions. A pasta da sessão, sozinha, não definia o alcance.
- A junction global não podia expor todas as skills. O teste antigo ainda cobrava isso depois de a regra ser corrigida.
- Um pequeno erro de texto invertia o teste de segredo: o segredo deve estar abrangido pela exclusão.

## Recomendações

- Começar a próxima revisão com uma tabela curta: requisito, fonte, estado da decisão e lugares da spec que o repetem.
- Ler os Comments antes de classificar uma divergência. Registrar a decisão posterior que substitui a anterior.
- Dividir a leitura por tema e volume, além da contagem de tickets. Compartilhar os pontos de fronteira cedo.
- Manter arquivos por rodada e relator único. Nas rodadas seguintes, votar nas pendências e ajustes, sem repetir tudo que já foi aceito.
- Reservar uma rodada só para o diff da aplicação. Conferir também testes, resumos e listas finais.
- Reduzir duplicação entre núcleo e partes. O resumo pode apontar para o requisito detalhado, em vez de reescrevê-lo.
- No plano de construção, separar requisito de ordem, responsável e ambiente de ensaio. Tratar os minutos e dublês antigos como histórico.
- Se houver etapas sequenciais, usar a entrega real anterior quando disponível. Manter dublês apenas com justificativa de teste.
- Preservar as lacunas técnicas no plano. Não chamar releitura de arquivo ou consulta de URL de garantia já demonstrada.
- Planejar provas das fronteiras: edição concorrente do sincronizador, banco cifrado, busca pelo proxy, guarda pela junction e isolamento das skills.
- Distinguir componente ensaiado de instalação real. Preparação anunciada não é ambiente já verificado.
- O acordo documental orienta a construção. Ele não substitui as provas de funcionamento, que não foram executadas nesta revisão.
