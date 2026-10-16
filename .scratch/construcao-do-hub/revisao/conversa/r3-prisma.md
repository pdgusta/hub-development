# Rodada 3: Prisma

Li `r2-sextante.md`, `r3-quadrante.md` e o "Aplicado" de `r2-quadrante.md`. Conferi a `proposta/` contra `antes/` por
diff: o núcleo e as cinco partes, com mais cuidado nas faixas 4 a 10 (os meus tickets).

## 1. Votos nas mudanças novas

- **Prisma-26** (citar 33 e 12 para "nenhuma iniciativa vetada"): concordo com o ajuste do Quadrante. A story 13 e a
  frase de "Cópia de segurança diária" citam 33 e 12, sem a marca [56]; a story 37 (cliente nos modelos na nuvem)
  segue [56], porque é sobre o cliente, não sobre a cópia.
- **Sextante-18** (guarda pelo arquivo-alvo, inclusive fora do hub e pela junction): concordo, [núcleo] na
  conciliação. A guarda decide pelo caminho real da gravação (40, R46; 16, comentário de 2026-10-12, teste pelo caminho
  real e pela junction), não pela pasta onde a sessão abriu.
- **Sextante-19** (URL sem resposta não prova par desligado): concordo, [núcleo] no mecanismo. Ajuste pequeno de texto:
  o caso incerto nunca vira `ok` nem suprime a divergência de replicação parada; vai, no mínimo, como `informa`, com o
  motivo ("outro par sem resposta; não sei se está desligado"). Fonte: 33, Answer (divergência só com a outra ligada;
  desligada só informa a hora da última troca); 33, R63.

## 2. Conferência da proposta aplicada

O que votei nas rodadas 1 e 2 está aplicado como combinado nas faixas 5, 6, 7, 8, 9 e 10 e no núcleo. Achei quatro
pontos, todos pequenos:

- **C-1 (núcleo, Worker 4):** "**E2EE com caminho ofuscado** (34)". O 34 decide a E2EE; o caminho ofuscado vem do teste
  do 48 (item 11, "E2EE v2, metadados internos cifrados e caminho ofuscado"), que testou, não decidiu. Proposta: "E2EE
  (34), com caminho ofuscado como no teste do 48 **[núcleo]**". A faixa 7 já cita o 48 certo.
- **C-2 (núcleo, Worker 3 e Worker 10 (e)):** o ajuste da Prisma-23 (Sextante: configurar o `--allowed-host` com o `Host`
  realmente observado, não assumir o endereço do proxy) entrou na faixa 10, mas o núcleo ainda diz "subo com
  `--allowed-host` para o endereço do proxy que a faixa 10 disser" (Worker 3) e "a faixa 3 a usa no `--allowed-host`"
  (Worker 10 (e)). Proposta: o mesmo texto da faixa 10 nos dois lugares, com [núcleo].
- **C-3 (núcleo, Worker 4):** "roda em laço no terminal, e a tarefa agendada sai como XML" sem marca. É o mesmo caso da
  vigia (Prisma-25), que ficou [formato]. Proposta: marcar [formato] ali também; a tarefa agendada em si é requisito do 33.
- **C-4 (esperado, só registro):** story 13 da faixa 10 e núcleo Worker 7 (a) aguardam esta rodada (Prisma-26 e
  Sextante-19).

Marcas faltando ou sobrando: fora de C-1 e C-3, não achei nenhuma nas faixas 4 a 10. Não conferi linha a linha as
faixas 1 a 3 (são do Sextante).

## 3. Sobra algo sem acordo?

Não, pela minha leitura. Toda mudança das rodadas 1 e 2 tem "concordo" ou "concordo com ajuste" aceito pelos três; as
três novas desta rodada eu aprovo. C-1 a C-3 são alinhamento ao que já foi acordado, não decisão nova. Concordo que a
rodada 4 só confira e a 5 confirme.

## Mudanças novas

Nenhuma, fora C-1 a C-3 acima.
