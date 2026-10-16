# Teste curto: a gravação dos agentes quando o arquivo muda (ticket 11, rodada 1 = C)

Brief do maestro, 2026-10-15. Pedido do Gustavo: antes de decidir por onde o agente grava, um teste curto do que cada
ferramenta de gravação faz quando o arquivo muda entre a leitura e a gravação, e se um hook antes da ferramenta
recusa a regravação inteira. Rodada em `portal/rodadas/2026-10-15-como-os-agentes-gravam-r1.md` (leia a pergunta 1 e o
contexto). Responda em pt-BR.

## Onde

A bancada de acesso: `C:\Projetos\bancada-acesso\` (hub de mentira, já usada; relatório em
`C:\Projetos\context-hub\.scratch\context-hub\bancada-acesso-relatorio.md`). Crie uma pasta `gravacao\` lá dentro para
os arquivos e os logs deste teste.

## Os casos, em cada harness

Para cada um: o agente lê uma nota de teste; um script seu muda a nota no disco (outra linha, ou o trecho que o agente
vai trocar); o agente grava. Registre o que ficou no disco e o que a ferramenta respondeu.

1. **Troca de trecho, trecho ainda igual:** a mudança externa foi em outra linha.
2. **Troca de trecho, trecho mudou:** a mudança externa alterou o próprio trecho.
3. **Regravação inteira de um arquivo que existe:** depois da mudança externa.
4. **Hook antes da ferramenta:** um hook de teste (só na bancada, no escopo de projeto quando o harness permitir)
   recusa a regravação inteira de um arquivo que já existe e deixa passar a troca de trecho e o arquivo novo. Confira
   que recusa e que deixa passar.

Ferramentas: no **Claude Code**, Edit e Write; no **Copilot CLI**, a edição dele (e a regravação, se houver); no
**Codex**, o `apply_patch`.

## Quem faz o quê

- **Subagente do maestro:** Claude Code e Copilot CLI. Rode o Claude Code com `claude -p` na pasta da bancada (modelo
  `haiku`) e o Copilot CLI como no relatório da bancada.
- **Recruta Sonda Codex:** o Codex, com o contorno já achado (`codex exec -s workspace-write -c
  'windows.sandbox="unelevated"'`); se o hook não rodar assim, tente com acesso total e diga.

## Regras

- Fonte primária para o que a ferramenta promete (documentação oficial, com trecho); o resto é o que o teste mostrou.
- Arquivos globais (`~/.claude/`, `~/.codex/`, `~/.copilot/`): de preferência não toque; se precisar, cópia antes e
  restauração conferida por hash depois, anotada.
- Não leia arquivos de credencial. Nada de dado de cliente. Processos que abrir, encerre pelo PID.
- Não toque no repositório `C:\Projetos\context-hub` além do arquivo de entrega.

## Entrega

`C:\Projetos\context-hub\.scratch\context-hub\bancada-gravacao-<harness>.md` (um por executor: `claude-copilot` e
`codex`), com uma tabela caso × ferramenta (o que ficou no disco, o que a ferramenta disse, passou ou falhou), as fontes
e o estado dos arquivos globais no fim.
