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

- 04:42 (maestro): reservado para o Cinzel (continua no fork). Costuras já; código depois do "passa" do 09, num ramo ticket-10 do fork a partir do ticket-09 (e no hub a partir de ticket-09 ou de integracao com o 09 juntado).

- 04:45 (maestro, mandato): costuras A e B do Cinzel aceitas; decisões (a) portas 8796 escrita do par, 8797 leitura, 8798 escrita do cliente, com URL/TOKEN de cada uma no `.env`; (b) regra curta completa nas 4 ferramentas de gravação (delete e move levam base_rev desde o 09); (c) cabeça ausente ou acima de 2.000: texto do upstream mais a linha "cabeça do AGENTS.md indisponível: <motivo>", nunca cabeça cortada; (d) validação também para nota nova, tipo pelo caminho; (e) estado.json ilegível: "estado indisponível: <motivo>". O caminho e o esquema do `estado.json` combinam com o 16 (Trilho, `agents/skills/vigia/`).

- 2026-10-17 ~04h55 (Cinzel): combinado com o Trilho (16, ramo ticket-16 60756e6, `agents/skills/vigia/SKILL.md`): caminho `<hub>/.local/vigia/estado.json`. Topo: `nivel`, `resumo`, `passada` (ISO; ausente se só outros donos gravaram), `outro_par {situacao, motivo?}` e `vistos` (interno da vigia: o `estado_do_hub` o tira). `itens[]`: `id`, `nivel`, `resumo`, às vezes `fonte`, `caminho`, `parada_desde`, `ultima_troca`. Sem arquivo ou ilegível: "estado indisponível". Estado velho: perguntado ao maestro (sugestão do Trilho: aviso "a vigia não roda desde <hora>" se `passada` > 15 min). Código só depois do "passa" do 09.

- 04:46 (maestro, mandato): estado velho aceito como proposto (Trilho e Cinzel): não vira "indisponível"; passada com mais de 15 min leva o aviso "a vigia não roda desde <hora>"; sem o campo `passada`, sem aviso de idade. O campo `vistos` (interno da vigia) não sai no `estado_do_hub`.
