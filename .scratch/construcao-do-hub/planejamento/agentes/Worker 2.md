# Worker 2: notas

## Volta 1 (2026-10-15)

- Achei o plano vazio e ninguém tinha gravado. Fiz: um corte candidato em 10 faixas (seção "Corte candidato" do
  `plano.md`), tirado das linhas do `map.md` e dos comentários do ticket 16; assumi a faixa 2 (retomada e checkpoint,
  ticket 10); propus quatro fronteiras (hub de ensaio pronto antes da hora, contrato do instalador, hooks por
  fragmento, CouchDB por faixa) e duas perguntas ao Gustavo (CouchDB de ensaio conta como serviço; login dos
  harnesses no HOME de ensaio).
- Não mandei `maestri ask` nesta volta: os 12 estão no meio do turno e o ask fica sem Enter.

## Minha faixa: retomada e checkpoint (ticket 10)

- Entrega: nota de retomada (sete campos, sobrescrita, teste de suficiência), hook de fim de resposta que a grava e
  leva ao hub o que só a memória privada sabe, checagem de início de sessão que a abre.
- Prova: `claude -p` em HOME de ensaio, numa iniciativa do hub de ensaio, duas sessões seguidas.
- A conferir na volta 2: os sete campos exatos no `## Answer` do ticket 10; os eventos de hook (Stop, SessionStart)
  em fonte primária (docs do Claude Code) e o equivalente no Codex e no Copilot (`notify`, hooks do Copilot).
- Não verificado: que `CLAUDE_CONFIG_DIR` sirva de HOME de ensaio do Claude Code sem tocar `~/.claude`.
- Fronteiras a fechar: faixa 6 e 9 (mesmos eventos de hook), faixa 8 (fragmentos de configuração), faixa 1 (forma da
  iniciativa onde a nota mora).

## Volta 2 (2026-10-15)

- Absorvi a correção do Prumo (fim da resposta no Claude Code é mod; Copilot `agentStop` + extensão `onAgentStop`;
  Codex `Stop`) e apaguei o item dele. A linha da faixa 2 foi reescrita.
- Fonte achada: a bancada do ticket 14 (`C:\Projetos\bancada-acesso\relatorio.md` §4) já provou os três: o mod carregou
  em `claude -p --plugin-dir` (sem tocar `~/.claude`) e devolveu/soltou; a extensão do Copilot só carrega com
  `--experimental`, que grava `{"experimental": true}` em `~/.copilot/settings.json`; o Codex devolveu, mas não gravou
  (sandbox). Isso tira o "não verificado" do Prumo sobre o mod no `-p`. `claude --help` desta máquina tem `--plugin-dir`
  e `--settings`.
- Mudança de comportamento proposta (conferir com o Prumo): devolver só quando o turno mudou arquivo da iniciativa ou a
  memória privada; a bancada devolvia em todo turno sem nota tocada.
- Peguei o verificador no fim (`Stop`) da Imposição do 12, que nenhuma faixa tinha; pedi ao Worker 1 o modo
  `--preencher`.
- Esclareci que o hub de ensaio é gerado antes da hora, não pela faixa 2.
- Não verificado: memória privada do Codex e do Copilot; soma de dois hooks de início; a pasta `memory/` do Claude Code
  num HOME de ensaio.
- Próxima volta: confirmar com o Worker 1 (`--preencher`, regra do contrato) e com o Worker 8 (pasta
  `extensoes-copilot/` e `--experimental` no HOME de ensaio); conferir se a faixa cabe na hora.
