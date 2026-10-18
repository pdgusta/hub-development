import { expect, test } from 'claude-code/testing'

import { lerAcoes, lerAvaliacao, lerEstado, lerRecrutas } from './analise'

const LIST = `You:
  - name: "Claude Code", maestro: true

Connected agents:
  - name: "Designer", role: "Designer de visuais"
    ⎿ agent: "Prumo"
  - name: "Prumo", role: "Revisor do portal"
    ⎿ agent: "Designer"

Connected portals (use \`maestri portal check\`):
  - name: "System design" - url: file:system-design.html`

test('acha os verbos que reiniciam ou removem', () => {
  expect(lerAcoes('maestri role edit "Designer de visuais" "a" "b"')).toEqual([
    { efeito: 'reinicia', recrutas: [], papel: 'Designer de visuais' },
  ])
  expect(lerAcoes(`maestri role write 'Revisor do portal' "x"`)[0].papel).toBe('Revisor do portal')
  expect(lerAcoes('maestri role assign "Anvil" "Outro"')[0].recrutas).toEqual(['Anvil'])
  expect(lerAcoes('maestri dismiss "Prumo"')[0]).toEqual({ efeito: 'remove', recrutas: ['Prumo'], papel: null })
  expect(lerAcoes('maestri recruit "Designer" --preset "Claude Code" --command "claude" --replace "Designer"')[0].recrutas).toEqual([
    'Designer',
  ])
  expect(lerAcoes('"$MAESTRI_CLI" dismiss "X"')[0].recrutas).toEqual(['X'])
})

test('ignora os comandos que não reiniciam', () => {
  expect(lerAcoes('maestri ask "Designer" "role edit nada"')).toEqual([])
  expect(lerAcoes('maestri role list; maestri role show "Designer de visuais"')).toEqual([])
  expect(lerAcoes('maestri recruit "Novo" --role "Revisor do portal"')).toEqual([])
})

test('lê os recrutas diretos com o papel', () => {
  expect(lerRecrutas(LIST)).toEqual([
    { nome: 'Designer', papel: 'Designer de visuais' },
    { nome: 'Prumo', papel: 'Revisor do portal' },
  ])
})

test('Claude Code no meio de um turno é ocupado', () => {
  const out = '✽ Choreographing… (24s · ↓ 602 tokens)\n────\n❯ \n────\n  Opus 5.5 │ d608 █░░░░░░░░░ 10%\n'
  expect(lerEstado(out)).toEqual({ ocupado: true, sinal: 'turno em andamento', contexto: 10 })
})

test('Codex trabalhando é ocupado', () => {
  const out = '• Working (22s • esc to interrupt)\n› Ask Codex to do anything\n  GPT-6.1-Sol medium · 80% context left\n'
  expect(lerEstado(out)).toEqual({ ocupado: true, sinal: 'turno em andamento', contexto: 20 })
})

test('subagente rodando conta como ocupado', () => {
  const out = '❯ \n  Fable 5.1 │ d608 ██░░░░░░░░ 20%\n  ● main\n  ◯ general-purpose  Grepping tickets 3m 8s\n'
  expect(lerEstado(out).sinal).toBe('subagente rodando')
})

test('prompt vazio é ocioso', () => {
  const out = 'Worked for 1m 38s\n❯ \n────\n  Fable 5.1 │ d608 ░░░░░░░░░░ 7%\n  ⏵⏵ auto mode on\n'
  expect(lerEstado(out)).toEqual({ ocupado: false, sinal: null, contexto: 7 })
})

test('avaliação curta demais não vale', () => {
  expect(lerAvaliacao('maestri dismiss "X"  # risco-avaliado: ok')).toBeNull()
  expect(lerAvaliacao('maestri dismiss "X"  # risco-avaliado: X ocioso, handoff em estado.md')).toBe(
    'X ocioso, handoff em estado.md',
  )
})
