# 26: Instalação de verdade no par 1 (com o Gustavo)

Type: task
Status: ready-for-human
Etapa: depois da junção
Blocked by: 25

**What to build:** O kit no HOME real desta máquina, com cópia e hash antes, à vista do Gustavo. A segunda máquina fica para depois.

**Fonte:** Spec, "Instalar em arquivo global de verdade... sem o aval do Gustavo" (fora de escopo das etapas). Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 25 (Junção e prova do hub de ensaio inteiro)

- [ ] o kit roda no HOME real com cópia e hash antes
- [ ] o Gustavo confere os três harnesses na pasta real

## Comments

- 08:42 (maestro): do 23 (Cinzel): o Copilot não tem chave de configuração nem variável para as instruções do servidor MCP; só a opção `--allow-all-mcp-server-instructions` na linha de comando. Quem abre o Copilot (o preset do Maestri, um atalho) tem de passá-la.
- 2026-10-17 19h50 (maestro): da reprodução do 25 (Brasa, `../etapas/diagnostico-25-nota-nao-desce.md`): um par novo leva minutos para receber o hub (semente de ~520 arquivos, ~4-7 min no ensaio). Na instalação do 2º par, avisar ou esperar a convergência antes de dar por pronto. Também: o 25 fechou o Codex nas fases 1-3 do hub inteiro; nas fases 4-7 o Codex está provado nos tickets de cada peça (17, 18, 21, 22); rodar o Codex nas fases 4-7 do 25 fica opcional, se quiser antes da instalação.
