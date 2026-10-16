# Brief da amostra, volta 2

Do maestro ao UI engineer, 2026-10-15. **Você recebeu /clear:** leia primeiro `amostra/retomada-ui-engineer.md` (o seu
contexto salvo; os geradores estão em `amostra/fontes/`), depois `amostra/brief.md` (o pedido da amostra) e
`portas/amostra-1/resultado.md`.

A porta da volta 1 devolveu a amostra pelo canvas. O conteúdo passou (o Tech lead aprovou: idêntico à mistura aprovada).
Aplique em `amostra/amostra.html` (guarde a volta 1 como `amostra-v1.html`):

1. `portas/amostra-1/prumo.md`, "Consertos para a próxima volta": os **3 bloqueios** (toque simples ativa fichas e
   botões, com captura só depois de distinguir arrasto; referência do gesto refeita ao passar de dois dedos para um, com a
   mesma limpeza no cancelamento e na perda de captura; "Ver tudo" e a tecla `0` enquadram a cidade inteira também em
   320 px, separados da abertura em 75%) e os 3 recomendados.
2. `portas/amostra-1/ux-revisor.md`, "Consertos" (8): o salto a partir do segundo arrasto com o botão direito (a
   reprodução está no parecer; confira com entrada real do navegador, não com eventos montados), + e − em volta do
   centro, sem seleção de texto no arrasto, o cabeçalho a 960 px, a vista inicial fora do canto dos botões de zoom, as
   linhas coladas ou cortando nomes e o respiro das etiquetas. O arrasto esquerdo que também anda (item 3, "opcional, se
   o Gustavo quiser") fica **fora** por ora.
3. `portas/amostra-1/tech-lead.md`: o conserto opcional, se não criar problema.

Se dois consertos se contradizem, anote a escolha em `decisoes.md`. Registre em `consertos.md` (crie em `amostra/`) uma
linha por conserto: feito, feito de outro jeito, não feito e por quê. Atualize o `retomada-ui-engineer.md` no fim.

Ao terminar: `maestri ask "Claude Code" "pronto: <caminho>"`.
