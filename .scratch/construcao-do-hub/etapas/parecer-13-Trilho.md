# Parecer do Fiel — ticket 13, gemini pronto e desligado (Trilho)

## Rodada 1 — 2026-10-17 — ramo ticket-13 em 6bfb506

Veredito: **passa**. Revisado pelo Fiel sozinho; leitura do Fielzinho fica para depois.

Conferido: integracao 57e85cf ancestral; worktree limpo. Li o ticket 13, o relatório, `gemini.env`, o diff do
`iniciar.ps1` e o teste.

Evidências (Fiel):
1. `13-gemini.test.mjs`: 4/4 (gateway dublê; nada sai para a rede).
2. Critério 1: `gemini.env` só tem `OPENAI_BASE_URL=${FREELLM_BASE_URL}/v1` e `OPENAI_EMBEDDING_MODEL=gemini-embedding-001`
   (modelo explícito, nunca `auto`), sem chave; só `iniciar.ps1 -Gemini` o lê; sem a opção, os `OPENAI_*` saem do
   ambiente e a busca segue no arctic.
3. Critério 2: teste único liberado pelo Gustavo, cota conferida antes (0 de 1000; teto de 250), gasto 62 pedidos,
   resultado gravado em `13-gemini/evidencia/teste-unico.json`; busca por chave (`sk-`, `AIza`, `api_key=`) na
   evidência: nada. O contêiner `freellmapi-freellmapi-1` não está rodando agora.
4. 12-busca pelo índice (f8b8769) e suíte comum (172/8/0): pela evidência do Trilho, com a trava; não repeti (trava
   pesada, a busca indexa).

Ressalvas (não seguram):
- `-Gemini` no hub de verdade reindexaria o índice padrão com o gemini (mesmo `estado` e mesmo banco). O aviso está no
  comentário; uma recusa quando `-Hub` é o hub padrão, ou um banco separado por modelo, tornaria isso impossível de
  fazer sem querer.
- `context_length` de 20 000 do gateway: um vetor por nota no gemini (declarado).
