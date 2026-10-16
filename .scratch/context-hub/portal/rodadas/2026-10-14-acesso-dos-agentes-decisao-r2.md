---
titulo: Acesso dos agentes: o teste em detalhe
ticket: 14
aberta: 2026-10-14
estado: absorvida
---

Ficou decidido na rodada 1: o MCP do banco no par fica preso a 127.0.0.1 e com token; e uma pesquisa procura um jeito
de mostrar o estado da vigia o tempo todo também no Codex e no Copilot.

**Por que testar:** a checagem de início e o fim da resposta são os mecanismos que garantem dois critérios do hub
(gravar sem pedir, e nada divergir em silêncio). No Claude Code os hooks são conhecidos; no Codex e no Copilot eles só
foram lidos na documentação. Se um hook não roda, a decisão muda: vira regra no contrato, ou outro caminho.

**Como o teste roda:**
- Num hub de mentira em `C:\Projetos\bancada-acesso\` (um `AGENTS.md` com uma frase-sonda, uma subpasta de iniciativa,
  uma nota de retomada e um `.git`), sem dado de cliente.
- Cada pergunta ao agente é feita por linha de comando (`claude -p`, `codex exec`, `copilot -p`), e o resultado é o
  agente repetir a frase-sonda ou o hook deixar rastro num arquivo de log.
- Os arquivos globais dos harnesses (`~/.codex/hooks.json`, `~/.copilot/hooks/`, `~/.claude/settings.json`) são
  alterados só durante o teste, com cópia de segurança antes e restauração conferida depois. Os arquivos de login nunca
  são lidos nem copiados.
- O que só dá por clique (VS Code e a política da empresa) vira uma lista para você, de uns 10 minutos.
- Entrega: um relatório em `bancada-acesso/relatorio.md`, só com dados, e cada teste como passou, falhou ou não deu
  para testar.

## Os testes
id: testes
tipo: proposta

```json
{
  "colunas": ["teste", "o que prova", "decisão que alimenta", "quem roda"],
  "linhas": [
    {"id": "inicio-codex", "teste": "Hook de início no Codex", "o que prova": "o texto que o hook devolve chega ao modelo; e se dá para deixar o hook aprovado pelo kit, sem você aceitar à mão em /hooks", "decisão que alimenta": "checagem de início", "quem roda": "subagente"},
    {"id": "inicio-copilot", "teste": "Hook de início no Copilot CLI", "o que prova": "o texto do hook chega ao modelo", "decisão que alimenta": "checagem de início", "quem roda": "subagente"},
    {"id": "inicio-claude", "teste": "Hook de início no Claude Code", "o que prova": "o mesmo script dos outros dois funciona aqui", "decisão que alimenta": "checagem de início", "quem roda": "subagente"},
    {"id": "fim-tres", "teste": "Hook de fim da resposta nos três", "o que prova": "um script sem modelo devolve o agente quando a nota de retomada não foi tocada, e solta quando foi", "decisão que alimenta": "fim da resposta", "quem roda": "subagente"},
    {"id": "maestri", "teste": "Hooks dentro de um terminal do Maestri", "o que prova": "os hooks rodam num recruta de teste e enxergam a variável que identifica o terminal do Maestri", "decisão que alimenta": "checagem de início dos recrutas", "quem roda": "subagente, com um recruta de teste criado e removido por mim"},
    {"id": "git-raiz", "teste": "O .git real no lugar do marcador de raiz", "o que prova": "Codex e Copilot abertos numa subpasta e na pasta de um papel chegam ao AGENTS.md da raiz só com o .git", "decisão que alimenta": "se o marcador de raiz ainda precisa existir", "quem roda": "subagente"},
    {"id": "dobro", "teste": "Contrato carregado em dobro", "o que prova": "se o contrato entra duas vezes quando a sessão abre na raiz (pelo arquivo global e pelo AGENTS.md da raiz)", "decisão que alimenta": "como ligar o contrato global sem duplicar", "quem roda": "subagente"},
    {"id": "token", "teste": "MCP com token lido de variável de ambiente", "o que prova": "Claude Code, Codex e Copilot CLI conectam a um MCP de teste em 127.0.0.1 com o token vindo da variável", "decisão que alimenta": "a porta local do par (já decidida) funciona nos três", "quem roda": "subagente"},
    {"id": "instrucoes-mcp", "teste": "Instruções do MCP no Copilot CLI", "o que prova": "com a opção --allow-all-mcp-server-instructions, o texto de instruções do MCP chega ao modelo", "decisão que alimenta": "o contrato nos clientes", "quem roda": "subagente"},
    {"id": "vigia-tela", "teste": "Estado da vigia o tempo todo (pesquisa)", "o que prova": "se Codex e Copilot têm barra de estado ou algo parecido que um script alimente; fonte primária, e teste se existir", "decisão que alimenta": "a pesquisa pedida na rodada 1", "quem roda": "subagente"},
    {"id": "vscode", "teste": "VS Code com Copilot", "o que prova": "hooks de usuário rodam; um MCP com token é aceito; o que a política da empresa permite (Policy Diagnostics)", "decisão que alimenta": "se o hub precisa virar plugin para o VS Code", "quem roda": "você, com uma lista passo a passo"},
    {"id": "empresa-mcp", "teste": "MCP do hub com a conta da empresa no Copilot CLI", "o que prova": "a lista de MCP permitidos da empresa não barra o MCP do hub (/mcp)", "decisão que alimenta": "se os clientes Copilot alcançam o hub", "quem roda": "você, com uma lista passo a passo"}
  ],
  "pode": ["editar", "remover", "adicionar"]
}
```

Tire os testes que não quer, mude o texto ou acrescente outros.

## Quem roda e quanto custa
id: quem
tipo: escolha
recomendada: A

- A: Um subagente Opus 5.5 médio roda agora os testes de linha de comando, em cerca de 1 hora, com 150 a 250 mil tokens; a lista dos seus testes chega junto com o relatório
- B: O mesmo subagente, mas Sonnet 5.5: custa menos tokens do Opus, e ele erra mais em teste que exige ler documentação e ajustar
- C: Só os testes de hook agora (início, fim e Maestri); o resto fica para a construção

## De onde a checagem de início lê o estado do sync
id: checagem
tipo: escolha
recomendada: A

- A: No par, o hook de início lê o arquivo de estado que a vigia grava a cada 5 min (não depende do MCP estar de pé). No cliente, que não tem vigia, o hook pede o estado a uma ferramenta do MCP. Vale se o teste de início passar nos três; onde falhar, a checagem vira regra no contrato daquele harness
- B: Sempre pela ferramenta do MCP, no par e no cliente: um caminho só, mas a checagem falha quando o MCP cai
- C: Esperar o resultado do teste para decidir

## O hook de fim da resposta
id: fim
tipo: escolha
recomendada: A

- A: O mesmo script nos três harnesses, sem modelo: confere se a nota de retomada foi tocada nesta resposta e, se não, devolve o agente para gravar. Vale se o teste de fim passar; onde falhar, fica só a regra no contrato daquele harness
- B: No Claude Code, um hook com modelo, que julga se a nota está boa; no Codex e no Copilot, que não aceitam hook com modelo, o script
- C: Esperar o resultado do teste para decidir

## Algo mais?
id: algo-mais
tipo: texto
