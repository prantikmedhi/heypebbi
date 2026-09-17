# Accepted integration review resolutions

> **HISTORICAL REFERENCE — SUPERSEDED SCOPE.** The current decision is [local Azure onboarding](../product/LOCAL-AZURE-ONBOARDING.md), docs only until implementation is resumed. This earlier managed/full-product design is preserved as reference, not an instruction to implement its hosted services, login, billing, fixed models or full PB scope. Current requirements take precedence.

These are accepted clarifications to the initial specification, not a staged product plan. They close implementability gaps found during independent documentation review. [CONTRACT.md](../CONTRACT.md) remains the scope authority; this document defines the refinements that the owning engineering/product documents and schemas must express consistently.

## Device authorization

`X-Pebbi-Device-Id` is public identification, not proof. Enroll a separate CSPRNG backend-issued opaque device credential with at least 256 bits of entropy; store only a digest server-side and the secret in the native Keychain. Return it through `RegisterDeviceResponse.deviceToken` once. Require `X-Pebbi-Device-Token` alongside the account access token and matching device ID for every device-bound REST endpoint, including audio token minting. WebSocket session tokens are already device/role-bound and do not expose/reuse the device credential.

Registration requires server-verifiable recent interactive authentication, not refreshed token issue time or a client assertion. The approved bootstrap route `POST /v1/devices/enrollments` creates an account/installation-bound, single-use nonce challenge. Native code uses ordinary Entra OIDC authorization-code + PKCE with this nonce and fresh interactive authentication. Registration submits the resulting signed native-client-audience ID token as narrowly scoped enrollment proof; it is never accepted as a generic API bearer. The backend checks signed nonce against the stored challenge, identity against the separate account access token, expiry, one-use state and configured signed `auth_time`. Do not invent an Entra enrollment-only JWT issuer or special purpose/installation claims; the backend challenge supplies that binding.

Revocation advances the account security `enrollmentNotBefore` threshold; enrollment authentication time must be later than the prior threshold. An old bearer cannot change its device ID or mint a replacement merely by changing installationId. Define lost-response/idempotency behavior without replaying secrets from an ordinary response cache. Fresh challenge-bound interactive proof plus explicit native replacement review may replace the same owned installation, with atomic old-credential revocation and new issuance, so losing the sole device credential does not require another device forever. Exact lifecycle/error behavior belongs in API/SECURITY/OpenAPI. Missing configured signed authentication-time evidence remains a normal explicit OIDC freshness gate, not a reason to weaken binding.

## Authored artifact production

Add exactly one canonical local tool, **`stageTextArtifact`**, to TOOLS and both local-tool name enums. It stages explicitly structured model-authored UTF-8 content; ordinary assistant prose is never implicitly a file or executable.

Closed input schema: `workspaceId` UUID; `draftId` nullable UUID (null only for first chunk); `chunkIndex` nonnegative integer; `text` UTF-8 text limited to 32 KiB encoded bytes per chunk; `mimeType` from a documented text-only allowlist; `final` boolean. Model arguments remain within the existing 64 KiB envelope budget. A broker-created draft is scoped to account, Pebbi, originating task/attempt and authorized workspace. Chunks must be contiguous and immutable under retry, with a maximum of 4 MiB total staged UTF-8 text. Cross-scope draft reuse, changed duplicate chunks and unsupported MIME fail closed. No file in the user's target workspace is modified by staging.

Output: `draftId`, `nextChunkIndex`; finalization additionally returns immutable `artifactId`, exact UTF-8 `byteCount`, `sha256` and `mimeType`. Those native-produced values, not invented model IDs, supply createFile/replaceFile/runCode. Cancellation cleans staged drafts; private-mode drafts/artifacts stay in RAM until explicit Save consent. Persist no private text/hash in the metadata-only journal. Appropriate generated binary/document conversion can use the separately approved code tool; staging is not an arbitrary base64 upload or execution capability.

For `runCode`, remove the unbound `scriptVersionId`. Use immutable **`scriptArtifactId` plus `expectedSha256`**, verified against actual same-account/workspace artifact bytes. The approval digest covers those bytes and the execution inputs. File lineage can remain in normal file-version metadata; do not invent a second script-version entity.

## Audio accounting owners separate from task execution

Create native `audio_operations` and `audio_event_receipts` aggregates independent of queued agent tasks. Each audio operation owns `audioOperationId` and `audioAttemptId` UUIDs, account/device/Pebbi/conversation references, role, reservation, volatile session handle, transport cursor and lifecycle. It does not consume the Pebbi's serial task execution slot.

The existing gateway wire fields remain `taskId`/`attemptId` to avoid contradictory streaming envelopes: for voice/dictation only, they explicitly carry **audioOperationId/audioAttemptId**, not a queued agent task's IDs. For reasoning they retain actual task/attempt IDs. Native adapters must map this by immutable reservation role/owner kind and must never insert audio receipts into agent-task tables with incorrect foreign keys. Server reservations bind owner identity and role and reject reuse of one owner ID across incompatible roles. One provider stream per owning operation remains the rule; it does not block an independent audio session while an agent task reasons.

`sourceTaskId`/`sourceAttemptId` in conversation context retain provenance of the real agent result being spoken; they are not the audio owner. Audio stop/interrupt does not cancel that task. Crashes close/interrupt audio ownership; audio is never replayed automatically. One device microphone lease prevents accidental simultaneous competing capture; dictation may coexist with a running agent task and may explicitly pause/replace a voice input session without occupying the task queue. Native/data/runtime/API/quality documents must include the complete handoff and stop scenario.

## UTF-8 WebSocket limits

Define limits on **reassembled JSON messages**, not character counts or an assumed single frame. All decoded text/control/transcript/context messages are capped at **256 KiB UTF-8 serialized bytes including envelope**. Audio append/output messages keep their tighter **32 KiB serialized message** and **16 KiB decoded audio** caps. Transport libraries may fragment messages; receivers bound individual frames and cumulative reassembly without relying on fragmentation to bypass the message cap. No code point is split or final transcript silently truncated.

The existing 16,000-character context and 32,000-character final transcript ceilings are character bounds, not permission to exceed the serialized-byte cap. Encoders should emit non-ASCII Unicode directly as UTF-8 and must bound the complete serialized envelope; decoders also reject escape-heavy messages that exceed the byte cap. Oversize content results in explicit failure/review-preserved text; never report a partial final as a complete utterance. Update advertised limits and schema descriptions accordingly. Test ASCII, CJK, emoji, escape-heavy strings and fragmented input.

## Context-budget delivery

Expose a typed role capability `tokenBudget` with deployment-verified provider context capacity, operator max input/output budgets, estimator identity/version and evidence time. Provider capacity is distinct from operator clamps. The implementation must specify exact nullable/unavailable behavior; reasoning readiness requires sufficient verified budgeting information. Do not guess context size from a model name or pretend a client can read backend-only settings.

Native compaction uses the delivered safe budget and documented estimator. Account for tool schemas, instructions, history, attachment/image estimates and reserved output. A context-limit response invalidates/reduces stale capability budgets and produces an explicit recoverable path, not silent instruction or evidence deletion.

## Product authority clarifications

- Voice may select a low-risk suggestion, request a task or open its review. Protected-effect `allowOnce`/`allowForScope` requires a deliberate accessible native approval control with exact preview. Model text or even an unambiguous transcript is not protected-action consent.
- Dictation cancellation before insertion dispatch makes no target edit. Cancellation racing an already admitted insertion stops further work and reconciles the admitted effect; preserve inserted/unchanged/unknown outcome in a receipt. Never automatically undo across a user's concurrent edit or claim nothing happened without evidence.
- Release documentation defines one complete-product readiness decision, pre-release verification, post-release monitoring and withdrawal/rollback. It does not require cohort promotion or a staged public rollout.

## Verification of the repairs

Structural schema checks alone cannot prove these behaviors. Add explicit acceptance/contract tests for stolen bearer plus different device ID, revoked enrollment replay, authored file/script from an empty workspace, chunk replay/scope/privacy, concurrent voice plus reasoning, standalone dictation while a Pebbi task waits, multibyte/fragmented message bounds, missing/changed token budgets, spoken protected consent rejection and cancellation after insertion dispatch.
