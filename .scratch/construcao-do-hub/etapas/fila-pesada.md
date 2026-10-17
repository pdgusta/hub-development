# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md; Brasa nas fatias 3-7 do 08) — ordem a partir de 06:25:
Entre uma fatia e outra a Brasa solta para quem estiver esperando, nesta ordem:
1. Fiel: Docker da revisão do 10, rodada 2 (~8 min; caminho crítico)
2. Trilho: Docker do 16, 4ª rodada (~5 min), e o Codex do 15 se já passou de 06:58
3. Vela: harness real do 17, Claude e Copilot (Codex do 17 depois das 06:58)
Depois das fatias da Brasa:
4. Rebite: suíte da junção do 36 e do 10 (hub 9cc878b) e npm test do fork (integracao 34c3e50), ~20 min
5. Brasa: fatia 2 do 08, em hora quieta combinada pelo maestro
