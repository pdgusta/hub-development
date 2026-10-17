# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md)
1. Trilho: Docker do 16 de novo (consertos ff0f362)
2. Brasa: Docker do 08, fatias 3 a 7 e o teste do 07 (leves). A fatia 2 (51 e 201 MiB) só numa hora de máquina
   quieta, combinada pelo maestro.
3. Rebite: suíte da junção do 28 e do 09 (~16 min)
4. Trilho: Codex do 15 (a partir de 06:58; entra entre fatias da Brasa)
