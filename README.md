# Pebbi

**A little presence. A lot off your plate.**

Pebbi is HeyPebbi's voice-first, native macOS companion: talk through what is on your screen, get clear visual guidance, dictate into your apps, and hand work to persistent Pebbis with their own memory and files.

**Repository status: complete build specification and original brand references only. No app or backend is implemented here yet.** This is a private product repository. The selected domain is `heypebbi.com`; registration, trademark clearance and production services are separate checks.

## Start here

- [One-prompt full-app build brief](docs/agents/BUILD-PROMPT.md)
- [Complete documentation map](docs/README.md)
- [Canonical scope and shared contracts](docs/CONTRACT.md)
- [Requirements PB-001 through PB-040](docs/product/REQUIREMENTS.md)
- [Every application flow](docs/product/APP-FLOWS.md)
- [Brand system](docs/design/BRAND.md) · [visual brand board](docs/design/brand-board.html) · [design tokens](DESIGN.md)
- [Architecture](docs/engineering/ARCHITECTURE.md) · [API contract](docs/engineering/API.md) · [acceptance criteria](docs/quality/ACCEPTANCE.md)

## Design direction

An expressive pocket world of ceramic pebbles, sea-glass color, warm paper, tactile controls and small characterful motions. **Not minimalism, not a monochrome dashboard, not a reskin of HeyClicky.** Native usability, legibility and accessibility take precedence when decorative treatment competes with an interaction.

## Intended product stack

Swift 6, SwiftUI/AppKit, ScreenCaptureKit, AVAudioEngine, GRDB/SQLite and native macOS tools; a TypeScript/Fastify backend on Azure Container Apps with PostgreSQL, Key Vault, Entra External ID and Stripe; Developer ID/notarized distribution with signed Sparkle updates. [Exact boundaries and rationale](docs/engineering/TECH-STACK.md).

Locked AI roles: `gpt-realtime-2.1` for conversation, `gpt-live-transcribe` for dictation, `gpt-6-astra` for reasoning and agents. The [dated access audit](docs/engineering/AI-MODELS.md) distinguishes confirmed Astra access from deferred audio-deployment blockers. Do not confuse catalog visibility or successful test fixtures with working live inference.

## Give this to a coding agent

Start the agent at this repository root, then use this prompt:

> Implement the complete Pebbi application described in `docs/agents/BUILD-PROMPT.md`. Follow `AGENTS.md` and all normative documents indexed by `docs/README.md`. Use the repository's specialist skills and agents where supported. Complete every PB requirement with real code, error handling, tests and evidence. Continue all unblocked work without routine clarification; preserve explicit security and external-input gates. Do not stop at scaffolding, substitute mock success, or claim a production release while live gates are blocked.

In Claude Code, `/build-pebbi` loads the same entry point. Reading the prompt file alone does not authorize implementation. There is no claim that an AI can manufacture missing credentials, OS permissions, signing certificates, paid resources, or an unlimited execution context.

## Verify this documentation pack

```sh
python3 scripts/validate_docs.py
npx -y @google/design.md lint DESIGN.md
```

The Python checker covers required files, relative links, machine-readable contracts, requirement coverage, original SVG structure, agent/skill frontmatter and obvious secret leakage. Design lint covers token references and component contrast; neither proves a future app works. Future native, integration and release checks are defined in [testing](docs/quality/TESTING.md).

## Agent entry points

[AGENTS.md](AGENTS.md) is canonical. [AGENT.md](AGENT.md) is a compatibility redirect. [CLAUDE.md](CLAUDE.md) imports the canonical contract. [`.claude/README.md`](.claude/README.md) explains the portable project skills and specialist agents.

## Sources and rights

Public reference behavior is mapped in [HeyClicky coverage](docs/reference/HEYCLICKY-COVERAGE.md); [sources and boundaries](docs/reference/SOURCES.md) distinguish original design, recommendations and tested facts. No proprietary HeyClicky code or branding is included. Future use of its MIT source requires retaining the relevant notices. See [third-party notices](THIRD-PARTY-NOTICES.md) and [license](LICENSE).
