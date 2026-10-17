# 39: A vigia grava a mensagem limpa no estado

Type: task
Status: ready-for-agent
Etapa: conserto do 16 (fora da sequência)
Blocked by: 16

**What to build:** Quando o kit do banco falha, o item `sincronizador` do `estado.json` leva o erro do PowerShell com
códigos de cor (`\u001b[31;1m...`) e o caminho do `TEMP` no resumo (achado da Vela no 17, com um `par.env` sem
`HUB_OUTRO_PAR_URL`). A tela do 17 já tira as cores, mas o texto vem do 16 (`vigia.mjs` / `kit.ps1`): a vigia passa a
gravar só a mensagem limpa (sem sequências de cor; caminho do `TEMP` trocado por um rótulo ou tirado), em todo item.

**Fonte:** achado da Vela no 17 (2026-10-17 ~11h45).

**Blocked by:** 16 (resolvido)

- [ ] com o kit falhando por falta de `HUB_OUTRO_PAR_URL`, o item do `estado.json` não tem sequência de cor nem caminho do `TEMP`
- [ ] os outros itens também passam pela limpeza
- [ ] a suíte segue verde

## Comments

- 2026-10-17 11h45 (maestro): publicado pelo achado da Vela. Dono: o Trilho (fez o 16), depois do 38.
