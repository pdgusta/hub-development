# Retomada do Nanquim (Designer da peça 2)

Estado (2026-10-17 ~22h45): **peça 2 passou** (Esquadro, volta 2; parecer-peca-2.md). Parado; o maestro chama se o
Gustavo pedir ajuste.

- Página: `peca-2-rio-estreito.html` ("O rio estreito": rio vertical, largura = memória livre; barcos = trava;
  ✕ = encalhe; pedras e pontes = achados; placas = regras do Gustavo; marcos = decisões do maestro; afluente = Codex).
- Para mudar: edite `modelo-peca-2.html` (motor) ou `montar-peca-2.py` (fatos, rótulos curtos, ajustes de hora com
  fonte) e rode `python montar-peca-2.py` nesta pasta (gera `fatos-peca-2.json` e a página). Dados brutos:
  `dados-memoria-trava.json`, `dados-achados.json`.
- Conferência: `python -m http.server 8773 --bind 127.0.0.1` nesta pasta; 390 px por `_moldura-390.html`;
  `#cartao=<id do achado>` abre um cartão. Edge sem cabeça com perfil `%TEMP%\edge-nanquim`.
- Ressalvas abertas (não obrigam): no 390, rótulos até ~1 h abaixo da marca nas horas cheias; dois trechos curtos da
  trava sem início e fim nas fontes (12-busca dos docs ~12h55; junção dos docs 12h37).
