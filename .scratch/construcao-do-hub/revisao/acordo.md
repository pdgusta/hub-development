# Acordo da revisão conversada do spec (2026-10-16)

Relator: Quadrante (Claude Fable 5.1). Revisores: Prisma (Claude Opus 5.5) e Sextante (Codex GPT 6.1 Sol). Cinco
rodadas em `conversa/r1..r5-<nome>.md`. A versão proposta está em `proposta/` (`spec.md` e `spec-partes/`); a versão
de antes, intocada, em `antes/`. Nada fora de `revisao/` foi editado; nenhum teste ou varredura rodou.

Fechado na rodada 5: Prisma e Sextante confirmaram o acordo (`conversa/r5-prisma.md`, `conversa/r5-sextante.md`); a
única correção de texto (Sextante-25, item 14 da lista c) está aplicada.

Resultado: **acordo dos três em tudo**. Nenhuma mudança ficou sem acordo. O que a proposta decide vem de ticket
resolvido; o que só o núcleo escolheu está marcado **[núcleo]** (lista c); o que depende do formato da execução está
marcado **[formato]** (lista d); o que vem do ticket 56, aberto, está marcado **[ticket aberto: 56]** e fora desta
construção (lista e). Os quatro fatos novos do Gustavo (protocolo, 2026-10-16 ~15h35) estão incorporados.

## (a) Mudanças aplicadas, com a fonte

Ids: Q = Quadrante, P = Prisma, S = Sextante; C = conferência do Prisma na rodada 3; P4 = rodada 4. Caminhos em
`proposta/`.

**Decisões de ticket que a versão de antes não refletia ou contradizia**

- Q-1, P-18, S-22: a guarda do acervo cobre `agents/skills/maestro-*/`, as skills de papel e a skill "nova iniciativa";
  `agents/maestro/` (`propostas/`, `uso/`) fica fora; exceção do maestro em `routing.yml` (40, Guarda e Quem usa; 15,
  rodada 3; 12). Núcleo Worker 9 e faixa 9.
- Q-2, P-15: o kit tira o GSD do arquivo global do Copilot e do escopo global, com cópia (15, rodada 2, vence 36 e 42).
  Faixa 8, story 11.
- Q-3: a lista "Contradições achadas" da faixa 8 vira "Precedência registrada": marcador de raiz vale o 14; GSD vale o
  15; ponte do Desktop vale o 11.
- Q-4, S-8: checagem de início sem arquivo da vigia e sem MCP diz "estado indisponível" (14; bancada de acesso,
  "DESCONHECIDO"). Faixas 2 e 7, núcleo Worker 7.
- Q-5: no Codex, a vigia (quando piora, 33) e o `notify` (fim de turno com divergência, 14, rodada 8) coexistem por
  decisão. Núcleo e faixa 7.
- Q-6, P-8: a descrição de cada ferramenta de gravação do MCP começa por "antes de gravar, leia `AGENTS.md`" (36, R33).
  Núcleo Worker 5, faixas 5 e 10.
- Q-7: teste (9) do núcleo Worker 5: os três harnesses com o MCP pronto, requisição do Codex capturada (36, 41).
- Q-9, P-17: ponte `mcp-remote` do Claude Desktop para a busca e o MCP do banco com escrita, mais a pasta conectada do
  Cowork (11, 36, 38); texto igual nas faixas 5, 8 e 10 e no núcleo.
- Q-10, P-16, S-21: junction global só com as skills de uso geral; as de papel só na pasta do papel (15, rodada 2).
  Núcleo Workers 8 e 9, faixas 8 e 9.
- Q-11: marcador de raiz, fonte do teste com o `.git` real (14, bancada; 45). Núcleo, Pontos abertos.
- Q-16, P-19, fato 2: user stories e decisões da faixa 10 que vêm do 56 marcadas e fora da construção (protocolo; 16,
  2026-10-16).
- Q-17, P-D1, P-D17: portas de ensaio das faixas 5 e 7 alinhadas ao núcleo (5996, 8796, 8797, 5997), marcadas
  [formato].
- P-1: gravação com base velha vira conflito, folha filha, resposta "conflito: releia e refaça" (25, 30; garantia do
  11). Faixa 5.
- P-2: `write_note` e `edit_note` exigem `base_rev`; sem ela, regravar existente é recusado (30). Faixa 5.
- P-3: instância de leitura por `READ_ONLY=true` (34). Faixa 5.
- P-4: E2EE no MCP do banco com a frase-senha do `.env`; testes de versão com a cifra (34, 30, 48). Faixa 5.
- P-5: ferramenta de estado do hub no MCP, com "estado indisponível" sem fonte (14). Faixa 5.
- P-9: validação de frontmatter no MCP é requisito (12, imposição C); "se couber" era corte. Núcleo Worker 5.
- P-10: a vigia lê o banco cifrado e cita o caminho em claro (34, 48). Faixa 7, núcleo Worker 7.
- P-13: Config Doctor é requisito da vigia (33). Núcleo Worker 7 e faixa 7.
- P-22, S-16: leitura por padrão e escrita ligável com guarda e token próprio são requisitos (11, 14, 34). Faixas 4, 5
  e 10, núcleo Worker 5.
- P-23, S-23, C-2: a busca é testada pelo proxy; `--allowed-host` com o `Host` observado (14). Núcleo Workers 3 e 10,
  faixa 10.
- P-24, S-4: o verificador grava sob a garantia "nenhuma gravação sem guarda de versão" (11), sem exceção; relê antes
  de gravar. Núcleo, faixas 1 e 6.
- P-25: forma do mod aberta (33, R64); tarefa agendada de 5 min é requisito (33). Faixa 7.
- P-26 (redação do Sextante): a cópia diária da vista inclui as iniciativas de cliente que integram a vista (33, 12),
  sem depender do 56. Faixa 10.
- S-1: o nível `clients/<cliente>/` guarda o comum às iniciativas (12, R18); a lista de conteúdos segue aberta. Faixa 1.
- S-2: o script de criação só em `clients/` e `initiatives/`; `operations/` e `reference/` com núcleo inteiro segue
  aberto (12). Faixa 1.
- S-3: `initiative` fora de iniciativa fica para o esquema (12). Faixa 1.
- S-5: `.secrets/` aninhado abrangido pela exclusão; teste com a varredura de partida (12; 48). Faixa 1.
- S-6: hook de fim não confunde nota sem mudança com nota insuficiente (10; 14). Faixa 2.
- S-7: sem revisão pós-sessão nem FreeLLMAPI é do 10; "sem IA nenhuma" é [núcleo]. Faixa 2.
- S-9: contrato por import no Claude Code e link simbólico nos outros (36 R28, 42). Faixa 2.
- S-10: `local: true` fora da busca do próprio par (12). Faixa 3 e núcleo Worker 3.
- S-11: todo caminho com ponto fora da busca (12; 09, R90). Faixa 3.
- S-15: a 0.16.2 só indexa `.md` (12, rodada 16). Faixa 3.
- S-18: a guarda do acervo decide pelo arquivo-alvo, inclusive fora do hub e pela junction (40 R46; 16; 44). Faixa 9 e
  teste do Worker 9.
- S-19 (ajuste do Prisma): URL sem resposta não prova máquina desligada; o incerto vai, no mínimo, como `informa`, com
  o motivo, e não suprime a divergência (33). Núcleo Worker 7 e faixa 7. P4-1 alinhou o texto dos Pontos abertos.
- Fato 1: o TI confirmou o Tailscale no notebook sem risco nem conflito corporativo (16, 2026-10-16). Núcleo Out of
  Scope, faixas 4 e 10.
- Fato 3: nenhuma política do Copilot aplicada nesta máquina (16, 2026-10-16; 14). Faixa 8.
- Fato 4: o Gustavo vai ligar o Docker Desktop e criar o repositório privado (16, 2026-10-16): pergunta do Docker
  respondida; deploy key por máquina no repositório novo (06, 33); push real segue `ready-for-human`. Núcleo Further
  Notes, faixas 4 e 10.

**Pontos abertos das partes que o núcleo já tinha resolvido, agora escritos como [núcleo] (ver lista c)**

- P-6 (conflito visível nas duas formas), P-7 e Q-13 (cabeça relida a cada `initialize`, antes do upstream), P-11
  (arquivo de estado da vigia), P-12 (detectores), P-14 (falha da cópia diária no estado da vigia), P-20 (data no
  nome da pasta arquivada), P-21 (limpeza na tarefa diária), S-13 (3 primeiras e 60 s), S-14 (relatório de YAML
  inválido), S-20 (marcas no núcleo Workers 5 e 6), Q-8 (hooks do acervo fora do hub), Q-12 (`COPILOT_SKILLS_DIRS`),
  C-1 (caminho ofuscado da E2EE).

**Formato da execução, marcado sem decidir (ver lista d)**

- Q-14 (perguntas abertas do 16, rodada 2, numa nota só), Q-15 e S-17 (nota do que muda com etapas sequenciais, sem
  ordem), S-12 (dono do gerador de exclusões), S-24 (regra de alcance da marca [formato] no núcleo; "Ordem de corte na
  hora" da faixa 4), C-3 (tarefa agendada do sincronizador), D13 (dono de ligar o verificador ao fim da resposta).

## (b) Sem acordo

Nenhuma. Toda mudança das cinco rodadas fechou com "concordo" ou "concordo com ajuste" aceito pelos três.

## (c) Escolhas do núcleo sem ticket, que ficaram na proposta marcadas [núcleo] (pedem o aval do Gustavo)

1. Conflito visível nas duas formas: aviso no `read_note` e ferramenta `get_conflicts` (o 25 exige visibilidade; o 30
   dá a alternativa).
2. A cabeça do contrato é o bloco `cabeca:inicio/fim` do `AGENTS.md`, relido pelo fork a cada `initialize`, sem cópia,
   antes do texto do upstream; a faixa 10 só confere tamanho e existência (fecha a lacuna de dono 5 do 16).
3. A segunda frase da regra curta ("grave com a `base_rev` lida; conflito = releia e refaça"), só nas operações cuja
   API leva `base_rev`; a guarda de `delete_note` e `move_note` fica a definir.
4. O nome `estado_do_hub` da ferramenta de estado (a ferramenta é requisito do 14).
5. Duas instâncias do MCP do banco por par, a de escrita reaproveitada atrás da rota `/banco-escrita/mcp` (os requisitos
   de leitura por padrão e escrita ligável são decisão; as duas juntas no mesmo par, não verificado).
6. Estado da vigia em `C:\context-hub\.local\vigia\estado.json`, troca atômica, `nivel` por item e o do topo igual ao
   pior.
7. Outro par ligado: `HUB_OUTRO_PAR_URL` como sinal; a representação do incerto como `informa`, no mínimo, com o motivo.
8. Falha da cópia diária: saída ≠ 0 e item `copia-diaria` no estado da vigia, com notificação (a política geral "quem
   percebe a falha" é do 56 e fica fora).
9. Data do arquivamento no nome da pasta (`_archive/<AAAA-MM-DD>--<nome>/`), sem substituir `archived_at`.
10. `limpar-arquivo` na tarefa diária, como desenho (o prazo é do 56 e fica fora).
11. Aceite da busca: nota esperada entre as 3 primeiras; nota nova visível em até 60 s.
12. Relatório da busca com a contagem de `.md` válidos e a lista das notas recusadas por YAML inválido.
13. `OBSIDIAN_IGNORE_PATTERNS` com `**/.*` e `**/.*/**` como mecanismo da exclusão (o requisito é do 12).
14. Ao completar frontmatter, o verificador só preenche campos deriváveis, por troca de trecho, relendo antes de
    gravar. Manter índices e conferir e corrigir links continuam funções do verificador (12) e seguem a mesma guarda. A
    garantia do 11 vale sem exceção; a janela entre releitura e gravação continua não verificada.
15. O hook da faixa 6 monta o conteúdo final (arquivo novo, ou o atual com a troca aplicada) antes de validar.
16. Checkpoint de fim de resposta sem modelo nenhum (o 10 exclui só revisão pós-sessão e FreeLLMAPI; o 14 não decidiu).
17. Os hooks de início do acervo (`MAESTRI_TERMINAL_ID`) e de uso agem em qualquer pasta, dentro ou fora do hub; a
    guarda do acervo decide pelo arquivo-alvo, inclusive pela junction e em sessão fora do hub (leitura conciliadora de
    14, 40 e 43). `MAESTRI_TERMINAL_ID` não distingue maestro de recruta (pendente).
18. `COPILOT_SKILLS_DIRS` apontando para a junction de ensaio, como saída para o ensaio das skills do Copilot (o
    `COPILOT_HOME` as desliga, 18); não dispensa o passo real.
19. `initiative` exigido só onde o caminho identifica uma iniciativa (esclarecimento; o esquema decide).
20. Criar o `AGENTS.md` da iniciativa pelo script "nova iniciativa".
21. Caminho ofuscado na E2EE, como no teste do 48.
22. Política de repetição entre a vigia e o `notify` do Codex, se houver (os dois canais são decisão).
23. `--allowed-host` com o `Host` realmente observado atrás do proxy, se o proxy repassar o `Host`.

## (d) O que depende do formato da execução, marcado [formato] (o Gustavo ajusta no plano)

- "1 hora, 10 workers em paralelo", "o que não couber fica para a próxima execução", subagente Fable para tarefa
  complexa; todos os minutos, dublês, "entrega cedo", "se sobrar", "se couber" e cortes de tempo nos blocos dos
  Workers (regra de alcance no núcleo, antes do Worker 1); "Ordem de corte na hora" da faixa 4.
- Portas de ensaio por faixa (5994 a 5997, 8796, 8797, 3939, 3940); com etapas sequenciais, um banco de ensaio só pode
  servir às faixas 4, 5 e 7.
- Donos de passo: ponte do Claude Desktop (o núcleo diz faixa 10); gerador de exclusões (o núcleo diz faixa 1); quem
  liga o verificador ao fim da resposta (faixa 1, 2 ou 6); conferência da cabeça (faixa 10); registro das tarefas
  diárias; tarefa agendada do sincronizador e da vigia (XML com `-WhatIf` no ensaio; registrar é `ready-for-human`).
- Perguntas abertas da rodada 2 do 16: login dos harnesses no HOME de ensaio; copiar os pilotos do vault; autorização e
  cota para o teste único do gemini. (O Docker foi respondido: fato 4.) Onde o spec depende delas (provas com `codex
  exec` e `copilot -p`, teste do gemini), está marcado.
- "Se couber" que viraram requisito (validação de frontmatter no MCP, Config Doctor, ponte do Desktop): a ordem de
  entrega é formato; o requisito não.
- Nota no núcleo (Further Notes) do que muda com etapas sequenciais: dublês só onde o real exige a segunda máquina;
  "entrega cedo" vira "a etapa anterior entrega"; nenhuma ordem de etapas foi proposta.

## (e) O que vem do ticket 56, aberto, marcado [ticket aberto: 56] e fora desta construção

- Prazo de 30 dias do `_archive/`, "remover = arquivar", agente só apaga com permissão ou depois do prazo, quem confere
  e apaga (lacuna de dono 4 do 16), "exclusão grande no `_archive/` pede aval?".
- Política de recuperação pelo GitHub (agente com o Gustavo vendo, ou ele por comando) e "dois dias de distância
  bastam". O comando de recuperar binário (33, R71) não depende disso.
- Política geral "quem percebe a falha" (vigia parada, hook calado, cópia diária, Tailscale bloqueado).
- "O cliente usa os modelos na nuvem com qualquer iniciativa" (faixa 10, story 37).
- Ficam, porque vêm de ticket resolvido: `arquivar` conferindo o outro par (36, R25; 12), a cópia diária (33, 06) e a
  cópia da vista com as iniciativas de cliente (33, 12).

## Lacunas de dono do ticket 16 que seguem abertas, para o Gustavo

- Onde fica o registro do aval de mudança no contrato (o plano sugeria a faixa 9).
- Quem escolhe o modelo do verificador da guarda do acervo.
- Como o erro de peça citada que sumiu chega ao Gustavo.

## Dúvida ao maestro

- Fato 4: o Gustavo liga o Docker Desktop; isso libera os CouchDB de ensaio em contêiner, em 127.0.0.1, durante a
  construção? A proposta supõe que sim (faixa 4, Pontos abertos).
