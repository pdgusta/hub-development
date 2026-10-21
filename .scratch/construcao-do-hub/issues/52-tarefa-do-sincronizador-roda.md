# 52: A tarefa hub-sincronizador roda de verdade

Type: task
Status: resolved
Etapa: conserto do 26 (fora da sequência; vale para o par B)
Blocked by: nenhum

**What to build:** Achado de 2026-10-21 no par A: a tarefa `hub-sincronizador` nunca rodou (LastRunTime 1999). O XML
escrito por `agents/code/kit/par/banco/banco.psm1` (por volta da linha 405) chama `<Command>pwsh.exe</Command>`; aqui o
`pwsh.exe` alcançável é o atalho da Store (WindowsApps), e o Agendador devolve 0x80070002 (arquivo não encontrado).
Sem a tarefa, nada religa o CLI do LiveSync se ele cair. A `hub-vigia` (`10-manutencao.ps1`, `conhost` + node) roda.
Consertar para que a ação aponte para um executável que o Agendador acha (por exemplo, o caminho completo do pwsh
resolvido na instalação), com teste do XML gerado. Reaplicar no par A é com o maestro e o Gustavo depois da junção.

- [x] teste que falha antes: o XML gerado não depende do PATH nem do atalho da Store
- [x] conserto; o mesmo teste verde
- [ ] a suíte segue verde
- [x] relatório diz como reaplicar a tarefa num par já instalado

## Comments

- 2026-10-21 (maestro): publicado. Dona: a Brasa, depois do 51. Revisão: o Fiel.
- 2026-10-21 (Brasa): feito no ramo `ticket-52` (2903ab7). A ação da tarefa chama o pwsh.exe pelo caminho completo
  (`Get-ExecutavelPwsh`: o do MSI, senão o executável do pwsh que roda o kit; nunca o atalho da Store). Teste no
  `kit-sem-docker.ps1`, vermelho antes e verde depois; leves 28/28. Reaplicação e a ressalva do pwsh da Store
  (atualização troca a pasta) em `etapas/relatorio-52-tarefa-do-sincronizador.md`. Pedida a revisão ao Fiel.
- 2026-10-21 (Brasa): o Fiel PASSA com ressalvas (`etapas/parecer-52-Brasa.md`); as ressalvas do relatório (o MSI
  também está no par A, e a tarefa o usa; o shell da receita; o `.env` em `C:\hub-transporte\`) ajustadas. Para o
  Rebite: ramo `ticket-52` (2903ab7), leves 28/28 (Fiel 37/37). A suíte fica com ele.
- 2026-10-21 12:49 (integrador, Rebite): resolvido. Junção b506910 (ticket-52 2903ab7; parecer do Fiel PASSA com
  ressalvas, só no relatório, ajustado). Leves 07-kit-sem-docker, 38, 45-duas-maquinas-sem-docker,
  46-kit-duas-maquinas (com os do 51): 69/69. Suíte com --test-concurrency=1 e trava em b506910: 391, 376 verdes, 15
  pulados, 0 falhas, git limpo (log etapas/logs/juncao-51-52-suite.log). Pendente fora do integrador: reaplicar a
  tarefa no par A (maestro e Gustavo; receita no relatório).
