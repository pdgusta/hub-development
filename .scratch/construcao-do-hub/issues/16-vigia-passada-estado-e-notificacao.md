# 16: Vigia: passada, estado e notificação

Type: task
Status: ready-for-agent
Etapa: 6 (vigia)
Blocked by: 08, 10

**What to build:** A vigia lê o banco real (cifrado) e o disco, grava o estado num arquivo local por troca atômica e avisa só quando piora. Confere a ferramenta `estado_do_hub` do MCP com o estado real (até aqui ela usava um exemplo). O item da cópia diária entra como exemplo; a etapa 9 o confere com o real.

**Fonte:** Bloco do Worker 7; faixa 7 em `spec-partes/faixas-07-08.md`; tickets 33, 08, 14, 34, 48; escolhas aceitas 6, 7, 8 e 22. Regras comuns: `../etapas/regras-da-construcao.md`.

**Blocked by:** 08 (Banco: limites e robustez), 10 (MCP do banco: três instâncias, cabeça, regra curta e estado)

- [ ] os cenários dão o estado esperado: tudo em ordem, conflito de texto, binário descartado, replicação parada com o outro par ligado, outro par incerto ("informa" com o motivo), arquivo acima de 200 MiB, sincronizador parado, Config Doctor travado, item da cópia diária
- [ ] a vigia cita a nota pelo caminho decifrado
- [ ] a notificação do Windows sai só na passada que piora
- [ ] o comando de recuperar devolve os bytes do binário perdido
- [ ] o `estado_do_hub` devolve o estado real

## Comments
