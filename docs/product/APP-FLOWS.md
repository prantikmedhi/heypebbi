# Pebbi — complete user journeys and state transitions

> **HISTORICAL REFERENCE — SUPERSEDED SCOPE.** The current decision is [local Azure onboarding](LOCAL-AZURE-ONBOARDING.md), docs only until implementation is resumed. This earlier managed/full-product design is preserved as reference, not an instruction to implement its hosted services, login, billing, fixed models or full PB scope. Current requirements take precedence.

Normative companion to [Requirements](REQUIREMENTS.md) and the [contract](../CONTRACT.md). Runtime enum spelling is exact. Surface presentation and evidence labels are not substitute runtime states. Every flow has a stable `pb-NNN` anchor and acceptance reference to the same PB identifier in [Acceptance](../quality/ACCEPTANCE.md). [IA](INFORMATION-ARCHITECTURE.md) names destinations; [Copy](COPY.md) supplies status and error strings. F0–F7 and A0–A5 below refer to the shared focus and approval rules in [Requirements](REQUIREMENTS.md#common-rules-inherited-by-every-pb).

## Global transition contract

### Task attempts

| From | Event and guard | To | Required observable effect |
| --- | --- | --- | --- |
| `queued` | Scheduler admits attempt and required initial resources are available | `running` | Name Pebbi and actual first step; create no duplicate attempt |
| `running` | Exact action version requires consent | `waitingForApproval` | Preserve proposal, consequence and decision controls |
| `running` | Missing user choice, scope, prerequisite permission or quota decision | `waitingForInput` | Ask one concrete question with resumable context |
| `running` | Provider, account or connector unavailable | `waitingForConnection` | Name dependency; preserve request and output |
| Any wait state | Required condition resolved, action version valid and scheduler resources reacquired | `running` | Continue the same attempt at its saved checkpoint; do not create a second queue entry |
| `running` | Outputs and relevant external effect have been verified | `succeeded` | Final result, artifacts, evidence and truthful limitations |
| `running` | Nonrecoverable failure or bounded retry exhausted | `failed` | Error, partial artifacts and linked Retry option |
| `queued` | Cancel before any dispatch | `cancelled` | Atomically remove only this queue entry; no inflight effect exists |
| `running` or any wait state | Stop, confirmed destructive workflow or explicit cancellation | `cancelling` | Stop new calls immediately; expose reconciliation |
| `cancelling` | No further calls can dispatch; in-flight effects reconciled or explicitly recorded as unresolved | `cancelled` | What stopped, what changed, what remains uncertain; retry stays disabled for unknown writes |
| Previously `running`, waiting or `cancelling` attempt | App restart detects unclean termination | `interrupted` | Never assert nothing happened; show recovery assessment; preserve undispatched `queued` entries |
| `interrupted` | Reconciliation classifies every dispatch | `failed` or `cancelled` | Close old attempt with interruption reason or explicit cancellation; unresolved effects retain a resource barrier |
| Classified interrupted attempt | User chooses resume/retry | New linked attempt starts `queued` | Preserve old evidence; reuse safe outputs; never bypass an unresolved resource barrier |
| `succeeded`, `failed`, `cancelled` | Follow-up or retry | Existing attempt unchanged; new attempt `queued` | Terminal attempt is immutable evidence |

A denied optional operation may be removed from a proposed plan only after showing its changed outcome. A denied necessary action enters `waitingForInput`; choosing End task follows `cancelling` → `cancelled`. An admitted attempt may enter `running` briefly for preflight before a wait. Queued work has not dispatched and can be cancelled directly. No wait state automatically spends usage indefinitely. Poll/retry policy is bounded in engineering; request, reconnect and duplicate UI events are idempotent.

### Voice, dictation, connections and routines

- **Voice:** `idle` → `connecting` → `listening` → `thinking` → `speaking` → `idle`. Explicit active conversational listening may return `speaking` → `listening` after playback only while that user-enabled session remains active. Barge-in gives `speaking` → `interrupted` → `listening`; a normal Stop speaking ends at `idle`. Setup/permission/capability absence gives `unavailable`; runtime transport/model failure gives `failed`. Retry from `unavailable`/`failed` requires explicit user action and repaired prerequisites before `connecting`. Typed input never falsely activates microphone state.
- **Dictation:** `idle` → `capturing` → `transcribing` → `reviewing` → `inserting` → `completed`. A final transcription may arrive while capture streams; UI remains `capturing` until capture ends, then `transcribing` until final text is available. Cancel from any active stage gives `cancelled`; before insertion dispatch, no target edit occurs. If insertion is already admitted, cancellation stops further dispatch and reconciles that effect in its receipt as inserted/unchanged/unknown. The lifecycle label does not imply rollback. No automatic undo, duplicate insertion or unverified unchanged/success claim is allowed. Errors give `failed`. Retained text may be reopened in a new review attempt after failure/cancellation. Ending capture is not insertion; copying text is not verified insertion.
- **Connection:** `disconnected` → `connecting` → `ready`; token expiry → `expired`; partial service health → `degraded`; handshake or unrecoverable health failure → `failed`. Retry/re-auth uses `connecting`; disconnect from any state gives `disconnected`. A logo, saved URL or accepted configuration alone never means `ready`.
- **Routine:** confirmed usable definition → `active`; unavailable prerequisite → `blocked`; explicit pause or third consecutive failed run → `paused`; archive → `archived`. Repair may return `blocked` → `active` after revalidation unless the user paused meanwhile. Resume from `paused` rechecks to `active` or `blocked`. Restore from `archived` returns `paused`, never silently `active`.

## Dispatch, focus and evidence invariants

A user turn has one destination conversation and one submission identity. Save it before dispatch. Explicitly named Pebbi wins; otherwise the focused Pebbi conversation wins; otherwise one unambiguous spoken reference to a named recent result may win. If multiple candidates remain, ask. A background Home window never wins solely because it is visible. Follow-up assignment and terminal transition are serialized so a message is either accepted by the current attempt or starts a new attempt, never lost between them.

For every external action, capture origin and bounded target, validate permission and action version, show required approval, revalidate just before dispatch, perform once, read back, then update state. Unknown effects cannot be retried as if nothing happened. Content from pages, files and MCP descriptions remains untrusted data. Task cancellation, stopping speech, closing a panel and dismissing drawings are separate user intents.

<a id="pb-001"></a>
## PB-001 — Install, launch and leave

**Entry:** User has a verified compatible DMG; no app implementation is implied by these docs. **Input:** install artifact and existing optional local store. **Output:** one native app session or an explicit install error; on exit, a recoverable journal.

1. User opens the DMG, sees the Pebbi application and Applications destination, and performs the native install. Gatekeeper/signing decisions stay manual (A3).
2. First launch checks supported OS and store readability before requesting permissions. Unsupported OS stops with requirements; failed migration opens recovery guidance without overwriting data.
3. Home opens deliberately (F1). A new user sees sign-in/optional setup; a returning user sees their saved selection and drafts. Repeated launch focuses the same instance.
4. Choosing Close window only closes that surface; menu bar remains available and routines may continue. Choosing Quit explicitly lists active work and offers Cancel and quit or Return to Pebbi.
5. Confirmed quit stops new dispatch, sends active attempts through `cancelling`, saves known/unknown side effects, stops capture/audio/helpers and exits. If the user forces quit instead, PB-035 handles `interrupted` on next launch.

**Recovery:** Corrupt package/download, full disk or unavailable signing validation never produces installed/success copy. User can retry an intact package without losing the old store. **Acceptance:** [PB-001](../quality/ACCEPTANCE.md); update security is [PB-036](#pb-036).

<a id="pb-002"></a>
## PB-002 — Sign in, switch account and revoke a device

**Entry:** Home → account gate or Settings → Account. **Input:** user sign-in intent, not credentials supplied to the assistant. **Output:** validated account/device session or a preserved signed-out view.

1. User chooses Sign in. Connection changes `disconnected` → `connecting`; Pebbi opens the system browser and remembers the return destination.
2. User completes identity UI manually. Pebbi accepts only a valid issuer/audience/nonce/state/PKCE return and stores account session material in Keychain. For new/replacement enrollment, call `POST /v1/devices/enrollments` with the account bearer and installation ID, then perform ordinary Entra code+PKCE authentication using the returned authorization nonce. Submit `enrollmentId` and the signed native-client-audience `enrollmentIdToken` to registration; the server verifies nonce/challenge binding, same account, freshness and one-use state. Store the once-returned `RegisterDeviceResponse.deviceToken` in Keychain, confirm possession and read back the nonsecret device record. A still-valid previously stored device credential may be revalidated rather than enrolled again. Device-bound REST calls carry account bearer, `X-Pebbi-Device-Id` and matching `X-Pebbi-Device-Token`; only then does the connection become `ready` and Home resume.
3. Cancellation returns to the original gate without marking setup failed. An invalid/stale return shows a new sign-in action; it never changes account.
4. In Settings, user sees current account and device sessions. Revoke names the target; confirmation invalidates it server-side and readback removes or marks it revoked. Revoking this device stops future authenticated calls and locks account data. Revocation advances server `enrollmentNotBefore`; stale authentication cannot enroll a replacement by changing installationId or refreshing the bearer. Re-enrollment requires verified new interactive authentication after that threshold. If the enrollment response is lost, retire its uncertain record and explicitly reauthenticate/re-enroll; do not fetch the old device secret from ordinary idempotency cache.
5. Sign out explains retained local content. On confirmation, stop/reconcile active authenticated tasks, revoke/clear session material and hide account-scoped content. A different account receives a separate local view and no prior grants.

**Focus/approval:** F1 only for explicit browser launch/return; A3 for auth; background token expiry never opens browser. Expiry makes connection `expired` and dependent task `waitingForConnection`. **Acceptance:** [PB-002](../quality/ACCEPTANCE.md).

<a id="pb-003"></a>
## PB-003 — Grant, skip and repair permissions

**Entry:** User chooses a capability requiring an absent OS permission. **Input:** capability and actual OS state. **Output:** permission readiness, still-usable alternate path or specific recovery.

1. Pebbi explains what permission is needed and what data/action it permits. User chooses Continue or Not now; no blanket bundle of grants.
2. Continue invokes the appropriate native request/settings route; the user decides in macOS (A3). Returning to Pebbi triggers a state recheck, not a presumption of consent.
3. If granted, retry the original capability only after confirming its original capture/action scope remains valid. If denied, preserve the request and offer Open System Settings, Recheck and Continue without this feature.
4. Microphone denial yields voice `unavailable`; screen/action permission absence leaves the associated task `waitingForInput`. Typed/local Home remains usable. Notification denial changes only delivery policy.
5. If permission is revoked mid-operation, stop affected capture/dispatch immediately. Show retained text/partial output and exact grant needed; never repeat OS prompts in a loop.

**Recovery:** Managed policy, required relaunch or wrong settings page receives manual directions plus Recheck. Relaunch does not imply permission was granted. F1/F4/F7; no setting is toggled by automation. **Acceptance:** [PB-003](../quality/ACCEPTANCE.md).

<a id="pb-004"></a>
## PB-004 — Personalize and meet the first Pebbis

**Entry:** First launch setup or Settings → rerun personalization. **Input:** optional answers and original appearance choice. **Output:** user-confirmed Pebbi profiles and memories.

1. Show explicit AI identity and processing disclosure. Offer guided interview, manual setup or Skip. The user may choose keyboard at any point.
2. Interview collects the four optional topics in [Requirements](REQUIREMENTS.md#pb-004), retaining saved answers only. The interface names the active voice state and never fabricates an interview reply when the role is unavailable.
3. Show an editable summary, each proposed durable memory and default Pebbi plus up to two proposed jobs. Unchecked memories are not saved; unconfirmed extra Pebbis are not created.
4. Save commits profiles/workspaces atomically. If a job already exists from interrupted setup, reuse its identity rather than duplicate it. Model unavailability offers the same manual fields.
5. Optional tutorial opens a safe in-app sample, asks for scoped capture permission only if used, demonstrates a pointer, then records dictation into a review field. Skip/End cancels tutorial work, stops speech, clears every overlay and restores Home focus.
6. Home selects the default Pebbi and presents an empty composer, not a task already running. Setup usage is shown separately if an operator-configured allowance exists.

**Recovery:** Relaunch resumes the last saved setup step; unsaved interview text remains a draft, not memory. F1/F7; A1 for memory and capture, A3 for OS grants. **Acceptance:** [PB-004](../quality/ACCEPTANCE.md).

<a id="pb-005"></a>
## PB-005 — Move between perch, menu bar and Home

**Entry:** Any app, any supported display. **Input:** deliberate menu/perch/Home action. **Output:** consistent selected Pebbi, draft, preview and scroll state.

1. User activates the menu item or expands the perch. Read selected conversation state; do not create a new conversation or move its draft.
2. User selects a Pebbi, types an unsent draft and attaches a file. Persist ownership to that conversation before surface changes.
3. Expand into Home transfers the same selection and preview; explicit action may focus the composer (F1). Return to perch changes presentation only. Running tasks continue without extra dispatch.
4. Escape closes the expanded perch, restores the prior app if still available, and latches hover closed until the pointer leaves the activation region. It neither clears the draft nor cancels the task.
5. A clicked external link first dismisses obstructing attached surfaces and then opens the destination. Pending approval/billing controls remain reachable, never underneath a notch overlay.

**Recovery:** If the stored conversation is missing, show disclosure and Create fresh conversation; retain known task references. If display disappears, reposition within a remaining visible safe area without switching Space. Background events obey F0; no additional approval is needed for local navigation (A0). **Acceptance:** [PB-005](../quality/ACCEPTANCE.md).

<a id="pb-006"></a>
## PB-006 — Invoke from another app without stealing text

**Entry:** Another app has an editable field or user wants Home. **Input:** validated shortcut gesture. **Output:** one routed interaction with an origin token.

1. Recognize the configured gesture, rejecting key repeat and conflicts. Snapshot originating app/window/field before presenting any Pebbi surface.
2. Home shortcut deliberately opens Home (F1). Talk hold starts PB-007 without focusing Home (F2). Dictation hold starts PB-010 with the captured origin. Hands-free starts/stops one dictation session on successive valid double-taps.
3. Route to an explicitly named Pebbi, the genuinely focused conversation or one unambiguous recent spoken context. If there are two plausible destinations, ask and retain the message as `waitingForInput` rather than dispatching twice.
4. Hold release ends the audio capture segment. It does not press Return in the source app or cancel an already running task.
5. Before eventual insertion, recheck the original field and actual current focus. A visible but background Home composer is never selected as a fallback.

**Recovery:** Secure input refuses capture/insertion with a quiet explanation; active native menus and Settings shortcut recorder do not trigger assistant work. Unsupported Fn delivery prompts rebind, preserving an accessible button path. **Approval:** A0 for invocation; any subsequent capture/action follows its own approval. **Acceptance:** [PB-006](../quality/ACCEPTANCE.md).

<a id="pb-007"></a>
## PB-007 — Converse, type, interrupt and hand off work

**Entry:** Selected Pebbi or correctly routed global request. **Input:** audio/typed message and explicitly approved context. **Output:** persisted user message, response and optional task reference.

1. For voice, check permission, quota and selected deployment readiness before `idle` → `connecting`. On actual session establishment show `listening`; stop capture at gesture/session boundary, then show `thinking`. Typed input is saved and dispatched without opening the mic.
2. Render transcript and response incrementally with the Pebbi's name. Audio response gives `speaking`; text remains selectable. Complete playback returns to `idle` unless an explicitly enabled active conversation session is continuing.
3. If the request is actionable, create a journaled `queued` task and show its named card; never imply a tool ran merely because the voice said it would. Run PB-015 and applicable approvals. Keep the voice audio operation/reservation separate from that agent task: the task can reason while voice remains active. In voice/dictation wire envelopes only, `taskId`/`attemptId` carry `audioOperationId`/`audioAttemptId`; reasoning retains real task/attempt IDs. A spoken result’s `sourceTaskId`/`sourceAttemptId` identify its real source task, not its audio owner.
4. User barges in: stop playback, voice becomes `interrupted`, retain the response, then `listening` if the session remains active. User choosing Stop speaking instead returns to `idle`. The task keeps its own state until Stop task is chosen.
5. Typed follow-ups enter the same conversation and serialized dispatcher. A quiet user can inspect all output and approve using native controls. Speech may select a low-risk task or open its review; even a clear spoken “yes” does not authorize protected effects. Wait for deliberate accessible native approval against the exact preview.

**Recovery:** `unavailable` names missing role/permission; runtime failure becomes `failed`. Preserve partial transcript and offer Retry, Type a task or Close only when the alternate capability is actually ready. F0/F2/F7; A1/A2 gate real work. **Acceptance:** [PB-007](../quality/ACCEPTANCE.md).

<a id="pb-008"></a>
## PB-008 — Ask about exactly the selected screen content

**Entry:** User chooses Add screen context or asks about visible work. **Input:** window/display/region selection and question. **Output:** scoped transient capture and analysis with provenance.

1. If no scope exists for this request, show a native picker/region control with a disclosure that this content will be processed remotely. User chooses and confirms one scope (A1); permission repair uses PB-003.
2. Inspect selection identity/geometry, suppress excluded sensitive surfaces and show the capture indicator. Optional user marks identify a subregion; they do not broaden scope.
3. Task `queued` → `running` captures only the approved scope and reasons about it. If the question needs the whole document, explain the difference and request a file/DOM source through PB-014/PB-019.
4. Answer names what was actually inspected. Delete transient capture buffers when no longer needed; history retains text analysis and scope metadata, not a raw screenshot.
5. A follow-up requiring fresh pixels asks for/uses a clearly active bounded recapture scope; it never silently watches the display between requests.

**Recovery:** Closed window, permission revocation, blank capture or changed display geometry yields `waitingForInput`; invalidate coordinates and choose/recapture again. Secure or uncertain secret content requires manual redaction. F0/F3/F6; no pointer takeover from capture alone. **Acceptance:** [PB-008](../quality/ACCEPTANCE.md).

<a id="pb-009"></a>
## PB-009 — Complete a walkthrough across manual pauses

**Entry:** User requests guidance for a concrete goal. **Input:** goal, allowed screen/file context and inspected target. **Output:** saved step history and completed procedure evidence.

1. Task starts `queued` → `running`; state the goal, proposed next step and current target. Render a textual instruction plus optional original pointer/ring, never an instruction only in a drawing.
2. Save step number, target identity, expected result and completion predicate before showing it. Guidance itself cannot click; the user performs the manual step.
3. Move to `waitingForInput` while manual work is required. User chooses Continue or a reliable observed event triggers reinspection. Verify expected result, record evidence, then `running` for the next step after resource revalidation. If uncertain, ask; elapsed time is insufficient evidence.
4. Pause retains goal/completed steps and clears intrusive marks. Resume reinspects current app, adapts the next step without repeating completed work, and continues beyond any presentation batch limit until the real goal is met.
5. Back revisits an instruction without undoing external effects. End follows `cancelling` → `cancelled` and clears overlay/speech. Escape clears current presentation but not unrelated tasks.
6. Goal verification yields `succeeded` with concise completed-step summary. Relaunch recovery marks the attempt `interrupted`; safe resume uses a linked attempt with saved progress.

**Recovery:** Moved/missing target invalidates its mark and waits; do not point at a stale coordinate. F0/F6/F7; control requests require new A1 authority. **Acceptance:** [PB-009](../quality/ACCEPTANCE.md).

<a id="pb-010"></a>
## PB-010 — Dictate, review and insert in the right field

**Entry:** User invokes dictation with a real target field or chooses a blank review draft. **Input:** audio, origin, language/dictionary preferences. **Output:** reviewed transcript and evidence of insertion, or an honest retained draft.

1. Snapshot origin and verify non-secure target; check selected transcription capability. Create an independent dictation audio owner without queueing an agent task; a running or waiting Pebbi task must not block dictation. If voice owns the device microphone, offer an explicit pause/replace choice, release its lease before dictation acquires it and never cancel its associated agent task. Start `idle` → `capturing` only after live session readiness, not just an accepted provider configuration.
2. Stream recognized text without asserting it is final. Release/stop ends audio, `transcribing` waits for final segments, then `reviewing` displays complete available text and named destination. Preserve long-session partials locally according to retention settings.
3. User edits text. Cleanup cannot add facts. Review is default; opted-in direct insertion still requires all target/secure-input checks. A terminal target collapses newlines and shows the exact resulting string.
4. Insert revalidates current app/window/field and action version. If unchanged and eligible, `inserting` performs one safe insertion, reads back where possible and becomes `completed` only on confirmation. It never sends Return or clicks Send.
5. If direct insertion is unsupported, show Copy instead. User-authorized clipboard fallback records ownership and restores the old clipboard only if no later user clipboard change occurred. Copy-only receipt must say Copied, not Inserted.

**Recovery:** Focus changed → retain `reviewing` and ask user to refocus/choose. Route failure → `failed` with partial draft, or review completed partial on explicit user choice. Cancel before insertion dispatch gives `cancelled` with zero target edits. Cancel after admission stops new work, retains text under privacy policy and reconciles the one dispatched insertion; show actual inserted/unchanged/unknown receipt beside `cancelled`. If the user edits concurrently, preserve their edit; never automatically restore old text or retry an uncertain insert. Late transcripts/readbacks cannot cause another insertion or relabel cancellation as completed. An already verified `completed` operation is not retroactively cancelled. F2/F3; actual outbound send is separate A2. **Acceptance:** [PB-010](../quality/ACCEPTANCE.md).

<a id="pb-011"></a>
## PB-011 — Create, refine and archive a persistent Pebbi

**Entry:** Home → Pebbis → New Pebbi, or a named creation request. **Input:** name, job, original appearance, optional approved memory. **Output:** durable isolated profile/workspace.

1. Open the form; conversational creation may propose fields but does not commit them. Missing model access leaves the form fully usable.
2. User reviews job boundaries, appearance and workspace, corrects required fields, then Save commits one Pebbi. Duplicate name receives job-based disambiguation, not silent renaming.
3. Home selects the new Pebbi with an empty conversation. Later profile edits preserve the identity and prior work. Job edits affect future tasks; an active attempt keeps its original instruction snapshot unless explicitly amended through PB-016.
4. Pin changes only deliberate ordering. Status updates cannot reorder the collection under the pointer.
5. Archive previews active tasks and routines. User chooses finish existing work or cancel/reconcile it; associated routines become `paused`, profile moves out of normal view, drafts/results remain searchable.
6. Restore returns the profile without silently resuming routines. Missing saved conversation offers a new linked conversation, explaining that inaccessible old messages were not recovered.

**Recovery:** Save error retains draft; repeated Save does not duplicate profile. F1/F7; A0 for edits, A1 for consequential archive choice. **Acceptance:** [PB-011](../quality/ACCEPTANCE.md).

<a id="pb-012"></a>
## PB-012 — Find a conversation and keep your place

**Entry:** Home → Conversations or Pebbi history. **Input:** query, read/archive/pin action, draft and preview selection. **Output:** stable local view state and explicit read flags.

1. Enter query; return matching local conversations with Pebbi, title, snippet and date. Include archived results only through the visible filter. Selecting one restores scroll, open file and its own draft/attachments.
2. Scroll up to load older messages while preserving the first visible anchor. New replies below the viewport do not move the reader; Jump to latest explicitly moves and clears its new-result count.
3. Type an unsent draft, switch Pebbi/surface, then return or relaunch. Restore exactly that conversation's draft and attachment references; never send on switch.
4. Mark unread explicitly shows unread even in the open chat. It remains until Mark read, or leaving and reopening the chat as a read action; incoming token renders alone do not clear it. Mark read works without opening.
5. Pin/archive changes local organization. Archive does not cancel work or hide its pending approval from Home's attention section. Delete separately previews permanent local loss and active-task effects, then confirms.

**Recovery:** Missing record offers Create fresh conversation tied to the same Pebbi, preserving known task metadata and disclosing unavailable history. Search no-result and extraction failures are distinguishable. F0/F1/F7; A0 except destructive confirmation. **Acceptance:** [PB-012](../quality/ACCEPTANCE.md).

<a id="pb-013"></a>
## PB-013 — Approve memory and continue a long conversation

**Entry:** Pebbi profile → Memory, proposed memory card, or context limit reached. **Input:** source fact, user edit/forget and conversation context. **Output:** versioned approved memories and inspectable compacted context.

1. A model proposes a fact with source and intended global/Pebbi scope. User chooses Save, Edit or Not now; no consent means it remains absent from durable memory.
2. In Memory, user sees every saved item with provenance. Editing/forgetting commits locally and invalidates derived summaries containing the old fact before the next request.
3. Before a context limit, obtain the current verified `tokenBudget` from capabilities; apply its estimator, provider capacity, operator clamps and reserved-output/headroom rules. Assemble a compaction summary retaining goals, constraints, approved memories, source links, incomplete steps and unresolved approvals. Keep original history accessible; expose the summary and its coverage. Missing/unusable budgeting prevents reasoning readiness, not local browsing; never guess a context size.
4. A new request reads only the latest permitted memory and summary versions and sends the current `tokenBudgetId`. A changed-budget rejection refreshes and re-estimates before dispatch. A provider context-limit error invalidates budgeting and preserves instructions/evidence for explicit recovery, never hidden deletion or blind retry. If compaction fails or critical context is ambiguous, task becomes `waitingForInput` with a concrete clarification, not a loop rejecting all messages.
5. Forget explains that it removes future remembered context, not original chat messages. User may navigate to/delete original messages separately. A private session makes no automatic durable memory.

**Recovery:** Conflicting memories ask which is current; secret-like data is rejected; missing original history is marked unavailable rather than reconstructed as fact. F0/F7; A1 for proposed facts, A0 for direct user edits. **Acceptance:** [PB-013](../quality/ACCEPTANCE.md).

<a id="pb-014"></a>
## PB-014 — Attach and read a whole document

**Entry:** Composer attachment control, drag/drop or intentional paste. **Input:** selected file(s), question or attachment-only send. **Output:** managed attachments, extraction manifest and cited answer/preview.

1. Validate type, declared size and current limits before accepting processing. Import within the chosen file scope and show name/size; failed drops leave typing functional and explain the rejected item.
2. Sending an attachment alone asks what to do or offers accessible read/summary actions; it never guesses a consequential workflow. Explain cloud disclosure before sending content to reasoning.
3. Task `queued` → `running` reads every supported page/section and records coverage, extraction method and unreadable portions. Scanned content uses available OCR; no OCR availability means a stated gap, not a complete-read claim.
4. Answer cites page/section evidence, including material beyond the visible preview. If limits prevent complete reading, stop at `waitingForInput` with split/select options or deliver an explicitly approved partial result.
5. Open preview beside chat; expand, Quick Look, Open in app or Show in Finder are deliberate navigation. Changed Markdown refreshes safely; scripts/macros never execute. Switching conversations preserves independent preview state.

**Recovery:** Encrypted document requires user manual unlock; corrupt/unsupported/oversize files keep their original attachment reference and error. Missing external original cannot invalidate a successfully imported copy. F0/F1/F7; A1 for remote disclosure. **Acceptance:** [PB-014](../quality/ACCEPTANCE.md).

<a id="pb-015"></a>
## PB-015 — Ask for work and receive a verified result

**Entry:** User sends an actionable task. **Input:** original request, context manifest, workspace and allowance. **Output:** attempt event journal, artifacts, verification and actual usage.

1. Save the message with a unique submission identity. Create logical task/attempt and show `queued` with named Pebbi and goal. Reserve required initial usage; lack of entitlement goes to PB-028.
2. Scheduler admits to `running`; persist the current operation before dispatch. Stream actual events ordered by task-local sequence. Distinguish preparing, attempted and verified steps in text, without inventing enum states.
3. At missing consent/input/connection, enter the matching wait state and present a resumable action. Resume the same attempt in `running` after the requirement and scheduler resources are resolved and revalidated.
4. Tool writes record intent, execute once and read back the exact target. Files record location, content/version and test evidence. Unknown side effects block retry and remain explicit.
5. On verified goal completion set `succeeded`; collapse steps into an inspectable history and show final artifacts, citations and limitations. Finalize metering from trusted provider/backend records.
6. On unrecoverable failure set `failed`, retain partial outputs and offer linked Retry only after reconciliation. Closing Home is not cancellation.

**Recovery:** Stream reconnect resumes from journal sequence, deduplicates events and cannot resend a write. A provider acknowledgement is not an external success receipt. F0/F7; A1/A2 apply to every real action. **Acceptance:** [PB-015](../quality/ACCEPTANCE.md).

<a id="pb-016"></a>
## PB-016 — Run two Pebbis and send a racing follow-up

**Entry:** One Pebbi is starting/running while user addresses it or another Pebbi. **Input:** follow-up, approved suggestion or new independent request. **Output:** exactly one ordered association and visible queue.

1. Save incoming message immediately. Resolve explicit name/focused context; ambiguous “retry it” becomes `waitingForInput` before any retry.
2. Serialize destination assignment with the active attempt's lifecycle. If it still accepts input, attach to its next safe checkpoint and acknowledge delivery. If it has become terminal, create one new `queued` attempt linked to the prior result.
3. Voice and standalone dictation use separate audio owners and never occupy this queue. A second agent task for the same Pebbi joins its queue; a different Pebbi may run concurrently under actual capacity. Approved suggestion sources travel with their queue entry.
4. For shared file or interactive-control resource, obtain exclusive lease before dispatch. Waiting for capacity remains `queued`; do not interleave two writes or two typists. User may inspect/reorder not-yet-running tasks; running task order cannot be rewritten silently.
5. When the active attempt reaches terminal state, release leases and admit next valid queue entry. If follow-up changed a pending action, invalidate its old approval and present the new preview.

**Recovery:** Crash restores message/queue order from journal. Duplicate submissions return the existing association; archived Pebbi asks to restore or reassign. F0/F7; A4 handles amended actions. **Acceptance:** [PB-016](../quality/ACCEPTANCE.md).

<a id="pb-017"></a>
## PB-017 — Approve, deny, stop and retry safely

**Entry:** Task requests an action outside current scope, or user wants to stop work. **Input:** immutable action preview/decision or Stop. **Output:** audit trail, reconciled cancellation or linked retry.

1. Move attempt to `waitingForApproval`; show Pebbi, app/connector, exact operation/target, transmitted data and consequence. High-risk actions omit persistent grant choice; payment/credential/OS-auth entry remains manual.
2. `allowOnce` authorizes this version only. Eligible `allowForScope` additionally displays bounded resource/expiry. `deny` dispatches nothing; if essential, enter `waitingForInput` for a revised plan or End task. Protected-effect `allowOnce`/`allowForScope` is recorded only by deliberate accessible native approval-control activation against this preview. Unambiguous spoken “yes,” replayed transcripts and model assertions are not consent and leave the action in `waitingForApproval`. Voice may select low-risk work or open this review; keyboard/VoiceOver activation is fully supported without requiring a pointer.
3. Before dispatch, revalidate approval version and target. Stale/edited proposals ask again. User may revoke scopes in Settings at any time; next call must honor revocation.
4. Stop task changes running/waiting states to `cancelling`, disables new calls, requests cancellation and reconciles inflight effects. An undispatched `queued` attempt cancels directly to `cancelled`. Speech stops promptly, but Stop speaking alone never runs this path.
5. Once safe dispatch cessation is established, show `cancelled` with known changes and any unknown outcome. Unknown writes retain a prominent unresolved warning and disabled automatic Retry.
6. User chooses Retry after reconciliation: create a new `queued` attempt with linked history and fresh high-risk approvals, not mutate the terminal attempt.

**Focus:** F4/F5/F7; Stop remains keyboard reachable during takeover. **Acceptance:** [PB-017](../quality/ACCEPTANCE.md).

<a id="pb-018"></a>
## PB-018 — Operate a native app, escalating only when needed

**Entry:** User asks for a specific action in a named app/window. **Input:** bounded goal, OS permission and approved action scope. **Output:** verified app change and released control lease.

1. Inspect AX semantics and identify target app/window/element. Classify action risk and preview missing authority. Obtain relevant A1/A2 approval before input.
2. If the semantic action is truly background-safe, dispatch to the target without moving cursor/activating app. Read back changed semantics or visible effect before another action.
3. If AX cannot perform it, pause in `waitingForApproval` and explain foreground takeover, pointer movement, bounded steps and Stop. No “background” label may conceal CGEvent delivery.
4. After explicit takeover approval, revalidate window and acquire exclusive control lease. Show ongoing indicator, perform one bounded step, reinspect and verify. User intervention pauses rather than competes with their input.
5. Completion releases lease/restores prior focus where safe and reports verified changes. If the action needs credential/permission/payment UI, move to `waitingForInput` and ask the user to complete it manually.

**Recovery:** Vanished target, unreliable capture, blocked AX or managed policy offers guided manual alternative. Never repeat confirmed input; uncertain input is inspected before retry. Stop uses PB-017, not assumed rollback. F3/F5; A3 cannot be automated. **Acceptance:** [PB-018](../quality/ACCEPTANCE.md).

<a id="pb-019"></a>
## PB-019 — Use a chosen browser tab or separate window

**Entry:** Browser task with Chrome/Brave selected. **Input:** extension/helper readiness and explicit profile/window/tab scope. **Output:** scoped DOM artifacts/actions and target verification.

1. If disconnected, Connections explains extension installation and native helper pairing; user approves in browser. Perform authenticated handshake/discovery before connection becomes `ready`.
2. Ask Use this tab or Open dedicated window. Show selected browser/profile and current tab/domain. A dedicated window is created only after consent and is visibly associated with the task.
3. Task `queued` → `running` reads DOM/text first. Document/element references belong to current navigation; re-read after navigation before action. Off-scope domains/tabs require fresh A1 consent.
4. Before clicks/forms, classify action and obtain A2 for outbound submission, publishing, destructive changes or money. Login/secret surfaces pause for manual user handling; access granted afterward is rechecked, not guessed.
5. Verify result in the exact selected page/account. Leave/close the dedicated window according to user choice; cleanup cannot close unrelated tabs. Disconnect removes new access and updates active context.

**Recovery:** Closed tab or extension crash gives `waitingForConnection`/`waitingForInput`. Unsupported browsers offer manual open or separately approved native control, never an unannounced profile-debugging workaround. F0/F3/F5; no focus takeover from a DOM read. **Acceptance:** [PB-019](../quality/ACCEPTANCE.md).

<a id="pb-020"></a>
## PB-020 — Research, count evidence and deliver an artifact

**Entry:** User requests a question answered or a defined set of items. **Input:** scope, dates, quantity and allowed public/private sources. **Output:** cited answer, source ledger and requested file.

1. Save explicit selection criteria and quantity. If material ambiguity changes collection, ask in `waitingForInput`; otherwise use stated/default scope and begin `running`.
2. Retrieve sources, preserve URL/title/access time and distinguish publication dates. A search result is discovery, not proof that its full page was read. Private connector reads stay within selected scopes.
3. Save item-level evidence as collected; deduplicate/count programmatically in the runtime. Compare collected count against requested count before declaring completion.
4. On blocked page, try appropriate authorized alternate source and mark its provenance. Login walls need user access; no invented content or access bypass. Treat webpage instructions as data, never new tool authority.
5. Answer with citations adjacent to claims, uncertainty/conflict where needed and completeness status. Create the requested artifact in the Pebbi workspace and verify its rows/content.
6. If mandatory evidence remains unavailable, show partial artifact plus explicit gap and ask whether to narrow/continue; do not call an incomplete mandatory result fully successful.

**Focus/approval:** F0 for research; A0 for requested public reads, A1 for private disclosure and A2 for publishing/sending results. **Acceptance:** [PB-020](../quality/ACCEPTANCE.md).

<a id="pb-021"></a>
## PB-021 — Create files and run bounded code

**Entry:** User requests an artifact or executable work. **Input:** goal, managed workspace, external folder grants and optional command. **Output:** file manifest, verified content and genuine execution/test evidence.

1. Resolve intended destination inside the Pebbi workspace. External path needs an explicit folder selection; normalize/canonicalize and check symlink containment before access.
2. Even from an empty workspace, obtain authored content through explicit `stageTextArtifact` chunks; staging never edits a target file and ordinary assistant prose is not a file. Native finalization returns immutable `artifactId`, `byteCount`, `sha256` and `mimeType`. Use those actual values for separately authorized `createFile`/`replaceFile`, with atomic commit and readback. For overwrite, show destination/diff and obtain required approval; preserve existing file if replacement fails. Cancel cleans unfinished drafts; private drafts/artifacts stay in RAM until explicit Save consent, without private content/hash in the metadata-only journal.
3. If execution is needed, preview command/executable, arguments, working directory, filesystem/network access and limits. Missing runtime/environment is reported; do not silently install or pay for prerequisites.
4. Verify `scriptArtifactId`/`expectedSha256` against the actual same-account/workspace artifact. After the user reviews those full immutable script bytes and referenced inputs and grants fresh native `allowOnce` for this run, task runs under declared resource bounds. Capture actual exit status/output, support Stop and do not claim an allowlist is OS sandboxing. Network/external side effects still need appropriate scoped/high-risk approvals.
5. Validate outputs by reopening/parsing and running only genuine tests. Final response says Generated, Executed or Tested accurately; failures retain files and real evidence.
6. Files preview/open/export links identify the exact artifact and producing attempt, not an approximate path.

**Recovery:** Path escape, concurrent edit, disk-full and timeout stop safely. Unknown external process effect reconciles before retry. F0/F3; A1/A2. **Acceptance:** [PB-021](../quality/ACCEPTANCE.md).

<a id="pb-022"></a>
## PB-022 — Connect an app, expire and reconnect

**Entry:** Connections catalog or task missing a connector. **Input:** catalog entry, requested scopes and selected account. **Output:** verified connection capabilities and local revocable credentials.

1. Open an entry; show real support level, read/write operations, required operator configuration and data disclosure. Unconfigured entry is visible but cannot pretend to launch working auth.
2. User chooses Connect and scope. Connection `disconnected` → `connecting`; OAuth opens system browser, native app integration checks its actual local permission path. User handles auth manually.
3. Validate returned identity/scopes, store required tokens in Keychain and perform a minimal authorized capability check. Only then mark `ready`. Partial scope is `degraded` with unavailable tools explained.
4. Update capability context immediately for existing voice/tasks. A waiting task rechecks scope/resources and resumes `running`; connection consent does not grant permission to send messages/publish/pay.
5. On expiry/revocation mark `expired` and pause dependent calls at `waitingForConnection`. Reconnect repeats validated auth, preserving task context. Disconnect stops new calls, removes token material and retains history without secrets.

**Recovery:** Cancel returns `disconnected`; network/protocol failure is `failed`, wrong account requires deliberate reselection. Never replace user account with a developer's. F1/F4; A1/A2/A3. **Acceptance:** [PB-022](../quality/ACCEPTANCE.md); actual adapter behavior is defined in [Tools](../engineering/TOOLS.md).

<a id="pb-023"></a>
## PB-023 — Add a custom MCP safely

**Entry:** Connections → Add custom connection. **Input:** remote HTTPS URL or executable + separate arguments, workspace, auth choice. **Output:** validated connection and reviewed tool inventory.

1. User chooses remote or local. Validate format without launching code; reject URL-embedded secrets and invalid TLS. Local form explicitly warns that a server command runs on the Mac.
2. Show exact origin/command, arguments, workspace and environment variable names; protected secret entry goes to Keychain and never into logs/export. Require first-launch consent for local code; never interpret input as an implicit shell command.
3. Connection becomes `connecting`; handshake and discover tools read-only. Show tool descriptions as untrusted metadata and classify read/write/destructive/external effects before enabling them.
4. User enables chosen tools; a successful check marks `ready`. An existing waiting task may then resume `running` after resource revalidation, with its own action approval requirements.
5. Updated schemas, executable or origin trigger re-review of changed authority; disconnect stops owned local server processes and invalidates grants. Quit stops helpers rather than leaving a daemon.

**Recovery:** Unsupported auth, malformed schema, startup timeout and failed process appear as redacted `failed`/`degraded` with Edit and Retry. An instruction embedded in a tool description cannot authorize itself. F1/F4; A1/A2/A3. **Acceptance:** [PB-023](../quality/ACCEPTANCE.md).

<a id="pb-024"></a>
## PB-024 — Receive, adjust and approve a sourced suggestion

**Entry:** Suggestions first opt-in or daily local research trigger. **Input:** opted-in sources/lookback and user preference. **Output:** versioned proposal or one approved queued task.

1. Explain read-only research, default 72-hour lookback and local schedule. User selects sources/frequency; no opt-in means no suggestion reads.
2. Research uses only read tools, persists supporting source references and records unavailable sources. Proposals identify named Pebbi, concrete result, rationale and likely access/usage requirements.
3. Show one proposal. Skip moves to next and optionally records reason; Dismiss closes invitation. Neither starts work. Adjust opens a draft version; Cancel restores the unchanged original and stops pending adjustment speech.
4. Approve on the visible proposal, or unambiguous spoken selection of a low-risk proposal, atomically records task selection and creates one `queued` task carrying source details/snapshots. This is not a protected-action grant. Speech can instead open the named review. Busy Pebbi retains queue entry; repeated selections reuse it.
5. Before execution, revalidate source availability and action version. Research consent does not authorize high-risk action: PB-017 still prompts at the exact send/publish/payment/destructive step.
6. Opening Suggestions or dismissing greeting clears pending invitation, preventing later repeated greetings.

**Recovery:** Expired source connection explains missing evidence rather than inventing an idea. Changed material or ambiguous voice target requires `waitingForInput`. F0/F4/F7; A1 source consent, A5 low-risk task selection, A1/A2 native approval for protected effects. **Acceptance:** [PB-024](../quality/ACCEPTANCE.md).

<a id="pb-025"></a>
## PB-025 — Schedule, catch up, pause and recover a routine

**Entry:** User asks to repeat a task or opens Routines → New routine. **Input:** task, Pebbi, timezone/schedule and source scope. **Output:** routine definition, next due and durable run history.

1. Parse request into an editable preview; show timezone, next occurrence and “Runs on this Mac while Pebbi is open.” Ambiguous time remains a form question, not a guessed background schedule.
2. Confirm commits `active` if dependencies are ready, otherwise `blocked` with named dependency. Every due event is identified once; duplicate ticks cannot enqueue duplicate runs.
3. At due time, ready/idle Pebbi receives a `queued` task. Offline/busy/sleep postpones and coalesces missed occurrences to one catch-up. Quit runs nothing. On next launch advance past the closed-app backlog, show the next scheduled run and offer explicit Run now for missed work.
4. Task uses ordinary approvals. High-risk routine steps wait for fresh approval; denied action does not repeatedly retry. Results land silently in the same conversation with unread marker.
5. A transient failed occurrence allows at most two additional safe attempts, after one minute and five minutes within a fifteen-minute retry window; show the next retry time. Exhausting those retries counts as one failed occurrence. Three consecutive failed occurrences set `paused`; success resets the streak. Each occurrence also obeys its approved usage ceiling. No retry occurs while a prior external outcome is unknown. Waiting, cancellation and coalesced slots are not failed occurrences.
6. Pause cancels future scheduling, not silently the current task; user is asked whether to stop current run. Resume rechecks to `active`/`blocked`. Archive restores later as `paused`; archiving the Pebbi pauses its routines.

**Time rules:** One execution per repeated DST occurrence; nonexistent wall time advances to next valid local instant; changing timezone previews next due before confirmation. F0/F4; A1 schedule, A2 side effects. **Acceptance:** [PB-025](../quality/ACCEPTANCE.md).

<a id="pb-026"></a>
## PB-026 — Deliver a result without taking attention

**Entry:** Background task/routine completes, approval awaits, or suggestions become ready. **Input:** event, quiet policy and available Focus/call/share signals. **Output:** persistent in-app result/unread and optional permitted notification.

1. Persist result/attention event before deciding presentation. Background completion never focuses Home or changes Space (F0).
2. Routine result marks its conversation unread and stays silent. Interactive task may use configured cue; sensitive lock-screen content remains redacted.
3. Suppress optional sound/greeting when Focus, detected call/share or manual Quiet applies. Detection gaps are disclosed; Quiet always overrides. A waiting approval remains visible in Home even when notifications are suppressed.
4. Coalesce suggestion invitation to one pending invitation. On opening Suggestions or dismissal, remove it; on wake do not replay every suppressed sound or old greeting.
5. User explicitly opens notification/result; Home selects that conversation and marks it read. Explicit Mark unread follows PB-012 rather than clearing immediately because it is on screen.

**Recovery:** OS notification denied/unavailable affects notification only, not result storage. Audio device failure cannot drop the message. User can navigate Home → attention/result without a banner. F4/F7; A3 for notification permission, no extra action authority from tapping a result. **Acceptance:** [PB-026](../quality/ACCEPTANCE.md).

<a id="pb-027"></a>
## PB-027 — Understand usage and change plan

**Entry:** Settings → Account/usage or task usage gate. **Input:** server plans/ledger and user-selected billing operation. **Output:** authoritative entitlement, reservation and billing status.

1. Fetch configured plan/usage data. Show consumed/reserved/available with unit and reset policy; unavailable prices show configuration unavailable, not invented amounts.
2. User chooses a plan/Manage subscription; show currency, interval and terms from server then open hosted Checkout/Portal deliberately. Move perch aside so the card remains usable.
3. User completes payment authentication manually. Returning browser is only navigation; show checking status while reading authoritative account state.
4. Signed/idempotent webhook processing and readback determine actual plan. On verified change update entitlement/usage; on cancellation retain old plan; on pending event show pending confirmation without granting unearned access.
5. Before task work, reserve allowance. After actual provider/tool consumption finalize server-side; abandoned/no-work reservation is reconciled under server policy. Extra-usage approval states it uses existing allowance, not a card charge.

**Recovery:** Link-open failure restores card with error and Retry. Duplicate/out-of-order webhooks cannot double-charge ledger/grant. Missing live Stripe IDs leaves paid checkout unavailable while local work continues. F1/F4; A2/A3, never automate purchase UI. **Acceptance:** [PB-027](../quality/ACCEPTANCE.md).

<a id="pb-028"></a>
## PB-028 — Reach a limit or unavailable model without losing work

**Entry:** Preflight or active request discovers insufficient quota/provider readiness. **Input:** authoritative capability/error/entitlement and saved request. **Output:** truthful blocker, retained partials and valid options.

1. Save pending message/attachment references before request. Preflight checks the exact role/usage class; catalog visibility alone does not count as connection readiness.
2. Missing provider/deployment moves task to `waitingForConnection`; voice shows `unavailable`. Runtime voice failure uses `failed`; dictation failure retains recoverable transcript. Quota decision gives task `waitingForInput`.
3. Show affected feature, known reason and next action: reconnect, administrator configuration, wait until stated reset, review plan, or continue an actually ready local/typed task path. Never silently substitute selected models.
4. User may close the notice without losing draft. A bounded retry checks readiness again; if restored, resume the waiting attempt in `running` after resource revalidation, or create a new linked `queued` attempt if the prior attempt was terminal.
5. Reconcile usage reservation based on actual consumption and retain generated output. Do not bill unperformed work from optimistic client counters.

**Known blocker:** Selected realtime failed the recorded Azure operation and dictation actual audio failed deployment lookup; neither is live accepted until reverified. These facts never become a fabricated successful demo. F0/F4; usage consent separate from A2 payment. **Acceptance:** [PB-028](../quality/ACCEPTANCE.md).

<a id="pb-029"></a>
## PB-029 — Change preferences without changing the task

**Entry:** Home → Settings. **Input:** device-scoped or account-scoped preference edit. **Output:** validated persisted value and effective capability update.

1. Open requested category with current effective value and scope. Do not play preview audio or start mic capture just by opening Voice.
2. User selects a voice and explicitly presses Preview. Run normal live voice path; unavailable preview says so and retains last working choice. Cancel stops only preview speech.
3. User selects device/language/dictation-review/dictionary/appearance/quiet options. Validate and save; changes that affect active capture apply at a safe boundary with disclosure through PB-034.
4. Shortcut recorder temporarily owns keyboard input, shows exact gesture, checks conflicts and saves only valid choice. Escape cancels recorder; Reset restores validated defaults without triggering talk/dictation.
5. Existing conversations receive updated allowed capability/preferences without losing messages or changing locked provider roles. Settings close restores deliberate prior focus.

**Recovery:** Missing device, unsupported option or save error keeps prior value and displays an actionable issue. Secrets are never stored in ordinary preference fields/export. F1/F7; A0 for settings, A3 for device permissions. **Acceptance:** [PB-029](../quality/ACCEPTANCE.md).

<a id="pb-030"></a>
## PB-030 — Export data and delete with explicit scope

**Entry:** Settings → Privacy & data or Account. **Input:** selected local/server data scope and user confirmation. **Output:** validated export or truthful per-scope deletion receipt.

1. Offer local export, account export and combined app-driven package; explain that server account data does not include local chats/files. User chooses destination in native save UI.
2. Local exporter snapshots selected data/artifact manifest excluding secrets/transient captures, writes package and verifies readability/counts. Server export authenticates request and retrieves real artifact; combine only when both succeed, naming any missing scope.
3. For deletion, show exact scope, active work, subscription consequences and legal retention limits. Offer export first. Require explicit confirmation and reauthentication where necessary; never infer deletion consent from sign-out.
4. Stop/reconcile affected tasks, disable routines/new work, then perform requested local deletion and/or authenticated server deletion. Each scope reports its actual result; a failed server deletion cannot be labeled “all deleted.”
5. Account completion requires authoritative confirmation and token revocation. Other devices' local stores are not claimed erased; give truthful instructions for deleting those local copies.

**Recovery:** Disk-full/expired export link retains original data. Offline local deletion may finish while server deletion remains visibly pending/request not completed; never silently discard the server intent. F1/F4; A2/A3. **Acceptance:** [PB-030](../quality/ACCEPTANCE.md).

<a id="pb-031"></a>
## PB-031 — Choose privacy boundaries and revoke them mid-task

**Entry:** First disclosure, Settings → Privacy & data, or Pebbi private-session control. **Input:** retention/source/memory/suggestion choices. **Output:** inspectable context manifest and enforced retention/grant changes.

1. Show what stays local, what approved content goes to the backend/model, and what minimal account/usage records remain. Do not claim on-device inference.
2. User chooses retention and independent memory/suggestion consent. A private session disables durable conversation/memory/artifact retention except explicitly saved outputs, necessary minimal usage/security accounting and minimal unresolved-effect reconciliation metadata; clearly disclose these exceptions before composing.
3. Before sending, assemble context only from current allowed sources. Sensitive/secret material pauses for redaction; secure fields are never captured for convenience. User can inspect included context.
4. Revoking a source/grant invalidates future calls immediately; active task waits in `waitingForInput` or `waitingForConnection` with partial work preserved. Already transmitted content cannot be falsely recalled.
5. Retention cleanup removes expired local items and derived summaries consistently while preserving minimal required accounting. Forget-memory and delete-history remain distinguishable.

**Recovery:** Cleanup/storage failure is visible; diagnostics exclude content regardless of consent to product analytics. Export/deletion explain provider/legal limits. F0/F7; A1 for scope changes, A3 for manual secret handling. **Acceptance:** [PB-031](../quality/ACCEPTANCE.md).

<a id="pb-032"></a>
## PB-032 — Finish the same job using keyboard and VoiceOver

**Entry:** Any main flow with VoiceOver/reduced motion/large text enabled. **Input:** accessibility settings and keyboard commands. **Output:** equivalent task outcome without pointer/voice dependency.

1. Open Home; focus lands on a meaningful existing control, not decorative mascot. Navigate sidebar, Pebbi selector and composer in stable order; control names expose purpose/state.
2. Submit a typed task and hear one semantic start announcement. Streaming tokens remain readable without constantly moving focus. Jump to latest is explicit.
3. At approval, announce target, consequence and options. User can review full preview, choose allow/deny or Stop using keyboard alone; no hover or spoken-only control is required.
4. For guided work, every visual mark has text target/instruction and accessible Next/Back/Pause. Reduced motion swaps decorative transitions for static state without hiding progress.
5. At completion, announce concise result availability and retain focus unless user opens it. Large text/small window scrolls to all controls; contrast/shape/labels make state distinguishable without color.

**Recovery:** Audio unavailable leaves complete typed path. Focus loss to removed element returns to its owning section, not arbitrary composer auto-submit. F7 and all safety approvals are unchanged; accessibility is not an exception to scopes. **Acceptance:** [PB-032](../quality/ACCEPTANCE.md).

<a id="pb-033"></a>
## PB-033 — Move displays and Spaces during work

**Entry:** User changes monitor topology, scaling, active Space or perch preference. **Input:** live display IDs/geometries and saved policy. **Output:** reachable windows and valid screen targets.

1. Choose fixed perch display or follow-active-display policy in Settings. Place perch within safe visible bounds independent of hardware notch.
2. Open Home/guide on a selected display. Convert coordinates through actual display/window scaling; do not assume all display origins are positive or equal scale.
3. On disconnect/rearrangement, invalidate affected overlay/capture target. Task needing that target becomes `waitingForInput`; unrelated research continues.
4. Move stranded surfaces to the nearest remaining visible display safe area, clamping their size/position. Ask user to confirm new capture/action scope before reinspection; old pixels never authorize a new target.
5. Switching Spaces/full-screen does not make background completion drag the user back. Menu bar and explicit Home invocation remain available; notchless/external displays do not masquerade as permanently open menus or swallow shortcuts.

**Recovery:** No selected display available chooses a remaining visible display deterministically, reports the reassignment and retains preferences for user review. F0/F3/F6; A1 for changed scope. **Acceptance:** [PB-033](../quality/ACCEPTANCE.md).

<a id="pb-034"></a>
## PB-034 — Recover from a headset, mic or call interruption

**Entry:** Active voice/dictation or explicit device selection. **Input:** real route/format events, consent and partial transcript. **Output:** preserved text and explicit resumed/ended session.

1. Before audio starts, validate chosen input/output format and actual permission. Warm playback only within explicit audio use; no unconsented always-active mic.
2. On route change/call, stop invalid audio work and persist finalized text. Voice becomes `interrupted`; dictation moves to review of retained partial on user choice or `failed` with recovery text.
3. Show device lost/interrupted notice and offered input. Built-in fallback starts automatically only if the user previously opted in; otherwise ask. Always show which mic is now used.
4. After valid route/permission, user Resume leads voice through `connecting` to `listening`, or starts a new dictation segment linked to retained text. If user had stopped/cancelled, a late route event must not restart capture.
5. Playback uses safe pre-roll and route timing; mute shows text/Open transcript rather than overwriting clipboard. Selected device preference remains visible if temporarily unavailable.

**Recovery:** Repeated no-audio/format failure reports specific diagnosis and typed alternative, not silent deafness. Preserve partial work when provider reconnection fails. F0/F2; A1 for fallback choice, A3 for OS permission. **Acceptance:** [PB-034](../quality/ACCEPTANCE.md).

<a id="pb-035"></a>
## PB-035 — Recover local work after offline, sleep or crash

**Entry:** Loss of network, wake or app relaunch after unclean exit. **Input:** durable local journal and current capability/device state. **Output:** restored drafts/view, reconciled attempts and safe retry choices.

1. Network loss leaves local Home/search/drafts/exports usable. Network-dependent active work enters `waitingForConnection` when resumable; partial outputs remain visible.
2. On wake, recheck account, provider, connector, OS permissions and audio routes before resuming capability. Never automatically open the mic. Routine due events coalesce through PB-025.
3. On crash recovery, mark all previously active attempts `interrupted` before presenting status. Restore queue and drafts independently from attempting task execution.
4. For every prior external operation, inspect intent and provider/target receipt. Known successful write is recorded without repeating; known unperformed read may be offered for safe retry; unknown write waits for user/manual reconciliation.
5. User chooses resume/retry only after assessment. Create linked `queued` attempt, invalidate stale targets/grants and request fresh high-risk approval. Old attempt closes as `failed` with interruption reason or `cancelled` after classification; its evidence remains unchanged.
6. Missing/corrupt conversation/store segment shows bounded recovery/export guidance; never claim reconstructed text is original history.

**Recovery:** Connection retry is bounded and visible. A duplicate event or delayed callback cannot repeat write or reopen completed task. F0/F4; A4/A2. **Acceptance:** [PB-035](../quality/ACCEPTANCE.md).

<a id="pb-036"></a>
## PB-036 — Install a secure update or recover from one

**Entry:** Settings → Support & Updates, or nonintrusive update notice. **Input:** trusted version/feed/package and user install choice. **Output:** verified install/data migration or safe rejection.

1. Check actual update feed; show current/available version and release notes. Download and Install and relaunch are separate explicit actions. No signed release means no live download promise.
2. Verify package authenticity/integrity before replacement; a bad signature stops with error while current version stays intact.
3. Before install, list active tasks and save drafts. User either returns to work or approves stopping/reconciling and relaunch. Follow PB-017/PB-035 for task effects.
4. Install verified package and run explicit compatible migrations with recovery protection. On success reopen saved state and show concise release notes without stealing focus from other apps.
5. On migration/install failure retain/restore supported working version and data. Rollback is offered only for a signed build compatible with the current store or a verified supported backup restore path.

**Recovery:** Never fetch an unsigned substitute or downgrade data blindly. Missing Developer ID/notarization/Sparkle authority is a release blocker; local implementation/tests continue separately. F1/F4; A3 for real signing/install authority. **Acceptance:** [PB-036](../quality/ACCEPTANCE.md).

<a id="pb-037"></a>
## PB-037 — Inspect diagnostics and ask for support

**Entry:** Settings → Support & Updates or an error's diagnostics link. **Input:** chosen range, reproduction notes and consent. **Output:** redacted export and optional verified support receipt.

1. Show product/OS/version and capability health, explicitly distinguishing disconnected roles from app defects. User selects diagnostic range/categories; content bodies, screenshots, audio and credentials are excluded by design.
2. Generate a preview with redacted identifiers/paths and allow removal of optional fields. Run redaction checks before export/send; seeded sensitive content must not escape.
3. Export locally through save UI or explicitly choose Send support report. Show destination and included data; outbound send requires A2 approval.
4. After submission, read authoritative receipt/status and show Sent only when verified. If upload fails, retain local bundle with Retry or Copy support link.
5. Product analytics consent is separate; disabling it cannot disable required privacy-safe security/usage accounting. Public support documentation remains reachable without sending telemetry.

**Recovery:** Broken support link offers a verified alternative, never an invented address. Redaction failure blocks delivery until corrected, not merely warns after send. F1/F4; no background report submission. **Acceptance:** [PB-037](../quality/ACCEPTANCE.md).

<a id="pb-038"></a>
## PB-038 — Stay responsive during heavy work and idle quietly

**Entry:** Long history/document/concurrent workload or no active user work. **Input:** actual workload and declared device budget. **Output:** bounded responsive execution and measured report.

1. Queue work beyond configured capacity instead of launching unlimited tasks. Keep one active attempt per Pebbi and interactive-control exclusivity.
2. Render first truthful progress after actual admission. Large extraction/history work stays off UI-critical execution; Stop and scrolling remain available.
3. If pressure/latency grows, show real queue/wait information and preserve cancellation. Timeout is failure/explicit wait with partial artifacts, never an invented completed response.
4. When surfaces hide, stop offscreen animation and unnecessary polling/capture. Idle means no continuous audio/screen/AX activity without an explicit active capability.
5. In verification, measure declared cold/warm scenarios, long-session growth and idle CPU/power on actual hardware. Record settings/workload/version and compare with pinned engineering/acceptance budgets.

**Recovery:** Thermal/provider/network slowness changes measured result, not the test evidence. Missing hardware leaves corresponding performance gate unverified. F0/F7; increasing paid capacity/resources needs separate authorization, not an optimization shortcut. **Acceptance:** [PB-038](../quality/ACCEPTANCE.md).

<a id="pb-039"></a>
## PB-039 — Discover, download, get support and manage account on web

**Entry:** Public selected domain or explicit in-app link. **Input:** anonymous navigation or authenticated account action. **Output:** truthful accessible page, actual download or verified account/support operation.

1. Public page identifies Pebbi as AI and states actual macOS requirement/release availability. Navigation reaches support, privacy, account and download without dark patterns or copied reference branding.
2. Download shows real version/platform and only links to a verified signed artifact. If release/domain configuration is incomplete, show unavailable information; no dummy file or claimed ownership.
3. Privacy explains local-versus-server data and verified operator/provider disclosures. Support shows real configured contact/routing; legal text cannot invent entity, address or certification.
4. Account sign-in uses validated browser auth. Usage/plan/export/delete pages read authoritative state and explicitly exclude nonexistent local-content sync. Billing and deletion use PB-027/PB-030.
5. User returns to app through a validated destination or keeps using web account management; no browser page becomes the native app shell.

**Recovery:** Invalid sign-in retains safe return path; unavailable server data displays error, not zero usage; missing download/support config blocks launch acceptance. F1 for user-opened link; A2/A3 for consequential actions. **Acceptance:** [PB-039](../quality/ACCEPTANCE.md).

<a id="pb-040"></a>
## PB-040 — Decide honestly whether the whole product is ready

**Entry:** Candidate build and authorized verification environment. **Input:** all PB cases, real artifact and actual credentials/hardware/permissions where supplied. **Output:** evidence manifest and release decision.

1. Validate that each PB-001–PB-040 exists in requirements, this flow document, screens, acceptance and machine-readable coverage. Missing linkage is a coverage failure, not an implicitly excluded feature.
2. Run native installation/onboarding, typed/live voice/dictation, capture/guidance, persistence/memory/files, task concurrency/approvals, native/browser/connectors, suggestions/routines, billing/privacy/export/delete, accessibility/hardware/recovery/update and support journeys with their unhappy paths.
3. Record exact environment and actual pass/fail/blocked/not-run evidence, attaching artifacts, logs and manual observations. These classifications are test metadata, not runtime enum additions.
4. Missing selected-model deployment, signing, real identity/billing configuration or physical hardware becomes a named external blocker. Continue all independent implementation/fixture/unit tests; never relabel fixture output as a live pass.
5. Any mandatory failure, unsafe action, secret leakage, fake success or unresolved live gate prevents complete-release claim. Fix defects, rerun affected journeys and update coverage evidence.
6. Final deliverable lists working verified outcomes, actual blocked items and the next authority needed. No calendar-based scope cut or “scaffolding done” report substitutes for full acceptance.

**Focus/approval:** Every exercised flow retains F0–F7/A0–A5; test automation cannot bypass user-controlled credentials, payment, OS permission or signing authority. **Acceptance:** [PB-040](../quality/ACCEPTANCE.md).
