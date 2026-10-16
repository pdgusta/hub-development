---
tipo: alteracao-laco
laco: pesquisa-de-regas
ticket: 05
execucao: regas-2026-10-14
operacao: mudar-controle
enviada: 2026-10-14T21:59:30-03:00
envio: 5b0c7e2a-3f41-4d8e-9a17-2c6e8f0b4d31
estado: aplicado
substitui:
aplicando_desde: 2026-10-14T22:05:00-03:00
aplicado_em: 2026-10-14T22:05:40-03:00
efeito: aguarda
valeu_em:
recibo_execucao: regas-2026-10-14
recibo_antes: {"tipo": "numero", "valor": 0.15}
recibo_depois: {"tipo": "numero", "valor": 0.1}
recibo_revisao: e10c217c4b732a968b0059fcb4932dfae421e16d6fa525888fc840d407e9cdfa
agora_esta:
motivo:
---

# Alteração de laço: Pesquisa de horários de rega

pedido: mudar "novos por onda abaixo de" (nó Parada) de 15% para 10% (configurado)
controle: gate_novos
onde está: config.json, chave gate_novos
vale: na próxima onda (quando a onda em curso fechar); quem lê o valor só lê ao ligar (aplicar = gravar e religar quem lê)
configurado no envio: 15% (lido às 2026-10-14T21:59:01-03:00)
em uso no envio: não confirmado
revisão vista: e96e47268d9614816180b17bb035b8f54393851f7bcc80fcf0ef1ad2836c5972
texto:
> a curva já está achatando
