# Acceptance contract

> **HISTORICAL REFERENCE — SUPERSEDED SCOPE.** The current decision is [local Azure onboarding](../product/LOCAL-AZURE-ONBOARDING.md), docs only until implementation is resumed. This earlier managed/full-product design is preserved as reference, not an instruction to implement its hosted services, login, billing, fixed models or full PB scope. Current requirements take precedence.

Status: **SPECIFIED, NOT EXECUTED**. This repository contains documentation and original brand references, not an application. This file defines future pass/fail obligations. No entry below is evidence of a working feature. All live launch gates are **BLOCKED** until the actual external inputs and release-candidate behavior are verified. Astra was audited working in the limited context recorded in [CONTRACT](../CONTRACT.md); that is not production readiness. Missing Azure realtime and dictation deployments are explicitly **USER-DEFERRED**, not permission to substitute another model.

## Authority and use

[Requirements](../product/REQUIREMENTS.md) owns behavior, [app flows](../product/APP-FLOWS.md) owns journeys, [screens](../design/SCREENS.md) and [DESIGN.md](../../DESIGN.md) own presentation. [API](../engineering/API.md), [data model](../engineering/DATA-MODEL.md) and [tools](../engineering/TOOLS.md) own wire/storage/action details. These tests enforce those contracts without redefining them. Resolve conflicts by the precedence in [CONTRACT](../CONTRACT.md), never by weakening safety or reducing scope.

[coverage.json](coverage.json) contains exactly the 40 canonical requirement IDs, verbatim titles and repository-relative links. Its testCases refer to test specifications, not existing test implementations. Every requirement needs both its P (positive) and N (negative) case and the linked shared scenarios. P or N may contain several assertions; all must pass. Execute each negative injection in isolation as well as the combined journeys.

## Verification classes and result states

- **automated**: executable deterministic unit, integration, contract, property/race, migration and UI checks. Use isolated test accounts, synthetic files and explicitly labeled fixtures. Fixtures never certify provider availability or hardware behavior.
- **manual**: a named human records expected/observed user behavior, native interaction craft, recovery clarity and evidence. A generated screenshot is not an interaction test.
- **live**: authorized real service/account, deployment, identity, billing, source or release endpoint on the actual intended path. Record deployment/configuration version privately; never commit keys, private endpoint URLs or raw user data.
- **hardware**: physical supported Macs and peripherals exercising OS permissions, audio, display, energy and distribution behavior. Emulation and compile targets cannot clear this class.

Result states: NOT_RUN, PASS, FAIL, BLOCKED. BLOCKED includes a reason, owner and exact missing input; NOT_RUN includes no claimed observation. A case passes only when all its required assertions and classes have evidence for the candidate. A successful automatic variant cannot turn a blocked live variant into PASS. Manual and hardware gates require a named observer. Release-level aggregation is the logical conjunction, not an average or percentage.

Record for every execution: case ID, candidate/source revision, backend/extension/config revision, test data revision, class, OS/architecture/device, preconditions, actions, observed assertions, result, redacted evidence location, observer and timestamp. Evidence must show actual external effect readback where relevant. No inference from a successful tool return alone. Do not use real customer data in destructive tests.

All numeric latency/resource bounds in [TESTING.md](TESTING.md) are acceptance targets, not measurements. All pricing and allowances remain unapproved operator configuration until [external inputs](../operations/EXTERNAL-INPUTS.md) are verified. Security, approvals and OS consent cannot be disabled to achieve one-prompt autonomy.

## Requirement cases

<a id="pb-001"></a>
## PB-001 — Native installation, launch, update and quit

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-01](TESTING.md#gj-01), [GJ-09](TESTING.md#gj-09).

<a id="tc-pb-001-p"></a>
### TC-PB-001-P — positive

On a clean supported Mac, mount the notarized DMG, install Pebbi, launch from Finder and reopen with local state intact. The running binary is native for the machine architecture. An authorized compatible update preserves state. Quit terminates Pebbi-owned capture, audio, task execution and helper processes; local routines do not run after Quit. Verify a second launch attaches to the existing account store, Dock visibility choices cannot strand the app, and update availability/download/install-relaunch are separately observable.

<a id="tc-pb-001-n"></a>
### TC-PB-001-N — negative

A tampered, unsigned, wrong-architecture or unsupported-OS artifact cannot be presented as supported. Interrupted install/update leaves either the prior launchable build or a recoverable installation, not partial success. Relaunch does not duplicate a task or regenerate existing Pebbis. Disk-full installation/update preserves prior data and exposes unresolved effects before shutdown rather than hiding them.

**Required gate/evidence:** Inspect bundle architecture, signing, notarization and quarantine on real Intel and Apple Silicon machines; verify process exit and a canary routine stays unexecuted after Quit. Use LG-NATIVE, LG-DISTRIBUTION and FI-CRASH.

<a id="pb-002"></a>
## PB-002 — Account sign-in, sign-out and device sessions

Required classes: **automated, manual, live**. Shared journeys: [GJ-01](TESTING.md#gj-01), [GJ-08](TESTING.md#gj-08).

<a id="tc-pb-002-p"></a>
### TC-PB-002-P — positive

Complete Entra External ID authorization-code + PKCE in the system browser, validate identity, register a device and reload the session from Keychain. Sign-out disconnects protected transports and removes local session material while retaining local user content unless deletion was requested. Enroll using verified recent interactive authentication, store the once-returned device credential in Keychain, and exercise account bearer plus matching device ID/token on every device-bound route. Revoke another test device and observe its next protected operation rejected; old authentication cannot mint a replacement enrollment. Run [TC-REPAIR-DEVICE](TESTING.md#tc-repair-device), including successful fresh post-revocation re-enrollment and explicit lost-response recovery without secret replay. Retained local account data is locked against a different signed-in identity; device/session listing and revocation match server state.

<a id="tc-pb-002-n"></a>
### TC-PB-002-N — negative

Reject mismatched state, nonce, issuer, audience, redirect URI, reused code, expired token and cross-account device IDs. A stolen valid bearer with a guessed/changed device ID, absent or mismatched device credential, revoked credentials, stale enrollment authentication or refreshed-token issue time grants no device-bound admission or audio session minting. No changed installationId bypasses `enrollmentNotBefore`; equal/older authentication time is rejected. A cancelled browser sign-in is not a connected account. A signed-out user cannot spend quota or access account data using cached authorization; account switching does not mix local histories. Sign-out is not deletion, and another account cannot browse retained private data or inherit its grants.

**Required gate/evidence:** Capture redacted auth decisions and server revocation readback. Real tenant/client/redirect and two test sessions are required for LG-IDENTITY; fixture auth cannot clear it.

**Mandatory repair fixtures:** [TC-REPAIR-DEVICE](TESTING.md#tc-repair-device). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-003"></a>
## PB-003 — Permission onboarding and denied/revoked recovery

Required classes: **automated, manual, hardware**. Shared journeys: [GJ-01](TESTING.md#gj-01), [GJ-02](TESTING.md#gj-02), [GJ-03](TESTING.md#gj-03).

<a id="tc-pb-003-p"></a>
### TC-PB-003-P — positive

Explain the requested capability before its system prompt; request microphone, screen capture, Accessibility and notifications only when needed. Denial leaves unrelated typed/local features usable. After a grant or revocation, recheck authoritative OS permission state and show the matching recovery action; return from System Settings without losing the pending user intent. Exercise managed-policy denial and permission changes requiring app relaunch; show the manual Settings route if the deep link lands elsewhere.

<a id="tc-pb-003-n"></a>
### TC-PB-003-N — negative

Deny each permission at onboarding and revoke during use. No capture, insertion or desktop action occurs after denial/revocation, no permission is auto-granted, and no repeated prompt loop runs. Missing Accessibility cannot silently trigger foreground CGEvent takeover. A prompt being dismissed or Settings being opened is never treated as proof of an OS grant.

**Required gate/evidence:** Run FI-PERMISSIONS on real macOS with clean and existing TCC state. Test harness records attempted calls as well as visible UI; a hidden denied operation is still a failure.

<a id="pb-004"></a>
## PB-004 — Personalization interview and first Pebbis

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-01](TESTING.md#gj-01).

<a id="tc-pb-004-p"></a>
### TC-PB-004-P — positive

Complete or skip the personalization interview using typed input. Show editable name, role, appearance and disclosed AI identity before saving a persistent Pebbi and its workspace. Restart and verify exactly the saved choices. A default Pebbi named Pebbi is available without completing optional questions. Test name/pronunciation, work context, useful help and boundary questions as individually skippable/editable; create the default plus up to two confirmed tailored Pebbis. Run voice and keyboard interview variants, manual offline setup, and the safe-sample talk/type/capture/pointer/dictation tour.

<a id="tc-pb-004-n"></a>
### TC-PB-004-N — negative

Cancel or crash between interview answers and save. No duplicate Pebbi/workspace is committed and unapproved inferred memory is not silently promoted to user preference. Blank/invalid names produce inline feedback, not a broken card. Skipping does not block core access. Skip tour clears drawings and speech; cancelled interview retains only explicitly saved answers, and an exhausted operator-configured setup allowance offers manual forms without forced Checkout.

**Required gate/evidence:** Use deterministic local persistence fixtures plus keyboard and VoiceOver review of the interview; inspect saved rows and workspaces after restart. The spoken interview and safe dictation tour also require LG-VOICE/LG-DICTATION live hardware evidence; offline/manual setup cannot clear those blocked variants.

<a id="pb-005"></a>
## PB-005 — Menu bar, top-edge perch and full Home window

Required classes: **automated, manual, hardware**. Shared journeys: [GJ-01](TESTING.md#gj-01), [GJ-02](TESTING.md#gj-02).

<a id="tc-pb-005-p"></a>
### TC-PB-005-P — positive

Open Home from the menu bar and compact top-edge perch. Navigate Home, Pebbis, Conversations, Files, Suggestions, Routines, Connections and Settings without duplicate windows or orphaned focus. The perch works on notchless and external displays, communicates actual voice/task status, and can be dismissed without stopping a task. Move a nonempty draft, running task, scrolled conversation and open artifact between menu bar/perch/Home. Escape dismisses the expanded perch and prevents hover reopening until the pointer leaves; external reply links make room for the destination.

<a id="tc-pb-005-n"></a>
### TC-PB-005-N — negative

Closing Home does not imply Quit or task completion. Rapid open/close/reopen during motion never traps input, teleports focus or leaves an invisible interactive overlay. Hidden/perch-only presentation never suggests a microphone is idle while it is capturing. No surface transition discards drafts or hides an approval/billing sheet; a missing conversation yields recovery rather than an endless reopen failure.

**Required gate/evidence:** Run LG-NATIVE and LG-ACCESSIBILITY; inspect AX roles and native controls, state-to-label mapping and reversible, interruptible motion against root DESIGN.md, not against web-shell screenshots.

<a id="pb-006"></a>
## PB-006 — Global shortcuts and focus-safe activation

Required classes: **automated, manual, hardware**. Shared journeys: [GJ-02](TESTING.md#gj-02), [GJ-03](TESTING.md#gj-03).

<a id="tc-pb-006-p"></a>
### TC-PB-006-P — positive

Record and invoke supported global shortcuts from another app; show the intended Pebbi surface while preserving the prior target context. Changing a shortcut unregisters the old binding. Escape/dismiss returns focus where safe. Pointer-down feedback occurs before an eventual commit and cancellation by moving away does not commit. Exercise Control–Command–A Home, Control–Option hold talk, Fn–Control hold dictation and Fn–Control double-tap hands-free defaults when the OS supports them, plus alternate bindings, external keyboards and keyboard layouts. Hold release ends capture, not task execution.

<a id="tc-pb-006-n"></a>
### TC-PB-006-N — negative

Conflicting/reserved shortcuts are rejected with recovery, not silently intercepted. Repeated activation does not create duplicate voice sessions. Secure input, lock screen and another app changing focus cannot cause an insertion or hidden foreground action. Key repeat, a shortcut recorder, active menus, Caps Lock and unsupported Fn delivery cannot create duplicate turns or swallow Escape; explain unsupported bindings and retain the last valid binding.

**Required gate/evidence:** Exercise shortcut registration with real apps, secure fields and fullscreen Spaces; log focus identity before activation and before any effect. FI-FOCUS applies.

<a id="pb-007"></a>
## PB-007 — Real-time spoken conversation and typed equivalent

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-02](TESTING.md#gj-02).

<a id="tc-pb-007-p"></a>
### TC-PB-007-P — positive

An explicit start opens the selected gpt-realtime-2.1 session and maps idle, connecting, listening, thinking and speaking to visible and accessible status. The user can speak, receive audible output, interrupt playback and continue. A typed equivalent is available and transcript persistence follows the selected privacy policy. Stopping speech does not cancel an independently running task. Exercise [TC-REPAIR-AUDIO-OWNER](TESTING.md#tc-repair-audio-owner): ongoing voice and a reasoning task make independent progress, use distinct reservations/receipts, and never confuse real source-task provenance with the audio wire owner. Typed users can invoke the same tools and approval flows; no-audio or muted output remains readable, and every work handoff exposes a task reference.

<a id="tc-pb-007-n"></a>
### TC-PB-007-N — negative

Inject unsupported deployment, disconnect, duplicate turn events and user interruption. Stop old playback and reject stale audio; never play a prior turn after a new one starts. Show unavailable/failed rather than synthetic success. No silent model substitution or unsolicited microphone start is allowed. Run [TC-REPAIR-MESSAGE-BYTES](TESTING.md#tc-repair-message-bytes) against multibyte/escaped/fragmented transcript and context messages; serialized UTF-8 caps include the envelope and must never silently truncate a final utterance. Audio retains its tighter message/decoded-byte limits. No spontaneous always-listening restart is allowed; incomplete transcript/response is labeled partial rather than silently completed.

**Required gate/evidence:** LG-VOICE is BLOCKED pending the user-deferred Azure realtime input; test real bidirectional audio on hardware plus FI-PROVIDER and FI-VOICE. Typed Astra success cannot satisfy voice.

**Mandatory repair fixtures:** [TC-REPAIR-AUDIO-OWNER](TESTING.md#tc-repair-audio-owner), [TC-REPAIR-MESSAGE-BYTES](TESTING.md#tc-repair-message-bytes), [TC-REPAIR-NATIVE-APPROVAL](TESTING.md#tc-repair-native-approval). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-008"></a>
## PB-008 — Explicit screen capture scope and screen understanding

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-02](TESTING.md#gj-02).

<a id="tc-pb-008-p"></a>
### TC-PB-008-P — positive

Choose a specific permitted window/display and explicitly attach that context. The indicator identifies the active scope; explanation refers to observable selected content and identifies uncertainty. Switching scope requires user selection and invalidates stale frames. Stop sharing clears capture and ephemeral buffers. Test selected region as well as window/display, user-drawn focus marks, recapture and removal; persistent history contains scope metadata, not raw frames unless separately saved.

<a id="tc-pb-008-n"></a>
### TC-PB-008-N — negative

A denied, closed, protected, stale or off-scope window cannot be captured by broadening to the whole desktop. Screenshots containing untrusted instructions do not authorize tools. Synthetic canary text in an excluded window does not appear in provider input, storage, telemetry or response claims. Blank capture or newly appearing sensitive content pauses for re-selection/redaction and never infers unseen content.

**Required gate/evidence:** Run LG-NATIVE screen capture, LG-AI and FI-PERMISSIONS. Keep redacted scope receipts and controlled-frame hashes; inspect actual outbound payload boundaries using test-owned content.

<a id="pb-009"></a>
## PB-009 — Drawing, pointing and resumable guided walkthroughs

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-02](TESTING.md#gj-02).

<a id="tc-pb-009-p"></a>
### TC-PB-009-P — positive

Draw a point/outline or step guide against the chosen window with a text/VoiceOver equivalent. Next, Back, Pause, Resume and Dismiss preserve a stable step identity. Geometry follows permitted window moves and display scale changes; a guide resumes only after revalidating the target. Run a guide longer than fifteen steps with goal, target, expected result and completion evidence for each; pause, relaunch and resume. End cancels the guide task through canonical cancellation while retaining progress; Escape only clears current presentation/speech and unrelated work remains unchanged.

<a id="tc-pb-009-n"></a>
### TC-PB-009-N — negative

Close the target, navigate away or change permission mid-guide. Hide stale overlays and ask for a new target; do not point at unrelated pixels. Guidance never intercepts clicks meant for another app, falsely claims execution or requires animated motion to understand the step. A timer cannot mark a manual step complete; uncertain completion waits for confirmation/reinspection and continuation never silently truncates the procedure.

**Required gate/evidence:** Compare controlled target bounds and overlay hit-testing on real displays, review reduced-motion equivalence, and verify Astra target interpretation with LG-AI; FI-DISPLAY applies.

<a id="pb-010"></a>
## PB-010 — Dictation, review and focus-safe insertion

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-03](TESTING.md#gj-03).

<a id="tc-pb-010-p"></a>
### TC-PB-010-P — positive

Start dictation deliberately with a selected input device; stream through gpt-live-transcribe into reviewing text, permit correction and cancel, then insert only after revalidating the original app, field and secure-input status. One confirmed insertion yields one completed transcript and no duplicated characters. Test standalone dictation while the Pebbi’s agent task runs or waits for approval/connection, without surrogate agent-task queue admission; explicitly hand off a single microphone lease from voice if needed. Test attachment-free dictation with language preference and explicitly edited personal dictionary; review-first is default. User-enabled direct insertion is limited to revalidated nonsensitive fields. Test terminal/shell destinations with line breaks collapsed and a mandatory preview; never press Return to submit or execute.

<a id="tc-pb-010-n"></a>
### TC-PB-010-N — negative

Switch focus, close the field, enable secure input, deny Accessibility, unplug the microphone, interrupt the network or replay final transcript events. Preserve recoverable text for review without inserting elsewhere. Cancel before insertion dispatch leaves the target unchanged. After an insertion is admitted, cancellation stops further work and reconciles that one effect; retain inserted/unchanged/unknown outcome in the insertion receipt alongside the canonical lifecycle state. Do not automatically undo over concurrent user edits, insert again or claim unchanged/success without evidence. Run all [TC-REPAIR-DICTATION-CANCEL](TESTING.md#tc-repair-dictation-cancel) barriers, including target acceptance before readback and restart with uncertainty. A pasteboard fallback is disclosed and does not silently overwrite a changed clipboard. Punctuation cleanup cannot invent meaning; a copied transcript is not an inserted transcript, and a no-final provider close is failed, not an empty success.

**Required gate/evidence:** LG-DICTATION is BLOCKED pending the user-deferred deployment. Verify real transcription and app insertion separately with FI-FOCUS, FI-AUDIO and FI-DUPLICATE, including a native text field and supported browser editor.

**Mandatory repair fixtures:** [TC-REPAIR-AUDIO-OWNER](TESTING.md#tc-repair-audio-owner), [TC-REPAIR-MESSAGE-BYTES](TESTING.md#tc-repair-message-bytes), [TC-REPAIR-DICTATION-CANCEL](TESTING.md#tc-repair-dictation-cancel). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-011"></a>
## PB-011 — Persistent Pebbi creation, editing and appearance

Required classes: **automated, manual**. Shared journeys: [GJ-01](TESTING.md#gj-01), [GJ-04](TESTING.md#gj-04).

<a id="tc-pb-011-p"></a>
### TC-PB-011-P — positive

Create distinct named Pebbis with job, original appearance, workspace and memory; edit one and restart. Saved identity remains stable across Conversations, Files, Routines and task events. Selecting another Pebbi changes context without reassigning in-flight work. Verify duplicate display names are allowed with job-based disambiguation, stable list order and explicit pinning. Archive previews active-work handling and pauses associated routines; unarchive never resumes those routines automatically.

<a id="tc-pb-011-n"></a>
### TC-PB-011-N — negative

Cancel an edit or attempt duplicate concurrent writes. No partial profile is exposed and another Pebbi's memory/files are not reassigned. Missing/corrupt optional artwork has an accessible fallback; removing a Pebbi with active work requires explicit resolution, not orphan tasks. An empty name/job cannot save, a failed save retains the draft, and a conversational profile proposal cannot rewrite a running attempt without an explicit follow-up.

**Required gate/evidence:** Inspect GRDB transactions and immutable ownership IDs; review keyboard navigation, naming and appearance contrast with multiple Pebbis.

<a id="pb-012"></a>
## PB-012 — Conversations, search, archive, unread and pinning

Required classes: **automated, manual**. Shared journeys: [GJ-04](TESTING.md#gj-04), [GJ-08](TESTING.md#gj-08).

<a id="tc-pb-012-p"></a>
### TC-PB-012-P — positive

Persist and search conversations with matching snippets, timestamps and owner; pin/unpin, archive/unarchive and mark/read unread state. Restart preserves these choices. Opening a conversation does not create or resume a task; a running task links back to the correct conversation. Preserve separate drafts, attachments, scroll and preview for each conversation. Paginate long history without jumping; new messages while scrolled up expose Jump to latest. Explicit Mark unread while open survives until an explicit read action or leaving and reopening.

<a id="tc-pb-012-n"></a>
### TC-PB-012-N — negative

Deleted or other-account material never appears in search. Empty/no-result and oversized queries have bounded behavior. Concurrent incoming events and mark-read updates neither lose unread messages nor manufacture unread counts; stale search results cannot reopen purged content. Archiving cannot hide outstanding approvals or lose a draft. Missing/deleted history offers a clearly labeled fresh conversation with surviving Pebbi memory and task references, not fabricated recovered messages.

**Required gate/evidence:** Use local search-index fixtures, event races and restart assertions; review empty/error/loading screens and VoiceOver result navigation.

<a id="pb-013"></a>
## PB-013 — Memory inspect, edit, forget and context compaction

Required classes: **automated, manual, live**. Shared journeys: [GJ-04](TESTING.md#gj-04), [GJ-08](TESTING.md#gj-08).

<a id="tc-pb-013-p"></a>
### TC-PB-013-P — positive

Inspect each saved memory with provenance and scope, edit it, forget it and reload. Context compaction preserves current instructions, tool receipts, approvals and unresolved work; show that a compacted summary is derived. A forgotten canary is absent from newly constructed prompts, active retrieval indexes and subsequent compactions. Test disabling memory proposals, explicit global versus Pebbi scope, user correction of summaries and a failed compaction that leaves original history usable. Forgetting a fact does not claim deletion of unrelated original chats.

<a id="tc-pb-013-n"></a>
### TC-PB-013-N — negative

Inject contradictory/stale memory, cross-Pebbi records and malicious memory instructions. The current explicit instruction and scoped authorization win; forgotten items are not resurrected from summaries, caches or queued context. If an in-flight provider request already received content, disclose that it cannot be recalled and invalidate subsequent use. Run [TC-REPAIR-TOKEN-BUDGET](TESTING.md#tc-repair-token-budget): missing/null/unusable delivered budgets fail readiness closed, changed budgets re-estimate before dispatch, and provider context-limit recovery preserves instructions, citations, approvals and unresolved receipts instead of silently dropping them. Sensitive inferences/secrets are not saved; conflicts ask which fact to retain, and deleted/unavailable source references are not silently fabricated.

**Required gate/evidence:** Run FI-MEMORY and LG-AI using synthetic canaries. Inspect actual prompt construction and provider requests, not only a friendly model answer saying it forgot.

**Mandatory repair fixtures:** [TC-REPAIR-TOKEN-BUDGET](TESTING.md#tc-repair-token-budget). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-014"></a>
## PB-014 — Attachments, whole-document reading and previews

Required classes: **automated, manual, live**. Shared journeys: [GJ-04](TESTING.md#gj-04).

<a id="tc-pb-014-p"></a>
### TC-PB-014-P — positive

Attach supported files, validate type/size, preview via native Quick Look/PDFKit where appropriate and read the full requested document. Index every page/section or report the exact unsupported/encrypted/missing ranges. A cited answer points to the actual page/section, including a controlled fact at the end of the document. Exercise picker, drag/drop and intentional paste, including attachment-only messages, duplicate detection and managed copy behavior after original deletion. Markdown refresh preserves scroll and never runs embedded code; restore preview per conversation.

<a id="tc-pb-014-n"></a>
### TC-PB-014-N — negative

Corrupt, encrypted, misleading-extension, oversized, symlinked or malicious documents cannot crash the app, escape the workspace or authorize execution. Truncation must be explicit; a first-page-only answer cannot claim whole-document reading. Removal invalidates retrieval caches and pending attachment access. Failed drops preserve the composer. Sending file content needs disclosure separately from local preview; document macros/scripts never run.

**Required gate/evidence:** Use multi-page fixtures with first/middle/final canaries, Unicode and scanned pages; LG-AI verifies actual document-grounded reasoning. Compare extraction manifest with the complete file, not a preview thumbnail.

**Mandatory repair fixtures:** [TC-REPAIR-ARTIFACT](TESTING.md#tc-repair-artifact). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-015"></a>
## PB-015 — Agent task execution and truthful live progress

Required classes: **automated, manual, live**. Shared journeys: [GJ-04](TESTING.md#gj-04), [GJ-05](TESTING.md#gj-05).

<a id="tc-pb-015-p"></a>
### TC-PB-015-P — positive

Submit a bounded task and inspect queued, running and any wait states, ordered journal events, tool receipts and final artifacts. Only verified completed effects/artifacts yield succeeded; failures carry the failed step and recovery option. Retry creates a linked new attempt, not mutation of a terminal attempt. Show original goal, named Pebbi, elapsed/usage context, current verified step and inspectable collapsed details. The final response names artifacts/evidence, partial results and remaining blockers.

<a id="tc-pb-015-n"></a>
### TC-PB-015-N — negative

Duplicate/out-of-order SSE events, provider hallucinated receipts, dropped tool results and unavailable transports cannot create false progress or succeeded. A conversation reply is not proof of execution. Failed tools remain visible; no test fixture result is exposed as a real provider result. A decorative progress percentage without a meaningful denominator is not execution evidence; incomplete required work cannot be hidden by delivering only independent outputs.

**Required gate/evidence:** Correlate UI, task-local sequence journal, actual tool readback and output hashes; LG-AI plus FI-NETWORK, FI-DUPLICATE and FI-CRASH are mandatory.

**Mandatory repair fixtures:** [TC-REPAIR-ARTIFACT](TESTING.md#tc-repair-artifact), [TC-REPAIR-AUDIO-OWNER](TESTING.md#tc-repair-audio-owner), [TC-REPAIR-TOKEN-BUDGET](TESTING.md#tc-repair-token-budget). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-016"></a>
## PB-016 — Concurrent Pebbis, queues and race-free follow-ups

Required classes: **automated, manual, live**. Shared journeys: [GJ-05](TESTING.md#gj-05).

<a id="tc-pb-016-p"></a>
### TC-PB-016-P — positive

Run independent tasks for two Pebbis concurrently while serializing conflicting work on the same resource. Display bounded queue position and reason; a follow-up is bound to an explicit task/conversation and queued or applied only at a safe boundary. Completed events return to the correct owner. Assert one active agent-task attempt per Pebbi, with independent voice/dictation audio ownership outside the serial task slot; a follow-up racing startup/completion is included exactly once or becomes a visible successor. Reorder queued work transactionally; preserve source-carrying suggestion context and explicit task destination.

<a id="tc-pb-016-n"></a>
### TC-PB-016-N — negative

Saturate queues, interleave follow-ups, cancel a queued task and replay an old completion. No queue grows without bound, no cross-Pebbi memory or artifact leakage occurs, and no exclusive resource is held by two writers. Queue overflow is explicit and does not silently discard accepted work. Ambiguous “retry it” or duplicate-name routing asks; archived Pebbis require reassign/unarchive. A follow-up that changes a preview invalidates its old approval before dispatch.

**Required gate/evidence:** Run FI-QUEUE with deterministic scheduling and a live controlled parallel task; assert event ownership, bounded concurrency, fairness and resource lease release after crash.

**Mandatory repair fixtures:** [TC-REPAIR-AUDIO-OWNER](TESTING.md#tc-repair-audio-owner). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-017"></a>
## PB-017 — Approval, stop, cancellation and recovery

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-05](TESTING.md#gj-05), [GJ-06](TESTING.md#gj-06).

<a id="tc-pb-017-p"></a>
### TC-PB-017-P — positive

Preview exact target/action/payload before a protected effect; bind allowOnce, allowForScope or deny to the displayed scope and expiry. Protected-effect allows require deliberate accessible native approval-control activation by pointer, keyboard, VoiceOver or equivalent assistive interaction; task/suggestion selection by speech is not that decision. Stop moves running work through cancelling to cancelled after quiescence. Recovery marks active attempts interrupted and reconciles uncertain effects before offering a new attempt. Inspect and revoke existing grants; keep Stop reachable during streaming, approval waits and heavy load. Test cancellation racing dispatch/completion and denial of an essential action yielding input/replan or explicit cancellation.

<a id="tc-pb-017-n"></a>
### TC-PB-017-N — negative

Replay, expire or change an approval payload; reject it. Payment, credentials, destructive bulk, publishing and outbound messages always require fresh approval. Prompt injection, local allowlists and one-prompt build autonomy cannot disable these checks. Speech interruption alone does not cancel tasks and cancellation never promises reversal of a completed effect. Unambiguous spoken “yes,” replayed transcripts, typed/model-asserted consent and ambiguous spoken approval all leave protected effects waiting for native approval with zero dispatch; late Allow after cancellation cannot resurrect the task, and repeated unchanged proposals after Deny cannot form a nag/bypass loop.

**Required gate/evidence:** Run FI-APPROVAL and FI-DUPLICATE using a controlled recipient/resource; verify both server and native boundaries. Hardware takeover permission must be tested separately from application approval.

**Mandatory repair fixtures:** [TC-REPAIR-ARTIFACT](TESTING.md#tc-repair-artifact), [TC-REPAIR-AUDIO-OWNER](TESTING.md#tc-repair-audio-owner), [TC-REPAIR-NATIVE-APPROVAL](TESTING.md#tc-repair-native-approval), [TC-REPAIR-DICTATION-CANCEL](TESTING.md#tc-repair-dictation-cancel). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-018"></a>
## PB-018 — Native desktop control and takeover boundaries

Required classes: **automated, manual, hardware**. Shared journeys: [GJ-06](TESTING.md#gj-06).

<a id="tc-pb-018-p"></a>
### TC-PB-018-P — positive

Use native AXUIElement semantics against an allowlisted app/resource, re-resolve the target and verify the result. When semantic action is impossible, request explicit foreground takeover before any CGEvent fallback; state that it affects the real cursor/focus and provide immediate Stop.

<a id="tc-pb-018-n"></a>
### TC-PB-018-N — negative

Deny AX permission or takeover, change the active window, expose a password/payment/permission dialog or revoke scope. No fallback action occurs. Secure controls are not read or typed into by automation, and background capability is never inferred from a successful action in one app.

**Required gate/evidence:** Test real AX-compatible and incompatible apps, minimized windows and user focus interference. Count issued native events; denied cases must emit zero protected events. FI-FOCUS and FI-PERMISSIONS apply.

<a id="pb-019"></a>
## PB-019 — Browser DOM tools and user-selected sessions

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-06](TESTING.md#gj-06).

<a id="tc-pb-019-p"></a>
### TC-PB-019-P — positive

Install the opt-in Chromium MV3 extension and authenticated native-messaging helper through documented Chrome and Brave flows. Explicitly select a tab or dedicated window, inspect DOM and perform one approved test action with readback. Native host verifies extension origin and per-session authorization.

<a id="tc-pb-019-n"></a>
### TC-PB-019-N — negative

Wrong extension origin, stale tab ID, closed tab, cross-origin navigation, removed extension, forged native messages and host disconnect invalidate access. No ordinary signed-in profile remote-debugging port is opened and another tab's content is not exposed. Web page instructions cannot change grants.

**Required gate/evidence:** Run LG-BROWSER on both browsers with real signed native packaging, clean profiles and upgraded profiles; FI-BROWSER covers stale sessions and unauthorized messages.

<a id="pb-020"></a>
## PB-020 — Web research with source-grounded results

Required classes: **automated, manual, live**. Shared journeys: [GJ-04](TESTING.md#gj-04).

<a id="tc-pb-020-p"></a>
### TC-PB-020-P — positive

Research a specified question using real retrieved sources; report titles, URLs and retrieval context and support each material factual claim with a source that actually contains it. Distinguish observation, inference, outdated evidence and unresolved contradictions. Save a requested source-grounded result to the selected workspace. Include a constrained multi-item/date research request: save item-level evidence, distinguish publication from access date, deduplicate and verify exact collected count before claiming completeness; prefer inspected primary sources.

<a id="tc-pb-020-n"></a>
### TC-PB-020-N — negative

Blocked pages, misleading snippets, stale sources or insufficient evidence yield an explicit limitation, never invented citations or fabricated quotes. Hostile page instructions cannot access another workspace, change recipient or grant authority. Citation URLs cannot be replaced by model-guessed paths. A partial item set cannot satisfy a complete-list task, and private connector evidence cannot silently become public-web scope.

**Required gate/evidence:** LG-AI requires a live source fetch plus human claim-to-source review; deterministic fixtures cover inaccessible pages, contradictory documents and prompt injection.

<a id="pb-021"></a>
## PB-021 — Files, workspace boundaries and code execution

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-04](TESTING.md#gj-04), [GJ-06](TESTING.md#gj-06).

<a id="tc-pb-021-p"></a>
### TC-PB-021-P — positive

From an empty selected Pebbi workspace, stage explicitly structured authored UTF-8 text with `stageTextArtifact`, then finalize and use its native immutable ID/byte count/digest for a separately authorized file creation. Staging alone changes no user target file and ordinary assistant prose is not a file. Preview the created artifact, show its final path and verify actual bytes. Execute a staged harmless script only after actual same-account/workspace `scriptArtifactId`/`expectedSha256` verification and fresh native review of the script bytes and execution inputs; an invented ID or `scriptVersionId` cannot supply authority. Run code only through a scoped, disclosed tool policy with working directory, timeout, output limits and child-process lifecycle control. Access beyond the workspace requires a new bounded user grant. Preview destination/diff before overwrite, preserve the prior file until atomic commit, show command exit status and distinguish generated code from actually executed/tested output. Missing executable is a recoverable prerequisite failure.

<a id="tc-pb-021-n"></a>
### TC-PB-021-N — negative

Path traversal, symlink escape, alias escape, home-directory expansion, malicious filenames, environment-secret access and unapproved network/process execution are rejected. Run [TC-REPAIR-ARTIFACT](TESTING.md#tc-repair-artifact) with Unicode byte fidelity, duplicate/changed/gapped chunks, cross-scope drafts, chunk/aggregate/envelope limits, immutable finalization and private cleanup. No private draft/artifact text or hash enters the metadata-only journal; only explicit Save permits durable private output. An allowlist is not claimed as an OS sandbox. Stop/Quit terminates owned execution; output flooding cannot freeze Home. No automatic package install, paid resource scaling or environment repair may expand scope/spend without authorization.

**Required gate/evidence:** Use test-owned workspaces and OS process/file observations; FI-WORKSPACE and FI-QUEUE apply. Exercise cooperative owned-process termination, and reject work requiring guaranteed adversarial-code confinement until a reviewed OS-isolation design exists; process groups/allowlists alone cannot guarantee it. Live reasoning must not convert suggested commands into silently authorized execution.

**Mandatory repair fixtures:** [TC-REPAIR-ARTIFACT](TESTING.md#tc-repair-artifact). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-022"></a>
## PB-022 — Built-in connection catalog and OAuth lifecycle

Required classes: **automated, manual, live**. Shared journeys: [GJ-06](TESTING.md#gj-06).

<a id="tc-pb-022-p"></a>
### TC-PB-022-P — positive

For every built-in catalog connection declared supported, show required scopes, complete its applicable real OAuth or native permission flow, execute an authorized read and any documented separately approved write, refresh/revalidate credentials or grants and disconnect. Connection state reflects disconnected, connecting, ready, expired, degraded or failed; tokens remain in Keychain unless an explicit server operation requires transfer. Required catalog coverage includes Google Workspace (Gmail, Drive, Sheets, Calendar), Notion, Slack, Linear, Spotify and native Notes/Calendar/Reminders. Test each documented adapter capability, OAuth for OAuth-backed services and native OS grants for native integrations; report unavailable entries rather than omitting them. Connection changes update existing conversation tool context.

<a id="tc-pb-022-n"></a>
### TC-PB-022-N — negative

Cancel login, revoke refresh token, remove a scope, replay callback or change account. The connector cannot remain falsely ready or silently ask for broader scope. Disconnect closes sessions and prevents subsequent queued access; a catalog card is not evidence of working integration. A native integration is not forced through invented OAuth, and read-only capabilities are not advertised as writable. Unsupported scopes require explanation, not a fake connected logo.

**Required gate/evidence:** LG-CONNECTIONS requires a per-connector capability/scopes/result inventory; unsupported or uncredentialed entries stay disconnected and make the advertised support gate BLOCKED.

<a id="pb-023"></a>
## PB-023 — Custom remote/local MCP connections

Required classes: **automated, manual, live**. Shared journeys: [GJ-06](TESTING.md#gj-06).

<a id="tc-pb-023-p"></a>
### TC-PB-023-P — positive

Add a user-authorized remote HTTPS MCP or local stdio MCP connection with inspected tool schemas, bounded resource scope and explicit process/transport lifecycle. Display identity and trust implications, execute a safe tool and verify its actual response. Disconnect terminates owned processes and expires grants. Expose separate local executable, arguments, declared environment-variable names and chosen workspace; approve first process launch, discover schemas read-only, and allow individual tools to be disabled.

<a id="tc-pb-023-n"></a>
### TC-PB-023-N — negative

Malformed schemas, oversized outputs, redirects to private metadata hosts, untrusted TLS, malicious tool descriptions and unexpected executable arguments cannot widen authority or leak secrets. Local commands are not arbitrary shell strings; no unsigned/untrusted server gains credential/payment permission through allowForScope. Pasted shell expressions and unknown package installs never execute implicitly; credential-in-URL input is rejected and changed command/origin/risk invalidates relevant grants.

**Required gate/evidence:** LG-CONNECTIONS includes one controlled remote and one local server, OAuth where applicable, process cleanup and hostile schema fixtures. FI-MCP covers timeout and tool-list changes.

<a id="pb-024"></a>
## PB-024 — Read-only personalized suggestions and approve-to-run

Required classes: **automated, manual, live**. Shared journeys: [GJ-07](TESTING.md#gj-07).

<a id="tc-pb-024-p"></a>
### TC-PB-024-P — positive

Generate personalized Suggestions only from granted readable context and show reason, source context and proposed scope. Dismiss, snooze or approve a suggestion. Selecting a low-risk suggestion by native Approve or unambiguous speech creates one visible task; speech may also open its review. This selection creates no protected-effect grant: task-level protected effects still require deliberate accessible native approval against the exact preview. Reopening Suggestions does not execute anything. Test the default disclosed 72-hour source lookback, one proposal at a time, named owner/outcome, estimated usage class and explicit Approve, Skip, Adjust, Dismiss. Adjust creates a proposal version; Cancel restores the original; approved busy work retains source snapshots in its queue.

<a id="tc-pb-024-n"></a>
### TC-PB-024-N — negative

Background suggestion computation cannot send messages, write files, charge usage beyond authorized limits or connect a new service. Sensitive/forgotten content is excluded. Duplicate clicks/replayed suggestion events create at most one task; stale proposals must refresh before execution. A skipped proposal or optional rejection reason is not authorization; stale source changes require revalidation before launch.

**Required gate/evidence:** Run deterministic suggestion/action separation and LG-AI on test-owned context; inspect side-effect ledger showing zero writes before approve-to-run.

**Mandatory repair fixtures:** [TC-REPAIR-NATIVE-APPROVAL](TESTING.md#tc-repair-native-approval). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-025"></a>
## PB-025 — Routines, local scheduling, wake and retry policy

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-07](TESTING.md#gj-07).

<a id="tc-pb-025-p"></a>
### TC-PB-025-P — positive

Create an approved local routine with timezone, trigger, target Pebbi and bounded tool scope; inspect active, paused, blocked and archived states. While Pebbi is open it schedules correctly; wake produces at most one catch-up per eligible routine. View next eligible run, missed occurrence summary and actual run history. Test Run now and ambiguous schedule editing, overlap skip, bounded occurrence retries, exactly three consecutive failed occurrences pausing the routine, and successful occurrence resetting failure streak. Waiting/cancelled/skipped occurrences are not failures. Launch after Quit advances watermark without replay; Run now is explicit.

<a id="tc-pb-025-n"></a>
### TC-PB-025-N — negative

Quit, sleep across repeated triggers, change clock/timezone, deny permission or replay scheduler events. No cloud execution while the Mac is off, no backlog flood and no duplicate effect for one occurrence. Paused/archived routines do not fire; expired permissions make blocked, not implicit consent. Archive/unarchive never silently resumes a routine; denied or uncertain effects cannot be retried by a schedule timer. Timezone changes show recalculated next run.

**Required gate/evidence:** Use virtual clocks for DST/clock jumps and real sleep/wake/Quit hardware. LG-SCHEDULER and FI-SLEEP verify one catch-up and side-effect reconciliation before retry.

<a id="pb-026"></a>
## PB-026 — Notifications, Focus/call suppression and unread delivery

Required classes: **automated, manual, hardware**. Shared journeys: [GJ-05](TESTING.md#gj-05), [GJ-07](TESTING.md#gj-07).

<a id="tc-pb-026-p"></a>
### TC-PB-026-P — positive

Deliver meaningful task completion/failure notifications according to user permission/preferences; opening one routes to its exact Pebbi/task. Focus/call suppression avoids sound, interruption and unnecessary overlays, while recording unread in the app. On return, present a bounded summary without replaying every alert. Routine results are silent conversation/unread delivery. Include explicit Quiet mode because Focus/call/screen-share detection is incomplete; drop coalesced suggestion greetings after Suggestions is opened/dismissed.

<a id="tc-pb-026-n"></a>
### TC-PB-026-N — negative

Deny notifications, activate Focus, begin a call or change account. No bypass of OS suppression or sensitive lock-screen preview occurs. Duplicate completion events do not create duplicate notifications, and dismissing an alert does not erase unread content without a read action. Suppressed or failed sound cannot lose the result; wake never replays old chimes, and quiet mode does not hide waiting approvals from Home.

**Required gate/evidence:** Test actual Notification Center and permitted Focus/call detection; when call status is unknown, honor explicit quiet mode and conservative suppression. FI-DUPLICATE applies.

<a id="pb-027"></a>
## PB-027 — Plans, metering, reservations and billing changes

Required classes: **automated, manual, live**. Shared journeys: [GJ-08](TESTING.md#gj-08).

<a id="tc-pb-027-p"></a>
### TC-PB-027-P — positive

Render server-approved plan configuration only, reserve usage before provider work, finalize once from trusted metering and show consistent available/reserved/consumed amounts. Hosted Stripe Checkout/Portal updates entitlements after a verified webhook and authoritative reconciliation, not merely a browser success return.

<a id="tc-pb-027-n"></a>
### TC-PB-027-N — negative

Absent/unapproved price IDs disable paid Checkout. Client-forged usage, concurrent reservations, webhook replay/out-of-order delivery, invalid signature and currency mismatch cannot add entitlement or double-charge. Proposed Nest, Studio and Constellation names do not establish approved prices, subscriptions or allowances.

**Required gate/evidence:** LG-BILLING needs approved operator configuration, Stripe test-mode lifecycle evidence and explicitly authorized limited production verification; FI-QUOTA and FI-DUPLICATE cover exact ledger effects. Use integer minor units and ISO currency.

**Mandatory repair fixtures:** [TC-REPAIR-DEVICE](TESTING.md#tc-repair-device), [TC-REPAIR-AUDIO-OWNER](TESTING.md#tc-repair-audio-owner). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-028"></a>
## PB-028 — Quota limits and graceful provider unavailability

Required classes: **automated, manual, live**. Shared journeys: [GJ-02](TESTING.md#gj-02), [GJ-08](TESTING.md#gj-08).

<a id="tc-pb-028-p"></a>
### TC-PB-028-P — positive

When quota is exhausted or a selected provider is unavailable, show the affected capability, remaining usable local features and a specific retry/configuration action. Reconcile held reservations according to trusted final usage, including partial streams. Restoring verified capability permits explicit retry without duplicate spending.

<a id="tc-pb-028-n"></a>
### TC-PB-028-N — negative

Inject 429, 401, unsupported-operation, deployment-not-found, timeout and midstream failure. No unapproved provider fallback, infinite retry, negative balance or fake response occurs. An unauthenticated/unentitled request never reaches a paid provider; a disconnected service cannot display ready. A missing/unusable `tokenBudget` cannot be guessed from a model name or hidden backend configuration; run TC-REPAIR-TOKEN-BUDGET and TC-REPAIR-MESSAGE-BYTES for explicit preserved-review failures without fake success.

**Required gate/evidence:** Run FI-PROVIDER and FI-QUOTA; all three selected model roles need live evidence under LG-AI, LG-VOICE and LG-DICTATION. Known user-deferred voice failures remain BLOCKED, not waived.

**Mandatory repair fixtures:** [TC-REPAIR-DEVICE](TESTING.md#tc-repair-device), [TC-REPAIR-MESSAGE-BYTES](TESTING.md#tc-repair-message-bytes), [TC-REPAIR-TOKEN-BUDGET](TESTING.md#tc-repair-token-budget). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-029"></a>
## PB-029 — Preferences, voice/device choice and shortcut recording

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-03](TESTING.md#gj-03).

<a id="tc-pb-029-p"></a>
### TC-PB-029-P — positive

Settings exposes voice, input/output device, shortcut, privacy, notifications and relevant startup choices using native controls. Apply an allowed change and restart to verify persistence. Show disconnected/unavailable device or voice choices honestly and retain a usable typed path. Test explicit voice preview/cancel, language, dictionary/review mode, appearance/perch/display policy and shortcut Cancel/Reset; settings apply without restart unless a real technical requirement is disclosed.

<a id="tc-pb-029-n"></a>
### TC-PB-029-N — negative

Unplug a selected device, enter a conflicting shortcut or load incompatible preference data. Do not silently route private speech to an unexpected output or start capture. Invalid values recover to a disclosed safe choice; preference changes do not rewrite unrelated permissions or scoped grants. Voice preview cannot launch a task, choosing Settings cannot start playback, and unavailable voices retain the previous choice without a hidden model picker/fallback.

**Required gate/evidence:** Test actual system device enumeration, VoiceOver labels and migrations; compare saved settings with runtime state after restart and after audio hot-plug. Explicit voice preview requires LG-VOICE on the selected live deployment; an unavailable preview must remain labeled unavailable.

<a id="pb-030"></a>
## PB-030 — Local export, account export and deletion

Required classes: **automated, manual, live**. Shared journeys: [GJ-08](TESTING.md#gj-08).

<a id="tc-pb-030-p"></a>
### TC-PB-030-P — positive

Export local Pebbis, conversations, files and memory with a versioned manifest and integrity information using an explicit destination. Separately request account/usage export from the backend; disclose that it does not contain local conversations/screenshots. Deletion scope is previewed; account deletion revokes sessions and applies the published server retention policy, while local deletion clears selected local records and indexes. Local export also includes selected routine definitions and task/artifact metadata; optionally combine separately consented server and local artifacts without implying cloud sync. Stop/reconcile relevant active work before deletion and offer export first.

<a id="tc-pb-030-n"></a>
### TC-PB-030-N — negative

Cancelled destination selection, insufficient disk, interrupted archive, expired server download and retry cannot expose a partial file as complete or cross-account data. Legal retention exceptions are disclosed rather than promising immediate erasure. Account deletion alone does not falsely claim a powered-off Mac's local files were erased. Local deletion can succeed offline while server deletion stays pending; no “all deleted” message is allowed for this split outcome.

**Required gate/evidence:** Run LG-PRIVACY using synthetic canaries, export parse/integrity checks, negative authorization tests and backend deletion readback. FI-PRIVACY covers backups, derived indexes and interrupted jobs.

<a id="pb-031"></a>
## PB-031 — Privacy controls, retention and sensitive-content boundaries

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-02](TESTING.md#gj-02), [GJ-08](TESTING.md#gj-08).

<a id="tc-pb-031-p"></a>
### TC-PB-031-P — positive

Privacy controls separately govern capture, memory, retention and diagnostics; show what leaves the Mac before use. Local data uses GRDB under Application Support/HeyPebbi and secrets use Keychain. New collection stops immediately when disabled, and retention removes eligible original and derived data according to the approved policy. Run private-session save/restart tests: no durable chat/memory/unsaved artifact content, except explicitly saved outputs and disclosed minimal usage/security/safety records. Test local history retention and source revocation before the next tool request; privacy controls remain usable offline.

<a id="tc-pb-031-n"></a>
### TC-PB-031-N — negative

Canary secrets, secure fields, excluded windows and raw audio/screenshots never appear in telemetry or support exports by default. Failed redaction blocks sending diagnostics. Changing a retention toggle does not silently claim provider-side deletion; cloud sync of local content must not exist in this architecture. No hidden clipboard/app tracking, unsupported “nothing leaves this Mac” claim or new optional telemetry after revocation is allowed.

**Required gate/evidence:** LG-PRIVACY combines network payload inspection, local/server retention sweeps, Keychain review and real permission revocation. FI-PRIVACY verifies logs, exports, caches and interrupted deletion.

**Mandatory repair fixtures:** [TC-REPAIR-DEVICE](TESTING.md#tc-repair-device), [TC-REPAIR-ARTIFACT](TESTING.md#tc-repair-artifact). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-032"></a>
## PB-032 — VoiceOver, keyboard, contrast and reduced motion

Required classes: **automated, manual, hardware**. Shared journeys: [GJ-01](TESTING.md#gj-01), [GJ-02](TESTING.md#gj-02), [GJ-03](TESTING.md#gj-03), [GJ-08](TESTING.md#gj-08).

<a id="tc-pb-032-p"></a>
### TC-PB-032-P — positive

Complete all essential journeys using keyboard only and VoiceOver with meaningful names, roles, values and state announcements. Focus order follows reading order and returns after sheets. Normal text meets 4.5:1, large text 3:1 and essential controls/focus indicators 3:1 contrast against actual backgrounds; material variants remain legible. Test long approval text/small windows with scrolling instead of clipped buttons, selectable transcripts and milestone announcements rather than every streamed token. Safety controls work without hover or speech.

<a id="tc-pb-032-n"></a>
### TC-PB-032-N — negative

Enable Reduce Motion, Reduce Transparency and Increase Contrast independently and together. No task/control disappears, large spring/parallax motion persists, focus trap occurs or state relies only on color/animation/audio. Rapidly reverse perch/sheet motion: input remains usable and transition starts from the presentation state without a jump. The mascot is never the sole state signal; disabled/error/selected states must remain distinguishable under all accessibility settings.

**Required gate/evidence:** LG-ACCESSIBILITY requires real VoiceOver plus contrast measurements and native accessibility-tree checks across light/dark, disabled/error/loading states. Screenshots alone cannot pass it.

**Mandatory repair fixtures:** [TC-REPAIR-NATIVE-APPROVAL](TESTING.md#tc-repair-native-approval). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-033"></a>
## PB-033 — Multi-display, notchless, Spaces and scaling behavior

Required classes: **automated, manual, hardware**. Shared journeys: [GJ-02](TESTING.md#gj-02), [GJ-09](TESTING.md#gj-09).

<a id="tc-pb-033-p"></a>
### TC-PB-033-P — positive

Use built-in notched and notchless screens plus external displays; move Home/perch/guides across mixed scaling and coordinate origins. Enter/exit fullscreen Spaces and switch active displays; controls remain visible in safe areas, overlays remain bound to the intended target and no new space is forced unexpectedly. Test explicit perch-display versus follow-active-display policy, menu-bar auto-hide, negative screen origins and deterministic nearest-visible-display recovery.

<a id="tc-pb-033-n"></a>
### TC-PB-033-N — negative

Hot-unplug the display hosting a perch or active guide, change resolution/scaling or move the target to another Space. Recover to an accessible display or pause with target re-selection; no invisible windows, stranded approval dialogs, misdirected pointers or focus theft occur. A background completion cannot switch Spaces; no hardcoded single-resolution coordinate mapping is acceptable.

**Required gate/evidence:** LG-NATIVE includes physical mixed-display and fullscreen Spaces tests on both architectures; FI-DISPLAY verifies bounds and presentation behavior, not only a simulated screen size.

<a id="pb-034"></a>
## PB-034 — Audio devices, Bluetooth, interruption and mic recovery

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-02](TESTING.md#gj-02), [GJ-03](TESTING.md#gj-03).

<a id="tc-pb-034-p"></a>
### TC-PB-034-P — positive

Use built-in, wired/USB and Bluetooth input/output choices; start, interrupt and stop voice/dictation without leaked capture. Report route changes and sample-format changes; explicitly recover from device loss. Barge-in stops queued prior speech while preserving correct transcript and separate task state. Test detected silence, format mismatch and pre-roll against audible garbage. Explicit preauthorized mic fallback is permitted only when visibly indicated; otherwise recovery needs new consent. Muted output uses text, not clipboard replacement.

<a id="tc-pb-034-n"></a>
### TC-PB-034-N — negative

Bluetooth profile switching, unplug/replug, call takeover, device permission revocation and lock/sleep cannot produce stale audio playback, capture from an unapproved replacement mic or duplicated transcript insertion. If private output becomes unavailable, pause before routing to speakers. A stopped/cancelled session must never reopen when a device returns; finalized words cannot be silently erased by a Bluetooth cold start or profile switch.

**Required gate/evidence:** LG-AUDIO needs real devices and working live voice/dictation providers; transport-only and prerecorded fixture tests remain useful but do not clear the blocked live audio gate. FI-AUDIO and FI-VOICE apply.

**Mandatory repair fixtures:** [TC-REPAIR-AUDIO-OWNER](TESTING.md#tc-repair-audio-owner). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-035"></a>
## PB-035 — Offline, sleep/wake and app-crash recovery

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-05](TESTING.md#gj-05), [GJ-07](TESTING.md#gj-07).

<a id="tc-pb-035-p"></a>
### TC-PB-035-P — positive

Lose network, sleep and kill the app at controlled task boundaries. Persist intent and ordered journal state; on restart first mark formerly active attempts interrupted, revalidate account/permissions and reconcile uncertain effects before retry. Offline local navigation/search/export stay available where no server capability is required.

<a id="tc-pb-035-n"></a>
### TC-PB-035-N — negative

No automatic replay of an uncertain payment/message/file overwrite occurs. Expired grants or stale provider sessions are not resumed as valid. Wake does not start covert capture, flood routine runs or hide failed/partial work. A corrupt database enters a safe recovery path without replacing it with an empty success state.

**Required gate/evidence:** Run FI-NETWORK, FI-SLEEP, FI-CRASH and FI-DUPLICATE on physical hosts with controlled external effect readback and GRDB migration/journal assertions.

**Mandatory repair fixtures:** [TC-REPAIR-AUDIO-OWNER](TESTING.md#tc-repair-audio-owner), [TC-REPAIR-DICTATION-CANCEL](TESTING.md#tc-repair-dictation-cancel). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-036"></a>
## PB-036 — Secure updates, signing and release rollback

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-09](TESTING.md#gj-09).

<a id="tc-pb-036-p"></a>
### TC-PB-036-P — positive

Verify Developer ID, hardened runtime, notarized/stapled DMG and Sparkle 2 signed feed/artifact from the selected release channel. Update a previous supported build and retain app data. Demonstrate a signed rollback or higher-version corrective release with compatible schema/API before increasing distribution.

<a id="tc-pb-036-n"></a>
### TC-PB-036-N — negative

Tampered feed, artifact hash/signature mismatch, wrong team/bundle, untrusted/revoked signing chain or invalid secure timestamp, downgrade attack, interrupted download and incompatible schema are rejected. Never disable Gatekeeper, notarization, TLS or Sparkle signature checks to finish a build; never restore an old database that would replay reconciled external effects.

**Required gate/evidence:** LG-DISTRIBUTION requires real signing authority, public delivery and physical fresh/upgrade installs. FI-UPDATE includes a rehearsed rollback with preserved journal and account state.

<a id="pb-037"></a>
## PB-037 — Diagnostics, support and redacted telemetry

Required classes: **automated, manual, live**. Shared journeys: [GJ-08](TESTING.md#gj-08), [GJ-09](TESTING.md#gj-09).

<a id="tc-pb-037-p"></a>
### TC-PB-037-P — positive

Generate an opt-in diagnostics bundle with build/OS, redacted state transitions and correlation IDs; preview contents before sharing. Support can correlate a task/provider incident without seeing secrets or raw user content. Respect telemetry choice and published retention; user-facing errors provide a safe recovery and support path.

<a id="tc-pb-037-n"></a>
### TC-PB-037-N — negative

Inject secrets and sensitive content into errors, URLs, filenames, transcripts and tool output. Redaction removes or excludes them before persistence/export; failure blocks upload. Telemetry disabled means no optional telemetry transmission. A support operator cannot request credentials or silently enable screen/mic collection.

**Required gate/evidence:** LG-SUPPORT and LG-PRIVACY use canary scans of actual bundle/network/log outputs; exercise incident correlation against an authorized staging failure without storing raw provider payloads.

<a id="pb-038"></a>
## PB-038 — Resource budgets, latency and idle efficiency

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-02](TESTING.md#gj-02), [GJ-05](TESTING.md#gj-05).

<a id="tc-pb-038-p"></a>
### TC-PB-038-P — positive

Measure cold launch, interaction acknowledgement, speech onset/interruption, idle resource use and saturated work against the versioned budgets in TESTING.md. Keep work off the main actor, bound buffers/queues/logs and release mic/capture/network when idle or stopped. Record distributions and worst cases, not only one favorable run. Measure warm/cold voice, dictation, Home switching and first meaningful progress separately, with long-history/large-file and thermal/power-mode conditions. Offscreen/hidden decorative animation must stop.

<a id="tc-pb-038-n"></a>
### TC-PB-038-N — negative

Memory pressure, oversized attachments, slow consumer, stalled stream and output flood cannot yield unbounded growth, UI hangs or silent accepted-work loss. When a budget is exceeded, apply backpressure and show recoverable degraded state; no security or data integrity check is skipped to improve latency. Resource expansion cannot silently authorize cloud spending, and throttled slow work cannot be relabeled succeeded to satisfy a latency target.

**Required gate/evidence:** LG-PERFORMANCE requires Instruments/energy evidence on Intel and Apple Silicon and actual selected providers for network-dependent latency. Fixtures establish algorithmic limits only; FI-MEMORY-PRESSURE and FI-QUEUE apply.

**Mandatory repair fixtures:** [TC-REPAIR-MESSAGE-BYTES](TESTING.md#tc-repair-message-bytes), [TC-REPAIR-TOKEN-BUDGET](TESTING.md#tc-repair-token-budget). Each linked assertion is required in addition to the P/N cases above.

<a id="pb-039"></a>
## PB-039 — Support, privacy, account and download web surfaces

Required classes: **automated, manual, live**. Shared journeys: [GJ-08](TESTING.md#gj-08), [GJ-09](TESTING.md#gj-09).

<a id="tc-pb-039-p"></a>
### TC-PB-039-P — positive

Publish original Pebbi-styled support, privacy, account and download pages using the chosen backend surface. Download advertises the actual signed release, minimum OS and supported architectures; account actions require authenticated identity. Navigation, keyboard access and legal links work at supported viewport sizes. Exercise anonymous and authenticated pages, privacy/support/legal links, actual fallback contact and configured/unconfigured states. Failed sign-in preserves a safe intended return destination.

<a id="tc-pb-039-n"></a>
### TC-PB-039-N — negative

Before a verified build exists, no working-app download/availability claim appears. Unapproved prices cannot be sold; stale release links, cross-account exports, unsafe redirect parameters and inaccessible forms block launch. Domain selection is not proof of registration or trademark clearance. No fake testimonials, legal operator/contact or dummy download is allowed; public account state cannot leak another user's data.

**Required gate/evidence:** LG-WEB requires deployed HTTPS pages, authorized domain ownership, actual artifact download and authenticated account flow; the static brand board cannot satisfy this requirement.

<a id="pb-040"></a>
## PB-040 — Complete end-to-end acceptance and honest release gating

Required classes: **automated, manual, live, hardware**. Shared journeys: [GJ-01](TESTING.md#gj-01), [GJ-02](TESTING.md#gj-02), [GJ-03](TESTING.md#gj-03), [GJ-04](TESTING.md#gj-04), [GJ-05](TESTING.md#gj-05), [GJ-06](TESTING.md#gj-06), [GJ-07](TESTING.md#gj-07), [GJ-08](TESTING.md#gj-08), [GJ-09](TESTING.md#gj-09).

<a id="tc-pb-040-p"></a>
### TC-PB-040-P — positive

For the exact release candidate, every PB-001 through PB-040 has linked positive and negative evidence, all required golden journeys and failure injections are run, and launch-gate owners sign a manifest tying results to app/backend/extension/configuration versions. Re-run invalidated gates after material changes. Include every shared integration-repair fixture linked in coverage, with real boundary observations rather than schema-only checks. A single all-gates-passed decision authorizes the complete product after isolated pre-release verification; continuous monitoring and withdrawal/corrective-release controls do not require staged public-cohort promotion.

<a id="tc-pb-040-n"></a>
### TC-PB-040-N — negative

Any missing evidence, live input, required architecture/device, security review or rollback rehearsal keeps release BLOCKED. A docs validator, catalog metadata, fixture demo, audited Astra response or successful build cannot substitute for complete product acceptance. No requirement is dropped to claim completion.

**Required gate/evidence:** Use every LG gate, the exact coverage index and RELEASE.md evidence rules. This repository currently provides specifications only; no application test or launch gate is asserted to have passed.

**Mandatory repair fixtures:** [TC-REPAIR-DEVICE](TESTING.md#tc-repair-device), [TC-REPAIR-ARTIFACT](TESTING.md#tc-repair-artifact), [TC-REPAIR-AUDIO-OWNER](TESTING.md#tc-repair-audio-owner), [TC-REPAIR-MESSAGE-BYTES](TESTING.md#tc-repair-message-bytes), [TC-REPAIR-TOKEN-BUDGET](TESTING.md#tc-repair-token-budget), [TC-REPAIR-NATIVE-APPROVAL](TESTING.md#tc-repair-native-approval), [TC-REPAIR-DICTATION-CANCEL](TESTING.md#tc-repair-dictation-cancel). Each linked assertion is required in addition to the P/N cases above.
