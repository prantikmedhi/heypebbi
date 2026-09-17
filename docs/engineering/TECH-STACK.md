# Backend technology and deployment contract

Status: specification only; no service, cloud resource, credentials or production deployment is created here. [CONTRACT](../CONTRACT.md) takes precedence. Target: the complete Pebbi product, not a smaller backend demonstration.

## Fixed implementation choices

| Boundary | Required implementation | Reason / limit |
| --- | --- | --- |
| HTTPS, SSE and WebSocket gateway | Node.js 24 LTS; strict TypeScript; Fastify 5 | One long-running service; no separate Python inference service or short-duration function for audio. Pin supported patch versions and lock dependencies at implementation. |
| Durable server metadata | PostgreSQL 17 on Azure Database for PostgreSQL; versioned SQL migrations | Accounts, devices, entitlements, usage reservations/ledger, idempotency records, webhook inbox and export/deletion jobs. Use transactions and constraints, not a second queue service by default. |
| Hosting | Azure Container Apps | Explicit ingress, WebSocket/SSE idle limits, graceful draining, quotas and private resource access must be verified on the real deployment. No promise that default ingress timeouts suffice. |
| Artifacts | Azure Blob Storage | Signed releases and short-lived account export artifacts only; not a conversation/file/screenshot sync store. |
| Secrets / authority | Key Vault and managed identity | Separate app, migration and release identities. Azure model keys, if needed by the verified operation, stay server-side. |
| Observability | Azure Monitor with allowlisted, redacted structured records | Metadata and latency, not prompt, screen, audio, access-token or connector-token logging. |
| Identity | Entra External ID, OIDC authorization-code + PKCE S256 | System browser sign-in, no embedded credential form, no native client secret. |
| Payments | Stripe hosted Checkout and Customer Portal | Server creates sessions from configured price IDs; signed webhook + reconciliation establishes entitlements. |
| Native runtime | Swift 6 actors / async-await; SwiftUI + AppKit; local SQLite via GRDB | Native app owns Pebbis, tasks, memory, files, permissions and tools. Backend is not a cloud desktop-control agent. |
| Infrastructure source | Bicep, when later authorized | Documentation work does not authorize provisioning, charges, signing, DNS changes or paid resources. |
| Public pages | Server-rendered Fastify pages | Support, privacy, download and account surfaces; no React framework merely to render these pages. |

Use the smallest coherent runtime: gateway process plus a worker mode of the same codebase for webhook reconciliation, expired reservations, account export and deletion. PostgreSQL transactional outbox / row leases are adequate initially; do not introduce Kafka, Redis, vector databases or an agent framework without a demonstrated requirement. Durable workers must not execute local routines: routines stop when Pebbi quits.

## Separation of responsibilities

1. Native app authenticates the API bearer, creates `/v1/devices/enrollments`, then uses its nonce in ordinary Entra auth-code + PKCE with `prompt=login` and configured signed `auth_time`; it registers using the scoped native-client-audience ID-token body proof, never an ID-token API bearer; it saves the single-return device credential in Keychain and confirms it by authenticated REST use before the 300-second deadline. It checks OS permissions and user scopes before collecting context.
2. Backend authenticates account bearer AND matching device ID/credential digest, checks the exact role capability (including delivered verified token budgets) and entitlement, atomically reserves usage, then forwards only validated minimum context to the locked Azure deployment.
3. Native runtime receives normalized events and model tool proposals. A local trusted broker validates tool schemas, resources, current OS permission, approval and cancellation before executing anything. A model tool call is not authorization.
4. Azure never obtains the native app's Entra refresh token, connector refresh token, Stripe secret, arbitrary shell access or unrestricted filesystem access.
5. Backend bills from server-observed provider work; native estimates and tool outputs cannot mutate the usage ledger.

## Deployment configuration contract

These are logical configuration requirements, not populated environment files. Bind them once in typed startup validation; secret values come from Key Vault, never app resources or committed examples.

- Service origin and explicit allowed web origins; `heypebbi.com` is selected, not ownership-verified. No production hostname is asserted by this pack.
- Entra issuer, API audience, native public-client ID, exact redirect URI allowlist and required delegated scope; trusted service identity audience and explicit metering application role are separate. Enrollment uses the same approved Entra OIDC authority and ordinary native-client-audience ID tokens, not a new enrollment assertion issuer/audience or custom claims. Configure and verify signed `auth_time`, nonce round-trip, `prompt=login` freshness, timestamp precision and canonical cross-audience account mapping using pinned issuer/tenant + immutable signed `oid`, with matching signed `tid` where provided. Reject absent/unconfigured immutable mapping; `sub` stays token/audience-specific metadata and email/name are never keys. Use `max_age` only if verified supported. API/OpenAPI own the exact server challenge and proof checks; [external inputs](../operations/EXTERNAL-INPUTS.md) retain the actual deployment gates. Missing verified support/mapping disables enrollment (`enrollmentUnavailable`), not a fallback to bearer-only registration.
- PostgreSQL connection identity and TLS policy; Blob containers for releases and exports; Monitor destination with redaction enabled.
- PostgreSQL account identity ledger maps a unique `(pinnedIssuer, verifiedTenant, oid)` to the opaque Pebbi `accountId`; verify signed `tid` equals that tenant when present. Store only necessary verified immutable identifiers, not tokens or full claims. `sub` may be token/audience-specific metadata but is not a cross-client account key. No email/name auto-linking or missing-`oid` fallback; an absent/unconfigured immutable mapping fails closed. Native receives the backend `accountId` and caches that opaque value, not a locally derived subject key. Request OIDC `openid profile` for the native proof and verify required claims on actual tokens before enabling enrollment.
- Per model role: exact underlying model, exact deployment name, verified API family, operation, API version if that family requires one, resource endpoint secret/config reference, region, permission and quota. No guessed endpoint or fallback model.
- Stripe live/test mode, secret reference, webhook signing-secret reference, configured plan-to-price mapping and entitlement version; currency/allowances are explicit operator decisions.
- Budget, concurrency, request-size, retention and provider-timeout limits; startup rejects invalid combinations. Per-role capability `tokenBudget` delivers verified provider capacity, distinct operator input/output clamps, compatible estimator ID/version/kind, hidden-instruction overhead, per-image bound, budget revision and evidence expiry. No verified budget means no ready reasoning or invented context length. Missing AI or billing inputs disable that feature, not existing authentication/local editing. Missing verified OIDC nonce/auth_time/account-mapping support disables enrollment and credential replacement.
- Account/installation-bound enrollment challenge nonce hashes, 300-second expiry/one-use consumption, bounded creation/completion counters, device digests, pending-confirmation expiry and account-lifetime `enrollmentNotBefore` are shared transactional PostgreSQL authority, not per-process caches. Revoke/enroll/admission and explicitly reviewed same-installation replacement serialize; replacement atomically revokes old/creates new credentials without requiring another working device. Security thresholds survive restore. Never cache raw challenge nonce, enrollment ID token or registration/session response bodies; challenge rows expire/purge per SECURITY.
- WebSocket ingress/data-frame payload maximum 32 KiB; reassembled UTF-8 JSON text/control messages 256 KiB, audio JSON 32 KiB and decoded PCM 16 KiB. Disable permessage-deflate; enforce cumulative limits before allocation/parse, not character counts or one-frame assumptions.

Read [AI-MODELS](AI-MODELS.md), [API](API.md), [SECURITY](SECURITY.md), [BILLING](BILLING.md) and [CONNECTIONS](CONNECTIONS.md) for the normative contracts.

## Operational boundaries

- TLS 1.2+ minimum, TLS 1.3 preferred; private database ingress, least-privilege managed identities, encrypted disks and backups. Network isolation is a future deployment requirement, not a claim that a private endpoint currently exists.
- Fastify validates request and response shapes against [openapi.json](openapi.json); reject unknown request properties, oversized bodies, malformed UUIDs and identifiers with suspicious whitespace rather than normalizing them. JSON currency uses integers.
- Graceful shutdown rejects new provider work, drains bounded requests, closes audio streams with retryable reason, persists metering reconciliation and releases unused reservations. A deployment restart is not a successful task completion.
- A single agent task owner may have one active reasoning stream; independent audio operation owners may run concurrently without consuming that Pebbi's task slot. Audio wire `taskId`/`attemptId` alias `audioOperationId`/`audioAttemptId`, fixed by reservation role; cursor/receipt ownership never aliases agent foreign keys. One provider stream per owner and separate audio/reasoning quotas remain enforced, while native holds one device microphone lease. Different Pebbis can run concurrently within account/device quotas. Server shared state and reservations live in PostgreSQL; process-local state is never the sole spend authority.
- Use short-lived row leases for workers; reclaim safely after crash. Transactional outbox commits externally intended operations before dispatch. At-least-once dispatch requires stable idempotency keys and reconciliation, not a promise of exactly-once network delivery.
- Bound all upstream retries, timeouts and buffers. Never retry a model generation after uncertain dispatch as though it were free or side-effect-free; reconcile first.
- Pin an actual supported Node/TypeScript/Fastify/Azure SDK and database migration toolchain when implementing. Tests, migration dry-runs, SSE through ingress, WebSocket upgrade/drain, Key Vault access, Stripe sandbox callbacks and restore drills must run before deployment claims.

## Developer-only adapters

LiteLLM is optional on a developer's authenticated loopback interface for an explicitly selected development test. It is not installed on customer machines, not an end-user credential distributor and not the production inference path. Do not depend on Hermes, Claude Code, Codex, a paid development subscription or a local proxy being present. Test fixtures remain labeled and cannot satisfy live Azure acceptance.
