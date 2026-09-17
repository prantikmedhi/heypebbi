# Billing, entitlements and trusted usage

Status: implementation specification; no live prices, Stripe products, paid allowances or provisioning have been approved or created. [CONTRACT](../CONTRACT.md) fixes Stripe hosted Checkout/Customer Portal, the three proposed plan names and server-authoritative usage. [API](API.md) / [openapi.json](openapi.json) define exact paths and payloads.

## Plans and operator gates

Plan names are **Nest**, **Studio**, **Constellation**. Names do not imply a free tier, currency, billing amount, seat count, token allowance, trial, overage policy or promised discount. Production amounts and allowances must be explicitly operator-configured. Do not copy a competitor's prices or promote development fixtures to live configuration.

Each enabled plan needs an approved Stripe product/price mapping, billing interval, integer minor-unit amount, ISO currency, usage allowances, entitlement rules, tax/refund/cancellation disclosures, jurisdiction-specific financial retention and live/test mode. The present public plan schema exposes one configured price/interval per plan. Checkout accepts only that published interval. Supporting more intervals requires an intentional schema update, not an undocumented hidden price.

Until configured, `/v1/billing/plans` returns the three names with `configured:false`, `checkoutEnabled:false`, `price:null`, `allowance:null`, and `billingConfigured:false`. Entitlement is `unconfigured`; do not silently authorize unlimited model usage or call it a free plan. Local editing, previously saved material and sign-in remain available. Controlled developer tests can use explicit test-mode allowances, never production entitlements or acceptance evidence.

## Ownership and source of truth

PostgreSQL stores account-to-Stripe-customer mapping, canonical subscription snapshot, versioned entitlement projection, reservation/ledger records, outbound idempotency records and webhook inbox. User email is not a Stripe-customer authorization key. Provider IDs are opaque strings and never repaired. Clients can display estimates but cannot create a ledger debit/credit, report authoritative audio duration, select a Stripe customer, submit a price ID/amount or unlock entitlements from a redirect.

Use separate identities for the public app API, internal metering and billing worker. Stripe secret and webhook-signing secret are distinct Key Vault entries; neither ships in the app. Stripe test and live objects are isolated by configuration/storage namespace, and mismatched `livemode` events fail closed. Logs contain safe event IDs/status only, never card data, raw request bodies or signed URLs.

## Reservation and debit algorithm

`UsageQuantity` has four nonnegative integer dimensions: `inputTokens`, `outputTokens`, `audioInputMilliseconds`, `audioOutputMilliseconds`. These are quantities, not currency; plan allowances and conversion policy are versioned separately. Token and audio pricing must not be guessed from model names. No floating-point currency arithmetic.

1. Native checks ready role capability and obtains a reservation via `POST /v1/usage/reservations` with task/attempt/role and `requestedCeiling`. These are requested maximums only. Server validates compatible dimensions (`reasoning`: token dimensions, audio dimensions zero; `dictation`: audio-input only unless a separately verified measured billing dimension is explicitly configured; `conversation`: configured audio input/output dimensions), clamps to service/plan/provider budgets and rejects an unusable ceiling.
2. Under an account/period transaction lock or equivalent serializable constraint, compute `remaining = max(allowance - consumed - held, 0)` per dimension. Include every simultaneous reservation, not just completed ledger entries. Verify account/device, entitlement version and provider capability, then insert one reservation and hold its ceiling atomically. Do not perform the Azure request inside a long DB transaction.
3. Unused reservation expires after 60 seconds. Before dispatch, atomically transition reservation from `reserved` to `active`, bind exactly one provider operation/session and recheck role/account/device/task/attempt/entitlement. A reservation cannot authorize two concurrent generations or be repurposed between roles.
4. Bound input and output against the reserved ceiling before and during dispatch. For reasoning use the verified tokenizer or a conservative documented bound plus enforced output ceiling. For PCM meter accepted samples using negotiated sample rate/channel/bit depth; fractional milliseconds round upward for reservation safety. Client timestamps, chunk counts and bytes offered but not accepted are not billing evidence. Capture provider operation ID and trusted receipt when available.
5. Stop input/output before exhausting a ceiling; cancellation stops further work but does not erase already consumed usage. Work may consume upstream resources after cancellation propagation, so reserve a documented conservative overhead inside the ceiling. If the provider cannot enforce a strict ceiling, the operator bears any verified overrun; do not silently charge the user beyond the approved hold or enable uncapped overages.
6. Trusted worker finalizes with immutable evidence and a stable metering event ID. In one DB transaction insert the unique ledger debit, release unused hold and mark `finalized`; return the same result for matching duplicate finalization. A retry does not create another debit. Failed validation before provider dispatch releases the entire hold and emits no usage debit.
7. On crash, missing receipt or uncertain delivery move to `reconciling`. Reconcile provider evidence / gateway acceptance counters before settlement. An unused undispatched expired reservation becomes `expired` and releases its hold; a deliberately abandoned undispatched request becomes `released`. Never let a timer release an active operation as though it cost zero.

Reservation states are billing-record states, not task or connection enums: `reserved`, `active`, `reconciling`, `finalized`, `released`, `expired`. `succeeded`, `failed`, `cancelled` remain task-attempt states only where defined in CONTRACT. Account/period locking and SQL uniqueness are the authority; two app windows/Pebbis cannot overspend through a check-then-insert race.

## Finalization route: workload only

`POST /v1/usage/reservations/{reservationId}/finalize` is an **internal service route**. It is blocked from public ingress and requires a separate verified workload token audience/application role plus explicit service-principal allowlist. A valid app delegated token is rejected with 403 `untrustedMetering`; a client claiming a service name/header is not a workload identity. Do not expose it as a user balance-adjustment API.

`FinalizeRequest` contains `meteringEventId`, `providerOperationId`, `observedUsage`, `measurementSource`, `outcome` and server `completedAt`. Even a trusted caller must match the stored operation/reservation and verify its claimed source against server-held evidence. An app-provided copy of that JSON has no authority. `measurementSource` is `providerReceipt`, `gatewayObservation` or `reconciliation`; it names evidence, not a license to estimate silently.

Database uniqueness covers `(reservationId, providerOperationId)` finalization and `meteringEventId`. `Idempotency-Key` adds HTTP duplicate protection but is not the sole ledger constraint. Duplicate exact evidence returns the original `ledgerEntryId`; conflicting quantities/source/outcome return 409 and enter operator reconciliation without overwriting history. Persist only minimum billing dimensions and identifiers, not audio/transcripts/screens.

The ledger is append-only: debit entries consume quantities, explicit credit entries reference `adjustsLedgerEntryId` and reduce quantities according to a verified adjustment. No in-place negative charge edits. User `GET /v1/usage` is read-only. Operational reconciliation is worker/admin work outside the public app route inventory; do not invent an app “credit” endpoint.

If evidence remains unavailable, keep a bounded reconciliation hold and prevent additional unbounded exposure. Target reconciliation within 24 hours. At that deadline an explicit operator-approved customer-protective policy may release the hold without a debit and record provider cost as operator expense; do not fabricate a zero provider receipt or bill a guessed quantity. The launch configuration must choose this policy and alert on breaches. Missing metering policy prevents chargeable dispatch.

## Checkout and Customer Portal

The native UI shows the configured plan, currency/amount, billing interval, renewal/tax disclosure and allowance before `CheckoutRequest`. Each purchase requires fresh user `allowOnce` intent. `consent.previewId`/`approvedAt` records local preview correlation; the server still derives price, customer, allowed plan/interval and current entitlement itself. Reject stale local previews older than 5 minutes as UX protection, but do not mistake a client timestamp for payment authorization. The hosted Stripe confirmation is the final payment action; an LLM cannot fill payment credentials or approve it.

`POST /v1/billing/checkout`:

- Require authenticated device, configured Stripe mode/product/price and a valid fresh purchase request.
- Atomically create/reuse the account's Stripe-customer mapping, with provider idempotency for both customer creation and Checkout creation. Resolve uncertain customer creation before generating another customer.
- Choose server-side success/cancel destinations from verified HTTPS origin allowlist. The client cannot submit a price ID, amount, customer ID, discount, arbitrary URL or destination domain.
- Reuse the same operation UUID-derived Stripe idempotency key for the same immutable request. Persist intent before sending and reconcile timeouts by provider ID/key before retry. Do not create another paid session because a HTTP response was lost.
- Return hosted `sessionId`, HTTPS `url`, and actual provider expiration when known. Validate returned host belongs to the expected Stripe hosted surface before opening in the system browser; do not redirect secrets through arbitrary URLs.
- A success redirect only says navigation returned. Display confirming state until a verified entitlement update arrives from webhook/reconciliation. Poll existing `/v1/me` or `/v1/usage`, not an invented billing-status endpoint.

`POST /v1/billing/portal` creates a hosted portal for the caller's existing Stripe customer and a fixed verified return URL. No customer ID is accepted from the app. Opening the portal is not consent to a subscription change; the user completes that change in Stripe. Provider expiration may be absent and `expiresAt` is then null rather than invented. Missing Stripe/customer configuration is a clear error, not a fake portal URL.

Only one active subscription per account is supported by this contract. Detect an existing subscription before Checkout; direct the user to Portal for changes or reconcile a pending checkout. Concurrent different idempotency keys do not authorize duplicate subscriptions. Entitlement/price changes are versioned; do not silently mutate an existing reservation's price context.

## Signed webhook inbox and Stripe idempotency

`POST /v1/billing/webhook` accepts Stripe's original event JSON; it does not accept app bearer authentication as proof. Verify `Stripe-Signature` with the configured endpoint signing secret against the **raw byte body**, using the official library and 300-second timestamp tolerance. Clock monitoring is required. Reject missing/invalid signatures and wrong live/test mode before writing entitlement state. A provider delivery retry uses a newly signed timestamp; the original event's creation time is not the signature-age check.

1. Bound raw body to 1 MiB and preserve bytes for verification without body logging. Validate basic event fields only after signature validation. Unknown event types can be acknowledged after safe durable receipt as explicitly ignored; they do not grant access.
2. Insert event ID into a transactional inbox with a unique constraint and minimal safe fields/content needed for immediate processing. Do not retain full webhook payloads beyond processing; store required parsed billing metadata and digest. If persistence fails return 5xx so Stripe retries. If signature fails return 400. Matching duplicate already stored events return 200 `received:true` without another entitlement effect.
3. Process at least once with row leases. Stripe ordering is not guaranteed. For subscription/payment-relevant events retrieve the current relevant Stripe object through trusted server credentials, verify mapped customer/account and allowed product/price/mode, then apply the **current authoritative state**, not the last-arriving historical event.
4. In one transaction write the canonical subscription snapshot, recompute the entitlement projection/version and mark inbox processed. An inbox acknowledgement is durable receipt, not a promise that a payment already succeeded.
5. A worker retry or concurrent event cannot duplicate an allowance grant. Period grant uniqueness is `(accountId, subscriptionId, periodStart, entitlementVersion/policy identity)` with stable business-period identity so a metadata version bump cannot grant the same period twice. Store upgrades/adjustments as explicit deltas keyed to the provider change, not fresh full-period grants.
6. Periodic reconciliation reads current Stripe subscription/payment state for active mappings and unfinished webhook jobs. It repairs missed events without duplicating ledger or grants. Invoice, charge, refund and dispute IDs are opaque foreign references, not app UUIDs.

Handle documented subscription lifecycle, successful/failed invoice payment, checkout completion and applicable refund/dispute events. Pin actual Stripe SDK/API/webhook versions when implementing and test the relevant event schema. Do not treat `checkout.session.completed` alone as evidence a delayed payment settled. Do not grant entitlement on an unverified event body or browser URL query.

Stripe idempotency retention is provider-defined. Pebbi stores its own 24-hour request results and durable business uniqueness constraints; after the provider's replay window, unknown operations require object reconciliation before a new request. Never assume Stripe will dedupe an arbitrarily old key forever. Outbound retries send the exact same parameters; key reuse with changed price/customer is a conflict.

## Entitlement transitions and cancellation

`Subscription.entitlementState` is `unconfigured`, `enabled` or `restricted`, distinct from Stripe's raw subscription statuses. The server mapping is explicit: no approved mapping/config → unconfigured; a currently paid/configured trial status explicitly approved by operator → enabled; unverified payment, revoked/cancelled/expired access or nonapproved status → restricted. Do not automatically enable trialing/past_due/unpaid without an approved policy. Unsupported Stripe states restrict access and alert the operator.

Plan change recomputes future allowances from the verified Stripe state; no refund/credit arithmetic is invented by the native app. Running reserved operations may finish only within their existing ceiling if policy still authorizes them; cancellation/deletion or fraud/security restriction stops work immediately. Remaining quantity cannot become negative; any consumed-over-new-allowance condition prevents new reservations without rewriting history. Period rollover uses server UTC provider period boundaries, never the Mac clock.

Cancellation in the hosted Portal follows the approved policy (at period end or immediate as configured), reflected by `cancelAtPeriodEnd`, `periodStart`/`periodEnd` in `/v1/me`. Account deletion is different: immediately stop new work and queue verified subscription cancellation; do not delete the Stripe mapping before cancellation/reconciliation succeeds. If Stripe is offline, retain minimal deletion-operation billing linkage with restricted access, retry safely and report the unresolved cancellation. Do not promise a refund or cancellation receipt that was not read back.

## Retention and export

Server account export includes usage ledger and entitlement information, not payment card data, Stripe secrets, provider prompts or local chat/file data. Detailed usage retention is at most 90 days, reservation/cursor metadata 30 days, operational idempotency responses 24 hours and dedupe identifiers 90 days. On account deletion remove task/device correlation within 30 days. Minimal mandatory invoice/accounting records use operator-approved jurisdiction-specific retention, disclosed before charging/deletion; missing retention policy is a paid-billing gate. See [SECURITY](SECURITY.md) for backup/export retention.

## Required money-path tests

- Two simultaneous reservations cannot exceed allowance; zero/negative/unsafe integer inputs and role-incompatible dimensions fail before dispatch.
- Native app token cannot finalize, even with a copied internal JSON body. Forged provider operation, client usage counts and conflicting finalization are rejected.
- Duplicate finalizer, duplicate/out-of-order webhook, delayed payment, mode mismatch, signature mismatch, expired signature, corrupted raw bytes, DB failure and worker restart do not duplicate charges/grants or unlock access.
- Checkout/customer creation timeout, different-key concurrent checkouts and reuse with changed price/customer preserve one intended customer/subscription.
- Actual provider usage after cancel settles correctly; lost receipt enters reconciliation, never free unlimited generation or guessed billing. Exhausted quota closes streams gracefully and preserves local drafts.
- Stripe sandbox Checkout → payment event → current object read-back → entitlement update → reservation → metering → usage display → Portal cancellation → account deletion is tested end to end with **test** labels. It proves sandbox integration, not live paid readiness.
- Production Stripe keys/product IDs/tax/retention policy, real Azure metering evidence and operator authorization remain unresolved gates until supplied and verified. Fixtures/schema checks never count as live payment or model passes.

Implementation references: [Stripe webhook signatures](https://docs.stripe.com/webhooks/signature), [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests), [hosted Checkout](https://docs.stripe.com/payments/checkout), [Customer Portal](https://docs.stripe.com/customer-management). Verify current provider behavior and configured versions when implementing.
