# Retomada do maestro

Reescrita em 2026-10-17 ~01h (Brasília), antes de um /clear pedido pelo Gustavo.

## Leia nesta ordem

Caminhos relativos a `C:\Projetos\context-hub\`.

1. **Este arquivo**, inteiro.
2. `AGENTS.md` e o `MEMORY.md` da memória (já vem no contexto). Memórias novas de 2026-10-16/17 que mandam no dia a dia:
   `maestro-nao-executa`, `contexto-dos-recrutas-40`, `rodadas-pelo-chat`, `rodada-explicacao-acima-das-perguntas`.
3. `.scratch/construcao-do-hub/etapas/regras-da-construcao.md`, inteiro (o que os recrutas seguem).
4. `.scratch/construcao-do-hub/etapas/juntar-tickets.md` e `revisao-em-dupla.md` (o fluxo do Rebite e da dupla).
5. `.scratch/construcao-do-hub/issues/`: a linha `Status:` e `Blocked by:` dos 32 tickets (a fronteira) e o `## Comments`
   dos `claimed`.
6. `.scratch/context-hub/issues/16-passagem-para-a-construcao.md`: só os comentários de 2026-10-16 e 2026-10-17 (fim do
   arquivo; toda decisão do Gustavo está lá, em ordem).
7. Só se precisar: `.scratch/construcao-do-hub/spec.md` (nota "Onde mora o código" no topo) e `spec-partes/`.

Depois, confira o mundo real: `maestri list`, `maestri check` de cada recruta (contexto pela barra), `git -C
C:\context-hub log --oneline -3 integracao`, `etapas/trava-pesada.md` e `etapas/registro-de-juncoes.md`.

## Como a operação funciona agora

- **Construção pelo `/implement-spec`**, invocado pelo Gustavo em 2026-10-16. Até 3 construtores. Plano em
  `.scratch/construcao-do-hub/revisao/plano/proposta-de-etapas.md` ("Decidido").
- **Ciclo de um ticket:** o construtor faz (skill `tdd`), pede revisão ao **Fiel**, que revisa em dupla com o
  **Fielzinho**; depois do "passa", o construtor avisa o **Rebite**, que junta em `integracao` (worktree
  `C:\context-hub-wt\integracao`), roda a suíte, resolve o ticket e avisa o maestro. O maestro **não junta nem executa a
  construção** e não é o centro da comunicação (os três construtores estão ligados entre si); ele passa o próximo ticket
  da fronteira, responde perguntas técnicas (registrando no ticket) e leva ao Gustavo as decisões.
- **Decisões do Gustavo:** o portal está **fechado** desde 2026-10-17 00h24 (RAM curta; o servidor parou, o terminal
  "Portal" fica no canvas, religa com `.\iniciar.cmd` na pasta do portal). Enquanto isso, cada rodada é escrita em
  `.scratch/context-hub/portal/rodadas/` (explicação lá; validar com `leitores._parse_perguntas`) e enviada pelo
  **Maestri Chat, thread blue** (`maestri say`, curta, opções e a recomendada); a resposta dele vale como da rodada:
  `estado: absorvida`, nota "respondida pelo Maestri Chat", absorver no ticket dono.
- **Commits do repositório de planejamento** (`C:\Projetos\context-hub`, ramo `main`, sem remoto) a cada rodada absorvida
  ou ticket resolvido; o maestro faz (varredura e git são dele). Rodapé do commit: `Co-Authored-By` e `Claude-Session`.
- **Contexto dos recrutas:** acima de 40%, no próximo ponto seguro o recruta grava `etapas/retomada-<nome>.md` e diz
  "salvo para limpar"; com ele ocioso e sem fila, `MSYS_NO_PATHCONV=1 maestri ask "<nome>" --raw "/clear\r"`, depois
  "leia a sua retomada". No Codex (Fielzinho): `--raw "/new\r"`, `--raw "1"`, retomada. Nada de `&` dentro de comando
  em segundo plano (o envio morre com o shell).
- **Memória da máquina no limite** (commit ~30 de 35,7 GB; o Docker é uma VM Hyper-V de 4 GB fixos; `wsl --shutdown`
  não ajuda). Regra **"Um trabalho pesado por vez"** com a trava `etapas/trava-pesada.md` (Docker, suíte inteira,
  indexação, npm, harness real). Suíte comum: `node --test "agents/code/test/**/*.test.mjs"` sem `HUB_HARNESS_REAL`
  (os de harness ficam pulados; ticket 29); `--test-concurrency=1` sob carga. Se travar de novo, as saídas são do
  Gustavo: baixar a memória do Docker (Settings > Resources) ou aumentar o arquivo de paginação.
- **Codex:** a conta bateu no limite; volta às 01:34 de 2026-10-17. Pendentes nessa hora: as provas do Codex do 12, 15 e
  20 (commits só de evidência, rodada curta do Fiel) e as leituras do Fielzinho do 07, 12, 15, 19, 20 e 29. Até lá o
  Fiel revisa sozinho.

## Quem está no canvas

- **Brasa** (Claude Opus 5.5 médio, construtora): **07** (banco do par). Consertos feitos; o teste do ticket com Docker
  passou (24 PASSA); faltam as provas 01, 02 e o teste do 06 com Docker, um de cada vez, piso de 2 GB livres e trava.
  Depois: **08**. Contexto ~40%.
- **Vela** (idem): **31** (acervo: registro dos avais, verificador escolhido pelo maestro, peça que sumiu), depois **32**
  (link para fora do hub). Contexto ~16%.
- **Trilho** (idem): **13** (gemini pronto e desligado). Teste único liberado pelo Gustavo (A), com a cota conferida
  antes; pode ligar o contêiner `freellmapi-freellmapi-1` e pará-lo ao fim. Contexto ~42%.
- **Fiel** (Claude Opus 5.5 médio, desde 2026-10-16 ~20h; era Codex): revisor principal; estado em
  `etapas/estado-revisor.md`. Contexto ~42%.
- **Fielzinho** (Codex GPT 6-Astra médio, acesso total, iniciado pelo Gustavo): revisor parceiro; sem cota até 01:34.
- **Rebite** (Claude, "Integrador da construção"): junta e resolve. Contexto ~20%.
- **Portal** (terminal do servidor, parado). Aquarela e Lente saíram do canvas a pedido do Gustavo.

## Placar (2026-10-17 ~01h)

- Resolvidos e juntados (15): 01-06, 12, 14, 15, 19, 20, 27, 29, 30 (`integracao` em 5d84d76). Etapas 0 e 1 completas.
- Em curso: 07 (Brasa), 13 (Trilho), 31 (Vela). Fila: 32 (Vela). **Quase tudo o mais espera o 07**: 08, 09, 28 dependem
  dele, e 10, 11, 16-18, 21-25 dependem desses. 26 é `ready-for-human`.
- Tickets criados além dos 26 do `/to-tickets`: 27 (verificador das pastas), 28 (pastas locais: script e git), 29
  (harness só sob pedido), 30 (montador mostra a falha do git), 31 (três lacunas do acervo), 32 (link fora do hub).

## Decisões do Gustavo em 2026-10-16/17 (detalhe no ticket 16)

Lugar do código (`agents/skills/` para o que o agente chama, `agents/code/` para o motor); tabela `stage`→`status`;
`operations/` não é iniciativa; login dos harnesses no ensaio liberado para a construção inteira; receita da etapa 2
(Brasa 07 e 08); pastas locais (script, vigia roda o gerador, tornar local, `.git/info/exclude`); laço do fim da
resposta (até três devoluções); linha nova no catálogo é livre; três lacunas do acervo (avais em
`agents/maestro/avais/`, o maestro escolhe o verificador, peça sumida vira item da vigia); link fora do hub
`par://<par>/<unidade>/<caminho>`; teste único do gemini liberado. Radar: recrutas em sessões do Claude na nuvem.
Repositório de planejamento versionado (primeiro commit 2026-10-16).

## Desde a reescrita (2026-10-17 ~01h15)

- Duas suítes rodaram juntas (Brasa 00h58, Trilho 01h06; a trava da Brasa foi sobrescrita). O Trilho parou a dele; a da
  Brasa deu 2 falhas por tempo na busca do 12. Agora: Trilho roda a suíte do 13 com a trava e pede a revisão; a Brasa
  (limpa às ~01h15, leu a retomada) repete a suíte do 07 depois, então rodada 2 ao Fiel.
- Trilho (49%) e Fiel (43%) estão acima de 40%: limpar no próximo ponto seguro.

## Nenhuma rodada aberta.
