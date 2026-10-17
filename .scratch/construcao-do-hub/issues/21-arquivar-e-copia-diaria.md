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
