---
titulo: Escolhas do spec, carta 3: a busca
ticket: 16
aberta: 2026-10-16
estado: absorvida
carta: escolhas-3-busca
---

A carta **"escolhas-3-busca"** segue o caminho de uma nota até a resposta e marca onde cada escolha age. São quatro
escolhas, na mesma ordem desta rodada. Ela foi feita pelo Nanquim e revisada pelo Esquadro, que a passou na segunda
volta.

## 1. Quando a busca passa no teste
id: aceite
tipo: escolha
recomendada: A

- A: Aceitar: a nota certa entre as 3 primeiras e uma nota nova visível em até 60 segundos, com prazo e posição fixos (nota lenta reprova)
- B: Entre as 5 primeiras, como na bancada, e o tempo só medido, sem reprovar

## 2. A nota que fica de fora não some calada
id: recusadas
tipo: escolha
recomendada: A

- A: Aceitar: a busca conta as notas indexadas e lista as que ficaram de fora por cabeçalho quebrado, e o teste confere esse número
- B: O teste só observa: sai o total do índice e ninguém sabe quais ficaram de fora

## 3. Nada com ponto entra na busca
id: exclusao
tipo: escolha
recomendada: A

- A: Aceitar: duas regras na lista de exclusão da própria ferramenta (o nome com ponto e o que está dentro de pasta com ponto), e o teste confere que nada com ponto aparece num resultado
- B: Confiar que a ferramenta ignora sozinha o que tem ponto (não verificado nela)

## 4. O porteiro confere o endereço
id: endereco-proxy
tipo: escolha
recomendada: A

- A: Aceitar: testar pelo proxy, ver o endereço que realmente chega e só então pô-lo na lista; um endereço estranho continua recusado
- B: Pôr na lista o endereço do proxy de palpite (se errar, o cliente fica sem busca)

## Algo mais?
id: algo-mais
tipo: texto
