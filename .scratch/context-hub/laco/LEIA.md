# Laço da pesquisa ampla

Os scripts da [proposta refeita](../prototipos/proposta-50-laco-da-pesquisa.md). Os modelos só respondem;
quem grava é o script. O estado comum fica em `estado/laco.db` (SQLite), e cada gerador escreve o seu
livro-razão em `livros/<grupo>.jsonl` (só de acréscimo). Tudo retoma de onde parou: se um processo cair,
basta rodar o mesmo comando de novo.

Requisitos: Python 3.12, o gateway em `http://localhost:3001`, as variáveis de usuário `FREELLM_API_KEY` e
`FREELLM_DASHBOARD_TOKEN`. Nenhuma dependência fora da biblioteca padrão.

## Partida (maestro)

```
python plano.py                      # cria as 98 células da onda 1 (7 ângulos x 7 línguas x 2 formulações)
python despachante.py --uma-vez      # lê o gateway e monta a tabela de modelos
python despachante.py --teto P H     # teto do Gustavo: P tentativas no total, H horas (0 = sem esse limite)
```

Depois, cada recruta liga o seu processo. Para parar tudo: `python -c "from comum import *; c=abrir_banco(); gravar_controle(c,'parar',True)"`.

## Papéis

### Despachante (Claude Opus 5.5)

- Liga: `python despachante.py --servico`. A cada 60 s ele relê catálogo, limites e pools, devolve à fila
  pedidos presos em voo e grava `estado/despachante.json`.
- Olha só `estado/despachante.json` e `estado/despachante.log.jsonl`. Não lê as respostas dos modelos.
- Reage: se um modelo erra sem parar e não sai sozinho, põe o id em `excluir_manual` no `config.json` (o
  despachante só lê o config ao ligar: reiniciar o despachante para valer). Se `aptos` cair a zero, avisa o maestro.
- O roteamento roda dentro dos geradores (`despachante.escolher` e `despachante.liberar`), no mesmo banco;
  o serviço só mantém a tabela em dia.

### Geradores (3, Claude Haiku 5.5)

- Cada um liga o seu grupo: `python gerador.py --grupo pt-es`, `--grupo en-de-ru` ou `--grupo zh-ja`.
- Olha a saída do processo e as linhas `"estado": "erro_do_script"` no seu livro-razão. Se o processo cair,
  roda o mesmo comando de novo. Não mexe em prompts nem em modelos.
- O processo para sozinho no teto ou quando o laço termina.

### Juntador (Claude Sonnet 5.5)

- Liga: `python juntador.py --servico`. Quando uma onda termina, ele junta tudo em `catalogo/itens.json`,
  mede a taxa de novos, cria as células da onda seguinte (bola de neve) e grava `ondas/onda-N.md`.
- A cada onda, lê `catalogo/ambiguos.json` (o mesmo nome com repositórios diferentes) e decide em
  `catalogo/decisoes.jsonl`, uma linha por decisão:
  `{"juntar": ["gh:a/x", "gh:b/x"]}`, `{"separar": "nomenormalizado"}` ou
  `{"quarentena": "chave", "motivo": "fora do escopo: ..."}`. Nada é apagado; a quarentena só separa.
- Não abre `sementes.json` e não cita os nomes de lá em lugar nenhum.
- Quando o laço termina (duas ondas abaixo de 5% de novos, mais a onda de calibração), avisa o maestro.

### Maestro (Claude Opus 5.5) e conferidor (Claude Sonnet 5.5)

O maestro dispara o conferidor sobre `catalogo/itens.json` (os mais citados e as sementes primeiro), faz a
auditoria por amostra e escreve a síntese. Isso fica fora destes scripts.

## Arquivos

| Arquivo | Quem escreve | O que é |
|---|---|---|
| `config.json` | maestro, despachante | limites, ritmo, grupos, gate |
| `plano.json` | maestro | contexto, perguntas por ângulo e língua, formato da resposta, modelos da bola de neve |
| `sementes.json` | maestro | sementes ocultas; só o juntador lê |
| `estado/laco.db` | todos os scripts | modelos, uso por janela, células, pedidos, controle |
| `livros/<grupo>.jsonl` | gerador | cada chamada: modelo, provedor, tentativas de chave, tempo, estado, itens ou erro |
| `catalogo/itens.json` | juntador | o catálogo junto, com fontes, famílias e menções |
| `ondas/onda-N.md` | juntador | o painel de cada onda |

## Desde 2026-10-13: processos fora do Claude Code

O limpador de memória do Claude Code mata processos em segundo plano quando a máquina fica sem memória. Por
isso o maestro liga os 5 processos com `Start-Process` (PowerShell, `-WindowStyle Hidden`), com a saída em
`logs/<nome>.out.log` e `logs/<nome>.err.log`. O juntador roda com `--servico`. Os recrutas não religam nada.
