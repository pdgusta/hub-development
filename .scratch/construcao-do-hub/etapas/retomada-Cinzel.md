# Retomada do Cinzel (construtor, Claude)

Leia antes: `etapas/regras-da-construcao.md` (inteiras), o ticket do momento e esta retomada.

## Ticket 09: MCP do banco, gravar com versão (em revisão com o Fiel)

- Fork `C:/Projetos/hub-mcp-banco`, ramo `ticket-09`: 289ec4c, dd9ddb5, 61a6e70 (base v0.10.0 1a4d53f). O
  `package-lock.json` modificado fica fora dos commits (efeito do `npm install`: tirou o `jose` opcional).
- Hub: worktree `C:/context-hub-wt/ticket-09`, ramo `ticket-09`: ce9790b, 619655f e a junção de `integracao` 33b817a
  em 3d9d0bb.
- Relatório: `etapas/relatorio-09-mcp-do-banco.md`. As decisões do maestro estão nos comentários do ticket 09.
- Testes:
  - Costura A: `cd C:/Projetos/hub-mcp-banco && node scripts/e2e-banco.mjs` (Docker `hub-ensaio-09-f`, 5996, com a
    trava). Deu 12/12.
  - Costura B: `pwsh -NoProfile -File agents/code/test/09-mcp-banco.test.ps1` na worktree (Docker
    `hub-ensaio-09-a/b`, 5996/5997, com a trava, ~3 min). Deu 21 PASSA (`etapas/logs/09-docker-4.log`).
  - Sem Docker: `node --test agents/code/test/09-mcp-banco-sem-docker.test.mjs` (12 PASSA dentro).
  - Upstream: unitários `node --import tsx --test "src/**/*.test.ts"` com `TEMP` em caminho longo dá 272/1; e2e local
    `sh .local/e2e-local.sh` dá 36/7. As falhas são as mesmas da base (separador `\` do Windows).
- Leitura prévia do Fiel (04:43), antes do parecer:
  - Concorrência: duas gravações simultâneas da mesma base viva responderiam as duas "gravado, conflito segue
    aberto". Conserto pensado: é conflito quando, depois da gravação, há folha nova que não estava em `before` nem é a
    nossa (`outcome` em `src/vault.ts`).
  - Ressalvas: o `move_note` com conflito na origem não diz que o destino já foi gravado; o passo 05 remonta um build
    velho mas não religa o MCP que já roda (o código velho segue rodando).
  - A sonda dele: `etapas/logs/sonda-09-fiel.e2e.test.ts`.
- Próximo: o parecer do Fiel, e então os consertos (até duas voltas). Depois do "passa", avisar o Rebite:
  `maestri ask "Rebite" "Cinzel: ticket 09 passou na revisão, ramo ticket-09 (hub) e ticket-09 (fork hub-mcp-banco), testes ..., relatório ..., parecer ..."`.

## Ticket 10: três instâncias, cabeça, regra curta e estado (próximo; código só depois do "passa" do 09)

- Ramo `ticket-10` no fork, a partir de `ticket-09`. No hub, `ticket-10` a partir de `ticket-09`, até o 09 entrar
  em `integracao`; depois, `git merge integracao`.
- Costuras e decisões (a) a (e) aceitas pelo maestro, registradas no ticket 10:
  - Portas: 8796 (escrita do par), 8797 (leitura), 8798 (escrita do cliente). No `.env`: `HUB_MCP_BANCO_URL/TOKEN`,
    `HUB_MCP_BANCO_LEITURA_URL/TOKEN` e `HUB_MCP_BANCO_CLIENTE_URL/TOKEN`.
  - Regra curta completa nas 4 ferramentas de gravação.
  - Cabeça ausente ou acima de 2.000 caracteres: o MCP sobe sem ela e o `instructions` diz "cabeça do AGENTS.md
    indisponível: <motivo>".
  - A validação de frontmatter vale também para nota nova. É feita pelo `HUB_ROOT/agents/code/bin/lib/frontmatter.mjs`
    (`carregarCatalogo` e `analisar`).
  - Estado da vigia: `<hub>/.local/vigia/estado.json`, como combinado com o Trilho (16). O JSON vai como está, menos
    o campo `vistos`. Sem arquivo ou ilegível: "estado indisponível: <motivo>". Com `passada` de mais de 15 min, vai
    junto o aviso "a vigia não roda desde <hora>"; sem `passada`, sem aviso.
- O FastMCP cria cada sessão lendo `this.#options.instructions` (`node_modules/fastmcp/dist/chunk-DMSZ2FEE.js`,
  linhas 1508 e 1680). Um getter no objeto de opções deve reler o `AGENTS.md` a cada sessão; conferir se o FastMCP
  copia as opções.

## Armadilhas

- Rode a trava e a fila: `etapas/trava-pesada.md` e `etapas/fila-pesada.md`. Ao soltar, avise quem o maestro mandar.
- O passo 05 só remontava o fork quando faltava o `dist`. Depois de mudar o `src`, rode `npx tsup` no fork, ou
  confie no `Test-BuildVelho`.
- No e2e, uma chamada por vez: os pedidos usam o mesmo `id` JSON-RPC na mesma sessão.
- O sincronizador do LiveSync funde sozinho conflitos de linhas diferentes. Um conflito de verdade, no teste, é na
  mesma linha.
- `maestri ask` sem barra invertida nos caminhos.
