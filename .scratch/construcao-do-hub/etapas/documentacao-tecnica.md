# Documentação técnica do hub (desde 2026-10-17)

O Gustavo pediu um agente só para documentar, a nível técnico, **tudo** o que a construção cria: MCP, hooks, scripts,
skills, kit, stack. A documentação serve a quem mudar o hub depois (gente ou agente): lendo-a, entende cada peça sem
reler o código inteiro. O documentador é o **Lume**. Ele não atrapalha a execução nem cria burocracia: ninguém espera
por ele, nenhum ticket depende dele, ele não revisa nem aprova nada.

## Onde a documentação mora

- No repositório do hub, `C:\context-hub`, em **`agents/code/docs/`** (o código está em `agents/code/` e
  `agents/skills/`; o `paths.yml` dá `tipo: null` a `agents/code/**`, então os `.md` daqui não levam frontmatter do hub).
  Ela replica com o hub e vai junto com o código para a segunda máquina.
- O fork do MCP do banco (`C:\Projetos\hub-mcp-banco`) é documentado **aqui**, na página dele, citando caminhos e
  commits do fork; nada se escreve no fork.
- Ramo e worktree próprios: `docs`, em `C:\context-hub-wt\docs`, a partir da ponta de `integracao`. A documentação
  descreve o que está em `integracao` (o que foi juntado); ramo aberto de ticket não entra, salvo como "a caminho".

## O que se escreve (nível de referência técnica)

```
agents/code/docs/
  README.md            índice, mapa das peças e como ler esta pasta
  arquitetura.md       visão geral: par A e B, CouchDB cifrado, LiveSync CLI e a vista .md, MCP do banco (fork),
                       busca, vigia, guardas, hooks, kit de par e de cliente, proxy; fluxo de uma gravação e de uma
                       leitura, de ponta a ponta, com diagrama em texto (mermaid)
  stack.md             linguagens e versões (Node, PowerShell, TypeScript do fork), dependências e de onde vêm,
                       Docker e imagens, portas, variáveis de ambiente (.env de cada passo), caminhos fixos
  harnesses.md         como cada peça liga em Claude Code, Codex e Copilot: eventos de hook, matchers, settings,
                       linhas de MCP, diferenças entre os três (ex.: hífen vira sublinhado no Codex), o que cada um
                       aceita ou descarta, com a fonte
  operacao.md          runbook: subir e descer o par, rodar cada teste (comando, variáveis, trava), recuperar um
                       binário, ler o estado da vigia, o que fazer quando a memória não deixa
  decisoes.md          índice das decisões técnicas: uma linha por decisão, com o ticket ou a rodada de origem
  componentes/<peça>.md uma página por peça
```

Cada página de componente, sempre nesta ordem:
1. **Para que serve** (duas linhas) e os tickets que a construíram.
2. **Onde mora**: arquivos e pastas, com o papel de cada um; ponto de entrada.
3. **Como funciona**: o fluxo, passo a passo, com os nomes reais de funções, scripts e arquivos de estado.
4. **Interfaces**: parâmetros de linha de comando, ferramentas MCP (nome, entrada, saída, erros), eventos de hook,
   formato dos arquivos que lê e grava (com exemplo), códigos de saída.
5. **Configuração**: variáveis, `.env`, portas, padrões.
6. **Decisões e porquês**: o que foi escolhido e por quê, com link para o ticket ou a rodada.
7. **Limites conhecidos e ressalvas** (dos pareceres e relatórios).
8. **Testes**: quais arquivos, como rodar, o que provam, o que é pesado (Docker, harness real).
9. **Armadilhas**: o que já derrubou alguém (achados comuns, consertos de rodada).

Regra de ouro: **só o que se confere no código, no teste, no relatório ou no parecer**; o que não conferiu, marca
"não verificado". Nada inventado, nada de dado de cliente nem dado pessoal.

## Fontes

O código em `integracao` (hub e fork), os testes, os relatórios e pareceres em
`C:\Projetos\context-hub\.scratch\construcao-do-hub\etapas\`, os tickets em `...\issues\` (`## Comments`), o spec
(`spec.md`, `spec-partes/`), as regras (`regras-da-construcao.md`, com os achados comuns) e
`etapas/registro-de-juncoes.md`. Doc externa (Claude Code, Codex, Copilot, LiveSync, CouchDB) por curl na fonte primária,
com o link na página.

## Ritmo

- **Fase 1 (atrasado):** documentar tudo o que já foi juntado, pela ordem das dependências: esqueleto e hub de ensaio
  (04), frontmatter e verificador (05, 27, 32, 33), gerador de exclusões (06), banco do par (07, 08), pastas locais (28),
  busca (12, 13), guardas (14, 15), roteamento (19, 34), acervo (20, 31, 35), MCP do banco (09, 10, fork), vigia (16, 39),
  vigia nas telas (17), arquivar e cópia diária (21), proxy e kit de cliente (22), provas da etapa zero (01-03),
  infraestrutura de teste (29, 30, 36, 38). Uma página por vez, com commit por página.
- **Fase 2 (em dia):** a cada junção, o Rebite manda uma linha ao Lume ("ticket NN juntado, <hash>"). O Lume põe na sua
  fila e atualiza a página no seu ritmo. A fila e o progresso ficam em `etapas/estado-documentacao.md`.
- **Junção dos docs:** a cada umas cinco páginas (ou quando o Lume pedir), o Rebite junta o ramo `docs` em
  `integracao` como um ticket só de documentação: confere que o diff só toca `agents/code/docs/`, roda o
  o verificador de frontmatter e o `27-pastas.test.mjs` (desde o 41 a busca não indexa `agents/code/**`, então o `12-busca` não muda com os docs); sem suíte inteira, sem revisão do
  Fiel. Antes de pedir, o Lume faz `git merge integracao` no `docs`.

## Como o Lume trabalha

- Só lê código e roda comando leve de leitura (git log/show, grep, `--help`, `-WhatIf`). **Nunca** roda teste pesado,
  Docker, harness real, `npm install`, nem entra na fila da trava. Não muda código nem ticket de ninguém.
- Pergunta a um construtor só quando código, teste e relatório não bastam: uma pergunta curta por vez, sem esperar a
  resposta para seguir com outra página. Nunca pergunta ao Fiel nem ao Rebite sobre revisão.
- Achou defeito ou contradição entre código e relatório: anota na página ("divergência: ...") e avisa o maestro numa
  linha; não conserta.
- Até um subagente comum e três Haiku por vez, como os outros (regras): bom para varrer arquivos e conferir formatos.
- Contexto acima de 40%: grava `etapas/retomada-Lume.md` e diz "Lume: salvo para limpar".
