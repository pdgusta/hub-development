# Ticket 09 — Cinzel — parecer do Fiel — rodada 1

2026-10-17 ~05h10. Fork `C:/Projetos/hub-mcp-banco`, ramo ticket-09, 61a6e70 (base v0.10.0 1a4d53f); hub worktree
`C:/context-hub-wt/ticket-09`, 3d9d0bb (contém integracao 33b817a). Fiel sozinho (Fielzinho sem cota até 06h58;
leitura dele pendente).

## Veredito: VOLTA (3 consertos, já feitos nos ramos `ticket-09-conserto` e conferidos com Docker)

A regra "só é conflito se a base não é mais versão viva" está certa em sequência: reler e regravar grava e avisa que
o conflito segue aberto (sem ela, o aceite entraria em laço). O furo é a simultaneidade.

## Consertos
1. **Duas gravações ao mesmo tempo da mesma base respondem as duas "Note saved"** (Fiel). `vault.ts` `writeVersioned`
   lê `before` antes de gravar, sem serializar; as duas veem a base viva e o `outcome` diz `saved` com
   `openConflict`, como se o conflito fosse antigo. Sonda (`etapas/logs/sonda-09-fiel.e2e.test.ts`, `Promise.all` de
   dois `write_note` com a mesma `base_rev`) contra o CouchDB do e2e: no ramo ticket-09, `SONDA A => Note saved`,
   `SONDA B => Note saved`, 2 folhas (`logs/revisao-09-r1-fork.log`). Nada se perde, mas nenhum dos dois ouve
   "conflito: releia e refaça".
   Conserto (d2a5a40): também é conflito quando aparece uma folha que não estava em `before` e não é a sua. Sonda
   no conserto: `A => Note saved`, `B => conflito: releia e refaça` (`logs/revisao-09-conserto-fork.log`).
2. **`move_note` com conflito na origem não dizia que o destino já foi gravado** (Fiel). Conserto (d2a5a40): a
   resposta acrescenta "`<to>` já foi gravada ...; `<from>` não foi apagada".
3. **Passo 05 com o MCP de pé não religava depois de remontar o build** (Fiel): o código velho seguia rodando.
   Conserto (hub ca17738): religa quando o build é mais novo que o processo; caso novo no teste B: `com build novo, o
   passo religa o MCP (PID 214236 -> 200752)`.

## Evidências do Fiel
- Hub sem Docker (`09-mcp-banco-sem-docker.test.mjs`): 1/1 (12 casos).
- Docker com a trava (05h02–05h05): fork ticket-09 + sonda 14/14 (sonda mostra o furo 1); fork conserto-09 + sonda
  16/16 (os 12, os 2 novos e as 2 sondas); hub conserto-09 com `HUB_MCP_BANCO_DIR` no fork conserto-09: 21 PASSA,
  0 FALHA, "ticket 09: tudo passou" (`logs/revisao-09-conserto-hub.log`). Sem contêiner sobrando.
- Sonda extra: apagar com a base e recriar sem base grava como nota nova (`3-...`), sem recusa.

## Ressalvas (não bloqueiam)
1. Na corrida, quem grava primeiro ainda pode ouvir "saved" se conferir antes de a outra folha chegar; só quem chega
   depois ouve conflito. A próxima leitura de qualquer um mostra o CONFLITO. Aceitável.
2. Folha que chega pela replicação do outro par entre a leitura e a gravação também vira "conflito" para esta
   gravação: conservador, certo.
3. As do relatório: fusão automática do LiveSync em linhas diferentes (caso 4b), compactação do CouchDB e banco
   recriado ficam como pontos abertos da faixa 5.

## Rodada 2 (curta)
Levar `ticket-09-conserto` ao `ticket-09` nos dois repositórios. O Fiel confere que a árvore é a do conserto já
testado; sem Docker de novo se for idêntica.

# Rodada 2 (curta) — Fiel — 2026-10-17 ~05h15

## Veredito: PASSA

- Fast-forward conferido: fork `ticket-09` = d2a5a40, hub `ticket-09` = ca17738, as mesmas pontas que rodaram no
  Docker da rodada 1 (fork 16/16 com a sonda; hub 21 PASSA). Sem Docker de novo.
- Hub sem Docker: 1/1. Árvore do hub limpa. No fork, só o `package-lock.json` modificado, como no relatório (fora dos
  commits).
- `integracao` andou (ea6f353, junta do 28) e o ramo não a contém. `git merge-tree` junta sem conflito; o 28 não toca
  no banco nem no kit do MCP. O Rebite junta e roda a suíte.
- Ressalvas da rodada 1 seguem. A leitura do Fielzinho fica pendente (cota até 06h58).
