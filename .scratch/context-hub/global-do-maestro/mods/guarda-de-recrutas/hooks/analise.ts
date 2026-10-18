// Leitura pura: o comando que reinicia ou remove recrutas, e o estado deles no `maestri list` e no `maestri check`.

export type Acao = {
  // O que o comando faz com os terminais, em palavras.
  efeito: 'reinicia' | 'remove'
  // Os nomes dos recrutas atingidos, ou o papel cujos terminais todos são atingidos.
  recrutas: string[]
  papel: string | null
}

const CLI = String.raw`(?:maestri(?:\.exe)?|"?\$MAESTRI_CLI"?|"[^"]*maestri(?:\.exe)?")`
const ARG = String.raw`(?:"([^"]+)"|'([^']+)')`

function arg(m: RegExpMatchArray, i: number): string {
  return m[i] ?? m[i + 1]
}

// Acha no comando um verbo do Maestri que reinicia (role edit/write/assign, recruit --replace) ou remove (dismiss).
export function lerAcoes(comando: string): Acao[] {
  const acoes: Acao[] = []
  for (const m of comando.matchAll(new RegExp(`${CLI}\\s+role\\s+(?:edit|write)\\s+${ARG}`, 'g')))
    acoes.push({ efeito: 'reinicia', recrutas: [], papel: arg(m, 1) })
  for (const m of comando.matchAll(new RegExp(`${CLI}\\s+role\\s+assign\\s+${ARG}`, 'g')))
    acoes.push({ efeito: 'reinicia', recrutas: [arg(m, 1)], papel: null })
  for (const m of comando.matchAll(new RegExp(`${CLI}\\s+dismiss\\s+${ARG}`, 'g')))
    acoes.push({ efeito: 'remove', recrutas: [arg(m, 1)], papel: null })
  for (const m of comando.matchAll(new RegExp(`${CLI}\\s+recruit\\b[^\\n;&|]*--replace\\s+${ARG}`, 'g')))
    acoes.push({ efeito: 'reinicia', recrutas: [arg(m, 1)], papel: null })
  return acoes
}

// Os recrutas diretos do `maestri list`, com o papel de cada um.
export function lerRecrutas(saidaList: string): { nome: string; papel: string | null }[] {
  const inicio = saidaList.indexOf('Connected agents:')
  if (inicio < 0) return []
  const fim = saidaList.search(/\n(?:Connected (?:notes|portals)|$)/)
  const bloco = saidaList.slice(inicio, fim > inicio ? fim : undefined)
  const recrutas: { nome: string; papel: string | null }[] = []
  for (const m of bloco.matchAll(/^ {2}- name: "([^"]+)"(?:, role: "([^"]+)")?/gm))
    recrutas.push({ nome: m[1], papel: m[2] ?? null })
  return recrutas
}

export type Estado = {
  ocupado: boolean
  // Por que parece ocupado, em palavras.
  sinal: string | null
  contexto: number | null
}

const OCUPADO: [RegExp, string][] = [
  [/esc to interrupt/i, 'turno em andamento'],
  [/…\s*\(\d+[smh]/, 'turno em andamento'],
  [/Running \d+ (?:shell )?commands?/i, 'comando rodando'],
  [/^\s*◯ \S+/m, 'subagente rodando'],
  [/Press up to edit queued messages/i, 'mensagem na fila'],
]

// O fim do terminal de um recruta: se está no meio de um turno e quanto de contexto já usou.
export function lerEstado(saidaCheck: string): Estado {
  const linhas = saidaCheck.split(/\r?\n/).filter(l => l.trim() !== '')
  const fim = linhas.slice(-25).join('\n')
  const achado = OCUPADO.find(([re]) => re.test(fim))
  let contexto: number | null = null
  for (let i = linhas.length - 1; i >= 0 && contexto === null; i--) {
    const esquerda = linhas[i].match(/(\d{1,3})% context left/i)
    if (esquerda) contexto = 100 - Number(esquerda[1])
    else if (linhas[i].includes('│')) {
      const pct = linhas[i].match(/(\d{1,3})%\s*$/)
      if (pct) contexto = Number(pct[1])
    }
  }
  return { ocupado: Boolean(achado), sinal: achado ? achado[1] : null, contexto }
}

// A avaliação de risco escrita pelo modelo no próprio comando, como comentário.
export function lerAvaliacao(comando: string): string | null {
  const m = comando.match(/#\s*risco-avaliado:\s*(.+)$/m)
  const texto = m?.[1]?.trim() ?? ''
  return texto.length >= 15 ? texto : null
}
