# Parecer do ticket 21 (Trilho): arquivar e cópia diária

## Rodada 1 — 2026-10-17 ~10h20 (Fiel sozinho; Fielzinho sem cota até 12h15, leitura dele pendente)

Ramo `ticket-21`, HEAD 1c87f9b (com o ticket-16 0332466). `integracao` andou só pela junção do 16 (fce0529); merge
sem conflito (`git merge-tree`).

**Veredito: VOLTA** (2 consertos).

### Consertos

1. **A guarda "dentro do hub" deixa passar pasta de outro disco** (Fiel). `agents/skills/arquivar/arquivar.mjs:39`:
   `resolve(rel) === rel` não pega caminho absoluto no Windows, porque `rel` já teve `\` trocado por `/`.
   Sonda (lógica da linha 39, hub `C:/context-hub`): `D:/fora/pasta` → `rel = 'D:/fora/pasta'`, guarda `false`;
   tem 2 partes, sem ponto, sem `_archive` → segue. Com os pares em dia e a pasta existindo, o arquivar move uma pasta
   de fora do hub para `D:/fora/_archive/...`. Conserto: `isAbsolute(relative(hub, origem))` (ou `path.win32`
   antes de trocar a barra), com um caso de teste.
2. **O Docker não mostra que o sincronizador de A segue vivo depois do arquivar** (Fiel). O
   `logs/trilho-21-docker-3.log` termina com `Assertion failed: !_wcsnicmp(filename, dir, dirlen), file
   src\win\fs-event.c, line 72`: um node com `fs.watch` abortou (libuv) na rodada, sem que o teste diga qual. É o mesmo
   abortar que reproduzi:
   - no `node --test agents/code/test/21-*.test.mjs`, o observador dublê (`21-arquivar.test.mjs:152`) aborta igual;
   - sonda isolada: `fs.watch` em cada pasta, depois mover um arquivo para fora ou apagar a subpasta → aborta (saída
     127) com o TEMP curto (`C:\Users\GUSTAV~1.DEL\...`); com o caminho longo, fica vivo nos dois casos.
   O sincronizador real é node com chokidar (`fs.watch` por pasta). Se ele cair ao arquivar, as edições seguintes
   param de replicar, e a vigia só vê depois. O caso 1 do Docker passa porque a mudança chega ao B antes ou sem
   depender da queda. Pedido: no `21-arquivar.test.ps1`, depois do arquivar, (a) conferir que o processo do CLI de A
   segue de pé e (b) gravar uma nota nova em A e vê-la chegar ao B; e dizer de onde vem o `Assertion` do log (se for do
   teardown ou de outro processo, mostrar). No teste leve, conferir que o observador dublê não morreu (ou rodá-lo no
   caminho longo, como o achado comum do fork), senão o caso não prova que o sincronizador aguenta.

### Ressalvas (não bloqueiam)

- **Junção com o 22:** o 21 e o 22 (Brasa) criam o mesmo arquivo novo `agents/code/kit/par/env/10.env.modelo`, com
  conteúdos diferentes (o 21: `HUB_MAQUINA`, `HUB_COPIA_*`; o 22: `HUB_PROXY_*`). Quem juntar depois terá conflito
  add/add; as duas metades têm de ficar. Aviso ao Rebite junto com o passa.
- No caminho arquivo por arquivo, subpasta vazia não vai para o destino (só arquivos são movidos; o `rmdir` a
  apaga). O LiveSync não replica pasta vazia; fica igual para o outro par, mas some nesta máquina.
- Se devolver no meio falhar (`arquivar.mjs:120-127`), sai exceção sem recusa e o estado fica parcial; caso raro.
- `frontmatter.mjs`: o comentário antigo "Troca de trecho: ..." ficou em cima do `trocarCampos`, longe do
  `aplicarTrocas`.
- `copia-diaria.mjs`: a data da mensagem do commit é UTC (`toISOString`); depois das 21h sai o dia seguinte.

### Conferido sem conserto

- Aceite 1: move com o outro par em dia; recusa com replicação parada, pendentes, sem resposta, edição < 15 min
  (testes leves e Docker caso 2). Aceite 2: commit no `par/<máquina>`, push para nu local, remoto quebrado sai 1 e a
  vigia notifica (Docker casos 6-8; testes leves 4/4). Aceite 3: `conferir-cabeca` recusa ausente e acima de 2.000
  (4/4); `verificar-hub` usa a mesma regra. `limpar-arquivo` sem caminho que apague.
- Costuras do maestro (15 min, outro par desligado recusa, em dia = running e 0 pendentes, arquivo por arquivo) seguidas.

### Evidências

- `node --test agents/code/test/21-*.test.mjs agents/code/test/harness-real.test.mjs` (detector do 29): 25/25,
  com o `Assertion` do observador dublê no meio da saída. `git status` limpo depois.
- Sondas em `%TEMP%\hub-ensaio-21-fiel-w` (apagada; os dois node da sonda encerrados por PID).

## Rodada 2 — 2026-10-17 ~11h55 (Fiel sozinho; leitura do Fielzinho pendente, depois das 12h15)

Ramo `ticket-21`, HEAD 462b55e (consertos f32bd4c e 462b55e; o `ticket-16` 6a0ab17 juntado). **Veredito: PASSA**,
com um passo antes do Rebite.

- Conserto 1 feito: `isAbsolute` no `relative` nativo; casos `Z:/fora/pasta` e `Z:\fora\pasta` recusam.
- Conserto 2 feito: Docker 4ª (`logs/trilho-21-docker-4.log`): o sincronizador de A tem o mesmo PID antes e depois do
  arquivar (233468) e uma nota nova em A chega ao B; o hub de A está no caminho longo. O `Assertion` era do dublê no
  TEMP curto: o dublê agora observa pelo caminho longo, e os testes conferem que ele segue vivo.
- 462b55e: a description do `arquivar/SKILL.md` tinha o mesmo `: ` do 16; as 10 skills leem pelo `separar`.
- Fiel: `21-* + harness-real` 25/25, sem `Assertion` na saída; `git status` limpo.
- **Antes do Rebite:** a `integracao` já tem o 22 (4a47576), e o `git merge-tree` dá **CONFLICT (add/add)** em
  `agents/code/kit/par/env/10.env.modelo`. Juntar a `integracao` no ramo e deixar as duas metades (as linhas do proxy
  do 22 e as da cópia do 21); repetir os testes do 21 e os do 22 (`22-kit-cliente`, `22-proxy-sem-docker`), que leem
  esse modelo. Mandar a ponta: confiro só o arquivo e os testes.
- Junção da `integracao` (~12h05), ponta 6b6c65e: o ramo contém a `integracao` (4a47576, com o 22); o
  `10.env.modelo` tem as duas metades (proxy em cima, cópia embaixo), sem marca de conflito; só o `10-proxy.ps1` e
  o `proxy.psm1` citam o modelo (nos comentários). Fiel: `21-* + 22-kit-cliente + 22-proxy-sem-docker + harness-real`
  29/29; `git status` limpo; nenhum `mcp-proxy` de pé. **PASSA**; pode ir ao Rebite (a junção do 21 segue esperando o
  16 resolvido, como diz o ticket).
