# Sync de banco entre duas máquinas pares

Type: research
Status: resolved
Blocked by: 22

## Question

Que mecanismos existem para manter um banco local (SQLite ou outro embutido) igual em duas máquinas
pares, ambas gravando, às vezes offline, sem divergência silenciosa? Para cada um: o que faz quando
as duas mudam o mesmo registro, se precisa de servidor ou serviço pago, se roda no Windows nativo e
se o GitHub privado já decidido serve de ponto de encontro. Critérios 4 e 5 do destino. Protocolo da
§10.4. Origem: "Markdown: vista ou fonte da verdade".

## Comments

- 2026-10-04: lançada a pedido do Gustavo (R5). Relatório em `exploracao/anexos/pesquisa-24-sync-de-banco.md`.

## Answer

Relatório completo: [`pesquisa-24-sync-de-banco.md`](../../../exploracao/anexos/pesquisa-24-sync-de-banco.md)
(2026-10-04; 38 consultas registradas, 15 mecanismos conferidos na fonte; o Reddit ficou sem
cobertura porque bloqueia a busca; nada clonado, instalado ou executado).

- **CRDT/multi-master** (cr-sqlite, sqlite-sync, Turso Sync, Syzy, Marmot, Corrosion, Automerge): na
  colisão, vence um em silêncio (cr-sqlite: *"the largest value is taken"*). Nenhum cumpre "nada
  diverge em silêncio".
- **Dolt é o único pronto que para e avisa:**
  - detecta a colisão por célula e a guarda em `dolt_conflicts_<tabela>`; o commit é recusado até a
    resolução;
  - roda no Windows (`.msi`, winget) e é Apache-2.0;
  - **aceita um repositório git como remote** (conferido por mim na
    [documentação oficial](https://docs.dolthub.com/sql-reference/version-control/remotes): *"By
    default Dolt uses refs/dolt/data"*), então o GitHub privado de "Ponto de encontro do sync" serve
    também para o banco. O beads migrou para esse desenho.
  - Contras:
    - o remote git é recente e tem bugs sérios (push cancelado que trava, pull que baixa tudo);
    - o modo embutido aceita um escritor só;
    - o motor é MySQL;
    - a colisão é por célula, então dois parágrafos diferentes da mesma nota colidem onde o git
      juntaria (inferência, não testada).
- **Texto por linha no git** (sql-md-sync, sqlite-diffable, git-sqlite): a colisão vira conflito do
  git, como em "Divergência e edição concorrente", mas a verdade volta a trafegar como texto.
- **Extensão de sessão do SQLite:** nativa, detecta a colisão, mas o sincronizador inteiro teria de
  ser escrito.
- **Eliminados:** sqlite-sync (a licença prende ao transporte da SQLite Cloud), Turso Sync (*"last
  push wins"*, exige servidor), Syzy e Marmot (sem Windows), Litestream (um escritor só).
- **Recomendação do relatório:** spike no Windows com (a) Dolt e o GitHub como remote git e (b) texto
  por linha no git; a extensão de sessão fica de reserva. Quem decide é o Gustavo.
- **Não verificado:**
  - deploy key pelo Dolt no Windows;
  - crescimento do repositório com o histórico;
  - concorrência no `dolt sql-server`.
