# Retomada do Fiel (revisor, Claude Opus 5.5 médio) — 2026-10-17

Leia nesta ordem: `regras-da-construcao.md` e `revisao-em-dupla.md` (inteiros), o fim de `estado-revisor.md`, este
arquivo. Depois `maestri list`. Todos os caminhos abaixo são relativos a
`C:/Projetos/context-hub/.scratch/construcao-do-hub/etapas/`.

## Quem é quem
- Construtores: Brasa, Vela, Trilho. Integrador: Rebite (junta em `integracao`). Maestro: "Claude Code".
- Fielzinho (Codex): parceiro de revisão. Esteve sem cota do Codex; o maestro mandou revisar sozinho e registrar no
  parecer que a leitura dele fica para depois. Quando a cota voltar, ele lê os que fechei sozinho e conta o que achar
  (vira ressalva para o Rebite, sem segurar junção).
- Eu respondo só ao construtor (maestri ask); ele leva o passa ao Rebite.

## FEITO desde a fila: 07 r3 PASSA (acordo, Docker 4/4); 31 r3 PASSA com ressalva (aval sem parecer não registrado
-> ticket seguinte); 19 leitura tardia do Fielzinho: 2 achados aceitos -> Vela leva ao maestro. Leituras do Fielzinho
ainda pendentes: 13, 32, 30, 20, 15, 12, 29.

## FILA (maestro, depois da cota do Codex voltar às 01h34; o Fielzinho está livre)
1. **07 rodada 2 (Brasa)**: vem depois da suíte dela. Detalhes abaixo em "Próximos pedidos", item 2. Com o
   Fielzinho de volta, revisão em dupla normal (repassar na hora; Docker só eu, com trava).
2. **31 rodada nova (Vela)**: ela mudou código em 050fb14 (a guarda casa CRLF/LF) e trouxe a evidência do Claude e
   do Codex do 20. Ramo ticket-31 (worktree `C:/context-hub-wt/ticket-31`); conferir o diff b710f2d..050fb14, rodar
   `20-acervo`, sondar a guarda com arquivo CRLF (Edit/Write sobre peça com `\r\n`), ler a evidência do 20 (registro,
   hashes iguais, login apagado). Parecer: acrescentar "Rodada 3" em `parecer-31-Vela.md` (é a 3ª: passa com
   ressalvas escritas se ainda houver algo).
3. **Leituras atrasadas do Fielzinho**: 13, 31, 32, 30, 20, 15, 12, 19, 29. Ele lê os pareceres que fechei sozinho e
   conta o que achar; eu registro como "Leitura do Fielzinho" no parecer de cada um (aceito/recusado com motivo); achado
   novo vira ressalva para o Rebite, sem segurar junção já feita (ou conserto, se o ticket ainda não foi juntado).

## Próximos pedidos (anunciados pelo maestro)
1. **Ticket 13 (Trilho)**: ainda não pedido. Seguir o fluxo: repassar ao Fielzinho, ler ticket/relatório/diff, rodar.
2. **Ticket 07 rodada 2 (Brasa, banco do par)**: ramo ticket-07, worktree `C:/context-hub-wt/ticket-07`. Conferir os
   3 consertos da r1 (`02-banco/parecer-Brasa.md`): (1) `Get-PidSincronizador` conferir a linha de comando do daemon,
   não só o nome `node` (banco.psm1:215); (2) `Initialize-Dispositivo` comparar banco/cifra/frase/ofuscação com o
   `.env` em vez de voltar cedo com `isConfigured` (:185); (3) `isConfigured` só depois do `ACCEPTED` do
   `mark-resolved` (:197/:199). Cada um com teste. Docker (com trava): `pwsh -NoProfile -File
   agents/code/test/07-banco.test.ps1`, provas 01 e 02 (`agents/code/test/provas/0{1,2}-*/prova.ps1`),
   `agents/code/test/gerar-exclusoes/sincronizador.ps1`, um de cada vez, logs `revisao-07-r2-<nome>.log`. Na r1, sob
   carga, 07-banco e prova02 deram 1 vermelho de tempo cada; repetidos, passaram. Esta é a 2ª volta: na 3ª, passa com
   ressalvas.
3. **Rodadas curtas de evidência do Codex** (aceite real, cota voltou às 01:34 de São Paulo): 12 (Trilho), 15
   (Trilho), 20 (Vela). Conferir o commit só de evidência: registro/saída do Codex, hashes iguais, login apagado.
   Não rodar harness eu mesmo sem necessidade.

## Pareceres fechados (todos passa, salvo nota)
| Ticket | Construtor | Parecer | Nota |
|---|---|---|---|
| 05 r4 | Trilho | `01-esqueleto/parecer-Trilho.md` | acordo com Fielzinho |
| 01 r1 | Brasa | `00-provas/parecer-Brasa.md` | acordo |
| 06 r2 | Vela | `01-esqueleto/parecer-Vela.md` | acordo |
| 14 r2 | Trilho | `parecer-Trilho.md` | acordo |
| 27 r2 | Vela | `parecer-Vela.md` | acordo; ressalva "link fora do hub" aberta ao maestro |
| 29 r2 | Brasa | `parecer-29-Brasa.md` | Fiel sozinho |
| 19 r1 | Vela | `parecer-19-Vela.md` | Fiel sozinho |
| 12 r2 | Trilho | `parecer-12-Trilho.md` | Fiel sozinho; Codex pendente |
| 15 r1 | Trilho | `parecer-15-Trilho.md` | Fiel sozinho; Codex pendente |
| 20 r2 | Vela | `parecer-20-Vela.md` | Fiel sozinho; Codex pendente |
| 30 r1 | Vela | `parecer-30-Vela.md` | Fiel sozinho; reabre se a suíte da Vela der vermelho fora do 12-busca |
| 31 r2 | Vela | `parecer-31-Vela.md` | Fiel sozinho; suíte e ponta a ponta Claude pendentes da trava (reabre se vermelho) |
| 32 r2 | Vela | `parecer-32-Vela.md` | Fiel sozinho; suíte pendente da trava (reabre se vermelho) |
| 13 r1 | Trilho | `parecer-13-Trilho.md` | Fiel sozinho |
| 07 r1 | Brasa | `02-banco/parecer-Brasa.md` | **VOLTA** (3 consertos), aguardando r2 |

Leitura do Fielzinho pendente: 07, 12, 15, 19, 20, 29, 30.

## Como reviso (o que funcionou)
- `git log`, `git status`, `git merge-base --is-ancestor integracao HEAD`; ler ticket (`../issues/NN-*.md`),
  relatório e diff; rodar os testes do ticket eu mesmo; reproduzir cada achado com sonda própria (hub de ensaio por
  `node agents/code/test/hub-de-ensaio/montar.mjs <dest>`, eventos JSON pelo stdin dos hooks).
- Parecer: veredito passa/volta, consertos numerados com linha, reprodução e quem achou; ressalvas; evidências.
- Depois de rodar testes, `git status` limpo; se meu teste sujou a árvore, desfazer só o que eu causei.
- Gravar estado no `estado-revisor.md` a cada passo.

## Regras vivas
- Trabalho pesado (Docker, suíte inteira, indexação da busca, npm install, harness real): conferir `trava-pesada.md`;
  se existe com menos de 30 min, esperar; senão criar com nome, o que roda e hora; apagar no fim, mesmo falhando.
  Teste de um arquivo só não precisa.
- Harness real só com `HUB_HARNESS_REAL=1` (ticket 29 juntado); a suíte comum pula esses testes.
- Docker só o Fiel; um teste por vez; derrubar o que sobrar (`docker ps -a | grep hub-ensaio`).
- maestri ask com `/`, nunca `\`. Ask longo pode estourar o tempo do comando (o construtor está ocupado); a
  mensagem chega mesmo assim.
- Teto: duas voltas; na terceira, passa com ressalvas escritas. Sem subagentes. Nada global de verdade.
