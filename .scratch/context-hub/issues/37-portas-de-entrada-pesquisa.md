# Portas de entrada: pesquisa

Type: research
Status: resolved

## Question

Para cada porta candidata de "Portas de entrada do hub", o que a fonte primária diz sobre onde a
sessão abre, o que carrega sozinha, o que alcança e como acha o resto? Sem inferência: o que a fonte
não disser fica "não verificado", e o que só um teste resolve fica "precisa de teste". Pedido do
Gustavo em 2026-10-10 (resposta à R20).

Portas: (1) harness na raiz do hub; (2) harness numa subpasta; (3+4) workspace e papel do Maestri;
(5) Obsidian; (6) Claude sem disco (app, claude.ai, Cowork, conectores); (7) cliente pelo MCP de um
par; (8) sessão num repositório de código fora do hub.

## Comments

- 2026-10-10: sete subagentes, um por porta (3 e 4 juntas), só fonte primária lida em texto bruto
  (curl), com citação literal. Resultados em `exploracao/anexos/pesquisa-37-portas/`.

## Answer

Relatórios por porta, com citações, "Não verificado" e "Precisa de teste":
`exploracao/anexos/pesquisa-37-portas/porta-*.md` (2026-10-10, fonte primária lida em texto bruto).

1. **Harness na raiz:** o Claude Code carrega no início os `AGENTS.md` da pasta e das de cima (só sem
   `CLAUDE.md`), os de subpasta quando lê ou edita ali; `@import` até 4 níveis. O Codex lê do "project
   root" até a pasta atual, até 32 KiB. O Copilot CLI lê raiz do git, cwd e o caminho do arquivo; no VS
   Code o `AGENTS.md` aninhado é experimental e vem desligado.
2. **Harness numa subpasta:** o Claude Code carrega os `AGENTS.md` de cima; restringir leitura a uma
   pasta existe (`blockReadsOutsideWorkingDirectories`, sandbox), mas não cobre o Bash. O Codex só lê
   o `AGENTS.md` da raiz se ela for "project root" (por padrão, pasta com `.git`; ajustável com
   `project_root_markers`). O Copilot lê "Git root and cwd"; no VS Code o da raiz exige `.git`.
   **O hub não tem `.git`** (a verdade está no CouchDB), então Codex e Copilot numa subpasta não
   chegam ao `AGENTS.md` da raiz sem configuração.
3. **Maestri:** o terminal abre na pasta do workspace; com papel, em `.maestri/roles/<id>/`, onde o
   Maestri grava `CLAUDE.md` e `AGENTS.md` (o prompt do papel, sem importar o `AGENTS.md` da raiz) e
   `role.json`. Pela doc do Claude Code, esse `CLAUDE.md` faz o `AGENTS.md` do hub não ser lido, salvo
   com `claude-md-and-agents-md`. Papéis ficam em `~/.maestri/preferences.json` e partituras em
   `~/.maestri/partituras/`; não há pasta configurável, só "Discover Roles" (importa `role.json` da
   pasta de trabalho) e importar e exportar partituras.
4. **Obsidian:** qualquer pasta abre como cofre; a ajuda desaconselha cofre aninhado; links são
   atualizados ao renomear arquivo. O LiveSync sincroniza todos os arquivos normais; pastas com ponto
   só pela Hidden File Sync; mover é por arquivo (grava o destino e apaga a origem) e a doc **não promete
   suporte completo a renomear pasta**. Celular é suportado, com HTTPS.
5. **Claude sem disco:** conector remoto parte sempre dos servidores da Anthropic, então um MCP só da
   tailnet não é alcançável; a saída oficial para rede privada são os MCP tunnels (Enterprise, preview).
   O MCP local do Desktop parte da máquina, mas não existe no celular nem na web. O Cowork lê e grava
   pasta local pelo Desktop, mas desde 2026-10-06, no Pro e no Max, a sessão roda na nuvem; ler
   `AGENTS.md` não consta. Projetos e memória são cópias.
6. **Cliente pelo MCP:** o es617 serve HTTP em `/mcp`, com um único token Bearer estático;
   `READ_ONLY` vale para a instância inteira; tem `read_note`, `list_folders`, `list_notes` e
   `search_notes` (contradiz a pesquisa 26, que dizia não haver busca de texto; reconferir).
   `MCP_INSTRUCTIONS_FILE` vira o `instructions` do MCP, o único canal que chega sem ação do usuário:
   o Claude Code corta em 2.048 caracteres, e o Codex recomenda os primeiros 512 autossuficientes. Nó
   efêmero do Tailscale some de 30 a 60 minutos depois da última atividade; grants negam por padrão,
   mas a política padrão "allow-all" anula a restrição.
7. **Repositório fora do hub:** o `~/.claude/CLAUDE.md` aceita `@` com caminho absoluto; o
   `AGENTS.md` de um `--add-dir` não carrega; skill pode ser link simbólico (junction não consta). O
   Codex sempre lê `~/.codex/AGENTS.md`. O Copilot CLI só aceita `@` relativo, mas tem
   `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` e `COPILOT_SKILLS_DIRS`.

**Precisa de teste:** cerca de 35 itens listados nos relatórios; nada foi testado.
