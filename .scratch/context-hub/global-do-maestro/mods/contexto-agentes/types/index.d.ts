export type AgentUsage = {
  name: string
  model: string
  percent: number | null
}

export type Snapshot = {
  agents: AgentUsage[]
  updatedAt: string
  error: string | null
}

declare module 'claude-code' {
  interface PluginState {
    'contexto-agentes': { snapshot: Snapshot }
  }
}
