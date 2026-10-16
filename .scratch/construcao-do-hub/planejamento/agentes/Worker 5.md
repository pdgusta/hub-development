# Worker 5: notas

## Volta 1 (2026-10-15)

**Faixa assumida: 5, MCP do banco com versão** ("faixa N = Worker N", como os Workers 2 e 8). Linha completa no
`plano.md`; fronteiras em "Worker 5 (volta 1)"; uma pergunta ao Gustavo (onde mora o fork).

### O que conferi (fonte)

- Answer do 25: fork do es617 com R1 (`base_rev`) e conflito visível antes de usar.
- Answer do 30 (spike): R1 emulada no CouchDB (`C:\Projetos\spike-livesync\r1.py`, `_bulk_docs` com
  `new_edits=false` e `_revisions`) virou conflito e o plugin abriu o modal; `edit_note` com `replace` já recusa
  texto velho; `append`/`prepend` agem sobre o atual; `read_note` devolve só a vencedora. Esforço estimado: R1 ~1 dia,
  conflito visível ~0,5 dia (agora em 1 hora com 10 subagentes: apertado; o R1 com E2EE é o candidato ao Fable).
- README do es617 (cópia em `C:\Projetos\spike-livesync\docs\es617_obsidian-sync-mcp_main_README.md`, data da cópia
  não conferida, versão atual não verificada): ferramentas `read_note`, `write_note`, `edit_note`, `delete_note`,
  `move_note`; `READ_ONLY` desliga todas as de gravação; `MCP_INSTRUCTIONS(_FILE)` só acrescenta, lido na partida,
  fatal se faltar, máx. 32 KB; `COUCHDB_PASSPHRASE` para E2EE; Node 22+; `npm test` e `npm run test:e2e`; "No
  conflict resolution ... last write wins".
- Answers do 34 e 14: segunda instância `READ_ONLY=true` com token por par; 127.0.0.1 com token de variável de
  ambiente; o proxy de cliente (faixa 10) tem `/banco/mcp` e `/banco-escrita/mcp`.
- Answer do 36: cabeça do contrato até 2.000 caracteres (corte do Claude Code em 2.048).
- Answer do 11: `write_note` com a versão lida é o caminho da regravação inteira; banco fora = a regravação espera.
- Answer do 12: imposição C inclui o MCP do banco validar o esquema (deixei como "se couber").
- Nesta máquina: Node v24.19.0; Docker 29.8.2 instalado (motor desligado, segundo o Worker 4).

### Riscos

- O gancho `conflictBaseRev` da commonlib vem da pesquisa 26 e não foi conferido no código; se não existir, o R1 vai
  pelo `_bulk_docs` com `new_edits=false` (provado no spike), cifrando o pedaço pelo caminho do upstream quando houver
  E2EE.
- Duas instâncias do es617 sobre o mesmo banco: não testado.
- A cabeça antes do texto do upstream depende do tamanho dele (não verificado).

### Próxima volta

- Corrigir a parte da faixa 5 em `../spec-partes/` (pedido do maestro no ticket 16, 21h50), se já existir.
- Conferir com o Worker 4 a porta 5996 e o `.env.modelo`, e com o Worker 8 os nomes `hub-banco`/`hub-banco-leitura`.

## Volta 2 (2026-10-15)

**Uma coisa: o R1 pela recusa 409 nativa do CouchDB** (mudou o plano: linha do Worker 5, fronteira "E2EE e o R1" e
"Riscos de tamanho").

- Fonte primária (docs.couchdb.org, lida por subagente web-fetch, citações literais):
  - `api/document/common.html`, PUT: "409 Conflict – Document with the specified ID already exists or specified
    revision is not latest for target document"; `new_edits`: "The false value is intended for use only by the
    replicator."
  - `replication/conflicts.html`, 2.3.2: "If that _rev has already been superseded, the update is rejected with a 409
    Conflict response"; no diagrama, "409 Conflict (not saved)"; "these conflicts never end up inside the database".
- Leitura das decisões: o Answer do 11 (2026-10-15) diz "se o arquivo mudou desde a leitura, a gravação é recusada, e
  o agente relê e refaz"; o do 25 (2026-10-06) dizia "vira conflito se a base mudou". A recusa cumpre a garantia dos
  dois (nada se desfaz sem o agente ver) e é a forma do mais novo. A folha em conflito (`new_edits=false`, `r1.py`)
  fica de reserva. Pedido ao Prumo: conferir 11 × 25.
- Não verificado: onde o upstream busca a revisão atual antes de gravar; se pedaços gravados antes de um 409 ficam
  órfãos (custo de espaço, sem perda).

### Correções à parte da faixa 5 em `../spec-partes/faixas-05-06.md` (não editei: o PROMPT limita a escrita a `planejamento/`)

1. **Porta do banco de ensaio:** 5986 → **5996** (fronteira do Worker 4); contêiner `hub-ensaio-05-couchdb`; MCP em
   8796 (escrita) e 8797 (leitura).
2. **Ponto aberto "Recusa ou conflito gravado":** fechar como recusa 409 (acima), com a folha em conflito de reserva.
   Ajustar a user story 4 ("me volte como conflito explícito" → "seja recusada, me dizendo para reler e refazer") e o
   aceite de ponta a ponta ("o banco guarda as duas folhas" → "o banco não ganha revisão nova").
3. **Ponto aberto "De onde vem a cabeça do contrato":** fechado na rodada: bloco `cabeca:inicio/fim` do `AGENTS.md`
   (Worker 1), lido a cada `initialize`, antes do texto do upstream. Em "Out of scope", "a atualização da cabeça do
   contrato no MCP quando o `AGENTS.md` muda: faixa 10" sai; a faixa 10 só confere que o bloco existe e cabe.
4. **Ponto aberto "Instância só de leitura":** o upstream já tem `READ_ONLY=true` ("disable all write tools ... the
   vault backend rejects writes as well", README do es617, cópia do spike). Segunda instância = mesma linha, só essa
   variável e o token trocados.
5. **Ponto aberto "Cifra do banco":** a E2EE está decidida (Answer do 34, conforme o Worker 4); o fork recebe a
   frase-senha (`COUCHDB_PASSPHRASE`). Sai "a decisão sobre cifrar é da faixa 4".
6. **Falta na spec:** a ferramenta `estado_do_hub` (checagem de início onde o hook falhar e no cliente, Answer do 14),
   lendo `HUB_VIGIA_ESTADO`; sem arquivo, "vigia sem estado neste par".
7. **Falta na spec:** o crivo do Prumo 2: prova em um comando (`pwsh agents/test/05-mcp-banco.ps1`).
8. **Nota nova pelo MCP:** proposta: grava sem `base_rev` só se o caminho não existe (PUT sem `_rev` também volta 409
   se o documento existe, mesma linha da doc).
9. **Escopo da hora:** as user stories 23, 27 e 28 (Desktop pela ponte, os três harnesses reais, "regra seguida")
   dependem do login de ensaio e da faixa 8; ficam para outra execução (já no plano). A validação de frontmatter
   (stories 10 a 12) fica como "se couber".
