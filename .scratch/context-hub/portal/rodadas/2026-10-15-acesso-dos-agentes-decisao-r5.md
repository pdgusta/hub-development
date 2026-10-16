---
titulo: Acesso dos agentes: seu teste no VS Code e na conta da empresa
ticket: 14
aberta: 2026-10-15
estado: absorvida
---

Uns 10 minutos. Faça os passos na ordem e responda o que viu em cada um. Tudo é de mentira: o token `bancada-fake-7f3a`
é falso, e nada toca o hub. Se quiser, mande fotos das telas pelo chat.

**Passo 0, preparar (um PowerShell só para o teste inteiro):**
1. `$env:BANCADA_MCP_TOKEN='bancada-fake-7f3a'`
2. `Start-Process python 'C:\Projetos\bancada-acesso\scripts\mcp_teste.py' -WindowStyle Hidden -PassThru` e anote o
   número do processo (Id).
3. `code C:\Projetos\bancada-acesso`: o VS Code precisa ser aberto daqui, para enxergar o token.

**Passo 1, política da empresa no VS Code:** abra o chat do Copilot no modo agente. Na paleta de comandos, rode
**"Developer: Policy Diagnostics"** e procure `ChatHooks`, `ChatMCP`, `ChatAllowedMcpServers`,
`ChatAllowManagedMcpServersOnly` e `ChatStrictPluginOnlyCustomization`.

**Passo 2, hook de usuário no VS Code:** copie `C:\Projetos\bancada-acesso\.github\hooks\bancada.json` para
`%USERPROFILE%\.copilot\hooks\zz-bancada-acesso.json`. Abra um chat **novo** e pergunte: "Repita a frase SONDA-INICIO
que veio no início da sessão". Olhe a resposta e o fim de `C:\Projetos\bancada-acesso\logs\inicio.log`.

**Passo 3, MCP com token no VS Code:** crie `C:\Projetos\bancada-acesso\.vscode\mcp.json` com
`{ "servers": { "bancada": { "type": "http", "url": "http://127.0.0.1:8799/mcp", "headers": { "Authorization": "Bearer ${env:BANCADA_MCP_TOKEN}" } } } }`.
Clique em "Start" no próprio arquivo e peça no chat "chame a ferramenta estado_sync do MCP bancada". Olhe a resposta e
o fim de `logs\mcp.log`. Se o servidor não subir, troque `${env:BANCADA_MCP_TOKEN}` por `bancada-fake-7f3a` e tente
de novo.

**Passo 4, sessão "Copilot CLI" dentro do VS Code:** se a lista de sessões do chat tiver uma do tipo "Agent Host" ou
"Copilot CLI", repita nela os passos 2 e 3. Se não tiver, pule.

**Passo 5, desfazer no VS Code:** apague `%USERPROFILE%\.copilot\hooks\zz-bancada-acesso.json` e a pasta
`C:\Projetos\bancada-acesso\.vscode`. Feche o VS Code.

**Passo 6, Copilot CLI com a conta da empresa:** no mesmo PowerShell, logado na conta da empresa (`copilot login`, se
precisar), vá para `C:\Projetos\bancada-acesso` e rode
`copilot --additional-mcp-config @C:/Projetos/bancada-acesso/config/copilot-mcp.json`. Dentro dele: `/mcp`, depois
peça "chame a ferramenta estado_sync do MCP bancada" e olhe o fim de `logs\mcp.log`.

**Passo 7, desfazer:** `/exit` no Copilot e `Stop-Process -Id <o número do passo 0>`.

## Passo 1: a política da empresa no VS Code
id: politica
tipo: escolha

- A: Nenhuma das cinco aparece restrita (hooks e MCP liberados)
- B: Alguma aparece restrita (diga qual em "Algo mais?" ou mande a foto)
- C: Não achei o comando "Developer: Policy Diagnostics"

## Passo 2: o hook de usuário no VS Code
id: hook-vscode
tipo: escolha

- A: A resposta trouxe `pinheiro-dourado-07` e apareceu uma linha nova no `inicio.log`
- B: Apareceu a linha no `inicio.log`, mas a resposta não trouxe a frase
- C: Nada: nem frase nem linha nova

## Passo 3: o MCP com token no VS Code
id: mcp-vscode
tipo: escolha

- A: Subiu com `${env:BANCADA_MCP_TOKEN}`: a resposta trouxe `SONDA-MCP-ESTADO` e o `mcp.log` mostra `token_ok=True`
- B: Só subiu com o token escrito direto no arquivo
- C: Não subiu de jeito nenhum, ou a política barrou

## Passo 4: a sessão "Copilot CLI" dentro do VS Code
id: sessao-cli
tipo: escolha

- A: Não existe essa sessão na minha lista
- B: Existe, e o hook e o MCP funcionaram nela
- C: Existe, e o hook ou o MCP falhou nela (diga qual em "Algo mais?")

## Passo 6: o MCP do hub com a conta da empresa
id: empresa-mcp
tipo: escolha

- A: O `/mcp` mostrou o `bancada` conectado e o `mcp.log` mostra `token_ok=True`
- B: O `/mcp` mostrou o `bancada` bloqueado pela empresa ("blocked by your enterprise" ou parecido)
- C: Outro resultado (descreva em "Algo mais?")

## Algo mais?
id: algo-mais
tipo: texto
