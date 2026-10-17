# Relatório do ticket 33: link fora do hub, imagem, espaço cru e caminho de rede (Trilho, 2026-10-17)

Ramo `ticket-33`, worktree `C:/context-hub-wt/ticket-33`, de `integracao` 3c24d68. Código do 27 e do 32
(`agents/code/bin/lib/pastas.mjs`, `agents/code/bin/verificar-pastas.mjs`).

## Feito
- 4323d0c, imagem: o `!` passa adiante no `paraPar` e no `peloAbsoluto`. `![foto](C:/Imagens/x.png)` vira
  `![foto](par://<par>/C/Imagens/x.png)`; `![[C:/Imagens/y.png]]` vira `![y.png](par://...)` (o rótulo segue a regra do
  32: só o `.md` sai); imagem para pasta que não replica também. A volta (par:// para o que replica) já mantinha o `!`;
  agora há teste. A segunda passada não muda nada.
- aea27ff, espaço cru: `corrigirLinks` devolve `alertas` (o que fica como está e merece aviso a cada passada), além de
  `avisos` (o que a troca fez) e `faltas`. O verificador imprime cada alerta como `aviso:` (sai 0), com ou sem
  `--corrigir`. `[x](C:\Program Files\x.md)` e `[y](inbox/minha nota.md)` avisam; `[t](url "título")` (título do
  CommonMark) não.
- 07e6b92, caminho de rede: `\servidor\...`, `//servidor/...` e `file://servidor/...` (não `file:///C:/`), em link
  Markdown ou wikilink, ficam como estão e avisam. Antes, `[x](\servidor\pasta\x.md)` caía em `alvoNoHub` como
  `servidor/pasta/x.md`.
- O fim da resposta (27) já repassa os avisos do verificador ao agente, uma vez por sessão, sem gastar devolução.

## Testes
- `node --test agents/code/test/27-pastas.test.mjs agents/code/test/27-fim-da-resposta.test.mjs`: 37 passam.
- Suíte inteira só na junção (regra nova).

## Downloads, login, Docker
Nenhum.
