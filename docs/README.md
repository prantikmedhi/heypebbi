# Pebbi documentation map

This is the complete specification for a future native macOS implementation. **Current artifact: documentation, formal contracts and original design references, not a working application.** Read [CONTRACT.md](CONTRACT.md) before treating any subsystem document as authoritative.

## One entry point for a build agent

[BUILD-PROMPT.md](agents/BUILD-PROMPT.md) is the full kickoff brief. [AGENTS.md](../AGENTS.md) sets repository conduct; [CLAUDE.md](../CLAUDE.md) and [project-local skills](../.claude/README.md) provide client-specific entry points. [ORCHESTRATION.md](agents/ORCHESTRATION.md) defines specialist ownership and [build-state.template.json](agents/build-state.template.json) preserves progress and external blockers across context limits.

No calendar roadmap or staged feature release is used. Every PB requirement remains in the final product contract. Missing live inputs are tracked honestly; they do not authorize mocked success or security bypass.

## Product and complete user flow

| Document | Owns |
| --- | --- |
| [PRODUCT.md](product/PRODUCT.md) | Promise, audience, principles, product boundaries and defaults |
| [REQUIREMENTS.md](product/REQUIREMENTS.md) | All PB-001 through PB-040 observable requirements, normal and failure behavior |
| [APP-FLOWS.md](product/APP-FLOWS.md) | Deterministic end-to-end journeys, transitions, cancellation and recovery |
| [INFORMATION-ARCHITECTURE.md](product/INFORMATION-ARCHITECTURE.md) | Navigation, surfaces, object relationships and focus ownership |
| [COPY.md](product/COPY.md) | Product language, permission prompts, errors, states and recovery copy |

## Brand, native UI and interaction

| Document | Owns |
| --- | --- |
| [DESIGN.md](../DESIGN.md) | Normative light/dark palette, typography, spacing and component tokens |
| [BRAND.md](design/BRAND.md) | Pebbi identity, ceramic mascot, material and composition rules |
| [SCREENS.md](design/SCREENS.md) | Every PB requirement's screen treatment and adaptive behavior |
| [COMPONENTS.md](design/COMPONENTS.md) | Controls, visual state axes and approval/takeover semantics |
| [MOTION.md](design/MOTION.md) | Interruptible motion, character expression, feedback and reduced motion |
| [ACCESSIBILITY.md](design/ACCESSIBILITY.md) | VoiceOver, keyboard, contrast, text scaling and display requirements |
| [ASSETS.md](design/ASSETS.md) | Original vector asset inventory, licensing and runtime export requirements |
| [brand-board.html](design/brand-board.html) | Static designed identity and product-composition reference; open locally in a browser |

Editable original assets: [logo](design/assets/logo-mark.svg), [monochrome mark](design/assets/logo-mark-mono.svg), [wordmark](design/assets/wordmark.svg), [app-icon reference](design/assets/app-icon-reference.svg), [ceramic mascot](design/assets/mascot-ceramic.svg), [expression sheet](design/assets/mascot-expression-sheet.svg), [pocket world](design/assets/pocket-world.svg). These are reference artwork, not signed application resources or proven trademark clearance.

## Engineering and machine-readable contracts

| Document | Owns |
| --- | --- |
| [TECH-STACK.md](engineering/TECH-STACK.md) | Fixed stack, dependency decisions and service boundaries |
| [ARCHITECTURE.md](engineering/ARCHITECTURE.md) | Proposed target tree, modules, actor ownership and system flows |
| [NATIVE-MACOS.md](engineering/NATIVE-MACOS.md) | Windows, TCC, focus, audio, capture, coordinates and OS lifecycle |
| [AGENT-RUNTIME.md](engineering/AGENT-RUNTIME.md) | Tasks, Pebbi queues, memory, follow-ups, routines and recovery |
| [TOOLS.md](engineering/TOOLS.md) | Native tool names, inputs/results, authority and side-effect handling |
| [DATA-MODEL.md](engineering/DATA-MODEL.md) | Local SQLite tables, migrations, journal and file lifecycle |
| [BROWSER-AUTOMATION.md](engineering/BROWSER-AUTOMATION.md) | Opt-in MV3 extension/native bridge, pairing, selected tabs and DOM tools |
| [API.md](engineering/API.md) | REST semantics, SSE/WebSocket sequences, auth, errors and idempotency |
| [openapi.json](engineering/openapi.json) | OpenAPI 3.1 REST schemas plus explicit WebSocket contract extensions |
| [tool-envelope.schema.json](engineering/schemas/tool-envelope.schema.json) | JSON Schema for validated local tool envelopes |
| [AI-MODELS.md](engineering/AI-MODELS.md) | Locked roles, dated audit, transport constraints and unresolved audio access |
| [SECURITY.md](engineering/SECURITY.md) | Trust boundaries, policy, prompt injection, SSRF, sensitive content and fail-closed rules |
| [CONNECTIONS.md](engineering/CONNECTIONS.md) | Built-in and custom connectors, OAuth, MCP and credential ownership |
| [BILLING.md](engineering/BILLING.md) | Plans, server-authoritative reservations/ledger and Stripe lifecycle |
| [DECISIONS.md](engineering/DECISIONS.md) | Accepted architecture decisions and rejected alternatives |
| [REVIEW-RESOLUTIONS.md](engineering/REVIEW-RESOLUTIONS.md) | Accepted integration clarifications for identity, artifacts, audio ownership and message budgets |

The model provider, local runtime and backend have different responsibilities. Native task execution is not an Azure Responses feature; a model proposes tools, trusted code authorizes and performs them. No raw cloud screenshot/conversation synchronization is part of the chosen architecture.

## Acceptance, release and operating the product

| Document | Owns |
| --- | --- |
| [ACCEPTANCE.md](quality/ACCEPTANCE.md) | Complete PB acceptance cases with explicit live/manual/hardware gates |
| [TESTING.md](quality/TESTING.md) | Test architecture, golden journeys, failure injection and resource targets |
| [coverage.json](quality/coverage.json) | Machine-readable requirements-to-flow/design/test traceability |
| [EXTERNAL-INPUTS.md](operations/EXTERNAL-INPUTS.md) | Deferred Azure deployments, identity/billing/signing prerequisites and blocker protocol |
| [RELEASE.md](operations/RELEASE.md) | Native signing, notarization, distribution, compatibility and rollback gates |
| [OPERATIONS.md](operations/OPERATIONS.md) | Local/backend recovery, incident handling, observability and change control |
| [PRIVACY-AND-DATA.md](operations/PRIVACY-AND-DATA.md) | Retention, exports, deletion, consent and publishable privacy commitments |
| [SUPPORT.md](operations/SUPPORT.md) | User-safe diagnostics, support intake and recovery guidance |

## Sources and documentation quality

- [HEYCLICKY-COVERAGE.md](reference/HEYCLICKY-COVERAGE.md): public reference evidence mapped to original Pebbi requirements.
- [SOURCES.md](reference/SOURCES.md): official references, evidence categories and uncertainty boundaries.
- [THIRD-PARTY-NOTICES.md](../THIRD-PARTY-NOTICES.md): source reuse and asset-license requirements.
- [Documentation manifest](manifest.json): explicit expected files and shared requirement roster.
- [Documentation validation record](quality/DOCUMENTATION-VALIDATION.md): checks exercised and limits of documentation-only evidence.
- [Documentation checker](../scripts/validate_docs.py): structural, link, coverage, schema-reference and hygiene checks. This checker never claims app functionality or live-provider readiness.
- [Contract regression fixtures](../scripts/validate_contracts.py): synthetic schema checks for device credentials, authored artifacts, role/budget readiness and UTF-8 message bounds; not runtime security evidence.

## Reading without losing context

The coordinator reads CONTRACT, requirements, architecture, security and acceptance, then assigns authoritative subsets to specialist agents. A UI implementer needs screens/flows/tokens, not a full provider catalog. A service engineer needs exact API/OpenAPI and metering rules, not guessed messages. Specialists record precise contracts and evidence; the coordinator reconciles them before completion.

The full pack is intentionally detailed because the owner asked an implementation agent to recover no product intent from chat history. It is a cross-linked system, not a stack of independent drafts. Change the owning document and all consumers together when an accepted decision changes.
