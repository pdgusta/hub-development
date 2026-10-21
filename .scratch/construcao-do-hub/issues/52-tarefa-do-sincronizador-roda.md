# 52: A tarefa hub-sincronizador roda de verdade

Type: task
Status: ready-for-agent
Etapa: conserto do 26 (fora da sequência; vale para o par B)
Blocked by: nenhum

**What to build:** Achado de 2026-10-21 no par A: a tarefa `hub-sincronizador` nunca rodou (LastRunTime 1999). O XML
escrito por `agents/code/kit/par/banco/banco.psm1` (por volta da linha 405) chama `<Command>pwsh.exe</Command>`; aqui o
`pwsh.exe` alcançável é o atalho da Store (WindowsApps), e o Agendador devolve 0x80070002 (arquivo não encontrado).
Sem a tarefa, nada religa o CLI do LiveSync se ele cair. A `hub-vigia` (`10-manutencao.ps1`, `conhost` + node) roda.
Consertar para que a ação aponte para um executável que o Agendador acha (por exemplo, o caminho completo do pwsh
resolvido na instalação), com teste do XML gerado. Reaplicar no par A é com o maestro e o Gustavo depois da junção.

- [ ] teste que falha antes: o XML gerado não depende do PATH nem do atalho da Store
- [ ] conserto; o mesmo teste verde
- [ ] a suíte segue verde
- [ ] relatório diz como reaplicar a tarefa num par já instalado

## Comments

- 2026-10-21 (maestro): publicado. Dona: a Brasa, depois do 51. Revisão: o Fiel.
