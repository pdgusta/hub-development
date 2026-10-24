# Relatório do ticket 48: correio entre os maestros dos dois pares

Malho, construtor do par B (lenovo-ideapad), 2026-10-24. Ramo `ticket-48` em `C:/context-hub-wt/ticket-48`, a partir
do `main` do hub (a9f1b4d): 5d2d641 (código e testes), fa78f26 (skill e docs), 3e83b76 (consertos da revisão). Sem
junção nem push. Página técnica: `agents/code/docs/componentes/correio.md`.

## O que foi feito (desenho aprovado, itens 1 a 6)

1. **Arquivo por par** `operations/hub-development/maestros/<par_id>.md`, com `## Recados` (`### AAAA-MM-DD hh:mm:
   <assunto>`, o texto, `Status: aberto|feito`) e `## Lido do outro` (`até: <cabeçalho>`). O par é o `HUB_PAR_ID`. Só o
   maestro daquele par grava nele, pela skill.
2. **Campainha:** o `recado` da skill imprime a linha, `recado novo em <arquivo>: <assunto>`, e o destino,
   `maestro-<outro>`. A `SKILL.md` diz ao agente para procurar o destino no `ListAgents` e mandar pelo `SendMessage`.
   Sem a sessão na lista, ou com ela `offline`, segue sem campainha.
3. **Item `correio` da vigia** (`informa`, `fonte: 'correio'`):
   - a passada chama `conferirCorreio` antes de gravar, e o recado novo entra no `piorou`, com a notificação do
     Windows;
   - o `lido` tira o item na hora;
   - a barra (Claude Code e Copilot) e o início da sessão mostram o recado também com outro item no topo.
4. **Rotina do Maestri:** o `correio pendente` serve de `--pre-run`. Com recado não lido, imprime o pedido e sai 0;
   sem recado, sai 1 calado.
5. **Skill `correio`** em `agents/skills/correio/` (`metadata.camada: geral`, então o 08 do kit a liga por junction),
   com `recado`, `ver`, `lido` e `pendente`. A lógica fica em `agents/code/bin/lib/correio.mjs`, que a vigia e a skill
   usam.
6. **Remote Control do maestro** (decisão 3): fica com o maestro (comandos abaixo).

## O que a construção decidiu, com a razão

- **Tipo novo `correio`, no caminho da decisão 1** (`agents/frontmatter/correio.yml`, regra em `paths.yml`).
  - O caminho `work/` com `work_kind: handoff` mudaria o caminho que o Gustavo decidiu.
  - `handoff` é a passagem de um recruta, outra coisa.
  - O esquema exige `par_id`, no formato do `HUB_PAR_ID`.
  - O catálogo passa de 28 a 29 tipos.
- **O arquivo do correio não cobra a retomada de `operations/hub-development`** (`nota.mjs`). Achado na leitura:
  `operations/<o>` conta como iniciativa para o fim da resposta. Gravar o recado pela ferramenta Edit pediria
  `operations/hub-development/retomada.md`, que pelo desenho (item 5) fica no repositório de planejamento. Outra nota
  da operação segue cobrando, e o 18 tem um caso para isso.
- **A rotina com saída vazia** (o item 4 pedia verificar antes): a skill `maestri-routines` diz que o pre-run "must
  exit 0, or the fire is skipped". O `pendente` sai 1 quando não há recado, então a pergunta da saída vazia não se
  põe, e a rotina **fica no desenho**. Não verificado na prática: criar rotina é do Maestro Mode, e eu sou recruta.
- **O item é de outro dono** (`fonte: 'correio'`, como pede o desenho), e não da vigia. Assim o `lido` o tira na hora;
  a passada o regrava ou o tira a cada 5 min.
- **A tela** (`tela.mjs`): o topo do estado mostra um item só, e um `correio` atrás de outro `informa` ou de uma
  divergência não aparecia. A barra passa a acrescentar ` · <resumo do correio>`, e o início com divergência ganha a
  linha do correio.
- **Proteções do formato:**
  - o texto do recado não pode ter linha `## ` ou `### `, e a skill o recusa;
  - o cabeçalho repetido no mesmo minuto ganha ` (2)`;
  - o `até` que não está mais no arquivo do outro (recado editado) cai para a data.

## Achados para o maestro

- **Os maestros de hoje não veem a barra nem o início.** A tela da vigia só fala com a sessão aberta dentro do hub
  (`dentroDoHub`), e os maestros abrem em `C:/Projetos/context-hub`. Para eles chegam:
  - a campainha;
  - a rotina;
  - a notificação do Windows da passada (o recado novo entra no `piorou`).

  Abrir o maestro no hub, ou deixar a tela falar fora dele, é decisão sua; não mexi.
- **O nome da sessão para o `ListAgents`.** Pela `cross-session-messaging.md` (seção dos nomes), a sessão "answers to
  the name you set with `/rename` or `--name`". Pela `remote-control.md`, o nome passado ao `--remote-control` é o
  título da sessão. Não verifiquei se esse título vira o nome no `ListAgents`. Se não virar, use
  `claude --remote-control "maestro-<par>" --name "maestro-<par>"`.
- **`offline` também recebe.** A doc diz que a mensagem a uma sessão `offline` "goes through, but arrives only after
  that session's machine reconnects". O desenho manda seguir sem campainha nesse caso, e a skill segue o desenho; mandar
  mesmo assim também funcionaria. Fica a seu critério.
- **`isolatePeerMachines`** (`settings-reference`): se estiver ligado, cada `SendMessage` para outra máquina pede aval.
  Não conferi o valor nas duas máquinas.

## Testes

- **`48-correio.test.mjs`** (novo, leve, 4 testes; dois hubs de ensaio, `maquina-a` e `maquina-b`; a réplica é a
  cópia do arquivo):
  - o recado do A faz a passada de verdade do B acusar o `correio`; o `lido` o tira; a passada seguinte não o devolve;
    um recado novo volta a contar;
  - o `pendente` sai 0 com recado e 1 calado sem ele;
  - o `$&` e o CRLF do texto ficam como vieram, e o arquivo sem `## Lido do outro` recusa alto;
  - os arquivos passam no verificador de frontmatter sem aviso.
- **Vermelho antes:**
  - o primeiro teste falhou sem a skill;
  - o do verificador falhou com "caminho sem tipo no catálogo" até o tipo `correio`;
  - o caso novo do 18 falhou com "operations/hub-development/retomada.md: atualize..." até a isenção;
  - o caso novo do 17 falhou até a mudança da tela.

  Dois testes não passaram pelo vermelho: o do `pendente` (o código veio no primeiro corte) e o do `$&`/CRLF (escrito
  junto com o conserto da revisão).
- **Sozinhos, no fim:** 48 4/4, 17-vigia-tela 20/20, 18-retomada 18/18, 16-vigia 21/21,
  23-kit 25/25, 09-mcp-banco-sem-docker 1/1.
- **Suíte inteira**, uma vez: 400 testes, **373 passam, 13 falham**, 14 pulados. Os consertos da revisão entraram com
  a suíte já rodando, por isso os arquivos tocados rodaram de novo sozinhos (acima). As 13 falhas:
  - as 12 de ambiente do 53 e do 54: 12-busca (9) e 13-gemini (1), "busca não ficou pronta" com a máquina carregada;
    25-pares-sem-docker (1) e gerar-exclusoes (1), caminhos-padrão do A;
  - **09-mcp-banco-sem-docker (1):** cortado no limite de 120 s sob carga. Sozinho, passa.

  O 48 não toca em nenhuma delas.
- Sem Docker, sem harness de verdade, sem `SendMessage` de verdade, sem rotina do Maestri.

## Revisão (skill `code-review`, desde `main`)

Os dois eixos rodaram em sequência, por causa da regra de um subagente por vez.

- **Padrões, consertado** (3e83b76):
  - o texto do recado ia como string de substituição do `replace`: um `$&` estragava o arquivo. Agora vai por função;
  - o arquivo sem `## Lido do outro` ou sem `até:` não gravava nada e dizia "gravado". Agora recusa, com o caminho;
  - o texto em CRLF virava `\r\r\n`; agora o fim de linha é normalizado;
  - faltava um `?? ''`: o arquivo do outro que some derrubava o `ver`;
  - o `ehCorreio` pegava o `index.md` da pasta;
  - a recusa de uso sai com código 2, separada da falha (1);
  - o comentário da `linha` na tela; a linha do 48 no "Estado" das docs.
- **Padrões, ficou:**
  - o caminho da pasta aparece fixo na lib, no `paths.yml`, no teste e nas docs. O teste o repete de propósito, como
    fonte independente;
  - o `até` é um só, para dois pares (registrado nos limites);
  - o `pendente` sai 1 também sem `HUB_PAR_ID`. A rotina pula nos dois casos, e o stderr diz o motivo.
- **Spec:** nenhum requisito do desenho ficou de fora no código. Pontos levados ao relatório e ao ticket:
  - a escolha do tipo, anotada no ticket;
  - tirar das retomadas a seção "Recados ao outro maestro", que é passo do maestro (comandos abaixo);
  - a rotina conferida só pelo texto da skill `maestri-routines`;
  - o nome no `ListAgents`, a conferir;
  - os maestros fora do hub não veem a barra.

  Ressalva nova da revisão: um segundo recado que chega com o primeiro ainda não lido não notifica de novo, porque o
  item já está em `informa`. A barra e o início seguem mostrando a contagem.

## Comandos para o maestro, depois da junção

O código chega ao hub ao vivo pela junção. A vigia (tarefa `hub-vigia`) e a tela usam o código novo sem reinstalar. A
skill precisa da junction do 08.

```powershell
# Par B (lenovo-ideapad); no A, o mesmo com $EnvA = 'C:\hub-transporte\armis00323.env' (conferir o caminho)
$Hub = 'C:\context-hub'; $EnvB = 'C:\hub-transporte\lenovo-ideapad.env'
pwsh "$Hub\agents\code\kit\par\instalar.ps1" -Casa $HOME -Hub $Hub -EnvFile $EnvB -Passos 08 -WhatIf   # "faria:" a junction da skill correio
pwsh "$Hub\agents\code\kit\par\instalar.ps1" -Casa $HOME -Hub $Hub -EnvFile $EnvB -Passos 08
Test-Path "$HOME\.claude\skills\correio\SKILL.md"                                                      # True
```

Preset "Maestro" e a reabertura (decisão 3; no Maestro Mode, em cada máquina). Ponha no `--command` o modelo e o
esforço de hoje:

```
maestri preset create "Maestro" --command "claude --remote-control \"maestro-lenovo-ideapad\"" --maestro on
# no A: --command "claude --remote-control \"maestro-armis00323\""
```

Reabra o maestro por esse preset e confira no `/list-agents` de cada um que o outro aparece como `maestro-<par>`, com
o rótulo `Remote Control`.

O recado de teste, nos dois sentidos (no B; no A, troque o par):

```powershell
'Recado de teste do correio (ticket 48). Responda com um recado seu e marque lido.' |
  node C:\context-hub\agents\skills\correio\correio.mjs recado "Teste do correio"
# a saída diz a campainha; o maestro manda pelo SendMessage a linha impressa para maestro-armis00323
# no A, em ~1 min: item correio na vigia (notificação do Windows); depois "correio ver" e "correio lido"
```

Desenho, item 5: os recados entre maestros saem das retomadas do git. Tire de `.scratch/context-hub/retomada-maestro.md` e
de `retomada-maestro-par-b.md` a seção "Recados ao outro maestro (par ...)". Mande como recado o que estiver aberto
nela. Troque a regra que a cita no `onboarding-maestro.md` por "o correio mora no hub, pela skill `correio`".

Rotina de reserva (opcional, no Maestro Mode, em cada máquina):

```
maestri routine create "Correio" --terminal "<terminal do maestro>" --every 5m --command "{{output}}" --pre-run "node C:/context-hub/agents/skills/correio/correio.mjs pendente"
maestri routine run "Correio"    # sem recado pendente: a rotina não dispara (conferir que não digita nada)
```

## Arquivos

Hub (ramo `ticket-48`):
- código: `agents/code/bin/lib/correio.mjs` (novo), `agents/skills/correio/correio.mjs` e `SKILL.md` (novos),
  `agents/skills/vigia/vigia.mjs`, `agents/code/hooks/vigia/tela.mjs`, `agents/code/hooks/retomada/nota.mjs`;
- catálogo: `agents/frontmatter/correio.yml` (novo), `agents/frontmatter/paths.yml`;
- testes: `agents/code/test/48-correio.test.mjs` (novo), `17-vigia-tela`, `18-retomada`, `23-kit` (lista das skills
  gerais);
- docs: `componentes/correio.md` (nova), `README.md`, `vigia.md`, `vigia-nas-telas.md`, `frontmatter-e-verificador.md`,
  `retomada.md`, `kit-de-par.md`, `decisoes.md`, mais o `agents/skills/vigia/SKILL.md`.
