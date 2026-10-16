# Acervo do maestro: pesquisa de peças

Type: research
Status: resolved

## Question

Que tipos de peça podem morar no "acervo do maestro" do hub, além de papéis, setups e contratos-opção
(como o roteamento de modelos), e como cada uma se apoia no que o Maestri e os harnesses oferecem? Para
cada tipo candidato: o que a fonte primária diz (documentação oficial do Maestri, skills oficiais
`maestri-*` instaladas, documentação de Claude Code, Codex e Copilot sobre skills, subagentes, plugins,
hooks e instruções), o que a peça guardaria, com que comando ou recurso o maestro a usa, e se a peça
pode ser personalizada por workspace. Também: como a família de skills oficiais `maestri-*` se organiza
(o modelo que o Gustavo quer seguir para o acervo), e o que a fonte diz sobre o CLAUDE.md/AGENTS.md "do
workspace" do Maestri (onde fica, o que injeta), que pode levar a "primeira instrução" a workspaces fora
do hub. Sem inferência: o que a fonte não disser fica "não verificado". Pedido do Gustavo em 2026-10-12
(resposta à R38 de "Maestri: padrão e liberdade").

## Comments

- Fatos de partida: `exploracao/anexos/pesquisa-37-portas/porta-3-4-maestri.md` e os comentários de
  "Maestri: padrão e liberdade" (fatos da CLI e do uso atual).

## Answer

Relatório completo: [pesquisa-43-acervo-do-maestro.md](../../../exploracao/anexos/pesquisa-43-acervo-do-maestro.md).

- **Tipos de peça novos com apoio na fonte:** preset de agente (a linha de comando de cada agente), nota-modelo e
  quadro de fichários, rotina-modelo, receita de floor (com os comandos de preparo), workspace-modelo (clonar com
  `workspace create --from`), receita de portal (telas e tamanhos para QA) e ambiente (Local, WSL...). Conta é um
  campo dos setups e do roteamento, não uma peça própria.
- **Dos harnesses:** subagente (ajudante que roda dentro do recruta, sem ocupar um terminal), perfil de modelo (a
  parte executável do roteamento: `--model`, `--profile`, endereço de gateway), hook de início de sessão e skill
  de procedimento. Estilo de saída e plugin valem pouco; atalhos de barra já foram trocados por skills nos três.
- **Limite importante:** o maestro não aplica partitura nem configura hooks de floor pela CLI (só a interface ou
  a API Wire). Setup que o maestro monta sozinho precisa ser uma receita de comandos.
- **Papel global** é o papel sem workspace (doc Wire). Hoje nenhum dos 41 papéis é global.
- **Família oficial:** sete skills, cada uma um único SKILL.md (3 a 18 KB), divididas por assunto, com descrição
  "faz X. Use when...", referência cruzada pelo nome e o mesmo preâmbulo. O app regrava só esses sete nomes e
  apaga só essas pastas; um acervo com outro nome (sugestão: sem o prefixo `maestri-`) não colide.
- **Para o acervo crescer:** SKILL.md curto como catálogo, mais um arquivo por peça (padrão de referências das
  skills).
- **CLAUDE.md/AGENTS.md "do workspace"** são os arquivos da pasta de trabalho do workspace. O Maestri só os edita;
  quem lê é o próprio agente. Neste build, a "sincronia" é um botão que copia um arquivo sobre o outro.
- **Terminal com papel:** abre numa pasta própria com o texto do papel e o caminho do projeto. Só Gemini e Qwen
  ganham do Maestri um ponteiro para o AGENTS.md do projeto.
- **Primeira instrução:** o Maestri não tem instrução global para workspace novo. O que alcança todo workspace,
  dentro ou fora do hub, é o arquivo global de cada harness; reforços possíveis são a skill do acervo e um hook de
  início de sessão que só age quando a variável `MAESTRI_TERMINAL_ID` existe.
- **Precisa de teste** antes de decidir: Codex e Copilot dentro da pasta de um papel, o FreeLLMAPI em cada
  harness, e se o clone de workspace leva os arquivos da pasta.
