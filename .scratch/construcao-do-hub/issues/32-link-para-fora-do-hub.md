# 32: O verificador reescreve link para fora do hub

Type: task
Status: ready-for-agent
Etapa: 1 (esqueleto), complemento do 27
Blocked by: 27

**What to build:** No verificador de pastas (`agents/code/bin/verificar-pastas.mjs`, ticket 27), um link para um arquivo fora do hub (caminho absoluto do Windows, `file:///`, wikilink com unidade) vira `par://<HUB_PAR_ID>/<unidade>/<caminho>` (ex.: `C:\Projetos\x\README.md` → `par://par-1/C/Projetos/x/README.md`), com aviso ao agente. Dentro do hub segue sem letra de unidade. Sem `HUB_PAR_ID`, não reescreve e devolve a falta, como já faz. `AGENTS.md` e `SKILL.md` ficam de fora, como no resto do verificador.

**Fonte:** Decisão do Gustavo na rodada `2026-10-16-link-para-fora-do-hub` (B, respondida pelo Maestri Chat); spec faixa 1 ("Links"); ressalva do Fiel e do Fielzinho no 27. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 27 (O verificador cuida das pastas)

- [ ] `[x](C:\Projetos\x\README.md)`, `[x](file:///C:/Projetos/x/README.md)` e `[[C:/Projetos/x/README.md]]` viram `par://<par_id>/C/Projetos/x/README.md`, com aviso
- [ ] o `par://` com unidade para fora do hub não é desfeito na passada seguinte
- [ ] sem `HUB_PAR_ID`, nada é reescrito e a falta volta ao agente

## Comments

- 2026-10-17 ~00h30 (maestro): publicado pela decisão do Gustavo. Dono natural: a Vela (fez o 27).
