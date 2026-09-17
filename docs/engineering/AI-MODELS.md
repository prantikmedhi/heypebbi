# Locked AI roles and Azure evidence

Authority: [CONTRACT](../CONTRACT.md). Status: target architecture and sanitized evidence summary, not a live Pebbi deployment. This documentation-only task did not run new tenant inference or modify client/provider configuration.

## Exactly three role assignments

| Role | Locked model identifier | Intended use | Non-negotiable boundary |
| --- | --- | --- | --- |
| `conversation` | `gpt-realtime-2.1` | Low-latency spoken conversation, native interruption and speech output | Do not substitute another realtime model, standalone TTS pipeline or vendor when unavailable. Typed conversation uses the separately selected Astra reasoning path and is labeled as such, not a passing realtime test. |
| `dictation` | `gpt-live-transcribe` | Streaming speech transcription, partial/final transcript and reviewed insertion | Never bill or claim success from session configuration alone. No silent operating-system or other-model transcription substitute. |
| `reasoning` | `gpt-6-astra` | Text/vision reasoning, screen analysis, tool planning, research and code generation | Native broker executes tools after checks; the model itself has no permission to control a Mac. |

A role's model identifier is not necessarily an Azure deployment name. Keep both fields separately. An operator may map a differently named deployment only after proving it serves the same locked model; changing the underlying model requires an explicit product decision, never an automatic fallback. Catalog discovery, deployment discovery, operation acceptance and useful generated output are four different checks.

## Actual authorized audit — 2026-09-17

The following is the sanitized audit supplied by the canonical contract. It is not inferred from marketing pages or recreated with fixtures.

| Check | Actual result | What it establishes / does not establish |
| --- | --- | --- |
| Astra through Azure directly | **Passed** | Actual generation worked with the authorized resource and selected deployment at audit time. This is not proof that future production credentials exist. |
| Astra through an existing private LiteLLM proxy | **Passed** | The existing developer adapter could reach Astra; the proxy is not a Pebbi runtime dependency. |
| `gpt-realtime-2.1`, tested v1 operation | **Failed: HTTP 400 `OperationNotSupported`** | The requested realtime operation was not supported through the tested route/deployment. A visible catalog row is not a working audio session. |
| `gpt-realtime-2.1`, documented classic-preview operation | **Failed: HTTP 400 `OpperationNotSupported`** | Preserve the provider's actual misspelling. Do not rewrite it to imply both payloads were identical. Trying the documented alternative did not establish support. |
| `gpt-live-transcribe` configuration | **Configuration accepted** | A session accepted its configuration; that is not transcription. |
| `gpt-live-transcribe` actual synthetic-audio transcription | **Failed: `DeploymentNotFound`** | Actual transcription did not work through the tested deployment name. No live dictation pass exists. |
| Catalog lifecycle metadata | Realtime 2.1: preview; live-transcribe: generally available | Resource catalog metadata at audit time, not a guarantee of region, tenant, operation or deployment availability. Public pages may disagree. |

The user deferred resolving missing Azure inputs. Do not repeatedly ask for them during unrelated implementation. Implement validated interfaces, fail-closed states and tests; record the live audio gates as blocked. Do not copy private resource endpoints, keys, resource names, transcripts, raw audit output or developer-local audit paths into this repository. No fixture, mocked transport, accepted config, screenshot, catalog lookup or fabricated response counts as a live provider pass. No additional streaming, vision, latency or tool-round-trip result is claimed unless independently measured.

## Endpoint and capability discipline

Pebbi's own `/v1/ai/responses`, `/v1/voice/sessions` and `/v1/dictation/sessions` are product endpoints, not claims that Azure/OpenAI exposes the same routes. Their [wire protocols](API.md) terminate at Pebbi's gateway. Gateway adapters translate to an operation verified against the actual deployment.

- Azure OpenAI v1, classic dated Azure APIs, Foundry `/models`, and Foundry project endpoints are distinct API families. Do not transform one into another based on a hostname or append a guessed operation.
- For a verified Responses deployment, use its documented Responses transport. Preserve the exact supplied deployment identifier and any required classic API version. A v1 base does not itself require a dated `api-version` parameter.
- Realtime conversation and streaming transcription each require a currently documented, resource-supported operation and protocol. Do not invent `/sessions`, `/realtime`, `/transcriptions` or a deployment path in an SDK merely because another provider offers it. Capture the exact operation in private deployment configuration only after verification.
- Key-based or managed-identity authentication must match the actual operation. Prefer least-privilege managed identity where supported; otherwise retrieve the narrow Azure key from Key Vault. Never transmit it to the Mac, browser extension or user-visible logs.
- Disable unsupported parameters instead of claiming the model implements them. Context length, maximum output, tools, vision, sampling, reasoning levels, audio format, voice identifiers and pricing require deployment-specific verification. Operator safety budgets are not model capacity claims.
- Keep startup capability state `disconnected` when credentials/deployment inputs are absent; attempted provider failure becomes `failed` or `degraded` with safe reason. Never expose a ready capability merely because a configuration string is nonempty.

## Native and backend flow

1. The native app requests `/v1/capabilities`. It checks connection state, allowed voices/audio formats and service limits rather than shipping a hardcoded list of invented provider voices.
2. A trusted gateway verifies device, scope, configured entitlement and a bounded reservation before a provider call or issuing a single-purpose audio-session token.
3. Screen/file context is explicitly selected, minimized, converted locally, and transmitted only for that request. No server conversation synchronization or implicit file upload service exists.
4. Astra receives bounded context plus allowlisted tool definitions/results, never connector credentials or executable authority. Tool arguments are untrusted proposals. Follow [tool-envelope.schema.json](schemas/tool-envelope.schema.json) and the native tool broker.
5. Conversation uses the selected realtime deployment's native speech capabilities only after a real audio round trip succeeds. Do not invoke standalone dictation on every conversation turn by default.
6. Dictation uses its own locked role and protocol. Partial text is provisional; only final text may be reviewed and inserted after rechecking focus. Recognized text is not permission to execute its contents.
7. Provider usage and completion are recorded server-side. Native task completion still requires verified task/tool effects, not merely a model's success sentence.

## Failure and release gates

Voice state `unavailable` explains a disabled conversation capability; the corresponding connection remains `disconnected`, `failed` or `degraded` as appropriate. Dictation uses its canonical `failed` state on attempted unsupported capture/transcription and keeps review/manual typing available. Do not invent a dictation `unavailable` state. A blocked tool task uses `waitingForConnection`, not fake progress.

Required independent evidence before each feature is called live:

- Exact deployment and operation identified; intended model confirmed; bounded direct request produces useful output with no fallback.
- Native → authenticated Pebbi backend → Azure round trip succeeds, including identity, quota and metering. Realtime context input and speaking a verified Astra task result are separate required checks; capability flags must reflect actual support.
- Astra text streaming, real image understanding and harmless tool-result round trip tested separately; audio conversation actually hears input and returns playable output; dictation produces correct final text from actual audio.
- Cancellation, speech interruption, quota exhaustion, missing deployment, revoked device, reconnect, partial delivery, ingress draining and provider timeout produce canonical states; buffers remain bounded.
- Usage reconciliation and privacy/retention are tested; synthetic fixtures are reported separately. Three-role live acceptance stays blocked until the two audio deployments are resolved.

## First-party implementation references

These are reference entry points to recheck when implementing, not new proof of tenant access or an assertion that a particular audio endpoint exists:

- [Azure Responses API](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/responses)
- [Azure endpoint and deployment differences](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/switching-endpoints)
- [Azure realtime audio documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/realtime-audio)
- [Entra native authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)

Follow the actual authorized deployment's current documentation and sample. If unavailable, keep the adapter disabled and report the missing input; do not silently choose a substitute.
