# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md; Brasa desde 09:16, Docker do 22) — ordem a partir de 09:35:
2. **Janela quieta** (o maestro conduz; plano na retomada do maestro): todos salvam, os agentes menos Brasa e Vela
   saem; Brasa roda o Docker do 22 (com os harnesses) e a fatia 1+2 do 08; Vela roda a 1ª rodada real do 25 (fases 1-3); depois o maestro religa todos. Começa quando o Trilho soltar a trava do 21.
3. Rebite: suítes das junções que estiverem prontas
4. Depois das 12h15 (Codex): Cinzel (11, depois 24) e Vela (18), um de cada vez
