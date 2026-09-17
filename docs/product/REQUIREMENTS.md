# Pebbi — complete observable requirements

Normative; documentation only. The [contract](../CONTRACT.md) takes precedence. Every PB identifier below is mandatory and maps to the same identifier in [Acceptance](../quality/ACCEPTANCE.md) and [coverage.json](../quality/coverage.json). An acceptance reference is an obligation, not evidence that a test passed. [App flows](APP-FLOWS.md) define exact journeys; [Screens](../design/SCREENS.md) supplies visual treatment.

## Common rules inherited by every PB

**Identity and artifacts.** Preserve opaque IDs and original user input. Store task lineage, draft ownership, source provenance, approvals and output evidence locally according to [Data model](../engineering/DATA-MODEL.md). Use the contract's camelCase, UUID, timestamp and event conventions. Render a human label, never an internal ID in place of essential meaning.

**State authority.** Task: `queued`, `running`, `waitingForApproval`, `waitingForInput`, `waitingForConnection`, `cancelling`, `cancelled`, `succeeded`, `failed`, `interrupted`. Voice: `idle`, `connecting`, `listening`, `thinking`, `speaking`, `interrupted`, `unavailable`, `failed`. Dictation: `idle`, `capturing`, `transcribing`, `reviewing`, `inserting`, `completed`, `cancelled`, `failed`. Connection: `disconnected`, `connecting`, `ready`, `expired`, `degraded`, `failed`. Routine: `active`, `paused`, `blocked`, `archived`. Conversation read/archive/pin flags and surface presentation are not additional task states. Retry is a new attempt, not `failed` → `running` on the same attempt.

**Focus rules.** F0: a background event never activates an app, replaces the clipboard, switches Spaces or focuses a composer. F1: explicit Home/menu/shortcut activation may focus the selected control and must restore the prior app when dismissed, if that app still exists. F2: voice hold does not claim text focus; capture the originating app/field and do not route dictated text to a visible-but-background Home. F3: external insertion/action must revalidate app, window, field/tab and resource identity immediately before execution. F4: approval appears without stealing focus; user activation brings its native controls into focus. F5: foreground pointer/keyboard takeover requires an explicit bounded approval, an indicator and a reachable Stop. Escape is an emergency stop for the active takeover, never for unrelated tasks. F6: overlays are click-through except their explicit controls; Escape dismisses the current presentation, not an unrelated task. F7: accessibility focus follows user navigation and deliberate state changes, never every streamed token or background status event.

**Approval rules.** A0: local navigation, drafts and explicitly requested reads inside an already authorized scope do not require repetitive confirmation. A1: action outside a granted scope must preview app/connector, operation, resource, relevant data disclosure and consequence; decisions are exactly `allowOnce`, `allowForScope`, `deny`. A2: `allowForScope` is bounded by user, tool class, resource and expiry, is revocable, and never includes payments, credentials, destructive bulk operations, publishing or outbound messages. Those require a fresh exact preview and approval. A3: credentials, OS permission consent and payment authentication are entered/confirmed by the user; Pebbi never automates their entry or pretends to bypass them. A4: approval is bound to an immutable action version; editing a recipient, amount, destination, command, payload or scope invalidates it. A5: “do it” only resolves to one visible/current named proposal; ambiguity becomes `waitingForInput`. A tool allowlist is not an OS sandbox.

**Verification.** Persist external operation intent before dispatch. After a write, read the exact target or obtain a trustworthy authoritative receipt; distinguish an accepted request from a verified result. Unknown side effects enter reconciliation and are never blindly repeated. Durable success requires output artifacts plus evidence. No fake live response, hidden fallback model or silent scope reduction is permitted. Actual network/provider/OS/credential constraints are visible blockers.

<a id="pb-001"></a>
## PB-001 — Native installation, launch, update and quit

- **Required:** A signed/notarized DMG installs a native macOS 14.2+ app with clear Applications placement. Relaunch reopens existing local data without duplicate instances. Menu bar, Dock option and Home can launch the same account store. Quit stops capture, audio, browser helper work and local scheduling; active attempts are journaled for recovery. Updates expose availability, download and install/relaunch separately.
- **Inputs → outputs:** DMG, installed version, local store and user launch/quit intent → one app session, restored navigation, update result and recoverable task journal.
- **States, focus, approvals:** Active tasks follow PB-017 before Quit; unexpected exit follows PB-035 to `interrupted`. F0/F1; installation/relaunch is explicit user intent, OS authorization is A3.
- **Unhappy paths:** Unsupported OS explains minimum without starting capture; corrupted signature rejects installation; disk full preserves previous install/data; a pending quit reports outstanding side effects instead of hiding them.
- **Non-goals:** App Store release, automatic OS-security bypass, daemon execution after Quit.
- **Acceptance:** [PB-001](../quality/ACCEPTANCE.md): install/launch on supported targets; reopen same data; verify no owned capture/scheduler/helper survives Quit. [Flow](APP-FLOWS.md#pb-001).

<a id="pb-002"></a>
## PB-002 — Account sign-in, sign-out and device sessions

- **Required:** System-browser Entra External ID OIDC/PKCE sign-in validates the returned identity; Home shows the signed-in account. Device sessions can be listed and revoked. Sign-out removes session material from Keychain, stops authenticated new work, and locks retained local account data against another account. Explain whether local data remains; deletion is separate.
- **Inputs → outputs:** Sign-in request and verified browser return → account session and device record; sign-out/revoke → revoked access and retained-or-explicitly-deleted local data.
- **States, focus, approvals:** Connection `disconnected` → `connecting` → `ready`; expired access → `expired`, dependent tasks → `waitingForConnection`. F1 only on deliberate sign-in; A3 for credential UI. Switching identity cannot reuse the previous user's grants.
- **Unhappy paths:** Cancelled browser flow returns to sign-in; stale/wrong-state callbacks are rejected; revoked devices cannot continue provider requests; network failure never yields a signed-in success banner.
- **Non-goals:** Shared account folders, cross-device content sync, credentials typed by Pebbi.
- **Acceptance:** [PB-002](../quality/ACCEPTANCE.md): valid and invalid callback; revoke current/other device; sign out/in as a different identity without data leakage. [Flow](APP-FLOWS.md#pb-002).

<a id="pb-003"></a>
## PB-003 — Permission onboarding and denied/revoked recovery

- **Required:** Explain Microphone, Screen Recording, Accessibility and Notifications individually at point of need. Detect each permission independently; offer native settings guidance and recheck. Skipping one capability must not prevent typed/local use. Permission revocation closes the affected capture/action path promptly.
- **Inputs → outputs:** Requested capability and actual OS grants → capability-specific readiness and actionable recovery card; never infer permission from a dismissed prompt.
- **States, focus, approvals:** Denied mic maps voice to `unavailable`; denied action permission maps its task to `waitingForInput`; provider connections are not mislabeled as OS grants. F1/F4; A3 exclusively for OS consent.
- **Unhappy paths:** Settings opens to a different page, permission requires relaunch, managed policy disallows grant, or permission changes during work: show the detected state and manual path; avoid duplicate prompts.
- **Non-goals:** Mandatory blanket permission grant, keystroke monitoring, bypass of managed Mac policies.
- **Acceptance:** [PB-003](../quality/ACCEPTANCE.md): deny/retry each grant; revoke during capture; skip all optional permissions and use local Home. [Flow](APP-FLOWS.md#pb-003).

<a id="pb-004"></a>
## PB-004 — Personalization interview and first Pebbis

- **Required:** Optional interview asks name/pronunciation preference, work context, useful help and boundaries. Every answer is skippable/editable. Show proposed memory and jobs before saving. Create default Pebbi plus up to two user-confirmed tailored Pebbis; manual creation remains available without models. Tour demonstrates talk/type, capture scope, a pointer and dictation review in a safe sample field, never a real outbound message.
- **Inputs → outputs:** Optional answers, original appearance selection and explicit confirmation → profile, approved memory, Pebbis and onboarding completion marker.
- **States, focus, approvals:** AI turns use PB-007; missing provider is `unavailable`/`waitingForConnection`, not invented personalization. F1/F7; A0 for manual setup, A1 for memory confirmation. Any separate onboarding allowance must be server configured and identified, not billed as undisclosed normal work.
- **Unhappy paths:** Cancel mid-interview retains only saved answers; relaunch resumes; exhausted setup allowance offers manual form; Skip tour stops speech and clears drawings.
- **Non-goals:** Compulsory sensitive profiling, copied character families, forced paid checkout.
- **Acceptance:** [PB-004](../quality/ACCEPTANCE.md): complete voice and keyboard paths; skip/offline manual path; verify unapproved personal facts never enter memory. [Flow](APP-FLOWS.md#pb-004).

<a id="pb-005"></a>
## PB-005 — Menu bar, top-edge perch and full Home window

- **Required:** All three entry points reach the same selected Pebbi and drafts. Perch summarizes named work/approval without hiding Home's controls. Expand/detach and return preserve navigation, scroll and open artifact. Escape closes the expanded perch and suppresses immediate hover reopening until the pointer leaves its activation region. Opening a reply link makes room for the external destination.
- **Inputs → outputs:** User surface command and saved view state → coherent selected conversation and usable controls on the chosen display.
- **States, focus, approvals:** Presentation changes never change task state. F0/F1/F6/F7; A0. Pending billing/approval sheets are not covered by the perch.
- **Unhappy paths:** Detached display moves Home to visible usable bounds; hidden Dock cannot strand the app; reopening a missing conversation offers recovery with disclosure.
- **Non-goals:** Hardware-notch dependency, a cursor-following reference character, full web-shell UI.
- **Acceptance:** [PB-005](../quality/ACCEPTANCE.md): switch all surfaces with a draft and running task; Escape/hover behavior; unobscured approval and billing. [Flow](APP-FLOWS.md#pb-005).

<a id="pb-006"></a>
## PB-006 — Global shortcuts and focus-safe activation

- **Required:** Offer configurable Home, hold-to-talk, hold-to-dictate and hands-free dictation bindings with collision detection and accessible button equivalents. Defaults: Home Control–Command–A; talk Control–Option hold; dictate Fn–Control hold; hands-free Fn–Control double-tap. If the OS cannot deliver a binding reliably, report it and require an alternate rather than silently stealing another command. Capture the origin before showing UI; ambiguous routing asks which Pebbi.
- **Inputs → outputs:** Binding and key gesture → one intended action, origin token and reversible activation; no duplicate turns from key repeat.
- **States, focus, approvals:** Voice/dictation start only on valid gestures; hold release ends capture, not the underlying task. F1/F2/F3; A0, A3 for OS permissions.
- **Unhappy paths:** Secure fields suppress dictation; active menu/shortcut recorder does not swallow Escape or submit work; Caps Lock, layouts and external keyboards retain consistent routing.
- **Non-goals:** Global keylogging, arbitrary hotkeys guaranteed across all OS configurations.
- **Acceptance:** [PB-006](../quality/ACCEPTANCE.md): held and double-tap gestures; shortcut conflict; background Home never receives another app's text. [Flow](APP-FLOWS.md#pb-006).

<a id="pb-007"></a>
## PB-007 — Real-time spoken conversation and typed equivalent

- **Required:** Selected `gpt-realtime-2.1` powers live conversation when actually available; typed interaction and reasoning use the configured role contract, not a hidden substitute. Display transcript, named Pebbi and streaming response. Typed users can invoke the same tools and approvals. Barge-in stops current speech while retaining the response and does not cancel a task. Requests for work create an identifiable task, never an invisible handoff.
- **Inputs → outputs:** User audio or typed message and approved context → transcript/message, response, optional task reference and metered usage.
- **States, focus, approvals:** Voice `idle` → `connecting` → `listening` → `thinking` → `speaking` → `idle`; barge-in → `interrupted` then `listening` only while the session is still explicitly active. F0/F2/F7; A1/A2 before tools exceed authorized read scope.
- **Unhappy paths:** No audio, timeout, provider error and disconnected role are visible; partial response remains labeled; silent output remains readable; no spontaneous always-listening session.
- **Non-goals:** Guaranteed unrestricted languages, synthetic results passed as live, talk interruption treated as task cancellation.
- **Acceptance:** [PB-007](../quality/ACCEPTANCE.md): live multi-turn/typed parity; barge-in with task continuing; unavailable realtime does not fake a reply. [Flow](APP-FLOWS.md#pb-007).

<a id="pb-008"></a>
## PB-008 — Explicit screen capture scope and screen understanding

- **Required:** Screen context is off until the user selects a window, display or region for a request. Show chosen scope before sending and a capture indicator while active. Allow user-drawn focus marks, recapture and removal. Read visible content faithfully; use files/DOM for full content when separately authorized. Raw captures are ephemeral and excluded from history/diagnostics unless the user explicitly exports a capture.
- **Inputs → outputs:** Selected scope, permission, user question and optional marks → ephemeral capture, provenance-bearing analysis and textual answer.
- **States, focus, approvals:** Screen reasoning is a task `queued` → `running` → verified `succeeded`; missing scope/permission → `waitingForInput`. F0/F3/F6; A1 for capture/data disclosure, refreshed when scope changes.
- **Unhappy paths:** Window closes, sensitive content appears, display topology changes or capture is blank: invalidate old geometry and ask to recapture; do not infer unseen content.
- **Non-goals:** Continuous surveillance, hidden whole-desktop capture, automatic password/secret collection.
- **Acceptance:** [PB-008](../quality/ACCEPTANCE.md): correct selected scope only; revoke during capture; demonstrate no raw screenshot in persistent logs. [Flow](APP-FLOWS.md#pb-008).

<a id="pb-009"></a>
## PB-009 — Drawing, pointing and resumable guided walkthroughs

- **Required:** Guidance combines text with original Pebbi annotations anchored to verified display/window coordinates or semantic targets. Each step has goal, target, expected result and completion evidence. Provide Next, Back, Pause, Resume and End; manual work pauses without losing goal or completed steps. Target changes require reinspection. Support procedures longer than fifteen steps by continuation, not silent truncation.
- **Inputs → outputs:** Goal, approved scope and inspected targets → saved walkthrough progress and temporary overlay marks; user may add circles as context.
- **States, focus, approvals:** Task `running` → `waitingForInput` at manual step → `running` after confirmation/reinspection; End → `cancelling` → `cancelled`, retaining progress. F0/F6/F7; guidance does not imply A1 authority to click.
- **Unhappy paths:** Missing/moved control removes obsolete marks; uncertain completion asks, never advances by elapsed time; Escape clears overlay and stops its speech without cancelling unrelated work.
- **Non-goals:** Unverified coordinate clicking, drawings as the only instruction, copied illustration language.
- **Acceptance:** [PB-009](../quality/ACCEPTANCE.md): long procedure; pause/relaunch/resume; moved target; keyboard and VoiceOver equivalent. [Flow](APP-FLOWS.md#pb-009).

<a id="pb-010"></a>
## PB-010 — Dictation, review and focus-safe insertion

- **Required:** Use selected `gpt-live-transcribe` only when operational. Preserve meaning; punctuation cleanup never invents content. Show editable transcript and explicit destination before insertion; default is review-first, with user-enabled direct insertion allowed only for revalidated non-sensitive fields. Preserve partial transcription through interruption. Support language preference and an explicitly edited personal dictionary without watching global typing. Never press Return to submit; terminal/shell destinations collapse line breaks and require preview.
- **Inputs → outputs:** Audio, language preference, user edits and origin field → reviewed transcript, local recovery draft and verified insertion or explicit copy option.
- **States, focus, approvals:** `idle` → `capturing` → `transcribing` → `reviewing` → `inserting` → `completed`; Cancel → `cancelled`; errors → `failed`, retained transcript available for a new attempt. F2/F3; A0 for confirmed field insertion, A2 for any separate send/execute action.
- **Unhappy paths:** Changed focus, missing field, secure input, disconnected provider or uncertain insert keeps review visible. Clipboard fallback is opt-in and restore is conditional on unchanged clipboard ownership; never report insertion after copy alone.
- **Non-goals:** Automatic message sending/command execution, implicit clipboard overwrite, hidden model substitution.
- **Acceptance:** [PB-010](../quality/ACCEPTANCE.md): native/browser/terminal insertion; focus race; long recording interrupted by route change; unavailable transcription. [Flow](APP-FLOWS.md#pb-010).

<a id="pb-011"></a>
## PB-011 — Persistent Pebbi creation, editing and appearance

- **Required:** Create through a form or conversational proposal; show name, job, original appearance and workspace before Save. Default assistant is named Pebbi. Rename/edit preserves identity, conversations and task history. List order remains stable while tasks run; pinning is explicit. Archive confirms routine pausing and handling of active work; unarchive never silently resumes routines.
- **Inputs → outputs:** Confirmed profile fields → durable Pebbi with isolated context/workspace and editable appearance.
- **States, focus, approvals:** Profile changes do not mutate running attempt instructions; amendments use PB-016. Archive sets associated routines to `paused`; active attempts need explicit stop or finish decision. F1/F7; A0 for local save, A1 for consequential archive choice.
- **Unhappy paths:** Duplicate name allowed with disambiguating job; empty name/job prevented with inline errors; failed save preserves draft; missing conversation offers a new linked conversation, not repeated failure.
- **Non-goals:** Reusing reference character designs; shared memory by default; silent deletion of previous work.
- **Acceptance:** [PB-011](../quality/ACCEPTANCE.md): create/edit/relaunch; archive during work; duplicate-name spoken routing. [Flow](APP-FLOWS.md#pb-011).

<a id="pb-012"></a>
## PB-012 — Conversations, search, archive, unread and pinning

- **Required:** New conversation, local full-text search, archive/unarchive, pin/unpin, mark read/unread and delete are reachable by keyboard and native menus. Preserve independent draft, attachments, scroll position and open preview per conversation. Older messages paginate without changing position; new messages while reading above the end expose Jump to latest. Explicit Mark unread remains until explicit read action or leaving and reopening that conversation.
- **Inputs → outputs:** Query/navigation/edit commands → stable conversation results, persisted view state and read/archive/pin flags.
- **States, focus, approvals:** Opening/read flag changes do not alter task state. F0/F1/F7; A0 for archive/read, confirmation before destructive local deletion with active-task impact disclosed.
- **Unhappy paths:** Deleted/missing conversation is detected; offer a fresh conversation preserving Pebbi memory and known task references, clearly label inaccessible history. Archive cannot lose drafts or hide outstanding approvals.
- **Non-goals:** Server-backed chat sync, automatic unread clearing on every background token, conflating conversation archive with cancellation.
- **Acceptance:** [PB-012](../quality/ACCEPTANCE.md): long-history search/pagination; mark unread while open; restart draft/preview restoration; missing history recovery. [Flow](APP-FLOWS.md#pb-012).

<a id="pb-013"></a>
## PB-013 — Memory inspect, edit, forget and context compaction

- **Required:** Profile shows every durable memory with scope, provenance and last change. User may add/edit/forget and disable future proposals. Save model-proposed facts only after review. Global preferences versus Pebbi-specific facts are explicit. Compaction preserves goal, constraints, approved facts, task links, source references and unresolved questions, with a visible summary the user can correct. Forget excludes the fact from subsequent context and derived summaries without pretending to delete unrelated original chats.
- **Inputs → outputs:** Approved fact/edit or long context → versioned memory/summary and traceable context manifest.
- **States, focus, approvals:** Context assembly occurs before task `running`; insufficient/rejected context → `waitingForInput`; compaction failure leaves original history usable. F0/F7; A1 for proposed memories, A0 for explicit user edits.
- **Unhappy paths:** Conflicting facts ask which to retain; secrets/sensitive inferences rejected; stale compaction is invalidated after edits; unavailable original source remains marked unavailable.
- **Non-goals:** Invisible psychological profiles, certainty from inferred identity, immutable or shared-by-default memory.
- **Acceptance:** [PB-013](../quality/ACCEPTANCE.md): edit/forget reflected in next turn; long conversation continues; compaction retains pending approvals and citations. [Flow](APP-FLOWS.md#pb-013).

<a id="pb-014"></a>
## PB-014 — Attachments, whole-document reading and previews

- **Required:** Attach via picker, drag/drop and intentional paste, including attachment-only messages. Validate allowed types/size against published runtime limits before upload/processing. Show source, size and ingestion status. Read all supported document pages/sections with a coverage manifest; inaccessible/encrypted/unsupported portions are explicit. Preview text/Markdown, PDF and images in Home, with Quick Look/open in app/Finder; changing Markdown refreshes without stealing scroll or executing embedded content.
- **Inputs → outputs:** Granted file URLs or pasted content → managed attachment, extraction coverage, preview and cited answer.
- **States, focus, approvals:** Reading task `queued` → `running`; password-needed document → `waitingForInput` with manual unlock; unsupported extraction → `failed` or explicit partial result. F0/F1/F7; A1 for sending file contents to model, A0 for local preview.
- **Unhappy paths:** Drop failure keeps composer usable; deleted source retains managed copy if imported; duplicate attachments identified; insufficient disk/provider limit fails before claiming complete reading.
- **Non-goals:** Reading only visible pages while claiming whole document; document macro/script execution; unapproved broad folder traversal.
- **Acceptance:** [PB-014](../quality/ACCEPTANCE.md): all three attach routes; whole-document sentinel on last page; encrypted/malformed/oversize files; per-chat preview restoration. [Flow](APP-FLOWS.md#pb-014).

<a id="pb-015"></a>
## PB-015 — Agent task execution and truthful live progress

- **Required:** Work requests produce durable task/attempt IDs, named Pebbi, original goal, current step, elapsed/usage context and output area. Journal progress before rendering; deduplicate/order events by contract sequence. Distinguish planned, attempted and verified work in prose without inventing task states. Completed step details collapse but remain inspectable. Final response includes artifacts, evidence, uncertainty and remaining blockers.
- **Inputs → outputs:** User request, approved context and usage reservation → ordered task events, verified outputs and accounting finalization.
- **States, focus, approvals:** Start `queued` → `running`; wait states name the missing condition; only verified completion → `succeeded`. F0/F7; A1/A2 gate tools; speech acknowledgement is not proof of execution.
- **Unhappy paths:** Stream reconnect does not repeat steps; missing events are reconciled; provider error preserves partial results; a write response without readback cannot become confirmed success.
- **Non-goals:** Animated fake progress, pretending code was run, unbounded autonomous work or undocumented tools.
- **Acceptance:** [PB-015](../quality/ACCEPTANCE.md): event replay/deduplication; actual file/external target verification; truthful partial/failure completion. [Flow](APP-FLOWS.md#pb-015).

<a id="pb-016"></a>
## PB-016 — Concurrent Pebbis, queues and race-free follow-ups

- **Required:** Independent Pebbis can work concurrently within advertised execution capacity; each Pebbi has one running attempt and an ordered queue. A follow-up is atomically assigned to the current attempt at a safe input boundary or becomes a new turn after terminal completion. Preserve message order and acknowledge destination by name. “Retry it” identifies an exact task; ambiguity asks. Queued suggestions retain sources and original approved scope.
- **Inputs → outputs:** New requests/follow-ups/cancel/reorder → durable queue entries and deterministic task association.
- **States, focus, approvals:** New work `queued`; busy follow-up remains durable until consumed; missing context → `waitingForInput`. One shared desktop-control lease; waiting for it remains `queued` before work or `waitingForInput` if user mediation is needed. F0/F7; A4 invalidates grants when follow-up changes approved action.
- **Unhappy paths:** Arrival during startup/completion is never dropped; archived Pebbi requires reassign/unarchive; resource conflict cannot cause interleaved writes; duplicate submission token creates no duplicate work.
- **Non-goals:** Two tasks simultaneously typing into one field; routing solely by recency when intent is ambiguous.
- **Acceptance:** [PB-016](../quality/ACCEPTANCE.md): startup/terminal-boundary races; concurrent independent jobs; same-file/control conflict; source-carrying busy queue. [Flow](APP-FLOWS.md#pb-016).

<a id="pb-017"></a>
## PB-017 — Approval, stop, cancellation and recovery

- **Required:** Preview consequence before execution and expose `allowOnce`, eligible `allowForScope`, `deny`. Show current grants and revoke. Stop task is always reachable and distinct from Mute/Stop speaking. On Stop, cease new tool calls, cancel cancellable work, reconcile inflight side effects and retain partial artifacts with exact status. Retry creates a linked attempt after reconciliation and applicable fresh approvals.
- **Inputs → outputs:** Versioned action proposal/decision, cancellation and reconciliation evidence → grant/denial audit, terminal attempt and recoverable results.
- **States, focus, approvals:** `running` → `waitingForApproval` → `running` after valid allow; deny essential action → `waitingForInput` for alternative or explicit `cancelled`. Stop from running/waiting states → `cancelling` → `cancelled` after reconciliation; undispatched `queued` work cancels directly to `cancelled`. Crash → `interrupted`. F4/F5/F7; A1–A5.
- **Unhappy paths:** Stale approval cannot execute; failed cancellation never claims rollback; unknown send outcome stays visibly unresolved and cannot auto-retry; voice decision ambiguity remains waiting.
- **Non-goals:** Standing high-risk authority, cancellation as proof of undo, retrying unknown external writes.
- **Acceptance:** [PB-017](../quality/ACCEPTANCE.md): all decisions; stop during external write; stale/duplicate approvals; crash-before-readback reconciliation. [Flow](APP-FLOWS.md#pb-017).

<a id="pb-018"></a>
## PB-018 — Native desktop control and takeover boundaries

- **Required:** Native AX semantic inspection/action targets a specific app/window/element first. Confirm capability and target; perform background-safe actions only when actually supported. If CGEvent/foreground input is necessary, disclose cursor/focus use, action bounds and affected window; obtain takeover approval and expose Stop. Reinspect after changes, verify effect and release control immediately on completion/cancel.
- **Inputs → outputs:** User goal, target identity, OS grants and action approval → bounded native action, readback evidence and control-lease release.
- **States, focus, approvals:** `running` → `waitingForApproval` for takeover or changed scope; unavailable AX → `waitingForInput`, not blind repeat. F3/F5; A1/A2/A3. Pause takeover on user interruption rather than fight the user.
- **Unhappy paths:** Element disappears, app blocks AX, secure UI or managed policy prevents action: stop and offer manual guidance; capture verification before retrying an uncertain input.
- **Non-goals:** Claiming all background clicks are possible, password/permission/payment clicking, moving the real pointer under a background label.
- **Acceptance:** [PB-018](../quality/ACCEPTANCE.md): true background AX control; foreground fallback approval; user interruption and target drift; no duplicate confirmed input. [Flow](APP-FLOWS.md#pb-018).

<a id="pb-019"></a>
## PB-019 — Browser DOM tools and user-selected sessions

- **Required:** Opt-in Chrome/Brave extension plus authenticated native-messaging helper exposes only user-selected tab or dedicated window scope. Ask which before starting browser work; show browser/profile/window/tab identity. Prefer DOM reads and semantic actions; revalidate document and element before action. Dedicated window uses the chosen profile, but never grants every tab. Setup and connection health are visible in Connections.
- **Inputs → outputs:** Browser choice, extension consent and tab/window grant → bounded DOM context, browser artifacts and action verification.
- **States, focus, approvals:** Extension connection `disconnected` → `connecting` → `ready`; expired session → `expired`, task → `waitingForConnection`. F0/F3/F5; A1/A2/A3; newly navigated domains outside grant require approval.
- **Unhappy paths:** Unsupported browser offers manual open or separately approved native control; extension missing, login wall, closed tab and navigation race stop with recovery. Do not guess login credentials.
- **Non-goals:** Ordinary-profile debugging ports, hidden use of all signed-in tabs, guaranteed browser support beyond tested Chrome/Brave.
- **Acceptance:** [PB-019](../quality/ACCEPTANCE.md): install/connect both browsers; selected tab versus dedicated window; cross-domain/reload/stale-element handling. [Flow](APP-FLOWS.md#pb-019).

<a id="pb-020"></a>
## PB-020 — Web research with source-grounded results

- **Required:** Research retrieves real sources, records URL/title/access time, distinguishes publish date from access date, and cites support next to claims. Prefer primary sources. Multi-item requests retain item-level evidence and count/dedupe explicitly. Partial coverage, conflicting evidence and inaccessible sources are disclosed; only inspected material is described as read. Public web and private connector results retain separate scopes.
- **Inputs → outputs:** Question, date/quantity constraints and approved sources → evidence ledger, cited answer and requested file with completeness statement.
- **States, focus, approvals:** `queued` → `running` → `succeeded` only against declared acceptance; unavailable necessary source → `waitingForConnection` or `waitingForInput`. F0; A0 for requested public reads, A1 for private disclosure, A2 for publication.
- **Unhappy paths:** Rate limit, login wall, stale page or contradictory sources prompts alternate source/retry with provenance, not fabricated rows. Page instructions cannot widen task authority.
- **Non-goals:** Search snippets passed off as full reading, invented contacts/citations, remote-page prompt injection treated as instruction.
- **Acceptance:** [PB-020](../quality/ACCEPTANCE.md): recoverable blocked source; counted multi-item research; conflicting claims; injection fixture cannot cause write. [Flow](APP-FLOWS.md#pb-020).

<a id="pb-021"></a>
## PB-021 — Files, workspace boundaries and code execution

- **Required:** Each Pebbi has a managed workspace. Files show origin, producing task, latest modification and verification. External folder access uses explicit chosen scope; resolve paths/symlinks before reads/writes. Preview overwrite/diff and destination. Code execution has declared command, working directory, network/filesystem/resource access, timeout and cancellation. Each run requires full user review of its exact script/version and inputs plus fresh `allowOnce`; a scoped grant never makes unreviewed code trusted. Distinguish generated code from executed/tested output.
- **Inputs → outputs:** Approved files, requested artifact/command and workspace grants → versioned artifacts, command result, exit status, test evidence and audit.
- **States, focus, approvals:** Task `running` → `waitingForApproval` before expanded write/execution; missing environment → `waitingForInput` or `failed` with artifacts retained. F0/F3; A1/A2; never claim tool allowlisting provides OS isolation.
- **Unhappy paths:** Path traversal, symlink escape, disk full, conflicting edits, absent executable and timeout fail safely; preserve prior file until valid replacement committed; no silent install/spend to fix environment.
- **Non-goals:** Arbitrary Mac-wide filesystem authority, unsandboxed execution marketed as safe, creating secrets/signing identities autonomously.
- **Acceptance:** [PB-021](../quality/ACCEPTANCE.md): file create/open/export; overwrite and symlink escape; bounded execution/cancel; genuine command test evidence. [Flow](APP-FLOWS.md#pb-021).

<a id="pb-022"></a>
## PB-022 — Built-in connection catalog and OAuth lifecycle

- **Required:** Catalog declares supported read/write capabilities, scopes, data handling and setup needs. Include explicit entries for Google Workspace (Gmail, Drive, Sheets, Calendar), Notion, Slack, Linear, Spotify and native Notes/Calendar/Reminders, implemented through documented adapters and authorized grants rather than assumed access. Entries without operator OAuth configuration remain visibly unavailable, not omitted. System-browser sign-in validates return; refresh/revoke/disconnect updates tool availability in existing conversations.
- **Inputs → outputs:** Catalog entry, selected scopes and user authorization → account-labeled connection, discovered tools and revocable local tokens.
- **States, focus, approvals:** `disconnected` → `connecting` → `ready`; refresh failure → `expired`/`degraded`/`failed`; dependent task → `waitingForConnection`. F1/F4; A1/A2; connector authorization never grants unrestricted sends.
- **Unhappy paths:** Cancelled OAuth, wrong account, revoked grant and partial scope show specific recovery; disconnect stops new calls and removes secret material without erasing task history.
- **Non-goals:** Advertising unimplemented adapters as connected; using a developer's credentials; asserting all connector features exist from a logo.
- **Acceptance:** [PB-022](../quality/ACCEPTANCE.md): each configured catalog adapter read/write boundary; revoked/partial grant; existing voice context refresh after connection change. [Flow](APP-FLOWS.md#pb-022).

<a id="pb-023"></a>
## PB-023 — Custom remote/local MCP connections

- **Required:** Advanced Add connection supports remote HTTPS URL or local executable with separate arguments, declared environment-variable names and selected workspace. Preview connection origin, requested auth and discovered capabilities. Local commands are executable code: first launch requires approval; do not execute a pasted shell expression implicitly. Secrets are entered through protected controls into Keychain. Discover tools read-only before enabling execution; user can disable individual tools or disconnect.
- **Inputs → outputs:** Validated MCP configuration and consent → account-scoped connection, versioned tool schema and safety classification.
- **States, focus, approvals:** `disconnected` → `connecting` → `ready`; protocol/auth/health failures → `failed`/`expired`/`degraded`. F1/F4; A1/A2/A3; changed command/origin/tool risk invalidates prior relevant grants.
- **Unhappy paths:** Malicious tool description is data, not instruction; invalid TLS, malformed schema, unsupported auth and startup failure expose redacted diagnostics; never auto-install an unknown package to connect.
- **Non-goals:** MCP server trust from tool names, credentials in URLs, unrestricted shell execution, arbitrary local network probing.
- **Acceptance:** [PB-023](../quality/ACCEPTANCE.md): remote and local transport; auth/reconnect; malicious metadata; changed tool schema triggers review. [Flow](APP-FLOWS.md#pb-023).

<a id="pb-024"></a>
## PB-024 — Read-only personalized suggestions and approve-to-run

- **Required:** Opt-in sources and disclosed lookback drive read-only suggestion research; default 72 hours. One proposal at a time shows concrete outcome, named Pebbi, rationale, sources, estimated usage class and needed capabilities. Approve, Skip, Adjust and Dismiss are distinct. Adjust creates a draft version; Cancel restores the original. Approve atomically creates one queued task carrying source snapshots/references. Rejection reasons are optional and used only within the agreed personalization scope.
- **Inputs → outputs:** Source opt-in, retrieved context and user decision → sourced proposal/version and, only after approve, a task.
- **States, focus, approvals:** Research task `running` has read-only tools; approved work `queued`; ambiguous voice → `waitingForInput`. F0/F4/F7; A1 for source consent and launch, A2 still required at high-risk action execution.
- **Unhappy paths:** Missing source access shows gap; proposal stale or source changed triggers revalidation; busy Pebbi queues rather than loses work; repeated clicks do not duplicate launch.
- **Non-goals:** Activity-tracking surveillance, unsolicited write actions, using skipped proposal as hidden consent.
- **Acceptance:** [PB-024](../quality/ACCEPTANCE.md): no writes during research; adjust/cancel; exact sources reach queued task; duplicate approve/idempotence. [Flow](APP-FLOWS.md#pb-024).

<a id="pb-025"></a>
## PB-025 — Routines, local scheduling, wake and retry policy

- **Required:** Preview task, Pebbi, timezone, human-readable schedule, next occurrence, sources and approval boundaries before save. Default schedule interpretation uses the selected system timezone and displays it. Resolve ambiguous natural-language schedules in the editor. Run now, pause, resume and archive/delete are accessible with history. Runs occur only while app open; sleep/offline/busy periods coalesce to one catch-up, never a backlog. Three consecutive failed occurrences after bounded retries pause the routine and expose reason; success resets streak. Each occurrence allows at most two additional safe attempts within fifteen minutes and its approved usage ceiling. Waiting is not failure. Closed-app backlog is skipped on launch, with explicit Run now available.
- **Inputs → outputs:** Confirmed repeat-task definition → routine and ordered run history, local next-due calculation and silent conversation results.
- **States, focus, approvals:** `active`, `paused`, `blocked`, `archived`; missing dependency → `blocked`; explicit resume rechecks to `active`. Task attempts use normal states/approvals. F0/F4; A1 for schedule/source scope, A2 for each high-risk side effect.
- **Unhappy paths:** DST repeats execute at most once per occurrence; nonexistent wall time advances to next valid local time; timezone change previews recalculation; no retries on denied actions or unknown writes.
- **Non-goals:** Cloud scheduling, running after Quit, unlimited credit-consuming retries, archive auto-resume.
- **Acceptance:** [PB-025](../quality/ACCEPTANCE.md): sleep/offline coalescing; DST/timezone; three failures; archive Pebbi pauses routines; high-risk scheduled action still waits. [Flow](APP-FLOWS.md#pb-025).

<a id="pb-026"></a>
## PB-026 — Notifications, Focus/call suppression and unread delivery

- **Required:** Routine results arrive silently in conversation with unread marker. Optional task sounds, approval invitations and suggestion greetings honor settings, Focus and available call/screen-share signals. Always expose manual Quiet mode because detection is incomplete. Notification payloads omit sensitive content on lock screen by default. Opening a result marks the relevant conversation read; explicit Mark unread is respected. Suppressed greeting is coalesced and dropped after suggestions opened/dismissed.
- **Inputs → outputs:** Task/result/approval event and attention policy → in-app status, optional notification and persistent unread state.
- **States, focus, approvals:** Delivery never alters underlying task or routine state. F0/F4/F7; A3 for OS notification permission; A0 for quiet preference.
- **Unhappy paths:** Permission denied falls back to in-app unread; dropped sound never loses result; after sleep do not replay old chimes/greetings; active Focus does not conceal a waiting approval from Home.
- **Non-goals:** Guaranteed call detection, spoken routine completion, focus-stealing banners or exposing full documents in notifications.
- **Acceptance:** [PB-026](../quality/ACCEPTANCE.md): Focus/call/manual quiet matrix; unread persistence; no late notification storm. [Flow](APP-FLOWS.md#pb-026).

<a id="pb-027"></a>
## PB-027 — Plans, metering, reservations and billing changes

- **Required:** Nest, Studio and Constellation display only server-configured prices, currency, billing interval, entitlements and reset rules. Reserve usage before metered work; finalize trusted actual usage server-side; expose reserved versus consumed separately. Hosted Checkout/Portal is explicitly opened by the user. Plan change is confirmed from authoritative account/usage state, never merely a browser return. Manage subscription and cancellation are reachable without an obscuring perch.
- **Inputs → outputs:** Plan configuration, authenticated selection and provider accounting → reservation, consumption record, authoritative entitlement and billing receipt/history.
- **States, focus, approvals:** Unavailable billing configuration leaves connection `disconnected`; insufficient allowance routes to PB-028. F1/F4; A2/A3 for payment; extending task usage requires a bounded allowance decision, not permission to charge a card.
- **Unhappy paths:** Duplicate webhooks/requests are idempotent; cancelled checkout retains old plan; portal open failure restores card with error; abandoned reservation releases under server policy.
- **Non-goals:** Invented approved prices, app-supplied billable counts, standing permission for purchases, “unlimited” without real entitlement.
- **Acceptance:** [PB-027](../quality/ACCEPTANCE.md): configured test-mode checkout/webhooks; duplicate/out-of-order events; reservation reconciliation; visibly unconfigured live billing. [Flow](APP-FLOWS.md#pb-027).

<a id="pb-028"></a>
## PB-028 — Quota limits and graceful provider unavailability

- **Required:** Identify the exact unavailable capability, limit and reset/repair path. Save unsent request and partial work. Offer available local/typed paths only when their own dependencies are actually ready. A voice failure does not automatically send audio to another model. Capability status reflects actual deployment health, not catalog visibility. Retry is explicit or bounded/read-safe as documented; no hidden cost loop.
- **Inputs → outputs:** Capability/entitlement result, provider error and pending request → clear blocked explanation and resumable task/input.
- **States, focus, approvals:** Task needing provider → `waitingForConnection`; quota needing user decision → `waitingForInput`; active voice → `unavailable` or `failed`; dictation → `failed` with recovery text. F0/F4; A1 for usage extension, A2 for checkout.
- **Unhappy paths:** Selected realtime/dictation deployments are currently not live-verified; show external configuration blocker, not a working demo. Outage during reservation reconciles actual billed usage.
- **Non-goals:** Promising talk always works after every quota, silent fallback, fixtures satisfying live gates.
- **Acceptance:** [PB-028](../quality/ACCEPTANCE.md): each quota class; unavailable selected roles; partial output survives; no false usage/success. [Flow](APP-FLOWS.md#pb-028).

<a id="pb-029"></a>
## PB-029 — Preferences, voice/device choice and shortcut recording

- **Required:** Settings exposes voice preview, input/output device, language, dictation review/dictionary, keyboard shortcuts, appearance, perch/display, notifications, privacy and account preferences. Show effective values; unsupported options remain explained. Voice preview is an explicit request and cannot launch a task. Shortcut recorder captures binding only, validates conflicts and provides Cancel/Reset. Preferences persist per appropriate device/account scope.
- **Inputs → outputs:** Validated preferences → persisted settings and updated capability/context without app restart unless technically required and disclosed.
- **States, focus, approvals:** Preview voice uses normal voice states, never a separate fake live path. Device changes follow PB-034; connection credentials are PB-022/023, not plain text settings. F1/F7; A0/A3.
- **Unhappy paths:** Voice unavailable retains prior choice; removed device shows selected-but-unavailable and prompts fallback; invalid shortcut does not erase current working binding.
- **Non-goals:** Model picker that changes locked roles, secret fields in exported preferences, forced voice previews on navigation.
- **Acceptance:** [PB-029](../quality/ACCEPTANCE.md): preview/cancel; recording conflicts; persistence; settings change during active turn without data loss. [Flow](APP-FLOWS.md#pb-029).

<a id="pb-030"></a>
## PB-030 — Local export, account export and deletion

- **Required:** Local export includes selected Pebbis, conversations, approved memories, routine definitions, artifact manifest/files and version metadata, excluding secrets and raw ephemeral captures. Server account export separately covers account/usage data. UI distinguishes both scopes and offers combined app-driven packaging without implying server sync. Delete confirmation states local/server/billing effects and recoverability; export remains available before deletion. Account deletion disables sessions and future work; actual server response/readback determines completion.
- **Inputs → outputs:** Export scope/destination or explicit destructive confirmation → readable export and manifest/check result, or deletion receipt plus disclosed retained legal/billing records.
- **States, focus, approvals:** Export task uses normal states; deletion first stops/reconciles active tasks. F1/F4; A2/A3 with reauthentication where required. Local deletion can proceed offline separately from pending server deletion.
- **Unhappy paths:** Disk full, expired link and failed server deletion preserve truthful per-scope status; do not say “all deleted” when only local files were removed. Other-device local copies cannot be remotely erased by nonexistent sync.
- **Non-goals:** Secret export, guaranteed erasure from third-party recipients/backups, hiding subscription obligations.
- **Acceptance:** [PB-030](../quality/ACCEPTANCE.md): export integrity/redaction; independent local/server deletion failures; account revocation and no cross-account residue. [Flow](APP-FLOWS.md#pb-030).

<a id="pb-031"></a>
## PB-031 — Privacy controls, retention and sensitive-content boundaries

- **Required:** Explain local history versus cloud processing and selected roles at point of disclosure. Capture/audio are transient by default; local transcripts/history persist until user deletes or chooses a shorter supported retention setting. Memory and suggestions consent are separate. Per-Pebbi private session excludes durable chat/memory/artifact retention except explicitly saved outputs, mandatory minimal usage/security accounting and minimal unresolved-effect reconciliation metadata. These exceptions are disclosed before composing. Block secret/secure-field capture and require manual redaction where detection is uncertain. Privacy controls remain usable offline.
- **Inputs → outputs:** Privacy/retention choices and scoped content → context manifest, retention action and revocable consents.
- **States, focus, approvals:** Revoking source scope halts dependent task at `waitingForInput`/`waitingForConnection` before next tool call. F0/F7; A1/A3. Explain provider/legal retention rather than claiming deletion beyond control.
- **Unhappy paths:** Sensitive content encountered mid-task pauses disclosure; history retention removes derived summaries consistently; telemetry cannot include prompts, file bodies, credentials or raw screenshots.
- **Non-goals:** Continuous clipboard/app tracking, unconsented memory, unverified “nothing leaves this Mac”/compliance claims.
- **Acceptance:** [PB-031](../quality/ACCEPTANCE.md): context inspection/redaction; private session after restart; revoke during work; retention and diagnostics secret scans. [Flow](APP-FLOWS.md#pb-031).

<a id="pb-032"></a>
## PB-032 — VoiceOver, keyboard, contrast and reduced motion

- **Required:** Every main/safety flow is operable by keyboard and VoiceOver with named native controls, logical order, focus visibility, selectable transcripts and textual alternatives to drawings/audio. Semantic states never rely only on color, shape or animation. Use accessible design tokens, readable text scaling and reduced-motion alternatives. Streaming updates announce semantic milestones, not every token; approvals are read with consequence before buttons.
- **Inputs → outputs:** Assistive settings and user navigation → equivalent completion, stable accessibility focus and understandable status.
- **States, focus, approvals:** Canonical state labels and counts have accessible equivalents. F7 overrides decorative focus/motion; A1/A2 controls cannot be hidden behind hover or speech-only UI.
- **Unhappy paths:** Small window/large text reflows to scrolling, not clipped controls; unavailable audio still leaves transcript; contrast setting changes preserve selected state.
- **Non-goals:** Visual-only mascot communication, inaccessible custom menu substitutes, animation required for comprehension.
- **Acceptance:** [PB-032](../quality/ACCEPTANCE.md): full keyboard/VoiceOver journeys; contrast and reduced motion; large-text approval and stop controls. [Flow](APP-FLOWS.md#pb-032).

<a id="pb-033"></a>
## PB-033 — Multi-display, notchless, Spaces and scaling behavior

- **Required:** User chooses perch display or follow-active-display policy. Respect safe areas/menu bar/notch, scaled coordinates and display origins. Home/perch/overlays stay visible after display disconnect/rearrangement; choose nearest remaining visible display deterministically. Overlay targets belong to a specific display/window and invalidate after geometry change. Full-screen/Spaces transitions never steal the user's current Space.
- **Inputs → outputs:** Display topology, chosen policy and window geometry → constrained window placement and validated overlay mapping.
- **States, focus, approvals:** Geometry invalidation pauses affected task in `waitingForInput` until reinspection; unrelated tasks continue. F0/F3/F6; new capture scope needs A1.
- **Unhappy paths:** Notchless Studio Display, menu-bar auto-hide, negative display origins and mixed scaling cannot swallow shortcuts or hide controls; missing target asks rather than guessing.
- **Non-goals:** Hardware-notch-only operation, one-resolution coordinate assumptions, Spaces switching in response to background completion.
- **Acceptance:** [PB-033](../quality/ACCEPTANCE.md): notchless/notched/mixed-DPI; disconnect during walkthrough; full-screen Space and keyboard routing. [Flow](APP-FLOWS.md#pb-033).

<a id="pb-034"></a>
## PB-034 — Audio devices, Bluetooth, interruption and mic recovery

- **Required:** Enumerate real devices and selected/default policy. Detect route loss, silence where audio is expected and format mismatch. Preserve finalized transcript and partial dictation through interruption. Offer explicit built-in-mic fallback; automatic fallback is allowed only if preauthorized and visibly indicated. Playback pre-roll must not produce audible garbage; device switching waits for safe boundary where possible. Muted output exposes text, not automatic clipboard replacement.
- **Inputs → outputs:** Audio frames, route events and fallback consent → recoverable transcript, device status and resumed/restarted session.
- **States, focus, approvals:** Voice active → `interrupted` then `connecting`/`listening` only after valid recovery; missing permission/device → `unavailable`; dictation → `reviewing` for retained partial or `failed` with recovery draft. F0/F2; A1 for new fallback mic consent, A3 for OS grant.
- **Unhappy paths:** Bluetooth profile switch/call/external interface loss does not silently erase words or reopen a mic after user stopped. Device failure count and reason are diagnostic, no raw audio logs.
- **Non-goals:** Perfect all-headset support without hardware tests; secret mic switching; pasted reply on mute.
- **Acceptance:** [PB-034](../quality/ACCEPTANCE.md): Bluetooth cold start; interface format; call/route loss; explicit fallback and cancelled-session nonrestart. [Flow](APP-FLOWS.md#pb-034).

<a id="pb-035"></a>
## PB-035 — Offline, sleep/wake and app-crash recovery

- **Required:** Local browsing, draft editing, memory inspection and export remain available offline. No cloud response is fabricated. On wake recheck device/permission/session/capability and refresh due routines once. On crash mark every previously active attempt `interrupted`, inspect its journal and reconcile external effects before offering a linked retry. Preserve drafts, queue order, artifact references and unanswered approvals, but invalidate obsolete grants/targets.
- **Inputs → outputs:** Connectivity/sleep/lifecycle event and journal → restored local view, reconciliation report and resumable work choices.
- **States, focus, approvals:** Connected work loses dependency → `waitingForConnection`; crash active attempts → `interrupted`; safe retry creates new `queued` attempt. F0/F4; A4 for stale action version, A2 fresh where required.
- **Unhappy paths:** Missing/corrupt local record is isolated with backup/export guidance; duplicate stream events do not replay writes; expired account waits for sign-in; no endless reconnect loop.
- **Non-goals:** Offline model inference, silent resume of uncertain side effects, mass catch-up or microphone autoactivation after wake.
- **Acceptance:** [PB-035](../quality/ACCEPTANCE.md): offline editor; crash around external write; sleep/wake coalescing; interrupted recovery with no duplicate send. [Flow](APP-FLOWS.md#pb-035).

<a id="pb-036"></a>
## PB-036 — Secure updates, signing and release rollback

- **Required:** Only Developer ID signed/notarized, hardened-runtime DMGs and Sparkle-signed trusted updates are installable through product channels. Show installed/available version and release notes. Explicit install/relaunch journals work and migrates data safely. Verify update signature before replacement. Rollback uses a supported signed compatible build and documented database compatibility; never overwrite newer data blindly.
- **Inputs → outputs:** Trusted update metadata/package and user install choice → verified install, preserved data or safe rejection/rollback result.
- **States, focus, approvals:** Update presentation does not invent task states; running work follows PB-017/PB-035. F1/F4; A3 for signing/install authority. Missing signing identity blocks release, not local implementation work.
- **Unhappy paths:** Tampered feed/package, failed download, insufficient disk and incompatible migration retain working version/data; expose recovery, not success. Never claim universal hardware verified from architecture flags alone.
- **Non-goals:** Unsigned fallback updates, bypassing notarization, untested automatic data downgrades.
- **Acceptance:** [PB-036](../quality/ACCEPTANCE.md): signature/tamper rejection; update with data; migration failure; supported rollback and arm64/x86_64 evidence. [Flow](APP-FLOWS.md#pb-036).

<a id="pb-037"></a>
## PB-037 — Diagnostics, support and redacted telemetry

- **Required:** Settings offers Support, documentation, release notes and previewable diagnostic export. Bundle version/OS/capability state, event timing, redacted error codes and user-selected reproduction notes; never include credentials, content bodies, screenshots/audio or home-path identifiers. Product analytics is opt-in and separate from necessary service security/usage logs. Sending support is an explicit outbound action; local export remains possible offline.
- **Inputs → outputs:** Selected time range and consent → redacted preview/bundle and, if approved, verified support receipt.
- **States, focus, approvals:** Diagnostic task uses normal states; failed upload retains local artifact. F1/F4; A2 for outbound submission; A1 for telemetry opt-in.
- **Unhappy paths:** Redaction failure blocks send/export until sensitive fields excluded; support URL cannot open offers copy link; unsupported diagnostics never fake a sent ticket.
- **Non-goals:** Silent content telemetry, automatic support emails, secrets in logs, fabricated compliance/security claims.
- **Acceptance:** [PB-037](../quality/ACCEPTANCE.md): seeded-secret scan; offline export; consent-controlled submission/readback; correct version and capability reporting. [Flow](APP-FLOWS.md#pb-037).

<a id="pb-038"></a>
## PB-038 — Resource budgets, latency and idle efficiency

- **Required:** Hidden/offscreen decorative animation and unused capture stop; idle app does not poll high-frequency AX/screen/audio. Work respects documented CPU/memory/concurrency/time budgets; UI/Stop remains responsive under load. Measure cold/warm voice, dictation, Home switching, first meaningful progress, idle power/CPU and long-session growth on declared hardware. Slow work reports actual wait and remains cancellable, not artificially truncated into success.
- **Inputs → outputs:** Workload, hardware profile and instrumentation → measured performance report, bounded scheduling and visible degradation.
- **States, focus, approvals:** Capacity exhaustion queues work as `queued`; timeout produces `failed` or a documented wait, never `succeeded`. F0/F7; resource-expanding command needs A1 and no implicit paid scaling.
- **Unhappy paths:** Model latency, huge history and thermal pressure do not freeze controls; repeated reconnect/retry consumes bounded resources; unavailable hardware performance remains unverified.
- **Non-goals:** Reusing vendor CPU/latency numbers as Pebbi evidence, idle microphone warmup without consent, fabricated benchmark output.
- **Acceptance:** [PB-038](../quality/ACCEPTANCE.md): pinned budget matrix and real measurements; long-history/large-file load; offscreen idle; responsive stop under saturation. [Flow](APP-FLOWS.md#pb-038).

<a id="pb-039"></a>
## PB-039 — Support, privacy, account and download web surfaces

- **Required:** Public original-styled pages explain Pebbi, supported macOS, actual availability, download verification, support and privacy. Account pages use real identity/billing state and distinguish server data from local Mac data. Downloads point only to verified releases; pre-release/configuration blockers are explicit. Web pages are keyboard/screen-reader accessible and match brand tokens without becoming the native app shell. Support destination and legal/operator details must be real before launch.
- **Inputs → outputs:** Public or authenticated browser navigation → truthful page, verified DMG link, account action or support route.
- **States, focus, approvals:** Browser account connection follows canonical connection states; checkout uses PB-027. F1 on user link opening; A2/A3 for billing/deletion/support submission.
- **Unhappy paths:** No release available shows unavailable, not dummy download; sign-in failure retains return destination; unreachable support route has alternate verified contact; no forged legal entity/contact.
- **Non-goals:** React framework mandated for static support pages, copied reference homepage, fake testimonials, domain ownership claim from selected name.
- **Acceptance:** [PB-039](../quality/ACCEPTANCE.md): anonymous/download/privacy/support pages; authenticated account; broken/unconfigured route states; accessibility and artifact verification. [Flow](APP-FLOWS.md#pb-039).

<a id="pb-040"></a>
## PB-040 — Complete end-to-end acceptance and honest release gating

- **Required:** Release candidate evidence covers every PB in requirements, flows, screens, acceptance and machine-readable coverage. Exercise real native installation, account, permissions, live models, connector/browser/native control, outputs, billing, recovery, accessibility, update and deletion on authorized environments. Mark each test's environment and actual pass/fail/blocked/not-run result; fixture results cannot satisfy live gates. Final release requires no unresolved safety-critical or mandatory behavior failures.
- **Inputs → outputs:** Candidate artifact, configured test resources and all acceptance cases → traceable evidence manifest, defect/blocker list and honest release decision.
- **States, focus, approvals:** Test state labels are evidence classifications, not runtime task states. All runtime tests use contract states, F0–F7 and A0–A5. Human OS/identity/payment/signing consent remains required.
- **Unhappy paths:** Missing credentials/hardware/signing blocks corresponding live gate; continue all independent work. No passing subset is described as a complete release; revalidate affected flows after fixes.
- **Non-goals:** Stopping at scaffolding, fake successful provider calls, silent acceptance exclusions, calendar-based scope cuts.
- **Acceptance:** [PB-040](../quality/ACCEPTANCE.md): verify exact PB-001–PB-040 coverage; inspect real artifacts and evidence; confirm blocked dependencies remain labeled and prevent false production readiness. [Flow](APP-FLOWS.md#pb-040).
