# Testes 38, grupo B: Obsidian e LiveSync (2026-10-10)

Ticket: "Testes das portas de entrada". Ambiente: o spike (`C:\Projetos\spike-livesync`), CouchDB
local e dois cofres (`cofre-a`, `cofre-b`) abertos no Obsidian em duas janelas, com o LiveSync. O
Gustavo fez os cliques; Claude conferiu pelo disco dos dois cofres e pelo CouchDB (MCP do spike).
Ao abrir, o "Config Doctor" do LiveSync ofereceu aumentar o tamanho dos chunks; a resposta foi "No",
para manter a configuração do spike.

## Resultados

| # | O que foi feito | Resultado |
|---|---|---|
| B3 | Mover `initiatives/x/` para `initiatives/_archive/` pelo Obsidian, com links de `reference/r.md` apontando para as notas | O Obsidian perguntou se atualizava os links ("2 links em 1 arquivo"). A mudança chegou ao outro cofre e ao CouchDB; o caminho antigo sumiu; sem conflito. Os links foram reescritos **para a forma curta**: `[[initiatives/x/nota-2]]` virou `[[nota-2]]` e `[nota 1](initiatives/x/nota-1.md)` virou `[nota 1](nota-1.md)`, que só o Obsidian resolve (a partir de `reference/` o caminho literal não existe) |
| B4 | Com o CouchDB desligado: no A, mover a pasta de volta para `initiatives/x/`; no B, editar `nota-2` no caminho antigo; religar | A mudança do A ganhou: as notas ficaram em `initiatives/x/` nos dois cofres **sem a edição**. A edição do B voltou como `initiatives/_archive/x/nota-2.md` (no B e no CouchDB). O LiveSync abriu "Conflicting changes" nas duas janelas para o caminho antigo, com "Base" (a versão editada) contra "Deleted"; as opções (Use Base, Use Conflicted, Concat both, Not now) só agem no caminho antigo. Não é silencioso, mas a edição fica separada da nota, e juntar é manual |
| B5 | Mover `initiatives/x/` para `initiatives/y/` direto no disco do A, fora do Obsidian | Captado: `y` apareceu no outro cofre e no CouchDB, `x` sumiu, sem conflito. Links não foram reescritos (o Obsidian não participou) |
| B6 | Criar no A `.scratch/oculta.md`, `.git-teste/arquivo`, `dados.json` e `agents/oficina.md` | O explorador do Obsidian mostrou **só** `agents/oficina.md` nas duas janelas. No disco do B chegaram `agents/oficina.md` e `dados.json`; **as pastas com ponto não replicaram** (Hidden File Sync desligada) |

## O que isso decide

- **Mover pasta funciona quando ninguém mais está editando**, pelo Obsidian ou pelo disco.
- **Mover pasta com a outra máquina editando separa a edição da nota**: o LiveSync avisa, mas a
  edição fica no caminho antigo, e a junção é manual. Isso pesa contra arquivar movendo a pasta
  (`_archive/`) e a favor de arquivar por propriedade, ou de só mover com as duas máquinas
  sincronizadas.
- **A reescrita de links do Obsidian usa a forma curta**, que um agente lendo o disco não resolve
  pelo caminho. Links que o agente segue precisam de outra convenção (frontmatter ou configuração do
  Obsidian para caminho completo, a decidir).
- **Pastas com ponto não aparecem no Obsidian nem replicam**; `agents/` sem ponto aparece e replica.
  Arquivos `.json` replicam, mas o explorador não os mostra nesta configuração.

## Pendente de limpeza

O conflito de `initiatives/_archive/x/nota-2.md` ficou em "Not now" nos dois cofres; as notas e pastas
de teste continuam no spike.
