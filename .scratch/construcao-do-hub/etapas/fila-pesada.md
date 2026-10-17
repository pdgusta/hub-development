# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md) — ordem a partir de 12:55 (Codex sem cota até 17h15):
1. Rebite: suíte de 38+39+22 manutenção (trava desde 13:40; Docker Desktop parado, religar com `docker desktop start` depois)
2. Vela: fase 4 do 25 de novo, com Docker (~4 min; conserto fe0b800)
3. Rebite: junções 42, 41 (depois da revisão do Fiel), docs; 40, 37, 23 quando der
4. Depois das 17h15 (Codex), um de cada vez: Cinzel (11, 24), Vela (18, 25), Brasa (22)
