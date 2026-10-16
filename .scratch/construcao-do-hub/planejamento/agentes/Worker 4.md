# Worker 4: notas

## Volta 1 (2026-10-15)

Achei o corte candidato do Worker 2 já no plano (quase igual ao que eu tinha tirado do mapa) e o Worker 8, que primeiro anotou a vigia, ficou com a faixa 8 (kit de par); a vigia é a faixa 7, ainda sem dono na volta 1.
Assumi a **faixa 4: banco e vista `.md`**. Não mandei `maestri ask`: os 12 estão no meio do turno (o ask fica sem
Enter, memória "Ask a recruta ocupado"); as fronteiras foram para o `plano.md`.

### Fontes lidas

- `map.md` "Decisions so far"; Answers dos tickets 25, 33, 48; trechos de 26, 30, 34 e 09 (E2EE); comentários do 16.
- Montagem do spike em `C:\Projetos\spike-livesync\` (só leitura): `docker-compose.yml` (imagem `couchdb:3`, porta
  `127.0.0.1:5984`, `db-init`, MCP do es617 em `127.0.0.1:8787`), `couchdb-init.ini`, `tarefa-cli.xml` (CLI em
  `livesync-src\src\apps\cli\dist\index.cjs`, commit `14141446` do ticket 48), pastas `cli-db*`.

### Achados que mexem em outras faixas

1. **E2EE está decidida** (ticket 34, "Segurança": "E2EE do LiveSync … cada par guarda a cópia completa e a
   frase-senha"). Os spikes 30 e 48 rodaram quase tudo sem E2EE; o 48 (item 11) provou o CLI com E2EE v2 e caminho
   ofuscado: no servidor o caminho fica cifrado e `size`/`mtime`/`children` zerados. Consequências:
   - faixa 5 (MCP do banco): o fork precisa da frase-senha (o 30 cita "E2EE (com a passphrase também no MCP)");
   - faixa 7 (vigia, dono a definir): para dizer **qual arquivo** está em conflito, a vigia precisa decifrar o caminho
     (o ticket 09 fez isso no Node com `livesync-commonlib` 0.1.36, `outgoingDecryptHKDF`). Lendo só o
     `_conflicts` do CouchDB, ela sabe que há conflito, não onde.
2. **O Docker Desktop está desligado agora** (`docker ps`: sem o pipe `dockerDesktopLinuxEngine`, 2026-10-15). Ligar
   o Docker Desktop é ligar serviço: entra na pergunta do Worker 2 sobre o CouchDB de ensaio.
3. **Porta 5984 é do spike** (compose do spike em `127.0.0.1:5984`, com dados dos testes 30 e 48). O Worker 8 quer usar
   o spike como fonte de fixture; se alguém subir o spike na hora, as portas 5984/5985 do corte batem. Troquei a faixa
   de portas de ensaio para 5994–5997.

### Minha faixa: banco e vista `.md` (par A e par B de ensaio nesta máquina)

Decisões: 25 (CouchDB + LiveSync), 34 (S3: um CouchDB por par, replicação mestre-mestre; E2EE; primeiro teste = dois
CouchDB replicando), 33 (CLI do LiveSync como sincronizador; 200 MiB; fora pastas com ponto em qualquer nível;
`mark-resolved`; CLI antes do plugin), 47/48 (comportamento do CLI no Windows, defeito das pastas com ponto aninhadas,
limite padrão de 50 MiB), ticket 16 de 2026-10-14 (exclusão `**/.*` cobre arquivos com ponto, não só pastas).

Orçamento da hora:
- 0–10 min: `kit/par/banco/compose.yml` + `couchdb.ini` + `.env.modelo` publicados (o contrato das faixas 5 e 7);
  dois CouchDB de ensaio (5994 = par A, 5995 = par B); replicação contínua nos dois sentidos (dois documentos no
  `_replicator`).
- 10–30 min: o CLI (build do commit `14141446` copiado do spike, sem recompilar; se não servir, compilar é o risco)
  configurado pelo caminho dos testes oficiais, dois dispositivos, `mark-resolved`, E2EE com caminho ofuscado,
  `syncMaxSizeInMB` 200, exclusão de tudo que começa com ponto em qualquer nível. Roda em laço no terminal; a tarefa
  agendada sai como XML (`ready-for-human`).
- 30–50 min: testes automáticos, um subagente por grupo (abaixo).
- 50–60 min: README da faixa, passagem pelos Prumos.

Critério de aceite (cada item é um teste que roda sozinho):
1. nota criada na pasta A aparece na pasta B (e a editada em B volta a A) em até 30 s, passando por CouchDB A →
   replicação → CouchDB B;
2. nenhum texto claro no CouchDB (busca pela frase da nota nos documentos crus dá zero);
3. `.oculto/x.md`, `.env` na raiz, `projeto/.git/config` e `projeto/.venv/x` não chegam ao banco (o terceiro é o
   defeito 8 do ticket 48: se a exclusão não pegar, a faixa entrega o teste vermelho documentado, e a parte vira
   candidata a Fable);
4. arquivo de 60 MiB viaja (acima do padrão de 50, abaixo de 200); arquivo de 201 MiB não viaja;
5. colisão de texto (replicação pausada, a mesma linha editada em A e em B, replicação religada): o documento fica com
   `_conflicts` nos dois CouchDB e nenhuma das duas versões some;
6. a faixa deixa em `execucao/ensaio/banco/` um retrato do banco de ensaio com um conflito aberto e um binário com
   ramo apagado, como dado de ensaio para as faixas 5 e 7 na próxima execução.

Fica fora da hora: o plugin no Obsidian (configuração por tela, `ready-for-human`, Setup URI pronto pelo kit), a
replicação real pela tailnet, a tarefa agendada registrada de verdade, a tela de três vias.

### Não verificado

- Que o build do CLI do spike (commit `14141446`) aceite a exclusão de arquivos com ponto em qualquer nível; o
  `.livesync/ignore` nunca foi testado (ticket 48, "Não testado").
- Que a replicação de CouchDB para CouchDB funcione com dados E2EE do LiveSync (inferência: a replicação copia
  documentos sem abrir; o ticket 34 marca o primeiro teste como NV).
- Que o CLI gere o Setup URI para o plugin.

### Para a próxima volta

- Fechar com o dono da faixa 5 (MCP do banco) o `.env` do banco (URL, banco, usuário, frase-senha de ensaio).
- Fechar com o dono da faixa 7 (vigia) a decifragem do caminho (achado 1).
- Conferir com o Prumo 2 se cabe na hora com o Docker hoje desligado.

## Volta 2 (2026-10-15)

O maestro já escreveu a spec (`../spec.md`, `../spec-partes/`) e os tickets (`../issues/`), e o cabeçalho da spec pede
que cada worker corrija a parte da sua faixa. Fiz uma coisa só: **ajustei a faixa 4 para caber na hora e corrigi a spec
dela.**

- **Plano:** a linha do Worker 4 ganhou ordem de corte (núcleo N1–N4 até o min 35; S1–S6 se sobrar), os caminhos da
  faixa (crivo do Prumo 2, item 6), `kit/par/env/04.env` no lugar do `.env.modelo` comum (proposta do Prumo 2),
  contêineres `hub-ensaio-04-*`, credenciais de ensaio geradas (item 7; apaguei o item 4 do crivo aplicado) e os
  exemplos de `_scheduler/docs` no min 15 (pedidos dos Workers 10 e 7). Fronteira nova "Worker 4 (volta 2)".
- **Fonte primária lida** (código do CLI no spike, commit `1414144`, só leitura):
  - `src/apps/cli/main.ts`: a regra embutida corta por `path.sep` (no Windows `\`): explica o defeito 8 do 48
    (inferência, não verificada; o teste N4 confere);
  - `serviceModules/IgnoreRules.ts`: `.livesync/ignore` com minimatch `dot: true`, troca `\` por `/`, `**/` na frente de
    padrão sem barra, `**` atrás de padrão terminado em barra; `import: .gitignore`; negação recusada;
  - ajuda do CLI: `init-settings`, `remote-add`, `setup <URI>`, `mark-resolved`, `ls`, `info`, `cat-rev`, `pull-rev`,
    `resolve`; `encodeSettingsToSetupURI` da commonlib usado em `commands/runCommand.unit.spec.ts`.
- **Spec corrigida:** `spec-partes/faixas-03-04.md` (portas 5994–5997; `.ini` sem `[admins]`; exclusão pelo
  `.livesync/ignore`; o CLI decifra para a vigia; ordem de corte; harness só com login; pontos abertos do Setup URI, da
  exclusão, das portas e do dono do script de `local: true`); `spec.md` seção Worker 4 e `issues/04-banco-e-vista-md.md`
  iguais à linha do plano.
- **Achado para outros:** as partes das faixas 5 e 7 na spec ainda dizem 5986 (`spec-partes/faixas-05-06.md` linhas 114
  e 120) e 5987 (`faixas-07-08.md` linha 116); o plano e a tabela do Prumo 2 dizem 5996 e 5997. Cabe aos Workers 5 e 7.
- Não verificado e aberto: segundo processo do CLI no mesmo banco local com o `daemon` rodando; replicação CouchDB ×
  CouchDB com dados E2EE; Setup URI gerado de ponta a ponta.

### Para a próxima volta

- Conferir se os Workers 5 e 7 trocaram as portas e se o Worker 7 aceita o CLI (`ls`, `info`, `pull-rev`) na vigia.
- Ver se `kit/` fora do ticket 12 (aviso do Worker 7) virou decisão; a faixa 4 depende de onde o kit mora.
