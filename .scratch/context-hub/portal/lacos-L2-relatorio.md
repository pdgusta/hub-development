# Laços, marco L2 (núcleo): relatório para revisão (2026-10-14)

Construído por subagente do Designer; conferido pelo Designer. Contrato: `proposta.md` §4.4–§4.5 e Anexo A (L1
aprovado, `revisao-lacos-L1.md`). Sem tela (é o L3).

## Testes (rodados pelo Designer)

- Núcleo: **206 OK em três rodadas seguidas** (eram 135; 69 de `teste_lacos.py` + 2 da correção abaixo).
  `python -m unittest discover -s nucleo/testes -t nucleo/testes -p "teste_*.py"`, ~85 s.
- Projeto real: **6 OK** (eram 4): os dois exemplos do Anexo A passam no validador sem aviso; as pastas reais num
  `lacos.json` temporário são lidas só para leitura; `/carta/system-design/laco/config.json` agora dá 404.
- Instabilidade achada e corrigida: em 2 de 8 rodadas, 1 erro `PermissionError [WinError 5]` no `os.replace` de
  `caixa/.avisos.json`. Causa verificada: no Windows, um leitor com o destino aberto barra o `os.replace`
  (reproduzido à parte). Correção: `caixa._trocar` tenta de novo por até ~1 s (20 × 50 ms), só em
  `PermissionError`; testes `teste_caixa.TrocaComDestinoAberto` (leitor segurando o arquivo por 0,2 s → a gravação
  conclui; acesso negado persistente → ainda levanta). Pode ser também a causa do erro isolado anotado no marco 7.
  Antes da correção o subagente viu uma vez `Seguranca.test_post_sem_origin_ou_x_torre_ou_tipo_403` com ERROR, sem
  repetir; causa não confirmada.

## Arquivos (em `portal/`)

- `nucleo/lacos.py` (novo): leitor (`laco.json` + fontes de estado, só leitura), revisão, situação e grupo,
  configurado × em uso, pedidos com recibo validado, validação do envio `alteracao-laco`.
- `nucleo/leitores.py`: chave opcional `lacos` no `projeto.json`, leitura do `lacos.json`, versão (só `lacos.json` e
  cada `laco.json`), tipo novo na caixa, regra de entrega por tipo.
- `nucleo/caixa.py`: nome/slug e `.md` de `alteracao-laco` com as chaves de desfecho vazias; `_trocar` (acima).
- `nucleo/aviso.py`: linha "alteração de laço", instrução com "§4.5"; entrega marcada por qualquer estado válido
  diferente de `nova` (estado desconhecido não marca).
- `nucleo/torre.py`: `GET /api/lacos`, `GET /api/laco/<id>`, envio pelo `POST /api/caixa`, problemas dos laços no
  estado, bloqueio das fontes dos laços em `/carta`.
- `nucleo/LEIA.md`; testes `teste_lacos.py` (novo), `apoio.py` (cópia "avivada", `MENSAGENS_DA_FIXTURE`), contagens
  em `teste_caixa.py`/`teste_torre.py`; fixture `horta/lacos/regas` (em voo, SQLite) e `horta/lacos/sementes`
  (terminado, `laco_final.json`), `horta/portal/lacos.json`, chave `lacos` no `projeto.json` da fixture, dois
  pedidos na caixa da fixture (aplicado aguardando efeito; comentário lido), `fixtures/LEIA.md`,
  `estado-esperado.json`; `testes-do-projeto/teste_projeto_real.py`.

`teste_lacos.py` cobre: os critérios do fim da §4.5; caminho (`..`, absoluto, unidade, componente com ponto,
atalho/junction para fora, `laco.json` atalho); SQLite `mode=ro`, `uri=True`, timeout 2 s, banco igual byte a
byte; o portal nunca grava na pasta do laço; situação e grupo; configurado × em uso; versão; os 400 e 409;
idempotência; `substitui`; recibos; aviso (emissor e vigia).

## Decisões de detalhe onde a spec era ambígua (leitura conservadora)

1. Problemas dos laços entram em `problemas` de `/api/estado` (registro, `laco.json` malformado ou com chave
   desconhecida, estado desconhecido, recibo inválido); para isso lê só descritores e caixa, nunca as fontes.
2. Obrigatórios no `laco.json`: formato, id, titulo, ticket, execucao, nos, ligacoes, controles, capacidades,
   contadores, sinal. Opcionais: `parado`, `esperando_cota`.
3. Laço malformado: `faixa`/`opcoes`/`itens` em tipo que não os usa; `onda_atual` para contador inexistente;
   origem com duas formas. Chave desconhecida só vira problema (também dentro de origem).
4. Caminho ruim em dois níveis: regra léxica → laço malformado; atalho/junction para fora → só aquela origem
   ilegível, com problema, sem ler.
5. Arquivo de origem ausente = ilegível (o `ausente` não vale para arquivo). NULL na coluna do SQLite = valor nulo.
6. Hora de uma fonte de sinal: o valor dela quando tem `formato`; senão, a hora do arquivo.
7. `definicao_mudou`: `true` quando o tipo difere ou o valor pedido não cabe na definição atual (só com o hash não
   se sabe se a regra mudou).
8. Ordem em `mudar-controle`: forma de antes/depois → configurado ilegível (409) → revisão (409) → tipo (400) →
   antes ≠ configurado (409) → valor (400) → nada muda (400).
9. Onda já passada: 400 `onda-invalida`.
10. `pedir-retomada` não confere se está pausado (o contrato não tem fonte); o maestro revalida.
11. `revisao` obrigatória (64 hex) em toda operação, mas só dá 409 em `mudar-controle`.
12. Instrução estendida do aviso só quando o aviso tem alteração de laço.
13. `pedidos_abertos`: pedidos da execução atual com trabalho pendente; exclui comentário lido, inclui estado
    desconhecido.
14. Conflito conta em "espera você" mesmo com recibo inválido.
15. Comentário em estado diferente de `nova`/`lida` = recibo inválido.
16. `aplicando_desde` também tem de ser ≥ `enviada`.
17. Linha malformada na lista: título = id, grupo em-voo, situação desconhecido, destaque e pedidos abertos nulos.
18. Retrato no `.json` na chave `laco`; em `mudar-controle` inclui `definicao` (o controle como declarado, com as
    origens). O `.md` ganha controle, configurado no envio, em uso no envio e precondições.
19. Fontes fora de `/carta`: antes, a carta mestra (`pasta` `.scratch/context-hub`) servia
    `/carta/system-design/laco/config.json` e o resto das pastas dos laços. Agora uma carta cuja pasta contém um laço
    registrado não serve nada de dentro dele; painéis cuja pasta fica dentro do laço continuam servidos.

## Laços reais

O maestro escreveu `laco-embeddings/laco.json`, `laco/laco.json`, `portal/lacos.json` e `"lacos": "lacos.json"` no
`projeto.json`. Lidos pelo leitor novo (só leitura, portal temporário): nenhum problema. Embeddings: em voo,
rodando, 4 925 tentativas, onda 6, aptos 88, fora 65; teto relido, demais controles "não confirmado". Ampla:
terminado, 7 382 tentativas. O portal real ainda roda o código antigo (reinício depois que a fila de avisos esvaziar).

## Pendências conhecidas

- Banco travado sem teste (timeout de 2 s por origem deixaria a suíte lenta); o código trata como ilegível.
- `GET /api/estado` agora relê registro, `laco.json` e caixa para os problemas (custo pequeno).
- Para o L3: a tela atual filtra os tipos conhecidos da caixa (mensagens de laço não a quebram); uma cópia da
  fixture só mostra o laço em voo como "rodando" depois de `apoio.avivar_laco(...)` (o sinal é a hora dos arquivos).
- As decisões acima ainda não estão na `proposta.md`; entram no estilo da §3.7 se o Prumo concordar.

## Correção dos três achados do Prumo (`revisao-lacos-L2.md`), para revisão dirigida

Conferido pelo Designer: **218 testes do núcleo OK em duas rodadas** (eram 206), **6 do projeto real OK**.
Casos do `review_l2.py` refeitos pelo subagente: painel na raiz `/carta/painel-regas/` e `/config.json` 200 → 404;
`ligacoes[0].de = []` → `/api/lacos` 500 → 200 com o laço malformado ("ligacoes[0].de precisa ser o id de um nó
(texto), não list") e o outro intacto, detalhe 422; faixa 0,49 + pedido 0,1 → 0,2 com hash velho → 409 com
`definicao_mudou: null` (era `false`).

1. **Painel (bloqueava):** `torre.py` chama `lacos.carta_pode_servir(projeto, pasta_real, alvo)`; `lacos.py` ganhou
   `arquivos_declarados` e `carta_pode_servir`. Carta cuja pasta é a raiz do laço ou o contém não serve nada de
   dentro dele (nem o HTML). Carta com pasta dentro do laço só serve se o laço está bem formado, o `laco.json` não
   está na pasta dela e nenhuma origem declarada está nela (bancos incluem `-wal`, `-shm`, `-journal`); laço
   malformado → painel 404; atalho para fonte cai fora da pasta → 404. Laços reais não declaram nada em `painel/`;
   `painel-mare`, `painel-sintese`, `painel-garimpo` continuam servidos. Testes `PainelDoLaco` (6) e no projeto
   real (painéis 200 com `dados.js`, `etapas.js`, `fontes/sintese.css`; subidas a `config.json`, `laco.json`,
   `estado/` 404; carta na raiz de `laco` 404 em tudo).
2. **Ids com tipo errado:** `_Validador.ref` confere texto antes de procurar (`ligacoes.de/para`, `controles.no`,
   `contadores.no`, `onda_atual`); POST com `no`/`controle` não texto → 400 `tipo-errado` com o campo. Sem `except`
   geral. Testes `DescritorComTipoErrado` (3: 11 campos × lista/objeto/número; varredura do descritor; POST).
   Varreduras fora da suíte: 5 620 casos no descritor, 430 nas fontes, 259 no POST, nenhuma exceção fora de
   `LacoMalformado`/`Recusa`.
3. **`definicao_mudou`:** no 409 de revisão, `true` só provado (tipo mudou ou valor pedido fora da definição atual),
   senão `null` ("a configuração ou a regra mudou; o portal não sabe qual"). No 409 de `antes` continua `false`
   (mesma revisão, e a definição entra no hash: provado). Proposta §4.5 (trecho do 409) ajustada. Testes novos para
   tipo, para mudança compatível (faixa, unidade, origem, releitura, outro controle → `null`) e para `antes`.

Decisões registradas na `proposta.md` §4.6 "Contrato fixado na construção do L2" (19 itens; 7, 10 e 19 com o texto
novo; robustez dos ids nos itens 3 e 12). `nucleo/LEIA.md`: só a frase da regra das cartas. Arquivos: `lacos.py`,
`torre.py`, `LEIA.md`, `teste_lacos.py` (81), `teste_projeto_real.py`, `proposta.md`.
