# 21: Arquivar e cópia diária

Type: task
Status: claimed
Etapa: 9 (manutenção e cliente)
Blocked by: 08, 16

**What to build:** Arquivar uma pasta só com o outro par em dia, com a data no nome; a cópia diária para o GitHub (commit e push, nunca pull), que sai com erro e acende o item na vigia se falhar (confere a vigia com o item real); conferir a cabeça do contrato; a limpeza do arquivo só desenhada, simulando.

**Fonte:** Bloco do Worker 10; faixa 10; tickets 33, 36, 06, 12; escolhas aceitas 8, 9 e 10. O prazo de 30 dias é do laço do system design e fica fora. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 08 (Banco: limites e robustez), 16 (Vigia: passada, estado e notificação)

- [ ] arquivar move com o outro par em dia e recusa com ele atrasado ou com edição recente
- [ ] a cópia diária gera commit no ramo do par e empurra para um repositório nu local; com o remoto quebrado, sai com erro e a vigia mostra o item
- [ ] conferir a cabeça recusa bloco ausente ou longo

## Comments

- 07:31 (maestro, mandato): começa já com o Trilho, num ramo ticket-21 da ponta de `integracao` com o `ticket-16` juntado por merge (o item da cópia diária na vigia é do 16). As partes que dependem do 08 entram quando ele for juntado. Junção só com 08 e 16 resolvidos.
- 2026-10-17 ~07h50 (Trilho): pego (claimed). Worktree C:/context-hub-wt/ticket-21, ramo ticket-21, de integracao 9cc878b com o ticket-16 juntado (c36ece4). Costuras propostas em etapas/costuras-21-Trilho.md (quatro perguntas ao maestro).

- 07:34 (maestro, mandato): costuras do Trilho aceitas (`../etapas/costuras-21-Trilho.md`). (1) edição recente = arquivo da pasta mudado nos últimos 15 min; (2) outro par desligado ou sem resposta = recusa (só arquiva com o outro par em dia); (3) em dia = as duas replicações `running` e 0 pendentes no momento; (4) o `10-manutencao.ps1` (XML da tarefa diária, sem registrar) fica fora do 21 e vai para o 23.
- 2026-10-17 08:35 (Trilho): código e testes leves prontos (HEAD 22abdd2): arquivar (skill), copia-diaria, conferir-cabeca, limpar-arquivo só simulando. Docker 1ª rodada: o rename deu EPERM com o sincronizador rodando (arquivo aberto na pasta); conserto 22abdd2 (espera 10 s, depois recusa "em uso"). Falta a 2ª rodada do Docker (fila), o relatório (etapas/relatorio-21-arquivar-e-copia.md) e o Fiel.

- 09:13 (maestro, mandato): o rename da pasta é bloqueado pelo watch do CLI numa subpasta (EPERM no Windows, provado pelo Trilho). Aceito: o arquivar move arquivo por arquivo para a pasta nova e apaga a árvore velha vazia; se falhar no meio, devolve o que moveu; sem parar o sincronizador (o LiveSync já vê rename como apagar+criar). Ressalva: durante a mudança o outro par pode ver o estado parcial; o fim é consistente.
