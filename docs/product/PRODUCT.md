# Pebbi — product definition

> **HISTORICAL REFERENCE — SUPERSEDED SCOPE.** The current decision is [local Azure onboarding](LOCAL-AZURE-ONBOARDING.md), docs only until implementation is resumed. This earlier managed/full-product design is preserved as reference, not an instruction to implement its hosted services, login, billing, fixed models or full PB scope. Current requirements take precedence.

Status: normative product specification; documentation only. No application, live integration, hardware validation or release is represented as complete.

## Authority and reading map

The [canonical contract](../CONTRACT.md) fixes names, scope, stack and state vocabulary. [Requirements](REQUIREMENTS.md) own observable behavior, [App flows](APP-FLOWS.md) own journeys, [Information architecture](INFORMATION-ARCHITECTURE.md) owns destinations, and [Copy](COPY.md) owns interface language. Exact visual tokens belong to [DESIGN.md](../../DESIGN.md); compositions belong to [Screens](../design/SCREENS.md). Wire, persistence and tools are defined in [API](../engineering/API.md), [Data model](../engineering/DATA-MODEL.md) and [Tools](../engineering/TOOLS.md). [Acceptance](../quality/ACCEPTANCE.md) and its [coverage index](../quality/coverage.json) decide whether implementation evidence satisfies the specification.

## Promise

**Pebbi helps you understand what is on your Mac and finish work with a small team you can return to.** Speak or type; ask for an explanation, a pointed walkthrough, a draft, research, a file, or a bounded action. Every Pebbi retains its job, conversations, approved memory, workspace and routines. The user can see what is happening, why input is needed and what actually changed.

The app and default assistant are **Pebbi**. The project-facing identity is **HeyPebbi** and the selected domain is `heypebbi.com`. Persistent assistants are **Pebbis**, never disposable chat costumes. This domain selection is not evidence of registration or trademark clearance. Pebbi is explicitly AI, not a human coworker, therapist or infallible operator.

## Audience and primary jobs

| Audience | Job | Observable value |
| --- | --- | --- |
| Independent creators and knowledge workers | Move between research, documents, browser tools and desktop apps without repeatedly explaining a project | Resume the named Pebbi, inspect source material and retrieve its verified output |
| People learning unfamiliar software | Understand a specific visible control and complete a procedure | Capture a chosen scope; receive accessible, resumable guidance that verifies the target before continuing |
| People who prefer speaking or benefit from alternate input | Compose and navigate without forced voice-only interaction | Every voice command has a typed or native-control equivalent; insertion goes only to the confirmed field |
| Small-team operators working from their own Mac | Run connected tasks and recurring checks with oversight | Read-only suggestions, bounded approvals, local routines, a traceable result and visible failure recovery |

This is an individual-account desktop product, not shared team administration. Plan names do not imply multi-user workspaces.

## Product principles

1. **Personality with legibility.** Pocket-world tactility means colorful ceramic-like forms, a warm expressive desk, authored illustration and small purposeful reactions. It is not minimalism, a monochrome productivity dashboard or a reference-product reskin. Visual character must not obscure focus, status, quotas or safety decisions.
2. **Voice first, never voice required.** A keyboard, VoiceOver or quiet-room user can finish the same jobs. Stop speaking and stop a task are separate controls.
3. **Persistent identity, bounded authority.** A Pebbi can remember its job without acquiring indefinite permission to operate every app. Memory, context and grants are inspectable and separately revocable.
4. **Evidence before celebration.** A task reports `succeeded` only when its required result and any relevant external readback are verified. Partial files, pending submissions and untested code are labeled as such.
5. **Do not take the user's desk.** Background-safe native actions and selected-tab DOM tools are preferred. An action requiring real pointer movement or foreground takeover pauses for explicit approval.
6. **Local continuity, explicit cloud processing.** Conversations, files and journals stay local in the chosen architecture; approved request content goes through the authenticated backend to selected model roles. Local storage is not a promise of on-device inference.
7. **Offer useful work, do not secretly start it.** Suggestions research only opted-in read sources and become tasks only after approval. Routines execute only while Pebbi is open, with one catch-up after sleep.
8. **Finish the full product honestly.** No staged MVP substitutes for PB-001–PB-040. Missing credentials block their actual dependent checks, not unrelated implementation. Simulations never become proof of live success.

## Product system

Home is the full native workspace. The menu bar and compact top-edge perch expose quick access, voice, status and pending input without requiring a hardware notch. Each Pebbi has a profile, local workspace, conversations, memory and routines. A conversation contains messages and task references; it is not itself a task. A task can wait, run, fail or be cancelled while its conversation remains usable. An attempt is one execution of a logical task; retries preserve lineage and never overwrite earlier evidence.

Conversations hold drafts, attachments, citations, progress and results. Files is an index of managed artifacts, not an unrestricted view of the Mac. Suggestions contains source-backed proposals. Routines contains repeat-task definitions and their run histories. Connections exposes actual granted capability and connection health. Settings contains account, permissions, voice, dictation, shortcuts, privacy, appearance, usage, diagnostics and updates.

The native app owns the interaction loop, scheduling and durable local state. The authenticated backend owns identity validation, provider access, reservations and usage truth. Connectors and external apps remain separate trust domains. No background daemon survives Quit. No server route silently synchronizes local conversations, files or screenshots.

## Full scope map

| Product outcome | Requirements |
| --- | --- |
| Install, identify, onboard and reach Pebbi from any supported display | PB-001–PB-006 |
| Speak, see, guide and dictate safely | PB-007–PB-010 |
| Return to persistent assistants, conversations, memory and documents | PB-011–PB-014 |
| Execute useful work with concurrency, approval and control boundaries | PB-015–PB-023 |
| Receive suggestions, run routines and manage attention | PB-024–PB-026 |
| Understand access, preferences, privacy and ownership | PB-027–PB-031 |
| Use and trust the app across accessibility, hardware and failures | PB-032–PB-038 |
| Obtain public support and a truthfully verified release | PB-039–PB-040 |

All requirements are mandatory for complete acceptance. Capability flags may accurately expose an unavailable dependency, not silently remove a required feature from the definition of complete.

## Non-goals and explicit exclusions

- No Windows, mobile, browser-only or Linux app; no Electron, Tauri or WebView application shell.
- No dependency on Hermes, a paid development-agent subscription, a bundled coding CLI or a developer's local model proxy for end-user operation.
- No cross-device conversation/file sync, collaborative editing, organization administration or remote routine execution while the Mac app is closed.
- No continuous screen surveillance, global keystroke collection, ambient clipboard monitoring or hidden behavioral profiling for suggestions.
- No plugin that implies arbitrary background interaction is guaranteed; no remote-debugging port on an ordinary signed-in browser profile.
- No automatic purchases, payments, credential entry, bulk destructive edits, publishing or outbound messages under a standing grant. User-controlled credential/OS authorization surfaces remain manual.
- No community Skills marketplace, legacy HeyClicky data importer, copied characters, copied distinctive prose or promise that the public reference repo implements the current private product.
- No approved pricing invented from reference-site prices. Nest, Studio and Constellation have operator-configured prices and entitlements, clearly unavailable until configured.
- No claim of being offline AI, clinically qualified, universally multilingual, perfectly sandboxed, compliance-certified or production-ready without evidence.
- No application implementation, infrastructure provisioning, Git operation or paid-resource action as part of this documentation delivery.

## Default product decisions

- Onboarding is skippable except disclosures needed for the particular capability the user activates. Manual assistant setup always works without a live model.
- Create the default Pebbi and offer two editable job suggestions from the optional interview; commit additional Pebbis only after confirmation. Never fabricate a model-authored interview result when the model is disconnected.
- All names and jobs remain editable. Appearance choices come from original Pebbi assets and design tokens. Color is never the sole identity or state indicator.
- Store drafts locally per conversation and restore them after relaunch. Unsent text is never sent merely because a window closes or focus changes.
- Memory proposals require confirmation before becoming durable user facts. User-authored preferences can be saved directly. Secret-looking content is not eligible for automatic memory.
- Suggestions are off until sources and frequency are opted in. The default lookback is 72 hours, disclosed per source; unreadable or unavailable material is reported, not invented. A daily local suggestion check defaults to 09:00 in the selected timezone; the user may change or disable it.
- One running attempt per Pebbi preserves conversational ordering. Independent Pebbis may run concurrently within the configured execution budget; one interactive computer-control lease protects the user's desktop. Queue order is visible and stable.
- A routine pauses after three consecutive failed scheduled occurrences, each with bounded safe retries and an approved usage ceiling; a successful occurrence resets the streak. Time spent offline, busy or waiting for approval is not a failed run. There is no five-minute retry loop without a stop condition.
- Routine completion is silent and unread until opened. Greeting and optional interactive task sounds respect Focus, calls, screen-sharing detection and the user's quiet setting. Detection cannot guarantee knowledge of every app; Quiet mode is always available.
- Deletion, external sends and signing require actual authority. No product requirement licenses bypassing OS prompts, sign-in, paid-resource approval or provider restrictions.

## Success criteria, not invented metrics

The product succeeds when representative users can complete the journeys in [App flows](APP-FLOWS.md), recover from their unhappy paths, inspect their data and stop actions without developer intervention. Measure actual completion and recovery, focus errors, false success reports, approval bypasses, idle resource use and accessibility coverage. A false external success, unauthorized side effect, secret leak, inaccessible safety control or unbounded retry is a release blocker rather than a percentage to average away.

Latency/resource targets and device measurement conditions must be pinned in engineering and acceptance before performance signoff. Reference-vendor performance numbers are not Pebbi measurements. Unavailable audio deployments leave live voice/dictation acceptance blocked; local persistence, typed flows and independent runtime tests must still be completed.

## Research boundary

The [HeyClicky coverage audit](../reference/HEYCLICKY-COVERAGE.md) records the homepage, current changelog and MIT repository evidence inspected on 2026-09-17. It distinguishes vendor-advertised capability, documentation inspected and actual firsthand testing. This product is an original implementation with stricter scoped approvals, native interaction boundaries and its own identity. The audit is a source of coverage, not a grant to copy branding or a claim of reference-app behavior personally tested.
