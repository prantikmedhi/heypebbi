# Release authority and launch gates

> **HISTORICAL REFERENCE — SUPERSEDED SCOPE.** The current decision is [local Azure onboarding](../product/LOCAL-AZURE-ONBOARDING.md), docs only until implementation is resumed. This earlier managed/full-product design is preserved as reference, not an instruction to implement its hosted services, login, billing, fixed models or full PB scope. Current requirements take precedence.

Current state: **DOCUMENTATION_ONLY; RELEASE BLOCKED**. No app/backend has been implemented, built, signed, notarized, deployed or accepted by this documentation work. Tests described here are future obligations. [CONTRACT](../CONTRACT.md) fixes the product and stack; [ACCEPTANCE](../quality/ACCEPTANCE.md), [TESTING](../quality/TESTING.md) and [coverage.json](../quality/coverage.json) define evidence.

Release readiness is a durable state of an exact artifact/configuration set, not a calendar roadmap. No numbered phases, date targets or elapsed time can make a gate pass. A later build agent carries every unblocked implementation task through actual execution/review and records external blockers without disabling security or dropping requirements.

## Release record and allowed decisions

Maintain one immutable release-candidate record containing:

- Candidate ID, app version/build, source revision, universal artifact digest, bundle ID `com.heypebbi.app`, minimum OS, selected Xcode/Swift toolchain and dependency lock/SBOM revisions.
- Backend revision, Node 24/Fastify 5/PostgreSQL 17 compatibility, database migration set, public API compatibility range, capability/model routing revision and approved operator configuration revision. Secrets and private endpoints are not values in this record.
- Browser extension/native-host version and Chrome/Brave compatibility; Sparkle 2 version/feed channel and signing-key identity reference, never a private key.
- Local schema read/write compatibility, supported upgrade origins, rollback/corrective-release artifact and rehearsed recovery evidence.
- Every PB case, shared journey/failure injection and LG gate result with class, evidence reference, exact OS/architecture/device, named observer/reviewer and timestamp. Gate results are NOT_RUN, PASS, FAIL or BLOCKED.
- External-input status, residual issues with severity, release owner, security/privacy/operations reviewers and explicit decision: BLOCKED, INTERNAL_TEST_ONLY or APPROVED_FOR_RELEASE. INTERNAL_TEST_ONLY is never public production readiness and must not expose fixture successes as real features.

Default is BLOCKED. Any FAIL, BLOCKED or NOT_RUN required gate prevents public release. No weighted score, majority vote or coverage percentage replaces the conjunction of required evidence. Security, privacy, app integrity, missing selected providers and required hardware cannot be waived by a product owner. A supported feature cannot be silently removed to change a blocking gate to not applicable.

## Launch-gate ledger

All gates below start **NOT_RUN**, except live/external-input-dependent portions are **BLOCKED**. No PASS is asserted by this file. Owners are roles to assign, not fictitious named employees.

| Gate | Required evidence | Classes | Accountable owner / present blocker |
| --- | --- | --- | --- |
| LG-DOCS | Canonical PB-001–040 coverage, exact titles/paths, complete positive/negative cases, link/schema validation and no implementation claims or secrets. | automated, manual | Build owner; parent documentation validation must record actual output. This gate alone never certifies the app. |
| LG-AUTOMATED | Actual native/backend/extension test suites, fresh/upgrade migrations, contract/property/race/negative tests and CI artifact logs against candidate, including all [integration-repair fixtures](../quality/TESTING.md#integration-repair-contract-fixtures) and their readback/dispatch oracles. No skipped safety tests or empty passing suites. | automated | Engineering; no implementation exists. |
| LG-SECURITY | Independent threat/code review, authorization/SSRF/path/injection/secret scans, Keychain/managed identity, abuse limits, token/webhook/native-host authenticity, protected-action approvals and supply-chain/SBOM review. | automated, manual, live | Security; review and deployed boundaries not yet verified. |
| LG-NATIVE | Native Swift 6/SwiftUI/AppKit application, macOS 14.2+ availability guards, arm64/x86_64 artifacts and physical Intel/Apple Silicon matrix; notchless/notched/mixed displays/fullscreen Spaces, TCC and foreground takeover. | automated, manual, hardware | Native lead; actual binaries and physical evidence absent. |
| LG-IDENTITY | Entra External ID real tenant/app/redirect/PKCE and server-verifiable recent interactive authentication, two devices, device bearer/credential binding, revocation threshold and re-enrollment/lost-response recovery without secret replay, refresh/sign-out, cross-account denial and production system-browser callback (TC-REPAIR-DEVICE). | automated, manual, live | Identity operator; actual approved identity inputs and usable Entra step-up/recent-interactive-authentication assertion required; do not weaken device binding when unavailable. |
| LG-AI | `gpt-6-astra` through the actual authenticated Pebbi backend; authorized Responses/tool use, screen/file context, streaming, refusal/failure paths, metering and latency. | automated, manual, live | AI operator; limited Astra audit is working evidence only for its audited path, not this gate. |
| LG-VOICE | Actual `gpt-realtime-2.1` bidirectional audio, interruption, provider/session authentication, quota and private-route behavior on real Macs. | automated, manual, live, hardware | AI operator; Azure deployment is **USER-DEFERRED; BLOCKED**. |
| LG-DICTATION | Actual `gpt-live-transcribe` audio transcription plus review/target-safe insertion, device loss, duplicated events and secure-field refusal. | automated, manual, live, hardware | AI/native operators; Azure deployment is **USER-DEFERRED; BLOCKED**. |
| LG-CONNECTIONS | Every advertised built-in connector's documented scopes, applicable OAuth/native grants, reads and supported approved writes, refresh/revalidation/revoke plus remote/local MCP, hostile schema and process-lifecycle evidence. | automated, manual, live | Integrations; provider registrations/test identities/support inventory required. |
| LG-BROWSER | Real Chrome and Brave MV3 install/upgrade, selected tab/dedicated window, authenticated native host, stale-origin/tab refusal, no normal-profile debug port, packaged signed helper. | automated, manual, live, hardware | Browser/native leads; packages and browser evidence absent. |
| LG-SCHEDULER | Local routines only while app open; approved occurrence scope, virtual DST/clock tests, physical sleep/wake/Quit, one catch-up maximum and uncertain-effect reconciliation. | automated, manual, hardware | Runtime lead; physical/local implementation evidence absent. |
| LG-RECOVERY | Network/crash/duplicate/queue/memory-pressure/partial-effect injection, durable journal, store recovery and no replay of uncertain external writes. | automated, manual, live, hardware | Runtime/operations; actual durable runtime and controlled external readbacks absent. |
| LG-AUDIO | Built-in/USB/Bluetooth devices, route/profile change, call interruption, sleep, mic recovery, private-output safeguards and live voice/dictation. | automated, manual, live, hardware | Native lead; hardware and user-deferred voice inputs required. |
| LG-ACCESSIBILITY | VoiceOver and keyboard essential journeys, focus/order/announcements, contrast across real materials/states, Reduce Motion/Transparency/Increase Contrast and native text adaptation. | automated, manual, hardware | Accessibility/design reviewers; interactive product evidence absent. |
| LG-PERFORMANCE | TESTING.md resource/latency targets, physical Intel/Apple Silicon traces, bounded queues/output/logs, idle capture/CPU/memory and live-provider timing distributions. | automated, manual, live, hardware | Performance lead; no measurements exist. |
| LG-BILLING | Approved prices/allowances/entitlements and Stripe IDs; test-mode lifecycle/idempotency; authorized limited production-path verification, server-only metering and webhook reconciliation. | automated, manual, live | Billing operator; pricing is deliberately **UNAPPROVED OPERATOR CONFIGURATION**. No invented subscriptions or amounts. |
| LG-PRIVACY | Approved published retention/subprocessors, payload/log canaries, optional telemetry consent, account/local export separation, deletion/tombstones/backup restoration and retention sweep evidence. | automated, manual, live, hardware | Privacy/security; policy approval and real data-path verification required. |
| LG-DISTRIBUTION | Developer ID/hardened runtime, notarization acceptance and staple, signed DMG/Sparkle feed, clean Gatekeeper installs, update/tamper rejection and rehearsed compatible rollback/corrective release. | automated, manual, live, hardware | Release operator; signing authority, delivery endpoints and hardware evidence required. |
| LG-WEB | Actual HTTPS support/privacy/account/download pages, domain/control proof, keyboard accessibility, correct signed artifact, auth-protected account actions and approved commercial copy. | automated, manual, live | Web/operations; domain selection/brand board is not deployment evidence. |
| LG-SUPPORT | Support ownership/channel, redacted diagnostics/incident correlation, privacy request routing, outage notices and on-call/rollback exercise with real test incidents. | automated, manual, live | Operations; actual support endpoints/roster/runbooks must be exercised. |

## Candidate integrity and packaging procedure

This is a later authorized release procedure, not provisioning authorization now.

1. Freeze candidate source/dependency/configuration revisions. Select and record a stable Xcode/Swift toolchain that actually supports Swift 6 language mode and the macOS 14.2 deployment target. Verify newer SDK APIs have runtime availability guards. Do not invent installed versions.
2. Build and test native arm64 and x86_64 release slices; produce the universal application and record both slice architectures. A Rosetta run is supplemental evidence, never physical Intel certification. Review entitlements and hardened runtime exceptions; each exception needs a justified, tested boundary.
3. Verify owned helper and native-messaging binaries, extension manifests and process lifecycle. The app cannot depend on Hermes or a paid Claude/Codex desktop/CLI subscription. No daemon may continue routines after Quit.
4. Run tests and independent security/code review on the exact release diff. Verify locked dependencies, licenses and generated artifact provenance. No Apple system fonts are bundled; license any shipped display/web font and original assets appropriately.
5. Sign with authorized Developer ID and hardened runtime; notarize and wait for accepted status. Staple applicable artifacts and verify the stapled DMG/application. Record digests, public certificate identity/team and sanitized acceptance receipt. Submission alone is not acceptance.
6. Verify actual delivered bytes under normal Gatekeeper/quarantine in clean standard-user sessions. Read bundle identity/minimum OS and verify signatures recursively without hiding invalid components. Typical later evidence commands include `codesign --verify --strict --verbose=2 <App.app>`, `spctl --assess --type execute --verbose=2 <App.app>` and `xcrun stapler validate <artifact>`; placeholders are not runnable verification and no output is claimed here. Do not disable Gatekeeper or TCC to force a pass.
7. Publish only to an authorized isolated candidate channel first. Sign Sparkle 2 update metadata/artifacts using the configured key procedure, preserve TLS and bind updates to the correct bundle/channel. Keep signing material out of source, logs, build artifacts and client configuration.
8. Perform GJ-09 including fresh install, upgrade, tamper rejection and rollback/corrective-release drill from the actual endpoint. Validate frontend download labels against artifact metadata and digest. Do not advertise a release whose gate manifest is blocked.
9. Make one complete-product public-release authorization only after the entire gate ledger passes. Isolated pre-release candidate verification is not a public rollout stage. After release, continuously monitor error, rollback, usage and privacy indicators against the approved budgets; withdraw distribution or ship a verified corrective release when required. No staged public-cohort promotion or approval of progressively wider exposure is required.

## Backend, schema and configuration compatibility

Use additive, backward-compatible API and schema changes while supported app builds exist. Backend capabilities must truthfully report disconnected/unavailable models and never infer deployment from public catalog metadata. Keep signed releases compatible with the deployed gateway and operator configuration version. Validate long SSE/WebSocket lifetimes and drain behavior on Azure Container Apps; a health response is not a long-session test.

Before a local migration, create a verified recoverable checkpoint and record schema compatibility. Do not destructively migrate away the only recovery route. Backend migrations require validated restore and compatibility evidence in an isolated authorized environment. Keep deletion tombstones and task/effect high-water marks across recovery. Configuration changes to prices/allowances/model routes are reviewed artifacts with explicit versions and authorization; a production secret being present is not pricing approval.

## Rollback and corrective-release runbook

**Triggers:** update failure, launch regression, data corruption, repeated crash, broken critical permission/audio/browser path, billing/authorization defect or privacy exposure. Security/privacy/data-integrity triggers immediately stop distribution and affected execution; they do not wait for a performance threshold.

1. Identify impacted app/backend/configuration versions and preserve sanitized logs/evidence. Withdraw the faulty candidate from further offers and distribution. Do not delete evidence or pretend already-downloaded copies were recalled.
2. Disable only the affected cloud capability through server-side authorization/capability controls where safe; show a specific unavailable message. This cannot remotely erase local state or bypass consent. Revoke compromised credentials/signing authority using its approved incident process if required.
3. Prefer a **higher-version signed corrective release** compatible with current local schema, because arbitrary downgrades can be blocked by Sparkle and can corrupt newer stores. A lower-version rollback is allowed only if the updater's supported secure behavior, signed metadata, version policy and schema compatibility were explicitly rehearsed; never weaken downgrade/signature protections.
4. For backend rollback, ensure the old binary supports the current schema and active app API range before switching. Do not reverse a destructive migration or publish old commercial entitlements by accident. Drain/reconnect long-lived sessions and reconcile usage reservations.
5. For local recovery, preserve the task journal, deletion tombstones, ownership and external-effect reconciliation checkpoints. Never restore an old database and automatically replay writes made since the checkpoint. If compatibility is unknown, stop affected work in a readable recovery mode and require inspected reconciliation.
6. Re-run affected GJ-09, crash/duplicate/migration tests and identity/billing checks, then re-download actual bytes and verify integrity. Record exact target readbacks. Notify users of impact, workaround and recovery without exposing customer data.
7. Close the incident only after forward/rollback safety, stable observations and the revised gate ledger are independently reviewed. Repair the root cause and tests; do not mark the withdrawn candidate passed retroactively.

## Evidence invalidation and final sign-off

- Native/entitlement/toolchain changes invalidate installation, native, accessibility, performance and relevant permission/audio/browser gates.
- Provider/model/deployment/protocol changes invalidate the corresponding live role, quota/latency and affected golden journeys. Astra's prior audit does not survive arbitrary routing changes as production evidence.
- Identity, metering, Stripe configuration or pricing changes invalidate identity/billing/security journeys as applicable.
- Schema/event/queue/tool changes invalidate migrations, recovery, duplicate-effect, memory and workspace tests.
- Privacy/retention/logging/export changes invalidate redaction, deletion, support and published policy review.
- Signing, feed, extension/helper or artifact changes invalidate delivered-artifact/distribution gates even if source code is unchanged.

Final sign-off requires engineering, security/privacy, native/accessibility and release/operations review plus verified operator commercial inputs. Record actual reviewers; unassigned roles keep their approval BLOCKED. The release report lists delivered artifacts and exact PASS/FAIL/NOT_RUN/BLOCKED evidence. It must never convert documentation validation into a claim that the app exists.
