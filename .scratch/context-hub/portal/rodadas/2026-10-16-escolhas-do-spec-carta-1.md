---
titulo: Escolhas do spec, carta 1: gravar e ler no banco
ticket: 16
aberta: 2026-10-16
estado: absorvida
carta: escolhas-1-banco
---

A carta **"escolhas-1-banco"** mostra o MCP do banco como uma agência: os agentes no balcão, os guichês e o cofre. São
seis escolhas, na mesma ordem desta rodada. Ela foi feita pelo Designer e revisada pelo Lente, que a passou na segunda
volta. No celular, o mapa do topo abre só com os agentes e o proxy; é preciso arrastar para o lado para ver o resto.

## 1. Conflito à vista
id: conflito
tipo: escolha
recomendada: A

- A: Aceitar: ver o conflito de dois jeitos, um aviso com as duas versões ao ler a nota e uma ferramenta que lista todos os conflitos abertos
- B: Só o aviso ao ler a nota
- C: Só a ferramenta que lista os conflitos

## 2. A cabeça do contrato
id: cabeca
tipo: escolha
recomendada: A

- A: Aceitar: um bloco marcado no `AGENTS.md`, relido a cada conexão, sem cópia, posto antes do texto que o MCP já traz; a manutenção só confere se ele existe e cabe em 2.000 caracteres
- B: Relida, mas depois do texto que o MCP já traz (o Claude Code corta o fim e a cabeça pode chegar pela metade)
- C: Um texto copiado e fixo na configuração do MCP (se o `AGENTS.md` mudar, a cópia fica velha)

## 3. A regra curta
id: regra-curta
tipo: escolha
recomendada: A

- A: Aceitar: "antes de gravar, leia `AGENTS.md`" em todas as ferramentas de gravação, e a segunda frase ("grave com a versão lida; conflito = releia e refaça") só nas que recebem a versão (gravar e editar); apagar e mover ficam com a guarda a definir
- B: A segunda frase nas quatro ferramentas, mesmo nas que não recebem a versão
- C: Só a primeira frase, em todas

## 4. O nome da ferramenta de estado
id: nome-estado
tipo: escolha
recomendada: A

- A: Aceitar: `estado_do_hub`, que devolve o estado da vigia e, sem arquivo, "estado indisponível" (nunca "em ordem")
- B: Outro nome, em inglês como as vizinhas (diga qual no "Algo mais?")

## 5. Quantos guichês por máquina
id: guiches
tipo: escolha
recomendada: A

- A: Aceitar: dois por máquina, um de leitura e um de escrita, e o de escrita atende também o cliente pelo proxy (os dois juntos ainda não foram testados)
- B: Três: um de escrita só para o cliente, separado do que os agentes da máquina usam

## 6. Cifra de ponta a ponta com o caminho embaralhado
id: caminho-embaralhado
tipo: escolha
recomendada: A

- A: Aceitar: o banco cifra o conteúdo e também o caminho das notas (como no teste de disco e banco sem o Obsidian); o MCP e a vigia usam a frase-senha para ler o caminho em claro
- B: Cifrar só o conteúdo: o caminho fica legível no banco (nomes de clientes e de notas à vista para quem abrir o banco)

## Algo mais?
id: algo-mais
tipo: texto
