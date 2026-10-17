# Retomada do Fiel (revisor, Claude Opus 5.5 médio) — 2026-10-17

Leia nesta ordem: `regras-da-construcao.md` e `revisao-em-dupla.md` (inteiros), o fim de `estado-revisor.md`, este
arquivo. Depois `maestri list`. Caminhos relativos a `C:/Projetos/context-hub/.scratch/construcao-do-hub/etapas/`.

## Quem é quem
- Construtores: Brasa, Vela, Trilho. Integrador: Rebite. Maestro: "Claude Code". Parceiro: Fielzinho (Codex; cota
  voltou às 01h34; revisão em dupla normal: repassar na hora, cada um lê sozinho, acordo por maestri ask, eu fecho).
- Respondo só ao construtor; ele leva o passa ao Rebite. Achado em ticket já juntado: gravo no parecer e o construtor
  leva ao maestro (vira ticket seguinte).

## Fila (2026-10-17 ~07h; nada em curso)
1. **15 (Trilho)**: rodada nova depois do Codex real (cota 06h58). Fragmento só com a search; o 15-leitura.test.mjs
   precisa gravar o claude-settings.json (ressalva 2 do 12 r3).
2. **16 (Trilho)**: rodada final quando o 08 for juntado. Faltam os cenários do 08, o gerador a cada passada, o
   estado_do_hub real e o item fim-da-resposta. Três ressalvas no parecer-16-Trilho.md (a principal: atualização
   perdida no estado.json). Docker meu na rodada final, com a trava.
3. **08 (Brasa)**: ainda não pedido.
4. **Leituras do Fielzinho** (cota a partir de 06h58), todas pendentes: 28 (achado 3 da r1, r2, r3), 12 r3, 35, 33,
   09, 36, 10, 16, mais as antigas 13, 32, 30, 20, 15, 12, 29. Quando chegar cada uma, gravar "Leitura do Fielzinho"
   no parecer; ticket já juntado → o construtor leva ao maestro.

## Pareceres fechados hoje (2026-10-17, depois da retomada das 04h; Fiel sozinho, salvo o 28 r1)
| Ticket | Construtor | Parecer | Nota |
|---|---|---|---|
| 28 r3 | Vela | `parecer-28-Vela.md` | PASSA; Docker 14 PASSA |
| 12 r3 | Trilho | `parecer-12-Trilho.md` | PASSA; só a search nos três |
| 35 r1 | Trilho | `parecer-35-Trilho.md` | PASSA |
| 33 r1 | Trilho | `parecer-33-Trilho.md` | PASSA com 3 ressalvas |
| 09 r2 | Cinzel | `parecer-09-Cinzel.md` | PASSA; simultânea vira conflito |
| 36 r2 | Vela | `parecer-36-Vela.md` | PASSA |
| 10 r2 | Cinzel | `parecer-10-Cinzel.md` | PASSA; Docker 33+21 |
| 16 | Trilho | `parecer-16-Trilho.md` | leitura intermediária, sem rodada |

Fila pesada: `etapas/fila-pesada.md` (o maestro ordena; quem solta avisa o próximo). Scripts meus de Docker em
`etapas/logs/fiel-docker-*.sh` (criam e apagam a trava). Regras novas: até 1 subagente leve e 3 Haiku 5.5 (tarefa
simples ou QA); construtor não roda a suíte inteira (o Rebite roda na junção).

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
