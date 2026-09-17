# Agent runtime, queues and recovery

**Proposed runtime specification; no implementation or passing integration tests are claimed.** Covers PB-007, PB-010, PB-013–PB-017, PB-020–PB-028, PB-030–PB-031, PB-034–PB-035, PB-037–PB-040. Native Swift actors implement this runtime without Hermes or a paid agent CLI. [CONTRACT](../CONTRACT.md) owns state names, [TOOLS](TOOLS.md) owns tool calls, [DATA-MODEL](DATA-MODEL.md) owns atomic persistence and [API](API.md) owns backend transport.

## 1. Independent units and state

- **Pebbi:** persistent identity, appearance, job, memories, workspace and queue. Editing a job or memory changes future context snapshots; it cannot rewrite a dispatched intent.
- **Conversation:** ordered user/assistant messages, attachments and pins. It can contain many tasks or no task. Closing/archiving it does not cancel execution.
- **Logical task (`taskId`):** user intent and follow-ups, stable across retries. Journal sequence is monotonic across all its attempts.
- **Attempt (`attemptId`):** one execution run. Retry creates another attempt with `previousAttemptId`; it never resets an old terminal attempt.
- **Tool intent (`toolCallId`):** immutable, validated description of one proposed action at an exact attempt/steering generation. A provider tool-call token is a separate opaque `providerCallRef`, not a local UUID.
- **Execution (`executionId`):** one authorized dispatch of that intent. A retry transmission for a provider supporting idempotency is linked to this same execution. A new effect requires a new intent, preview and idempotency key.
- **Result (`resultId`):** immutable observation. A later reconciliation appends another result referring to the execution and earlier result; it does not rewrite the first observation.

Task-state transitions are normative; event names in this document are journal event types, not additional task states.

| Current state | Allowed next states | Guard |
|---|---|---|
| `queued` | `running`, `cancelled` | Durable queue claim, or cancellation before dispatch |
| `running` | `waitingForApproval`, `waitingForInput`, `waitingForConnection`, `cancelling`, `succeeded`, `failed`, `interrupted` | Journal boundary committed; completion barrier satisfied for success |
| `waitingForApproval` | `running`, `waitingForInput`, `cancelling`, `failed`, `interrupted` | Exact approval plus fresh revalidation, denial/revise, cancel, fatal policy or app interruption |
| `waitingForInput` | `running`, `cancelling`, `failed`, `interrupted` | New user input/checkpoint, cancel or interruption |
| `waitingForConnection` | `running`, `cancelling`, `failed`, `interrupted` | Explicit reconnect/capability recovery, bounded retry exhausted, cancel or interruption |
| `cancelling` | `cancelled`, `interrupted` | No new dispatch; in-flight effects settled or durably recorded unknown; crash may interrupt |
| `interrupted` | `failed`, `cancelled` | Reconcile/classify all dispatches first; retry is a new attempt |
| `succeeded`, `failed`, `cancelled` | none | Terminal attempt is immutable |

Queued attempts survive app exit without pretending to be running. Launch presents pending user tasks; those requiring fresh capture, browser scope, takeover or approval cannot auto-dispatch. Explicit cancellation of a queued attempt is a single queued→cancelled transaction.

Voice states and dictation states are the separate canonical enums. A chat draft, playback generation, queue position, approval expiry or tool verification outcome is not a new task state.

## 2. Proposed runtime interfaces

The following are interface pseudocode, not implemented Swift declarations. All IDs are opaque UUID strings on the local JSON boundary; Swift wraps them in typed `Sendable` value types. Return values are committed facts, not optimistic UI claims.

```text
TaskCoordinator.submit(command: SubmitTask, ingressId) async -> TaskReceipt
TaskCoordinator.followUp(command: FollowUp, ingressId) async -> FollowUpReceipt
TaskCoordinator.cancel(taskId, attemptId, expectedRevision) async -> CancelReceipt
TaskCoordinator.retry(taskId, failedAttemptId, ingressId) async -> TaskReceipt
PebbiExecutor.runNext(pebbiId) async
Store.acceptIngress(command) async -> CommittedIngress
Store.commitAttemptMutation(expectedVersion, events, projectionChanges) async -> CommitResult
ToolBroker.prepare(proposal, contextVersion) async -> IntentReceipt
ToolBroker.execute(toolCallId, expectedVersion) async -> ToolResult
ToolBroker.reconcile(executionId) async -> ToolResult
VoiceController.stopSpeech(voiceSessionId) async -> PlaybackStopped
RoutineScheduler.evaluate(now, reason: timer | wake | launch) async -> ScheduleSummary
```

`SubmitTask` contains `schemaVersion`, `pebbiId`, `conversationId`, user `messageId`, text/attachment references and origin (`user`, `acceptedSuggestion`, `routineOccurrence`). The trusted caller, not the model, supplies origin. Backend/provider input cannot construct `user` authorization.

`ContextVersion` is `{accountEpoch, attemptId, attemptRevision, steeringRevision, cancelEpoch, memoryRevision}`. An awaited operation returns with the version it started from. Consumers compare only relevant dimensions explicitly: any account/cancel mismatch drops live presentation and prevents further dispatch; steering mismatch discards an obsolete plan; memory revision mismatch invalidates retrieval before the next request. Old tool results remain audit evidence even when they cannot advance the current plan.

## 3. Durable ingress and race-free follow-ups

Store is the linearization point, not actor call order. Ingress commands carry a caller-generated UUID `ingressId`; uniqueness in SQLite makes network/UI retry return the original receipt. Persist the user message, inbox record, task mutation and events in **one** transaction.

A follow-up explicitly addresses `taskId` and the UI's observed `attemptId`. It is not silently routed to whichever task is selected later. The receipt includes `{acceptedMessageId, disposition, taskId, attemptId, acceptedSequence, steeringRevision}`; `disposition` is `attached`, `queuedSuccessor` or `staleAttempt`. A stale attempt with a newer retry already active returns `staleAttempt` and asks which active task to steer; preserve the draft rather than guess.

### Atomic algorithm (pseudocode)

```text
BEGIN write transaction
  if ingressId already exists: return its stored receipt
  validate local account/Pebbi/conversation ownership
  load addressed attempt and active attempt pointer
  if addressed attempt is terminal, cancelling or interrupted and no different retry is active:
    insert user message
    create successor logical task linked by parentTaskId, queued at queue tail
    persist queuedSuccessor receipt and events
  else if addressed attempt is not the current active/queued attempt:
    persist staleAttempt receipt; do not move the message into another task
  else:
    insert user message and pending inbox item
    increment steeringRevision and attemptRevision
    append followUpAccepted event with messageId
    invalidate unconsumed approvals for older steeringRevision
    persist attached receipt
COMMIT
```

While `cancelling` or `interrupted`, do not reopen that attempt. An accepted follow-up creates a queued successor task with a recovery dependency; its affected resources remain blocked until prior uncertain effects are resolved. This is the same explicit successor behavior as a terminal attempt, not a state transition back to running.

Executor safe-point algorithm:

1. Before every model request, tool preparation, dispatch reservation and completion, reload pending inbox/revision.
2. Consume an ordered batch of pending follow-ups into a new immutable context snapshot and commit `followUpsConsumed` with message IDs. Marking consumed means included in that context, not “the request was obeyed.”
3. Cancel/discard old model generation when steering changes. Invalidate not-yet-dispatched intent approval and replan. Never mutate an old intent's arguments.
4. An in-flight tool cannot be unwritten by a follow-up. Cancel if safely cancellable, otherwise settle/reconcile its effect first, then reason over the new user message and actual result. Display “Update received; finishing/checking the current action” rather than implying instantaneous rerouting.
5. Completion transaction checks expected `steeringRevision`, no pending inbox, no unresolved dispatch, current attempt state and cancel epoch. If any guard fails, no `succeeded` event is appended; resume the loop.

Therefore a follow-up racing completion is deterministically either included before completion or committed as a visible successor. It is never accepted and lost between reading a Boolean and setting “done.” A delayed callback must not append a final answer to a newer attempt merely because `taskId` matches.

## 4. Per-Pebbi queues and shared-resource arbitration

Queue position is a monotonically allocated integer within a Pebbi. Do not use wall-clock timestamps for FIFO. One attempt per Pebbi may occupy the serial execution slot, including waiting states. `queued` tasks behind it do not overtake approval/input blockers. UI may cancel or explicitly move queued work; reordering is a versioned DB transaction and never preempts an already running effect.

One `PebbiExecutor` actor supervises a Pebbi. Store's partial uniqueness constraint independently prevents duplicate claims if two workers start accidentally. Registry operations in `TaskCoordinator` are actor-isolated, but uniqueness in storage is the final safety check.

Global `ResourceArbiter` defaults:

| Lease | Capacity / use |
|---|---|
| `reasoning` | Two active task model/tool loops; released during user/connection wait |
| `microphone` | One owner: voice or dictation |
| `foregroundInput` | One takeover/insertion sequence across the entire app |
| `appMutation:<processIdentity>` | One mutator per AX app process |
| `browserMutation:<browserSessionId>:<tabId>` | One mutator per authorized tab |
| `workspaceMutation:<workspaceId>` | One workspace mutation/controlled code run; narrower file locks may follow only with evidence they are needed |
| `connectionMutation:<connectionId>:<resourceScope>` | One non-idempotent connector mutation for that resource |

Resource key components are internal canonical values, not provider-chosen lock names. Acquire the entire sorted resource set atomically; no nested wait while holding half the set. Fair FIFO waiters and cancellation-safe release prevent starvation. Never hold these leases while showing approval UI or waiting for a missing connection. After approval, acquire and revalidate again; a displayed preview is not a resource lock.

Read-only research inside an attempt uses a bounded task group of at most four requests. Parallel read results retain their own evidence IDs; deterministic sorting in the result does not falsely imply chronological execution. No parallel browser/desktop mutations even if the model emits many proposals at once. Record and execute ordered effects one at a time through the broker.

Uncertain prior effects create durable resource barriers, distinct from process-local leases. Crash drops leases; it must not drop barriers. Another Pebbi cannot repeat an uncertain send merely by getting a new lease.

## 5. Intent → approval → dispatch → result

1. **Prepare:** Validate model proposal against the local registry and current target/resource generation. Normalize permitted data to a canonical payload, create `toolCallId`, hash the full immutable intent and commit `toolIntentPrepared`. No external write yet.
2. **Policy:** Compute risk and required scopes locally. Sensitive actions always require fresh exact previews. Persistent grant matching is bounded to user, connector/app, tool class, resource, expiry and current policy version. Routine authorization is not permission for future outbound messages/payments/publishing.
3. **Approval:** Commit request before showing UI. Decision is a CAS against pending request, intent digest, steering/cancel/account generations and expiry. Duplicate Allow returns the same receipt; late Allow cannot resurrect a cancelled task. Denial produces a result and input/replan path, not an infinite repeat-prompt loop.
4. **Dispatch reservation:** In one transaction verify all guards again, consume one-shot approval, insert immutable execution dispatch record and append `toolDispatchReserved`. Commit durably before crossing the process/network boundary.
5. **Execute once:** Adapter receives exact intent + authority handle + lease. It cannot read a new arbitrary prompt or change tool arguments. A crash after reservation but before actual call is still potentially uncertain for non-idempotent adapters unless transport proves not sent.
6. **Observe:** Append immutable tool result. `succeeded` transport is not equivalent to verified effect; effect evidence includes read-back of the exact target/version or a truthful unresolved state.
7. **Reconcile:** Query exact external request ID/target/expected value where possible; append a new result with evidence. Never edit the original result or invent provider support for idempotency.
8. **Continue:** Give only sanitized bounded results to the model; local sensitive payloads/grants/secrets never enter model context. UI completion is based on verified effects and journaled artifacts, not the model saying “done.”

Idempotency is per operation, not per prompt. `idempotencyKey` is a UUID generated locally and retained across supported replay transmissions. Native UI clicks, AX inserts, generic MCP calls and arbitrary scripts have **no guaranteed external idempotency**. See [TOOLS](TOOLS.md) for adapter classes and [DATA-MODEL](DATA-MODEL.md) for immutable records.

## 6. Cancellation, speech-stop and interruption

| User action | Effect | Does not do |
|---|---|---|
| Stop speaking / barge-in | Increment playback generation, flush audio, cancel remote speech response where supported | Does not cancel queued or running tasks |
| Stop listening | Close microphone capture lease and stream; preserve typed/chat context | Does not undo dictation already inserted or a completed external action |
| Cancel dictation | Stop that dictation session; discard uninserted draft according to user flow | Does not cancel a task in the conversation |
| Cancel task | Commit `cancelling` and cancel epoch; block new dispatch; cancel model/children; settle or record unknown effects; terminal `cancelled` | Does not promise undo or erase evidence |
| Cancel queued task | Atomically queued→cancelled | Does not affect the Pebbi's current attempt |
| Quit / sleep / crash | Stop local interactive resources; persist interruption/uncertainty and recover later | Does not make a completed remote operation disappear |

Task Cancel has a transaction-linearized response: after it commits, no later dispatch reservation can pass the old cancel epoch. A dispatch already reserved may have crossed the boundary; cancellation must show its outcome separately. Completion racing Cancel uses CAS; only one wins. If completion already committed, Cancel returns `alreadyTerminal`, not a fabricated cancellation.

Graceful Cancel waits at most five seconds for cooperative adapters, then terminates owned cancellable processes and records unknown external effects. UI can say “Cancelled; one external action needs verification.” Keep a resource barrier until resolved. Successful cancellation means no further Pebbi dispatch, not proof that the remote system stopped. Approval windows for that attempt close/invalidate immediately.

## 7. Crash recovery and retries

Startup under an exclusive instance/account store lock:

1. Migrate/validate DB; do not launch tasks if storage is unsafe.
2. Atomically mark old `running`, waiting and `cancelling` attempts `interrupted`, append recovery events and invalidate all process-bound refs, leases, one-shot unconsumed approvals and capture handles. Preserve queued work.
3. List dispatches without a conclusive effect result. Reconcile in read-only mode by adapter capability. No side-effect replay while reconciliation is pending.
4. If committed effect found, append confirmed evidence and include it in retry context. If absence is authoritatively proven, permit a new action only under appropriate fresh authorization. If ambiguous, keep a barrier and ask the user; elapsed time is not proof of absence.
5. Close interrupted attempts as `failed` with an interruption reason or `cancelled` per explicit cancellation, after classification. Retry creates a new attempt; linked confirmed effects are not repeated. A new attempt may proceed on unrelated work but cannot bypass an unresolved resource barrier.

Automatic transport retries: read-only requests and explicitly idempotent provider requests only, at most two retries after the first transmission, backoff one then three seconds with bounded ±20% jitter. MCP read calls use the stricter CONNECTIONS.md limit of one retry. Inference is not a free read: API.md forbids replay of a dispatched Responses generation; never resend an uncertain model request/reservation or invent an event replay. Respect `Retry-After` up to 60 seconds; longer waits become `waitingForConnection` with a visible next step rather than tying up permits. Validation, permission, auth, policy and quota rejection are not transient retries. Ambiguous writes, native actions, generic MCP mutation and code execution are never blindly auto-retried. User “Retry” does not override this rule.

Do not log request secrets while diagnosing. A bug investigation must reproduce a specific failing boundary (journal CAS, transport frame, adapter result), rank falsifiable causes and leave a regression test; random permission toggles or fallback click loops are not fixes.

## 8. Memory, retrieval and context compaction

Each context snapshot identifies the Pebbi, conversation, accepted messages, memory revision, file versions, source passages, capabilities and approved scope descriptions. Grant credentials and authority handles are never context material. Treat memory/document/browser/connector text as data with provenance, not runtime instructions.

Memory design deliberately starts with local SQLite FTS5, not another vector service or cloud copy. Retrieval order:

1. User-pinned instructions/preferences for the current Pebbi, with explicit ownership and sensitivity controls.
2. Current task and unconsumed follow-ups, recent conversational turns, exact relevant tool results.
3. Scoped FTS5 query over that Pebbi's nondeleted memories and authorized document passages; include at most eight memory items and twelve evidence passages, rank by FTS score then recency and stable ID for ties.
4. Sibling-Pebbi memories only if the user explicitly shared the item into a shared scope; no automatic cross-Pebbi or cross-account recall.

Budgets derive from the actually available model context limit reported/configured through the backend. Reserve at least 25% for output/tool results and safety overhead; begin compaction when projected input exceeds 70% of the usable input budget. Do not assert a hardcoded model token capacity. If an exact tokenizer is unavailable, use a conservative estimator and a bounded shrink-and-retry on context-length error; never drop new user instructions or pending approvals to fit.

Compaction creates a versioned structured summary containing source message ranges, facts with citations, unresolved questions, user preferences, artifact refs and pending work. It is not a free-text replacement for the task journal. Preserve recent turns, pending follow-ups, approval/dispatch/results and high-priority constraints verbatim outside the summary. Validate every referenced message/file ID and coverage interval; reject hallucinated references. Keep originals searchable locally subject to user retention; no silent deletion during compaction.

Memory suggestions derived by the model are proposals. User can inspect, edit, reject and forget them. Forget increments the memory revision, deletes the item/FTS entries, invalidates summaries/cache containing it and prevents it from being sent in the next request; if an old request is already in flight, cancel/discard its future plan rather than pretending the provider can unsee data. Deleting source conversations/documents also invalidates derived entries. State that provider retention is separately governed by backend/security policy.

### Private session execution

PB-031 private mode is a trusted retention choice carried outside model proposals. Use the in-memory context/journal plus minimal durable effect journal specified in DATA-MODEL.md. Do not create durable chat/memory/artifact bodies or learn from private context. Exact tool intents remain immutable in memory; the minimum digest/locator dispatch record remains durable before a write. If recovery cannot be performed without retaining sensitive content, explain and require an explicit retention choice before dispatch. Quit discards private dialogue while preserving only unresolved-effect safety metadata. Private mode does not disable billing, approvals, cancellation or idempotency.

## 9. Routines and suggestions

Routines are entirely local, app-open work. No LaunchAgent, server scheduler or push service secretly executes them while Quit. UI shows this limitation when enabling a routine. Supported schedule specifications are fixed interval (minimum five minutes), daily at local time, or weekly at local time and weekdays, with an explicit IANA time zone. Zone changes require recomputing future slots, not replaying old ones. DST gap runs at the next valid local time; a repeated wall time runs once at its first occurrence.

`RoutineScheduler` uses an injected wall clock for schedule semantics and a monotonic clock for timeouts. Persist `scheduleRevision`, last evaluated watermark and unique occurrence key before enqueueing. Exactly one occurrence may be active per routine. User editing the schedule increments revision; already running work retains the old snapshot and the next slot uses the new one.

- While open, each due slot creates one normal task with routine provenance and the authorized read/resource scope. It still passes all broker checks.
- On wake, coalesce all missed slots to **one latest due occurrence per routine**. Record older missed slots as coalesced metadata, not failed task attempts. Global queues naturally bound simultaneous routines; do not flood the model.
- On launch after Quit, do not run the closed-app backlog. Advance the schedule watermark and show the next run. A user can choose Run now for missed work.
- If a routine is still running, offline or blocked when slots arrive, retain only the latest missed slot as a pending catch-up and coalesce older slots. After the active occurrence finishes or the user resolves the dependency, enqueue at most one catch-up, through the same unique occurrence transaction; never create concurrent duplicates. Coalescing is not a routine failure.
- A retryable transient occurrence failure permits at most two additional attempts, after one minute and five minutes, within a 15-minute occurrence retry window. This sits above bounded transport retries and uses a persisted count. No retry can duplicate an uncertain mutation.
- Three consecutive **failed occurrences**, after exhausting permitted retries, set routine state `paused` atomically and notify with the last error. Success resets the count to zero. User cancellation and skipped/coalesced occurrences neither increment nor reset it.
- Missing permission/connection or unresolved approval makes the routine `blocked` with the actual task waiting state. It cannot accumulate more runs. Reauthorize/resolve explicitly; a scheduler timer cannot grant permission. Approval-dependent publishing/outbound work always waits for fresh approval.
- `paused` is user or failure-policy pause; `archived` prevents future scheduling. No hidden synonym states.

Suggestions operate only on user-enabled, read-only scopes. Persist why a suggestion exists, supporting source refs, freshness and expiry. Accept creates a new task via ingress; dismiss/archive has no effect on external systems. Duplicate acceptance returns the same task receipt. Suppress notification interruptions under configured quiet/call controls; always retain truthful unread state. Do not claim universal call detection across third-party apps: use explicit quiet mode and available observed signals, with Unknown treated conservatively.

## 10. Result delivery and completion

A task succeeds only when required effects are verified, required artifacts exist as committed immutable versions, evidence links are recorded and no inbox/dispatch barrier remains. A research answer distinguishes sourced facts from inference and identifies incomplete retrieval. A file task returns the actual artifact ID/version and native reveal/preview actions, not a fabricated path. A task blocked by unavailable live APIs reports the blocker and may deliver completed independent artifacts; it must not mark the whole task succeeded if acceptance requires the missing operation.

Persist the final message and task terminal event in one transaction. Unread delivery is separate: mark read only when the relevant conversation/result is actually presented as read according to product flow, not when a notification API accepts a request. Focus/call suppression delays interruption, not durable result creation.

## 11. Required deterministic tests

These are proposed test cases, not results. Use injected clocks, fake transports explicitly confined to tests, SQLite temp databases and deterministic suspension gates.

| ID | Interleaving/failure | Assertion |
|---|---|---|
| RUN-01 | Same `ingressId` submitted concurrently | One message/task and same receipt |
| RUN-02 | Follow-up commits immediately before/after completion | Included or successor receipt, never lost; no old final answer on successor |
| RUN-03 | Follow-up after preview, before dispatch | Old approval invalid; new immutable intent required |
| RUN-04 | Follow-up/cancel while AX/send is in flight | Actual old effect retained; no repeat; correct cancellation/steering behavior |
| RUN-05 | Cancel races dispatch reservation/completion | CAS determines one linearized outcome; no dispatch after committed cancel |
| RUN-06 | Two executors claim same Pebbi; two Pebbis mutate same target | DB uniqueness + arbiter enforce serialization |
| RUN-07 | Waiting approval in Pebbi A, runnable research in B | A holds queue slot but not global reasoning/input permit |
| RUN-08 | Kill process at each intent/approval/reservation/result boundary | Recovery marks interrupted; unknown writes reconciled, not replayed |
| RUN-09 | Late provider audio/text after stop/account switch/retry | Old generation ignored; speech-stop leaves unrelated task running |
| RUN-10 | Memory forget during retrieval/compaction | Derived cache invalidated; forgotten content excluded from next request |
| RUN-11 | Sleep over many slots, repeated wake callbacks, DST fold/gap | One catch-up per routine; no duplicate occurrence; defined wall-time behavior |
| RUN-12 | Transient routine failures vs blocked/cancelled/skipped slots | Bounded retries; exactly third failed occurrence pauses; success resets |
| RUN-13 | Disk full before dispatch reservation | No side effect; error preserves last durable state |
| RUN-14 | Model requests unknown tool or says done with unverified artifact | Reject proposal; no false success |
| RUN-15 | User denies mutation then model proposes it again unchanged | No nag loop or alternate-path bypass; ask for new user intent |

Property tests generate legal transition sequences and assert terminal immutability, monotonic task-local sequence, at most one active attempt per Pebbi and no terminal success with pending inbox. Replay tests rebuild task projections from the journal and compare to live rows. Live OS/provider/device tests remain separate release gates; passing fakes is necessary but never sufficient.
