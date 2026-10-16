---
titulo: Por onde o agente grava, agora com o teste
ticket: 11
aberta: 2026-10-15
estado: absorvida
---

Na rodada anterior você pediu um teste curto antes de decidir por onde o agente grava. O teste rodou na bancada (o hub de
mentira) com os três harnesses: o agente lê uma nota, um script muda a nota no disco e o agente grava. Os relatórios
completos estão em `bancada-gravacao-claude-copilot.md` e `bancada-gravacao-codex.md`.

**O que cada ferramenta fez com o arquivo mudado entre a leitura e a gravação:**

| Caso | Claude Code | Copilot CLI | Codex (`apply_patch`) |
|---|---|---|---|
| Troca de trecho, mudança externa em outra linha | grava e mantém a mudança externa; avisa que o arquivo mudou | grava e mantém; não avisa | grava e mantém; não avisa |
| Troca de trecho, mudança externa no próprio trecho | recusa e manda reler | recusa ("trecho não encontrado") | recusa ("linhas esperadas não encontradas") |
| Regravação inteira de arquivo lido e depois mudado | recusa e manda reler | recusa qualquer arquivo que já existe | **sobrescreve sem avisar** (criar arquivo por cima de um que existe) |
| Regravação inteira de arquivo existente que o agente nunca leu | **sobrescreve sem avisar** | recusa | **sobrescreve sem avisar** |
| Hook antes da ferramenta que recusa a regravação inteira | recusou, e deixou passar a troca de trecho e o arquivo novo | igual | igual |

Em resumo: a **troca de trecho é segura nos três**. O **furo é a regravação inteira**, aberto no Claude Code (arquivo não
lido) e no Codex (criar por cima). O **hook fecha o furo nos três**. O teste usou o hook no escopo de projeto da bancada;
o hub prevê os hooks no escopo do usuário ("Acesso dos agentes: decisão"), o que fica para conferir na construção. No
Copilot, o hook de projeto no modo `-p` precisou de uma variável de ambiente; no Codex rodou sem acesso total.

A garantia já fixada continua a mesma: nenhuma gravação desfaz outra sem que o agente veja; se o arquivo mudou desde a
leitura, a gravação é recusada, e o agente relê e refaz.

## Por onde o agente grava, nas sessões do Claude Code, do Codex e do Copilot
id: disco-ou-mcp
tipo: escolha
recomendada: A

- A: Pelos dois, cada um no que confere: no disco, só troca de trecho, segura nos três pelo teste; a regravação inteira de um arquivo que já existe vai pelo `write_note` do MCP do banco, com a versão lida. Um hook antes da ferramenta recusa no disco a regravação inteira de arquivo existente (o Write do Claude Code, o criar e a regravação do `apply_patch`, o criar do Copilot) e manda usar o MCP. Arquivo novo nasce no disco
- B: Disco livre, sem hook, confiando no que as ferramentas já conferem: menos construção, mas ficam abertos os dois furos do teste (o Claude Code regrava arquivo que não leu e o Codex cria por cima de arquivo existente, os dois sem aviso)
- C: Guarda por marca: um hook guarda o hash do arquivo quando o agente lê e recusa qualquer gravação no disco se ele mudou. Funciona no Claude Code e no Copilot, que avisam a leitura ao hook; o Codex lê por comando de shell, e reconhecer a leitura dentro de um comando de shell não é confiável (não testado)

## Algo mais?
id: algo-mais
tipo: texto
