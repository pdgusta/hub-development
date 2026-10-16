# Carta-proposta Laços — Prumo, 2026-10-14

**APROVADA para apresentar ao Gustavo, após as correções de informação.** Sem bloqueantes ou importantes pendentes nesta carta-proposta. Não é autorização de construir a página, API ou controlar laços; isso depende do aval dele.

## Correções encerradas

Conferi no HTML e em novas capturas próprias nos dois tamanhos: maquete delimitada como “Retrato de 14/10 às 20h14”, com aviso explícito de que lista/fluxo/números não são atuais; início posterior informado. Teto agora diz “proposto:1.200·4h” e “sem aprovação” junto do nó. Bloco “A confirmar” visível registra limite da ampla não confirmado, semântica das chamadas em voo e nomes dos parâmetros pendentes. A nota distingue recomendação histórica do teto gravado depois, **600 tentativas ou2h**. A unidade foi corrigida: embora a chave interna se chame pedidos, `despachante.teto_atingido` compara o teto com `SUM(tentativas)` de uso. Assim, pedidos enfileirados e tentativas não são confundidos.

A organização visual explica a página proposta e a edição que vira pedido, sem sugerir implementação já concluída. Preserva-se a decisão de alcance do Gustavo; não há outro pedido de acabamento.

## Conferência e histórico dos achados

Contrato conferido: estado real/pedido/esboço distintos, envio imutável e idempotente, execução identificada, parâmetros permitidos e antes/depois tipados, revisão relevante, conflito sem sobrescrita, aplicado apenas com recibo/efeito, encerramento sem transmitir à execução seguinte, pausa/retomada como capacidade proposta. Painel observador e trabalho humano fora dos scripts separados. Três perguntas de alcance/nome/entrada das suítes, cada uma com recomendação.

Fontes conferidas em leitura: pesquisa ampla 5 ondas, 5.526 itens, 7.382 tentativas, 267 modelos; término 13/10 18:13 UTC =15:13 local, parada pedida após onda5. Última taxa21,66% ≈21,7%, sem alegar parada por saturação. Etapas com1.063 itens de conferência e107/88 na auditoria conferem. Contagem estática de métodos de teste: leitores37, caixa23, torre58, aviso17 e projeto real4; suíte é exemplo sem adaptador, execução desconhecida.

**Achados factuais dirigidos, enviados ao Designer e encerrados acima:**

1. Nó Teto mostrava1.200·4h como se vigente. Na primeira leitura própria do banco de embeddings,36 células/72 pedidos e controle só onda1, sem teto; ticket54 registra1.200/4h como recomendação a aprovar. Marcar proposta junto do valor, sem aparência de limite aplicado.
2. Os “A confirmar” relatados não estavam visíveis na carta. Acrescentar limite histórico da ampla não confirmado, semântica das chamadas em voo a confirmar e parâmetros editáveis ainda a definir.
3. **Origem mudou durante a revisão:** segunda leitura própria encontrou44 células/88 pedidos,12 modelos tentados registrados e teto600 tentativas/2h. Conservar os dados antigos é aceitável como **retrato histórico das20h14, não estado atual**. Não perseguir contador vivo em carta estática.1.200/4h não é o limite escolhido agora.

Provas próprias: capturas file1280/1600 abertas, iframe allow-scripts, fontes embarcadas carregadas, zero pedidos externos/zeroJS. Banco aberto com mode=ro; nenhuma execução de laço/testes, nenhuma escrita na caixa real. Evidências em `C:/Projetos/context-hub/.maestri/roles/d4ce63fd-ce3e-45b5-88f6-6bbd68695030/revisao-lacos-proposta/` (`resultados.json`, PNGs); navegador/servidor próprios encerrados.
