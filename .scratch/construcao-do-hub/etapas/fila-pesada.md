# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md; Rebite desde 06:44, suíte do 36+10 e npm test do fork) — ordem a partir de 06:55:
1. Trilho: Docker do 16, 4ª rodada (~5 min), e o Codex do 15
2. Vela: harness real do 17 (Claude, Copilot e Codex)
4. Brasa: fatias 1 e 2 do 08 numa subida (51 e 201 MiB), aceite final da revisão do Fiel: só com a máquina quieta (ninguém mais com teste
   rodando); o maestro avisa.
5. Brasa: Docker do 22 (proxy e kit de cliente: par do 07 com 5996/5997, MCP 8796-8798, busca com npm ci, ~15 min); depois os três harnesses como cliente (~10 min)
