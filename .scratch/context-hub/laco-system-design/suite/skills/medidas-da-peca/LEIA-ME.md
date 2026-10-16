# Medidas da peça: origem e uso

Skill nossa, escrita em 2026-10-15 para a suíte de design do laço "System design: a cidade nova" (especificação em
`laco-system-design/suite/categorias-v2.md`, "As duas skills nossas"). Papel: QA tester.

## Arquivos

| Arquivo | Origem | O que faz |
|---|---|---|
| `SKILL.md` | nosso | quando usar, como rodar, como ler |
| `medir.html` + `medir.js` | nosso | carregam a peça num iframe da mesma origem e medem no navegador; JSON em `<pre id="medidas">` |
| `rodar.ps1` | nosso | sobe o servidor local, roda o Edge sem cabeça por largura (`--dump-dom` e `--screenshot`), roda `links.mjs`, grava em `qa/` |
| `links.mjs` | nosso | confere `href`, `src`, `srcset`, `xlink:href` e `url()` da peça no servidor local; externos só listados |
| `contraste/check_contrast.py` | cópia sem alteração | conta de contraste WCAG para pares de cores |
| `contraste/LICENSE` | cópia | licença MIT do tastemaker |
| `teste/` | saída do teste | uma rodada em `prototipos/prototipo-09-roteamento-da-pesquisa.html`, 320 e 1280 px |

`check_contrast.py`: `codeswithroh/tastemaker`, `skills/tastemaker/scripts/check_contrast.py`, commit
`792a28a820ec4e9159ef8621c21a6c88528bbf2e` (HEAD em 2026-10-15, por `git ls-remote`), MIT, copyright 2026
codeswithroh. Lido inteiro antes de copiar: cálculo puro, só `sys`, sem rede e sem escrita. O `medir.js` repete a
mesma conta (limiar 0.03928, pesos 0.2126, 0.7152 e 0.0722); conferido em três pares do teste (1.92, 2.37 e 2.52
iguais nos dois).

## Como funciona o servidor

`rodar.ps1` sobe `python -m http.server`-equivalente (código Python escrito no próprio `rodar.ps1`, passado em
base64 só para o transporte), preso a `127.0.0.1` numa porta livre. Serve a pasta `-Raiz` e, em `/__medidas/`, só
`medir.html` e `medir.js` desta pasta. A mesma origem é o que deixa o `medir.js` ler o DOM da peça. O servidor e o
Edge são encerrados pelo PID e pelo perfil temporário ao fim, mesmo com erro.

## Regras de uso

- Saída só em `qa/` da pasta do papel; o script recusa gravar na pasta da peça ou na raiz servida.
- Sem rede além de `127.0.0.1`; `links.mjs` recusa outro host e nunca acessa link externo.
- Sem tocar na peça: o único efeito é focar e desfocar cada focável para ver se ele muda de aparência.
- Um Edge por vez, perfil temporário próprio, encerrado só pelo perfil. Nunca matar `msedge` pelo nome.
- Sem mouse e sem teclado.

## Limites conhecidos

- No modo adivinhado (peça sem `data-*`), "itens" são as caixas e círculos SVG que não contêm outra forma; uma
  grade de células conta como muitos itens (no teste, as células da matriz de 20 x 20 deram a menor folga). Marque a
  peça para medir só o que importa.
- Cruzamentos em curva são aproximados (amostra a cada 3 px): saem como "suspeita".
- Contraste de texto HTML sobe pelos fundos dos ancestrais; um elemento posicionado por cima, fora dessa linha, não
  é visto. Texto SVG procura a forma pintada antes dele sob o centro do texto.
- "Muda ao focar" usa foco por script (`el.focus`), que pode não acionar `:focus-visible` como o Tab acionaria.
- Tempos com tempo virtual do Edge sem cabeça: comparativos, não reais.

## Alterações

- 2026-10-15 (maestro, depois da porta da volta 1): o foco por script (`el.focus`) não aciona `:focus-visible`, e os
  três conceitos da volta 1 saíram como "sem mudança ao focar" quando o foco aparecia com Tab real. Agora `medir.js`
  procura regras `:focus`/`:focus-visible` no CSS que valem para o elemento; quem tem regra e não mudou vai para
  `nao_verificado_focus_visible`. Na volta 2 não pegou regra posta num filho (`.bairro:focus-visible .zona`); corrigido para tomar o seletor até a pseudo-classe de foco.
- 2026-10-15, volta 3: mesmo com a correção, a medição seguiu com `regra_de_foco_no_css: false` nos 10 itens, com a
  regra `.bairro:hover .zona,.bairro:focus-visible .zona` na peça. Causa **não investigada** (suspeitas: cache do Edge
  ou leitura das folhas de estilo dentro do iframe). Pendência: trocar o foco por script por Tab real via
  `--remote-debugging-port` e comparar os pixels da caixa do item antes e depois (sugestão do UX revisor). Até lá, o
  foco visível é do UX revisor, com Tab real.
