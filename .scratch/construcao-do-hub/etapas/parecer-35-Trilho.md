# Ticket 35 — Trilho — parecer do Fiel — rodada 1

2026-10-17 ~04h30. Ramo ticket-35, HEAD ebae5ca; contém integracao. Fiel sozinho (Fielzinho sem cota até 06h58;
leitura dele pendente).

## Veredito: PASSA

## Conferido
- `decidir.mjs`: todo `ask` da guarda grava a pendência daquela mudança (função `pendencia`): tabela sem
  `HUB_PAPEL` (linha ~165), nome parecido (~174) e o caso do verificador (como no 31). A ordem segue: avais/ e
  `.local/acervo/` negados antes; tabela com `HUB_PAPEL=maestro` passa antes de criar pendência.
- `aval.mjs`: registra com a pendência, com ou sem parecer; sem parecer diz "sem verificador: dispensado" nas duas
  linhas, sem parecer inventado. Tabela gravada pelo maestro apaga a pendência sobrada e não registra. Nome do
  registro da tabela: `AAAA-MM-DD--routing.md`.
- Critérios 1 e 2: testes `35: peça de nome parecido aprovada...` e `35: tabela de roteamento aprovada sem
  HUB_PAPEL...`. Critério 3: os testes do 31 seguem iguais.
- `node --test agents/code/test/20-acervo.test.mjs`: 22/22 (Fiel). Árvore limpa. Suíte inteira: na junção (regra nova).

## Ressalva (não bloqueia)
- Limite já escrito no relatório: a pendência de um ask recusado fica; se o mesmo texto exato for gravado depois por
  um caminho sem aval, vira registro "aprovado". Igual ao 31 com parecer.
