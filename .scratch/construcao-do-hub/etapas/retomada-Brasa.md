# Retomada da Brasa

Atualizada em 2026-10-17 ~02h25. Papel: construtora. Regras em `etapas/regras-da-construcao.md`: leia inteiras, em
especial "Um trabalho pesado por vez" (a trava `etapas/trava-pesada.md`) e "Testes com harness de verdade".
- Revisores: Fiel e Fielzinho, em dupla (o Fiel fecha).
- Integrador: Rebite (`maestri ask "Rebite" ...`, depois do "passa").
- Maestro: `maestri ask "Claude Code" ...`.
- Fila: o ticket 07 agora, depois o 08 (receita da etapa 2, opção A).

## Ticket 08 (banco: limites e robustez): começando

- Ramo `ticket-08`, worktree `C:/context-hub-wt/ticket-08`, de `integracao` 763813a. Status claimed.
- Costuras confirmadas pelo maestro ~03h15 (comentário no ticket 08). Retrato em `agents/code/test/banco/retrato/`. Kit só escreve o XML da tarefa.
- Lição do Rebite: esperas pelo estado, com folga, e falha que diz "tempo".

### Próximo passo exato

1. Com as costuras confirmadas: primeiro teste vermelho (fatia 1: ponto e local fora do banco, rodando e na partida).

## Ticket 07 (fechado: juntado e resolvido, integracao 763813a)

- Ramo `ticket-07`, worktree `C:/context-hub-wt/ticket-07`. Ponta `6b1d7e8` (consertos da r2) sobre 99ea624 (`integracao` 57e85cf juntada).
- Rodada 2 voltou (parecer `etapas/02-banco/parecer-Brasa.md`, seção "Rodada 2"); consertos feitos, relatório seção "Rodada 3".
- Suíte comum em 99ea624, com a trava e `--test-concurrency=1`: 179 PASSA, 8 pulados, 0 falhas (`.local/suite-r2d.log`).
- A rodada 3 é a última: passa, com ressalvas escritas. O Fiel roda o Docker nela.

### Próximo passo exato

1. Ticket 07 juntado e resolvido pelo Rebite (integracao 763813a, 186 verdes, 8 pulados). Lição das esperas fixas comentada no 08. Espero o maestro passar o 08.
2. Depois do passa: avisar o Rebite (ramo, testes, relatório, parecer).

### Os testes com Docker da rodada 2 (todos verdes, um de cada vez)

| Teste | Resultado | Log |
|---|---|---|
| `07-banco.test.ps1` (em 6911857) | 24 PASSA | `.local/07-r2e.log` |
| prova 01 (em 87ce68b) | 17 PASSA; hub A→B de 260 arquivos em 70 s | `.local/prova01-r2g.log` |
| prova 02 | 12 PASSA | `.local/prova02-r2f.log` |
| teste do 06 | 14 PASSA | `.local/06-r2f.log` |

- A fila tem conferência de memória: `.local/fila-docker.ps1`, registro em `.local/fila-docker.log`. Antes de cada
  prova, abaixo de 2 GB livres, espera 3 min. O Docker roda numa VM do Hyper-V com 4 GB fixos.
- A fila não cria nem apaga a trava sozinha: criar antes e apagar depois, à mão.
- O sistema parou a fila duas vezes por falta de memória (~23h05 e ~23h40). Limpei o que sobrou e registrei no
  relatório.

### O que a rodada 2 mudou no kit (`agents/code/kit/par/banco/banco.psm1`)

- `Get-PidSincronizador`: o PID só vale se o processo for `node.exe`, com o `CliDb` do par e `daemon` na linha de
  comando.
- `Initialize-Dispositivo`:
  - O dispositivo aceito tem a marca `<cli-db>\.livesync\hub-aceito`, com db, porta, usuário e hora, sem senha. A marca
    só é gravada depois do `ACCEPTED`. Se o `mark-resolved` falha, `isConfigured` volta a `false`.
  - Na volta cedo, o kit confere `encrypt`, `passphrase` e `usePathObfuscation` do `settings.json`, e db, porta e
    usuário da marca, contra o `.env`. Se algo diverge, recusa e diz o campo.
- Espera do `LiveSync active`: 180 s.

### Decisões e armadilhas

- **O remoto no CLI de verdade.** Depois do aceite, o CLI guarda o remoto cifrado em
  `remoteConfigurations[...].uri` (`isEncrypted: true`); os `couchDB_*` ficam vazios.
  - Com o daemon rodando, nenhum outro comando do CLI abre o banco local. O `remote-export` falhava assim, e por isso
    a conferência usa a marca.
- **O daemon não herda handles.** Ele sobe por `cmd /c ... > log 2> err`, sem `-Redirect*`. O PID gravado é o do
  `node` filho do `cmd`.
- **O passo e o gerador.** O passo roda o gerador de exclusões antes da partida. Se a lista mudou com o daemon
  rodando, o passo religa o CLI.
- **Lições da etapa 0, já no módulo:**
  - o mesmo sal nos dois bancos (o kit recusa outro sal);
  - um `couchdb.ini` por par;
  - esperar o `_up` sem credencial;
  - vale a linha `[Done]`;
  - `HUB_ROOT` sob pasta com ponto é recusado.
- **Achar daemon órfão:** o script `.local/orfaos.ps1` filtra a linha de comando por `hub-ensaio-00`. No Git Bash, a
  consulta Win32 com aspas quebra: use um script `.ps1`. Nunca matar por nome.
- **Escape no Python dentro de heredoc:** `\t` e `\b` em caminho viram caractere de controle. Para editar caminho com
  barra invertida, use o Edit ou `chr(92)`.

### Comandos de teste

- Sem Docker (entram na suíte):
  - `node --test agents/code/test/07-kit-sem-docker.test.mjs`
  - ou direto: `pwsh -NoProfile -File agents/code/test/banco/kit-sem-docker.ps1` (11 PASSA).
- Com Docker, com a trava e um de cada vez:
  - `pwsh -NoProfile -File agents/code/test/07-banco.test.ps1`
  - `agents/code/test/provas/01-banco/prova.ps1`
  - `agents/code/test/provas/02-pastas-com-ponto/prova.ps1`
  - `agents/code/test/gerar-exclusoes/sincronizador.ps1`
- Suíte comum, com a trava: `node --test "agents/code/test/**/*.test.mjs"`. Os testes de harness ficam pulados sem
  `HUB_HARNESS_REAL=1`.

## Feito antes (fechado)

- **Ticket 01** (prova dos dois CouchDB): juntado pelo Rebite em 45ec3b0.
- **Ticket 29** (harness só sob pedido): juntado e resolvido pelo Rebite (`integracao` d5e4e16).
  - Parecer: `etapas/parecer-29-Brasa.md`. Relatório: `etapas/relatorio-29-harness-sob-pedido.md`.
  - Fica comigo só o que o Fielzinho achar depois, como ressalva.
