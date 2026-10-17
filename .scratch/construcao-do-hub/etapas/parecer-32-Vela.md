# Parecer do Fiel — ticket 32, link para fora do hub (Vela)

## Rodada 1 — 2026-10-17 — ramo ticket-32 em 94c42ac

Veredito: **volta**, por um conserto. Revisado pelo Fiel sozinho; leitura do Fielzinho fica para depois.

Conferido: integracao 5d84d76 ancestral; worktree limpo. Diff de `lib/pastas.mjs` lido. `27-pastas`: 17/17.
Sonda no hub de ensaio (`verificar-pastas --corrigir`, `HUB_PAR_ID=pc`, duas passadas):
`[y](C:\Projetos\x\README.md#sec)` → `[y](par://pc/C/Projetos/x/README.md#sec)`; caminho absoluto para dentro do hub
→ link sem unidade; segunda passada não desfaz. Critérios 1 a 3 atendidos nos exemplos do ticket.

### Conserto

1. **Caminho com espaço gera link quebrado.** `[[C:/Meus Docs/x.md]]` → `[x](par://pc/C/Meus Docs/x.md)`. Destino de
   link Markdown com espaço não é link (CommonMark; o Obsidian também pede `%20` ou `<...>`), e a passada seguinte
   nem o reconhece (o `MARKDOWN` não casa espaço). Codificar o caminho (`%20`) ou usar `<...>` no destino; teste com
   espaço, de wikilink e de `file:///` com `%20`. Pastas do Windows com espaço são comuns (`Program Files`, OneDrive).

### Ressalvas (não seguram)

- Imagem embutida para fora (`![img](C:/...png)`) perde o `!` e vira link; aceitável (par:// não embute), mas vale
  o aviso dizer.
- `[x](C:\Program Files\x.md)` (Markdown com espaço cru) e caminho UNC (`\servidor\...`) ficam como estão, calados.
- Suíte inteira pendente da trava.

## Rodada 2 — 2026-10-17 — ramo ticket-32 em 6beaf15

Veredito: **passa**. Fiel sozinho (Fielzinho lê depois). `27-pastas`: 18/18; worktree limpo. Sonda:
`[[C:/Meus Docs/x (v2).md]]` → `[x (v2)](par://pc/C/Meus%20Docs/x%20%28v2%29.md)`; a segunda passada não muda nada.
Ressalvas da rodada 1 seguem. Suíte inteira pendente da trava: se vier com vermelho, a rodada reabre.
