# Testes da porta do repositório fora do hub

Type: task
Status: resolved

## Question

Rodar, numa pasta de teste e restaurando as configurações globais depois, os pontos que faltam para
uma sessão aberta num repositório fora do hub receber o contrato e as skills do hub. Pedido do
Gustavo em 2026-10-12 (resposta à R32 de "Portas de entrada do hub"). No Claude Code já funcionaram
o import absoluto no `~/.claude/CLAUDE.md` e a skill por junction (grupo A de "Testes das portas de
entrada").

1. **Codex:** o `~/.codex/AGENTS.md` é sempre lido; ele importa outro arquivo? Um link de arquivo
   para o `AGENTS.md` do hub funciona?
2. **Copilot CLI:** `~/.copilot/copilot-instructions.md` ligado ao contrato do hub; e se
   `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` funciona fora do hub (numa subpasta do hub não teve efeito).
3. **Skills:** junction em `~/.agents/skills`, a pasta que Codex e Copilot leem.
4. **Copilot no VS Code:** os mesmos pontos.
5. **O link sobrevive ao LiveSync:** quando uma edição vinda da outra máquina regrava o `AGENTS.md`,
   o link continua apontando para o arquivo novo? (ambiente do spike em `C:\Projetos\spike-livesync`)

O resultado serve a "Acesso dos agentes: decisão", onde se escolhe o mecanismo de cada harness.

## Comments

- 2026-10-12: pontos 1, 2, 3 e 5 rodados (relatório em
  `exploracao/anexos/testes-42-repositorio-fora-do-hub.md`). Codex e Copilot CLI recebem o contrato
  por link simbólico no arquivo global de cada um; import com `@` no Codex e
  `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` não carregam. Skills por junction em `~/.agents/skills` servem
  aos dois. O LiveSync grava no lugar, e os dois tipos de link sobrevivem; mas o link físico se solta
  quando uma ferramenta troca o arquivo do hub por um novo, e editar pelo link com essa ferramenta
  troca o link simbólico por uma cópia. Falta o ponto 4 (Copilot no VS Code), que precisa do Gustavo.
- 2026-10-12, ponto 4, primeira tentativa (Gustavo, VS Code 1.141, chat no modo Agent, Claude Haiku
  5.5, com `~/.copilot/copilot-instructions.md` ligado ao hub falso): a pergunta do marcador foi
  recusada ("Reviewed confidential instruction and declined to disclose it"), o que não prova nem
  descarta a carga; a skill `teste-girassol` da junction apareceu (o chat disse "sem descrição"). Segunda
  tentativa por comportamento: o contrato falso agora manda terminar toda resposta com "GIRASSOL".
- 2026-10-12, ponto 4, segunda tentativa: "Quanto é 2 + 2?" em chat novo. Haiku 5.5 respondeu "4"
  sem "GIRASSOL". Grok 4.7 mostrou no raciocínio "The custom instruction references GIRASSOL-42",
  carregou a skill `teste-girassol` e também respondeu sem "GIRASSOL". O arquivo chega; a regra não
  foi seguida. Configurações restauradas e pasta de teste apagada.

## Answer

Relatório: `exploracao/anexos/testes-42-repositorio-fora-do-hub.md`.

- **Contrato fora do hub:** um link simbólico no arquivo global de cada harness para o `AGENTS.md`
  do hub funciona no Codex (`~/.codex/AGENTS.md`), no Copilot CLI e no Copilot do VS Code
  (`~/.copilot/copilot-instructions.md`); no Claude Code já funcionava o import no
  `~/.claude/CLAUDE.md`. Não funcionam: import com `@` no Codex e `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`
  (só lista o arquivo para leitura sob demanda).
- **Skills:** junction em `~/.agents/skills` serve a Codex, Copilot CLI e Copilot do VS Code (e em
  `~/.claude/skills` ao Claude Code). Não testado: `copilot skill add <pasta>`, que apontaria direto
  para a pasta de skills do hub.
- **Tipo de link:** simbólico. O LiveSync grava no lugar, e os dois tipos sobrevivem; mas o link
  físico se solta sem aviso quando uma ferramenta troca o arquivo do hub por um novo (git, `sed -i`,
  muitos editores). O simbólico pede o modo de desenvolvedor do Windows em cada par.
- **Editar só dentro do hub:** gravar pelo link com uma ferramenta que cria arquivo novo troca o
  link por uma cópia, e a edição não chega ao hub.
- **Arquivo global do Copilot ocupado:** hoje tem as instruções do GSD; o kit de par precisa juntar
  os dois.
- **Chegar não é obedecer:** no VS Code, o contrato chegou, mas uma regra trivial dele não foi seguida
  por Haiku 5.5 nem por Grok 4.7.
