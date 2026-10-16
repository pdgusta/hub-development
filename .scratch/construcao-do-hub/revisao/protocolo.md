# Protocolo da revisão conversada do spec (2026-10-16)

Pedido do Gustavo: "3 revisores conversem entre eles por 5 rodadas até entrar num acordo, à luz de TODOS os tickets já
definidos, como o spec deve ficar". Depois o maestro compara a versão de antes com a proposta e pergunta ao Gustavo.

## Quem

- **Quadrante** (Claude Fable 5.1): relator. Conduz as rodadas e é o único que edita a proposta.
- **Prisma** (Claude Opus 5.5) e **Sextante** (Codex GPT 6.1 Sol): revisores. Não editam a proposta.
- Os três estão ligados entre si e ao maestro ("Claude Code") no canvas do Maestri. Sem subagentes.

## Arquivos (todos em `C:\Projetos\context-hub\.scratch\construcao-do-hub\revisao\`)

- `antes/`: cópia do spec como estava. **Ninguém mexe.**
- `proposta/`: `spec.md` e `spec-partes/`, a versão que vocês propõem. Só o Quadrante edita.
- `conversa/rN-<nome>.md`: o que cada um escreve na rodada N (um arquivo por pessoa por rodada, para ninguém gravar por
  cima de ninguém).
- `acordo.md`: o fechamento, escrito pelo Quadrante na rodada 5.
- Insumos já prontos: `divergencias-prisma.md` (34), `divergencias-sextante.md` (15) e `triagem.md` (o agrupamento do
  maestro).

## O que vale como decisão

- Só o que consta de um ticket **resolvido** em `C:\Projetos\context-hub\.scratch\context-hub\issues\` (Answer e
  Comments) e o resumo em "Decisions so far" do `map.md`. Ticket mais recente vence o mais antigo; diga qual e por quê.
- O ticket 56 (laço do system design) está **aberto**: o que vem dele é "vem de ticket aberto", não decisão.
- O que só o núcleo do spec decidiu, sem ticket, é "escolha do núcleo": pode ficar na proposta, mas marcado assim, para o
  Gustavo dar aval.
- **Formato da execução** (faixas, 1 hora, 10 workers, dublês, minutos, quem é dono de quê): não decidam. O Gustavo vai
  ajustar o plano depois; a ideia inicial dele é cada faixa virar uma etapa sequencial. Marquem "depende do formato" e,
  se ajudar, digam o que muda com etapas sequenciais.

## Divisão da leitura

Todos leem o `map.md` ("Decisions so far"), a proposta inteira e os insumos. Cada um lê **por inteiro** um terço dos
tickets e traz à conversa o que eles decidem sobre o spec:

- **Sextante:** 01, 02, 03, 04, 09, 10, 12, 19, 20, 21, 35, 49, 50, 54.
- **Prisma:** 05, 06, 07, 08, 11, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 47, 48 e o 56 (aberto).
- **Quadrante:** 13, 14, 15, 16, 18, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 52, 53, 55.

Quem precisar de um ticket de outro grupo pode abri-lo, ou perguntar a quem o leu (`maestri ask "<nome>" "..."`).

## As 5 rodadas

1. **Rodada 1:** cada um escreve `conversa/r1-<nome>.md` com as mudanças que propõe ao spec. Cada mudança com id
   (`<nome>-<n>`), onde no spec, o texto atual, o texto proposto e a fonte (ticket e trecho). Inclui as divergências
   dos insumos que continuam valendo.
2. **Rodadas 2 a 4:** cada um lê as rodadas anteriores dos outros e escreve `conversa/rN-<nome>.md`: para cada
   mudança, "concordo", "discordo, porque..." (com fonte) ou "concordo com ajuste: ...". Pode propor mudança nova. Ao fim
   de cada rodada, o Quadrante aplica na `proposta/` o que tem o acordo dos três e lista no próprio arquivo da rodada o
   que aplicou.
3. **Rodada 5 (fechamento):** cada um dá o voto final nas pendências. O Quadrante aplica os últimos acordos e grava
   `acordo.md` com: (a) mudanças aplicadas, uma linha cada, com a fonte; (b) sem acordo, com a posição de cada um;
   (c) escolhas do núcleo sem ticket que ficaram; (d) o que depende do formato da execução.

**Condução:** o Quadrante abre cada rodada com `maestri ask` aos dois ("rodada N aberta"); cada revisor, ao gravar o
seu arquivo, responde `maestri ask "Quadrante" "<nome>: rodada N gravada"`. Ninguém pula rodada. Se o acordo chegar antes
da rodada 5, a rodada 5 só confirma.

**Fim:** o Quadrante avisa o maestro: `maestri ask "Claude Code" "Quadrante: revisão conversada pronta, acordo em
<caminho>"`. Se travar, avisa do mesmo jeito.

## Regras

- pt-BR, frases curtas. Grave a cada passo: um `/clear` a qualquer momento não pode perder nada.
- Dados de cliente (STRATA, VOEGOL, AVIANCA, TRF3, SBF): cite a iniciativa pelo nome; dados pessoais não entram.
- Nada de testes, varreduras ou mudanças fora de `revisao/`.

## Fatos novos do Gustavo (2026-10-16, ~15h35, registrados no ticket 16)

- O TI já confirmou: o Tailscale no notebook não tem risco nem conflito com o software corporativo. A "consulta ao TI"
  deixa de ser pendência.
- O laço do system design (ticket 56) só continua depois da construção: o que vem dele fica fora da construção ou
  marcado como "vem de ticket aberto".
- As políticas do Copilot da empresa foram conferidas: não há política aplicada nesta máquina.
- O Gustavo vai ligar o Docker Desktop e criar o repositório privado do hub no GitHub.
