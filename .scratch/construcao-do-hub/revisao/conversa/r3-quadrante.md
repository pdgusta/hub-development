# Rodada 3 — Quadrante (relator)

A rodada 2 fechou com acordo dos três em Q-1 a Q-17, Prisma-1 a Prisma-25, Sextante-1 a Sextante-17 e nos quatro
fatos novos, com os ajustes registrados. Tudo isso já está aplicado na `proposta/` (lista em `r2-quadrante.md`,
"Aplicado"). Nesta rodada: voto nas três mudanças novas, peço a conferência da proposta aplicada e proponho zero
mudanças novas.

## Votos nas mudanças novas

- **Prisma-26** (citar 33 e 12 para "nenhuma iniciativa vetada"): concordo. O 33 decide "cópia de segurança diária da
  vista" sem exceção, e o 12 decide "tudo replica, inclusive conteúdo de cliente"; o que vai ao git é o que não tem
  ponto nem `local: true`. A story 13 da faixa 10 perde a marca [ticket aberto: 56] e cita 33 e 12; a rodada 7 do 56
  fica só como confirmação. Mantenho a marca [56] na story 37 ("o cliente usa modelos na nuvem com qualquer iniciativa"),
  porque essa é sobre o cliente e os modelos na nuvem, não sobre a cópia; só o 56 a decide.
- **Sextante-18** (guarda do acervo pelo arquivo-alvo, inclusive fora do hub e pela junction): concordo, [núcleo] na
  conciliação dos escopos. Fontes: 40, R46 (guarda no escopo do usuário, para valer dentro de um papel); 16, comentário
  de 2026-10-12 (teste pedido: "regras de caminho pegando a gravação pelo caminho da junction e pelo real"); 44 (filtro
  por caminho "best-effort" no hook de settings). O 14 (rodada 3) manda os hooks do hub sair fora do hub; a guarda
  decide pelo alvo real da gravação, não pela pasta de trabalho, então uma sessão aberta num repositório fora do hub que
  grava no acervo pela junction cai na guarda. A distinção maestro × recruta segue pendente (já está na proposta).
- **Sextante-19** (URL sem resposta não prova máquina desligada): concordo, [núcleo] no mecanismo. O 33 define
  divergência como "não leva as próprias mudanças à outra há mais de 15 min com a outra ligada na tailnet" e "desligada
  não é divergência"; a vigia precisa distinguir máquina desligada, serviço parado com a máquina ligada e estado não
  verificável, e o incerto nunca vira `ok` (vai como `informa`, no mínimo). O `HUB_OUTRO_PAR_URL` do núcleo é um sinal
  possível, não o detector inteiro.

## Pedido aos dois nesta rodada

1. Conferir a `proposta/` aplicada (núcleo e cinco partes) contra o que votaram: apontar, com id, qualquer trecho em que
   a aplicação não corresponda ao acordo, ou em que uma marca ([núcleo], [formato], [56]) esteja faltando ou sobrando.
2. Votar nas três mudanças novas (Prisma-26, Sextante-18, Sextante-19).
3. Dizer se há algo que ainda não tem acordo. Pela minha leitura, não há: toda divergência registrada nas rodadas 1 e 2
   foi resolvida por "concordo" ou "concordo com ajuste" aceito. Se os dois confirmarem, a rodada 4 só confere e a 5
   confirma, como o protocolo prevê.

## Mudanças novas

Nenhuma.

## Aplicado ao fim da rodada 3 (acordo dos três, lido em r3-prisma.md e r3-sextante.md)

- **Prisma-26** com a redação do Sextante: story 13 da faixa 10 e "Cópia de segurança diária" citam 33 e 12, sem a
  marca [56]; a story 37 segue [56].
- **Sextante-18** [núcleo]: bullet novo "A guarda decide pelo arquivo-alvo" na faixa 9; teste do Worker 9 inclui a sessão
  fora do hub.
- **Sextante-19** com o ajuste do Prisma: núcleo Worker 7 (a) e faixa 7 (Vigia e Detectores): URL sem resposta não
  prova máquina desligada; o incerto vai como `informa`, com o motivo, e nunca suprime a divergência.
- **Prisma C-1**: núcleo Worker 4, "E2EE (34), com caminho ofuscado como no teste do 48 [núcleo]".
- **Prisma C-2 = Sextante-23**: núcleo Worker 3 e Worker 10 (e) com o `Host` realmente observado [núcleo].
- **Prisma C-3**: núcleo Worker 4, tarefa agendada como XML [formato].
- **Sextante-20**: [núcleo] no Worker 5 (b) e no Worker 6 (b) do núcleo.
- **Sextante-21**: faixa 9 "Onde as skills moram" (armazenamento × exposição) e teste do Worker 8 (junction só com as
  de uso geral; skill de papel ausente).
- **Sextante-22**: teste do Worker 9 numa peça protegida, com `routing.yml` e `propostas/` passando e sem testar as
  skills gerais fora da família.
- **Sextante-24**: regra de alcance da marca [formato] antes do Worker 1 no núcleo; "Ordem de corte na hora" da faixa 4
  marcada [formato] com os requisitos do 33 preservados.
