# Montar: banco central com plugin do Obsidian

Type: research
Status: resolved

## Question

Como montar o caminho O3: um banco central comum (Postgres ou outro) com um plugin de sync do
Obsidian (obsidian-postgres-sync ou alternativas) dando a vista de mão dupla? Que bancos e plugins
existem, como o agente acessa (MCP), como acrescentar a conferência de versão na volta, como as
máquinas trabalham offline, como a busca do agente entra, e o que falta construir.

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
  `exploracao/anexos/pesquisa-28-montagem.md`.

## Answer

Relatório completo: [`pesquisa-28-montagem.md`](../../../exploracao/anexos/pesquisa-28-montagem.md)
(2026-10-04; descoberta pelo catálogo oficial de plugins do Obsidian, com 8.405 plugins, pelo
registry de MCP e pela pesquisa 23; sem busca web).

- **Três trilhas prontas, todas de mão dupla e com MCP:**
  - **A:** Postgres + pgvector + PostgREST, com o plugin obsidian-postgres-sync e o MCP Toolbox;
  - **B:** Supabase, com o Supabase Vault Sync ou o SupSync;
  - **C:** Fast Note Sync Service (FNS): binário Go com build Windows, SQLite, MySQL ou Postgres, e
    MCP nativo. Conferido por mim no
    [README](https://raw.githubusercontent.com/haierkeys/fast-note-sync-service/HEAD/README.md):
    *"Native support for ... SQLite, MySQL, and PostgreSQL"* e MCP por SSE e StreamableHTTP, com
    Claude Code citado entre os clientes.
- **Conferência de versão:**
  - **C:** o FNS já tem `baseHash`, a estratégia Manual Merge (base, servidor e local) e o código 530
    quando a base mudou. Falta a gravação do agente pelo MCP levar a base: de 0,5 a 1 dia.
  - **A:** o plugin decide por mtime e sobrescreve a edição offline mais antiga. Um fork que grave a
    base leva de 1 a 3 dias.
  - **B:** a volta compara três estados e gera uma cópia de conflito, mas a subida é cega: de 0,5 a
    1 dia.
- **Offline:** cada máquina tem o vault inteiro e o plugin enfileira as mudanças, mas só com o
  Obsidian aberto. Mitigações:
  - a checagem de início de sessão;
  - o cliente headless do FNS (no Windows, "não garantido" pelo projeto);
  - um daemon próprio (de 3 a 5 dias).
- **Busca:** três opções:
  - híbrida no Postgres (FTS em português + pgvector);
  - a busca por palavra do MCP do FNS;
  - a camada local de "Camada de busca" sobre a vista `.md`.
- **Recomendação do relatório:** ensaiar primeiro a trilha C (cerca de 2 dias de construção), com a
  A como alternativa "Postgres puro" (de 3 a 5 dias).
- **Não verificado:** as estrelas de vários plugins (a cota da API esgotou) e os servidores do Central
  Vault Sync e do Pageden.
