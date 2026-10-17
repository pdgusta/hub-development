# Relatório do ticket 16: vigia, passada, estado e notificação (Trilho)

2026-10-17 07:20. Rodada 1 do Fiel foi leitura intermediária (parecer-16-Trilho.md); ressalvas feitas. Falta o 08.

## Estado

- Ramo `ticket-16` (HEAD c36ece4, com integracao 9cc878b: o 10 junto), worktree `C:\context-hub-wt\ticket-16`, de `integracao` 33b817a.
- Começou antes dos bloqueios (maestro, 04:23): os cenários do 08 e o `estado_do_hub` real do 10 entram quando eles
  forem juntados. **Junção só com 08 e 10 resolvidos.**
- Conserto do 12 em commit à parte (pedido do maestro), b4e7272: `agents/skills/busca/SKILL.md` não cita mais a
  ferramenta `read` do `hub-busca`, que o 12 r3 tirou dos harnesses.

## Decisões (maestro, 2026-10-17)

1. **Piora** (o spec deixava em aberto): um item sobe de nível em relação à passada anterior; item novo conta como `ok`
   antes; sem repetição enquanto nada sobe; um item que desce e volta a subir notifica de novo.
2. Lugar: `agents/skills/vigia/` (o agente chama o `recuperar`).
3. Costuras aceitas: `etapas/costuras-16-Trilho.md`.
4. Combinado com o Cinzel (10): o `estado_do_hub` devolve o `estado.json` sem `vistos`; sem arquivo ou ilegível,
   "estado indisponível"; passada com mais de 15 min, o JSON e o aviso "a vigia não roda desde <hora>".

## O que foi construído

- **Skill** `agents/skills/vigia/`:
  - `vigia.mjs passada --env <par>.env`: lê o CouchDB (`_scheduler/docs`, `_changes?style=all_docs`,
    `open_revs=all` com `Accept: application/json`) e o leitor da vigia (dispositivo do CLI com banco próprio: `sync`,
    `ls`, `info`). Itens: replicação (em dia; parada há mais de 15 min com o outro par ligado = `divergencia`), outro
    par (`HUB_VIGIA_OUTRO_PAR_URL`; sem resposta = `informa` com o motivo, nunca `ok`, e não suprime a replicação
    parada), conflito de texto (`divergencia`, pelo caminho em claro do `ls`), `copia-diaria` de exemplo (`informa`).
    Grava `<hub>/.local/vigia/estado.json` por troca atômica e guarda os itens dos outros (`fim-da-resposta`,
    `acervo-peca-sumida`, `copia-diaria`).
  - `vigia.mjs recuperar <caminho> --env <par>.env`: acha o id pelo `info` do leitor, as folhas apagadas com corpo
    (`path`), e restaura cada uma ao lado do original (`<nome>.recuperado-<n>.<ext>`) pela receita do 08
    (`recuperar.ps1`: cópia `<db>-recupera`, folha reaberta, sal no `_local`, leitor na cópia, `pull-rev`). Nada
    apagado; a cópia sai no fim.
  - `notificar.ps1`: toast do Windows; `HUB_VIGIA_NOTIFICAR` troca o comando (dublê nos testes).
  - `SKILL.md`.
- `gravarPassada` em `agents/code/bin/lib/vigia.mjs`: itens da vigia com `fonte: 'vigia'`, `vistos`, `piorou`.
- Kit: `HUB_VIGIA_LEITOR_DB` e `HUB_VIGIA_OUTRO_PAR_URL` no `04.env.modelo`; o `Install-ParBanco` prepara o leitor.

## Achados

1. `HUB_OUTRO_PAR_URL` é o outro par visto de dentro do contêiner (`host.docker.internal`). A vigia roda na máquina e usa
   `HUB_VIGIA_OUTRO_PAR_URL`.
2. `open_revs=all` responde em multipart sem `Accept: application/json`.
3. O JSON do `info` do CLI vem entre linhas de registro: a vigia pega o bloco de `{` a `}` em linhas próprias.
4. **O daemon apaga o ramo perdedor do binário** (confirmado no Docker, 3ª rodada: folhas `2-…` viva e `3-…` apagada).
5. **Com o caminho ofuscado, `path`, `mtime` e os pedaços vão cifrados no `path` (`/\:…`)**: o `children` claro vem
   vazio e o `mtime` 0. A folha apagada se reconhece pelo `path` (o toco de um DELETE não tem). O `recuperar` olhava o
   `children` e não achava nada; consertado em 67e1f04, com caso novo no teste sem Docker. Vale para o 08
   (`Get-RamosApagados` no `ensaio.psm1` filtra por `children`) e para o cenário "binário descartado" da passada.
6. No PowerShell, `Invoke-RestMethod` devolve o array do `open_revs` como um item só: o teste desenrola.

## Ressalvas do Fiel (leitura intermediária, ~06h55), feitas
1. **Atualização perdida** (5709117): `gravarItem`, `gravarPassada` e `tirarItem` leem, mudam e gravam sob a trava
   `<estado>.trava` (criada com `wx`; espera de 50 ms; trava com mais de 10 s é de dono morto e sai). Testes: quem grava
   espera o outro dono e não perde o item dele; trava velha é tomada.
2. **CouchDB que recusa** (5709117): o `pedir` devolve nada só no 404; outra recusa é erro com o código. Um 401 vira
   "replicação não conferida: o CouchDB do par respondeu 401" (`informa`), nunca parada. Teste novo.
3. **Uma cópia só** (5709117): o `recuperar` chama o `recuperar.ps1` uma vez, com `-Revs` e `-Destinos` (separados por
   `|`, mesma ordem): uma cópia do banco, um `sync`, um `pull-rev` por folha. A cópia ainda é do banco inteiro (o id dos
   pedaços vai cifrado no `path`, então não dá para filtrar por `doc_ids`).

## Entrou depois do parecer
- `estado_do_hub` real (3e29a85, 084b138): o ponta a ponta sobe o MCP do banco do 10 pelo passo 05 sobre o mesmo par;
  a instância de leitura devolve o `estado.json` que a vigia gravou, sem `vistos`, em um bloco. Precisa de
  `HUB_MCP_BANCO_DIR` com o fork do 10 compilado (o `C:\Projetos\hub-mcp-banco` padrão está no 09 e não tem a
  ferramenta; usei `C:\Projetos\hub-mcp-banco-wt/ticket-11`, em 34c3e50, só leitura).
- `fim-da-resposta` (3ab8898): o teste grava o item pela lib, na forma do hook do 27 (`faltas`, `hora`); a passada o
  guarda e notifica.

## Testes

- Sem Docker: `node --test agents/code/test/16-vigia.test.mjs`: 12/12 (dublê HTTP do CouchDB, CLI falso em
  `agents/code/test/vigia/`, notificador dublê).
- Docker: `pwsh -NoProfile -File agents/code/test/16-vigia.test.ps1` (hub-ensaio-16-a/b, 5996/5997, pela fila).
  - 1ª rodada (05h): 6 falhas (achados 1 a 3, base da colisão antes do hub inteiro replicar).
  - 2ª (05:14, `logs/trilho-16-docker-2.log`): 10 passam; forja do ramo apagado com 409, sem dados.
  - 3ª (05:40, `logs/trilho-16-docker-3.log`): 12 passam; o daemon apagou, o `recuperar` não achou (achados 4 a 6).
  - 4ª (06:35, `logs/trilho-16-docker-4.log`, ramo aa70e98): **tudo passou** (16 casos). O daemon apagou o ramo
    perdedor (sem forja); o `recuperar` gravou `inbox/foto-da-vigia.recuperado-3.png` com os bytes da versão perdida;
    o original fica; a cópia do banco e os contêineres saem.
  - 5ª (07:01): caminho do passo 05 estragado no teste (084b138). 6ª: o fork padrão não tem o `estado_do_hub`.
  - 7ª (07:10, `logs/trilho-16-docker-7.log`, c36ece4, `HUB_MCP_BANCO_DIR` = fork do 10): **tudo passou** (15 casos,
    com o `estado_do_hub` real e o `recuperar` de uma cópia só).

## O que espera o 08 e o 10

- 08 (Brasa): binário descartado na passada, acima de 200 MiB, sincronizador parado, gerador de exclusões a cada passada
  (código 2 vira item com o caminho), item `fim-da-resposta` casado com o hook do 27.
- 10: juntado (9cc878b); feito.
- 27: feito (item pela lib).
