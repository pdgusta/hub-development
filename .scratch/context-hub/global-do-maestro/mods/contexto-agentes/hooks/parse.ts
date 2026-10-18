// Leitura pura da saída do `maestri list` e do `maestri check <agente>`.

export function parseAgentNames(listOutput: string): string[] {
  const start = listOutput.indexOf('Connected agents:')
  if (start < 0) return []
  const end = listOutput.indexOf('Connected notes', start)
  const block = listOutput.slice(start, end < 0 ? undefined : end)
  const names: string[] = []
  for (const match of block.matchAll(/^\s*- name: "([^"]+)"/gm)) names.push(match[1])
  return names
}

const MODEL = /(Fable|Opus|Sonnet|Haiku|gpt-[\w.-]+)\s*[\d.]*/i

// Claude Code: «Opus 5.5 │ <id> ███░░ 32%» (sessão nova: sem barra = 0%).
// Copilot: «Claude Haiku 5.5 · 936K context» (sem percentual).
// Codex: «NN% context left».
export function parseUsage(checkOutput: string): { model: string; percent: number | null } {
  const lines = checkOutput.split(/\r?\n/).filter(line => line.trim() !== '')
  for (let i = lines.length - 1; i >= 0; i--) {
    const line = lines[i]
    const left = line.match(/(\d{1,3})% context left/i)
    if (left) {
      const model = line.match(MODEL)?.[0]?.trim() ?? 'Codex'
      return { model, percent: 100 - Number(left[1]) }
    }
    if (line.includes('│')) {
      const model = line.match(MODEL)?.[0]?.trim()
      if (!model) continue
      const percent = line.match(/(\d{1,3})%\s*$/)
      return { model, percent: percent ? Number(percent[1]) : 0 }
    }
    const copilot = line.match(/Claude (\w+ [\d.]+) · [\dKM]+ context/)
    if (copilot) return { model: `${copilot[1]} (Copilot)`, percent: null }
  }
  return { model: '?', percent: null }
}

// Só a sessão marcada como maestro no `maestri list` mostra o painel.
export function isMaestro(listOutput: string): boolean {
  const you = listOutput.split('Connected agents:')[0]
  return /^You:[\s\S]*maestro: true/m.test(you)
}
