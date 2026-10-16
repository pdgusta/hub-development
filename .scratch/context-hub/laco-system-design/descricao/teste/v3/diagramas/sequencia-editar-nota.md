# Teste v3: sequência "editar nota no Obsidian até o agente que busca"

Desenho: `sequencia-editar-nota.html`. Lido só `descricao-do-hub.md`, nenhuma outra fonte.

## Faltou

1. **Tempo da troca entre bancos pela rede privada.** Seção 6 (Ligações: "tempo pela rede [NV]") e 8.1, passo 4, não dão número. Desenhei sem tempo.
2. **Tempo até a busca de B enxergar a edição.** Seção 8.9 ("tempo de uma edição até aparecer [NV]") e seção 6 (Camada de busca: "tempo [NV]"). Desenhei a reindexação (passo 8) sem tempo.
3. **O ~2 s do disco ao banco vale com dois pares?** Seção 6 diz "~2 s medido com um banco só". O desenho usa o número como se valesse no cenário de dois pares, sem dado para isso.
4. **Obsidian aberto na máquina B.** Seção 8.1, passo 5, cita só o sincronizador de B. Não diz se o plugin de B também grava o disco de B quando o Obsidian está aberto lá. Omiti o Obsidian e o plugin de B.
5. **O que o agente faz quando a porta do banco B está fora.** Seção 8.5 ("pode ler o .md do disco", marcado [L]) e seção 8.18 ("o que o agente deve fazer" marcado [A]). Desenhei a porta fora como caixa opt, sem decisão.

## Inventei

1. **Qual máquina é A e qual é B.** Seções 1 e 2 dizem "as duas máquinas" sem papel na troca. Chamei de A a que o Gustavo edita e de B a outra, sem dizer se é o notebook ou a pessoal, porque o cenário não diz qual edita.
2. **Seta do banco B para o sincronizador B.** Seção 8.1, passo 5, diz só "o sincronizador de B escreve no disco de B". Inventei o passo entre o banco e o sincronizador de B; sem ele, o disco de B não tem origem no desenho.
3. **Ordem da reindexação.** Desenhei a busca de B reindexando depois de o sincronizador escrever o `.md` (passos 7 e 8). Seção 6 diz só "quando o disco muda"; a ordem entre os dois é minha.
4. **Condições fora da sequência principal.** "Sincronizador A parado" e "B mudou o mesmo trecho" entraram como caixas opt, em posições que as seções não ordenam. "B ligada" é uma caixa alt com o "else" de B desligada, o que também é minha leitura de 8.1, falha 1.
5. **Sessão do agente já aberta.** O agente em B já está com a busca e o contrato carregados. O início de sessão (8.3) não entra, porque o cenário é de busca, não de abertura.
6. **Leitura pela porta do banco depois da busca.** Escolhi a porta (passos 11 a 13) porque 7.2 e 8.5 dizem isso. Ver Ambíguo, item 2.

## Ambíguo

1. **Plugin e sincronizador como escritores.** Seção 7.1 diz "o plugin ou o sincronizador (o primeiro que vir) leva ao banco". Seção 8.1, passo 3, diz "os dois são escritores e, juntos, não criam ciclo". Desenhei os dois (passos 3a e 3b) e deixei a dúvida numa nota.
2. **Por qual caminho o agente lê depois da busca.** Seção 8.9, passo 3, diz "o agente abre só o que precisa", sem dizer o caminho. Seções 7.2 e 8.5 dizem porta do banco. Seção 8.5 (falhas) permite ler o `.md` do disco, marcado [L], e 8.18 diz que isso está a decidir [A]. Desenhei pela porta.
