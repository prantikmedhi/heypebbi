# Native product architecture

> **HISTORICAL REFERENCE — SUPERSEDED SCOPE.** The current decision is [local Azure onboarding](../product/LOCAL-AZURE-ONBOARDING.md), docs only until implementation is resumed. This earlier managed/full-product design is preserved as reference, not an instruction to implement its hosted services, login, billing, fixed models or full PB scope. Current requirements take precedence.

**Status: proposed implementation specification; documentation only.** No targets, actors, tests or integrations named below exist yet. [CONTRACT](../CONTRACT.md) fixes the stack and vocabulary. This document owns native module boundaries, not backend wire definitions, security policy, visual tokens or acceptance certification.

## 1. Architectural decision

Pebbi is a Swift 6, strict-concurrency, macOS 14.2+ universal native application. SwiftUI supplies views and navigation; AppKit supplies windows, menu bar, overlays, native panels and focus behavior. Home is not a browser shell. A WebView must not host app navigation, tasks, settings, approvals or the perch. System browser authentication, a browser extension, PDFKit and Quick Look are bounded integrations, not alternate app runtimes.

Use one application target, one native-messaging executable, one execution-supervisor executable and one local Swift package. Keep feature folders inside the package rather than adding a framework per feature. GRDB and Sparkle 2 are the justified native third-party dependencies; pin compatible releases and an actual stable toolchain during implementation. The runtime never launches Hermes, Codex, Claude or another paid development-agent CLI. The backend owns Azure access, authoritative metering and identity validation; the app owns task execution and local history. No conversation/file/screenshot sync server is implied.

### Proposed target tree — not existing files

The following paths define the native/browser implementation boundary. Backend, infrastructure, web pages and their tests retain their independently documented paths; moving these roots or changing the fixed stack requires parent architecture review.

```text
apps/
  macos/
    Pebbi.xcodeproj/
    Pebbi/
      App/PebbiApp.swift
      App/AppComposition.swift
      App/LifecycleController.swift
      Presentation/Home/
      Presentation/Pebbis/
      Presentation/Conversations/
      Presentation/Files/
      Presentation/Suggestions/
      Presentation/Routines/
      Presentation/Connections/
      Presentation/Settings/
      Presentation/Perch/
      Presentation/Approvals/
      Presentation/Shared/
      Resources/Assets.xcassets/
      Resources/Localizable.xcstrings
      Configuration/Pebbi.entitlements
      Configuration/Info.plist
    PebbiNativeHost/
      NativeHostMain.swift
      NativeMessagingFramer.swift
      AppSocketClient.swift
      Configuration/Info.plist
    PebbiExecutionSupervisor/
      SupervisorMain.swift
      ProcessGroupRunner.swift
      Configuration/Info.plist
    Packages/PebbiCore/
      Package.swift
      Sources/PebbiCore/
        Domain/Identifiers.swift
        Domain/States.swift
        Domain/TaskEvents.swift
        Runtime/TaskCoordinator.swift
        Runtime/PebbiExecutor.swift
        Runtime/ResourceArbiter.swift
        Runtime/ApprovalCoordinator.swift
        Runtime/ToolBroker.swift
        Runtime/RecoveryCoordinator.swift
        Runtime/RoutineScheduler.swift
        Runtime/SuggestionService.swift
        Runtime/MemoryService.swift
        Persistence/Store.swift
        Persistence/Migrations/
        Persistence/Repositories/
        Services/BackendClient.swift
        Services/IdentityService.swift
        Services/EntitlementService.swift
        Services/PermissionService.swift
        Services/ConnectionManager.swift
        Services/MCPProcessManager.swift
        Services/FileService.swift
        Services/DocumentReader.swift
        Services/NotificationService.swift
        Services/DiagnosticsService.swift
        Native/WindowCoordinator.swift
        Native/ShortcutController.swift
        Native/AXDriver.swift
        Native/TakeoverController.swift
        Native/CaptureService.swift
        Native/DisplayGeometry.swift
        Native/OverlayController.swift
        Native/VoiceController.swift
        Native/DictationController.swift
        Native/AudioEngineBridge.swift
        Browser/BrowserSessionBroker.swift
        Execution/ExecutionService.swift
      Tests/PebbiCoreTests/
    PebbiTests/
    PebbiUITests/
    NativeHostTests/
    ExecutionSupervisorTests/
  browser-extension/
    manifest.json
    src/serviceWorker.ts
    src/contentScript.ts
    src/popup.ts
    src/protocol.ts
    test/
```

`Pebbi`, `PebbiNativeHost` and `PebbiExecutionSupervisor` are signed Xcode targets; the app embeds both helpers under its bundle's helper directory. The browser manifest points to the installed native host through per-user registration. No login item, LaunchDaemon or always-on service is part of this design. Tests in this tree are required future deliverables, not a claim of present coverage.

## 2. Ownership and allowed dependencies

| Component | Sole ownership | Isolation and dependencies | Requirements |
|---|---|---|---|
| `AppComposition`, `LifecycleController` | Compose real services; startup, account partition, orderly quit; no business rules | `@MainActor`; inject services once; manages child lifetimes | PB-001, PB-002, PB-035, PB-036 |
| Presentation folders | Native views, accessibility, user drafts, visible state projection; no tool execution | `@MainActor`; consume immutable `Sendable` snapshots and send commands to coordinators | PB-004–PB-007, PB-011–PB-012, PB-026, PB-029, PB-032–PB-033 |
| Domain | IDs, canonical enums, value types, validation, tool envelopes | Pure `Sendable` values; no AppKit, network, database or clocks | PB-015–PB-017, PB-040 |
| `Store` | All local DB mutations, migrations, task and separate audio journals, authored-artifact staging, transactional projections and CAS checks | Actor wrapping GRDB `DatabasePool`; async reads/writes; SQL transaction closures contain no `await` | PB-011–PB-017, PB-025, PB-030–PB-031, PB-035 |
| `TaskCoordinator` | Ingress dedupe, task/attempt creation, per-Pebbi executor registry, cancellation routing; native management commands commit through Store, never model tools | Actor; Store is ordering authority; never execute an OS side effect here | PB-015–PB-017 |
| `PebbiExecutor` | One Pebbi's serial queue; model/tool loop and checkpoints | One actor per loaded Pebbi; Store, broker, backend, memory; child tasks retained explicitly | PB-015–PB-016, PB-028 |
| `ToolBroker` | Validate immutable intent, policy/approval, resource lease, durable dispatch, reconcile exact target | Actor; adapters expose execution functions; never accepts permission claims from the model | PB-008–PB-010, PB-017–PB-023, PB-031 |
| `ApprovalCoordinator` | Native approval requests, human decision CAS, grant matching/revocation | Actor; UI presentation crosses MainActor; canonical security policy applies | PB-017, PB-022–PB-023, PB-031 |
| `ResourceArbiter` | Fair global capacity and exclusive resource leases | Actor; sorted all-or-nothing acquisition; no DB transaction waits while holding resources | PB-016, PB-018–PB-019, PB-034, PB-038 |
| `RecoveryCoordinator` | Crash/unknown-effect reconciliation; restart safety barriers | Actor; Store, broker adapters; no blind replays | PB-017, PB-035 |
| `RoutineScheduler`, `SuggestionService` | Open-app scheduling and read-only suggestion derivation | Actors; clock injected; Store; create tasks only through coordinator after authorization | PB-024–PB-026, PB-035 |
| `MemoryService` | User-editable memory, scoped retrieval, compaction validation | Actor; Store, document reader, reasoning backend; no tool grants derived from memory | PB-013–PB-014, PB-031 |
| `BackendClient`, `IdentityService`, `EntitlementService` | Authenticated HTTP/SSE/WS; PKCE/Keychain; authoritative capability and quota projection | Actors; URLSession; AuthenticationServices bridge on MainActor; API.md is wire authority | PB-002, PB-007, PB-020, PB-027–PB-028, PB-030 |
| `WindowCoordinator`, `ShortcutController`, `OverlayController`, `TakeoverController` | Window lifecycle, input routing, overlay accessibility and explicit foreground input | `@MainActor`; do not own task state | PB-005–PB-006, PB-009, PB-018, PB-032–PB-033 |
| `AXDriver` | Bounded semantic accessibility reads/actions and stale-element validation | Dedicated serial AX worker thread/run loop; actor façade returns value snapshots, never AX objects | PB-003, PB-010, PB-018 |
| `CaptureService`, `DisplayGeometry` | Authorized ScreenCaptureKit frames; coordinate snapshots and invalidation | Actor; SCK delegate queue copies metadata/frame buffers with explicit ownership; UI geometry on MainActor | PB-008–PB-009, PB-033 |
| `VoiceController`, `DictationController`, `AudioEngineBridge` | Separate audio_operations/audio_event_receipts ownership, speech/dictation lifecycles, microphone lease and audio device handling; no task queue slot | Controller actors; dedicated audio graph serial queue and realtime-safe callback; no DB/network in callback | PB-007, PB-010, PB-034 |
| `FileService`, `DocumentReader` | User-selected roots, bounded stageTextArtifact producer, immutable artifact/hash and file versions, extraction coverage and preview leases | Actors; bounded file IO/parsing workers; PDFKit/Quick Look UI on MainActor | PB-014, PB-021, PB-030–PB-031 |
| `BrowserSessionBroker`, native host, extension | Pairing, tab selection, DOM session generation and result verification | App actor; stdio native host; MV3 service worker/content scripts; authenticated IPC | PB-019–PB-020 |
| `ConnectionManager`, `MCPProcessManager` | Catalog/configuration, OAuth state, MCP capability snapshots, process lifetime | Actors; subprocess pipes read off MainActor; Keychain injection at use, never model context | PB-022–PB-023 |
| `ExecutionService`, execution supervisor | Explicitly consented local code run, process-group containment and output quotas | Actor + signed helper; ordinary user privileges, explicitly not an OS sandbox | PB-021, PB-031, PB-035 |
| `NotificationService`, `DiagnosticsService` | Unread delivery/suppression, redacted support export and operational metrics | Actors; UserNotifications/MainActor bridges as needed; no raw transcripts in telemetry | PB-026, PB-037–PB-038 |

Dependency direction: Presentation → coordinators → domain/services → adapters/Store. Adapters cannot call model APIs or present approval UI directly. Database records are not UI observable objects. The app's process-local services can use protocols only at real substitution/testing boundaries (clock, provider transport, OS adapters); do not invent a dependency-injection framework or event bus.

## 3. Swift concurrency contract

1. Build every native target in Swift 6 mode with complete strict concurrency. No broad `@unchecked Sendable`, `nonisolated(unsafe)` or warning suppression to make platform handles cross actors. If a platform wrapper genuinely requires an audited unchecked conformance, keep it private to its owning serial worker and prove lifetime/serialization in tests.
2. Actor isolation is not transactional isolation. Any actor may reenter at `await`. Reserve a version/lease in Store before awaiting; after the await, validate attempt ID, steering revision, cancel epoch, account epoch and lease generation before publishing or performing the next side effect.
3. Only Store writes SQL. One GRDB write transaction atomically inserts journal events and updates projections. No tool/network work or inter-actor call inside that transaction. UI never reads half-written state.
4. Long work uses retained structured tasks or explicit supervised workers. Do not spawn fire-and-forget detached tasks. App exit cancels children; helpers receive channel closure. Blocking AX, file parsing and `waitpid` must not occupy MainActor or Swift cooperative executor threads indefinitely.
5. MainActor observes coalesced state snapshots; transient token/audio frames do not cause one SQL write or full view redraw each. Final text and state boundaries are durable under normal retention (private content remains memory-only); UI token deltas are provisional and labelled as such.
6. Cancellation is cooperative and does not imply an external action was undone. Keep enough dispatch metadata to reconcile even after the task's model generation is cancelled. Delayed provider frames must never revive a cancelled task or an old account's UI.

## 4. End-to-end flows and trust boundaries

### A. Typed or spoken task

Native UI/voice creates a user-origin ingress command → Store commits message + logical task/attempt + event → Pebbi queue claims attempt → retrieval produces a bounded, attributable context → backend capability/usage authorization → Responses stream supplies text/tool proposals → ToolBroker validates against local registry → native approval if required → durable immutable intent/dispatch record → one adapter executes → read-back verifier → immutable result and visible journal progress → model sees sanitized result → completion guarded against pending follow-ups.

Voice without work allocates a separate audio operation, not a queued task. Audio wire taskId/attemptId map to audioOperationId/audioAttemptId by reservation role; reasoning retains task/attempt IDs. Voice remains available while the same Pebbi runs Astra; verified result speech carries real sourceTaskId/sourceAttemptId provenance. Voice speech output may be interrupted at any point without cancelling this pipeline. Dictation is a separate focused-edit/audio-receipt pipeline that can run while the Pebbi task waits and never needs its serial slot. [AGENT-RUNTIME](AGENT-RUNTIME.md) owns their interaction, queue algorithms and cancellation semantics.

### B. Screen help or browser research

User selects scope → permission/capture or browser session lease → untrusted page/document content enters as quoted evidence → reasoning proposes explanation/action → semantic target ref revalidated → drawing or approved action → explicit read-back. Screen visibility is not permission to capture other windows or act in other tabs. A browser result, OCR passage or MCP response cannot grant access, request hidden credentials or change system instructions.

### C. Files and connections

Native open/save panel creates a bounded workspace/resource grant → versioned file/attachment metadata in Store → extraction with full-coverage manifest → local preview or selected content sent to backend with disclosure. Authored text/script starts with explicit stageTextArtifact chunks → sealed artifact/hash → createFile/replaceFile or per-run approved runCode(scriptArtifactId, expectedSha256). Staging is internal, not a target write/execution permission; private bytes/hashes remain RAM-only until native Save. Connector discovery is read-only configuration; launching a local MCP binary or accepting OAuth scopes is a distinct user action. Connectors never bypass the ToolBroker.

### D. Routines and suggestions

Typed `/pebbi` and `/routine` commands and natural-language draft reviews use the closed native management contract in AGENT-RUNTIME.md; only native Save/Enable commits, never assistant prose or a model tool. Suggestions can analyze approved read-only context; they cannot dispatch tools with side effects. Accepting a suggestion creates a normal task with provenance. Routine schedules are local and execute only while the app is open. Catch-up, overlap, retry and pause rules live in [AGENT-RUNTIME](AGENT-RUNTIME.md). Scheduled status must never suggest a server daemon is working while Quit.

## 5. Platform and account boundaries

- Developer ID distribution, hardened runtime, notarized DMG and signed Sparkle updates are required; App Store sandbox distribution is not selected. Hardened runtime, TCC, an app-level file grant and process allowlisting are four different controls, none is a general code sandbox.
- Account local partition root: `Application Support/HeyPebbi/Accounts/<accountId>/`. `accountId` is the opaque backend account UUID, never an email or Entra tenant ID. Sign-out disconnects voice/providers, cancels dispatch, revokes ephemeral leases and prevents access to that partition until the same user signs in. Preserve or delete local data only according to an explicit user choice; no cross-account memory search.
- Per-Pebbi private sessions use an in-memory content store and the minimal durable uncertain-effect journal in DATA-MODEL.md; no private chat/memory/artifact bodies are silently retained. Explicit Save is required for durable outputs.
- Keychain contains session/refresh material, backend-issued deviceToken bound to account/device, OAuth secrets and pairing keys. IdentityService sends the device token only in X-Pebbi-Device-Token on device-bound backend requests, with matching public device ID and account bearer; it is never a browser pairing key or WebSocket session token. SQLite stores references, never secret values. App-local data is not advertised as database-encrypted: GRDB SQLite here is ordinary SQLite protected by user filesystem permissions and the user's device security/FileVault configuration.
- Provider roles remain exactly `gpt-realtime-2.1`, `gpt-live-transcribe`, `gpt-6-astra`. Unsupported/deployment-missing responses mean unavailable, not fallback to a different model or a fake live fixture. The backend API and deployment audit own provider details.
- PB-039 public pages are served by the canonical backend/web boundary; native Settings opens verified HTTPS support/privacy/account/download links in the system browser. Do not create another native embedded website shell.

## 6. Failure containment and resource policy

| Failure | Containment and visible behavior |
|---|---|
| AX app hangs | Bound AX messaging timeout, invalidate refs and release leases; no repeated click; ask for app recovery or explicit takeover |
| Provider disappears / quota denied | `waitingForConnection` or `failed` with precise reason; keep local drafts, files, queue and manual UI usable; no repeated billable retries |
| Tool response missing after dispatch | Preserve uncertain effect; reconcile target before retry; display uncertainty, not success |
| DB disk full/corrupt | Fail closed before new effects; stop dispatch; offer redacted diagnostics and recoverable export; never silently reset DB |
| Helper or extension crashes | Revoke session, record unknown dispatch outcome, restart only under valid consent; no speculative resend |
| App sleeps/quits | Stop audio/capture/input, revoke interactive leases, journal interruption; no work continues behind Quit |
| File extraction partial | Coverage manifest exposes missing pages/sheets; no claim to have read the whole document |
| Slow UI or excess workload | Global bounded permits, lazy lists, coalesced deltas, cancellation; retain safety and accessibility instead of dropping checks |

Initial engineering limits are explicit tunable policy, not measured performance promises: two active reasoning attempts globally, one active **agent task** attempt per Pebbi (audio_operations are excluded), four concurrent read-only research requests per attempt, one global microphone owner, one foreground takeover owner, one mutator per AX app/browser tab/workspace resource. Waiters release expensive permits. Completed transient frame buffers are dropped rather than queued without bound. Quantitative release budgets and actual measurements belong in quality documentation; no invented benchmark is a release pass.

## 7. Invariants and verification ownership

The build must implement the detailed tests in [NATIVE-MACOS](NATIVE-MACOS.md), [AGENT-RUNTIME](AGENT-RUNTIME.md), [TOOLS](TOOLS.md), [DATA-MODEL](DATA-MODEL.md) and [BROWSER-AUTOMATION](BROWSER-AUTOMATION.md). Quality owns execution evidence and final gates.

Mandatory architecture checks:

- Dependency tests forbid Presentation importing subprocess execution/provider credential plumbing and forbid adapters bypassing ToolBroker.
- Strict-concurrency compilation and Thread Sanitizer exercises expose unsafely shared platform handles; actor tests deliberately suspend at every policy/dispatch boundary.
- Kill/relaunch at every journal boundary produces no silent repeat of a non-idempotent effect.
- Two Pebbis competing for one target cannot interleave mutations; one Pebbi's approval wait does not freeze another's read-only work.
- Denied permissions, offline providers and absent model deployments retain truthful states and a working native Home.
- Same-Pebbi voice plus reasoning and dictation during a task wait use independent owners/receipts; duplicate/late audio events cannot touch agent task FKs or consume its slot.
- Empty-workspace authored file/script succeeds only through stageTextArtifact; cancel/privacy/hash mismatches are verified before any destination write or spawn.
- Backend tokenBudget is the only native inference budget source; absent/changed budgets fail closed without dropping mandatory input.
- Fresh install on both architectures, notchless/multi-display use, VoiceOver and real Chrome/Brave native messaging require actual device evidence. A mocked adapter does not satisfy these gates.

Root changes, new privileged helpers, cloud task execution or sync, alternative model roles and alternate shells are architecture changes, not implementation conveniences. Record proposals in [DECISIONS](DECISIONS.md) and request review rather than silently modifying the fixed contract.
