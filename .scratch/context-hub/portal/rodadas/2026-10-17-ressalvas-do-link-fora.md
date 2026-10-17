---
titulo: Link fora do hub: as três sobras
ticket: 16
aberta: 2026-10-17
estado: aberta
---

**O link para fora do hub entrou** (ticket 32, juntado e resolvido; suíte com 186 testes, nenhuma falha). Na sua
decisão, um link para um arquivo fora do hub vira `par://<máquina>/<unidade>/<caminho>`; o caminho com espaço sai
codificado (`%20`) e o verificador avisa.

**O que o revisor deixou como ressalva**, sem segurar a junção:

1. **Imagem embutida perde o `!`.** `![foto](C:/Imagens/x.png)` vira `[foto](par://...)`: deixa de ser imagem e vira
   link comum, sem aviso. É defeito de verdade.
2. **Link Markdown com espaço cru fica calado.** `[x](C:\Program Files\x.md)` já nasce quebrado (Markdown não aceita
   espaço cru no destino); o verificador não reescreve nem avisa.
3. **Caminho de rede (UNC) fica calado.** `\\servidor\pasta\x.md` não tem unidade; o verificador deixa como está, sem
   aviso.

Hoje quase tudo o que falta construir espera o banco do par (ticket 07, Brasa, na rodada 2 da revisão). A Vela fica
livre depois da prova do 31; um ticket pequeno caberia nela agora.

## As três sobras do link fora do hub
id: sobras-link-fora
tipo: escolha
recomendada: A

- A: Ticket 33 pequeno para a Vela agora: a imagem mantém o `!` (`![foto](par://...)`); espaço cru e caminho de rede passam a gerar aviso do verificador, sem reescrever
- B: Ticket 33 só com a imagem (o defeito); espaço cru e caminho de rede seguem calados
- C: Nada agora: as três viram itens do radar

## Algo mais?
id: algo-mais
tipo: texto
