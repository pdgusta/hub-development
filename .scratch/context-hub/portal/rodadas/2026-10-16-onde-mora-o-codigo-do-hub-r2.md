---
titulo: Onde mora o código do próprio hub (2)
ticket: 16
aberta: 2026-10-16
estado: absorvida
---

Você perguntou qual é a diferença entre tudo virar skill e o código ficar só em `agents/`.

**Funcionar, os dois funcionam igual.** O hook, o mod e o kit rodam pelo caminho do arquivo, esteja onde estiver. A
diferença está em **quem lê** e **com o que se mistura**:

- **Skill** é uma pasta com um `SKILL.md` (nome e descrição, com frontmatter conferido pelo verificador) e os scripts
  ao lado. É o formato que Claude Code, Codex e Copilot reconhecem: quando a pasta está ligada a um harness, a descrição
  entra em toda sessão e o agente decide sozinho usá-la. O `SKILL.md` é o **manual para o agente**.
- **Pasta de código** em `agents/` só guarda arquivos que o harness ou o kit executam. Nenhum agente a vê como skill.

Pense numa cozinha: a skill é a **ficha de receita** que o cozinheiro lê e decide seguir; o hook é o **detector de
fumaça** ligado na fiação, que ninguém lê e que só dispara. Guardar o detector no fichário de receitas funciona, mas
mistura as coisas.

O que isso muda na prática:

1. **Quem chama cada peça.** A busca, a "nova iniciativa", o `vigia recuperar` e o arquivar são chamados por um
   agente: para eles o `SKILL.md` é o manual de uso. Já os hooks, o mod do Claude Code, o kit de par, o verificador e os
   testes ninguém chama numa sessão, quem os roda é o harness ou o kit. Como skill, cada um levaria um `SKILL.md` que
   nenhuma sessão lê, porque pelo spec só as skills de uso geral entram na pasta global dos harnesses.
2. **A guarda do acervo.** `agents/skills/` é onde mora o acervo que a guarda protege (a família `maestro-*`, as
   skills de papel, a "nova iniciativa"). Com o motor ali dentro, a guarda e a tabela de roteamento precisam separar,
   pasta por pasta, o que é instrução e o que é motor.
3. **O que já foi decidido.** "Arquitetura de pastas" fixou o conteúdo de `agents/` (`skills/`, `machines/`,
   `maestro/`, `blocks.md`, `frontmatter/`). Só a A não acrescenta nada ali.
4. **Hoje.** O Trilho deixou, provisórios, `agents/bin/verificar-hub.mjs` e `agents/test/` (a forma da B). O que você
   escolher, ele move.

**A recomendação mudou** desde a rodada anterior (era tudo como skill). Sua pergunta me fez separar quem chama cada
peça: o motor não tem leitor para o `SKILL.md`, e misturá-lo com o acervo complica a guarda. Por isso agora recomendo a
C.

## Onde mora o código do hub
id: codigo-do-hub
tipo: escolha
recomendada: C

- A: Tudo vira skill: cada peça em `agents/skills/<peça>/` (busca, vigia, guardas, kit de par, manutenção, verificador), com `SKILL.md`, scripts, fragmentos de hook e testes juntos; `agents/` fica como decidido, mas o motor divide pasta com o acervo e cada peça leva um manual que ninguém lê
- B: Só código em `agents/`, nada vira skill: pastas novas `agents/kit/`, `agents/hooks/`, `agents/mods/`, `agents/bin/` e `agents/test/`, sem `SKILL.md`; nem a busca nem a "nova iniciativa" teriam manual para o agente
- C: Meio a meio pelo critério "quem chama": o que um agente chama vira skill em `agents/skills/<peça>/` (busca, "nova iniciativa", `vigia recuperar`, arquivar); o que só o harness ou o kit roda (hooks, mod do Claude Code, kit de par, verificador, testes) vai numa pasta nova, `agents/code/`, com `hooks/`, `mods/`, `kit/`, `bin/` e `test/` dentro; acrescenta uma única pasta a `agents/`
- D: Pastas de código na raiz do repositório (`kit/`, `hooks/`, `mods/`, `busca/`), como o spec antigo; muda a raiz decidida

## Algo mais?
id: algo-mais
tipo: texto
