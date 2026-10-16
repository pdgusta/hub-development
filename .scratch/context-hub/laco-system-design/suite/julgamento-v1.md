# Julgamento das categorias, versão 1 (o maestro, 2026-10-15)

**Veredito: volta para ajuste (volta 1 de 3).** A divisão em 11 categorias está boa e os nomes saíram do conteúdo,
como o Gustavo pediu. A suíte por papel ainda não fecha a régua nem o QA, e há pontos em aberto que eu decido aqui.

## Decisões do maestro sobre os pontos em aberto

1. **Skills manuais:** ficam manuais. Um recruta do Maestri recebe o meu `maestri ask` como se fosse texto do
   usuário, então "/prototype …" no começo da mensagem chama a skill pelo nome. `prototype` fica com a marca de
   manual (nada de invocação autônoma), e o conflito com `parallel-concepts` fica resolvido.
2. **Plugins `design:*` do usuário:** os recrutas herdam os plugins do usuário. A pasta de cada papel ganha um
   `.claude/settings.json` que desliga esses plugins só ali (`enabledPlugins`). Conferir na documentação oficial do
   Claude Code a chave e o formato exatos, com citação.
3. **Checkpoints do `web-design-engineer`:** edito a cópia. Onde ele manda esperar o usuário, passa a gravar a
   decisão tomada e seguir. Quem decide a direção é a porta (Tech lead e UX revisor) e, depois, o Gustavo na carta.
   A seção Direction Advisor sai, porque sugere escolas visuais, e isso é restilizar.
4. **Tastemaker:** não entra como skill, pelos riscos e pelo gatilho largo. Ficam (a) o `check_contrast.py`, copiado
   depois de relido, no QA; e (c) as referências do Gustavo como imagens para o UX revisor. Elogiados: o mapa de
   metrô e a maré. Recusados: o laudo denso e a cidade radial v2 restilizada.
5. **A régua não coberta:** criamos uma skill nossa, `regua-da-cidade`. Ela traz os critérios do Gustavo escritos como
   regras verificáveis: linhas sem se cruzar, vista de cima, distância mínima entre itens, nomes que digam o que o item
   referencia, papel de cada item na cidade, reinventar a forma. Traz também como medir cada regra e as referências
   elogiadas e recusadas. Vai para o UX revisor, o Tech lead e o QA, e o UI engineer a lê antes de construir.
6. **"Faz sentido como cidade":** `information-architecture` entra no Tech lead, com a nota "ignore card sort e tree
   test". O resto é o texto do hub.
7. **Movimento:** a primeira amostra é estática. `animate` sai do UI engineer por ora, e nada de GSAP.
8. **Corpos não lidos:** ler inteiros `variant`, `heuristic-evaluation`, `ux-writing` e `information-architecture`
   antes de fechar. `variant` contra `parallel-concepts` + `prototype`: fica a combinação que dá conceitos realmente
   diferentes lado a lado num seletor, sem duplicar.
9. **Medição:** criamos uma segunda skill nossa, `medidas-da-peca`, com scripts escritos e lidos por nós. Ela conta
   cruzamentos de linhas e a distância mínima entre nós no SVG ou no DOM, confere links, mede peso e tempo de carga, e
   inclui o `check_contrast.py`. Vai para o QA.
10. **Copiar pastas, não instalar:** aceito. Cada skill copiada leva o LICENSE junto e a origem (repositório, caminho,
    commit) anotada.

## O que a versão 2 precisa trazer

- As leituras do item 8 e a escolha que resulta delas.
- A suíte por papel refeita com as decisões acima, incluindo as duas skills nossas como itens a escrever, cada uma com
  a lista do que contém.
- Para cada skill copiada: a origem (repositório, caminho, commit), as alterações na cópia (o que sai ou muda) e a
  invocação (autônoma ou manual).
- O formato exato do `.claude/settings.json` que desliga os plugins `design:*` na pasta do papel, com a citação da
  documentação.
- Nenhuma skill nova de fora sem ficha.
