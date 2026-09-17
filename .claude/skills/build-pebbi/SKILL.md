---
name: build-pebbi
description: "Use when explicitly asked to build the complete Pebbi app."
disable-model-invocation: true
---

# Build Pebbi

The user explicitly invoking this skill requests implementation of the complete documented app. Read [AGENTS.md](../../../AGENTS.md), [the master build prompt](../../../docs/agents/BUILD-PROMPT.md), [the canonical contract](../../../docs/CONTRACT.md), and [the documentation index](../../../docs/README.md), then execute that build instruction.

Do not stop at a plan, scaffold or subset. Use the specialist agents and their skills where supported, preserve all security and external-input gates, continue every unblocked task, and return evidence rather than simulated success. The user has not authorized purchases, new paid resources, public deployment or permission bypass merely by invoking the skill.
