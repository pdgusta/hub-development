# Onboarding do maestro de outra máquina

Para o Claude que abrir este repositório (`C:\Projetos\context-hub`) noutra máquina do Gustavo e for ser o **maestro**
de lá. Escrito pelo maestro do par A em 2026-10-17 ~23h, quando o projeto passou a viver num repositório privado no
GitHub (ticket `.scratch/construcao-do-hub/issues/47-projeto-do-hub-nas-duas-maquinas.md`).

## 0. Antes de tudo: a memória

As memórias do maestro (o que o Gustavo ensinou, preferências, armadilhas) moram no perfil do Claude, por caminho do
projeto, e não vêm pelo git. Há uma cópia em `.scratch/context-hub/memorias-do-maestro/` (com o `MEMORY.md`, o índice).
Na primeira vez, copie-a para a sua pasta de memória deste projeto:

```
~/.claude/projects/C--Projetos-context-hub/memory/
```

(É o mesmo nome se o repositório estiver em `C:\Projetos\context-hub`; se não estiver, a pasta muda de nome.) Depois,
releia o `MEMORY.md`: ele entra no contexto de toda sessão. Quando uma memória mudar de um lado, atualize a cópia no
repositório no mesmo commit, para o outro maestro receber.

## 1. Leia nesta ordem

1. `AGENTS.md` (raiz): como trabalhar nesta frente (pt-BR, file-first, uma decisão por vez, fonte primária, dados de
   cliente, só o fluxo do Matt Pocock).
2. `.scratch/context-hub/retomada-maestro.md`: o estado atual, o que vem a seguir, o mandato, a lista "Para rever".
3. `.scratch/construcao-do-hub/etapas/regras-da-construcao.md`: as regras que os recrutas seguem.
4. Os tickets abertos em `.scratch/construcao-do-hub/issues/` (linha `Status:`).
5. Para saber como foi: `.scratch/construcao-do-hub/etapas/diario-da-construcao.md` e as duas peças visuais em
   `.scratch/construcao-do-hub/resumo-visual/`.
6. Para o código do hub: a documentação técnica no próprio hub, `C:\context-hub\agents\code\docs\` (README,
   arquitetura, operação, um arquivo por peça).

## 2. Convivência entre os dois maestros

- **Um repositório, duas máquinas** (`github.com/pdgusta/hub-development`, privado): `git pull` antes de começar e
  antes de cada rodada; commit e `git push` ao fim de cada etapa. O Gustavo autorizou o maestro a fazer push **deste**
  repositório (2026-10-17 ~23h10); o do hub (`C:\context-hub`) continua só com ele. Se o modo automático do Claude
  Code barrar o push, peça ao Gustavo a regra de permissão (não contorne).
- **Identidade do git** (Gustavo, 2026-10-17 ~23h25): neste repositório e no do hub, `user.name = pdgusta` e
  `user.email = gustavopottpott@hotmail.com`, só na configuração local de cada um (`git config --local`); o global da
  máquina é do trabalho e fica como está. Na máquina nova, grave a mesma configuração local nos dois.
- **Cada maestro, a sua retomada** (2026-10-17 ~23h30, depois de um conflito de rebase): o maestro do par A escreve em
  `.scratch/context-hub/retomada-maestro.md`; o de outra máquina, em `.scratch/context-hub/retomada-maestro-par-b.md`.
  Cada um lê a do outro e nunca escreve nela; recado vai na seção "Recados ao outro maestro" da própria retomada.
- **Não pisar no outro:** antes de mexer numa frente, veja no diário da retomada se o outro maestro está nela. Até o
  correio do ticket 48 existir, o recado entre maestros vai numa seção "Recados entre maestros" da retomada (com
  pull/push) ou pelo Gustavo.
- **O que é de cada máquina e não viaja:** as worktrees (`C:\context-hub-wt\`), os ramos de ticket do hub, o fork do MCP
  do banco (`C:\Projetos\hub-mcp-banco`), o build do CLI do LiveSync, os terminais e papéis do Maestri (`.maestri/`
  está no `.gitignore`), as memórias (ver 0).

## 3. Como o maestro trabalha (o que levou dias para aprender)

**Papel.** O maestro orquestra: passa tickets, responde perguntas técnicas registrando no ticket, decide pelo Gustavo
quando ele delega, e não executa a construção (junção, testes e worktrees são de recrutas). Varredura e git deste
repositório são do maestro.

**Recrutas no canvas do Maestri** (trabalho visível; o Gustavo não quer camadas de subagentes que ele não vê):
- `maestri list`, `maestri check "<nome>"` (a tela e o contexto pela barra), `maestri ask "<nome>" "..."`,
  `maestri ask --batch '{"A":"...","B":"..."}'`, `maestri connect "A" "B"` (ligar recrutas entre si),
  `maestri recruit "<nome>" --preset "Claude Code" --role "<papel>" --command "claude --model claude-opus-5-5 --effort high"`,
  `maestri role create "<papel>" "<prompt>"`, `maestri dismiss "<nome>"` (a guarda de recrutas pede
  `# risco-avaliado: ...` no fim do comando, e só com o recruta ocioso e com a retomada gravada).
- **Nunca editar um papel em uso** (`role edit`/`write`/`assign` reinicia o terminal e perde o contexto): instrução nova
  vai por `ask`.
- Mensagem presa sem Enter no prompt do recruta: `maestri ask "<nome>" --raw "\r"`.
- `/exit`, `/clear` e caminhos com barra: mande **pelo PowerShell** (`maestri ask "<nome>" --raw "/exit`r"`). Pelo Git
  Bash, o MSYS troca `/exit` por um caminho. Depois do `/exit`, se aparecer "Enter to confirm", mande `--raw "1`r"`.
- Religar um recruta fechado: `maestri ask "<nome>" --raw "claude --model claude-opus-5-5`r"` e depois "leia a sua
  retomada" (cada recruta grava `etapas/retomada-<nome>.md`).
- Reiniciar o Maestri ou o Windows religa todos os terminais em sessões **antigas**: feche os sem trabalho.
- **Contexto dos recrutas:** acima de 40%, no ponto seguro gravam a retomada e dizem "salvo para limpar"; então
  `/clear` e "leia a sua retomada" (confira que chegou; `/clear` com o recruta ocupado entra na fila).
- **Maestri Chat:** mensagem com o cabeçalho "Below is a message from the user through Maestri Chat" se responde só com
  `maestri say` (skill `maestri-chat`); cada cor de thread é uma conversa (`maestri recall <cor>` ao trocar).

**Fluxo da construção** (`/implement-spec`, invocado pelo Gustavo): construtor (skill `tdd`, worktree por ticket) →
revisor (Fiel; a 2ª leitura por subagente Opus) → integrador (Rebite) junta em `integracao`, roda a suíte inteira (só ele,
só na junção), resolve o ticket e avisa o maestro e o documentador (Lume). Até 4 construtores; cada recruta até 1
subagente e mais 3 Haiku para tarefa simples ou QA.

**Trabalho pesado** (Docker, suíte inteira, harness real, indexação): um por vez, pela trava
`etapas/trava-pesada.md` e a fila `etapas/fila-pesada.md`. No par A a memória foi o gargalo do dia inteiro: com Docker,
**janela quieta** (os sem trabalho gravam a retomada e saem). `docker desktop stop`/`start` (o `wsl --shutdown` sozinho
não basta: o Docker religa o WSL).

**Codex** só para os testes que precisam dele (o Codex como harness), com `gpt-6-luna` por padrão e `gpt-6.1-sol` se o
teste for difícil; execução e revisão no Claude.

**Decisões do Gustavo.** Uma decisão por vez, sempre com a recomendada. Rodada escrita em
`.scratch/context-hub/portal/rodadas/` (explicação no topo, opções curtas; sem código interno sem dizer o que é) e
enviada pelo Maestri Chat (o portal está fechado por memória). A resposta vai ao ticket dono. **Mandato:** no par A, o
Gustavo delegou decisões ao maestro durante a construção (2026-10-17 ~04h, ver a retomada); pergunte a ele se o mandato
vale para você antes de decidir por ele.

**Nunca:** escrever no global real (`~/.claude`, `~/.codex`, `~/.copilot`, `~/.agents`) sem o aval dele; matar processo
por nome (`taskkill /IM`); matar agentes, laços ou o portal; contornar uma permissão negada; dado pessoal de cliente
(só o nome da iniciativa); `git push` do hub sem ele.

## 4. Primeiro contato com o Gustavo

Diga em uma linha que leu este onboarding, a retomada e as memórias, e pergunte: (1) o mandato vale para você? (2)
qual frente você conduz desta máquina?
