# Direção da proposta Laços — Prumo, 2026-10-14

**Recomendo a direção, com contrato de pedido explícito e sem comandos diretos.** É só parecer sobre a proposta de conteúdo/funcionalidades/forma; não autoriza construir a tela, a API ou executar laços. Li o pedido do Gustavo, os LEIA/configs do laço e de embeddings, `parar_apos.py` e o ticket 54. Não executei testes nem processos dos laços.

## Vira pedido

Recomendo um pedido imutável com UUID, identidade do laço **e da execução**, operação, nó/parâmetro estável, valor antigo/novo tipados e revisão da configuração/controle que foi lida. Usar a revisão da configuração relevante, não o hash do estado inteiro: contadores mudam continuamente e não devem criar conflito em toda edição. O registro do maestro declara parâmetros permitidos, tipos/limites e quando cada um pode ter efeito.

O portal grava o pedido na caixa e conserva o rascunho separado do estado real. Reenvio após falha usa o mesmo UUID/corpo. Maestro relê configuração e situação da execução **antes de aplicar**: revisão ou valor-base incompatível → conflito visível com comparação “você viu / agora está / você pediu”. Nada de sobrescrever ou recalcular silenciosamente. Dois pedidos sobre a mesma base não ganham ambos autorização automática depois que o primeiro mudou a configuração. Nova proposta após conflito é outro envio, ligado ao anterior.

“Lido” só prova leitura. **“Aplicado” exige recibo persistido do maestro**, com UUID, execução, antes/depois, revisão resultante, hora e momento de efeito. Alteração gravada para a próxima onda ou próxima partida continua explicitamente “aguarda efeito”, não aplicada ao processo corrente. Se o mecanismo não confirma o uso do valor novo, mostrar “configuração gravada; efeito não confirmado”. Recusa precisa de motivo. Conflito e dados indisponíveis também precisam aparecer em palavras, sem fingir sucesso. O pedido e seu desfecho ficam nos arquivos; a nota transitória do chat não é o recibo.

**Laço terminado/cancelado antes de aplicar:** pedido para aquela execução é encerrado sem aplicação, com motivo. Nunca alterar uma execução futura com o mesmo nome. “Criar nova execução com estes valores” é pedido separado, explícito. Para pausa/parada que já foi satisfeita, registrar “já estava pausado/terminado; nada alterado”, em vez de alegar que o pedido causou a mudança. A checagem vale na aplicação, não só no clique: o laço pode terminar enquanto o maestro está ocupado.

## Pausar e parar

**Sim, também devem virar pedido.** Botões “Pedir pausa” e “Pedir parada”, com o efeito e o ponto seguro em poucas palavras. A maquete não deve mostrar pausa instantânea quando só gravou um envio.

Definir por capacidade do laço: parar de despachar novos trabalhos, esperar os atuais; parar depois desta onda; encerrar preservando resultados. Não usar “matar tudo” como sinônimo. `parar_apos.py` já expressa parada após fechar uma onda; isso não comprova pausa/retomada genérica nem cancelamento instantâneo de chamadas em voo. Onde não existir capacidade correspondente, marcar “proposto” e não oferecer como controle ligado. Retomar, reiniciar e aumentar teto também são pedidos distintos, sempre vinculados à execução correta. Explicar que até a parada ter efeito pode haver consumo de cota por chamadas já em voo.

## Conteúdo e forma

- As três camadas devem ter rótulos e formas além da cor: **estado real**, **pedido**, **esboço**. Um valor editado aparece como proposta ao lado do vigente, sem pintar o nó real com o valor ainda não aplicado. Esboços nunca viram arestas do estado observado por acidente.
- O fluxo da pesquisa ampla é bom exemplo, mas **painel observa**, não é etapa causal que espera auditoria para funcionar. O LEIA diz que conferência/auditoria/síntese são conduzidas pelo maestro fora dos scripts: separar esse trecho como humano. Ondas são repetição com condição de parada, não apenas uma fila linear; teto/regra de parada são controles que condicionam o fluxo, não tarefas que executam uma vez.
- Registrar cada laço em arquivo é adequado, com identificadores estáveis e fontes locais declaradas pelo maestro. O navegador envia ids permitidos, não caminhos/comandos livres. Nenhuma criação de adaptador/comando de execução está autorizada por uma edição de nó.
- Estado real mostra fonte, última leitura e situação observada. Arquivo antigo não prova processo vivo; prever “sem atualização / estado desconhecido”. Distinguir esperando cota, esperando humano e pausado. Na carta-proposta, dados simulados têm marca visível; suíte do núcleo como **exemplo de laço possível**, sem alegar que roda ou que já tem adaptador. Embeddings usa estado observado/horário, não a suposição de que ainda não começou.
- Recomendo navegação Mesa de mapas, lista de laços e canvas com detalhe por seleção. Não transformar a carta numa especificação longa: demonstrar um parâmetro vigente → pedido pendente → desfecho e uma parada solicitada é suficiente para explicar a experiência. Indicar o que já existe no maré e o que é proposta nova. Preservar texto digitado em atualizações.

## Perguntas ao Gustavo

Não gastar as três perguntas com hashes, idempotência ou conflito: o time resolve isso. Recomendo perguntar apenas o alcance desejado para o primeiro passo, com opção recomendada **ver todos os laços + pedir parâmetros/pausa/parada**; desenho livre de nós/relações permanece esboço. Se for necessário outro julgamento, perguntar se prefere a lista abrir o laço com ação humana pendente ou manter o último escolhido. No máximo três perguntas, sem antecipar construção antes do aval da carta.
