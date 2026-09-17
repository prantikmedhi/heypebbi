# Test strategy, golden journeys and failure injection

Status: **test specification only; nothing here reports an executed app test**. There is no app or backend implementation in this documentation repository. Fixtures, previews and the brand board cannot satisfy live or native gates. [ACCEPTANCE.md](ACCEPTANCE.md) contains the 80 requirement-level positive/negative cases; [coverage.json](coverage.json) is the complete PB-001–PB-040 traceability index. [RELEASE.md](../operations/RELEASE.md) owns launch decisions.

## Test architecture and evidence

Build automated verification alongside the eventual implementation, not as a post-build checklist. Use Swift Testing/XCTest for Swift 6 actors, native persistence and macOS UI; TypeScript tests for Node 24/Fastify 5 and contract validation; isolated PostgreSQL 17 and GRDB SQLite stores for migrations. Pin actual compatible tools when code exists. This document does not assert a project, test command, CI job or installed toolchain already exists.

Required layers:

1. **Pure logic/property tests:** state transitions; sequence ordering; grant matching and expiry; path/symlink containment; usage arithmetic using integer minor units; event deduplication; scheduler clocks/timezones; redaction. Generate invalid transitions and interleavings, not only examples.
2. **Persistence/migration tests:** fresh database, every supported upgrade path, power-loss boundaries, full disk, corrupt database, transaction rollback, index rebuild and forgotten-content invalidation. Test real SQLite through GRDB and PostgreSQL, not in-memory stand-ins alone. Verify terminal attempts are immutable and retry links are preserved.
3. **Boundary contracts:** API schemas, authorization, Entra issuer/audience/nonce/state/PKCE, SSE reconnection and task-local sequences, single-purpose voice tokens, signed Stripe webhooks, native-messaging origin/session authentication, MCP schema changes. Validate inbound and outbound payloads.
4. **Native integration/UI:** SwiftUI/AppKit accessibility, AVAudioEngine, ScreenCaptureKit, AXUIElement, Keychain and native file previews. Real CGEvent tests need explicit takeover consent in a dedicated test session; never hijack a developer's ordinary workspace.
5. **Live provider/connector:** all selected roles through Pebbi's authenticated Azure Container Apps backend. Development LiteLLM success is not production-path success. Catalog availability never establishes deployment support.
6. **Hardware/distribution:** actual supported Macs, peripherals, TCC, Spaces, signed DMG, Gatekeeper and Sparkle. Verify artifacts users receive, not a debug build with extra entitlements.
7. **Human craft/security review:** native feel, readable original Pebbi identity, correct status language, grounded research, accessible controls, privacy boundaries and safe recovery. Product review may not waive missing security evidence.

The code-review discipline for later implementation is independent review of the actual diff and security findings before merge, with tests and baseline comparison. Review credentials, command/SQL injection, deserialization, paths, authorization, telemetry and process/network bounds. Existing failing security or acceptance cases remain release blockers even if they predate a change. Documentation-only work does not run imaginary code tests or claim an independent code-review verdict.

### Evidence format

For each case preserve: `caseId`, `requirementIds`, `verificationClass`, `result` (NOT_RUN/PASS/FAIL/BLOCKED), app build/source revision, backend/config/schema/extension revisions, fixture revision, OS build, physical architecture/device, input/expected/observed assertions, redacted artifact locations, timestamp and observer. These are evidence-record fields, not application API additions. Results expire on relevant changes; RELEASE.md defines invalidation.

Use synthetic names, seeded documents, canary strings, controlled email recipients and test-owned connector resources. Keep credentials in approved secret stores. Evidence must not include raw customer screens/audio or provider keys. A controlled side effect requires a pre-read, an effect receipt and a post-read of the exact target. When the provider cannot determine whether a non-idempotent effect occurred, the correct outcome is waitingForInput or interrupted with reconciliation required, not blind retry.

Live variants start **BLOCKED** until [EXTERNAL-INPUTS.md](../operations/EXTERNAL-INPUTS.md) inputs are authorized and verified. Enabling a fixture flag records automated/preview evidence only. Missing inputs do not justify shortening the acceptance roster.

## Test assets to implement

- Long text/PDF/Office fixtures with numbered pages/sections and unique canaries at beginning, middle and end; scanned/encrypted/corrupt variants and extraction manifests. Do not infer support for a format merely because Quick Look previews it.
- Two account identities, two devices, three Pebbis with distinct workspaces, concurrent tasks with conflicting and independent resources; every authorization test includes an unauthorized counterpart.
- Controlled app with AX text fields, secure fields, unresponsive targets and changing focus; supported real apps for integration verification. A test control app is not sufficient proof of arbitrary application automation.
- Chrome and Brave profiles with the signed extension/helper, a test-owned DOM page with navigation/mutation/injection cases, unrelated tabs with exclusion canaries, and invalid native-host senders.
- Provider transport fixtures for all state/event shapes; distinct approved live model deployments. Test fixtures label themselves visibly and in evidence.
- OAuth/MCP servers with expiry, revocation, slow/hung responses, changed tool schema and hostile tool descriptions; genuine supported connections for live checks.
- Server-authoritative usage ledgers seeded with boundary values, expiring reservations and Stripe test-mode event fixtures; production price/allowance values are never invented for tests.
- Earlier signed release candidate and rollback/corrective release, migratable local store with unfinished/uncertain effects, and authorized isolated update channel.

## Golden end-to-end journeys

Each journey must be executed with the positive and relevant failure variants, from a declared initial state. Assertions refer to externally observable behavior and durable records, not model narration. Capture evidence at each checkpoint. Clear only test-owned data afterward. Core journeys must work with keyboard/VoiceOver where applicable; spoken paths additionally require hardware/live evidence.

<a id="gj-01"></a>
### GJ-01 — Install, choose agency and make a Pebbi

**Coverage:** PB-001–006, PB-011, PB-032. **Classes:** automated, manual, live, hardware.

**Preconditions:** signed candidate on a clean supported Mac; authorized Entra identity; no previous local store; notifications/mic/screen/AX initially undetermined. Seed no personal information.

1. Download the real DMG from the download page, verify the artifact/channel, install and launch from Finder under normal Gatekeeper enforcement. Observe native Pebbi UI, accurate minimum OS and no security bypass instructions.
2. Start sign-in in the system browser; cancel once and retry successfully. Assert no device/account is shown ready after cancellation, and a successful session is Keychain-backed with correct account identity.
3. Navigate the interview entirely by keyboard; edit the suggested name/job/appearance, inspect optional memory choices and create the Pebbi. Skip optional permissions. Assert one saved Pebbi/workspace and the default Pebbi named Pebbi remains available.
4. Open Home from menu bar and perch; visit all eight canonical navigation destinations. Assert meaningful empty states and no fake tasks, files or connections.
5. Invoke a microphone-dependent action, deny the prompt and use typed interaction instead. Typed local navigation must remain usable; cloud reasoning additionally requires an available authorized provider. Grant mic later through normal OS controls and observe permission state refresh without repeated prompts.
6. Quit, inspect no owned helpers/capture/routines still running, relaunch and confirm the saved profile/session treatment. Sign out and verify protected transports stop, then sign back in without duplicated Pebbis.

**Recovery variants:** interrupted interview save, cancelled sign-in, changed account, denied permissions, corrupt optional appearance asset, unsupported OS install. **Terminal oracle:** saved local identity and native navigation are usable; permission/account states match actual authority. A docs image or unsigned local launch cannot pass installation.

<a id="gj-02"></a>
### GJ-02 — Speak about one window, guide, interrupt and resume

**Coverage:** PB-005–009, PB-028, PB-031–034, PB-038. **Classes:** automated, manual, live, hardware. **Live state:** BLOCKED pending verified user-deferred realtime deployment.

**Preconditions:** signed candidate, granted mic and chosen screen scope, live `gpt-realtime-2.1` and `gpt-6-astra`, controlled two-window scene with an exclusion canary in the unselected window, visible microphone indicator.

1. Invoke the global shortcut from a normal app; identify the selected Pebbi without silently taking control of the app. Choose one window for context and begin an explicit voice turn. Record connecting/listening/thinking/speaking transitions and outbound capture scope.
2. Ask about a test-owned visible chart. Verify the response matches its values/labels and acknowledges obscured content; no excluded-window canary reaches provider payloads or explanation.
3. Request guidance to a visible control. Assert a target-bound marker plus textual/VoiceOver equivalent, no click/effect, and Next/Back/Pause/Dismiss controls. Move the target across displays; marker coordinates remain correct or the guide pauses for re-selection.
4. During spoken output, interrupt with a new utterance. Measure playback stop; old queued audio is discarded. Ask for a bounded task and verify it has its own journal/task state. Interrupt speech again: the task continues unless explicitly stopped.
5. Pause and resume guidance after a window move. Close the target and switch fullscreen Spaces; require revalidation rather than stale pointing. Stop screen sharing and speech; capture/audio buffers and indicators become inactive.
6. Repeat with typed input, VoiceOver, Reduce Motion/Transparency and a notchless display. The task and guidance meaning remain available without motion or sound.

**Recovery variants:** permission revoked mid-frame, network partition, provider unsupported-operation, quota exhaustion, Bluetooth output loss, another call, stale source frame. **Terminal oracle:** correct selected context, no leaked scope, no late audio after interruption, and independent task state. The typed path cannot pass the voice gate.

<a id="gj-03"></a>
### GJ-03 — Dictate, correct, protect focus and insert once

**Coverage:** PB-003, PB-006, PB-010, PB-029, PB-032, PB-034. **Classes:** automated, manual, live, hardware. **Live state:** BLOCKED pending verified user-deferred dictation deployment.

**Preconditions:** real `gpt-live-transcribe`, selected input device, consented target native text field, separate unrelated/secure fields and known clipboard sentinel; granted mic/AX only where necessary.

1. Start dictation from the original field using its shortcut; retain immutable target identity and show capturing/transcribing rather than a task-running label.
2. Dictate a controlled sentence with punctuation, a proper name and a correction. Verify partial/final transcript ordering; review and edit before insertion. No text reaches any target during review.
3. Deliberately focus another app and request insertion. Expect a safe refusal/review state and zero change to either field. Restore/reselect the original target and explicitly insert once; verify exact corrected text and completed state.
4. Repeat final transcript and insertion events. Assert no duplicated characters and a single insertion receipt. Cancel another dictation before insertion; the target and clipboard remain unchanged.
5. Repeat in the supported browser editor and with a secure field, lost Accessibility permission and changed clipboard. Secure fields block automation; any fallback offers explicit Copy and does not paste into an unvalidated field or clobber a newer clipboard value during restoration.
6. Switch built-in, USB and Bluetooth routes during capture; lose a device and resume deliberately. Verify no stale turn resumes, no unauthorized replacement mic is selected and recoverable text remains reviewable.

**Terminal oracle:** exact one-time insertion into the revalidated target, safe cancellation, no secret-field capture and a stopped mic. Transcription configuration acceptance without an actual audio result is a failed/blocked live path.

<a id="gj-04"></a>
### GJ-04 — Research a whole document and save a truthful artifact

**Coverage:** PB-011–015, PB-020, PB-021. **Classes:** automated, manual, live.

**Preconditions:** two Pebbis with distinct workspaces; permitted local multi-page document with canaries and a test-owned live source; live Astra; no outbound-write grants.

1. Attach the document to a new conversation, preview it and ask for full-document analysis with a final-section question. Compare extraction coverage against the complete manifest; partial extraction must name exactly what is missing.
2. Ask the Pebbi to research a related claim and separate supported facts from inference. Open every cited source and check each material claim; a blocked source yields an explicit limitation and never a fabricated citation.
3. Add a job-specific memory, inspect provenance, edit it and compact the conversation. Verify instructions, active tool receipts and unresolved work survive without cross-Pebbi context mixing.
4. Request a report inside that Pebbi's workspace. Inspect the intended path/scope, execute the permitted write, read back the artifact bytes and open native preview. Only after readback may the task say succeeded; the conversation links to that attempt and file.
5. Pin/archive/search/unarchive the conversation; restart and confirm state. Switch to the second Pebbi: no memory or workspace reassignment occurs.
6. Forget the memory canary, rebuild context and retry a read-only query. Inspect actual prompt/retrieval inputs for absence, not merely the assistant's claim that it forgot.

**Recovery variants:** corrupt/encrypted attachment, last-page extraction failure, source injection, symlink escape, insufficient disk and interrupted write. **Terminal oracle:** verifiable artifact, complete reading or exact limitation, grounded citations and durable ownership.

<a id="gj-05"></a>
### GJ-05 — Concurrent work, approval, cancellation and uncertain effects

**Coverage:** PB-015–017, PB-026, PB-035, PB-038. **Classes:** automated, manual, live, hardware.

**Preconditions:** two Pebbis, independent tasks plus a shared exclusive resource, controlled recipient/account, no previously granted outbound-message authorization, event journal logging without payload secrets.

1. Start a read-only research task and a local artifact task concurrently. Inspect task ownership/queue positions and responsive Home. Start two writes to the same resource; assert one holds the exclusive lease and the other waits.
2. Send a follow-up to one specific task while the other completes. Assert the follow-up binds to the chosen task and applies at a safe boundary; no event or answer crosses owners.
3. Propose an outbound message. Inspect exact recipient/body/account, deny it and verify no external write. Propose again, explicitly allow once, then inject a transport loss immediately after external acceptance but before the local receipt.
4. Stop other queued/running work; assert queued cancellation does not run and running cancellation records completed effects separately from pending work. Stop speech separately to demonstrate it is not task cancellation.
5. Kill/relaunch Pebbi. Active attempts first become interrupted. Reconcile the uncertain message against the exact recipient/provider before any retry; if unknown after crash, keep the interrupted attempt and durable resource barrier visible, request user input without reopening that attempt, and do not resend. Verify no duplicate effect after replaying the event.
6. Suppress notification interruption using Focus/quiet mode. Complete a task; unread is retained and a later summary links to its exact conversation/task without an alert flood.

**Terminal oracle:** one effect at most where verifiable idempotency applies, honest uncertainty otherwise, no cross-owner state, and no lost accepted queue items. This journey must include actual process termination on hardware.

<a id="gj-06"></a>
### GJ-06 — Connect, inspect a tab and act with bounded authority

**Coverage:** PB-017–019, PB-021–023. **Classes:** automated, manual, live, hardware.

**Preconditions:** authorized connector account; user-installed Chrome/Brave extension/helper; selected test tab; controlled remote HTTPS and local stdio MCP; ordinary user profile with no remote-debugging port; AX permission initially denied.

1. Open Connections, inspect a supported connector's scopes and authenticate. Execute a read, refresh/revoke the token and observe ready/expired/disconnected transitions. Queue a tool, disconnect and assert it cannot reuse credentials.
2. Install/select the browser connection and choose one tab. Read DOM and request an approved form change. Re-read exact DOM state to confirm. Navigate, close or replace that tab; stale authority is invalidated and unrelated tabs remain unread.
3. Add remote/local MCP with explicit trust and executable/argument disclosure. Inspect tool definitions, run a bounded safe tool and disconnect. Verify helper processes exit. Malicious descriptions cannot grant authority or alter the user's goal.
4. Attempt a native app action without AX permission. Follow OS recovery; use AX semantics after grant. For an incompatible control, explain that fallback affects real cursor/focus and ask for takeover. Deny once: no CGEvent is sent. Approve a bounded controlled action and verify the target result.
5. Encounter a credential/payment/system-permission screen or changed target. Stop and return control; never type secrets or grant system permission through automation. Repeat a persistent scoped grant against a fresh outbound message: fresh preview/approval is still required.
6. Quit. Assert no MCP/native helpers or hidden remote browser sessions remain executing.

**Terminal oracle:** only explicitly authorized resources are accessed, real effect readback matches preview, credentials remain protected and connection catalog claims match tested capability.

<a id="gj-07"></a>
### GJ-07 — Read-only suggestion to local routine through sleep

**Coverage:** PB-024–026, PB-035. **Classes:** automated, manual, live, hardware.

**Preconditions:** granted synthetic context, local Pebbi runtime open, permitted bounded routine operation and recorded timezone; test clock and physical sleep available.

1. Generate Suggestions and inspect source/reason/scope. Open/dismiss a card: verify zero external writes or created tasks. Approve another suggestion twice rapidly: one task is created; protected effects retain their own fresh approval.
2. Create a routine from the approved behavior; inspect trigger/timezone, next eligible run, local-only explanation and permissions. Let one occurrence run and verify its journal and result.
3. Pause then archive a routine; assert no new occurrence starts. Resume an active test routine and sleep across multiple due occurrences. Wake: at most one eligible catch-up is offered/run according to policy, not a backlog of missed effects.
4. Revoke a required permission during sleep and wake again. The routine becomes blocked and explains recovery. Expired approvals are not extended and an uncertain previous effect is reconciled before retry.
5. Quit Pebbi across another trigger and keep the Mac off/asleep. Verify no server task/routine execution occurred. Reopen and inspect the missed occurrence summary and next run. Assert that launch after Quit advances the watermark without replaying the closed-app backlog; Run now requires explicit user intent.
6. Change timezone and test daylight-saving gap/fold with virtual clocks. Due occurrence identity is deterministic and no duplicate run is created for the same local scheduled occurrence.

**Terminal oracle:** local execution only while app open, durable history and grants, one catch-up maximum, no autonomous protected side effects.

<a id="gj-08"></a>
### GJ-08 — Meter, hit a limit, export, delete and seek support

**Coverage:** PB-002, PB-012, PB-013, PB-027–028, PB-030–032, PB-037, PB-039. **Classes:** automated, manual, live.

**Preconditions:** authorized test account, approved test-mode entitlement configuration, Stripe test mode, server-authoritative usage ledger, synthetic local/server canaries and accessible public/account pages. Production money movement requires separate explicit authorization.

1. Inspect Plans/Usage: only operator-approved test configuration appears, clearly labeled as test mode. Start concurrent requests at a reservation boundary; assert accepted work has unique reservations and rejected work does not reach providers.
2. Finish one and interrupt another stream. Reconcile trusted partial usage; display reserved/consumed/available consistently. Reach a limit and see a usable local fallback plus truthful provider/quota status, not invented entitlement or alternate model.
3. Open hosted Checkout/Portal. Cancel once; no entitlement change. Complete an authorized test transaction; replay and reorder signed webhook events. Read back Stripe/server state; exactly one entitlement/ledger effect applies. Fake browser return and invalid signature do nothing.
4. Export local content to a chosen folder and account/usage content separately. Parse manifests, check counts/integrity and canary locations; no Keychain tokens or unrelated account data appears. Interrupted export never presents a partial artifact as complete.
5. Generate a support bundle, preview redaction and cancel upload. No optional data leaves the device. Approve a sanitized bundle and verify support correlation works without raw screen/audio/transcript content.
6. Delete selected local memory/history and inspect indexes/caches. Request account deletion with disclosed retention exceptions; sessions are revoked and server deletion status verified. An offline second Mac is explicitly not claimed remotely erased.
7. Repeat account/export/delete flows using keyboard and VoiceOver on native and web surfaces. Check privacy/support links and account boundaries.

**Terminal oracle:** no double metering or unauthorized entitlement, correct export boundaries, verified deletion scope and safe diagnostic consent. Unapproved production pricing keeps LG-BILLING blocked even if test-mode behavior passes.

<a id="gj-09"></a>
### GJ-09 — Deliver, update, recover and roll back a native release

**Coverage:** PB-001, PB-033, PB-036–037, PB-039–040. **Classes:** automated, manual, live, hardware.

**Preconditions:** authorized Developer ID/notarization/Sparkle keys, actual download/update endpoints, prior signed build and candidate on physical Intel/Apple Silicon Macs, synthetic local store with history and an interrupted external effect.

1. Download from the public page in a normal browser, verify version/architecture/OS disclosure, mount/install and launch without weakening Gatekeeper. Verify signature, hardened runtime, notarization/staple and bundle ID `com.heypebbi.app`.
2. Open the prior build with its real store; update through the signed Sparkle channel. Confirm exact candidate bytes, compatibility checks, preserved local data/Keychain handling and no helper left executing after Quit.
3. Try tampered artifact/feed, interrupted download and incompatible schema. The previous valid build remains usable or a clear recovery path exists; invalid payloads never launch.
4. Exercise the release rollback runbook: withdraw the faulty candidate and publish a signed compatible corrective release or approved compatible rollback. Preserve journal/reconciliation state; do not restore a stale database and replay an external effect.
5. Use perch and Home on notchless/notched/mixed-scale displays, fullscreen Spaces and display hot-unplug during update/recovery dialogs. Confirm all recovery actions remain reachable.
6. Open support/privacy/account links and inspect an actual downloaded artifact again. Collect sanitized diagnostics and complete the release evidence manifest tied to all component revisions.

**Terminal oracle:** authenticated delivered artifact, safe update/rollback, usable data and complete manifest. A compile, a notarization submission without acceptance or a screenshot of a download page is insufficient.

## Failure-injection catalog

Run these in isolated test environments with rollback/cleanup prepared. Each injection is run before a protected effect, while it is in flight and immediately after external acceptance where meaningful. Verify both positive recovery and refusal to retry when outcome is unknown. The harness must observe attempted I/O, not only displayed status.

| ID | Injection and setup | Required oracle / recovery |
| --- | --- | --- |
| <a id="fi-permissions"></a>FI-PERMISSIONS | Deny each initial TCC prompt; revoke mic, screen or AX while active; deny notifications; return from System Settings without a grant. | Zero protected calls after revocation; stop affected capture/actions; explain exact permission; unrelated typed/local use works; no prompt loop or CGEvent fallback. |
| <a id="fi-provider"></a>FI-PROVIDER | Selected deployment missing, unsupported operation, invalid credential, malformed response, timeout, 429 with Retry-After, partial stream and stale capability cache. | Affected connection/capability is unavailable/degraded/failed as canonical state permits; bounded retry only when safe; no silent substitute or fabricated result; reservation reconciliation uses trusted consumption. |
| <a id="fi-network"></a>FI-NETWORK | Drop DNS/TLS, captive portal, partition mid-SSE/WebSocket, delayed/out-of-order reconnect events, gateway restart. | No secret token in query strings; finite connect/read deadlines; local journal reconstructs by validated sequence without duplicate effects; a provider SSE generation is not replayed/resubmitted and a reused dispatched request is rejected per API; uncertain write waits for reconciliation; offline local content remains usable. |
| <a id="fi-crash"></a>FI-CRASH | Kill app before/after journal commit, after external acceptance before receipt, during migration/export, and while child process owns resource. | Durable store remains consistent; formerly active attempts become interrupted first; no auto-resend; leases/processes are reclaimed; partial artifacts are not marked complete. Corruption never silently resets data. |
| <a id="fi-duplicate"></a>FI-DUPLICATE | Replay click, task event, SSE sequence, connector callback, webhook, reservation/finalization and scheduler occurrence; reorder completion before earlier events. | Idempotency scopes retain exact prior result; no second insertion/charge/message; out-of-order gaps are buffered/refetched within bounds; mismatched payload with reused key is rejected. Unknown external result is not guessed. |
| <a id="fi-sleep"></a>FI-SLEEP | Sleep during audio/stream/effect and over multiple schedules; wake with expired identity/approval; Quit across trigger; DST gap/fold and wall-clock jump. | Audio never resumes covertly; expired authority revalidated; one eligible routine catch-up maximum; no remote execution while closed; monotonic deadlines and durable occurrence IDs prevent duplicates. |
| <a id="fi-memory"></a>FI-MEMORY | Forget/edit a memory while retrieval, queued prompts and compaction exist; inject conflicting summaries and another Pebbi's canary. | New prompts/indexes/summaries exclude forgotten/cross-scope data; active context revalidates generation/version; external already-sent content limitation disclosed; no memory-derived authority. |
| <a id="fi-queue"></a>FI-QUEUE | Burst above configured queue bound; slow tool/consumer; simultaneous conflicting resources; cancelled queued item; stuck lease owner. | Explicit backpressure before accepting overflow, bounded queues and buffers, fair progress for nonconflicting work; exactly one exclusive writer; cancellation does not execute; no lost accepted item. |
| <a id="fi-voice"></a>FI-VOICE | Barge-in at connection, thinking and speaking; replay old audio chunks; interrupt during concurrent task; stop then new turn. | Old output stops within budget and never resumes; turn identity isolates chunks; explicit task Stop is separate; mic state/status accurate; transcript treatment remains consistent with privacy settings. |
| <a id="fi-quota"></a>FI-QUOTA | Parallel reservations at boundary, expiring reservation with active stream, partial usage, forged client finalize, delayed provider accounting, upgrade/downgrade during work. | Server-authoritative ledger does not overspend or double settle; trusted finalization only; conservative pending reconciliation when cost unknown; honest UI and no unauthorized paid call. |
| <a id="fi-focus"></a>FI-FOCUS | Switch app/field between preview and effect; secure input turns on; target closes; user moves cursor during takeover. | Re-resolve authority and target; cancel/pause stale operation; no wrong-field insertion; immediate Stop; no hidden foreground fallback. |
| <a id="fi-audio"></a>FI-AUDIO | Hot-unplug mic/headphones; Bluetooth profile/sample-rate change; call claims device; output changes to speakers; device returns. | No unauthorized reroute/capture; stop or explicit recovery; no device-engine leak, repeated transcript or stale audio; selected route shown accurately. |
| <a id="fi-approval"></a>FI-APPROVAL | Expired grant, modified recipient/payload, replay allowOnce, cross-account grant, tool description claiming consent, persistent grant on protected action. | Zero effect; fresh exact preview required; grant matching covers user/app/tool/resource/expiry; policy cannot be overridden by prompt, fixture flag or build autonomy. |
| <a id="fi-display"></a>FI-DISPLAY | Mixed-DPI display move, negative screen origin, notchless display, fullscreen Space, unplug host screen, rapid reverse motion. | Safe visible placement and accessible recovery; overlays revalidate target; no capture widening or focus theft; motion stays interruptible and reduced-motion equivalent. |
| <a id="fi-browser"></a>FI-BROWSER | Stale tab/window, origin navigation, forged native sender, extension upgrade/uninstall, host crash, malicious DOM instructions. | Scope/session invalidation; exact sender authentication; zero unrelated-tab access; no ordinary profile debugging port; selected-tab recovery is explicit. |
| <a id="fi-mcp"></a>FI-MCP | Changed schemas, malformed/oversized response, hung local process, redirect to metadata/private endpoint, hostile description, OAuth revocation. | Bounded parsing/timeouts/process exit; reapproval when scope changes; no SSRF/secret leak; disconnected/failed state truthful; no shell interpolation of untrusted content. |
| <a id="fi-workspace"></a>FI-WORKSPACE | Traversal, symlink/alias swap, filename injection, attempted home/Keychain access, disk full, subprocess fork/output flood. | Containment rechecked at access; unapproved read/write/process/network refused; atomic artifact commit; bounded output and cooperative owned-child lifecycle; no sandbox claim for mere allowlisting. Adversarial detached code is unsupported without reviewed OS isolation and must not be advertised as contained. |
| <a id="fi-privacy"></a>FI-PRIVACY | Canary secrets in error/URL/output, telemetry disabled, redactor failure, deletion interrupted, backup restore, expired export link, changed account. | No optional upload/secret persistence; redactor fails closed; deletion resumes by scope; restored stores reapply tombstones before use; signed export URLs remain short-lived and account-bound. |
| <a id="fi-update"></a>FI-UPDATE | Tampered feed/artifact, wrong signing team/bundle, failed notarization, network interruption, downgrade attack, schema incompatibility. | Reject unsafe artifact without disabling checks; preserve viable signed build/data; corrective release uses verified compatibility; no journal rewind causing duplicate effects. |
| <a id="fi-memory-pressure"></a>FI-MEMORY-PRESSURE | Sustained task load, large document, OS memory pressure, slow consumer, repeated voice start/stop, unbounded tool output attempt. | Enforce resource limits, shed recomputable caches before durable state, backpressure new work, responsive cancellation and stable idle plateau; never silently discard accepted work or weaken policy. |

## Native/hardware launch matrix

Every row below is a release blocker until its required evidence exists; “built for” is not “tested on.” Record exact machine model, architecture and OS build. Use minimum supported macOS **14.2** and the then-current supported stable macOS on each architecture where Apple supplies that combination. If a latest OS no longer supports Intel, test the newest supported Intel OS as well as 14.2; record the OS support boundary rather than pretending a nonexistent combination was tested. At least one physical Intel and one physical Apple Silicon Mac are mandatory; Rosetta does not substitute for Intel hardware.

| Area | Required combinations and observations |
| --- | --- |
| Install/update | Fresh standard-user install, upgrade from oldest supported source schema, normal quarantine/Gatekeeper, clean and existing Keychain, offline first launch, interrupted Sparkle update and compatible recovery on both architectures. |
| Display/Spaces | Notched Apple Silicon built-in; notchless Intel/Apple Silicon or external; two displays mixed scale and coordinate origins; full-screen app Spaces, Mission Control transitions and display hot-unplug with perch/guidance/approval open. |
| Input/focus | Keyboard-only and pointer, registered/conflicting shortcuts, minimized/hidden targets, secure-input fields, intentional user focus changes, approved and denied CGEvent takeover. |
| Accessibility | VoiceOver essential journeys; Reduce Motion, Reduce Transparency, Increase Contrast independently/combined; light/dark, long labels and enlarged text where supported; all interactive states and error recovery. |
| Audio | Built-in mic/speakers, wired/USB audio and Bluetooth headset; route/profile switching, device loss/reconnect, call interruption, lock/sleep, permissions revoked, spoken interruption and live dictation. Record device/firmware where relevant. |
| Browser | Chrome and Brave current supported stable versions, clean install and extension/helper upgrade, user-selected tab and dedicated-window paths, normal profile without debugging port, native host auth and uninstall/reinstall. |
| Recovery | Offline/online, sleep/wake, Quit/relaunch, forced crash at effect boundary, database migration/disk-full recovery, queue/lease reclamation and corrupt-store safe mode. |
| Efficiency | Intel and Apple Silicon idle/active Instruments traces, memory-pressure tests, CPU/energy idle, voice latency and local interaction latency; thermal/power mode and network conditions recorded. |

Do not rely on undocumented access to Focus/call state. Verify permitted platform signals; expose an explicit quiet-mode override and conservative behavior when status is unknown. Do not work around unavailable OS permission by private API or TCC database modification.

## Performance and bounded-runtime acceptance targets

The following are **unmeasured acceptance targets**, not benchmark results or provider promises. They apply to the release profile and synthetic representative corpus defined in the evidence manifest. Reconcile implementation limits with [TOOLS.md](../engineering/TOOLS.md), [DATA-MODEL.md](../engineering/DATA-MODEL.md) and product requirements; a conflicting numeric requirement must be resolved explicitly before release, never silently loosened by a test runner.

| Metric | Gate target | Measurement |
| --- | --- | --- |
| Visible local acknowledgement | p95 <= 100 ms | Shortcut/button action to visible/AX state feedback; exclude external response time, not UI dispatch time. |
| Cold launch to usable Home | p95 <= 3 seconds | Normal signed install, idle test machine, persisted representative local store, no forced wait for cloud login. |
| Barge-in playback stop | p95 <= 150 ms | Physical input/explicit interruption event to last old-turn audible sample. Old chunks must remain discarded afterward. |
| Task Stop acknowledgement | p95 <= 200 ms | User Stop to cancelling feedback; remote effect quiescence measured separately and reported honestly, not claimed reversible. |
| First spoken response | p95 <= 2 seconds | End of user turn to first intelligible audio on a warm selected live session; record network RTT and region. Connection startup is a separate reported metric. |
| Idle CPU | <= 1% of one logical core average over 10 minutes | App open, no routine due, no capture or active task; include owned helper processes and exclude initial indexing warmup. |
| Idle resident memory | <= 350 MiB aggregate | Settled Home/perch plus owned helpers; record local corpus and OS; retained caches must plateau. |
| Sustained operation | No growing unbounded buffers or leaked engines/processes over a 60-minute mixed workload | Compare end-of-run settled memory with initial plateau; investigate > 10% persistent growth and require a documented bounded explanation, not a pass by average. |
| Runtime queue bounds | Every queue/buffer/subprocess has an explicit tested positive bound and timeout in canonical engineering configuration | Exercise bound, bound+1 and stalled consumer. The accepted-work journal is durable; overflow is rejected before acceptance. |
| Idle privacy/energy | Zero active mic/screen streams and zero provider calls while idle without an explicitly authorized due operation | Observe OS indicators, instrumentation and outbound requests; no polling used merely to animate status. |

Collect at least 30 samples per latency metric on each required architecture, with p50/p95/max and failures included; report cold versus warm separately. Use a documented deterministic percentile convention in the harness. For live voice collect real audio, not synthetic timing callbacks, and keep only consented redacted measurements. Failed samples are failures, not removed outliers. Any adjustment to targets needs an explicit product/engineering decision with before/after evidence.

## Completion rules

A requirement is fully verified only when both its acceptance cases and applicable shared journeys/injections/classes pass for the candidate. Manual observation cannot substitute for missing automated tests; automated checks cannot substitute for live/hardware evidence. Missing deployment/signing/identity/billing/privacy inputs keep the relevant gates BLOCKED, while independent work can continue. The final report must enumerate what passed, failed, was not run and was blocked; never say “all tests passed” when only documentation validation ran.
