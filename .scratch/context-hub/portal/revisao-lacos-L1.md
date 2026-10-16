# Laços L1 — revisão do contrato, Prumo, 2026-10-14

## Parecer vigente após correção dirigida

**L1 APROVADO para abrir L2.** Os cinco importantes do parecer original abaixo estão resolvidos no contrato revisado; o texto anterior fica como histórico. Esta aprovação é da especificação, não da implementação.

Conferidas §2.6, §3.4, §4.4, §4.5, exceções nas regras gerais e Anexo A:

1. Revisão inclui definições relevantes, fontes, capacidades e valores de precondições; `teto.inicio` detecta reinício do relógio. Retrato persistido permite conferência campo a campo antes do efeito.
2. Configurado e em uso são separados na API e na tela. Em uso é não confirmado por padrão; confirmação exige fonte apropriada ou recibo válido compatível. Releitura contínua é apresentada como releitura, não prova de uso.
3. Entrega do aviso não encerra o trabalho. `lida`, `aplicando` e efeito aguardado entram na retomada; `aplicando_desde` precede efeitos e a reconciliação confere UUID e efeito existente antes de continuar, sem reiniciar processo/relógio às cegas.
4. Recibos têm serialização, tipos, execução, valores e ordem temporal validados; inválidos são visíveis e não confirmam aplicação/uso. Dono das chaves e exceções estão declarados. `substitui` tem compatibilidade, estados e unicidade definidos.
5. Espera você exclui rodada respondida na versão atual, conflito substituído, execução antiga e laço terminado; critérios correspondentes constam no L2.

Versão, retomada condicionada à capacidade, SQLite ausente/nulo/múltiplas linhas, onda ilegível e resumo do gate com calibração também tratados. Anexo distingue fatos/suposições e o retrato final da ampla do banco reutilizado.

**Sugestão de redação, sem bloquear L2:** §4.3 e §4.5, trabalho pendente em `lida`: explicitar “exceto comentários já lidos”, pois a regra específica encerra comentários em `lida`. Ao dizer “pedido já com desfecho → nada a fazer”, ressalvar `aplicado` com `efeito: aguarda`, cuja confirmação continua pendente conforme os parágrafos seguintes. São exceções já definidas no próprio contrato, não funcionalidades novas.

Revisão documental dirigida: nenhum teste, consulta nova ao banco, execução de laço ou escrita na caixa real. Próximo: Designer consolidar essas ressalvas na redação e conduzir L2, trazendo implementação e provas para revisão própria do marco.

---

**Ainda não aprovo L1 para implementação: cinco ajustes importantes de contrato abaixo.** Recomendo manter a arquitetura e corrigir só esses pontos no texto/anexos. Não pedi redesenho, código nem execução de laço.

Li `lacos-brief.md`, a decisão do ticket55 e as seções novas de `proposta.md`, confrontando os mecanismos com `gerador.py`, `juntador.py` e `despachante.py`. Não executei testes, consultas novas aos bancos ou processos dos laços nesta revisão de especificação.

## Escolhas aceitas

- Registro explícito `lacos.json`, relido por pedido, com fontes confinadas e ids estáveis. Endpoints próprios fora do estado geral; incluir descrições na versão e consultar contadores apenas na tela Laços é adequado. O texto da §3.4 deve dizer “fontes de estado dos laços não entram em api/versao”, pois a frase inicial diz que nada entra e a seguinte inclui os descritores.
- A mesma caixa e tipo `alteracao-laco`, idempotência antes da validação corrente, campos tipados e execução obrigatória. Revisão só contextual para comentários/pausa/parada/retomada é aceitável: essas operações precisam revalidar execução, capacidade e alvo temporal, não todos os valores dos controles.
- Hash sem contadores/timestamps de leitura; origens declaradas rotuladas como tal; releitura ao ligar; SQLite sem comandos vindos do browser. Não trocar SQLite por immutable: respeitar WAL como especificado.
- Maestro preencher desfecho/recibo no Markdown é uma extensão coerente do dono da caixa, sem nova aprovação humana necessária. Mas deve ser explicitada nas regras gerais, hoje ainda contraditórias (item4).
- Anexo distingue fatos/suposições, controla o reinício do relógio de teto e usa o retrato final da ampla em vez do banco reaproveitado. Suítes depois e comentários por nó/laço atendem ao ticket55.

## Importantes

1. **Revisão ignora mudanças que alteram o significado do pedido.** §4.4, “Revisão da configuração”, §4.5, “Como o maestro aplica”, A.1 teto. Só `{id,execucao, valores dos controles}` não detecta mudança de origem, tipo, unidade, opções/faixa ou capacidade; o maestro pode interpretar pedido antigo por uma descrição nova. Caso concreto: `--teto` muda `controle.teto.inicio` sem necessariamente mudar pedidos/horas; a revisão continua igual, embora a janela de horas tenha sido reiniciada. **Recomendação:** manter títulos/contadores fora, mas incluir uma revisão das definições relevantes e contexto estável que afeta o controle (incluindo início do teto), ou precondições equivalentes explícitas. Na aplicação, revalidar nó/controle/tipo/unidade/faixa/opções/capacidade e a semântica do alvo; mudança incompatível encerra em conflito/recusa, nunca se aplica por hash de valor igual. Não precisa exigir hash global para comentários/parada.

2. **“Vigente” mistura configurado com valor em uso.** §2.6/GET laço/§4.4 e A.1 trabalhadores. A própria análise confirma que gerador pode subir com `--trabalhadores` e sobrepor o arquivo; processos guardam config em memória. Ler config não comprova uso corrente, mesmo com releitura ao ligar. Exemplo: arquivo diz6, processo usa20, ou arquivo já foi editado mas o processo ainda não religou. **Recomendação:** no contrato de API/tela, distinguir configurado/declarado de em uso confirmado ou não confirmado; hash e antes/depois podem comparar a configuração, desde que isso seja nomeado. Valor do arquivo não deve ser exibido como efetivo só porque é legível. Definir como o recibo confirma efeito/partida e a apresentação enquanto isso não ocorreu. A ressalva na tabela do anexo precisa virar regra do leitor e da tela.

3. **Pedido lido sem desfecho pode desaparecer do trabalho pendente; repetição da aplicação não está protegida.** §4.5 “Aviso ao maestro” suprime todo estado diferente de nova, e a rede de segurança só olha nova; §4.3 ainda manda ignorar lida como já absorvida. Para alterações, lida é intermediário, não absorção/aplicação. Se o turno acabar aí, nada no contrato manda retomá-la. Também falta checar UUID/recibo/ticket **antes** dos efeitos: passo5 cita UUID só depois da aplicação. **Recomendação:** distinguir confirmação de entrega da fila de trabalho; lida de alteração continua pendente de desfecho em retomada file-first, e recibo aguarda continua pendente de confirmar efeito. Antes de reaplicar, conferir UUID e resultado existente. Aplicação interrompida/ambígua pede reconciliação do efeito, não repetição cega (especialmente reinício de processo/relógio). Não reavisar por estado desconhecido como se fosse entrega comprovada: reconhecer os estados válidos e registrar malformação.

4. **Formato do recibo ainda não é implementável sem decisões do L2, e a regra de dono contradiz a extensão.** §4.5 frontmatter/estados; §3.1 árvore, §3.5 texto livre e abertura da §4 ainda dizem que maestro só troca estado. Definir a serialização e validação de `recibo_antes/depois` (objetos tipados para controle, texto para operações), `agora_esta`, motivo, horas e revisão: JSON em uma linha ou outro formato fechado, sem multiline ambígua no frontmatter. Validar execução do recibo igual à do pedido, tipos/unidades, valores e horas coerentes; presença não basta. Definir erros visíveis sem promover recibo inválido a aplicado. Explicitar a exceção do tipo novo nas regras gerais e na instrução do aviso ao maestro. O POST também deve dizer como valida `substitui` (mesmo laço/execução e quais operações podem substituir quais), preservando histórico sem cancelar pedido alheio.

5. **“Espera você” inclui rodada já respondida e conflito histórico resolvido.** §3.4 grupo e §2.6 lista dizem só “rodada aberta ou pedido em conflito”. Rodadas respondidas podem continuar abertas, conforme a correção já aprovada; pedidos substituídos preservam o desfecho conflito no histórico. Isso deixaria o laço esperando eternamente. **Recomendação:** usar aberta, legível e não respondida na base atual; conflito somente da execução atual, não substituído/não encerrado e ainda acionável. Terminados continuam prioritários. Registrar teste de rodada respondida/reaberta e conflito substituído como critérios do L2.

## Esclarecimentos pequenos para o texto

- A frase “retomar execução parada não é variação destas operações” precisa distinguir parada definitiva de pausa: `pedir-retomada` existe quando `pausar-retomar` é declarado; nessa capacidade é a mesma execução. Nova partida depois da parada/fim tem outro id.
- Definir precedência para origem SQLite sem linha/mais de uma linha e nulo permitido, bem como contador de onda ilegível em pedir parada após onda: não sugerir N nem validar contra zero inventado. O maestro revalida o alvo temporal antes de armar parada.
- O exemplo de parada por gate deve conservar a calibração da regra dos laços, ou declarar que é um resumo. Não apresentar “duas ondas abaixo” como descrição exaustiva se o script ainda executa calibração.

**Próximo recomendado:** corrigir contrato e anexos, devolver para revisão dirigida desses cinco pontos; só depois abrir L2. O restante da direção está aceito.
