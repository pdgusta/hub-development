# Brief da porta da amostra, volta 2

Do maestro, 2026-10-15. Peça: `amostra/amostra.html` (volta 2), com `amostra/consertos.md` (uma linha por conserto pedido
na volta 1), `amostra/decisoes.md` (13 a 19 são desta volta) e a volta 1 em `amostra/amostra-v1.html`. Contexto, ordem e
critério: os mesmos de `portas/amostra-1/brief.md` (leia se chegar sem memória). Resultado da volta 1:
`portas/amostra-1/resultado.md`.

## Ordem

1. **QA tester** testa de novo, em `qa/amostra-2/` (relatório em `qa/amostra-2/relatorio.md`): as medidas nas quatro
   larguras e os sete cenários, e **a navegação do canvas com entrada real do navegador** (o protocolo do navegador, não
   eventos montados): dois e três arrastos seguidos com o botão direito (a vista não pode saltar), Ctrl + roda, Shift +
   roda, + e − em volta do centro, "Ver tudo" e a tecla `0` em 320 px, e o toque (toque simples abre ficha e botão; pinça
   e retirada de um dedo sem salto), se o navegador emular toque.
2. Em paralelo, com o relatório do QA, cada um confere primeiro os consertos que pediu na volta 1
   (`portas/amostra-1/<seu parecer>.md`) contra `amostra/consertos.md` e a peça (feito, feito de outro jeito, aceito ou
   não, faltando), depois só problema novo que um conserto criou:
   - **UX revisor:** com entrada real, o salto, o zoom no centro, a seleção de texto, o cabeçalho a 960 x 800 e a vista
     inicial. Parecer em `portas/amostra-2/ux-revisor.md`.
   - **Tech lead:** que os consertos não mudaram o conteúdo aprovado. Parecer em `portas/amostra-2/tech-lead.md`.
   - **Prumo:** os 3 bloqueios e os 3 recomendados no código. Parecer em `portas/amostra-2/prumo.md`.

Passa com os três aprovando. Esta é a volta 2 de 3. Cada um avisa: `maestri ask "Claude Code" "pronto: <caminho>"`.
