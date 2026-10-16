# Teste curto: a vigia no Codex pelo nome da conversa (ticket 14, rodada 7, opção C)

Brief do maestro, 2026-10-15. Pedido do Gustavo: testar se um programa ao lado de um Codex **já aberto** consegue mostrar
o estado da vigia o tempo todo, renomeando a conversa, com o nome aparecendo na barra de estado e no título do terminal.
Responda em pt-BR. Orçamento: cerca de 1 hora.

## O que já se sabe (sua entrega anterior, `bancada-acesso-codex.md`, seção 4)

- `tui.status_line` e `tui.terminal_title` aceitam `thread-name` (enums `ThreadName`/`ThreadTitle` na 0.161.0, iguais
  na 0.162.1); nenhum item roda comando.
- Pelo app-server, `thread/start` → `thread/name/set` → `thread/read` passou numa instância própria, com
  `thread/name/updated`; conversa efêmera recusa (`ephemeral thread does not support metadata updates`).
- **Não testado:** se outra instância do app-server (ou outro cliente) renomeia a conversa de um **TUI já aberto**, e se
  o TUI redesenha a barra e o título; e emitir o título por OSC a partir de um hook.

## Onde

`C:\Projetos\bancada-acesso\nome-conversa\` (crie). Codex com `danger-full-access` (decidido na rodada 7) ou o
contorno já usado; diga qual.

## Os casos

1. Um Codex interativo aberto (TUI, numa janela/terminal próprio) com `-c 'tui.status_line=["thread-name"]' -c
   'tui.terminal_title=["thread-name"]'`, conversa persistida (não efêmera), pelo menos um turno feito.
2. Um programa separado (script seu) renomeia **essa** conversa para `vigia: <estado> <hora>` pelo caminho que existir
   (outra instância do app-server sobre o mesmo histórico, ou o que a documentação oficial der). Registre se o nome muda no
   disco/`thread/read` e se **a barra de estado e o título do terminal do TUI aberto** mudam sem nova interação, depois de
   um turno novo, ou nunca.
3. Repita a renomeação 3 vezes com intervalo, para ver se a tela acompanha.
4. Se nada atualizar a tela aberta, diga o que seria preciso (ex.: o próprio TUI ser cliente do app-server) e se há
   caminho documentado; não construa um host completo.
5. Opcional, se sobrar tempo: um hook do Codex consegue mudar o título do terminal (OSC) ou a saída dele é capturada?

Para ver a tela: captura do terminal ou o que o Maestri mostrar (a sua própria tela, se rodar no seu terminal). Não use
mouse nem teclado em janelas que não sejam suas.

## Regras

- Fonte primária (documentação oficial ou código da tag usada, com trecho e URL) para o que a ferramenta promete; o
  resto é o que o teste mostrou; marque "não verificado" o que não conferiu.
- Globais (`~/.codex/`): de preferência não toque; se precisar, cópia antes e restauração conferida por hash.
- Não leia credenciais. Nada de dado de cliente. Processos que abrir, encerre pelo PID, nunca por nome.
- Não toque no repositório `C:\Projetos\context-hub` além do arquivo de entrega. Não publique nada (a #20244 é do maestro).

## Entrega

`C:\Projetos\context-hub\.scratch\context-hub\bancada-nome-conversa.md`: tabela caso × resultado (o que mudou no disco, na
barra de estado, no título; com evidência), as fontes, se o caminho serve para a vigia (sim, não, com que custo) e se o
texto sugerido para a #20244 (na sua entrega anterior) precisa mudar. Estado dos globais no fim.
