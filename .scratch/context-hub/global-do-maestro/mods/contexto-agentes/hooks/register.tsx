import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { AgentUsage, Snapshot } from '../types'
import { isMaestro, parseAgentNames, parseUsage } from './parse'

const PANE = 'contexto-agentes'
const LIMIT = 40
const PERIOD_MS = 60_000
const MAESTRI = 'C:\\Users\\gustavo.delfino\\AppData\\Local\\Programs\\Maestri\\resources\\cli\\maestri.exe'

const snapshot = atom({ plugin: 'contexto-agentes', key: 'snapshot' } as const, {
  agents: [],
  updatedAt: '',
  error: null,
} as Snapshot)

function bar(percent: number): string {
  const filled = Math.min(10, Math.round(percent / 10))
  return '█'.repeat(filled) + '░'.repeat(10 - filled)
}

let busy = false

async function refresh($: EngineInterface) {
  if (busy) return
  busy = true
  try {
    const list = await $.process.run([MAESTRI, 'list'], { timeoutMs: 20_000 })
    const names = parseAgentNames(list.stdout)
    const agents: AgentUsage[] = []
    for (const name of names) {
      const check = await $.process.run([MAESTRI, 'check', name], { timeoutMs: 20_000 })
      agents.push({ name, ...parseUsage(check.stdout) })
    }
    const now = new Date()
    const updatedAt = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
    await update($, snapshot, () => ({ agents, updatedAt, error: null }))
    const over = agents.filter(a => a.percent !== null && a.percent >= LIMIT)
    $.ui.status(over.length ? `contexto ≥${LIMIT}%: ${over.map(a => a.name).join(', ')}` : undefined)
  } catch (err) {
    await update($, snapshot, s => ({ ...s, error: String(err).slice(0, 120) }))
  } finally {
    busy = false
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const who = await $.process.run([MAESTRI, 'list'], { timeoutMs: 20_000 }).catch(() => null)
    if (!who || !isMaestro(who.stdout)) return next(e)

    await $.command.register({
      name: 'contexto',
      description: 'Abre o painel com o contexto de cada agente do canvas',
    })
    void $.ui.open({ id: PANE, title: 'Contexto dos agentes' })
    void refresh($)
    $.clock.every(PERIOD_MS, () => refresh($))

    return next(e)
  })

  on('command.run', { command: 'contexto' }, async $ => {
    await $.ui.open({ id: PANE, title: 'Contexto dos agentes' })
    void refresh($)

    return { text: 'Painel de contexto aberto.' }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const snap = await read($, snapshot)

    return (
      <Box flexDirection="column">
        {snap.agents.length === 0 && <Text dimColor>Lendo os agentes…</Text>}
        {snap.agents.map(agent => {
          const pct = agent.percent
          const color = pct === null ? 'inactive' : pct >= LIMIT ? 'error' : pct >= 30 ? 'warning' : 'success'
          return (
            <Text>
              <Text bold>{agent.name.padEnd(9)}</Text>
              <Text color={color}>{pct === null ? '    —     ' : bar(pct)} {pct === null ? '  ?' : `${String(pct).padStart(3)}%`}</Text>
              <Text dimColor> {agent.model}</Text>
            </Text>
          )
        })}
        <Text dimColor>
          {snap.updatedAt ? `atualizado ${snap.updatedAt} · a cada 1 min · limite ${LIMIT}%` : ''}
        </Text>
        {snap.error && <Text color="error">{snap.error}</Text>}
      </Box>
    )
  })
}
