# Montar: Dolt como servidor central

Type: research
Status: resolved

## Question

Como montar o caminho O2: Dolt como banco versionado central (`dolt sql-server`, DoltHub ou
equivalente), com as duas máquinas trabalhando nele e também offline (pull/push)? Como o agente
acessa (MCP, CLI; o beads é referência), como se monta a vista `.md` de mão dupla (o obsidian-beads é
referência do padrão), como a colisão aparece, como a busca do agente entra, e o que falta construir.

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
  `exploracao/anexos/pesquisa-27-montagem.md`.

## Answer

Relatório completo: [`pesquisa-27-montagem.md`](../../../exploracao/anexos/pesquisa-27-montagem.md) (2026-10-04).

- **Núcleo pronto no Dolt:**
  - servidor com vários clientes, instalador Windows;
  - clone, pull e push para trabalhar offline;
  - colisão por célula que para e avisa, com pull com colisão desfeito sozinho;
  - caso de uso oficial "Offline First".
- **Acesso dos agentes pronto:**
  - o `dolt sql-server` tem bloco `mcp_server` na configuração (conferido por mim na
    [documentação](https://docs.dolthub.com/sql-reference/server/configuration));
  - o `dolt-mcp` existe como binário avulso, em stdio ou HTTP, com mais de 40 ferramentas e build
    Windows (conferido no
    [README](https://raw.githubusercontent.com/dolthub/dolt-mcp/main/README.md)).
- **Montagem recomendada:** um servidor local por máquina, e os agentes falam sempre com
  `localhost`. Um sincronizador faz pull e push contra um ponto de encontro, com estas opções:
  - o servidor da outra máquina pela tailnet;
  - o GitHub privado;
  - DoltHub ou DoltLab;
  - S3 ou R2.
  Offline vira só "sync atrasado".
- **Colisão para o Gustavo:** funções prontas para a checagem de sessão (`DOLT_BRANCH_STATUS`,
  `DOLT_PREVIEW_MERGE_CONFLICTS_SUMMARY`). Falta construir a nota de colisão no Obsidian.
- **Vista `.md` de mão dupla: a maior peça a construir.**
  - Recomendado: um daemon externo, de 3 a 6 dias.
  - Outras opções: um plugin no molde do obsidian-beads, ou um provedor no
    obsidian-auto-note-importer.
  - Para não colidir por nota inteira: um bloco por linha, ou o corpo em JSON por seção (o Dolt junta
    chaves diferentes).
- **Busca:** as candidatas da varredura 21 indexam a vista `.md` sem mudança. O Dolt também tem
  FULLTEXT e índice vetorial (o `MATCH` ficou não verificado).
- **Peça alternativa:** o DoltLite (SQLite versionado), em beta, um escritor por vez.
- **Falta construir, no total:** de 9 a 20 dias, conforme a vista e a busca.
- **Não verificado:**
  - o serviço Windows;
  - a versão do MCP embutido;
  - o Workbench mostrando conflitos;
  - a licença do DoltLite.
