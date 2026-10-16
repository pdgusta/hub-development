# Rodada 2 — Quadrante (relator)

Voto em cada mudança do Prisma (r1-prisma.md) e do Sextante (r1-sextante.md). Marcas: [núcleo], [formato],
[ticket aberto: 56], como propus na rodada 1. "Aplicado" no fim do arquivo: o que entra na `proposta/` ao fim desta
rodada, só com o acordo dos três.

## Resposta ao pedido do Sextante (Sextante-7)

Conferi o ticket 14 inteiro. Não há decisão explícita "checkpoint sem IA". A rodada 1 do 14 **recomendou** "fim da
resposta: o mesmo script, sem modelo, nos três harnesses", mas a resposta do Gustavo (rodada 2) foi outra: "hook claude
mod e o correlato de claude mod pros outros harness". O `fim.py` da bancada era "sem modelo" por escolha da bancada. O
ticket 10 exclui só a revisão pós-sessão e o FreeLLMAPI. Logo "sem IA no checkpoint" é [núcleo]. O verificador de
frontmatter sem IA é decisão do 12. Concordo com a Sextante-7.

## Votos: Prisma

- **Prisma-1** (recusa ou conflito): concordo. Fonte 25 e 30; o 11 é a garantia, o 25 a forma.
- **Prisma-2** (`base_rev` em `write_note` e `edit_note`): concordo.
- **Prisma-3** (`READ_ONLY=true`): concordo; o 34 decide a instância, o teste é do núcleo.
- **Prisma-4** (E2EE no MCP): concordo.
- **Prisma-5** (ferramenta de estado): concordo; o nome `estado_do_hub` fica [núcleo].
- **Prisma-6** (conflito visível nas duas formas): concordo, [núcleo].
- **Prisma-7** (cabeça relida a cada `initialize`, antes do upstream): concordo, [núcleo]. Igual à minha Q-13 (lacuna 5).
- **Prisma-8** (regra curta): concordo. Igual à minha Q-6: a primeira frase é do 36, o resto [núcleo].
- **Prisma-9** (validação no MCP é requisito; "se couber" é formato): concordo.
- **Prisma-10** (vigia lê o banco cifrado): concordo.
- **Prisma-11** (arquivo de estado): concordo, [núcleo].
- **Prisma-12** (detectores): concordo; "outro par ligado por `HUB_OUTRO_PAR_URL`" fica [núcleo]; o ramo apagado vem do
  48. Config Doctor segue aberto como detector.
- **Prisma-13** (Config Doctor é requisito): concordo.
- **Prisma-14** (falha da cópia diária): concordo com ajuste: a proposta fica com a forma do núcleo (saída ≠ 0 e item
  `copia-diaria` no estado da vigia), marcada [núcleo] e "ligada à pendência 'quem percebe a falha' do 56". No
  `acordo.md` ela entra na lista (c), escolhas do núcleo, com a nota de que o Gustavo pode decidir junto com o 56.
- **Prisma-15** (GSD): concordo. Conferido: ticket 15, rodada 2, 2026-10-15 20:42. Igual à Q-2.
- **Prisma-16** (junction só com as de uso geral): concordo. Igual à Q-10.
- **Prisma-17** (ponte do Desktop): concordo. Igual à Q-9. Texto igual nas três partes; dono [formato].
- **Prisma-18** (guarda sem propostas e uso): concordo. Igual à Q-1. Ajuste pequeno: `agents/maestro/` só tem
  `propostas/` e `uso/` (ticket 12), então a guarda cobre `agents/skills/maestro-*/` e as skills de papel; `agents/maestro/`
  fica inteira fora da guarda.
- **Prisma-19** (56 aberto): concordo. Igual à Q-16.
- **Prisma-20** (data no nome da pasta): concordo, [núcleo].
- **Prisma-21** (limpeza na tarefa diária): concordo, [núcleo]. Igual à Q-13 (lacuna 4).
- **Prisma-22** (duas instâncias): concordo com o ajuste da Sextante-16: os requisitos (leitura por padrão, escrita
  ligável com guarda e token próprio) são decisão (11, 14, 34); "duas instâncias, a de escrita reaproveitada atrás do
  proxy" é [núcleo]; "não verificado: as duas juntas no mesmo par" fica.
- **Prisma-23** (`--allowed-host` atrás do proxy): concordo.
- **Prisma-24** (pontos da faixa 6): concordo com ajuste da Sextante-4: "o verificador só completa campos deriváveis,
  por troca de trecho" fica [núcleo] e não dispensa a guarda (a troca de trecho já recusa quando o trecho mudou, 11);
  os outros dois itens como propostos.
- **Prisma-25** (forma do mod aberta; tarefa agendada como XML com `-WhatIf`, [formato]): concordo.
- **Portas de ensaio (D1, D17)**: Prisma pôs em "depende do formato" sem texto. Proponho (Q-17, abaixo) alinhar os
  números das partes aos do núcleo e marcar [formato].

## Votos: Sextante

- **Sextante-1** (nível do cliente): concordo. A função é decidida (R18 do 12); a lista de conteúdos fica aberta.
- **Sextante-2** (núcleo só em iniciativas): concordo.
- **Sextante-3** (`initiative` fora de iniciativa): concordo; a restrição "onde o caminho identifica uma iniciativa"
  fica como esclarecimento [núcleo].
- **Sextante-4** (verificador preserva gravação concorrente): concordo. Ver Prisma-24.
- **Sextante-5** (segredo aninhado abrangido pela exclusão): concordo.
- **Sextante-6** (nota sem mudança): concordo.
- **Sextante-7** (sem IA é [núcleo]): concordo; resposta acima.
- **Sextante-8** (estado indisponível): concordo. Igual à Q-4.
- **Sextante-9** (import no Claude Code, link nos outros, faixa 2): concordo.
- **Sextante-10** (`local: true` fora da busca do próprio par): concordo.
- **Sextante-11** (todos os caminhos com ponto fora da busca; `OBSIDIAN_IGNORE_PATTERNS` como mecanismo proposto):
  concordo.
- **Sextante-12** (dono do gerador de exclusões é [formato]): concordo com ajuste: a proposta mantém a atribuição do
  núcleo (faixa 1) como texto, com a marca [formato], para não ficar sem dono nenhum até o plano.
- **Sextante-13** (limites de aceite da busca são [núcleo]): concordo; o mesmo número no núcleo e na parte, marcado.
- **Sextante-14** (relatório de YAML inválido é [núcleo]): concordo.
- **Sextante-15** (0.16.2 só indexa `.md`): concordo.
- **Sextante-16** (instâncias do MCP): concordo. Ver Prisma-22.
- **Sextante-17** (requisitos fora do corte de tempo): concordo com ajuste: retiro da minha Q-15 a "ordem sugerida das
  etapas" (o protocolo não pede ordem); fica a nota do que muda com etapas sequenciais, sem ordem.

## Mudança nova

### Q-17: Portas de ensaio: as partes seguem os números do núcleo, marcados [formato]
- Onde: `faixas-05-06.md`, faixa 5, "Banco de ensaio" e Testing decisions (5986); `faixas-07-08.md`, faixa 7, "Costura"
  (5987).
- Texto atual: 5986 e 5987.
- Texto proposto: faixa 5: "CouchDB de ensaio em 127.0.0.1:5996, MCP em 8796 (escrita) e 8797 (leitura) [formato]";
  faixa 7: "CouchDB de ensaio em 127.0.0.1:5997 [formato]". Nota: com etapas sequenciais, um banco de ensaio só pode
  servir às faixas 4, 5 e 7.
- Fonte: núcleo, Worker 5 e Worker 7; faixa 4, "Compose de ensaio publicado" (5994 a 5997). (D1 e D17 do Prisma.)

## Minhas Q-1 a Q-16: situação

Aguardo o voto dos dois. Ajustes já aceitos por mim: Q-15 sem a ordem das etapas (Sextante-17); Q-6 = Prisma-8;
Q-13 = Prisma-7 e Prisma-21.

## Fatos novos do Gustavo (protocolo, seção acrescentada pelo maestro em 2026-10-16 ~15h35)

Repasso os quatro fatos e o efeito que vejo no spec. Peço voto dos dois na rodada 2.

1. **TI confirmou o Tailscale no notebook, sem risco nem conflito.** Efeito: a frase "sem consulta ao TI" (faixa 4,
   "Kit de par") fica; o ponto aberto da faixa 4 "Docker Desktop e Tailscale: o Tailscale documenta conflitos com ...
   software de segurança e VPN corporativa (05); não verificado nesta máquina" perde a parte corporativa: proponho
   "o TI confirmou que não há conflito com o software corporativo (16, 2026-10-16); conflito com Docker Desktop e WSL
   segue não verificado". O "Out of scope" comum do núcleo ("a consulta ao TI antes do Tailscale no notebook") sai.
2. **O ticket 56 só continua depois da construção.** Efeito: confirma Q-16 e Prisma-19: as user stories da faixa 10
   que vêm do 56 ficam marcadas [ticket aberto: 56] e **fora desta construção**; o `_archive/` e a cópia diária entram
   sem o prazo de 30 dias e sem "nenhuma iniciativa vetada" como requisito (o script `limpar-arquivo` do núcleo fica
   [núcleo] e também [ticket aberto: 56], porque o prazo é dele).
3. **Não há política do Copilot aplicada nesta máquina.** Efeito: já está na faixa 8 (14, rodadas 5 e 6); nada a mudar.
4. **O Gustavo vai ligar o Docker Desktop e criar o repositório privado no GitHub.** Efeito: a pergunta "Docker de
   ensaio" da rodada 2 do 16 fica respondida (Q-14 passa a citar só login de ensaio, cópia dos pilotos e teste do
   gemini como abertas); a cópia diária continua testada contra um repositório nu local, e o `push` real ao GitHub segue
   `ready-for-human` (nada de serviço de verdade sem aval, núcleo "Out of Scope").

## Aplicado ao fim da rodada 2 (acordo dos três, lido em r2-prisma.md e r2-sextante.md)

Tudo abaixo está na `proposta/`. Cada item com os ajustes aceitos nas rodadas 1 e 2.

- **Núcleo (`spec.md`):** nota das marcas [núcleo], [formato], [ticket aberto: 56] no topo; "1 hora, 10 workers"
  marcado [formato]; Out of Scope: a consulta ao TI sai (fato 1) e o que vem só do 56 entra como fora da construção
  (fato 2); Further Notes: perguntas abertas do 16 (login, pilotos, cota do gemini; Docker respondido, fato 4) e a nota
  do que muda com etapas sequenciais, sem ordem (Q-14, Q-15, Sextante-17); Worker 3: aceite 3 primeiras e 60 s
  [núcleo], relatório de YAML inválido [núcleo], gerador de exclusões com dono [formato], `local: true` fora da busca
  (Sextante-10 a 14, 12); Worker 5: regra curta (Q-6, Prisma-8, ajuste Sextante), cabeça relida [núcleo] (Prisma-7),
  ferramenta de estado com "indisponível" (Prisma-5), instâncias (Prisma-22, Sextante-16), E2EE (Prisma-4), validação
  de frontmatter como requisito (Prisma-9), teste (9) dos três harnesses (Q-7); Worker 7: Config Doctor requisito
  (Prisma-13), outro par por URL [núcleo] (Prisma-12), E2EE (Prisma-10), estado em `.local/vigia/estado.json` [núcleo]
  (Prisma-11), `copia-diaria` [núcleo] (Prisma-14), "estado indisponível" (Q-4), tarefa agendada [formato]
  (Prisma-25); Worker 8: duas camadas de skills (Q-10, Prisma-16); Worker 9: guarda sem `agents/maestro/`, com a skill
  "nova iniciativa" e a exceção do `routing.yml` (Q-1, Prisma-18, ajuste Sextante), hooks do acervo fora do hub
  [núcleo] (Q-8); Worker 10: data no nome [núcleo] (Prisma-20), `limpar-arquivo` [56] fora (fato 2), falha da cópia
  [núcleo] (Prisma-14), ponte do Desktop com conteúdo do 11 e dono [formato] (Q-9, Prisma-17); Pontos abertos:
  verificador sob a guarda do 11 (Sextante-4, Prisma-24), marcador de raiz com a fonte do teste (Q-11), avisos no
  Codex coexistem (Q-5, ajuste Sextante), `COPILOT_HOME` e `COPILOT_SKILLS_DIRS` [núcleo] (Q-12).
- **Faixas 1 e 2:** `initiative` fora de iniciativa (Sextante-3); script de criação só em iniciativas (Sextante-2);
  segredo aninhado abrangido pela exclusão, com a varredura de partida (Sextante-5); nível do cliente (Sextante-1);
  verificador sob a guarda (Sextante-4); checkpoint sem IA [núcleo] (Sextante-7); import no Claude Code (Sextante-9);
  hook de fim sem confundir nota sem mudança (Sextante-6); hook de início com "estado indisponível" (Q-4, Sextante-8);
  login como pergunta aberta do 16 [formato] (Q-14).
- **Faixas 3 e 4:** `local: true` fora da busca do próprio par (Sextante-10); todos os caminhos com ponto (Sextante-11);
  3 primeiras e 60 s [núcleo] (Sextante-13); relatório de YAML [núcleo] (Sextante-14); só `.md` (Sextante-15); gerador
  de exclusões com dono [formato] (Sextante-12); gemini como pergunta aberta de cota (Q-14); TI e Tailscale (fato 1);
  Docker (fato 4, com a dúvida do Prisma ao maestro); instâncias (Prisma-22, Sextante-16); deploy key no repositório
  novo (fato 4, Prisma).
- **Faixas 5 e 6:** conflito gravado (Prisma-1); `base_rev` (Prisma-2); `READ_ONLY=true` (Prisma-3); E2EE (Prisma-4);
  ferramenta de estado (Prisma-5); duas formas de conflito visível [núcleo] (Prisma-6); cabeça relida (Prisma-7);
  regra curta (Prisma-8, Q-6); instâncias (Prisma-22); portas 5996/8796/8797 [formato] (Q-17); testes novos; Out of
  scope com a ponte do Desktop (Q-9); pontos abertos fechados; dono do verificador no fim da resposta [formato] (D13);
  frontmatter na troca de trecho [núcleo] e verificador sob a guarda (Prisma-24, Sextante-4); login [formato].
- **Faixas 7 e 8:** stories 12a (E2EE), 12b (`copia-diaria` [núcleo]); story 20 com "indisponível"; vigia lê Config
  Doctor e outro par [núcleo], E2EE; avisos no Codex coexistem; arquivo de estado [núcleo]; porta 5997 [formato] e
  tarefa agendada [formato] (Q-17, Prisma-25); casos de teste novos; pontos abertos fechados (Prisma-12, Q-5); faixa 8:
  story 11 do GSD (Q-2, Prisma-15), stories 15, 16, 16a das duas camadas (Q-10, Prisma-16), story 37 e "Claude
  Desktop" (Q-9, Prisma-17), conta da empresa (fato 3), `COPILOT_HOME` (Q-12), "Contradições achadas" vira
  "Precedência registrada" (Q-3), login [formato].
- **Faixas 9 e 10:** "O que a guarda cobre" (Q-1, Prisma-18); hooks do acervo fora do hub [núcleo] (Q-8); faixa 10:
  abertura e stories 5, 6, 7, 13, 14, 15, 37 marcadas [56] (Q-16, Prisma-19, fato 2); story 16 e 20; prazo de 30 dias
  fora e data no nome [núcleo] (Prisma-20, 21); cópia diária com repositório novo, deploy key e falha [núcleo];
  cabeça (Prisma-7); `--allowed-host` (Prisma-23, ajuste Sextante); instâncias; testes; Out of scope (fato 1, Q-9);
  pontos abertos (Q-13, Prisma-14).

Não aplicado (esperam voto na rodada 3): Prisma-26, Sextante-18, Sextante-19.
