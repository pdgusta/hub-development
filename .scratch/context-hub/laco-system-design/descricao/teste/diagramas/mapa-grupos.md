# Mapa de grupos e lugares: notas do desenhista

Diagrama: `teste/diagramas/mapa-grupos.html`. Fonte única: `descricao-do-hub.md` (v1, 2026-10-15).
Não renderizei o HTML em navegador; confirmei só que o SVG é XML bem formado. Confira no navegador se algum texto
estourar a caixa.

## Faltou

1. **Lugar dos atores.** §2 diz por onde cada ator chega, mas não diz em qual lugar ele está. O Claude Desktop roda no
   Windows e aparece em §5.1 como "fora do par", então não dá para saber de qual lado desenhar (ver Ambíguo 1).
2. **Lugar da sessão do agente e da configuração da ferramenta.** §5.2 lista os dois como lugares, mas não diz se estão
   dentro da máquina ou ao lado dela. Desenhei dentro, por serem por máquina (§3.1 "Em cada par"; §5.2 "cada máquina tem
   a sua").
3. **Regra para grupo que atravessa lugares.** §5.1 põe a "Disciplina do agente" com componentes que moram em três
   lugares (disco, configuração, sessão). Falta dizer como desenhar um grupo cujos membros estão em lugares diferentes.
4. **Agendador do Windows como lugar.** §5.2 coloca sincronizador, vigia e cópia diária no agendador, mas §3.1 e §5.1
   não o citam como componente nem grupo.
5. **Grupo da cópia diária.** §4 e §5.2 tratam a cópia diária como tarefa própria, e §5.1 não a põe em nenhum grupo.
6. **Lugar das portas (MCP).** §5.2 não diz em que processo ou lugar rodam a porta do banco, a porta de leitura e a
   camada de busca. Pus todas dentro da máquina.
7. **Lugar dos avisos.** §3.1 diz que o estado aparece na tela via mod, barra ou checagem, mas §5.2 não diz onde o
   aviso mora (ver Inventei 9).

## Inventei

1. **Aninhamento.** Desenhei sessão do agente e configuração da ferramenta dentro do quadro da máquina, e não ao lado.
   Motivo: §3.1 e §5.2 dizem que ambas são por máquina.
2. **Claude Desktop fora do quadro da máquina.** Está no topo, como ator, com a ponte até a porta do banco. Motivo: §2
   e §5.1 o tratam como quem chega, mesmo rodando no Windows.
3. **Gustavo no topo.** Não há lugar para ele em nenhuma seção; é ator, como em §2.
4. **Divisão do "Fora do par" de §5.1 em subgrupos.** Criei "Ponte entre máquinas", "Cópia de segurança" e "Referência e
   modelos". §5.1 traz um único grupo com todos.
5. **Divisão da "Disciplina do agente" de §5.1.** Desenhei só "Disciplina do agente: hooks" na configuração. Contrato e
   nota de retomada foram para "Conteúdo no disco", e a checagem de sessão ficou em hooks, não em vigilância, apesar de
   §5.1 pôr em ambos.
6. **Grupo "Ligações, memória e configuração de MCP".** Não existe em nenhuma seção; agrupei ligações, memória privada,
   MCP, mod e biblioteca do Maestri porque §5.2 os lista juntos na configuração do usuário.
7. **Credenciais e nó da rede na periferia do par.** §5.1 põe nó da rede na periferia, mas não diz onde ficam as
   credenciais (§3.1 só diz "ficam na máquina").
8. **"Porta principal: sessão na raiz" como componente da sessão.** §3.4 o trata como porta de entrada, não como
   componente. Pus na sessão para caber no desenho.
9. **Avisos na configuração.** Coloquei o mod do Claude Code na configuração (§5.2 cita o mod nessa linha) e o aviso em
   geral na vigilância. Ver Ambíguo 3.
10. **Quais ligações desenhar como seta.** Só as entre vizinhos diretos; as demais aparecem como números nos dois
    extremos, com a lista abaixo do desenho. As setas do agente para o disco (7) e para a camada de busca (6) estão nos
    números, não desenhadas.
11. **Tratamento dos tracejados.** Usei tracejado para "a construir, em curso ou a decidir" e para lacuna, juntos, por
    §11 pedir marca de "a decidir" ou "não verificado" sem separar as duas.

## Ambíguo

1. **Claude Desktop.** §2 o põe como "o app Claude no Windows", ou seja, dentro da máquina. §5.1 o põe em "Quem chega" e
   em "Fora do par" ao mesmo tempo. §3.4 só fala da ponte.
2. **Hooks e checagem de sessão.** §3.1 diz "hook no começo de toda sessão de agente", o que sugere que rodam na sessão.
   §5.2 põe os hooks na configuração do usuário. Desenhei o hook na configuração e a sessão recebendo o efeito.
3. **Onde mora o aviso.** §3.1 ("Avisos") diz que a saída aparece na tela, mas §5.1 o põe no grupo de vigilância e §5.2 não
   o lista como lugar. Não há resposta única.
4. **Sincronizador.** §3.1 o descreve como componente de cada par; §5.1 o põe no núcleo de dados; §5.2 o põe no
   agendador do Windows. Desenhei no núcleo de dados dentro da máquina, com a nota "agendado".
5. **Biblioteca do Maestri.** §5.2 a trata como lugar próprio (`~/.maestri`). Desenhei dentro da configuração da
   ferramenta, mas §12 a trata como coisa de fora do hub; a leitura é minha.
