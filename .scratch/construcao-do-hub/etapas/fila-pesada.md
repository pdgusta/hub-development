# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md) — ordem a partir de 08:00:
1. Trilho: Docker do 21 (~6 min, hub-ensaio-21-a/b, 5996/5997)
2. Brasa: Docker do 22 (~15 min) e os três harnesses como cliente (~10 min)
3. Rebite: suítes das próximas junções (08, 16, ...), quando houver
4. Cinzel: harness real do 11, só o Codex de novo (~5 min; conserto bfd1af3), só depois de 12h15 (cota do Codex)
