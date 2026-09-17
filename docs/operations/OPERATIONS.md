# Operations and durable runtime recovery

> **HISTORICAL REFERENCE — SUPERSEDED SCOPE.** The current decision is [local Azure onboarding](../product/LOCAL-AZURE-ONBOARDING.md), docs only until implementation is resumed. This earlier managed/full-product design is preserved as reference, not an instruction to implement its hosted services, login, billing, fixed models or full PB scope. Current requirements take precedence.

Status: **operating specification for a future implementation**. No service, job, monitor or on-call process is running because this file exists. [RELEASE.md](RELEASE.md) defines launch gates; [EXTERNAL-INPUTS.md](EXTERNAL-INPUTS.md) records required authorization. This is a state/recovery runbook, not a calendar roadmap or provisioning request.

## Boundaries and owners

| Boundary | Authority and durable state | Operational obligation |
| --- | --- | --- |
| Native app | Swift 6 actors, SwiftUI/AppKit; local GRDB SQLite under Application Support/HeyPebbi; Keychain secrets. | Local task journal, queue, Pebbi memory/history/workspaces, routine occurrence state, permission/device state and process lifecycle. No daemon after Quit. |
| Tool broker | Native immutable intent, approval, dispatch and result records; exact contracts in [TOOLS](../engineering/TOOLS.md). | Validate scope/target immediately before effect, preserve uncertainty and reconcile exact external target. Model output never grants permission. |
| Authenticated backend | Node 24/TypeScript strict/Fastify 5 on Azure Container Apps; PostgreSQL 17 account, devices, reservations/usage, webhooks and export/deletion jobs. | Authenticate/admit, proxy selected providers, authorize server-side metering, validate webhook signatures and maintain account isolation. It does not execute the user's local routines. |
| Provider | Only selected role/deployment after actual verification. | Report real availability/failures and usage; do not log content or silently substitute a model. |
| Distribution/web | Developer ID/notarized DMG, Sparkle 2 signed feed; HTTPS support/privacy/account/download pages and Blob release/export artifacts. | Deliver exact verified bytes, preserve compatible rollback, protect expiring account exports and publish truthful status. |
| Operations/security/privacy | Named roles assigned before launch. | Least-privilege access, incident accountability, retention/deletion, support redaction and release decisions. A role in a document is not an assigned operator. |

Runtime state/algorithms are canonical in [AGENT-RUNTIME](../engineering/AGENT-RUNTIME.md), storage in [DATA-MODEL](../engineering/DATA-MODEL.md), routes in [API](../engineering/API.md). Operators must not repair state by inventing new enum values or directly editing customer rows outside a reviewed recovery mechanism. [SECURITY](../engineering/SECURITY.md#data-location-and-retention) owns fixed retention ceilings and [BILLING](../engineering/BILLING.md) owns settlement/deletion accounting; operator choices must remain within those limits.

## Durable state rules

- Task states are exactly `queued`, `running`, `waitingForApproval`, `waitingForInput`, `waitingForConnection`, `cancelling`, `cancelled`, `succeeded`, `failed`, `interrupted`. Terminal `succeeded`, `failed`, `cancelled` attempts are immutable; retry creates a linked attempt. A conversation is not a task.
- Voice and dictation have separate canonical states and independent `audio_operations`/`audio_event_receipts`, outside the agent-task queue. Audio wire `taskId`/`attemptId` map to `audioOperationId`/`audioAttemptId` by immutable reservation role/owner kind; real result provenance stays in `sourceTaskId`/`sourceAttemptId`. Audio receipts never populate agent-task foreign keys. Barge-in flushes speech generation, not task execution. Stop listening, cancel dictation and cancel task are different user actions and must remain different audit events.
- Persist accepted ingress, user message, task mutation and event in one transaction. Store is the linearization point; actor scheduling alone cannot guarantee race safety. Journal events retain monotonic task-local `sequence` across attempts and opaque IDs.
- Persist immutable tool intent and dispatch reservation before crossing a side-effect boundary. Consume one-shot approval transactionally. Tool response acceptance is not proof of effect; preserve a separate verified result or unresolved uncertainty.
- A crash invalidates process-bound targets, capture handles, leases and stale approvals, but **not durable uncertainty barriers**. A second Pebbi cannot repeat an unknown send by obtaining a fresh lease.
- No task becomes succeeded while required work, unconsumed follow-ups, missing artifact verification or unresolved effects remain. Show completed independent outputs without falsely completing the whole request.
- One active agent-task attempt per Pebbi, bounded global reasoning and separate foreground-input/microphone leases follow AGENT-RUNTIME. Voice can coexist with reasoning; standalone dictation can coexist with a running/waiting task without using its serial slot. One device microphone lease requires explicit pause/replacement before dictation displaces voice capture; never cancel the task as part of that handoff. Waiting for approval/connection releases expensive global permits but does not silently reorder that Pebbi's queue.
- Suggested work is read-only until approved; scheduled work still respects fresh protected-action approvals. Persistent grants never cover payment, credentials, destructive bulk, publishing or outbound messages. Protected-effect allows originate only from deliberate accessible native approval controls with exact preview, never spoken yes, replayed transcript or model assertions. Voice selection of low-risk tasks/opening review is separate authority.

## Startup, sleep, Quit and crash recovery

**Startup procedure:** acquire the exclusive account-store/instance lock; validate/migrate safely; lock retained local account data against a different identity; mark formerly active/waiting/cancelling attempts interrupted; preserve queued work; invalidate ephemeral targets/grants; reconstruct projections and uncertainty barriers; reconcile read-only; show pending work and recovery choices. Do not start a mic, resurrect a browser tab scope or replay a write merely because a process restarted.

**Reconciliation order:** inspect immutable dispatch record and adapter class; query provider idempotency/result ID or exact target where supported; append authoritative result. Proven performed effects become part of future context and are not repeated. Proven absent effects may be proposed under fresh authorization. Unknown effects stay visibly blocked on that resource and require user/operator investigation. Elapsed time is not proof of absence. After classification, close interrupted attempt appropriately and create a new retry attempt; never interrupted → running as a shortcut.

**Sleep/lock:** stop capture/audio and foreground takeover, checkpoint active work and close authority/streams as required. Use monotonic clocks for deadlines and wall clocks only for schedule semantics. **Wake:** re-evaluate identity, TCC, device routes, connection/model health and target geometry; no covert mic resume; coalesce missed slots to one latest eligible occurrence per active routine. **Quit:** stop ingress/scheduling, cancel/checkpoint attempts, terminate/reap owned subprocess groups/native/MCP work, close transports/database and exit within bounded shutdown policy while preserving unresolved effects. No launch agent or server scheduler continues the routine.

**Dictation cancellation:** before insertion dispatch, zero target edits; after admission, stop new work and reconcile that one insertion. Store inserted/unchanged/unknown outcome in the insertion receipt without inventing a lifecycle state. No automatic undo across concurrent user edits, duplicate insertion or unverified unchanged/success claim. Preserve privacy-compliant text for review and durable minimal uncertainty metadata for unresolved effects.

**Audio recovery:** close/interrupt audio ownership, reconcile its reservation separately and discard volatile session handles/buffers. Never replay audio from the task queue or restart a mic on recovery. Unfinished staged drafts are cleaned on cancellation; private staged content/hash must not enter the durable recovery journal.

**Launch after Quit is not wake:** advance routine watermark and show next run; do not replay the closed-app backlog. A user may explicitly choose Run now. Physical evidence must distinguish this from the permitted single wake catch-up.

## Queues, deadlines and routine policy

Use canonical limits rather than independent operational overrides. AGENT-RUNTIME specifies two global active reasoning loops, one active attempt per Pebbi, at most four parallel read-only research requests per attempt and serial resource mutations. Queues/output/audio/frame/log buffers must each have a tested configured bound; missing bounds block launch. WebSocket text/control/context/transcript limits apply to reassembled serialized UTF-8 messages (256 KiB including envelope), with independent frame/cumulative reassembly bounds and tighter 32 KiB serialized/16 KiB decoded audio caps. Reject oversize explicitly; preserve available text for review, never truncate it into a false final. Delivered verified `tokenBudget` governs context assembly; missing or changed budgeting needs readiness failure/re-estimation, and context-limit errors trigger budget invalidation and explicit recovery without deleting instructions/evidence. Reject overflow before acknowledging acceptance; accepted work remains durably visible and cancellable.

Read-only or explicitly idempotent transport failures permit at most two retries after the first transmission, with canonical backoff/jitter and Retry-After handling. Validation/auth/permission/quota rejection is not transient. Generic native clicks, AX insertion, arbitrary code and MCP mutation do not acquire idempotency merely because an operator presses Retry. Resource barriers survive retry/new attempts.

Routines use persisted occurrence identity, schedule revision and watermark. Exactly one active occurrence per routine; overlap is skipped and recorded. Supported interval/daily/weekly/DST behavior follows AGENT-RUNTIME. Retryable occurrence failures permit the specified bounded retry window; three consecutive failed occurrences pause the routine, successful occurrence resets the count, and waiting/cancelled/skipped/coalesced events are not counted as failures. Missing permission/connection/unresolved approval sets blocked; timers never grant permission. Routine results are silent conversation/unread delivery, not a spoken completion flood.

## Observability without content collection

Required dimensions: app/backend/extension/config/schema version, capability/role, safe error code, operation category, state transition, duration, sequence gap/duplicate count, queue depth/wait, resource ownership category, reservation state and redacted correlation IDs. Exclude prompts, file/document bodies, full URLs/query strings, usernames/home paths, screenshots, raw audio, credentials and connector payloads. A correlation identifier is still restricted metadata, not public analytics.

Use separate optional product analytics and necessary security/usage logging with separate purposes/retention/access. Optional telemetry off means no optional transmission. Redaction is performed before logging/export; redactor failure drops unsafe fields or blocks the diagnostic upload, never sends raw data to help debugging. See [PRIVACY-AND-DATA.md](PRIVACY-AND-DATA.md).

| Signal | Operational interpretation and action |
| --- | --- |
| New protected dispatch after deny/expiry/cancel, transcript-authorized effect, wrong-account/device admission or sensitive telemetry canary | Immediate security incident; contain affected admission/tool route, preserve redacted evidence, withdraw affected distribution. Zero tolerated occurrences. An effect admitted before cancellation must instead be reconciled honestly, not falsely classified as a new dispatch. |
| Duplicate external effect or duplicate ledger settlement | Data-integrity incident; suspend automatic affected retries, reconcile exact target/ledger, investigate idempotency boundary. Do not auto-compensate with another write. |
| Stale/invalid voice deployment | Mark that capability unavailable; keep local/independently ready paths available. USER-DEFERRED deployments remain blocked rather than repeatedly paged as a new outage. |
| Unresolved effect/reservation backlog | Reconcile read-only by age/state under bounded workers; alert on exceeding the canonical settlement deadline, never release unknown consumption blindly. |
| Queue/buffer saturation | Backpressure new work, release waiting permits, investigate stalled adapter/consumer; preserve accepted tasks and responsive Stop. |
| Repeated crash/migration failure | Withdraw affected build from distribution, preserve store safely, use compatibility runbook; never reset a user's store as a hidden fix. |
| Provider error/latency or audio-route failure | Compare role/config revision and failure class; avoid logging raw requests. Use measured budgets from TESTING.md and explicit degraded state. |
| Idle CPU/memory/capture over budget | Investigate leaked engines, invisible animation, polling, processes or buffers; captures must be zero when unauthorized/idle. |
| Export/deletion/retention deadline at risk | Privacy incident queue and owner notification before deadline; do not mark deletion complete until observed. |

Production alert thresholds/windows/contact routes are approved operator configuration tied to tested budgets; no paging system or SLA is claimed here. Security/data-integrity invariants above are unconditional, not configurable warning thresholds. Use `/healthz` only for minimal process health; readiness for a role needs authenticated admission plus actual role-specific verification. A health 200 cannot mark voice ready.

## Incident runbooks

### Provider/authentication/network incident

1. Determine role and boundary: native permission/device, network, backend admission, Entra, quota or upstream deployment. Read sanitized error/correlation/config revisions; never request the user's secret.
2. Contain only affected paths; capability unavailable/connection expired is truthful. Keep local navigation, drafts and permitted exports usable. Do not claim typed cloud fallback if Astra is also unavailable.
3. Reconcile partial-stream usage and reservation state server-side. Close stale session authority; explicit retry creates new voice/dictation session/reservation and does not replay committed audio/tools.
4. Verify credential/deployment support through authorized non-secret metadata and a bounded approved test. Unknown/missing selected voice deployments remain USER-DEFERRED as registered; do not provision or switch models.
5. Exercise positive and negative boundary cases through the actual backend, update scoped evidence and communicate verified recovery. Reopening a socket alone is not recovery.

### Unknown or duplicate external effect

1. Freeze new mutations on the exact affected resource, not all independent tasks. Preserve task/attempt/intent/execution/result identity and existing uncertainty barrier.
2. Query exact external operation/target with authorized read access. Compare expected payload/version and provider receipt; do not guess from a conversation answer or a generic success banner.
3. Append reconciliation evidence. If duplicate is confirmed, disclose it; reversal/deletion/refund is a new consequential action requiring appropriate fresh authorization, not an automatic “fix.”
4. Reconcile billing separately from external effects. A cancelled task can still have consumed real provider work; no automatic false credit/charge claim.
5. Add a boundary regression test and invalidate affected release gates before resuming automatic safe operations.

### Local store corruption, disk full or lost files

Stop dispatch when durable intent cannot commit. Preserve readable data and existing artifact versions, report the storage boundary and offer user-selected export/backup recovery. Do not silently delete the database, overwrite original files or regenerate missing evidence. Validate backup schema/ownership/digest, replay journal where safe, restore deletion tombstones and reconcile external effects before resuming. If recovery cannot preserve integrity, keep local read-only/recovery presentation with an honest support path. Disk-space cleanup never deletes arbitrary personal files.

### Billing/webhook/usage incident

Disable new affected paid admission if entitlements cannot be trusted. Keep signed webhook inbox and stable event identity, reject forged signatures and reconcile account state against Stripe through authorized reads. Trusted server accounting alone finalizes reservations; client counts cannot authorize/bill work. Replayed/out-of-order events must not duplicate ledger settlement or revert a newer entitlement blindly. Missing/unapproved operator pricing keeps Checkout disabled; do not fill production plans with fixture allowances. Follow deletion/cancellation obligations and approved refund policy without inventing prices or issuing unapproved refunds.

### Native device/browser/permission incident

Inspect actual TCC, route, focus/geometry and browser/native-host session state. Stop affected streams/control first. Restore via user-visible OS/browser setup, not TCC database edits, security bypass, port exposure or repeated blind clicks. Chrome and Brave are separately verified. An extension logo or heartbeat does not prove DOM/action scope. Invalidated targets require explicit re-selection and fresh effect authorization where applicable.

### Privacy/security incident

Stop unsafe collection/admission/logging and withdraw affected releases if needed. Preserve minimal access-controlled evidence, revoke compromised authority through an authorized operator and trace access/exports without distributing sensitive payloads. Notify designated security/privacy owners and determine affected accounts/data/processors and legal duties. Public/customer notices require factual scope and approved process; do not fabricate breach absence or compliance. Follow SUPPORT.md for identity-safe contact. Document containment, remediation, regression coverage and verified deletion/recovery before closure.

## Backup, restore and data lifecycle operations

Local backups are app/user-authorized snapshots for migration/recovery, not secret cross-device sync. Server PostgreSQL backup/point-in-time restore and Blob lifecycle need approved actual Azure configuration and tested restore evidence. Verify restored identity/account boundaries, ledger uniqueness, webhook inbox, export/deletion jobs, tombstones and schema compatibility in an isolated environment before live use. Production backup existence is not assumed from an Azure product choice.

[API](../engineering/API.md) defines account deletion admission and deadlines; [PRIVACY-AND-DATA](PRIVACY-AND-DATA.md) defines handling. Workers use durable idempotent job records and bounded leases. Preserve minimal deletion tombstones long enough to reapply deletion after backup restoration; restore never makes deleted data available pending the sweep. Logs/exports/backups have explicit configured lifecycle, not an unbounded default. Operators may not download customer account exports for debugging without authorized purpose/consent.

Recovery-time/recovery-point objectives, operational alert routes and commercial support response promises require operator approval and measured exercises before publication. They are not invented guarantees. Required invariant now: zero acknowledged loss from normal committed local/server transactions within the supported storage failure model, honest disclosure for disaster/backup gaps, and no release without a demonstrated compatible restore/rollback path.

## Operational change control and closure

Treat model routing, limits, entitlements, retention, auth redirect/issuer, native-host origins and signing/feed settings as versioned reviewed configuration. Validate shape/range/relationships and reject invalid configurations at startup; missing feature inputs disable that feature explicitly. Record change authority, before/after version and affected gates. Never put secrets into a diff or change protected policy to avoid a build interruption.

An incident closes only when exact-target/state readback, user impact, root cause, regression tests, remediation/corrective artifact and updated release gates are recorded. A transport retry that stopped failing is not by itself proof of resolved data integrity. Every report separates local tests, live tests, hardware observations and remaining blockers.
