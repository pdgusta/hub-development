# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md) — ordem a partir de 08:00:
1. Trilho: Docker do 21, 2ª rodada (~6 min, hub-ensaio-21-a/b, 5996/5997; a 1ª, 08:05, achou o EPERM do rename, consertado em 22abdd2), depois do corredor do 22 da Brasa; e o Docker do 16 com o 08 (~6 min) quando os cenários do 08 estiverem prontos
2b. Vela: harness real do 18, Claude e Copilot (~15 min); o Codex depois das 12h15
3. Rebite: suítes das próximas junções (08, 16, ...), quando houver
4. Cinzel e Vela: Codex do 11 e do 18 (depois das 12h15), um depois do outro
4a. Cinzel: harness real do 11, só o Codex de novo (~5 min; conserto bfd1af3), só depois de 12h15 (cota do Codex)
