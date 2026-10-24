# 54: A busca dentro do vault deixa o CLI do LiveSync lento

Type: task
Status: needs-triage
Etapa: conserto do 26 (achado na instalação do par B)
Blocked by: nenhum

**What to build:** Achado do maestro do par B em 2026-10-21 ~13h45 e confirmado às 13h58
(`.scratch/context-hub/retomada-maestro-par-b.md`, recados ao A). O passo 03 instala a busca em
`C:/context-hub/.local/busca` (8.588 arquivos, 538 MB) antes de o hub descer. A cada arquivo que grava, o CLI do
LiveSync refaz a lista do vault inteiro no filtro de nomes repetidos (`isAcceptedInFilenameDuplicationFactory` →
`getFileNames()` → `scanDirectoryInto`, sem pular pastas com ponto, com `lstat` em cada segmento). No B foram 83.947
`lstat` e 13,6 s por volta; o perfil de CPU deu 62% em `assertNoSymbolicLinks`. Com a busca fora do vault, a descida
foi de 10 arquivos a cada 4 min para cerca de 1 arquivo/s. O custo também vale em regime, no A inclusive (cada evento
de arquivo dispara a varredura inteira; não medido no A).

Caminhos a decidir (antes, fonte primária no código do CLI do LiveSync):
- busca fora do vault (por exemplo, `C:/hub-par/busca`), com o kit e o MCP da busca apontando para lá;
- ou a varredura do CLI sem as pastas com ponto (mudança no fork ou na configuração, se houver opção).

- [ ] decisão registrada aqui
- [ ] conserto no kit, com teste
- [ ] medida no A antes e depois (tempo da varredura com e sem `.local`)

## Comments

- 2026-10-24 (maestro do A): aberto a partir do recado do B. Precisa de triagem: escolher o caminho.
