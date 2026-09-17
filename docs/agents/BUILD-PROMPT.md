# One-prompt complete Pebbi build

This is the kickoff instruction for a **future authorized implementation run**. The repository currently contains specifications, not a working app. The owner requested documentation first. Merely reading this file does not start a build.

## Paste this instruction into your coding agent

> Build the complete Pebbi product specified in this repository. This is an implementation request, not a planning request. Read and follow `AGENTS.md`, `docs/CONTRACT.md`, the complete documentation index at `docs/README.md`, and all normative subsystem documents before modifying that subsystem. The app is Pebbi, the project is HeyPebbi, and the selected domain is heypebbi.com. Build every PB-001 through PB-040 requirement; do not reduce the product to a demo, chat window, voice toy, frontend mockup or older Clicky snapshot. Use the original Pebbi visual identity, not minimalism. Continue all unblocked work through implementation, integration, testing, independent review and repair without asking for routine decisions already settled by these documents. Use specialist agents and project skills where supported. Keep required approvals and external-input gates intact. Finish with real execution evidence and an honest release status.

The sections below are part of that same instruction.

## Product to deliver

A native SwiftUI/AppKit macOS app with expressive ceramic-pebble characters, a compact top-edge perch, ordinary Home window and menu-bar fallback; real voice conversation and typed equivalent; explicit screen understanding and drawing; reliable dictation into other applications; persistent Pebbis with jobs, memory, chats and files; resumable tasks, concurrent work and follow-ups; approved native/browser automation; document and web research; built-in and custom MCP connections; source-grounded suggestions; local routines; notifications, account/billing/privacy controls; signing, updates and support surfaces.

The visual references are [brand board](../design/brand-board.html), [brand rules](../design/BRAND.md), [screens](../design/SCREENS.md), and [root token source](../../DESIGN.md). Rich material and character are required. Preserve desktop utility: content density, keyboard operation, VoiceOver and legible reading areas must not be sacrificed to decorative effects.

The engineering source of truth is [architecture](../engineering/ARCHITECTURE.md), [native behavior](../engineering/NATIVE-MACOS.md), [agent runtime](../engineering/AGENT-RUNTIME.md), [API](../engineering/API.md), [data](../engineering/DATA-MODEL.md), [tool contracts](../engineering/TOOLS.md), and [security](../engineering/SECURITY.md). Use the documented stack instead of substituting an easier web wrapper.

## Autonomous operating procedure

Inspect actual source and environment. If application code already exists, preserve it, compare it against every requirement, and complete gaps rather than overwriting it with a starter. If only docs exist, create the documented source structure and working build/test commands. Identify the actual macOS SDK, toolchain and service credentials without printing secrets.

Read the complete PB roster and create `.pebbi-build/state.json` from [the template](build-state.template.json) only if no ledger exists. On continuation, preserve the existing ledger and revalidate its evidence; never reset completed work by copying the template over it. This ledger is local execution state, not product runtime storage. Each requirement needs implementation paths, tests, evidence and a status. Do not mark a requirement verified because a child says so or because its source file exists.

Use a dependency-aware work queue, not a calendar roadmap. Resolve shared contract shapes first; assign bounded, disjoint subsystem ownership next. Implement vertical user journeys fully, including denied permissions, network failure, cancellation and focus restoration. Keep the whole product in scope throughout. Do not present numbered rollout stages, time estimates, or requests for approval of minor design choices.

If delegation is available, use [the specialist allocation](ORCHESTRATION.md). Each child gets the current contracts and relevant PB IDs, not assumed shared memory. The coordinator owns integration and checks every returned artifact. Avoid concurrent edits to common schemas, enums, build files and design tokens.

After implementing a behavior, run its smallest meaningful check and the affected integration path. Repair root causes rather than weakening tests. Run the overall acceptance matrix repeatedly as integrations converge. Verify the actual desktop surfaces and audio/device behavior on a real Mac runner; a Linux-only build session may implement and unit-test portable code but cannot honestly certify macOS GUI behavior.

## Implementation constraints

- The app must run without Hermes, Claude Code, Codex CLI or a personal AI subscription installed. Those may help build it; they are not the product runtime.
- Implement actual provider transports, identity, persistence, browser bridge, tools, metering and billing according to the wire contracts. A click handler that does nothing, a fake progress animation, a hardcoded transcript or a success-shaped stub does not count.
- Add deterministic fixture transports for tests and explicitly marked design previews. They must not be enabled automatically in a production build or presented as live data.
- Treat model output and external content as untrusted. The policy engine enforces tool scope, approvals, path/host restrictions, idempotency and cancellation outside the prompt.
- Keep Azure secrets server-side, local connector secrets in Keychain, and personal content out of logs. Use real authentication and account isolation even in the smallest working backend.
- Use truthful provider-unavailable states; preserve a typed non-voice path where the requirements allow it. Do not quietly switch the locked model or call a different transport equivalent without verification.
- Screen/audio capture is explicit and visible. Protect focused targets before dictation or automation. Cancellation of a task is not merely cancelling its speech.
- Routines run only while Pebbi is open. App quit and device sleep behavior must match the product contract; do not imply always-on cloud execution.
- Persist before risky side effects, reconcile uncertain results after interruption and never automatically replay an ambiguous outbound action.
- No copied HeyClicky assets or proprietary private source. If MIT source is deliberately reused later, preserve its notices and inventory the reused files.

## External prerequisites and interruption policy

Consult [EXTERNAL-INPUTS.md](../operations/EXTERNAL-INPUTS.md) before live checks. The known Azure audio deployment failures were deferred by the owner. The repo contains no tenant credentials or signing identity.

Continue implementing and verifying all work that does not depend on a missing input. Maintain a precise blocker record naming the affected requirement, failing live operation, observed error, required owner action and next verification command. Batch unavoidable questions instead of repeatedly interrupting for each missing setting.

Do not provision paid Azure resources, activate real Stripe prices, publish a production domain, create signing credentials, grant TCC access, alter an existing user's AI routing, or perform destructive production operations without the appropriate authorization. User approvals inside the finished app remain a required feature; they cannot be removed to satisfy the development instruction to work continuously.

When inputs become available, run real integration tests with bounded costs and record results. Do not claim deployment access from a catalog, a successful WebSocket handshake, or an accepted transcription configuration. Require actual audio/transcript output. Do not weaken certificate, auth, sandbox, signature or permission controls when an integration fails.

## Deliverables and completion standard

Deliver the native app, authenticated backend, required browser extension/helper, public support/account/download surfaces, migrations, infrastructure definitions, locked dependencies, test suites, configuration templates without secrets, packaging/update artifacts and maintained documentation. The intended locations belong to the architecture doc; update the docs if an explicit approved decision changes them.

Every PB requirement must have implemented normal and failure behavior, and a recorded acceptance outcome. Required tests that cannot run remain `blocked` or `notRun`, never passed. Separate **implementation complete** from **release ready**. A developer-run unsigned app can prove local behavior but cannot satisfy notarized distribution. A mocked service can prove local control flow but cannot satisfy a live provider gate.

Before concluding, run documentation/schema checks, native builds, app/backend/browser tests, security review, accessibility and supported-device checks, identity/billing checks, real Azure voice/dictation/agent calls, and signing/update validation to the extent authorized and available. See [acceptance](../quality/ACCEPTANCE.md), [testing](../quality/TESTING.md) and [release](../operations/RELEASE.md) for exact gates.

Keep the repository private. Commit coherent verified work when repository writes are authorized. Never upload secrets, private captures, raw user transcripts or signing material.

## Final response from the implementation agent

Report only: what actually exists; where to launch/download it; exact commands/checks run and outcomes; remaining failed/blocked requirements; signing/deployment status; and the next concrete action for any real external blocker. Attach logs/artifacts without secrets. Do not give a triumphant completion statement for a partial app.

If context or process limits force a handoff, checkpoint state and resume instructions so a new agent can continue from the same single build brief. Do not fabricate ongoing background execution or claim unlimited unattended operation.
