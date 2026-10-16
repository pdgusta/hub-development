---
name: regua-da-cidade
description: "Judge or build the system-design city diagram of the Context Hub against Gustavo's six rules: lines never cross, top-down overview, minimum distance between items, names that say what each item references, each item's role makes sense in a city, and reinvent the form instead of restyling. Use when building, reviewing, comparing or scoring any version of the city diagram or a capture of it. Run together with the general critiques; for portal screens other than the city, do not use."
---

# Régua da cidade

A régua do Gustavo para o diagrama de system design do context hub (a "cidade"), escrita como seis regras
verificáveis. Vale para construir, revisar, comparar e dar nota a qualquer versão da cidade ou a uma captura dela.
Não vale para as outras telas do portal.

## Arquivos

- `regras.md`: as seis regras (R1 a R6), cada uma com enunciado, como verificar e limiar, e as regras de comparação
  entre conceitos.
- `como-julgar.md`: o roteiro da nota por dimensão e o formato da lista de consertos.
- `referencias/LEIA.md`: as capturas elogiadas e recusadas pelo Gustavo, com o motivo nas palavras dele. Olhe as
  imagens antes de construir ou julgar.

Fontes de que a régua depende, fora desta pasta:
- `texto-do-hub.md` do laço (rótulos na seção 3, agrupamentos naturais em 3.5, ligações na seção 4, itens "a decidir"
  na seção 7). R4 e R5 se conferem contra ele.
- `GLOSSARY.md` na raiz do projeto.
- A skill `medidas-da-peca` (só no papel QA tester), que mede R1, R3 e parte de R2 e R4.

## Ordem de uso por papel

1. **UI engineer:** lê `regras.md` e as referências **antes** de construir. Escreve, junto da peça, a tabela de R5
   (item, papel no hub, equivalente na cidade) e marca no código os itens, grupos e ligações (atributos em
   `regras.md`, "Marcação na peça"), para a medição não depender de palpite.
2. **UX revisor:** aplica R1, R2, R3 e R6 sobre a **captura** real (nunca sobre o código), junto das críticas gerais
   (`critique-*`). A régua cobre o que é específico da cidade; as críticas cobrem hierarquia, composição, densidade,
   cor e tipografia em geral. Use as duas.
3. **Tech lead:** aplica R4, R5 e R6 contra o `texto-do-hub.md`: nomes, papéis e se a forma é nova.
4. **QA tester:** roda `medidas-da-peca` e confere R1, R3 e os números de R2 e R4 (contagem de rótulos, lista de
   rótulos). Relata; não corrige.

## Formato da resposta

Para cada regra, uma linha:

`R<n> <nome curto>: passa | falha | não verificado. Evidência: <número medido, ou captura e onde olhar>. Conserto: <o que mudar>.`

- "Passa" exige evidência. Sem número nem captura, a regra fica "não verificado", nunca "passa".
- Depois das seis linhas, a nota por dimensão e a lista de consertos, como em `como-julgar.md`. Essa nota é a
  porta do laço (Tech lead e UX revisor, fase de conceitos e de amostra).

## O que esta skill não cobre

Gosto estético genérico (fica nas `critique-*`), animação (a amostra é estática) e movimento de dados.
