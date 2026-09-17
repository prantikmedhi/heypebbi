---
name: pebbi-native
description: "Use when implementing Pebbi native services or agent tools."
---

# pebbi-native

Read [AGENTS.md](../../../AGENTS.md) and [the canonical contract](../../../docs/CONTRACT.md) first. This skill guides an authorized task; it does not authorize implementation by itself.

## Read for this work

- [docs/engineering/NATIVE-MACOS.md](../../../docs/engineering/NATIVE-MACOS.md)
- [docs/engineering/AGENT-RUNTIME.md](../../../docs/engineering/AGENT-RUNTIME.md)
- [docs/engineering/TOOLS.md](../../../docs/engineering/TOOLS.md)
- [docs/engineering/DATA-MODEL.md](../../../docs/engineering/DATA-MODEL.md)
- [docs/engineering/BROWSER-AUTOMATION.md](../../../docs/engineering/BROWSER-AUTOMATION.md)

## Procedure

Trace the complete user flow and callers before editing. Reuse native APIs and existing code first; introduce no framework merely for one helper. Keep UI on MainActor, audio/capture/storage off it, and mutable runtime state actor-isolated. Use the canonical task journal and state enums. Persist intent before side effects and reconcile before retry. Verify focus/window identity, display coordinates and privacy scope at execution, not only when planning. AX background semantics are capability-dependent; CGEvent fallback is an approved foreground action. Test denial, revocation, interruption, races, sleep and crash recovery. Never represent workspace path checks as a sandbox or require a personal coding CLI at runtime.

Return changed paths, actual checks, evidence and blockers. Keep shared contracts unchanged unless the coordinator approves and updates all consumers.
