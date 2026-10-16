# Hub no WSL: comportamento

Type: research
Status: resolved

## Question

Como o Obsidian, o Maestri, os três harnesses (Claude Code, Codex, OpenCode), o git e as candidatas à
camada de busca lidam com um hub guardado dentro do WSL e acessado pelo Windows, e vice-versa?
Inclui servir SSH a partir do WSL comparado com o Windows (pergunta do Gustavo na Q15). Seguir o
protocolo da §10.4 da exploração, citando fontes primárias.

## Answer

Relatório completo: [`pesquisa-03-hub-no-wsl.md`](../../../exploracao/anexos/pesquisa-03-hub-no-wsl.md)
(2026-10-01, docs, repositórios e issues oficiais; nada testado; 13 lacunas, 44 consultas).

- **Regra da Microsoft:** guardar os arquivos do lado de quem trabalha neles. Cruzar a fronteira
  (`/mnt/c` ou `\wsl$`) passa pelo 9P, é "Slow", e a doc manda evitar `/mnt/c` para repositórios git.
- **Detecção de mudanças não atravessa a fronteira em nenhum sentido** (WSL #4739 e #7674, abertas).
  Watchers de candidatas à busca mandam usar polling nesses casos.
- **Obsidian (Windows) com cofre em `\wsl.localhost`:** sem suporte oficial (pedido aberto desde
  2020), relatos de erro de watch contraditórios. Com cofre no NTFS, mudanças externas atualizam sozinhas.
- **Claude Code:** roda nos dois; abrir arquivos do WSL pelo Windows "is slow and breaks file watching".
- **Codex:** recomenda agente nativo do Windows com projeto no NTFS; issues abertas do sandbox nativo
  com projeto em `\wsl.localhost`.
- **OpenCode:** recomenda rodar dentro do WSL; aceita `/mnt/c`, sugere ext4; issues de `\wsl$` fechadas
  como not planned.
- **Maestri:** tem ambiente WSL próprio (caminhos em formato Linux); comportamento de notas, árvore e
  busca num workspace WSL não documentado.
- **git no cruzamento:** fim de linha (`.gitattributes`), `core.fileMode`, `safe.directory` falha em
  diretórios WSL vistos pelo Git for Windows, fsmonitor recusa repositório em rede.
- **SSH dentro do WSL:** NAT por padrão (portproxy ou modo mirrored); WSL desliga ocioso (15 s por
  distro, 60 s a VM; configurável com -1); systemd não mantém a instância viva.
- **OpenSSH Server do Windows:** nativo e atualizado pelo Windows Update; pegadinhas: arquivo de chaves
  próprio para administradores, Entra ID sem login por chave, sessão por chave sem credencial para
  fora, shell padrão `cmd.exe` (com "known issue" de `git clone` por SSH), `wsl.exe` dentro de sessão
  SSH com issue aberta (WSL #9231).
- **Lacunas principais:** Obsidian atual em `\wsl.localhost`; números de desempenho para o tamanho do
  hub; Maestri em workspace WSL.
