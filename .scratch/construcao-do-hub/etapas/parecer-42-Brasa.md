# Parecer do ticket 42 (Brasa): o mod do fim da resposta reconhece o hub aberto pelo atalho

## Rodada 1 — 2026-10-17 ~14h10 (Fiel sozinho; Fielzinho sem cota até 17h15, leitura pendente)

Ramo `ticket-42`, 363e733 (de `integracao` e7203b4; merge com a ponta de agora, limpo). **Veredito: PASSA** com 1
ressalva.

- `register.ts`: `dentro` compara pelo texto e, se não bate, pelo `realPath` dos dois (`$.fs.stat(p, { resolve:
  true })`); caminho que não resolve conta como fora; sem processo fora do hub.
- API conferida no tipo do motor deste build (`claude-code.d.ts`, `FsStat.realPath` e `FsStatOptions.resolve`): o
  `realPath` vem só com `resolve: true` e fica ausente quando o caminho não leva a lugar nenhum, como o mod espera.
- Fiel: `claude plugin test .` 3/3 (atalho, direto, fora); `claude plugin validate .` passa (avisos de antes);
  `27-*` e o detector 43/43; `git status` limpo.

Ressalva: o teste responde o `fs.stat` pelo dublê, e a doc do motor fala em "symbolic link followed"; se o
`realPath` também atravessa uma **junction** (o atalho do hub) só se vê com o Claude Code de verdade aberto no atalho
(não rodado; declarado no relatório). Vale uma rodada real pela fila quando houver cota e trava.
