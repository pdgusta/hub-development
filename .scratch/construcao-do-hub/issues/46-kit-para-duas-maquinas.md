# 46: O kit de par pronto para duas máquinas

Type: task
Status: claimed
Etapa: preparo do 26 (duas máquinas)
Blocked by: 25

**What to build:** Preparo do kit de par para a instalação nas duas máquinas (roteiro `../etapas/roteiro-26.md`;
decisão do Gustavo, 2026-10-17 ~21h45, pelo Maestri Chat: "A", abrir agora).
1. **`HUB_PAR_ID`:** nenhum script do kit a define (divergência do Lume; sem ela, nenhum link para fora do hub vira
   `par://`). O kit grava a identificação do par (vinda do `.env` do par) onde os verificadores e hooks a leem.
2. **Esperar a convergência:** um par novo leva minutos para receber o hub (~530 arquivos; diagnóstico do 25). Ao fim
   do `instalar.ps1`, o kit espera o disco do par convergir com o banco (com prazo e progresso) ou diz claramente que
   ainda está recebendo; reaproveitar `agents/code/test/ponta-a-ponta/25/convergiu.mjs` se couber.
3. **Proxy na fila:** o `10-proxy.ps1` (acesso de clientes) entra na fila do `instalar.ps1` como passo opcional.
4. **O que fica de fora, escrito:** o mod do Claude Code, a extensão do Copilot e o `notify` do Codex continuam fora do
   kit (ressalva do 23): a saída do kit lista o que falta ligar à mão, para o 26.

**Fonte:** divergência do Lume (`componentes/pastas-e-links.md` §5), `operacao.md` ("O que o kit ainda não faz"),
diagnóstico do 25.

**Blocked by:** 25 (resolvido)

- [ ] `HUB_PAR_ID` vem do `.env` do par e chega aos verificadores e hooks (teste com link para fora do hub virando `par://`)
- [ ] o `instalar.ps1` espera a convergência ou avisa, com prazo (teste no ensaio)
- [ ] `10-proxy.ps1` na fila como passo opcional; a lista do que falta ligar à mão sai no fim
- [ ] a suíte segue verde

## Comments

- 2026-10-17 ~21h50 (maestro): publicado pela decisão do Gustavo (Maestri Chat). Dono: o Cinzel (fez o 23 e o 24).
- 2026-10-17 ~22h10 (Cinzel): claimed. Worktree `C:\context-hub-wt\ticket-46` (ramo ticket-46, de `integracao` dc514db).
  Desenho: `HUB_PAR_ID` do `.env` gravado pelo passo 08 em `<hub>/.local/par.json` (lido pelo verificar-pastas e pelo
  roteamento); passo `espera` no fim (ls do leitor da vigia contra o disco, com prazo); passo opcional `proxy`; lista do
  que falta à mão na saída. Combinado com a Brasa: `etapas/logs/46-combinado-brasa.md`. Costuras enviadas ao maestro.
