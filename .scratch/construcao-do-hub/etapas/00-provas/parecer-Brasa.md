# Parecer do Fiel — ticket 01, prova: dois CouchDB replicando (Brasa)

## Rodada 1 — 2026-10-16 — ramo ticket-01 em 0c8c639

Veredito: **passa**, sem consertos. Ressalvas abaixo, para o ticket 07.

Conferido: integracao 0d04985 é ancestral de 0c8c639; diff contra integracao = 5 arquivos em
`agents/code/test/provas/01-banco/`. Li o ticket 01, o relatório, o bloco do Worker 4 no spec e `prova.ps1`.
`banco.psm1` da 01 = cópia da 02 menos os três acréscimos da 02, mais `-SemSalComum` (diff conferido).

Evidências (rodadas pelo Fiel):
1. `pwsh agents/code/test/provas/01-banco/prova.ps1` (com E2EE e caminho ofuscado): 19 PASSA, saída 0;
   hub de ensaio de 90 arquivos A->B em 18,2 s; travessias 1,0–3,6 s; conflito com `_conflicts` e 2 folhas nos dois
   bancos; nada em claro. Log: `etapas/00-provas/revisao-01-r1-cifrada.log`. Contêineres e pasta apagados no fim.
2. Sonda própria (o teste só procura os nomes e textos que ele mesmo cria): rodada com `-Manter`, li os
   `_all_docs?include_docs=true` crus dos dois bancos (589 kB cada) e procurei 63 nomes de arquivo e 22 trechos de
   texto do hub de ensaio: nada achado. Log da rodada: `revisao-01-r1-manter.log`. Derrubei o ensaio à mão
   (PIDs do `.pid`, `down -v`, pasta apagada; sem contêiner nem volume hub-ensaio-00).
3. Critérios do ticket: os quatro atendidos (tabela do relatório confere com o que rodei).

Ressalvas (não seguram):
- O caso "nada em claro" da prova só procura o que a própria prova escreve; o ticket 07 deveria incluir nomes e
  trechos do hub de ensaio, como a sonda 2.
- Contêineres `hub-ensaio-00-*`; o spec do Worker 4 fala em `hub-ensaio-04-*`. Nome de ensaio; o kit (07) decide.
- `banco.psm1` duplicado entre as provas 01 e 02 (e o 06 importa o da 02); o 07 junta, como o relatório diz.

Limpeza: a rodada órfã do revisor anterior (20:00, `revisao-01-cifrada.log`) foi derrubada pelo Fiel às ~20:15.

Fielzinho: no limite de uso do Codex até 20:26; a leitura dele fica para depois. Se ele achar algo, entra como
ressalva para o Rebite.
