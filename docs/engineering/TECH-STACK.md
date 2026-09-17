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

1. Native app authenticates and registers a device; it checks OS permissions and user scopes before collecting context.
2. Backend authenticates the account/device, checks the exact role capability and entitlement, atomically reserves usage, then forwards only validated minimum context to the locked Azure deployment.
3. Native runtime receives normalized events and model tool proposals. A local trusted broker validates tool schemas, resources, current OS permission, approval and cancellation before executing anything. A model tool call is not authorization.
4. Azure never obtains the native app's Entra refresh token, connector refresh token, Stripe secret, arbitrary shell access or unrestricted filesystem access.
5. Backend bills from server-observed provider work; native estimates and tool outputs cannot mutate the usage ledger.

## Deployment configuration contract

These are logical configuration requirements, not populated environment files. Bind them once in typed startup validation; secret values come from Key Vault, never app resources or committed examples.

- Service origin and explicit allowed web origins; `heypebbi.com` is selected, not ownership-verified. No production hostname is asserted by this pack.
- Entra issuer, audience, native public-client ID, exact redirect URI allowlist and required delegated scope; trusted service identity audience and explicit metering application role are separate.
- PostgreSQL connection identity and TLS policy; Blob containers for releases and exports; Monitor destination with redaction enabled.
- Per model role: exact underlying model, exact deployment name, verified API family, operation, API version if that family requires one, resource endpoint secret/config reference, region, permission and quota. No guessed endpoint or fallback model.
- Stripe live/test mode, secret reference, webhook signing-secret reference, configured plan-to-price mapping and entitlement version; currency/allowances are explicit operator decisions.
- Budget, concurrency, request-size, retention and provider-timeout limits; startup rejects invalid combinations. Missing AI or billing inputs disable that feature, not authentication/local editing.

Read [AI-MODELS](AI-MODELS.md), [API](API.md), [SECURITY](SECURITY.md), [BILLING](BILLING.md) and [CONNECTIONS](CONNECTIONS.md) for the normative contracts.

## Operational boundaries

- TLS 1.2+ minimum, TLS 1.3 preferred; private database ingress, least-privilege managed identities, encrypted disks and backups. Network isolation is a future deployment requirement, not a claim that a private endpoint currently exists.
- Fastify validates request and response shapes against [openapi.json](openapi.json); reject unknown request properties, oversized bodies, malformed UUIDs and identifiers with suspicious whitespace rather than normalizing them. JSON currency uses integers.
- Graceful shutdown rejects new provider work, drains bounded requests, closes audio streams with retryable reason, persists metering reconciliation and releases unused reservations. A deployment restart is not a successful task completion.
- A single native task may have one active inference stream at a time. Different Pebbis can run concurrently within account/device quotas. Server shared state and reservations live in PostgreSQL; process-local state is never the sole spend authority.
- Use short-lived row leases for workers; reclaim safely after crash. Transactional outbox commits externally intended operations before dispatch. At-least-once dispatch requires stable idempotency keys and reconciliation, not a promise of exactly-once network delivery.
- Bound all upstream retries, timeouts and buffers. Never retry a model generation after uncertain dispatch as though it were free or side-effect-free; reconcile first.
- Pin an actual supported Node/TypeScript/Fastify/Azure SDK and database migration toolchain when implementing. Tests, migration dry-runs, SSE through ingress, WebSocket upgrade/drain, Key Vault access, Stripe sandbox callbacks and restore drills must run before deployment claims.

## Developer-only adapters

LiteLLM is optional on a developer's authenticated loopback interface for an explicitly selected development test. It is not installed on customer machines, not an end-user credential distributor and not the production inference path. Do not depend on Hermes, Claude Code, Codex, a paid development subscription or a local proxy being present. Test fixtures remain labeled and cannot satisfy live Azure acceptance.
