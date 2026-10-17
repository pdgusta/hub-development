# Retomada da Brasa

Atualizada em 2026-10-17 ~01h20. Papel: construtora. Regras em `etapas/regras-da-construcao.md`: leia inteiras, em
especial "Um trabalho pesado por vez" (a trava `etapas/trava-pesada.md`) e "Testes com harness de verdade".
- Revisores: Fiel e Fielzinho, em dupla (o Fiel fecha).
- Integrador: Rebite (`maestri ask "Rebite" ...`, depois do "passa").
- Maestro: `maestri ask "Claude Code" ...`.
- Fila: o ticket 07 agora, depois o 08 (receita da etapa 2, opção A).

## Ticket 07 (banco do par): rodada 2 quase pronta para o Fiel

- Ramo `ticket-07`, worktree `C:\context-hub-wt\ticket-07`.
- Ponta `cea150b`: merge da `integracao` 5d84d76 (ticket 30).
- Código da rodada 2: 6911857 (os três consertos) e 87ce68b (180 s para o daemon ficar pronto).
- Parecer da rodada 1 (volta): `etapas/02-banco/parecer-Brasa.md`.
- Relatório: `etapas/relatorio-07-banco-do-par.md`. A seção "Rodada 2" está escrita; falta preencher a linha da suíte.

### Próximo passo exato

1. Repetir a suíte comum **com a trava**:
   - Conferir `etapas/trava-pesada.md`. Se existir com menos de 30 min, esperar. Se não, criá-la com nome, o que roda e
     hora.
   - Rodar `node --test "agents/code/test/**/*.test.mjs"` na worktree, com log em `.local/suite-r2d.log`.
   - Apagar a trava ao fim, também se falhar.
   - A última rodada (`.local/suite-r2c.log`) deu 177 testes, 167 passam, 8 pulados e 2 falhas. As duas são da
     indexação da busca (ticket 12): a rajada de 200 notas estourou 300 s, e a segunda partida estourou 80 s. Rodou
     junto com a suíte do Trilho (o maestro pediu que ele parasse). É vermelho por tempo, não do 07.
2. Preencher no relatório (seção "Rodada 2") o resultado da suíte.
3. Pedir a rodada 2 ao Fiel. Ramo `ticket-07` na ponta atual; relatório, seção "Rodada 2".
4. Depois do passa: avisar o Rebite (ramo, testes, relatório, parecer).

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
