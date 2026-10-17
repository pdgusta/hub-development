# Relatório do ticket 18: retomada (nota de sete campos, início e fim)

Vela, 2026-10-17. Ramo `ticket-18`, worktree `C:/context-hub-wt/ticket-18`: `integracao` 9cc878b com o `ticket-17`
juntado por merge (86c5a88, depois 3e8bbc8; merge 5dedcc1), por mandato do maestro (07:28): o 18 usa o hook de início
do 17 e o fim da resposta do 27. **Junção só depois do 17 e do 16 resolvidos.** Costuras aceitas pelo maestro em
`etapas/costuras-18-Vela.md` (07:31).

## Mudança do spec, para rever com o Gustavo (maestro, 07:31)

Várias sessões no mesmo trabalho: **opção A**. O spec dizia uma nota única por trabalho. Agora:

- quem conduz (sem `MAESTRI_TERMINAL_ID`, ou com `HUB_PAPEL=maestro`) mantém a `retomada.md` da iniciativa;
- cada recruta do Maestri mantém a sua passagem em `<iniciativa>/work/passagem-<terminal>.md` (mesmos sete campos, só
  da parte dele; `work_kind: handoff`, `stage: open`, `agent: <terminal>`);
- o início abre as duas; quem conduz leva as passagens para a nota (regra do `AGENTS.md`, sem mecanismo).

Motivo: sessões paralelas não brigam pela mesma nota. É como esta construção já trabalha.

## O que se fez

- `agents/code/hooks/retomada/nota.mjs`, a regra num lugar só:
  - `iniciativaDe(rel)`: `clients/<c>/<i>`, `initiatives/<i>`, `operations/<o>`; pasta com `_` ou `.` não conta.
  - `recruta(env)` e `notaDe(iniciativa, env)`: a `retomada.md` ou a passagem do recruta.
  - `conferirRetomada` (fim): para cada iniciativa onde o turno gravou algo que não é nota, a nota de quem responde
    tem de ter mudado depois da marca do turno. Senão, falta. Nota que mudou sem um dos sete rótulos
    (`- **Rótulo:**`): falta. O `next_step` o verificador do 05 já cobra pelo esquema.
  - `gravarUltimoAgente`: `last_agent: "<claude-code|codex|copilot> <modelo>"` na `retomada.md` que mudou. Modelo:
    `evento.model` no Codex (doc "Common input fields"); transcript no Claude Code (como no 31); o Copilot não manda.
  - `memoriaDoClaude` e `avisoDaMemoria`: a memória automática do Claude Code
    (`<CLAUDE_CONFIG_DIR|~/.claude>/projects/<cwd com - no lugar de cada sinal>/memory/`) que mudou no turno vira
    **aviso**, uma vez por mudança, sem gastar devolução (o agente não desfaz a memória).
  - `retomadaDoInicio(hub, rel, env)` (início): a nota da iniciativa onde a sessão abre, e a passagem do recruta (ou
    onde gravá-la, se não existe). Corte em 4.000 caracteres, com "cortada; leia o resto em <caminho>". Na raiz ou fora
    de iniciativa: "nenhuma nota aberta; ache o trabalho pela busca, pelo nome que o Gustavo der, ou pergunte".
- `agents/code/hooks/fim-da-resposta/nucleo.mjs` (27): as faltas da retomada somam-se às do verificador, com a mesma
  conta de três devoluções e o registro na vigia na quarta (Gustavo, opção B). A devolução do recruta diz o caminho e o
  frontmatter da passagem.
- `agents/code/hooks/vigia/tela.mjs inicio` (17): depois do estado da vigia, uma linha em branco e a retomada. Erro ao
  ler a nota não leva o estado junto.
- `AGENTS.md`: uma linha na cabeça (1.869 de 2.000 caracteres) e a seção "Retomada" (sete campos na forma exata, fato
  e hipótese, critério de suficiência, passagem do recruta, memória privada, banco fora: troca de trecho e pendência
  em "Perguntas abertas").

Commits: ca2bb45, 511ad2a, b2ba08d, c603970, b291ca2, 8950ed7, e4e3708, 68bf70b.

## Escolhas

- **Regra mecânica, sem modelo** (escolha aceita 16): só pede a nota quando o turno gravou numa iniciativa. Resposta
  só de conversa, ou que gravou fora de iniciativa, solta (ponto aberto da faixa 2: "não devolver toda resposta").
- **Copilot só pelo hook `agentStop`**, sem a extensão `onAgentStop` com `--experimental`: o 27 provou que o hook
  sozinho devolve e solta. **Para rever com o Gustavo** (o spec, faixa 2, pede os dois).
- **Memória privada só a do Claude Code**: a do Codex e a do Copilot não foram verificadas.
- O teste do 17 "com tudo em ordem, uma linha curta" agora olha só o primeiro bloco (o da vigia); a nota vem depois.

## Testes

- `node --test agents/code/test/18-retomada.test.mjs agents/code/test/17-vigia-tela.test.mjs`: 31/31.
- `04-esqueleto`, `05-nova-iniciativa`, `18-retomada`: 32/32 (a cabeça do `AGENTS.md` cabe).
- `harness-real.test.mjs` (detector do 29): 6/6; a prova real aparece pulada sem `HUB_HARNESS_REAL`.

## Prova real (`agents/code/test/ponta-a-ponta/18-retomada.test.mjs`)

Por harness, um hub de ensaio e um HOME de ensaio, com o início da vigia (17) e o fim da resposta (27: mod do Claude
Code por `--plugin-dir`, `Stop` do Codex, `agentStop` do Copilot):

1. Sessão 1 em `clients/aurora/migracao-de-tenant`: o agente cria `research/ensaio-18.md` sem mexer na nota. O fim o
   devolve; ele atualiza a `retomada.md`; o fim solta "sem falta". Confere: os sete campos, o `next_step`, o
   `last_agent` com o harness.
2. Entre as sessões, o teste põe na nota um próximo passo que só ela traz (`ZEBRA-42`).
3. Sessão 2, nova, sem ferramentas: a resposta traz `ZEBRA-42`, e nenhuma ferramenta leu a nota.

Rodadas:

- **Claude Code e Copilot, 2026-10-17 08:28–08:30: 2/2 verdes** (`etapas/logs/18-real-1.log`; evidência em
  `evidencia-18/`). Nos dois: uma devolução ("atualize a nota de retomada"), depois solta "sem falta"; no Copilot, a
  devolução voltou como prompt (`continuacao: true`, como no 27). `last_agent`: `claude-code claude-haiku-5-5` e
  `copilot`. Sessão 2: "Pedir ao setor ZEBRA-42 a lista das caixas compartilhadas", sem ferramenta na nota.
- Login: `.credentials.json` do Claude e os campos de login do Copilot copiados para `%TEMP%\hub-ensaio-18-*`; pastas
  apagadas (`apagado: true`); configurações reais iguais por hash (`hashes-claude-copilot.json`). Sem token na
  evidência (procura por `ghu_|gho_|sk-|refresh_token|access_token`). Modelos: haiku e claude-haiku-5.5.
- **Claude Code e Copilot de novo, depois do conserto (f36df85), 2026-10-17 09:14–09:16: 2/2 verdes**
  (`etapas/logs/18-real-2.log`; evidência 31afe63). A devolução saiu pela lista do `anota` (Claude pelo `PostToolUse` do
  `settings.json`, Copilot pelo `postToolUse`); depois soltou "sem falta". `last_agent` igual à primeira rodada.
  Sessão 2 com `ZEBRA-42` nos dois. Pastas apagadas, configurações reais iguais por hash, sem token na evidência.
- **Codex: pendente**, depois das 12h15 (cota), junto com o do Cinzel. Primeiro uso real do `PostToolUse` do
  `apply_patch`.

## Rodada 1 do Fiel: volta, 1 conserto (e1c5eac)

- **O fim cobrava a nota de quem não gravou** (`etapas/parecer-18-Vela.md`). O `mudados` do núcleo (27) pegava todo
  arquivo do hub com data depois da marca: a gravação de outra sessão, ou do sincronizador, devolvia quem só
  conversou, e o `last_agent` podia carimbar quem não escreveu.
- Conserto, no núcleo (resolve o 27 junto):
  - modo novo `fim-da-resposta.mjs <h> anota`, no hook depois da ferramenta (Claude Code e Codex `PostToolUse`;
    Copilot `postToolUse`). Os caminhos saem dos adaptadores da guarda (14) e entram no arquivo da sessão
    (`gravados`); a marca de um turno novo zera a lista;
  - o fim, a cobrança da nota e o `last_agent` usam só essa lista;
  - carga da guarda dentro do `anota`: se ela não carrega, a marca e o fim seguem;
  - fragmentos: `claude.json` novo (PostToolUse `Write|Edit|MultiEdit`, no `settings.json`; marca e fim seguem no
    mod), `PostToolUse` do `apply_patch` no Codex, `postToolUse` de `create|edit|apply_patch` no Copilot;
  - de passagem (ressalva 3): só `<iniciativa>/retomada.md` e `work/passagem-*.md` são nota; `research/retomada.md`
    é nota comum.
- Testes: ajudante `agents/code/test/gravacao.mjs` (o evento de gravação de cada harness). No 27 e no 18, as gravações
  passam pela sessão. Casos novos: duas sessões (a que só conversa solta, quatro paradas sem nada na vigia, sem
  `last_agent` dela; a que gravou é devolvida) e `research/retomada.md`. O de duas sessões falha no código antigo.
  18, 27, 17 e 19: 69/69. Provas reais (18, 19, 27) com o preparo ajustado (fragmento do Claude; contagem do Codex).
- **Limite:** gravação por shell (Codex pelo `Bash`, Copilot pelo `powershell`) não é anotada e não é conferida. As
  provas pedem `apply_patch`/`create`. O `PostToolUse` do `apply_patch` no Codex não foi visto ainda no real.
- Falta: o real de novo (Claude e Copilot pela fila; Codex depois das 12h15), commit só de evidência.

## Rodada 2 do Fiel: passa com ressalvas (e1c5eac); 2 e 3 consertadas depois

- (1) Gravação por shell fica fora da lista: regressão de cobertura do 27. Levada ao maestro (aceitar ou somar uma
  rede).
- (2) Corrida no `anotar` (8 em paralelo perdiam caminho; leitura no meio virava "sem marca"). Conserto: a lista vai
  num arquivo à parte (`<sessão>.gravados`), uma linha por anotação com `appendFileSync`; a sessão é gravada por troca
  atômica; a marca de turno novo apaga a lista. Teste das oito em paralelo: vermelho 1 em 3 antes, verde 4 em 4 depois.
- (3) `NotebookEdit` no matcher do Claude; o `anota` pega o `notebook_path` (a guarda do 14 não muda). Teste novo.
- 18, 27, 17, 19, 14, provas reais (puladas) e harness-real: 114 passam, 8 pulados. Pede rodada curta de código.

## Fora deste ticket

- Banco fora com o MCP parado (pede o fork e o Docker): só a regra no `AGENTS.md`.
- Retomada pelo cliente; trabalho fora de iniciativa.
- Juntar as passagens na nota: regra, sem mecanismo.

## Deslizes

- Nenhum nesta sessão.
