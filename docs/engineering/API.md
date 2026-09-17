# Service API and streaming contract

Status: documentation only. [CONTRACT](../CONTRACT.md) owns product vocabulary; [openapi.json](openapi.json) is OpenAPI 3.1 / JSON Schema 2020-12 and owns every REST request/response field and every decoded streaming message. This document owns protocol sequencing, authorization and invariants that structural schema cannot express. No domain, tenant, service or Azure deployment is asserted to be provisioned.

## Shared wire rules

- All Pebbi JSON uses camelCase and `schemaVersion: 1`; identifiers are opaque, case-preserved UUID strings, UTC timestamps end in `Z`, and quantities are nonnegative integers within JSON's exact integer range. Vendor Stripe IDs are opaque provider strings; the signed incoming Stripe event is an explicit vendor-owned snake_case/version exception, not a new Pebbi schema style.
- `/healthz` alone is outside `/v1`. Paths below are literal; there are no hidden conversation, file, screenshot, task-cancel or cross-device-sync endpoints. Entra authorization/token endpoints and Stripe-hosted pages are external services, not additional Pebbi routes.
- `Content-Type: application/json` for REST request bodies; successful nonstreaming bodies are JSON. `DELETE /v1/devices/{deviceId}` returns 204 without a body. Unknown request properties, invalid enum values, malformed IDs, invalid UTF-8, duplicate JSON keys, nonfinite numbers and unsafe integers are rejected before dispatch.
- General request limit: 12 MiB; non-inference JSON limit: 64 KiB, except signed Stripe events capped at 1 MiB. `/v1/ai/responses` may include at most 8 MiB of decoded selected image content in total, no remote image URLs, no more than 128 messages, 32 content blocks per message and 64 tools. Text/definition limits also apply exactly as in the schema. Decode and inspect MIME rather than trusting a label.
- `X-Request-Id` is an optional UUID, server-generated if absent and echoed in responses. It is correlation, not authorization. No request ID, path or exception log may include content or secrets.
- `Cache-Control: no-store` on all API responses, including account data and tokens. HTTP errors are JSON until a stream has started. HTTPS is mandatory outside a developer-only loopback test. Do not redirect authenticated requests to another origin.
- `Authorization: Bearer <Entra access token>` is required except public health, signed Stripe webhook, internal metering and session-token WebSocket upgrades. No cookies are needed for native API calls. If server-rendered account pages use cookies, they require Secure/HttpOnly/SameSite cookies and CSRF protection; they do not weaken the API bearer contract.
- `X-Pebbi-Device-Id` is required for app-authorized endpoints except `GET /v1/me` and `POST /v1/devices`. Validate that this registered, nonrevoked UUID belongs to the bearer account. A header alone is never a device credential. The finalizer and webhook use their own authentication and no device header.
- Required `Idempotency-Key` values are UUIDs. Optional W3C `traceparent` may be validated for telemetry only, never propagated into identity/permission decisions. Reject sensitive bearer query parameters; never log authorization, signature, cookies, session tokens or signed URLs.

## Authentication and identity

Microsoft Entra External ID is the identity authority, not a password database in Pebbi. Native sign-in uses AuthenticationServices/system browser, OIDC authorization code and PKCE `S256`; fresh cryptographic verifier, `state` and `nonce` per attempt, bounded expiry and exactly one callback consumption. Register an exact native redirect URI for bundle `com.heypebbi.app`; the actual URI/client/tenant/issuer/audience are deployment inputs, not guessed from `heypebbi.com`. No embedded web password UI and no native client secret.

The native client validates the ID token issuer/audience/signature/nonce/time and state/redirect match before associating an account. The API accepts access tokens, not ID tokens, and verifies signature using issuer-pinned discovery/JWKS, approved algorithms, configured issuer and API audience, lifetime (maximum 60-second skew), expected tenant/policy and the configured delegated API scope. It resolves the account from issuer + subject, never user-supplied email. Do not fetch token-supplied `jku` or accept a token merely because it decodes. Refresh/session material stays in Keychain; refresh is single-flight, failures require sign-in. If secure refresh rotation is supported by the configured policy, preserve the newest token atomically.

Revoked devices, deletion-pending accounts and removed entitlements are checked server-side on admission and during long streams. Device revocation takes effect immediately for new requests and within 5 seconds for active streams. Sign-out revokes the current device while online, closes streams, clears its Keychain session and disconnects local connector leases; offline sign-out clears local credentials immediately and warns that remote revocation could not yet be confirmed.

`DELETE /v1/account` requires recent verified authentication no older than 5 minutes plus `X-Pebbi-Reauth: required` and explicit typed confirmation. That header is not proof. The Entra deployment must supply a trustworthy authentication-time/step-up assertion in an API-verifiable token/policy; missing assertion fails closed with 403. Merely refreshing an access token or sending the local clock is not reauthentication. Configure and test this external identity requirement before enabling deletion.

## REST inventory

Every referenced name below is a complete component schema in [openapi.json](openapi.json). Fields without nullability/optionality there are required; no application may improvise a field or endpoint.

| Method and exact path | Request → successful response | Authorization and effect |
| --- | --- | --- |
| `GET /healthz` | no body → 200 `Health` | Public, minimal process liveness only. Never exposes model/config/database detail. |
| `GET /v1/me` | no body → 200 `Me` | App bearer; account, owned device list, entitlement summary. No registered-device header needed for bootstrap. |
| `POST /v1/devices` | `RegisterDeviceRequest` → 201 `RegisterDeviceResponse` | App bearer + idempotency. Account/installation uniqueness; platform is `macOS`. Device name is display-only. At most 50 retained device records per account; reject new registration at that limit instead of truncating `/v1/me` or silently revoking another device. |
| `DELETE /v1/devices/{deviceId}` | no body → 204 | App bearer + current device + idempotency. Target must belong to account; repeated revoke returns 204, foreign/missing ID 404. |
| `GET /v1/capabilities` | no body → 200 `Capabilities` | App bearer + device. Exactly one entry for each role, correct locked model, state, context-input support and actually verified voices/formats. |
| `POST /v1/ai/responses` | `ResponseRequest` → 200 SSE `ResponseEvent` data | App bearer + device + own reasoning reservation. No arbitrary model/provider URL field. One model call, not cloud task execution. |
| `POST /v1/voice/sessions` | `VoiceSessionRequest` → 201 `VoiceSession` | App bearer + device + conversation reservation. One-use token, only for `/v1/voice/stream`. |
| `POST /v1/dictation/sessions` | `DictationSessionRequest` → 201 `DictationSession` | App bearer + device + dictation reservation. One-use token, only for `/v1/dictation/stream`. |
| `POST /v1/usage/reservations` | `ReservationRequest` → 201 `Reservation` | App bearer + device + idempotency. Atomic bounded hold; requested counts are ceilings, never billable evidence. |
| `POST /v1/usage/reservations/{reservationId}/finalize` | `FinalizeRequest` → 200 `Finalization` | **Internal metering workload identity only**, separate audience/application role/allowlist + idempotency; public ingress blocked and app tokens rejected. |
| `GET /v1/usage` | optional `limit` 1–100 (default 50), opaque `cursor` → 200 `Usage` | App bearer + device. Current period authoritative totals plus ledger page; cursor account/filter-bound. |
| `GET /v1/billing/plans` | no body → 200 `Plans` | App bearer + device. Three plan names once each; null unconfigured price/allowance, no invented free/paid entitlements. |
| `POST /v1/billing/checkout` | `CheckoutRequest` → 201 `HostedBillingSession` | App bearer + device + idempotency; fresh `allowOnce` preview. Server chooses configured Stripe price. |
| `POST /v1/billing/portal` | `PortalRequest` → 201 `HostedBillingSession` | App bearer + device + idempotency. Own existing Stripe customer only; system browser handles changes. |
| `POST /v1/billing/webhook` | raw signed `StripeEvent` → 200 `WebhookAck` | Stripe signature, not app bearer. Signature verified on raw bytes before semantic parsing; durable inbox before acknowledgement. |
| `POST /v1/account/export` | `ExportRequest` → 202 `ExportResult` | App bearer + device + idempotency. Same key observes pending/ready/failed export; never starts another job on a poll. |
| `DELETE /v1/account` | `DeleteAccountRequest` → 202 `Deletion` | App bearer + device + idempotency + verified recent auth. Stops access and starts explicit deletion workflow. |

The two `GET` WebSocket upgrades are described below and in OpenAPI's `x-websocket` extension, not misrepresented as JSON REST operations or as OpenAI endpoints. No websocket bearer token is accepted in a URL query string or subprotocol field.

## Request semantics beyond shape

### Bootstrap, plans and capability response

Device registration uses client-generated `installationId`, not hardware serials or persistent tracking identifiers. Re-registration after revocation needs a fresh sign-in and a new device record, never resurrection of a stolen token's session. Native installation ID can remain stable within that install; server enforces active uniqueness and preserves revoked records only for the security-retention window.

A ready capability requires configured access and verified operation support; publish `verifiedAt` only for an actual successful role-specific probe, never a catalog fetch. A capability's model must match its role. Only ready, independently verified modes advertise usable formats/voice IDs. Limits are service safety budgets, not provider capacity claims. Readiness can change between discovery and dispatch; recheck at dispatch. Missing billing config returns `billingConfigured: false`, not a fake zero-cost subscription.

`Plans` lists Nest, Studio, Constellation. Each plan exposes the one configured purchasable interval/price in this contract; checkout rejects an unlisted interval. `price` and `allowance` are null until operator-approved. Amounts are integer minor units with uppercase ISO currency. `HostedBillingSession.expiresAt` uses provider evidence and may be null for a Portal link whose expiration is not returned; never fabricate it.

### Inference and tools

`ResponseRequest` includes `taskId`, `attemptId`, `pebbiId`, a unique `requestId`, reservation, `afterSequence`, bounded messages, tool definitions and an operator-clamped output ceiling. The reservation owner/account/device/task/attempt/role must all match. Client `pebbiId` and task IDs correlate local work, not an assertion of server-persisted Pebbis.

`input` accepts text, selected images, prior tool proposals and sanitized tool-result content only. The `user` role may carry text/images; `assistant` carries prior text and `toolProposal` blocks (`callId`, canonical `tool`, untrusted `arguments`); `tool` carries only `toolResult` blocks with a matching preceding proposal `callId`. Stateless continuation replays these bounded history blocks; it does not rely on a hidden server conversation or invented provider previous-response endpoint. The adapter preserves or translates opaque provider call references through the gateway correlation mapping. Reject role/content mismatches or unknown tool results. Client-provided history is untrusted context, not policy. Gateway-controlled system instructions cannot be overwritten by client roles.

The local registry validates `ToolDefinition.inputSchema` as bounded JSON Schema 2020-12, with no remote `$ref`, code-evaluating keywords or unbounded recursion. Backend validates shape and size but does not execute tools. `response.tool.proposed` is an untrusted proposal with complete parsed arguments, not a partially streamed executable object. Map gateway `tool` to native `toolName` and gateway `callId` to the opaque `providerCallRef` correlation in a `ToolProposal`; the broker creates a separate local UUID `toolCallId`. Keep this mapping for the next `ContextToolResult.callId`; never confuse Azure/provider tokens with local IDs. Only canonical local tool names from TOOLS.md are exposed; dynamic MCP tools are wrapped by `callConnectionTool`. Native broker produces an immutable validated [tool envelope](schemas/tool-envelope.schema.json), performs permission/approval/capability checks, and supplies the verified result in the next inference call with a new reservation. Never continue automatically after rejected/unknown effects.

### Errors

Nonstreaming error body is always `Error`: `schemaVersion`, `error.code`, safe `message`, `requestId`, `retryable`, nullable `retryAfterSeconds`. The schema enumerates every code. No raw Azure/Stripe/MCP error body, path, key or prompt leaks through it. Internal audit may retain the allowlisted provider error code without payload.

| HTTP | Typical codes / client behavior |
| --- | --- |
| 400 | `invalidRequest`; correct input, no retry loop. |
| 401 | `unauthenticated`; one synchronized refresh if applicable, otherwise sign-in. Include `WWW-Authenticate`. |
| 403 | `forbidden`, `approvalRequired`, `untrustedMetering`, `accountDeleting`; do not bypass. |
| 404 | `notFound`; missing and foreign-owned resources are indistinguishable. |
| 409 | `conflict`, `idempotencyConflict`, `reservationExpired`; inspect current local task state; do not create duplicate work. |
| 413 / 415 | `payloadTooLarge` / `unsupportedMediaType`; reduce/correct selected input before retry. |
| 429 | `quotaExceeded` or `rateLimited`; distinguish subscription allowance from request-rate throttling. Honor `Retry-After`. |
| 500 | `internalError`; do not expose exception stacks. |
| 502 | `providerUnavailable`; upstream response was malformed/unusable. |
| 503 | `capabilityUnavailable`, `providerUnavailable`, `billingNotConfigured`, `exportNotReady`; explain unavailable dependency; honor `Retry-After` when present. |
| 504 | `providerTimeout`; outcome may be uncertain; reconcile before dispatch retry. |

`streamInterrupted` is a streaming/disconnection error code and not a claim that a task failed safely. No undocumented HTTP 402 is used. Schema-validation failures occur before chargeable dispatch; started upstream work may still consume usage if its response fails or the user cancels.

## Idempotency and race rules

- Required on device mutations, reservations/finalization, Checkout/Portal, export and account deletion. Scope keys by account/service principal + method + exact path; hash canonical validated request bytes, including relevant path parameters, not volatile tracing headers. Reuse with different semantics returns 409 `idempotencyConflict`.
- Persist pending/committed/failed dispatch metadata before an external side effect. Concurrent same-key requests wait a bounded time or return 409 while in flight, never double-dispatch. Successful results are retained 24 hours; webhook IDs and metering uniqueness follow the longer billing policy. Authenticate before every replay.
- Replays of export intentionally return the same `exportId` with its **current** `exportState`; pending has null URL/expiry, ready has a signed URL/expiry, failed has null URL/expiry. This is observation of one job, not a second job. Poll same POST/key/body at most once every 2 seconds, exponential backoff capped at 30 seconds. The 202 response remains the same resource contract when ready. URLs expire after 15 minutes; a same-key authenticated observation may issue a new URL for the same artifact during its 24-hour lifetime. No status route is invented.
- SSE generation is not replayable. Unique `ResponseRequest.requestId` + reservation must be atomically claimed once. Reusing an already dispatched request returns 409, not a fresh generation or reconstructed stream. Keep only metadata/hash for 24 hours, never prompt/output content for replay. HTTP reconnect/resend must not charge twice behind the user's back.
- Audio token creation is deliberately not replayable: a reservation supports one pending/active session. A lost 201 response is recovered by letting its unused 60-second token expire and requesting a new reservation/session; repeated creation against the old reservation is 409. Never return the same bearer secret from an idempotency cache.
- Finalization is one charge per provider operation/reservation. End-user API calls cannot finalize, release or claim zero usage. Worker retries use the same key/evidence; conflicting values go to reconciliation, not ledger overwrite.

## SSE protocol

`POST /v1/ai/responses` uses `Accept: text/event-stream`. Validate authentication, schema, provider capability and reservation before committing HTTP 200. Until then return a normal JSON error. Once streaming starts use `Content-Type: text/event-stream; charset=utf-8`, `Cache-Control: no-store`, disabled proxy buffering/compression that delays frames, and flush each bounded frame.

Each event is framed as:

```text
id: <eventId UUID>
event: <type>
data: <one JSON object conforming to ResponseEvent>

```

There is no vendor `[DONE]` sentinel. `schemaVersion`, `eventId`, `taskId`, monotonic task-local `sequence`, `type`, UTC `occurredAt`, and `payload` are present. Send `: keepalive` comments every 15 seconds while waiting. Maximum decoded event size is 64 KiB. Bound unsent data to 256 KiB or 5 seconds, then cancel a persistently slow consumer. Engineering timeouts: first upstream output within 30 seconds, total reasoning call 300 seconds; actual supported ingress budgets must be tested and aligned.

Ordering for one call:

1. `response.started` supplies generated `responseId` and locked Astra model.
2. Zero or more `response.text.delta` and/or complete `response.tool.proposed` events.
3. Exactly one of `response.completed`, `response.cancelled`, `response.failed`, then close. Completion `usage` contains verified server quantities, or null when metering still needs reconciliation; never fabricate zero usage. `/v1/usage` remains the accounting authority. `finishReason: toolProposals` means native work is pending, not task success. `length` means truncated model output, not permission to claim completion.

The backend allocates a monotonically increasing **transport** sequence per account/device/logical task across its provider streams; `afterSequence` is the client's durable remote cursor. Start above both accepted cursor and server high-water mark, checked against the safe integer bound. Only one active provider stream per task is admitted. Counter metadata is not conversation sync. The native Store assigns its own journal sequence while preserving remote `eventId` and `sequence` as source metadata; do not interleave transport numbers into local journal primary keys. Deduplicate remote event IDs and reject regressions. An attempted new stream cannot reset the high-water mark. Cross-task ordering is not defined.

No server event replay is available: `Last-Event-ID` must not trigger provider execution or invented backfill. Closing the HTTP stream propagates abort to Azure and releases unused reservation capacity after server metering reconciliation. A user task cancel separately advances native `cancelling` → `cancelled` only after owned resources stop; the native runtime cancels all its associated transports and pending tool dispatch. The transport cannot acknowledge its own disconnect, so absent terminal event means uncertain/interrupted work, not success. Already-sent effects require target read-back before retry. A 200 alone is never model/task completion.

## WebSocket protocol

These are **Pebbi gateway protocols**, not claims about Azure wire names. Complete message schemas are `AudioClientMessage` and `AudioServerMessage` in OpenAPI; `x-websocket` associates them with the exact upgrades.

### Admission and token lifecycle

1. Reserve usage for `conversation` or `dictation`; request the corresponding session with the same task/attempt/reservation. Choose a voice/audio format only from the actually verified capability. No freeform upstream endpoint, model, codec or token is accepted.
2. Server checks account/device/scopes, role readiness, limits and reservation. It creates a CSPRNG token with at least 256 bits entropy; returns token once plus `sessionId`, same-origin relative `streamPath`, `expiresAt` (60 seconds), `subprotocol: pebbi.audio.v1`, accepted format and 600-second session maximum. Store a token digest with user/device/task/attempt/reservation/role/path binding, not the raw token. Do not cache/log the response.
3. Native URLSession opens `wss` on that origin and exact path with `Authorization: Bearer <sessionToken>`, `X-Pebbi-Device-Id`, `Sec-WebSocket-Protocol: pebbi.audio.v1` and the normal RFC 6455 upgrade headers. No app bearer or Azure key is sent as the session token. Reject query credentials, missing/wrong subprotocol, wrong role/path/device, expired/reused token and unapproved browser Origin. Native no-Origin is allowed only for the authenticated native protocol. Tokens are not conveyed in the subprotocol.
4. Atomically consume token and claim reservation before HTTP 101. Replay/concurrent upgrades lose. Failed upgrades after consumption require a new session; never relax one-use semantics. Before 101 use the normal JSON errors. An unused expired token releases its hold if there is no dispatched provider work.
5. The upgrade token's 60-second lifetime is **admission only**, not a requirement to disconnect a healthy stream after 60 seconds. Active authority is the server-side session and account/device/entitlement checks; absolute session limit is 600 seconds, plus ceiling and revocation. Never renew authority via a model message.

### Frame rules

Use UTF-8 JSON text frames only; binary frames are rejected with 1003. This deliberately avoids a second custom binary protocol. Audio is base64 PCM signed 16-bit little-endian, mono, at the negotiated sample rate (only verified 16000/24000/48000 Hz may be advertised). Server may adapt/resample only to a verified upstream format and must account from actual accepted samples. Do not claim a provider natively accepts all client formats.

Maximum frame length is 32 KiB; base64 data decodes to at most 16 KiB and an even PCM byte count. Audio chunks represent 20–100 ms each; enforce duration from bytes/rate, not a client timestamp. `clientSequence` starts at 1 and increments exactly once per client JSON message; `clientEventId` is a UUID. `audio.append` carries `utteranceId` on every input chunk, so partial transcripts before commit have an unambiguous owner. The same `utteranceId` must appear in `audio.commit`. `chunkIndex` starts at 0 and increments over the session's input chunks; output chunk indices restart per `outputId`. Gaps, conflicting duplicates, invalid IDs, wrong session IDs, out-of-state commands or malformed PCM fail closed. A same-event duplicate with identical content can be acknowledged without reconsumption; never bill a duplicate twice. No buffered audio is replayed on reconnection.

Server envelopes use the same task-local transport sequencing rule as SSE; payloads carry `sessionId`. At most one uncommitted utterance is buffered per session and at most 1 second of unacknowledged audio can be in flight. `audio.accepted` acknowledges the highest accepted client sequence, not paid usage authorization. Backpressure pauses capture; do not silently accumulate recordings. An unacknowledged buffer exceeding 5 seconds causes a retryable failure and clearing of volatile audio. Send WebSocket ping every 20 seconds; require pong within 10 seconds. Dead connections abort provider work and reconcile usage.

### Conversation sequence

```text
POST /v1/usage/reservations             role=conversation
POST /v1/voice/sessions                approved format + voice
GET /v1/voice/stream -> HTTP 101        one-use token, correct headers
client session.start                  empty payload; clientSequence=1
server session.ready                  accepted role/format
server voice.state                    listening
client audio.append ...               bounded chunks, acknowledgements
client audio.commit                   utteranceId; freezes this utterance
server voice.input.transcript         provisional/final text if verified upstream supports it
server voice.state                    thinking, then speaking
server voice.output.audio/text ...    outputId + ordered playable chunks/text
server voice.output.done              interrupted=false
server voice.state                    listening
client session.stop                   stop after committed work drains, bounded 5 seconds
server session.closed                 reason=completed; WebSocket 1000
```

`session.start` must arrive within 5 seconds; otherwise close 1008. `audio.commit` ends the utterance and requests the upstream response using its verified protocol. Do not invent a transcript when the provider supplies only audio; lack of verified transcript support cannot masquerade as a final transcript for task execution. Voice intent requiring tools is handed to the native task coordinator and Astra; streamed audio never runs tools directly.

For barge-in, the client stops playback immediately and sends `response.interrupt {outputId}`. Server cancels/truncates only that audio response using supported upstream behavior, drops future chunks for it, emits `voice.output.done {interrupted:true}` and `voice.state: interrupted`, then returns to `listening`. If upstream truncation is unavailable, stop that upstream response/session honestly rather than pretend interruption synchronized history. This does **not** cancel an associated agent task. Late audio cannot resume playback after the output ID is cancelled. `response.interrupt` is rejected on dictation sessions.

### Pebbi context and speaking verified task results

`VoiceSessionRequest.contextSummary` carries only the selected Pebbi/job/memory/conversation summary (maximum 16,000 characters; empty allowed), not system policy or credentials. Gateway-owned safety instructions remain separate. A ready full-product conversation capability requires independently verified `supportsContextInput`; missing text/context input support is a capability gate, never a claimed workaround through another model.

While the conversation is `listening` with no uncommitted utterance or output, the native app may send `conversation.context` with a strictly increasing session-local `revision`, bounded `text`, nullable `sourceTaskId`/`sourceAttemptId`, and `speak`. The server acknowledges `conversation.context.accepted` after the verified upstream operation accepts it. Context changes affect only subsequent responses and never mutate an in-flight utterance. `speak:false` refreshes selected context without unsolicited speech. `speak:true` requires the native coordinator's verified task/attempt result references and asks the selected conversation model to speak that result; normal `voice.state` and output events follow. The backend checks shape/session capability, while native trusted records establish actual tool verification. A caller's text alone is not proof a task succeeded.

Screen images stay on the Astra reasoning path. Its verified explanation/result can be supplied through this context message for speech; do not send unrelated raw screenshots to the conversation session or install a substitute TTS model. Typed tasks likewise use Astra; speaking a result does not repeat its tools or change task state. `conversation.context` is rejected for dictation and when its capability is unavailable. No context transcript is retained server-side after session end.

### Dictation sequence

```text
POST /v1/usage/reservations             role=dictation
POST /v1/dictation/sessions             format + nullable languageHint
GET /v1/dictation/stream -> HTTP 101    one-use token
client session.start
server session.ready
native state capturing
client audio.append ...
server dictation.state                 transcribing when provider starts
server dictation.transcript.partial    replacement draft, never inserted
client audio.commit                   utteranceId
server dictation.transcript.final     entire final utterance text
client session.stop
server session.closed                 reason=completed; WebSocket 1000
native reviewing -> inserting -> completed, only after current focus check
```

Use one utterance per dictation session. Partial text replaces the current draft rather than appending duplicate hypotheses; only a final transcript closes the utterance. Backend never emits `inserting` or local `completed` as evidence that another app changed. Those transitions and exact-target verification belong to the Mac. A no-final close is a failure, not an empty successful transcription. Dictation `capturing`, `reviewing`, `inserting` and `completed` are local UI states; server `dictation.state` is limited to `transcribing` or `failed` despite sharing the canonical enum.

### Stop, cancel, close and recovery

`session.stop` stops accepting new input; it drains only already committed work for at most 5 seconds, never commits an uncommitted utterance implicitly. Discard uncommitted audio. A dictation final not received before drain timeout is failed, not complete. `session.cancel` immediately stops recording/playback/transcription and clears volatile buffers; reason `taskCancelled` is sent only when the native task was explicitly cancelled. `session.cancel` does not claim externally executed tools were undone. Sleep, quit, device change or account revocation stops capture and closes authority; no hidden audio reconnection or microphone restart after Quit.

Server sends `session.error` with a sanitized `Error`, then `session.closed` when transport permits. Close codes: 1000 normal completion/cancel; 1008 protocol/authorization/session-expiry violation; 1009 oversized frame; 1011 provider/internal failure; 1012 controlled service restart; 1013 temporary overload/quota. Close reasons are short safe codes, no content. Quota exhaustion or provider disconnect preserves local review text, rejects new work and reconciles consumed usage. Native state becomes canonical `unavailable`/`failed` for voice or `failed` for dictation; never a synthetic success.

Reconnect creates a new reservation/session/token after the old session has stopped/reconciled or expired. It does not resume audio, repeat committed utterances, resurrect an attempt or replay tools. The user can explicitly retry with a new attempt linked to the logical task. Transport success and useful audio/transcription success are independently tested.

## Export, deletion and privacy

`POST /v1/account/export` includes server-held account, devices, entitlement and usage information only. It excludes provider secrets, connector tokens, other users' data and raw local conversations/files/screens. The native app combines that artifact with a separately consented local export; `includesLocalData` remains false for the server result. Download URLs are read-only, object-scoped, short-lived and never logged. Pending/failed/ready schema combinations are validated semantically.

`DELETE /v1/account` atomically marks deletion pending, revokes device/session admission, blocks new billing/model work, and enqueues subscription cancellation and deletion. Return server deadlines: active eligible data within 30 days, backup expiry no later than 35 days after active deletion. Legal billing-retention exceptions are disclosed before confirmation; raw model content was never retained as account history. Current-device local erasure is separately verified by the app; other offline Macs and user-created exports cannot be remotely erased by this contract. See [SECURITY](SECURITY.md) and [BILLING](BILLING.md).

## Required contract verification

Validate OpenAPI structurally and every JSON Schema with a 2020-12 validator. Compare the 17 REST operations and two WebSocket upgrades with CONTRACT, including `/healthz` exception. Generate/hand-check Swift and TypeScript models against these schemas, not provider DTOs. Exercise authentication negatives, unknown fields, cross-account IDs, token replay, wrong-role upgrades, frame sequencing, cancellation races, export observation, Stripe replay and workload-only finalization. Documentation/schema checks are not live Azure, Stripe, Mac permission or deployment acceptance.

Run from repository root (validation only, no provisioning or application code):

```sh
uvx --from openapi-spec-validator python -c 'import json; from openapi_spec_validator import validate; from jsonschema import Draft202012Validator; o=json.load(open("docs/engineering/openapi.json")); t=json.load(open("docs/engineering/schemas/tool-envelope.schema.json")); validate(o); Draft202012Validator.check_schema(t); [Draft202012Validator.check_schema(s) for s in o["components"]["schemas"].values()]; print("OpenAPI and JSON Schemas valid; no live integration tested")'
```

A schema validator cannot prove approval provenance, token revocation, state-machine ordering, quota arithmetic, SSRF protection or exact-target read-back. Those remain required implementation tests, including negative and race cases above.
