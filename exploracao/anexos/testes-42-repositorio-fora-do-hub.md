# Testes 42: porta do repositório fora do hub (2026-10-12)

Ticket: "Testes da porta do repositório fora do hub". Ambiente: um hub falso em `C:\teste42\hub-falso`
(um `AGENTS.md` com a palavra-marcador `GIRASSOL-42` e uma skill `teste-girassol`) e um repositório
git em `C:\teste42\repo-fora`, fora dele. Em cada caso o harness foi aberto no repositório e
perguntado, sem ler arquivos nem rodar comandos, quais palavras-marcador apareciam nas instruções que
recebeu. Versões: Codex CLI 0.161.0, Copilot CLI 1.0.95, VS Code 1.141.0. Modo de desenvolvedor do
Windows ligado: o `pwsh` cria link simbólico sem admin; o Windows PowerShell 5 pede admin.

## Resultados

| Harness | Como o contrato do hub foi ligado | Resultado |
|---|---|---|
| Codex | nada (`~/.codex/AGENTS.md` vazio, como está hoje) | não vê o marcador |
| Codex | `~/.codex/AGENTS.md` com a linha `@C:/teste42/hub-falso/AGENTS.md` | **não** importa: o modelo vê só a linha. Controle: um marcador escrito direto no mesmo arquivo aparece |
| Codex | `~/.codex/AGENTS.md` como link simbólico para o `AGENTS.md` do hub | vê o marcador |
| Codex | `~/.codex/AGENTS.md` como link físico | vê o marcador |
| Copilot CLI | `~/.copilot/copilot-instructions.md` como link simbólico para o `AGENTS.md` do hub | vê o marcador |
| Copilot CLI | `COPILOT_CUSTOM_INSTRUCTIONS_DIRS=C:\teste42\hub-falso` | **não** carrega: `copilot instruction list` mostra um "Nested AGENTS.md", e o modelo diz que o arquivo só aparece listado numa tabela, para ler se precisar |
| Codex e Copilot CLI | junction `~/.agents/skills/teste-girassol` → a skill do hub falso | os dois listam a skill com a descrição |

`copilot skill --help` também mostra um quarto caminho para skills, não testado: "Custom —
directories added with `copilot skill add <directory>`", que apontaria direto para a pasta de skills
do hub, sem junction.

## Copilot no VS Code (o Gustavo no chat)

VS Code 1.141.0, chat no modo Agent, harness Copilot ("Interactive"), com o
`~/.copilot/copilot-instructions.md` ligado ao hub falso e a junction da skill no lugar.

| Pergunta | Resultado |
|---|---|
| Copiar a palavra-marcador das instruções (Claude Haiku 5.5) | recusou: "Reviewed confidential instruction and declined to disclose it". Inconclusivo |
| Listar skills com "girassol" (Haiku 5.5) | achou `teste-girassol` ("sem descrição", segundo o modelo) |
| "Quanto é 2 + 2?", com o contrato falso mandando terminar toda resposta com "GIRASSOL" (Haiku 5.5) | respondeu "4" sem a palavra |
| A mesma pergunta com Grok 4.7 | o raciocínio visível diz "The custom instruction references GIRASSOL-42" e carregou a skill `teste-girassol`; a resposta também saiu sem "GIRASSOL" |

Leitura: o arquivo global ligado **chega** ao Copilot do VS Code (o marcador `GIRASSOL-42` só existe
nele, e o raciocínio o cita); a skill da junction também. A regra de terminar com "GIRASSOL" não foi
seguida por nenhum dos dois modelos; não se sabe se por adesão fraca a uma regra sem sentido ou se o
VS Code guardou a versão anterior do arquivo, aberta antes da regra ser escrita.

## O link e o LiveSync

Ambiente do spike (`C:\Projetos\spike-livesync`), com `cofre-a` e `cofre-b` abertos no Obsidian e o
CouchDB local. Ao abrir, o "Config Doctor" do LiveSync perguntou de novo sobre o tamanho dos chunks;
a resposta foi "No", como no grupo B dos testes anteriores. Um `AGENTS.md` criado no cofre B chegou ao
cofre A; no repositório de teste foram criados um link simbólico e um link físico para o arquivo do
cofre A.

| O que aconteceu com o arquivo | Link simbólico | Link físico |
|---|---|---|
| Edição vinda do cofre B, regravada pelo LiveSync no cofre A (mesmo id de arquivo antes e depois: o LiveSync grava no lugar) | mostra o texto novo | mostra o texto novo |
| No cofre A, o arquivo trocado por um arquivo novo (`sed -i`, que é como git e muitos editores salvam) | mostra o texto novo | **fica com o texto velho**, sem aviso: o link físico se soltou |
| Edição no lugar feita pelo link, de fora do hub (PowerShell `Set-Content`) | chega ao cofre B em cerca de 4 s | chega ao cofre B em cerca de 4 s |
| Edição pelo link com uma ferramenta que grava arquivo novo (`sed -i`) | **o link vira um arquivo comum** com a edição; o hub não recebe nada | não testado |

## O que isso decide

- **Codex e Copilot CLI recebem o contrato do hub fora dele por um link** no arquivo global de cada
  um (`~/.codex/AGENTS.md`, `~/.copilot/copilot-instructions.md`). Import com `@` no Codex não existe,
  e a variável `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` só lista o arquivo.
- **O link tem de ser simbólico.** O físico sobrevive ao LiveSync, mas se solta quando qualquer
  ferramenta troca o arquivo do hub por um novo, e não avisa. O simbólico exige o modo de
  desenvolvedor do Windows (ou admin) em cada par.
- **O contrato não deve ser editado pelo link.** Uma ferramenta que grava arquivo novo troca o link
  por uma cópia, e a edição não chega ao hub. Editar só dentro do hub.
- **O Copilot do VS Code também recebe** o `~/.copilot/copilot-instructions.md` ligado e a skill da
  junction, no modo Agent. Obedecer ao contrato é outra questão: uma regra trivial dele não foi seguida.
- **Skills por junction em `~/.agents/skills` servem a Codex, Copilot CLI e Copilot do VS Code** (e ao Claude Code em
  `~/.claude/skills`, pelo grupo A dos testes anteriores).
- O arquivo global do Copilot hoje tem as instruções do GSD; ligar o contrato do hub ali troca esse
  texto. O kit de par teria de juntar os dois (por exemplo, o contrato no `copilot-instructions.md` e
  o GSD em `~/.copilot/instructions/`, que o VS Code lista; não testado no CLI).

## Efeito colateral no spike

Ao reconectar, o LiveSync apagou dos dois cofres as notas de teste que restavam (`agents/oficina.md`,
`reference/r.md`, `initiatives/y/`), às 18:20:37, logo depois do "No". A causa provável, não
conferida no CouchDB, é a limpeza do grupo D, que tinha apagado as notas de teste do banco: o cofre
que estava desligado aplicou as exclusões ao voltar. Só dado de teste do spike; nada a recuperar.

## Limpeza feita

`~/.codex/AGENTS.md` e `~/.copilot/copilot-instructions.md` restaurados do backup (conferidos);
junction `~/.agents/skills/teste-girassol` apagada; links do repositório de teste e o `AGENTS.md` dos
cofres apagados; Obsidian fechado; spike parado; `C:	este42` apagado, menos a pasta vazia
`repo-fora`, presa pela janela do VS Code aberta nela.
