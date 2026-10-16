# Triagem das divergências (maestro, 2026-10-16)

Fontes: `divergencias-prisma.md` (P, 34, faixas 5 a 10) e `divergencias-sextante.md` (S, 15, faixas 1 a 4). Nenhum
revisor mudou spec, ticket ou mapa. As rodadas no portal saem desta triagem, um grupo por vez.

## 1. Correção mecânica (alinhar a parte ao núcleo ou a um ticket resolvido; sem decisão nova)

P1, P2, P4, P5, P6, P7, P9, P14, P16, P17, P18, P23, P24, P26, P33, P34; S3, S4, S9, S10, S11, S13, S14.
P27 também, mas aqui quem erra é o **núcleo** (põe `agents/maestro/**` inteiro sob a guarda; o ticket 40 deixa as
propostas e o registro de uso fora): corrigir núcleo e parte.
Pede só um aval em bloco ("aplicar"); quem aplica fica para o plano.

## 2. Escolhas que o núcleo fez sem ticket resolvido (pedem aval)

- P3: conflito visível nas duas formas (aviso na leitura e ferramenta que lista os conflitos).
- P8 e P30: a cabeça do contrato relida do `AGENTS.md` a cada conexão do MCP, sem cópia; a limpeza do `_archive/` (30
  dias) na tarefa diária.
- P15: o verificador grava sem guarda de versão (já está na rodada r3, desempate 5).
- P19: estado da vigia em `.local/vigia/estado.json`, fora do banco e do git.
- P29: a data do arquivamento no nome da pasta (`_archive/<AAAA-MM-DD>--<nome>/`).
- S12: aceite da busca com a nota esperada entre as 3 primeiras e nota nova visível em até 60 s.

## 3. Decisões de verdade

- P10: texto da regra curta nas ferramentas de gravação do MCP ("antes de gravar, leia `AGENTS.md`" do ticket 36 ou
  "leia antes, grave com a versão lida; conflito = releia e refaça" do núcleo), e em quais ferramentas.
- P20 e P31: como a falha da cópia diária chega ao Gustavo (núcleo: item no estado da vigia; a parte manda perguntar).
  Liga com a pendência "quem percebe a falha" do laço do system design.
- P28: user stories da faixa 10 vêm de rodadas respondidas do ticket 56 (laço do system design), que segue `claimed`.
  Resolver o 56 (ou registrar as respostas num ticket resolvido) antes de construir.
- S1: o que mora no nível do cliente (`clients/<cliente>/`): aberto no ticket 12.
- S2: se `operations/` e `reference/` levam o núcleo de iniciativa inteiro: aberto no ticket 12.
- S5: `initiative` só onde o caminho identifica uma iniciativa (e a forma de `inbox/`, aberta no ticket 12).
- S6: o hook de fim exige mudar a nota de retomada mesmo quando a resposta não mudou o trabalho?
- S7: início de sessão sem vigia e sem MCP: avisar "estado indisponível" (nenhuma terceira fonte decidida).

## 4. Dependem do formato da execução (vão para a rodada do plano)

P11, P25, P32 (dono da ponte do Claude Desktop: três partes, três donos; o núcleo diz faixa 10); P12, P21 (o que ficou
"se couber": validação de frontmatter no MCP, Config Doctor); P13 (quem liga o verificador ao fim da resposta); P22
(tarefa agendada no ensaio); S8, S15 (fronteiras, dublês, minutos e adiamentos da execução de 1 hora).
