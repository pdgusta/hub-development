# Brief do ticket 54 (par B, lenovo-ideapad, 2026-10-24)

Para o **Malho**, depois do 53. O Gustavo invocou `/implement 54` em 2026-10-24. Valem todas as regras e as
"Diferenças do par B" de `etapas/brief-53-par-b.md` (hub ao vivo só leitura, par rodando intocado, sem junção nem
push, roteiro do par B sem commit, retomada e 40%).

## O trabalho

- Ticket: `C:/Projetos/context-hub/.scratch/construcao-do-hub/issues/54-busca-dentro-do-vault-pesa-no-cli.md`. Leia
  inteiro, com a pesquisa e a **decisão (caminho A)**: a busca sai do vault para `C:/hub-par/busca`, ao lado de
  `banco`, `cli-db` e `livesync`, por uma chave nova no `.env` (sugestão `HUB_BUSCA_DIR`; o nome final é seu, com a
  razão no relatório). O CLI do LiveSync não muda.
- Worktree: se o 53 ainda não foi juntado, parta do ramo `ticket-53` (os dois mexem em `instalacao.md`):
  `git -C C:/context-hub worktree add C:/context-hub-wt/ticket-54 -b ticket-54 ticket-53`. Diga no relatório de qual
  ponta partiu.
- Quem usa o caminho hoje (lista da pesquisa, não conferida linha a linha): `kit/par/03-busca.ps1`,
  `skills/busca/iniciar.ps1` (pacote e `XDG_CACHE_HOME`), `skills/busca/relatorio.mjs`, `skills/busca/SKILL.md`,
  `kit/cliente/ligar-cliente.ps1`, `kit/par/proxy/proxy.psm1`, `kit/par/08-harnesses.mjs`, `env/*.env.modelo`, o teste
  `12-kit-busca` e as docs (`busca.md`, `kit-de-par.md`, `instalacao.md`, `operacao.md`). Varra de novo; o resto de
  `.local` (vigia, guardas, exclusões, `par.json`...) fica onde está.
- **Par já instalado** (A e B têm a busca em `.local/busca`): o kit precisa de um caminho para mudar de lugar sem
  reinstalar do zero (por exemplo, o 03 rodado de novo move a instalação e o índice em `estado`), e o `desfazer`
  continua funcionando. Descreva o comando no guia.
- Teste que falha antes: depois do 03, nada da busca dentro do vault (`.local/busca` ausente) e a busca sobe pelo
  caminho novo. Hub de ensaio, nunca o ao vivo.

## Fora da construção (fica com o maestro)

- Aplicar a mudança nos dois pares que estão rodando e a medida no A antes e depois (último item do ticket): só
  depois da junção, com o Gustavo. Deixe no relatório os comandos exatos para isso.

## Como

Igual ao 53: `claimed` no ticket; `tdd`; arquivo de teste sozinho a cada passo; suíte inteira uma vez no fim;
`code-review` sobre o ramo (desde a ponta de onde partiu); relatório em
`etapas/relatorio-54-busca-fora-do-vault.md`; comentário no ticket; `maestri ask "Claude Code" "54 pronto: ..."`.
