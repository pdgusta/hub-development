# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md; Rebite desde 06:44, suíte do 36+10 e npm test do fork) — ordem a partir de 06:55:
1. Trilho: Docker do 16, 4ª rodada (~5 min), e o Codex do 15
1b. Rebite: testes do fork do 10 (node --import tsx --test, ~5 min); resolve o 10
2. Vela: harness real do 17 (Claude, Copilot e Codex)
3. Cinzel: harness real do 11 (Claude, Codex e Copilot duas vezes, ~10 min, uma sessão por vez)
4. Brasa: fatia 2 do 08 (51 e 201 MiB), como evidência da revisão: só com a máquina quieta (ninguém mais com teste
   rodando); o maestro avisa.
Rebite: unitários do fork para fechar o 10 (node --import tsx --test "src/**/*.test.ts" na worktree integracao do fork; ~5 min)
