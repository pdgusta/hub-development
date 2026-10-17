# Relatório do 37: o fim da resposta vê a gravação feita pelo shell (Cinzel, 2026-10-17)

Ramo `ticket-37` (worktree `C:/context-hub-wt/ticket-37`), do `ticket-18` 31afe63. Commits 977ea86 e c16e53f.
Costuras aceitas: `costuras-37-Cinzel.md` (Vela: 1, 3 e 4 com os ajustes a-d; maestro: 5, 6 e e).

## O que foi feito

- **O shell marca a sessão.** O hook depois da ferramenta (`fim-da-resposta.mjs anota`) agora ouve também a ferramenta
  de shell: Claude Code `Bash` e `PowerShell`; Codex `Bash` (achado do 15); Copilot CLI `bash` e `powershell` (doc
  `hooks-configuration`, tabela de nomes). O caminho gravado não vem no evento; fica só o arquivo
  `.local/fim-da-resposta/<sessão>.shell`. A marca do turno o apaga. Os matchers dos três fragmentos do fim ganharam
  esses nomes.
- **O fim varre o cwd só se houve shell no turno** (`foraDasFerramentas` no `nucleo.mjs`). Conta o arquivo dentro do
  `cwd` da sessão (e do hub), com `mtime` desde a marca, fora do `.gravados` de qualquer sessão. Pula partes com ponto e
  `node_modules`; para em 20.000 entradas.
- **Nota ou passagem gravada pelo shell** (`ehNota`, agora exportado de `nota.mjs`) conta como mudada: entra no
  `conferirRetomada` (sete campos) e no `gravarUltimoAgente`. Não vira aviso.
- **O resto vira aviso, não falta**, no cabeçalho "Antes de terminar:" (lista dos avisos que pedem ação, com o da
  memória do 18), uma vez por turno, sem gastar devolução:
  `gravado fora das ferramentas (shell ou outro processo) nesta resposta: <até 10 caminhos> (e mais N). Confira o que
  mudou; se foi trabalho de uma iniciativa, a nota de retomada mudou?`
- O comentário do `fim()` dizia "uma vez por sessão"; o certo é por turno (a marca zera os `avisados`). Corrigido.

## Testes

`agents/code/test/37-gravacao-pelo-shell.test.mjs`, 11/11, pelo script com o evento de cada harness (ajudante novo
`eventoDeShell` em `test/gravacao.mjs`):

- os três harnesses: o gravado pelo shell no cwd gera o aviso, uma vez por turno (critério 1);
- fora do cwd, ou de antes do turno, nada (critério 2);
- sem shell no turno, nada: a sessão que só conversou solta, mesmo com outra gravando pelo shell;
- o que outra sessão gravou pela ferramenta não vira aviso;
- mais de dez: dez caminhos e "(e mais 3)";
- os três harnesses: Edit na iniciativa e a nota pelo shell, solta; a nota pelo shell sem um campo, devolvida.

Critério 3 (o que já está na lista segue como no 18; suíte verde): 14, 18, 27 (fim e pastas) e 37 juntos, log
`logs/37-testes.log`: **105/105** (14-guardas, 18-retomada, 27-fim-da-resposta, 27-pastas, 37), 10:25.

Sem harness real (aceito pelo maestro: o que muda não depende da ferramenta; o evento de cada um entra pelo teste).

## Ressalvas

1. **Falso positivo do sincronizador ou de outro processo:** se a sessão rodou shell no turno, o que o LiveSync ou outro
   processo gravou no cwd no mesmo intervalo entra no aviso. É só aviso, e o texto diz "shell ou outro processo".
2. **Turno novo de outra sessão:** a marca apaga o `.gravados` dela; o que ela gravou pela ferramenta no turno anterior
   vira "fora das ferramentas" para mim, se eu rodei shell no meu turno. Aceitável (Vela).
3. **Shell que só lê** também marca a sessão: o fim varre o cwd e não acha nada novo. Custo só de varredura, limitado.
4. **Junção:** o kit do 23 lê as peças do fim pelo nome (`23-kit.test.mjs:201`), sem fixar matcher; os matchers novos
   entram sozinhos. O 37 junta depois do 18.

## Rodada 2 (conserto da rodada 1 do Fiel, combinado com a Vela)

- **Conserto 1:** o fim não sabe quem gravou o que veio de fora das ferramentas. A nota ou a passagem de fora não passa
  mais pelos sete campos como falta e não ganha `last_agent`. Ela só cala o "atualize a nota" da iniciativa (parâmetro
  `deFora` do `conferirRetomada`) e vai ao aviso "Antes de terminar:" com o texto: `a nota de retomada <rel> mudou fora
  das ferramentas e contou como atualizada; se não foi você, atualize-a com o que esta resposta fez (sete campos)`.
- **Risco aceito (Vela):** outro processo muda a nota no turno em que a sessão gravou na iniciativa pela ferramenta e
  rodou shell: a cobrança desta sessão cala, e o aviso fica no lugar. Devolver três vezes quem gravou a nota pelo shell
  seria pior.
- **Testes novos:** os dois casos da sonda do Fiel (shell que só lê + nota de fora sem campo: aviso, sem falta, nota
  intacta; nota de fora completa com o `last_agent` da outra máquina: intacta) e o do risco. Os três "Edit na iniciativa
  e nota pelo shell" agora esperam o aviso, sem falta, e soltam na parada seguinte. O teste "nota pelo shell sem campo é
  devolvida" saiu (contrariava o conserto).
- `37-gravacao-pelo-shell.test.mjs` 13/13. Com 14, 18, 27 e harness-real: RESULTADO2 (`logs/37-testes-r2.log`).
