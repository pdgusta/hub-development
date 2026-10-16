---
titulo: Login dos harnesses nas pastas de ensaio
ticket: 16
aberta: 2026-10-16
estado: absorvida
---

O Trilho terminou a guarda do ticket 14 (o hook que recusa regravar inteiro um arquivo que já existe no hub), com 68
testes verdes pelos eventos que os harnesses mandam. Falta a prova de ponta a ponta que o spec pede: **o Claude Code, o
Codex e o Copilot de verdade** tentando regravar uma nota e sendo recusados. Para isso cada harness precisa estar logado
numa **pasta de configuração de ensaio**, nunca na sua pasta real.

**O que ele propõe, por harness:**

- **Claude Code:** copiar `%USERPROFILE%\.claude\.credentials.json` para uma pasta de ensaio em
  `%TEMP%\hub-ensaio-14-*` (variável `CLAUDE_CONFIG_DIR`).
- **Codex:** copiar `%USERPROFILE%\.codex\auth.json` para um `CODEX_HOME` de ensaio. É o que a prova do ticket 03 já
  fez com o seu aval.
- **Copilot:** no `COPILOT_HOME` de ensaio, um `config.json` só com os campos que dizem quem está logado. O token fica no
  cofre do Windows e **não é copiado**: o Copilot de ensaio lê do cofre.

Tudo é apagado no fim de cada rodada, e as pastas reais são conferidas por hash antes e depois. Os modelos são baratos
(haiku no Claude e no Copilot, gpt-6-luna baixo no Codex), com uma sessão por harness.

**Risco não verificado:** o login do Claude e o do Codex guardam uma chave que se renova sozinha. Se a sessão de ensaio
renovar a chave, a cópia na sua pasta real pode ficar velha e pedir login de novo. A prova 03 rodou o Codex assim várias
vezes sem esse efeito, mas isso não está provado para o Claude. Se acontecer, basta logar de novo (`claude` e depois
`/login`); nada se perde.

**Os mesmos logins vão ser pedidos de novo** nos tickets 11 (o MCP do banco pelos três harnesses), 17 (a vigia nas
telas), 18 (a retomada) e 24 (o kit de par ao vivo). Por isso a pergunta vale para a construção inteira.

## Login dos harnesses nas pastas de ensaio
id: login-de-ensaio
tipo: escolha
recomendada: A

- A: Aval para a construção inteira, nas condições acima: qualquer ticket que precise dos harnesses de verdade copia o login dos três para uma pasta de ensaio em `%TEMP%`, apaga ao fim de cada rodada, confere as pastas reais por hash e usa modelos baratos; o construtor registra cada uso no relatório
- B: Aval só para o ticket 14, nas condições acima; cada ticket seguinte pede de novo
- C: Só o Codex, como na prova 03: o Claude Code e o Copilot ficam provados pelos eventos gravados, e a ponta a ponta deles fica para o kit de par (ticket 24)
- D: Nenhum login copiado: a ponta a ponta dos três fica para o kit de par, e o 14 entrega só a prova pelos eventos gravados

## Algo mais?
id: algo-mais
tipo: texto
