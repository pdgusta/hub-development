"""Células (lente x tipo x formulação) e o prompt de cada chamada. Os modelos só respondem; o script grava."""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

LENTES = {
    "gustavo-dia-a-dia": "o Gustavo no dia a dia: o dono do hub, que escreve e lê notas no Obsidian, pede coisas aos "
                         "agentes e alterna entre as duas máquinas",
    "agente-novo": "um agente de código (Claude Code, Codex ou Copilot) que acabou de abrir uma sessão no hub e não sabe "
                   "nada do que aconteceu antes",
    "maestro": "o maestro do Maestri: o agente que monta e conduz uma equipe de recrutas e usa o acervo do maestro",
    "outro-par": "a outra máquina (o outro par): o que ela vê, recebe e faz quando esta máquina muda alguma coisa, ou "
                 "quando ela própria muda algo",
    "cliente": "um cliente: um sandbox ou outro computador sem cópia própria, que usa o hub através de um par",
    "falhas-divergencia": "as falhas e a divergência: o que acontece quando algo quebra, para, colide ou fica para trás",
    "seguranca-dado-cliente": "a segurança e o dado de cliente: quem pode ver e gravar o quê, chaves, rede entre as "
                              "máquinas, iniciativas de cliente",
    "responsabilidade": "quem é responsável por quê: quem é dono de cada peça, quem a aciona, quem a lê e quem só a vê",
    "grupos-onde-vive": "os grupos lógicos e onde cada coisa vive: a que grupo cada peça pertence (pode ser mais de um) "
                        "e se ela vive na máquina, dentro da sessão do agente ou fora",
    "vida-da-nota": "a vida de uma nota: como ela nasce, muda, viaja entre as máquinas, é encontrada e é arquivada",
    "leitor-novo": "um leitor que nunca viu o hub e quer entender para que ele serve e como as peças se encaixam",
    "construtor": "quem vai construir o hub: a pessoa ou o agente que vai instalar, ligar e testar cada peça",
}

TIPOS = {
    "se-x": 'perguntas do tipo "Se X, o que acontece?"',
    "relacao": 'perguntas do tipo "Qual a relação entre X e Y?"',
    "responsavel": 'perguntas do tipo "Quem é responsável por X?"',
    "grupo": 'perguntas do tipo "X faz parte do grupo de Y?"',
    "onde-vive": 'perguntas do tipo "Onde X vive?"',
    "quem-usa": 'perguntas do tipo "Quem vê ou usa X?"',
    "o-que-nao-faz": 'perguntas do tipo "O que X não faz?"',
    "ordem": 'perguntas do tipo "Em que ordem acontece X?"',
    "falha": 'perguntas do tipo "E se X falhar?"',
    "quando": 'perguntas do tipo "Quando X acontece?"',
    "por-que": 'perguntas do tipo "Por que X existe?"',
    "diferenca": 'perguntas do tipo "O que muda entre X e Y?"',
}

FORMULACOES = {
    "pratica": "Pense em situações concretas do dia a dia dessa lente e pergunte com as palavras simples que essa "
               "pessoa usaria (\"edito uma nota\", não \"gravo na vista Markdown\").",
    "borda": "Procure casos de borda: duas peças ao mesmo tempo, uma peça desligada, algo que pode dar errado, algo que "
             "o resumo não deixa claro ou que ainda não está decidido.",
}

SEMENTES = [
    "Se o Gustavo editar um arquivo do context hub (no Obsidian ou direto no disco), o que acontece?",
    "Se um agente novo iniciar a sessão no context hub, o que acontece?",
    "Se um maestro novo iniciar a sessão no context hub, o que acontece?",
    "Se o Gustavo pede a um agente uma leitura, alteração ou remoção de arquivo, o que acontece?",
    "Se o outro par altera um arquivo, o que acontece?",
]


def resumo():
    with open(os.path.join(AQUI, "resumo-neutro.md"), encoding="utf-8") as f:
        return f.read().strip()


def celulas():
    return [f"{l}|{t}|{f}" for l in LENTES for t in TIPOS for f in FORMULACOES]


def montar_prompt(celula, ja_temos=()):
    lente, tipo, form = celula.split("|")
    exemplos = "\n".join(f"- {s}" for s in SEMENTES)
    partes = [
        "Você ajuda a montar um banco de PERGUNTAS sobre um sistema chamado context hub. Você escreve só perguntas; "
        "não responda a nenhuma delas. As perguntas vão servir para testar se uma descrição do hub é completa.",
        "## O hub\n\n" + resumo(),
        f"## Sua tarefa\n\nLente: {LENTES[lente]}.\n\nEscreva de 8 a 15 {TIPOS[tipo]}, como alguém dessa lente "
        f"perguntaria. {FORMULACOES[form]}",
        "Exemplos do tom, escritos pelo dono do hub (não os repita, são de outro tipo e lente):\n" + exemplos,
    ]
    if ja_temos:
        partes.append("Já temos estas perguntas nesta lente e tipo; escreva perguntas DIFERENTES delas, sobre outras "
                      "peças, situações ou combinações:\n" + "\n".join(f"- {q}" for q in ja_temos))
    partes.append(
        "Regras:\n"
        "- Escreva em português do Brasil.\n"
        "- Uma pergunta por item, terminando em \"?\"; nada de duas perguntas no mesmo item.\n"
        "- Cite peças e atores pelo nome que estão no resumo, ou com palavras do dia a dia.\n"
        "- Inclua perguntas difíceis: casos de borda, falhas, o que não está decidido.\n"
        "- Iniciativas de cliente aparecem só pelo nome da iniciativa; nada de nomes de pessoas ou e-mails.\n"
        "- Nada de códigos internos (como T2, C3, R18).\n\n"
        "Responda SÓ com um objeto JSON, sem texto antes ou depois, neste formato:\n"
        '{"perguntas": [{"pergunta": "...?", "tipo": "' + tipo + '", "lente": "' + lente + '", '
        '"cita": ["nomes de peças ou atores citados na pergunta"]}]}')
    return "\n\n".join(partes)
