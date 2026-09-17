# Local data model, journal and migrations

**Proposed schema specification; not a database implementation.** Owns native storage for PB-002, PB-009–PB-017, PB-021–PB-026, PB-030–PB-031, PB-035, PB-037. PostgreSQL account/billing/service tables remain in backend-owned documents; do not mirror a server billing ledger into an authoritative local table.

## 1. Storage roots and types

Use Foundation application-support URLs, never a developer's absolute home path. The proposed on-disk tree is:

```text
Application Support/HeyPebbi/
  install.json                         # installationId + nonsensitive preferences
  Accounts/<accountId>/
    pebbi.sqlite
    pebbi.sqlite-wal
    pebbi.sqlite-shm
    Blobs/<sha256-prefix>/<sha256>       # immutable content within this account
    Workspaces/<workspaceId>/            # managed Pebbi workspace roots
    Staging/<operationId>/               # recoverable internal staging
    Execution/<executionId>/             # temporary trusted-code inputs/outputs
    Exports/<exportId>/                  # explicit user-requested local exports
  Runtime/                              # ephemeral socket/lock; never durable credentials
Caches/HeyPebbi/                         # rebuildable, nonsensitive cache only
```

`accountId`, installation/device IDs and every entity ID are UUID strings. Blob digests are SHA-256 hex **content hashes**, not UUID identifiers. A blob is referenced by an `artifactId`; never accept a hash/path from a model as authority to read it. No deduplication across accounts. Filesystem directories are user-only (0700), files 0600 subject to native APIs; validate ownership and reject unexpectedly permissive runtime sockets. User-selected external workspace roots are referenced by bookmark, not silently copied into install metadata.

Database: SQLite through GRDB `DatabasePool`, WAL, foreign keys ON on every connection, bounded busy timeout 5000 ms, `synchronous=FULL` for durable dispatch transactions. Use SQLite backup API/GRDB backup for consistent backups, not a live copy of only the main file while WAL is active. No claim of SQLCipher/database encryption; device FileVault and filesystem access protection are separate concerns.

Logical type notation below: `Id`/`Text` → SQLite TEXT, `Int`/`Bool` → INTEGER (Bool CHECK 0/1), `Time` → UTC RFC 3339 TEXT with fixed formatter and millisecond precision, `Json` → validated canonical UTF-8 TEXT with `json_valid` check where JSON1 is supported by the pinned SQLite, `Bytes` → BLOB. IDs require strict format validation before binding. Use bound parameters. Revisions/sequences are nonnegative integers constrained within JSON's exact integer range. `?` means nullable; all other fields NOT NULL. Every primary key/foreign key and uniqueness constraint is explicit below. Mutable entities include `createdAt`, `updatedAt`, `revision` unless the row lists alternative version fields. Immutable entities carry `createdAt`/`occurredAt` only and reject UPDATE/DELETE through normal app connections.

## 2. Relational dictionary

This is the proposed **final schema**, not an instruction to scaffold empty tables. Table/column names use camelCase so persistence mappings do not introduce another vocabulary.

### Identity, Pebbis and content

| Table | Fields / keys | Constraints and purpose |
|---|---|---|
| `accountMetadata` | `accountId Id PK`, `deviceId Id?`, `accountEpoch Int`, `lastVerifiedAt Time?`, `displayName Text`, `createdAt`, `updatedAt`, `revision` | Exactly one row per account database. No access/refresh tokens, email-based ownership or tenant ID. Account epoch increments on sign-out/security reset. |
| `settings` | `settingKey Text PK`, `valueJson Json`, `updatedAt Time`, `revision Int` | Typed allowlisted settings only; no arbitrary secret/config dump. Contains local quiet mode, device selection refs, shortcut bindings and retention selections. |
| `workspaces` | `workspaceId Id PK`, `label Text`, `kind Text`, `bookmarkRef Id?`, `managedRelativePath Text?`, `accessRevision Int`, mutable timestamps/revision | Kind `managed` or `selected`; exactly one path strategy. An unavailable/stale bookmark is a blocked resource, not a new default directory. |
| `pebbis` | `pebbiId Id PK`, `workspaceId Id FK`, `name Text`, `job Text`, `appearanceJson Json`, `profileRevision Int`, `memoryRevision Int`, `nextQueuePosition Int`, `displayOrder Int`, `pinned Bool`, `archivedAt Time?`, mutable timestamps/revision | Names not unique. Default named Pebbi. Archive pauses routines via transaction; does not delete identity/history. |
| `conversations` | `conversationId Id PK`, `pebbiId Id FK`, `title Text`, `nextMessageSequence Int`, `readThroughSequence Int`, `manualUnread Bool`, `pinned Bool`, `archivedAt Time?`, mutable timestamps/revision | Read cursor ≤ committed maximum message sequence; manualUnread survives opening until the explicit read rule clears it. |
| `messages` | `messageId Id PK`, `conversationId Id FK`, `messageSequence Int`, `taskId Id? FK`, `attemptId Id? FK`, `role Text`, `text Text`, `deliveryKind Text`, `createdAt Time`, `editedFromMessageId Id? FK` | UNIQUE(conversationId,messageSequence). Immutable committed message; edit is a new row with lineage. Role user/assistant/tool/systemNotice; systemNotice is UI history, not a model system prompt. Partial/final represented by separate deliveryKind, not overwritten evidence. |
| `drafts` | `draftId Id PK`, `conversationId Id FK`, `composerKind Text`, `text Text`, `attachmentSelectionJson Json`, `focusRecoveryJson Json?`, `updatedAt Time`, `revision Int` | UNIQUE(conversationId,composerKind). Dictation recovery stores text and nonsensitive target description, never a reusable AX pointer/authority token. |
| `artifacts` | `artifactId Id PK`, `sha256 Text`, `byteCount Int`, `mimeType Text`, `blobRelativePath Text`, `sourceKind Text`, `createdAt Time` | Immutable. UNIQUE(sha256,byteCount) within account. Blob path is internal and validated; no secret/raw capture auto-storage. Same bytes can be referenced from many file versions. |
| `files` | `fileId Id PK`, `workspaceId Id FK`, `relativePath Text`, `displayName Text`, `currentVersionId Id? FK`, `trashedAt Time?`, mutable timestamps/revision | UNIQUE(workspaceId,relativePath) for nontrashed rows, normalized per actual filesystem path semantics without rewriting opaque IDs. Version pointer changes only after verified file commit. |
| `fileVersions` | `fileVersionId Id PK`, `fileId Id FK`, `versionNumber Int`, `artifactId Id FK`, `previousVersionId Id? FK`, `sourceIdentityJson Json`, `createdAt Time` | Immutable; UNIQUE(fileId,versionNumber). Source identity includes file resource identifier, byte count, mtime and verified hash; metadata alone is not content identity. |
| `messageAttachments` | `attachmentId Id PK`, `messageId Id FK`, `artifactId Id FK`, `fileVersionId Id? FK`, `displayName Text`, `position Int`, `createdAt Time` | Immutable; UNIQUE(messageId,position). Exact artifact version remains stable when external source file changes. |

### Tasks, ingress and durable execution

| Table | Fields / keys | Constraints and purpose |
|---|---|---|
| `tasks` | `taskId Id PK`, `pebbiId Id FK`, `conversationId Id FK`, `parentTaskId Id? FK`, `origin Text`, `originRef Id?`, `activeAttemptId Id? FK`, `nextEventSequence Int`, `title Text`, mutable timestamps/revision | Logical task; origin user/acceptedSuggestion/routineOccurrence set by trusted coordinator. Parent links successors, not retries. |
| `taskAttempts` | `attemptId Id PK`, `taskId Id FK`, `pebbiId Id FK`, `previousAttemptId Id? FK`, `attemptNumber Int`, `queuePosition Int`, `state Text`, `steeringRevision Int`, `cancelEpoch Int`, `attemptRevision Int`, `claimedBySessionId Id?`, `startedAt Time?`, `finishedAt Time?`, `failureCode Text?`, `createdAt Time` | UNIQUE(taskId,attemptNumber), UNIQUE(pebbiId,queuePosition). State CHECK is exactly CONTRACT list. Composite task/Pebbi ownership validated by FK or trigger. See active-slot index below. |
| `taskEvents` | `eventId Id PK`, `taskId Id FK`, `attemptId Id FK`, `sequence Int`, `type Text`, `occurredAt Time`, `schemaVersion Int`, `payloadJson Json` | Immutable append-only; UNIQUE(taskId,sequence). Local journal ordering authority. Event payloads contain refs/redacted operational facts, not secrets/raw frames. |
| `ingressCommands` | `ingressId Id PK`, `commandKind Text`, `commandDigest Text`, `receiptJson Json`, `createdAt Time` | Immutable dedupe receipt. Same ID/different digest is conflict, not reinterpretation. User message and receipt committed atomically. Stale receipt leaves the draft intact. |
| `taskInbox` | `inboxId Id PK`, `taskId Id FK`, `attemptId Id FK`, `messageId Id FK`, `acceptedEventSequence Int`, `consumedContextId Id? FK`, `createdAt Time` | UNIQUE(messageId,attemptId). Pending iff consumedContextId null; setting it requires context snapshot and event in same transaction. |
| `contextSnapshots` | `contextId Id PK`, `attemptId Id FK`, `steeringRevision Int`, `memoryRevision Int`, `profileRevision Int`, `manifestJson Json`, `estimatedTokens Int`, `createdAt Time` | Immutable references and bounded rendered context snapshot; exclude credentials. Manifest identifies exact message/memory/file/source versions and summary lineage. Retention/redaction purge can remove body through dedicated deletion path. |
| `remoteEvents` | `remoteEventId Id PK`, `taskId Id FK`, `attemptId Id FK`, `remoteSequence Int`, `localEventId Id FK`, `requestId Id`, `receivedAt Time` | UNIQUE(taskId,remoteSequence). Deduplicate remote events; API transport sequence is not local journal sequence. No raw SSE frame dump. |
| `remoteCursors` | `taskId Id PK FK`, `lastRemoteSequence Int`, `updatedAt Time` | Durable `afterSequence` source for next inference request; advance with remote event acceptance. No claim of remote event replay. |
| `toolIntents` | `toolCallId Id PK`, `attemptId Id FK`, `taskId Id FK`, `intentDigest Text`, `argumentDigest Text`, `intentJson Json`, `idempotencyKey Id`, `createdAt Time` | Immutable; UNIQUE(idempotencyKey). Full local envelope from TOOLS.md. No tool/proposal can choose authority fields. |
| `toolExecutions` | `executionId Id PK`, `toolCallId Id FK`, `approvalRequestId Id? FK`, `grantId Id? FK`, `dispatchReservedAt Time`, `executionJson Json` | Immutable; UNIQUE(toolCallId). One dispatch identity per intent; permitted transport retransmissions recorded as events using same execution. |
| `toolResults` | `resultId Id PK`, `toolCallId Id FK`, `executionId Id? FK`, `reconciliationOfResultId Id? FK`, `resultJson Json`, `observedAt Time` | Immutable. Reconciliation chain must match same tool/execution; no cycles. Result JSON validated against local contract. |
| `effectBarriers` | `barrierId Id PK`, `executionId Id FK`, `resourceKey Text`, `reason Text`, `resolvedByResultId Id? FK`, `createdAt Time`, `resolvedAt Time?` | UNIQUE(executionId,resourceKey). Open iff resolvedByResultId null; blocks conflicting effects across attempts/Pebbis after crash. Resolution requires evidence and event, not an expired timer. |
| `fileOperations` | `operationId Id PK`, `executionId Id FK`, `operationKind Text`, `sourceJson Json?`, `destinationJson Json`, `expectedHash Text?`, `stagedArtifactId Id FK`, `state Text`, `createdAt Time`, `updatedAt Time` | Recovery projection for staged filesystem effects; states prepared/staged/installed/verified/abandoned are **file-operation states**, never task states. Paths relative to validated roots. |

`taskAttempts` partial UNIQUE(pebbiId) applies to states running/waitingForApproval/waitingForInput/waitingForConnection/cancelling/interrupted while `finishedAt` is null. Queued rows do not claim the serial slot. Retry closes the old interrupted attempt first; the independent effect barrier can continue blocking resources. A UNIQUE(taskId) partial index over nonterminal attempts prevents two retries of one logical task from running or queueing simultaneously. All ownership FKs use composite unique keys where necessary to ensure a conversation/task/attempt cannot point into another Pebbi.

### Approval, connections and executable identity

| Table | Fields / keys | Constraints and purpose |
|---|---|---|
| `approvalRequests` | `approvalRequestId Id PK`, `toolCallId Id FK`, `intentDigest Text`, `previewArtifactId Id? FK`, `previewJson Json`, `requestedAt Time`, `expiresAt Time`, `state Text`, `decidedAt Time?`, `decision Text?`, `consumedByExecutionId Id? FK`, `revision Int` | Request snapshot immutable; state projection pending/decided/expired/invalidated/consumed. Decision CHECK allowOnce/allowForScope/deny. UNIQUE(toolCallId) for a given prepared intent; reapproval after changed intent creates new toolCallId. Consumption is transactional with dispatch. |
| `approvalDecisions` | `approvalDecisionId Id PK`, `approvalRequestId Id FK`, `decision Text`, `intentDigest Text`, `userInteractionId Id`, `createdAt Time` | Immutable; UNIQUE(approvalRequestId), UNIQUE(userInteractionId). Persist exact human decision without forging provenance from model/voice text. |
| `grants` | `grantId Id PK`, `accountId Id FK`, `connectionId Id? FK`, `appBundleId Text?`, `toolClass Text`, `resourceJson Json`, `policyVersion Int`, `expiresAt Time`, `revokedAt Time?`, `createdAt Time` | Bounded user/tool/resource scope. Never grants sensitive always-fresh classes. No serialized Keychain secret. |
| `resourceBookmarks` | `bookmarkId Id PK`, `bookmarkData Bytes`, `resourceLabel Text`, `accessKind Text`, `lastResolvedAt Time?`, `stale Bool`, `createdAt Time` | Native bookmark for chosen resource. Use security-scoped access only when issued/required; ordinary non-sandbox bookmark is location persistence, not security isolation. |
| `connections` | `connectionId Id PK`, `catalogKey Text?`, `label Text`, `transportKind Text`, `state Text`, `configurationJson Json`, `keychainReference Id?`, `capabilitiesRevision Int`, mutable timestamps/revision | States exactly CONTRACT. Config may contain URL/executable/args, never secret values. Opaque reference resolves via Keychain. No raw OAuth callback/token logs. |
| `connectionCapabilities` | `capabilitiesId Id PK`, `connectionId Id FK`, `capabilitiesRevision Int`, `schemaArtifactId Id FK`, `executableIdentityJson Json?`, `createdAt Time` | Immutable; UNIQUE(connectionId,capabilitiesRevision). Digest, signing identity and approved config for local MCP; capability drift invalidates pending approval. |
| `browserPairings` | `pairingId Id PK`, `browserKind Text`, `extensionId Text`, `profileLabel Text`, `keychainReference Id`, `lastVerifiedAt Time?`, `revokedAt Time?`, `createdAt Time` | Persistent pairing record only; pairing key remains Keychain. No cookies, browser profile path enumeration or session bearer in SQLite. |

Live AX refs, browser DOM refs, socket keys, foreground leases, frame buffers and microphone/capture handles are **not persisted as reusable authority**. Durable history can retain a human target description and opaque expired ref for audit, but restore requires fresh selection/observation.

### Memory, document coverage, routines and delivery

| Table | Fields / keys | Constraints and purpose |
|---|---|---|
| `memoryItems` | `memoryId Id PK`, `pebbiId Id FK`, `text Text`, `kind Text`, `sensitivity Text`, `pinned Bool`, `sourceJson Json`, `sharedScopeJson Json?`, mutable timestamps/revision | User-approved items only; proposals separate. Forget physically deletes text and indexes in deletion transaction. |
| `memoryProposals` | `memoryProposalId Id PK`, `pebbiId Id FK`, `text Text`, `sourceJson Json`, `replacesMemoryId Id? FK`, `reviewState Text`, mutable timestamps/revision | pending/accepted/rejected; accepting creates/revises memory with user provenance, no silent fact inference. |
| `summaries` | `summaryId Id PK`, `pebbiId Id FK`, `conversationId Id FK`, `memoryRevision Int`, `sourceManifestJson Json`, `summaryArtifactId Id FK`, `supersedesSummaryId Id? FK`, `invalidatedAt Time?`, `createdAt Time` | Summary payload immutable; invalidation metadata mutable. Forget/source deletion invalidates all dependent summaries before next retrieval. |
| `documents` | `documentId Id PK`, `fileVersionId Id FK`, `parserName Text`, `parserVersion Text`, `coverageJson Json`, `extractionState Text`, `updatedAt Time` | UNIQUE(fileVersionId,parserName,parserVersion). States pending/reading/complete/partial/failed are extraction states only. Declared units vs extracted units must reconcile. |
| `documentPassages` | `passageId Id PK`, `documentId Id FK`, `unitKey Text`, `ordinal Int`, `text Text`, `sourceLocatorJson Json`, `confidenceValue Text?`, `createdAt Time` | UNIQUE(documentId,unitKey,ordinal). Page/sheet/cell/slide/section refs preserved. OCR confidence optional, not a fact certainty measure. |
| `evidence` | `evidenceId Id PK`, `taskId Id? FK`, `sourceKind Text`, `url Text?`, `title Text`, `retrievedAt Time`, `artifactId Id? FK`, `passageId Id? FK`, `locatorJson Json`, `coverageJson Json` | Immutable source observation; no local hidden content upload implied. Web redirects retain original/final URL in locator. Raw screenshot not stored here by default. |
| `walkthroughs` | `walkthroughId Id PK`, `taskId Id FK`, `goal Text`, `currentStepId Id? FK`, `paused Bool`, mutable timestamps/revision | Progress survives restart; overlay geometry does not. Resume requires fresh refs. |
| `walkthroughSteps` | `stepId Id PK`, `walkthroughId Id FK`, `ordinal Int`, `goal Text`, `targetDescriptionJson Json`, `expectedResult Text`, `completionEvidenceId Id? FK`, `completedAt Time?`, `revision Int` | UNIQUE(walkthroughId,ordinal). No hard 15-step cap. Manual confirmation recorded distinctly from automated evidence. |
| `routines` | `routineId Id PK`, `pebbiId Id FK`, `name Text`, `instruction Text`, `state Text`, `scheduleJson Json`, `scheduleRevision Int`, `evaluatedThrough Time`, `pendingCatchUpSlot Text?`, `pendingCatchUpDueAt Time?`, `consecutiveFailureCount Int`, `authorizationSnapshotJson Json`, mutable timestamps/revision | Routine states exactly CONTRACT. Schedule snapshot has IANA zone; approval does not authorize future sensitive sends. |
| `routineOccurrences` | `occurrenceId Id PK`, `routineId Id FK`, `scheduleRevision Int`, `scheduleSlot Text`, `dueAt Time`, `taskId Id? FK`, `retryCount Int`, `nextRetryAt Time?`, `finalOutcome Text?`, `coalescedCount Int`, `createdAt Time`, `updatedAt Time` | UNIQUE(routineId,scheduleRevision,scheduleSlot). Slot is recurrence descriptor, not ID. Outcome succeeded/failed/cancelled/skipped; count failed once per occurrence, not each attempt. |
| `suggestions` | `suggestionId Id PK`, `pebbiId Id FK`, `title Text`, `rationale Text`, `evidenceRefsJson Json`, `scopeJson Json`, `expiresAt Time`, `acceptedTaskId Id? FK`, `dismissedAt Time?`, mutable timestamps/revision | Accept under ingress transaction once; read-only derivation does not grant tool permissions. |
| `notificationDeliveries` | `deliveryId Id PK`, `taskId Id? FK`, `conversationId Id? FK`, `messageId Id? FK`, `notificationKind Text`, `suppressionReason Text?`, `requestedAt Time`, `presentedAt Time?`, `readAt Time?` | OS delivery request is not proof presented/read. Deduplicate terminal task notification by task/attempt event. |
| `exportJobs` | `exportId Id PK`, `scopeJson Json`, `manifestArtifactId Id? FK`, `state Text`, `errorCode Text?`, `createdAt Time`, `updatedAt Time` | Local export bookkeeping only; server export is a separate API resource. Secrets/ephemeral capture omitted. |
| `deletionJobs` | `deletionId Id PK`, `scopeJson Json`, `progressJson Json`, `createdAt Time`, `updatedAt Time` | Resumable local purge; no false “deleted everywhere” claim. Account deletion waits for explicit server API separately. |

FTS5 tables: `messageSearch` (messageId UNINDEXED, conversationId UNINDEXED, text), `memorySearch` (memoryId UNINDEXED, pebbiId UNINDEXED, text), `documentSearch` (passageId UNINDEXED, documentId UNINDEXED, text). Maintain in the same write transaction as base changes; never trust FTS scope filtering alone—join back to authorized base rows. Indexing is a derived cache that can be rebuilt. No cloud vector index is required.

## 3. Migrations and storage safety

Use GRDB `DatabaseMigrator` with immutable ordered identifiers and explicit checksum metadata recorded by the application's migration verification layer. Identifiers describe schema dependencies, not product delivery phases:

| Migration ID | Objects introduced |
|---|---|
| `m001IdentityAndWorkspaces` | accountMetadata, settings, resourceBookmarks, workspaces, pebbis |
| `m002ConversationTaskJournal` | conversations, messages, drafts, tasks, taskAttempts, taskEvents, ingressCommands, taskInbox, contextSnapshots, remoteEvents, remoteCursors |
| `m003ArtifactsAndEvidence` | artifacts, files, fileVersions, messageAttachments, documents, documentPassages, evidence |
| `m004AuthorityAndEffects` | connections, connectionCapabilities, browserPairings, grants, approvalRequests, approvalDecisions, toolIntents, toolExecutions, toolResults, effectBarriers, fileOperations |
| `m005MemoryAndAutomation` | memoryItems, memoryProposals, summaries, walkthroughs, walkthroughSteps, routines, routineOccurrences, suggestions, notificationDeliveries, exportJobs, deletionJobs |
| `m006SearchAndIntegrity` | FTS tables, all secondary indexes, immutability triggers, cross-owner constraints and projection replay verification metadata |

Within each migration, create circular-reference tables in a single transaction and use deferred foreign-key constraints for pointer cycles. No writes of application data until all migrations complete and `foreign_key_check` passes. SQLite cannot retroactively add arbitrary FK clauses to existing tables: create final constraints when defining tables (references may name tables created later in the same migration) or use an explicit create-copy-validate-swap migration. Do not claim `ALTER TABLE` can add unsupported constraints.

Migration policy: never edit a released migration; add one. Before migrating, acquire exclusive instance/store lock, verify free disk space, checkpoint/backup consistently and run integrity checks. Roll back the migration transaction on failure; keep the old file/backup and show recovery, never delete data to make startup succeed. A binary opening a newer schema must refuse write access and offer the compatible app/export path; Sparkle rollback is not permission to down-migrate destructively. Test upgrades from every supported released schema and interrupted writes. No “erase on schema change” release flag.

## 4. Journal, remote stream and projections

Store allocates the next local task sequence inside the same transaction as append and projection update. One transaction may append multiple sequential events. An event always belongs to exactly one logical task and attempt; JSON event envelope is `{schemaVersion,eventId,taskId,sequence,type,occurredAt,payload}` and payload includes `attemptId` and type-specific fields. External transport IDs/sequences remain source metadata, never reuse them as local journal keys.

Required journal families: taskSubmitted/attemptClaimed/stateChanged, followUpAccepted/followUpsConsumed, contextPrepared, toolIntentPrepared/approvalRequested/approvalDecided/toolDispatchReserved/toolResultObserved/toolReconciled, cancellationRequested, attemptInterrupted, artifactCommitted, routineOccurrenceLinked, finalMessageCommitted. Event schemas must be versioned alongside readers; unknown event versions fail replay safely rather than silently skipping safety events.

Transient audio and token deltas are not written per frame. Persist semantic response segments/checkpoints and terminal provider events with remote ID/cursor atomically. API.md owns `afterSequence`; never resend an uncertain inference call merely because a local text fragment was not durable. Store enough request/reservation refs to explain uncertainty without retaining raw provider bodies.

Immutable-row triggers reject normal UPDATE/DELETE for taskEvents, toolIntents, toolExecutions, toolResults, approvalDecisions and committed messages/artifacts/versions. **Privacy deletion is an explicit exception**, not an impossible append-only promise: a dedicated purge transaction/connection path temporarily applies an audited deletion operation, removes all dependent content/indexes/blobs and records only nonsensitive purge metadata outside the deleted scope. It never edits evidence to make an operation look successful. The implementation must use a narrowly scoped mechanism (e.g. a connection-authorized purge flag guarded in application code and tests), not a generally writable SQL switch exposed to tools.

Projection rebuild consumes journal in sequence to a temp schema and compares state/attempt versions/results. Orphaned/gapped safety events stop recovery for the affected task. UI reads snapshots from committed projections; it cannot synthesize a terminal result that the journal cannot reproduce.

## 5. File commit protocol and whole-document coverage

File inputs are imported into immutable account-local blobs with user disclosure; user-selected external references may be retained, but model requests/previews bind to a snapshot version. Scope/path checking uses directory file descriptors and component-wise `openat`/no-follow validation, rejects `..`, absolute paths, symlink escapes, special devices and unexpected ownership changes. A string-prefix allowlist is insufficient.

Never modify a hardlinked source in place. Replacement writes a new file and atomically replaces the directory entry when supported; preserve a snapshot of the previous version. NSFileCoordinator can coordinate participating apps but cannot lock arbitrary noncooperating programs. Therefore expected-hash checks are **not** claimed as a kernel-wide compare-and-swap against other apps. Revalidate immediately before install and read back afterwards; external interference can require conflict/reconciliation. Prefer managed workspaces for writes that need stronger ownership.

Commit steps:

1. Validate root/target identity and approved expected version; create immutable intent and fileOperations prepared row before effect.
2. Stage bytes with exclusive-create, bounded size and hash verification. For atomic same-volume install, stage under the validated destination directory/volume, not assume Application Support is on the same filesystem.
3. Flush staged bytes, record staged artifact/recovery metadata, revalidate expected target and install through native atomic replacement/rename with no overwrite when `ifAbsent` applies. Use appropriate no-replace semantics, not a racy exists-then-rename shortcut.
4. Read exact destination through validated handle and verify digest/identity. Then commit fileVersion/current pointer, operation verified, tool result and artifact event in one SQL transaction.
5. Crash anywhere: inspect operation marker, staged blob, prior/current target hashes; classify installed/not applied/unknown. Never overwrite a user-modified destination just to match the journal. Cross-volume move is copy+verify+remove, with independently recoverable steps.

Document coverage manifest has `{fileVersionId, parserName, parserVersion, totalUnits, extractedUnits, failedUnits, skippedUnits, units, complete}`. `totalUnits` may be unknown until enumeration finishes; `complete` must then be false. Each unit has ordinal/key, source locator, extracted character count, method (`text`, `ocr`, `structured`) and error if any. Counts are computed from the unit records, never eyeballed from excerpts.

Native extraction contract: PDFKit text layer first and Vision OCR for explicitly selected scanned PDF/image units; UTF-8/text/Markdown direct; RTF through native attributed-text parsing; DOCX/PPTX/XLSX via bounded, nonexecuting ZIP/XML parsing with relationships, shared strings, tables/sheets/slides retained. Choose a small reviewed ZIP dependency only if platform APIs do not safely cover required archive access; no macro execution or shelling out to Office. Reject path traversal/zip bombs, external XML entities, excessive expanded size or password-protected input until manual unlock. Legacy binary Office formats need an explicitly approved conversion adapter or manual export; Quick Look renderability is not proof of complete extraction. Return unsupported/partial with the affected units rather than truncate silently.

Whole-document reading iterates all units and appends batches to storage, then reconciles counts. Long documents can be summarized in bounded model contexts, but an excerpt is never labelled whole-file reading. Preview selects PDFKit/Quick Look/plain text by verified UTI/MIME. Preview lease binds artifact ID, consumer and expiry; temp preview copies are removed when last consumer closes, subject to honest OS-cache limitations.

## 6. Retention, forgetting and export

User-visible retention settings govern conversations, artifacts, memories and diagnostics under canonical SECURITY.md ceilings. Temporary rendered/extracted preview copies are removed at last-consumer/session cleanup and no later than 24 hours; local redacted diagnostic logs roll off at seven days. Durable user-approved document passage indexes are user content, not temporary render files. Defaults are product/security policy, not ad hoc parser choices. Ephemeral capture/audio lifetimes are separate and must not be expanded by a general chat-retention preference. Cleanup is interruptible, journaled and never races a live consumer of an immutable blob; reference counts/leases are recalculated before unlink.

Forget/delete transaction removes base text, FTS entries and dependent summaries/context caches, increments Pebbi memoryRevision and invalidates in-flight contexts before the next model/tool step. Purge unreferenced blobs through a resumable job. Do not claim SQLite DELETE securely erases WAL/backups/SSD cells. Checkpoint/vacuum/backup rotation can reduce retained copies, but forensic erasure requires device/storage controls and is not promised.

Local export includes a schema-versioned manifest, Pebbi profiles, messages, memories, task/result evidence and selected durable files. Include checksums and per-item extraction/export errors; no secret values, auth tokens, browser pair keys, raw ephemeral captures or hidden diagnostic payloads. Export paths are generated/sanitized against traversal. Server account export contains only server-held account/usage data through API.md; combine manifests explicitly, do not imply chat sync. Deleting an account has separate local purge, Keychain removal, helper revocation and server request/results; show incomplete remote deletion honestly when offline.

## 7. Private-session storage exception

PB-031 private sessions use an account-scoped in-memory GRDB store with the same domain schema for messages, context, memories proposed during the session and full tool payloads. They do not write those bodies to the normal account database/WAL, FTS, diagnostics, autosave, backups or disk previews. `Store` routes a session using a trusted `retentionMode` selected in native UI, never a model argument. No learning/personalization is retained from that session. Closing/sign-out/restart loses its ephemeral conversation, and the UI must say so before enabling it.

Safety durability still applies. Add `privateEffectRecords` in `m004AuthorityAndEffects`: `recordId Id PK`, `privateSessionId Id`, `taskRef Id`, `attemptRef Id`, `toolCallRef Id`, `executionRef Id`, `intentDigest Text`, `idempotencyKey Id`, `toolClass Text`, `connectionRef Id?`, `safeTargetLocatorJson Json?`, `externalRequestRef Text?`, `eventKind Text`, `effectState Text`, `occurredAt Time`. This is an immutable append-only minimal safety journal with no FK to ephemeral entities and no prompt, message, script, screenshot, arguments or artifact bodies. Field suffix Ref here explicitly denotes a detached historical reference, not a dereferenceable authority. Public UUID values remain UUIDs; externalRequestRef is provider-owned opaque text. The write-ahead dispatch record commits here before the effect, and results/reconciliation append another record for the same executionRef. No private-mode fallback writes full ToolIntent JSON to disk.

The broker's full immutable intent/approval/result remain in memory; their digests bind the minimal durable records. The native approval explains any minimum target/provider identifiers necessary for uncertain-effect recovery. If even a safe locator would disclose sensitive content, require an explicit choice to retain that minimum recovery metadata or refuse that mutation in private mode. Do not sacrifice crash-safe effect handling to promise an impossible zero-record write. On restart, show only unresolved private-action recovery cards; do not reconstruct a fake private chat. After reconciliation, purge those records according to the minimal security-retention rule.

Private attachments/text previews are memory-only. An explicit Save action creates a normal durable artifact with its usual disclosure; without Save, do not use Quick Look/disk parsers or code runners that require writing private bodies to temporary files. Offer the inert memory preview or explain that the requested operation requires an explicit saved working copy. This preserves full feature access through a deliberate privacy choice rather than silently breaking private mode. Server usage/security metadata remains under SECURITY.md and cannot be disabled by a local privacy preference.

Required test: run a private typed/file session, crash/relaunch and search the actual DB/WAL, FTS, artifacts, logs and backups for unique canary content. It must be absent unless explicitly saved. An approved uncertain private mutation must retain only the declared minimal reconciliation metadata and block replay until resolved.

## 8. Required migration and persistence tests

| ID | Test | Required result |
|---|---|---|
| DATA-01 | Every migration from empty + every supported old schema; kill mid-migration | Full final schema or intact old state; no partial application use |
| DATA-02 | Two writers submit/claim/follow up/complete same task | Unique ingress/slot/sequence constraints hold; exactly one deterministic receipt |
| DATA-03 | UPDATE immutable intent/result and delete outside purge path | SQL/app guard rejects; legitimate privacy purge removes dependent content |
| DATA-04 | Remote and local sequence overlap, duplicate/out-of-order SSE | Remote dedupe/cursor valid; local journal monotonic and independent |
| DATA-05 | Disk full before reservation, after file install, before result commit | No pre-reservation effect; recover installed file without duplicate overwrite |
| DATA-06 | Path traversal, symlink/hardlink swap, external app modifies destination | No scope escape by FileService; conflict/unknown reported; prior snapshot recoverable |
| DATA-07 | Multi-sheet XLSX, scanned PDF, missing page, encrypted/zip-bomb file | Accurate unit counts and source locators; complete false on any unexplained omission |
| DATA-08 | Forget item or delete source while summary/request in flight | No future retrieval from base/FTS/summary cache; honest already-transmitted limitation |
| DATA-09 | Export twice, verify checksums, interrupt purge, reopen newer schema | Deterministic manifests, resumable deletion, old binary refuses writes |
| DATA-10 | Rebuild task projections from event journal | Matches live state and terminal evidence; gaps fail closed |

Tests must query row counts and constraints programmatically and read actual generated artifacts. Empty schemas, sample-only files and plausible migration output do not satisfy this specification.
