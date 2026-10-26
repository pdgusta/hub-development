# Context Hub: prova de conceito

> **Histórico, só de leitura (desde 2026-10-26).** O hub existe em `C:\context-hub`, e o trabalho nele mora em
> `operations/hub-development/` do próprio hub (retomada, tarefas, decisões). Workspace e sessão que mexem no hub abrem
> na raiz do hub. Aqui ficam a exploração, a spec e os tickets da construção, para consulta.

Este repositório é a **prova de conceito** do context hub do Gustavo, onde ele é planejado e ensaiado.
O hub final nasce do zero em outro lugar (`C:\context-hub` ou WSL, ainda em aberto). Uma decisão só
está fechada quando consta de um ticket resolvido.

## Onde está o quê

- **Exploração** (`exploracao/2026-09-28-context-hub.md`): levantamento, objetivo proposto (§7.1),
  zonas (§9), pesquisa com fontes (§10) e rodadas de decisão. Leia antes de propor qualquer desenho do hub.
- **Mapa** (`.scratch/<frente>/map.md`, com os tickets em `issues/`): decisões em curso. Leia ao retomar o trabalho.
- **Anexos** (`exploracao/anexos/`): relatórios integrais das varreduras. São saída de modelo; consulte
  quando a §10 não bastar.

## Como trabalhar

- Responda em pt-BR.
- **File-first**: grave cada rodada de decisão no ticket ou arquivo dono no momento em que acontece. O chat
  leva só o resumo. Critério: um `/clear` a qualquer momento não perde nada.
- **Uma decisão por vez**, sempre com uma recomendação. O Gustavo responde em texto livre, e a resposta pode
  mudar o rumo.
- **Fonte primária** antes de explicar ferramenta ou mecanismo: README ou documentação oficial, com citação.
  Resumo do WebFetch não conta. Marque como "não verificado" o que não conferiu.
- Rode testes, provas e varreduras só a pedido do Gustavo. Varreduras seguem o protocolo da §10.4.
- **Dados de cliente** (STRATA, VOEGOL, AVIANCA, TRF3, SBF): notas, tickets e handoffs citam a iniciativa
  pelo nome. Dados pessoais (UPNs, e-mails, nomes) ficam nas pastas de origem.
- **Processo**: só o fluxo do Matt Pocock (`/wayfinder` → `/to-spec` → `/to-tickets` → `/implement-spec`;
  `/implement` só para um ticket isolado). Essas skills são invocadas pelo Gustavo. A spec e os tickets de construção
  nascem neste repositório, em `.scratch/`, mesmo que o hub final viva em outro lugar.

## Agent skills

### Issue tracker

Tickets e specs são arquivos Markdown locais em `.scratch/<frente>/`, versionados no git. Ver `docs/agents/issue-tracker.md`.

### Triage labels

Os cinco papéis padrão (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), numa linha `Status:` de cada ticket. Ver `docs/agents/triage-labels.md`.

### Domain docs

Contexto único: `GLOSSARY.md` e `docs/adr/` na raiz. Ver `docs/agents/domain.md`.
