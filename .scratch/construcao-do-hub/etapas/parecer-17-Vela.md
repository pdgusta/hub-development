# Parecer do ticket 17 (Vela): vigia nas telas dos harnesses

## Rodada 1 — 2026-10-17 ~08h (ramo ticket-17, HEAD 86c5a88, com integracao 9cc878b)

Veredito: **VOLTA**, em acordo com o Fielzinho (`parecer-17-Vela-fielzinho.md`), por 1 conserto. A junção continua
dependendo do 16 resolvido (relatório, "Falta" 1).

### Conferido pelo Fiel

- Árvore limpa. `node --test agents/code/test/17-vigia-tela.test.mjs`: 15/15.
- Li `tela.mjs` inteiro, relatório e costuras aceitas. Reserva pelo MCP (initialize, sessão, Bearer, SSE) e notify do
  Codex com assinatura e troca atômica, como nas costuras. Evidência real e hashes: leitura do Fielzinho (seis
  respostas, notify uma vez, `apagado`).

### Consertos

1. **(Fielzinho; reproduzido pelo Fiel) Estado sem passada vira "tudo em ordem".** `agents/code/bin/lib/vigia.mjs`
   (`gravarItem`/`tirarItem`, usados por `verificar-acervo.mjs` e pelo `fim-da-resposta/nucleo.mjs`) cria ou regrava o
   `estado.json` sem `passada` quando a vigia nunca rodou nessa máquina: `{"nivel":"ok","resumo":"tudo em ordem",
   "itens":[]}`. O `tela.mjs` lê isso como passada válida: `inicio` → "Vigia do hub: tudo em ordem (passada às Invalid
   Date)."; `barra` → "hub: em ordem (Invalid Date)". Afirma a sincronização conferida sem nenhuma passada (o spec pede
   o contrário: o incerto nunca vira `ok`). Reprodução: `etapas/logs/repro-17-fielzinho.mjs` (log `.log`), repetida pelo
   Fiel com o mesmo resultado.
   - Conserto: sem `passada` válida, nunca "em ordem" (nem no `inicio`, nem na `barra`, nem no notify): dizer que a
     vigia ainda não rodou / estado não conferido, e manter os itens que outros hooks gravaram (o aviso do fim da
     resposta e a peça sumida continuam aparecendo). Teste com o estado que a própria `lib/vigia.mjs` grava.

### Ressalvas (não seguram)

1. (Fielzinho) `outro_par.situacao = nao-verificavel` vira "a outra máquina não responde" e perde o `motivo`; o spec
   (faixa 7) distingue máquina desligada, serviço parado e não verificável. Conferir com o `estado.json` real do 16.
2. O teste usa o `estado.json` de exemplo das costuras; o teste sobre o arquivo do `vigia passada` vem quando o 16
   entrar (declarado).
3. Linha de status na tela de verdade e toast real: não verificados (declarado; modo `-p` sem tela).

## Rodada 2 — 2026-10-17 ~08h15 (HEAD 3e8bbc8)

Veredito: **PASSA** (Fiel sozinho: Fielzinho sem cota até 12h15; leitura dele pendente).

- Conserto 1 feito: `rodou(estado)` exige `passada` que o `Date.parse` aceita. Sem ela: o `inicio` diz "a vigia ainda
  não rodou nesta máquina; não diga que a sincronização foi conferida", junto com os itens dos outros hooks; a `barra`
  diz "hub: vigia ainda não rodou" (ou o resumo do item informa com "(vigia ainda não rodou)"); divergência continua
  primeiro. O aviso de "vigia parada" só com passada válida.
- `17-vigia-tela.test.mjs`: 16/16 (Fiel), com o caso novo sobre o estado da própria `lib/vigia.mjs`. A reprodução do
  Fielzinho agora dá "a vigia ainda não rodou" (não confirma mais o defeito). Árvore limpa.
- Ressalvas da rodada 1 seguem; a 1 (nao-verificavel) vai para o teste sobre o estado real do 16. Junção só com o 16.

## Rodada nova de código (junção do 16) — 2026-10-17 ~12h15 (Fiel sozinho; leitura do Fielzinho pendente)

Ramo `ticket-17`, HEAD b6ace6b (merge da `integracao` fdd3760 em 0eed25d, sem conflito; o ramo contém a ponta).
**Veredito: PASSA**; as ressalvas 1 e 2 da r1 saíram.

- Ressalva 1 consertada: `nao-verificavel` diz "não dá para conferir a outra máquina (<motivo>)" e, na barra, "outra
  máquina não verificável"; "sem resposta" segue como antes. Ressalva 2: três testes sobre o `estado.json` que o
  `vigia.mjs passada` grava (dublês do 16).
- Cores: `semCor` tira `\u001b[...m` do texto do JSON antes do parse (arquivo e MCP).
- Fiel: `17-*`, `16-vigia`, `27-*` e o detector do 29: 81/81; `git status` limpo; sem sobra no TEMP.

Ressalvas (não seguram):
- `semCor` só tira SGR (`ESC[...m`); outra sequência (OSC, cursor) passa. E se o texto não parsear depois da troca,
  a tela diz "a vigia não rodou" (arquivo) ou "o MCP não respondeu" (MCP), o que engana. Caso raro.
- O texto colorido nasce no item `sincronizador` do 16: o certo é limpar lá (a Vela levou ao maestro).
- A ressalva 3 da r1 (tela de verdade e toast real) segue.
