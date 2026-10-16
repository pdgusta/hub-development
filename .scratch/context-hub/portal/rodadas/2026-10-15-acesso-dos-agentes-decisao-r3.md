---
titulo: Acesso dos agentes: o que o teste mostrou
ticket: 14
aberta: 2026-10-15
estado: absorvida
---

A bancada rodou (relatório em `bancada-acesso-relatorio.md`; ~258 mil tokens, acima da estimativa de 150 a 250 mil, pela
pesquisa de extensões e de aprovação de hooks). O teste dentro do Maestri eu rodei com três recrutas de teste, já
removidos. Todos os arquivos globais foram restaurados e conferidos.

**O que passou:**
- **Início de sessão:** o hook roda nos três (Claude Code, Codex, Copilot CLI), lê o arquivo da vigia e, sem ele, cai
  para a ferramenta do MCP, como você pediu. Dentro do Maestri também, e cada recruta enxerga o próprio id de terminal.
- **Codex:** o kit consegue deixar o hook aprovado sem você aceitar à mão em `/hooks`.
- **O `.git` real substitui o marcador de raiz:** Codex e Copilot chegam ao `AGENTS.md` da raiz numa subpasta e na pasta
  de um papel.
- **Contrato em dobro:** não acontece.
- **MCP com token de variável de ambiente:** funciona nos três. As instruções do MCP chegam ao Copilot com a opção
  `--allow-all-mcp-server-instructions`.
- **Fim da resposta no Claude Code:** o mod devolve o agente quando a nota de retomada não foi tocada e solta quando foi.

**O que muda o desenho:**
- **Copilot:** o correlato de um mod é uma extensão. Ela funciona, mas só com a opção `--experimental`. O hook de fim
  comum também funciona.
- **Codex:** não tem correlato de mod (o plugin dele só empacota hooks). O hook de fim devolve o agente; o "solta quando
  a nota foi tocada" não foi visto, porque o Codex não consegue rodar comando nem gravar arquivo pelo `codex exec` nesta
  máquina (erro do sandbox do Windows, causa não investigada).
- **Copilot e hooks do projeto:** hook posto na pasta do projeto só roda se a pasta for marcada como confiável; o hook do
  usuário roda sempre.
- **Estado da vigia o tempo todo:** o Copilot tem barra de estado alimentada por script; o Codex não tem nada parecido.
- **Mod em Claude Code gerenciado pela empresa:** o próprio validador avisa que, onde uma organização gerencia o Claude
  Code, o mod pessoal de fim pode não rodar. Aqui rodou; nas máquinas da empresa, não verificado.

## O fim da resposta no Copilot
id: fim-copilot
tipo: escolha
recomendada: A

- A: O hook de fim comum agora (estável, mesmo script do Codex); a extensão entra quando sair do modo experimental
- B: A extensão já, com `--experimental` ligado pelo kit em todo Copilot do hub
- C: Os dois: o hook de fim e a extensão experimental, ligados juntos

## O fim da resposta no Codex
id: fim-codex
tipo: escolha
recomendada: A

- A: O hook de fim, já que não existe correlato de mod; o "solta quando a nota foi tocada" é conferido na construção, junto com o erro de sandbox do Codex nesta máquina
- B: Investigar agora o erro de sandbox do Codex (um teste curto) e só então decidir

## Onde moram os hooks
id: escopo
tipo: escolha
recomendada: A

- A: No escopo do usuário, nos três harnesses, com o script saindo na hora quando a pasta não é do hub. É o mesmo lugar da guarda do acervo, já decidido, e não depende de marcar o hub como pasta confiável
- B: Na pasta do hub (nível do projeto), com o kit marcando o hub como confiável em cada harness

## O marcador de raiz
id: marcador
tipo: escolha
recomendada: A

- A: Sai: o `.git` da raiz já basta para o Codex e o Copilot chegarem ao contrato, e o kit deixa de criar o marcador
- B: Fica junto com o `.git`, por garantia, se um dia o `.git` sair da raiz

## O estado da vigia na tela
id: vigia-tela
tipo: escolha
recomendada: A

- A: Claude Code pelo mod, Copilot pela barra de estado; no Codex, só na checagem de início e na notificação do Windows
- B: Pedir ao Codex o recurso (uma issue no repositório deles) e, até lá, como na A

## Sua lista do VS Code e da conta da empresa
id: lista-gustavo
tipo: escolha
recomendada: A

- A: Você roda agora, uns 10 minutos, com o passo a passo no fim do relatório (seção "Teste 12"); me manda as fotos das telas pelo chat
- B: Fica para a construção, antes de ligar o Copilot do VS Code ao hub

## Algo mais?
id: algo-mais
tipo: texto
