# Costuras do ticket 23 (Cinzel, 2026-10-17 ~08h20): kit de par, a forma

Fontes: ticket 23 (com os comentários de 03, 06, 12, 15, 21 e 11), Worker 8 do spec, faixa 8 de
`spec-partes/faixas-07-08.md`, passos 03/04/05 do kit em `integracao` e2b7607, os ensaios dos testes 14, 15, 19 e 20
(como cada um liga hook e skill no HOME de ensaio), a prova 03 (`instalar.mjs`) e o ramo `ticket-21` (cópia e cabeça).
Olhei o HOME real só para ler a forma do GSD; nada gravado.

## Como proponho

1. **Forma.** `agents/code/kit/par/instalar.ps1` é a entrada: `-Casa` (o HOME), `-Hub`, `-EnvFile`, `-Passos`,
   `-WhatIf` e `-Desfazer`. O miolo da faixa 8 fica em Node (`agents/code/kit/par/kit/*.mjs`): JSON, TOML por chave e
   tabela, hash e cópia. A prova 03 já faz isso em Node; tiro de lá o leitor de TOML e o `listarHooks` para um módulo
   comum.
2. **Ordem dos passos.** 00 conferir → 03 busca → 04 banco → 05 MCP do banco → 08 contrato → 08 skills → 08 MCP →
   08 hooks → 08 GSD → 08 Codex → 10 manutenção. Os passos 03 a 05 já existem e têm testes próprios (npm e Docker). O
   instalador os enfileira, mas o teste do 23 roda `-Passos 00,08,10`.
3. **Nunca o HOME real.** Sem `-Casa` nem `HUB_HOME_ENSAIO`, o kit recusa. A instalação de verdade é o 26. Dentro da
   casa, o kit usa a forma real (`.claude.json`, `.claude/`, `.codex/`, `.copilot/`, `.agents/skills/`). Como os
   harnesses a enxergam é assunto do 24.
4. **Cópia e hash antes de tocar.** Antes de mudar um caminho, o kit guarda uma cópia dele (ou "não existia") em
   `<casa>/.hub-kit/copias/<carimbo>/`. O `registro.json` anota, por caminho, o hash de antes, o hash de depois e o
   tipo (arquivo, link ou junction).
5. **Idempotente.** Cada ação compara o desejado com o atual. Sem diferença, não grava nem abre carimbo. A segunda
   passada sai com "nada a mudar", e o hash da casa não muda.
6. **Desfazer.** Volta os carimbos em ordem inversa e apaga o que não existia. Antes, confere se o arquivo está como
   o kit deixou. Se mudou depois, para e diz qual. No fim apaga o `.hub-kit`, e o hash da casa volta ao de antes.
7. **Contrato.**
   - Claude Code: a linha `@<hub>/AGENTS.md` no `~/.claude/CLAUDE.md`. Ela entra se faltar, e o resto do arquivo fica.
   - Codex: link simbólico `~/.codex/AGENTS.md`.
   - Copilot: link simbólico `~/.copilot/copilot-instructions.md`.
   - Nunca link físico. O teste confere o destino de cada link.
8. **Skills.** Uma junction por skill, em `~/.claude/skills/<skill>` e `~/.agents/skills/<skill>`, para
   `<hub>/agents/skills/<skill>`. Só as marcadas de uso geral (ver a pergunta 1). Se já existe pasta ou link com o mesmo
   nome, o kit guarda uma cópia e troca. As outras entradas da pasta ficam.
9. **Linhas de MCP nos três.**
   - `hub-busca`: pelos fragmentos de `busca/registro/`, como estão, com o `permissions.deny` juntado no
     `settings.json` sem sobrescrever (lição do 12).
   - `hub-banco`: a instância de escrita dos agentes (`HUB_MCP_BANCO_URL` do `.env`), com o token por variável.
     - Codex: `bearer_token_env_var` e `default_tools_approval_mode = "approve"`.
     - Claude e Copilot: a forma de ler a variável no cabeçalho, conferida na doc por curl antes de codar.
   - Copilot, ressalva do 11: confiro na doc se há chave de configuração para liberar as instruções do `hub-banco`. Se
     só existir a opção de linha de comando, registro, e o 24 a usa.
10. **Hooks.** Entra a junção genérica de todo `agents/code/hooks/<peça>/fragmentos/<harness>.json` que existir, com
    `{{DIR}}` e `{{HUB}}`, na forma dos ensaios de 14 a 20:
    - Claude: o `settings.json`, por evento;
    - Codex: o `hooks.json`, por evento, mais o `hooks.state` com o hash lido do app-server (não chama o modelo nem
      pede login);
    - Copilot: um `~/.copilot/hooks/hub-<peça>.json` por peça.
    Ela acrescenta sem apagar, e o que já é igual não se repete. Os fragmentos de 17 e 18 entram sozinhos numa
    segunda passada, depois da junção deles.
11. **Codex.** Na config, por chave: `sandbox_mode = "danger-full-access"`. O `notify` fica como está até o 17
    entregar o consumidor do hub. Aí o kit o compõe com o que existir, num programa só (lição 1 do 03).
12. **GSD fora do global, com cópia.** O GSD deixa um manifesto por harness (`gsd-file-manifest.json`, com a lista
    de arquivos e o sha256, em `.claude`, `.codex` e `.copilot`). O kit tira, com cópia:
    - os arquivos do manifesto, o próprio manifesto, o `gsd-install-state.json`, o `gsd-migration-journal` e o
      `gsd-core`;
    - os hooks cujo comando aponta um arquivo do manifesto, no `settings.json` e no `hooks.json`;
    - o bloco `<!-- GSD Configuration ... -->` / `<!-- /GSD Configuration -->` do `copilot-instructions.md`;
    - a seção marcada "managed by gsd-core installer" do `config.toml`, por tabela;
    - as pastas `~/.agents/skills/gsd-*`.
    O ensaio leva um GSD de mentira, nessa mesma forma.
13. **`10-manutencao.ps1`.** Gera dois XML de tarefa agendada em `<casa>/.hub-kit/tarefas/`:
    - a diária: `copia-diaria.mjs --env` e `conferir-cabeca.mjs`, do 21;
    - a de 5 min: a passada da vigia, do 16.
    Registrar pede `-Registrar` e passa pelo `ShouldProcess`; os testes nunca o passam. O teste lê o XML (gatilho,
    comando e pasta de trabalho).
14. **Conferências (00).**
    - Nenhum `CLAUDE.md` no hub nem acima dele: se houver, para e diz o caminho.
    - Modo de desenvolvedor, pelo registro: se estiver desligado, para e explica, sem ligar (ponto aberto do spec).
    - Node ≥ 22 e Python.
15. **Fora do esqueleto, para depois de 17 e 18:** o mod do Claude Code, a extensão `onAgentStop` e a `statusLine`
    do Copilot, o `notify` composto, o `claude-md-and-agents-md` do Maestri, o MCP do Copilot do VS Code e o
    `trust_level` (ponto aberto do spec).
16. **Testes.** Um `23-kit.test.mjs` sem harness, com hub e casa de ensaio (`pastaDeEnsaio`). Ele cobre:
    - a simulação não muda o hash e lista o que faria;
    - a primeira passada liga tudo, e a segunda não muda nada;
    - o desfazer volta ao hash de antes;
    - com um `CLAUDE.md` acima do hub, o kit para e diz onde está;
    - com um GSD de mentira, o GSD sai, com cópia, e o contrato entra;
    - uma skill de papel fica fora da junction;
    - os links, as junctions, as linhas de MCP e os hooks juntados conferem.
    O app-server do Codex sobe só para o `hooks.state`.

## Perguntas

1. **Como o kit sabe que uma skill é de uso geral?** Recomendo um campo no frontmatter do `SKILL.md`:
   `metadata: { camada: geral }`. O `metadata` é o mapa livre do padrão das skills, e a palavra é a mesma do
   `routing.yml`. Sem o campo, a skill fica fora da junction. A outra saída é uma lista no kit. Se for o frontmatter:
   marco já como de uso geral a `busca`, a família `maestro-*`, a `nova-iniciativa` e a `nova-pasta-local`? A
   `arquivar` e a `vigia` entram quando forem juntadas.
2. **E um arquivo global ocupado com texto que não é do GSD?** Por exemplo, um `copilot-instructions.md` com texto
   próprio, ou um `~/.claude/skills/<x>` real com o nome de uma skill do hub. Recomendo: o texto que sobra além do GSD
   faz o kit parar e mostrar o trecho, para ir ao hub antes. Uma pasta de skill com o mesmo nome vai para a cópia e
   vira junction. A outra saída é trocar sempre, com cópia.
3. **App-server do Codex no teste da forma:** ele sobe por segundos, sem modelo e sem login. Pode rodar sem a trava?
   Recomendo que sim.

## Respostas (maestro, 2026-10-17 ~08h25)

As três como recomendado: (1) `metadata.camada: geral` no frontmatter, já marcando busca, `maestro-*`, `nova-iniciativa`
e `nova-pasta-local`; (2) texto além do GSD faz parar e mostrar; pasta de skill de mesmo nome vai para a cópia e vira
junction; (3) app-server do Codex no teste sem trava.
