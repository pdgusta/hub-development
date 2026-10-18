# 47: O projeto do hub dentro do próprio hub (`operations/hub-development`)

Type: task
Status: needs-triage
Etapa: depois do 26 (os dois pares de pé)
Blocked by: 26

**What to build:** Decisão do Gustavo (2026-10-17 ~22h45, Maestri Chat, thread roxa): o projeto que cuida do context
hub (hoje `C:\Projetos\context-hub`, git só local) passa a morar **dentro do hub**, em **`operations/hub-development`**,
para que o maestro de cada par continue o trabalho de qualquer máquina (o hub replica entre os pares). Antes ele tinha
pensado num repositório privado à parte; mudou de ideia ("por enquanto").

O que migrar e como (a desenhar neste ticket, com uma rodada ao Gustavo se mudar decisão):
1. **Só o que está vivo**, não o repositório inteiro: hoje são ~11.700 arquivos versionados (159 MB de git; laços de
   pesquisa com catálogos de 10 MB, capturas, logs). Um par novo leva minutos para receber ~530 arquivos (25): levar
   tudo travaria a replicação. Candidatos: `AGENTS.md` desta frente, a retomada do maestro, as regras e o fluxo
   (`regras-da-construcao.md`, `juntar-tickets.md`, `revisao-em-dupla.md`), os tickets abertos e o índice dos
   resolvidos, o spec, o glossário e os ADRs, o roteiro do 26, o diário da construção. O resto fica como arquivo
   histórico aqui (ou num `_archive/` enxuto).
2. **Forma do hub:** cada `.md` em `operations/**` segue o frontmatter do tipo (`paths.yml`) e passa nos verificadores;
   HTML, PNG e JSON grandes não entram (ou entram como binário pequeno, abaixo do limite).
3. **A memória do maestro:** as memórias deste projeto ficam hoje no perfil do Claude desta máquina
   (`~/.claude/projects/C--Projetos-context-hub/memory/`). Viram notas em `operations/hub-development/` (ou o acervo
   do maestro em `agents/maestro/`), para o maestro do outro par saber o mesmo.
4. **Onboarding do maestro do par B:** uma retomada que ensina o maestro de lá a assumir tudo o que o maestro daqui
   sabe para orquestrar o context hub (Maestri, recrutas, fluxo do Matt Pocock, regras, mandato, armadilhas).
5. **O que acontece com `C:\Projetos\context-hub`:** fica só leitura (histórico) depois da migração.

**Relacionado:** ticket 48 (correio entre os maestros dos dois pares).

- [ ] lista do que migra e do que fica, aprovada
- [ ] `operations/hub-development/` no hub, verificadores verdes, replicado aos dois pares
- [ ] memórias e onboarding do maestro lá; o maestro do par B retoma por eles

## Comments

- 2026-10-17 ~22h50 (maestro): publicado pela decisão do Gustavo.
