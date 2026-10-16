# Comentário para a issue openai/codex#20244 (texto novo, depois do teste do nome da conversa)

Não publicado. Fonte: `bancada-nome-conversa.md` (Sonda Codex, 2026-10-15). Destino: https://github.com/openai/codex/issues/20244

---

We verified on Windows CLI 0.161.0 that a sidecar connected to the same app-server as the native `codex --remote` TUI can call `thread/name/set` and update the footer and terminal-title OSC while idle, without a new turn. A separate app-server over the same persisted history did not update an already-open isolated local TUI, even after another turn. The shared-server route works, but requires that connection setup and replaces the conversation's useful name with status text. Please consider a dedicated externally supplied status item with refresh/stale semantics, without renaming the thread. Is there a supported equivalent for an already-open local TUI?
