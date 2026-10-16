# 09: MCP do banco: gravar com versão e conflito à vista

Type: task
Status: ready-for-agent
Etapa: 3 (MCP do banco)
Blocked by: 07

**What to build:** O fork do MCP do banco grava sempre conferindo a versão lida e mostra o conflito ao agente dos dois jeitos aceitos, contra o banco real da etapa 2.

**Fonte:** Bloco do Worker 5; faixa 5 em `spec-partes/faixas-05-06.md`; tickets 25, 30, 11; escolha aceita 1. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 07 (Banco do par: dois CouchDB, LiveSync e vista `.md`)

- [ ] ler e gravar com a versão lida grava, e a leitura seguinte traz a versão nova
- [ ] gravar com versão velha deixa as duas versões no banco e a resposta diz "conflito: releia e refaça"
- [ ] regravar nota existente sem a versão é recusado
- [ ] a leitura de nota em conflito avisa e lista as versões; a ferramenta de conflitos lista os abertos

## Comments
