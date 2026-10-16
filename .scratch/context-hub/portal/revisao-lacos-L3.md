# Laços L3 — Prumo, 2026-10-15

## Parecer vigente após correção dirigida

**L3 APROVADO. A recuperação de `substitui-invalido` está resolvida; sem bloqueantes ou importantes pendentes neste marco.** O parecer inicial abaixo permanece como histórico. Nenhum acabamento reaberto.

Conferidos `lacoAtual`, releitura antes do envio, alvo mostrado versus escolha explícita, migração do rascunho antigo, bloco de recuperação e contrato §2.6 item 4. O retry ambíguo usa `emVoo.corpo` antes de reler/recalcular; continua imutável.

**Provas próprias no Edge, cópia curta, 1280×800:**

- Repeti 120→200/250, comecei 300 e dei desfecho ao anterior. Nenhum POST novo saiu sem decisão; mensagem trouxe pedido, recusa e motivo em palavras.
- Após recarga, valor 300 e texto continuaram. “Enviar como pedido novo” retornou 200, UUID novo, sem `substitui` no recusado, com valor/texto preservados.
- Fiz aparecer outro pedido aberto durante a edição: nenhuma substituição silenciosa. A tela ofereceu as duas opções e só substituiu o arquivo correto após escolher “Enviar substituindo…”.
- Repeti com parada: desfecho concorrente → escolha → envio novo 200, sem referência, onda 4 e comentário preservados.
- Abortei a primeira tentativa de comentário na rede: “Tentar de novo” repetiu exatamente o mesmo corpo e UUID. Zero erro JS no roteiro.

Captura própria da recuperação aberta e conferida; `review_l3_recuperacao.py` e `revisao-l3-recuperacao/resultados.json` na pasta deste papel. O roteiro próprio passou após substituir esperas fixas por espera da resposta HTTP nas transições; as falhas intermediárias eram sincronização do roteiro, não achados do produto.

Conferi também código e prova fornecida **12/12, tudo_ok**, cobrindo 400 real após leitura antiga, pausa/retomada e recarga. Não apresento esses casos adicionais como repetição própria. Dica do contador zerado agora diz “nenhuma rodada ou carta espera você”, conforme a sugestão.

Aceites anteriores de forma, rotas, foco, preservação e dois tamanhos permanecem. Não repeti suítes do núcleo: backend sem alteração; **223+6 são resultados do Designer** nesta entrega. Cópia removida, Edge/servidor próprios encerrados, nenhuma escrita na caixa real ou implementação pelo Prumo.

**Próximo:** Designer entregar o marco ao maestro. Esta aprovação conclui a revisão da tela dos Laços neste escopo.

---

**Ainda não aprovo L3: uma quebra de uso na recuperação da substituição automática.** Direção visual, separação dos estados e as duas decisões de tela são aceitas, com a correção dirigida abaixo. Sem reabrir acabamento ou L2.

## Importante — rascunho fica preso a pedido que já teve desfecho

`nucleo/web/telas/lacos.js:1171`, `:1203`, `:1215` e tratamento de `substitui-invalido` em `:864`.

Prova própria no Edge sobre cópia curta:

1. No Juntador, pedir 120→200; pedir 120→250 enquanto o primeiro está aberto. Ambos retornam 200, e o segundo substitui corretamente o primeiro.
2. Começar uma terceira proposta, 300. Simular o maestro recusando o segundo pedido (`estado: recusado`, motivo), antes do envio.
3. O envio novo retorna 400 `substitui-invalido`. A tela diz “envie sem substituir”, mas conserva `d.substitui` apontando o recusado e não oferece ação para retirá-lo.
4. Recarregar e reenviar repete o mesmo 400, mesmo UUID e referência. O texto/valor persistem, mas o pedido não pode sair pela interface.

Isso não pede mudar a regra do núcleo: ele recusou corretamente. **Recomendação:** no 400 inequívoco de substituição, reler os pedidos e oferecer recuperação executável (por exemplo “Enviar como pedido novo”, retirando a referência inválida e gerando outro UUID, preservando valor/texto). Se houver substituto atual compatível, não o substituir silenciosamente com informação antiga. Conferir o mesmo caso para parada/pausa/retomada, cujo formulário preservado também fecha sobre o retrato anterior. Não alterar corpo/UUID de retry ambíguo de rede: esse caminho deve continuar imutável.

Critério dirigido: pedido anterior encerrado enquanto o usuário escreve → erro em palavras → recuperação pela tela → novo envio 200 sem substituir pedido encerrado; valor/texto preservados e nenhum efeito direto no laço. Repetir após recarga.

## Decisões aceitas

- **(a) Conflito fora do contador global:** aceito no escopo declarado. O contador conta rodadas/cartas; não exigir polling de laços em todas as telas. A página Laços mostra grupo, faixa terracota e pedido em conflito. **Sugestão pequena:** no tooltip do contador zerado, trocar “nada espera por você” por “nenhuma rodada ou carta espera por você”; a primeira frase promete ausência global de pendência que o contador não consulta. Isso não exige acrescentar laços à conta.
- **(b) Substituição automática:** aceita quando há pedido atual compatível em nova/lida/conflito, com aviso visível. Prova própria confirmou o vínculo e preservação dos dois arquivos. A recuperação de desfecho concorrente é o importante acima. Comentários permanecem envios independentes.
- Configurado, em uso e proposta estão separados; recibo inválido não vira aplicação; laço terminado não oferece alteração/parada e mantém comentário. Rotas/gaveta, faixas por papel e observador fora da causalidade seguem o brief.

## Evidência

- Li `lacos.js`, integração de rota/casca e decisões de §2.6; examinei relatório/roteiros fornecidos (31 passos registrados, incluindo 400/409 null/true, rede, conflito e recibo).
- **Próprio, cópia:** 1600×900 e 1280×800, 8 nós, fontes SVG mínimas 14 px, documento sem rolagem horizontal. Oito gavetas por foco/Enter/Esc em cada tamanho, retorno ao nó correto. Texto/foco/cursor e o próprio nó do formulário preservados após redesenho. Zero erro JS. Capturas próprias abertas.
- **Próprio, real só leitura:** Pesquisa ampla nos dois tamanhos, todas as requisições não GET bloqueadas. Capturas abertas; nenhuma escrita na caixa real. Relatório fornecido cobre também embeddings/gavetas reais e limpeza nos dois tamanhos. Sem novos achados de acabamento.
- Teste alterado do maestri falso: `EmissorSemThread.test_erro_vira_pendente_com_esperas_1_5_15_e_depois_falhou` executado aqui, **1 OK**. Não repeti 223+6 do núcleo para uma tela sem alteração de backend; esses números são do Designer. Aceite do aviso permanece vigente.

Provas próprias: `review_l3.py`, `revisao-l3/resultados.json` e capturas na pasta deste papel. Cópia em `C:/tmp/pr-l3` removida; Edge e servidor próprios encerrados. Nenhuma alteração de implementação por este papel.

**Próximo:** corrigir somente a recuperação da substituição, consolidar a redação do tooltip e devolver revisão dirigida. O restante está aceito.
