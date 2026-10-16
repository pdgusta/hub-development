---
titulo: Onde mora o código do próprio hub
ticket: 16
aberta: 2026-10-16
estado: absorvida
---

O Trilho, que constrói o esqueleto, achou uma lacuna. "Arquitetura de pastas" decidiu que a raiz do hub tem só o
`AGENTS.md` e as seis raízes, com a **oficina em `agents/`**, e listou o que mora lá: `skills/`, `machines/`,
`maestro/`, `blocks.md` e `frontmatter/`. Mas o hub também tem **código próprio**: o kit de par, os hooks, o mod do
Claude Code, os scripts da busca e os testes. O spec antigo punha isso em pastas soltas na raiz (`kit/`, `hooks/`,
`mods/`, `busca/`), o que contradiz a raiz decidida. Os repositórios de código de trabalho continuam fora do hub; aqui
é só o código que faz o hub funcionar, que replica igual nas duas máquinas.

Enquanto você decide, o verificador da estrutura só avisa (sem recusar) pasta a mais na raiz, e o Trilho não cria essas
pastas.

## Onde mora o código do hub
id: codigo-do-hub
tipo: escolha
recomendada: A

- A: Cada peça é uma skill com scripts em `agents/skills/<peça>/` (a busca, a vigia, as guardas, o kit de par, a manutenção), com o seu código, os seus testes e o fragmento de hook, como o spec já faz com a vigia e a "nova iniciativa"; não muda o que foi decidido para a raiz nem para `agents/` (e a pasta global de skills continua levando só as de uso geral)
- B: Abrir pastas de oficina novas dentro de `agents/` (`agents/kit/`, `agents/hooks/`, `agents/mods/`, `agents/test/`): código separado das skills, mas amplia o conteúdo de `agents/` decidido
- C: Pastas de código na raiz do repositório (`kit/`, `hooks/`, `mods/`, `busca/`), como o spec antigo: muda a raiz decidida

## Algo mais?
id: algo-mais
tipo: texto
