# Ticket 10 — Cinzel — parecer do Fiel — rodada 1

2026-10-17 ~06h35. Fork worktree `C:/Projetos/hub-mcp-banco-wt/ticket-10`, ramo ticket-10 58c8504 (de ticket-09
d2a5a40); hub `C:/context-hub-wt/ticket-10`, 6095213 (contém integracao 9453e3e). Fiel sozinho (leitura do Fielzinho
pendente).

## Veredito: VOLTA (1 conserto)

## Conserto
1. **A nota passa na checagem, mas grava sem o que o verificador completa: fica no banco fora do esquema** (Fiel).
   `hub.ts` `checkFrontmatter` só olha `r.faltas`. O `analisar` cobra as faltas sobre `{...dados, ...trocas}`, isto é,
   já com o derivável completado; o `write_note`, o `edit_note` e o `move_note` gravam o `content` original, sem as
   `trocas`. Sonda direta no `analisar` do hub:
   - `inbox/ideia.md` com só `# Ideia\n\nTexto.` (sem frontmatter): `faltas=[]`,
     `trocas=type,title,status,created,updated`. O MCP aceita e grava a nota sem frontmatter nenhum;
   - `initiatives/context-hub/decisions.md` sem `status`: recusada (certo).
   No disco, quem completa o derivável é o verificador do fim da resposta, que só roda no harness do agente que grava
   no disco. Pelo MCP (cliente ou agente do par) ninguém completa: a vigia do 16 não roda o verificador. No `move_note`,
   o `type` de origem vai junto para o tipo do destino.
   Conserto: gravar o `novoTexto` do `analisar` (com as `trocas`), não o `content`, nas três ferramentas, e dizer na
   resposta o que foi completado. A `base_rev` devolvida já é a da versão gravada. Teste: nota nova sem frontmatter em
   `inbox/` grava com `type`, `title`, `status`, `created`, `updated`; `move_note` de `inbox/` para outro tipo troca o
   `type`.

## Conferido
- Cabeça: getter `instructions` relido a cada sessão; bloco `cabeca:inicio/fim` inteiro ou fora com o motivo
  (limite 2.000); a cabeça vem antes do texto do upstream.
- Regra curta: texto igual ao aceito (spec faixa 5, história 15) e completo nas 4, pela decisão (b) do maestro.
- `estado_do_hub`: sem `vistos`; aviso de passada velha acima de 15 min; "estado indisponível: <motivo>"; nas três
  instâncias.
- Instância de leitura: `READ_ONLY`, nenhuma ferramenta de gravação registrada.
- Passo 05: três instâncias com porta e token próprios; recusa porta ou token repetido.
- Fork `test/hub.e2e.test.ts` com `HUB_TESTE_HUB`: 10/10 (Fiel). Hub `09-mcp-banco-sem-docker.test.mjs`: 1/1 (Fiel).
  Árvores limpas.
- Docker (`10-mcp-banco.test.ps1` e o 09): não rodado pelo Fiel nesta rodada, porque o código vai mudar. Roda na
  rodada 2, com a trava.

## Ressalvas (não bloqueiam)
1. O verificador fica no cache de `import`: um `frontmatter.mjs` novo no hub pede religar o MCP (escrito no relatório).
2. Os caminhos `/banco/mcp` e `/banco-escrita/mcp` do spec ficam para a faixa 10 (proxy): decisão (a) do maestro.
3. A instância do cliente grava no mesmo banco; a separação é só o token (escrito no relatório).
