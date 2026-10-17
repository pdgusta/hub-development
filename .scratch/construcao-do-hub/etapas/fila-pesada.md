# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(com a trava: Rebite, suíte da junção do 35 e do 33, desde 04:37)
1. Trilho: Docker do 16 (~5 min)
1b. Fiel: Docker da revisão do 28 (Vela, rodada 3)
2. Brasa: Docker do 08, uma fatia por vez, destacado, piso de 2 GB. **Entre fatias, solte a trava se o Trilho estiver
   esperando o Codex do 15 (depois das 06:58, curto) e retome depois dele.**
3. Trilho: Codex do 15 (só a partir de 06:58)
4. Fiel: Docker do 28 rodada 3 (28-pastas-locais.test.ps1, ~3 min; o 28 só espera isso para passar) e Docker do 09 (fork test:e2e:banco + sonda, e 09-mcp-banco.test.ps1, ~5 min)
