import type { EngineInterface, Register } from 'claude-code'

import { lerAcoes, lerAvaliacao, lerEstado, lerRecrutas } from './analise'
import type { Acao, Estado } from './analise'

const MAESTRI = 'C:\\Users\\gustavo.delfino\\AppData\\Local\\Programs\\Maestri\\resources\\cli\\maestri.exe'
const REGRAS = 'C:\\Users\\gustavo.delfino\\.claude\\mods\\guarda-de-recrutas\\regras-do-maestro.md'

type Alvo = { nome: string; estado: Estado | null }

// Os recrutas que o comando atinge, com o estado de cada um no terminal.
async function alvos($: EngineInterface, acoes: Acao[]): Promise<Alvo[]> {
  const list = await $.process.run([MAESTRI, 'list'], { timeoutMs: 20_000 })
  const recrutas = lerRecrutas(list.stdout)
  const nomes = new Set<string>()
  for (const acao of acoes) {
    for (const nome of acao.recrutas) nomes.add(nome)
    if (acao.papel) for (const r of recrutas) if (r.papel === acao.papel) nomes.add(r.nome)
  }
  const resultado: Alvo[] = []
  for (const nome of nomes) {
    const check = await $.process.run([MAESTRI, 'check', nome], { timeoutMs: 20_000 }).catch(() => null)
    resultado.push({ nome, estado: check && check.exitCode === 0 ? lerEstado(check.stdout) : null })
  }
  return resultado
}

function descrever(alvo: Alvo): string {
  if (!alvo.estado) return `${alvo.nome}: estado desconhecido (o maestri check falhou)`
  const contexto = alvo.estado.contexto === null ? 'contexto ?' : `contexto ${alvo.estado.contexto}%`
  return alvo.estado.ocupado
    ? `${alvo.nome}: OCUPADO (${alvo.estado.sinal}), ${contexto}`
    : `${alvo.nome}: ocioso, ${contexto}`
}

async function julgar($: EngineInterface, comando: string): Promise<string | null> {
  const acoes = lerAcoes(comando)
  if (acoes.length === 0) return null

  const efeito = acoes.some(a => a.efeito === 'remove') ? 'reinicia ou remove' : 'reinicia'
  const lista = await alvos($, acoes)
  const ocupados = lista.filter(a => a.estado?.ocupado)
  const linhas = lista.length ? lista.map(a => `- ${descrever(a)}`).join('\n') : '- nenhum recruta conectado com esse papel'
  const cabeca = `guarda-de-recrutas: este comando ${efeito} o terminal destes recrutas, e a sessão deles acaba:\n${linhas}`

  if (ocupados.length)
    return `${cabeca}\n\nHá recruta no meio de um turno. Espere ele terminar; não há liberação para recruta ocupado. Antes de qualquer nova tentativa, leia ${REGRAS}.`
  if (lerAvaliacao(comando)) return null
  return `${cabeca}\n\nLeia ${REGRAS} antes de seguir. Para dar uma instrução nova, use maestri ask, não edite o papel. Se reiniciar for mesmo o certo, peça o handoff e repita o comando com "# risco-avaliado: <o que você conferiu>" no fim.`
}

export const register: Register = on => {
  for (const tool of ['Bash', 'PowerShell'] as const) {
    on('tool.call', { tool }, async ($, e, next) => {
      const motivo = await julgar($, e.command)
      return motivo ? { deny: motivo } : next(e)
    }).catch(($, e, next) => {
      if (next.called) return next(e)
      return lerAcoes(e.command).length && !lerAvaliacao(e.command)
        ? { deny: `guarda-de-recrutas: não consegui conferir o estado dos recrutas. Leia ${REGRAS}; se, avaliado o risco, ainda for o certo, repita com "# risco-avaliado: <o que você conferiu>".` }
        : next(e)
    })
  }
}
