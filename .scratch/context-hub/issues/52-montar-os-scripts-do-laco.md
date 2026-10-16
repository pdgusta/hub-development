# Montar os scripts do laço da pesquisa ampla

Type: task
Status: resolved

## Question

Construir os scripts que a [proposta refeita](../prototipos/proposta-50-laco-da-pesquisa.md) pede, para que a
"Pesquisa ampla: lugares e mecanismos de busca" possa rodar: o despachante (roteamento por modelo fixado, com
orçamento, ritmo por pool e saúde), o gerador (pedidos, validação, divisão de célula, retomada), o juntador
(junção, bola de neve, gate dos 5%, calibração com sementes ocultas) e o plano inicial de células, mais as
instruções de cada papel. AFK: o agente constrói; nada chama o gateway de verdade sem o "pode iniciar".

## Answer

Scripts em [`laco/`](../laco/LEIA.md), usados na pesquisa ampla de 2026-10-13 (5 ondas, 7388 tentativas, 5526
itens): `comum.py`, `despachante.py`, `gerador.py`, `juntador.py`, `plano.py` com `plano.json`, `sementes.json`,
`config.json`, `painel.py` com `painel_dados.py` e `painel/index.html` (Designer), `verificar_urls.py`,
`verificar_atualidade.py` e `parar_apos.py`. Correções feitas durante o uso:
- JSON pedido só no texto (`usar_response_format: false`);
- a onda fecha com até 3% de adiados (`fracao_para_fechar`);
- os processos rodam fora do Claude Code, porque o limpador de memória do Claude Code os matava;
- 20 trabalhadores por gerador.

Base do template "suite de busca" do acervo do maestro (ver o "Not yet specified" do mapa).

## Comments

- 2026-10-13: aberto e reivindicado a partir da cobrança do Gustavo: "você ainda nem criou o script que os
  despachantes vão usar pra ficar roteando corretamente".
- 2026-10-13: scripts escritos em [`laco/`](../laco/LEIA.md): `comum.py` (config, banco SQLite em WAL, gateway),
  `despachante.py` (serviço que relê o gateway a cada 60 s; `escolher` e `liberar` numa transação
  `BEGIN IMMEDIATE`: orçamento a 90% do limite diário por janela de cada pool, reserva de 4 tentativas de
  chave, limite por minuto por modelo e por pool, teto de em voo, par com família e pool diferentes, sorteio por
  folga × acerto, espera depois de 429 e até a virada depois de 3 seguidos), `gerador.py` (fila do grupo,
  validação, até 2 reenvios com o erro apontado, `max_tokens` sobe na 1ª resposta cortada e a célula se divide
  na 2ª, retomada), `juntador.py` (junção por repositório e nome, decisões do recruta, bola de neve, gate dos
  5%, calibração com as sementes ocultas, relatório por onda), `plano.py` (98 células da onda 1), `plano.json`,
  `sementes.json`, `config.json` e `LEIA.md` com os papéis. Compilam; nenhum rodou. Rodada na nota: ensaio
  com gateway falso.
- 2026-10-13: rodada 1 respondida: **B**, sem ensaio; "pode iniciar" a pesquisa de verdade.
- 2026-10-13: primeira rodada de verdade (um gerador, 2 min, 16 chamadas): 5 aceitas, 3 inválidas (reenvio
  funcionou), 1 cortada, 7 falhas do provedor. Três delas eram `format_ignored`: o gateway devolve 502 quando
  pede JSON por `response_format` e o modelo não obedece. Correção: `usar_response_format: false` (JSON só no
  texto, como diz a proposta).
- 2026-10-13: um único pedido adiado por cota segurava a onda 1 inteira. O juntador agora fecha a onda quando
  só restam adiados e eles são até 3% dos pedidos (`fracao_para_fechar`); os que sobram passam para a onda
  seguinte. Rotina "Painel do laço" do Maestri a cada 10 min (o pre-run roda `painel.py --uma-vez
  --pular-disparo`, que manda o estado e sai com 1 para não disparar nada no terminal do maestro).
