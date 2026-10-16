# Etapa zero: provas de risco (brief do maestro, 2026-10-16)

Leia antes `..\regras-da-construcao.md`. Decidido na rodada `2026-10-16-etapa-0-receita` (ticket 16).

Tickets: `issues\01-prova-dois-couchdb-replicando.md`, `02-prova-pastas-com-ponto-fora-do-livesync.md` e
`03-prova-hooks-do-codex-em-acesso-total.md`.

## O que provar

Três peças nunca provadas que podem derrubar o desenho (lições do Prisma, `revisao\licoes\prisma.md`):

1. **Dois CouchDB replicando entre si com os documentos do LiveSync** (ticket 34: um CouchDB em cada par, replicação
   mestre-mestre; o spec chama de S3: "uma replicação de envio em cada um"). Provar: nota criada, editada e apagada no
   par A chega ao B e vice-versa; colisão vira conflito visível nas duas pontas, nada sobrescrito; com E2EE e caminho
   ofuscado ligados (a escolha aceita).
2. **Exclusão de pastas com ponto aninhadas no LiveSync** (ticket 48, item 6: `projeto/.venv/` e `projeto/.cache/`
   vazaram para o banco e para os discos). Provar: com `.livesync/ignore` (linhas `.*` e `.*/`, ou o que funcionar),
   nada com ponto em qualquer nível chega ao banco nem ao outro disco, inclusive na partida do CLI.
3. **Hooks do Codex em acesso total** (ticket 14 decidiu `danger-full-access`; a bancada só provou `workspace-write`).
   Provar: com `CODEX_HOME` de ensaio, os hooks `SessionStart`, `PreToolUse` (recusa no `apply_patch`) e `Stop` (devolve e
   solta) rodam em `codex exec --sandbox danger-full-access`; e o `notify` dispara.

## Quem faz o quê

- **Construtor das provas 1 e 2** (banco): ramos `ticket-01` e `ticket-02`. Material: `C:\Projetos\spike-livesync` (o spike do
  ticket 30, com o código do LiveSync em `livesync-src`; o ticket 48 diz como o CLI do commit `14141446` foi montado), tickets 30, 33, 34, 47, 48 e o bloco do Worker 4
  no `spec.md`. CouchDB `3.5.2` em contêineres `hub-ensaio-00-a` e `hub-ensaio-00-b`.
- **Construtor da prova 3** (hooks do Codex): ramo `ticket-03`. Material: tickets 14 e 44, a bancada de acesso
  (`C:\Projetos\context-hub\.scratch\context-hub\bancada-acesso-codex.md` e `bancada-acesso-relatorio.md`), e os blocos dos Workers 2, 6 e 8 no `spec.md`. **Aval do Gustavo:** copiar só o arquivo de login do Codex
  (`%USERPROFILE%\.codex\auth.json`) para o `CODEX_HOME` de ensaio durante a prova e apagá-lo ao fim (confirme no
  relatório que apagou). Nada além desse arquivo sai da pasta real.

## Como (o pedido do Gustavo)

"Testar porém já tentando prever dificuldades ao ligar o resultado final com o que foi testado." Então:

- Use a forma de configuração que a construção vai usar (os mesmos arquivos, nomes e variáveis que o spec descreve
  para as faixas 4, 5, 7 e 8), não um arranjo só de teste. Os scripts das provas ficam no seu ramo, em `provas/`, para
  as etapas seguintes reaproveitarem.
- Cada prova termina com uma seção **"O que vai doer ao ligar"**: o que a prova não cobriu, o que muda quando juntar com
  as outras peças, o que depende da segunda máquina.

## Relatório

Cada construtor grava a sua parte em
`C:\Projetos\context-hub\.scratch\construcao-do-hub\etapas\00-provas\relatorio-<banco|codex>.md`: para cada prova,
passou / falhou / parcial, a evidência (comando, saída, arquivo), o que vai doer ao ligar, e o que muda no spec se
falhou. Contêineres e o login copiado apagados ao fim, com a confirmação no relatório.
