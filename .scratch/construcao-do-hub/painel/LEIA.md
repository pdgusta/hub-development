# Painel da construção: carcaça

Só lê a pasta da execução e mostra. Nenhum controle manda nada para ela. Contrato: `contrato.md`.

## Como abrir

| Para quê | Comando | Endereço |
|---|---|---|
| A execução de verdade (`../execucao/`) | `painel\iniciar.cmd` | http://127.0.0.1:8771/ |
| A simulação do QA, ao vivo | `node fixture\gerar.mjs`, depois `painel\iniciar.cmd --fixture` | http://127.0.0.1:8771/ |
| Outra pasta | `python servidor.py --pasta CAMINHO [--porta N]` | http://127.0.0.1:N/ |
| Sem servidor (fixture parada) | abrir `web\index.html` direto do disco | lê `fixture\embutida.js` |
| Pelo portal | carta que aponta para `abrir.html` | embute 8771; se o painel estiver desligado, diz como ligar |

`fixture\embutida.js` sai de `python -I fixture\instantaneo_ui.py` (a fixture parada do UI engineer, em
`fixture\instantaneo-ui\`) ou de `python -I fixture\embutir.py PASTA --agora ISO` (qualquer pasta de execução).

## Peças

- `servidor.py`: Python, só biblioteca padrão, 127.0.0.1, só GET, confere o `Host` (contra rebinding de DNS).
  `/api/execucao` e `/api/eventos?c=agente:byte` (só o novo de cada arquivo). Não interpreta eventos.
- `web/leitor.js`: a reconstrução inteira (contrato, seção 7), igual para o servidor e para a fixture embutida.
  `montar()` é pura e roda no Node (`require('./web/leitor.js')`).
- `web/tela.js` e `web/painel.css`: a tela. Pede o novo a cada 3 s e redesenha a cada 1 s, no lugar (sem refazer o
  DOM): foco, hover e gaveta aberta ficam.
- `web/index.html`: as regiões. Placar (trabalhando agora, feitos, desde quando, estado da leitura), alertas (falhou,
  passou de 1 hora, sem sinal, espera você; "nada travado" quando vazio), centro (rede dos agentes com as conversas
  dos últimos 20 min pelas calhas entre os cartões; linha dos tickets por etapa), gaveta de detalhe (cobre a coluna dos
  tickets; a rede fica parada e à vista), faixa de leitura na borda de baixo.

## Quando o desenho do laço for aprovado

Muda a tela, não o contrato: papéis e cores em `painel.css` (`--p-<papel>`) e em `GRUPOS` de `tela.js`; etapas da
linha em `ESTACOES`; nomes de tipo e de status em `TIPOS` e `STATUS` de `leitor.js`.
