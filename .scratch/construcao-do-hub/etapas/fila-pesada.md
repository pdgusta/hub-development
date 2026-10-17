# Fila do trabalho pesado (o maestro ordena; atualizada 04:40 de 2026-10-17)

Quem solta a trava avisa o primeiro da fila (`maestri ask "<nome>" "trava livre, sua vez"`) e se tira da fila.
Quem pega a trava se tira da fila. Ordem pelo caminho crítico; o maestro reordena. Portas 5996/5997 são de vários
testes (09, 16): limpe os contêineres ao soltar.

(trava: ver trava-pesada.md) — ordem a partir de 14:25 (Codex com cota: o Gustavo redefiniu às 14:25; Windows reinicia às 21h):
1. (feito 14:47: suíte do 42)
2. (feito 14:54: Codex do 11, Cinzel)
2b. (feito 15:20: 41, 40, 43 resolvidos; docs pendente da página do Lume)
3. (feito 15:19: Codex do 18, Vela) (segura o 23 e o 37)
4. (cortada 15:33: Codex do 22, Brasa; 583 MB livres na subida, antes dos harnesses)
5. Rebite: suíte do 11 (51fa382), e do 18 se já passou no Fiel; com os docs se a página do Lume já mudou (Docker parado)
6. Rebite: junções 18, 37, 44, 23 (sem Docker)
7. JANELA QUIETA DA NOITE (a partir de ~17h30, ou quando o 23 juntar): só o maestro, o Rebite e quem roda; os outros
   gravam a retomada e saem. Um de cada vez, Docker ligado bem antes, wsl --shutdown se a memória pedir:
   a. Brasa: Codex do 22 (pilha de cliente)
   b. Cinzel: Codex do 24
   c. Vela: 25, fases 4, 5 e 7 e as do Codex (diagnóstico 3c1221a)
   Quem termina sai; o Rebite junta ao fim de cada um.
Até 20h30: todos gravam a retomada; nada pesado rodando às 21h (reinício do Windows).
