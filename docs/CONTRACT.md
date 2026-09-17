# Pebbi — canonical build contract

Status: documentation and original brand assets only. No application implementation exists in this repository yet.

This contract fixes cross-document vocabulary and decisions. Every specialist document expands it, never silently changes it. Product: **Pebbi**. Project/company-facing name: **HeyPebbi**. Selected domain: `heypebbi.com` (selection is not proof of registration or trademark clearance). Bundle ID: `com.heypebbi.app`. GitHub: private `prantikmedhi/heypebbi`.

## Scope and execution intent

Specify and later implement the complete native macOS product, not an MVP or staged roadmap. No calendar-based milestones or numbered implementation phases. A later agent receives one build prompt and carries all unblocked work through implementation, tests, review and packaging. It must not stop after scaffolding or replace live integrations with convincing fake successes. Actual missing Azure deployments, identity/billing credentials, signing authority, OS permissions and paid-resource authorization remain real blockers. Continue other work and record blockers rather than repeatedly asking about routine design decisions. Never bypass security to avoid interruption.

Now: docs, machine-readable contracts, original SVG brand assets, a static HTML brand board, agent instructions and documentation validation only. No Swift app, backend service, website implementation, provisioned cloud infrastructure or real credentials in this commit.

## Product behavior

Pebbi is a personable, explicitly AI, voice-first desktop companion and a persistent team of task assistants. It explains what a user is looking at, draws guidance, dictates into the focused app, researches, creates files, operates allowed apps, connects tools, proposes useful tasks, and runs user-approved routines. It has a native Home window and a compact top-edge perch. A hardware notch is optional; menu-bar and ordinary-window paths must work on notchless/external displays. App-native controls and accessibility semantics are mandatory; do not build an Electron/Tauri/WebView shell.

Persistent assistants are called **Pebbis**. Each Pebbi has a name, job, appearance, memory, chats, a workspace and routines. The default Pebbi is named Pebbi. UI nouns: Home, Pebbis, Conversations, Files, Suggestions, Routines, Connections, Settings. A conversation is not a running task; interrupting speech is not task cancellation.

## Fixed stack and system boundaries

- macOS 14.2+ runtime; universal arm64/x86_64 release target, with hardware verification required before claiming both. Swift 6 language mode, strict concurrency; SwiftUI, AppKit, ScreenCaptureKit, AVAudioEngine, Apple Vision, PDFKit, Quick Look, UniformTypeIdentifiers, AuthenticationServices and Keychain. Use availability guards for newer SDK features. Pin an actual compatible stable Xcode/Swift toolchain when implementation starts; do not invent installed versions.
- Native persistence: SQLite via GRDB with explicit migrations; app state and task event journal remain local. Secrets only in Keychain. Local user data under `Application Support/HeyPebbi`; do not embed any developer-specific home path.
- Native agent runtime written in Swift using async/await and actors, invoking Responses and tools. No dependency on a paid Claude/Codex desktop/CLI subscription or on Hermes being installed. Development agents are not runtime dependencies.
- Own native AXUIElement driver first for semantic desktop actions. CGEvent fallback moves/affects the real foreground session and requires explicit takeover approval. Never promise arbitrary background clicks are possible. Browser work uses an opt-in Chromium MV3 extension + authenticated native-messaging helper for a user-selected tab or dedicated window; support Chrome and Brave installation flows. DOM read/action tools are preferred to screenshot clicks. No opening a remote-debugging port on the user's ordinary signed-in profile.
- Backend: Node.js 24 LTS, TypeScript strict, Fastify 5, PostgreSQL 17 with versioned SQL migrations, Azure Container Apps for HTTPS/SSE/WebSocket gateway, Azure Database for PostgreSQL, Azure Blob Storage for release/account export artifacts, Key Vault and managed identity, Azure Monitor with redaction. Provisioning is later via Bicep, never during docs-only setup. Long WebSockets must not depend on short-lived serverless functions.
- Identity: Microsoft Entra External ID, OIDC authorization-code + PKCE in system browser. Validate issuer/audience/nonce/state and authorized redirect URIs; native refresh/session material in Keychain. Actual tenant/client IDs are external inputs, not fabricated values.
- Billing: Stripe hosted Checkout and Customer Portal, signed/idempotent webhooks and a server-authoritative usage ledger. Proposed plan names Nest, Studio, Constellation. Prices and production allowances are deliberately operator-configured, not copied from HeyClicky or invented as approved pricing. Development fixtures have explicit test labels. No paid checkout until real product/price IDs and entitlements are configured.
- Distribution: Developer ID signed + notarized DMG, hardened runtime, Sparkle 2 signed update feed. App Store distribution is not the chosen channel. No bundled Apple system fonts. No background daemon that outlives Quit. Routines execute locally while Pebbi is open; one catch-up after wake, not a backlog flood.
- macOS app and backend are primary implementation deliverables. Public support/privacy/download/account pages are required but may be server-rendered Fastify pages with original Pebbi styling; do not add a React website framework merely for a few pages. Brand-board HTML in this docs repo is an identity reference, not that website.

## Locked model roles and known provider status

Selected roles, no silent substitutions:
- conversation: `gpt-realtime-2.1`;
- streaming dictation: `gpt-live-transcribe`;
- reasoning, screen analysis, orchestration, coding/research: `gpt-6-astra`.

A local authorized audit on 2026-09-17 verified Astra directly through Azure and through an existing private LiteLLM proxy. The selected realtime model failed with HTTP 400 `OperationNotSupported` on v1 and `OpperationNotSupported` on the documented classic-preview route. The dictation session accepted configuration but actual synthetic-audio transcription returned `DeploymentNotFound`. Both were catalog-visible; neither was working through the tested deployment names. Catalog marked realtime 2.1 preview and live-transcribe generally available. The user deferred resolving these Azure inputs. Public docs may differ from resource metadata; verify the actual resource again at implementation time. Do not include the real endpoint, resource name, keys, transcripts or raw local audit files here.

The production app talks to its own authenticated backend, not the developer's localhost LiteLLM. LiteLLM remains an optional developer adapter, not a requirement for end users. Runtime providers must stay explicitly disconnected when credentials/deployments are absent. Fixture transports exist only in tests and explicitly labeled previews and never satisfy live acceptance criteria.

## Shared formats and state vocabulary

JSON contracts use camelCase; `schemaVersion: 1`. IDs are UUID strings, timestamps RFC 3339 UTC, amounts integer minor units with explicit ISO currency. Never use floating-point currency. Identifiers are opaque and case-preserved. Streaming events carry `eventId`, `taskId`, monotonic task-local `sequence`, `type`, `occurredAt`, `payload`.

Task states: `queued`, `running`, `waitingForApproval`, `waitingForInput`, `waitingForConnection`, `cancelling`, `cancelled`, `succeeded`, `failed`, `interrupted`. `succeeded`, `failed`, `cancelled` are terminal for that attempt; retry creates a new attempt linked to the same logical task. App-crash recovery first marks active attempts `interrupted`; external side effects are reconciled before any retry.

Voice states: `idle`, `connecting`, `listening`, `thinking`, `speaking`, `interrupted`, `unavailable`, `failed`. Dictation states: `idle`, `capturing`, `transcribing`, `reviewing`, `inserting`, `completed`, `cancelled`, `failed`. Connection states: `disconnected`, `connecting`, `ready`, `expired`, `degraded`, `failed`. Routine states: `active`, `paused`, `blocked`, `archived`. Screens must map to these states rather than inventing synonyms in contracts.

Approval decisions: `allowOnce`, `allowForScope`, `deny`. Persistent scoped grants never cover payments, credentials, destructive bulk operations, publishing or outbound messages; those require a fresh preview and approval. Grants are keyed to user, connector/app, tool class, bounded resource and expiry. Tool allowlisting is not an OS sandbox.

## Backend route inventory (wire definitions belong in engineering/API.md)

All routes under `/v1` unless stated: `GET /healthz` (public minimal health); `GET /me`; `POST /devices`; `DELETE /devices/{deviceId}`; `GET /capabilities`; `POST /ai/responses` (SSE); `POST /voice/sessions`; WebSocket upgrade `GET /voice/stream` with Authorization session token; `POST /dictation/sessions`; WebSocket upgrade `GET /dictation/stream`; `POST /usage/reservations`; `POST /usage/reservations/{reservationId}/finalize`; `GET /usage`; `GET /billing/plans`; `POST /billing/checkout`; `POST /billing/portal`; `POST /billing/webhook` (Stripe signature instead of app bearer); `POST /account/export`; `DELETE /account`. Voice/dictation session tokens are single-purpose, short-lived and never contain the Azure key. Do not put bearer tokens in URL query strings. Finalization is trusted server-side metering; app-supplied usage counts never authorize or bill work. Backend agent-call clients may call this internal route; end-user finalization payloads are rejected.

No server route synchronizes conversations, files or raw screenshots in the chosen initial architecture. Cross-device state sync is explicitly outside this product contract. Account export includes server-held account/usage data plus an app-driven local export; distinguish both. Connector OAuth tokens remain local unless a specific authorized server operation requires one.

## Complete requirement roster

Every requirement below must have normative behavior in `product/REQUIREMENTS.md`, a user flow in `product/APP-FLOWS.md`, design treatment in `design/SCREENS.md`, and executable/manual acceptance coverage in `quality/ACCEPTANCE.md` and `quality/coverage.json`. Multiple requirements can share one documented screen or scenario, but none may disappear.

- PB-001 — Native installation, launch, update and quit.
- PB-002 — Account sign-in, sign-out and device sessions.
- PB-003 — Permission onboarding and denied/revoked recovery.
- PB-004 — Personalization interview and first Pebbis.
- PB-005 — Menu bar, top-edge perch and full Home window.
- PB-006 — Global shortcuts and focus-safe activation.
- PB-007 — Real-time spoken conversation and typed equivalent.
- PB-008 — Explicit screen capture scope and screen understanding.
- PB-009 — Drawing, pointing and resumable guided walkthroughs.
- PB-010 — Dictation, review and focus-safe insertion.
- PB-011 — Persistent Pebbi creation, editing and appearance.
- PB-012 — Conversations, search, archive, unread and pinning.
- PB-013 — Memory inspect, edit, forget and context compaction.
- PB-014 — Attachments, whole-document reading and previews.
- PB-015 — Agent task execution and truthful live progress.
- PB-016 — Concurrent Pebbis, queues and race-free follow-ups.
- PB-017 — Approval, stop, cancellation and recovery.
- PB-018 — Native desktop control and takeover boundaries.
- PB-019 — Browser DOM tools and user-selected sessions.
- PB-020 — Web research with source-grounded results.
- PB-021 — Files, workspace boundaries and code execution.
- PB-022 — Built-in connection catalog and OAuth lifecycle.
- PB-023 — Custom remote/local MCP connections.
- PB-024 — Read-only personalized suggestions and approve-to-run.
- PB-025 — Routines, local scheduling, wake and retry policy.
- PB-026 — Notifications, Focus/call suppression and unread delivery.
- PB-027 — Plans, metering, reservations and billing changes.
- PB-028 — Quota limits and graceful provider unavailability.
- PB-029 — Preferences, voice/device choice and shortcut recording.
- PB-030 — Local export, account export and deletion.
- PB-031 — Privacy controls, retention and sensitive-content boundaries.
- PB-032 — VoiceOver, keyboard, contrast and reduced motion.
- PB-033 — Multi-display, notchless, Spaces and scaling behavior.
- PB-034 — Audio devices, Bluetooth, interruption and mic recovery.
- PB-035 — Offline, sleep/wake and app-crash recovery.
- PB-036 — Secure updates, signing and release rollback.
- PB-037 — Diagnostics, support and redacted telemetry.
- PB-038 — Resource budgets, latency and idle efficiency.
- PB-039 — Support, privacy, account and download web surfaces.
- PB-040 — Complete end-to-end acceptance and honest release gating.

## Brand direction

**Pocket-world tactility:** Pebbi feels like a small collection of friendly ceramic pebbles on an expressive creative desk. Color, material, illustration, playful type and authored motion give it personality; hierarchy and native controls keep it usable. This is expressly not minimalism, a monochrome productivity clone, an indigo SaaS dashboard, or a copy of HeyClicky's characters. Choose warm cream, sea-glass teal, clay coral, lilac and butter accents with deep plum ink; exact semantic tokens belong only in root DESIGN.md. Let the brand designer settle accessible exact values. Native UI uses intentional system rounded typography; web/identity can use an OFL-licensed display face with a documented fallback. Static brand SVGs are real original reference assets, not proof of shipped application screens.

## Document ownership and precedence

1. This contract fixes scope, architecture defaults, IDs and vocabulary.
2. `product/REQUIREMENTS.md` owns observable requirements; `product/APP-FLOWS.md` owns transitions and user journeys.
3. `engineering/API.md`, `engineering/DATA-MODEL.md`, `engineering/TOOLS.md` own their respective wire, storage and tool contracts.
4. Root `DESIGN.md` owns exact tokens; design documents own composition and interaction.
5. `quality/ACCEPTANCE.md` owns verification requirements; `quality/coverage.json` is the coverage index.
6. Root `AGENTS.md` owns build-agent conduct. Singular `AGENT.md` redirects to it. `CLAUDE.md` and `.claude` specialize without changing product requirements.

If documents conflict, fix the lower-precedence file and update cross-references. Never resolve a conflict by silently reducing scope. New decisions go in `engineering/DECISIONS.md` with rationale and affected requirements.
