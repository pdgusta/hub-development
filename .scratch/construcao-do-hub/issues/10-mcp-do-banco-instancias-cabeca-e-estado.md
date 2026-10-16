# 10: MCP do banco: três instâncias, cabeça, regra curta e estado

Type: task
Status: ready-for-agent
Etapa: 3 (MCP do banco)
Blocked by: 09, 05

**What to build:** O MCP do banco completo: três instâncias por máquina (leitura; escrita dos agentes da máquina; escrita só do cliente), a cabeça do `AGENTS.md` relida a cada conexão e posta antes do texto do upstream, a regra curta nas ferramentas de gravação, a cifra de ponta a ponta, a ferramenta `estado_do_hub` com um estado de exemplo no esquema da vigia, e a recusa de nota fora do esquema pelo verificador.

**Fonte:** Bloco do Worker 5; faixa 5; escolhas aceitas 2, 3, 4 e 21; decisão do Gustavo de três instâncias (escolha 5). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 09 (MCP do banco: gravar com versão e conflito à vista), 05 (Frontmatter imposto: esquemas, verificador e "nova iniciativa")

- [ ] a instância de leitura não lista ferramenta de gravação e recusa gravar; as duas de escrita gravam com a guarda de versão, cada uma com o seu token
- [ ] a conexão traz a cabeça do `AGENTS.md` de ensaio e, trocado o arquivo, a sessão nova traz a cabeça nova
- [ ] as descrições das ferramentas trazem a regra curta como aceita
- [ ] os testes de versão passam de novo com a cifra ligada
- [ ] `estado_do_hub` devolve o estado de exemplo e, sem arquivo, "estado indisponível"
- [ ] nota fora do esquema é recusada

## Comments
