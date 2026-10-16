---
titulo: Fim da resposta: o que roda dentro do hook
ticket: 16
aberta: 2026-10-16
estado: absorvida
carta: escolhas-4-regras
---

Você perguntou por que a conferência do fim da resposta (passo 3 da carta) é "um script e não um hook ou um mod do
Claude".

**Ela é hook e mod.** Isso já está decidido em "Acesso dos agentes": no Claude Code, o fim da resposta é um mod; no
Codex, o hook `Stop`; no Copilot, o hook `agentStop`, junto com a extensão do Copilot. O "script" da carta é **o que roda
dentro** desse hook ou mod, na hora de conferir se a nota de retomada conta o que foi feito. A escolha em aberto é só
quem julga ali dentro: uma regra fixa (a nota mudou ou não) ou um modelo de IA. A carta não muda.

## Quem julga dentro do hook do fim da resposta
id: fim-quem-julga
tipo: escolha
recomendada: A

- A: Uma regra fixa, sem IA: o mod ou hook pergunta "a nota de retomada mudou nesta resposta?"; se mudou, solta, e se não mudou, devolve ao agente (local, de graça, na hora, mas não julga se a nota ficou boa)
- B: O mod ou hook chama um modelo de IA, que lê a conversa e a nota e julga se basta (julga a qualidade, mas custa, demora e manda a conversa, com dado de cliente, para o modelo)

## Algo mais?
id: algo-mais
tipo: texto
