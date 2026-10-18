import { expect, test } from 'claude-code/testing'

import { isMaestro, parseAgentNames, parseUsage } from './parse'

const LIST = `You:
  - name: "Claude Code", maestro: true

Connected agents:
  - name: "Pauta", role: "Escrivao TRF3"
    ⎿ agent: "Atlas"
  - name: "Atlas", role: "Analista Intune TRF3"

Connected notes (use \`maestri note read/write/edit\`):
  - name: "Roteiro — Perfil consolidado TRF3"`

test('lê só os agentes conectados', () => {
  expect(parseAgentNames(LIST)).toEqual(['Pauta', 'Atlas'])
})

test('lê o percentual do Claude Code', () => {
  const out = '❯ \n───\n  Opus 5.5 │ a997 ███░░░░░░░ 32%\n  ⏵⏵ auto mode on\n'
  expect(parseUsage(out)).toEqual({ model: 'Opus 5.5', percent: 32 })
})

test('sessão nova do Claude Code conta 0%', () => {
  expect(parseUsage('  Haiku 5.5 │ 5f23d952\n  ⏵⏵ auto mode on\n')).toEqual({ model: 'Haiku 5.5', percent: 0 })
})

test('Copilot fica sem percentual', () => {
  const out = ' ← open sidebar · Interactive   Claude Haiku 5.5 · 936K context\n'
  expect(parseUsage(out)).toEqual({ model: 'Haiku 5.5 (Copilot)', percent: null })
})

test('Codex converte o que resta em uso', () => {
  expect(parseUsage('  gpt-6-astra medium · 72% context left\n').percent).toBe(28)
})

test('reconhece o maestro', () => {
  expect(isMaestro(LIST)).toBe(true)
  expect(isMaestro('You:\n  - name: "Atlas", role: "Analista"\n\nConnected agents:\n  - name: "Pauta"')).toBe(false)
  expect(isMaestro('')).toBe(false)
})
