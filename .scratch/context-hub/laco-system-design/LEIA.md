# Laço do system design (ticket 56)

Laço conduzido pelo maestro e pelo recruta Designer, sem scripts próprios: os nós são trabalho de agentes. O portal
mostra este laço pela `laco.json`; o Gustavo pede mudanças pela página Laços.

- `config.json`: os valores configurados dos controles. O maestro aplica um pedido gravando o valor novo aqui.
  Todos valem na próxima execução (`proxima-execucao`) e são trocados à mão (`manual`).
- `estado.json`: fase, voltas feitas e tokens gastos; o maestro atualiza a cada etapa.
- `sinal.txt`: o maestro o cria quando a primeira etapa começa e o toca a cada etapa. Antes disso o laço aparece como
  "estado desconhecido" de propósito: é só uma proposta.
- Ao começar: trocar `execucao.id` para `system-design-<data>` e preencher `inicio`.
- Parada (`parar-de-despachar`): nenhuma etapa nova começa; a que está em curso termina e fica registrada.
