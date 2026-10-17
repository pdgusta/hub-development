# 25: Junção e prova do hub de ensaio inteiro

Type: task
Status: ready-for-agent
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
