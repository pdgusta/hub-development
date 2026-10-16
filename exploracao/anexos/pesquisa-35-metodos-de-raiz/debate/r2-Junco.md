# r2 — Junco

## Onde concordo e mudo

- **8 Arquivo (Cinzel, Astrolabio): três de três.** Cinzel cortou como eu, com o mesmo FHS
  (`08-fhs.json`); Astrolabio chegou a "arquivo por tipo" (`01-para.json` não trata replicação).
  Proponho fechar: `Arquivo` deixa de ser raiz e vira estado dentro de cada raiz.
- **6 Oficina (Cinzel): achado que me escapou.** Perfil de máquina não pode dividir pasta com
  contrato e skills: um é por máquina, os outros precisam de caminho fixo (`15-diretorio-claude.json`).
  Concordo em separar. Ressalva: `15` diz "OAuth session, per-project trust decisions", ou seja,
  estado pessoal; "da máquina" é inferência de Cinzel, plausível mas fora do JSON.
- **7 Entrada (Astrolabio): corrijo meu voto.** Citei GTD como sustento, mas `05-gtd.json` tem
  `nivel_raiz` vazio: sustenta a função (capture→clarify), não a pasta. A pasta se sustenta por
  "variável" (`08`) e pelo runtime com limpeza (`09-xdg.json`), como Cinzel disse.

## Onde discordo

**Cinzel, 2 e 4 não se juntam só porque "método de sistema" não os separa.** O teste de Cinzel
é "só replicação é critério de sistema". Mas o briefing define a raiz por quatro colunas: dado
de cliente, termina, quem lê, o que acontece ao envelhecer. Descartar as outras três porque FHS e XDG
são calados nelas é usar o limite dos métodos como regra. Métodos de
sistema nada dizem de envelhecer (`08`, `09`): não podem ser juiz disso.

- **4 × 3 (Estudo × Produtos):** diferem em "quem lê": ele, contra agentes no repositório (briefing).
  "Termina" é estado, concordo; "quem lê" não é. Diferem também no destino: promover ou arquivar ×
  arquivo. A junção ganharia promoção sem mudar de pasta, o que depende de um fato fora dos JSON:
  spike vira produto na prática?
  **Pergunta ao Gustavo.** Se sim, concedo a junção; se não, 4 fica.
- **2 × 1 (Operações × Clientes):** aqui Cinzel tem mais razão que eu. A evidência de separar é só
  PARA (`01`: Projects × Areas), e mesma replicação. Mantenho a separação por um motivo de uso: o
  destino é diferente (compactar × arquivar) e "todo arquivo tem destino" precisa de casa. Concedo
  condicionalmente: se destino puder ser declarado por pasta, como replicação, então 2 vira estado de
  1. Falta saber se SOC STRATA é cliente ou operação interna: não está nos JSON.

## Onde Astrolabio errou, ou deixou em aberto

- **3 "fica aberto" porque PARA não decide.** Não precisa: PARA falha ali (`01`: "short-term
  efforts"), e 3 se sustenta por outro lado: sem dado de cliente, replicado, lido por agentes no
  repositório. Resolve sem PARA.
- **9 junto de 2, "como PARA".** Em `01`, Areas inclui Health (pessoal), mas 2 carrega dado de
  cliente não replicado. Juntar jogaria dado pessoal numa pasta declarada de cliente. Só
  é junção se replicação coincidir: o teste de Cinzel serve aqui.

## O que falta

1. **Nenhum JSON diz algo sobre o que o Gustavo vê na vista Markdown** quando uma pasta é não
   replicada (a outra máquina por SSH, camada de busca não indexa: GLOSSARY). Uma raiz com 1+2+perfil
   some da busca da segunda máquina. É custo real do dia a dia, ainda sem dono.
2. **Entrada:** padrão local (meu voto) ou replicada com checkpoint que destina? Cinzel deixou como
   aberto, e eu proponho: local por máquina, e o checkpoint é o único ponto em que dado de cliente
   sai dela, rumo a 1/2 (promoção explícita). Teste: contradiz alguém?
3. **Nota de retomada:** só Cline (`10`) toca, e Cinzel concorda. Proponho: mora dentro da pasta de
   cada iniciativa, não numa raiz própria.

## Placar provisório

Manter: 1, 5, 6 (dividido), 7, 3. Cortar como raiz: 8. Aberto, dependendo do Gustavo: 4, 2, 9.
