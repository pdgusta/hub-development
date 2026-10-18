# Parecer da peça 1: "A construção, em partitura"

Revisora: Lupa. Designer: Traço. Página: `resumo-visual/peca-1-partitura.html`. Fatos: `fatos-peca-1.json`.

## Volta 1 (2026-10-17 ~21h50): VOLTA

Capturei em 1600 px e em 390 px (moldura), mais o cartão `#t=23`, todos no Edge sem cabeça, na porta 8772. Os fatos foram conferidos contra o diário, o registro de junções, os tickets, os pareceres e o git.

**O que está bom.** O tempo está em escala e cada sistema mostra só quem toca. A letra com número e nome dá para ler sem tocar. Na ficha, 44 tickets, 43 resolvidos (o 26 está com o Gustavo), 36 voltas, 39 junções e 370 testes conferem. Os construtores dos 43 tickets conferem, e as 44 dependências também. A cadeia até o 25, nas horas dos 14 tickets amostrados, confere com os hashes de início e de junção. O crescendo vai de 11 a 370 e confere com o registro. A redução "O fio que segurou o fim" é a melhor parte da página. O acorde final soma certo: 8 + 16 + 13 + 6 = 43 tickets e 6 + 13 + 9 + 8 = 36 voltas.

### Consertos obrigatórios (fato errado)

1. **Ticket 18, rodadas da revisão.** Hoje aparecem "8h55 volta" e "8h56 passa". O diário:98 às 08:56 fala do ticket 08, não do 18. A rodada 2 do 18 passou às 09:07 (diário:99). A rodada 3 é a rodada curta de ~10h20 (parecer-18-Vela.md:68-70): use ~10h20 aproximada ou deixe sem hora.
2. **Lume entra às 12h05, não 11h55.** O diário:140 diz "12:05: Lume recrutado", e o git confirma (62e93f7, 12:05). O 11h55 vem do quadro aproximado do diário:240. Pela regra da própria peça (o git é o relógio), vale 12h05. Corrija na pauta do maestro, no cartão do Lume e no json.
3. **Junção das 14h47 não é "verde" limpa.** O registro:38 traz 1 falha alheia (a do teste do verificador de pastas), mantida, e os docs ficaram pendentes. Rotule "verde com 1 falha alheia, mantida". Ajuste "37 verdes" no cartão do Rebite para 36 verdes, 1 com falha alheia e 2 desfeitas. Corrija também "1 falhas" para "1 falha".
4. **Código interno e hash no texto visível** (dicas e cartões):
   - troque "12-busca" por "o teste da busca" e "27-pastas" por "o teste do verificador de pastas";
   - tire os hashes soltos e diga em palavras: "integracao voltou a e98a891" / "e7203b4" vira "a integração voltou ao estado anterior"; tire também "merge 7c54148" e "commit 8d8f1b9".
5. **Subtítulo em 390 px.** O subtítulo diz "cada linha são seis horas", mas em 390 cada sistema tem 2 horas. Troque o texto conforme a largura.

### Consertos da régua

6. **A pauta do maestro está quase muda.** O conceito prometeu mandato e regras novas como indicações de expressão, e só há recomeço, etapas, "Lume entra" e fim. Entram, com hora real (o git é o relógio; o diário entre ~03h e ~04h45 está adiantado ~1h):
   - mandato do Gustavo: ~03h20, git d7a0f33 às 03:19 ("mandato de autonomia");
   - 4 construtores e 1 subagente por recruta;
   - subagentes Haiku;
   - suíte inteira só na junção: 04:15 no diário, que já está no relógio real;
   - Codex só para testes;
   - o documentador.

   Palavras curtas, cada uma com fonte no json.
7. **O crescendo não se lê.** A faixa verde tem espessura quase constante, com uma linha diagonal e outra vertical soltas (em 174, 210 e 294/355). Precisa abrir de verdade, como o "<" da dinâmica: estreito no 11, largo no 370. A escala vertical tem que dar diferença visível. Tire as linhas soltas.
8. **Transbordo.** No sistema 02h–08h, o tracejado da prova pendente do 22 (Brasa) passa da barra final e vai até a borda da página. Corte no fim do sistema, como as outras frases.
9. **"· 1 volta" na letra engana.** Ali só contam as voltas sem hora. O 07 e o 28 mostram "1 volta" e têm 2. Escolha uma das saídas:
   - a letra mostra o total de voltas do ticket;
   - a legenda diz "voltas sem hora na fonte".

   Prefiro o total.
10. **Cartão com bolinha invertida.** No cartão, a bolinha cheia é volta e a vazada é passa. Na bula e na pauta do Fiel, a bolinha cheia é passa. Alinhe com a bula.
11. **390 px: sistemas vazios.** Das 14h30 às ~19h, os sistemas de 2 h saem vazios: um com o recomeço e outro só com um tracinho solto. Junte esse trecho num sistema só, com uma indicação ("revisão do spec") ou um compasso de espera numerado, à moda das partituras. Mesmo cuidado nas sobreposições da borda direita da pauta do Fiel (em 390 aparece "22" sobre "2", e em 1600 "41" duas vezes às 14h).

### Ressalvas que não seguram a peça

- "105 rodadas" inclui 6 leituras só do Fielzinho. Escreva "105 rodadas (com as do Fielzinho)".
- A 4ª leva de docs aparece às 15h20, mas o git a7d1517 é das 15:31. Confira qual hora usar.
- O 25 resolvido às 20h18 no ticket, contra o fim às 20h17: aceitável.
- A legenda "○ 2ª leitura (Fielzinho)" quase não aparece na pauta do Fiel. Se a marca existe, deixe visível; se não, tire da bula.

## Volta 2 (2026-10-17 ~22h30): PASSA

Capturei de novo em 1600 px, em 390 px e no cartão `#t=18`. Os 11 consertos estão feitos.

- 1: o Traço tem razão sobre a volta das 8h55, que está no diário:97 e no parecer-18-Vela.md:5. O erro era só o passa das 8h56, que saiu. Agora a rodada 2 aparece às 9h07.
- 2: o Lume entra às 12h05.
- 3: a junção das 14h47 aparece como verde com 1 falha alheia, mantida, e o Rebite conta 36 verdes.
- 4: o texto visível não tem código nem hash; os hashes só aparecem nas fontes do json.
- 5: o subtítulo diz "duas horas" em 390 px.
- 6: a pauta do maestro tem as seis indicações. Conferi os seis hashes no git, todos com a hora certa (d7a0f33 03:19, 2e605d1 03:23, 8493aaf 03:25, 1d3a611 04:15, 62e93f7 12:05, a1c7fb0 14:33).
- 7: o crescendo abre em "<".
- 8: o tracejado do 22 foi cortado no fim do sistema.
- 9: a letra mostra o total de voltas.
- 10: o cartão segue a bula.
- 11: o compasso de espera, com 4, entrou em 390 px, e os rótulos da borda direita do Fiel não se sobrepõem mais.

Ressalvas (não seguram):
- Em 1600 px, o primeiro sistema ainda mostra 4 h quase vazias (14h30–18h30). É fiel à escala, mas o compasso de espera do 390 caberia também aqui.
- O crescendo abre devagar porque a suíte cresce devagar; está certo, só é sutil.

## Rodada curta: visão retilínea horizontal (2026-10-17 ~22h45): VOLTA (3 consertos)

Capturas no Edge sem cabeça, porta 8772:
- 1600×1000: abertura, #hora=900, #hora=1500, #ver=pFio, #ver=pFim e #t=25;
- 1280×720: #hora=900;
- moldura deitada 844×390: abertura, #hora=900 e #t=25;
- moldura em pé 390×844: abertura, #hora=900, #t=25 e #ver=pFim.

Os fatos não mudaram; só o subtítulo.

**O que está bom.** Uma faixa só, sem rolar para baixo, e o tempo em escala de verdade numa linha. Os nomes das pautas ficam presos à esquerda. O compasso de espera (4) agora aparece também na tela larga, o que resolve a ressalva da volta 2. O modo denso, com pílula numerada no celular deitado, é uma boa saída. O cartão vira folha embaixo no celular em pé e funciona. Fio do fim e acorde final ficam lado a lado e leem bem.

### Consertos

1. **A letra some no meio da rolagem.** O número e o nome ficam só no começo da frase. Quem rola até 5h30 ou 15h vê barras compridas sem nome: na Vela, o 25 e o 17; no Cinzel, o 23, o 24 e o 37; no Trilho, o 16. Para saber o que são, precisa tocar, e a régua pede ler sem clique. A letra tem que ficar presa à borda esquerda da área visível enquanto a frase estiver na tela, como os nomes das pautas. Em modo denso, vale o mesmo para a pílula.
2. **A coluna dos nomes vaza.** A letra cortada aparece ao lado dos nomes das pautas: "tificação · 1 volta", "aço cru e caminho de rede avisam", "volta", e os "9" e "8" junto de Fiel e Rebite. A coluna presa precisa de fundo opaco, com o creme do papel e uma sombra leve na borda.
3. **Falta o dia no meio.** Rolando, aparece "9h" sem dizer de qual dia: o "17/10" só aparece junto da 0h. Ponha o dia preso no canto, acima dos nomes ("16/10" ou "17/10", conforme o trecho visível), ou junto de cada hora cheia de 6 em 6 horas.

### Rodada curta, conferência dos consertos (2026-10-17 ~23h): PASSA

Recapturei em 1600×1000 (#hora=300, #hora=900, #hora=1500), na moldura deitada (#hora=900) e na moldura em pé (#hora=1500).

1. A letra presa funciona. Em 5h30 e em 15h aparecem com nome o 08, 28, 17, 16, 15, 10, 25, 23, 24 e 37; no modo denso, vale para as pílulas.
2. A coluna é opaca, com sombra, e nada de "9" ou "8" soltos.
3. O dia fica preso no canto ("17/10").

Ressalvas (não seguram):
- Os tocos de frases que terminam logo depois da coluna ficam sem nome, porque a letra some (por exemplo, o 41 do Trilho e o 43 da Brasa em #hora=1500). É coerente com a regra, e o toque completa.
- Na moldura em pé, aparece um "s" solto ao lado de "Mae.". É resto de uma indicação do maestro, que não seguiu a mesma regra de sumir sob a coluna.
