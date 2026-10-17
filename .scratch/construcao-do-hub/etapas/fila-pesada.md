# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md; Rebite desde 08:30, suíte do 08, até ~08:55) — ordem a partir de 08:45:
1. Trilho: Docker do 21, 2ª rodada (~6 min; conserto 22abdd2); e o Docker do 16 com o 08 (~6 min) quando os cenários
   do 08 estiverem prontos
2. Cinzel: harness real do 24, Claude e Copilot (~6 min, uma sessão de cada)
2b. Vela: harness real do 18 de novo, Claude e Copilot (~5 min; conserto e1c5eac)
3. Brasa: Docker do 22 de novo (~15 min + harnesses ~10 min), com wsl --shutdown antes, indexação antes dos pares e
   mem_limit nos CouchDB do ensaio
4. Rebite: suítes das próximas junções, quando houver
5. Depois das 12h15 (Codex): Cinzel (11, depois 24) e Vela (18), um de cada vez
