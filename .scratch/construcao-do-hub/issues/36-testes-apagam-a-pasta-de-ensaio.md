# 36: Os testes apagam a pasta de ensaio, também quando falham

Type: task
Status: resolved
Etapa: infraestrutura de teste (fora da sequência)
Blocked by: None (can start immediately)

**What to build:** O Fiel achou 1.325 pastas `hub-ensaio-*` esquecidas em `%TEMP%` (2026-10-17 ~05h). Por prefixo:
27=556, 05=394, 04=209, 05n=76, 14=36, 20=31, 19=17, mais algumas. A regra da construção diz que teste que cria pasta em
`%TEMP%` apaga a sua no fim, mesmo falhando; esses testes não cumprem. Conserto: um ajudante comum de pasta de ensaio
(cria e registra a limpeza com `t.after`/`after` do `node:test`, e `try/finally` nos `.ps1`) usado pelos testes que
montam hub de ensaio, a começar pelos prefixos acima. Nenhuma pasta tem cópia de login (conferido pelo maestro).

**Fonte:** aviso do Fiel; `../etapas/regras-da-construcao.md` ("Teste que cria pasta em `%TEMP%` apaga a sua no fim,
mesmo falhando").

**Blocked by:** None (can start immediately)

- [ ] rodar os testes de 04, 05, 14, 19, 20 e 27 (inclusive com uma falha forçada) não deixa pasta `hub-ensaio-*` nova
      em `%TEMP%`
- [ ] os testes novos usam o mesmo ajudante
- [ ] a suíte segue verde

## Comments

- 2026-10-17 05h20 (maestro): publicado pelo aviso do Fiel. As 1.325 pastas antigas continuam lá (nenhuma tem login; a
  limpeza em massa foi recusada pela permissão automática e fica para o Gustavo). Dono: o primeiro construtor livre.
- 2026-10-17 05h25 (maestro): dona: a Vela, enquanto o 17 espera o Codex (06h58) e a fila.

- 05:39 (maestro): costura da Vela aceita (ajudante `agents/code/test/pasta-de-ensaio.mjs`, limpeza no after e no exit). Arquivos de teste que um ramo aberto mexe ficam para depois da junção dele. Medida: das 1.326 pastas, só 87 nasceram depois do after (quase todas de uma rodada interrompida 01:06-01:09).
- 2026-10-17 ~05h50 (Vela): claimed; ramo ticket-36 (de integracao 9453e3e). Ajudante comum agents/code/test/pasta-de-ensaio.mjs + teste 36-pasta-de-ensaio.test.mjs (90f6463); troca nos testes 04, 05, 05n, 14, 15, 19, 20, 27 (dois) e 06. Ficam para depois da junção dos ramos abertos: 08, 10, 15 (ponta a ponta), 16, 17; e 12/13 (pesados). Relatório: ../etapas/relatorio-36-pasta-de-ensaio.md. Falta: rodada com falha forçada, commit, Fiel, Rebite.
- 2026-10-17 06:28 (Vela): rodada 2 do Fiel PASSA em 5b90550 (rodada 1 voltou: limpeza no meio por exceção solta, consertada). Levado ao Rebite. Pendentes: leitura do Fielzinho; troca nos arquivos dos ramos abertos (08, 10, 15, 16, 17) e no 12/13, depois da junção.
- 2026-10-17 07h00 (integrador, Rebite): juntado em `integracao`, commit 85efe3b (merge `--no-ff` de `ticket-36` 5b90550, o HEAD da rodada 2 "passa" do Fiel). Testes, com a trava, junto com o 10 (9cc878b): `node --test --test-concurrency=1 "agents/code/test/**/*.test.mjs"` sem variáveis = 210, 202 verdes, 8 pulados, 0 falhas (15 min); `git status` limpo. Ressalva do parecer: uma exceção solta num `before` da raiz, antes do primeiro teste, ainda limpa, mas aí os testes do arquivo já caem. Nota da Vela: o TEMP isolado precisa de caminho curto (o git dá "Filename too long" no scratchpad). A leitura do Fielzinho ficou pendente. **Resolvido.**
