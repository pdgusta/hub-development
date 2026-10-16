# Pesquisa ampla: o que vem depois do laço (aprovado em 2026-10-13)

Ticket "Pesquisa ampla: lugares e mecanismos de busca". O Gustavo aprovou com a resposta B: as 5 etapas, com dois
ajustes:
1. antes de começar, ele dá `/clear` no maestro;
2. **50% da triagem** é feita por subagentes Claude Haiku 5.5, e a outra metade pelo FreeLLMAPI.

## De onde se parte

- Laço concluído às 18:13Z, depois da onda 5 (decisão do Gustavo; o gate dos 5% não foi alcançado e a calibração
  não rodou).
  - Curva de novos: 100%, 76%, 37%, 27% e 22%.
  - 7388 tentativas e 5526 itens em `laco/catalogo/itens.json`.
- Todos os processos do laço estão parados. A rotina "Painel do laço" está pausada.
- No canvas sobram os recrutas Tear (Juntador do laço, Sonnet 5.5) e Designer.
- O que se aprendeu sobre os geradores:
  - nenhum modelo busca na web, nem quando o pedido manda buscar
    ([`laco/verificacao/atualidade.md`](../laco/verificacao/atualidade.md));
  - por citação, de 52% a 76% das URLs são reais
    ([`laco/verificacao/urls-por-provedor.md`](../laco/verificacao/urls-por-provedor.md)).
- Números do catálogo:
  - menções: 888 itens com 3 ou mais, e 4079 com uma só;
  - URLs: 1241 itens com URL real, 1563 só com URL inventada, 1016 com URL bloqueada (429 ou 403 do GitHub) e
    1706 sem URL;
  - ambíguos: 298 em `laco/catalogo/ambiguos.json`.

## As 5 etapas

1. **Limpar (sem modelo).**
   - O Tear decide os 298 ambíguos em `laco/catalogo/decisoes.jsonl`, e depois roda `python juntador.py --agora`.
     Atenção: com `parar` gravado, o juntador sai sem fechar a onda. Para só rejuntar, é preciso um modo novo ou
     rodar `juntar_tudo()` direto.
   - Reconferir devagar as 1016 URLs bloqueadas (`verificar_urls.py` com pausa entre pedidos; hoje ele não repete
     URL já conferida, então os 429 precisam sair de `verificacao/urls.json` antes).
   - Um script baixa o README bruto de cada item com repositório vivo no GitHub (fonte primária) e monta o cartão
     do item.
2. **Triagem.**
   - Cada item recebe o seu README e responde num esquema fixo:
     - serve para a busca do hub, para outra parte da stack do hub, ou para nada;
     - as colunas do catálogo que o README responde: lugar, mecanismo, MCP, Windows, pt-BR, licença e maturidade.
   - **Metade dos itens** vai ao FreeLLMAPI, pelo laço com outro prompt, a 2 modelos de famílias diferentes.
   - **A outra metade** vai a subagentes Haiku 5.5, disparados por um agente no Maestri, em paralelo na casa das
     dezenas. Cada subagente grava no mesmo formato e devolve só "ok".
   - A divisão por sorteio permite comparar as duas metades: concordância, custo e tempo.
3. **Conferência.**
   - Um agente no Maestri dispara uns 30 subagentes Sonnet 5.5, que conferem contra o README só os itens que a
     triagem marcou como úteis e aqueles em que os avaliadores discordaram ou tiveram dúvida.
   - Antes, um piloto com 1 subagente e 10 itens mede os tokens de verdade, e o maestro diz o custo ao Gustavo antes
     de soltar os 30.
4. **Auditoria:** o Opus confere uma amostra de 10% do que o Sonnet marcou.
5. **Síntese:**
   - o mapa de lugares × mecanismos;
   - as combinações leves e robustas, com o que falta montar em cada uma;
   - um capítulo à parte para o que serve à stack do hub além da busca;
   - o Designer faz a página.

## Regras que valem (memória da frente)

- Pesquisa pesada pelo FreeLLMAPI. Agente ou subagente Claude só com o custo dito antes e o aval do Gustavo.
- Orçar cota antes de qualquer bateria de chamadas.
- Estimar com fonte primária, e dimensionar o paralelismo pelo que a ferramenta aguenta.
- Processos longos rodam fora do Claude Code (`Start-Process`), porque o limpador de memória do Claude Code mata
  processos em segundo plano.
