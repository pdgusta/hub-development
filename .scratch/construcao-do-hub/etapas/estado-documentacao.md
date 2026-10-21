# Estado da documentação técnica (Lume)

Plano: `documentacao-tecnica.md`. Fila e progresso; o Lume atualiza a cada página.

## Fila (fase 1, ordem das dependências)

04 · 05/27/32/33 · 06 · 07/08 · 28 · 12/13 · 14/15 · 19/34 · 20/31/35 · 09/10 + fork · 16/39 · 17 · 21 · 22 · 01-03 ·
29/30/36/38 · depois: arquitetura, stack, harnesses, operação, decisões, README.

## Ramo

`docs`, worktree `C:/context-hub-wt/docs`, criado de `integracao` e7203b4 (2026-10-17). README aprovado pelo maestro
(seções: para que serve e regra de ouro · como ler · mapa das peças · páginas gerais · estado · como manter).

## Feito

- 2026-10-17: `componentes/esqueleto-e-hub-de-ensaio.md` (04, com 05, 21, 30, 36), commit 37ede62. Verificador de
  frontmatter ignora a página (saída 0). Ressalva anotada: comentário velho no topo de `conteudo.mjs` (valores "não
  decididos", já fixados pelo 05); menor, avisar o maestro junto com o pedido da junção.

- 2026-10-17: `componentes/frontmatter-e-verificador.md` (05, 21, 27), commit 3a16079.
- 2026-10-17: `componentes/pastas-e-links.md` (27, 32, 33), commit 1caa703. O fim da resposta (parte do 27, e o 37)
  fica para página própria.
- 2026-10-17: `componentes/gerador-de-exclusoes.md` (06, 28, 36), commit 102068a.

- 2026-10-17: `componentes/banco-do-par.md` (07, 08), commit 12f780a. Link corrigido em 5b6e9b5.
- 2026-10-17 ~12h20: **1ª junção dos docs pedida ao Rebite** (ponta 5b6e9b5, `integracao` e7203b4 contida); ele junta
  depois da suíte do 17. Maestro avisado (com a divergência menor do `conteudo.mjs`).

- 2026-10-17: `componentes/pastas-locais.md` (28), commit 455e160.
- 2026-10-17: `componentes/busca.md` (12, 13), commit dc01f6f.

- 2026-10-17: `componentes/guardas.md` (14, 15, 31), commit 9d7490f.
- 2026-10-17: `componentes/roteamento-de-skills.md` (19, 34), commit e5b97bb. Divergência avisada ao maestro: a regra
  do Copilot que o relatório do 19 entrega à faixa 1 não está no `AGENTS.md`.
- 2026-10-17: `componentes/acervo-do-maestro.md` (20, 31, 35), commit 50275bc.

- 2026-10-17: `componentes/mcp-do-banco.md` (09, 10, fork), commit ae3723d. Roteamento cita o ticket 40 (7d94e58).

- 2026-10-17: `componentes/vigia.md` (16; 39 a caminho), commit 0f71698.
- 2026-10-17: `componentes/vigia-nas-telas.md` (17), commit 2c0894e.

- 1ª junção dos docs (74f201a) **desfeita pelo Rebite**: o `12-busca.test.mjs` caiu 0/9 por tempo (a busca indexa o
  repositório; com as páginas de docs, não ficou pronta em 3 min). Levado ao maestro; o Rebite junta de novo quando ele
  decidir. Nota do Rebite: o verificador de frontmatter sai 0 sem conferir nada em `agents/code/docs/` (sem
  frontmatter, tipo null). Decisão do maestro: o **ticket 41** (Trilho) tira `agents/code/**` da busca; depois o Rebite junta os
  docs. Quando o 41 juntar: atualizar `busca.md` e `gerador-de-exclusoes.md` (o que fica fora da busca).

- 2026-10-17: `componentes/arquivar-e-copia-diaria.md` (21), commit 811cc83.

- 2026-10-17: `componentes/proxy-e-kit-de-cliente.md` (22), commit ce0e2a5.

- 2026-10-17: `componentes/fim-da-resposta.md` (27, 19, 31), commit 703a634. Divergência avisada ao maestro: o mod do
  Claude Code não resolve junction (o script resolve, 8acd1ce).

- 2026-10-17: `componentes/provas-da-etapa-zero.md` (01, 02, 03), commit 29d2994.

- 2026-10-17: `componentes/infraestrutura-de-teste.md` (29, 30, 36; 38 a caminho), commit d58a6da. Fim da resposta
  cita o ticket 42 (a divergência do mod, Brasa), 6889a25.
- **Fase 1 dos componentes completa: 18 páginas.** Tickets a caminho a acompanhar quando juntarem: 11, 18, 23, 24, 25,
  37, 38, 39, 40, 41 (busca sem `agents/code/**`: atualizar `busca.md` e `gerador-de-exclusoes.md`), 42.

- 2026-10-17: `harnesses.md` 9471cc9, `stack.md` 92ed0cf, `arquitetura.md` cb92668, `operacao.md` 4dd1fd3,
  `decisoes.md` 33a968f, `README.md` e4df1e2. **Gerais completas.**
- Juntados em `integracao` depois de e7203b4 (vistos no log, 2d5c528): 38 e 39. Atualizar `infraestrutura-de-teste.md`
  e `vigia.md` depois das gerais.

## Próximo

Em dia com `integracao` b506910 (49 a 52); 9ª junção feita (`integracao` b2ae3db, `main` 70a9f73).

Em dia com `integracao` 8c01cfb (45, 46); 7ª junção feita (`integracao` 7b6c406, `main` fe55b12). Depois: o 26, quando der.

Fase 2: em dia até `integracao` ca62332 (construção fechada; só o 26 a caminho). 6ª junção pedida (docs b20bf5f).
Antes: em dia até `integracao` df6c2e5 (44). Docs: 5ª leva juntada em f640bbd (Rebite, 27-pastas verde; suíte do lote
em curso). Ponta do docs a71e407, 4 páginas sobre f640bbd (pastas-e-links, mcp-do-banco, decisões, README): pedir a
6ª junção quando somar ~5 páginas ou na próxima leva. Esperados: 24 (`kit-de-par.md`, `operacao.md`, `HUB_PAR_ID` em
`pastas-e-links.md` §5), 25, 26.

## Avisos de junção recebidos (fase 2)

- 2026-10-21: 8ª junção feita (5753a7a; frontmatter 0, 27-pastas 24/24). 51 (30564d3) e 52 (b506910) juntados; a Brasa
  já tinha posto uma linha no `vigia.md` e no `banco-do-par.md`. Merge fast-forward no docs. Páginas: vigia 363476e
  (`notificar.ps1` em UTF-8, `-Xml`, teste 51, armadilhas), banco do par 02c3643 (52: ressalvas, teste, armadilha),
  instalação 99e41b6 (§12: o pwsh por caminho completo, a receita de reaplicar no par A, pwsh pelo MSI), decisões
  845ba41, README 1820326. Verificadores 0. **9ª junção feita pelo Rebite** (`integracao` b2ae3db; frontmatter 0, 27-pastas 24/24; `main` 70a9f73).

- 2026-10-21: 49 (e82dd85, cabeçalho 35da1e6) e 50 (c3f2868) nas páginas, pedido do maestro. `git merge integracao`
  no docs (4219de9). `instalacao.md` reescrita 96972ad (o B com o hub vazio: kit de fora `00,03,04,05,espera`, o git
  com `reset --mixed` e `checkout` só do que tem ponto, o kit do hub `04,08,10`; `core.autocrlf`; só 2 tarefas; o que
  se fez no par A em 2026-10-18; achado da `hub-sincronizador` que não roda, ticket 52); banco do par 517803c (teste e
  medidas do 49); gerador e2f234f (exclude só com `.git`; o 50); decisões b5ad179; README 58b5122. `verificar-pastas`
  rc 0, frontmatter 0. **8ª junção pedida ao Rebite** (depois de ele resolver o 49).

- 2026-10-18: 45 (6494a38) e 46 (8c01cfb) juntados (Rebite; `main` 7d0c25d). `git merge integracao` no docs
  (fast-forward a 8c01cfb). Páginas: banco do par 5b0c155; kit de par 83b880b; pastas e links, fim da resposta e
  roteamento 292bbf2 (id do par de reserva em `.local/par.json`: a divergência do `HUB_PAR_ID` fechou); operação e
  stack 82fec3c; **página nova `instalacao.md`** b810a58 (passo a passo do 26 para o maestro de cada par); arquitetura
  cefca1b, decisões eaddd6c, README e33b71f. `verificar-pastas` rc 0, frontmatter 0. **7ª junção feita pelo Rebite** (`integracao` 7b6c406; frontmatter 0, 27-pastas 24/24; `main` fe55b12).
  Avisados ao maestro: o checkout `C:/Projetos/hub-mcp-banco` está em `ticket-09` (d2a5a40), 6 commits atrás de
  `integracao` do fork (34c3e50); nenhum script põe `HUB_MCP_BANCO_TOKEN` no ambiente do usuário; B com o clone já no
  disco não foi provado (a espera e o 25 tinham o B vazio).

- 2026-10-17 (depois do reinício): `git merge integracao` no docs (48eb75d, `integracao` ca62332: 24 a4fa7e3, evidência
  do Codex do 22 56cd23a, 25 ca62332). Páginas: kit de par a87d81a e 9813220 (o kit ao vivo); **página nova**
  `componentes/prova-do-hub-inteiro.md` ca5126d (25); proxy 138b868 (Codex cliente PASSA, 22811cb; `lido.json` sem
  modelo); infraestrutura 62796e0 (Luna real; `harnesses.mjs`); pastas e links 0596cb4 (`HUB_PAR_ID`: o 24 não mexeu
  no kit; nenhum ticket a põe: não verificado); operação 5c0ed96 (corredor do 25, picos de memória, par novo leva
  minutos); decisões 4e0fdea; arquitetura b555035; MCP do banco 60d440c (o que o 25 mediu); guardas ab39eea (37
  juntado); README b20bf5f. `verificar-pastas` rc 0. **6ª junção feita pelo Rebite** em `integracao` dc514db (docs b20bf5f, 11 páginas). Maestro avisado; o `HUB_PAR_ID` foi anotado por ele no ticket 26. Rebite: verificador 0, 27-pastas 24/24; o 12-busca espera o maestro (memória).

- 2026-10-17 ~16h50: Rebite: 18, 37, 23 e 44 (df6c2e5) juntados; docs da 5ª leva em f640bbd. `git merge integracao`
  fast-forward. 44 nas páginas: pastas e links 7a9740c (topo df6c2e5; código em linha, `./`/`../`, assinatura com
  `nota`, ressalvas do parecer e da 2ª leitura, 24 testes, link para o fim da resposta); MCP do banco 1d9ae1f (o exemplo
  `[Open in Obsidian](<deep link>)` de volta); decisões ff8dbfc; README a71e407. `verificar-pastas` na pasta: rc 0,
  sem avisos (os 2 antigos eram código em linha). A regra "nada de `../` nem `[texto](alvo)` em código" caiu.

- 2026-10-17: 38 e 39 (vistos no log, `integracao` 2d5c528, sem aviso do Rebite): páginas da vigia 8b8f92a, vigia nas
  telas 7a0fbb4, infraestrutura de teste 0a27ccb, esqueleto 439f3eb (comentário do `conteudo.mjs` em dia); README
  1f721f1, arquitetura b8f219f, decisões ceeecee. Ressalva anotada: ponta a ponta 17 e 22-cliente fora do `MODELO_CODEX`
  (o relatório do 38 já diz).
- 2026-10-17: manutenção do 22 (c42ffa0, vista no log): proxy 946c536 (Codex por tabela; Codex cliente segue não
  verificado), infraestrutura 6c04ee6 (22-cliente no `gpt-6.1-sol`), README.

- 2026-10-17 ~17h20: 23 nas páginas: `componentes/kit-de-par.md` nova 631ffb5; operação, arquivar, vigia, harnesses,
  esqueleto, roteamento, infraestrutura (`SO_APP_SERVER`), arquitetura e README (mapas com retomada e kit), decisões.
  **5ª junção pedida ao Rebite** (docs b028a2d, `integracao` 9f122c2; 14 páginas; `pastas-e-links.md` intocada).
- 2026-10-17 ~16h50: 18 e 37 nas páginas: `componentes/retomada.md` nova aa72537; fim da resposta ac0d65a (reescrita:
  anota, `.gravados`, `.shell`, retomada); vigia nas telas e25a50d; esqueleto 80abbee; roteamento 1fb75a7; harnesses
  7f88d73. Falta: 23 (página nova do kit de par + `operacao.md`), depois arquitetura, decisões, README e a 5ª junção.
- 2026-10-17 ~16h20: juntados (vistos no merge, docs 9f122c2 = `integracao`): 18 (dc4ed6a), 37 (ebfbe6c), 23 (9f122c2).
  Documentar nessa ordem.
- 2026-10-17 ~16h10: 4ª leva juntada e verde (`integracao` a7d1517; Rebite). 11 verde (51fa382). Aviso do maestro: a Brasa mexeu em
  `componentes/pastas-e-links.md` no `ticket-44` (dc748bc: tira a divergência do `..`, código em linha fora, linha nova
  da tabela para `./` e `../`, ressalva do wikilink com `./`/`../` ainda lido da raiz). **Quando o 44 juntar**: `git merge
  integracao` no docs; não mexer em `pastas-e-links.md` antes (evita conflito); depois conferir a página pelo código do
  44, linha do topo com o hash, e liberar a forma `[texto](alvo)` em código (`mcp-do-banco.md` pode voltar ao exemplo).
- 2026-10-17 ~16h: 11 (51fa382): MCP do banco 8ef0e36, harnesses, decisões, arquitetura, README (ponta 9d0bc24).
  Divergência achada e avisada ao maestro (entrou no 44, Brasa): o verificador de pastas lê link Markdown relativo a
  partir da raiz do hub e toma `..` por parte com ponto ("não replica"); anotada em `pastas-e-links.md` (b212ce1).
  Nos docs, nada de link com `../` nem `[texto](alvo)` em código até o 44 juntar. **4ª junção pedida ao Rebite**
  (9d0bc24, `integracao` b22b099; 27-pastas, 12-busca, frontmatter). Antes de pedir junção, rodar aqui
  `node agents/code/bin/verificar-pastas.mjs --raiz . agents/code/docs` (rc 0; só os 2 avisos da `pastas-e-links.md`).
- 2026-10-17: suíte da junção com os docs (Rebite): 1 falha no `27-pastas.test.mjs:247`. O exemplo
  `[Open in Obsidian](...)` em `componentes/mcp-do-banco.md:105` (dentro de código) é recusado pelo verificador de
  pastas como link sem `par://`; `agents/code/` não pode ter recusa. Avisos do mesmo tipo em `pastas-e-links.md`
  (espaço cru, `//host`) não falham. **Esperando o maestro**: muda a página (ex.: tirar o `(...)`) ou o verificador pula
  código. Não mexer antes.
  Decisão do maestro: mudar a página (a causa no verificador é o ticket 44, Brasa). Conserto a43decc (a linha 105 em
  palavras; `verificar-pastas` na pasta rc 0, só os 2 avisos da `pastas-e-links.md`); o Rebite juntou em b22b099
  (com a 3ª leva, 98a7ced). Quando o 44 juntar, a forma `[texto](alvo)` em código volta a valer.
- 2026-10-17 ~15h10: 40 (7caed05): roteamento 7994b44, harnesses e426749. 43 (45e34c7): infraestrutura 7650d6b, proxy
  62c74c4, decisões d1e3601 (também 40 e 41), stack 08c34a9, harnesses 923222c, operação 3c76fcf, arquitetura 8f72402,
  README ee3926a. **3ª junção dos docs pedida ao Rebite** (ponta ee3926a, `integracao` 576b462 contida, 9 páginas).
- 2026-10-17 ~14h50: 42 (d298826): fim da resposta d1afa5a, harnesses 2d47295. 41 (e8dde26): gerador 9ed660b, busca
  109687d, guardas 3ede923 (aviso de leitura fora de `agents/code/`), operação 77b0423; README fb278d4.
  **2ª junção dos docs** pedida e feita pelo Rebite: `integracao` 576b462 (docs fb278d4; o 12-busca dela roda na suíte
  do 41/40/43). A 1ª leva (b0ef690) já tinha entrado em d7a8e07. Faltam nas páginas: 40 (7caed05) e 43 (45e34c7).
- 2026-10-17 (depois da janela quieta): `git merge integracao` no `docs`, ponta b0ef690 com c42ffa0 contida; diff
  contra `integracao` só em `agents/code/docs/` (24 arquivos). Nada juntado depois de c42ffa0; 41 em revisão (Fiel).
- 2026-10-17: ticket 17 juntado, e7203b4 (Rebite). Já documentado (`vigia-nas-telas.md`, conferida em e7203b4).
