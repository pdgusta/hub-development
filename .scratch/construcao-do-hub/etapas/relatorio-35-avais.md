# Relatório do ticket 35: todo aval aprovado é registrado, também sem parecer (Trilho, 2026-10-17)

Ramo `ticket-35`, worktree `C:/context-hub-wt/ticket-35`, de `integracao` 236b3ef.

## Feito
- `agents/code/hooks/acervo/decidir.mjs`: todo `ask` da guarda deixa a pendência daquela mudança exata
  (`.local/acervo/pendentes/<chave>.json`): nome parecido, tabela de roteamento sem `HUB_PAPEL`, e o caso com parecer
  (como no 31). Função `pendencia`; `TABELA` exportada.
- `agents/code/hooks/acervo/aval.mjs`: registra com a pendência, com ou sem parecer. Sem parecer, o registro diz
  "Verificador: sem verificador: dispensado." e, na seção do relatório, "Sem verificador: dispensado (...)". Nenhum
  parecer inventado. A tabela vira `AAAA-MM-DD--routing.md`.
- Tabela gravada com `HUB_PAPEL=maestro` (passa sem aval): a pendência que sobrou de um ask sem resposta é apagada e
  não vira registro de aprovação.
- `agents/skills/maestro-harnesses/guarda-do-acervo.md`: o texto do registro diz que todo aval aprovado fica.
- Testes novos em `agents/code/test/20-acervo.test.mjs`: `35: peça de nome parecido aprovada...` e `35: tabela de
  roteamento aprovada sem HUB_PAPEL...`. Os do 31 seguem iguais.

## Commits
140417a (nome parecido), d65b18a (tabela), 0b01cd9 (texto da guarda).

## Testes
- `node --test agents/code/test/20-acervo.test.mjs`: 21 passam, 0 falham.
- Teste do ticket (20-acervo) depois de juntar integracao 3c24d68 (ebae5ca): 22 passam. Suíte inteira só na junção (regra nova).

## Limite conhecido
- Pendência de um ask recusado pelo Gustavo fica no `.local/acervo/pendentes/`. Se o mesmo texto exato for gravado
  depois por um caminho que não pede aval (ex.: a peça parecida foi apagada), o registro diria "aprovado". Só o caso
  da tabela pelo papel do maestro está fechado. Igual ao 31 com parecer.

## Downloads, login, Docker
Nenhum.
