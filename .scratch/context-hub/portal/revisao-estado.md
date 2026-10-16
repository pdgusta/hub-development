# Estado da revisão — Prumo, 2026-10-14

- Papel: revisor; não editar o portal. Briefing em pedido.md; especificação em proposta.md; diário em construcao.md.
- **Marcos 0–6 aprovados.** Marcos 0, 3 e 4 mantêm as aprovações anteriores.
- Marcos 1–2 aprovados nesta revisão dirigida: .tmp confinada no arranque/escrita/limpeza, sentinelas externas preservadas; retratos e respostas malformados rejeitados inteiros, fora do índice e sem Markdown. 105 testes do núcleo + 4 do projeto real OK; 0 problemas no projeto real.
- Marcos 5–6 aprovados: correção conserva cinco respostas, outras quatro iguais ao mudar só o texto; UUID novo/substitui certo, correção persiste após recarga; leitor fecha por Esc/X com rota/foco e histórico corretos; glossário em pares; dica mestra acessível; oito códigos explicados; fontes das quatro cartas carregam sem rede externa e nenhuma requisição externa foi emitida.
- projeto.codigos aprovado: leitura/API/LEIA.md/contrato §3.7 e casos ausente/válido/inválidos conferidos.
- Parecer vigente: C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-dirigida1256/parecer.md.
- Evidências dados.json, telas.json e capturas próprias na mesma pasta. Scripts review_dirigida_dados2.py, review_dirigida56.py e capture_leitor_dirigida.py no diretório pai. Servidores próprios encerrados; cópias temporárias preservadas. Sem escrita de teste no projeto real.
- Pareceres anteriores recusados superados dentro do escopo dos marcos 1–2 e 5–6; servem de histórico.
- **Marcos 7–8 não revisados; aviso ao maestro não verificado.** Aprovação atual não é entrega final.
- Próximo: aguardar Designer com marco 7; ajudar maestro na conferência final quando solicitado.
- Aprovação enviada ao Designer pela skill Maestri; maestri check confirmou recebimento e resposta dele: vai registrar no diário e iniciar preparação do marco 7. Nenhum texto ficou preso no prompt.
- Após cada maestri ask, conferir check; texto preso → ask --raw "\r"; persistindo → ask "(enviar)".

## Retorno visual do Gustavo e direção em avaliação

- Gustavo recusou a tipografia atual por falta de legibilidade e pediu aconchego, vida e interação (literal em pedido.md). As aprovações técnicas anteriores não equivalem ao aceite visual dele.
- Designer propôs Mesa de mapas, papel claro, novas fontes e interações; pediu crítica antes de registrar e levar ao maestro, que mostrará ao Gustavo antes de aplicar.
- Recomendação do Prumo: Mesa de mapas como direção para amostra, marco 7 em paralelo, preservar contratos. Metáfora acompanha tarefas com nomes claros; mapa não inventa sequência/progresso; legibilidade avaliada com conteúdo real; interação funcional antes de ornamento; nada essencial exige virar cartão/envelope/arrastar.
- Parecer desta rodada: portal/revisao-direcao-visual.md. Não houve implementação, teste ou aprovação visual antecipada. Amostra deve provar clima/leitura; uma interação pequena é recomendada para avaliar o pedido interativo.
- Crítica enviada ao Designer pela skill Maestri. maestri check mostrou a mensagem no histórico e o prompt inferior vazio; não há texto preso para enviar. Designer ainda processando, sem resposta nesta conferência.

## Revisão da primeira amostra Mesa de mapas

- Amostra v2/amostra-inicio.html revisada no Edge em 1600×900 e 1280×800, com capturas e medições próprias; fontes locais carregadas, sem HTTP externo, interação pequena e reduced-motion conferidos.
- Clima e fontes recomendados como direção; **amostra ainda não aprovada para apresentar nesta versão**. Quatro importantes: SVG reduz letras a 9–10 px em 1280 (12–13 px em 1600); contraste do chip aberto/menu ativo/dependências falha; ticket09/Próximo passo inventam espera por absorção do 50 já resolved; dependências sem setas e trilha decorativa dominante sugerem encadeamento inexistente.
- Sugestões: quarta-feira em vez de terça; “Nenhuma pergunta espera você” é mais preciso; zoom e abrir ticket ainda demonstrativos, não verificados como funções reais.
- Parecer: portal/revisao-amostra-v2.md. Evidências próprias em revisao-amostra-v2/ nesta pasta do papel; script review_amostra_v2.py. Marco7 continua independente, aguardando entrega.
- Parecer da amostra enviado ao Designer pela skill Maestri; check mostrou mensagem no histórico, prompt inferior vazio e Designer processando. Sem texto preso; resposta ainda não chegou nesta conferência.

## Revisão dirigida da amostra corrigida

- Quatro frentes principais atendidas: títulos HTML 15 px estáveis nos dois tamanhos, critérios fora do SVG, setas e remoção da trilha decorativa, texto09/dia da semana corrigidos. Chip aberto 7,17:1, setas 5,15:1, ativo escuro 7,63:1; interação e reduced-motion passaram.
- Ainda duas importantes para aprovar amostra: hover do menu permanece claro e cai a cerca de 3,86:1; badges de espera16/17 aparecem junto de rótulos dos outros tickets em 1600 e confundem associação. Sugestão: regra antiga ainda deixa números em 13,5 px, sobrescrevendo os 14 prometidos.
- Parecer vigente da amostra: portal/revisao-amostra-v2-dirigida.md. Evidências em revisao-amostra-v2-dirigida/ na pasta deste papel. Não altera aprovações técnicas anteriores; visual ainda aguarda correção e opinião do Gustavo.
- Revisão dirigida enviada ao Designer pela skill Maestri; check mostrou mensagem no histórico, prompt inferior vazio e Designer processando. Sem texto preso; resposta ainda não chegou.

## Amostra aprovada para apresentar ao Gustavo

- Três últimas pendências corrigidas e conferidas: hover escuro 6,61:1; selos de espera junto das próprias tendas nos dois tamanhos; números HTML de 14 px (regra residual removida). Interação curta/reduced-motion passaram, sem erro JS.
- **Amostra Mesa de mapas aprovada para o maestro apresentar ao Gustavo**, sem antecipar aceite estético dele, integração nas cinco telas ou marco7.
- Parecer vigente da amostra: portal/revisao-amostra-v2-final.md. Provas/capturas próprias em revisao-amostra-v2-final/ na pasta deste papel. Script review_amostra_v2_dirigida.py atualizado para calcular camada de hover efetivamente lida do navegador.
- Próximo: aguardar retorno do Gustavo pela via combinada e entrega do marco7; depois revisar visual integrado conforme novo escopo aprovado.
- Aprovação da amostra enviada ao Designer pela skill Maestri; check confirmou recebimento e resposta dele: vai registrar no diário e encaminhar ao maestro. Prompt vazio, sem mensagem presa.

## Nova forma v3: revisão pendente de três correções

- Gustavo aprovou clima/paleta/tipografia da v2, mas recusou a trilha de triângulos; literal em pedido.md. Designer agora Claude Opus5.5 propôs faixa feito/frentes/verificação/destino. Não reabrir clima e fontes já aceitos.
- Revisão v3: recomendo manter a forma; amostra ainda não aprovada para apresentação. Três importantes: realce reduz contraste de itens operáveis (marcos .32 e folhas .22 em reduced-motion); dicas não dispensáveis por Esc/não hoveráveis; “nenhum critério verificado” inventa estado individual ausente da API (usar verificação final pendente pelo ticket17 aberto).
- Dados/camadas/contagens/arestas conferem com API real. Margem32/53 com bloqueia=[], fio17→destino correto como finalidade. Contrastes base passam; fonte mínima14, sem overflowhorizontal, roving índice e reduced-motion conferidos. Sugestão: mostrar dois/três resultados em palavras no Jáfeito, além dos números.
- Parecer vigente desta amostra: portal/revisao-amostra-v3.md. Evidências em revisao-amostra-v3/ na pasta deste papel, script review_amostra_v3.py. Sem alteração de dados reais; marco7 não revisado nesta rodada.
- Parecer v3 enviado ao Designer pela skill Maestri; check mostrou mensagem no histórico, prompt inferior vazio e Designer processando. Sem texto preso; resposta ainda não chegou nesta conferência.

## Amostra v3 aprovada para apresentar ao Gustavo

- Revisão dirigida encerrou os três importantes: opacidade1 em marcos/folhas com e sem reduced-motion, quadrados claros com contraste7,26:1; Esc fecha dica/placa sem reabrir e mantém foco, ponteiro entra/sai da dica corretamente; textos falam em verificação/aceite final pendente.
- Destaques em palavras25/22/34 conferem com API:6/4/4 dependentes diretos, filtroresolved e desempatepornumero. Foco no25 acende seu quadrado e mostra os dependentes.
- **V3 APROVADA para devolver ao maestro e mostrar ao Gustavo.** Não antecipa preferência estética dele, implementação nas cinco telas ou marco7. Clima/paleta/tipografia da v2 já foram aceitos por ele; forma v3 ainda aguarda seu retorno.
- Parecer vigente: início de portal/revisao-amostra-v3.md; primeira revisão preservada abaixo como histórico. Evidências próprias em revisao-amostra-v3-dirigida/ na pasta deste papel; script review_amostra_v3_dirigida.py. Faixa inteira em1600x900 (bottom868), rolagem vertical em1280x800 (bottom1014), sem horizontal/erroJS.
- Aprovação v3 enviada ao Designer pela skill Maestri; check confirmou recebimento e resposta dele, com registro da aprovação no construcao.md e encaminhamento ao maestro. Sem texto preso no prompt.

## Marco visual v2 integrado: três correções pendentes

- Gustavo autorizou aplicar nas cinco telas. Designer aplicou fontes/papel/menu e faixa da v3 gerada da API; nota de leitura no Início para não cobrir vizinhos. Marco7 continua segurado e não foi revisado aqui.
- Parecer: portal/revisao-visual-v2.md. Linguagem visual/composição geral aprovadas; marco integrado ainda não aprovado por três importantes: (1) função de layout ignora aresta de ciclo/inexistente e libera falsamente cartão/placa/nota/próximo passo; (2) doca fica fora da janela ao focar criterio-5/conquista-34 em1280; (3) obstáculos das dicas só existem no Início, onde se usa doca, e tooltip de Designs cobre cartão vizinho.
- 120 testes do núcleo +4 do projeto real OK,0 problemas reais; sete rotas nos dois tamanhos fonte mínima14 e sem overflowhorizontal; rascunho/envio/cópia da correção/filtro/leitor/foco da placa após mudança de arquivo passaram. Sem erroJS ou HTTP externo no roteiro. Escritas de teste só em cópias temporárias próprias, servidores próprios encerrados.
- Evidências em revisao-visual-v2/ na pasta deste papel; scripts review_visual_v2.py, review_visual_v2_fronteiras.py, review_visual_v2_dica.py. Recomendação: manter desenho e corrigir comportamento/veracidade; alinhar proposta.md ao visual vigente.
- Parecer visual v2 enviado ao Designer pela skill Maestri; check mostrou mensagem no histórico, prompt inferior vazio e Designer processando. Sem mensagem presa; aguardando resposta/correções.

## Restrição de escopo e prazo — Gustavo

- Gustavo cobrou demora e determinou que a próxima revisão dirigida confira **só os três achados de revisao-visual-v2.md**, sem novos achados de acabamento nem repetição da revisão geral.
- **Área fixa e sempre visível para dica/nota resolve os achados 2 e 3.** Aceitar essa solução sem exigir outro posicionador ou refinamento visual.
- Só bloquear por informação incorreta (como liberação falsa de ticket) ou quebra de uso. Sugestões documentais/estéticas não bloqueiam.
- Aguardar correção do Designer e fazer apenas provas dirigidas dos três pontos; preservar essa restrição em qualquer retomada.

## Marco visual v2 aprovado após revisão dirigida

- **APROVADO**, somente pelos três achados da revisão anterior, conforme limite do Gustavo. Bloqueadores inexistentes/cíclicos agora informam espera verdadeira em cartão, aria-label, nota, placa e Próximo passo.
- Faixa de leitura fixa da casca resolve os itens 2 e 3: 16 focos dirigidos em Início, Designs e Decisões, nos dois tamanhos, todos visíveis e sem sobrepor a tela. Esc preserva/devolve foco e não reabre leitura nem placa.
- Parecer vigente no topo de portal/revisao-visual-v2.md; histórico preservado abaixo. Provas próprias em revisao-visual-v2-dirigida/ na pasta deste papel; script review_visual_v2_dirigida_final.py. Não repetidas suítes/revisão geral; nenhum novo achado de acabamento. Escrita só em fixture própria; servidor encerrado.
- Marco 7 continua segurado e fora deste aceite. Próximo: comunicar aprovação ao Designer e aguardar entrega específica do marco 7.
- Aprovação enviada ao Designer pela skill Maestri; check confirmou mensagem no histórico, prompt vazio e encaminhamento do aceite ao maestro já em execução. Sem texto preso. Aguardar entrega específica do marco 7.

## Marco 7 aprovado — canal A

- **APROVADO** em portal/revisao-marco7.md. Canal A autorizado por Gustavo em pedido.md; canal B permanece reserva sem aceite de ponta a ponta. Visual v2 continua aprovado. Marco 8/conferência final ainda não aprovados.
- Execução própria: 123 testes do núcleo OK (45,667 s), 4 reais OK/0 problemas. Código das três correções conferido; capturas próprias no real (somente leitura) e cópia fora do canvas abertas. Faixa acompanha disponibilidade.
- Cinco cenários reais realizados pelo Designer/maestro cruzados com construcao.md, ticket 53, seis arquivos lida e fila/API entregue. Envio com 0 tentativas já absorvido é comportamento correto; primeiro envio após correção está encerrado.
- Limites: escada/timeout completos apenas nos testes controlados; causa do erro isolado sem traceback permanece não verificada, não reproduzida nesta rodada; motivo detalhado na API é limitação sem bloqueio. Não repetir testes reais sem necessidade.
- Provas em revisao-marco7/ e review_marco7.py na pasta deste papel; escritas só em cópias, servidor próprio encerrado. Próximo: devolver aceite ao Designer e aguardar marco 8.
- Aceite enviado ao Designer via Maestri; check mostrou mensagem no histórico e prompt inferior vazio. Recebido, sem texto preso; Designer em turno. Aguardar marco 8.

## Marco 8 — fechamento em curso

- Parecer em portal/revisao-final.md. 123 + 4 testes próprios OK; 18 capturas próprias nos dois tamanhos, mínimo 14 px/sem overflow/zero JS; provas mapa/rodada, sanitização e isolamento de iframe passaram. Selo/proposta corrigidos. Sem achados de acabamento.
- Falta confirmar verbete R: R1 no ticket 25 é remendo técnico do spike, não pergunta. Designer confirmou e corrige só configuração; recomendação explícita de solução simples sem refatoração. Aguardar retorno e verificar a dica corrigida antes do aceite final.

## Portal aprovado — marco 8 e aceite final

- **APROVADO** em portal/revisao-final.md. Sem bloqueantes/importantes pendentes. Marcos anteriores e visual v2 permanecem aprovados; marco 8 agora encerra a revisão do portal, que pode seguir ao maestro/Gustavo.
- R1 corrigido sem alteração de núcleo: verbete explica pergunta de decisão e exceção técnica dos tickets 25/30. Fonte pesquisa-26-montagem.md linha 108, API e faixa por foco conferidas após reinício; provas R1-corrigido.json/PNG na pasta revisao-marco8 deste papel.
- 123 + 4 testes próprios OK; capturas próprias, atualização automática, sanitização e sandbox passaram. Selo/proposta atendidos. Limites das provas preservados nos pareceres final e marco 7; nenhuma escrita na caixa real nem novos avisos de teste ao maestro.
- Próximo: comunicar aceite final ao Designer, confirmar entrega; aguardar eventual pedido específico do maestro/Gustavo. Não abrir nova rodada de acabamento por iniciativa própria.
- Aceite final enviado via Maestri; check confirmou mensagem no histórico, prompt vazio e Designer registrando/devolvendo ao maestro. Sem mensagem presa. Revisão encerrada; aguardar pedido específico.

## Pós-aceite — duas correções relatadas pelo Gustavo

- **APROVADAS** em portal/revisao-correcao-rodada.md: rodada reescrita depois da resposta volta a esperar, nova resposta usa base atual/substitui; atualizações preservam edição na rodada, gaveta e tira do leitor. Sem reabertura de acabamento/revisão geral.
- 127 testes próprios do núcleo OK (41,755 s), 4 reais OK/0 problemas. Prova própria no navegador em cópia curta: mesmo nó/foco/seleção/texto/rolagem/details, aviso e transição explícita da rodada, resposta nova gravada corretamente; zero JS. Capturas abertas, servidor próprio encerrado, nenhuma escrita na caixa real.
- Evidências/script revisao-correcao-rodada/ e review_correcao_rodada.py na pasta do papel. **Caminhos acima de 260 caracteres: pendência separada declarada pelo Designer, não corrigida nem investigada nesta rodada.** Não afirmar que este aceite resolveu isso.
- Próximo: comunicar aceite dirigido ao Designer e aguardar pedido específico.
- Aceite enviado via Maestri; check confirmou mensagem no histórico, prompt vazio e Designer registrando/devolvendo ao maestro. Sem texto preso. Aguardar pedido específico.

## Três entregas — substituição, ritmos e amostra do System design

- Parecer portal/revisao-tres-entregas.md: **regra de carta substituída e prototipo-12-ritmos aprovados; System design planta aprovado somente como AMOSTRA para Gustavo**. Não trocar system-design.html antes do aval dele.
- 135 testes próprios do núcleo OK (39,991 s), 4 reais OK/0 problemas. Substituição em cópia: arquivo JSON intacto, antiga histórica com selo/link, leitores antigo/novo corretos. Números/parcelas da carta conferem com levantamento-12-iniciativas.md §2b; sem nomes de pessoas.
- Amostra: 124 textos idênticos com contagem, sem scroll, arraste direito/Ctrl+roda/Shift+roda/card/Esc funcionando em file e iframe sandbox nos dois tamanhos. Capturas próprias abertas, zero JS.
- Fontes CDN nas duas páginas foram apontadas e corrigidas pelo Designer durante a revisão: embutidas em data, carregamento próprio offline confirmado. Sem outro achado pendente nestes três itens. Caminhos longos permanecem pendência separada.
- Provas em revisao-tres-entregas/ e review_tres_entregas.py na pasta do papel; servidores próprios encerrados, nenhuma escrita na caixa real. Próximo: comunicar ao Designer, aguardar retorno do Gustavo sobre a amostra.
- Parecer enviado via Maestri; check confirmou recebimento, prompt vazio e Designer registrando/devolvendo ao maestro. Sem texto preso. Aguardar aval do Gustavo sobre a amostra.
- Designer declarou ao fechar: cartas históricas/substituídas prototipo-12-miolo e prototipo-12-blocos ainda dependem de jsDelivr. Não fazem parte das duas páginas novas aprovadas aqui; ficam registradas como dependência externa pendente, sem solicitação de ampliação desta rodada.

## Proposta nova — cidade 2.5D, após recusa da planta

- Gustavo recusou a planta técnica por conservar a forma do diagrama. Brief novo em amostras/system-design-cidade-brief.md; ainda é proposta, subagente do Designer já construindo. Não substituir System design vigente.
- Parecer em portal/revisao-direcao-cidade.md: direção recomendada com limites; conteúdo pode ir para ficha, mas 124 strings precisam de associação semântica e acesso real. Acrescentar paridade de componentes/arestas/estados e todas as fichas operáveis.
- Cuidados: ilhas pares sem centralização, GitHub só cópia, túnel é junction local, muralha não inventa exclusividade de entrada, fronteira de gravação não engloba todo acesso Markdown, placas de sync não são bloqueio da ponte. Recomendo 14 px efetivos e amostra estática primeiro.
- Sem testes/aceite de entrega nesta rodada. Próximo: comunicar parecer ao Designer para ajustar brief/subagente; aguardar amostra, depois aval do Gustavo.
- Parecer enviado via Maestri; check confirmou mensagem no histórico, prompt vazio e Designer atualizando brief/repassando ao subagente. Sem texto preso. Aguardar amostra.

## Carta r12 — sumário do hub

- **APROVADA** em portal/revisao-carta-r12.md. Três decisões/opções/recomendadas conferem com a rodada; caminhos previstos, exemplos e limites não verificados identificados; sem nomes de pessoas.
- Origem TRF3 conferida em leitura: 32 prints-intune, 319 piloto, 56 anexos +12 diagramas (=68 repasse), 73 operacao, 4 context, total496. Print de 2026-08-19 existe. Designer corrigiu 57→56 durante revisão; HTML e capturas próprias confirmam.
- Fontes embutidas carregadas em iframe sandbox, zero externo/zero JS, capturas próprias nos dois tamanhos abertas. API confirma ritmos substituída por sumario. Sem suites repetidas para carta estática, sem escrita na caixa real/origem, Edge próprio encerrado.
- Provas em revisao-r12/ na pasta do papel. Próximo: comunicar aceite ao Designer; aguardar amostra da cidade, ainda não entregue/aprovada.
- Aceite enviado via Maestri; check confirmou mensagem no histórico, prompt vazio e Designer encaminhando ao maestro. Sem texto preso. Aguardar amostra da cidade.

## Cidade 2.5D — amostra aprovada para Gustavo

- **APROVADA PARA APRESENTAR AO GUSTAVO**, em portal/revisao-amostra-cidade.md. Agora forma de cidade/bairros/volumes/ruas, com fatos preservados. Não substituir System design vigente antes do aval dele.
- Prova própria em file/iframe sandbox e nos dois tamanhos: 28 componentes e30 arestas conferem semanticamente; 28 fichas por foco/Enter com subtítulos/selos completos, Esc devolve foco; arraste direito/Ctrl/Shift/sem scroll passaram. Menor fonte mapa14,40/16,67px, Outfit carregada, zero externo/zeroJS.
- Selos até200MiB e commit+push no mapa final; podefechar/+Copilot nas fichas, dentro do brief. Relatório fornecido124/124 e cliques28 após pan/zoom conferido junto das provas próprias. Cadastro como amostra e planta histórica conferidos.
- Provas em revisao-cidade/ e review_cidade.py na pasta do papel; servidores/Edges próprios encerrados, sem escrita na caixa real. Próximo: comunicar ao Designer e aguardar aval do Gustavo.
- Aceite da amostra enviado via Maestri; check confirmou mensagem no histórico, prompt vazio e Designer processando. Sem texto preso. Aguardar aval do Gustavo, sem troca antecipada do vigente.

## Direção nova — proposta Laços

- Pedido explícito do Gustavo em pedido.md: só carta-proposta de página Laços abaixo de Decisões; nada de construir antes do aval. Designer tem subagente produzindo amostras/portal-lacos-proposta.html. Este parecer não é revisão de entrega.
- Direção recomendada em portal/revisao-direcao-lacos.md: estado real/pedido/esboço distintos; pedido imutável por UUID, laço+execução, revisão config relevante, antes/depois; conflito revalidado ao aplicar, recibo persistido e efeito confirmado. Lido não é aplicado; execução encerrada não transmite pedido para próxima.
- Pausa/parada também pedidos com capacidade/ponto seguro declarado. Não prometer pausa genérica/kill instantâneo pelo parar_apos.py. Painel observador separado de etapas humanas fora dos scripts; suíte hipotética marcada exemplo. Fontes e parâmetros registrados pelo maestro, sem caminhos/comandos arbitrários do browser.
- Sem testes/execuções nesta rodada. Próximo: comunicar direção ao Designer, aguardar carta-proposta e aval do Gustavo antes de implementar.
- Direção enviada via Maestri; check confirmou mensagem no histórico e prompt inferior vazio. Sem texto preso. Aguardar carta-proposta.

## Carta-proposta Laços — fechamento em curso

- Parecer em portal/revisao-lacos-proposta.md. Contrato/forma/fatos ampla/testes conferem, arquivo offline renderizado nos dois tamanhos e iframe; zero externo/zeroJS. Não autoriza construir.
- Corrigir informação: Teto1.200/4h aparecia vigente apesar de ser recomendação; faltavam A confirmar visíveis. Designer corrige. Origem embeddings mudou durante revisão de36/72/sem teto para44/88/teto600/2h: pedir retrato histórico20h14 explícito, sem perseguir contadores atuais.
- Pedidos enviados ao Designer e recebidos; aguardar/conferir correção final antes de aprovar para Gustavo. Nenhuma escrita na caixa real nem execução de laço/suíte.

## Carta-proposta Laços aprovada para Gustavo

- **APROVADA PARA APRESENTAR AO GUSTAVO** em portal/revisao-lacos-proposta.md. Não autoriza implementar página/API/controles antes do aval.
- Correções de informação conferidas: maquete como retrato histórico20h14, não atual; Teto1.200/4h proposto/sem aprovação; A confirmar visível; teto gravado depois600 tentativas/2h (chave pedidos compara SUM(tentativas), unidade corrigida).
- Capturas próprias corrigidas nos dois tamanhos abertas; contrato/fatos amplos/testes estáticos/fontes locais/iframe conferidos. Sem bloqueantes/importantes pendentes na carta. Sem escrita na caixa real, sem laço/testes executados, processos próprios encerrados.
- Próximo: comunicar aceite ao Designer; aguardar escolhas do Gustavo e entrega separada da cidade v2 se solicitada.
- Aceite enviado via Maestri; check confirmou mensagem no histórico, prompt vazio e Designer encaminhando ao maestro. Sem texto preso. Aguardar escolhas do Gustavo, sem implementação antecipada.

## Laços L1 — especificação ainda não aprovada

- Gustavo liberou construção no ticket55: passoB, nomeLaços, suítesdepois, opções e comentário por nó/laço. Brief portal/lacos-brief.md define L1 sótexto, L2núcleo, L3tela.
- Parecer portal/revisao-lacos-L1.md: arquitetura mantida, **L1 ainda não aprovado por5 importantes**: revisão ignora definições/contexto do teto.inicio; configurado não é efetivo; pedidos lida/aguarda precisam retomada e aplicação idempotente; recibo precisa formato/validação/dono/substitui fechados; grupoEsperaVocê deve excluir rodada respondida e conflito histórico substituído.
- Aceitos registro explícito/endpoints separados/caixaúnica, revisão semcontadores e contextual para comentários/comandos, releitura, fontes confinadas, SQLiteWALro, exemplosfato/suposição. Sem testes/execuções/consultas novas aosbancos nesta revisão só especificação.
- Próximo: comunicar aoDesigner e aguardar correção dirigida antes deL2. Não implementar por este papel.
- Parecer enviado via Maestri; check confirmou mensagem no histórico, prompt vazio e repasse ao subagente de contrato. Sem texto preso. Designer recebeu também esclarecimentos do maestro enquanto a revisão acontecia; próxima entrega deve consolidar esses esclarecimentos e os cinco pontos, ainda só texto.

## Cidade v2 — aprovada para apresentar ao Gustavo

- Parecer em portal/revisao-amostra-cidade-v2.md. Pedido radial/vista de cima/rótulos/analogias atendido; sem bloqueantes ou importantes pendentes. Não substituir vigente antes do aval do Gustavo.
- Duas frases factuais corrigidas e conferidas: guarda preserva base/ramo de conflito, não “barra conflito”; MCP restringe esta porta, não todo acesso externo.
- Provas próprias file/iframe nos dois tamanhos: 28 componentes e 30 ligações preservados, 28 fichas acessíveis, foco/Enter/Espaço/Esc, arraste/Ctrl/Shift OK, sem scroll/externo/erro JS. Mínimo 14,07/17,40 px. Relatório radial fornecido e algoritmo conferidos, sem reabrir encostos de acabamento.
- Provas em revisao-cidade-v2/ na pasta do papel. Processos próprios encerrados, nenhuma escrita na caixa real. Próximo: comunicar aceite ao Designer e aguardar Gustavo. Laços L1 permanece separado, aguardando correção dirigida.
- Aceite enviado via Maestri; check confirmou mensagem no histórico, prompt vazio e Designer encaminhando ao maestro. Sem texto preso. Aguardar aval do Gustavo.

## Laços L1 — correção dirigida aprovada

- Parecer vigente no topo de portal/revisao-lacos-L1.md: **L1 APROVADO para abrir L2**, cinco importantes resolvidos. O parecer inicial permanece histórico.
- Revisão/precondições/retrato, configurado versus em uso, retomada/reconciliação antes de efeitos, recibos/substitui e espera você atual conferidos; menores e ressalvas do anexo tratados.
- Sugestão sem bloquear: explicitar que comentários em lida estão concluídos e que aplicado com efeito aguarda ainda requer confirmação, nas frases gerais de pendência/desfecho. As regras específicas já dizem isso.
- Só revisão documental, sem testes, bancos, execução ou caixa real. Próximo: comunicar ao Designer e aguardar implementação/provas do L2.
- L1: aceite enviado via Maestri; check confirmou no histórico, prompt vazio e Designer consolidando as duas ressalvas. Sem texto preso. L2 pode seguir.

## Laços L2 — três correções; contador e histórico aprovados

- Parecer portal/revisao-lacos-L2.md: L2 ainda não aprovado. Bloqueia: exceção /carta de painel na raiz do laço serve config.json (200). Importantes: id de nó em lista no descritor derruba GET /api/lacos (500); mudança compatível de faixa retorna definicao_mudou false indevido (409 permanece correto).
- Decisões 8/10/11 aceitas com ajuste explícito do contrato; 7 precisa desconhecido ou comparação confiável; 19 precisa restringir publicação de painel sem fontes. Demais conservadoras aceitas.
- Contador de cartas aprovado: prova própria Edge/cópia 2→1 depois de aprovação, sem JS; cadastro cidade v2 histórico/recusado conferido. Sem reabrir acabamento/desenho.
- 206 núcleo +6 projeto real OK executados nesta revisão. Provas extras em revisao-l2/ e review_l2.py na pasta do papel. Cópia curta removida, processos próprios encerrados, nenhuma escrita na caixa real/implementação.
- Próximo: comunicar Designer e aguardar revisão dirigida dos três achados do L2.
- Parecer L2 enviado via Maestri; check confirmou no histórico, prompt vazio e Designer encaminhando os três achados para correção. Sem texto preso.

## Laços L2 — correção dirigida aprovada

- Parecer vigente no topo de portal/revisao-lacos-L2.md: **L2 APROVADO, pode seguir L3**. Três achados resolvidos, parecer anterior histórico.
- Provas próprias repetidas: painel na raiz/config 404; ligação com id lista vira laço malformado, lista200/outro intacto; mudança de faixa + hash anterior retorna409/definicao_mudou null. Contrato §4.5/§4.6 alinhado; testes de painéis legítimos/ids/POST/detalhe422 passaram.
- 218 núcleo OK (97,6s) +6 reais OK executados aqui. review_l2.py incluindo Edge repetido: contador2→1, zeroJS. Sem novos achados, caixa real ou implementação; processos próprios encerrados/cópia removida.
- Próximo: comunicar aceite ao Designer; aguardar L3 (tela ainda não revisada).
- Aceite L2 enviado via Maestri; check confirmou no histórico, prompt vazio e Designer seguindo para L3. Sem texto preso.

## Aviso sem esperar o ask — aprovado, 2026-10-15

- Parecer portal/revisao-aviso-sem-espera.md: APROVADO. Prova de entrega libera a trava sem esperar maestro ocioso; Markdown de todos ou UUIDs fora do prompt; saída em temporários, acompanhante limitado com portal vivo.
- Reproduzi órfão após saída do pai. Designer corrigiu parada normal (encerra asks já provados) e declarou limite após queda abrupta/procedimento de recuperação por UUID entregue em proposta/LEIA. Processo remanescente não justifica reenvio. Filho próprio da prova encerrado, nenhum processo real tocado.
- 222 núcleo OK (558,4s) +6 reais OK; teste de parada normal acrescentado durante revisão rodado separadamente:1 OK. Não são223 em uma execução. Sem prova real nova de envio ao maestro; suíte usa falso. Nenhuma escrita na caixa real/implementação pelo Prumo.
- Próximo: comunicar aceite ao Designer. L3 Laços segue separado.
- Aceite enviado via Maestri; check confirmou a mensagem na fila do Designer (Press up to edit queued messages), fora da caixa de digitação. Sem Enter extra: está enfileirada, não presa. Aguardar L3.

## Laços L3 — uma quebra de uso para corrigir

- Parecer portal/revisao-lacos-L3.md: ainda não aprovado. Importante: d.substitui persiste depois de desfecho concorrente; POST400 manda enviar sem substituir, mas UI não oferece recuperação, e recarga repete400. Prova própria:120→200/250 substituem OK; rascunho300 enquanto anterior recusado fica preso.
- Decisões a/b aceitas no escopo: contador global só rodadas/cartas, conflitos na faixa de Laços; substituição automática compatível com aviso. Sugestão: tooltip zerado não prometer ausência global de pendência.
- Edge próprio/cópia dois tamanhos,8 gavetas Enter/Esc/foco, preservação texto/cursor/nó, SVG14px/sem overflow/zeroJS. RealGET somente, Pesquisa ampla dois tamanhos. Provas revisao-l3/ +review_l3.py na pasta papel. Cópia removida/processos encerrados/caixa real intacta.
- Teste alterado do falso (erro→retry)1 OK próprio. Não repeti núcleo completo;223+6 são evidência do Designer. Aviso/L2 seguem aprovados.
- Próximo: comunicar Designer e aguardar correção dirigida da recuperação, sem reabrir acabamento.
- Parecer L3 enviado via Maestri; check confirmou no histórico, prompt vazio e Designer encaminhando só a recuperação e tooltip. Sem texto preso.

## Laços L3 — correção dirigida aprovada

- Parecer vigente no topo de portal/revisao-lacos-L3.md: **L3 APROVADO**, recuperação resolvida. Parecer anterior histórico; sem novos acabamentos.
- Próprio Edge/cópia1280: pedido anterior com desfecho não gera POST silencioso; recarga mantém300/texto; escolha novo gera200/UUIDnovo/sem referência. Outro aberto exige escolha e substitui só o arquivo escolhido. Parada recupera onda4/texto. Rede repete corpo/UUIDidênticos. ZeroJS.
- Fonte/contrato/rascunho antigo/tooltip conferidos. Prova fornecida12/12 inclui400 real e pausa/retomada, não confundidos com repetição própria.223+6 são do Designer; backend não repetido.
- Provas review_l3_recuperacao.py/revisao-l3-recuperacao na pasta papel; roteiro próprio final passou com espera por respostasHTTP. Cópia removida, processos encerrados, caixa real/implementação intactas.
- Próximo: comunicar aceite ao Designer para entregar ao maestro.
- Aceite L3 enviado via Maestri; check confirmou no histórico, prompt vazio e Designer preparando entrega ao maestro. Sem texto preso.
