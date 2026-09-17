# Architecture decisions

> **HISTORICAL REFERENCE — SUPERSEDED SCOPE.** The current decision is [local Azure onboarding](../product/LOCAL-AZURE-ONBOARDING.md), docs only until implementation is resumed. This earlier managed/full-product design is preserved as reference, not an instruction to implement its hosted services, login, billing, fixed models or full PB scope. Current requirements take precedence.

**Status: documentation decisions for the proposed complete product, not implementation evidence.** [CONTRACT](../CONTRACT.md) remains authoritative. “Fixed” means fixed by that contract; “specified” means this documentation selects a compatible implementation default. A root stack, trust-boundary, model-role or scope change needs parent architecture review before implementation. No entry below authorizes cloud spending, credentials, app code, signing or repository publication during this docs-only task.

## ADR-001 — Native shell, bounded platform integrations

**Status:** fixed. **Requirements:** PB-001, PB-005–PB-006, PB-029, PB-032–PB-033, PB-036.

Use Swift 6 strict concurrency, macOS 14.2+, universal arm64/x86_64, SwiftUI + AppKit. Native controls/windows remain usable without a notch. ScreenCaptureKit, AVAudioEngine, Vision, PDFKit, Quick Look, AuthenticationServices and Keychain are platform integrations. A browser extension is not a WebView application shell. Do not replace the app with Electron, Tauri, a PWA or a web-hosted Home to simplify development.

Rationale: focus, input, audio, accessibility, permission and multi-display behavior require native ownership. Keep colorful Pocket-world tactility and original Pebbi artwork through native composition; simplicity is not monochrome minimalism. Consequence: real Mac and both-architecture verification are release obligations; cloud build output alone does not certify native behavior.

Authority: [ARCHITECTURE](ARCHITECTURE.md), [NATIVE-MACOS](NATIVE-MACOS.md).

## ADR-002 — One local runtime, no development-agent dependency

**Status:** fixed. **Requirements:** PB-007, PB-015–PB-016, PB-020–PB-028.

Native Swift actors orchestrate Responses, tools, approvals, memory and queues. End users do not need Hermes, a Codex/Claude CLI subscription or a developer LiteLLM proxy. Production inference uses the authenticated canonical backend with locked model roles. Development agents are implementation tools, not runtime components.

Rationale: product capability and billing must not depend on a separate developer account. Consequence: all runtime behavior is explicitly implemented and tested; missing voice deployments remain unavailable, not silently substituted.

## ADR-003 — Few targets, explicit ownership and actor reentrancy guards

**Status:** specified. **Requirements:** PB-015–PB-018, PB-023, PB-034–PB-038.

Use one native app, one local Swift package, signed native host and signed execution supervisor. Feature folders are not separate frameworks. MainActor owns UI; actors own services; dedicated workers isolate blocking AX/process/file operations and realtime audio callbacks.

Rationale: standard platform facilities cover the problem without a plugin framework/event bus. Actor isolation does not make a sequence atomic across awaits, so use DB CAS revisions and lease generations. Consequence: every awaited external boundary has an explicit stale-version guard; no broad unchecked Sendable workaround.

The exact proposed tree and ownership matrix live in [ARCHITECTURE](ARCHITECTURE.md). Backend paths remain backend-owned; moving native/browser roots needs coordination.

## ADR-004 — Local GRDB journal, not cloud task history

**Status:** fixed stack; specified schema. **Requirements:** PB-011–PB-017, PB-025, PB-030–PB-031, PB-035.

Use SQLite/GRDB with migrations, WAL, transactional journal/projection updates and per-account data partitions under Application Support/HeyPebbi. Local task events are the durable task authority. Preserve remote event IDs/sequences as source metadata separate from the local journal cursor. No conversation/file/screenshot sync route exists.

Rationale: interrupted local effects must be recoverable without inventing a backend task engine. Consequence: exports distinguish local content from server account/usage metadata. SQLite is not advertised as encrypted. Privacy purge is an explicit exception to ordinary append-only records; do not make deletion impossible by calling the journal immutable.

Authority: [DATA-MODEL](DATA-MODEL.md), [API](API.md), [SECURITY](SECURITY.md).

## ADR-005 — Intent/effect records are immutable; exactly-once is not assumed

**Status:** specified. **Requirements:** PB-015, PB-017–PB-023, PB-025, PB-035.

A prepared tool intent binds exact validated arguments, target/resource revision, policy, attempt and steering/cancel generations. Native approval binds its digest. Dispatch is durable before the external call. Results and reconciliations append; they do not rewrite earlier evidence.

Rationale: a network timeout or app crash cannot prove whether a side effect happened. Consequence: provider idempotency is used only where documented; AX/browser clicks, arbitrary code and generic MCP mutation are not replayed blindly. Uncertain effects create durable resource barriers across Pebbis/retries. Model prose and exit code zero alone cannot establish task success.

Authority: [TOOLS](TOOLS.md), [AGENT-RUNTIME](AGENT-RUNTIME.md).

## ADR-006 — Follow-up acceptance and completion share one transaction boundary

**Status:** specified. **Requirements:** PB-012, PB-015–PB-017.

Follow-ups carry explicit task/attempt destination and ingress dedupe ID. Store commits accepted message/inbox/revision/receipt atomically. Completion commits only with matching steering revision and empty pending inbox. A message after terminal completion becomes a linked successor task; stale retry destinations ask instead of guessing.

Rationale: a Boolean “busy” flag or actor callback order loses messages at completion. Consequence: an in-flight effect settles first; a follow-up cannot retroactively change its recipient/path. UI acknowledges the committed destination and preserves the original request.

## ADR-007 — One serial queue per Pebbi, shared resource arbitration

**Status:** specified. **Requirements:** PB-015–PB-018, PB-021, PB-025, PB-034, PB-038.

One agent task attempt occupies each Pebbi's slot, including waiting states. Separate audio operations do not consume that slot or a reasoning permit; voice can remain available while the same Pebbi runs Astra, and dictation while its task waits. Independent Pebbis can work concurrently under bounded global permits. Exclusive leases cover foreground input, app/tab mutation, workspace mutation and connector resource mutations. All-or-nothing sorted acquisition avoids nested lock deadlocks; approval waits release resource permits.

Rationale: a personal assistant's task order must be predictable while multiple assistants can work independently. Consequence: waiting behind an approval is visible and reorder/cancel is explicit; two Pebbis cannot type into the same field or interleave writes to the same target.

## ADR-008 — Speech interruption is not task cancellation

**Status:** fixed. **Requirements:** PB-007, PB-009–PB-010, PB-017, PB-034.

Playback has its own generation and stop path. Barge-in flushes audio and cancels remote speech output where supported, but does not stop unrelated work. Task cancel durably blocks new dispatch, stops owned resources and records actual/unknown effects. Dictation review/insertion is independently stateful and focus-validated.

Rationale: users need to talk over their assistant without silently destroying work. Consequence: UI labels, shortcuts, VoiceOver actions and tests distinguish Stop speaking, Stop listening, Cancel dictation and Cancel task.

## ADR-009 — AX first; CGEvent is visible takeover, never hidden background control

**Status:** fixed boundary; specified driver. **Requirements:** PB-003, PB-008–PB-010, PB-018, PB-032–PB-033.

Semantic AX actions operate only where actually supported and verified. CGEvent requires exact native takeover approval, global input lease, current target/capture geometry and interruption handling. No permission/password/payment UI automation. Capture refs and coordinate transforms carry explicit generations and lifetimes.

Rationale: macOS does not offer a universal arbitrary background-click mechanism. Consequence: some apps require manual steps; unsupported behavior is a truthful limitation, not a fallback click loop. Mixed display scales, negative origins, rotation, Spaces and stale frames are tested against observed transforms.

## ADR-010 — Authenticated MV3 selected-session browser integration

**Status:** fixed architecture; specified protocol. **Requirements:** PB-019–PB-020, PB-031, PB-035.

Chrome/Brave MV3 extension plus signed native host, exact extension-origin allowlist, verified private app IPC and user pairing. No ordinary-profile debug port, all-tab scraping, cookie copying or arbitrary model JavaScript. UUID registry handles wrap native browser IDs; document/navigation changes invalidate refs.

Rationale: DOM tools provide better target semantics than screenshot clicks without commandeering the whole profile. Consequence: site-required trusted gestures and inaccessible frames may require manual action or separate takeover. Pairing keys are Keychain-backed on the app side; extension counterpart is volatile trusted `storage.session`, never persistent browser storage. Browser restart requires pairing confirmation again. A same-user compromise remains outside this protocol's protection; release security review must verify the handshake and code-identity checks.

Authority: [BROWSER-AUTOMATION](BROWSER-AUTOMATION.md).

## ADR-011 — Controlled local code, not a pretend sandbox

**Status:** specified within canonical security policy. **Requirements:** PB-017, PB-021, PB-031, PB-035.

Use signed supervisor + explicitly reviewed immutable script + system `/bin/zsh` with a minimal environment, disposable working directory, bounded resources/output, process-group cleanup and fresh per-run `allowOnce`. No automatic installs or downloaded shell pipes; no inherited provider/connector secrets. Run only code the user has explicitly inspected and consented to execute under their ordinary macOS authority.

Rationale: workspace allowlists, process groups, hardened runtime and TCC do not isolate arbitrary code. Consequence: UI states network/files outside the workspace may still be reachable; malicious children may detach. This is not suitable for adversarial unattended execution. If a required release use case needs guaranteed confinement, keep that execution path disabled until a separately reviewed OS-enforced design is approved/tested. Never weaken this statement to pass PB-021.

Authority: [TOOLS](TOOLS.md), [SECURITY](SECURITY.md). A future VM/privileged helper/OS sandbox changes the architecture and requires parent review; this record does not authorize it.

## ADR-012 — Native file snapshots and transparent document coverage

**Status:** specified. **Requirements:** PB-013–PB-014, PB-020–PB-021, PB-030–PB-031.

File/attachment snapshots are immutable account-local artifacts. Native preview uses PDFKit, Quick Look or inert text; it does not execute HTML/scripts/macros. File commits validate roots/handles and hashes, stage on the proper volume, preserve previous versions and reconcile interruptions. Noncooperating external file writes are not claimed to be protected by an imaginary OS-wide CAS.

Rationale: previews, approvals and model evidence must refer to the same bytes. Consequence: whole-document reading has enumerated unit counts and source locators; partial parsing/OCR is visible. Legacy/unsupported formats require honest conversion/manual export rather than silent omission. OS preview caches and SSD erasure limits are disclosed.

## ADR-013 — Local FTS retrieval and attributable compaction

**Status:** specified. **Requirements:** PB-013–PB-014, PB-031, PB-038.

SQLite FTS5 retrieves authorized memories/passages. No vector service or automatic cross-Pebbi sharing is needed. Compaction stores source-linked summaries; task safety state, recent messages, approvals and pending follow-ups are not replaced by a lossy summary. Forget invalidates every derived cache before future use.

Rationale: use existing persistence and explicit provenance rather than another index/backend. Consequence: measure retrieval quality; adding embeddings later would require privacy/budget review, not a silent model dependency. Already transmitted provider context cannot be retroactively erased by local deletion.

## ADR-014 — Routines only while open, coalesced catch-up and bounded failure

**Status:** fixed lifecycle; specified recurrence/retry mechanics. **Requirements:** PB-024–PB-026, PB-035.

Local scheduler, no daemon or server routine engine. Sleep/offline/busy missed slots coalesce to one latest catch-up per routine; no closed-app backlog at launch. Persist occurrence uniqueness/watermarks before enqueue. Three consecutive failed occurrences after bounded retries pause the routine; success resets the streak. Waiting/skipped/cancelled is not failure. Every high-risk action still needs fresh approval.

Rationale: predictable resource usage and honest app lifecycle. Consequence: users see local-only scheduling in the editor; a cron-like always-on service is not secretly added for reliability. Suggestions remain read-only until accepted into a normal task.

## ADR-015 — Honest live capability and release evidence

**Status:** fixed. **Requirements:** PB-027–PB-028, PB-036–PB-040.

Selected model roles remain realtime `gpt-realtime-2.1`, dictation `gpt-live-transcribe`, reasoning `gpt-6-astra`. Historical access evidence is not current live certification. Missing deployments/identity/billing/signing/permissions are real blockers. Continue all independent implementation and testing under the one-prompt build contract, but never count fixtures as live evidence.

Rationale: the product is complete scope, not a staged MVP or a convincing demo. Consequence: no invented prices, tenant IDs, credentials, passing tests or deployed endpoints. Quality owns release acceptance; source/docs validity does not certify runtime behavior.

## ADR-016 — Explicit authored artifact producer and immutable code binding

**Status:** accepted review repair H-02/M-02. **Requirements:** PB-014, PB-017, PB-021, PB-031.

Exactly one new local tool, stageTextArtifact, accepts closed bounded UTF-8 chunks and returns native-created immutable artifact IDs/hashes. No implicit prose-to-file execution. Contiguous immutable chunks, exact retry receipts, finalization, scoped provenance and cancellation/private cleanup are specified in TOOLS.md and DATA-MODEL.md; private bytes/hashes stay in RAM until native Save. runCode binds scriptArtifactId + expectedSha256 and complete execution inputs; no independent script-version entity. Script staging or Save does not authorize code execution.

## ADR-017 — Audio accounting is independent of queued agent tasks

**Status:** accepted review repair H-03. **Requirements:** PB-007, PB-010, PB-015–PB-017, PB-027, PB-034–PB-035.

Use audio_operations/audio_event_receipts with explicit owner/attempt, cursor, reservation, lifecycle, privacy and cleanup. Only for audio roles do gateway taskId/attemptId carry audioOperationId/audioAttemptId; typed reservation owner/role controls routing. sourceTaskId/sourceAttemptId refer to a real verified result being spoken. Standalone dictation effects use audio-owned approval/effect receipt FKs, not fake queued tasks. One mic owner and one stream per operation remain; serial agent-task execution is unchanged. Stop speech is not Cancel task, crash never auto-replays audio or insertion.

## ADR-018 — Native control-plane authority and backend-delivered limits

**Status:** accepted clarification. **Requirements:** PB-002, PB-004, PB-011, PB-017, PB-025, PB-027–PB-028.

Typed/conversational management drafts feed the same native review/Save/Enable commands; no extra model permission tool. Protected approval, setup and privacy Save remain deliberate native controls, never model/voice assertions. Device credential is the backend-issued deviceToken stored in Keychain, separate from browser MAC/session keys. Native context budgeting consumes authenticated role tokenBudget and its verified estimator, not a guessed capacity; metered usage remains server authoritative. Missing audio deployments/fresh-auth/budget evidence stay honest external gates.

## Change control and verification

For a changed decision: identify affected PB IDs, explain the observed failure/requirement, enumerate invariant/security impact, add or update the tight regression test, obtain parent review where the fixed boundary changes, then update owning contract and all consumers. Do not fix a conflict by editing a lower-level adapter to bypass policy.

Before accepting this documentation into a build, check relative links, state/tool vocabularies, tool envelope/schema agreement, ownership scope, absence of credentials and the current docs-only statement. Implementation tests listed in the owning documents remain pending until actually run. No plan completion or document checker result is a release approval.
