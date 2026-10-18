---
name: headless-edge-para-qa-visual
description: "O painel de navegador embutido trava screenshots e congela o requestAnimationFrame; para revisar páginas animadas, renderizar com o Edge headless servindo o arquivo por http.server local"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a8562ee9-94be-4d53-81d8-74e57b69f06b
  modified: 2026-10-16T19:23:01.986Z
---

No painel de navegador do app, `requestAnimationFrame` quase não avança (o ticker do GSAP ficou em 0,4 s depois de
20 s) e os screenshots expiram quando a janela está em segundo plano. O `javascript_tool` continua funcionando, e
áudio toca. O painel também não abre `file://` fora da pasta do projeto, só `http://localhost`.

**Why:** fluxo de player que depende de GSAP ticker (delayedCall, fades) nunca termina nesse painel; a verificação
visual por screenshot não é confiável lá.

**How to apply:** servir a pasta com `python -m http.server 8765 --bind 127.0.0.1` e renderizar quadros com
`msedge.exe --headless=new --disable-gpu --user-data-dir=<perfil único por captura> --window-size=1200,675
--virtual-time-budget=6000 --screenshot=<png> <url&v=timestamp>`; esperar o PNG aparecer (o processo volta antes de
gravar) e matar os msedge do perfil depois. **Matar só pelo perfil:** filtrar `Win32_Process` de `msedge.exe` pela
linha de comando com o `--user-data-dir` único; nunca `taskkill /IM msedge.exe`, por título de janela ou "todos" (o
Edge do Gustavo fica intocado; regra do maestro em 2026-10-14 depois de um subagente fazer um taskkill largo), e
repetir a regra em todo brief de subagente que capture com o Edge. Montar folhas 2x2 com ffmpeg hstack/vstack. Fluxo de player: usar
setTimeout e classes CSS, nunca o ticker, para avançar cenas. Ver [[gemini-tts-interactions-api]].

**Celular (390 px):** o Edge sem cabeça não desce de 492 px de largura (`innerWidth` medido em 2026-10-16), então
`--window-size=390,...` dá uma captura falsa, cortada na direita. Para 390 de verdade: uma moldura HTML com
`<iframe style="width:390px;height:14000px">` apontando para a página, captura em `--window-size=492,14000` e recorte
dos 390 px da esquerda (PIL). Fundo com textura engana o recorte automático do fim da página: conferir as telas.

**Vídeo (MP4):** `puppeteer.launch` com o msedge falha ("Failed to launch the browser process"); o que funciona é
spawnar `msedge --headless=new --remote-debugging-port=9333 --user-data-dir=<perfil>` e `puppeteer.connect`
(`puppeteer-core@23.11.1`, instalado com npm no scratchpad). Com a página em modo export (`?export=1`, função
`Player.renderAt(T)`), um `page.screenshot` JPEG 1600x900 leva cerca de 120 ms por quadro, entubado no ffmpeg
(`image2pipe`, libx264 crf 18); a narração entra depois com `adelay` por cena e `amix normalize=0`.

**Armadilhas do motor (vídeo 2, 2026-10-10):** em elementos `H.word`/`H.counter` (posicionados por `gsap x/y`), um tween
`{y:16}→{y:0}` manda o elemento para o topo da tela; animar `y` com o valor absoluto. `scaleY` com `svgOrigin` em
paths deixou barras deslocadas no seek: usar subida + opacidade. Legendas e frase-síntese só não colidem com a
legenda a 22 px do rodapé (25 px) e a frase em y ≤ 712. Render do MP4 em 3 workers (portas 9340+) em cerca de
um terço do tempo.
