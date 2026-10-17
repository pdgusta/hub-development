# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md; Rebite desde 06:44, suíte do 36+10 e npm test do fork) — ordem a partir de 06:55:
1. Brasa: AGORA (máquina quieta, avisada pelo maestro 07:38): fatias 1 e 2 do 08 (51 e 201 MiB), aceite final da revisão.
   Durante ela, ninguém roda nada pesado.
2. Brasa: Docker do 22 (~15 min) e os três harnesses como cliente (~10 min)
3. Rebite: suíte do hub do 15 rodada 2 (e2b7607, ~15 min)
