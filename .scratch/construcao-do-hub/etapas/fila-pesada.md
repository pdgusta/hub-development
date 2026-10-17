# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md; Brasa desde 05:20, fatias 3-7 e 07 do 08)
1. Cinzel: Docker do 10 (novo, ~5 min) e do 09 de novo com as três instâncias (~3 min), worktree ticket-10
   (caminho crítico: o 10 abre 11, 22 e a junção do 16)
2. Rebite: suíte da junção do 28 e do 09 (~16 min)
3. Trilho: Codex do 15 (a partir de 06:58; entra entre fatias da Brasa se ela ainda estiver)
4. Brasa: a fatia 2 do 08 (51 e 201 MiB), numa hora de máquina quieta, combinada pelo maestro
