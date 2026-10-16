# 28: Pastas locais: o script "nova pasta local", o "tornar local" e a exclusão do git

Type: task
Status: ready-for-agent
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
