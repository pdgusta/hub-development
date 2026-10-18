# 25: Junção e prova do hub de ensaio inteiro

Type: task
Status: resolved
Etapa: 11 (junção)
Blocked by: 13, 21, 22, 24

**What to build:** Todas as peças juntas no ramo de integração e o hub de ensaio provado de ponta a ponta: um agente grava, o outro par recebe, a busca acha, a vigia acusa, a retomada segura.

**Fonte:** Spec inteiro; o antigo ticket 11 (juntar e provar), em `../issues-tentativa-paralela/`. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 13 (Gemini pronto e desligado), 21 (Arquivar e cópia diária), 22 (Proxy e kit de cliente), 24 (Kit de par ao vivo nos três harnesses)

- [ ] a prova de ponta a ponta passa com todas as peças juntas
- [ ] o relatório lista o que fica para a instalação de verdade e para a segunda máquina

## Comments

- 07:53 (maestro): do 11 (Cinzel): fica para cá a prova de que o agente segue a regra, o banco recriado e o banco cifrado de ponta a ponta pelos harnesses.

- 08:33 (maestro, mandato): começa já com a Vela, como preparo: as costuras e o roteiro da prova de ponta a ponta sobre o que já está em `integracao` (07, 08, 09, 10, 12, 15), estendido quando 16, 17, 18, 21, 22, 23 e 24 forem juntados. **Memória é o risco**: o Docker do 22 e a fatia 2 do 08 caíram na subida (pares + MCP + indexação passam da memória livre). A prova precisa ser desenhada por fases (indexar antes dos pares, descer o que não se usa mais, `wsl --shutdown` antes) e medir o pico; se não couber, o relatório diz o que fica para a máquina do Gustavo com menos agentes abertos.
- 2026-10-17 08:55 (Vela): preparo começado; costuras propostas em ../etapas/costuras-25-Vela.md (prova por fases, medidor de memória, quatro perguntas). Esperando o maestro antes de codar.

- 08:38 (maestro, mandato): costuras da Vela aceitas (`../etapas/costuras-25-Vela.md`, prova por fases com medidor e corte em 700 MB). Respostas: (1) `wsl --shutdown` pelo corredor, só com a trava dele e `docker ps` vazio; (2) `mem_limit` de 384 MB nos CouchDB por override só do ensaio, sim (se o CouchDB cair por ele, o relatório diz); (3) busca em fase separada; (4) agora só o leve.
- 2026-10-17 10:40 (Vela): preparo leve feito no ramo ticket-25 (medidor, ponte dos pares, orquestrador das fases 1-3, corredor; testes sem Docker verdes). Relatório ../etapas/relatorio-25-hub-inteiro.md. Falta a rodada real pela fila.
- 2026-10-17 09:13 (Vela): correção: os meus comentários de hoje marcados 09:30, 10:40 e 11:00 tinham hora estimada; foram entre 08:40 e 09:13.
- 2026-10-17 10:02 (Vela): 1ª rodada real verde nas fases 1-3 com Claude e Copilot (rodada 1: defeito do teste na fase 2, conserto 627f1a8; rodada 2: 2/2). Evidência fc678b0; pico por fase no relatório. Falta: Codex depois das 12h15, fases 4-7.
- 2026-10-17 10:27 (Vela): fases 4 a 7 escritas contra 16/17/18/21/22 (851dcdc; puladas até as peças entrarem); teste sem Docker da ponte 2/2. Falta: Codex das fases 1-3 e a rodada real das fases 4-7.

- 10:28 (maestro): fases 4-7 escritas pela Vela (851dcdc). Decidido: cada fase registra o que subiu e o corte do medidor desce tudo o que estiver registrado (na fase 7, a pilha do 22).
- 2026-10-17 13:45 (Vela): fases 4, 6 e 7 reais (Claude e Copilot): 6 verde (evidência b3fbac2); 4 falhou por defeito da ponte (fork no ticket-09, sem o estado_do_hub), conserto fe0b800, rodar de novo com Docker; 7 cortada (memória), vai sozinha na janela do maestro. Relatório atualizado.
- 2026-10-17 18:24 (Vela): janela da noite: fases 5 e 7 verdes (Claude e Copilot; 9c5a795, cee35c1); Codex Luna 1 e 3 verdes (c0d2b97); fase 4 e fase 2 do Codex caem no A que não desce ao B (intermitente): diagnóstico com a Brasa. Relatório atualizado (tabela por fase e harness). **Corrigido às 19:12: a fase 7 NÃO estava verde** (o 22-cliente herdou o NODE_TEST_CONTEXT, não rodou harness e saiu 0; rodada 1 do Fiel); e a fase 3 não abre harness, então não diz nada do Codex.
- 2026-10-17 19:12 (Vela): rodada 1 parcial do Fiel VOLTA (parecer-25-Vela.md; provado: 1, 2, 3, 5, 6 com Claude e Copilot; fase 1 do Codex). Consertos: fc6b10c (causa da descida A→B achada pela Brasa: a semente leva ~6,5 min a descer e a nota nova entra na fila; o `subir` espera o B convergir, até 15 min; fase 2 com 120 s), dac76e6 (fase 7 sem NODE_TEST_CONTEXT e exige um ok por harness), f6a0f21 (evidência por rodada; a da manhã e a do Codex repostas). Falta: fases 4 e 7 (Claude, Copilot) e 2 do Codex com a trava; rodada 2 do Fiel.
- 2026-10-17 19:40 (Vela): 2ª volta com rodadas reais: fase 7 Claude+Copilot verde (b78c49d; o 22 rodou: # pass 2); fases 2 Codex e 4 Claude+Copilot verdes numa subida (4a60595; B convergiu em 218 s). integracao 56cd23a junta (4628138). Rodada 2 pedida ao Fiel. Codex nas fases 4-7 fica para amanhã, se o maestro quiser.
- 2026-10-17 19:46 (maestro, pela Vela): o 25 fecha sem o Codex nas fases 4-7 do hub inteiro (mandato; vai ao 'Para rever'); o Codex nessas peças está provado nos tickets 17, 18, 21 e 22. A observação do kit (par novo leva minutos para receber o hub) foi ao ticket 26. Com o PASSA do Fiel, o Rebite junta.
- 2026-10-17 19:52 (Vela): rodada 2 do Fiel PASSA com ressalvas (parecer-25-Vela.md), em 4628138. Texto da instalação corrigido (fase 7 835 MB, fase 4 1.690 MB). Levado ao Rebite.
- 2026-10-17 20h18 (integrador, Rebite): juntado em `integracao`, commit ca62332 (merge `--no-ff` de `ticket-25` 4628138, rodada 2 "passa com ressalvas" do Fiel em acordo com a 2ª leitura, na mesma ponta, que já trazia `integracao` 56cd23a; sem conflito; a junção não toca `evidencia-22` nem `evidencia-24`). Testes: suíte `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis, com a trava: 370, 355 verdes, 15 pulados, 0 falhas, `git status` limpo, nenhum contêiner `hub-ensaio` sobrando (log `../etapas/logs/juncao-25-suite.log`). Docker e harness real não repetidos (arquivos idênticos aos revisados). Escopo: fases 1-7 com Claude e Copilot; Codex nas fases 1 e 2; Codex nas fases 4-7 fora (decisão do maestro, ~19h45). Ressalvas do parecer: nome da pasta `rodadas/2026-10-17-1248-claude-copilot-f1-2-3` engana; `hashes.json` do Codex das 18:00 sem `modelo`; `HARNESSES_F<n>` que não cruza com `HARNESSES` deixa a fase vazia e verde (deveria falhar); cada rodada real da fase 7 suja o `evidencia-22` (volta por `git checkout` à mão); `cliente.ps1` deixa `%TEMP%/hub-ensaio-25-subir-22.log`; 25-medidor com 1 falha em ~16 rodadas; B conferido só no `tasks.md`; `write_note` pelos harnesses e reconexão do MCP fora. **Resolvido.**
