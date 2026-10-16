# Worker 9: notas

## Volta 1 (2026-10-15)

**Faixa assumida: skills e acervo do maestro** (faixa 9 nos cortes do Worker 2 e do Worker 8). Fontes lidas: `## Answer`
dos tickets 15 (roteamento de skills), 40 (Maestri: padrão e liberdade) e 14 (acesso dos agentes: hooks), comentários
de 2026-10-12 do ticket 16 (testes da construção para o acervo).

Gravado no `plano.md`: a minha linha na tabela de faixas, quatro fronteiras (seção "Worker 9") e o que fica para outra
execução. Não mandei `maestri ask`: os 12 estão no meio do turno (o ask fica sem Enter).

### Como divido a hora (até 10 subagentes, em paralelo desde o minuto 0)

1. `routing.yml` (esquema e primeiras linhas) e o hook de entrada sem IA, com fixtures da entrada de cada harness.
2. Hook de início com `MAESTRI_TERMINAL_ID`.
3. Guarda do acervo (aval no Claude Code; recusa com caminho de propostas no Codex e no Copilot; caminho real e da
   junction normalizados).
4. Registro de uso (depois da ferramenta de skill) e registro de "a skill indicada rodou?" no fim.
5. a 8. Primeiro lote do acervo, um subagente por grupo: `maestro-acervo` e catálogos; papéis genéricos e o Designer;
   setups (a partitura de hoje como receita, o arranjo deste workspace); contratos-opção (roteamento de modelos com o
   FreeLLMAPI, orquestração, onde abrir), o lembrete e a guarda.
9. Pesquisador de fonte: eventos de hook dos três harnesses (entrada, início, antes e depois da ferramenta, fim), como
   juntam várias respostas no mesmo evento, hook de modelo no Claude Code. Responde até o minuto 15.
10. Teste ao vivo com `claude -p` num HOME de ensaio, no fim.

Marcos: minuto 30, `hooks/09-skills/fragmento.json` e `regra-contrato.md` prontos para o kit; minuto 50, testes verdes.

### Não verificado

- Que o Codex e o Copilot tenham um evento de entrada que injete contexto (o ticket 15 já prevê a regra no contrato).
- Como os harnesses juntam respostas de dois hooks no mesmo evento (recusa × aval; contexto de início somado).
- Hook de modelo (`agent`/`prompt`) no Claude Code e o tempo dele em Sonnet.
- Que `CLAUDE_CONFIG_DIR` sirva de HOME de ensaio (a mesma dúvida do Worker 2).

## Volta 2 (2026-10-15)

Absorvi as duas correções do Prumo para a faixa 9 e apaguei os itens da "Conferência":
- **Guarda:** arquivo novo no acervo passa; aval só para alterar ou apagar peça citada ou usada, catálogo ou descrição
  de skill, nome ou gatilho parecido, contrato-opção que se diz padrão (Answer do 40). Eu tinha posto aval em toda
  gravação: errado.
- **Verificador em outro modelo fica na hora:** hook de settings tipo `agent` (experimental, aceita `"model"`), Answer
  do 44; medir o tempo em Sonnet é parte do teste; só sai da hora se falhar.
- Do 44 também: registro de uso no Claude Code precisa de dois ganchos (`PreToolUse` em `Skill` e
  `UserPromptExpansion`); filtro por caminho do hook é "best-effort" (o mod fica de reserva).
- Fim da resposta no Claude Code por mod (ticket 14), como o Prumo apontou à faixa 2: meu registro de "a skill rodou?"
  vai em `mods/09-skills/`.
- Prova num comando só: `pwsh agents/test/09-skills.ps1` (crivo do Prumo 2).
- Lacunas de dono do 16 (pedido do Worker 10): assumi a 9 e a 10 como propostas; a 7 aceito como mecanismo da guarda
  se Workers 1 e 6 concordarem, com o lugar do registro como decisão nova para a spec.
- Onde mora o código: o Prumo já levou a pergunta ao Gustavo; a faixa 9 segue a resposta, sem esperar.

### Para a próxima volta

- Conferir se Workers 1 e 6 aceitam a guarda cobrindo `AGENTS.md` (lacuna 7).
- Contar o tamanho real da faixa: guarda com verificador `agent` + mod + primeiro lote pode passar da hora; se passar,
  cortar o primeiro lote para porta, papéis e roteamento de modelos.
- Confirmar com Worker 1 (frontmatter fora de `agents/skills/**` e a regra no contrato), Worker 6 (mesmo "antes da
  ferramenta") e Worker 2 (mesmos início e fim).
- Conferir se o primeiro lote cabe na hora; se não, cortar pelo que o maestro usa primeiro (porta, papéis, roteamento
  de modelos).
- Ver a resposta do Gustavo sobre copiar `armis-docx` (linha da tabela depende dela; sem cópia, a linha aponta para
  uma skill de marca no ensaio).
