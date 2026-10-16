# Pesquisa e teste: o Codex no acesso dos agentes

Brief do maestro para o recruta Codex (GPT 6.1 Sol, esforço médio, acesso total), pedido do Gustavo em 2026-10-15
(ticket 14, rodada 3). Responda em pt-BR.

## Contexto (leia antes)

- `C:\Projetos\context-hub\.scratch\context-hub\bancada-acesso-relatorio.md`: a bancada de acesso. Seções 1, 4
  ("Codex: correlato de mod"), 10 (estado da vigia) e "O que ficou não verificado".
- A bancada mora em `C:\Projetos\bancada-acesso\` (hub de mentira com `AGENTS.md`, `scripts\inicio.py`,
  `scripts\fim.py`, `logs\`). Use-a para os testes.
- Já decidido: hooks no escopo do usuário nos três harnesses (Claude Code, Codex, Copilot CLI), com o script saindo
  na hora fora do hub. No Codex, o estado da vigia aparece hoje só na checagem de início e na notificação do Windows
  como reserva.

## O que fazer

1. **O erro de sandbox do Codex nesta máquina.** O `codex exec` não grava arquivo nem roda comando:
   `Failed to create unified exec process: helper_unknown_error: setup refresh had errors`, e `apply_patch` dá
   `patch: failed`, com `sandbox_mode="workspace-write"`. O `~/.codex/config.toml` tem `sandbox = "elevated"`.
   Ache a causa em fonte primária (documentação do Codex sobre o sandbox do Windows, código e issues de
   `openai/codex`) e teste um conserto curto. Prefira opções por linha de comando (`-c chave=valor`, `-s`) a mudar o
   arquivo global.
2. **O fim da resposta no Codex.** Com o Codex gravando, repita o caso que faltou: o hook `Stop` com o `fim.py`
   **solta** o agente quando a nota de retomada foi tocada na resposta (o caso "devolve" já passou).
3. **Correlato de mod no Codex, pesquisa melhor.** A bancada não achou API de código dentro do processo (o plugin só
   empacota hooks). Procure de novo em fonte primária: plugins, app-server, SDK, `notify`, extensões, qualquer coisa
   que rode código no fim da resposta ou recuse uma ação. Diga o que existe, o que cada caminho permite e se dá para
   testar aqui; teste o que for curto.
4. **O estado da vigia o tempo todo no Codex.** O `tui.status_line` tem lista fechada de itens, sem item de comando.
   Procure outros caminhos: título do terminal ou da aba, `ThreadName`/`ThreadTitle` alimentados por hook, o
   `systemMessage` de hook, notificação, um item novo em versão mais recente. Teste o que for curto. Se nada existir,
   diga se vale abrir um pedido no repositório deles e com que texto.

## Regras

- Fonte primária para cada afirmação (link e trecho citado); o que não conferiu vai como "não verificado".
- Arquivos globais (`~/.codex/config.toml`, `~/.codex/hooks.json`, `~/.copilot/`, `~/.claude/`): cópia antes,
  restauração conferida depois (diff ou hash), anotada no relatório.
- Não leia nem copie arquivos de credencial (`auth.json`, `.env`, `credenciais*`, `token*`).
- Não toque no repositório `C:\Projetos\context-hub` além do arquivo de entrega. Sem commit.
- Nada de dado de cliente.
- Processos que você abrir, você encerra (por PID, nunca por nome).

## Entrega

`C:\Projetos\context-hub\.scratch\context-hub\bancada-acesso-codex.md`: para cada um dos quatro itens, o que achou, as
fontes, o que testou e o resultado (passou, falhou, não deu para testar), e o estado dos arquivos globais no fim. Ao
terminar, responda só "pronto" e o caminho do arquivo.
