# Brief do ticket 53 (par B, lenovo-ideapad, 2026-10-24)

Você é o **Malho**, construtor do par B. Quem te chama é o maestro do par B ("Claude Code" no canvas). O Gustavo
invocou `/implement 53` em 2026-10-24.

## O trabalho

- Ticket: `C:/Projetos/context-hub/.scratch/construcao-do-hub/issues/53-clone-do-fork-com-submodulo.md`. Leia inteiro.
  Contexto do achado: `C:/Projetos/context-hub/.scratch/context-hub/retomada-maestro-par-b.md`, recado de 2026-10-21
  ~13h25 e diário de 13:22.
- Regras: `C:/Projetos/context-hub/.scratch/construcao-do-hub/etapas/regras-da-construcao.md`, com as diferenças
  abaixo. Comando da suíte e jeito de rodar: `etapas/juntar-tickets.md` (só leia; aqui não há integrador).

## Diferenças do par B (valem sobre as regras)

- **`C:/context-hub` é o hub ao vivo** desta máquina: replica para o par A pelo LiveSync. **Nunca edite, crie ou
  apague nada nele**, nem rode `git checkout`, `reset`, `stash` ou `merge` lá. Só leitura.
- Não há `integracao` aqui. Worktree a partir do `main`, fora do vault:
  `git -C C:/context-hub worktree add C:/context-hub-wt/ticket-53 -b ticket-53 main`.
- Você é o único construtor nesta máquina: a trava pesada não se aplica. Mesmo assim, só um trabalho pesado por vez
  (o note é um i5-8250U).
- **Não toque no par que está rodando:** contêiner `hub-banco`, daemon do CLI (`C:/hub-par/livesync`, `cli-db`), MCP
  do banco nas portas 8796-8798, busca em 3939, tarefas `hub-sincronizador` e `hub-vigia`, fork em
  `C:/Projetos/hub-mcp-banco`. Teste do passo 05 só com hub, fork e portas de ensaio, como os testes existentes fazem.
- Não junte no `main` e não faça `push` do hub. Pare com o ramo `ticket-53` pronto e revisado; a junção é decisão
  do maestro com o Gustavo.
- O roteiro do par B (`C:/Projetos/context-hub/.scratch/context-hub/instalacao-par-b.md`, passo 2) mora no
  repositório de planejamento: edite, mas **não faça commit** nele; o git do planejamento é do maestro.

## Como

1. Status do ticket para `claimed`; comentário com data e hora.
2. Skill `tdd`: primeiro o teste que falha (fork sem o submódulo dá erro claro, com a saída do `npm run build`, e não
   só "build do fork falhou"). Rode o arquivo de teste sozinho, sempre.
3. Conserto no passo 05 (`mcp-banco.psm1` e o que mais for preciso), no guia `agents/code/docs/instalacao.md` (na
   worktree) e no roteiro do par B.
4. No fim: a suíte inteira uma vez; depois a skill `code-review` sobre o ramo (desde `main`); conserte o que ela achar
   de verdade.
5. Relatório em `C:/Projetos/context-hub/.scratch/construcao-do-hub/etapas/relatorio-53-clone-do-fork-com-submodulo.md`
   (o que mudou, testes com números, o que ficou de fora) e comentário no ticket. Avise o maestro:
   `maestri ask "Claude Code" "53 pronto: ..."` (caminhos com `/`, nunca `\`).

## Estado e contexto

- Sua retomada: `C:/Projetos/context-hub/.scratch/construcao-do-hub/etapas/retomada-Malho.md`, atualizada a cada
  passo (um `/clear` não pode perder nada).
- Acima de 40% de contexto: no próximo ponto seguro, grave a retomada e avise o maestro com "salvo para limpar".
- Dúvida que não está escrita: pergunte ao maestro; não invente.
