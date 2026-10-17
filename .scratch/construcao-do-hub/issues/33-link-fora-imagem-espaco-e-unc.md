# 33: Link fora do hub: a imagem mantém o `!`; espaço cru e caminho de rede avisam

Type: task
Status: ready-for-agent
Etapa: conserto do 32 (fora da sequência)
Blocked by: 32

**What to build:** Três sobras do link para fora do hub (ticket 32), ressalvas do parecer. (1) Imagem embutida para fora
(`![foto](C:/Imagens/x.png)`) hoje vira `[foto](par://...)` e deixa de ser imagem: passa a virar `![foto](par://...)`.
(2) Link Markdown com espaço cru no destino (`[x](C:\Program Files\x.md)`), que já nasce quebrado, passa a gerar aviso
do verificador, sem reescrever. (3) Caminho de rede UNC (`\\servidor\pasta\x.md`) passa a gerar aviso, sem reescrever.

**Fonte:** decisão do Gustavo, rodada `2026-10-17-ressalvas-do-link-fora` (A), no ticket 16; `../etapas/parecer-32-Vela.md`
(ressalvas). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 32 (Link para fora do hub)

- [ ] `![foto](C:/Imagens/x.png)` vira `![foto](par://<par>/C/Imagens/x.png)`, e a volta mantém o `!`
- [ ] `[x](C:\Program Files\x.md)` fica como está e o verificador avisa que o destino tem espaço cru
- [ ] `\\servidor\pasta\x.md` fica como está e o verificador avisa que é caminho de rede
- [ ] a suíte segue verde

## Comments

- 2026-10-17 ~03h35 (maestro): publicado pela decisão do Gustavo (A). A opção dizia "para a Vela agora", mas ela está no
  28 e depois no 09; dono: o Trilho, depois do 35 e do Codex do 12 e do 15 (código da Vela no 27 e no 32; perguntar a
  ela).
