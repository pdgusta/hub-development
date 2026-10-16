# Worker 7: notas

## Volta 1 (2026-10-15)

**Faixa assumida: 7, vigia e divergência** (linha do Worker 7 no `plano.md`). O Worker 2 gravou o corte em 10 faixas e
pegou a 2; o Worker 8 começou pela vigia e passou para a 8 (kit) para manter "faixa N = Worker N", deixando o desenho
da vigia em `agentes/Worker 8.md` como proposta para mim. Herdei esse desenho e o ajustei às decisões.

### Fontes conferidas nesta volta

- Ticket 33, `## Answer` ("Divergência", "Aviso"): os quatro casos de divergência, 15 min, 200 MiB, binário por
  `mtime` com ramo apagado recuperável (R71), vigia a cada 5 min, notificação quando piora, mod do Claude Code.
- Ticket 14, `## Answer` ("Checagem de início", "Estado da vigia na tela"): hook lê o arquivo da vigia, senão a
  ferramenta do MCP; Copilot pela `statusLine`; Codex na checagem de início mais o `notify` disparando o toast.
- Ticket 34, "Segurança": **E2EE do LiveSync decidida**. O 48 (item 11) mostrou caminho cifrado e `size`, `mtime`,
  `children` zerados no servidor. O Worker 4 apontou que o ticket 09 decifrou no Node com `livesync-commonlib` 0.1.36.
- Spike `C:\Projetos\spike-livesync\` (só leitura): `revs.py` lê folhas com `open_revs=all`; `tarefa-cli.xml` é o
  modelo de tarefa agendada (IgnoreNew, reinício em falha).

### Decisões de desenho da faixa (minhas, a conferir pelo Prumo)

- Node ≥ 22 `.mjs`, como as faixas 6 e 9: uma dependência só no par, e decifrar exige a lib do LiveSync, que é JS.
- Hook de início próprio, separado do da nota (faixa 2).
- Níveis por item; topo = pior item. Sincronizador parado e Config Doctor como `divergencia`; cópia diária falha como
  `informa` com notificação (inferência).
- O `notify` do Codex é da faixa 7; encadeia outro programa se alguém precisar.

### Não verificado

- Como o LiveSync marca o ramo de binário descartado pela resolução por `mtime` (o 48 recuperou por script: ler lá).
  Hipótese: o ramo perdedor aparece em `deleted_conflicts` / `open_revs=all` com `_deleted`.
- API de mods do Claude Code para a faixa acima do prompt ou linha de status.
- `notify` do Codex aceitar um programa só.
- Notificação do Windows sem módulo instalado (WinRT pelo PowerShell).
- Detectar Config Doctor travado sem o Obsidian aberto.
- Somar o contexto de dois hooks de início no mesmo evento nos três harnesses.

### Cabe em 1 hora?

O núcleo (passada, estado, notificação, testes com dublê, hook de início, `statusLine`, `notify`) cabe com subagentes
em paralelo (pesquisa de fonte; scheduler e conflitos; binário e recuperar; notificação; mod; hooks dos três
harnesses; testes). O risco é decifrar o caminho e recuperar o binário com E2EE: candidato a subagente Fable 5.1 médio.
Se não fechar, sai sem E2EE e o resto fica para a próxima execução.

### Para a próxima volta

- Ler a linha final do Worker 4 (retrato do item 6) e do Worker 5 (ferramenta reserva) e fechar por `maestri ask`.
- Pedir ao Prumo que confira os níveis propostos contra o glossário.
- Conferir no ticket 48 como o ramo de binário foi achado e recuperado.

## Volta 2 (2026-10-15, última, 3 min)

- Corrigi na spec (seção Worker 7): `agents/vigia/` → `agents/skills/vigia/` (o ticket 12 não tem `agents/vigia/`;
  skill com scripts, como a "nova iniciativa"; a confirmar pelo Prumo); `copia_diaria` → `copia-diaria`, com nível
  `informa` e notificação; caminho do `estado.json` e nível por item explícitos no critério de aceite.
- Ficou sem corrigir (sem tempo): `hooks/`, `mods/`, `kit/` e `agents/test/` também não estão no ticket 12; vale para
  todas as faixas, é a "tabela de donos" do item 6 do crivo do Prumo 2.
