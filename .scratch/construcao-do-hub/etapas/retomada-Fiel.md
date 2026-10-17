# Retomada do Fiel (revisor, Claude Opus 5.5 médio) — 2026-10-17

Leia nesta ordem: `regras-da-construcao.md` e `revisao-em-dupla.md` (inteiros), o fim de `estado-revisor.md`, este
arquivo. Depois `maestri list`. Caminhos relativos a `C:/Projetos/context-hub/.scratch/construcao-do-hub/etapas/`.

## Quem é quem
- Construtores: Brasa, Vela, Trilho. Integrador: Rebite. Maestro: "Claude Code". Parceiro: Fielzinho (Codex; cota
  voltou às 01h34; revisão em dupla normal: repassar na hora, cada um lê sozinho, acordo por maestri ask, eu fecho).
- Respondo só ao construtor; ele leva o passa ao Rebite. Achado em ticket já juntado: gravo no parecer e o construtor
  leva ao maestro (vira ticket seguinte).

## Fila (nada em curso agora)
1. **35 (Trilho)**, **28 (Vela)**, **08 (Brasa)**, **33** (dono a ver): ainda não pedidos. Fluxo: repassar ao
   Fielzinho, `git log/status`, `merge-base --is-ancestor integracao HEAD`, ler ticket (`../issues/NN-*.md`),
   relatório e diff, rodar os testes do ticket, sondar, parecer, acordo, avisar o construtor.
   - 08 é do banco (limites, laço, retrato; ressalvas do 07 apontam para ele): Docker com a trava, um de cada vez.
2. **Leituras atrasadas do Fielzinho** ainda sem parecer dele: 13, 32, 30, 20, 15, 12, 29. Quando chegar cada uma,
   gravar "Leitura do Fielzinho" no parecer (aceito/recusado com motivo); ticket já juntado → construtor leva ao
   maestro.

## Pareceres fechados
| Ticket | Construtor | Parecer | Nota |
|---|---|---|---|
| 05 r4 | Trilho | `01-esqueleto/parecer-Trilho.md` | acordo |
| 01 r1 | Brasa | `00-provas/parecer-Brasa.md` | acordo |
| 06 r2 | Vela | `01-esqueleto/parecer-Vela.md` | acordo |
| 14 r2 | Trilho | `parecer-Trilho.md` | acordo |
| 27 r2 | Vela | `parecer-Vela.md` | acordo (link fora do hub virou o 32) |
| 29 r2 | Brasa | `parecer-29-Brasa.md` | Fiel sozinho; leitura do Fielzinho pendente |
| 19 r1 | Vela | `parecer-19-Vela.md` | leitura tardia do Fielzinho: 2 achados → consertados no 34 |
| 12 r2 | Trilho | `parecer-12-Trilho.md` | Fiel sozinho; leitura pendente |
| 15 r1 | Trilho | `parecer-15-Trilho.md` | Fiel sozinho; leitura pendente |
| 20 r2 | Vela | `parecer-20-Vela.md` | Fiel sozinho; leitura pendente |
| 30 r1 | Vela | `parecer-30-Vela.md` | Fiel sozinho; leitura pendente |
| 32 r2 | Vela | `parecer-32-Vela.md` | Fiel sozinho; leitura pendente |
| 13 r1 | Trilho | `parecer-13-Trilho.md` | Fiel sozinho; leitura pendente |
| 31 r3 | Vela | `parecer-31-Vela.md` | acordo; passa com ressalva (aval sem parecer não registrado → ticket seguinte) |
| 07 r3 | Brasa | `02-banco/parecer-Brasa.md` | acordo; Docker 4/4 com a trava |
| 34 r1 | Vela | `parecer-34-Vela.md` | acordo |

Aceites reais do Codex pendentes de rodada curta, se os construtores pedirem: 12, 15, 20 (o do 20 veio no 31).

## Como reviso
- Rodo os testes do ticket eu mesmo; reproduzo cada achado com sonda (hub de ensaio por
  `node agents/code/test/hub-de-ensaio/montar.mjs <dest>`; eventos JSON no stdin dos hooks; no bash, passar ao node o
  caminho do Windows de `pwd -W`, não o `/tmp/...`, e lembrar que `$(...)` come o `\n` final).
- Parecer: veredito, consertos numerados com linha, reprodução e quem achou; ressalvas; evidências.
- `git status` limpo depois; desfazer só o que meu teste sujou.
- Estado no `estado-revisor.md` a cada passo.

## Regras vivas
- Trabalho pesado (Docker, suíte inteira, indexação da busca, npm install, harness real): `trava-pesada.md`; se existe
  com menos de 30 min, esperar; senão criar (nome, o que roda, hora) e apagar no fim, mesmo falhando. Teste de um
  arquivo só não precisa.
- Harness real só com `HUB_HARNESS_REAL=1`; a suíte comum pula.
- Docker só o Fiel; um teste por vez; derrubar o que sobrar.
- maestri ask com `/`, nunca `\`; ask a recruta ocupado pode estourar o tempo do comando, mas chega.
- Teto: duas voltas; na terceira, passa com ressalvas escritas. Sem subagentes. Nada global de verdade.
- Contexto acima de 40%: no ponto seguro, atualizar estado e retomada e responder "Fiel: salvo para limpar".
