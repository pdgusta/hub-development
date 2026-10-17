# 28: Pastas locais: o script "nova pasta local", o "tornar local" e a exclusão do git

Type: task
Status: resolved
Etapa: 2 (banco)
Blocked by: 06, 07

**What to build:** A skill "nova pasta local" em `agents/skills/nova-pasta-local/` (o agente a chama, como a "nova iniciativa"), com dois passos. **Nova:** para o sincronizador, cria a pasta com o `index.md` `local: true`, roda o gerador de exclusões e religa o sincronizador. **Tornar local** (pasta que já replicou): para o sincronizador, põe `local: true` no `index.md`, roda o gerador e apaga a pasta do banco pelo CLI do LiveSync, o que tira a cópia da outra máquina e mantém a desta. O gerador (`agents/code/bin/gerar-exclusoes.mjs`, ticket 06) passa a escrever também `.git/info/exclude` com as pastas locais e tudo que tem ponto, por máquina e sem versionar. O `AGENTS.md` ganha a regra curta: pasta local só pelo script. Se o gerador recusar (YAML ilegível), o script para sem religar o sincronizador e mostra o caminho.

**Fonte:** Decisão do Gustavo na rodada `2026-10-16-pastas-locais-depois-do-gerador` (as quatro, A; registro no spec, faixa 1, "Pasta não replicada"); relatório do 06 (`etapas/relatorio-06-gerador-de-exclusoes.md`, "O que vai doer ao ligar"); lição do 02 (o `.livesync/ignore` só vale a partir da partida do CLI). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 06 (Gerador de exclusões), 07 (Banco do par: o par de ensaio com o CLI do LiveSync rodando)

- [ ] com o sincronizador do par A rodando, "nova pasta local" cria a pasta e nada dela (nem o `index.md`) chega ao banco do par A nem ao disco do par B
- [ ] "tornar local" numa pasta que já replicou tira a pasta do banco e do disco do par B e mantém todos os arquivos no disco do par A
- [ ] o gerador escreve `.git/info/exclude`, e `git status` do hub de ensaio não mostra a pasta local nem nada com ponto
- [ ] com um `index.md` de YAML ilegível, o script para, mostra o caminho e deixa o sincronizador parado e avisado

## Comments

- 2026-10-16 ~21h (maestro): publicado pela decisão do Gustavo na rodada `2026-10-16-pastas-locais-depois-do-gerador`. A parte da vigia (rodar o gerador a cada passada e religar) foi para o ticket 16 da construção.

- 2026-10-17 ~02h50 (maestro): reservado para o Trilho, depois do 35 e do Codex do 12 e do 15; começa quando o 07 for resolvido.

- 2026-10-17 ~03h15 (maestro): troca de dono: a Vela faz o 28 agora (o 09 espera a resposta do Gustavo sobre onde mora o fork); o Trilho segue no 35 e no Codex do 12 e do 15.
- 2026-10-17 03h02 (Vela): claimed; worktree C:/context-hub-wt/ticket-28 da ponta de integracao 763813a.

- 2026-10-17 ~03h25 (maestro): aceito o `git rm -r --cached` no "tornar local" (a pasta já versionada sai do git do hub daqui para frente; o histórico guarda as versões antigas, e limpar histórico não entra), proposta da Vela.
- 03h30 (Vela): Docker 14 PASSA, suíte 188/0/8 em fc6c78b; revisão pedida ao Fiel. Relatório etapas/relatorio-28-pastas-locais.md.
- 2026-10-17 05h08 (Vela): Fiel rodada 3 PASSA (Docker 14 PASSA com a trava; sem Docker 9/9; 3 ressalvas no parecer; leitura do Fielzinho pendente). Passa levado ao Rebite.
- 2026-10-17 06h12 (integrador, Rebite): juntado em `integracao`, commit ea6f353 (merge `--no-ff` de `ticket-28` 5436cad, o HEAD da rodada 3 "passa" do Fiel, teto de voltas; sem arquivo em comum com `integracao`). Testes, com a trava, junto com o 09 (9453e3e): `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis = 202, 194 verdes, 8 pulados, 0 falhas (16 min); `git status` limpo. O Docker `28-pastas-locais.test.ps1` não foi repetido: o Fiel o rodou com a trava em 5436cad (14 PASSA), e os arquivos dele não mudam com a junção. Ressalvas do parecer: o Docker passa `-Titulo 'Rascunhos de A'` sem conferir o título (o teste sem Docker confere); o histórico do git guarda as versões antigas da pasta tornada local (aval do maestro; a skill avisa); a leitura do Fielzinho ficou pendente (achado 3 da rodada 1 e rodadas 2 e 3), e se ele achar algo vira ticket seguinte. **Resolvido.**
