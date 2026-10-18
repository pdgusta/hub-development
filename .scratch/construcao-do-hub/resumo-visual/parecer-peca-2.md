# Parecer da peça 2 — "O que atrapalhou e como se resolveu"

Revisor: Esquadro. Designer: Nanquim.

## Conceito (2026-10-17): aprovado, com 7 ajustes

Bom: a metáfora é uma só e carrega a pergunta (a memória é o gargalo, então o rio estreita). Os dados ficam em escala,
na vertical, o oposto da peça 1. O detalhe vai em camadas.

Ajustes:

1. **Baixio de 700 MB.** Hoje ele fica "no meio do leito", e isso não fecha com "largura = memória". Melhor: o **barco
   tem 700 MB de boca** (o corte). Quando o rio fica mais estreito que o barco, ele encalha (✕). Os pisos (2 GB do 08,
   2.500 → 1.800 MB do 25) viram marcas de largura na margem.
2. **Dia 16.** Comprima-o com uma **quebra visível** (traço em zigue-zague e "~10 h sem medida"). A escala só fica
   constante da madrugada de 17 em diante. Dez horas de rio "sem sondagem" empurram o gargalo para baixo da dobra.
   Os eventos do dia 16 continuam na peça.
3. **Horas do diário de ~03h a ~04h45.** Elas estão adiantadas ~1 h. Não use "~". Use a hora real do commit, que está
   no git deste repositório. Exemplos: mandato de autonomia 03:19 (d7a0f33); 4 construtores 03:23 (2e605d1);
   subagentes Haiku 03:25 (8493aaf); 12 e 15 só com a search 03:14 (142a47f).
4. **Os CSV de medida estão em UTC** (sufixo Z). Exemplo: 12:59Z = 09:59 no horário local. Converta para −03:00 antes
   de pôr na escala.
5. **Sondagens.** A memória medida é esparsa: as rondas e os eventos do diário, mais os CSV do 25. O rio entre duas
   sondagens é interpolação. Desenhe a margem lisa e fina entre as medidas. Os números escritos são só os medidos.
   Não invente picos.
6. **Carga visual.** Barcos, pedras, pontes, placas, afluente, barragens e pontos de recrutas, tudo junto, viram ruído.
   Prioridade: rio, encalhes, barcos e pedras com ponte. Placas e afluente vêm em segundo. Os pontos de recruta só
   aparecem nas janelas quietas (quem ficou), não o dia todo.
7. **Dois episódios da trava merecem desenho próprio:** a trava sobrescrita (~01h08, duas suítes juntas, Brasa e
   Trilho) e a corrida na trava (05:48, o corredor da Brasa furando a fila). Desenhe dois barcos lado a lado no canal.

Para o arquivo de fatos:
- A redefinição do Codex é **14:26** no diário (linha 160), não 14h25.
- O reinício do Windows é **21:10**, com 714 MB livres (retomada-maestro.md:117).
- "Suíte interrompida 00h35": preciso ver a fonte.
- Toda pedra precisa da hora do achado **e** da hora do conserto, cada uma com fonte. Sem a do conserto, não tem ponte.

## Volta 1 (2026-10-17 ~22h): VOLTA — 3 consertos visuais + consertos de fato

Capturas: 1600 e 390 px, no Edge sem cabeça (porta 8774). O cartão (#cartao=d2-25-nota-nao-desce) abre bem.
Conferência: 774 fatos. Memória: as 540 sondagens batem (CSV convertidos a −03 sem erro). Todos os hashes
existem. Os seis achados do brief estão presentes com o conserto certo.

**Pela régua, passa no essencial.** Uma metáfora só, que carrega a pergunta (onde o rio estreita, o pesado encalha).
Dados medidos e em escala, números grandes, detalhe no toque, legível em 390. Bem diferente da peça 1. Os ajustes do
conceito entraram.

### Consertos obrigatórios

**Visuais**

1. **Grade das horas deslocada 30 min.** As linhas saem de múltiplos de 60 min contados desde 14h30
   (modelo-peca-2.html:157-158). Por isso a linha "10h" é 10h30, a "14h" é 14h30, e assim por diante. Os dados estão
   certos, só a grade está errada: ela faz a barragem do Maestri (~10h05) parecer 09h35 e a comporta das 14h26
   parecer 13h56. Ponha a grade nas horas cheias.
2. **Rótulos encavalados.**
   - Em 1600: "Maestri reiniciado (atualização)" fica sobre "proxy sem instructions: no radar (22)". O rótulo
     "janela quieta / no canvas só" da 1ª janela fica sobre a pedra "teste citava linha já trocada (25)" e o chip da
     Vela. A sondagem "0,7" fica sobre a barragem do Windows.
   - Em 390: o rio atravessa os três títulos "janela quieta". "Maestri reiniciado" cobre a sondagem "1,1" e "guardar
     os 3 reinícios". "17/10 00h" fica sob o rio. "0,7" fica sobre "Windows reinicia".
3. **Losangos sem rótulo.** Cerca de 30 marcos de decisão na coluna da direita não têm texto nenhum (1600 e 390).
   Símbolo sem palavra é ruído. Agrupe os marcos próximos num só, com o número ("3 decisões") e a lista no toque, ou
   dê a cada um um rótulo curto.

**Fatos**

4. **Encalhes, no detalhe do número 12.** O texto diz "três mortos pelo sistema… e nove cortes do medidor". A lista
   tem 4 que não são do medidor (o 07 duas vezes, a suíte das 00h35 e o Docker do 08) e 8 do medidor. A fonte do
   Docker do 08 também diverge: relatorio-08-banco-limites.md:113 diz "parada pelo Claude Code", e issues/08:25 diz
   "pelo sistema". Escreva "quatro quedas fora do medidor e oito cortes do medidor" e não use "pelo sistema" no do 08.
5. **Trava com dois donos ao mesmo tempo.** Nesses trechos a barra mostra dois donos juntos, o que não houve:
   - trava[66] (Vela, Codex do 18): o ini 14:55 está errado. O Rebite tinha a trava até ~15:18
     (juncao-41-40-43-docs-suite.log, gravado 15:18:09). O 18-codex.log (42 s) é das 15:19:32. Use ini ~15:18.
   - trava[68] (Rebite, suíte do 11 + docs): o ini 15:33 está errado. O log tem 2.100 s e foi gravado às 16:15:18,
     então ini ~15:40. A nota da trava já diz "depois das 15:43".
   - Também se cruzam, por inícios inferidos: trava[1] com trava[0] (a suíte do Rebite deve começar ~00:45) e
     trava[6] com trava[5] (01:50-02:21). Recorte cada barra inferida para não invadir a do vizinho.
6. **Achado depois do conserto.** Em achados[9] (CRLF, conserto 050fb14 às 02:03) e achados[39] (fase 7 "verde" sem
   harness, dac76e6 às 19:09), a hora escrita do achado vem depois do conserto, porque é a hora do registro. Use a
   hora do `t` no texto também.
7. **Horas de achado.**
   - achados[34]: a 1ª queda A→B foi às **14:06**, não 14:17 (etapas/diagnostico-25-nota-nao-desce.md).
   - achados[35] (link em código inline): foi às **15:18** (issues/44:30). Hoje o `t` diz 15:20 e o texto diz 15:22.
   - achados[3]: foi às ~21:20, não ~21:30 (issues/07:24).
8. **regras[4]:** troque "antes: até 3 agentes" por "até 3 construtores" (2e605d1).
9. **Códigos sem palavras.** Pela régua, "ticket 22" pode aparecer, mas diga o que ele é. Faltam palavras em:
   - decisões com rótulo: "faixa 5 do banco (09)", "16 começa antes dos bloqueios", "(16)", "(09)", "17 começa antes
     do 16", "(17)", "18 começa sobre o 17", "18: opção A", "23 começa antes dos bloqueios", "(22)", "25 fecha sem o
     Codex nas fases 4-7", "nota A→B";
   - textos de cartão: d32, d39, d46, d47 e d54;
   - regras[7] ("fatia 2") e regras[13] ("ticket 26");
   - o fecho e a foz ("o 26");
   - achados[1] ("ticket 36");
   - o `curto` de achados[35] ("27-pastas").

   No rótulo curto, basta o nome em palavras (ex.: "vigia (16)" → "a vigia"). O número fica no cartão, com o nome.
10. **Dado pessoal.** "GUSTAV~1.DEL" aparece na causa de achados[20] e de achados[26]. Escreva "o nome curto do
    Windows (8.3)", sem o nome.
11. **Junções desfeitas:** use uma fonte só para as horas. O registro dá 10:46 e 12:37; o diário dá 10:49 e 12:46.
    Sugiro o registro de junções.

### Ressalvas (não obrigam)

- O 448 MB das 14:18 é o mínimo global, e isso confere. Só que, pelos logs, a fase 4 já tinha sido cortada às 14:17:47.
  "Logo depois do corte da fase 4" é mais exato que "fase 4 rodando".
- `codex_inicio` 20:00 e codex[1] ini ~22:00 não têm fonte de início. Se ficarem, marque como "desde antes de".
- Faltam na trava dois trechos menores: o 12-busca do 41 (~12:55-13:10) e o da junção dos docs (12:37).
- Os pontos que você pôs para eu julgar: (1) as medidas de fora da pasta podem ficar, com a marca no cartão. (2) A ponta
  inferida, apagada e com até 45 min, pode ficar, desde que não invada o barco vizinho (item 5). (3) Fechar a janela às
  18h20 pode ficar. (4) Os 12 encalhes podem ficar. (5) Só 3 bugs da revisão pode ficar. (6) Os dois relatos no cartão
  da trava sobrescrita podem ficar.
