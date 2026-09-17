---
name: pebbi-visual
description: "Use when implementing Pebbi screens, assets, or motion."
---

# pebbi-visual

Read [AGENTS.md](../../../AGENTS.md) and [the canonical contract](../../../docs/CONTRACT.md) first. This skill guides an authorized task; it does not authorize implementation by itself.

## Read for this work

- [DESIGN.md](../../../DESIGN.md)
- [docs/design/BRAND.md](../../../docs/design/BRAND.md)
- [docs/design/SCREENS.md](../../../docs/design/SCREENS.md)
- [docs/design/COMPONENTS.md](../../../docs/design/COMPONENTS.md)
- [docs/design/MOTION.md](../../../docs/design/MOTION.md)
- [docs/design/ACCESSIBILITY.md](../../../docs/design/ACCESSIBILITY.md)

## Procedure

Use Pebbi's expressive tactile identity, not a minimal monochrome productivity template. Compose each surface for its actual task: Home operates work; Settings configures; a walkthrough teaches. Implement real SwiftUI/AppKit controls and accessible semantics. Use the canonical palette and original mascot construction rather than approximate colors or emoji substitutes. Motion must begin from the current presentation state, remain interruptible and have reduced-motion equivalents. Keep colored material away from long reading surfaces where it hurts contrast. Build normal, loading, empty, unavailable, denied and error states. Verify small and large windows, notchless displays, VoiceOver, focus, text scaling and dark appearance on actual rendered UI.

Return changed paths, actual checks, evidence and blockers. Keep shared contracts unchanged unless the coordinator approves and updates all consumers.
