# Brief da porta da amostra, volta 3 (a última)

Do maestro, 2026-10-15. Peça: `amostra/amostra.html` (volta 3), com `amostra/consertos.md` (seção "Volta 3"),
`amostra/decisoes.md` (20 a 22) e a volta 2 em `amostra/amostra-v2.html`. Contexto e critério: `portas/amostra-1/brief.md`.
Resultado da volta 2: `portas/amostra-2/resultado.md`. Esta volta trata só do toque e de acabamento; o conteúdo já
passou duas vezes.

## Ordem

1. **QA tester**, em `qa/amostra-3/` (relatório `qa/amostra-3/relatorio.md`), com **entrada real do navegador**: o
   arrasto com um dedo nos mesmos alvos e percurso que mostraram a regressão na volta 2 (tem de seguir até o fim); e de
   novo, para garantir que nada voltou: toque simples abre ficha e botão, nenhum clique depois do arrasto, pinça → um
   dedo sem salto, cancelamento, três arrastos seguidos com o botão direito, + e − no centro, Ver tudo e 0 em 320, Tab
   23/23. Mais as medidas nas quatro larguras e os sete cenários, e o cabeçalho a 1280 x 720 e a fileira de cenários a
   960.
2. Com o relatório do QA, em paralelo:
   - **Prumo:** o bloqueio da volta 2 e a ressalva da ficha, no código. Parecer em `portas/amostra-3/prumo.md`.
   - **UX revisor:** só os dois menores da volta 2 (cabeçalho a 1280 x 720, fileira a 960) e qualquer problema novo.
     Parecer em `portas/amostra-3/ux-revisor.md`.
   - **Tech lead:** confere que o conteúdo segue igual. Parecer curto em `portas/amostra-3/tech-lead.md`.

Passa com os três aprovando. É a última volta: se não passar, o laço para e espera o Gustavo. Cada um avisa:
`maestri ask "Claude Code" "pronto: <caminho>"`.
