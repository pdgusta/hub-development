# Montar: CouchDB, LiveSync e MCP

Type: research
Status: resolved

## Question

Como montar o caminho O1 nas duas máquinas: CouchDB como verdade, o plugin LiveSync
(vrtmrz/obsidian-livesync) fazendo do vault a vista de mão dupla, e o agente gravando no mesmo banco
por um MCP (es617/obsidian-sync-mcp ou alternativa)? Onde o servidor pode morar (numa das máquinas,
container, VPS, serviço gerenciado), como as máquinas o alcançam, como a busca do agente entra (sobre
o banco ou sobre o vault), como a gravação do agente respeita a revisão, como a colisão aparece para
o Gustavo, e o que falta construir.

Pesquisa de **montagem**, não de eliminação (Gustavo, 2026-10-04: "achar oportunidades para chegar
no objetivo ... sem objeções"). Lacuna vira "o que falta montar", com opções e esforço. Nenhum
critério além das decisões dele:
- duas máquinas Windows nativas, NTFS ("Windows ou WSL");
- agentes Claude Code, Codex e Copilot (critério 1 do destino);
- a verdade num banco e o `.md` como vista editável no Obsidian, com volta ao banco ("Markdown:
  vista ou fonte da verdade");
- nada diverge em silêncio, com proteção contra edição concorrente (critérios 4 e 5; garantias de
  "Divergência e edição concorrente").
Servidor é permitido. Recursos já disponíveis, não obrigatórios: GitHub privado e Tailscale ("Ligar
as máquinas com segurança"). Fonte primária, com o que não foi conferido marcado "não verificado";
nada instalado. Origem: R7 de "Como a verdade viaja entre as máquinas".

## Comments

- 2026-10-04: lançada a pedido do Gustavo (R7: "1 pesquisa para cada caminho"). Relatório em
  `exploracao/anexos/pesquisa-26-montagem.md`.

## Answer

Relatório completo: [`pesquisa-26-montagem.md`](../../../exploracao/anexos/pesquisa-26-montagem.md) (2026-10-04).

- **Peças prontas:**
  - CouchDB, com MSI para Windows e opção de serviço;
  - plugin LiveSync, com merge de três vias e diálogo de conflito;
  - es617/obsidian-sync-mcp, por HTTP (npm, GHCR);
  - os três agentes aceitam MCP por HTTP.
- **CLI oficial do LiveSync** (conferido por mim no
  [README](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/src/apps/cli/README.md)):
  `mirror` faz *"Bidirectional sync between the local database and ... the actual vault"* sem o
  Obsidian aberto; tem também `cat`, `put` e `push`/`pull`. Monta-se a partir do código-fonte ou pelo
  Docker.
- **Lacuna principal:** o MCP grava por cima (conferido por mim no
  [README](https://raw.githubusercontent.com/es617/obsidian-sync-mcp/main/README.md): *"No conflict
  resolution ... last write wins"*).
  - Montagem: um fork ou PR pequeno que passe a revisão-base (`conflictBaseRev` da biblioteca do
    LiveSync), fazendo a escrita atrasada virar um ramo de conflito que o LiveSync mostra. Esforço
    de 1 a 2 dias. Não testado.
  - Alternativa pronta: odiak/livesync-workers, que exige hash na escrita e tem busca, mas roda só
    na Cloudflare e exige o E2EE desligado.
- **Onde o servidor mora:** recomendado começar num container numa das máquinas, alcançado pelo
  Tailscale (o compose oficial tem perfil `tailscale`). As outras opções:
  - CouchDB nativo como serviço;
  - um CouchDB em cada máquina com replicação nos dois sentidos;
  - VPS ou Fly.io;
  - serviço gerenciado.
- **Busca:** buscar no vault em disco com as ferramentas da varredura 21 e gravar pelo MCP. As outras
  opções são a pasta espelho do CLI ou uma busca dentro do MCP (3 a 7 dias).
- **Colisão para o Gustavo:** o diálogo de merge e o aviso no arquivo ativo do LiveSync, que
  persistem até a resolução.
- **Falta construir**, cada item de horas a 2 dias, salvo a busca: a guarda de revisão, subir o
  servidor, ligar os agentes, a busca, um aviso de conflito para o agente, a validação no Windows e o
  backup.
- **Não verificado:**
  - MCP e CLI no Windows nativo (o CI é só Ubuntu);
  - o efeito do `conflictBaseRev` num CouchDB remoto;
  - o plugin offline;
  - a replicação nos dois sentidos com os documentos de controle do LiveSync.
