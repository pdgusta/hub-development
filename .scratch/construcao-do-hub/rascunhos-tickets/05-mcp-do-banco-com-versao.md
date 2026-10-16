# MCP do banco com versão

Type: task
Status: ready-for-agent
Dono: Worker 5
Com: Prumo
Blocked by:

Faixa 5 da spec (`../spec.md`, seção "Faixas", Worker 5). Fatia vertical: entrega funcionando de ponta a ponta no hub
de ensaio e no HOME de ensaio, sem esperar as outras faixas.

## O que construir

**MCP do banco com versão** (faixa 5 do corte; Answers dos tickets 25, 30, 11, 34, 14, 41 e comentários de 2026-10-12 do 16): fork local do es617/obsidian-sync-mcp (TypeScript, Node ≥ 22; nesta máquina Node 24) em repositório próprio fora do hub (pergunta abaixo). Muda no fork: (a) **R1**: `read_note` devolve a revisão; `write_note` e `edit_note` exigem `base_rev` e gravam como filha dela (o caminho do `r1.py` do spike, `new_edits=false`, já provado com o plugin no ticket 30), então base velha vira conflito com as duas folhas guardadas, nunca sobrescrita; sem `base_rev`, regravar nota existente é recusado; (b) **conflito visível ao agente**: `read_note` de nota em conflito avisa e lista as folhas, e a ferramenta `get_conflicts` lista os conflitos abertos; (c) **`instructions`**: o bloco `cabeca:inicio/fim` do `AGENTS.md` (Worker 1) lido a cada `initialize`, sem cópia, posto **antes** do texto do upstream para sobreviver ao corte do Claude Code, até 2.000 caracteres (Answer do 36); a regra curta ("leia antes, grave com a `base_rev` lida; conflito = releia e refaça") na descrição de `write_note`, `edit_note`, `delete_note` e `move_note`; (d) **ferramenta `estado_do_hub`**: devolve o `estado.json` da vigia (esquema do Worker 8), para a checagem de início onde o hook falhar e para o cliente (14); (e) **duas instâncias por par**, em 127.0.0.1, cada uma com o seu token de variável de ambiente: escrita e `READ_ONLY=true` (já existe no upstream: "disable all write tools", README do es617, cópia do spike), a mesma linha de comando com só essa variável trocada; (f) **E2EE**: a frase-senha do `.env` do banco (`COUCHDB_PASSPHRASE` no upstream), ligada depois dos testes sem ela; (g) se couber: a gravação chama o verificador de frontmatter (Worker 1) e recusa nota fora do esquema (imposição C do 12)

## Critério de aceite (de ponta a ponta)

testes e2e automáticos (`npm run test:e2e` do fork) contra um CouchDB de ensaio só da faixa em 127.0.0.1:5996, com o MCP em 127.0.0.1:8796 (escrita) e 8797 (leitura): (1) ler e gravar com a revisão lida grava, e a leitura seguinte traz a revisão nova; (2) gravar com revisão velha deixa duas folhas no banco, nenhuma versão some, e a resposta diz "conflito: releia"; (3) `read_note` da nota em conflito avisa, e `get_conflicts` a lista; (4) regravar sem `base_rev` é recusado; (5) a instância de leitura não lista nenhuma ferramenta de gravação e recusa gravar; (6) o `initialize` traz a cabeça do `AGENTS.md` de ensaio e, trocado o arquivo, a sessão nova traz a cabeça nova; (7) `estado_do_hub` devolve o arquivo de exemplo; (8) os testes 1 a 3 de novo com E2EE ligada; os testes unitários do upstream seguem verdes. Mais `kit/par/05-mcp-banco.ps1` no contrato do instalador (Worker 2) e as duas linhas no `.env.modelo`

## Como segue sem esperar

o banco (faixa 4): não espera; sobe `couchdb:3.5.2` na 5996 pelos nomes do `.env.modelo` do Worker 4 e, quando o `compose.yml` dela chegar, troca por ele; usa o retrato do item 6 dela (conflito aberto e binário com ramo apagado) como caso extra, se chegar a tempo. O `AGENTS.md` (faixa 1): um `AGENTS.md` de ensaio com o bloco `cabeca:` até a faixa 1 entregar. O estado da vigia (faixa 7): um `estado.json` de exemplo no esquema do Worker 8. O verificador (faixa 1): o dublê que sai 0. O kit (faixa 8): só escreve `HUB_MCP_BANCO_URL`, `HUB_MCP_BANCO_TOKEN`, `HUB_MCP_BANCO_LEITURA_URL` e `HUB_MCP_BANCO_LEITURA_TOKEN` no `.env.modelo` no minuto 0–10. As faixas 6 e 10 recebem de mim só nomes: `write_note` com `base_rev`, e as duas URLs

## Regras

- Ramo e pasta próprios (git worktree) do repositório do hub em `C:\context-hub`; nada global de verdade sem o aval do
  Gustavo (HOME de ensaio); a execução inteira dura 1 hora: o que não couber vai para "Fica para outra execução" no plano.
- Até 10 subagentes; parte muito complexa: um subagente Fable 5.1 médio.
- Antes de juntar: revisão do Prumo (decisões) e do Prumo 2 (construção).
- Erro achado na spec: corrija a spec na sua faixa.

## Comments
