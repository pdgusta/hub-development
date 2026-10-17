# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md)
1. Fiel: Docker das revisões do 28 (Vela, rodada 3) e do 09 (fork test:e2e:banco + sonda, e 09-mcp-banco.test.ps1),
   uma depois da outra (~10 min)
2. Brasa: Docker do 08, uma fatia por vez, destacado, piso de 2 GB. **Entre fatias, solte a trava se o Trilho estiver
   esperando (Docker do 16 de novo, ~5 min; Codex do 15 depois das 06:58) e retome depois dele.**
3. Trilho: Docker do 16 de novo (consertos ff0f362) e, a partir de 06:58, Codex do 15
