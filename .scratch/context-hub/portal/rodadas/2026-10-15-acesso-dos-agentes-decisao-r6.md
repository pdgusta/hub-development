---
titulo: Acesso dos agentes: repetir o passo da conta da empresa
ticket: 14
aberta: 2026-10-15
estado: absorvida
---

Seu teste respondeu quase tudo. A política da empresa no VS Code não restringe hooks nem MCP. O hook e o MCP com token
funcionaram no VS Code, na conta da empresa.

Ficou sem resposta o passo do Copilot CLI com a conta da empresa. O erro foi meu: no PowerShell, `@C:/...` sem aspas
vira outra coisa, e a opção não chegou ao Copilot. Por isso o MCP de teste não entrou na sessão.

Se for repetir, uns 2 minutos, num PowerShell:
1. `$env:BANCADA_MCP_TOKEN='bancada-fake-7f3a'`
2. `Start-Process python 'C:\Projetos\bancada-acesso\scripts\mcp_teste.py' -WindowStyle Hidden -PassThru` e anote o Id.
3. `cd C:\Projetos\bancada-acesso` e `copilot --additional-mcp-config '@C:/Projetos/bancada-acesso/config/copilot-mcp.json'`
   (agora com aspas).
4. Dentro dele: `/mcp`, e peça "chame a ferramenta estado_sync do MCP bancada".
5. `/exit` e `Stop-Process -Id <o Id do passo 2>`.

## O passo da conta da empresa
id: empresa
tipo: escolha
recomendada: A

- A: Repito agora e respondo aqui o que aconteceu (bancada conectado e a ferramenta respondeu, ou bloqueado pela empresa)
- B: Não repito: a mesma conta já usou o MCP no VS Code, e o CLI fica para conferir na construção

## O que aconteceu, se repetiu
id: resultado
tipo: escolha

- A: O `/mcp` mostrou o `bancada` conectado e a ferramenta respondeu
- B: O `/mcp` mostrou o `bancada` bloqueado pela empresa
- C: Não repeti

## Algo mais?
id: algo-mais
tipo: texto
