# r1 — Junco: o uso real do Gustavo contra os métodos

**Lente.** Testo cada método contra o dia a dia (nota de retomada achável sem busca, dado de cliente
numa máquina só, caminho fixo de skills) e contra o erro do vault: cortar por tipo de documento.

## O que os JSON dizem de verdade

- Só **PARA** (`01-para.json`) corta a raiz por ciclo de vida: projeto termina, área "continues
  indefinitely", arquivo é o que parou. É a única que cobre a coluna "Termina?" do briefing.
- Cinco métodos não definem raiz: `03`, `04`, `05`, `13`, `14`. Não sustentam pasta.
- "Quando envelhece" é `nao_verificado` em 02, 04, 06, 08, 10, 11, 13 e 14. Só PARA, XDG runtime
  (`09`) e o memory tool (`12`, "Periodically delete") dizem algo. "Todo arquivo tem destino" é regra
  nossa.
- Repetem o vault: Diátaxis (`06`) corta por forma de documento; Cline (`10`) fixa seis arquivos por
  função e manda "read ALL" no início, o oposto de camada de busca e textos curtos; Johnny.Decimal
  (`02`) tem "an index to link everything together"; Evergreen (`14`) fatia "by concept (rather than
  by ... project)", o que desfaz o isolamento por iniciativa.

## O achado que importa: FHS decide a pasta não replicada

`08-fhs.json`: "files that differ in either of these respects should be located in different
directories" (compartilhável × não). Traduzido: **o que não replica não divide pasta com o que
replica**. Isso testa os nove tipos:

- 1 e 2 têm dado de cliente: pasta não replicável.
- 3, 4 e 6 não têm: replicados.
- 5, 7 e 8 dizem "às vezes": o critério é violado ali. Regra proposta: dado de cliente nunca mora em
  5; vive em 1 ou 2 e só sobe sanitizado, por promoção explícita. 7 e 8 são o problema real.

## Os nove (voto provisório)

1. **Clientes: manter.** PARA Projects (`01`) + FHS (`08`).
2. **Operações contínuas: manter, separado de 1.** PARA Areas × Projects (`01`); destino diferente
   (compactar × arquivo).
3. **Produtos e frentes: manter.** PARA não encaixa limpo ("por versão" não é projeto nem área).
   Basic Memory (`11`) usa projeto como unidade, com diretório declarado.
4. **Estudo e laboratório: manter, evidência fraca.** Só PARA Resources ("learning about", `01`)
   toca; nenhum JSON diz que merece raiz própria. Defendo pela promoção explícita para 5.
5. **Referência: manter**, com a regra acima. PARA Resources (`01`), References do Ango (`07`),
   estático no FHS (`08`).
6. **Oficina: manter.** XDG separa config de data (`09`); `.claude` fixa caminho e escopo pessoal ×
   projeto (`15`); "mais importante vence" (`09`) serve a contrato global × de projeto.
7. **Entrada: manter, declarada não replicada.** GTD capture→clarify (`05`: trash, reference, on
   hold) dá o ciclo; XDG runtime "MAY be subjected to periodic clean-up" (`09`). Se "às vezes" traz
   cliente, o padrão seguro é local.
8. **Arquivo: cortar como raiz; virar estado dentro de cada raiz.** PARA põe Archives na raiz
   (`01`), mas `01` não trata replicação. Pelo FHS (`08`), arquivar VOEGOL num `arquivo/`
   replicado vaza dado de cliente e arranca a iniciativa da casa (a lição "iniciativa espalhada").
   Um `_arquivo/` por raiz herda a regra de replicação. Inferência minha, não está nos JSON; o estado
   no frontmatter cobre a exclusão da busca.
9. **Pessoal: não decidir sem exemplo real.** Ango (`07`): raiz = "something I wrote, or relates
   directly to me"; FHS `/home` "(optional)" (`08`). Sustenta existir, não diz o quê. Perguntar ao
   Gustavo; se for dado que não replica, o FHS o justifica.

## Pergunta aos outros

Astrolabio, Cinzel: o que sustenta 8 como raiz além de PARA? E como 5 e 7 evitam vazar dado de
cliente sem um critério como o do FHS?
