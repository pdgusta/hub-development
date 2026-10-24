# Retomada do Malho (construtor do par B)

## Ticket 53: entregue

Relatório `etapas/relatorio-53-clone-do-fork-com-submodulo.md`; ramo `ticket-53` (e4ba4b5), não juntado. Armadilhas do
53: a mensagem de erro do pwsh quebra pela largura do console (`Test-NaSaida` compara sem espaço); o erro de uso do
`npm ci` vem no começo da saída, o do build no fim.

## Ticket 54: em curso

- **Ticket:** `issues/54-busca-dentro-do-vault-pesa-no-cli.md`, brief `etapas/brief-54-par-b.md` (valem as diferenças
  do par B do brief do 53: `C:/context-hub` só leitura, par rodando intocado, sem junção nem push, roteiro sem commit).
- **Ramo/worktree:** `ticket-54` em `C:/context-hub-wt/ticket-54`, a partir do `ticket-53` (e4ba4b5). `claimed`.
- **Desenho (meu, a pôr no relatório):**
  - Chave `HUB_BUSCA_DIR` no `.env` (no modelo `env/03.env`: `C:\hub-par\busca`), no padrão do `HUB_MCP_BANCO_DIR`
    (pasta da peça, com a instalação e o `estado`).
  - `03-busca.ps1` ganha `-EnvFile`. A pasta vem do `HUB_BUSCA_DIR` do `.env`; sem `.env`, do ponteiro
    `<hub>\.local\busca.json` (`{ "dir": ... }`); sem nenhum dos dois, recusa. Também recusa pasta dentro do hub. Se há
    `<hub>\.local\busca` (par antigo), move a pasta para o lugar novo (rename, sem npm ci); se o destino já tem a busca,
    apaga a antiga. Grava o ponteiro.
  - O `instalar.ps1` passa `-EnvFile` ao 03.
  - `iniciar.ps1` e `relatorio.mjs` acham a pasta pelo ponteiro; sem ponteiro, usam o `.local\busca` antigo (com aviso).
    `HUB_BUSCA_OHS` segue como desvio do pacote. O `estado` (`XDG_CACHE_HOME`) e o `relatorio.json` vão para
    `<pasta>\estado` e `<pasta>\relatorio.json`. Só com `HUB_BUSCA_OHS` e sem pasta o estado fica em `.local\busca`,
    como antes (testes).
  - O índice (`<hub>\.obsidian-hybrid-search.db*`, 3 arquivos) fica na raiz do vault: o obsidian-hybrid-search 0.16.2
    fixa esse caminho (`dist/src/config.js`, `dbPath = OBSIDIAN_VAULT_PATH/.obsidian-hybrid-search.db`).
  - Pela varredura, `proxy.psm1`, `ligar-cliente.ps1` e `08-harnesses.mjs` só usam a rota ou o nome `busca`, não o
    caminho: não mudam.
- **Feito:** commits dc6c0b0 (código e testes) e 43ff3f1 (docs, `SKILL.md`, guia §10 "Par já instalado") no
  `ticket-54`. Roteiro do par B: nota no passo 4 e seção "Depois do ticket 54" (sem commit). `12-kit-busca` sozinho: 7/7
  (vermelho antes: 7/7 falhando, `-EnvFile` não existia). O `estado` só aparece quando o pacote grava PID/log (não no
  `serve --foreground`): a asserção dele saiu; o `XDG_CACHE_HOME` não é verificado por teste. Ajudante novo
  `pacoteDoEnsaio` em `12-busca/servidor.mjs`, usado pelo 12-busca, 13-gemini e `13-gemini/teste-unico.mjs`;
  `22-proxy.test.ps1` (Docker) passa `-EnvFile` ao 03, sem rodar (não rodei Docker).
- **Fim:** consertos da revisão em a9f1b4d. 12-kit-busca 7/7, 12-busca 9/9, 13-gemini 4/4 sozinhos; suíte 368/12 falhas
  de ambiente. Relatório `etapas/relatorio-54-busca-fora-do-vault.md`; comentário no ticket.
- **Próximo passo:** nada; 54 entregue ao maestro. Esperar a junção ou um pedido de conserto.
