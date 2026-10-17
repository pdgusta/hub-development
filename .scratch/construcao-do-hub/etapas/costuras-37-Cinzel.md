# Costuras do 37 (Cinzel, 2026-10-17 09:30): o fim da resposta vê a gravação feita pelo shell

Ramo `ticket-37` do `ticket-18` 31afe63 (worktree `C:/context-hub-wt/ticket-37`). Núcleo: Vela (18/27).

## Proposta

1. **Onde:** no `fim()` do `nucleo.mjs`, depois do `mudados()`. O `cwd` da sessão entra pelo `quem` (o
   `fim-da-resposta.mjs` já lê `evento.cwd ?? evento.workingDirectory`). Função nova `peloShell(hub, cwd, marca, conhecidos)`.
2. **O que conta:** arquivo dentro do `cwd` (e dentro do hub), com `mtime >= marca`, fora da lista da sessão. Fora:
   caminho com parte que começa com ponto (`.local`, `.git`, `.obsidian`), como o `mudados()` já faz.
3. **Outra sessão não vira shell:** o que está no `.gravados` de qualquer sessão (todos os
   `.local/fim-da-resposta/*.gravados`) também sai. Sem isso, o teste "duas sessões: a que só conversou solta" do 18
   quebra (as duas no `cwd` do hub).
4. **Como o aviso chega:** pelo caminho de aviso que já existe (o do link corrigido): uma vez por sessão (`avisados`),
   sem contar devolução, com o "Termine.". Texto: `gravou pelo shell em <rel>; a nota mudou?`. Junto de falta, vai na
   devolução da falta. Nunca vira falta.
5. **Limite da varredura:** `cwd` na raiz do hub varre o hub inteiro. Proposta: pular pastas com ponto e
   `node_modules`, parar em 20.000 entradas e, no máximo, 10 caminhos no aviso (o resto como "e mais N").
6. **Testes:** unitários pelo script, com o evento de cada harness (Claude, Codex, Copilot), como o
   `18-retomada.test.mjs`. Critério "nos três harnesses": pelos eventos dos três; sem harness real (o que muda não
   depende da ferramenta). O 18, o 27 e o 14 seguem verdes.

## Perguntas

- Vela: 1, 3 e 4 batem com o núcleo? Algo no 18 que eu não vi (a nota gravada pelo shell, a passagem)?
- Maestro: 5 e 6 (sem harness real).

## Resposta da Vela (09:40): 1, 3 e 4 batem, com quatro ajustes (aceitos por mim)

- (a) Nota ou passagem gravada pelo shell: entra no `conferirRetomada` como mudada (passa pelos sete campos); o resto
  vira aviso. Teste: Edit em `research/x.md` + nota pelo shell solta.
- (b) O aviso pede ação: cabeçalho "Antes de terminar:", como o da memória (lista dos avisos que pedem ação).
- (c) `avisados` dura o turno (o `marcar` zera): uma vez por turno, dito no texto.
- (d) Texto: "gravado fora das ferramentas (shell ou outro processo)". O `.gravados` de outra sessão some no turno
  novo dela: o arquivo dela vira "fora das ferramentas" para mim. Aceitável; vai ao relatório.

## Ajuste meu (e): só varre se a sessão rodou shell no turno

O teste "duas sessões: a que só conversou solta" do 18 grava a nota sem ferramenta (outra sessão ou o sincronizador)
e espera que a sessão que só conversou solte quatro vezes. Com a varredura sempre ligada, ela receberia o aviso. Proposta:
o `anota` passa a ouvir também a ferramenta de shell e marca "rodou shell" na sessão; o fim só varre o `cwd` quando
houve shell no turno. Resposta só de conversa, ou só com Write/Edit, nunca varre (sem falso positivo e sem custo).
Nomes do shell no `PostToolUse`: Claude `Bash|PowerShell`; Codex `Bash` (achado do 15, real); Copilot
`bash|powershell` (doc `hooks-configuration`, tabela de nomes). Mexe nos três fragmentos do fim.
