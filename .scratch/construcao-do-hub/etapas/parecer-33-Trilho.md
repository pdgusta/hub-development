# Ticket 33 — Trilho — parecer do Fiel — rodada 1

2026-10-17 ~04h45. Ramo ticket-33, HEAD 07e6b92; contém integracao. Fiel sozinho (Fielzinho sem cota até 06h58;
leitura dele pendente).

## Veredito: PASSA (com ressalvas)

## Conferido
- `node --test 27-pastas.test.mjs 27-fim-da-resposta.test.mjs`: 37/37 (Fiel). Árvore limpa. Suíte inteira: na junção.
- Sonda direta em `corrigirLinks` (parId p1), 14 casos:
  - `![foto](C:/Imagens/x.png)` → `![foto](par://p1/C/Imagens/x.png)`; `![[C:/Imagens/x.png]]` →
    `![x.png](par://...)`; `![b](.local/b.png)` → `![b](par://p1/.local/b.png)`; a volta (par:// para o que replica)
    mantém o `!` (código na linha ~216 e teste da linha 136).
  - `[x](C:\Program Files\x.md)` fica e alerta; `[x](<C:/Program Files/x.md>)` não alerta; `[t](C:/x.md "título")`
    não alerta; espaço no caminho com título alerta (correto).
  - `[x](\servidor\...)`, `[[\servidor\...]]`, `[x](//servidor/...)`, `[x](file://servidor/...)` ficam e alertam.
  - Em `[a](C:/Imagens/a b.png) e ![b](C:/Imagens/b.png)`, o primeiro fica com alerta e o segundo vira par://.
- `verificar-pastas.mjs` imprime cada alerta como `aviso:` a cada passada, com ou sem `--corrigir`.

## Ressalvas (não bloqueiam)
1. Caminho de rede solto no texto (`\servidor\pasta\x.md` sem ser link) não avisa. O ticket cita o caminho sem a
   forma de link. Li como link, pelo título do ticket e pelo 32, que só trata links. Se o Gustavo quis o texto solto,
   fica para outro ticket.
2. Link dentro de código em linha (`` `[x](a b.md)` ``) também alerta, a cada passada: só os blocos cercados ficam de
   fora (igual à troca do 27/32).
3. `[x](//host/x)` (URL relativa ao protocolo) cai como caminho de rede: aviso a mais, sem reescrever.
