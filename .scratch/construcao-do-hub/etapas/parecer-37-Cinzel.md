# Parecer do ticket 37 (Cinzel): o fim da resposta vê a gravação feita pelo shell

## Rodada 1 — 2026-10-17 ~10h45 (Fiel sozinho; Fielzinho sem cota até 12h15, leitura dele pendente)

Ramo `ticket-37` (worktree `C:/context-hub-wt/ticket-37`), HEAD c16e53f sobre o `ticket-18` 31afe63.

**Veredito: VOLTA** (1 conserto).

### Consertos

1. **Com shell no turno, a nota de retomada gravada por outro processo vira falta desta sessão e ganha o
   `last_agent` dela** (Fiel). `nucleo.mjs`, `fim()`: `notasDeFora` (todo `ehNota` com mtime desde a marca, fora dos
   `.gravados`) entra no `conferirRetomada` e no `gravarUltimoAgente`. Mas o fim não sabe quem gravou: o relatório
   (ressalva 1) diz "é só aviso", e para a nota não é. É o mesmo defeito do conserto 1 do 18 r1 (cobrar nota pela
   gravação de outra sessão), de volta no caso do shell.
   Sonda (cópia do `37-gravacao-pelo-shell.test.mjs` com dois casos, apagada depois):
   - a sessão Claude roda um shell que só lê (`git status`); o "sincronizador" grava a `retomada.md` da aurora sem o
     **Onde parou:** → o fim **devolve**: "O verificador do hub achou o que falta no que você gravou nesta resposta ...
     faltam campos da nota de retomada: **Onde parou:**"; e o fim grava `last_agent: "claude-code"` nessa nota;
   - mesma coisa com a nota completa → solta, mas o `last_agent` da nota passa de `"claude-code opus"` (da outra
     máquina) para `"claude-code"` (desta sessão). A gravação vira uma edição nova desta máquina sobre a da outra:
     risco de conflito no LiveSync.
   Conserto: o que veio de fora das ferramentas não pode virar falta nem gravar `last_agent`, porque o fim não sabe
   quem gravou. Caminho simples: a nota de fora entra no aviso "Antes de terminar" (com um texto como "a nota de
   retomada mudou fora das ferramentas: confira se é sua e se tem os sete campos"). Isso mexe no ajuste (a) da Vela;
   combinar com ela (dona do núcleo) e, se preciso, com o maestro. Teste: os dois casos da sonda.

### Ressalvas (não bloqueiam)

- O nome da ferramenta de shell do Codex (`Bash`) vem do achado do 15; sem harness real aqui (aceito pelo maestro).
- O matcher do Claude é regex: `Bash` também casa `BashOutput`; o `anota` então segue pelo caminho dos adaptadores
  (nada a gravar). Sem efeito, só registro.
- Varredura com `cwd` na raiz do hub faz `statSync` de até 20.000 arquivos no Stop; conferir o tempo no hub real.

### Conferido sem conserto

- Critério 1: aviso nos três harnesses pelo evento de cada um (testes 1-3). Critério 2: fora do cwd ou de antes do
  turno, nada. Critério 3: 14, 18, 27 seguem verdes.
- Os três fragmentos com o matcher do shell; a marca do turno apaga o `.shell`.

### Evidências

- `node --test 14-guardas 18-retomada 27-fim-da-resposta 27-pastas 37-gravacao-pelo-shell harness-real` (detector do
  29): 111/111. `git status` limpo.
