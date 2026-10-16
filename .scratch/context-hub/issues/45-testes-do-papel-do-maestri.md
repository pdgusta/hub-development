# Testes do papel do Maestri com Codex e Copilot

Type: task
Status: resolved

## Question

Rodar, num hub falso em pasta temporária e restaurando tudo depois, os pontos que a pesquisa deixou em
"precisa de teste" para um agente aberto na pasta de um papel do Maestri (`.maestri/roles/<id>/`): o
Codex (com e sem o marcador de raiz `project_root_markers`) e o Copilot CLI chegam ao `AGENTS.md` da
raiz do hub e ao da pasta da iniciativa? O Maestri regrava os arquivos do papel a cada início de
terminal (ajuste manual neles sobrevive)? Pedido do Gustavo em 2026-10-12 (resposta à R37 de "Maestri:
padrão e liberdade": "podemos testar, após focarmos no problema que respondi na r34").

## Answer

- Recrutas do Maestri com papel abrem na pasta `.maestri/roles/<id-do-papel>/` do `--dir`; ali o Maestri grava só `AGENTS.md` e `CLAUDE.md` idênticos (prompt do papel + ponteiro para a pasta do projeto) e `role.json`.
- Codex padrão: só lê o arquivo do papel; não chega nem à iniciativa nem à raiz do hub.
- Codex com `-c project_root_markers=['HUB.md']` e `HUB.md` na raiz: lê raiz, iniciativa e papel.
- Copilot CLI (sem `.git`): lê papel e iniciativa, mas não a raiz; por que ele para na iniciativa ficou sem explicação.
- O Maestri não reescreve os arquivos do papel ao reiniciar o terminal: a linha manual sobreviveu ao `recruit --replace`.
- Mas editar o prompt do papel (`role edit`) reescreve os arquivos, apaga o ajuste manual e reinicia todos os terminais com o papel. `role delete` não apaga a pasta do papel.
- Efeito colateral: o `~/.codex/config.toml` ganhou `[projects.'c:\teste45\hub'] trust_level = "trusted"` (tela de confiança do Codex aceita sem querer). Não foi editado; o Gustavo decide se apaga.
- Pendente com o Gustavo: apagar `C:\teste45` (a trava de segurança bloqueou o `rm -rf`).

Relatório: [testes-45-papel-do-maestri.md](../../../exploracao/anexos/testes-45-papel-do-maestri.md)
