# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md) — ordem a partir de 08:45:
1. Trilho: Docker do 21, 3ª rodada (~6 min, hub-ensaio-21-a/b, 5996/5997; conserto do EPERM 9ce2496)
2b. Vela: harness real do 18 de novo, Claude e Copilot (~5 min; conserto e1c5eac)
3b. Vela: 1ª rodada real do 25 (fases 1-3, ~30 min, corredor com wsl --shutdown e medidor)
4. Rebite: suítes das próximas junções, quando houver
5. Depois das 12h15 (Codex): Cinzel (11, depois 24) e Vela (18), um de cada vez
