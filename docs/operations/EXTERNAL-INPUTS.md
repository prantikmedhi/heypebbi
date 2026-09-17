# External inputs and explicit blockers

Status: **documentation-only input register**. No cloud infrastructure, app registration, Stripe product, signing key, domain, deployment or paid resource is provisioned by this pack. This register records what a later implementation needs, what is known and what must remain disconnected until verified. [CONTRACT](../CONTRACT.md) is the source of the limited provider audit facts below.

An input is not verified merely because a name appears in a catalog, a secret exists, an OAuth dialog opens or a model accepts session configuration. The correct evidence is an authorized end-to-end operation on the intended account/deployment/route, plus relevant negative behavior. Do not include private endpoints, resource names, keys, raw transcripts or audit files in this repository.

## Input state machine

- **MISSING:** required input has not been supplied or validated; implementation can prepare adapters/tests but dependent live work is BLOCKED.
- **USER-DEFERRED:** the user explicitly chose not to resolve it now. Do not repeatedly request it, deploy a replacement or silently switch providers. Continue unrelated unblocked work; retain the exact blocked gate.
- **SUPPLIED-UNVERIFIED:** securely supplied with scope/authorization, but no valid operation on the intended path is recorded.
- **VERIFIED-FOR-SCOPE:** a named authorized verifier records successful and negative tests, account/deployment/config version and scope. This does not verify other routes, modalities or production readiness.
- **INVALIDATED:** revoked, expired or materially changed; affected capabilities disconnect and gates return to BLOCKED until reverified.

Audit provenance and release readiness are separate axes. An input can have limited historical working evidence and still be MISSING/SUPPLIED-UNVERIFIED for Pebbi production. All live release gates are **BLOCKED until actual inputs and candidate behavior are verified**.

## Selected AI roles: known evidence and required action

| Role | Locked model | Known authorized audit, 2026-09-17 | Input state / production consequence |
| --- | --- | --- | --- |
| Reasoning, screen analysis, orchestration, coding/research | `gpt-6-astra` | Verified working directly through Azure and through an existing private LiteLLM proxy. | **AUDITED WORKING IN LIMITED CONTEXT**, not production readiness. Pebbi's authenticated backend, Responses/tools, streaming, safety, metering, quotas and latency still require LG-AI. Production route authorization/configuration is not established by this audit. |
| Real-time spoken conversation | `gpt-realtime-2.1` | Catalog-visible; resource metadata marked preview. HTTP 400 `OperationNotSupported` on v1 and `OpperationNotSupported` on the documented classic-preview route. | **USER-DEFERRED; LG-VOICE BLOCKED.** Preserve both error spellings as observed; do not normalize them into a different source fact. No working bidirectional audio deployment was verified. |
| Streaming dictation | `gpt-live-transcribe` | Catalog-visible; resource metadata marked generally available. Session configuration accepted, but actual synthetic-audio transcription returned `DeploymentNotFound`. | **USER-DEFERRED; LG-DICTATION BLOCKED.** Configuration acceptance is not transcription. No successful actual audio transcription was verified on the tested name. |

Public documentation/catalogs may differ from resource metadata. Verify the actual selected deployment, modality/API support, region/lifecycle and resource access again when implementation is authorized. No silent model substitutions. Standalone transcription/TTS must not be invoked redundantly for every native speech-to-speech turn without an explicit revised architecture decision.

To clear a voice blocker after the user chooses to provide it: receive authorized deployment/region/API access securely; verify session authentication and actual audio input/output; test interruption, disconnect, quota and device behavior through Pebbi's backend; record private evidence reference and gate result. Do not ask for secrets in chat or commit them. Do not treat developer localhost LiteLLM as the app's production gateway. Optional development adapters/fixtures must stay visibly labeled and never clear a live gate.

## Required external-input inventory

Each item names required evidence and a release blocker rather than fabricating a value. Role owners below must later be assigned explicitly.

| Input | Securely supplied decision/data | Required verification | Present state / blocked gates |
| --- | --- | --- | --- |
| Azure subscription/resource authority | Authorized subscription, tenant/resource access scope, allowed regions, budget/cost approval and deployment authority. | Confirm least-privilege ability for the intended environment and explicit approval before any billable provisioning. | MISSING/UNVERIFIED; all Azure-dependent live gates BLOCKED. |
| Astra production route | Authorized selected deployment, API/modality support, quota and credentials/managed identity route. | Actual `gpt-6-astra` work through authenticated Pebbi backend, tool/screen/file/stream flows and metering; no private endpoint in public evidence. | Limited audit only; LG-AI/LG-PERFORMANCE BLOCKED. |
| Realtime Azure deployment | Working selected `gpt-realtime-2.1` deployment and authorized real audio route. | GJ-02 and device/interrupt/network/quota cases on hardware. | **USER-DEFERRED**; LG-VOICE/LG-AUDIO BLOCKED. |
| Dictation Azure deployment | Working selected `gpt-live-transcribe` deployment and actual audio transcription route. | GJ-03 including final transcript, duplicate handling and target-safe insertion. | **USER-DEFERRED**; LG-DICTATION/LG-AUDIO BLOCKED. |
| Azure backend/data environment | Container Apps, PostgreSQL 17, Blob, Key Vault, managed identity, Monitor, network/DNS and backup choices. | Authenticated HTTPS/SSE/WebSocket sessions, scale/drain/reconnect, database migrations/restore, managed-identity secret access and redacted telemetry. | Not provisioned by docs; LG-SECURITY/LG-RECOVERY/live gates BLOCKED. |
| Entra External ID | Approved tenant, native client registration, authorized redirect URIs, issuer/audience, system-browser PKCE setup and test identities. | Success/cancel/replay/mismatch, session refresh, device revoke, cross-account denial on real native callback. | MISSING/UNVERIFIED; LG-IDENTITY BLOCKED. |
| Commercial plan approval | Operator-approved catalog/version, prices in integer minor units with currency, included allowances, reservation rules, refunds/cancellation/tax/legal treatment and production entitlement mapping. | Human commercial approval plus server validation and displayed/charged/ledger consistency. Proposed names Nest, Studio, Constellation are not approved products. | **UNAPPROVED OPERATOR CONFIGURATION**; LG-BILLING and paid Checkout BLOCKED. |
| Stripe accounts/products/prices | Authorized test/live accounts, actual Product/Price IDs, webhook signing secret, Checkout/Portal return URLs and entitlements. | Signed/idempotent webhook replay/order, test-mode lifecycle and explicitly authorized limited production-path verification. No real charge without authorization. | MISSING/UNVERIFIED; LG-BILLING BLOCKED. |
| Built-in connection registrations | Registrations for the canonical Google Workspace, Notion, Slack, Linear and Spotify catalog; applicable native Notes/Calendar/Reminders grants; OAuth clients/redirects/scopes, test identities and provider approval where required. | Per-connector documented real read/supported approved write, OAuth refresh or native-grant revalidation, revoke/disconnect, auth scope and account isolation. | MISSING/UNVERIFIED; LG-CONNECTIONS BLOCKED for every unverified advertised connector. |
| Custom MCP test endpoints/processes | User-authorized remote/local server identities, transport/auth details and executable/argument trust choices. | Controlled safe tool, changed schema, hostile description, timeout, OAuth revocation, SSRF denial and process termination. | MISSING/UNVERIFIED; LG-CONNECTIONS BLOCKED. |
| Browser distribution authority | Chrome and Brave supported versions, extension identity/packaging/distribution method, authenticated native-host allowed origins and signed helper. | Real install/upgrade on clean/existing profiles; selected-tab scope and forged sender rejection. | No extension/helper exists yet; LG-BROWSER BLOCKED. |
| Apple signing/notarization | Developer Program authority, Developer ID signing identity, notarization authorization and approved secure build-key access. | Accepted notarization, signature/hardened runtime/staple, clean Gatekeeper install on both architectures. | MISSING/UNVERIFIED; LG-DISTRIBUTION BLOCKED. |
| Sparkle/release delivery | Authorized update signing key access, trusted public key in app, release channel/feed/artifact hosting and rollback authority. | Real signed update, tamper rejection, download digest, compatible rollback/corrective-release rehearsal. | MISSING/UNVERIFIED; LG-DISTRIBUTION BLOCKED. |
| Domain/public surfaces | Proof of control for selected `heypebbi.com`, DNS/TLS, legal identity/contact and support/privacy/account/download destinations. Selection is not registration or trademark clearance. | Domain/control and HTTPS checks, legal review as appropriate, accessible deployed pages and actual signed download. | UNVERIFIED; LG-WEB/LG-SUPPORT BLOCKED. |
| Privacy/compliance policy | Approved data retention/backups, processor/region choices, diagnostic consent, account deletion handling and contact/rights process. | Published policy matches actual collection, provider agreements, deletion/restore/export and canary tests. | MISSING/UNVERIFIED; LG-PRIVACY BLOCKED. |
| Test hardware and consent | Physical Intel and Apple Silicon Macs supporting the required OS matrix, notched/notchless/mixed displays, USB/Bluetooth devices, real TCC/AX/capture consent and dedicated test resources. | Complete TESTING.md matrix, VoiceOver, Spaces, audio route recovery and signed clean/upgrade install. | Evidence absent; hardware portions of gates BLOCKED until supplied and tested. |
| Operations/support authority | Named release/incident/security/privacy/billing contacts, authorized diagnostic storage/access, support channel and alert delivery. | Incident/rollback/support/privacy-request exercises with redacted evidence and exact-target readback. | MISSING/UNVERIFIED; LG-SUPPORT and operational sign-off BLOCKED. |

## Operator configuration, not invented commercial policy

No price, trial length, included usage amount, subscription term, discount, guarantee or production allowance is approved in this repository. A later implementation must consume a versioned server-authoritative plan configuration. Missing or invalid commercial fields disable paid Checkout and display an honest unavailable state; they do not fall back to hardcoded sample prices. Development test fixtures must contain conspicuous test labels and never reach the production account/catalog.

Validation must include actual Stripe IDs/account mode, currency consistency, integer amounts, entitlement version, reservation/finalization behavior, webhook authentication and operator approval evidence. A fixture named Nest does not create a Nest subscription. Secret availability alone never authorizes a purchase or resource creation.

## How a later build agent proceeds without repeated interruption

1. Read the register and inspect only authorized non-secret metadata/configuration references. Do not scrape local audit logs for keys/private endpoints.
2. Implement all independent native/backend/contracts, typed/local paths, adapters and automated negative tests. Keep unavailable capabilities explicitly disconnected.
3. Record a blocker once with affected PB/LG IDs, exact missing input, secure handoff route, owner and the unblocked work still possible. USER-DEFERRED voice inputs stay deferred until the user reopens them.
4. Do not deploy paid resources, create production Stripe products, register domains, issue certificates, grant OS permissions or change cloud settings merely because one-prompt autonomy is requested.
5. When an input is later supplied, verify actual operation and negative behavior, update the scoped evidence and invalidate/re-run affected gates. A successful call does not by itself promote the whole release.
6. End with implemented/tested versus blocked work separated. Never report a fake live success or provisioned service to make the output look complete.

The durable input record stores non-secret references, authorization scope, owner, verification result/time, configuration revision and invalidation conditions. Secret values belong only in Keychain, Key Vault or the specifically authorized secure delivery mechanism—not Markdown, coverage JSON, screenshots, terminal output or support tickets.
