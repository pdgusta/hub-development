# Brief da amostra, volta 3 (a última)

Do maestro ao UI engineer, 2026-10-15. Se chegar sem memória, leia antes `amostra/retomada-ui-engineer.md`. Resultado
da volta 2: `portas/amostra-2/resultado.md`. O conteúdo passou duas vezes (Tech lead) e o UX revisor passou: esta volta é
só o toque e acabamento. Guarde a volta 2 como `amostra-v2.html`.

1. **Bloqueio (Prumo, `portas/amostra-2/prumo.md`, conserto 1):** o arrasto com um dedo anda 12 px e para, porque o
   `lostpointercapture` de um descendente encerra o gesto. Distinga transferência de captura de encerramento; o arrasto
   de um dedo segue por todo o percurso, preservando o toque simples (abre ficha e botão), a supressão do clique depois
   do arrasto, a pinça → um dedo e o cancelamento. Reproduza antes com entrada real do navegador, nos alvos e no percurso
   do QA (`qa/amostra-2/relatorio.md`), e confira depois do mesmo jeito.
2. **Documentação (Prumo, conserto 3):** corrija em `amostra.md` e `consertos.md` a afirmação de que o arrasto de um dedo
   funcionava; registre a correção e a evidência nova, preservando o histórico.
3. **Ressalva (Prumo):** a modalidade da ficha acompanha a largura enquanto ela está aberta, preservando o foco; ou, se
   ficar fixa de propósito, registre a exceção à decisão 18.
4. **Menores (UX revisor, `portas/amostra-2/ux-revisor.md`):** o cabeçalho a 1280 x 720 (hoje 185 px: a legenda recolher
   também pela altura) e a fileira de cenários a 960 que corta um botão sem aviso (sinal de que há mais à direita).

Registre em `consertos.md` (seção "volta 3"). Atualize o `retomada-ui-engineer.md` no fim.
Ao terminar: `maestri ask "Claude Code" "pronto: <caminho>"`.
