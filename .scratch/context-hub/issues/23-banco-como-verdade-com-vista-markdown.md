# Banco como verdade com vista Markdown editável

Type: research
Status: resolved
Blocked by: 22

## Question

Que ferramentas prontas guardam o contexto de agentes num banco como fonte da verdade e oferecem ao
humano uma vista em Markdown editável, cuja edição volta ao banco? Para cada uma: como o agente
acessa (MCP, CLI), como a edição no `.md` volta (e o que acontece se o banco mudou no meio), se roda
no Windows nativo, como leva o banco a uma segunda máquina, licença e atividade. Reavaliar sob esta
premissa as descartadas por "não usar Markdown como fonte": a Guild (§10.4.2) e a categoria
"memória de agentes" (`exploracao/anexos/varredura-2-memoria-de-agentes.md`). Protocolo da §10.4.
Origem: "Markdown: vista ou fonte da verdade".

## Comments

- 2026-10-04: lançada a pedido do Gustavo (R5). Relatório em `exploracao/anexos/pesquisa-23-banco-com-vista.md`.

## Answer

Relatório completo: [`pesquisa-23-banco-com-vista.md`](../../../exploracao/anexos/pesquisa-23-banco-com-vista.md)
(2026-10-04; 45 consultas registradas em 7 línguas, 24 ferramentas conferidas na fonte; nada clonado,
instalado ou executado).

- **Nenhuma pronta cumpre tudo** (banco como verdade, `.md` editável com volta segura, Windows nativo,
  duas máquinas pares sem servidor).
- **Memória de agentes perde ou estraga a edição humana:**
  - memo: *"silently overwritten"*;
  - agent-memory: pula o que já existe;
  - Engram: *"the exporter is one-way. Engram writes to the vault, never reads from it"* (conferido
    por mim no
    [obsidian-brain.md](https://raw.githubusercontent.com/Gentleman-Programming/engram/main/docs/beta/obsidian-brain.md));
  - ConPort: duplica as decisões ao reimportar.
- **Melhores achados:**
  - LiveSync (CouchDB) com MCP: o vault é a vista viva de um banco replicado, com merge de três vias,
    mas exige servidor ou relay;
  - beads (Dolt) com o plugin obsidian-beads: sync pelo remote git e CI em Windows, mas só cobre
    tarefas e não gera `.md` no disco;
  - sqlite-memory com sqlite-sync: licença Elastic 2.0, exige backend e não confere a base na volta.
- **Reavaliadas:** a Guild e o seamless continuam fora. O ai-memory e o Basic Memory mantêm o `.md`
  como verdade.
- **Recomendação do relatório:** não adotar ferramenta de memória como hub. Escolher entre um banco
  replicado com o vault como vista viva (modelo LiveSync) e um banco próprio com vista gerada e volta
  conferida por hash, com sync por Dolt. O beads pode ser a casa das tarefas.
- **Observação do relatório:** se o sync continuar pelo git, o formato que o git junta bem é o `.md`,
  e o banco seria verdade só dentro de cada máquina.
