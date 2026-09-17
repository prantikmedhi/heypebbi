# Local tool contracts and authority boundary

**Proposed normative contract; no tool handlers are implemented.** This document owns native tool wire shapes. [CONTRACT](../CONTRACT.md) owns common formats/states; [API](API.md) owns HTTP/SSE/WebSocket shapes; canonical SECURITY.md owns policy. Never expose a raw backend/MCP/native action directly to the model without the broker defined here.

## 1. Envelope, IDs and immutable records

All local JSON fields and local tool names use camelCase. `schemaVersion` is integer `1`. IDs are UUID strings, opaque and case-preserved; dates are RFC 3339 UTC. Unknown fields, duplicate JSON keys, invalid Unicode, nonfinite numbers and unknown enum values are rejected before policy evaluation. Do not normalize a malformed identifier into a valid one. Provider tool names and provider IDs are opaque values in explicitly named fields; they need not be UUIDs and must not be rewritten to camelCase.

The following is proposed schema notation, not an implemented JSON Schema or executable code. A `?` denotes optional; `[]` denotes a bounded array.

```text
ToolProposal {
  schemaVersion: 1, toolName: LocalToolName, arguments: object,
  providerCallRef?: string
}
ToolIntent {
  schemaVersion: 1,
  toolCallId: UUID, taskId: UUID, attemptId: UUID, pebbiId: UUID,
  conversationId: UUID, toolName: LocalToolName, arguments: object,
  providerCallRef?: string, createdAt: timestamp,
  steeringRevision: integer, cancelEpoch: integer, accountEpoch: integer,
  policyVersion: integer, adapterVersion: string,
  resourceScopes: ResourceScope[], targetRevision?: string,
  riskClass: readOnly | localWrite | externalWrite | sensitive,
  idempotencyClass: readOnly | providerKey | compareAndSet | nonIdempotent,
  idempotencyKey: UUID, argumentDigest: string, intentDigest: string
}
ToolExecution {
  schemaVersion: 1, executionId: UUID, toolCallId: UUID,
  approvalRequestId?: UUID, grantId?: UUID,
  dispatchReservedAt: timestamp, authorityDigest: string,
  leaseGeneration: integer
}
ToolResult {
  schemaVersion: 1, resultId: UUID, toolCallId: UUID, executionId?: UUID,
  taskId: UUID, attemptId: UUID, observedAt: timestamp,
  outcome: succeeded | failed | denied | cancelled | unknown,
  effectState: notApplied | applied | unknown | notApplicable,
  verification: verified | unverified | notApplicable,
  output: object, evidenceRefs: UUID[], artifactRefs: UUID[],
  error?: ToolError, reconciliationOfResultId?: UUID,
  nextAction: continueTask | requestApproval | requestInput | reconnect | reconcile | stop
}
ToolError {
  code: ToolErrorCode, message: string, retryable: boolean,
  details: object
}
```

Agent task envelopes use actual task/attempt IDs. For standalone `insertDictation` only, the broker's trusted audio owner context maps envelope taskId/attemptId to audioOperationId/audioAttemptId and routes all records to audio_event_receipts (DATA-MODEL.md), not agent task tables. Resolve dictationSessionId through the active controller registry; it must match role=dictation, account/Pebbi/conversation, reviewed text artifact and current focus. Audio session IDs are never accepted as task authorization. Conversation audio cannot dispatch local tools; a reasoning proposal cannot choose or forge an audio owner.

Only the broker creates intent authority fields; a proposal cannot supply its own grants, risk or idempotency class. `ResourceScope` has `{scopeKind, resourceId, operation, expiresAt?}` with resource IDs resolved from trusted local registries. Values such as arbitrary absolute paths or unverified web origins do not become authority merely by appearing in a proposal.

Digest algorithm: UTF-8 RFC 8785 canonical JSON + SHA-256 lower-case hex. `argumentDigest` covers validated arguments. `intentDigest` covers all intent fields except itself, including target revisions and policy, not an abbreviated human summary. Finite numeric schemas only. Hashes are integrity bindings, not encryption or secret redaction. Except for the bounded authored-text producer below, large/secret data is never in the intent; use immutable artifact refs or private authority handles. `stageTextArtifact` contains bounded explicit text; in private mode its entire intent, digest and result remain in memory. Approval previews must show the exact meaningful content represented by the digest.

Intent, execution and result rows are immutable. Preparation failure can produce a result without an execution. Broker bookkeeping/status projections may change, but immutable rows cannot. Later verification appends another result; the derived current observation selects the latest valid reconciliation chain, preserving the first response.

Common error codes: `invalidArguments`, `unknownTool`, `policyDenied`, `approvalRequired`, `approvalExpired`, `scopeExpired`, `permissionDenied`, `staleTarget`, `focusChanged`, `requiresTakeover`, `invalidGeometry`, `protectedContent`, `connectionUnavailable`, `capabilityChanged`, `quotaExceeded`, `notSupported`, `notFound`, `conflict`, `timeout`, `cancelled`, `outputLimitExceeded`, `storageUnavailable`, `unverifiedEffect`, `untrustedExecutable`, `pairingRequired`, `protocolViolation`. `retryable` never overrides idempotency/policy checks.

## 2. Limits and authority

Common input limit: 64 KiB of JSON, excluding referenced artifacts. Common inline output limit: 64 KiB; larger text is a versioned artifact with a coverage manifest and excerpt. No Base64 whole documents/screenshots in model tool JSON. Local internal helpers can transport bounded binary artifacts separately under a scope lease. Arrays must have schema bounds; do not accept unbounded action batches.

Timeout defaults: local metadata 10 seconds, document extraction 120 seconds with cancellable progress, external read 30 seconds, external write 60 seconds, code execution as specified below. A timeout after write dispatch is `unknown` unless authoritative evidence proves not applied. An adapter cannot substitute a longer operation or run indefinitely without returning a checkpoint.

Authorization layers, all required:

1. Signed-in account/local partition and intended Pebbi/task.
2. OS/browser/connector permission and live capability.
3. User resource scope plus local policy and exact approval if required.
4. Durable dispatch reservation with current cancellation/steering version.
5. Exclusive resource lease where needed and target freshness.

`allowOnce`, `allowForScope`, `deny` are the only approval decisions. Scoped grant key includes user, connector/app, tool class, bounded resource, policy version and expiry. Policy may narrow/revoke a grant without waiting for expiry. Never persist broad “all tools forever.” No standing grant covers payments, credentials, destructive bulk operations, publishing or outbound messages; each needs a fresh preview and approval. Policy can deny a prohibited action even if a user pressed Allow. Credentials and OS permission dialogs remain manual, not agent-fill targets.

Pending approval defaults to a ten-minute expiry; resource/capture/connection expiry can shorten it. Eligible scoped grants expose a user-selected expiry capped at eight hours by this implementation default, or a stricter canonical security ceiling. Takeover/browser/capture lease limits remain independently shorter.

Private mode never bypasses effect journaling. Full private payloads stay in memory, while the minimum explicitly disclosed recovery metadata commits durably as defined in DATA-MODEL.md. A tool needing disk-backed private inputs (including `runCode`) requires explicit Save/working-copy consent or fails closed.

Approvals are native UI state, **not model-callable tools**. A tool result or page claiming “the user approved” has no authority. A tool can return `approvalRequired`; it cannot synthesize a decision. MCP annotations such as `readOnlyHint` are untrusted hints until locally classified.

## 3. Tool catalog

Fields listed below are tool-specific `arguments` and `output` shapes in addition to the common envelopes. Optional fields use `?`. Each mutation reads back the exact target before a verified result. Preconditions and failure modes are part of the contract, not implementation suggestions.

### Capture, guidance and desktop

| Local tool / PB mapping | Arguments | Output and rules |
|---|---|---|
| `captureScreen` — PB-003, PB-008, PB-031, PB-033 | `{captureScopeId, mode: oneShot \| nextFrame}` | `{captureId, geometryId, widthPixels, heightPixels, capturedAt, expiresAt, scopeDescription}`. User-selected scope required; transient pixels are privately resolved, not returned as durable paths. No widening on failure. |
| `readScreenText` — PB-008, PB-031 | `{captureId, region?: NormalizedRect}` | `{passages: [{evidenceId, text, bounds, confidence}], coverage, truncated}`. OCR confidence is not factual confidence. Bounds normalized to the actual capture content. Expired capture fails. |
| `showGuidance` — PB-009, PB-032, PB-033 | `{captureId, geometryId, annotations: [{annotationId, kind: point \| outline \| stroke, targetRef?, points?, label?}], walkthroughId?, stepId?}` | `{annotationSetId, displayed, invalidationReason?}`. Max 20 annotations/200 points per stroke; labels ≤160 characters. Only user-authorized selected scope; no unrelated-app overlay. |
| `clearGuidance` — PB-009 | `{annotationSetId}` | `{removed}`. Idempotent removal; already removed returns true. |
| `inspectDesktop` — PB-018 | `{appScopeId, windowRef?, cursor?, maxNodes?}` | `{treeGeneration, appBundleId, processIdentity, windows, elements, truncated, nextCursor?}`. Max 500 nodes; refs contain role, name, enabled, supportedActions and geometry. `processIdentity` is an opaque registry value, not a PID authorization token. |
| `inspectDesktopElement` — PB-018 | `{appScopeId, elementRef}` | `{treeGeneration, element}`. Re-resolve or stale target; no broad fallback search for similarly named controls. |
| `pressDesktopElement` — PB-017–PB-018 | `{appScopeId, elementRef, treeGeneration, expectedRole, expectedLabel}` | `{targetRef, observedChange, focusChanged}`. AXPress only; non-idempotent; blocked if secure/sensitive/out of scope. Semantic background limits apply. |
| `setDesktopValue` — PB-018 | `{appScopeId, elementRef, treeGeneration, expectedValueDigest, value}` | `{targetRef, resultingValueDigest, changed}`. Value ≤16 KiB; ordinary writable controls only. Native select/slider first; conditional read-check is not an OS-wide atomic CAS, so treat uncertain outcomes conservatively. |
| `scrollDesktop` — PB-018 | `{appScopeId, elementRef, treeGeneration, direction: up \| down \| left \| right, increments}` | `{targetRef, observedViewport}`. Increments integer 1–10; supported semantic scroll only. No hidden CGEvent fallback. |
| `takeoverAction` — PB-017–PB-018, PB-033 | `{takeoverRequestId, captureId, geometryId, action: click \| keyChord \| typeText, point?: NormalizedPoint, keyChord?, text?}` | `{posted, observedTarget, verificationEvidenceId?}`. Exact native preview and short foreground lease; one action, not an arbitrary batch. Manual credentials/payment UI excluded. No guessed coordinates. |
| `insertDictation` — PB-010, PB-017 | `{dictationSessionId, focusToken, textArtifactId, expectedSelectionDigest}` | `{inserted, targetRef, insertedTextDigest, method: accessibility \| approvedPaste}`. Review/fresh focus required; duplicate effect reconciled; no background focus stealing. |

`NormalizedPoint` has finite `{x,y}` in [0,1]. `NormalizedRect` has finite `{x,y,width,height}` inside [0,1] without overflow beyond the source. They are capture-local, not global event coordinates; only the geometry service converts. `keyChord` is a locally validated named combination; reject secure-attention shortcuts or chords outside the displayed takeover intent.

### Browser and research

| Local tool / PB mapping | Arguments | Output and rules |
|---|---|---|
| `inspectBrowser` — PB-019 | `{browserSessionId, tabId, documentId?, cursor?, maxElements?}` | `{documentId, navigationGeneration, domRevision, url, title, elements, truncated, nextCursor?}`. Max 500 elements, user-selected tab, authenticated native messaging only. |
| `readBrowser` — PB-019–PB-020 | `{browserSessionId, tabId, documentId, navigationGeneration, cursor?, maxCharacters?}` | `{evidenceId, url, title, text, coverage, nextCursor?}`. Default 16 KiB, max 64 KiB; DOM text, not guaranteed whole site. Password/payment/hidden sensitive fields excluded. |
| `navigateBrowser` — PB-019 | `{browserSessionId, tabId, expectedDocumentId, url}` | `{documentId, navigationGeneration, finalUrl, loadStatus}`. HTTPS or explicit user-approved HTTP; reject file, javascript, data, browser-internal URLs. New origin may require new grant. GET navigation can trigger server effects, so suspicious action URLs need mutation policy. |
| `clickBrowserElement` — PB-017, PB-019 | `{browserSessionId, tabId, documentId, navigationGeneration, elementRef, expectedLabel, expectedRole}` | `{observedChange, documentId, verificationEvidenceId?}`. Resolve fresh element and enforce semantic action classification; native .click is not guaranteed trusted user activation. No silent coordinate retry. |
| `fillBrowserElement` — PB-019 | `{browserSessionId, tabId, documentId, navigationGeneration, elementRef, expectedValueDigest, text}` | `{resultingValueDigest, inputEventsDispatched}`. Nonsecure ordinary inputs only; text ≤16 KiB. Does not submit; send/publish needs a separate fresh preview. |
| `scrollBrowser` — PB-019 | `{browserSessionId, tabId, documentId, elementRef?, direction, cssPixels}` | `{scrollPosition, domRevision}`. Bounded absolute delta ≤2000 CSS px; verify actual scroll; no viewport/global pixel confusion. |
| `searchWeb` — PB-020 | `{query, maxResults?, freshness?}` | `{results: [{evidenceId, title, url, snippet, retrievedAt}], providerLabel}`. Query ≤2000 characters; 1–20 results. Actual authorized search adapter required; unavailable provider is a blocker, not synthesized results. |
| `fetchWebSource` — PB-020 | `{url, cursor?, maxCharacters?}` | `{evidenceId, finalUrl, title, content, retrievedAt, coverage, nextCursor?}`. SSRF-safe HTTP client; reject loopback/private/link-local/cloud metadata, credentials in URL, unsafe redirects and DNS rebinding. Each redirect revalidated; preserve source URL and retrieval time. |

Search-provider transport is an adapter behind the approved backend/connection architecture; this table introduces no new HTTP route. If no search integration is configured, use an explicitly selected browser session where permitted or return unavailable. Do not fabricate a tool based on an assumed Responses built-in capability.

### Files, documents and memory

| Local tool / PB mapping | Arguments | Output and rules |
|---|---|---|
| `listWorkspace` — PB-021 | `{workspaceId, relativePath?, cursor?, maxItems?}` | `{entries: [{fileId?, relativePath, type, byteCount}], nextCursor?}`. Max 200 entries; validated root, no symlink traversal or hidden broad-home enumeration. |
| `readFile` — PB-014, PB-021 | `{fileId, fileVersionId, offset?, count?}` | `{artifactId, text?, mimeType, coverage, nextOffset?}`. Text read uses zero-based Unicode scalar offset and scalar count, max 16000; offsets never ambiguously mix byte/line units. Binary returns artifact metadata, not guessed text. |
| `extractDocument` — PB-014 | `{fileId, fileVersionId, unitCursor?, maxUnits?}` | `{documentId, passages, coverageManifestId, nextCursor?}`. PDF pages, document sections, spreadsheet sheets/cells, slide numbers retain provenance. Whole-document claim requires completed coverage manifest. |
| `stageTextArtifact` — PB-021, PB-031 | `{workspaceId, draftId: UUID \| null, chunkIndex, text, mimeType, final}` | Closed chunk/final result defined below; stages UTF-8 bytes in an internal account store, never writes a target workspace or executes text. |
| `createFile` — PB-021 | `{workspaceId, relativePath, contentArtifactId, mimeType, ifAbsent: true}` | `{fileId, fileVersionId, byteCount, sha256}`. Atomic staged write/rename after boundary checks; collision returns conflict, never overwrite by default. |
| `replaceFile` — PB-017, PB-021 | `{fileId, expectedVersionId, contentArtifactId}` | `{fileVersionId, sha256, previousVersionId}`. Preview diff, expected hash/version guard, atomic replacement, preserve prior version under retention. Concurrent outside edits cause conflict. |
| `moveFile` — PB-021 | `{fileId, expectedVersionId, destinationWorkspaceId, relativePath, ifAbsent: true}` | `{fileId, fileVersionId, relativePath}`. Cross-volume operation is copy-verify-then-remove with recovery journal; not falsely atomic. Moving outside grants fails. |
| `trashFile` — PB-017, PB-021 | `{fileId, expectedVersionId}` | `{trashed, recoveryReference?}`. Native Trash when supported, fresh preview for destructive scope; never permanent unlink as fallback. Batch destruction requires separate bounded preview. |
| `previewArtifact` — PB-014, PB-021 | `{artifactId}` | `{previewLeaseId, opened, previewKind}`. Native Quick Look/PDF/plain text; opening a preview executes no scripts. User action or current presentation scope required. |
| `searchMemory` — PB-013 | `{pebbiId, query, maxItems?}` | `{items: [{memoryId, revision, text, provenance}], memoryRevision}`. Current Pebbi only unless shared grants; max eight by default. |
| `proposeMemory` — PB-013 | `{pebbiId, text, sourceMessageIds, sensitivity, replacesMemoryId?}` | `{memoryProposalId, requiresUserReview: true}`. Does not silently store a new user fact; inspect/edit/forget are native user commands. |
| `runCode` — PB-017, PB-021, PB-031 | `{workspaceId, scriptArtifactId, expectedSha256, inputFileVersionIds, arguments, timeoutSeconds}` | `{executionReportArtifactId, exitCode?, stdoutArtifactId, stderrArtifactId, outputFileVersionIds, terminationReason, isolation: controlledLocalNotSandboxed}`. Exact per-run consent, trusted review and restrictions below. Non-idempotent. |

All file paths in tool arguments are relative to a granted workspace root. Absolute paths displayed by native panels may be useful to the user but must not become model authority. Artifact version references are immutable. `readFile` document extraction and binary reading are distinct; truncation is explicit. Document parser support/failure matrix belongs in [DATA-MODEL](DATA-MODEL.md).

### Authored UTF-8 producer and immutable script binding

`stageTextArtifact` is the only new model-callable producer. Ordinary assistant prose is never implicitly materialized, saved or executed. Its closed input and successful output schemas are `$defs.StageTextArtifactArguments` / `$defs.StageTextArtifactOutput` in [tool-envelope.schema.json](schemas/tool-envelope.schema.json). All six input properties are required, no extras:

- `workspaceId`: UUID of an already authorized workspace. Broker resolves account, Pebbi, task, attempt, retention mode and workspace access revision from trusted context; none is a model argument.
- `draftId`: null for the first request only, otherwise the broker-returned UUID; null requires `chunkIndex: 0`. A new provider call with null creates a new draft, not a guessed continuation.
- `chunkIndex`: integer 0–4095; contiguous from zero. At most 4096 chunks and 4,194,304 UTF-8 bytes per draft. At most one unfinished draft per attempt; finalize or cancel it before starting another.
- `text`: well-formed Unicode encoded exactly as UTF-8, at most 32,768 bytes per chunk. Reject lone surrogates/invalid UTF-8; do not normalize Unicode, line endings or add a BOM/newline. Empty text is allowed only on a final chunk (including a zero-byte artifact). JSON escaping/envelope overhead still counts against the independent 65,536-byte serialized proposal limit; a caller must use smaller chunks when necessary.
- `mimeType`: exact allowlist `text/plain`, `text/markdown`, `text/csv`, `text/html`, `application/json`, `application/x-sh`. No parameters, aliases, binary/base64 upload mode or MIME sniffing as authority. MIME is immutable at chunk zero; it is a content label, not a promise of valid JSON/CSV/HTML or execution permission. HTML/shell preview is inert text.
- `final`: Boolean; the last chunk seals the concatenation in index order. No separate finish tool, append-after-finish or mutating a sealed artifact.

Successful nonfinal output is exactly `{draftId, nextChunkIndex}`. Final output is exactly `{draftId, nextChunkIndex, artifactId, byteCount, sha256, mimeType}`. `nextChunkIndex` is the acknowledged chunk index plus one (1–4096), `byteCount` is 0–4,194,304 and `sha256` is lowercase 64-hex SHA-256 of the complete exact UTF-8 bytes. Partial outputs must not claim an artifact/hash. Success uses ToolResult outcome=succeeded, effectState=applied (internal staging only), verification=verified after exact stored-byte read-back; a rejected/cancelled-before-commit chunk is notApplied. The final ToolResult lists that artifact in `artifactRefs`; native producer IDs/bytes/hashes are the only valid inputs to consumers. Error output is `{}` with a common ToolError; it never returns a half-committed success.

**Linearization and idempotency:** broker classifies this as `localWrite` + `compareAndSet` limited to internal staging under the existing workspace scope; it does not confer a workspace write grant. Store deduplicates the first request by immutable broker `toolCallId`/execution/idempotency key and returns its stored draft receipt on a lost-response retry. A duplicate gateway proposal `callId` maps to that same local intent, never a fresh draft. Subsequent chunks dedupe by `(draftId,chunkIndex)` and exact `(text UTF-8 bytes,mimeType,final)` equality. An identical retry returns the original chunk output (including its original next index), not the draft's later progress. A changed duplicate is `conflict`; a gap, unsupported MIME, nonfinal empty text or invalid bounds is `invalidArguments`/`outputLimitExceeded` as appropriate. Unknown/cross-account/Pebbi/task/attempt/workspace drafts return `notFound` without existence disclosure; expired workspace scope returns `scopeExpired`. A changed access revision requires revalidation, never silently broadens access.

Commit chunk bytes and immutable chunk receipt atomically; at finalization verify all bytes, compute hash, commit immutable artifact + provenance/scope + final receipt in one Store transaction. Durable backing/blob installation is flushed before publishing that transaction and orphan-safe on restart. Identical final retries return the **same** artifact ID; another new authored draft gets a new artifact identity even if its blob bytes deduplicate. Finished drafts reject new indices with `conflict`. A retry of an earlier unchanged acknowledged chunk is receipt lookup only and cannot unseal or re-execute anything.

**Cancellation/privacy:** check account/cancel/steering generations before staging and commit. Cancellation linearizes against finalization: before commit, no artifact result is published; purge unfinished bytes/receipts and close the draft. After a committed finish, cancellation prevents downstream create/replace/run dispatch; it does not claim to undo that artifact or any already admitted effect. Normal completed artifacts follow explicit task retention/forget policy. Cancelled/abandoned drafts are not resumable; reject late calls with `cancelled`, or `notFound` after purge. Crash/retry marks unfinished drafts abandoned and cleans internal staging before a new attempt; no automatic resume or execution. Sign-out revokes staging access immediately and cleans unfinished bytes; account deletion purges drafts, chunks and artifacts under the normal deletion protocol.

Private drafts, chunks, artifact bytes **and their content hashes and staging intent digests** stay in the in-memory store; staging has no external uncertain effect and writes no `privateEffectRecords` entry. No private text/hash in WAL, logs, journal, filenames, previews or backups. Explicit accessible native Save/working-copy consent may export the selected sealed artifact into a new durable artifact identity/provenance; mere staging, file/code request or model text is not Save consent. Unsaved private artifacts cannot reach a disk-backed `createFile`, `replaceFile` or `runCode`. Closing the session discards them. Binary/document generation, if needed, uses separately reviewed code plus normal output import; staging itself grants no execution/network capability.

`createFile`/`replaceFile` resolve `contentArtifactId` to a sealed artifact authorized for this account/workspace/task context; `createFile.mimeType` must equal its stored MIME. A draft ID or invented UUID is not an artifact. For an existing imported artifact, the trusted file/version selection supplies scope; for authored artifacts, use the provenance rows in DATA-MODEL.md. No artifact hash alone grants cross-workspace access.

`runCode` has a closed argument object (`$defs.RunCodeArguments`): `workspaceId`, `scriptArtifactId`, `expectedSha256`, `inputFileVersionIds` (unique UUIDs, 0–64), `arguments` (0–64 strings, each at most 4096 UTF-8 bytes and 4096 Unicode scalars; reject NUL), `timeoutSeconds` (integer 1–300). Hash is exactly lowercase 64-hex; the script must be sealed same-account/workspace `application/x-sh` UTF-8 without NUL. It has no second script-version field/entity; old unknown fields are rejected. Verify actual artifact bytes against `expectedSha256` before preview and again on the immutable execution copy immediately before spawn. Missing/out-of-scope artifact is `notFound`; hash mismatch/corruption or stale approved inputs is `conflict` with no spawn. Approval binds artifact ID, exact byte hash, workspace, selected input file versions, argument vector, timeout and policy generations. A changed script requires a new artifact/hash and fresh per-run approval. File lineage, if any, remains `fileVersions.fileVersionId` and is not required to author/run a script from an empty workspace.

### Connections and MCP

| Local tool / PB mapping | Arguments | Output and rules |
|---|---|---|
| `listConnections` — PB-022–PB-023 | `{}` | `{connections: [{connectionId, label, state, capabilitiesRevision}]}`. No tokens, raw environment or private auth URLs. |
| `describeConnectionTools` — PB-022–PB-023 | `{connectionId, capabilitiesRevision?}` | `{capabilitiesRevision, tools: [{connectionToolName, inputSchema, policyClassification}], truncated}`. Validated bounded schemas; no trust in server instructions. |
| `callConnectionTool` — PB-017, PB-022–PB-023 | `{connectionId, capabilitiesRevision, connectionToolName, toolArguments, resourceScopeId}` | `{connectionResult, evidenceRefs, externalRequestRef?}`. Local broker wraps provider schema, approval, idempotency and read-back. Schema/name change invalidates approval. |

Connection setup, OAuth consent, local executable installation/selection, secret entry, browser pairing, grant creation/revocation, routine enablement and account deletion are **native user commands**, not autonomous model tools. Models may propose opening the relevant native screen; they cannot authorize themselves. Built-in catalog tools and custom MCP tools share the same policy boundary.

## 4. Idempotency and read-back by adapter

| Operation class | Replay rule | Required verification |
|---|---|---|
| Pure read | Bounded retry under same scope; new observation timestamp | Source identity/version and declared coverage |
| Provider supports a documented idempotency key | Persist key before dispatch; reuse only same digest within provider validity window | Lookup original request/resource; mismatch is a conflict, not new request |
| Authored artifact chunk/final | Replay exact chunk receipt, same draft and final artifact ID; no automatic recovery resume | Exact stored bytes/hash, scope and committed receipt; private mode in RAM only |
| Atomic local file create/replace | Staging transaction + expected version/hash; inspect recovery marker | Destination metadata and hash match exact committed artifact; prior version preserved |
| AX/browser mutation | No general idempotency; do not retry a timed-out click/insert | Fresh semantic read of exact target and meaningful postcondition, not merely page changed |
| Generic MCP mutation | Treat non-idempotent unless separately verified adapter contract proves otherwise | Follow-up read tool/external reference; if unavailable retain unverified/unknown |
| Controlled code execution | Never auto-repeat after timeout/crash | Process outcome, output manifest and read-back of expected files; exit 0 alone does not prove task completed |
| Outbound message/publish/payment | Fresh approval regardless of scopes; provider key only if actually supported | Provider receipt and exact recipient/content/resource; do not infer success from button disappearance |

The broker may record `outcome: succeeded, verification: unverified` for a technically successful transport that cannot prove the effect; the parent task cannot use it as verified fulfillment. If verifier fails after application, retain `effectState: applied` when evidence supports it rather than relabeling notApplied. Undo is another explicit tool intent with its own policy/preview, never an automatic rollback claim.

## 5. Controlled local code execution — explicit non-sandboxed design

**Selected implementation:** a signed `PebbiExecutionSupervisor` launches the system `/bin/zsh` as a noninteractive interpreter with startup files disabled (`-f`), an immutable reviewed script artifact and an explicit argument vector. No shell concatenation of tool arguments, no `eval`, no `curl | sh`, no downloading an executable in the run path, no paid coding-agent CLI, no administrator privileges. The supervisor uses `posix_spawn`/equivalent explicit process APIs, a new process group, pipes, parent-liveness monitoring and resource limits. Actual implementation must test startup-file behavior and reject ambient configuration it cannot suppress; system-wide shell startup behavior is disclosed, not represented as hermetic.

This capability is for user-reviewed, trusted transformations/code in a disposable working directory. Model-generated or downloaded code is untrusted until the user inspects the full script and its referenced inputs. A native review shows exact immutable script artifact/digest, arguments, input files, intended writes, maximum runtime and a plain warning: **“This runs with your macOS user permissions. Pebbi's workspace rules are not an OS sandbox; code may access other files or the network.”** `allowOnce` is required for every run, including routines. No `allowForScope` unattended code execution. A review checkbox is not proof that unsafe code became safe; reject a run whose purpose requires bypassing protected-resource policy.

Restricted context and operational controls:

- Copy only approved input file versions into a fresh per-execution working directory; generated script cannot reference the model's full chat/history through environment or arguments. No provider/OAuth/Keychain secrets passed; stdin closed unless an explicitly approved input artifact supplies it.
- Environment built from a small explicit set: controlled `PATH` (`/usr/bin:/bin`), working-directory `HOME`, `TMPDIR`, locale. No inherited environment variables, shell history or user startup dotfiles. Absolute interpreter path; show all explicit arguments.
- Default wall timeout 60 seconds; user-approved maximum 300 seconds. CPU soft limit 60 seconds, file-size limit 16 MiB per file, 128 open descriptors; configure available POSIX limits in the supervisor. A process-group RSS watchdog and output-size checks are best-effort controls, not security isolation guarantees.
- Stdout/stderr each limited to 1 MiB retained; terminate on sustained excess and return `outputLimitExceeded`. UTF-8 decode safely, strip terminal control sequences and redact known secret patterns before UI/model excerpts. Redaction is not a guarantee arbitrary secrets cannot appear.
- At cancel/timeout/parent EOF: SIGTERM owned process group, wait two seconds, SIGKILL if needed, reap children and record termination. Identity-check PIDs/group before signalling to avoid PID reuse. No launchd persistence. A hostile program can detach/escape process groups; therefore this path must not claim containment of malicious code or guarantee all descendants are stopped.
- Never auto-import outputs outside the fresh run directory. Enumerate without following symlinks, reject device/special files and excessive counts, hash accepted files and require user-approved destination writes through normal FileService commits. Do not execute resulting binaries/macros or automatically open active HTML.
- Network is **not OS-blocked** by this design. Do not display “network disabled” or “sandboxed.” A script can attempt reads outside the workspace; file-grant checks around Pebbi tools do not stop it. Hardened runtime and TCC are not a substitute.

Production safety caveat: this mode cannot safely host adversarial autonomous code. If release security requirements demand guaranteed filesystem/network confinement or untrusted background execution, this path must remain disabled until a separately reviewed OS-enforced isolation design (for example a disposable VM with explicit exports) is approved and tested. Do not quietly use deprecated/private sandbox mechanisms, weaken the threat model, or ship a falsely labelled sandbox to satisfy PB-021. Full product scope includes this explicit controlled mode and truthful gates, not a promise of impossible isolation.

## 6. Local MCP process contract

`MCPProcessManager` launches only a user-selected executable/configuration after native review. Show executable path/resolved identity, arguments, working directory, requested secret references and the fact it runs as the user. For interpreters/package launchers, disclose that the executable's signature does not authenticate downloaded package code. Installation/update commands require separate consent; never silently run `npx`, `uvx` or a package manager simply because a catalog entry exists.

Use explicit argument arrays, minimal environment, Keychain values only for individually authorized connector variables, closed extra file descriptors, bounded stdout/stderr, and a parent-lifetime channel. Stdio protocol is JSON-RPC MCP as negotiated; stdout contains protocol frames only, stderr bounded/redacted diagnostics. No shell command string. A local MCP process is not a sandbox and may have broad user-account access; consent and trusted executable provenance are required.

Initialize with the selected supported MCP protocol version, validate server capabilities/schemas and maintain `capabilitiesRevision`. Bound a message to 1 MiB, tool catalog to 200 tools and schema nesting to 32 levels; oversized/unparseable output degrades/fails the connection and does not reach the model as instructions. Tool schema updates invalidate pending intents/approvals. Disable server-initiated sampling, elicitation with privileged actions and arbitrary roots expansion unless separately implemented with explicit user consent and reviewed policy; server requests cannot expand privileges implicitly.

Process exit closes pending calls with known/unknown classification according to dispatch. At most two supervised restart attempts for a transient startup failure, with one/three-second backoff, only while the app is open and the original executable/config remains unchanged. Never replay an uncertain mutation on reconnect. Quit closes stdin, sends termination, then kills/reaps owned processes within the same bounded shutdown policy; a server requiring an always-on daemon is incompatible with the selected lifecycle unless the user manages it independently and connects remotely.

Remote MCP transport/auth and built-in OAuth lifecycle belong to CONNECTIONS.md/SECURITY.md. The same local broker applies read scopes, immutable requests, fresh sensitive approvals and exact-target verification regardless of transport.

## 7. Tests required before claiming tool support

- Contract table-driven tests: all names/field shapes, unknown fields, malformed UUIDs, oversized payloads, duplicate JSON keys and nonfinite coordinates rejected correctly.
- Approval digest tests: changing one recipient, text character, script artifact/hash, connector schema, target revision or scope invalidates the old approval.
- Cancellation/reentrancy test: after dispatch CAS observes a cancelled epoch, adapter call count is zero.
- Effect tests: timeout before/after external side effect, duplicate result, provider key expiration and unknown MCP outcome never produce a blind repeat.
- Boundary tests: symlink escape, hardlink write exposure, path traversal, race-replaced parent directory, private-network redirects and executable identity swap fail safely.
- Shell execution tests: no ambient secret environment, explicit args preserve spaces/metacharacters, parent crash closes supervisor, output/CPU/wall limits trigger, detached-child limitation is disclosed rather than hidden by a passing happy path.
- MCP tests: stdout pollution, schema change, malicious “approval” text, oversized response, restart during mutation and app Quit are contained.
- Authored-content tests: empty workspace → Unicode/multichunk stage → create, replace and approved run; verify exact bytes/hash and no inferred prose output. Cover null-first/gaps/changed duplicates/finish retries, MIME and per-chunk/total/envelope bounds, cross-scope attempts, cancellation before/after finish and crash cleanup. Private canaries must be absent on disk before explicit Save; Save alone never authorizes execution.
- Script binding tests: invented artifact, wrong MIME/hash, mutated execution copy and changed preview inputs produce zero spawns; a verified staged script uses only `scriptArtifactId` + `expectedSha256`.
- Native/browser tests in their dedicated docs exercise real focus, permission and extension behavior; a generic “tool returned success” assertion is insufficient.
