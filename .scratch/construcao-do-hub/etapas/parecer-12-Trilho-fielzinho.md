
## Leitura tardia — rodada 3 — 2026-10-17

Ponta 8558abe conferida. Li diff desde 763813a, fragmentos/README, teste real e lido.json dos três, relatório e parecer r3 do Fiel. **Sem achado novo; mantenho PASSA com as ressalvas registradas.** Claude lista apenas mcp__hub-busca__search; os três registram duas buscas (fulltext/semantic), nenhuma outra ferramenta e o caminho esperado. Configurações limitam a search por deny/allowlist; o teste Claude instala o settings com deny. A costura antes pendente com o 15 foi conferida na revisão própria de 3d34bd1: agora ele também grava o deny.

Próprio: teste ponta-a-ponta/12-busca.test.mjs sem HUB_HARNESS_REAL: 1 pulado, 0 falhas; diff check sem erro e árvore limpa. Isso verifica a trava do teste, não reexecuta o aceite. Hashes versionados: somente .claude.json difere (registro, como documentado), todos os usos apagado=true. Não rodei harness, indexação ou instalação. A execução de busca real continua sendo a evidência do construtor. Instalação dos fragmentos pelo kit e ausência de lista de ferramentas na saída Codex permanecem limites já escritos. Sem mensagem ao Fiel por não haver achado novo.
